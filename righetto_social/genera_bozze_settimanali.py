"""
Genera 3 bozze/settimana (lun, mer, ven) senza API AI a pagamento.
Fonti: Supabase immobili/blog/landing + titoli RSS istituzionali (solo titolo+link).

Uso:
  python genera_bozze_settimanali.py
  python genera_bozze_settimanali.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from postgrest.exceptions import APIError
from supabase import create_client

ROOT = Path(__file__).resolve().parent
BASE_SITE = "https://righettoimmobiliare.it"
TZ = ZoneInfo("Europe/Rome")

HASHTAGS_BASE = [
    "#padova",
    "#immobiliare",
    "#righettoimmobiliare",
    "#consulenzaimmobiliare",
    "#venditacasa",
    "#investimentiimmobiliari",
]

RSS_FEEDS = [
    ("Sole 24 Ore", "https://www.ilsole24ore.com/rss/economia.xml"),
    ("Agenzia delle Entrate", "https://www.agenziaentrate.gov.it/wps/content/Nsilib/NPI/IT/Comunicati/rss"),
]

PEAK_HOURS = ["09:45", "12:30", "18:45"]
WEEKDAY_SLOTS = (0, 2, 4)  # lun=0, mer=2, ven=4 (Python weekday)


def load_env() -> None:
    load_dotenv(ROOT / ".env")


def env_or_empty(name: str) -> str:
    return os.environ.get(name, "").strip()


def req_env(name: str) -> str:
    v = env_or_empty(name)
    if not v:
        print(f"Manca {name} nel file .env", file=sys.stderr)
        if name == "SUPABASE_KEY":
            print(
                "  → Supabase → Project Settings → API → copia "
                "'service_role' (server) oppure 'anon' (solo test).\n"
                "  → Incolla in .env accanto a SUPABASE_URL=https://TUO-PROGETTO.supabase.co",
                file=sys.stderr,
            )
        sys.exit(2)
    return v


def sb():
    return create_client(req_env("SUPABASE_URL"), req_env("SUPABASE_KEY"))


def demo_content() -> tuple[list[dict], list[dict], list[dict]]:
    """Dati fittizi per --dry-run senza credenziali Supabase."""
    return (
        [
            {
                "id": "demo-imm",
                "codice": "DEMO1",
                "titolo": "Trilocale zona Galileo (demo)",
                "zona": "Padova",
                "attivo": True,
            }
        ],
        [
            {
                "id": "demo-blog",
                "slug": "mutuo-prima-casa-padova",
                "titolo": "Mutuo prima casa Padova (demo)",
                "stato": "pubblicato",
            }
        ],
        [
            {
                "id": "demo-land",
                "slug": "landing-consulenza-immobiliare-gratuita",
                "titolo": "Consulenza gratuita (demo)",
                "url": "/landing-consulenza-immobiliare-gratuita.html",
                "stato": "pubblicata",
            }
        ],
    )


def load_content_sources(*, dry_run: bool) -> tuple[list[dict], list[dict], list[dict]]:
    url = env_or_empty("SUPABASE_URL")
    key = env_or_empty("SUPABASE_KEY")
    if not url or not key:
        if dry_run:
            print(
                "[dry-run] SUPABASE_URL/SUPABASE_KEY assenti — uso dati demo.",
                file=sys.stderr,
            )
            return demo_content()
        req_env("SUPABASE_URL")
        req_env("SUPABASE_KEY")

    client = sb()
    imm = (
        client.table("immobili")
        .select("*")
        .order("created_at", desc=True)
        .limit(40)
        .execute()
    ).data or []
    blog = _fetch_ordered(client, "blog", ("data_pubblicazione", "data", "created_at"), 30)
    land = _fetch_ordered(
        client, "landing_pages", ("data_pubblicazione", "created_at"), 20
    )
    return imm, blog, land


def _fetch_ordered(
    client: Any, table: str, order_cols: tuple[str, ...], limit: int
) -> list[dict]:
    last_err: Exception | None = None
    for col in order_cols:
        try:
            return (
                client.table(table)
                .select("*")
                .order(col, desc=True)
                .limit(limit)
                .execute()
            ).data or []
        except APIError as e:
            last_err = e
            if "does not exist" not in str(e):
                raise
    try:
        return client.table(table).select("*").limit(limit).execute().data or []
    except APIError:
        if last_err:
            raise last_err
        raise


def next_weekday_slots(from_day: date, count: int = 3) -> list[date]:
    out: list[date] = []
    cursor = from_day
    while len(out) < count:
        if cursor.weekday() in WEEKDAY_SLOTS:
            out.append(cursor)
        cursor += timedelta(days=1)
        if (cursor - from_day).days > 21:
            break
    return out


def fetch_rss_titles(max_items: int = 8) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for fonte, url in RSS_FEEDS:
        try:
            req = Request(url, headers={"User-Agent": "RighettoSocialBot/1.0"})
            with urlopen(req, timeout=15) as resp:
                raw = resp.read()
            root = ET.fromstring(raw)
            for item in root.iter("item"):
                title_el = item.find("title")
                link_el = item.find("link")
                if title_el is None or not (title_el.text or "").strip():
                    continue
                link = (link_el.text if link_el is not None else "").strip() or url
                items.append(
                    {
                        "fonte": fonte,
                        "titolo": title_el.text.strip()[:200],
                        "link": link,
                    }
                )
                if len(items) >= max_items:
                    return items
        except Exception as e:
            print(f"RSS skip {fonte}: {e}", file=sys.stderr)
    return items


def pick_immobile(rows: list[dict]) -> dict | None:
    active = [
        r
        for r in rows
        if r.get("attivo") and str(r.get("stato", "")).lower() not in ("venduto", "affittato")
    ]
    if not active:
        active = rows
    if not active:
        return None
    active.sort(key=lambda x: x.get("created_at") or "", reverse=True)
    return active[0]


def pick_blog(rows: list[dict]) -> dict | None:
    pub = [r for r in rows if (r.get("stato") or "pubblicato") == "pubblicato"]
    if not pub:
        pub = rows
    if not pub:
        return None
    pub.sort(
        key=lambda x: x.get("data_pubblicazione") or x.get("data") or x.get("created_at") or "",
        reverse=True,
    )
    return pub[0]


def pick_landing(rows: list[dict]) -> dict | None:
    pub = [r for r in rows if (r.get("stato") or "") != "bozza"]
    if not pub:
        return None
    pub.sort(
        key=lambda x: x.get("data_pubblicazione") or x.get("created_at") or "",
        reverse=True,
    )
    return pub[0]


def slug_immobile(i: dict) -> str:
    tit = (i.get("titolo") or "immobile").lower()
    tit = re.sub(r"[^a-z0-9]+", "-", tit).strip("-")[:80]
    cod = (i.get("codice") or i.get("id") or "")[:12]
    return f"{tit}-{cod}" if cod else tit


def make_bozza(
    *,
    slot_date: date,
    ora: str,
    tipo_canale: str,
    fonte: str,
    titolo: str,
    corpo: str,
    link: str,
    ref: str | None,
    media_url: str | None = None,
    meta: dict | None = None,
) -> dict[str, Any]:
    return {
        "stato": "bozza",
        "tipo_canale": tipo_canale,
        "fonte": fonte,
        "titolo": titolo[:220],
        "corpo": corpo,
        "hashtags": HASHTAGS_BASE,
        "link_pagina": link,
        "media_direct_url": media_url,
        "riferimento_id": ref,
        "data_pubblicazione_proposta": slot_date.isoformat(),
        "ora_proposta": ora,
        "note": "Generato da genera_bozze_settimanali.py — approva in Admin → Social",
        "meta": meta or {},
        "updated_at": datetime.now(tz=TZ).isoformat(),
    }


def build_bozze_list(
    imm: list[dict], blog: list[dict], land: list[dict], rss: list[dict[str, str]]
) -> list[dict[str, Any]]:
    today = datetime.now(tz=TZ).date()
    start = today + timedelta(days=1)
    slots = next_weekday_slots(start, 3)
    if len(slots) < 3:
        raise RuntimeError("Impossibile trovare 3 giorni lun/mer/ven nel prossimo mese.")

    bozze: list[dict[str, Any]] = []

    i_row = pick_immobile(imm)
    if i_row:
        link = f"{BASE_SITE}/immobile?s={slug_immobile(i_row)}"
        tit = f"🏠 {i_row.get('titolo', 'Nuovo incarico')}"
        corpo = (
            "{Scopri questo immobile a Padova|In esclusiva a Padova}: "
            f"{i_row.get('zona', 'zona centrale')}. "
            "{Richiedi informazioni|Prenota una visita} in agenzia.\n\n"
            + " ".join(HASHTAGS_BASE[:6])
        )
        bozze.append(
            make_bozza(
                slot_date=slots[0],
                ora=PEAK_HOURS[0],
                tipo_canale="instagram_feed",
                fonte="immobile",
                titolo=tit,
                corpo=corpo,
                link=link,
                ref=str(i_row.get("id") or ""),
            )
        )

    l_row = pick_landing(land)
    if l_row:
        path = l_row.get("url") or f"/{l_row.get('slug', '')}"
        if not str(path).startswith("/"):
            path = "/" + str(path)
        link = BASE_SITE.rstrip("/") + path
        tit = f"📋 {l_row.get('titolo', 'Landing')}"
        corpo = (
            "{Consulenza dedicata|Servizio su misura} — "
            f"{l_row.get('titolo', 'approfondimento')}.\n"
            f"Link: {link}\n\n" + " ".join(HASHTAGS_BASE)
        )
        bozze.append(
            make_bozza(
                slot_date=slots[1],
                ora=PEAK_HOURS[1],
                tipo_canale="facebook_post",
                fonte="landing",
                titolo=tit,
                corpo=corpo,
                link=link,
                ref=str(l_row.get("id") or ""),
            )
        )

    b_row = pick_blog(blog)
    news = rss[0] if rss else None
    reel_link = BASE_SITE + "/landing-consulenza-immobiliare-gratuita.html"
    reel_fonte = "landing"
    reel_ref: str | None = str(l_row.get("id") or "") if l_row else None
    reel_titolo_extra = ""
    if i_row:
        reel_fonte = "immobile"
        reel_ref = str(i_row.get("id") or "")
        reel_link = f"{BASE_SITE}/immobile?s={slug_immobile(i_row)}"
        reel_titolo_extra = f" · {i_row.get('titolo', '')[:80]}"
    elif b_row:
        reel_fonte = "blog"
        reel_ref = str(b_row.get("id") or "")
        slug = b_row.get("slug") or ""
        reel_link = f"{BASE_SITE}/blog-articolo?s={slug}"
        reel_titolo_extra = f" · {b_row.get('titolo', '')[:80]}"
    elif l_row:
        path = l_row.get("url") or f"/{l_row.get('slug', '')}"
        if not str(path).startswith("/"):
            path = "/" + str(path)
        reel_link = BASE_SITE.rstrip("/") + path
        reel_titolo_extra = f" · {l_row.get('titolo', '')[:80]}"
    elif news:
        reel_titolo_extra = f" · {news['titolo'][:80]}"
        reel_link = news["link"]
        reel_fonte = "notizia_esterna"

    reel = make_bozza(
        slot_date=slots[2],
        ora="07:15",
        tipo_canale="instagram_reel",
        fonte=reel_fonte,
        titolo=(
            "{Il mercato a Padova|La tua casa vale più di quanto pensi}: "
            "consulenza gratuita" + reel_titolo_extra
        ),
        corpo=(
            "MP4 generato automaticamente dalle foto del contenuto.\n"
            "CTA: Prenota la tua consulenza gratuita — 049 8755543\n\n"
            + " ".join(HASHTAGS_BASE)
        ),
        link=reel_link,
        ref=reel_ref,
        meta={
            "video_auto": True,
            "durata_target_sec": "10-15",
            "notizia_rss": news,
        },
    )
    bozze.append(reel)
    return bozze


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Anteprima JSON; senza .env usa dati demo",
    )
    args = parser.parse_args()
    load_env()

    try:
        imm, blog, land = load_content_sources(dry_run=args.dry_run)
        rss = fetch_rss_titles()
        bozze = build_bozze_list(imm, blog, land, rss)
    except RuntimeError as e:
        print(e, file=sys.stderr)
        return 1

    if args.dry_run:
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass
        print(json.dumps(bozze, ensure_ascii=False, indent=2))
        return 0

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

    client = sb()
    out_dir = ROOT / "content" / "bozze_generate"
    saved_db = 0
    saved_file = 0
    table_missing = False

    gen_reel = os.environ.get("GENERA_REEL_AUTO", "1").strip() not in ("0", "false", "no")

    for b in bozze:
        inserted_row: dict[str, Any] | None = None
        try:
            ins = client.table("bozze_social").insert(b).execute()
            inserted_row = (ins.data or [None])[0]
            saved_db += 1
            tit_safe = b["titolo"][:60].encode("ascii", "replace").decode("ascii")
            print(f"[Supabase] {tit_safe} ({b['data_pubblicazione_proposta']})")
            if (
                gen_reel
                and b.get("tipo_canale") == "instagram_reel"
                and inserted_row
            ):
                try:
                    from genera_reel import find_ffmpeg, process_bozza

                    process_bozza(client, inserted_row, ffmpeg=find_ffmpeg())
                except Exception as reel_err:
                    print(f"[reel] Non generato: {reel_err}", file=sys.stderr)
        except APIError as e:
            if "bozze_social" in str(e) and ("PGRST205" in str(e) or "does not exist" in str(e)):
                table_missing = True
                out_dir.mkdir(parents=True, exist_ok=True)
                stamp = datetime.now(tz=TZ).strftime("%Y%m%d_%H%M%S")
                fname = f"bozza_{stamp}_{saved_file}.json"
                (out_dir / fname).write_text(
                    json.dumps(b, ensure_ascii=False, indent=2), encoding="utf-8"
                )
                saved_file += 1
                print(f"[file] content/bozze_generate/{fname}")
            else:
                raise

    if saved_db:
        print(f"OK: {saved_db} bozze in Supabase. Admin > Social > Approva.")
    if saved_file:
        print(
            f"OK: {saved_file} bozze in content/bozze_generate/.\n"
            "Esegui sql/bozze-social.sql su Supabase, poi rilancia lo script "
            "oppure Admin > Social > Genera bozze settimanali."
        )
    if table_missing and not saved_db:
        print("Tabella bozze_social assente: vedi sql/bozze-social.sql", file=sys.stderr)
    return 0 if (saved_db or saved_file) else 1


if __name__ == "__main__":
    sys.exit(main())
