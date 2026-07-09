# -*- coding: utf-8 -*-
"""Genera pagine share-immobile-*.html con Open Graph statico (anteprima Facebook/WhatsApp).

Esegui: python scripts/sync_og_immobili.py
Richiede SUPABASE_KEY in .env (locale) o variabile d'ambiente (CI).
"""
from __future__ import annotations

import json
import os
import re
import shutil
import unicodedata
import urllib.request
from html import escape
from pathlib import Path

sys_path = Path(__file__).resolve().parent
if str(sys_path) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(sys_path))

from righetto_immobile_slug import (
    generate_property_slug,
    immobile_app_url,
    share_immobile_path,
    share_immobile_url,
)

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT_GLOB = "share-immobile-*.html"
SITE = "https://righettoimmobiliare.it"
SUPABASE_URL = "https://qwkwkemuabfwvwuqrxlu.supabase.co"


def load_supabase_key() -> str:
    key = os.environ.get("SUPABASE_KEY", "").strip()
    if key:
        return key
    env_path = ROOT / ".env"
    if env_path.is_file():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("SUPABASE_KEY="):
                return line.split("=", 1)[1].strip()
    raise SystemExit("SUPABASE_KEY mancante (.env o variabile d'ambiente)")


def fetch_immobili(key: str) -> list[dict]:
    url = (
        f"{SUPABASE_URL}/rest/v1/immobili"
        "?select=*&attivo=eq.true&venduto=eq.false&order=created_at.desc"
    )
    req = urllib.request.Request(
        url,
        headers={"apikey": key, "Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def cap(s: str) -> str:
    s = (s or "").strip()
    return s[:1].upper() + s[1:] if s else ""


def first_photo(row: dict) -> str:
    def to_public(u: str) -> str:
        u = (u or "").strip()
        if not u:
            return ""
        if u.startswith("img/"):
            return f"{SITE}/{u}"
        if u.startswith("http://") or u.startswith("https://"):
            return u
        return ""

    foto = row.get("foto") or []
    if isinstance(foto, list) and foto:
        hit = to_public(str(foto[0]))
        if hit:
            return hit
    fp = row.get("foto_principale") or ""
    hit = to_public(str(fp))
    if hit:
        return hit
    return f"{SITE}/img/team/titolari.webp"


def seo_title(row: dict) -> str:
    tip = cap(row.get("tipologia") or row.get("categoria") or "Immobile")
    op = row.get("tipo_operazione") or ""
    op_label = "in vendita" if op == "vendita" else ("in affitto" if str(op).startswith("affitt") else "")
    comune = row.get("comune") or "Padova"
    return f"{tip} {op_label} a {comune} — Righetto Immobiliare Padova".replace("  ", " ").strip()


def seo_description(row: dict) -> str:
    tip = cap(row.get("tipologia") or "Immobile")
    mq = row.get("superficie")
    loc = row.get("locali") or row.get("camere")
    prezzo = row.get("prezzo")
    cod = row.get("codice") or ""
    parts = [tip]
    if mq:
        parts.append(f"{mq} m²")
    if loc:
        parts.append(f"{loc} locali")
    if prezzo:
        parts.append(f"€ {int(prezzo):,}".replace(",", "."))
    if cod:
        parts.append(f"Rif. {cod}")
    parts.append("Righetto Immobiliare Padova")
    return " · ".join(parts)


def build_share_html(entry: dict) -> str:
    title = escape(entry["title"])
    desc = escape(entry["description"])
    share_url = entry["share_url"]
    app_url = entry["app_url"]
    image = escape(entry["image"])
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, follow, max-image-preview:large">
<link rel="canonical" href="{escape(app_url)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Righetto Immobiliare">
<meta property="og:locale" content="it_IT">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{escape(share_url)}">
<meta property="og:image" content="{image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{image}">
<meta http-equiv="refresh" content="0;url={escape(app_url)}">
<script>location.replace({json.dumps(app_url)});</script>
</head>
<body style="font-family:system-ui,sans-serif;padding:2rem;text-align:center">
<p>Reindirizzamento alla scheda immobile…</p>
<p><a href="{escape(app_url)}">Apri {escape(entry.get('titolo', 'immobile'))}</a></p>
</body>
</html>
"""


def main() -> int:
    key = load_supabase_key()
    rows = fetch_immobili(key)
    print(f"Immobili attivi: {len(rows)}")

    catalog: dict = {
        "generated": __import__("datetime").date.today().isoformat(),
        "bySlug": {},
        "byLegacySlug": {},
        "byCodice": {},
    }
    entries_by_file: dict[str, dict] = {}

    for row in rows:
        seo = generate_property_slug(row)
        if not seo:
            continue
        titolo = (row.get("titolo") or "").strip()
        entry = {
            "codice": row.get("codice"),
            "titolo": titolo,
            "seo_slug": seo,
            "title": seo_title(row),
            "description": seo_description(row),
            "image": first_photo(row),
            "share_url": share_immobile_url(seo),
            "app_url": immobile_app_url(seo),
            "share_file": share_immobile_path(seo),
        }
        catalog["bySlug"][seo] = entry
        if row.get("codice"):
            catalog["byCodice"][str(row.get("codice")).upper()] = entry
        legacy = (row.get("slug") or "").strip().lower()
        if legacy and legacy != seo.lower():
            catalog["byLegacySlug"][legacy] = entry
            alias_file = share_immobile_path(legacy)
            entries_by_file[alias_file] = {**entry, "share_url": share_immobile_url(legacy)}
        entries_by_file[entry["share_file"]] = entry

    # Rimuovi vecchie pagine share
    for old in ROOT.glob(OUT_GLOB):
        old.unlink()

    for fname, entry in entries_by_file.items():
        (ROOT / fname).write_text(build_share_html(entry), encoding="utf-8")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "og-immobili.json").write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"OK: {len(entries_by_file)} pagine share-immobile-*.html")
    print(f"OK: data/og-immobili.json ({len(catalog['bySlug'])} slug SEO)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
