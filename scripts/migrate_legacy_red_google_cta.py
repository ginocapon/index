#!/usr/bin/env python3
"""
Rimuove la CTA Google legacy (sfondo rosso #B71C1C) e allinea al pattern 8.1b:
- Se esiste gia' almeno un blog-rich-cta-strip: elimina solo il blocco rosso duplicato.
- Altrimenti: sostituisce il blocco rosso con blog-rich-cta-strip standard.
Aggiunge css/blog-rich.css?v=2 se manca (dopo welcome-popup o fonts.css).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Blocco lungo tipico fine blog/landing (prima di </main> o footer)
STANDARD_RED = re.compile(
    r"(?:<!--\s*CTA\s+RECENSIONE\s+GOOGLE\s*-->\s*)?"
    r'<section style="background:linear-gradient\(135deg,#B71C1C,#D32F2F\)[^>]*>'
    r".*?"
    r"</section>",
    re.DOTALL | re.IGNORECASE,
)

# Variante compatta (es. blog-scegliere-agenzia-immobiliare-padova-2026.html)
SHORT_RED = re.compile(
    r'<section style="background:linear-gradient\(135deg,#B71C1C,#D32F2F\);padding:2rem 1\.5rem;text-align:center">\s*'
    r"<div style=\"max-width:560px;margin:0 auto\">.*?</div>\s*</section>",
    re.DOTALL,
)

REPLACEMENT = """<section class="blog-rich-cta-strip" aria-label="Recensioni e contatti">
  <div class="blog-rich-cta-inner">
    <h2>Ti e' stato utile? <em>Lascia una recensione</em></h2>
    <p class="blog-rich-cta-text">Le recensioni Google aiutano altre famiglie sul territorio.</p>
    <a class="blog-rich-btn" href="https://maps.app.goo.gl/xuCiRGDCSKskpTSf6?g_st=ic" target="_blank" rel="noopener noreferrer">Recensione su Google</a>
    <span class="blog-rich-cta-sub"><a href="contatti" style="color:rgba(247,245,241,0.88);text-decoration:underline">Richiedi consulenza immobiliare</a></span>
  </div>
</section>"""

BLOG_RICH_LINK = '  <link rel="stylesheet" href="css/blog-rich.css?v=2">'


def ensure_blog_rich_css(html: str) -> str:
    if "blog-rich.css" in html:
        return html
    markers = (
        '<link rel="stylesheet" href="css/welcome-popup.css?v=3">',
        "<link rel=\"stylesheet\" href=\"css/welcome-popup.css?v=3\" media=\"print\" onload=\"this.media='all'\">",
        '<link rel="stylesheet" href="css/fonts.css?v=3">',
    )
    for m in markers:
        if m in html:
            return html.replace(m, m + "\n" + BLOG_RICH_LINK, 1)
    return html


def process_file(path: Path) -> tuple[bool, str]:
    raw = path.read_text(encoding="utf-8")
    if "#B71C1C" not in raw and "B71C1C" not in raw:
        return False, "skip_no_red"

    original = raw
    changed_note: list[str] = []

    def sub_short(_: re.Match) -> str:
        if "blog-rich-cta-strip" in raw:
            return ""
        return "\n" + REPLACEMENT + "\n"

    # Prima la variante corta (padding 2rem — non overlap col blocco 2.5rem)
    if SHORT_RED.search(raw):
        raw = SHORT_RED.sub(sub_short, raw, count=1)
        changed_note.append("short_red")

    if STANDARD_RED.search(raw):

        def sub_std2(m: re.Match) -> str:
            if "blog-rich-cta-strip" in m.string:
                return "\n"
            return "\n" + REPLACEMENT + "\n"

        raw = STANDARD_RED.sub(sub_std2, raw, count=1)
        changed_note.append("standard_red")

    raw = ensure_blog_rich_css(raw)

    if raw != original:
        path.write_text(raw, encoding="utf-8")
        return True, ",".join(changed_note) or "css_only"
    return False, "no_change"


def main() -> int:
    modified = []
    for path in sorted(ROOT.glob("*.html")):
        ok, note = process_file(path)
        if ok:
            modified.append(f"{path.name}: {note}")
    for line in modified:
        print(line)
    print(f"Totale file modificati: {len(modified)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
