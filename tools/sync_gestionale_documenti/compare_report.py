#!/usr/bin/env python3
"""Confronto allegati legacy vs nuovo (Supabase + indice archivio quando disponibile)."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from env_config import storage_state_path  # noqa: E402
from gestionale_allegati import fetch_all, list_client_ids_from_page, list_immobile_ids_from_page  # noqa: E402
from playwright.sync_api import sync_playwright

OUT_DIR = Path(__file__).resolve().parent / "reports"


def _has_supabase() -> bool:
    import os

    return bool(os.environ.get("SUPABASE_URL") and os.environ.get("SUPABASE_SERVICE_ROLE_KEY"))


def load_attachment_index() -> dict[str, list[str]]:
    """legacy_id -> file names (da indice Storage, se service_role)."""
    if not _has_supabase():
        return {}
    try:
        from supabase_sync import sb

        obj = "clienti-collegamenti/client-attachments-v1-f78f1f5cc622a0e5.json"
        raw = sb().storage.from_("documenti").download(obj)
        if raw.error or not raw.data:
            return {}
        m = json.loads(raw.data.decode("utf-8"))
        out: dict[str, list[str]] = {}
        for e in m.get("entries") or []:
            lid = str(e.get("legacy_id") or "")
            if lid:
                out[lid] = list(e.get("files") or [])
        return out
    except Exception as ex:
        print("INDICE_ARCHIVIO_SKIP", str(ex)[:120], file=sys.stderr)
        return {}


def supabase_cliente_docs() -> dict[str, dict]:
    if not _has_supabase():
        return {}
    try:
        from supabase_sync import list_clienti_with_legacy

        rows = list_clienti_with_legacy(None)
        return {
            r["legacy_id"]: {
                "id": r["id"],
                "documenti_cliente": r.get("documenti_cliente") or [],
            }
            for r in rows
            if r.get("legacy_id")
        }
    except Exception as ex:
        print("SUPABASE_CLIENTI_SKIP", str(ex)[:120], file=sys.stderr)
        return {}


def supabase_immobili_docs() -> dict[str, dict]:
    if not _has_supabase():
        return {}
    try:
        from supabase_sync import list_immobili

        rows = list_immobili(None)
        out = {}
        for r in rows:
            code = (r.get("codice") or "").strip()
            if not code:
                continue
            out[code] = {
                "id": r["id"],
                "documenti": r.get("documenti") or [],
                "planimetrie": r.get("planimetrie") or [],
            }
        return out
    except Exception as ex:
        print("SUPABASE_IMMOBILI_SKIP", str(ex)[:120], file=sys.stderr)
        return {}


def run(limit_clients: int, limit_imm: int, sample_legacy_clients: int) -> Path:
    state_path = storage_state_path()
    if not state_path:
        raise SystemExit("Manca storageState.json o GESTIONALE_STORAGE_STATE")

    archive = load_attachment_index()
    sb_cli = supabase_cliente_docs()
    sb_imm = supabase_immobili_docs()
    has_sb = bool(sb_cli or sb_imm)

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "supabase_readable": has_sb,
        "archive_legacy_ids": len(archive),
        "clienti_in_supabase_with_legacy": len(sb_cli),
        "clienti": [],
        "immobili": [],
        "summary": {},
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(storage_state=state_path)
        page = ctx.new_page()
        page.goto(
            "https://pannello.gestionaleimmobiliare.it/clienti.html?view_mode=list&sch_agente=10001",
            timeout=120_000,
        )
        client_ids = list_client_ids_from_page(page.content())[:sample_legacy_clients]

        for lid in client_ids:
            files = fetch_all(ctx, "clienti", lid)
            names = [f.file_name for f in files]
            arch = archive.get(lid, [])
            sb_row = sb_cli.get(lid, {})
            doc_json = sb_row.get("documenti_cliente") or []
            report["clienti"].append(
                {
                    "legacy_id": lid,
                    "legacy_file_count": len(files),
                    "legacy_files": names[:20],
                    "archive_github_count": len(arch),
                    "documenti_cliente_count": len(doc_json),
                    "in_supabase": lid in sb_cli,
                }
            )

        page.goto(
            "https://pannello.gestionaleimmobiliare.it/immobili.html?sch_incarico=normale&sch_agente=10001",
            timeout=120_000,
        )
        imm_ids = list_immobile_ids_from_page(page.content())[:limit_imm]
        for iid in imm_ids:
            files = fetch_all(ctx, "immobili", iid)
            report["immobili"].append(
                {
                    "legacy_immobile_id": iid,
                    "legacy_file_count": len(files),
                    "legacy_files": [f.file_name for f in files][:20],
                }
            )
        browser.close()

    lc = report["clienti"]
    report["summary"] = {
        "clienti_campionati": len(lc),
        "clienti_con_allegati_legacy": sum(1 for x in lc if x["legacy_file_count"] > 0),
        "clienti_con_archivio_github": sum(1 for x in lc if x["archive_github_count"] > 0),
        "clienti_con_documenti_cliente": sum(1 for x in lc if x["documenti_cliente_count"] > 0),
        "immobili_campionati": len(report["immobili"]),
        "immobili_con_allegati_legacy": sum(1 for x in report["immobili"] if x["legacy_file_count"] > 0),
    }

    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / f"compare-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M')}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample-clients", type=int, default=25)
    ap.add_argument("--sample-immobili", type=int, default=15)
    args = ap.parse_args()
    path = run(args.sample_clients, args.sample_immobili, args.sample_clients)
    print("REPORT", path)
    data = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps(data["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
