#!/usr/bin/env python3
"""Sposta pianificazioni [MAY27_BATCH] da oggi a domani mattina."""
from __future__ import annotations

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
TZ = ZoneInfo("Europe/Rome")
START = "09:00"
STEP = 20


def add_minutes(hhmm: str, delta: int) -> str:
    h, m = map(int, hhmm.split(":"))
    t = h * 60 + m + delta
    return f"{(t // 60) % 24:02d}:{t % 60:02d}"


def js_weekday(iso: str) -> int:
    d = datetime.strptime(iso[:10], "%Y-%m-%d").date()
    return {6: 0, 0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6}[d.weekday()]


def main() -> int:
    load_dotenv(ROOT / ".env")
    from supabase import create_client

    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_KEY", "").strip()
    if not url or not key:
        print("Manca SUPABASE_URL/KEY", file=sys.stderr)
        return 2

    tomorrow = (datetime.now(tz=TZ).date() + timedelta(days=1)).isoformat()
    client = create_client(url, key)

    rows = (
        client.table("pianificazioni")
        .select("id,ora,titolo,note,contenuto,data_inizio")
        .like("note", "%MAY27_BATCH%")
        .execute()
    ).data or []

    # Solo righe non ancora pubblicate su date passate o oggi
    rows = [r for r in rows if (r.get("data_inizio") or "") <= datetime.now(tz=TZ).date().isoformat()]
    if not rows:
        print("Nessuna pianificazione MAY27_BATCH da spostare.")
        return 0

    rows.sort(key=lambda r: (r.get("data_inizio") or "", r.get("ora") or ""))
    slugs: list[str] = []
    for r in rows:
        note = str(r.get("note") or "")
        if "static:" in note:
            s = note.split("static:")[-1].strip()
            if s not in slugs:
                slugs.append(s)

    slot_by_slug = {s: add_minutes(START, STEP * i) for i, s in enumerate(slugs)}
    now = datetime.now(tz=TZ).isoformat()
    updated = 0
    for r in rows:
        slug = str(r.get("note") or "").split("static:")[-1].strip()
        ora = slot_by_slug.get(slug, START)
        client.table("pianificazioni").update(
            {
                "data_inizio": tomorrow,
                "data_fine": tomorrow,
                "ora": ora,
                "giorni": [js_weekday(tomorrow)],
                "updated_at": now,
            }
        ).eq("id", r["id"]).execute()
        updated += 1
        print(f"{tomorrow} {ora}  {r.get('contenuto')}  {slug}")

    print(f"\nSpostate {updated} righe -> {tomorrow} mattina (primo slot {START})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
