# -*- coding: utf-8 -*-
"""Relazione di valutazione — CISCATO Teresa, Via Magarotto 23/A Limena."""
from __future__ import annotations

from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image as RLImage,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent.parent
LOGO_PATH = ROOT / "img" / "brand" / "logo-righetto-ri.png"
MAP_PATH = ROOT / "documenti" / "mappa_catasto_ciscato_limena.png"
OUT_PDF = ROOT / "documenti" / "Relazione_Valutazione_Immobile_Limena_CISCATO.pdf"

NERO = colors.HexColor("#152435")
BLU = colors.HexColor("#2C4A6E")
ORO = colors.HexColor("#FF6B35")
SFONDO = colors.HexColor("#ECE7DF")
GRIGIO = colors.HexColor("#6B7A8D")

DATA = date(2026, 7, 14)
VALORE_MIN = 235_000
VALORE_MAX = 250_000


class RighettoCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved: list[dict] = []

    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved) + 1
        for i, state in enumerate(self._saved):
            self.__dict__.update(state)
            self._frame(i + 1, total)
            canvas.Canvas.showPage(self)
        self.__dict__.update(self._saved[-1] if self._saved else {})
        self._frame(total, total)
        canvas.Canvas.save(self)

    def _frame(self, n: int, total: int):
        w, h = A4
        self.setStrokeColor(BLU)
        self.setLineWidth(1.2)
        self.rect(10 * mm, 12 * mm, w - 20 * mm, h - 22 * mm, stroke=1, fill=0)
        self.setFillColor(ORO)
        self.rect(10 * mm, h - 12 * mm - 2, w - 20 * mm, 2, stroke=0, fill=1)
        self.setFillColor(NERO)
        self.rect(10 * mm, 12 * mm, w - 20 * mm, 8 * mm, stroke=0, fill=1)
        self.setFillColor(colors.white)
        self.setFont("Helvetica", 6.8)
        self.drawString(
            14 * mm,
            15.5 * mm,
            "Gruppo Immobiliare Righetto di Capon Gino — Via Dalmazia 22, Curtarolo (PD) — Tel. 049.8843484 — info@righettoimmobiliare.it",
        )
        self.drawRightString(w - 14 * mm, 15.5 * mm, f"Relazione riservata — Pag. {n}/{total}")


def styled_table(rows: list[list], col_widths: list[float], header: bool = False) -> Table:
    t = Table(rows, colWidths=col_widths)
    style = [
        ("BOX", (0, 0), (-1, -1), 0.5, BLU),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#E1DBD1")),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), BLU),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]
    else:
        style += [("BACKGROUND", (0, 0), (0, -1), BLU), ("TEXTCOLOR", (0, 0), (0, -1), colors.white)]
    t.setStyle(TableStyle(style))
    return t


def build() -> None:
    styles = getSampleStyleSheet()
    title = ParagraphStyle("T", parent=styles["Heading1"], fontSize=18, textColor=BLU, alignment=TA_CENTER, spaceAfter=4)
    subtitle = ParagraphStyle("S", parent=styles["Normal"], fontSize=9, textColor=GRIGIO, alignment=TA_CENTER, spaceAfter=8)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=11, textColor=BLU, spaceBefore=6, spaceAfter=3, fontName="Helvetica-Bold")
    body = ParagraphStyle("B", parent=styles["Normal"], fontSize=9.5, leading=13, textColor=NERO, alignment=TA_JUSTIFY, spaceAfter=5)
    small = ParagraphStyle("Sm", parent=body, fontSize=8, textColor=GRIGIO)

    doc = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=22 * mm,
        title="Relazione di valutazione immobiliare — Limena",
        author="Gruppo Immobiliare Righetto di Capon Gino",
    )
    story: list = []

    logo = Paragraph("", body)
    if LOGO_PATH.is_file():
        logo = RLImage(str(LOGO_PATH), width=26 * mm, height=26 * mm)

    hdr = Table(
        [[
            logo,
            Paragraph(
                '<font name="Helvetica-Bold" size="12" color="#2C4A6E">GRUPPO IMMOBILIARE RIGHETTO</font><br/>'
                '<font size="9" color="#152435"><b>di Capon Gino</b></font><br/>'
                '<font size="7.5" color="#6B7A8D">Via Dalmazia 22 — 35010 Curtarolo (PD)</font><br/>'
                '<font size="7.5" color="#152435">Tel. 049.8843484 · info@righettoimmobiliare.it</font><br/>'
                '<font size="7" color="#6B7A8D">PEC gino.capon@pec.it · P.IVA 05182390285 · C.F. CPNGNI69A27A952T</font><br/>'
                '<font size="7" color="#6B7A8D">Iscrizione CCIAA di Padova</font>',
                ParagraphStyle("hdr", leading=10),
            ),
            Paragraph(
                f'<font size="8" color="#6B7A8D">Data relazione</font><br/>'
                f'<font size="11" color="#152435"><b>{DATA.strftime("%d/%m/%Y")}</b></font>',
                ParagraphStyle("dt", alignment=TA_CENTER),
            ),
        ]],
        colWidths=[30 * mm, 100 * mm, 44 * mm],
    )
    hdr.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (1, 0), (1, 0), 1, BLU),
        ("BACKGROUND", (1, 0), (1, 0), SFONDO),
        ("LEFTPADDING", (1, 0), (1, 0), 8),
        ("TOPPADDING", (1, 0), (1, 0), 6),
        ("BOTTOMPADDING", (1, 0), (1, 0), 6),
    ]))
    story += [hdr, Spacer(1, 6 * mm)]
    story += [
        Paragraph("RELAZIONE DI VALUTAZIONE IMMOBILIARE", title),
        Paragraph("Documento riservato — stima di mercato a scopo informativo e negoziale", subtitle),
    ]

    story.append(styled_table([
        ["Committente", "Sig.ra CISCATO Teresa"],
        ["Immobile", "Via Magarotto n. 23/A — Limena (PD)"],
        ["Valutazione indicativa", f"€ {VALORE_MIN:,.0f} – € {VALORE_MAX:,.0f}".replace(",", ".")],
    ], [52 * mm, 122 * mm]))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("1. Dati anagrafici committente", h2))
    story.append(styled_table([
        ["Cognome", "CISCATO"],
        ["Nome", "TERESA"],
        ["Codice fiscale", "CSCTRS39R57D226O"],
        ["Luogo di nascita", "Curtarolo (PD)"],
        ["Data di nascita", "17/10/1939"],
        ["Diritto reale", "Proprietà 1000/1000"],
    ], [48 * mm, 126 * mm]))
    story.append(Spacer(1, 3 * mm))

    story.append(Paragraph("2. Identificazione catastale", h2))
    story.append(Paragraph(
        "Dati desunti dalla visura catastale richiesta in data 14/07/2026 — Ufficio Territoriale di Padova.",
        body,
    ))
    cat = [
        ["U.I.", "Foglio", "Part.", "Sub", "Categoria", "Cl.", "Consistenza", "Rendita", "Piano / indirizzo"],
        ["1", "13", "705", "73", "A/2", "02", "6 vani", "€ 511,29", "Via Magarotto — S1-T"],
        ["2", "13", "705", "78", "C/6", "01", "30 m²", "€ 46,48", "Via Magarotto — S1 (garage)"],
    ]
    tc = Table(cat, colWidths=[12 * mm, 14 * mm, 14 * mm, 12 * mm, 18 * mm, 10 * mm, 22 * mm, 22 * mm, 50 * mm])
    tc.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLU),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("BACKGROUND", (0, 1), (-1, -1), SFONDO),
        ("BOX", (0, 0), (-1, -1), 0.5, BLU),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#E1DBD1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(tc)
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph(
        "<b>Comune:</b> Limena (codice catastale E592) — Provincia di Padova.",
        small,
    ))

    story.append(Paragraph("3. Descrizione dell'immobile", h2))
    story.append(Paragraph(
        "Unità abitativa di categoria <b>A/2</b> (abitazione di tipo civile), composta da "
        "<b>cucina separata</b>, <b>soggiorno</b>, <b>due bagni</b> e <b>taverna</b>, "
        "con annesso <b>garage triplo</b> (categoria <b>C/6</b>, 30 m² catastali) e "
        "<b>terrazza vivibile</b> e <b>giardino privato</b>. L'edificio risulta realizzato "
        "nei <b>primi anni 2000</b>, in zona residenziale di Limena, comune della cintura "
        "padovana con buona accessibilità verso Padova e principali servizi locali.",
        body,
    ))

    story.append(Paragraph("4. Valutazione economica di mercato", h2))
    story.append(Paragraph(
        "Sulla base delle caratteristiche dell'immobile, della consistenza catastale (6 vani + garage), "
        "della localizzazione in Limena e del confronto con transazioni e offerte analoghe nel segmento "
        "villetta/villetta a schiera con spazi esterni, si esprime una "
        f"<b>valutazione di mercato indicativa compresa tra € {VALORE_MIN:,.0f} e € {VALORE_MAX:,.0f}</b>.".replace(",", "."),
        body,
    ))
    val_box = Table(
        [[Paragraph(
            f'<font size="11" color="#F7F5F1">Valutazione indicativa</font><br/>'
            f'<font size="22" color="#FF6B35"><b>€ {VALORE_MIN:,.0f} – € {VALORE_MAX:,.0f}</b></font>'.replace(",", "."),
            ParagraphStyle("v", alignment=TA_CENTER, leading=28),
        )]],
        colWidths=[174 * mm],
    )
    val_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NERO),
        ("BOX", (0, 0), (-1, -1), 1.5, ORO),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    story += [Spacer(1, 3 * mm), val_box]

    story.append(Spacer(1, 4 * mm))
    story.append(
        KeepTogether([
            Paragraph("5. Note e limiti della stima", h2),
            Paragraph(
                "La presente relazione ha carattere <b>indicativo</b> e non sostituisce una perizia "
                "tecnico-giuridica redatta da perito abilitato né una revisione urbanistico-edilizia "
                "approfondita. Il valore effettivo di compravendita può variare in funzione di stato "
                "manutentivo, conformità documentale, eventuali vincoli, condizioni contrattuali e "
                "andamento del mercato al momento della trattativa. "
                "<b>Compenso di mediazione da concordare in sede</b> nel mandato — nessun listino online.",
                small,
            ),
        ])
    )

    story.append(PageBreak())
    story.append(Paragraph("6. Localizzazione catastale", h2))
    story.append(Paragraph(
        "Estratto cartografico catastale — Foglio <b>13</b>, Particella <b>705</b>, Comune di Limena (E592). "
        "Fonte: portale Agenzia delle Entrate.",
        body,
    ))
    story.append(Spacer(1, 3 * mm))
    if MAP_PATH.is_file():
        story.append(RLImage(str(MAP_PATH), width=174 * mm, height=120 * mm))
    else:
        story.append(Paragraph("<i>Mappa catastale non disponibile.</i>", small))

    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph(
        f"<i>Documento redatto il {DATA.strftime('%d/%m/%Y')} — Gruppo Immobiliare Righetto di Capon Gino — Uso riservato Sig.ra CISCATO Teresa</i>",
        ParagraphStyle("f", alignment=TA_CENTER, fontSize=8, textColor=GRIGIO),
    ))

    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    doc.build(story, canvasmaker=RighettoCanvas)
    dl = Path.home() / "Downloads" / OUT_PDF.name
    dl.write_bytes(OUT_PDF.read_bytes())
    print(f"OK: {OUT_PDF} ({OUT_PDF.stat().st_size // 1024} KB)")
    print(f"Copia: {dl}")


if __name__ == "__main__":
    build()
