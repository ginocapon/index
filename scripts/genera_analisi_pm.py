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
NERO = colors.HexColor("#152435")
RIGHE_VERDE = colors.HexColor("#E8F5EE")
RIGHE_RISPARMIO = colors.HexColor("#FDE8E8")
ROSSO = colors.HexColor("#C0392B")


def fit_image(path: Path, max_w: float, max_h: float) -> RLImage:
    with Image.open(path) as im:
        w, h = im.size
    ratio = h / w
    iw, ih = max_w, max_w * ratio
    if ih > max_h:
        ih = max_h
        iw = ih / ratio
    return RLImage(str(path), width=iw, height=ih)


def p_td(text: str, *, bold: bool = False, color=NERO, size: float = 9.5) -> Paragraph:
    st = ParagraphStyle(
        "ptd", fontName="Helvetica-Bold" if bold else "Helvetica",
        fontSize=size, leading=12, textColor=color,
    )
    content = f"<b>{_esc(text)}</b>" if bold else _esc(text)
    return Paragraph(content, st)


def tbl(header: list[str], rows: list[list[str]], widths: list[float], size: float = 9.5, highlight_last: bool = False) -> Table:
    th = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=size, leading=11, textColor=colors.white)
    data: list[list] = [[Paragraph(_esc(c), th) for c in header]]
    for row in rows:
        data.append([p_td(c, size=size) for c in row])
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
    t.setStyle(TableStyle(style))
    return t


def tbl_righetto_prezzi(header: list[str], rows: list[list[str]], widths: list[float], size: float = 9.5) -> Table:
    """Tabella offerta Righetto — importi in grassetto nero."""
    th = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=size, leading=11, textColor=colors.white)
    data: list[list] = [[Paragraph(_esc(c), th) for c in header]]
    for i, row in enumerate(rows):
        cells = []
        for j, cell in enumerate(row):
            bold = j >= 1 or i >= len(rows) - 2  # imponibile, ivato e totali in grassetto nero
            cells.append(p_td(cell, bold=bold, color=NERO, size=size))
        data.append(cells)
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), VERDE),
        ("BACKGROUND", (0, 1), (-1, -3), SFONDO),
        ("BACKGROUND", (0, -2), (-1, -1), colors.HexColor("#F5F0E8")),
        ("BOX", (0, 0), (-1, -1), 1.5, VERDE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D4CEC4")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def tbl_confronto_risparmio(rows: list[list[str]], widths: list[float], size: float = 8.5) -> Table:
    """Confronto: Righetto grassetto nero, Risparmio in rosso."""
    th = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=size, leading=11, textColor=colors.white)
    header = ["Scenario annuo", "Righetto annuo (gest. incl.)", "Mercato annuo", "Risparmio annuo"]
    data: list[list] = [[Paragraph(_esc(c), th) for c in header]]
    for i, row in enumerate(rows):
        data.append([
            p_td(row[0], size=size),
            p_td(row[1], bold=True, color=NERO, size=size),
            p_td(row[2], size=size),
            p_td(row[3], bold=True, color=ROSSO, size=size + 0.5),
        ])
    t = Table(data, colWidths=widths, repeatRows=1)
    n = len(rows)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), BLU),
        ("BACKGROUND", (0, 1), (-1, -1), SFONDO),
        ("BACKGROUND", (1, 1), (1, -1), colors.HexColor("#F5F5F5")),
        ("BACKGROUND", (3, 1), (3, -1), RIGHE_RISPARMIO),
        ("BOX", (0, 0), (-1, -1), 1.5, BLU),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D4CEC4")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    if n > 0:
        style.append(("BACKGROUND", (0, n), (-1, n), RIGHE_RISPARMIO))
        style.append(("BACKGROUND", (3, n), (3, n), colors.HexColor("#F5C6C6")))
    t.setStyle(TableStyle(style))
    return t


def box_gestione_inclusa(lines: list[str]) -> Table:
    ps_t = ParagraphStyle("gi_t", fontName="Helvetica-Bold", fontSize=10, textColor=NERO, leading=12)
    ps_b = ParagraphStyle("gi_b", fontName="Helvetica", fontSize=9.5, textColor=NERO, leading=13)
    data: list[list] = [[Paragraph("<b>GESTIONE COMPLETA INCLUSA NEL PREZZO</b>", ps_t)]]
    for line in lines:
        data.append([Paragraph(line, ps_b)])
    box = Table(data, colWidths=[174 * mm])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFF8E7")),
        ("BOX", (0, 0), (-1, -1), 2, colors.HexColor("#FF6B35")),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return box


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
    story.append(box_gestione_inclusa([
        "La nostra tariffa è <b>annua per immobile</b> e <b>comprensiva della gestione completa</b> per tutto l'anno di mandato: "
        "referente unico, rapporto con l'inquilino, contratto, registrazione, scadenze, piccole urgenze, "
        "coordinamento tecnici. <b>Non si paga di nuovo a ogni nuovo contratto locativo</b> nello stesso anno — "
        "e <b>non si aggiungono percentuali annue</b> sul canone come spesso fa il mercato.",
        "Riparazioni e pulizie restano a carico del proprietario — con avviso WhatsApp prima di ogni intervento.",
    ]))
    story.append(Spacer(1, 3 * mm))
    story.append(tbl(
        ["Voce", "Compenso annuo proprietario (gestione inclusa)"],
        [
            ["Contratto locazione — costo annuo", "1 mensilità + € 50 registrazione + IVA — una volta all'anno per immobile"],
            ["Contratto transitorio — costo annuo", "1 mensilità + € 50 registrazione + € 50 asseverazione + IVA — una volta all'anno per immobile"],
            ["Pulizie fine locazione", "A carico proprietario — le coordiniamo noi"],
            ["Riparazioni / manutenzioni", "A carico proprietario — avviso WhatsApp + preventivo"],
        ],
        [72 * mm, 102 * mm],
    ))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph(
        "<b>Come leggere gli importi:</b> tutti i compensi Righetto indicati nel documento sono "
        "<b>annui per singolo immobile</b>, nell'ambito del mandato annuale. "
        "Una mensilità all'anno copre gestione e attività contrattuale — "
        "<b>non</b> si ripete l'addebito a ogni nuovo inquilino o rinnovo nello stesso anno di mandato.",
        body,
    ))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph(
        "<b>Contratto di mandato</b> annuale tra Sig. Canton Romeo e " + AZIENDA + ", "
        "con <b>rinnovo tacito</b> salvo <b>disdetta scritta con 30 giorni</b> di preavviso.",
        body,
    ))

    # ── PAG. 3: RIGHETTO PRIMA, POI MERCATO + RISPARMIO ──
    story.append(PageBreak())
    story.append(band("LA NOSTRA OFFERTA RIGHETTO — gestione completa inclusa", colors.HexColor("#1B6B4A")))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "Canone tipo <b>€ 800/mese</b>. <b>Compenso annuo per immobile</b> (1 mensilità + oneri) — "
        "<b>gestione dell'immobile inclusa per tutto l'anno di mandato</b>, "
        "senza percentuali aggiuntive e <b>senza nuovo addebito a ogni contratto locativo</b> nello stesso anno. "
        "Tutti gli importi + IVA 22%.",
        body,
    ))
    story.append(Spacer(1, 2 * mm))
    story.append(tbl_righetto_prezzi(
        ["Voce Righetto — costo annuo / immobile", "Imponibile", "Ivato (22%)"],
        [
            ["1 mensilità annua — gestione + Contratto", fmt_euro(c), fmt_euro(mens_ivata)],
            ["Registrazione (annua)", fmt_euro(REG), fmt_euro(reg_ivata)],
            ["Asseverazione annua (transitorio)", fmt_euro(ASS), fmt_euro(ass_ivata)],
            ["TOTALE annuo transitorio", fmt_euro(c + REG + ASS), fmt_euro(nostra_trans)],
            ["TOTALE annuo contratto locazione", fmt_euro(c + REG), fmt_euro(nostra_std)],
        ],
        [58 * mm, 58 * mm, 58 * mm],
    ))

    story.append(Spacer(1, 6 * mm))
    story.append(band("COSA CHIEDE IL MERCATO — stesso appartamento"))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "Zona Piazzola sul Brenta, Camposampiero, Padova. Verifica su fonti di settore (Instahome, Rentila, "
        "RealAdvisor): le agenzie applicano spesso <b>più voci sommate all'anno</b> — non solo la mensilità iniziale. "
        "Gli importi sotto sono <b>costi annui indicativi per immobile</b>.",
        body,
    ))
    story.append(Spacer(1, 2 * mm))
    story.append(tbl(
        ["Voce mercato — costo annuo", "Importo ivato (22%)", "Note"],
        [
            ["1 mensilità canone (all'anno)", fmt_euro(mercato_mens_ivata), "Spesso ad ogni nuovo contratto"],
            ["Oppure 15% canone annuo", fmt_euro(mercato_pct_15_ivata), "Alternativa frequente"],
            ["Pratiche registrazione (annue)", fmt_euro(mercato_reg_ivata), "€ 80–150 + IVA"],
            ["Asseverazione transitorio (annua)", f"{fmt_euro(ivato(180))} – {fmt_euro(ivato(250))}", "€ 180–250 + IVA"],
            ["Gestione annua 8% canone", fmt_euro(mercato_gest_8_ivata), "Aggiuntiva, ogni anno"],
            ["Gestione annua 12% canone", fmt_euro(mercato_gest_12_ivata), "Gestione strutturata"],
        ],
        [52 * mm, 44 * mm, 78 * mm],
        size=8.5,
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(tbl(
        ["Scenario mercato — costo annuo / immobile", "Totale ivato annuo"],
        [
            ["A — Solo Contratto transitorio (annuo)", fmt_euro(mercato_solo_stipula)],
            ["B — Contratto + gestione 8% annua", fmt_euro(mercato_completo_min)],
            ["C — Contratto + gestione 12% annua", fmt_euro(mercato_completo_max)],
            ["D — 15% canone annuo + oneri", fmt_euro(mercato_pct15_tot)],
        ],
        [90 * mm, 84 * mm],
    ))

    story.append(Spacer(1, 6 * mm))
    story.append(band("RIGHETTO VS MERCATO — risparmio evidenziato in rosso", colors.HexColor("#2C4A6E")))
    story.append(Spacer(1, 3 * mm))
    story.append(tbl_confronto_risparmio(
        [
            ["A — Solo Contratto (annuo)", fmt_euro(nostra_trans), fmt_euro(mercato_solo_stipula), fmt_euro(risparmio_vs_solo)],
            ["B — Contratto + gest. 8% (annuo)", fmt_euro(nostra_trans), fmt_euro(mercato_completo_min), fmt_euro(risparmio_vs_completo_min)],
            ["C — Contratto + gest. 12% (annuo)", fmt_euro(nostra_trans), fmt_euro(mercato_completo_max), fmt_euro(risparmio_vs_completo_max)],
            ["D — 15% annuo + oneri", fmt_euro(nostra_trans), fmt_euro(mercato_pct15_tot), fmt_euro(risparmio_vs_pct15)],
            ["15 immobili — compenso annuo (B)", fmt_euro(15 * nostra_trans), fmt_euro(15 * mercato_completo_min), fmt_euro(15 * risparmio_vs_completo_min)],
        ],
        [40 * mm, 42 * mm, 42 * mm, 50 * mm],
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "Colonna <b>Righetto</b>: importi annui in grassetto nero — <b>gestione completa già inclusa, una volta all'anno per immobile</b>. "
        "Colonna <b>Risparmio annuo</b> in rosso: quanto resta in tasca rispetto al mercato "
        "(che spesso addebita mensilità a ogni contratto e aggiunge 8–15% annui sul canone).",
        body,
    ))

    # ── PAG. 4: ESEMPIO PRATICO ──
    story.append(PageBreak())
    story.append(Paragraph("Esempio pratico — 1 appartamento € 800/mese (costi annui)", h2))

    story.append(Paragraph("<b>Contratto transitorio 12 mesi — anno di mandato</b>", ParagraphStyle("h3", parent=body, fontName="Helvetica-Bold", textColor=BLU)))
    story.append(tbl(
        ["Voce annua", "Importo"],
        [
            ["Canone incassato (12 mesi)", fmt_euro(c * 12)],
            ["Compenso Righetto annuo (gestione inclusa, ivato)", fmt_euro(nostra_trans)],
            ["Riparazioni", "A carico proprietario (avviso WhatsApp)"],
            ["Netto indicativo proprietario (annuo)", fmt_euro(c * 12 - nostra_trans)],
        ],
        [110 * mm, 64 * mm],
    ))

    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("<b>Portafoglio 15 immobili</b> — compenso annuo per unità in mandato", ParagraphStyle("h3c", parent=body, fontName="Helvetica-Bold", textColor=BLU)))
    th_p = ParagraphStyle("th2", fontName="Helvetica-Bold", fontSize=9.5, leading=11, textColor=colors.white)
    t_port = Table([
        [Paragraph(_esc("Voce annua"), th_p), Paragraph(_esc("Importo"), th_p)],
        [p_td("Canoni annui incassati (15 × € 800 × 12)"), p_td(fmt_euro(15 * c * 12))],
        [p_td("Compensi Righetto annui — gestione inclusa (15 immobili)"), p_td(fmt_euro(15 * nostra_trans), bold=True, color=NERO)],
        [p_td("Risparmio annuo vs mercato (scen. B)"), p_td(fmt_euro(15 * risparmio_vs_completo_min), bold=True, color=ROSSO)],
        [p_td("Referente unico + WhatsApp"), p_td("Incluso nel mandato annuale per immobile")],
    ], colWidths=[110 * mm, 64 * mm])
    t_port.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLU),
        ("BACKGROUND", (0, 1), (-1, -1), SFONDO),
        ("BACKGROUND", (0, 3), (-1, 3), RIGHE_RISPARMIO),
        ("BOX", (0, 0), (-1, -1), 1, BLU),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D4CEC4")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t_port)

    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph(
        "Tutti i compensi agenzia indicati sono <b>annui per immobile</b> e <b>+ IVA 22%</b> dove applicabile. "
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
