# -*- coding: utf-8 -*-
"""Slug SEO immobili — allineato a generatePropertySlug() in js/homepage.js e immobile.html."""
from __future__ import annotations

import re
import unicodedata


def _norm_part(s: str) -> str:
    s = (s or "").lower().strip()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    for a, b in (("à", "a"), ("á", "a"), ("â", "a"), ("è", "e"), ("é", "e"), ("ê", "e"),
                 ("ì", "i"), ("í", "i"), ("î", "i"), ("ò", "o"), ("ó", "o"), ("ô", "o"),
                 ("ù", "u"), ("ú", "u"), ("û", "u"), ("ç", "c"), ("ñ", "n")):
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def generate_property_slug(row: dict) -> str:
    parts = [
        row.get("tipologia") or row.get("categoria") or "immobile",
        row.get("tipo_operazione") or row.get("tipo_contratto") or "vendita",
        row.get("comune") or "padova",
        (row.get("codice") or "").strip(),
    ]
    return "-".join(p for p in (_norm_part(x) for x in parts) if p)


def share_immobile_path(seo_slug: str) -> str:
    return f"share-immobile-{seo_slug}.html"


def share_immobile_url(seo_slug: str, base: str = "https://righettoimmobiliare.it") -> str:
    return f"{base}/{share_immobile_path(seo_slug).replace('.html', '')}"


def immobile_app_url(seo_slug: str, base: str = "https://righettoimmobiliare.it") -> str:
    return f"{base}/immobile?s={seo_slug}"
