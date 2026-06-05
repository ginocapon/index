#!/usr/bin/env python3
"""Inserisce in Supabase blog i seed da registry JSON se mancano (match per titolo)."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRIES = [
    ROOT / "scripts" / "giugno03_blog_registry.json",
    ROOT / "scripts" / "may27_blog_registry.json",
]

SUPA_COLS = {
    "titolo",
    "categoria",
    "data",
    "stato",
    "autore",
    "immagine_copertina",
    "contenuto",
    "evidenza",
    "tempo",
    "emoji",
}


def norm_title(t: str) -> str:
    return " ".join((t or "").lower().split())


def seed_to_row(s: dict) -> dict:
    return {
        "titolo": s["titolo"],
        "categoria": s["categoria"],
        "data": s["data"],
        "stato": s.get("stato", "pubblicato"),
        "autore": s.get("autore", "Gino Capon"),
        "immagine_copertina": s.get("immagine_copertina") or None,
        "contenuto": s.get("contenuto") or "",
        "evidenza": bool(s.get("evidenza")),
        "tempo": int(s.get("tempo") or 10),
        "emoji": s.get("emoji") or "🏠",
    }


def main() -> int:
    from dotenv import load_dotenv
    from supabase import create_client

    seeds: list[dict] = []
    for reg_path in REGISTRIES:
        if not reg_path.is_file():
            continue
        reg = json.loads(reg_path.read_text(encoding="utf-8"))
        seeds.extend(reg.get("admin_blogSeedArticles") or [])

    if not seeds:
        print("Nessun seed nei registry.", file=sys.stderr)
        return 2

    load_dotenv(ROOT / "righetto_social" / ".env")
    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_KEY", "").strip()
    if not url or not key:
        print("Manca SUPABASE_URL/KEY", file=sys.stderr)
        return 2

    sb = create_client(url, key)
    existing = (sb.table("blog").select("id,titolo").execute()).data or []
    by_title = {norm_title(str(r.get("titolo") or "")): r for r in existing}

    inserted = 0
    skipped = 0
    for s in seeds:
        title = str(s.get("titolo") or "")
        if not title:
            continue
        if norm_title(title) in by_title:
            skipped += 1
            continue
        row = seed_to_row(s)
        sb.table("blog").insert(row).execute()
        inserted += 1
        slug = s.get("url_statico") or title[:40]
        print(f"+ {slug}")

    print(f"OK: inseriti {inserted}, già presenti {skipped}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
