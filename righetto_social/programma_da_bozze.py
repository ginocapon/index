"""
Crea righe in pianificazioni dalle bozze_social (stato=bozza o approvata).

Uso:
  python programma_da_bozze.py --min 8
  python programma_da_bozze.py --bozza-id UUID
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

ROOT = __import__("pathlib").Path(__file__).resolve().parent
TZ = ZoneInfo("Europe/Rome")


def load_env() -> None:
    from dotenv import load_dotenv as _ld

    _ld(ROOT / ".env")


def sb():
    from dotenv import load_dotenv

    load_dotenv(ROOT / ".env")
    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_KEY", "").strip()
    if not url or not key:
        print("Manca SUPABASE_URL o SUPABASE_KEY", file=sys.stderr)
        sys.exit(2)
    return create_client(url, key)


def expand_spintax(text: str) -> str:
    out = text or ""
    prev = None
    while prev != out:
        prev = out
        out = re.sub(
            r"\{([^{}]+)\}",
            lambda m: (m.group(1).split("|")[0].strip() if m.group(1) else ""),
            out,
        )
    return out


def js_weekday(iso_date: str) -> int:
    d = datetime.strptime(iso_date[:10], "%Y-%m-%d").date()
    py_to_js = {6: 0, 0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6}
    return py_to_js.get(d.weekday(), 0)


def bozza_to_pianificazione(b: dict[str, Any]) -> dict[str, Any]:
    ds = str(b.get("data_pubblicazione_proposta") or "")[:10]
    corpo = b.get("corpo") or ""
    tags = b.get("hashtags") or []
    if isinstance(tags, list) and tags:
        corpo = corpo.rstrip() + "\n\n" + " ".join(tags)
    return {
        "tipo": b.get("tipo_canale") or "facebook_post",
        "contenuto": "immobile" if b.get("fonte") == "immobile" else "articolo",
        "titolo": (b.get("titolo") or "Post")[:200],
        "riferimento_id": b.get("riferimento_id"),
        "ora": b.get("ora_proposta") or "12:30",
        "giorni": [js_weekday(ds)],
        "data_inizio": ds,
        "data_fine": ds,
        "keywords": tags if isinstance(tags, list) else [],
        "note": f"[DA_BOZZA] id={b.get('id')}",
        "link_media": b.get("link_pagina"),
        "corpo_spintax": corpo,
        "media_direct_url": b.get("media_direct_url"),
        "updated_at": datetime.now(tz=TZ).isoformat(),
        "created_at": datetime.now(tz=TZ).isoformat(),
    }


def _safe_print(msg: str) -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass
    text = msg.encode("ascii", "replace").decode("ascii")
    print(text, flush=True)


def _already_scheduled(client: Any, bozza_id: str) -> bool:
    needle = f"id={bozza_id}"
    res = (
        client.table("pianificazioni")
        .select("id")
        .ilike("note", f"%{needle}%")
        .limit(1)
        .execute()
    )
    return bool(res.data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min", type=int, default=8, help="Minimo bozze da programmare")
    parser.add_argument("--bozza-id", type=str, default="")
    parser.add_argument(
        "--dal",
        type=str,
        default="",
        help="Solo bozze con data_pubblicazione_proposta >= YYYY-MM-DD",
    )
    parser.add_argument(
        "--al",
        type=str,
        default="",
        help="Solo bozze con data_pubblicazione_proposta <= YYYY-MM-DD",
    )
    parser.add_argument(
        "--max",
        type=int,
        default=0,
        help="Massimo righe da creare (0 = tutte)",
    )
    parser.add_argument(
        "--solo-approvate",
        action="store_true",
        help="Solo stato=approvata (default: tutte le bozze)",
    )
    args = parser.parse_args()
    load_env()
    client = sb()

    if args.bozza_id:
        res = client.table("bozze_social").select("*").eq("id", args.bozza_id).execute()
        rows = res.data or []
    else:
        stato = "approvata" if args.solo_approvate else "bozza"
        res = (
            client.table("bozze_social")
            .select("*")
            .eq("stato", stato)
            .order("data_pubblicazione_proposta")
            .execute()
        )
        rows = res.data or []
        if args.dal:
            rows = [
                r
                for r in rows
                if str(r.get("data_pubblicazione_proposta") or "")[:10] >= args.dal
            ]
        if args.al:
            rows = [
                r
                for r in rows
                if str(r.get("data_pubblicazione_proposta") or "")[:10] <= args.al
            ]

    if len(rows) < args.min and not args.bozza_id:
        print(f"Solo {len(rows)} bozze (min {args.min}). Genera prima con genera_bozze_settimanali.py")
        return 1

    n = 0
    skipped = 0
    for b in rows:
        bid = str(b.get("id") or "")
        if bid and _already_scheduled(client, bid):
            skipped += 1
            continue
        payload = bozza_to_pianificazione(b)
        client.table("pianificazioni").insert(payload).execute()
        client.table("bozze_social").update(
            {
                "stato": "programmata",
                "updated_at": datetime.now(tz=TZ).isoformat(),
            }
        ).eq("id", b["id"]).execute()
        n += 1
        _safe_print(
            f"[agenda] {payload['data_inizio']} {payload['ora']} {payload['tipo']} - {payload['titolo'][:50]}"
        )
        if args.max and n >= args.max:
            break

    _safe_print(f"OK: {n} righe in pianificazioni (skip {skipped}). Cron: publish_from_agenda.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
