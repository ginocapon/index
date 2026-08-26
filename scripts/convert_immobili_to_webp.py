# -*- coding: utf-8 -*-
"""Converte JPG/PNG in img/immobili/ → WebP (quality 82, max 1600px)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG_DIR = ROOT / "img" / "immobili"
SOURCE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tif", ".tiff"}


def to_webp(src: Path, dest: Path) -> bool:
    try:
        from PIL import Image  # type: ignore
    except ImportError:
        raise SystemExit("Pillow mancante: pip install Pillow")

    img = Image.open(src)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    max_w = 1600
    if img.width > max_w:
        ratio = max_w / img.width
        img = img.resize((max_w, int(img.height * ratio)), Image.Resampling.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "WEBP", quality=82, method=4)
    return True


def main() -> int:
    if not IMG_DIR.is_dir():
        print("Nessuna cartella img/immobili/")
        return 0

    converted = 0
    for src in sorted(IMG_DIR.rglob("*")):
        if not src.is_file():
            continue
        ext = src.suffix.lower()
        if ext not in SOURCE_EXT:
            continue
        dest = src.with_suffix(".webp")
        if dest.is_file() and dest.stat().st_size > 0:
            src.unlink(missing_ok=True)
            print(f"SKIP (webp esiste): {src.relative_to(ROOT).as_posix()}")
            continue
        to_webp(src, dest)
        src.unlink(missing_ok=True)
        print(f"OK {dest.relative_to(ROOT).as_posix()}")
        converted += 1

    print(f"\nConvertiti: {converted}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
