#!/usr/bin/env python3
"""Blog senza blog-rich: aggiunge link CSS + CTA strip standard prima di </main> (se manca)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CSS_LINE = '  <link rel="stylesheet" href="css/blog-rich.css?v=2">\n'

STRIP = """
<section class="blog-rich-cta-strip" aria-label="Recensioni e contatti">
  <div class="blog-rich-cta-inner">
    <h2>Ti e' stato utile? <em>Lascia una recensione</em></h2>
    <p class="blog-rich-cta-text">Le recensioni Google aiutano altre famiglie sul territorio.</p>
    <a class="blog-rich-btn" href="https://maps.app.goo.gl/xuCiRGDCSKskpTSf6?g_st=ic" target="_blank" rel="noopener noreferrer">Recensione su Google</a>
    <span class="blog-rich-cta-sub"><a href="contatti" style="color:rgba(247,245,241,0.88);text-decoration:underline">Richiedi consulenza immobiliare</a></span>
  </div>
</section>
"""

MARKERS = [
    '<link rel="stylesheet" href="css/welcome-popup.css?v=3" media="print" onload="this.media=\'all\'">',
    '<link rel="stylesheet" href="css/welcome-popup.css?v=3">',
    '<link rel="stylesheet" href="css/fonts.css?v=3"><link rel="stylesheet" href="css/nav-mobile.css?v=4">',
    '<link rel="stylesheet" href="css/fonts.css?v=3">',
]


def add_css(html: str) -> str:
    if "blog-rich.css" in html:
        return html
    for m in MARKERS:
        if m in html:
            return html.replace(m, m + "\n" + CSS_LINE.rstrip("\n"), 1)
    preload = '<link rel="preload" href="fonts/montserrat-400.woff2" as="font" type="font/woff2" crossorigin>'
    if preload in html:
        return html.replace(preload, preload + "\n" + CSS_LINE.rstrip("\n"), 1)
    i = html.lower().find("</head>")
    if i != -1:
        return html[:i] + CSS_LINE + html[i:]
    return html


def add_strip(html: str) -> str:
    if "blog-rich-cta-strip" in html:
        return html
    needle = "\n</main>\n"
    if needle in html:
        return html.replace(needle, "\n" + STRIP + "\n</main>\n", 1)
    return html


def main() -> int:
    changed = 0
    for path in sorted(ROOT.glob("blog-*.html")):
        raw = path.read_text(encoding="utf-8")
        if "blog-rich.css" in raw and "blog-rich-cta-strip" in raw:
            continue
        new = add_css(raw)
        if path.name != "blog-articolo.html":
            new = add_strip(new)
        if new != raw:
            path.write_text(new, encoding="utf-8")
            print(path.name)
            changed += 1
    print(f"File aggiornati: {changed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
