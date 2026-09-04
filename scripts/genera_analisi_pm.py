#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Report schematico gestione 15 immobili — Piazzola, Camposampiero, Padova.

Uso:
  python scripts/genera_analisi_pm.py
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

from PIL import Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image as RLImage,
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
COPERTINA = ROOT / "documenti" / "perizie" / "assets" / "villa_contarini_piazzola_copertina.jpg"

NERO = colors.HexColor("#152435")
BLU = colors.HexColor("#2C4A6E")
ORO = colors.HexColor("#FF6B35")
SFONDO = colors.HexColor("#ECE7DF")
GRIGIO = colors.HexColor("#6B7A8D")
VERDE = colors.HexColor("#1B6B4A")

CANONE_ESEMPIO = 800  # ipotesi bilocale/trilocale zona


def _esc(text: str) -> str:
    return str(text or "—").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fmt_euro(n: float | int) -> str:
    return f"€ {int(round(n)):,}".replace(",", ".")


class ReportCanvas(canvas.Canvas):
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
        if self._saved:
            self.__dict__.update(self._saved[-1])
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
        self.setFont("Helvetica", 7)
        self.drawString(14 * mm, 15.5 * mm, "Bertinato Gino — Righetto Immobiliare — 049.8843484")
        self.drawRightString(w - 14 * mm, 15.5 * mm, f"Gestione locazioni — Pag. {n}/{total}")


def fit_image(path: Path, max_w: float, max_h: float) -> RLImage:
    with Image.open(path) as im:
        w, h = im.size
    ratio = h / w
    iw, ih = max_w, max_w * ratio
    if ih > max_h:
        ih = max_h
        iw = ih / ratio
    return RLImage(str(path), width=iw, height=ih)


def tbl(header: list[str], rows: list[list[str]], widths: list[float], size: float = 10) -> Table:
    th = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=size, leading=12, textColor=colors.white)
    td = ParagraphStyle("td", fontName="Helvetica", fontSize=size, leading=13, textColor=NERO)
    data: list[list] = [[Paragraph(_esc(c), th) for c in header]]
    for row in rows:
        data.append([Paragraph(_esc(c), td) for c in row])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLU),
        ("BACKGROUND", (0, 1), (-1, -1), SFONDO),
        ("BOX", (0, 0), (-1, -1), 1, BLU),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D4CEC4")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def titolo_box(testo: str) -> Table:
    ps = ParagraphStyle("tb", fontName="Helvetica-Bold", fontSize=11, textColor=colors.white, alignment=TA_CENTER)
    t = Table([[Paragraph(testo, ps)]], colWidths=[174 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), VERDE),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def build_story(data_doc: date) -> list:
    c = CANONE_ESEMPIO
    h1 = ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=15, textColor=BLU, alignment=TA_CENTER, spaceAfter=3)
    h2 = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=12, textColor=BLU, spaceBefore=10, spaceAfter=6)
    body = ParagraphStyle("B", fontName="Helvetica", fontSize=10, leading=14, textColor=NERO, alignment=TA_JUSTIFY, spaceAfter=4)
    small = ParagraphStyle("Sm", fontName="Helvetica", fontSize=8, textColor=GRIGIO, alignment=TA_CENTER)

    story: list = []

    # ── COPERTINA CON FOTO ──
    if LOGO_PATH.is_file():
        story.append(RLImage(str(LOGO_PATH), width=28 * mm, height=28 * mm))
        story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("PROPOSTA GESTIONE LOCAZIONI", h1))
    story.append(Paragraph("15 immobili — Piazzola sul Brenta · Camposampiero · Padova", ParagraphStyle(
        "s", fontSize=10, textColor=GRIGIO, alignment=TA_CENTER, spaceAfter=6,
    )))
    if COPERTINA.is_file():
        story.append(fit_image(COPERTINA, 174 * mm, 95 * mm))
        story.append(Spacer(1, 2 * mm))
        story.append(Paragraph(
            "Villa Contarini — Piazzola sul Brenta (PD) · foto Wikimedia Commons, CC BY 2.5",
            small,
        ))
    story.append(Spacer(1, 4 * mm))
    story.append(tbl(
        ["", ""],
        [
            ["Destinatario", "Sig. Canton Romeo"],
            ["Data", data_doc.strftime("%d/%m/%Y")],
            ["Agenzia", "Gruppo Immobiliare Bertinato Gino"],
            ["Portafoglio", "15 immobili ipotetici in locazione"],
            ["Zone", "Piazzola sul Brenta, Camposampiero, Padova"],
        ],
        [50 * mm, 124 * mm],
    ))

    # ── CONTRATTI 12-18 MESI ──
    story.append(PageBreak())
    story.append(titolo_box("CONTRATTI DA 12 A 18 MESI"))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph(
        "Gestione completa: ci occupiamo noi di tutto. Piccole problematiche, idraulico, elettricista — "
        "chiamiamo noi, coordiniamo noi. La proprietaria non deve fare nulla.",
        body,
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(tbl(
        ["Periodo", "Compenso proprietario", "Cosa include"],
        [
            ["Primo anno", "1 mensilità del canone", "Avvio + gestione + piccole urgenze + tecnici"],
            ["Anni successivi", "½ mensilità del canone", "Gestione ordinaria continuativa"],
            ["Nuovo inquilino", "€ 0", "Paga il conduttore (1 mensilità — prassi di mercato)"],
        ],
        [38 * mm, 52 * mm, 84 * mm],
    ))

    # ── AFFITTI SOTTO 3 MESI ──
    story.append(Spacer(1, 8 * mm))
    story.append(titolo_box("AFFITTI SOTTO I 3 MESI"))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph(
        "I contratti molto brevi si ripetono più volte l'anno: più consegne, più verifiche, più lavoro. "
        "In mercato si applica di solito una <b>maggiorazione</b> sulla gestione (non una seconda commissione al proprietario).",
        body,
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(tbl(
        ["Voce", "Cosa applichiamo", "Come funziona di solito"],
        [
            ["Primo anno", "1 mensilità", "Come contratto lungo — avvio immobile"],
            ["Gestione annua", "½ mensilità + 30%", "Maggiorazione per alto turnover"],
            ["Nuovo inquilino", "€ 0 proprietario", "Paga il conduttore (1 mensilità)"],
            ["Proroga stesso inquilino", "¼ mensilità", "Solo rinnovo, senza nuove visite"],
            ["Pulizie fine locazione", "A carico proprietario", "Le coordiniamo noi"],
        ],
        [42 * mm, 48 * mm, 84 * mm],
        size=9.5,
    ))

    # ── ESEMPIO 1 APPARTAMENTO ──
    story.append(PageBreak())
    story.append(Paragraph("Esempio — 1 appartamento", h2))
    story.append(Paragraph(
        f"Canone ipotetico <b>{fmt_euro(c)}/mese</b> (bilocale/trilocale zona Piazzola–Camposampiero–Padova).",
        body,
    ))
    story.append(Spacer(1, 4 * mm))

    story.append(Paragraph("<b>Contratto 12 mesi</b>", ParagraphStyle("h3", parent=body, fontName="Helvetica-Bold", textColor=BLU)))
    story.append(tbl(
        ["", "Importo"],
        [
            ["Canone incassato dal proprietario (12 mesi)", fmt_euro(c * 12)],
            ["Compenso agenzia — anno 1 (1 mens.)", fmt_euro(c)],
            ["Compenso agenzia — anni dopo (½ mens.)", fmt_euro(c // 2)],
            ["Nuovo inquilino — costo proprietario", "€ 0"],
            ["Netto proprietario anno 1", fmt_euro(c * 12 - c)],
            ["Netto proprietario anni dopo", fmt_euro(c * 12 - c // 2)],
        ],
        [110 * mm, 64 * mm],
    ))
    story.append(Spacer(1, 6 * mm))

    gest_breve = round(c * 0.5 * 1.30)
    story.append(Paragraph("<b>Contratto 2 mesi</b> (es. 5 inquilini l'anno)", ParagraphStyle(
        "h3b", parent=body, fontName="Helvetica-Bold", textColor=BLU,
    )))
    story.append(tbl(
        ["", "Importo"],
        [
            ["Canone incassato (5 locazioni × 2 mesi)", fmt_euro(c * 2 * 5)],
            ["Compenso agenzia — anno 1 (1 mens.)", fmt_euro(c)],
            ["Compenso agenzia — gestione (+30%)", fmt_euro(gest_breve)],
            ["Nuovo inquilino — costo proprietario", "€ 0 (paga conduttore)"],
            ["Pulizie stimate (5 uscite)", "€ 400 – 600"],
            ["Netto proprietario indicativo anno 1", fmt_euro(c * 10 - c - gest_breve - 500)],
        ],
        [110 * mm, 64 * mm],
    ))

    # ── PORTAFOGLIO 15 ──
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph("Portafoglio 15 immobili — totali indicativi", h2))
    story.append(tbl(
        ["", "Contratto 12–18 mesi", "Contratto sotto 3 mesi"],
        [
            ["Compenso agenzia anno 1 (15 immobili)", fmt_euro(15 * c), fmt_euro(15 * c)],
            ["Compenso agenzia anni dopo / gestione", fmt_euro(15 * (c // 2)), fmt_euro(15 * gest_breve)],
            ["Canone totale incassato (15 immobili)", fmt_euro(15 * c * 12), fmt_euro(15 * c * 10)],
            ["Referente unico per tutto", "Sì", "Sì"],
        ],
        [54 * mm, 60 * mm, 60 * mm],
        size=9.5,
    ))
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph(
        "Canoni e compensi calcolati su ipotesi {canone}/mese — da adattare immobile per immobile.".format(canone=fmt_euro(c)),
        ParagraphStyle("foot", alignment=TA_CENTER, fontSize=8, textColor=GRIGIO),
    ))
    story.append(Paragraph(
        f"Bertinato Gino · Righetto Immobiliare · {data_doc.strftime('%d/%m/%Y')}",
        small,
    ))

    return story


def build_pdf(out_path: Path, data_doc: date) -> Path:
    doc = SimpleDocTemplate(
        str(out_path), pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=16 * mm, bottomMargin=22 * mm,
    )
    doc.build(build_story(data_doc), canvasmaker=ReportCanvas)
    return out_path


def main() -> int:
    data_doc = date(2026, 9, 4)
    out_name = "Analisi_PM_Portafoglio15_Canton_Romeo.pdf"
    out_pdf = ROOT / "documenti" / "perizie" / out_name
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    build_pdf(out_pdf, data_doc)
    archive = ROOT / "data" / "perizie" / out_name
    archive.parent.mkdir(parents=True, exist_ok=True)
    archive.write_bytes(out_pdf.read_bytes())
    print(f"OK: {out_pdf} ({out_pdf.stat().st_size // 1024} KB)")
    print(f"Archivio: {archive}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
