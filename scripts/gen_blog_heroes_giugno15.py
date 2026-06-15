# -*- coding: utf-8 -*-
"""Converte hero PNG batch giugno 15 2026 in WebP 1200x630."""
from __future__ import annotations

import os
from pathlib import Path

from PIL import Image

ASSETS = Path(r"C:\Users\Utente\.cursor\projects\c-Users-Utente-progetti-index\assets")
OUT = Path(__file__).resolve().parent.parent / "img" / "blog"
TARGET_W, TARGET_H = 1200, 630

PAIRS = [
    ("blog-hero-compravendite-q1-2026.png", "blog-compravendite-italia-q1-agenzia-entrate-2026.webp", 0.5, 0.42),
    ("blog-hero-affitti-fimaa-2026.png", "blog-affitti-canoni-fimaa-q1-2026-padova.webp", 0.5, 0.45),
    ("blog-hero-nuove-costruzioni-2026.png", "blog-nuove-costruzioni-mercato-veneto-2026-padova.webp", 0.5, 0.38),
    ("blog-hero-piano-casa-dl66-2026.png", "blog-piano-casa-decreto-66-2026-padova.webp", 0.48, 0.4),
    ("blog-hero-bce-mutui-giugno-2026.png", "blog-bce-tassi-mutui-giugno-2026-padova.webp", 0.5, 0.45),
]


def _open_path(path: Path) -> str:
    s = str(path.resolve())
    if os.name == "nt" and not s.startswith("\\\\?\\"):
        return "\\\\?\\" + s
    return s


def to_rgb(im: Image.Image) -> Image.Image:
    if im.mode in ("RGBA", "P"):
        if im.mode == "P":
            im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1] if im.mode == "RGBA" else None)
        return bg
    return im.convert("RGB")


def cover_resize(img: Image.Image, tw: int, th: int, ax: float, ay: float) -> Image.Image:
    ax, ay = min(1.0, max(0.0, ax)), min(1.0, max(0.0, ay))
    src_w, src_h = img.size
    scale = max(tw / src_w, th / src_h)
    new_w, new_h = int(round(src_w * scale)), int(round(src_h * scale))
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = int(round(max(0, new_w - tw) * ax))
    top = int(round(max(0, new_h - th) * ay))
    return img.crop((left, top, left + tw, top + th))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for src_name, dst_name, ax, ay in PAIRS:
        src = ASSETS / src_name
        if not os.path.isfile(_open_path(src)):
            raise SystemExit(f"Manca sorgente: {src}")
        with Image.open(_open_path(src)) as im:
            out_img = cover_resize(to_rgb(im), TARGET_W, TARGET_H, ax, ay)
        out_path = OUT / dst_name
        out_img.save(out_path, "WEBP", quality=86, method=6)
        print(f"{dst_name}\t{out_path.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
