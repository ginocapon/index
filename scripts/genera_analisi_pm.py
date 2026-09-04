#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera PDF analisi commerciale Property Management — Righetto / Bertinato Gino.

Uso:
  python scripts/genera_analisi_pm.py

Output: data/perizie/ + documenti/perizie/
"""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
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


def _esc(text: str) -> str:
    return (
        str(text or "—")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def fmt_euro(n: float | int) -> str:
    return f"€ {int(round(n)):,}".replace(",", ".")


class AnalisiCanvas(canvas.Canvas):
    def __init__(self, *args, doc_title: str = "Analisi commerciale riservata", **kwargs):
        super().__init__(*args, **kwargs)
        self._saved: list[dict] = []
        self._doc_title = doc_title

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
        self.drawString(
            14 * mm, 15.5 * mm,
            "Gruppo Immobiliare Bertinato Gino — Righetto Immobiliare — Via Roma 96, Limena (PD) — 049.8843484",
        )
        self.drawRightString(w - 14 * mm, 15.5 * mm, f"{self._doc_title} — Pag. {n}/{total}")


def make_kv(pairs: list[tuple[str, str]]) -> Table:
    lbl = ParagraphStyle("kl", fontName="Helvetica-Bold", fontSize=8, leading=10.5, textColor=colors.white)
    val = ParagraphStyle("kv", fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=NERO)
    rows = [[Paragraph(_esc(k), lbl), Paragraph(_esc(v), val)] for k, v in pairs]
    t = Table(rows, colWidths=[52 * mm, 122 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), BLU),
        ("BACKGROUND", (1, 0), (1, -1), SFONDO),
        ("BOX", (0, 0), (-1, -1), 0.5, BLU),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#E1DBD1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def make_table(header: list[str], body: list[list[str]], widths: list[float], body_size: float = 7.5) -> Table:
    th = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=body_size, leading=9.5, textColor=colors.white)
    td = ParagraphStyle("td", fontName="Helvetica", fontSize=body_size, leading=10, textColor=NERO)
    rows: list[list] = [[Paragraph(_esc(c), th) for c in header]]
    for row in body:
        rows.append([Paragraph(_esc(c), td) for c in row])
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLU),
        ("BOX", (0, 0), (-1, -1), 0.5, BLU),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#E1DBD1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def highlight_box(title: str, lines: list[str], styles: dict) -> Table:
    ps_t = ParagraphStyle("hb_t", fontName="Helvetica-Bold", fontSize=9, textColor=colors.white, leading=11)
    ps_b = ParagraphStyle("hb_b", fontName="Helvetica", fontSize=8.5, textColor=colors.white, leading=11.5)
    data: list[list] = [[Paragraph(title, ps_t)]]
    for line in lines:
        data.append([Paragraph(line, ps_b)])
    box = Table(data, colWidths=[174 * mm])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), VERDE),
        ("BOX", (0, 0), (-1, -1), 1, ORO),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return box


def build_story(data_perizia: date) -> list:
    styles = getSampleStyleSheet()
    title = ParagraphStyle("T", fontName="Helvetica-Bold", fontSize=17, textColor=BLU, alignment=TA_CENTER, spaceAfter=4)
    subtitle = ParagraphStyle("S", fontName="Helvetica", fontSize=9, textColor=GRIGIO, alignment=TA_CENTER, spaceAfter=6)
    h2 = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=11, textColor=BLU, spaceBefore=8, spaceAfter=4)
    h3 = ParagraphStyle("H3", fontName="Helvetica-Bold", fontSize=9.5, textColor=BLU, spaceBefore=5, spaceAfter=3)
    body = ParagraphStyle("B", fontName="Helvetica", fontSize=9, leading=13, textColor=NERO, alignment=TA_JUSTIFY, spaceAfter=4)
    bullet = ParagraphStyle("Bu", parent=body, leftIndent=10, spaceAfter=2)
    small = ParagraphStyle("Sm", parent=body, fontSize=7.5, textColor=GRIGIO, spaceAfter=2)
    st: dict = {"title": title, "h2": h2, "body": body}

    story: list = []

    # ── COPERTINA ──
    if LOGO_PATH.is_file():
        story.append(RLImage(str(LOGO_PATH), width=36 * mm, height=36 * mm))
        story.append(Spacer(1, 6 * mm))
    story.append(Paragraph("ANALISI DI MERCATO E DEFINIZIONE OFFERTA", title))
    story.append(Paragraph("Property Management — Portafoglio ~15 immobili in locazione", subtitle))
    story.append(Spacer(1, 4 * mm))
    story.append(make_kv([
        ("Destinatario", "Sig. Canton Romeo"),
        ("Committente interno", "Gruppo Immobiliare Bertinato Gino"),
        ("Redatto da", "Righetto Immobiliare — Ufficio consulenza"),
        ("Data documento", data_perizia.strftime("%d/%m/%Y")),
        ("Oggetto", "Definizione offerta commerciale Full Property Management"),
        ("Contesto", "Portafoglio ~15 unità — locazioni transitorie / brevi"),
        ("Classificazione", "Documento riservato — uso interno e commerciale"),
    ]))
    story.append(Spacer(1, 6 * mm))
    story.append(highlight_box("Executive Summary", [
        "<b>Verdetto:</b> la formula 1 mensilità (avvio) + ½ mensilità/anno (gestione) è <b>competitiva e consigliabile</b>, "
        "a condizione che la provvigione di intermediazione (≈1 mensilità dal nuovo conduttore) resti separata e non si "
        "addebiti doppio alla proprietaria per ogni turnover.",
        "<b>Modello consigliato:</b> compenso gestione proprietaria + maggiorazioni per alto turnover + listino Portfolio 15 unità.",
        "<b>Ricavo annuo stimato</b> (15 immobili, canone medio €900, turnover medio): <b>€ 19.000 – € 22.000</b> "
        "(gestione + intermediazione).",
    ], st))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(
        "<i>Fonti di mercato: Rentila, CSI Immobili, MN Agenzia, Worthington, Instahome, Invim/Gabetti, FreedHome, "
        "Rentger/Idealista — tariffe dove non pubblicate indicate come «su preventivo».</i>",
        small,
    ))
    story.append(PageBreak())

    # ── 1. CONTESTO ──
    story.append(Paragraph("1. Contesto e obiettivo", h2))
    story.append(Paragraph(
        "Gruppo Immobiliare Bertinato Gino valuta un'offerta di <b>gestione completa</b> per una proprietaria "
        "con circa <b>15 immobili</b> da mettere in locazione, prevalentemente con contratti <b>transitori</b> "
        "(1–18 mesi). La cliente richiede delega totale: niente rapporti con inquilini, niente burocrazia, "
        "referente unico operativo.",
        body,
    ))
    story.append(Paragraph(
        "<b>Elemento distintivo del modello Bertinato:</b> alla nuova locazione l'agenzia percepisce mediamente "
        "<b>1 mensilità di provvigione dal nuovo conduttore</b>. Il compenso chiesto alla proprietaria deve "
        "remunerare solo il <b>property management</b>, non duplicare la mediazione.",
        body,
    ))

    # ── 2. MERCATO ──
    story.append(Paragraph("2. Mercato italiano — sintesi", h2))
    story.append(Paragraph(
        "In Italia non esiste una tariffa legale obbligatoria (art. 1755 c.c.). Il mercato distingue "
        "<b>mandato d'affitto</b> (solo collocamento) da <b>mandato di gestione</b> (amministrazione continuativa).",
        body,
    ))
    story.append(make_table(
        ["Voce", "Prassi di mercato", "Fonte"],
        [
            ["Solo ricerca inquilino", "1 mensilità + IVA oppure 10–15% canone annuo", "Rentila, CSI, MN"],
            ["Gestione ordinaria annua", "~7–8% canone annuo", "Rentila"],
            ["Gestione full service", "4–10% annuo (per servizi inclusi)", "Worthington, Instahome"],
            ["Affitti brevi turistici", "15–30% ricavi (non comparabile)", "Propert.it, Hostmate"],
        ],
        [42 * mm, 88 * mm, 44 * mm],
        body_size=7.2,
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "<b>Nota:</b> Gabetti/Invim, Gruppocasa, Recasa non pubblicano listini online — condizioni su preventivo.",
        small,
    ))

    # ── 3. BENCHMARK ──
    story.append(Paragraph("3. Benchmark operatori", h2))
    story.append(make_table(
        ["Operatore", "Servizio", "Tariffa", "Note"],
        [
            ["Rentila (guida)", "Affitto + gestione", "1 mens. / 7–8% annuo", "Separazione netta"],
            ["CSI Immobili", "Mediazione locazione", "10–15% annuo o 1–2 mens.", "Transitorio incluso"],
            ["MN Agenzia", "Mediazione", "~15% annuo + IVA", "Blog agenzia"],
            ["Worthington", "Mediazione + PM", "10–15% / 4–8% gestione", "Zona Milano"],
            ["Instahome", "Pacchetti PM", "4–10% annuo", "Più servizi = % più alta"],
            ["Invim/Gabetti", "Gestione lungo", "Quota annuale (N/D)", "No provvigione dichiarata"],
            ["FreedHome", "PropTech", "Gratis al locatore*", "*Inquilino paga copertura"],
        ],
        [32 * mm, 38 * mm, 42 * mm, 62 * mm],
        body_size=6.8,
    ))

    story.append(PageBreak())

    # ── 4. DUE FLUSSI DI RICAVO ──
    story.append(Paragraph("4. Ricavo A (proprietaria) vs Ricavo B (conduttore)", h2))
    story.append(Paragraph(
        "<b>Risposta netta:</b> con 1 mensilità dal nuovo conduttore, <b>NON è necessario</b> addebitare "
        "alla proprietaria un'ulteriore mensilità per ogni nuova locazione. La provvigione del conduttore "
        "remunera marketing, visite, screening, contratto e registrazione.",
        body,
    ))
    story.append(make_table(
        ["Attività", "Remunerata da", "Motivo"],
        [
            ["Nuova locazione / turnover", "Conduttore (~1 mens.)", "Standard mercato mediazione"],
            ["Avvio gestione immobile", "Proprietaria (1 mens. anno 1)", "Setup, documenti, strategia"],
            ["Gestione ordinaria annua", "Proprietaria (½ mens./anno)", "Rapporto inquilino, scadenze, report"],
            ["Proroga transitorio", "Proprietaria (0,2–0,3 mens.)", "Lavoro ridotto vs nuova locazione"],
            ["Straordinari / sfratto", "Proprietaria (extra)", "Non inclusi nel canone base"],
        ],
        [48 * mm, 52 * mm, 74 * mm],
        body_size=7.2,
    ))

    # ── 5. TURNOVER ──
    story.append(Paragraph("5. Turnover e maggiorazioni", h2))
    story.append(Paragraph(
        "Con contratti brevi aumentano sopralluoghi, check-out, preparazione immobile e coordinamento "
        "manutenzioni — ma <b>non</b> la ricerca inquilino (già remunerata dal conduttore). "
        "Le maggiorazioni vanno applicate sul <b>compenso di gestione</b>, non sulla mediazione.",
        body,
    ))
    story.append(make_table(
        ["Fascia durata", "Turnover", "Maggiorazione gestione", "Valutazione ipotesi interna"],
        [
            ["12–18 mesi", "Basso", "Tariffa base (0%)", "Corretta"],
            ["6–12 mesi", "Medio", "+10%", "Ipotesi 10%: corretta"],
            ["3–6 mesi", "Alto", "+20%", "Ipotesi 20%: corretta"],
            ["1–3 mesi", "Molto alto", "+35%", "Meglio 35% che 30–40% a scaglioni"],
        ],
        [28 * mm, 28 * mm, 42 * mm, 76 * mm],
        body_size=7.2,
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "<b>Contratti &lt; 3 mesi:</b> consigliata categoria separata con maggiorazione <b>+35%</b> sulla "
        "gestione annua (Ipotesi C/D ibrida), oppure canone fisso aggiuntivo €120–180/trimestre se preferite "
        "semplicità commerciale.",
        body,
    ))

    # ── 6. CONFRONTO MODELLI ──
    story.append(Paragraph("6. Confronto modelli tariffari", h2))
    story.append(make_table(
        ["Modello", "Pro", "Contro", "Giudizio"],
        [
            ["1: 1m + ½m (vostra)", "Semplice, competitivo", "Rischio sottovalutazione se full service", "✓ Consigliato*"],
            ["2: % annua 4–8%", "Allineato mercato", "Meno intuitivo", "Alternativa valida"],
            ["3: Fisso €/mese", "Prevedibile", "Disallineato da canoni diversi", "Solo portafogli omogenei"],
            ["4: Ibrido + turnover", "Più equo", "Più articolato", "✓ Migliore tecnicamente"],
            ["5: Solo % alta unica", "Facile da vendere", "Caro per cliente fedele", "Sconsigliato"],
        ],
        [32 * mm, 38 * mm, 38 * mm, 66 * mm],
        body_size=6.8,
    ))
    story.append(Paragraph("* Con provvigione conduttore separata e maggiorazioni turnover.", small))

    story.append(PageBreak())

    # ── 7. FULL PM ──
    story.append(Paragraph("7. Full Property Management — perimetro servizi", h2))
    story.append(Paragraph("7.1 Inclusi nel compenso di gestione", h3))
    for item in [
        "Sopralluogo, analisi immobile, proposta canone, check documenti base",
        "Strategia locazione, annuncio, pubblicazione portali, gestione richieste",
        "Selezione conduttori, organizzazione visite (costo mediazione a carico conduttore)",
        "Contratto, registrazione, scadenzario, proroghe concordate, cessazione",
        "Punto di contatto inquilino, comunicazioni ordinarie, coordinamento manutenzioni ≤ €200",
        "Controllo periodico, verifica stato al cambio inquilino, report trimestrale proprietaria",
    ]:
        story.append(Paragraph(f"• {item}", bullet))
    story.append(Paragraph("7.2 Esclusi — fatturati a parte", h3))
    for item in [
        "Lavori straordinari e ristrutturazioni",
        "Contenzioso, sfratto, recupero crediti, assistenza legale",
        "Assicurazione morosità / rent guarantee",
        "Home staging premium, fotografia professionale avanzata",
        "Impuesto di registro, bollo, IMU, spese condominiali (sempre a carico proprietaria)",
    ]:
        story.append(Paragraph(f"• {item}", bullet))

    # ── 8. SCENARI ECONOMICI ──
    story.append(Paragraph("8. Scenari economici — 15 immobili", h2))
    story.append(Paragraph(
        "Calcolo ricavo totale = <b>Gestione proprietaria</b> + <b>Provvigioni conduttori</b> (turnover). "
        "Anno tipo con canone medio €900, turnover 50% (≈8 nuove locazioni/anno).",
        body,
    ))
    story.append(make_table(
        ["Canone medio", "Gestione annua (15×½ mens.)", "Turnover 50% intermediazione", "Totale annuo agenzia"],
        [
            ["€ 700", fmt_euro(15 * 350), fmt_euro(8 * 700), fmt_euro(15 * 350 + 8 * 700)],
            ["€ 900", fmt_euro(15 * 450), fmt_euro(8 * 900), fmt_euro(15 * 450 + 8 * 900)],
            ["€ 1.100", fmt_euro(15 * 550), fmt_euro(8 * 1100), fmt_euro(15 * 550 + 8 * 1100)],
            ["€ 1.300", fmt_euro(15 * 650), fmt_euro(8 * 1300), fmt_euro(15 * 650 + 8 * 1300)],
        ],
        [28 * mm, 52 * mm, 52 * mm, 42 * mm],
        body_size=7.5,
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "<b>Anno 1 (avvio portafoglio):</b> aggiungere 15 × 1 mensilità canone medio = "
        f"<b>{fmt_euro(15 * 900)}</b> una tantum (canone €900). Equivalente mensile anno 2+: "
        f"<b>{fmt_euro((15 * 450 + 8 * 900) / 12)}/mese</b>.",
        body,
    ))
    story.append(make_table(
        ["Turnover annuo", "Nuove locazioni (su 15)", "Extra intermediazione (€900)", "Impatto vs 0% turnover"],
        [
            ["0%", "0", "€ 0", "Solo gestione € 6.750"],
            ["25%", "≈ 4", fmt_euro(4 * 900), "+ € 3.600"],
            ["50%", "≈ 8", fmt_euro(8 * 900), "+ € 7.200"],
            ["75%", "≈ 11", fmt_euro(11 * 900), "+ € 9.900"],
            ["100%", "15", fmt_euro(15 * 900), "+ € 13.500"],
        ],
        [28 * mm, 38 * mm, 42 * mm, 66 * mm],
        body_size=7.2,
    ))

    story.append(PageBreak())

    # ── 9. VALUTAZIONE IPOTESI ──
    story.append(Paragraph("9. Valutazione formula «1 mens. + ½ mens.»", h2))
    story.append(make_table(
        ["Criterio", "Giudizio", "Commento"],
        [
            ["Competitività", "Alta", "Sotto molti operatori full service (7–8% annuo)"],
            ["Sostenibilità agenzia", "Buona*", "*Se provvigione conduttore copre turnover"],
            ["Rischio agenzia", "Medio-basso", "Turnover alto senza maggiorazioni gestione"],
            ["Convenienza cliente", "Alta", "Niente doppia commissione su nuove locazioni"],
            ["Facilità vendita", "Alta", "Due numeri chiari: avvio + gestione annua"],
        ],
        [38 * mm, 28 * mm, 108 * mm],
        body_size=7.5,
    ))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(
        "<b>LA CONSIGLIERESTI?</b> <b>SÌ</b>, con tre integrazioni: (1) maggiorazioni turnover sulla "
        "gestione; (2) listino Portfolio 15 unità; (3) proroga transitorio a tariffa dedicata (0,25 mens.).",
        body,
    ))

    # ── 10. TARIFFA PORTFOLIO ──
    story.append(Paragraph("10. Tariffa Portfolio — 15 immobili", h2))
    story.append(make_table(
        ["Scaglione", "Avvio gestione", "Gestione annua", "Nuova locazione proprietaria"],
        [
            ["1–3 immobili (listino)", "1,0 mensilità", "0,50 mens./anno", "Non richiesta (conduttore)"],
            ["4–10 immobili", "0,90 mensilità", "0,45 mens./anno", "Non richiesta"],
            ["10–15 immobili (Portfolio)", "0,85 mensilità", "0,45 mens./anno", "Non richiesta"],
        ],
        [42 * mm, 38 * mm, 42 * mm, 52 * mm],
        body_size=7.5,
    ))
    story.append(Spacer(1, 3 * mm))
    story.append(Paragraph(
        "<b>Presentazione commerciale consigliata:</b> «Listino standard X — per il Suo portafoglio di 15 unità "
        "applichiamo condizione Portfolio dedicata». Percepito come valore aggiunto, non come sconto disperato.",
        body,
    ))

    # ── 11. PROPOSTA FINALE ──
    story.append(Paragraph("11. Proposta commerciale operativa", h2))
    story.append(highlight_box("Offerta consigliata a presentare alla proprietaria", [
        "<b>Pacchetto Portfolio 15 — «Gestione Zero Pensieri»</b>",
        "• <b>Avvio</b> (una tantum per immobile): <b>0,85 mensilità</b> del canone",
        "• <b>Gestione annua</b>: <b>0,45 mensilità/anno</b> (≈ 5,4% canone annuo)",
        "• <b>Nuova locazione</b>: <b>€ 0 per la proprietaria</b> — provvigione standard a carico del conduttore",
        "• <b>Maggiorazioni gestione</b>: +10% (6–12 mesi), +20% (3–6 mesi), +35% (&lt; 3 mesi)",
        "• <b>Proroga transitorio</b> (stesso inquilino): <b>0,25 mensilità</b>",
        "• <b>Referente unico</b> + report trimestrale + manutenzioni ordinarie fino a €200 incluse",
    ], st))
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph(
        f"<b>Ricavo potenziale annuo (canone medio €900, turnover 50%, Portfolio):</b><br/>"
        f"Gestione: 15 × €405 = {fmt_euro(15 * 405)} · Intermediazione: 8 × €900 = {fmt_euro(7200)} · "
        f"<b>Totale ≈ {fmt_euro(15 * 405 + 7200)}/anno</b> "
        f"(+ avvio una tantum {fmt_euro(15 * 765)} al primo anno).",
        body,
    ))

    # ── 12. CONCLUSIONI ──
    story.append(Paragraph("12. Conclusioni e raccomandazione", h2))
    story.append(Paragraph(
        "Se fossi consulente di Gruppo Immobiliare Bertinato Gino, presenterei alla proprietaria il "
        "<b>Pacchetto Portfolio 15</b> sopra descritto: professionale, conveniente (niente doppie commissioni), "
        "e remunerativo grazie al mix gestione + provvigioni conduttori sui turnover transitori.",
        body,
    ))
    story.append(Paragraph(
        "La vostra ipotesi di partenza <b>non è sbagliata</b>: va solo <b>completata</b> con maggiorazioni "
        "turnover, sconto portfolio e chiara separazione tra mediazione (conduttore) e property management (proprietaria).",
        body,
    ))
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph("Documento redatto per uso interno — Gruppo Immobiliare Bertinato Gino", small))
    story.append(Paragraph(
        f"Righetto Immobiliare · {data_perizia.strftime('%d/%m/%Y')} · info@righettoimmobiliare.it",
        ParagraphStyle("sig", alignment=TA_CENTER, fontSize=8, textColor=GRIGIO),
    ))

    return story


def build_pdf(out_path: Path, data_doc: date) -> Path:
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=22 * mm,
    )

    def canvas_maker(*args, **kwargs):
        return AnalisiCanvas(*args, doc_title="Analisi PM riservata", **kwargs)

    doc.build(build_story(data_doc), canvasmaker=canvas_maker)
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
