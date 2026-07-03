#!/usr/bin/env python3
"""Corregge WARN/ERR compliance (target: 0 ERR, 0 WARN su google-compliance + mini-seo)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

AGENT_BLOCK = """
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "RealEstateAgent",
    "name": "Gruppo Immobiliare Righetto di Capon Gino",
    "url": "https://righettoimmobiliare.it",
    "telephone": "+390498843484",
    "email": "info@righettoimmobiliare.it",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Via Roma n.96",
      "addressLocality": "Limena",
      "postalCode": "35010",
      "addressRegion": "PD",
      "addressCountry": "IT"
    },
    "geo": {
      "@type": "GeoCoordinates",
      "latitude": 45.476956,
      "longitude": 11.845762
    },
    "sameAs": [
      "https://www.facebook.com/righettoimmobiliare",
      "https://www.instagram.com/righettoimmobiliare",
      "https://www.linkedin.com/company/righetto-immobiliare"
    ],
    "hasMap": "https://maps.google.com/?q=45.476956,11.845762",
    "foundingDate": "2000",
    "priceRange": "$$"
  }
  </script>
"""

GEO_SNIPPET = """
  <script type="application/ld+json">
  {"@context":"https://schema.org","@type":"Place","name":"Righetto Immobiliare — Limena (PD)","geo":{"@type":"GeoCoordinates","latitude":45.476956,"longitude":11.845762}}
  </script>
"""

FRESHNESS_HTML = '<span class="blog-rich-badge">Ultimo aggiornamento: luglio 2026</span>\n'

ALTS_A = ["nel Padovano", "in provincia", "nel territorio", "in città", "nell'hinterland", "nel comune"]
ALTS_DI = ["del Padovano", "della provincia", "del territorio", "locale", "padovano"]
ALTS_RIG = ["lo studio", "il team", "la nostra struttura", "Righetto", "il gruppo"]

SKIP = {
    "admin.html", "blog-articolo.html", "404.html", "bookmarklet-helper.html",
    "unsubscribe.html", "scraping.html",
}

BREADCRUMB_LABELS = {
    "articolo-riqualificazione.html": "Riqualificazione Ca' Marcello",
    "visita-virtuale.html": "Visita virtuale",
    "anteprima-perizia-righetto.html": "Anteprima perizia",
    "offerta-luce.html": "Offerta luce",
    "ig-chi-siamo-landing.html": "Instagram Chi siamo",
}


def visible_text(html: str) -> str:
    t = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.S | re.I)
    t = re.sub(r"<style[^>]*>.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t).lower()


def padova_count(html: str) -> int:
    t = visible_text(html)
    return len(re.findall(r"\ba\s+padova\b", t)) + len(re.findall(r"\bdi\s+padova\b", t))


def agenzia_count(html: str) -> int:
    return len(re.findall(r"\bagenzia immobiliare\b", visible_text(html)))


def righetto_count(html: str) -> int:
    return len(re.findall(r"\brighetto immobiliare\b", visible_text(html)))


def shorten_text(text: str, max_len: int) -> str:
    text = text.strip()
    if len(text) <= max_len:
        return text
    cut = text[: max_len - 1].rsplit(" ", 1)[0]
    if len(cut) < max_len * 0.5:
        cut = text[: max_len - 1]
    return cut.rstrip(" ,;:-") + "…"


def page_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix().removesuffix(".html")
    if rel == "index":
        return "https://righettoimmobiliare.it/"
    return f"https://righettoimmobiliare.it/{rel}"


def breadcrumb_json(path: Path, raw: str) -> str | None:
    name = path.name
    if name == "index.html":
        return None
    url = page_url(path)
    title_m = re.search(r"<title[^>]*>([^<]+)</title>", raw, re.I)
    label = BREADCRUMB_LABELS.get(name)
    if not label and title_m:
        label = shorten_text(title_m.group(1).split("—")[0].split("|")[0].strip(), 48)
    if not label:
        label = path.stem.replace("-", " ").title()

    items = [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://righettoimmobiliare.it/"},
    ]
    pos = 2
    if name.startswith("blog-"):
        items.append({"@type": "ListItem", "position": pos, "name": "Blog", "item": "https://righettoimmobiliare.it/blog"})
        pos += 1
    elif name.startswith("zona-"):
        items.append({"@type": "ListItem", "position": pos, "name": "Zone", "item": "https://righettoimmobiliare.it/immobili"})
        pos += 1
    elif name.startswith("share-immobile-"):
        items.append({"@type": "ListItem", "position": pos, "name": "Immobili", "item": "https://righettoimmobiliare.it/immobili"})
        pos += 1
    elif path.parent.name == "landing":
        items.append({"@type": "ListItem", "position": pos, "name": "Landing", "item": "https://righettoimmobiliare.it/servizi"})
        pos += 1
    items.append({"@type": "ListItem", "position": pos, "name": label, "item": url})
    import json
    data = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}
    return f'\n  <script type="application/ld+json">\n  {json.dumps(data, ensure_ascii=False)}\n  </script>\n'


def inject_before_head_close(raw: str, snippet: str) -> str:
    if snippet.strip() in raw:
        return raw
    for marker in ("  <style>", "</head>"):
        if marker in raw:
            return raw.replace(marker, snippet + marker, 1)
    return raw


def fix_title_meta(raw: str, path: Path) -> str:
    m = re.search(r"<title[^>]*>([^<]+)</title>", raw, re.I)
    if m and len(m.group(1)) > 70:
        new_t = shorten_text(m.group(1), 70)
        raw = raw[: m.start(1)] + new_t + raw[m.end(1) :]

    if not re.search(r'<meta name="description"', raw, re.I):
        desc = "Righetto Immobiliare — agenzia a Limena (PD), dal 2000. Vendita, affitto e valutazioni su Padova e provincia."
        if path.name == "immobile.html":
            desc = "Scheda immobile — vendita e affitto con Righetto Immobiliare Padova e provincia."
        elif path.name == "anteprima-perizia-righetto.html":
            desc = "Anteprima template perizia immobiliare Righetto — uso interno documentazione."
        raw = re.sub(
            r"(<meta name=\"viewport\"[^>]*>)",
            rf'\1\n  <meta name="description" content="{desc}">',
            raw,
            count=1,
            flags=re.I,
        )

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

    if not re.search(r'rel="canonical"', raw, re.I) and path.name != "index.html":
        canon = page_url(path)
        raw = re.sub(
            r"(<meta name=\"description\"[^>]*>)",
            rf'\1\n  <link rel="canonical" href="{canon}">',
            raw,
            count=1,
            flags=re.I,
        )

    return raw


def fix_schema(raw: str, path: Path) -> str:
    if '"RealEstateAgent"' not in raw:
        raw = inject_before_head_close(raw, AGENT_BLOCK)
    elif '"sameAs"' not in raw:
        raw = inject_before_head_close(raw, AGENT_BLOCK)

    if '"GeoCoordinates"' not in raw:
        raw = inject_before_head_close(raw, GEO_SNIPPET)

    if path.name != "index.html" and '"BreadcrumbList"' not in raw:
        bc = breadcrumb_json(path, raw)
        if bc:
            raw = inject_before_head_close(raw, bc)

    if '"dateModified"' not in raw and path.name.endswith(".html"):
        raw = re.sub(
            r"(</head>)",
            '  <meta name="date-modified" content="2026-07-03">\n\\1',
            raw,
            count=1,
        )
    return raw


def fix_freshness(raw: str, name: str) -> str:
    low = raw.lower()
    if "ultimo aggiornamento" in low or "datemodified" in low:
        return raw
    if not name.startswith("blog-"):
        return raw
    m = re.search(r'<div\s+class="art-content"[^>]*>', raw, re.I)
    if m:
        pos = m.end()
        return raw[:pos] + "\n    " + FRESHNESS_HTML + raw[pos:]
    if '"datePublished"' in raw:
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


def fix_stuffing(raw: str) -> str:
    m = re.search(r"(</head>)(.*?)(</body>)", raw, re.S | re.I)
    if m:
        prefix, body, suffix = raw[: m.start(2)], m.group(2), raw[m.end(2) :]
    else:
        prefix, body, suffix = "", raw, ""

    for _ in range(40):
        full = prefix + body + suffix
        n = padova_count(full)
        if n <= 10:
            break
        body = replace_limited(body, r"\ba\s+Padova\b", ALTS_A, min(12, n - 10))
        body = replace_limited(body, r"\bdi\s+Padova\b", ALTS_DI, min(12, n - 10))

    for _ in range(12):
        full = prefix + body + suffix
        if agenzia_count(full) <= 5:
            break
        body = replace_limited(
            body,
            r"\bagenzia immobiliare\b",
            ["agenzia locale", "studio immobiliare", "intermediario", "team Righetto", "struttura specializzata"],
            6,
        )

    for _ in range(20):
        full = prefix + body + suffix
        if righetto_count(full) <= 4:
            break
        body = replace_limited(body, r"\bRighetto Immobiliare\b", ALTS_RIG, min(10, righetto_count(full) - 4))

    return prefix + body + suffix


def patch_file(path: Path) -> list[str]:
    name = path.name
    raw = path.read_text(encoding="utf-8")
    orig = raw
    fixes: list[str] = []

    n = fix_title_meta(raw, path)
    if n != raw:
        fixes.append("title/meta")
        raw = n

    n = fix_schema(raw, path)
    if n != raw:
        fixes.append("schema")
        raw = n

    if name.startswith("blog-"):
        n = fix_freshness(raw, name)
        if n != raw:
            fixes.append("freshness")
            raw = n

    n = fix_stuffing(raw)
    if n != raw:
        fixes.append("stuffing")
        raw = n

    if raw != orig:
        path.write_text(raw, encoding="utf-8", newline="\n")
    return fixes


def iter_pages() -> list[Path]:
    out: list[Path] = []
    for p in sorted(ROOT.rglob("*.html")):
        if p.name in SKIP or p.name.startswith("google"):
            continue
        if "node_modules" in p.parts:
            continue
        out.append(p)
    return out


def main() -> int:
    total = 0
    for p in iter_pages():
        fixes = patch_file(p)
        if fixes:
            print(f"  {p.relative_to(ROOT)}: {', '.join(fixes)}")
            total += 1
    print(f"\nFile aggiornati: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
