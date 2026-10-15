# -*- coding: utf-8 -*-
"""Aggiorna annuncio LF0353 — porzione 40 mq Piazzola (foto WhatsApp + dati corretti)."""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from righetto_immobile_slug import generate_property_slug  # noqa: E402

SUPABASE_URL = "https://qwkwkemuabfwvwuqrxlu.supabase.co"
CODICE = "LF0353"
IMMO_ID = "6b0c7023-02ff-48b1-ae57-844c6993a226"
OUT_DIR = ROOT / "img" / "immobili" / CODICE

ASSETS = Path(
    r"C:\Users\Utente\.cursor\projects\c-Users-Utente-progetti-index\assets"
)
# Ordine galleria: soggiorno/cucina → soggiorno → camera → bagno → doccia
SOURCE_FILES = [
    "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_WhatsApp_Image_2026-10-15_at_16.25.00-3235aba4-ea45-4618-a0c6-6e5688b3be4f.jpg",
    "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_1WhatsApp_Image_2026-10-15_at_16.25.00-5d8360e6-1105-4a09-9d56-c0554c88a174.jpg",
    "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_5WhatsApp_Image_2026-10-15_at_16.25.26-e1317c41-04b2-4755-8a6e-2d0b4378c443.jpg",
    "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_4WhatsApp_Image_2026-10-15_at_16.25.01-c1471780-9962-4216-872d-4d053e8ec551.jpg",
    "c__Users_Utente_AppData_Roaming_Cursor_User_workspaceStorage_02d993d5cc19e4bea5396422fd725780_images_3WhatsApp_Image_2026-10-15_at_16.25.01-7a6d7951-31d7-4d9d-aef0-0bc2ed2ad3af.jpg",
]

DESCRIZIONE = """AFFITTASI — Piccola porzione di casa su due livelli a Piazzola sul Brenta (40 m²).

Porzione di casa su piano terra e primo piano, disponibile da subito.

Al piano terra ingresso diretto nel soggiorno con angolo cottura. Al piano superiore camera matrimoniale con bagno con doccia.

L'appartamento viene affittato arredato, con gli arredi presenti nelle foto.

Ambiente suggestivo: travi a vista e pareti con tinta originale dell'Ottocento, per un'atmosfera di carattere.

Classe energetica D. Nessuna spesa condominiale.

Canone: 495,00 € al mese.

Per informazioni e visite contattare Righetto Immobiliare."""


def load_key() -> str:
    key = os.environ.get("SUPABASE_KEY", "").strip()
    if key:
        return key
    for env_path in (ROOT / ".env", ROOT / "righetto_social" / ".env"):
        if not env_path.is_file():
            continue
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if line.startswith("SUPABASE_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("SUPABASE_KEY mancante")


def load_admin_secret() -> str:
    admin_html = ROOT / "admin.html"
    if not admin_html.is_file():
        return ""
    m = re.search(r"const RIG_ADMIN_RLS_SECRET = '([^']+)'", admin_html.read_text(encoding="utf-8"))
    return m.group(1) if m else ""


def headers(key: str, *, patch: bool = False) -> dict[str, str]:
    h = {"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    sec = load_admin_secret()
    if sec:
        h["x-righetto-admin"] = sec
    if patch:
        h["Prefer"] = "return=minimal"
    return h


def convert_photos() -> list[str]:
    try:
        from PIL import Image
    except ImportError:
        raise SystemExit("Installa Pillow: pip install Pillow")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # Rimuovi vecchie foto (solo webp in cartella)
    for old in OUT_DIR.glob("*.webp"):
        old.unlink()

    ts_base = int(time.time() * 1000)
    paths: list[str] = []
    labels = [
        "soggiorno-angolo-cottura",
        "soggiorno-scala",
        "camera-matrimoniale",
        "bagno",
        "doccia",
    ]
    for i, (name, label) in enumerate(zip(SOURCE_FILES, labels), start=1):
        src = ASSETS / name
        if not src.is_file():
            raise SystemExit(f"Foto mancante: {src}")
        webp_name = f"{i:03d}-{ts_base + i}-{label}-piazzola-40mq.webp"
        dest = OUT_DIR / webp_name
        im = Image.open(src)
        if im.mode in ("RGBA", "P"):
            im = im.convert("RGB")
        im.save(dest, "WEBP", quality=85, method=6)
        paths.append(f"img/immobili/{CODICE}/{webp_name}")
    return paths


def patch_immobile(key: str, foto: list[str]) -> None:
    row = {
        "tipologia": "appartamento",
        "tipo_operazione": "affitto_residenziale",
        "contratto_affitto_res": "affitto_ordinario",
        "titolo": "Affittasi porzione di casa su due livelli — Piazzola sul Brenta",
        "comune": "Piazzola sul Brenta",
        "indirizzo": "Via delle Logge, 12",
        "indirizzo_mappa": "Piazzola sul Brenta (PD)",
        "prezzo": 495,
        "superficie": 40,
        "locali": 2,
        "camere": 1,
        "bagni": 1,
        "bagni_totali": 1,
        "spese_condominio": 0,
        "classe_energetica": "D",
        "consegna": "Disponibile da subito",
        "descrizione": DESCRIZIONE,
        "arredato": True,
        "arredo": True,
        "giardino": False,
        "ingresso_indipendente": True,
        "piano_terra": True,
        "primo_piano": True,
        "soggiorno": True,
        "soggiorno_angolo_cottura": True,
        "cucina": True,
        "attivo": True,
        "venduto": False,
        "affittato": False,
        "lat": 45.5452,
        "lng": 11.7858,
        "foto": foto,
        "foto_urls": foto,
    }
    row["slug"] = generate_property_slug(
        {
            "tipologia": row["tipologia"],
            "tipo_operazione": row["tipo_operazione"],
            "comune": row["comune"],
            "codice": CODICE,
        }
    )
    url = f"{SUPABASE_URL}/rest/v1/immobili?id=eq.{IMMO_ID}"
    data = json.dumps(row, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="PATCH", headers=headers(key, patch=True))
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            r.read()
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"PATCH fallito {e.code}: {body}") from e
    print("Supabase aggiornato:", row["slug"])


def main() -> None:
    key = load_key()
    foto = convert_photos()
    print("Foto:", len(foto))
    patch_immobile(key, foto)
    print("OK — esegui: python scripts/sync_og_immobili.py")


if __name__ == "__main__":
    main()
