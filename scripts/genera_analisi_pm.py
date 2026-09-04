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
ASSEV = 50


def _esc(text: str) -> str:
    return str(text or "—").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fmt_euro(n: float | int) -> str:
    return f"€ {int(round(n)):,}".replace(",", ".")


def ivato(imponibile: float | int) -> int:
    return int(round(float(imponibile) * (1 + IVA)))


NERO = colors.HexColor("#152435")
BLU = colors.HexColor("#2C4A6E")
ORO = colors.HexColor("#FF6B35")
SFONDO = colors.HexColor("#ECE7DF")
GRIGIO = colors.HexColor("#6B7A8D")
VERDE = colors.HexColor("#1B6B4A")


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
        self.drawString(14 * mm, 15.5 * mm, f"{AZIENDA} — Limena (PD) — 049.8843484")
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


def tbl(header: list[str], rows: list[list[str]], widths: list[float], size: float = 9.5) -> Table:
    th = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=size, leading=11, textColor=colors.white)
    td = ParagraphStyle("td", fontName="Helvetica", fontSize=size, leading=12, textColor=NERO)
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
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def titolo_verde(testo: str) -> Table:
    ps = ParagraphStyle("tv", fontName="Helvetica-Bold", fontSize=11, textColor=colors.white, alignment=TA_CENTER)
    t = Table([[Paragraph(testo, ps)]], colWidths=[174 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), VERDE),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def offerta_righetto_transitorio() -> tuple[int, int, int]:
    """Imponibile e totale IVA inclusa — contratto transitorio."""
    imp = CANONE + REG + ASSEV
    return imp, ivato(imp), ivato(CANONE)


def build_story(data_doc: date) -> list:
    imp_tr, tot_tr, mens_ivata = offerta_righetto_transitorio()
    proroga_imp = CANONE // 4
    proroga_tot = ivato(proroga_imp)

    # Mercato indicativo su € 800/mese — fonti Rentila, CSI (guide pubbliche)
    mercato_gest_annua = int(CANONE * 12 * 0.075)  # ~7,5% canone annuo
    mercato_reg = "150 – 250"
    mercato_assev = "80 – 150"

    h1 = ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=15, textColor=BLU, alignment=TA_CENTER, spaceAfter=3)
    h2 = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=12, textColor=BLU, spaceBefore=8, spaceAfter=5)
    body = ParagraphStyle("B", fontName="Helvetica", fontSize=10, leading=14, textColor=NERO, alignment=TA_JUSTIFY, spaceAfter=4)
    small = ParagraphStyle("Sm", fontName="Helvetica", fontSize=7.5, textColor=GRIGIO, alignment=TA_CENTER)

    story: list = []

    # ── COPERTINA ──
    if LOGO_PATH.is_file():
        story.append(RLImage(str(LOGO_PATH), width=28 * mm, height=28 * mm))
        story.append(Spacer(1, 3 * mm))
    story.append(Paragraph("PROPOSTA GESTIONE LOCAZIONI", h1))
    story.append(Paragraph("Piazzola sul Brenta · Camposampiero · Padova — 15 immobili", ParagraphStyle(
        "sub", fontSize=10, textColor=GRIGIO, alignment=TA_CENTER, spaceAfter=5,
    )))
    if COPERTINA.is_file():
        story.append(fit_image(COPERTINA, 174 * mm, 88 * mm))
        story.append(Paragraph("Villa Contarini — Piazzola sul Brenta (PD)", small))
    story.append(Spacer(1, 4 * mm))
    story.append(tbl(
        ["", ""],
        [
            ["Destinatario", "Sig. Canton Romeo"],
            ["Data", data_doc.strftime("%d/%m/%Y")],
            ["Agenzia", AZIENDA],
            ["Portafoglio", "15 immobili in locazione (1–18 mesi)"],
        ],
        [48 * mm, 126 * mm],
    ))

    # ── PAG. 2: MERCATO vs NOI ──
    story.append(PageBreak())
    story.append(titolo_verde("COSA CHIEDONO DI SOLITO LE ALTRE AGENZIE (contratti 1–18 mesi)"))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(
        f"Riferimento: appartamento <b>{fmt_euro(CANONE)}/mese</b> — zona Piazzola, Camposampiero, Padova. "
        "Sintesi da prassi di mercato (Rentila, CSI Immobili — guide online).",
        body,
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(tbl(
        ["Voce", "Mercato tipico", "Righetto — nostra offerta"],
        [
            ["Nuovo inquilino — proprietario", "Spesso 1 mens. extra", "€ 0 — paga il conduttore"],
            ["Nuovo inquilino — conduttore", "1 mensilità", "1 mensilità"],
            ["Gestione contratto (1–18 mesi)", f"7–8% annuo (~{fmt_euro(mercato_gest_annua)}/anno)", f"1 mens. a contratto ({fmt_euro(CANONE)} + IVA)"],
            ["Registrazione contratto", f"{mercato_reg} €", f"{fmt_euro(REG)} + IVA"],
            ["Asseverazione transitorio", f"{mercato_assev} €", f"{fmt_euro(ASSEV)} + IVA"],
            ["Proroga stesso inquilino", "Spesso ½ mensilità", f"¼ mens. ({fmt_euro(proroga_imp)} + IVA)"],
            ["Riparazioni", "Proprietario", "Proprietario — avviso WhatsApp + costo ditta"],
            ["Pulizie fine locazione", "Proprietario", "Proprietario — le coordiniamo noi"],
        ],
        [46 * mm, 58 * mm, 70 * mm],
        size=8.5,
    ))

    story.append(Spacer(1, 6 * mm))
    story.append(titolo_verde("LA NOSTRA OFFERTA — RIEPILOGO"))
    story.append(Spacer(1, 4 * mm))
    story.append(tbl(
        ["Voce", "Importo", "Note"],
        [
            ["Gestione per ogni contratto", f"{fmt_euro(CANONE)} + IVA", "1 mensilità — uguale se 1 o 18 mesi"],
            ["Registrazione", f"{fmt_euro(REG)} + IVA", "Per ogni contratto"],
            ["Asseverazione transitorio", f"{fmt_euro(ASSEV)} + IVA", "Solo contratti transitori"],
            ["Totale transitorio (imponibile)", fmt_euro(imp_tr), "Prima dell'IVA"],
            ["Totale transitorio (IVA incl.)", fmt_euro(tot_tr), "IVA 22%"],
            ["Proroga stesso inquilino", f"{fmt_euro(proroga_tot)}", "IVA incl. — niente nuove visite"],
            ["Nuovo inquilino", "€ 0 proprietario", "Provvigione a carico conduttore"],
        ],
        [52 * mm, 42 * mm, 80 * mm],
    ))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(
        "<b>Riparazioni:</b> sempre a carico del proprietario. Per ogni intervento inviamo "
        "<b>WhatsApp</b> con la problematica e il preventivo/costo della ditta esecutrice, "
        "poi coordiniamo idraulico, elettricista o altro tecnico.",
        body,
    ))

    # ── PAG. 3: ESEMPI NUMERICI ──
    story.append(PageBreak())
    story.append(Paragraph("Esempi concreti — canone 800 €/mese", h2))

    canone_12 = CANONE * 12
    story.append(Paragraph("<b>Esempio 1 — Contratto transitorio 12 mesi</b>", ParagraphStyle(
        "h3", parent=body, fontName="Helvetica-Bold", textColor=BLU,
    )))
    story.append(tbl(
        ["", "Mercato (indicativo)", "Righetto"],
        [
            ["Canone incassato dal proprietario", fmt_euro(canone_12), fmt_euro(canone_12)],
            ["Costo gestione — proprietario", f"~{fmt_euro(mercato_gest_annua)} (7,5% annuo)", fmt_euro(tot_tr)],
            ["Registrazione + asseverazione", "Inclusa nei costi sopra", f"Inclusa ({fmt_euro(REG)}+{fmt_euro(ASSEV)} + IVA)"],
            ["Nuovo inquilino — proprietario", "0 – 800 € (varia)", "€ 0"],
            ["Riparazioni (es. rubinetto)", "Proprietario", "Proprietario (WhatsApp)"],
            ["Netto proprietario indicativo", fmt_euro(canone_12 - mercato_gest_annua - 200), fmt_euro(canone_12 - tot_tr - 200)],
        ],
        [52 * mm, 58 * mm, 64 * mm],
        size=8.5,
    ))
    story.append(Paragraph(
        "<i>Ipotesi riparazione € 200 a carico proprietario — avvisata via WhatsApp prima dell'intervento.</i>",
        small,
    ))
    story.append(Spacer(1, 5 * mm))

    story.append(Paragraph("<b>Esempio 2 — Contratto transitorio 3 mesi</b> (stesso immobile, 4 contratti/anno)", ParagraphStyle(
        "h3b", parent=body, fontName="Helvetica-Bold", textColor=BLU,
    )))
    canone_3 = CANONE * 3
    canone_4x3 = canone_3 * 4
    costo_rig_4 = tot_tr * 4
    costo_mercato_4 = (mercato_gest_annua + 800) * 4  # gestione + spesso doppia commissione
    story.append(tbl(
        ["", "Mercato (indicativo)", "Righetto"],
        [
            ["Canone incassato (4 locazioni × 3 mesi)", fmt_euro(canone_4x3), fmt_euro(canone_4x3)],
            ["Costo gestione proprietario (×4 contratti)", f"~{fmt_euro(costo_mercato_4)}", fmt_euro(costo_rig_4)],
            ["Nuovo inquilino — proprietario", "Spesso 1 mens. ×4", "€ 0 (paga conduttore)"],
            ["Proroga stesso inquilino", "—", f"{fmt_euro(proroga_tot)} se rinnovo"],
            ["Pulizie (4 uscite, stimate)", "€ 400 – 600", "€ 400 – 600 (coordiniamo)"],
            ["Netto proprietario indicativo", fmt_euro(canone_4x3 - costo_mercato_4 - 500), fmt_euro(canone_4x3 - costo_rig_4 - 500)],
        ],
        [52 * mm, 58 * mm, 64 * mm],
        size=8.5,
    ))

    story.append(Spacer(1, 6 * mm))
    story.append(titolo_verde("PERCHÉ SIAMO COMPETITIVI"))
    story.append(Spacer(1, 3 * mm))
    story.append(tbl(
        ["Vantaggio Righetto", "Dettaglio"],
        [
            ["Niente doppia commissione", "Il conduttore paga la nuova locazione, non la proprietaria"],
            ["Prezzo fisso e chiaro", "1 mens. + € 50 + € 50 — stesso prezzo per 1 o 18 mesi"],
            ["Proroga economica", "¼ mensilità invece di ½ o nuova locazione"],
            ["Registrazione contenuta", f"{fmt_euro(REG)} + IVA vs {mercato_reg} € di mercato"],
            ["Comunicazione diretta", "WhatsApp su ogni problema e costo riparazione"],
            ["Referente unico", "15 immobili — un solo interlocutore"],
        ],
        [54 * mm, 120 * mm],
    ))

    # ── PAG. 4: PORTAFOGLIO 15 ──
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("Portafoglio 15 immobili — ipotesi annua", h2))
    story.append(tbl(
        ["Scenario", "Canoni incassati", "Costo gestione Righetto", "Nuovo inquilino proprietario"],
        [
            ["15 contratti da 12 mesi", fmt_euro(15 * canone_12), fmt_euro(15 * tot_tr), "€ 0"],
            ["15 contratti da 3 mesi (×4/anno)", fmt_euro(15 * canone_4x3), fmt_euro(15 * costo_rig_4), "€ 0"],
        ],
        [44 * mm, 44 * mm, 44 * mm, 42 * mm],
        size=8.5,
    ))
    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph(
        f"{AZIENDA} · Via Roma 96, Limena (PD) · {data_doc.strftime('%d/%m/%Y')} · "
        "Tutti gli importi Righetto + IVA 22%. Canone esempio € 800/mese.",
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
    return 0


if __name__ == "__main__":
    sys.exit(main())
