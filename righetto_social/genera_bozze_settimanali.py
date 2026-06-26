"""
Genera bozze social: 3 invii/settimana per sezione (immobile, blog, landing, agenzia),
ogni slot = contenuto diverso in rotazione su tutto il catalogo sito; a fine giro ricomincia.
+ 2 notizie/settimana da RSS (Sole 24 Ore, Agenzia Entrate, Milano Finanza) con testo
originale (no copiatura) e titoli SEO Padova/immobiliare.

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
    (
        "Agenzia delle Entrate",
        "https://www.agenziaentrate.gov.it/wps/content/Nsilib/NPI/IT/Comunicati/rss",
    ),
    (
        "Milano Finanza",
        "https://news.google.com/rss/search?q=site:milanofinanza.it+(immobili+OR+casa+OR+mutuo+OR+fisco+OR+affitti)&hl=it&gl=IT&ceid=IT:it",
    ),
]

NOTIZIA_POSTS_PER_WEEK = 2
RSS_RELEVANCE = re.compile(
    r"immobil|casa|mutuo|affitt|locaz|credito|mercato|impost|fisco|ediliz|"
    r"costruz|ipotec|acquisto|vendit|locazione|bonus|cedolari|tasse|finanz|"
    r"propriet|abitaz|condomin|rendita|catast|superbonus|ecobonus",
    re.I,
)

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


def pick_rotating_batch(pool: list[dict], start: int, count: int) -> list[dict | None]:
    """Prossimi `count` elementi dal pool ordinato; a fine lista ricomincia da capo."""
    if not pool:
        return [None] * count
    return [pool[(start + i) % len(pool)] for i in range(count)]


def filter_active_immobili(rows: list[dict]) -> list[dict]:
    return [
        r
        for r in rows
        if r.get("attivo") is not False
        and str(r.get("stato", "")).lower() not in ("venduto", "affittato")
    ]


def stable_sort_immobili(pool: list[dict]) -> list[dict]:
    return sorted(
        pool,
        key=lambda x: (
            str(x.get("codice") or "").strip().upper(),
            str(x.get("id") or ""),
        ),
    )


def rotation_pool_blog(rows: list[dict]) -> list[dict]:
    pub = [r for r in rows if (r.get("stato") or "pubblicato") == "pubblicato"]
    pub.sort(
        key=lambda x: str(
            x.get("slug") or x.get("url_statico") or x.get("id") or ""
        ).lower(),
    )
    return pub


def rotation_pool_landing(rows: list[dict]) -> list[dict]:
    pub = [r for r in rows if (r.get("stato") or "") != "bozza"]
    pub.sort(key=lambda x: str(x.get("slug") or x.get("url") or x.get("id") or "").lower())
    return pub


def rotation_cursor(client: Any | None, section: str) -> int:
    """
    Indice prossimo slot nel pool: conta bozze già generate per la sezione
    (ciclo completo = len(pool) slot per tipo, poi riparte da 0).
    """
    if client is None:
        return 0
    try:
        res = (
            client.table("bozze_social")
            .select("id")
            .eq("fonte", section)
            .neq("stato", "rifiutata")
            .execute()
        )
        n = len(res.data or [])
        if section == "immobile":
            res2 = (
                client.table("pianificazioni")
                .select("id,note")
                .eq("contenuto", "immobile")
                .execute()
            )
            for p in res2.data or []:
                if "[DA_BOZZA]" not in (p.get("note") or ""):
                    n += 1
        elif section == "blog":
            res2 = (
                client.table("pianificazioni")
                .select("id,note")
                .eq("contenuto", "articolo")
                .execute()
            )
            for p in res2.data or []:
                if "[DA_BOZZA]" not in (p.get("note") or ""):
                    n += 1
        elif section == "landing":
            res2 = (
                client.table("pianificazioni")
                .select("id,note")
                .eq("contenuto", "landing")
                .execute()
            )
            for p in res2.data or []:
                if "[DA_BOZZA]" not in (p.get("note") or ""):
                    n += 1
        elif section == "agenzia":
            res2 = (
                client.table("pianificazioni")
                .select("id,note")
                .eq("contenuto", "pagina_agenzia")
                .execute()
            )
            for p in res2.data or []:
                if "[DA_BOZZA]" not in (p.get("note") or ""):
                    n += 1
        return n
    except APIError:
        return 0


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
                "id": "demo-imm-1",
                "codice": "DEMO1",
                "titolo": "Trilocale zona Galileo (demo)",
                "zona": "Padova",
                "attivo": True,
            },
            {
                "id": "demo-imm-2",
                "codice": "DEMO2",
                "titolo": "Bilocale centro (demo)",
                "zona": "Padova",
                "attivo": True,
            },
            {
                "id": "demo-imm-3",
                "codice": "DEMO3",
                "titolo": "Villa Mandria (demo)",
                "zona": "Mandria",
                "attivo": True,
            },
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


def _fetch_paginated(
    client: Any,
    table: str,
    *,
    filters: list[tuple[str, str, Any]] | None = None,
    order_col: str = "codice",
    page_size: int = 200,
) -> list[dict]:
    out: list[dict] = []
    start = 0
    while True:
        q = client.table(table).select("*")
        for col, op, val in filters or []:
            if op == "eq":
                q = q.eq(col, val)
        q = q.order(order_col).range(start, start + page_size - 1)
        batch = (q.execute()).data or []
        out.extend(batch)
        if len(batch) < page_size:
            break
        start += page_size
    return out


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
    imm = _fetch_paginated(
        client,
        "immobili",
        filters=[("attivo", "eq", True)],
        order_col="codice",
    )
    if not imm:
        imm = _fetch_paginated(client, "immobili", order_col="codice")
    blog = _fetch_ordered(client, "blog", ("data_pubblicazione", "data", "created_at"), 500)
    land = _fetch_ordered(
        client, "landing_pages", ("data_pubblicazione", "created_at"), 100
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


def _parse_rss_items(raw: bytes, fonte: str, source_url: str) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    try:
        root = ET.fromstring(raw)
        for item in root.iter("item"):
            title_el = item.find("title")
            link_el = item.find("link")
            if title_el is None or not (title_el.text or "").strip():
                continue
            link = (link_el.text if link_el is not None else "").strip() or source_url
            out.append(
                {
                    "fonte": fonte,
                    "titolo": title_el.text.strip()[:200],
                    "link": link,
                }
            )
        if out:
            return out
    except ET.ParseError:
        pass
    text = raw.decode("utf-8", "replace")
    for block in re.findall(r"<item\b[^>]*>(.*?)</item>", text, re.I | re.S):
        tm = re.search(r"<title[^>]*>(.*?)</title>", block, re.I | re.S)
        if not tm:
            continue
        title = re.sub(r"<[^>]+>", "", tm.group(1))
        title = re.sub(r"\s+", " ", title).strip()
        if not title:
            continue
        lm = re.search(r"<link[^>]*>(.*?)</link>", block, re.I | re.S)
        link = source_url
        if lm:
            link = re.sub(r"<[^>]+>", "", lm.group(1)).strip() or source_url
        out.append({"fonte": fonte, "titolo": title[:200], "link": link})
    return out


def fetch_rss_titles(max_items: int = 40) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    seen_links: set[str] = set()
    for fonte, url in RSS_FEEDS:
        try:
            req = Request(url, headers={"User-Agent": "RighettoSocialBot/1.0"})
            with urlopen(req, timeout=20) as resp:
                raw = resp.read()
            for row in _parse_rss_items(raw, fonte, url):
                lk = row["link"].split("#")[0].rstrip("/")
                if lk in seen_links:
                    continue
                seen_links.add(lk)
                items.append(row)
        except Exception as e:
            print(f"RSS skip {fonte}: {e}", file=sys.stderr)
    return items[:max_items]


def filter_rss_immobiliare(items: list[dict[str, str]]) -> list[dict[str, str]]:
    out = [i for i in items if RSS_RELEVANCE.search(i.get("titolo") or "")]
    return out or items[:12]


def shorten_theme(original: str, *, max_len: int = 72) -> str:
    t = re.sub(r"\s+", " ", (original or "").strip())
    t = re.sub(r"^[\W\d]+", "", t)
    if len(t) <= max_len:
        return t
    cut = t[: max_len - 1].rsplit(" ", 1)[0]
    return (cut or t[:max_len]).strip() + "…"


def rework_news_title(original: str, fonte: str, variant: int) -> tuple[str, str]:
    tema = shorten_theme(original)
    patterns = [
        "{Mercato immobiliare Padova|Casa e finanza a Padova}: {tema}",
        "{Imposte e casa Padova|Fisco e immobili a Padova}: {tema}",
        "{Consulenza immobiliare Padova|Padova e provincia}: {tema}",
    ]
    titolo = apply_pattern(
        patterns[variant % len(patterns)],
        {"tema": tema, "fonte": fonte},
    )
    return titolo[:220], tema


def _shift_ora(ora: str, minutes: int) -> str:
    parts = (ora or "12:00").split(":")
    h = int(parts[0]) if parts else 12
    m = int(parts[1]) if len(parts) > 1 else 0
    total = h * 60 + m + minutes
    return f"{(total // 60) % 24:02d}:{total % 60:02d}"


def build_notizia_bozze(
    rss_items: list[dict[str, str]],
    tpl: dict[str, Any],
    *,
    week_monday: date,
    week_index: int,
    used_links: set[str],
) -> list[dict[str, Any]]:
    sec = tpl.get("notizia_esterna") or {}
    if not sec:
        return []
    tags = list(sec.get("hashtags") or [])[:15]
    if len(tags) < 10:
        raise RuntimeError("Sezione notizia_esterna: servono almeno 10 hashtag nel template")
    titoli_p = sec.get("titoli_spintax") or ["{tema}"]
    corpi_p = sec.get("corpo_spintax") or ["{tema}"]
    slots = sec.get("slot_settimana") or [
        {"giorno_offset": 1, "ora": "10:30"},
        {"giorno_offset": 3, "ora": "11:00"},
    ]
    canali = sec.get("canali") or ["facebook_post", "google"]

    pool = filter_rss_immobiliare(rss_items)
    picked: list[dict[str, str]] = []
    start = week_index * NOTIZIA_POSTS_PER_WEEK
    for item in pool[start:] + pool:
        lk = (item.get("link") or "").split("#")[0].rstrip("/")
        if not lk or lk in used_links:
            continue
        picked.append(item)
        used_links.add(lk)
        if len(picked) >= NOTIZIA_POSTS_PER_WEEK:
            break

    bozze: list[dict[str, Any]] = []
    for idx, item in enumerate(picked):
        slot = slots[idx % len(slots)]
        off = int(slot.get("giorno_offset", 1))
        slot_date = week_monday + timedelta(days=off)
        ora_base = str(slot.get("ora") or "10:30")
        titolo, tema = rework_news_title(
            item["titolo"], item["fonte"], week_index + idx
        )
        ctx = {
            "tema": tema,
            "fonte": item["fonte"],
            "link_esterno": item["link"],
        }
        corpo_base = apply_pattern(corpi_p[(week_index + idx) % len(corpi_p)], ctx)
        corpo_base += "\n\n" + " ".join(tags)
        for ch_idx, tipo in enumerate(canali):
            ora = _shift_ora(ora_base, ch_idx * 5)
            bozze.append(
                make_bozza(
                    slot_date=slot_date,
                    ora=ora,
                    tipo_canale=tipo,
                    fonte="notizia_esterna",
                    titolo=titolo,
                    corpo=corpo_base,
                    link=item["link"],
                    ref=None,
                    hashtags=tags,
                    media_url=None,
                    meta={
                        "settimana": week_index,
                        "rss_link": item["link"],
                        "rss_titolo_originale": item["titolo"][:160],
                        "rss_fonte": item["fonte"],
                    },
                )
            )
    return bozze


def _existing_rss_links(client: Any, from_iso: str, to_iso: str) -> set[str]:
    links: set[str] = set()
    try:
        res = (
            client.table("bozze_social")
            .select("meta,stato")
            .eq("fonte", "notizia_esterna")
            .gte("data_pubblicazione_proposta", from_iso)
            .lte("data_pubblicazione_proposta", to_iso)
            .execute()
        )
    except APIError:
        return links
    for row in res.data or []:
        if (row.get("stato") or "") == "rifiutata":
            continue
        meta = row.get("meta") or {}
        lk = (meta.get("rss_link") or "").split("#")[0].rstrip("/")
        if lk:
            links.add(lk)
    return links


_SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
from righetto_immobile_slug import generate_property_slug, share_immobile_url


def slug_immobile(i: dict) -> str:
    """Slug SEO (tipologia-operazione-comune-codice) — allineato al sito."""
    return generate_property_slug(i)


def link_immobile_social(i: dict) -> str:
    """URL per anteprima Facebook/WhatsApp (OG statico)."""
    return share_immobile_url(generate_property_slug(i))


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


def _ctx_from_immobile(row: dict, supabase_url: str) -> tuple[dict[str, str], str, str | None, str | None]:
    link = link_immobile_social(row)
    ref = str(row.get("id") or "")
    prezzo = row.get("prezzo")
    dettaglio = (
        f"da € {int(prezzo):,}".replace(",", ".") if prezzo else "su richiesta"
    )
    ctx = {
        "titolo": str(row.get("titolo") or "Immobile"),
        "zona": str(row.get("zona") or row.get("comune") or "Padova"),
        "dettaglio": dettaglio,
        "pagina": "il sito",
        "link": link,
    }
    photos = immobile_photos(row, supabase_url)
    media = photos[0] if photos else None
    return ctx, link, ref, media


def _ctx_from_blog(row: dict, supabase_url: str) -> tuple[dict[str, str], str, str | None, str | None]:
    slug = row.get("slug") or row.get("url_statico") or ""
    link = f"{BASE_SITE}/blog-articolo?s={slug}"
    ref = str(row.get("id") or "")
    ctx = {
        "titolo": str(row.get("titolo") or "Articolo"),
        "zona": "Padova",
        "dettaglio": "",
        "pagina": "il sito",
        "link": link,
    }
    media = resolve_image_url(str(row.get("immagine_copertina") or ""), supabase_url) or None
    return ctx, link, ref, media


def _ctx_from_landing(row: dict) -> tuple[dict[str, str], str, str | None, str | None]:
    path = row.get("url") or f"/{row.get('slug', '')}"
    if not str(path).startswith("/"):
        path = "/" + str(path)
    link = BASE_SITE.rstrip("/") + path
    ref = str(row.get("id") or "")
    tit = str(row.get("titolo") or "Landing")
    ctx = {"titolo": tit, "zona": "Padova", "dettaglio": "", "pagina": tit}
    return ctx, link, ref, None


def _ctx_from_agenzia(pg: dict) -> tuple[dict[str, str], str, str | None, str | None]:
    path = pg.get("path", "/")
    link = BASE_SITE.rstrip("/") + (path if str(path).startswith("/") else "/" + str(path))
    tit = str(pg.get("titolo") or "Righetto Immobiliare")
    ctx = {"titolo": tit, "zona": "Padova", "dettaglio": "", "pagina": tit}
    return ctx, link, None, None


def build_section_bozze(
    section: str,
    tpl: dict[str, Any],
    *,
    week_monday: date,
    week_index: int,
    rotation_start: int,
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

    slots = canali[:POSTS_PER_SECTION]
    n_slots = len(slots)

    if section == "immobile":
        pool = stable_sort_immobili(filter_active_immobili(imm))
    elif section == "blog":
        pool = rotation_pool_blog(blog)
    elif section == "landing":
        pool = rotation_pool_landing(land)
    elif section == "agenzia":
        pool = list(tpl.get("pagine_agenzia") or [])
    else:
        pool = []

    if not pool:
        return []

    batch = pick_rotating_batch(pool, rotation_start, n_slots)
    bozze: list[dict[str, Any]] = []

    for slot_idx, slot in enumerate(slots):
        row = batch[slot_idx]
        if not row:
            continue

        if section == "immobile":
            ctx, link, ref, media_url = _ctx_from_immobile(row, supabase_url)
        elif section == "blog":
            ctx, link, ref, media_url = _ctx_from_blog(row, supabase_url)
        elif section == "landing":
            ctx, link, ref, media_url = _ctx_from_landing(row)
        elif section == "agenzia":
            ctx, link, ref, media_url = _ctx_from_agenzia(row)
        else:
            continue

        off = int(slot.get("giorno_offset", 0))
        slot_date = week_monday + timedelta(days=off)
        if slot_date.weekday() not in WEEKDAY_SLOTS:
            continue
        tipo = slot.get("tipo") or "facebook_post"
        pat_i = (rotation_start + slot_idx) % max(len(titoli_p), 1)
        titolo = apply_pattern(titoli_p[pat_i % len(titoli_p)], ctx)
        corpo = apply_pattern(corpi_p[pat_i % len(corpi_p)], ctx)
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
                meta={
                    "settimana": week_index,
                    "video_auto": tipo == "instagram_reel",
                    "rotazione_indice": rotation_start + slot_idx,
                    "rotazione_pool": len(pool),
                },
            )
        )
    return bozze


def _bozza_dedupe_key(b: dict[str, Any]) -> str:
    return "|".join(
        [
            str(b.get("data_pubblicazione_proposta") or "")[:10],
            str(b.get("fonte") or ""),
            str(b.get("tipo_canale") or ""),
            str(b.get("ora_proposta") or ""),
        ]
    )


def _existing_bozza_keys(client: Any, planned: list[dict[str, Any]]) -> set[str]:
    dates = sorted(
        {str(b.get("data_pubblicazione_proposta") or "")[:10] for b in planned if b.get("data_pubblicazione_proposta")}
    )
    if not dates:
        return set()
    try:
        res = (
            client.table("bozze_social")
            .select("data_pubblicazione_proposta,fonte,tipo_canale,ora_proposta,stato")
            .gte("data_pubblicazione_proposta", dates[0])
            .lte("data_pubblicazione_proposta", dates[-1])
            .execute()
        )
    except APIError:
        return set()
    keys: set[str] = set()
    for row in res.data or []:
        if (row.get("stato") or "") == "rifiutata":
            continue
        keys.add(
            "|".join(
                [
                    str(row.get("data_pubblicazione_proposta") or "")[:10],
                    str(row.get("fonte") or ""),
                    str(row.get("tipo_canale") or ""),
                    str(row.get("ora_proposta") or ""),
                ]
            )
        )
    return keys


def build_bozze_list(
    imm: list[dict],
    blog: list[dict],
    land: list[dict],
    rss: list[dict[str, str]],
    *,
    settimane: int = 1,
    used_rss_links: set[str] | None = None,
    client: Any | None = None,
) -> list[dict[str, Any]]:
    tpl = load_templates()
    supabase_url = env_or_empty("SUPABASE_URL") or BASE_SITE
    today = datetime.now(tz=TZ).date()
    start_monday = week_monday_on_or_after(today + timedelta(days=1))
    used_links = set(used_rss_links or [])

    cursors = {s: rotation_cursor(client, s) for s in SECTIONS}
    imm_pool = stable_sort_immobili(filter_active_immobili(imm))
    if imm_pool:
        print(
            f"Rotazione immobili: {len(imm_pool)} annunci attivi, "
            f"prossimo indice {cursors['immobile']} "
            f"(~{len(imm_pool) // POSTS_PER_SECTION or 1} settimane per giro completo).",
            file=sys.stderr,
        )

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
                    rotation_start=cursors[section],
                    imm=imm,
                    blog=blog,
                    land=land,
                    supabase_url=supabase_url,
                )
            )
            cursors[section] += POSTS_PER_SECTION
        all_bozze.extend(
            build_notizia_bozze(
                rss,
                tpl,
                week_monday=monday,
                week_index=w,
                used_links=used_links,
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
        used_rss: set[str] = set()
        client_probe = None
        if not args.dry_run:
            try:
                client_probe = sb()
                monday = week_monday_on_or_after(
                    datetime.now(tz=TZ).date() + timedelta(days=1)
                )
                end = monday + timedelta(days=7 * max(1, args.settimane) - 1)
                used_rss = _existing_rss_links(
                    client_probe, monday.isoformat(), end.isoformat()
                )
            except SystemExit:
                raise
            except Exception:
                used_rss = set()
        client_rot = client_probe if not args.dry_run else None
        bozze = build_bozze_list(
            imm,
            blog,
            land,
            rss,
            settimane=max(1, args.settimane),
            used_rss_links=used_rss,
            client=client_rot,
        )
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

    # Reel in batch DOPO tutte le bozze (evita blocco FFmpeg sulla prima insert)
    gen_reel_after = os.environ.get("GENERA_REEL_AUTO", "0").strip() not in (
        "0",
        "false",
        "no",
    )
    existing_keys = _existing_bozza_keys(client, bozze)

    total = len(bozze)
    for idx, b in enumerate(bozze, start=1):
        key = _bozza_dedupe_key(b)
        if key in existing_keys:
            tit_safe = b["titolo"][:60].encode("ascii", "replace").decode("ascii")
            print(
                f"[skip {idx}/{total}] gia presente: {tit_safe} ({b['data_pubblicazione_proposta']})",
                flush=True,
            )
            continue
        try:
            ins = client.table("bozze_social").insert(b).execute()
            saved_db += 1
            existing_keys.add(key)
            tit_safe = b["titolo"][:60].encode("ascii", "replace").decode("ascii")
            print(
                f"[Supabase {idx}/{total}] {tit_safe} ({b['data_pubblicazione_proposta']})",
                flush=True,
            )
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

    if gen_reel_after and saved_db:
        try:
            from genera_reel import find_ffmpeg, process_bozza

            ffmpeg = find_ffmpeg()
            reel_rows = (
                client.table("bozze_social")
                .select("*")
                .eq("stato", "bozza")
                .eq("tipo_canale", "instagram_reel")
                .execute()
            ).data or []
            reel_ok = 0
            for row in reel_rows:
                if (row.get("media_direct_url") or "").strip().endswith(".mp4"):
                    continue
                try:
                    if process_bozza(client, row, ffmpeg=ffmpeg):
                        reel_ok += 1
                except Exception as reel_err:
                    print(f"[reel] skip {row.get('id')}: {reel_err}", file=sys.stderr)
            print(f"Reel generati: {reel_ok}", flush=True)
        except Exception as e:
            print(
                f"[reel] Batch non completato: {e}\n"
                "  → python genera_reel.py --pending",
                file=sys.stderr,
            )

    if saved_db:
        print(
            f"OK: {saved_db} nuove bozze (target ~16/settimana: 12 contenuti sito + "
            "2 notizie RSS × FB/Google). Admin > Social > Approva.",
            flush=True,
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
    skipped = total - saved_db if total else 0
    if not saved_db and not saved_file and skipped:
        print(
            f"Nessuna nuova bozza: {skipped} slot gia coperti in Supabase. "
            "Admin > Social > Approva oppure python genera_reel.py --pending",
            flush=True,
        )
        return 0
    return 0 if (saved_db or saved_file) else 1


if __name__ == "__main__":
    sys.exit(main())
