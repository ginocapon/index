# -*- coding: utf-8 -*-
"""Sincronizza corpo HTML articolo statico → Supabase blog.contenuto."""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def extract_art_content(html: str) -> str:
    m = re.search(
        r'<div class="art-container"><div class="art-content">(.*?)</div></div>',
        html,
        re.DOTALL | re.IGNORECASE,
    )
    if not m:
        raise ValueError("art-content non trovato")
    return m.group(1).strip()


def main() -> int:
    from dotenv import load_dotenv
    from supabase import create_client

    slug = "blog-bonus-edilizi-2026-incentivi-casa-padova"
    article_id = "ff2a45fe-8e92-4cf4-9796-4bff142b13fd"
    html_path = ROOT / f"{slug}.html"
    if not html_path.is_file():
        print(f"Manca file: {html_path}", file=sys.stderr)
        return 2

    body = extract_art_content(html_path.read_text(encoding="utf-8"))
    print(f"Corpo estratto: {len(body)} caratteri")

    load_dotenv(ROOT / "righetto_social" / ".env")
    sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
    sb.table("blog").update({"contenuto": body}).eq("id", article_id).execute()
    print(f"OK Supabase aggiornato: {article_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
