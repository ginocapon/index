# -*- coding: utf-8 -*-
"""WebP 1200x630 copertine blog acquisizioni giugno 16 — da foto portale."""
from __future__ import annotations

import io
import os
import urllib.request
from pathlib import Path

from PIL import Image

OUT = Path(__file__).resolve().parent.parent / "img" / "blog"
TARGET_W, TARGET_H = 1200, 630

PAIRS = [
    (
        "https://qwkwkemuabfwvwuqrxlu.supabase.co/storage/v1/object/public/foto-immobili/1779963017206-casa-singola-altichiero-4-.jpg",
        "blog-ultime-acquisizioni-residenziali-padova-giugno-2026.webp",
        0.5,
        0.42,
    ),
    (
        "https://qwkwkemuabfwvwuqrxlu.supabase.co/storage/v1/object/public/foto-immobili/1772466603404-999-643894af-2b59-4ddb-982e-3f6fa6f56801-y-3728210613.jpg",
        "blog-ultime-acquisizioni-commerciali-padova-giugno-2026.webp",
        0.5,
        0.38,
    ),
]


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


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "RighettoBlogHero/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for src_url, out_name, ax, ay in PAIRS:
        data = fetch(src_url)
        with Image.open(io.BytesIO(data)) as im:
            cover = cover_resize(to_rgb(im), TARGET_W, TARGET_H, ax, ay)
            dest = OUT / out_name
            cover.save(dest, "WEBP", quality=82, method=6)
            print(f"OK {dest} ({cover.size[0]}x{cover.size[1]})")


if __name__ == "__main__":
    main()
