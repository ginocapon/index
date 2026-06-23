# -*- coding: utf-8 -*-
"""Genera perizia immobiliare PDF — stile Righetto Immobiliare."""
from __future__ import annotations

import io
from datetime import date
from pathlib import Path

import fitz
from PIL import Image, ImageOps
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4, landscape
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
PLAN_PDF = Path(r"c:\Users\Utente\Downloads\pinate e prospetti (2).pdf")
OUT_PDF = ROOT / "documenti" / "Perizia_Turato_Antonio_Bifamiliare.pdf"

# Brand Righetto (skill-design / blog)
NERO = colors.HexColor("#152435")
BLU = colors.HexColor("#2C4A6E")
ORO = colors.HexColor("#FF6B35")
SFONDO = colors.HexColor("#ECE7DF")
GRIGIO = colors.HexColor("#6B7A8D")
BIANCO = colors.HexColor("#F7F5F1")

DATA_PERIZIA = date(2026, 6, 15)
PROPRIETARIO = "Sig. Turato Antonio"
TIPOLOGIA = "Bifamiliare"
SUP_COMM = 196.30
VALORE = 240_000
EURO_MQ = round(VALORE / SUP_COMM)


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


def stack_images_vertical(paths: list[Path], gap: int = 14, labels: list[str] | None = None) -> Image.Image:
    """Impila planimetrie/prospetti alla stessa larghezza, senza buchi bianchi."""
    from PIL import ImageDraw

    ims: list[Image.Image] = []
    for p in paths:
        with Image.open(p) as im:
            ims.append(im.convert("RGB"))

    target_w = max(im.width for im in ims)
    scaled: list[Image.Image] = []
    for im in ims:
        if im.width != target_w:
            nh = int(im.height * target_w / im.width)
            im = im.resize((target_w, nh), Image.Resampling.LANCZOS)
        scaled.append(im)

    label_h = 28 if labels else 0
    block_heights = [im.height + (label_h if labels else 0) for im in scaled]
    total_h = sum(block_heights) + gap * (len(scaled) - 1)
    out = Image.new("RGB", (target_w, total_h), (255, 255, 255))
    draw = ImageDraw.Draw(out)
    y = 0
    for i, im in enumerate(scaled):
        if labels and i < len(labels):
            draw.rectangle((0, y, target_w, y + label_h - 6), fill=(236, 231, 223))
            draw.text((8, y + 6), labels[i], fill=(44, 74, 110))
            y += label_h
        out.paste(im, (0, y))
        y += im.height + gap
    return out


def fit_rl_image(path: Path, max_w: float, max_h: float) -> RLImage:
    """Scala immagine/composito per riempire lo spazio disponibile senza lasciare buchi."""
    with Image.open(path) as im:
        w, h = im.size
    ratio = h / w
    img_w = max_w
    img_h = img_w * ratio
    if img_h > max_h:
        img_h = max_h
        img_w = img_h / ratio
    return RLImage(str(path), width=img_w, height=img_h)


def save_composite(im: Image.Image, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    im.save(path, "JPEG", quality=92, optimize=True)
    return path


def split_prospetto_horizontal(im: Image.Image) -> Image.Image:
    """Due elevazioni impilate → affiancate in orizzontale."""
    w, h = im.size
    mid = h // 2
    top = trim_white(im.crop((0, 0, w, mid - 20)))
    bottom = trim_white(im.crop((0, mid + 20, w, h)))
    target_h = max(top.height, bottom.height)

    def scale_to_h(img: Image.Image) -> Image.Image:
        if img.height == target_h:
            return img
        nw = int(img.width * target_h / img.height)
        return img.resize((nw, target_h), Image.Resampling.LANCZOS)

    top = scale_to_h(top)
    bottom = scale_to_h(bottom)
    gap = 24
    out = Image.new("RGB", (top.width + gap + bottom.width, target_h), (255, 255, 255))
    out.paste(top, (0, 0))
    out.paste(bottom, (top.width + gap, 0))
    return out


def extract_plan_images(pdf_path: Path, tmp_dir: Path) -> list[tuple[str, Path]]:
    tmp_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    labels = [
        "Planimetria piano terra",
        "Planimetria piano primo / sottotetto",
        "Prospetto est",
        "Prospetto ovest",
    ]
    out: list[tuple[str, Path]] = []
    for i, page in enumerate(doc):
        pix = page.get_pixmap(matrix=fitz.Matrix(2.5, 2.5), alpha=False)
        raw = Image.open(io.BytesIO(pix.tobytes("png")))
        rotated = raw.transpose(Image.Transpose.ROTATE_270)
        cleaned = trim_white(rotated)
        if i >= 2:
            cleaned = split_prospetto_horizontal(cleaned)
        path = tmp_dir / f"plan_{i}.jpg"
        cleaned.convert("RGB").save(path, "JPEG", quality=92, optimize=True)
        out.append((labels[i] if i < len(labels) else f"Allegato {i + 1}", path))
    doc.close()
    return out


class RighettoCanvas(canvas.Canvas):
    """Footer e cornice su ogni pagina."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states: list[dict] = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved_page_states) + 1
        for i, state in enumerate(self._saved_page_states):
            self.__dict__.update(state)
            self._draw_frame(i + 1, total)
            canvas.Canvas.showPage(self)
        self.__dict__.update(self._saved_page_states[-1] if self._saved_page_states else {})
        self._draw_frame(total, total)
        canvas.Canvas.save(self)

    def _draw_frame(self, page_num: int, total: int):
        w, h = A4
        # Bordo esterno
        self.setStrokeColor(BLU)
        self.setLineWidth(1.2)
        self.rect(10 * mm, 12 * mm, w - 20 * mm, h - 22 * mm, stroke=1, fill=0)
        # Accento oro in alto
        self.setFillColor(ORO)
        self.rect(10 * mm, h - 12 * mm - 2, w - 20 * mm, 2, stroke=0, fill=1)
        # Footer
        self.setFillColor(NERO)
        self.rect(10 * mm, 12 * mm, w - 20 * mm, 8 * mm, stroke=0, fill=1)
        self.setFillColor(colors.white)
        self.setFont("Helvetica", 7)
        self.drawString(
            14 * mm,
            15.5 * mm,
            "Righetto Immobiliare — Via Roma n.96, Limena (PD) — Tel. 049.8843484 — righettoimmobiliare.it",
        )
        self.drawRightString(
            w - 14 * mm,
            15.5 * mm,
            f"Perizia riservata — Pag. {page_num}/{total}",
        )


def build_pdf(plan_images: list[tuple[str, Path]], tmp_dir: Path) -> None:
    doc = SimpleDocTemplate(
        str(OUT_PDF),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=20 * mm,
        bottomMargin=22 * mm,
        title="Perizia immobiliare — Sig. Turato Antonio",
        author="Righetto Immobiliare",
    )

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "RTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        textColor=BLU,
        spaceAfter=4,
        alignment=TA_CENTER,
    )
    subtitle = ParagraphStyle(
        "RSub",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        textColor=GRIGIO,
        alignment=TA_CENTER,
        spaceAfter=10,
    )
    h2 = ParagraphStyle(
        "RH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=BLU,
        spaceBefore=8,
        spaceAfter=4,
        borderPadding=2,
    )
    body = ParagraphStyle(
        "RBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=NERO,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
    )
    small = ParagraphStyle(
        "RSmall",
        parent=body,
        fontSize=8,
        textColor=GRIGIO,
        alignment=TA_JUSTIFY,
    )

    story = []

    # Header brand con logo
    logo_cell = Paragraph("", ParagraphStyle("empty"))
    if LOGO_PATH.is_file():
        logo_cell = RLImage(str(LOGO_PATH), width=28 * mm, height=28 * mm)
    header_data = [
        [
            logo_cell,
            Paragraph(
                '<font name="Helvetica-Bold" size="14" color="#2C4A6E">RIGHETTO IMMOBILIARE</font><br/>'
                '<font size="8" color="#6B7A8D">Gruppo Immobiliare dal 2000 — Padova e Provincia</font><br/>'
                '<font size="7.5" color="#152435">Via Roma n.96, Limena (PD) · Tel. 049.8843484 · info@righettoimmobiliare.it</font>',
                ParagraphStyle("hdr", alignment=TA_LEFT, leading=11),
            ),
            Paragraph(
                f'<font size="8" color="#6B7A8D">Data perizia</font><br/>'
                f'<font size="11" color="#152435"><b>{DATA_PERIZIA.strftime("%d/%m/%Y")}</b></font>',
                ParagraphStyle("dt", alignment=TA_CENTER),
            ),
        ]
    ]
    ht = Table(header_data, colWidths=[32 * mm, 98 * mm, 44 * mm])
    ht.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOX", (1, 0), (1, 0), 1, BLU),
                ("BACKGROUND", (1, 0), (1, 0), SFONDO),
                ("LEFTPADDING", (1, 0), (1, 0), 8),
                ("RIGHTPADDING", (1, 0), (1, 0), 8),
                ("TOPPADDING", (1, 0), (1, 0), 6),
                ("BOTTOMPADDING", (1, 0), (1, 0), 6),
            ]
        )
    )
    story.append(ht)
    story.append(Spacer(1, 8 * mm))

    story.append(Paragraph("RELAZIONE DI STIMA IMMOBILIARE", title))
    story.append(
        Paragraph(
            "Documento riservato — valutazione di mercato a scopo informativo e negoziale",
            subtitle,
        )
    )

    # Box riepilogo
    riep = [
        ["Proprietario", PROPRIETARIO],
        ["Tipologia immobile", TIPOLOGIA],
        ["Superficie commerciale stimata", f"{SUP_COMM:,.2f} mq".replace(",", ".")],
        ["Valore di mercato stimato", f"€ {VALORE:,.0f}".replace(",", ".")],
        ["Incidenza unitaria", f"€ {EURO_MQ:,.0f}/mq".replace(",", ".")],
    ]
    t = Table(riep, colWidths=[58 * mm, 116 * mm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), BLU),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9.5),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("BACKGROUND", (1, 0), (1, -1), SFONDO),
                ("BOX", (0, 0), (-1, -1), 0.5, BLU),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#E1DBD1")),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(t)
    story.append(Spacer(1, 6 * mm))

    story.append(Paragraph("1. Oggetto della perizia", h2))
    story.append(
        Paragraph(
            f"La presente relazione illustra la stima del valore di mercato dell'immobile "
            f"di proprietà del <b>{PROPRIETARIO}</b>, tipologia <b>{TIPOLOGIA}</b>, "
            f"desumibile dalle planimetrie catastali e dagli elaborati grafici allegati "
            f"(planimetrie piano terra e piano primo/sottotetto, prospetti est e ovest). "
            f"La valutazione è stata redatta da <b>Righetto Immobiliare</b> in data "
            f"<b>{DATA_PERIZIA.day} giugno {DATA_PERIZIA.year}</b> sulla base del metodo comparativo "
            f"e del calcolo della superficie commerciale secondo prassi di mercato.",
            body,
        )
    )

    story.append(Paragraph("2. Calcolo superficie commerciale", h2))
    story.append(
        Paragraph(
            "Dati rilevati dalle planimetrie — maggiorazione murature +15%, "
            "coefficiente sottotetto 70%.",
            body,
        )
    )

    calc_rows = [
        ["Livello", "Dettaglio", "Superficie commerciale"],
        [
            "Piano terra",
            "Interno 94,05 mq + portici 14,50 mq → netto 108,55 mq × 1,15",
            "124,83 mq",
        ],
        [
            "Sottotetto",
            "Netto 88,78 mq × 1,15 = 102,10 mq × 0,70",
            "71,47 mq",
        ],
        ["Totale stimato", "124,83 + 71,47", f"{SUP_COMM:.2f} mq"],
    ]
    tc = Table(calc_rows, colWidths=[32 * mm, 98 * mm, 44 * mm])
    tc.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BLU),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("BACKGROUND", (0, -1), (-1, -1), SFONDO),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                ("BOX", (0, 0), (-1, -1), 0.5, BLU),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#E1DBD1")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(tc)
    story.append(Spacer(1, 4 * mm))
    story.append(
        Paragraph(
            "<i>Espressione complessiva: [(94,05 + 14,50) × 1,15] + [(88,78 × 1,15) × 0,70] "
            "= 124,83 + 71,47 = <b>196,30 mq</b></i>",
            small,
        )
    )

    story.append(Paragraph("3. Valutazione economica", h2))
    story.append(
        Paragraph(
            f"Sulla base della superficie commerciale stimata in <b>{SUP_COMM:.2f} mq</b>, "
            f"delle caratteristiche costruttive desumibili dagli elaborati grafici allegati "
            f"e del confronto con immobili analoghi nel segmento bifamiliare, si stima un "
            f"<b>valore di mercato complessivo pari a € {VALORE:,.0f}</b> "
            f"(incidenza indicativa € {EURO_MQ:,.0f}/mq).".replace(",", "."),
            body,
        )
    )

    val_box = Table(
        [[Paragraph(f'<font size="22" color="#FF6B35"><b>€ {VALORE:,.0f}</b></font>'.replace(",", "."), ParagraphStyle("v", alignment=TA_CENTER))]],
        colWidths=[174 * mm],
    )
    val_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), NERO),
                ("BOX", (0, 0), (-1, -1), 1, ORO),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(val_box)

    story.append(PageBreak())

    # Pagina planimetrie — composito unico, riempie la pagina senza buchi
    plan_labels = [lbl for lbl, _ in plan_images[:2]]
    plan_paths = [p for _, p in plan_images[:2]]
    plan_composite = stack_images_vertical(
        plan_paths,
        gap=10,
        labels=plan_labels,
    )
    plan_composite_path = save_composite(plan_composite, tmp_dir / "composite_planimetrie.jpg")

    story.append(Paragraph("5. Allegati grafici — Planimetrie", h2))
    story.append(Spacer(1, 2 * mm))
    max_w = 174 * mm
    max_h_plans = 228 * mm
    story.append(fit_rl_image(plan_composite_path, max_w, max_h_plans))

    story.append(PageBreak())

    # Pagina prospetti — composito unico
    prosp_labels = [lbl for lbl, _ in plan_images[2:]]
    prosp_paths = [p for _, p in plan_images[2:]]
    prosp_composite = stack_images_vertical(prosp_paths, gap=12, labels=prosp_labels)
    prosp_composite_path = save_composite(prosp_composite, tmp_dir / "composite_prospetti.jpg")

    story.append(Paragraph("6. Allegati grafici — Prospetti", h2))
    story.append(Spacer(1, 2 * mm))
    max_h_prosp = 228 * mm
    story.append(fit_rl_image(prosp_composite_path, max_w, max_h_prosp))

    story.append(Spacer(1, 5 * mm))
    story.append(
        KeepTogether(
            [
                Paragraph("4. Note e limiti", h2),
                Paragraph(
                    "La presente stima ha carattere <b>indicativo</b> e non sostituisce una perizia "
                    "tecnico-giuridica redatta da perito abilitato. Il valore effettivo può variare "
                    "in base a stato manutentivo, conformità urbanistico-catastale e condizioni di "
                    "mercato. Righetto Immobiliare — Gruppo Immobiliare dal 2000, Limena (PD).",
                    small,
                ),
            ]
        )
    )

    story.append(Spacer(1, 4 * mm))
    story.append(
        Paragraph(
            f"<i>Documento generato il {DATA_PERIZIA.strftime('%d/%m/%Y')} — "
            f"{PROPRIETARIO} — Uso riservato</i>",
            ParagraphStyle("foot", alignment=TA_CENTER, fontSize=8, textColor=GRIGIO),
        )
    )

    doc.build(story, canvasmaker=RighettoCanvas)
    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    print(f"OK: {OUT_PDF} ({OUT_PDF.stat().st_size // 1024} KB)")
    dl = Path.home() / "Downloads" / OUT_PDF.name
    try:
        dl.write_bytes(OUT_PDF.read_bytes())
        print(f"Copia: {dl}")
    except OSError as e:
        print(f"Download non copiato: {e}")


def main() -> int:
    tmp = ROOT / "scripts" / "_tmp_perizia"
    if not PLAN_PDF.is_file():
        print(f"Manca file planimetrie: {PLAN_PDF}")
        return 2
    plans = extract_plan_images(PLAN_PDF, tmp)
    build_pdf(plans, tmp)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
