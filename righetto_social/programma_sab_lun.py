#!/usr/bin/env python3
"""
Programma rotazione immobili su 3 giorni: domani, dopodomani e lunedì.

- N immobili diversi al giorno (default 10), senza ripetizioni nel batch.
- Ordine catalogo per codice; riparte dal cursore rotazione (skill §2).
- Per ogni immobile: reel → +30 min FB → +32 min IG → +60 min storia (storia manuale).
- Tra un immobile e il successivo: +30 min sull'orario base (primo post 09:30).

Uso:
  python programma_sab_lun.py --dry-run
  python programma_sab_lun.py --per-giorno 10
  python programma_sab_lun.py --giorni 2026-05-30,2026-05-31,2026-06-01 --per-giorno 10
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
BASE_START = "09:30"
STAGGER_IMM_MINUTES = 30
# Offset minuti dal reel dello stesso immobile
CHANNEL_OFFSET = (
    ("instagram_reel", 0),
    ("facebook_post", 30),
    ("instagram_feed", 32),
    ("instagram_story", 60),
)
PUB_OK = "PUB_OK"


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


def default_days(today: date) -> list[date]:
    """Domani, dopodomani e lunedì (3 date distinte in ordine cronologico)."""
    tomorrow = today + timedelta(days=1)
    day_after = today + timedelta(days=2)
    monday = day_after
    while monday.weekday() != 0:
        monday += timedelta(days=1)
    out: list[date] = []
    for d in (tomorrow, day_after, monday):
        if d not in out:
            out.append(d)
    return sorted(out)


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


def pending_future_ids(client, from_date: str) -> list[str]:
    res = (
        client.table("pianificazioni")
        .select("id,note,data_inizio")
        .gte("data_inizio", from_date)
        .execute()
    )
    out: list[str] = []
    for row in res.data or []:
        if PUB_OK in str(row.get("note") or ""):
            continue
        rid = row.get("id")
        if rid:
            out.append(str(rid))
    return out


def delete_pending(client, from_date: str, *, dry_run: bool) -> int:
    ids = pending_future_ids(client, from_date)
    if not ids:
        return 0
    if dry_run:
        print(f"Dry-run: cancellerei {len(ids)} righe future senza {PUB_OK}.")
        return len(ids)
    deleted = 0
    for i in range(0, len(ids), 50):
        batch = ids[i : i + 50]
        client.table("pianificazioni").delete().in_("id", batch).execute()
        deleted += len(batch)
    print(f"OK: cancellate {deleted} righe future senza {PUB_OK}.")
    return deleted


def _safe_print(msg: str) -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    print(msg.encode("ascii", "replace").decode("ascii"), flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--per-giorno",
        type=int,
        default=10,
        help="Immobili diversi per ogni giorno (default 10)",
    )
    parser.add_argument(
        "--giorni",
        default="",
        help="Date ISO separate da virgola (default: domani+dopodomani+lunedì)",
    )
    parser.add_argument(
        "--cursore",
        type=int,
        default=-1,
        help="Indice rotazione manuale (-1 = auto da Supabase)",
    )
    parser.add_argument(
        "--no-cancella",
        action="store_true",
        help="Non cancellare righe future pending",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    load_env()

    from genera_bozze_settimanali import (
        _ctx_from_immobile,
        _fetch_paginated,
        apply_pattern,
        filter_active_immobili,
        load_templates,
        pick_rotating_batch,
        rotation_cursor,
        stable_sort_immobili,
    )

    client = sb()
    supabase_url = __import__("os").environ.get("SUPABASE_URL", "").strip()
    tpl = load_templates()
    today = datetime.now(tz=TZ).date()

    if args.giorni.strip():
        days = [date.fromisoformat(x.strip()[:10]) for x in args.giorni.split(",") if x.strip()]
    else:
        days = default_days(today)

    if not days or args.per_giorno < 1:
        print("Giorni o --per-giorno non validi.", file=sys.stderr)
        return 1

    total = args.per_giorno * len(days)
    d_from = min(days).isoformat()
    d_to = max(days).isoformat()

    pool = stable_sort_immobili(
        filter_active_immobili(
            _fetch_paginated(client, "immobili", filters=[("attivo", "eq", True)])
        )
    )
    if not pool:
        print("Nessun immobile attivo nel catalogo.", file=sys.stderr)
        return 1

    cursor = args.cursore if args.cursore >= 0 else rotation_cursor(client, "immobile")
    batch = pick_rotating_batch(pool, cursor, total)
    batch = [r for r in batch if r is not None]
    if len(batch) < total:
        print(
            f"WARN: pool={len(pool)} cursore={cursor} — solo {len(batch)} immobili unici",
            file=sys.stderr,
        )

    note = (
        f"[SAB_LUN_ROT] programma_sab_lun.py {d_from}..{d_to} "
        f"cursor={cursor} pool={len(pool)}"
    )

    if not args.no_cancella:
        delete_pending(client, today.isoformat(), dry_run=args.dry_run)

    imm_tpl = tpl.get("immobile") or {}
    imm_cor = (imm_tpl.get("corpo_spintax") or [""])[0]
    base_tags = list(imm_tpl.get("hashtags") or [])

    rows: list[dict[str, Any]] = []
    for idx, imm in enumerate(batch):
        day = days[idx // args.per_giorno]
        pos_in_day = idx % args.per_giorno
        ctx, link, ref, media = _ctx_from_immobile(imm, supabase_url)
        titolo = str(ctx.get("titolo") or "Immobile")
        corpo = apply_pattern(imm_cor, ctx)
        tags = tags_for_immobile(imm, base_tags)
        reel_base = add_minutes(BASE_START, pos_in_day * STAGGER_IMM_MINUTES)

        for tipo, off_min in CHANNEL_OFFSET:
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
                    ora=add_minutes(reel_base, off_min),
                    tags=tags,
                    note=note,
                )
            )

    rows.sort(key=lambda r: (r["data_inizio"], r["ora"], r["tipo"]))

    _safe_print(
        f"Pool catalogo: {len(pool)} imm | cursore rotazione: {cursor} | "
        f"{args.per_giorno}/giorno × {len(days)} giorni = {len(batch)} immobili unici | "
        f"{len(rows)} righe agenda"
    )
    for day in days:
        day_imm = batch[
            (days.index(day) * args.per_giorno) : (days.index(day) + 1) * args.per_giorno
        ]
        codes = ", ".join(str(i.get("codice") or "?") for i in day_imm)
        _safe_print(f"  {day.isoformat()}: {codes}")

    for r in rows[:12]:
        _safe_print(
            f"  {r['data_inizio']} {r['ora']} {r['tipo']:18} {(r['titolo'] or '')[:50]}"
        )
    if len(rows) > 12:
        _safe_print(f"  … +{len(rows) - 12} righe")

    if args.dry_run:
        print("Dry-run: nessun insert.")
        return 0

    for i in range(0, len(rows), 20):
        client.table("pianificazioni").insert(rows[i : i + 20]).execute()
    print(f"OK: inserite {len(rows)} righe in pianificazioni.")
    print("Prossimo passo: python genera_reel.py --agenda-pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
