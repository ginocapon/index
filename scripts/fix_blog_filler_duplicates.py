#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rimuove paragrafi filler duplicati dai blog (anti wordCount loop)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FILLER = (
    "<p>Righetto Immobiliare: supporto operativo su Padova e 101 comuni, "
    "350+ immobili gestiti, 98% soddisfazione clienti verificata.</p>"
)

BAD_CAP = "Scheda annuncio: verificare coerenza tra foto, testo e documenti."
GOOD_CAP = (
    "Immagine editoriale elaborata digitalmente (anche con intelligenza artificiale): "
    "illustrazione a scopo informativo, non documento fotografico dell'immobile o della scena descritta."
)


def clean_html(text: str) -> tuple[str, int]:
    removed = text.count(FILLER)
    text = text.replace(FILLER, "")
    text = text.replace(BAD_CAP, GOOD_CAP)
    # normalizza figcaption blog
    text = re.sub(
        r"<figcaption>([^<]*elaborata digitalmente[^<]*)</figcaption>",
        r'<figcaption class="rig-photo-caption">\1</figcaption>',
        text,
        flags=re.I,
    )
    return text, removed


def main() -> None:
    total_removed = 0
    for path in sorted(ROOT.glob("blog*.html")):
        raw = path.read_text(encoding="utf-8")
        cleaned, n = clean_html(raw)
        if n or BAD_CAP in raw:
            path.write_text(cleaned, encoding="utf-8")
            print(f"{path.name}: rimossi {n} filler")
            total_removed += n
    print(f"Totale paragrafi filler rimossi: {total_removed}")


if __name__ == "__main__":
    main()
