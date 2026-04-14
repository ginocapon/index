# -*- coding: utf-8 -*-
"""Sostituzioni mirate H2 in formato domanda (AEO) sui blog statici — pattern ripetuti + file specifici."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Sostituzioni globali (toc + h2 dove testo identico)
GLOBAL: list[tuple[str, str]] = [
    (
        '<h2 id="previsioni">Previsioni per il secondo semestre 2026</h2>',
        '<h2 id="previsioni">Cosa attendersi nel secondo semestre 2026?</h2>',
    ),
    (
        ">Previsioni per il secondo semestre 2026</a>",
        ">Cosa attendersi nel secondo semestre 2026?</a>",
    ),
    (
        "<h2 id=\"prezzi\">Prezzi delle case a Padova nel 2026: +3-5% rispetto al 2025</h2>",
        "<h2 id=\"prezzi\">Quanto sono cresciuti i prezzi delle case a Padova nel 2026 (+3-5% sul 2025)?</h2>",
    ),
    (
        "<h2 id=\"mutui\">Mutui casa a Padova 2026: tassi stabilizzati, accesso migliorato</h2>",
        "<h2 id=\"mutui\">Come stanno mutui e tassi per chi compra casa a Padova nel 2026?</h2>",
    ),
    (
        "<h2 id=\"affitti\">Dinamiche degli affitti nel Padovano: +8% anno su anno</h2>",
        "<h2 id=\"affitti\">Perché gli affitti nel Padovano crescono circa l'8% anno su anno?</h2>",
    ),
    (
        "<h2 id=\"tabella-prezzi\">Tabella prezzi medi per zona &mdash; Padova e provincia 2026</h2>",
        "<h2 id=\"tabella-prezzi\">Quali sono i prezzi medi al mq per zona a Padova e in provincia (2026)?</h2>",
    ),
    (
        '<h2 id="previsioni">Previsioni sul listino immobiliare: secondo semestre 2026</h2>',
        '<h2 id="previsioni">Cosa prevedere sul listino immobiliare nel secondo semestre 2026?</h2>',
    ),
    (
        ">Previsioni sul listino secondo semestre 2026</a>",
        ">Cosa prevedere sul listino nel secondo semestre 2026?</a>",
    ),
]

PER_FILE: dict[str, list[tuple[str, str]]] = {
    "blog-comprare-casa-padova-guida-2026.html": [
        (
            '<h2 id="budget">Passo 1 &mdash; Definire il budget reale</h2>',
            '<h2 id="budget">Come definire il budget reale prima di comprare casa (passo 1)?</h2>',
        ),
        (
            '<h2 id="mutuo">Passo 2 &mdash; La pre-delibera del mutuo: il vostro asso nella manica</h2>',
            '<h2 id="mutuo">Come ottenere la pre-delibera mutuo e perche conviene (passo 2)?</h2>',
        ),
        (
            '<h2 id="ricerca">Passo 3 &mdash; Cercare l\'immobile giusto</h2>',
            '<h2 id="ricerca">Come cercare l\'immobile giusto a Padova (passo 3)?</h2>',
        ),
        (
            '<h2 id="sopralluogo">Passo 4 &mdash; Il sopralluogo: cosa controllare davvero</h2>',
            '<h2 id="sopralluogo">Cosa controllare al sopralluogo prima dell\'offerta (passo 4)?</h2>',
        ),
        (
            '<h2 id="conformita">Passo 5 &mdash; Verifiche urbanistiche e catastali</h2>',
            '<h2 id="conformita">Quali verifiche urbanistiche e catastali servono (passo 5)?</h2>',
        ),
        (
            '<h2 id="proposta">Passo 6 &mdash; La proposta d\'acquisto</h2>',
            '<h2 id="proposta">Come impostare la proposta d\'acquisto (passo 6)?</h2>',
        ),
        (
            '<h2 id="preliminare">Passo 7 &mdash; Il compromesso (contratto preliminare)</h2>',
            '<h2 id="preliminare">Come funziona il compromesso o preliminare (passo 7)?</h2>',
        ),
        (
            '<h2 id="rogito">Passo 8 &mdash; Il rogito notarile e la consegna delle chiavi</h2>',
            '<h2 id="rogito">Cosa succede al rogito e alla consegna delle chiavi (passo 8)?</h2>',
        ),
        (
            "<h2 id=\"costi\">Tutti i costi per acquistare un immobile nel Padovano: la tabella completa</h2>",
            "<h2 id=\"costi\">Quali sono tutti i costi per acquistare un immobile nel Padovano (tabella)?</h2>",
        ),
        (
            "<h2 id=\"errori\">I 7 errori piu' comuni quando si acquista un immobile nel Padovano</h2>",
            "<h2 id=\"errori\">Quali sono i 7 errori piu' comuni quando si acquista nel Padovano?</h2>",
        ),
    ],
    "blog-vendita-immobiliare-padova-strategie-2026.html": [
        (
            '<h2 id="pricing">Strategia 1: Pricing corretto con dati OMI &mdash; la base di tutto</h2>',
            '<h2 id="pricing">Perche il pricing con dati OMI e la base della vendita (strategia 1)?</h2>',
        ),
        (
            '<h2 id="home-staging">Strategia 2: Home staging professionale nel Padovano</h2>',
            '<h2 id="home-staging">Come aiuta lo home staging professionale nel Padovano (strategia 2)?</h2>',
        ),
        (
            '<h2 id="documenti">Strategia 3: Documenti pronti prima di mettere in vendita</h2>',
            '<h2 id="documenti">Quali documenti avere pronti prima di mettere in vendita (strategia 3)?</h2>',
        ),
        (
            '<h2 id="foto">Strategia 4: Foto e video professionali</h2>',
            '<h2 id="foto">Perche foto e video professionali fanno differenza (strategia 4)?</h2>',
        ),
        (
            '<h2 id="agenzia">Strategia 6: Agenzia immobiliare vs vendita tra privati</h2>',
            '<h2 id="agenzia">Agenzia o vendita tra privati: cosa conviene nel Padovano (strategia 6)?</h2>',
        ),
        (
            '<h2 id="negoziazione">Strategia 7: Negoziazione strategica per ottenere il massimo</h2>',
            '<h2 id="negoziazione">Come negoziare per ottenere il massimo prezzo (strategia 7)?</h2>',
        ),
        (
            "<h2 id=\"costi\">Quanto costa cedere un immobile nel Padovano? Tabella per fascia prezzo</h2>",
            "<h2 id=\"costi\">Come leggere i costi di cessione nel Padovano per fascia di prezzo?</h2>",
        ),
        (
            "<h2 id=\"errori\">I 5 errori che fanno perdere soldi nella vendita</h2>",
            "<h2 id=\"errori\">Quali sono i 5 errori che fanno perdere soldi in vendita?</h2>",
        ),
    ],
}


def main() -> int:
    for path in sorted(ROOT.glob("blog-*.html")):
        if path.name == "blog-articolo.html":
            continue
        text = path.read_text(encoding="utf-8")
        orig = text
        for o, n in GLOBAL:
            text = text.replace(o, n)
        for o, n in PER_FILE.get(path.name, []):
            text = text.replace(o, n)
        if text != orig:
            path.write_text(text, encoding="utf-8")
            print("OK", path.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
