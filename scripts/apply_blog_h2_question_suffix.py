# -*- coding: utf-8 -*-
"""
Aggiunge '?' agli <h2> dei blog statici se il testo (senza tag) non contiene gia' un punto interrogativo.
Esclusi: blog-articolo, h2 recensione/footer, titoli troppo corti o troppo lunghi.
Idempotente se rieseguito.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_SUBSTR = ("domande frequenti", "lasciaci", "recensione", "ti e' stato utile", "articolo non trovato")


def process_html(html: str) -> str:
    def repl(m: re.Match[str]) -> str:
        attrs, inner = m.group(1), m.group(2)
        if "style=" in attrs and "Cormorant" in m.group(0):
            return m.group(0)
        plain = re.sub(r"<[^>]+>", "", inner)
        plain = " ".join(plain.split())
        if not plain or len(plain) < 12 or len(plain) > 220:
            return m.group(0)
        if "?" in plain:
            return m.group(0)
        low = plain.lower()
        if any(s in low for s in SKIP_SUBSTR):
            return m.group(0)
        if plain.endswith("?"):
            return m.group(0)
        return f"<h2{attrs}>{inner}?</h2>"

    return re.sub(r"<h2([^>]*)>([\s\S]*?)</h2>", repl, html)


def main() -> int:
    n = 0
    for path in sorted(ROOT.glob("blog-*.html")):
        if path.name == "blog-articolo.html":
            continue
        text = path.read_text(encoding="utf-8")
        new = process_html(text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            print("OK", path.name)
            n += 1
    print("Totale file modificati:", n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
