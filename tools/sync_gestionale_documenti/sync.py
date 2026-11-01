#!/usr/bin/env python3
"""
Sync allegati gestionale legacy → Supabase (clienti + immobili).
Secret: vedi README.md (Environment secrets).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

from env_config import dry_run, gestionale_base_url, load_config, supabase_url  # noqa: E402
from gestionale_auth import fetch_page_html, open_context  # noqa: E402
from supabase_sync import (  # noqa: E402
    append_cliente_doc,
    append_immobile_doc,
    list_clienti_with_legacy,
    list_immobili,
    legacy_id_from_note,
    sb,
    store_file,
    _ext,
)

LOG = Path(__file__).resolve().parent / ".sync-log.jsonl"


def log(event: dict) -> None:
    line = json.dumps(event, ensure_ascii=False)
    print(line)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def collect_links(html: str, base: str, selector: str) -> list[tuple[str, str]]:
    """Estrae href + testo visibile (regex leggero, no BeautifulSoup per zero dipendenze extra)."""
    out: list[tuple[str, str]] = []
    for m in re.finditer(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]*)', html, re.I):
        href, label = m.group(1).strip(), re.sub(r"\s+", " ", m.group(2)).strip()
        if not href or href.startswith("#") or href.lower().startswith("javascript:"):
            continue
        full = urljoin(base + "/", href)
        if any(x in full.lower() for x in (".pdf", "download", "allegat", "documento", "file=")):
            name = label or Path(urlparse(full).path).name or "documento"
            out.append((full, name))
    # dedupe by URL
    seen = set()
    deduped = []
    for url, name in out:
        if url in seen:
            continue
        seen.add(url)
        deduped.append((url, name))
    return deduped


def download_url(context, url: str) -> tuple[bytes, str] | None:
    try:
        resp = context.request.get(url, timeout=120_000)
        if not resp.ok:
            return None
        body = resp.body()
        if len(body) < 32:
            return None
        ct = resp.headers.get("content-type", "application/octet-stream")
        return body, ct
    except Exception:
        return None


def is_planimetria(name: str, keywords: list[str]) -> bool:
    n = name.lower()
    return any(k in n for k in keywords)


def sync_cliente(context, cfg: dict, base: str, row: dict) -> int:
    lid = row["legacy_id"]
    tpl = cfg["cliente"]["documents_url"]
    url = base + tpl.format(legacy_id=lid)
    html = fetch_page_html(context, url)
    links = collect_links(html, base, cfg["cliente"].get("link_selector", ""))
    kw = cfg["cliente"].get("section_planimetrie_keywords") or []
    n = 0
    for file_url, name in links:
        got = download_url(context, file_url)
        if not got:
            log({"ok": False, "kind": "cliente", "legacy_id": lid, "url": file_url, "error": "download"})
            continue
        data, ct = got
        safe_name = re.sub(r"[^\w.\-]+", "_", name)[:180]
        if not safe_name.lower().endswith(".pdf") and "pdf" in ct:
            safe_name += ".pdf"
        path_prefix = f"migrazione/clienti/{lid}"
        pub = store_file("documenti", path_prefix, safe_name, data, ct)
        tipo = "Planimetria" if is_planimetria(safe_name, kw) else _ext(safe_name)
        append_cliente_doc(row["id"], row.get("documenti_cliente"), safe_name, pub, tipo)
        n += 1
        log({"ok": True, "kind": "cliente", "legacy_id": lid, "nome": safe_name, "dry_run": dry_run()})
    return n


def sync_immobile(context, cfg: dict, base: str, row: dict) -> int:
    code = (row.get("codice") or "").strip()
    if not code:
        return 0
    tpl = cfg["immobile"]["documents_url"]
    url = base + tpl.format(legacy_codice=code, legacy_id=code)
    html = fetch_page_html(context, url)
    links = collect_links(html, base, cfg["immobile"].get("link_selector", ""))
    kw = ["planimetr"]
    n = 0
    for file_url, name in links:
        got = download_url(context, file_url)
        if not got:
            log({"ok": False, "kind": "immobile", "codice": code, "url": file_url, "error": "download"})
            continue
        data, ct = got
        safe_name = re.sub(r"[^\w.\-]+", "_", name)[:180]
        path_prefix = f"migrazione/immobili/{code}"
        plan = is_planimetria(safe_name, kw)
        bucket = "planimetrie" if plan else "documenti"
        pub = store_file(bucket, path_prefix, safe_name, data, ct)
        field = "planimetrie" if plan else "documenti"
        tipo = "Planimetria" if plan else _ext(safe_name)
        append_immobile_doc(row["id"], field, row.get(field), safe_name, pub, tipo)
        n += 1
        log({"ok": True, "kind": "immobile", "codice": code, "nome": safe_name, "dry_run": dry_run()})
    return n


def cmd_check() -> None:
    print("SUPABASE_URL:", supabase_url())
    print("DRY_RUN:", dry_run())
    sb().table("clienti").select("id").limit(1).execute()
    print("Supabase OK (service_role)")
    with open_context() as (_pw, _br, ctx):
        cfg = load_config()
        base = gestionale_base_url(cfg)
        html = fetch_page_html(ctx, base + "/")
        if len(html) < 200:
            raise SystemExit("Sessione gestionale non valida o pagina vuota")
        print("Gestionale OK (sessione o login)")


def cmd_list(limit: int | None) -> None:
    cl = list_clienti_with_legacy(limit)
    im = list_immobili(limit)
    print(f"Clienti con legacy_id: {len(cl)}")
    print(f"Immobili con codice: {len(im)}")


def cmd_probe_cliente(legacy_id: str) -> None:
    cfg = load_config()
    base = gestionale_base_url(cfg)
    tpl = cfg["cliente"]["documents_url"]
    url = base + tpl.format(legacy_id=legacy_id)
    out = Path("/tmp/gestionale-probe-cliente.html")
    with open_context() as (_pw, _br, ctx):
        html = fetch_page_html(ctx, url)
    out.write_text(html, encoding="utf-8")
    print(f"HTML salvato in {out} — URL: {url}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Sync documenti gestionale → Supabase")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--probe-cliente", metavar="LEGACY_ID")
    ap.add_argument("--clienti", action="store_true")
    ap.add_argument("--immobili", action="store_true")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    if args.check:
        cmd_check()
        return
    if args.list:
        cmd_list(args.limit)
        return
    if args.probe_cliente:
        cmd_probe_cliente(args.probe_cliente)
        return

    if not (args.clienti or args.immobili or args.all):
        ap.print_help()
        sys.exit(1)

    cfg = load_config()
    base = gestionale_base_url(cfg)
    with open_context() as (_pw, _br, ctx):
        if args.clienti or args.all:
            for row in list_clienti_with_legacy(args.limit):
                sync_cliente(ctx, cfg, base, row)
        if args.immobili or args.all:
            for row in list_immobili(args.limit):
                sync_immobile(ctx, cfg, base, row)


if __name__ == "__main__":
    main()
