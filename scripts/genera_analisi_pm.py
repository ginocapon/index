#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Report semplice Property Management — Piazzola sul Brenta / Camposampiero (PD).

Uso:
  python scripts/genera_analisi_pm.py

Output: data/perizie/ + documenti/perizie/
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
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

NERO = colors.HexColor("#152435")
BLU = colors.HexColor("#2C4A6E")
ORO = colors.HexColor("#FF6B35")
SFONDO = colors.HexColor("#ECE7DF")
GRIGIO = colors.HexColor("#6B7A8D")
VERDE = colors.HexColor("#1B6B4A")

# Ipotesi concrete zona Piazzola / Camposampiero (canone mensile tipo)
CANONE_TIPO = 800


def _esc(text: str) -> str:
    return str(text or "—").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def fmt_euro(n: float | int) -> str:
    return f"€ {int(round(n)):,}".replace(",", ".")


class AnalisiCanvas(canvas.Canvas):
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
        self.drawString(14 * mm, 15.5 * mm, "Bertinato Gino — Righetto Immobiliare — Limena (PD) — 049.8843484")
        self.drawRightString(w - 14 * mm, 15.5 * mm, f"Report PM — Pag. {n}/{total}")


def make_kv(pairs: list[tuple[str, str]]) -> Table:
    lbl = ParagraphStyle("kl", fontName="Helvetica-Bold", fontSize=9, leading=11, textColor=colors.white)
    val = ParagraphStyle("kv", fontName="Helvetica", fontSize=9.5, leading=12, textColor=NERO)
    rows = [[Paragraph(_esc(k), lbl), Paragraph(_esc(v), val)] for k, v in pairs]
    t = Table(rows, colWidths=[55 * mm, 119 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), BLU),
        ("BACKGROUND", (1, 0), (1, -1), SFONDO),
        ("BOX", (0, 0), (-1, -1), 0.5, BLU),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#E1DBD1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def make_table(header: list[str], body: list[list[str]], widths: list[float], size: float = 9) -> Table:
    th = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=size, leading=11, textColor=colors.white)
    td = ParagraphStyle("td", fontName="Helvetica", fontSize=size, leading=12, textColor=NERO)
    rows: list[list] = [[Paragraph(_esc(c), th) for c in header]]
    for row in body:
        rows.append([Paragraph(_esc(c), td) for c in row])
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLU),
        ("BOX", (0, 0), (-1, -1), 0.5, BLU),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#E1DBD1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def green_box(title: str, lines: list[str]) -> Table:
    ps_t = ParagraphStyle("gt", fontName="Helvetica-Bold", fontSize=10, textColor=colors.white, leading=12)
    ps_b = ParagraphStyle("gb", fontName="Helvetica", fontSize=9.5, textColor=colors.white, leading=13)
    data: list[list] = [[Paragraph(title, ps_t)]]
    for line in lines:
        data.append([Paragraph(line, ps_b)])
    box = Table(data, colWidths=[174 * mm])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), VERDE),
        ("BOX", (0, 0), (-1, -1), 1.5, ORO),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return box


def flow_step(num: str, text: str, note: str = "") -> Table:
    ps_n = ParagraphStyle("sn", fontName="Helvetica-Bold", fontSize=11, textColor=ORO, alignment=TA_CENTER)
    ps_t = ParagraphStyle("st", fontName="Helvetica-Bold", fontSize=9, textColor=colors.white, leading=11)
    ps_n2 = ParagraphStyle("sn2", fontName="Helvetica", fontSize=8, textColor=SFONDO, leading=10)
    left = Paragraph(num, ps_n)
    right_rows = [[Paragraph(text, ps_t)]]
    if note:
        right_rows.append([Paragraph(note, ps_n2)])
    right = Table(right_rows, colWidths=[148 * mm])
    right.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BLU),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    t = Table([[left, right]], colWidths=[18 * mm, 156 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0.5, ORO),
    ]))
    return t


def flow_down() -> Paragraph:
    return Paragraph(
        "▼",
        ParagraphStyle("fd", fontName="Helvetica-Bold", fontSize=12, textColor=ORO, alignment=TA_CENTER, spaceBefore=1, spaceAfter=1),
    )


def build_story(data_doc: date) -> list:
    c = CANONE_TIPO
    avvio = round(c * 0.85)       # Portfolio 15
    gestione = round(c * 0.45)    # annua
    gestione_breve = round(c * 0.45 * 1.35)

    h1 = ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=16, textColor=BLU, alignment=TA_CENTER, spaceAfter=4)
    h2 = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=12, textColor=BLU, spaceBefore=10, spaceAfter=5)
    body = ParagraphStyle("B", fontName="Helvetica", fontSize=10, leading=14, textColor=NERO, alignment=TA_JUSTIFY, spaceAfter=5)
    small = ParagraphStyle("Sm", fontName="Helvetica", fontSize=8, textColor=GRIGIO, spaceAfter=3)

    story: list = []

    # ── PAG. 1 — COPERTINA + IN SINTESI ──
    if LOGO_PATH.is_file():
        story.append(RLImage(str(LOGO_PATH), width=32 * mm, height=32 * mm))
        story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("GESTIONE LOCAZIONI — PROPOSTA SEMPLICE", h1))
    story.append(Paragraph("Piazzola sul Brenta · Camposampiero · hinterland Padova", ParagraphStyle(
        "sub", fontName="Helvetica", fontSize=10, textColor=GRIGIO, alignment=TA_CENTER, spaceAfter=8,
    )))
    story.append(make_kv([
        ("Destinatario", "Sig. Canton Romeo"),
        ("Agenzia", "Gruppo Immobiliare Bertinato Gino / Righetto Immobiliare"),
        ("Data", data_doc.strftime("%d/%m/%Y")),
        ("Portafoglio", "Circa 15 immobili in locazione"),
        ("Zona", "Piazzola sul Brenta, Camposampiero e comuni limitrofi"),
        ("Obiettivo cliente", "Zero gestione diretta — un solo referente per tutto"),
    ]))
    story.append(Spacer(1, 6 * mm))
    story.append(green_box("In 30 secondi — cosa proponiamo", [
        "1. <b>Avvio</b> (una volta per immobile): <b>0,85 mensilità</b> del canone",
        "2. <b>Gestione annua</b>: <b>0,45 mensilità/anno</b> — ci occupiamo noi di tutto il resto",
        "3. <b>Nuovo inquilino</b>: la proprietaria <b>non paga</b> — paga il conduttore (1 mensilità)",
        "4. Contratti <b>brevi</b> (sotto 3 mesi): gestione <b>+35%</b> perché si ripete più spesso",
    ]))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(
        f"Ipotesi di lavoro: canone mensile tipo <b>{fmt_euro(c)}</b> per un bilocale/ trilocale "
        "in zona Piazzola–Camposampiero (valutazione puntuale immobile per immobile).",
        body,
    ))

    # ── PAG. 2 — TARIFFA + CHI PAGA COSA ──
    story.append(PageBreak())
    story.append(Paragraph("1. Listino Portfolio 15 immobili", h2))
    story.append(make_table(
        ["Cosa", "Quanto", "Chi paga"],
        [
            ["Avvio gestione (una tantum)", "0,85 mensilità", "Proprietaria"],
            ["Gestione ordinaria (ogni anno)", "0,45 mensilità", "Proprietaria"],
            ["Trova nuovo inquilino", "1 mensilità", "Conduttore — non la proprietaria"],
            ["Proroga stesso inquilino", "0,25 mensilità", "Proprietaria"],
            ["Contratto sotto 3 mesi", "+35% sulla gestione", "Proprietaria"],
        ],
        [58 * mm, 48 * mm, 68 * mm],
    ))
    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph("2. Cosa facciamo noi (incluso nel prezzo)", h2))
    story.append(make_table(
        ["Servizio", "Dettaglio"],
        [
            ["Annuncio e visite", "Foto, portali, selezione inquilini"],
            ["Contratto", "Predisposizione, registrazione, scadenze"],
            ["Referente unico", "Nessun contatto diretto proprietario–inquilino"],
            ["Manutenzioni piccole", "Coordinamento fino a € 200"],
            ["Cambio inquilino", "Verifica immobile, consegna chiavi, nuovo annuncio"],
            ["Report", "Aggiornamento trimestrale alla proprietaria"],
        ],
        [52 * mm, 122 * mm],
    ))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("3. Cosa resta a carico della proprietaria (extra)", h2))
    for item in [
        "Lavori importanti (idraulico, elettrico, ristrutturazione)",
        "Pulizie fine locazione (le coordiniamo noi, le paga lei)",
        "IMU, bollo, registro, spese condominiali",
        "Contenzioso o sfratto",
    ]:
        story.append(Paragraph(f"• {item}", ParagraphStyle("bu", parent=body, leftIndent=8, spaceAfter=2)))

    # ── PAG. 3 — DUE ESEMPI CONCRETI ──
    story.append(PageBreak())
    story.append(Paragraph(f"4. Due esempi concreti — canone {fmt_euro(c)}/mese", h2))

    story.append(Paragraph("<b>Esempio A — Contratto 12 mesi</b> (1 inquilino all'anno)", ParagraphStyle(
        "h3", parent=body, fontName="Helvetica-Bold", textColor=BLU, spaceBefore=4,
    )))
    story.append(make_table(
        ["Voce", "Importo", "Note"],
        [
            ["Avvio (anno 1)", fmt_euro(avvio), "Una volta sola"],
            ["Gestione annua", fmt_euro(gestione), "Ogni anno"],
            ["Nuovo inquilino", "€ 0 proprietaria", f"Conduttore paga {fmt_euro(c)}"],
            ["Totale proprietaria anno 1", fmt_euro(avvio + gestione), "Poi solo gestione"],
            ["Totale proprietaria anni dopo", fmt_euro(gestione), "Circa € 38/mese"],
        ],
        [52 * mm, 40 * mm, 82 * mm],
    ))
    story.append(Spacer(1, 5 * mm))

    story.append(Paragraph("<b>Esempio B — Contratto 2 mesi</b> (più cambi inquilino)", ParagraphStyle(
        "h3", parent=body, fontName="Helvetica-Bold", textColor=BLU, spaceBefore=4,
    )))
    story.append(make_table(
        ["Voce", "Importo", "Note"],
        [
            ["Avvio (anno 1)", fmt_euro(avvio), "Una volta sola"],
            ["Gestione annua (+35%)", fmt_euro(gestione_breve), "Più lavoro per noi"],
            ["Nuovi inquilini (×5/anno)", "€ 0 proprietaria", f"5 × {fmt_euro(c)} dai conduttori"],
            ["Pulizie extra stimate", "€ 400–600/anno", "A carico proprietaria"],
            ["Totale proprietaria/anno", fmt_euro(avvio + gestione_breve), "Anno 1; poi ~" + fmt_euro(gestione_breve)],
        ],
        [52 * mm, 40 * mm, 82 * mm],
    ))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(
        "<b>Differenza chiave:</b> nei contratti brevi la proprietaria paga un po' di più in gestione (+35%) "
        "e qualche pulizia in più, ma <b>non paga mai</b> la commissione per trovare l'inquilino.",
        body,
    ))

    # ── PAG. 4 — ORGANIGRAMMA SEMPLICE ──
    story.append(PageBreak())
    story.append(Paragraph("5. Come funziona — passo per passo", h2))

    story.append(Paragraph("<b>Caso standard (contratto 6–18 mesi)</b>", ParagraphStyle(
        "h3b", parent=body, fontName="Helvetica-Bold", textColor=BLU,
    )))
    for num, text, note in [
        ("1", "Presa in carico immobile", f"Proprietaria: {fmt_euro(avvio)}"),
        ("2", "Annuncio + visite + scelta inquilino", f"Conduttore: {fmt_euro(c)}"),
        ("3", "Contratto e registrazione", "Incluso"),
        ("4", "Gestione per tutta la durata", f"{fmt_euro(gestione)}/anno — noi referenti"),
        ("5", "Fine contratto: verifica + consegna", "Incluso"),
        ("6", "Nuovo inquilino se serve", f"Di nuovo conduttore: {fmt_euro(c)}"),
    ]:
        story.append(flow_step(num, text, note))
        if num != "6":
            story.append(flow_down())

    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("<b>Caso breve (contratto sotto 3 mesi)</b>", ParagraphStyle(
        "h3c", parent=body, fontName="Helvetica-Bold", textColor=BLU,
    )))
    story.append(Paragraph(
        "Stessi passi, ma <b>più veloce</b> e si ripete 4–5 volte l'anno. "
        f"Gestione maggiorata: {fmt_euro(gestione_breve)}/anno invece di {fmt_euro(gestione)}.",
        body,
    ))
    for num, text, note in [
        ("1", "Inquilino entra (contratto 1–3 mesi)", "Veloce"),
        ("2", "Gestione + scadenza", f"+35% gestione"),
        ("3", "Check-out + verifica immobile", "Incluso"),
        ("4", "Pulizie + nuovo annuncio", "Extra proprietaria ~€ 100"),
        ("5", "Nuovo inquilino", f"Conduttore: {fmt_euro(c)} — loop"),
    ]:
        story.append(flow_step(num, text, note))
        if num != "5":
            story.append(flow_down())

    # ── PAG. 5 — PORTAFOGLIO 15 + CHIUSURA ──
    story.append(PageBreak())
    story.append(Paragraph("6. Portafoglio 15 immobili — numeri totali", h2))
    story.append(make_table(
        ["Scenario", "Canone medio", "Ricavo agenzia/anno", "Note"],
        [
            ["Tranquillo (poche rotazioni)", fmt_euro(c), fmt_euro(15 * gestione + 4 * c), "~4 nuovi inquilini"],
            ["Medio (mix contratti)", fmt_euro(c), fmt_euro(15 * gestione + 8 * c), "~8 nuovi inquilini"],
            ["Attivo (molti brevi)", fmt_euro(c), fmt_euro(15 * gestione_breve + 12 * c), "Contratti corti"],
        ],
        [42 * mm, 32 * mm, 42 * mm, 58 * mm],
        size=8.5,
    ))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(
        f"<b>Primo anno (avvio 15 immobili):</b> 15 × {fmt_euro(avvio)} = <b>{fmt_euro(15 * avvio)}</b> una tantum, "
        "poi solo gestione annua.",
        body,
    ))
    story.append(Spacer(1, 6 * mm))
    story.append(green_box("Proposta da presentare alla cliente", [
        "<b>Pacchetto «Zero pensieri» — 15 immobili Piazzola / Camposampiero</b>",
        f"Canone tipo zona: {fmt_euro(c)}/mese · Avvio {fmt_euro(avvio)} · Gestione {fmt_euro(gestione)}/anno",
        "Nuovo inquilino: € 0 per lei — referente unico Bertinato Gino",
        "Contratti brevi: +35% gestione · Tutto il resto lo facciamo noi",
    ]))
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph(
        "Documento interno — Gruppo Immobiliare Bertinato Gino · Righetto Immobiliare · "
        f"{data_doc.strftime('%d/%m/%Y')}",
        ParagraphStyle("foot", alignment=TA_CENTER, fontSize=8, textColor=GRIGIO),
    ))
    story.append(Paragraph(
        "Canoni indicativi per Piazzola sul Brenta e Camposampiero — da confermare immobile per immobile.",
        small,
    ))

    return story


def build_pdf(out_path: Path, data_doc: date) -> Path:
    doc = SimpleDocTemplate(
        str(out_path), pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=18 * mm, bottomMargin=22 * mm,
    )
    doc.build(build_story(data_doc), canvasmaker=AnalisiCanvas)
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
    print(f"Archivio admin: {archive}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
