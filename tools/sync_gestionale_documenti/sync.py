#!/usr/bin/env python3
"""
Sync allegati gestionale legacy → Supabase (clienti + immobili).
API: dyna_media get_allegati_array + dyna_allegati_cloud.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from env_config import dry_run, storage_state_path, supabase_url  # noqa: E402
from gestionale_allegati import ItemKind, fetch_all, list_client_ids_from_page, list_immobile_ids_from_page  # noqa: E402
from gestionale_auth import open_context  # noqa: E402
from playwright.sync_api import sync_playwright
from supabase_sync import (  # noqa: E402
    append_cliente_doc,
    append_immobile_doc,
    list_clienti_with_legacy,
    list_immobili,
    store_file,
    _ext,
)

LOG = Path(__file__).resolve().parent / ".sync-log.jsonl"
MEDIA_TYPES = {
    "pdf": "application/pdf",
    "doc": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
}


def log(event: dict) -> None:
    line = json.dumps(event, ensure_ascii=False)
    print(line)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def download(context, url: str) -> tuple[bytes, str] | None:
    try:
        resp = context.request.get(
            url,
            timeout=120_000,
            headers={"Referer": "https://pannello.gestionaleimmobiliare.it/"},
        )
        if not resp.ok:
            return None
        body = resp.body()
        if len(body) < 16:
            return None
        ct = resp.headers.get("content-type") or "application/octet-stream"
        return body, ct
    except Exception:
        return None


def sync_files_cliente(context, row: dict, files) -> int:
    lid = row["legacy_id"]
    n = 0
    for f in files:
        got = download(context, f.url_file)
        if not got:
            log({"ok": False, "kind": "cliente", "legacy_id": lid, "file": f.file_name, "error": "download"})
            continue
        data, ct = got
        if ct == "application/octet-stream" and f.file_type in MEDIA_TYPES:
            ct = MEDIA_TYPES[f.file_type]
        safe = re.sub(r"[^\w.\-]+", "_", f.file_name)[:180]
        pub = store_file("documenti", f"migrazione/clienti/{lid}", safe, data, ct)
        tipo = "Planimetria" if f.flag_planimetria else _ext(safe)
        append_cliente_doc(row["id"], row.get("documenti_cliente"), safe, pub, tipo)
        n += 1
        log({"ok": True, "kind": "cliente", "legacy_id": lid, "nome": safe, "dry_run": dry_run()})
    return n


def sync_files_immobile(context, row: dict, legacy_id: str, files) -> int:
    code = (row.get("codice") or legacy_id).strip()
    n = 0
    for f in files:
        got = download(context, f.url_file)
        if not got:
            log({"ok": False, "kind": "immobile", "codice": code, "file": f.file_name, "error": "download"})
            continue
        data, ct = got
        if ct == "application/octet-stream" and f.file_type in MEDIA_TYPES:
            ct = MEDIA_TYPES[f.file_type]
        safe = re.sub(r"[^\w.\-]+", "_", f.file_name)[:180]
        plan = f.flag_planimetria or f.source == "image" and f.file_type in ("jpg", "jpeg", "png")
        bucket = "planimetrie" if plan else "documenti"
        field = "planimetrie" if plan else "documenti"
        pub = store_file(bucket, f"migrazione/immobili/{code}", safe, data, ct)
        tipo = "Planimetria" if plan else _ext(safe)
        append_immobile_doc(row["id"], field, row.get(field), safe, pub, tipo)
        n += 1
        log({"ok": True, "kind": "immobile", "codice": code, "nome": safe, "dry_run": dry_run()})
    return n


def open_session():
    path = storage_state_path()
    if path:
        pw = sync_playwright().start()
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(storage_state=path)
        return pw, browser, ctx
    return open_context()


def cmd_check() -> None:
    import os

    print("SUPABASE_URL", "OK" if os.environ.get("SUPABASE_URL") else "MISSING")
    print("DRY_RUN", dry_run())
    if os.environ.get("SUPABASE_URL") and os.environ.get("SUPABASE_SERVICE_ROLE_KEY"):
        try:
            from supabase_sync import sb

            sb().table("clienti").select("id").limit(1).execute()
            print("Supabase OK (service_role)")
        except Exception as e:
            print("Supabase FAIL", e)
    else:
        print("Supabase SKIP (secret mancanti)")
    path = storage_state_path()
    if not path:
        raise SystemExit("Manca sessione gestionale (storageState.json o GESTIONALE_STORAGE_STATE)")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(storage_state=path)
        page = ctx.new_page()
        page.goto("https://pannello.gestionaleimmobiliare.it/index.html", timeout=120_000)
        if "account_login" in page.url:
            raise SystemExit("Sessione gestionale scaduta — serve nuovo codice 2FA")
        print("Gestionale OK", page.url)
        browser.close()


def cmd_report_sample() -> None:
    from compare_report import main as report_main

    report_main()


def cmd_sync_cliente_legacy(context, legacy_id: str) -> None:
    rows = [r for r in list_clienti_with_legacy(None) if r.get("legacy_id") == legacy_id]
    if not rows:
        log({"ok": False, "error": "no_supabase_row", "legacy_id": legacy_id})
        return
    files = fetch_all(context, "clienti", legacy_id)
    sync_files_cliente(context, rows[0], files)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true", help="Campione confronto legacy vs nuovo")
    ap.add_argument("--clienti", action="store_true")
    ap.add_argument("--immobili", action="store_true")
    ap.add_argument("--legacy-id", help="Sync un solo cliente legacy")
    ap.add_argument("--limit", type=int, default=50)
    args = ap.parse_args()

    if args.check:
        cmd_check()
        return
    if args.report:
        cmd_report_sample()
        return

    pw, browser, ctx = open_session()
    try:
        if args.legacy_id:
            cmd_sync_cliente_legacy(ctx, args.legacy_id)
            return

        if args.clienti:
            rows = list_clienti_with_legacy(args.limit)
            for row in rows:
                lid = row["legacy_id"]
                files = fetch_all(ctx, "clienti", lid)
                if files:
                    sync_files_cliente(ctx, row, files)

        if args.immobili:
            # Mappa codice immobile → id legacy: richiede collegamento; per ora campione da lista legacy
            page = ctx.new_page()
            page.goto(
                "https://pannello.gestionaleimmobiliare.it/immobili.html?sch_incarico=normale&sch_agente=10001",
                timeout=120_000,
            )
            imm_ids = list_immobile_ids_from_page(page.content())[: args.limit]
            page.close()
            by_code = {(r.get("codice") or "").upper(): r for r in list_immobili(None)}
            for iid in imm_ids:
                files = fetch_all(ctx, "immobili", iid)
                if not files:
                    continue
                # TODO: mappa immobile_id legacy → codice LA (campo in DB o indice)
                log({"ok": False, "kind": "immobile", "legacy_imm_id": iid, "error": "mappa_codice_mancante", "files": len(files)})
    finally:
        browser.close()
        if hasattr(pw, "stop"):
            pw.stop()


if __name__ == "__main__":
    main()
