"""
Genera bozze social: 3 invii/settimana per sezione (immobile, blog, landing, agenzia).
Spintax + minimo 10 hashtag. Lun/mer/ven — no sab/dom.

Uso:
  python genera_bozze_settimanali.py
  python genera_bozze_settimanali.py --dry-run
  python genera_bozze_settimanali.py --programma-agenda
  python genera_bozze_settimanali.py --settimane 2
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

TEMPLATES_PATH = ROOT / "templates" / "social_sezioni.json"
POSTS_PER_SECTION = 3
SECTIONS = ("immobile", "blog", "landing", "agenzia")

RSS_FEEDS = [
    ("Sole 24 Ore", "https://www.ilsole24ore.com/rss/economia.xml"),
    ("Agenzia delle Entrate", "https://www.agenziaentrate.gov.it/wps/content/Nsilib/NPI/IT/Comunicati/rss"),
]

WEEKDAY_SLOTS = (0, 2, 4)  # lun=0, mer=2, ven=4 (Python weekday)


def load_templates() -> dict[str, Any]:
    with TEMPLATES_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def resolve_image_url(url: str, supabase_url: str) -> str:
    u = (url or "").strip()
    if not u:
        return ""
    if u.startswith(("http://", "https://")):
        return u
    path = u.lstrip("/")
    if path.startswith("foto-immobili/"):
        return f"{supabase_url.rstrip('/')}/storage/v1/object/public/{path}"
    return f"{BASE_SITE.rstrip('/')}/{path}"


def apply_pattern(pattern: str, ctx: dict[str, str]) -> str:
    out = pattern
    for k, v in ctx.items():
        out = out.replace("{" + k + "}", v)
    return out


def pick_rotating(pool: list[dict], index: int) -> dict | None:
    if not pool:
        return None
    return pool[index % len(pool)]


def week_monday_on_or_after(d: date) -> date:
    cursor = d
    while cursor.weekday() != 0:
        cursor += timedelta(days=1)
    return cursor


def immobile_photos(i: dict, supabase_url: str) -> list[str]:
    urls: list[str] = []
    val = i.get("foto")
    if isinstance(val, list):
        for u in val:
            abs_u = resolve_image_url(str(u), supabase_url)
            if abs_u and abs_u not in urls:
                urls.append(abs_u)
    return urls[:4]


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
    hashtags: list[str],
    media_url: str | None = None,
    meta: dict | None = None,
) -> dict[str, Any]:
    return {
        "stato": "bozza",
        "tipo_canale": tipo_canale,
        "fonte": fonte,
        "titolo": titolo[:220],
        "corpo": corpo,
        "hashtags": hashtags,
        "link_pagina": link,
        "media_direct_url": media_url,
        "riferimento_id": ref,
        "data_pubblicazione_proposta": slot_date.isoformat(),
        "ora_proposta": ora,
        "note": "Generato da genera_bozze_settimanali.py — approva in Admin → Social",
        "meta": meta or {},
        "updated_at": datetime.now(tz=TZ).isoformat(),
    }


def build_section_bozze(
    section: str,
    tpl: dict[str, Any],
    *,
    week_monday: date,
    week_index: int,
    imm: list[dict],
    blog: list[dict],
    land: list[dict],
    supabase_url: str,
) -> list[dict[str, Any]]:
    sec = tpl.get(section) or {}
    canali = sec.get("canali_settimana") or []
    tags = list(sec.get("hashtags") or [])[:15]
    if len(tags) < 10:
        raise RuntimeError(f"Sezione {section}: servono almeno 10 hashtag nel template")

    titoli_p = sec.get("titoli_spintax") or ["{titolo}"]
    corpi_p = sec.get("corpo_spintax") or ["{titolo}"]

    bozze: list[dict[str, Any]] = []
    link = ""
    ref: str | None = None
    media_url: str | None = None
    ctx: dict[str, str] = {
        "titolo": "Righetto Immobiliare",
        "zona": "Padova",
        "dettaglio": "",
        "pagina": "il sito",
    }

    if section == "immobile":
        row = pick_rotating(
            [i for i in imm if i.get("attivo")], week_index
        ) or pick_immobile(imm)
        if not row:
            return []
        link = f"{BASE_SITE}/immobile?s={slug_immobile(row)}"
        ref = str(row.get("id") or "")
        ctx["titolo"] = str(row.get("titolo") or "Immobile")
        ctx["zona"] = str(row.get("zona") or row.get("comune") or "Padova")
        prezzo = row.get("prezzo")
        ctx["dettaglio"] = (
            f"da € {int(prezzo):,}".replace(",", ".") if prezzo else "su richiesta"
        )
        photos = immobile_photos(row, supabase_url)
        if photos:
            media_url = photos[0]

    elif section == "blog":
        row = pick_rotating(
            [b for b in blog if (b.get("stato") or "") == "pubblicato"], week_index
        ) or pick_blog(blog)
        if not row:
            return []
        slug = row.get("slug") or row.get("url_statico") or ""
        link = f"{BASE_SITE}/blog-articolo?s={slug}"
        ref = str(row.get("id") or "")
        ctx["titolo"] = str(row.get("titolo") or "Articolo")
        media_url = resolve_image_url(
            str(row.get("immagine_copertina") or ""), supabase_url
        ) or None

    elif section == "landing":
        rows = [p for p in land if (p.get("stato") or "") != "bozza"]
        row = pick_rotating(rows, week_index) or pick_landing(land)
        if not row:
            return []
        path = row.get("url") or f"/{row.get('slug', '')}"
        if not str(path).startswith("/"):
            path = "/" + str(path)
        link = BASE_SITE.rstrip("/") + path
        ref = str(row.get("id") or "")
        ctx["titolo"] = str(row.get("titolo") or "Landing")
        ctx["pagina"] = ctx["titolo"]

    elif section == "agenzia":
        pages = tpl.get("pagine_agenzia") or []
        pg = pages[week_index % len(pages)] if pages else {"path": "/", "titolo": "Home"}
        path = pg.get("path", "/")
        link = BASE_SITE.rstrip("/") + (path if path.startswith("/") else "/" + path)
        ctx["titolo"] = str(pg.get("titolo") or "Righetto Immobiliare")
        ctx["pagina"] = ctx["titolo"]
        ref = None

    for slot in canali[:POSTS_PER_SECTION]:
        off = int(slot.get("giorno_offset", 0))
        slot_date = week_monday + timedelta(days=off)
        if slot_date.weekday() not in WEEKDAY_SLOTS:
            continue
        tipo = slot.get("tipo") or "facebook_post"
        titolo = apply_pattern(titoli_p[week_index % len(titoli_p)], ctx)
        corpo = apply_pattern(corpi_p[week_index % len(corpi_p)], ctx)
        corpo += "\n\n" + " ".join(tags)

        mv = media_url
        if tipo == "instagram_reel":
            mv = None

        bozze.append(
            make_bozza(
                slot_date=slot_date,
                ora=str(slot.get("ora") or "12:30"),
                tipo_canale=tipo,
                fonte=section,
                titolo=titolo,
                corpo=corpo,
                link=link,
                ref=ref,
                hashtags=tags,
                media_url=mv,
                meta={"settimana": week_index, "video_auto": tipo == "instagram_reel"},
            )
        )
    return bozze


def build_bozze_list(
    imm: list[dict],
    blog: list[dict],
    land: list[dict],
    _rss: list[dict[str, str]],
    *,
    settimane: int = 1,
) -> list[dict[str, Any]]:
    tpl = load_templates()
    supabase_url = env_or_empty("SUPABASE_URL") or BASE_SITE
    today = datetime.now(tz=TZ).date()
    start_monday = week_monday_on_or_after(today + timedelta(days=1))

    all_bozze: list[dict[str, Any]] = []
    for w in range(settimane):
        monday = start_monday + timedelta(days=7 * w)
        for section in SECTIONS:
            all_bozze.extend(
                build_section_bozze(
                    section,
                    tpl,
                    week_monday=monday,
                    week_index=w,
                    imm=imm,
                    blog=blog,
                    land=land,
                    supabase_url=supabase_url,
                )
            )

    if len(all_bozze) < 8:
        print(
            f"Attenzione: generate solo {len(all_bozze)} bozze (minimo consigliato 8).",
            file=sys.stderr,
        )
    return all_bozze


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Anteprima JSON; senza .env usa dati demo",
    )
    parser.add_argument(
        "--settimane",
        type=int,
        default=1,
        help="Settimane da pianificare (default 1 = 12 bozze)",
    )
    parser.add_argument(
        "--programma-agenda",
        action="store_true",
        help="Dopo insert, crea righe in pianificazioni (min 8)",
    )
    args = parser.parse_args()
    load_env()

    try:
        imm, blog, land = load_content_sources(dry_run=args.dry_run)
        rss = fetch_rss_titles()
        bozze = build_bozze_list(imm, blog, land, rss, settimane=max(1, args.settimane))
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
        print(
            f"OK: {saved_db} bozze (12/settimana: 3× immobile, blog, landing, agenzia). "
            "Admin > Social > Approva."
        )
        if args.programma_agenda:
            import subprocess

            r = subprocess.run(
                [sys.executable, str(ROOT / "programma_da_bozze.py"), "--min", "8"],
                cwd=str(ROOT),
            )
            return r.returncode
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
