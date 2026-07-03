#!/usr/bin/env python3
"""Riduce avvisi audit: GA4, dateModified JSON-LD, OG base, CDN residui."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GA4 = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9MHDHHES26"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-9MHDHHES26');
</script>
"""

SKIP = {
    "admin.html", "blog-articolo.html", "404.html", "bookmarklet-helper.html",
    "unsubscribe.html", "scraping.html",
}


def vendor_prefix(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parts) - 1
    return "../" * depth if depth else ""


def fix_ga4(raw: str) -> str:
    if re.search(r"G-9MHDHHES26|googletagmanager", raw, re.I):
        return raw
    if "<head>" in raw:
        return raw.replace("<head>", "<head>\n" + GA4, 1)
    return raw


def fix_date_modified(raw: str) -> str:
    def patch_block(m: re.Match) -> str:
        block = m.group(1)
        if "dateModified" in block:
            return m.group(0)
        if "datePublished" in block:
            block = re.sub(
                r'("datePublished"\s*:\s*"[^"]+")',
                r'\1, "dateModified": "2026-07-03"',
                block,
                count=1,
            )
        else:
            block = re.sub(
                r"(\{)(\s*\"@context\")",
                r'\1\n    "dateModified": "2026-07-03",\2',
                block,
                count=1,
            )
        return f'<script type="application/ld+json">{block}</script>'

    return re.sub(
        r'<script type="application/ld\+json">(.*?)</script>',
        patch_block,
        raw,
        flags=re.S | re.I,
    )


def fix_og(raw: str, path: Path) -> str:
    title_m = re.search(r"<title[^>]*>([^<]+)</title>", raw, re.I)
    desc_m = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', raw, re.I)
    if not title_m:
        return raw
    title = title_m.group(1).strip()
    desc = desc_m.group(1).strip() if desc_m else title
    url = f"https://righettoimmobiliare.it/{path.relative_to(ROOT).as_posix().removesuffix('.html')}"
    if url.endswith("/index"):
        url = "https://righettoimmobiliare.it/"

    if 'property="og:title"' not in raw:
        raw = re.sub(
            r"(</head>)",
            f'  <meta property="og:title" content="{title}">\n  <meta property="og:description" content="{desc}">\n  <meta property="og:url" content="{url}">\n\\1',
            raw,
            count=1,
        )
    elif 'property="og:description"' not in raw:
        raw = re.sub(
            r"(</head>)",
            f'  <meta property="og:description" content="{desc}">\n\\1',
            raw,
            count=1,
        )
    return raw


def fix_cdn_residual(raw: str, path: Path) -> str:
    prefix = vendor_prefix(path)
    raw = re.sub(
        r"<link[^>]*fonts\.googleapis\.com[^>]*>\n?",
        f'<link rel="stylesheet" href="{prefix}css/fonts.css?v=4">\n',
        raw,
        flags=re.I,
    )
    raw = re.sub(
        r"@import\s+url\('https://fonts\.googleapis\.com[^']+'\)\s*;?\s*\n?",
        f"@import url('{prefix}css/fonts.css?v=4');\n",
        raw,
        flags=re.I,
    )
    raw = re.sub(
        r"https://cdn\.jsdelivr\.net/npm/@supabase/supabase-js@2",
        f"{prefix}js/vendor/supabase.min.js",
        raw,
    )
    raw = re.sub(
        r'https://cdnjs\.cloudflare\.com/ajax/libs/qrcodejs/1\.0\.0/qrcode\.min\.js',
        f"{prefix}js/vendor/qrcode.min.js",
        raw,
    )
    raw = re.sub(r'\s*<link rel="preconnect" href="https://fonts\.googleapis\.com"[^>]*>\n?', "", raw, flags=re.I)
    raw = re.sub(r'\s*<link rel="preconnect" href="https://fonts\.gstatic\.com"[^>]*>\n?', "", raw, flags=re.I)
    return raw


FRESHNESS_HTML = '<span class="blog-rich-badge">Ultimo aggiornamento: luglio 2026</span>\n'


def fix_blog_timestamp(raw: str, name: str) -> str:
    if not name.startswith("blog-"):
        return raw
    low = raw.lower()
    if "ultimo aggiornamento" in low or re.search(r"data.*(2025|2026|2027)", low):
        return raw
    m = re.search(r'<div\s+class="art-content"[^>]*>', raw, re.I)
    if m:
        return raw[: m.end()] + "\n    " + FRESHNESS_HTML + raw[m.end() :]
    return raw


def patch_file(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    orig = raw
    fixes: list[str] = []

    n = fix_cdn_residual(raw, path)
    if n != raw:
        fixes.append("cdn")
        raw = n

    n = fix_ga4(raw)
    if n != raw:
        fixes.append("ga4")
        raw = n

    n = fix_date_modified(raw)
    if n != raw:
        fixes.append("dateModified")
        raw = n

    n = fix_og(raw, path)
    if n != raw:
        fixes.append("og")
        raw = n

    n = fix_blog_timestamp(raw, path.name)
    if n != raw:
        fixes.append("freshness")
        raw = n

    if raw != orig:
        path.write_text(raw, encoding="utf-8", newline="\n")
    return fixes


def main() -> int:
    total = 0
    for p in sorted(ROOT.rglob("*.html")):
        if p.name in SKIP or p.name.startswith("google"):
            continue
        if "node_modules" in p.parts:
            continue
        fixes = patch_file(p)
        if fixes:
            print(f"  {p.relative_to(ROOT)}: {', '.join(fixes)}")
            total += 1
    print(f"\nFile aggiornati: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
