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
N_IMMOBILI = 15


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
NOTA_ANNO_GESTIONE = "Gestione: importo <b>annuo per immobile</b> (1 anno di mandato) — <b>non</b> si ripete a ogni contratto."
NOTA_PER_CONTRATTO = "Registrazione e asseverazione: <b>a ogni contratto</b> stilato — non costi annui fissi."


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
    header = ["Scenario annuo", "Righetto", "Mercato", "Risparmio"]
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


def nota_anno_gestione() -> Paragraph:
    ps = ParagraphStyle(
        "na", fontName="Helvetica-Oblique", fontSize=8, textColor=GRIGIO,
        alignment=TA_CENTER, spaceBefore=2, spaceAfter=4,
    )
    return Paragraph(NOTA_ANNO_GESTIONE, ps)


def nota_per_contratto() -> Paragraph:
    ps = ParagraphStyle(
        "npc", fontName="Helvetica-Oblique", fontSize=8, textColor=GRIGIO,
        alignment=TA_CENTER, spaceBefore=2, spaceAfter=4,
    )
    return Paragraph(NOTA_PER_CONTRATTO, ps)


def build_story(data_doc: date) -> list:
    c = CANONE
    n_imm = N_IMMOBILI

    mens_ivata = ivato(c)
    reg_ivata = ivato(REG)
    ass_ivata = ivato(ASS)
    canone_annuo = c * 12

    # ── Righetto: gestione annua fissa + oneri a contratto (esempio: 1 contratto transitorio) ──
    righetto_gestione_annua = mens_ivata
    righetto_reg_contratto = reg_ivata
    righetto_ass_contratto = ass_ivata
    righetto_tot_esempio = righetto_gestione_annua + righetto_reg_contratto + righetto_ass_contratto

    # ── Mercato (fonti: Instahome, Rentila, RealAdvisor) ──
    mercato_mens_ivata = ivato(c)           # spesso ad ogni nuovo contratto
    mercato_reg_ivata = ivato(100)          # € 80–150 + IVA a contratto
    mercato_ass_ivata = ivato(200)          # € 150–200 + IVA a contratto transitorio
    mercato_gest_8_ivata = ivato(canone_annuo * 0.08)
    mercato_gest_12_ivata = ivato(canone_annuo * 0.12)
    mercato_pct_15_ivata = ivato(canone_annuo * 0.15)

    # Costi a contratto — esempio 1 contratto transitorio
    mercato_per_contratto_trans = mercato_mens_ivata + mercato_reg_ivata + mercato_ass_ivata
    mercato_oneri_1_contratto = mercato_per_contratto_trans
    mercato_reg_ass_contratto = mercato_reg_ivata + mercato_ass_ivata

    # Scenario annuo mercato — stesso esempio (1 contratto transitorio)
    mercato_a = mercato_oneri_1_contratto  # solo oneri a contratto (stipula+reg+ass)
    mercato_b = mercato_gest_8_ivata + mercato_oneri_1_contratto
    mercato_c = mercato_gest_12_ivata + mercato_oneri_1_contratto
    mercato_d = mercato_pct_15_ivata + mercato_reg_ass_contratto  # 15% annuo + reg/ass a contratto

    risparmio_vs_a = mercato_a - righetto_tot_esempio
    risparmio_vs_b = mercato_b - righetto_tot_esempio
    risparmio_vs_c = mercato_c - righetto_tot_esempio
    risparmio_vs_d = mercato_d - righetto_tot_esempio

    # Portafoglio 15 immobili — esempio 1 contratto transitorio per immobile
    righetto_portfolio = n_imm * righetto_tot_esempio
    mercato_portfolio_b = n_imm * mercato_b
    risparmio_portfolio_b = mercato_portfolio_b - righetto_portfolio

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
    story.append(Paragraph("Piazzola sul Brenta · Camposampiero · Padova", ParagraphStyle("sub", fontSize=10, textColor=GRIGIO, alignment=TA_CENTER, spaceAfter=2)))
    story.append(Paragraph("Tariffe: <b>gestione annua</b> + <b>oneri a contratto</b> (registrazione / asseverazione)", ParagraphStyle("sub2", fontSize=9, textColor=BLU, alignment=TA_CENTER, spaceAfter=5)))
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
            ["Portafoglio", f"{n_imm} immobili — locazione"],
            ["Mandato", "Contratto annuale — rinnovo tacito — disdetta 30 gg"],
            ["Esempio tariffario", "1 immobile — 1 contratto transitorio (reg. + ass.)"],
            ["Gestione", "1 mensilità annua / immobile — oneri reg./ass. a contratto"],
        ],
        [48 * mm, 126 * mm],
    ))
    story.append(nota_anno_gestione())
    story.append(nota_per_contratto())

    # ── PAG. 2: COSA FACCIAMO + REGOLE ──
    story.append(PageBreak())
    story.append(band("LA NOSTRA GESTIONE — gestione annua + oneri a contratto"))
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
        "Il compenso di <b>gestione è annuo per immobile</b> (1 mensilità all'anno): referente unico, rapporto con l'inquilino, "
        "scadenze, piccole urgenze, coordinamento tecnici — <b>senza percentuali aggiuntive</b> sul canone.",
        "<b>Registrazione</b> (€ 50 + IVA) e <b>asseverazione</b> transitorio (€ 50 + IVA) si pagano "
        "<b>a ogni contratto stilato</b>, non come voce annua fissa. "
        "Nell'esempio tariffario sotto: <b>1 contratto transitorio</b> con registrazione e asseverazione.",
        "Riparazioni e pulizie restano a carico del proprietario — con avviso WhatsApp prima di ogni intervento.",
    ]))
    story.append(Spacer(1, 3 * mm))
    story.append(tbl(
        ["Voce", "Come si applica", "Importo"],
        [
            ["Gestione immobile", "Annuo — 1 anno / immobile", "1 mensilità + IVA"],
            ["Registrazione contratto", "A ogni contratto stilato", f"€ {REG} + IVA / contratto"],
            ["Asseverazione transitorio", "A ogni contratto transitorio", f"€ {ASS} + IVA / contratto"],
            ["Pulizie fine locazione", "Quando serve", "A carico proprietario"],
            ["Riparazioni / manutenzioni", "Quando serve", "A carico proprietario — avviso WhatsApp"],
        ],
        [48 * mm, 52 * mm, 74 * mm],
        size=8.5,
    ))
    story.append(nota_anno_gestione())
    story.append(nota_per_contratto())
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph(
        "<b>Come leggere gli importi:</b> la <b>gestione</b> è un costo <b>annuo fisso</b> (1 mensilità) — "
        "non aumenta se si stipulano più contratti nello stesso anno. "
        "<b>Registrazione e asseverazione</b> sono <b>a contratto</b>: nell'esempio sotto, 1 contratto transitorio. "
        "Stessa logica per il confronto mercato.",
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
    story.append(band("LA NOSTRA OFFERTA RIGHETTO — gestione annua + oneri a contratto", colors.HexColor("#1B6B4A")))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        f"<b>Esempio — 1 immobile, canone € {c}/mese, 1 solo contratto transitorio.</b> "
        "Nessuna moltiplicazione per 6 contratti: gestione = 1 mensilità annua; reg. e ass. = una tantum a contratto. "
        "Tutti gli importi + IVA 22%.",
        body,
    ))
    story.append(Spacer(1, 2 * mm))
    story.append(tbl_righetto_prezzi(
        ["Voce Righetto — 1 immobile, 1 contratto", "Base", "Ivato (22%)"],
        [
            ["Gestione (1 mensilità canone / anno)", fmt_euro(c), fmt_euro(righetto_gestione_annua)],
            ["Registrazione — 1 contratto", fmt_euro(REG), fmt_euro(righetto_reg_contratto)],
            ["Asseverazione transitorio — 1 contratto", fmt_euro(ASS), fmt_euro(righetto_ass_contratto)],
            ["TOTALE esempio (1 contratto, non ×6)", fmt_euro(c + REG + ASS), fmt_euro(righetto_tot_esempio)],
        ],
        [68 * mm, 53 * mm, 53 * mm],
    ))
    story.append(nota_anno_gestione())
    story.append(nota_per_contratto())

    story.append(Spacer(1, 6 * mm))
    story.append(band("COSA CHIEDE IL MERCATO — stesso esempio (1 contratto)"))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "Zona Piazzola sul Brenta, Camposampiero, Padova. Fonti: Instahome, Rentila, RealAdvisor. "
        "Anche altre agenzie distinguono <b>gestione annua</b> (o % sul canone) da "
        "<b>registrazione e asseverazione a ogni contratto</b>. Spesso addebitano "
        "<b>1 mensilità a ogni nuovo contratto</b> — Righetto no: la mensilità è solo gestione annua.",
        body,
    ))
    story.append(Spacer(1, 2 * mm))
    story.append(tbl(
        ["Voce mercato", "Unità", "Ivato (22%)"],
        [
            ["1 mensilità canone (stipula)", "A ogni contratto", fmt_euro(mercato_mens_ivata)],
            ["Registrazione pratica", "A ogni contratto", fmt_euro(mercato_reg_ivata)],
            ["Asseverazione transitorio", "A ogni contratto transitorio", fmt_euro(mercato_ass_ivata)],
            ["Subtotale oneri — 1 contratto", "A contratto", fmt_euro(mercato_oneri_1_contratto)],
            ["Gestione annua 8% canone", "Annuo / immobile", fmt_euro(mercato_gest_8_ivata)],
            ["Gestione annua 12% canone", "Annuo / immobile", fmt_euro(mercato_gest_12_ivata)],
            ["Oppure 15% canone annuo", "Annuo / immobile", fmt_euro(mercato_pct_15_ivata)],
        ],
        [52 * mm, 44 * mm, 78 * mm],
        size=8.5,
    ))
    story.append(nota_per_contratto())
    story.append(Spacer(1, 2 * mm))
    story.append(tbl(
        ["Scenario mercato — 1 contratto / immobile", "Totale ivato annuo"],
        [
            ["A — Oneri a contratto (1 contr., no gest. %)", fmt_euro(mercato_a)],
            ["B — Oneri a contratto + gestione 8% annua", fmt_euro(mercato_b)],
            ["C — Oneri a contratto + gestione 12% annua", fmt_euro(mercato_c)],
            ["D — 15% annuo + reg./ass. a contratto", fmt_euro(mercato_d)],
        ],
        [90 * mm, 84 * mm],
    ))
    story.append(nota_per_contratto())

    story.append(Spacer(1, 6 * mm))
    story.append(band("RIGHETTO VS MERCATO — 1 contratto · risparmio in rosso", colors.HexColor("#2C4A6E")))
    story.append(Spacer(1, 3 * mm))
    story.append(tbl_confronto_risparmio(
        [
            ["A — Solo oneri (1 contr.)", fmt_euro(righetto_tot_esempio), fmt_euro(mercato_a), fmt_euro(risparmio_vs_a)],
            ["B — Oneri + gest. 8%", fmt_euro(righetto_tot_esempio), fmt_euro(mercato_b), fmt_euro(risparmio_vs_b)],
            ["C — Oneri + gest. 12%", fmt_euro(righetto_tot_esempio), fmt_euro(mercato_c), fmt_euro(risparmio_vs_c)],
            ["D — 15% + reg./ass.", fmt_euro(righetto_tot_esempio), fmt_euro(mercato_d), fmt_euro(risparmio_vs_d)],
            [f"{n_imm} immobili × scen. B", fmt_euro(righetto_portfolio), fmt_euro(mercato_portfolio_b), fmt_euro(risparmio_portfolio_b)],
        ],
        [40 * mm, 42 * mm, 42 * mm, 50 * mm],
    ))
    story.append(nota_anno_gestione())
    story.append(nota_per_contratto())
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "Colonna <b>Righetto</b>: gestione annua (1 mensilità) + reg. e ass. per "
        "<b>1 contratto transitorio</b>. Il mercato spesso addebita la mensilità "
        "<b>a ogni contratto</b> oltre alla gestione % — da qui il risparmio in rosso.",
        body,
    ))

    # ── PAG. 4: ESEMPIO PRATICO ──
    story.append(PageBreak())
    story.append(Paragraph(f"Esempio pratico — 1 appartamento € {c}/mese · 1 contratto transitorio", h2))

    story.append(Paragraph("<b>Costi annui — esempio 1 contratto (registrazione + asseverazione)</b>", ParagraphStyle("h3", parent=body, fontName="Helvetica-Bold", textColor=BLU)))
    story.append(tbl(
        ["Voce", "Calcolo", "Importo ivato"],
        [
            ["Canone incassato (12 mesi)", "€ 800 × 12", fmt_euro(c * 12)],
            ["Gestione Righetto (annua)", "1 mensilità / anno", fmt_euro(righetto_gestione_annua)],
            ["Registrazione (1 contratto)", f"€ {REG} + IVA", fmt_euro(righetto_reg_contratto)],
            ["Asseverazione (1 contratto)", f"€ {ASS} + IVA", fmt_euro(righetto_ass_contratto)],
            ["TOTALE compenso Righetto", "Gestione + reg. + ass.", fmt_euro(righetto_tot_esempio)],
            ["Riparazioni", "—", "A carico proprietario"],
            ["Netto indicativo proprietario", "Canoni − compenso Righetto", fmt_euro(c * 12 - righetto_tot_esempio)],
        ],
        [52 * mm, 58 * mm, 64 * mm],
        size=8.5,
    ))
    story.append(nota_anno_gestione())
    story.append(nota_per_contratto())

    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph(f"<b>Portafoglio {n_imm} immobili</b> — esempio 1 contratto/immobile (transitorio)", ParagraphStyle("h3c", parent=body, fontName="Helvetica-Bold", textColor=BLU)))
    th_p = ParagraphStyle("th2", fontName="Helvetica-Bold", fontSize=9.5, leading=11, textColor=colors.white)
    t_port = Table([
        [Paragraph(_esc("Voce annua"), th_p), Paragraph(_esc("Importo"), th_p)],
        [p_td(f"Canoni incassati ({n_imm} × € {c} × 12)"), p_td(fmt_euro(n_imm * c * 12))],
        [p_td(f"Gestione annua × {n_imm} immobili"), p_td(fmt_euro(n_imm * righetto_gestione_annua))],
        [p_td(f"Registrazione × {n_imm} immobili (1 contratto ciascuno)"), p_td(fmt_euro(n_imm * righetto_reg_contratto))],
        [p_td(f"Asseverazione × {n_imm} immobili (1 contratto ciascuno)"), p_td(fmt_euro(n_imm * righetto_ass_contratto))],
        [p_td(f"TOTALE compensi Righetto ({n_imm} immobili)"), p_td(fmt_euro(righetto_portfolio), bold=True, color=NERO)],
        [p_td("Risparmio vs mercato (scen. B)"), p_td(fmt_euro(risparmio_portfolio_b), bold=True, color=ROSSO)],
        [p_td("Referente unico + WhatsApp"), p_td("Incluso nella gestione annua")],
    ], colWidths=[110 * mm, 64 * mm])
    t_port.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLU),
        ("BACKGROUND", (0, 1), (-1, -1), SFONDO),
        ("BACKGROUND", (0, 6), (-1, 6), RIGHE_RISPARMIO),
        ("BOX", (0, 0), (-1, -1), 1, BLU),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D4CEC4")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t_port)
    story.append(nota_anno_gestione())
    story.append(nota_per_contratto())

    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph(
        "Gestione Righetto: <b>annua per immobile</b>. Registrazione e asseverazione: <b>a contratto</b>. "
        "Nell'esempio: <b>1 contratto transitorio</b> per immobile. "
        "Canone € 800/mese indicativo Piazzola–Camposampiero–Padova. Fonti: Instahome, Rentila, RealAdvisor. "
        "Tutti gli importi + IVA 22% dove applicabile.",
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
