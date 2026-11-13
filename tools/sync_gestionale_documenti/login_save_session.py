#!/usr/bin/env python3
"""Login manuale nel pannello legacy → salva storageState.json (da copiare in GESTIONALE_STORAGE_STATE)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from env_config import gestionale_base_url, load_config  # noqa: E402

OUT = Path(__file__).resolve().parent / "storageState.json"


def main() -> None:
    cfg = load_config()
    base = gestionale_base_url(cfg)
    print(f"Apri {base} — effettua login e 2FA, poi premi INVIO in questo terminale.")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(base + "/")
        input("Quando vedi la home del gestionale loggato, premi INVIO qui… ")
        state = context.storage_state()
        OUT.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
        print(f"Salvato {OUT} — copia il contenuto nel secret GESTIONALE_STORAGE_STATE (non committare).")
        browser.close()


if __name__ == "__main__":
    main()
