#!/usr/bin/env python3
"""Sincronizza URL visita virtuale e virtual_tour_scenes su Supabase da data/visite-virtuali.json."""
from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://righettoimmobiliare.it/visita-virtuale.html"


def main() -> None:
    load_dotenv(ROOT / "righetto_social" / ".env")
    sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
    catalog = json.loads((ROOT / "data" / "visite-virtuali.json").read_text(encoding="utf-8"))

    for slug, tour in catalog.items():
        vt_url = f"{BASE_URL}?slug={slug}&embed=1"
        scenes = [
            {"nome": s["nome"], "url": s["img"], "thumbnail": s["img"]}
            for s in tour.get("scenes", [])
        ]
        sb.table("immobili").update(
            {"virtual_tour": vt_url, "virtual_tour_scenes": scenes}
        ).eq("slug", slug).execute()
        print(f"OK {tour.get('codice', slug)} -> {len(scenes)} stanze")


if __name__ == "__main__":
    main()
