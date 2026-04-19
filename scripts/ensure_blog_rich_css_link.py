#!/usr/bin/env python3
"""Aggiunge css/blog-rich.css?v=2 se la pagina usa blog-rich-cta-strip ma non include il foglio."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
LINK = '  <link rel="stylesheet" href="css/blog-rich.css?v=2">\n'
MARKERS = [
    '<link rel="stylesheet" href="css/welcome-popup.css?v=3">',
    '<link rel="stylesheet" href="css/welcome-popup.css?v=3" media="print" onload="this.media=\'all\'">',
    '<link rel="stylesheet" href="css/fonts.css?v=3"><link rel="stylesheet" href="css/nav-mobile.css?v=4">',
    '<link rel="stylesheet" href="css/fonts.css?v=3">',
]


def patch(html: str) -> str | None:
    if "blog-rich.css" in html:
        return None
    if "blog-rich-cta-strip" not in html:
        return None
    for m in MARKERS:
        if m in html:
            return html.replace(m, m + "\n" + LINK.rstrip("\n"), 1)
    # blog-direttiva: dopo preload font self-hosted
    needle = '<link rel="preload" href="fonts/montserrat-400.woff2" as="font" type="font/woff2" crossorigin>'
    if needle in html:
        return html.replace(needle, needle + "\n" + LINK.rstrip("\n"), 1)
    # ultima risorsa: prima di </head>
    idx = html.lower().find("</head>")
    if idx == -1:
        return None
    return html[:idx] + LINK + html[idx:]


def main() -> int:
    n = 0
    for path in sorted(ROOT.glob("*.html")):
        raw = path.read_text(encoding="utf-8")
        new = patch(raw)
        if new is not None:
            path.write_text(new, encoding="utf-8")
            print(path.name)
            n += 1
    print(f"Aggiunto blog-rich.css in {n} file.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
