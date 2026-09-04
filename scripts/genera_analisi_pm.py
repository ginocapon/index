#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Report gestione locazioni — Gruppo Immobiliare Righetto di Capon Gino.

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

AZIENDA = "Gruppo Immobiliare Righetto di Capon Gino"
IVA = 0.22
CANONE = 800
REG = 50
ASS = 50


def _esc(text: str) -> str:
    return str(text or "—").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fmt_euro(n: float | int) -> str:
    return f"€ {int(round(n)):,}".replace(",", ".")


def ivato(imponibile: float | int) -> int:
    return int(round(float(imponibile) * (1 + IVA)))


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
        self.setStrokeColor(colors.HexColor("#2C4A6E"))
        self.setLineWidth(1.2)
        self.rect(10 * mm, 12 * mm, w - 20 * mm, h - 22 * mm, stroke=1, fill=0)
        self.setFillColor(colors.HexColor("#FF6B35"))
        self.rect(10 * mm, h - 12 * mm - 2, w - 20 * mm, 2, stroke=0, fill=1)
        self.setFillColor(colors.HexColor("#152435"))
        self.rect(10 * mm, 12 * mm, w - 20 * mm, 8 * mm, stroke=0, fill=1)
        self.setFillColor(colors.white)
        self.setFont("Helvetica", 7)
        self.drawString(14 * mm, 15.5 * mm, f"{AZIENDA} — Limena (PD) — 049.8843484")
        self.drawRightString(w - 14 * mm, 15.5 * mm, f"Proposta gestione — Pag. {n}/{total}")


BLU = colors.HexColor("#2C4A6E")
SFONDO = colors.HexColor("#ECE7DF")
GRIGIO = colors.HexColor("#6B7A8D")
VERDE = colors.HexColor("#1B6B4A")
RIGHE_VERDE = colors.HexColor("#E8F5EE")


def fit_image(path: Path, max_w: float, max_h: float) -> RLImage:
    with Image.open(path) as im:
        w, h = im.size
    ratio = h / w
    iw, ih = max_w, max_w * ratio
    if ih > max_h:
        ih = max_h
        iw = ih / ratio
    return RLImage(str(path), width=iw, height=ih)


def tbl(header: list[str], rows: list[list[str]], widths: list[float], size: float = 9.5, highlight_last: bool = False) -> Table:
    th = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=size, leading=11, textColor=colors.white)
    td = ParagraphStyle("td", fontName="Helvetica", fontSize=size, leading=12, textColor=colors.HexColor("#152435"))
    data: list[list] = [[Paragraph(_esc(c), th) for c in header]]
    for row in rows:
        data.append([Paragraph(_esc(c), td) for c in row])
    t = Table(data, colWidths=widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), BLU),
        ("BACKGROUND", (0, 1), (-1, -1), SFONDO),
        ("BOX", (0, 0), (-1, -1), 1, BLU),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D4CEC4")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    if highlight_last and len(rows) > 0:
        style.append(("BACKGROUND", (0, len(rows)), (-1, len(rows)), RIGHE_VERDE))
        style.append(("FONTNAME", (0, len(rows)), (-1, len(rows)), "Helvetica-Bold"))
    t.setStyle(TableStyle(style))
    return t


def band(text: str, bg=VERDE) -> Table:
    ps = ParagraphStyle("bd", fontName="Helvetica-Bold", fontSize=10.5, textColor=colors.white, alignment=TA_CENTER)
    t = Table([[Paragraph(text, ps)]], colWidths=[174 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), bg), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return t


def build_story(data_doc: date) -> list:
    c = CANONE
    mens_ivata = ivato(c)
    reg_ivata = ivato(REG)
    ass_ivata = ivato(ASS)
    nostra_trans = mens_ivata + reg_ivata + ass_ivata
    nostra_std = mens_ivata + reg_ivata
    proroga_ivata = ivato(c * 0.25)

    # Ipotesi mercato (fonti: Instahome, prassi agenzie — 1 mens. + % annua; ass. ~150 €)
    mercato_mens_ivata = ivato(c)
    mercato_pct_ivata = ivato(c * 12 * 0.15)  # 15% canone annuo
    mercato_ass = "€ 150 – 180"
    mercato_trans_tot = "~€ 1.130 – 1.160"  # 976 + 150-180 indicativo

    h1 = ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=15, textColor=BLU, alignment=TA_CENTER, spaceAfter=4)
    h2 = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=11.5, textColor=BLU, spaceBefore=8, spaceAfter=5)
    body = ParagraphStyle("B", fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=colors.HexColor("#152435"), alignment=TA_JUSTIFY, spaceAfter=4)
    sm = ParagraphStyle("Sm", fontName="Helvetica", fontSize=7.5, textColor=GRIGIO, alignment=TA_CENTER)

    story: list = []

    # ── COPERTINA ──
    if LOGO_PATH.is_file():
        story.append(RLImage(str(LOGO_PATH), width=30 * mm, height=30 * mm))
        story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("PROPOSTA GESTIONE LOCAZIONI", h1))
    story.append(Paragraph("Piazzola sul Brenta · Camposampiero · Padova", ParagraphStyle("sub", fontSize=10, textColor=GRIGIO, alignment=TA_CENTER, spaceAfter=5)))
    if COPERTINA.is_file():
        story.append(fit_image(COPERTINA, 174 * mm, 88 * mm))
        story.append(Paragraph("Villa Contarini — Piazzola sul Brenta (PD)", sm))
    story.append(Spacer(1, 4 * mm))
    story.append(tbl(
        ["", ""],
        [
            ["Destinatario", "Sig. Canton Romeo"],
            ["Agenzia", AZIENDA],
            ["Data", data_doc.strftime("%d/%m/%Y")],
            ["Portafoglio", "15 immobili — locazione 1–18 mesi"],
            ["Mandato", "Contratto annuale — rinnovo tacito — disdetta 30 gg"],
        ],
        [48 * mm, 126 * mm],
    ))

    # ── PAG. 2: COSA FACCIAMO + REGOLE ──
    story.append(PageBreak())
    story.append(band("LA NOSTRA GESTIONE — IN BREVE"))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(
        "Referente unico per tutto il portafoglio. Seguiamo l'immobile, gestiamo contratti e inquilini. "
        "Per <b>riparazioni e interventi tecnici</b> i costi restano <b>a carico del proprietario</b>: "
        "lo avvisiamo sempre via <b>WhatsApp</b> della problematica e dell'importo che l'impresa esecutrice "
        "addebiterà; coordiniamo noi idraulico, elettricista o altri tecnici.",
        body,
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(tbl(
        ["Situazione", "Cosa paga il proprietario"],
        [
            ["Stipula contratto (qualsiasi durata 1–18 mesi)", "1 mensilità canone + € 50 registrazione + IVA"],
            ["Stipula contratto transitorio", "Sopra + € 50 asseverazione + IVA"],
            ["Nuovo inquilino", "€ 0 — paga il conduttore (1 mensilità)"],
            ["Proroga stesso inquilino", "¼ mensilità + IVA"],
            ["Pulizie fine locazione", "A carico proprietario — le coordiniamo noi"],
            ["Riparazioni / manutenzioni", "A carico proprietario — avviso WhatsApp + preventivo"],
        ],
        [72 * mm, 102 * mm],
    ))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(
        "<b>Contratto di mandato</b> annuale tra Sig. Canton Romeo e " + AZIENDA + ", "
        "con <b>rinnovo tacito</b> salvo <b>disdetta scritta con 30 giorni</b> di preavviso.",
        body,
    ))

    # ── PAG. 3: MERCATO VS NOI ──
    story.append(Spacer(1, 6 * mm))
    story.append(band("CONFRONTO 1 — Cosa chiedono di solito le altre agenzie"))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        f"Esempio appartamento <b>{fmt_euro(c)}/mese</b>, contratto 1–18 mesi, zona Padova nord "
        "(Piazzola, Camposampiero). Prassi di mercato (Instahome e agenzie locali):",
        body,
    ))
    story.append(Spacer(1, 2 * mm))
    story.append(tbl(
        ["Voce", "Mercato tipico", "Note"],
        [
            ["Trova inquilino — proprietario", f"1 mensilità ({fmt_euro(mercato_mens_ivata)} ivata)", "Spesso anche conduttore paga 1 mens."],
            ["Gestione continuativa", f"10–15% annuo ({fmt_euro(mercato_pct_ivata)} ivata su € 9.600)", "Non sempre separata"],
            ["Registrazione contratto", "Inclusa o a parte", "Adempimento obbligatorio"],
            ["Asseverazione transitorio", mercato_ass, "Obbligatoria se transitorio agevolato"],
            ["Proroga / rinnovo", "Spesso nuova mensilità", "Variabile per agenzia"],
        ],
        [44 * mm, 58 * mm, 72 * mm],
        size=8.8,
    ))

    story.append(Spacer(1, 6 * mm))
    story.append(band("CONFRONTO 2 — La nostra offerta Righetto (più chiara e competitiva)", colors.HexColor("#1B6B4A")))
    story.append(Spacer(1, 3 * mm))
    story.append(tbl(
        ["Voce", "Righetto — imponibile", "Righetto — ivato (22%)"],
        [
            ["1 mensilità gestione/stipula", fmt_euro(c), fmt_euro(mens_ivata)],
            ["Registrazione", fmt_euro(REG), fmt_euro(reg_ivata)],
            ["Asseverazione (solo transitorio)", fmt_euro(ASS), fmt_euro(ass_ivata)],
            ["Totale transitorio", fmt_euro(c + REG + ASS), fmt_euro(nostra_trans)],
            ["Totale contratto ordinario", fmt_euro(c + REG), fmt_euro(nostra_std)],
            ["Nuovo inquilino — proprietario", "€ 0", "€ 0"],
            ["Proroga stesso inquilino", fmt_euro(c * 0.25), fmt_euro(proroga_ivata)],
        ],
        [58 * mm, 58 * mm, 58 * mm],
        highlight_last=False,
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(tbl(
        ["", "Mercato transitorio", "Righetto transitorio", "Vantaggio"],
        [
            ["Costo proprietario indicativo", mercato_trans_tot, fmt_euro(nostra_trans), "Accessori più bassi"],
            ["Nuovo inquilino", "Spesso doppia commissione", "€ 0 proprietario", "Risparmio netto"],
            ["Comunicazione riparazioni", "Variabile", "WhatsApp + preventivo", "Trasparenza"],
        ],
        [40 * mm, 44 * mm, 44 * mm, 46 * mm],
        size=8.8,
        highlight_last=False,
    ))

    # ── PAG. 4: ESEMPI NUMERICI ──
    story.append(PageBreak())
    story.append(Paragraph("Esempio pratico — 1 appartamento € 800/mese", h2))

    story.append(Paragraph("<b>A) Contratto transitorio 12 mesi</b>", ParagraphStyle("h3", parent=body, fontName="Helvetica-Bold", textColor=BLU)))
    story.append(tbl(
        ["", "Proprietario", "Conduttore"],
        [
            ["Canone incassato (12 mesi)", fmt_euro(c * 12), "—"],
            ["Compenso agenzia (stipula)", fmt_euro(nostra_trans), fmt_euro(mens_ivata)],
            ["Riparazioni", "A carico proprietario", "—"],
            ["Netto indicativo proprietario", fmt_euro(c * 12 - nostra_trans), "—"],
        ],
        [68 * mm, 53 * mm, 53 * mm],
    ))

    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("<b>B) Proroga stesso inquilino (senza nuove visite)</b>", ParagraphStyle("h3b", parent=body, fontName="Helvetica-Bold", textColor=BLU)))
    story.append(tbl(
        ["", "Importo"],
        [
            ["Compenso agenzia (¼ mensilità + IVA)", fmt_euro(proroga_ivata)],
            ["Nuove visite / annuncio", "Non necessario"],
        ],
        [110 * mm, 64 * mm],
    ))

    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("<b>C) Portafoglio 15 immobili</b> (ipotesi: 8 nuove stipule transitorio/anno)", ParagraphStyle("h3c", parent=body, fontName="Helvetica-Bold", textColor=BLU)))
    story.append(tbl(
        ["", "Totale indicativo"],
        [
            ["Canoni annui incassati (15 × € 800 × 12)", fmt_euro(15 * c * 12)],
            ["Compensi agenzia da proprietario (8 stipule × " + fmt_euro(nostra_trans) + ")", fmt_euro(8 * nostra_trans)],
            ["Compensi da conduttori (8 × " + fmt_euro(mens_ivata) + ")", fmt_euro(8 * mens_ivata)],
            ["Referente unico + WhatsApp per tutto", "Incluso nel mandato"],
        ],
        [110 * mm, 64 * mm],
        highlight_last=True,
    ))

    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph(
        "Tutti i compensi agenzia indicati sono <b>+ IVA 22%</b> dove applicabile. "
        "Canone € 800/mese è ipotesi per Piazzola–Camposampiero–Padova — da confermare per ogni unità. "
        "Fonte prassi mercato: Instahome (costi agenzia affitto), normativa contratto transitorio.",
        sm,
    ))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(f"{AZIENDA} · Limena (PD) · {data_doc.strftime('%d/%m/%Y')}", sm))

    return story


def build_pdf(out_path: Path, data_doc: date) -> Path:
    doc = SimpleDocTemplate(str(out_path), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=22 * mm)
    doc.build(build_story(data_doc), canvasmaker=ReportCanvas)
    return out_path


def main() -> int:
    data_doc = date(2026, 9, 4)
    out_name = "Analisi_PM_Portafoglio15_Canton_Romeo.pdf"
    out_pdf = ROOT / "documenti" / "perizie" / out_name
    out_pdf.parent.mkdir(parents=True, exist_ok=True)
    build_pdf(out_pdf, data_doc)
    archive = ROOT / "data" / "perizie" / out_name
    archive.write_bytes(out_pdf.read_bytes())
    print(f"OK: {out_pdf} ({out_pdf.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
