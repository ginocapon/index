#!/usr/bin/env python3
"""
Programma rotazione immobili + blog su più giorni (es. sabato e domenica).

Uso:
  python programma_weekend.py --count 6 --dry-run
  python programma_weekend.py --count 6
  python programma_weekend.py --count 6 --giorni 2026-05-31,2026-06-01
"""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

ROOT = __import__("pathlib").Path(__file__).resolve().parent
TZ = ZoneInfo("Europe/Rome")
CHANNELS = ("facebook_post", "instagram_feed")
DEFAULT_HOURS = ("10:00", "11:30", "13:00", "15:00", "17:00", "19:00")


def load_env() -> None:
    load_dotenv(ROOT / ".env")


def sb():
    import os
    from supabase import create_client

    load_env()
    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_KEY", "").strip()
    if not url or not key:
        print("Manca SUPABASE_URL o SUPABASE_KEY", file=sys.stderr)
        sys.exit(2)
    return create_client(url, key)


def js_weekday(d: date) -> int:
    py_to_js = {6: 0, 0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6}
    return py_to_js.get(d.weekday(), 0)


def add_minutes(hhmm: str, delta: int) -> str:
    h, m = map(int, hhmm.split(":"))
    total = h * 60 + m + delta
    return f"{(total // 60) % 24:02d}:{total % 60:02d}"


def next_weekend(today: date) -> tuple[date, date]:
    """Prossimo sabato e domenica (se oggi è sab/dom include oggi se sab)."""
    wd = today.weekday()  # lun=0 … dom=6
    if wd == 5:
        sat = today
    elif wd == 6:
        sat = today - timedelta(days=1)
    else:
        days_to_sat = (5 - wd) % 7
        if days_to_sat == 0:
            days_to_sat = 7
        sat = today + timedelta(days=days_to_sat)
    sun = sat + timedelta(days=1)
    return sat, sun


def refs_in_range(client, d_from: str, d_to: str) -> set[str]:
    res = (
        client.table("pianificazioni")
        .select("riferimento_id,data_inizio")
        .gte("data_inizio", d_from)
        .lte("data_inizio", d_to)
        .execute()
    )
    out: set[str] = set()
    for row in res.data or []:
        ref = str(row.get("riferimento_id") or "").strip()
        if ref:
            out.add(ref)
    return out


def tags_for_immobile(row: dict, base: list[str]) -> list[str]:
    import re

    def slug_tag(text: str) -> str:
        s = re.sub(r"[^a-z0-9]+", "", (text or "").lower())
        return f"#{s}" if len(s) > 2 else ""

    out = list(base)
    for field in ("comune", "zona", "tipologia", "tipo"):
        t = slug_tag(str(row.get(field) or ""))
        if t and t not in out:
            out.append(t)
    return out[:15]


def tags_for_blog(row: dict, base: list[str]) -> list[str]:
    import re

    def slug_tag(text: str) -> str:
        s = re.sub(r"[^a-z0-9]+", "", (text or "").lower())
        return f"#{s}" if len(s) > 2 else ""

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


def build_row(
    *,
    tipo: str,
    contenuto: str,
    titolo: str,
    corpo: str,
    link: str,
    ref: str | None,
    media: str | None,
    day: date,
    ora: str,
    tags: list[str],
    note: str,
) -> dict[str, Any]:
    day_iso = day.isoformat()
    corpo_full = corpo.rstrip()
    if link and link not in corpo_full:
        corpo_full += "\n\n" + link
    if tags:
        tag_line = " ".join(tags)
        if tag_line not in corpo_full:
            corpo_full += "\n\n" + tag_line
    return {
        "tipo": tipo,
        "contenuto": contenuto,
        "titolo": titolo[:200],
        "riferimento_id": ref,
        "ora": ora,
        "giorni": [js_weekday(day)],
        "data_inizio": day_iso,
        "data_fine": day_iso,
        "keywords": tags,
        "note": note,
        "link_media": link,
        "corpo_spintax": corpo_full,
        "media_direct_url": media,
        "updated_at": datetime.now(tz=TZ).isoformat(),
        "created_at": datetime.now(tz=TZ).isoformat(),
    }


def _safe_print(msg: str) -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    print(msg.encode("ascii", "replace").decode("ascii"), flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=6, help="Totale immobili E totale blog")
    parser.add_argument(
        "--giorni",
        default="",
        help="Date ISO separate da virgola (default: prossimo sab+dom)",
    )
    parser.add_argument(
        "--hours",
        default=",".join(DEFAULT_HOURS),
        help="Orari slot separati da virgola (6 consigliati)",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    load_env()

    from genera_bozze_settimanali import (
        _ctx_from_blog,
        _ctx_from_immobile,
        apply_pattern,
        filter_active_immobili,
        load_templates,
        rotation_pool_blog,
        stable_sort_immobili,
    )

    client = sb()
    supabase_url = __import__("os").environ.get("SUPABASE_URL", "").strip()
    tpl = load_templates()
    today = datetime.now(tz=TZ).date()

    if args.giorni.strip():
        days = [date.fromisoformat(x.strip()[:10]) for x in args.giorni.split(",") if x.strip()]
    else:
        sat, sun = next_weekend(today + timedelta(days=1))
        days = [sat, sun]

    if len(days) < 1:
        print("Serve almeno un giorno.", file=sys.stderr)
        return 1

    hours = [h.strip() for h in args.hours.split(",") if h.strip()]
    per_day = max(1, args.count // len(days))
    if per_day * 2 > len(hours):
        print(
            f"WARN: servono almeno {per_day * 2} orari/giorno, ne hai {len(hours)}",
            file=sys.stderr,
        )

    d_from = min(days).isoformat()
    d_to = max(days).isoformat()
    # Esclude contenuti già in agenda da oggi fino a fine weekend (rotazione)
    used_from = min(today, min(days)).isoformat()
    used = refs_in_range(client, used_from, d_to)

    imm_all = (
        client.table("immobili")
        .select("*")
        .eq("attivo", True)
        .limit(120)
        .execute()
    ).data or []
    pool_imm = [
        r
        for r in stable_sort_immobili(filter_active_immobili(imm_all))
        if str(r.get("id")) not in used
    ]

    blog_all = (
        client.table("blog")
        .select("*")
        .order("created_at", desc=True)
        .limit(120)
        .execute()
    ).data or []
    pool_blog = [
        r for r in rotation_pool_blog(blog_all) if str(r.get("id")) not in used
    ]

    need_imm = args.count
    need_blog = args.count
    immobili = pool_imm[:need_imm]
    blogs = pool_blog[:need_blog]

    if len(immobili) < need_imm or len(blogs) < need_blog:
        print(
            f"WARN: pool ridotto imm={len(immobili)}/{need_imm} blog={len(blogs)}/{need_blog}",
            file=sys.stderr,
        )
    if not immobili or not blogs:
        return 1

    imm_tpl = tpl.get("immobile") or {}
    blog_tpl = tpl.get("blog") or {}
    imm_cor = (imm_tpl.get("corpo_spintax") or [""])[0]
    blog_cor = (blog_tpl.get("corpo_spintax") or [""])[0]
    note = f"[WEEKEND_ROT] programma_weekend.py {d_from}..{d_to}"

    rows: list[dict[str, Any]] = []
    imm_i = 0
    blog_i = 0

    for day in days:
        imm_day = immobili[imm_i : imm_i + per_day]
        blog_day = blogs[blog_i : blog_i + per_day]
        imm_i += per_day
        blog_i += per_day

        imm_hours = hours[: len(imm_day)]
        blog_hours = hours[len(imm_day) : len(imm_day) + len(blog_day)]

        for imm, hh in zip(imm_day, imm_hours):
            ctx, link, ref, media = _ctx_from_immobile(imm, supabase_url)
            titolo = str(ctx.get("titolo") or "Immobile")
            corpo = apply_pattern(imm_cor, ctx)
            tags = tags_for_immobile(imm, list(imm_tpl.get("hashtags") or []))
            for ch_i, tipo in enumerate(CHANNELS):
                rows.append(
                    build_row(
                        tipo=tipo,
                        contenuto="immobile",
                        titolo=titolo,
                        corpo=corpo,
                        link=link,
                        ref=ref,
                        media=media,
                        day=day,
                        ora=add_minutes(hh, ch_i * 2),
                        tags=tags,
                        note=note,
                    )
                )

        for blog, hh in zip(blog_day, blog_hours):
            ctx, link, ref, media = _ctx_from_blog(blog, supabase_url)
            titolo = str(ctx.get("titolo") or "Articolo")
            corpo = apply_pattern(blog_cor, ctx)
            tags = tags_for_blog(blog, list(blog_tpl.get("hashtags") or []))
            for ch_i, tipo in enumerate(CHANNELS):
                rows.append(
                    build_row(
                        tipo=tipo,
                        contenuto="articolo",
                        titolo=titolo,
                        corpo=corpo,
                        link=link,
                        ref=ref,
                        media=media,
                        day=day,
                        ora=add_minutes(hh, ch_i * 2),
                        tags=tags,
                        note=note,
                    )
                )

    _safe_print(
        f"Giorni: {', '.join(d.isoformat() for d in days)} | "
        f"{len(immobili)} imm + {len(blogs)} blog | {len(rows)} righe FB+IG"
    )
    for r in rows:
        _safe_print(f"  {r['data_inizio']} {r['ora']} {r['tipo']:16} {(r['titolo'] or '')[:52]}")

    if args.dry_run:
        print("Dry-run: nessun insert.")
        return 0

    for i in range(0, len(rows), 20):
        client.table("pianificazioni").insert(rows[i : i + 20]).execute()
    print(f"OK: inserite {len(rows)} righe in pianificazioni.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
