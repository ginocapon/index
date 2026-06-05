#!/usr/bin/env python3
"""Rimuove righe pianificazioni duplicate (stesso giorno, ora, tipo, riferimento_id)."""
from __future__ import annotations

import os
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUB_OK = "PUB_OK"


def main() -> int:
    from dotenv import load_dotenv
    from supabase import create_client

    load_dotenv(ROOT / "righetto_social" / ".env")
    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_KEY", "").strip()
    if not url or not key:
        print("Manca SUPABASE_URL/KEY", file=sys.stderr)
        return 2

    sb = create_client(url, key)
    rows = (
        sb.table("pianificazioni")
        .select("id,data_inizio,ora,tipo,riferimento_id,note,created_at")
        .execute()
    ).data or []

    groups: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        key_g = (
            str(r.get("data_inizio") or "")[:10],
            str(r.get("ora") or ""),
            str(r.get("tipo") or ""),
            str(r.get("riferimento_id") or ""),
        )
        groups[key_g].append(r)

    to_delete: list[str] = []
    for key_g, items in groups.items():
        if len(items) < 2:
            continue

        def rank(row: dict) -> tuple:
            note = str(row.get("note") or "")
            pub = 0 if PUB_OK in note else 1
            created = str(row.get("created_at") or "")
            return (pub, created, str(row.get("id") or ""))

        items.sort(key=rank)
        keep = items[0]
        for dup in items[1:]:
            dup_id = str(dup.get("id") or "")
            if dup_id and dup_id != str(keep.get("id")):
                to_delete.append(dup_id)

    if not to_delete:
        print("OK: nessun duplicato da rimuovere.")
        return 0

    print(f"Elimino {len(to_delete)} righe duplicate (tengo la migliore per gruppo)...")
    deleted = 0
    for i in range(0, len(to_delete), 50):
        batch = to_delete[i : i + 50]
        sb.table("pianificazioni").delete().in_("id", batch).execute()
        deleted += len(batch)
        print(f"  -{len(batch)}")
    print(f"OK: rimosse {deleted} righe duplicate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
