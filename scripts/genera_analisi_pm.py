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

    canone_annuo = c * 12

    # Mercato — fonti: Instahome (10–15% annuo), Rentila (7–8% gestione annua), RealAdvisor (1 mens.)
    # Asseverazione transitorio: indicativamente € 150–200 imponibile (+ IVA) presso agenzie/CA
    mercato_mens_ivata = ivato(c)
    mercato_reg_ivata = ivato(100)          # pratiche registrazione (mercato spesso € 80–150)
    mercato_ass_ivata = ivato(200)          # asseverazione (€ 150–200 imponibile di mercato)
    mercato_gest_8_ivata = ivato(canone_annuo * 0.08)   # gestione continuativa ~8% (Rentila)
    mercato_gest_12_ivata = ivato(canone_annuo * 0.12)  # fascia media-alta
    mercato_pct_15_ivata = ivato(canone_annuo * 0.15)   # modello percentuale (Instahome)

    # Scenario A: solo stipula transitorio (minimo mercato)
    mercato_solo_stipula = mercato_mens_ivata + mercato_reg_ivata + mercato_ass_ivata

    # Scenario B: stipula + gestione annua 8–12% (gestione completa tipica)
    mercato_completo_min = mercato_mens_ivata + mercato_reg_ivata + mercato_ass_ivata + mercato_gest_8_ivata
    mercato_completo_max = mercato_mens_ivata + mercato_reg_ivata + mercato_ass_ivata + mercato_gest_12_ivata

    # Scenario C: 15% canone annuo + oneri (alternativa molto diffusa)
    mercato_pct15_tot = mercato_pct_15_ivata + mercato_reg_ivata + mercato_ass_ivata

    risparmio_vs_solo = mercato_solo_stipula - nostra_trans
    risparmio_vs_completo_min = mercato_completo_min - nostra_trans
    risparmio_vs_completo_max = mercato_completo_max - nostra_trans
    risparmio_vs_pct15 = mercato_pct15_tot - nostra_trans

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
        ["Voce", "Cosa paga il proprietario"],
        [
            ["Contratto locazione", "1 mensilità + € 50 registrazione + IVA"],
            ["Contratto transitorio", "1 mensilità + € 50 registrazione + € 50 asseverazione + IVA"],
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

    # ── PAG. 3: RIGHETTO PRIMA, POI MERCATO + RISPARMIO ──
    story.append(PageBreak())
    story.append(band("LA NOSTRA OFFERTA RIGHETTO — 1 appartamento € 800/mese", colors.HexColor("#1B6B4A")))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "Tariffa unica per ogni stipula, <b>senza percentuali annue</b> sul canone. Tutti gli importi + IVA 22%.",
        body,
    ))
    story.append(Spacer(1, 2 * mm))
    story.append(tbl(
        ["Voce Righetto", "Imponibile", "Ivato (22%)"],
        [
            ["1 mensilità canone", fmt_euro(c), fmt_euro(mens_ivata)],
            ["Registrazione", fmt_euro(REG), fmt_euro(reg_ivata)],
            ["Asseverazione (transitorio)", fmt_euro(ASS), fmt_euro(ass_ivata)],
            ["Totale transitorio", fmt_euro(c + REG + ASS), fmt_euro(nostra_trans)],
            ["Totale contratto locazione", fmt_euro(c + REG), fmt_euro(nostra_std)],
        ],
        [58 * mm, 58 * mm, 58 * mm],
    ))

    story.append(Spacer(1, 6 * mm))
    story.append(band("COSA CHIEDE IL MERCATO — stesso appartamento"))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "Zona Piazzola sul Brenta, Camposampiero, Padova. Verifica su fonti di settore (Instahome, Rentila, "
        "RealAdvisor): le agenzie applicano spesso <b>più voci sommate</b> — non solo la mensilità.",
        body,
    ))
    story.append(Spacer(1, 2 * mm))
    story.append(tbl(
        ["Voce mercato", "Importo ivato (22%)", "Note"],
        [
            ["1 mensilità canone (proprietario)", fmt_euro(mercato_mens_ivata), "Quasi sempre"],
            ["Oppure 15% canone annuo", fmt_euro(mercato_pct_15_ivata), "Alternativa frequente"],
            ["Pratiche registrazione", fmt_euro(mercato_reg_ivata), "€ 80–150 + IVA"],
            ["Asseverazione transitorio", f"{fmt_euro(ivato(180))} – {fmt_euro(ivato(250))}", "€ 180–250 + IVA"],
            ["Gestione annua 8%", fmt_euro(mercato_gest_8_ivata), "Aggiuntiva, ogni anno"],
            ["Gestione annua 12%", fmt_euro(mercato_gest_12_ivata), "Gestione strutturata"],
        ],
        [52 * mm, 44 * mm, 78 * mm],
        size=8.5,
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(tbl(
        ["Scenario mercato (1 anno)", "Totale ivato proprietario"],
        [
            ["A — Solo stipula transitorio", fmt_euro(mercato_solo_stipula)],
            ["B — Stipula + gestione 8% annua", fmt_euro(mercato_completo_min)],
            ["C — Stipula + gestione 12% annua", fmt_euro(mercato_completo_max)],
            ["D — 15% canone annuo + oneri", fmt_euro(mercato_pct15_tot)],
        ],
        [90 * mm, 84 * mm],
    ))

    story.append(Spacer(1, 6 * mm))
    story.append(band("RIGHETTO VS MERCATO — quanto risparmi", colors.HexColor("#2C4A6E")))
    story.append(Spacer(1, 3 * mm))
    story.append(tbl(
        ["Scenario", "Righetto", "Mercato", "Risparmio"],
        [
            [
                "A — Solo stipula",
                fmt_euro(nostra_trans),
                fmt_euro(mercato_solo_stipula),
                fmt_euro(risparmio_vs_solo),
            ],
            [
                "B — Stipula + gest. 8%",
                fmt_euro(nostra_trans),
                fmt_euro(mercato_completo_min),
                fmt_euro(risparmio_vs_completo_min),
            ],
            [
                "C — Stipula + gest. 12%",
                fmt_euro(nostra_trans),
                fmt_euro(mercato_completo_max),
                fmt_euro(risparmio_vs_completo_max),
            ],
            [
                "D — 15% annuo + oneri",
                fmt_euro(nostra_trans),
                fmt_euro(mercato_pct15_tot),
                fmt_euro(risparmio_vs_pct15),
            ],
            [
                "15 immobili — 8 stipule (scen. B)",
                fmt_euro(8 * nostra_trans),
                fmt_euro(8 * mercato_completo_min),
                fmt_euro(8 * risparmio_vs_completo_min),
            ],
        ],
        [40 * mm, 42 * mm, 42 * mm, 50 * mm],
        size=8.5,
        highlight_last=True,
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "Il risparmio più significativo si vede quando il mercato applica anche la <b>gestione annua</b> "
        "(8–15% del canone): in quel caso Righetto resta su <b>1 mensilità + € 50 + € 50 + IVA</b> "
        "per stipula, senza percentuali ricorrenti sul canone.",
        body,
    ))

    # ── PAG. 4: ESEMPIO PRATICO ──
    story.append(PageBreak())
    story.append(Paragraph("Esempio pratico — 1 appartamento € 800/mese", h2))

    story.append(Paragraph("<b>Contratto transitorio 12 mesi</b>", ParagraphStyle("h3", parent=body, fontName="Helvetica-Bold", textColor=BLU)))
    story.append(tbl(
        ["", "Importo"],
        [
            ["Canone incassato (12 mesi)", fmt_euro(c * 12)],
            ["Compenso agenzia Righetto (ivato)", fmt_euro(nostra_trans)],
            ["Riparazioni", "A carico proprietario (avviso WhatsApp)"],
            ["Netto indicativo proprietario", fmt_euro(c * 12 - nostra_trans)],
        ],
        [110 * mm, 64 * mm],
    ))

    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("<b>Portafoglio 15 immobili</b> (8 stipule transitorio/anno)", ParagraphStyle("h3c", parent=body, fontName="Helvetica-Bold", textColor=BLU)))
    story.append(tbl(
        ["", "Totale indicativo"],
        [
            ["Canoni annui incassati (15 × € 800 × 12)", fmt_euro(15 * c * 12)],
            ["Compensi agenzia da proprietario (8 × " + fmt_euro(nostra_trans) + ")", fmt_euro(8 * nostra_trans)],
            ["Risparmio vs mercato (scen. B, 8 stipule)", fmt_euro(8 * risparmio_vs_completo_min)],
            ["Referente unico + WhatsApp", "Incluso nel mandato annuale"],
        ],
        [110 * mm, 64 * mm],
        highlight_last=False,
    ))

    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph(
        "Tutti i compensi agenzia indicati sono <b>+ IVA 22%</b> dove applicabile. "
        "Canone € 800/mese è ipotesi per Piazzola–Camposampiero–Padova — da confermare per ogni unità. "
        "Fonti: Instahome (10–15% annuo), Rentila (7–8% gestione annua), RealAdvisor (provvigioni affitto). "
        "Scenari indicativi — ogni agenzia applica condizioni diverse.",
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
