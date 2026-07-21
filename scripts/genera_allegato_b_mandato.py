# -*- coding: utf-8 -*-
"""
Genera Allegato B — Scheda informativa comproprietari (Word)
Output: documenti/Allegato-B-Scheda-Informativa-Mandato-Esclusivo-Comproprieta.docx
"""
from __future__ import annotations

from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "documenti" / "Allegato-B-Scheda-Informativa-Mandato-Esclusivo-Comproprieta.docx"


def style_doc(doc: Document) -> None:
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(11)


def add_center(doc: Document, text: str, *, bold: bool = False, size: int = 14) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    r.font.name = "Times New Roman"


def add_body(doc: Document, text: str, *, bold: bool = False, size: int = 11) -> None:
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = bold
    r.font.name = "Times New Roman"
    r.font.size = Pt(size)


def add_heading(doc: Document, text: str) -> None:
    h = doc.add_heading(text, level=2)
    for r in h.runs:
        r.font.name = "Times New Roman"
        r.font.color.rgb = RGBColor(0x2C, 0x4A, 0x6E)


def add_bullets(doc: Document, items: list[str]) -> None:
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        r = p.add_run(item)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)


def add_table(doc: Document, headers: list[str], rows: list[list[str]]) -> None:
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    for i, h in enumerate(headers):
        table.rows[0].cells[i].text = h
    for ri, row in enumerate(rows):
        for ci, cell in enumerate(row):
            table.rows[ri + 1].cells[ci].text = cell


def build() -> Path:
    doc = Document()
    style_doc(doc)
    sec = doc.sections[0]
    sec.top_margin = Cm(2)
    sec.bottom_margin = Cm(2)
    sec.left_margin = Cm(2.5)
    sec.right_margin = Cm(2.5)

    today = date.today().strftime("%d/%m/%Y")

    add_center(doc, "GRUPPO IMMOBILIARE RIGHETTO", bold=True, size=13)
    add_center(doc, "Allegato B — Cosa sapere prima di firmare", bold=True, size=12)
    add_center(doc, "Mandato esclusivo · comproprietari", size=11)
    add_center(doc, f"Revisione {today}", size=10)
    doc.add_paragraph()

    add_body(
        doc,
        "Questa scheda spiega in modo semplice le regole del mandato. Fa fede il contratto "
        "firmato in agenzia; qui trovi solo un riassunto per capire chi paga cosa.",
    )
    doc.add_paragraph()

    add_heading(doc, "1. La provvigione — chi paga quanto")
    add_body(
        doc,
        "La provvigione dell'agenzia (es. 3% + IVA sul prezzo di vendita) si divide in base "
        "alla quota di proprietà di ciascuno.",
    )
    add_table(
        doc,
        ["Situazione", "Chi paga", "Quanto"],
        [
            [
                "Vendita conclusa e tutti firmano",
                "Ogni comproprietario",
                "Solo la propria parte (es. 1/3 se tre fratelli uguali)",
            ],
            [
                "Uno vuole vendere a prezzo pieno e firma",
                "Chi firma",
                "Solo la propria parte — non paga per gli altri",
            ],
            [
                "Uno si rifiuta di firmare a prezzo pieno senza motivo valido",
                "Solo chi rifiuta",
                "Penale = tutta la provvigione (100%)",
            ],
            [
                "Offerta sotto il prezzo del mandato",
                "—",
                "Nessuna penale; si può ridiscutere",
            ],
        ],
    )
    add_body(
        doc,
        "Esempio numerico: casa € 300.000, provvigione 3% = € 9.000 (+ IVA). Tre fratelli al "
        "33,33% ciascuno → ognuno paga € 3.000 (+ IVA) se la vendita si chiude. Se uno solo si "
        "rifiuta di firmare a € 300.000 senza motivo valido → quello paga € 9.000 (+ IVA) "
        "all'agenzia a titolo di penale; gli altri no.",
        bold=True,
    )

    add_heading(doc, "2. Acquirente al prezzo del mandato")
    add_bullets(
        doc,
        [
            "Se l'agenzia trova un acquirente al prezzo del mandato (o superiore), tutti devono "
            "collaborare per chiudere (proposta, preliminare, rogito).",
            "Non basta che uno solo sia d'accordo: servono tutti per vendere.",
            "Chi si rifiuta senza motivo serio documentato paga personalmente la penale pari "
            "all'intera provvigione.",
            "Chi firma e collabora paga solo la propria quota, se la vendita si conclude.",
        ],
    )

    add_heading(doc, "3. Offerta più bassa del mandato")
    add_body(
        doc,
        "Se l'acquirente propone meno del prezzo del mandato (es. mandato € 300.000, offerta "
        "€ 280.000), ognuno è libero di non firmare e di ridiscutere. Nessuna penale e nessuna "
        "provvigione solo per il rifiuto.",
    )

    add_heading(doc, "4. Visite — chi abita in casa")
    add_bullets(
        doc,
        [
            "Almeno un giorno a settimana per le visite, concordato all'inizio.",
            "Chi vive nell'immobile deve permettere l'accesso, salvo accordo diverso scritto.",
            "Impossibilità per motivo serio: avvisare subito l'agenzia e fissare altro appuntamento.",
            "Bloccare le visite senza motivo può comportare penali.",
        ],
    )

    add_heading(doc, "5. Documenti, preliminare, consegna")
    add_bullets(
        doc,
        [
            "Dall'accordo con l'acquirente: documenti catastali e urbanistici completi.",
            "Preliminare: chi firma si impegna a rispettare quanto concordato.",
            "Consegna casa all'acquirente entro 6 mesi dal preliminare, salvo altro accordo scritto.",
        ],
    )

    add_heading(doc, "6. Chi vive in casa e non libera l'immobile")
    add_body(
        doc,
        "Se chi abita in casa, senza motivi previsti dal contratto, non consente visite o "
        "consegna, risponde di spese e danni verso acquirenti e agenzia. Con preliminare già "
        "firmato, possono valere anche le regole del preliminare (es. doppia caparra "
        "all'acquirente, ove previsto).",
    )

    add_heading(doc, "7. Prima di firmare")
    add_bullets(
        doc,
        [
            "Controllare Allegato A (nomi e quote).",
            "Concordare il giorno delle visite se qualcuno abita in casa.",
            "Segnalare ipoteche o vincoli sulla propria quota.",
            "Dubbi? 049.8843484 · info@righettoimmobiliare.it",
        ],
    )

    doc.add_paragraph()
    add_body(
        doc,
        "Dichiarazione — Dichiaro di aver letto questa scheda e di aver potuto fare domande in "
        "agenzia prima di firmare il mandato.",
        bold=True,
    )
    doc.add_paragraph()

    for n in range(1, 5):
        add_body(doc, f"Comproprietario {n}", bold=True)
        add_body(doc, "Nome: _________________________________  Data: ___/___/______")
        add_body(doc, "Firma: _________________________________")
        doc.add_paragraph()

    add_body(
        doc,
        f"Allegato B informativo — revisione {today}. Non sostituisce il contratto di mediazione.",
        size=9,
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(OUT))
    return OUT


if __name__ == "__main__":
    path = build()
    print(f"OK: {path}")
