# -*- coding: utf-8 -*-
"""Verifica pagine share-immobile: OG completo, canonical su immobile?s=, noindex."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "data" / "og-immobili.json"
REQUIRED_OG = ("og:title", "og:description", "og:image", "og:url")


def check_file(path: Path) -> list[str]:
    errs: list[str] = []
    html = path.read_text(encoding="utf-8")
    if 'content="noindex, follow' not in html and 'content="noindex,follow' not in html:
        errs.append("manca noindex (rischio contenuto duplicato in Google)")
    m = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    if not m or "/immobile?s=" not in m.group(1):
        errs.append("canonical non punta a immobile?s=")
    for prop in REQUIRED_OG:
        if f'property="{prop}"' not in html:
            errs.append(f"manca {prop}")
    img = re.search(r'property="og:image" content="([^"]+)"', html)
    if img and not img.group(1).startswith("http"):
        errs.append("og:image non assoluto")
    if 'property="og:image" content="https://righettoimmobiliare.it/img/team/titolari.webp"' in html:
        errs.append("og:image fallback generico (nessuna foto annuncio)")
    return errs


def main() -> int:
    if not CATALOG.is_file():
        print("ERRORE: data/og-immobili.json assente — esegui sync_og_immobili.py")
        return 1
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    seo_count = len(catalog.get("bySlug") or {})
    legacy_count = len(catalog.get("byLegacySlug") or {})
    files = sorted(ROOT.glob("share-immobile-*.html"))
    print(f"Catalogo: {seo_count} slug SEO, {legacy_count} alias legacy")
    print(f"File share: {len(files)}")

    errors: list[str] = []
    for f in files:
        file_errs = check_file(f)
        for e in file_errs:
            errors.append(f"{f.name}: {e}")

    # Ogni immobile attivo deve avere pagina share SEO
    for slug, entry in (catalog.get("bySlug") or {}).items():
        fname = entry.get("share_file")
        if fname and not (ROOT / fname).is_file():
            errors.append(f"MANCANTE {fname} (codice {entry.get('codice')})")

    if errors:
        print(f"\nFAIL: {len(errors)} problemi")
        for e in errors[:30]:
            print(" -", e)
        if len(errors) > 30:
            print(f" ... e altri {len(errors) - 30}")
        return 1

    print("OK: tutte le pagine share hanno OG, noindex, canonical immobile?s=")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
