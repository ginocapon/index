# -*- coding: utf-8 -*-
"""Sostituisce gli H2 principali delle pagine zona con formato domanda (AEO)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (file, lista di (vecchio_tag_h2_completo, nuovo_tag_h2_completo))
REPLACEMENTS: list[tuple[str, list[tuple[str, str]]]] = [
    (
        "zona-arcella-padova.html",
        [
            (
                '<h2 class="sec-t">L\'Arcella: <strong>opportunita e vitalita</strong></h2>',
                '<h2 class="sec-t">Cos\'e oggi l\'<strong>Arcella</strong> a Padova e per chi conviene viverci?</h2>',
            ),
            (
                '<h2 class="sec-t">Prezzi e <strong>opportunita</strong> all\'Arcella</h2>',
                '<h2 class="sec-t">Quanto costano le case <strong>all\'Arcella</strong> nel 2026?</h2>',
            ),
            (
                '<h2 class="sec-t">Cosa si trova <strong>nel quartiere</strong></h2>',
                '<h2 class="sec-t">Quali <strong>tipologie immobiliari</strong> si trovano all\'Arcella?</h2>',
            ),
            (
                '<h2 class="sec-t">Muoversi <strong>dall\'Arcella</strong></h2>',
                '<h2 class="sec-t">Come ci si sposta <strong>dall\'Arcella</strong> verso Padova e la provincia?</h2>',
            ),
            (
                '<h2 class="sec-t">Pro e Contro di Vivere all\'<strong>Arcella</strong></h2>',
                '<h2 class="sec-t">Quali sono i <strong>pro e i contro</strong> di vivere all\'Arcella?</h2>',
            ),
            (
                '<h2 class="sec-t">Quanto vale la tua casa in <strong>Arcella</strong>?</h2>',
                '<h2 class="sec-t">Quanto vale oggi una casa in vendita in <strong>Arcella</strong>?</h2>',
            ),
        ],
    ),
    (
        "zona-centro-storico-padova.html",
        [
            (
                '<h2 class="sec-t">Il cuore di <strong>Padova</strong></h2>',
                '<h2 class="sec-t">Perche il <strong>Centro Storico</strong> di Padova resta cosi richiesto?</h2>',
            ),
            (
                '<h2 class="sec-t">Prezzi e <strong>tendenze</strong> nel cuore della citta\'</h2>',
                '<h2 class="sec-t">Come si muovono <strong>prezzi e tendenze</strong> nel Centro Storico?</h2>',
            ),
            (
                '<h2 class="sec-t">Cosa si trova nel <strong>nucleo antico</strong></h2>',
                '<h2 class="sec-t">Quali <strong>immobili e stili</strong> caratterizzano il nucleo antico?</h2>',
            ),
            (
                '<h2 class="sec-t">Muoversi dal <strong>cuore della citta\'</strong></h2>',
                '<h2 class="sec-t">Come muoversi <strong>dal centro storico</strong> verso il resto della citta?</h2>',
            ),
            (
                '<h2 class="sec-t">Pro e Contro di Vivere nel <strong>Nucleo Antico</strong></h2>',
                '<h2 class="sec-t">Quali sono i <strong>pro e i contro</strong> di vivere nel nucleo antico?</h2>',
            ),
            (
                '<h2 class="sec-t">Quanto vale la tua casa in <strong>Centro Storico</strong>?</h2>',
                '<h2 class="sec-t">Quanto vale oggi un immobile nel <strong>Centro Storico</strong>?</h2>',
            ),
        ],
    ),
    (
        "zona-guizza-padova.html",
        [
            (
                '<h2 class="sec-t">Un quartiere <strong>autentico e accessibile</strong></h2>',
                '<h2 class="sec-t">Che carattere ha oggi la <strong>Guizza</strong> a Padova sud?</h2>',
            ),
            (
                '<h2 class="sec-t">Servizi, parchi e <strong>vita di quartiere</strong></h2>',
                '<h2 class="sec-t">Quali <strong>servizi e parchi</strong> offre la Guizza ai residenti?</h2>',
            ),
            (
                '<h2 class="sec-t">Prezzi e andamento <strong>del mercato locale</strong></h2>',
                '<h2 class="sec-t">Come sono <strong>prezzi e domanda</strong> sul mercato della Guizza?</h2>',
            ),
            (
                '<h2 class="sec-t">Cosa si trova <strong>in vendita nella zona</strong></h2>',
                '<h2 class="sec-t">Quali <strong>immobili</strong> si trovano piu spesso in vendita in Guizza?</h2>',
            ),
            (
                '<h2 class="sec-t">Come muoversi <strong>dal quartiere</strong></h2>',
                '<h2 class="sec-t">Come collegarsi <strong>dalla Guizza</strong> al centro e alla tangenziale?</h2>',
            ),
            (
                '<h2 class="sec-t">Pro e Contro di Vivere alla <strong>Guizza</strong></h2>',
                '<h2 class="sec-t">Quali sono i <strong>pro e i contro</strong> di vivere alla Guizza?</h2>',
            ),
            (
                '<h2 class="sec-t">Quanto vale la tua casa in <strong>Guizza</strong>?</h2>',
                '<h2 class="sec-t">Quanto vale oggi una casa in <strong>Guizza</strong>?</h2>',
            ),
        ],
    ),
    (
        "zona-forcellini-padova.html",
        [
            (
                '<h2 class="sec-t">Il volto <strong>residenziale dell\'est padovano</strong></h2>',
                '<h2 class="sec-t">Che ruolo ha <strong>Forcellini</strong> nell\'est residenziale di Padova?</h2>',
            ),
            (
                '<h2 class="sec-t">Tranquillita, servizi e <strong>qualita della vita</strong></h2>',
                '<h2 class="sec-t">Quali <strong>servizi e qualita della vita</strong> offre Forcellini?</h2>',
            ),
            (
                '<h2 class="sec-t">Prezzi e tendenze <strong>del mercato locale</strong></h2>',
                '<h2 class="sec-t">Come si comportano <strong>prezzi e tendenze</strong> a Forcellini?</h2>',
            ),
            (
                '<h2 class="sec-t">Cosa si trova <strong>in vendita nella zona</strong></h2>',
                '<h2 class="sec-t">Quali <strong>tipologie</strong> dominano il mercato a Forcellini?</h2>',
            ),
            (
                '<h2 class="sec-t">Come muoversi <strong>dal quartiere</strong></h2>',
                '<h2 class="sec-t">Come raggiungere <strong>ospedale, universita e tangenziale</strong> da Forcellini?</h2>',
            ),
            (
                '<h2 class="sec-t">Pro e Contro di Vivere a <strong>Forcellini</strong></h2>',
                '<h2 class="sec-t">Quali sono i <strong>pro e i contro</strong> di vivere a Forcellini?</h2>',
            ),
            (
                '<h2 class="sec-t">Quanto vale la tua casa a <strong>Forcellini</strong>?</h2>',
                '<h2 class="sec-t">Quanto vale oggi un appartamento a <strong>Forcellini</strong>?</h2>',
            ),
        ],
    ),
    (
        "zona-limena.html",
        [
            (
                '<h2 class="sec-t">Qualita\' di vita <strong>a due passi</strong> dal capoluogo</h2>',
                '<h2 class="sec-t">Perche <strong>Limena</strong> e scelta per la qualita di vita vicino a Padova?</h2>',
            ),
            (
                '<h2 class="sec-t">Prezzi e <strong>opportunita\'</strong> sul mercato locale</h2>',
                '<h2 class="sec-t">Come sono <strong>prezzi e opportunita</strong> sul mercato di Limena?</h2>',
            ),
            (
                '<h2 class="sec-t">Cosa si trova <strong>sul mercato</strong></h2>',
                '<h2 class="sec-t">Quali <strong>immobili</strong> si trovano piu spesso a Limena?</h2>',
            ),
            (
                '<h2 class="sec-t">Muoversi <strong>verso la citta\' e il Veneto</strong></h2>',
                '<h2 class="sec-t">Come collegarsi <strong>da Limena</strong> a Padova e al Veneto?</h2>',
            ),
            (
                '<h2 class="sec-t">Pro e Contro di Vivere a <strong>Limena</strong></h2>',
                '<h2 class="sec-t">Quali sono i <strong>pro e i contro</strong> di vivere a Limena?</h2>',
            ),
        ],
    ),
    (
        "zona-prato-della-valle-padova.html",
        [
            (
                '<h2 class="sec-t">La piazza piu grande <strong>d\'Italia</strong></h2>',
                '<h2 class="sec-t">Perche vivere vicino a <strong>Prato della Valle</strong> attira acquirenti?</h2>',
            ),
            (
                '<h2 class="sec-t">Prezzi e <strong>tendenze</strong> nell\'area monumentale</h2>',
                '<h2 class="sec-t">Come sono <strong>prezzi e tendenze</strong> nell\'area di Prato della Valle?</h2>',
            ),
            (
                '<h2 class="sec-t">Tipologie di <strong>immobili disponibili</strong></h2>',
                '<h2 class="sec-t">Quali <strong>tipologie immobiliari</strong> caratterizzano la zona?</h2>',
            ),
            (
                '<h2 class="sec-t">Trasporti e <strong>collegamenti</strong></h2>',
                '<h2 class="sec-t">Come muoversi <strong>da Prato della Valle</strong> verso il resto della citta?</h2>',
            ),
            (
                '<h2 class="sec-t">Pro e Contro di Vivere a <strong>Prato della Valle</strong></h2>',
                '<h2 class="sec-t">Quali sono i <strong>pro e i contro</strong> di vivere a Prato della Valle?</h2>',
            ),
            (
                '<h2 class="sec-t">Quanto vale la tua casa a <strong>Prato della Valle</strong>?</h2>',
                '<h2 class="sec-t">Quanto vale oggi una casa vicino a <strong>Prato della Valle</strong>?</h2>',
            ),
        ],
    ),
    (
        "zona-sacra-famiglia-padova.html",
        [
            (
                '<h2 class="sec-t">Un paese <strong>nella citta</strong></h2>',
                '<h2 class="sec-t">Perche la <strong>Sacra Famiglia</strong> e descritta come un paese nella citta?</h2>',
            ),
            (
                '<h2 class="sec-t">Prezzi e <strong>tendenze</strong> nel quartiere residenziale</h2>',
                '<h2 class="sec-t">Come evolvono <strong>prezzi e tendenze</strong> alla Sacra Famiglia?</h2>',
            ),
            (
                '<h2 class="sec-t">Tipologie di <strong>immobili disponibili</strong></h2>',
                '<h2 class="sec-t">Quali <strong>tipologie</strong> si trovano piu spesso in zona?</h2>',
            ),
            (
                '<h2 class="sec-t">Trasporti e <strong>collegamenti</strong></h2>',
                '<h2 class="sec-t">Come collegarsi <strong>dalla Sacra Famiglia</strong> a scuole e servizi?</h2>',
            ),
            (
                '<h2 class="sec-t">Quanto vale la tua casa alla <strong>Sacra Famiglia</strong>?</h2>',
                '<h2 class="sec-t">Quanto vale oggi un immobile alla <strong>Sacra Famiglia</strong>?</h2>',
            ),
        ],
    ),
    (
        "zona-universitaria-padova.html",
        [
            (
                '<h2 class="sec-t">Il quartiere degli atenei: dove <strong>la storia incontra l\'investimento</strong></h2>',
                '<h2 class="sec-t">Perche la <strong>zona universitaria</strong> unisce storia e investimento?</h2>',
            ),
            (
                '<h2 class="sec-t">Cultura, servizi e <strong>vita vibrante</strong></h2>',
                '<h2 class="sec-t">Quali <strong>cultura e servizi</strong> definiscono la vita in zona?</h2>',
            ),
            (
                '<h2 class="sec-t">Prezzi, rendite e <strong>opportunita di investimento</strong></h2>',
                '<h2 class="sec-t">Come sono <strong>prezzi e rendite</strong> per chi investe in locazione?</h2>',
            ),
            (
                '<h2 class="sec-t">Cosa si trova <strong>in vendita nel quartiere degli atenei</strong></h2>',
                '<h2 class="sec-t">Quali <strong>immobili</strong> dominano il mercato vicino agli atenei?</h2>',
            ),
            (
                '<h2 class="sec-t">Come muoversi <strong>nell\'area accademica</strong></h2>',
                '<h2 class="sec-t">Come muoversi <strong>nell\'area accademica</strong> senza auto?</h2>',
            ),
            (
                '<h2 class="sec-t">Quanto vale la tua casa in <strong>Zona Universitaria</strong>?</h2>',
                '<h2 class="sec-t">Quanto vale oggi un immobile in <strong>zona universitaria</strong>?</h2>',
            ),
        ],
    ),
    (
        "zona-voltabarozzo-padova.html",
        [
            (
                '<h2 class="sec-t">Dove la citta <strong>incontra il fiume</strong></h2>',
                '<h2 class="sec-t">Perche <strong>Voltabarozzo</strong> e strategico tra citta e Bacchiglione?</h2>',
            ),
            (
                '<h2 class="sec-t">Verde, sport e <strong>comunita coesa</strong></h2>',
                '<h2 class="sec-t">Quali <strong>verde e sport</strong> caratterizzano il quartiere?</h2>',
            ),
            (
                '<h2 class="sec-t">Prezzi e opportunita <strong>a Voltabarozzo</strong></h2>',
                '<h2 class="sec-t">Come sono <strong>prezzi e opportunita</strong> a Voltabarozzo?</h2>',
            ),
            (
                '<h2 class="sec-t">Cosa si trova <strong>in vendita nel quartiere</strong></h2>',
                '<h2 class="sec-t">Quali <strong>immobili</strong> si trovano piu spesso in vendita?</h2>',
            ),
            (
                '<h2 class="sec-t">Come muoversi <strong>dal quartiere</strong></h2>',
                '<h2 class="sec-t">Come collegarsi <strong>da Voltabarozzo</strong> a Padova e tangenziale?</h2>',
            ),
            (
                '<h2 class="sec-t">Quanto vale la tua casa a <strong>Voltabarozzo</strong>?</h2>',
                '<h2 class="sec-t">Quanto vale oggi una casa a <strong>Voltabarozzo</strong>?</h2>',
            ),
        ],
    ),
    (
        "zona-rubano.html",
        [
            (
                '<h2 class="sec-t">Qualita\' di vita <strong>e servizi</strong> a ovest del capoluogo</h2>',
                '<h2 class="sec-t">Perche <strong>Rubano</strong> attira famiglie a ovest di Padova?</h2>',
            ),
            (
                '<h2 class="sec-t">Prezzi e <strong>opportunita\'</strong> sul mercato locale</h2>',
                '<h2 class="sec-t">Come sono <strong>prezzi e opportunita</strong> sul mercato di Rubano?</h2>',
            ),
            (
                '<h2 class="sec-t">Cosa si trova <strong>sul mercato</strong></h2>',
                '<h2 class="sec-t">Quali <strong>immobili</strong> caratterizzano l\'offerta a Rubano?</h2>',
            ),
            (
                '<h2 class="sec-t">Muoversi <strong>verso la citta\' e il Veneto</strong></h2>',
                '<h2 class="sec-t">Come raggiungere <strong>Padova e il Veneto</strong> da Rubano?</h2>',
            ),
        ],
    ),
    (
        "zona-vigonza.html",
        [
            (
                '<h2 class="sec-t">Qualita\' di vita <strong>e servizi</strong> a nord-est di Padova</h2>',
                '<h2 class="sec-t">Perche <strong>Vigonza</strong> e scelta a nord-est del capoluogo?</h2>',
            ),
            (
                '<h2 class="sec-t">Prezzi e <strong>opportunita\'</strong> nel mercato locale</h2>',
                '<h2 class="sec-t">Come sono <strong>prezzi e opportunita</strong> nel mercato di Vigonza?</h2>',
            ),
            (
                '<h2 class="sec-t">Cosa si trova <strong>sul mercato</strong></h2>',
                '<h2 class="sec-t">Quali <strong>tipologie</strong> si trovano piu spesso sul mercato?</h2>',
            ),
            (
                '<h2 class="sec-t">Muoversi <strong>verso Padova e il Veneto</strong></h2>',
                '<h2 class="sec-t">Come collegarsi <strong>da Vigonza</strong> a Padova e al Veneto?</h2>',
            ),
        ],
    ),
    (
        "zona-selvazzano.html",
        [
            (
                '<h2 class="sec-t">Qualita\' di vita <strong>tra verde e servizi</strong></h2>',
                '<h2 class="sec-t">Perche <strong>Selvazzano</strong> unisce verde e servizi vicino a Padova?</h2>',
            ),
            (
                '<h2 class="sec-t">Prezzi e <strong>opportunita\'</strong> nel territorio a ovest del capoluogo</h2>',
                '<h2 class="sec-t">Come sono <strong>prezzi e opportunita</strong> a ovest di Padova?</h2>',
            ),
            (
                '<h2 class="sec-t">Cosa si trova <strong>in questa zona residenziale</strong></h2>',
                '<h2 class="sec-t">Quali <strong>immobili</strong> caratterizzano Selvazzano residenziale?</h2>',
            ),
            (
                '<h2 class="sec-t">Muoversi <strong>dal comune verso Padova</strong></h2>',
                '<h2 class="sec-t">Come raggiungere <strong>Padova</strong> da Selvazzano ogni giorno?</h2>',
            ),
        ],
    ),
    (
        "zona-ponte-san-nicolo.html",
        [
            (
                '<h2 class="sec-t">Qualita\' della vita <strong>alle porte di Padova</strong></h2>',
                '<h2 class="sec-t">Perche <strong>Ponte San Nicolo\'</strong> e ambita alle porte di Padova?</h2>',
            ),
            (
                '<h2 class="sec-t">Prezzi e <strong>opportunita\'</strong> nel territorio a sud-est</h2>',
                '<h2 class="sec-t">Come sono <strong>prezzi e opportunita</strong> a sud-est del capoluogo?</h2>',
            ),
            (
                '<h2 class="sec-t">Tipologie di <strong>immobili disponibili</strong></h2>',
                '<h2 class="sec-t">Quali <strong>tipologie</strong> dominano il mercato locale?</h2>',
            ),
            (
                '<h2 class="sec-t">Come raggiungere <strong>il capoluogo e il Veneto</strong></h2>',
                '<h2 class="sec-t">Come raggiungere <strong>Padova e il Veneto</strong> da Ponte San Nicolo\'?</h2>',
            ),
            (
                '<h2 class="sec-t">Pro e Contro di Vivere a <strong>Ponte San Nicolo\'</strong></h2>',
                '<h2 class="sec-t">Quali sono i <strong>pro e i contro</strong> di vivere a Ponte San Nicolo\'?</h2>',
            ),
        ],
    ),
    (
        "zona-abano-terme.html",
        [
            (
                '<h2 class="sec-t">Eleganza termale <strong>alle porte di Padova</strong></h2>',
                '<h2 class="sec-t">Perche <strong>Abano Terme</strong> unisce eleganza termale e vicinanza a Padova?</h2>',
            ),
            (
                '<h2 class="sec-t">Prezzi e <strong>opportunita\'</strong> nella localita\' ai piedi dei Colli</h2>',
                '<h2 class="sec-t">Come sono <strong>prezzi e opportunita</strong> ai piedi dei Colli Euganei?</h2>',
            ),
            (
                '<h2 class="sec-t">Tipologie di <strong>immobili disponibili</strong></h2>',
                '<h2 class="sec-t">Quali <strong>tipologie</strong> si trovano piu spesso sul mercato termale?</h2>',
            ),
            (
                '<h2 class="sec-t">Come raggiungere <strong>Padova e il Veneto</strong></h2>',
                '<h2 class="sec-t">Come collegarsi <strong>da Abano</strong> a Padova e al Veneto?</h2>',
            ),
        ],
    ),
]

# Snippet CSS: primo paragrafo dopo H2 in .sec-text piu leggibile (snippet AEO visivo)
CSS_SNIPPET = """
    .sec-inner > .sec-text > p:first-of-type{font-size:.9rem;line-height:1.82;color:var(--nero);font-weight:500;max-width:800px}
"""


def main() -> int:
    for fname, pairs in REPLACEMENTS:
        path = ROOT / fname
        if not path.exists():
            print("MISSING", fname)
            continue
        text = path.read_text(encoding="utf-8")
        orig = text
        for old, new in pairs:
            if old not in text:
                print("WARN skip (not found):", fname, old[:60])
                continue
            text = text.replace(old, new, 1)
        if CSS_SNIPPET.strip() not in text and ".sec-inner > .sec-text > p:first-of-type" not in text:
            text = text.replace("</style>", CSS_SNIPPET + "\n  </style>", 1)
        if text != orig:
            path.write_text(text, encoding="utf-8")
            print("OK", fname)
        else:
            print("UNCHANGED", fname)
    return 0


if __name__ == "__main__":
    sys.exit(main())
