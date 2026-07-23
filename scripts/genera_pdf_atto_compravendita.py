#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unisce foto atto di compravendita in PDF A4 ad alta definizione (Pillow + PyMuPDF)."""
from __future__ import annotations

import io
import sys
from pathlib import Path

import fitz
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
ASSETS = Path(
    r"C:\Users\Utente\.cursor\projects\c-Users-Utente-progetti-index\assets"
)
OUT_DIR = ROOT / "documenti"
OUT_PDF = OUT_DIR / "atto-compravendita-via-santini-padova-2003.pdf"

# Ordine pagine (IMG_5853 = pag. 1 … IMG_5863 = pag. 11)
PAGE_FILES = [
    "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_IMG_5853-847b501f-5ce5-404a-88a5-1d4ec9ca3959.png",
    "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_IMG_5854-c0e59323-1ec9-4bf7-89f9-5e25e69b5c31.png",
    "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_IMG_5855-66a95ec7-c16e-4cfc-8ce1-e741cab1b06d.png",
    "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_IMG_5856-1219f13e-6583-452a-8f75-6221c0013ce5.png",
    "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_IMG_5857-b78491e2-0ed9-4eb4-9e8f-1f0b3a887ba9.png",
    "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_IMG_5858-ec59b332-05e0-4f5b-9e64-f0c3b364d6e8.png",
    "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_IMG_5859-bfc2809f-8b95-4484-b741-7692c4fb9285.png",
    "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_IMG_5860-8825759b-2eb1-4e8d-bb7c-537c3f7a75fc.png",
    "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_IMG_5861-e63a36ca-424e-4e8f-a99c-1b1d2caa99d8.png",
    "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_IMG_5862-5b6ea283-48f3-4e1d-9a55-0e467756c783.png",
    "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_IMG_5863-4dd2b595-ef15-487d-9ede-cb98ec907f3b.png",
]

# Rotazione manuale per pagine già in portrait o orientate diversamente (gradi CCW Pillow)
PAGE_ROTATION = {
    5: 0,   # pag. 5 (5857) già verticale
}


def load_oriented(path: Path, page_num: int) -> Image.Image:
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")

    extra = PAGE_ROTATION.get(page_num, None)
    if extra is not None:
        if extra:
            img = img.rotate(extra, expand=True, resample=Image.Resampling.BICUBIC)
        return img

    # Foto orizzontali: ruota 90° antiorario → testo in lettura verticale
    if img.width > img.height:
        img = img.rotate(90, expand=True, resample=Image.Resampling.BICUBIC)
    return img


def enhance_document(img: Image.Image, scale: float = 4.0) -> Image.Image:
    w, h = img.size
    nw, nh = int(w * scale), int(h * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)

    # Leggera correzione livelli (schiarisce carta, scurisce inchiostro)
    img = ImageOps.autocontrast(img, cutoff=1)
    img = ImageEnhance.Contrast(img).enhance(1.35)
    img = ImageEnhance.Brightness(img).enhance(1.04)
    img = ImageEnhance.Sharpness(img).enhance(2.0)
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=180, threshold=3))
    return img


def pil_page_to_pdf_bytes(img: Image.Image, dpi: int = 300) -> bytes:
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=96, optimize=True, dpi=(dpi, dpi))
    buf.seek(0)
    img_doc = fitz.open(stream=buf.read(), filetype="jpeg")
    pdf_bytes = img_doc.convert_to_pdf()
    img_doc.close()
    return pdf_bytes


def build_pdf(out_path: Path) -> int:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc = fitz.open()
    pages = 0

    for i, name in enumerate(PAGE_FILES, start=1):
        src = ASSETS / name
        if not src.exists():
            print(f"MANCA: {src}", file=sys.stderr)
            continue
        raw = load_oriented(src, i)
        enhanced = enhance_document(raw)
        page_pdf = pil_page_to_pdf_bytes(enhanced)
        sub = fitz.open("pdf", page_pdf)
        doc.insert_pdf(sub)
        sub.close()
        pages += 1
        print(f"  pag. {i:2d} OK  {src.name[-24:]}  -> {enhanced.size[0]}x{enhanced.size[1]} px")

    if pages == 0:
        raise SystemExit("Nessuna pagina elaborata.")

    # Metadati PDF
    doc.set_metadata({
        "title": "Atto di compravendita — Via G. Santini 1, Padova (2003)",
        "author": "Notaio Bruno Saglietti — elaborazione digitale Righetto",
        "subject": "Compravendita immobiliare — Poste Italiane / Agnoletto Flavio",
        "keywords": "compravendita, Padova, Santini, atto notarile",
    })
    doc.save(str(out_path), garbage=4, deflate=True)
    doc.close()
    return pages


def main() -> int:
    print(f"Output: {OUT_PDF}")
    n = build_pdf(OUT_PDF)
    size_kb = OUT_PDF.stat().st_size // 1024
    print(f"Completato: {n} pagine, {size_kb} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
