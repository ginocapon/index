"""One-shot: import user PNG heroes from Cursor assets into img/blog as 1200x630 WebP."""
import os
from pathlib import Path

from PIL import Image


def _open_path(path: Path) -> str:
    """Windows: percorsi >260 caratteri richiedono prefisso \\\\?\\."""
    resolved = path.resolve()
    s = str(resolved)
    if os.name == "nt" and not s.startswith("\\\\?\\"):
        return "\\\\?\\" + s
    return s

ASSETS = Path(
    r"C:\Users\Utente\.cursor\projects\c-Users-Utente-progetti-index\assets"
)
OUT = Path(__file__).resolve().parent.parent / "img" / "blog"
TARGET_W, TARGET_H = 1200, 630

PAIRS = [
    (
        "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_planimetria-catastale-rasterizzata1-752282081-4d36fb39-457e-4449-9f0f-8e5d74fa63d0.png",
        "blog-planimetria-catasto-padova-2026.webp",
    ),
    (
        "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_Casa_ecologica_in_costruzione_con_pannelli_solari-55862b8b-ad5f-499a-a349-6828c395751f.png",
        "blog-ape-acquisto-padova-2026.webp",
    ),
    (
        "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_come-funziona-la-permuta-immobiliare-2042395926-b9fb2051-a730-493d-85d1-f4b4c0b589cb.png",
        "blog-permuta-immobiliare-padova-2026.webp",
    ),
    (
        "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_Esposizione_di_auto_depoca_in_villa_storica-8eafe550-c775-47e0-8ddf-54198a0f6031.png",
        "blog-piazzola-brenta-mercato-2026.webp",
    ),
    (
        "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_vigonza-f994ae7f-bde4-4f76-ad20-ac17be216733.png",
        "blog-vigonza-rubano-cintura-2026.webp",
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


def cover_resize(img: Image.Image, tw: int, th: int) -> Image.Image:
    src_w, src_h = img.size
    scale = max(tw / src_w, th / src_h)
    new_w = int(round(src_w * scale))
    new_h = int(round(src_h * scale))
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - tw) // 2
    top = (new_h - th) // 2
    return img.crop((left, top, left + tw, top + th))


def main() -> None:
    if not ASSETS.is_dir():
        raise SystemExit(f"Cartella assets non trovata: {ASSETS}")
    OUT.mkdir(parents=True, exist_ok=True)
    for src_name, dst_name in PAIRS:
        src = ASSETS / src_name
        if not os.path.isfile(_open_path(src)):
            raise SystemExit(f"Manca il file sorgente: {src}")
        with Image.open(_open_path(src)) as im:
            rgb = to_rgb(im)
            out_img = cover_resize(rgb, TARGET_W, TARGET_H)
        out_path = OUT / dst_name
        out_img.save(out_path, "WEBP", quality=86, method=6)
        kb = out_path.stat().st_size // 1024
        print(f"{dst_name}\t{kb} KB")


if __name__ == "__main__":
    main()
