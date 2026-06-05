"""
Allinea righe esistenti in `pianificazioni` al copy §2b skill-social-automation:
titolo pari pari, link in caption, hashtag in keywords.

Non modifica righe già pubblicate (PUB_OK in note) né notizie RSS.

Uso:
  python aggiorna_agenda_copy.py --dry-run
  python aggiorna_agenda_copy.py
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from supabase import create_client

from genera_bozze_settimanali import (
    _ctx_from_blog,
    _ctx_from_immobile,
    apply_pattern,
    load_templates,
)

ROOT = __import__("pathlib").Path(__file__).resolve().parent
TZ = ZoneInfo("Europe/Rome")
PUB_OK = "| PUB_OK:"


def load_env() -> None:
    load_dotenv(ROOT / ".env")


def sb_client():
    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_KEY", "").strip()
    if not url or not key:
        print("Manca SUPABASE_URL o SUPABASE_KEY", file=sys.stderr)
        sys.exit(2)
    return create_client(url, key)


def slug_tag(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "", (text or "").lower())
    return f"#{s}" if len(s) > 2 else ""


def tags_for_immobile(row: dict, base: list[str]) -> list[str]:
    out = list(base)
    for field in ("comune", "zona", "tipologia", "tipo"):
        t = slug_tag(str(row.get(field) or ""))
        if t and t not in out:
            out.append(t)
    return out[:15]


def tags_for_blog(row: dict, base: list[str]) -> list[str]:
    out = list(base)
    raw = row.get("keywords") or row.get("keyword") or ""
    parts: list[str] = []
    if isinstance(raw, list):
        parts = [str(x).strip() for x in raw if str(x).strip()]
    elif isinstance(raw, str):
        parts = [p.strip() for p in re.split(r"[,;|\n]+", raw) if p.strip()]
    for p in parts:
        t = p if p.startswith("#") else slug_tag(p)
        if t and t not in out:
            out.append(t)
    return out[:15]


def build_copy(
    section: str,
    tpl: dict[str, Any],
    ctx: dict[str, str],
    link: str,
    tags: list[str],
) -> tuple[str, str, list[str]]:
    sec = tpl.get(section) or {}
    titolo = str(ctx.get("titolo") or "Post")[:220]
    corpi = sec.get("corpo_spintax") or [""]
    corpo = apply_pattern(corpi[0], ctx).rstrip()
    if link and link not in corpo:
        corpo += f"\n\n{link}"
    return titolo, corpo, tags


def _safe_print(msg: str) -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    print(msg.encode("ascii", "replace").decode("ascii"), flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--include-pubblicate",
        action="store_true",
        help="Aggiorna anche righe con PUB_OK (sconsigliato)",
    )
    args = parser.parse_args()
    load_env()
    client = sb_client()
    supabase_url = os.environ.get("SUPABASE_URL", "").strip()
    tpl = load_templates()

    res = (
        client.table("pianificazioni")
        .select("*")
        .in_("contenuto", ["immobile", "articolo", "blog"])
        .execute()
    )
    rows = res.data or []
    if not rows:
        print("Nessuna pianificazione immobile/blog trovata.")
        return 0

    imm_cache: dict[str, dict] = {}
    blog_cache: dict[str, dict] = {}

    updated = 0
    skipped = 0

    for row in rows:
        note = row.get("note") or ""
        if PUB_OK in note and not args.include_pubblicate:
            skipped += 1
            continue

        contenuto = str(row.get("contenuto") or "").lower()
        ref = str(row.get("riferimento_id") or "").strip()
        if not ref:
            skipped += 1
            continue

        if contenuto == "immobile":
            section = "immobile"
            if ref not in imm_cache:
                q = client.table("immobili").select("*").eq("id", ref).limit(1).execute()
                imm_cache[ref] = (q.data or [{}])[0]
            src = imm_cache.get(ref) or {}
            if not src.get("id"):
                skipped += 1
                continue
            ctx, link, _, _ = _ctx_from_immobile(src, supabase_url)
            base = list((tpl.get("immobile") or {}).get("hashtags") or [])
            tags = tags_for_immobile(src, base)
        elif contenuto in ("articolo", "blog"):
            section = "blog"
            if ref not in blog_cache:
                q = client.table("blog").select("*").eq("id", ref).limit(1).execute()
                blog_cache[ref] = (q.data or [{}])[0]
            src = blog_cache.get(ref) or {}
            if not src.get("id"):
                skipped += 1
                continue
            ctx, link, _, _ = _ctx_from_blog(src, supabase_url)
            base = list((tpl.get("blog") or {}).get("hashtags") or [])
            tags = tags_for_blog(src, base)
        else:
            skipped += 1
            continue

        if len(tags) < 10:
            print(f"WARN {row.get('id')}: meno di 10 hashtag", file=sys.stderr)

        titolo, corpo, tags = build_copy(section, tpl, ctx, link, tags)
        old_tit = (row.get("titolo") or "")[:80]
        payload = {
            "titolo": titolo,
            "corpo_spintax": corpo,
            "link_media": link,
            "keywords": tags,
            "updated_at": datetime.now(tz=TZ).isoformat(),
        }

        if args.dry_run:
            _safe_print(f"[DRY] {row.get('id')} | {old_tit} -> {titolo[:80]}")
            updated += 1
            continue

        client.table("pianificazioni").update(payload).eq("id", row["id"]).execute()
        _safe_print(f"OK {row.get('id')} | {titolo[:60]}")
        updated += 1

    print(f"Fine: aggiornate {updated}, saltate {skipped}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
