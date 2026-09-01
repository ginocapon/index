#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera perizia immobiliare PDF Righetto — template JSON riutilizzabile.

Uso:
  python scripts/genera_perizia.py scripts/perizia_config_ragazzo_curtarolo.json
  python scripts/genera_perizia.py   # default turato se presente

Dipendenze: pymupdf, reportlab, pillow
"""
from __future__ import annotations

import io
import json
import sys
from datetime import date, datetime
from pathlib import Path

import fitz
from PIL import Image, ImageOps
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

NERO = colors.HexColor("#152435")
BLU = colors.HexColor("#2C4A6E")
ORO = colors.HexColor("#FF6B35")
SFONDO = colors.HexColor("#ECE7DF")
GRIGIO = colors.HexColor("#6B7A8D")


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_date(s: str) -> date:
    return datetime.strptime(s, "%Y-%m-%d").date()


def trim_white(im: Image.Image, margin: int = 8) -> Image.Image:
    gray = im.convert("L")
    inv = ImageOps.invert(gray)
    bbox = inv.getbbox()
    if not bbox:
        return im
    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - margin)
    y0 = max(0, y0 - margin)
    x1 = min(im.width, x1 + margin)
    y1 = min(im.height, y1 + margin)
    return im.crop((x0, y0, x1, y1))


def pdf_page_to_jpg(pdf_path: Path, out_dir: Path, prefix: str, dpi: float = 2.0) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    paths: list[Path] = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi, dpi), alpha=False)
        p = out_dir / f"{prefix}_{i + 1}.jpg"
        Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB").save(p, "JPEG", quality=92)
        paths.append(p)
    doc.close()
    return paths


def image_to_jpg(src: Path, out_dir: Path, name: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    p = out_dir / name
    with Image.open(src) as im:
        im.convert("RGB").save(p, "JPEG", quality=92)
    return p


def stack_vertical(paths: list[Path], labels: list[str] | None = None, gap: int = 12) -> Image.Image:
    from PIL import ImageDraw

    ims = [Image.open(p).convert("RGB") for p in paths]
    target_w = max(im.width for im in ims)
    scaled: list[Image.Image] = []
    for im in ims:
        if im.width != target_w:
            nh = int(im.height * target_w / im.width)
            im = im.resize((target_w, nh), Image.Resampling.LANCZOS)
        scaled.append(im)
    label_h = 26 if labels else 0
    total_h = sum(im.height + (label_h if labels else 0) for im in scaled) + gap * (len(scaled) - 1)
    out = Image.new("RGB", (target_w, total_h), (255, 255, 255))
    draw = ImageDraw.Draw(out)
    y = 0
    for i, im in enumerate(scaled):
        if labels and i < len(labels):
            draw.rectangle((0, y, target_w, y + label_h - 4), fill=(236, 231, 223))
            draw.text((10, y + 5), labels[i], fill=(44, 74, 110))
            y += label_h
        out.paste(im, (0, y))
        y += im.height + gap
    for im in ims:
        im.close()
    return out


def compose_side_by_side(
    paths: list[Path],
    labels: list[str],
    out_path: Path,
    panel_h: int = 300,
    gap: int = 10,
) -> Path:
    """Due screenshot affiancati con didascalie — impaginazione compatta."""
    from PIL import ImageDraw

    margin = 10
    label_h = 28
    panels: list[Image.Image] = []
    for p in paths:
        with Image.open(p) as im:
            im = im.convert("RGB")
            nw = int(im.width * panel_h / im.height)
            panels.append(im.resize((nw, panel_h), Image.Resampling.LANCZOS))

    inner_w = sum(p.width for p in panels) + gap * max(0, len(panels) - 1)
    total_w = inner_w + margin * 2
    total_h = panel_h + label_h + margin * 2
    out = Image.new("RGB", (total_w, total_h), (236, 231, 223))
    draw = ImageDraw.Draw(out)
    x = margin
    for i, panel in enumerate(panels):
        cap = labels[i] if i < len(labels) else ""
        if cap:
            draw.rectangle((x, margin, x + panel.width, margin + label_h - 2), fill=(44, 74, 110))
            draw.text((x + 4, margin + 6), cap[:72], fill=(255, 255, 255))
        y = margin + label_h
        draw.rectangle((x - 1, y - 1, x + panel.width + 1, y + panel.height + 1), outline=(44, 74, 110))
        out.paste(panel, (x, y))
        x += panel.width + gap
    out.save(out_path, "JPEG", quality=90)
    for p in panels:
        p.close()
    return out_path

def fit_rl_image(path: Path, max_w: float, max_h: float) -> RLImage:
    with Image.open(path) as im:
        w, h = im.size
    ratio = h / w
    img_w, img_h = max_w, max_w * ratio
    if img_h > max_h:
        img_h = max_h
        img_w = img_h / ratio
    return RLImage(str(path), width=img_w, height=img_h)


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
        self.drawString(14 * mm, 15.5 * mm, "Righetto Immobiliare — Via Roma n.96, Limena (PD) — Tel. 049.8843484 — righettoimmobiliare.it")
        self.drawRightString(w - 14 * mm, 15.5 * mm, f"Perizia riservata — Pag. {n}/{total}")


def fmt_euro(n: int | float) -> str:
    return f"€ {int(n):,.0f}".replace(",", ".")


def _esc_html(text: str) -> str:
    return (
        str(text or "—")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def make_price_box(
    valore: int,
    title_lines: list[str],
    note: str = "",
    extra: str = "",
) -> Table:
    """Box prezzo a righe separate — evita sovrapposizione testo/importo."""
    ps_title = ParagraphStyle(
        "pht", fontName="Helvetica-Bold", fontSize=8.5, leading=11,
        alignment=TA_CENTER, textColor=colors.white,
    )
    ps_price = ParagraphStyle(
        "php", fontName="Helvetica-Bold", fontSize=22, leading=28,
        alignment=TA_CENTER, textColor=ORO,
    )
    ps_note = ParagraphStyle(
        "phn", fontName="Helvetica", fontSize=7.5, leading=10,
        alignment=TA_CENTER, textColor=colors.HexColor("#cccccc"),
    )
    data: list[list] = [[Paragraph(line, ps_title)] for line in title_lines]
    data.append([Paragraph(f"<b>{fmt_euro(valore)}</b>", ps_price)])
    if note:
        data.append([Paragraph(_esc_html(note), ps_note)])
    if extra:
        data.append([Paragraph(extra, ps_note)])
    box = Table(data, colWidths=[174 * mm])
    box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NERO),
        ("BOX", (0, 0), (-1, -1), 1.5, ORO),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ]))
    return box


def make_kv_table(pairs: list[tuple[str, str]]) -> Table:
    """Tabella chiave-valore con a capo automatico nelle celle."""
    lbl = ParagraphStyle(
        "kl", fontName="Helvetica-Bold", fontSize=8, leading=10.5, textColor=colors.white,
    )
    val = ParagraphStyle(
        "kv", fontName="Helvetica", fontSize=8.5, leading=11.5, textColor=NERO,
    )
    rows = [[Paragraph(_esc_html(k), lbl), Paragraph(_esc_html(v), val)] for k, v in pairs]
    t = Table(rows, colWidths=[58 * mm, 116 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), BLU), ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
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


def make_data_table(
    header: list[str],
    body_rows: list[list[str]],
    col_widths: list[float],
    *,
    header_size: float = 7.5,
    body_size: float = 7.5,
) -> Table:
    """Tabella dati con Paragraph per a capo in ogni cella."""
    th = ParagraphStyle(
        "th", fontName="Helvetica-Bold", fontSize=header_size, leading=9.5,
        textColor=colors.white,
    )
    td = ParagraphStyle(
        "td", fontName="Helvetica", fontSize=body_size, leading=10,
        textColor=NERO,
    )
    td_c = ParagraphStyle("tdc", parent=td, alignment=TA_CENTER)
    rows: list[list] = [[Paragraph(_esc_html(c), th) for c in header]]
    for row in body_rows:
        cells = []
        for i, cell in enumerate(row):
            st = td_c if i > 0 and i < len(row) - 1 else td
            cells.append(Paragraph(_esc_html(cell), st))
        rows.append(cells)
    t = Table(rows, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLU),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BOX", (0, 0), (-1, -1), 0.5, BLU),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#E1DBD1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t

def build_pdf(cfg: dict, attachments: dict[str, Path], tmp: Path) -> Path:
    data_perizia = parse_date(cfg["data"])
    out_name = cfg.get("output_nome", "Perizia_Righetto.pdf")
    out_pdf = ROOT / "documenti" / out_name
    sup = float(cfg["superficie_commerciale"])
    valore = int(cfg["valore_principale"])
    euro_mq = round(valore / sup) if sup else 0

    styles = getSampleStyleSheet()
    title = ParagraphStyle("T", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=18, textColor=BLU, alignment=TA_CENTER, spaceAfter=4)
    subtitle = ParagraphStyle("S", fontName="Helvetica", fontSize=9, textColor=GRIGIO, alignment=TA_CENTER, spaceAfter=8)
    h2 = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=11.5, textColor=BLU, spaceBefore=7, spaceAfter=4)
    body = ParagraphStyle("B", fontName="Helvetica", fontSize=9.2, leading=13.5, textColor=NERO, alignment=TA_JUSTIFY, spaceAfter=5)
    small = ParagraphStyle("Sm", parent=body, fontSize=8, textColor=GRIGIO)
    bullet = ParagraphStyle("Bu", parent=body, leftIndent=12, bulletIndent=0, spaceAfter=3)

    doc = SimpleDocTemplate(str(out_pdf), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=18 * mm, bottomMargin=22 * mm)
    story: list = []

    # Pagina presentazione — vista 3D / satellite (opzionale)
    if attachments.get("presentazione") and attachments["presentazione"].is_file():
        if LOGO_PATH.is_file():
            story.append(RLImage(str(LOGO_PATH), width=32 * mm, height=32 * mm))
            story.append(Spacer(1, 4 * mm))
        story.append(Paragraph("RELAZIONE DI STIMA IMMOBILIARE", title))
        story.append(Paragraph(cfg.get("tipologia", ""), subtitle))
        story.append(Paragraph(f'<b>{cfg.get("ubicazione", "")}</b>', ParagraphStyle("loc", alignment=TA_CENTER, fontSize=11, textColor=BLU, spaceAfter=6)))
        story.append(Spacer(1, 2 * mm))
        story.append(fit_rl_image(attachments["presentazione"], 174 * mm, 155 * mm))
        story.append(Spacer(1, 4 * mm))
        loc = cfg.get("locazione") or {}
        loc_extra = ""
        if loc.get("enabled") and loc.get("scenarios"):
            best = max(loc["scenarios"], key=lambda s: s.get("mensile", 0))
            loc_extra = (
                f"Locazione indicativa fino a {fmt_euro(best.get('mensile', 0))}/mese — vedi sezione dedicata"
            )
        prev = make_price_box(
            valore,
            ["Valore indicativo di vendita"],
            f"Incidenza € {euro_mq:,.0f}/m² su {sup:.0f} m² commerciali".replace(",", "."),
            loc_extra,
        )
        story += [prev, Spacer(1, 3 * mm)]
        story.append(Paragraph(
            f'<i>Documento riservato — {data_perizia.strftime("%d/%m/%Y")} — Righetto Immobiliare</i>',
            ParagraphStyle("pc", alignment=TA_CENTER, fontSize=8, textColor=GRIGIO),
        ))
        story.append(PageBreak())

    logo = RLImage(str(LOGO_PATH), width=26 * mm, height=26 * mm) if LOGO_PATH.is_file() else Paragraph("", body)
    hdr = Table(
        [[
            logo,
            Paragraph(
                '<b><font color="#2C4A6E" size="13">RIGHETTO IMMOBILIARE</font></b><br/>'
                '<font size="8" color="#6B7A8D">Gruppo Immobiliare dal 2000 — Padova e Provincia</font><br/>'
                '<font size="7.5">Via Roma n.96, 35010 Limena (PD) · Tel. 049.8843484 · Cell. 349 736 5930</font><br/>'
                '<font size="7.5">info@righettoimmobiliare.it · righettoimmobiliare.it · P.IVA 05182390285</font>',
                ParagraphStyle("hdr", leading=11),
            ),
            Paragraph(f'<font size="8" color="#6B7A8D">Data perizia</font><br/><b>{data_perizia.strftime("%d/%m/%Y")}</b>', ParagraphStyle("d", alignment=TA_CENTER)),
        ]],
        colWidths=[30 * mm, 100 * mm, 44 * mm],
    )
    hdr.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BACKGROUND", (1, 0), (1, 0), SFONDO), ("BOX", (1, 0), (1, 0), 0.5, BLU), ("LEFTPADDING", (1, 0), (1, 0), 8), ("TOPPADDING", (1, 0), (1, 0), 6), ("BOTTOMPADDING", (1, 0), (1, 0), 6)]))
    story += [hdr, Spacer(1, 6 * mm)]

    story.append(Paragraph("RELAZIONE DI STIMA IMMOBILIARE", title))
    sottotitolo_doc = "Documento riservato — vendita e locazione — valutazione a scopo informativo e negoziale"
    if not (cfg.get("locazione") or {}).get("enabled"):
        sottotitolo_doc = "Documento riservato — valutazione di mercato a scopo informativo e negoziale"
    story.append(Paragraph(sottotitolo_doc, subtitle))
    if cfg.get("destinatario"):
        story.append(Paragraph(f'<i>A: {cfg["destinatario"]}</i>', ParagraphStyle("dest", alignment=TA_CENTER, fontSize=9, textColor=GRIGIO, spaceAfter=6)))

    riep = [
        ("Committente / titolarità", cfg["proprietario"]),
        ("Dettaglio anagrafico", cfg.get("proprietario_dettaglio", "—")),
        ("Tipologia", cfg["tipologia"]),
        ("Ubicazione", cfg["ubicazione"]),
        ("Superficie commerciale", f"{sup:,.0f} m²".replace(",", ".")),
        ("Valore vendita indicativo", fmt_euro(valore)),
        ("Incidenza indicativa", f"€ {euro_mq:,.0f}/m²".replace(",", ".")),
    ]
    if cfg.get("euro_mq_nota"):
        riep.append(("Nota incidenza", cfg["euro_mq_nota"]))
    story += [make_kv_table(riep), Spacer(1, 5 * mm)]

    # Sezione 1
    story.append(Paragraph("1. Oggetto della perizia", h2))
    oggetto = cfg.get("oggetto_perizia") or (
        f"La presente relazione illustra la stima del valore di mercato dell'immobile "
        f"<b>{cfg['tipologia']}</b>, sito in <b>{cfg['ubicazione']}</b>, di competenza "
        f"<b>{cfg['proprietario']}</b>. La valutazione è stata redatta da "
        f"<b>Righetto Immobiliare</b> in data <b>{data_perizia.strftime('%d/%m/%Y')}</b> "
        f"a seguito di sopralluogo e consultazione della documentazione catastale disponibile."
    )
    story.append(Paragraph(oggetto, body))

    # Sezione 2 Catasto
    cat = cfg["catasto"]
    indirizzo_cat = cfg.get("indirizzo_immobile") or cat.get("via", "")
    data_visura = cat.get("data_visura", data_perizia.strftime("%d/%m/%Y"))
    story.append(Paragraph(f"2. Dati catastali (visura {data_visura})", h2))
    story.append(Paragraph(
        f"Comune <b>{cat['comune']}</b> — {indirizzo_cat} — Sez. {cat['sezione']}, Foglio {cat['foglio']}. "
        f"Planimetria storica: {cat.get('particella_nceu', '—')}. "
        f"{cat.get('titolarita', '')}. Rendita catastale complessiva indicativa: <b>{cat.get('rendita_totale', '—')}</b>.",
        body,
    ))
    cat_rows = []
    for u in cat["unita"]:
        cat_rows.append([
            u["sub"], u["categoria"], u.get("classe", "—"),
            u["consistenza"], u["piano"], u["rendita"],
        ])
    tc = make_data_table(
        ["Sub.", "Cat.", "Cl.", "Consistenza", "Piano", "Rendita"],
        cat_rows,
        [14 * mm, 18 * mm, 12 * mm, 38 * mm, 18 * mm, 74 * mm],
        body_size=8,
    )
    story += [tc, Spacer(1, 3 * mm)]

    # Terreni (opzionale)
    terreni = cat.get("terreni", [])
    if terreni:
        story.append(Paragraph("<b>Terreni annessi (visura):</b>", body))
        tr = [["Comune", "Fg", "Part.", "Cat.", "Cl.", "Sup.", "Rendite"]]
        for t in terreni:
            tr.append([
                t.get("comune", "—"), t.get("foglio", "—"), t.get("particella", "—"),
                t.get("categoria", "—"), t.get("classe", "—"), t.get("superficie", "—"),
                t.get("rendite", "—"),
            ])
        tt = Table(tr, colWidths=[28 * mm, 10 * mm, 12 * mm, 22 * mm, 10 * mm, 18 * mm, 74 * mm])
        tt.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BLU), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("FONTSIZE", (0, 0), (-1, -1), 7.5),
            ("BOX", (0, 0), (-1, -1), 0.5, BLU), ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#E1DBD1")),
            ("LEFTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))
        story += [tt, Spacer(1, 3 * mm)]
        if cat.get("nota_terreno"):
            story.append(Paragraph(cat["nota_terreno"], body))

    # Intestatari
    intestatari = cfg.get("proprietari", [])
    if intestatari:
        story.append(Paragraph("<b>Intestatari e quote di proprietà (visura):</b>", body))
        pr_rows = []
        for p in intestatari:
            pr_rows.append([
                p.get("nome", "—"), p.get("cf", "—"), p.get("nascita", "—"),
                p.get("diritti", "Proprietà"), p.get("quota", "—"),
            ])
        pt = make_data_table(
            ["Nominativo", "C.F.", "Nascita", "Diritti", "Quota"],
            pr_rows,
            [36 * mm, 36 * mm, 40 * mm, 26 * mm, 26 * mm],
            body_size=7.2,
        )
        story += [pt, Spacer(1, 3 * mm)]

    # Sezione 3 Descrizione immobile (unica, coerente vendita/locazione)
    story.append(Paragraph("3. Descrizione dell'immobile", h2))
    if cfg.get("descrizione_fabbricato"):
        story.append(Paragraph("<b>Fabbricato e contesto</b>", body))
        story.append(Paragraph(cfg["descrizione_fabbricato"], body))
    if cfg.get("descrizione_unita"):
        story.append(Paragraph("<b>Unità immobiliare oggetto di stima</b>", body))
        story.append(Paragraph(cfg["descrizione_unita"], body))

    # Sezione 4 Caratteristiche
    story.append(Paragraph("4. Caratteristiche generali e stato manutentivo", h2))
    for c in cfg.get("caratteristiche", []):
        story.append(Paragraph(f"• {c}", bullet))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph(f"<b>Stato manutentivo:</b> {cfg.get('stato_manutentivo', '—')}", body))

    # Sezione 5 Urbanistico
    story.append(Paragraph("5. Verifiche urbanistiche e criticità emerse", h2))
    for c in cfg.get("criticita_urbanistiche", []):
        story.append(Paragraph(f"• {c}", bullet))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph("<b>Obblighi per la vendita</b>", h2))
    obblighi = cfg.get("obblighi_vendita", [])
    if obblighi:
        for ob in obblighi:
            story.append(Paragraph(f"• {ob}", bullet))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph("<b>Attività prioritarie prima della commercializzazione:</b>", body))
    for a in cfg.get("attivita_prioritarie", []):
        story.append(Paragraph(f"• {a}", bullet))

    story.append(PageBreak())

    # Sezione 6 Valutazione vendita
    story.append(Paragraph("6. Valutazione economica — vendita", h2))
    story.append(Paragraph(
        f"Sulla base della superficie commerciale di <b>{sup:.0f} m²</b>, dello stato di fatto, "
        f"delle caratteristiche descritte e del confronto con immobili comparabili in "
        f"<b>{cfg.get('ubicazione', 'zona di riferimento')}</b>, si indica il seguente valore indicativo.",
        body,
    ))

    val_box = make_price_box(
        valore,
        ["PREZZO INDICATIVO DI PARTENZA", "COMMERCIALIZZAZIONE"],
        cfg.get("euro_mq_nota", ""),
    )
    story += [Spacer(1, 2 * mm), val_box, Spacer(1, 4 * mm)]

    for label, key in [
        ("Forchetta prudenziale di mercato (post-sopralluogo)", "valore_secondario"),
        ("Scenario conservativo (difformità non sanabili / costi elevati)", "valore_conservativo"),
    ]:
        if cfg.get(key):
            story.append(Paragraph(f"<b>{label}:</b> {cfg[key]}", body))

    story.append(Spacer(1, 4 * mm))
    nota_fin = cfg.get("nota_valore_finale") or (
        f"Il prezzo di partenza indicato in <b>{fmt_euro(valore)}</b> rappresenta il "
        f"<b>tetto massimo prudente</b> per l'avvio della commercializzazione, tenuto conto delle "
        f"criticità descritte. La stima dovrà essere confermata dopo l'accesso agli atti e la "
        f"quantificazione dei costi di ripristino e sanatoria."
    )
    story.append(Paragraph(nota_fin, body))

    for para in cfg.get("considerazioni_commerciali", []):
        story.append(Paragraph(para, body))
    if cfg.get("target_acquirente"):
        story.append(Paragraph(f"<b>Target indicativo:</b> {cfg['target_acquirente']}", body))
    if cfg.get("nota_mercato"):
        story.append(Paragraph(cfg["nota_mercato"], body))

    # Sezione 7 Locazione (opzionale)
    loc = cfg.get("locazione") or {}
    if loc.get("enabled"):
        story.append(PageBreak())
        story.append(Paragraph("7. Valutazione locazione — scenari indicativi", h2))
        if loc.get("intro"):
            story.append(Paragraph(loc["intro"], body))
        if loc.get("gestione_nota"):
            story.append(Paragraph(loc["gestione_nota"], body))
        body_rows = []
        for sc in loc.get("scenarios", []):
            lordo = sc.get("annuo_lordo")
            if lordo is None and sc.get("mensile"):
                lordo = sc["mensile"] * 12
            netto = sc.get("annuo_netto", "—")
            if isinstance(netto, (int, float)):
                netto = fmt_euro(netto)
            body_rows.append([
                sc.get("nome", "—"),
                fmt_euro(sc.get("mensile", 0)) if sc.get("mensile") else "—",
                fmt_euro(lordo) if isinstance(lordo, (int, float)) else str(lordo or "—"),
                str(netto),
                sc.get("note", sc.get("tassazione", "—")),
            ])
        lt = make_data_table(
            ["Soluzione", "Canone/mese", "Lordo annuo", "Netto annuo*", "Note"],
            body_rows,
            [50 * mm, 22 * mm, 24 * mm, 24 * mm, 54 * mm],
            body_size=7.2,
        )
        story += [Spacer(1, 3 * mm), lt, Spacer(1, 2 * mm)]
        story.append(Paragraph("* Netto indicativo dopo tassazione ipotizzata; da detrarre IMU secondo regime applicabile.", small))
        if loc.get("conclusioni"):
            story.append(Paragraph(loc["conclusioni"], body))

    # Sezione commercializzazione / portali (opzionale)
    comm = cfg.get("commercializzazione") or {}
    sec_num = 8
    if comm.get("enabled"):
        story.append(PageBreak())
        titolo_comm = comm.get("titolo") or f"{sec_num}. Commercializzazione, portali e reportistica"
        story.append(Paragraph(titolo_comm, h2))
        for para in comm.get("paragrafi", []):
            story.append(Paragraph(para, body))
        for punto in comm.get("punti", []):
            story.append(Paragraph(f"• {punto}", bullet))
        if comm.get("nota_whatsapp"):
            story.append(Paragraph(comm["nota_whatsapp"], body))
        if comm.get("nota_chatbot"):
            story.append(Paragraph(comm["nota_chatbot"], body))

        # Mockup chatbot Sara (visual)
        if comm.get("mostra_mockup_chatbot", True):
            chat = Table(
                [[
                    Paragraph(
                        '<font color="#2C4A6E"><b>Assistente Sara — righettoimmobiliare.it</b></font><br/>'
                        '<font size="8" color="#6B7A8D">Online · risponde anche fuori orario d\'ufficio</font>',
                        ParagraphStyle("chh", fontSize=8.5, leading=11),
                    ),
                ], [
                    Paragraph(
                        '<font size="8.5" color="#333">Buongiorno! Sono Sara, l\'assistente Righetto. '
                        'Posso aiutarla con informazioni su questo appartamento, fissare una visita '
                        'o richiedere una valutazione gratuita.</font>',
                        ParagraphStyle("cb", fontSize=8.5, leading=12, backColor=SFONDO, leftIndent=4, rightIndent=4),
                    ),
                ], [
                    Paragraph(
                        '<font size="8.5" color="#fff"><i>Vorrei sapere se l\'immobile è ancora disponibile '
                        'e fissare una visita.</i></font>',
                        ParagraphStyle("cu", fontSize=8.5, leading=12, alignment=TA_LEFT),
                    ),
                ]],
                colWidths=[120 * mm],
            )
            chat.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8F5E9")),
                ("BOX", (0, 0), (-1, -1), 0.5, BLU),
                ("BACKGROUND", (0, 1), (-1, 1), SFONDO),
                ("BACKGROUND", (0, 2), (-1, 2), BLU),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ]))
            story += [Spacer(1, 3 * mm), chat, Spacer(1, 2 * mm)]
            story.append(Paragraph(
                "<i>Esempio di interazione con l'assistente conversazionale del sito — "
                "orientamento visitatori e raccolta richieste anche di sera e nei weekend.</i>",
                small,
            ))

        imgs_comm = attachments.get("commercializzazione_immagini") or []
        if imgs_comm:
            story.append(Spacer(1, 4 * mm))
            labels = comm.get("immagini_didascalie") or []
            short_labels = [
                (labels[i][:55] + "…") if len(labels[i]) > 55 else labels[i]
                for i in range(min(len(labels), len(imgs_comm)))
            ]
            valid = [Path(p) for p in imgs_comm if Path(p).is_file()]
            if len(valid) >= 2:
                comp_path = tmp / "comm_side_by_side.jpg"
                compose_side_by_side(valid[:2], short_labels[:2] or ["Portali", "Agenda"], comp_path)
                story.append(fit_rl_image(comp_path, 174 * mm, 78 * mm))
            elif len(valid) == 1:
                if labels:
                    story.append(Paragraph(f"<b>{labels[0]}</b>", body))
                story.append(fit_rl_image(valid[0], 174 * mm, 72 * mm))
            story.append(Spacer(1, 3 * mm))
        sec_num += 1

    # Contatti
    story.append(Spacer(1, 5 * mm))
    ct = Table(
        [[
            Paragraph("<b>Per informazioni</b><br/>049.8843484<br/>349 736 5930", ParagraphStyle("c", fontSize=9)),
            Paragraph("<b>Email / Web</b><br/>info@righettoimmobiliare.it<br/>righettoimmobiliare.it", ParagraphStyle("c", fontSize=9)),
            Paragraph("<b>Sede</b><br/>Via Roma n.96<br/>35010 Limena (PD)", ParagraphStyle("c", fontSize=9)),
        ]],
        colWidths=[58 * mm, 58 * mm, 58 * mm],
    )
    ct.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), SFONDO), ("BOX", (0, 0), (-1, -1), 0.5, BLU), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    story.append(ct)

    story.append(PageBreak())

    # Allegati grafici
    max_w, max_h = 174 * mm, 230 * mm

    if attachments.get("planimetria"):
        imgs = [attachments["planimetria"]] if attachments["planimetria"].is_file() else []
        if imgs:
            comp = stack_vertical(imgs, ["Planimetria catastale storica (N.C.E.U.)"])
            cp = tmp / "comp_planimetria.jpg"
            comp.save(cp, "JPEG", quality=92)
            story.append(Paragraph("Allegato A — Planimetria catastale fabbricato", h2))
            story.append(fit_rl_image(cp, max_w, max_h))
            story.append(PageBreak())

    if attachments.get("catasto_pages"):
        labels = [f"Visura catastale — pagina {i+1}" for i in range(len(attachments["catasto_pages"]))]
        comp = stack_vertical(attachments["catasto_pages"], labels)
        cp = tmp / "comp_catasto.jpg"
        comp.save(cp, "JPEG", quality=92)
        story.append(Paragraph("Allegato B — Scheda / visura catastale", h2))
        story.append(fit_rl_image(cp, max_w, max_h))
        story.append(PageBreak())

    if attachments.get("visura_immagini"):
        labels = attachments.get("visura_labels") or [
            f"Estratto visura — {i + 1}" for i in range(len(attachments["visura_immagini"]))
        ]
        comp = stack_vertical(attachments["visura_immagini"], labels)
        cp = tmp / "comp_visura.jpg"
        comp.save(cp, "JPEG", quality=92)
        story.append(Paragraph(
            cfg.get("allegato_visura_titolo", "Allegato B — Visura catastale fabbricati"),
            h2,
        ))
        story.append(fit_rl_image(cp, max_w, max_h))
        story.append(PageBreak())

    if attachments.get("vista_aerea") and attachments["vista_aerea"].is_file() and cfg.get("allegati", {}).get("vista_aerea_in_allegati", False):
        story.append(Paragraph("Allegato C — Vista aerea dell'area (satellite)", h2))
        story.append(Paragraph("Inquadramento dell'immobile e del contesto edificato — Cavino di Curtarolo.", small))
        story.append(Spacer(1, 3 * mm))
        story.append(fit_rl_image(attachments["vista_aerea"], max_w, max_h * 0.85))

    doc.build(story, canvasmaker=RighettoCanvas)
    return out_pdf


def asset_path(p: str) -> Path:
    path = Path(p)
    if p and not path.is_file():
        alt = ROOT / p
        if alt.is_file():
            return alt
    return path


def prepare_attachments(cfg: dict, tmp: Path) -> dict[str, Path | list[Path]]:
    allegati = cfg.get("allegati", {})
    out: dict = {}

    plan_path = asset_path(allegati.get("planimetria_catastale", ""))
    if plan_path.is_file():
        if plan_path.suffix.lower() == ".pdf":
            pages = pdf_page_to_jpg(plan_path, tmp, "plan", dpi=2.2)
            if pages:
                out["planimetria"] = pages[0]
        else:
            out["planimetria"] = image_to_jpg(plan_path, tmp, "plan.jpg")

    scheda = asset_path(allegati.get("scheda_catastale", ""))
    if scheda.is_file():
        out["catasto_pages"] = pdf_page_to_jpg(scheda, tmp, "catasto", dpi=2.0)

    scheda_g = asset_path(allegati.get("scheda_catastale_garage", ""))
    if scheda_g.is_file():
        extra = pdf_page_to_jpg(scheda_g, tmp, "catasto_garage", dpi=2.0)
        if out.get("catasto_pages"):
            out["catasto_pages"].extend(extra)
        else:
            out["catasto_pages"] = extra

    visura_imgs = allegati.get("visura_immagini") or []
    paths = [asset_path(p) for p in visura_imgs if asset_path(p).is_file()]
    if paths:
        out["visura_immagini"] = [image_to_jpg(p, tmp, f"visura_{i+1}.jpg") for i, p in enumerate(paths)]
        out["visura_labels"] = allegati.get("visura_labels")

    aerial = asset_path(allegati.get("vista_aerea", ""))
    if aerial.is_file():
        jpg = image_to_jpg(aerial, tmp, "vista_aerea.jpg")
        out["vista_aerea"] = jpg
        if allegati.get("presentazione") or allegati.get("usa_vista_aerea_in_copertina", True):
            out["presentazione"] = jpg

    comm_imgs: list[Path] = []
    for key in ("immagine_portali", "immagine_report_visite"):
        src = asset_path(allegati.get(key, ""))
        if src.is_file():
            comm_imgs.append(image_to_jpg(src, tmp, f"comm_{key}.jpg"))
    if comm_imgs:
        out["commercializzazione_immagini"] = comm_imgs

    return out


def main() -> int:
    cfg_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "scripts" / "perizia_config_turato.json"
    if not cfg_path.is_file():
        print(f"Config non trovato: {cfg_path}")
        return 2
    cfg = load_config(cfg_path)
    tmp = ROOT / "scripts" / "_tmp_perizia" / cfg_path.stem
    attachments = prepare_attachments(cfg, tmp)
    out = build_pdf(cfg, attachments, tmp)
    archive = ROOT / "data" / "perizie" / out.name
    archive.parent.mkdir(parents=True, exist_ok=True)
    archive.write_bytes(out.read_bytes())
    print(f"Archivio admin: {archive}")
    legacy = ROOT / "documenti" / "perizie" / out.name
    legacy.parent.mkdir(parents=True, exist_ok=True)
    legacy.write_bytes(out.read_bytes())
    print(f"OK: {out} ({out.stat().st_size // 1024} KB)")
    dl = Path.home() / "Downloads" / out.name
    try:
        dl.write_bytes(out.read_bytes())
        print(f"Copia: {dl}")
    except OSError as e:
        print(f"Download non copiato: {e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
