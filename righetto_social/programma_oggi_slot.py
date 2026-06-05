#!/usr/bin/env python3
"""
Agenda giornaliera: 4 immobili + 4 blog + pagine sito (2×/settimana ciascuna).

Fasce orarie: 10:00, 13:00, 15:00, 19:00 — in ogni fascia:
  +0 min immobile, +15 min blog, +30 min pagina sito (landing o agenzia).
Tra contenuti diversi: minimo 15 min. FB e IG dello stesso contenuto: +2 min.

Uso:
  python programma_oggi_slot.py --dry-run --ciclo-completo
  python programma_oggi_slot.py --ciclo-completo
"""

from __future__ import annotations

import argparse
import math
import subprocess
import sys
from datetime import date, datetime, timedelta
from typing import Any, Callable
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

ROOT = __import__("pathlib").Path(__file__).resolve().parent
TZ = ZoneInfo("Europe/Rome")
ANCHOR_SLOTS = ("10:00", "13:00", "15:00", "19:00")
CHANNELS = ("facebook_post", "instagram_feed")
IMM_PER_DAY = 4
BLOG_PER_DAY = 4
STAGGER_MINUTES = 15
SITE_POSTS_PER_PAGE_PER_WEEK = 2
PUB_OK = "PUB_OK"

SiteItem = tuple[str, dict]  # ("landing"|"agenzia", row)


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


def day_range(start: date, count: int) -> list[date]:
    return [start + timedelta(days=i) for i in range(count)]


def week_monday(d: date) -> date:
    return d - timedelta(days=d.weekday())


def pending_ids_from(client, from_date: str) -> list[str]:
    res = (
        client.table("pianificazioni")
        .select("id,note")
        .gte("data_inizio", from_date)
        .execute()
    )
    return [
        str(row["id"])
        for row in (res.data or [])
        if PUB_OK not in str(row.get("note") or "") and row.get("id")
    ]


def delete_pending(client, from_date: str, *, dry_run: bool) -> int:
    ids = pending_ids_from(client, from_date)
    if not ids:
        return 0
    if dry_run:
        print(f"Dry-run: cancellerei {len(ids)} righe da {from_date} senza {PUB_OK}.")
        return len(ids)
    for i in range(0, len(ids), 50):
        client.table("pianificazioni").delete().in_("id", ids[i : i + 50]).execute()
    print(f"OK: cancellate {len(ids)} righe da {from_date} senza {PUB_OK}.")
    return len(ids)


def build_site_pool(
    landings: list[dict], agenzia_pages: list[dict]
) -> list[SiteItem]:
    out: list[SiteItem] = []
    for row in landings:
        out.append(("landing", row))
    for pg in agenzia_pages:
        out.append(("agenzia", pg))
    return out


def site_schedule_for_week(
    pool_site: list[SiteItem], cursor: int
) -> list[list[SiteItem]]:
    """7 liste (lun–dom): ogni pagina compare 2 volte nella settimana."""
    if not pool_site:
        return [[] for _ in range(7)]
    n = len(pool_site) * SITE_POSTS_PER_PAGE_PER_WEEK
    batch = [pool_site[(cursor + i) % len(pool_site)] for i in range(n)]
    per_day: list[list[SiteItem]] = [[] for _ in range(7)]
    for idx, item in enumerate(batch):
        per_day[idx % 7].append(item)
    return per_day


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


def tags_for_site(_row: dict, base: list[str]) -> list[str]:
    return list(base)[:15]


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


def append_content_rows(
    rows: list[dict[str, Any]],
    *,
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
) -> None:
    for ch_i, tipo in enumerate(CHANNELS):
        rows.append(
            build_row(
                tipo=tipo,
                contenuto=contenuto,
                titolo=titolo,
                corpo=corpo,
                link=link,
                ref=ref,
                media=media,
                day=day,
                ora=add_minutes(ora, ch_i * 2),
                tags=tags,
                note=note,
            )
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--slots",
        default=",".join(ANCHOR_SLOTS),
        help="4 fasce HH:MM (default 10,13,15,19)",
    )
    parser.add_argument("--giorni", default="", help="Date ISO esplicite")
    parser.add_argument(
        "--include-oggi",
        action="store_true",
        help="Include oggi (default: da domani)",
    )
    parser.add_argument(
        "--ciclo-completo",
        action="store_true",
        help="Giorni sufficienti a coprire tutto il catalogo",
    )
    parser.add_argument("--num-giorni", type=int, default=0)
    parser.add_argument("--no-cancella", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--pubblica", action="store_true")
    args = parser.parse_args()
    load_env()

    from genera_bozze_settimanali import (
        _ctx_from_blog,
        _ctx_from_immobile,
        _ctx_from_landing,
        _ctx_from_agenzia,
        _fetch_paginated,
        apply_pattern,
        filter_active_immobili,
        load_templates,
        pick_rotating_batch,
        rotation_cursor,
        rotation_pool_blog,
        rotation_pool_landing,
        stable_sort_immobili,
    )

    client = sb()
    supabase_url = __import__("os").environ.get("SUPABASE_URL", "").strip()
    tpl = load_templates()
    today = datetime.now(tz=TZ).date()
    start = today if args.include_oggi else today + timedelta(days=1)

    pool_imm = stable_sort_immobili(
        filter_active_immobili(
            _fetch_paginated(client, "immobili", filters=[("attivo", "eq", True)])
        )
    )
    pool_blog = rotation_pool_blog(
        _fetch_paginated(client, "blog", order_col="created_at")
    )
    pool_land = rotation_pool_landing(
        _fetch_paginated(client, "landing_pages", order_col="created_at")
    )
    pool_agenzia = list(tpl.get("pagine_agenzia") or [])
    pool_site = build_site_pool(pool_land, pool_agenzia)

    if not pool_imm or not pool_blog:
        print("Catalogo immobili o blog vuoto.", file=sys.stderr)
        return 1

    anchors = [s.strip() for s in args.slots.split(",") if s.strip()]
    if len(anchors) != 4:
        print("Servono 4 fasce orarie.", file=sys.stderr)
        return 1

    if args.giorni.strip():
        days = [date.fromisoformat(x.strip()[:10]) for x in args.giorni.split(",") if x.strip()]
    elif args.ciclo_completo:
        n = max(
            math.ceil(len(pool_imm) / IMM_PER_DAY),
            math.ceil(len(pool_blog) / BLOG_PER_DAY),
            7,
        )
        days = day_range(start, n)
    elif args.num_giorni > 0:
        days = day_range(start, args.num_giorni)
    else:
        days = day_range(start, 7)

    need_imm = IMM_PER_DAY * len(days)
    need_blog = BLOG_PER_DAY * len(days)

    cur_imm = rotation_cursor(client, "immobile")
    cur_blog = rotation_cursor(client, "blog")
    cur_site = rotation_cursor(client, "landing") + rotation_cursor(client, "agenzia")
    batch_imm = [r for r in pick_rotating_batch(pool_imm, cur_imm, need_imm) if r]
    batch_blog = [r for r in pick_rotating_batch(pool_blog, cur_blog, need_blog) if r]

    d_from = min(days).isoformat()
    d_to = max(days).isoformat()
    note = (
        f"[SLOT4x4] programma_oggi_slot.py {d_from}..{d_to} "
        f"imm={cur_imm}/{len(pool_imm)} blog={cur_blog}/{len(pool_blog)} "
        f"site={len(pool_site)}×2/sett"
    )

    cancel_from = d_from if args.giorni.strip() or args.include_oggi else start.isoformat()
    if not args.no_cancella:
        delete_pending(client, cancel_from, dry_run=args.dry_run)

    imm_tpl = tpl.get("immobile") or {}
    blog_tpl = tpl.get("blog") or {}
    land_tpl = tpl.get("landing") or {}
    ag_tpl = tpl.get("agenzia") or {}
    imm_cor = (imm_tpl.get("corpo_spintax") or [""])[0]
    blog_cor = (blog_tpl.get("corpo_spintax") or [""])[0]
    land_cor = (land_tpl.get("corpo_spintax") or [""])[0]
    ag_cor = (ag_tpl.get("corpo_spintax") or [""])[0]

    week_site_cache: dict[date, list[list[SiteItem]]] = {}
    site_week_cursor = cur_site

    rows: list[dict[str, Any]] = []
    imm_i = 0
    blog_i = 0

    def schedule_site(day: date, slot_idx: int, item: SiteItem) -> None:
        kind, row = item
        anchor = anchors[slot_idx]
        ora = add_minutes(anchor, STAGGER_MINUTES * 2)
        if kind == "landing":
            ctx, link, ref, media = _ctx_from_landing(row)
            titolo = str(ctx.get("titolo") or "Landing")
            corpo = apply_pattern(land_cor, ctx)
            contenuto = "landing"
            tags = tags_for_site(row, list(land_tpl.get("hashtags") or []))
        else:
            ctx, link, ref, media = _ctx_from_agenzia(row)
            titolo = str(ctx.get("titolo") or "Pagina")
            corpo = apply_pattern(ag_cor, ctx)
            contenuto = "pagina_agenzia"
            ref = str(row.get("path") or "/")
            tags = tags_for_site(row, list(ag_tpl.get("hashtags") or []))
        append_content_rows(
            rows,
            contenuto=contenuto,
            titolo=titolo,
            corpo=corpo,
            link=link,
            ref=ref,
            media=media,
            day=day,
            ora=ora,
            tags=tags,
            note=note,
        )

    for day in days:
        wm = week_monday(day)
        if wm not in week_site_cache:
            week_site_cache[wm] = site_schedule_for_week(pool_site, site_week_cursor)
            site_week_cursor += max(len(pool_site) * SITE_POSTS_PER_PAGE_PER_WEEK, 0)
        site_today = week_site_cache[wm][day.weekday()]

        for slot_idx, anchor in enumerate(anchors):
            imm = batch_imm[imm_i]
            blog = batch_blog[blog_i]
            imm_i += 1
            blog_i += 1

            ctx, link, ref, media = _ctx_from_immobile(imm, supabase_url)
            append_content_rows(
                rows,
                contenuto="immobile",
                titolo=str(ctx.get("titolo") or "Immobile"),
                corpo=apply_pattern(imm_cor, ctx),
                link=link,
                ref=ref,
                media=media,
                day=day,
                ora=anchor,
                tags=tags_for_immobile(imm, list(imm_tpl.get("hashtags") or [])),
                note=note,
            )

            ctx, link, ref, media = _ctx_from_blog(blog, supabase_url)
            append_content_rows(
                rows,
                contenuto="articolo",
                titolo=str(ctx.get("titolo") or "Articolo"),
                corpo=apply_pattern(blog_cor, ctx),
                link=link,
                ref=ref,
                media=media,
                day=day,
                ora=add_minutes(anchor, STAGGER_MINUTES),
                tags=tags_for_blog(blog, list(blog_tpl.get("hashtags") or [])),
                note=note,
            )

            if slot_idx < len(site_today):
                schedule_site(day, slot_idx, site_today[slot_idx])

    rows.sort(key=lambda r: (r["data_inizio"], r["ora"], r["tipo"]))

    posts_per_day = IMM_PER_DAY + BLOG_PER_DAY
    if pool_site:
        posts_per_day += math.ceil(len(pool_site) * SITE_POSTS_PER_PAGE_PER_WEEK / 7)

    print(
        f"Pool: {len(pool_imm)} imm, {len(pool_blog)} blog, {len(pool_site)} pagine sito | "
        f"{len(days)} giorni ({d_from}..{d_to}) | "
        f"{IMM_PER_DAY} imm + {BLOG_PER_DAY} blog/giorno | "
        f"pagine sito {SITE_POSTS_PER_PAGE_PER_WEEK}×/sett | "
        f"stagger {STAGGER_MINUTES} min | {len(rows)} righe FB+IG"
    )

    for day in (days[:2] + days[-1:]):
        day_rows = [r for r in rows if r["data_inizio"] == day.isoformat()]
        seen: set[str] = set()
        print(f"  {day.isoformat()}:")
        for r in sorted(day_rows, key=lambda x: x["ora"]):
            key = f"{r['contenuto']}:{r['riferimento_id']}:{r['ora'][:5]}"
            if key in seen:
                continue
            seen.add(key)
            tag = {"immobile": "I", "articolo": "A", "landing": "L", "pagina_agenzia": "P"}.get(
                r["contenuto"], "?"
            )
            print(f"    {r['ora'][:5]} {tag} {(r['titolo'] or '')[:42]}")
    if len(days) > 3:
        print(f"  … +{len(days) - 3} giorni")

    if args.dry_run:
        print("Dry-run: nessun insert.")
        return 0

    for batch_start in range(0, len(rows), 20):
        client.table("pianificazioni").insert(rows[batch_start : batch_start + 20]).execute()
    print(f"OK: inserite {len(rows)} righe in pianificazioni.")

    if args.pubblica:
        subprocess.run(
            [sys.executable, str(ROOT / "publish_from_agenda.py"), "--modo", "manuale", "--forza"],
            cwd=str(ROOT),
            check=False,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
