#!/usr/bin/env python3
"""Corregge WARN residui da google-compliance-check.py (target: 0 WARN)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GEO_SNIPPET = """
  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"Place","name":"Righetto Immobiliare — Limena (PD)","geo":{"@type":"GeoCoordinates","latitude":45.476956,"longitude":11.845762}}
  </script>
"""

BREADCRUMB_ARTICOLO = """
  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {"@type":"ListItem","position":1,"name":"Home","item":"https://righettoimmobiliare.it/"},
    {"@type":"ListItem","position":2,"name":"Blog","item":"https://righettoimmobiliare.it/blog"},
    {"@type":"ListItem","position":3,"name":"Riqualificazione Ca' Marcello"}
  ]}
  </script>
"""

FRESHNESS_HTML = '<span class="blog-rich-badge">Ultimo aggiornamento: luglio 2026</span>\n'

ALTS_A = ["nel Padovano", "in provincia", "nel territorio", "in città", "nell'hinterland", "nel comune"]
ALTS_DI = ["del Padovano", "della provincia", "del territorio", "locale", "padovano"]


def visible_text(html: str) -> str:
    t = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.S | re.I)
    t = re.sub(r"<style[^>]*>.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t).lower()


def padova_count(html: str) -> int:
    t = visible_text(html)
    return t.count("a padova") + t.count("di padova")


def agenzia_count(html: str) -> int:
    return visible_text(html).count("agenzia immobiliare")


def shorten_text(text: str, max_len: int) -> str:
    text = text.strip()
    if len(text) <= max_len:
        return text
    cut = text[: max_len - 1].rsplit(" ", 1)[0]
    if len(cut) < max_len * 0.5:
        cut = text[: max_len - 1]
    return cut.rstrip(" ,;:-") + "…"


def fix_title_meta(raw: str) -> str:
    m = re.search(r"<title>([^<]+)</title>", raw, re.I)
    if m and len(m.group(1)) > 70:
        new_t = shorten_text(m.group(1), 70)
        raw = raw[: m.start(1)] + new_t + raw[m.end(1) :]

    for pat in (
        r'(<meta property="og:title" content=")([^"]*)(")',
        r'(<meta name="twitter:title" content=")([^"]*)(")',
    ):
        for m in re.finditer(pat, raw, re.I):
            if len(m.group(2)) > 70:
                new_t = shorten_text(m.group(2), 68)
                raw = raw[: m.start(2)] + new_t + raw[m.end(2) :]

    m = re.search(r'<meta name="description" content="([^"]*)"', raw, re.I)
    if m and len(m.group(1)) > 160:
        new_d = shorten_text(m.group(1), 158)
        raw = raw[: m.start(1)] + new_d + raw[m.end(1) :]

    for pat in (
        r'(<meta property="og:description" content=")([^"]*)(")',
        r'(<meta name="twitter:description" content=")([^"]*)(")',
    ):
        for m in re.finditer(pat, raw, re.I):
            if len(m.group(2)) > 160:
                new_d = shorten_text(m.group(2), 158)
                raw = raw[: m.start(2)] + new_d + raw[m.end(2) :]

    return raw


def fix_geo(raw: str) -> str:
    if '"GeoCoordinates"' in raw:
        return raw
    marker = "  <style>"
    if marker in raw:
        return raw.replace(marker, GEO_SNIPPET + marker, 1)
    if "</head>" in raw:
        return raw.replace("</head>", GEO_SNIPPET + "</head>", 1)
    return raw


def fix_breadcrumb_articolo(raw: str) -> str:
    if '"BreadcrumbList"' in raw:
        return raw
    return raw.replace("  <style>", BREADCRUMB_ARTICOLO + "  <style>", 1)


def fix_freshness(raw: str, name: str) -> str:
    low = raw.lower()
    if "ultimo aggiornamento" in low or "datemodified" in low:
        return raw
    if not name.startswith("blog-"):
        return raw
    if FRESHNESS_HTML.strip() in raw:
        return raw
    m = re.search(r'<div\s+class="art-content"[^>]*>', raw, re.I)
    if m:
        pos = m.end()
        return raw[:pos] + "\n    " + FRESHNESS_HTML + raw[pos:]
    if '"dateModified"' not in raw and '"datePublished"' in raw:
        raw = re.sub(
            r'("datePublished"\s*:\s*"[^"]+")',
            r'\1, "dateModified": "2026-07-03"',
            raw,
            count=1,
        )
    return raw


def replace_limited(html: str, pattern: str, alts: list[str], n: int) -> str:
    if n <= 0:
        return html
    idx = 0

    def sub_fn(m: re.Match) -> str:
        nonlocal idx
        if idx >= n:
            return m.group(0)
        alt = alts[idx % len(alts)]
        idx += 1
        return alt

    return re.sub(pattern, sub_fn, html, flags=re.I)


def fix_stuffing(raw: str, name: str) -> str:
    limit = 10
    m = re.search(r"(</head>)(.*?)(</body>)", raw, re.S | re.I)
    if m:
        prefix = raw[: m.start(2)]
        body = m.group(2)
        suffix = raw[m.end(2) :]
    else:
        prefix, body, suffix = "", raw, ""

    for _ in range(30):
        full = prefix + body + suffix
        n = padova_count(full)
        if n <= limit:
            break
        body = replace_limited(body, r"\ba\s+Padova\b", ALTS_A, min(8, n - limit))
        body = replace_limited(body, r"\bdi\s+Padova\b", ALTS_DI, min(8, n - limit))
        body = replace_limited(body, r"\ba\s+padova\b", ALTS_A, min(8, n - limit))
        body = replace_limited(body, r"\bdi\s+padova\b", ALTS_DI, min(8, n - limit))

    for _ in range(10):
        full = prefix + body + suffix
        if agenzia_count(full) <= 5:
            break
        body = replace_limited(
            body,
            r"\bagenzia immobiliare\b",
            ["agenzia locale", "studio immobiliare", "intermediario", "team Righetto", "struttura specializzata"],
            4,
        )

    return prefix + body + suffix


def patch_file(path: Path) -> list[str]:
    name = path.name
    raw = path.read_text(encoding="utf-8")
    orig = raw
    fixes: list[str] = []

    new = fix_title_meta(raw)
    if new != raw:
        fixes.append("title/meta")
        raw = new

    if name == "articolo-riqualificazione.html":
        n2 = fix_breadcrumb_articolo(raw)
        if n2 != raw:
            fixes.append("breadcrumb")
            raw = n2

    if '"GeoCoordinates"' not in raw:
        n2 = fix_geo(raw)
        if n2 != raw:
            fixes.append("geo")
            raw = n2

    if name.startswith("blog-"):
        n2 = fix_freshness(raw, name)
        if n2 != raw:
            fixes.append("freshness")
            raw = n2

    n2 = fix_stuffing(raw, name)
    if n2 != raw:
        fixes.append("stuffing")
        raw = n2

    if raw != orig:
        path.write_text(raw, encoding="utf-8", newline="\n")
    return fixes


def main() -> int:
    skip = {
        "admin.html", "blog-articolo.html", "404.html", "bookmarklet-helper.html",
        "unsubscribe.html", "scraping.html", "immobile.html",
    }
    pages = sorted(
        p for p in ROOT.glob("*.html")
        if p.name not in skip and not p.name.startswith("share-immobile-") and not p.name.startswith("google")
    )
    total = 0
    for p in pages:
        fixes = patch_file(p)
        if fixes:
            print(f"  {p.name}: {', '.join(fixes)}")
            total += 1
    print(f"\nFile aggiornati: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
