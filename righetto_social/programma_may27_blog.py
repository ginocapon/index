#!/usr/bin/env python3
"""Programma 5 articoli blog 27 maggio 2026 su FB + IG (copy §2b skill)."""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
REG = json.loads((ROOT / "scripts" / "may27_blog_registry.json").read_text(encoding="utf-8"))
TZ = ZoneInfo("Europe/Rome")
BASE = "https://righettoimmobiliare.it"
CHANNELS = ("facebook_post", "instagram_feed")
TAGS = [
    "#Padova",
    "#Immobiliare",
    "#MercatoImmobiliare",
    "#Casa",
    "#RighettoImmobiliare",
    "#Veneto",
    "#Mutui",
    "#Investimento",
    "#Notizie",
    "#Blog",
]


def sb():
    import os
    from dotenv import load_dotenv
    from supabase import create_client

    load_dotenv(Path(__file__).resolve().parent / ".env")
    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_KEY", "").strip()
    if not url or not key:
        print("Manca SUPABASE_URL/KEY", file=sys.stderr)
        sys.exit(2)
    return create_client(url, key)


def js_weekday(iso: str) -> int:
    d = datetime.strptime(iso[:10], "%Y-%m-%d").date()
    return {6: 0, 0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6}[d.weekday()]


def add_minutes(hhmm: str, delta: int) -> str:
    h, m = map(int, hhmm.split(":"))
    t = h * 60 + m + delta
    return f"{(t // 60) % 24:02d}:{t % 60:02d}"


def caption(titolo: str, snippet: str, slug: str) -> str:
    link = f"{BASE}/{slug}"
    tags = " ".join(TAGS)
    return f"{titolo}\n\n{snippet}\n\n{link}\n\n{tags}"


def main() -> int:
    day = "2026-05-28"
    start = "09:00"
    step = 20
    client = sb()
    rows = []
    slot_i = 0
    for art in REG["blog_html_articoliStatici"]:
        titolo = art["titolo"]
        slug = art["url_statico"]
        snippet = art.get("contenuto", "")
        img = art["immagine_copertina"]
        media_url = f"{BASE}/{img}"
        ora = add_minutes(start, step * slot_i)
        slot_i += 1
        for ch in CHANNELS:
            rows.append(
                {
                    "tipo": "blog",
                    "contenuto": ch,
                    "titolo": titolo[:200],
                    "riferimento_id": None,
                    "ora": ora,
                    "giorni": [js_weekday(day)],
                    "data_inizio": day,
                    "data_fine": day,
                    "keywords": TAGS,
                    "note": f"[MAY27_BATCH] static:{slug}",
                    "link_media": f"{BASE}/{slug}",
                    "corpo_spintax": caption(titolo, snippet, slug),
                    "media_direct_url": media_url,
                    "updated_at": datetime.now(tz=TZ).isoformat(),
                    "created_at": datetime.now(tz=TZ).isoformat(),
                }
            )
    res = client.table("pianificazioni").insert(rows).execute()
    n = len(res.data or rows)
    print(f"Inserite {n} pianificazioni ({len(REG['blog_html_articoliStatici'])} articoli × FB+IG) — {day} da {start}")
    for art, t in zip(REG["blog_html_articoliStatici"], [add_minutes(start, step * i) for i in range(5)]):
        print(f"  {t}  {art['url_statico']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
