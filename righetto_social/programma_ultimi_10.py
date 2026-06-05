#!/usr/bin/env python3
"""
Programma ultimi N immobili + articoli blog su 3 giorni (oggi, domani, dopodomani)
negli slot 10:00, 13:00, 19:00 — Facebook post + Instagram feed (no reel).

Uso:
  python programma_ultimi_10.py
  python programma_ultimi_10.py --dry-run
  python programma_ultimi_10.py --count 10 --pubblica-oggi
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
BASE_SITE = "https://righettoimmobiliare.it"
SLOT_HOURS = ("10:00", "13:00", "19:00")
CHANNELS = ("facebook_post", "instagram_feed")


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


def js_weekday(iso_date: str) -> int:
    d = datetime.strptime(iso_date[:10], "%Y-%m-%d").date()
    py_to_js = {6: 0, 0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6}
    return py_to_js.get(d.weekday(), 0)


def day_slots(count: int) -> list[tuple[int, str]]:
    """Distribuisce count elementi su 3 giorni × slot 10/13/19 (+ offset minuti se >9)."""
    base: list[tuple[int, str]] = []
    for day in range(3):
        for hour in SLOT_HOURS:
            base.append((day, hour))
    if count <= len(base):
        return base[:count]
    extra: list[tuple[int, str]] = []
    for i in range(count - len(base)):
        day = i % 3
        hour = SLOT_HOURS[i % 3]
        # +5 min per evitare collisione stesso minuto
        h, m = map(int, hour.split(":"))
        m += 5 * (1 + i // 3)
        extra.append((day, f"{h:02d}:{m % 60:02d}"))
    return base + extra


def build_row(
    *,
    tipo: str,
    contenuto: str,
    titolo: str,
    corpo: str,
    link: str,
    ref: str | None,
    media: str | None,
    day_iso: str,
    ora: str,
    tags: list[str],
) -> dict[str, Any]:
    corpo_full = corpo.rstrip()
    if link and link not in corpo_full:
        corpo_full += "\n\n" + link
    if tags:
        corpo_full += "\n\n" + " ".join(tags)
    return {
        "tipo": tipo,
        "contenuto": contenuto,
        "titolo": titolo[:200],
        "riferimento_id": ref,
        "ora": ora,
        "giorni": [js_weekday(day_iso)],
        "data_inizio": day_iso,
        "data_fine": day_iso,
        "keywords": tags,
        "note": "[BATCH_3GG] programma_ultimi_10.py",
        "link_media": link,
        "corpo_spintax": corpo_full,
        "media_direct_url": media,
        "updated_at": datetime.now(tz=TZ).isoformat(),
        "created_at": datetime.now(tz=TZ).isoformat(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=10, help="Quanti immobili e quanti blog")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--pubblica-oggi",
        action="store_true",
        help="Dopo insert, lancia publish per slot di oggi già passati",
    )
    args = parser.parse_args()
    load_env()

    from genera_bozze_settimanali import (
        _ctx_from_blog,
        _ctx_from_immobile,
        apply_pattern,
        filter_active_immobili,
        load_templates,
        rotation_pool_blog,
    )

    tpl = load_templates()
    client = sb()
    supabase_url = __import__("os").environ.get("SUPABASE_URL", "").strip()

    imm_all = (
        client.table("immobili")
        .select("*")
        .eq("attivo", True)
        .order("created_at", desc=True)
        .limit(args.count * 2)
        .execute()
    ).data or []
    immobili = filter_active_immobili(imm_all)[: args.count]

    blog_all = (
        client.table("blog")
        .select("*")
        .order("created_at", desc=True)
        .limit(args.count * 2)
        .execute()
    ).data or []
    blogs = rotation_pool_blog(blog_all)[: args.count]

    if not immobili:
        print("Nessun immobile attivo trovato.", file=sys.stderr)
        return 1
    if not blogs:
        print("Nessun articolo blog pubblicato trovato.", file=sys.stderr)
        return 1

    today = datetime.now(tz=TZ).date()
    imm_slots = day_slots(len(immobili))
    blog_slots = day_slots(len(blogs))

    rows: list[dict[str, Any]] = []
    imm_tpl = tpl.get("immobile") or {}
    blog_tpl = tpl.get("blog") or {}
    imm_tags = list(imm_tpl.get("hashtags") or [])[:12]
    blog_tags = list(blog_tpl.get("hashtags") or [])[:12]
    imm_tit_p = imm_tpl.get("titoli_spintax") or ["{titolo}"]
    imm_cor_p = imm_tpl.get("corpo_spintax") or [""]
    blog_tit_p = blog_tpl.get("titoli_spintax") or ["{titolo}"]
    blog_cor_p = blog_tpl.get("corpo_spintax") or [""]

    for idx, imm in enumerate(immobili):
        day_off, ora = imm_slots[idx]
        day_iso = (today + timedelta(days=day_off)).isoformat()
        ctx, link, ref, media = _ctx_from_immobile(imm, supabase_url)
        titolo = apply_pattern(imm_tit_p[idx % len(imm_tit_p)], ctx)
        corpo = apply_pattern(imm_cor_p[idx % len(imm_cor_p)], ctx)
        for ch_i, tipo in enumerate(CHANNELS):
            ora_ch = ora
            if ch_i:
                h, m = map(int, ora.split(":"))
                m += 2
                ora_ch = f"{h:02d}:{m % 60:02d}"
            rows.append(
                build_row(
                    tipo=tipo,
                    contenuto="immobile",
                    titolo=titolo,
                    corpo=corpo,
                    link=link,
                    ref=ref,
                    media=media,
                    day_iso=day_iso,
                    ora=ora_ch,
                    tags=imm_tags,
                )
            )

    for idx, blog in enumerate(blogs):
        day_off, ora = blog_slots[idx]
        day_iso = (today + timedelta(days=day_off)).isoformat()
        ctx, link, ref, media = _ctx_from_blog(blog, supabase_url)
        titolo = apply_pattern(blog_tit_p[idx % len(blog_tit_p)], ctx)
        corpo = apply_pattern(blog_cor_p[idx % len(blog_cor_p)], ctx)
        for ch_i, tipo in enumerate(CHANNELS):
            h, m = map(int, ora.split(":"))
            m += 1 + ch_i  # offset rispetto agli immobili stesso slot
            ora_ch = f"{h:02d}:{m % 60:02d}"
            rows.append(
                build_row(
                    tipo=tipo,
                    contenuto="articolo",
                    titolo=titolo,
                    corpo=corpo,
                    link=link,
                    ref=ref,
                    media=media,
                    day_iso=day_iso,
                    ora=ora_ch,
                    tags=blog_tags,
                )
            )

    print(f"Immobili: {len(immobili)} | Blog: {len(blogs)} | Righe agenda: {len(rows)}")
    for r in rows[:6]:
        print(f"  {r['data_inizio']} {r['ora']} {r['tipo']:16} {r['contenuto']:8} {(r['titolo'] or '')[:50]}")
    if len(rows) > 6:
        print(f"  … +{len(rows) - 6} righe")

    if args.dry_run:
        print("Dry-run: nessun insert.")
        return 0

    inserted = 0
    for batch_start in range(0, len(rows), 20):
        batch = rows[batch_start : batch_start + 20]
        client.table("pianificazioni").insert(batch).execute()
        inserted += len(batch)
    print(f"OK: inserite {inserted} righe in pianificazioni.")

    if args.pubblica_oggi:
        import subprocess

        print("Pubblicazione slot di oggi (forza)…")
        subprocess.run(
            [sys.executable, str(ROOT / "publish_from_agenda.py"), "--modo", "manuale", "--forza"],
            cwd=str(ROOT),
            check=False,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
