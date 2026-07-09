#!/usr/bin/env python3
"""Aggiorna title/meta affitti su pagine zona-* (esclusa limena già fatto)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# file -> (label breve per title, slug filtro opzionale)
ZONES: dict[str, tuple[str, str]] = {
    "zona-arcella-padova.html": ("Arcella, Padova", "arcella"),
    "zona-centro-storico-padova.html": ("Centro Storico, Padova", "centro-storico"),
    "zona-forcellini-padova.html": ("Forcellini, Padova", "forcellini"),
    "zona-guizza-padova.html": ("Guizza, Padova", "guizza"),
    "zona-prato-della-valle-padova.html": ("Prato della Valle, Padova", "prato"),
    "zona-sacra-famiglia-padova.html": ("Sacra Famiglia, Padova", "sacra-famiglia"),
    "zona-universitaria-padova.html": ("Zona Universitaria, Padova", "universitaria"),
    "zona-voltabarozzo-padova.html": ("Voltabarozzo, Padova", "voltabarozzo"),
    "zona-vigonza.html": ("Vigonza", "vigonza"),
    "zona-rubano.html": ("Rubano", "rubano"),
    "zona-selvazzano.html": ("Selvazzano Dentro", "selvazzano"),
    "zona-abano-terme.html": ("Abano Terme", "abano"),
    "zona-ponte-san-nicolo.html": ("Ponte San Nicolo', Padova", "ponte-san-nicolo"),
}


def patch_file(path: Path, label: str) -> bool:
    raw = path.read_text(encoding="utf-8")
    orig = raw
    new_title = f"Case in Vendita e Affitto a {label} | Righetto Immobiliare"

    raw = re.sub(
        r"<title>[^<]+</title>",
        f"<title>{new_title}</title>",
        raw,
        count=1,
    )
    raw = re.sub(
        r'<meta property="og:title" content="[^"]*"',
        f'<meta property="og:title" content="{new_title}"',
        raw,
        count=1,
    )
    raw = re.sub(
        r'<meta name="twitter:title" content="[^"]*"',
        f'<meta name="twitter:title" content="{new_title}"',
        raw,
        count=1,
    )

    desc_m = re.search(r'<meta name="description" content="([^"]*)"', raw)
    if desc_m:
        old = desc_m.group(1)
        if "affitt" not in old.lower()[:40]:
            new_desc = f"Affitti e {old[0].lower()}{old[1:]}" if old else f"Affitti e case in vendita a {label}. Righetto Immobiliare dal 2000."
            if len(new_desc) > 158:
                new_desc = f"Affitti e case in vendita a {label}. Agenzia Righetto Immobiliare — vendita e locazione dal 2000."
            raw = raw.replace(
                f'<meta name="description" content="{old}"',
                f'<meta name="description" content="{new_desc}"',
                1,
            )

    og_m = re.search(r'<meta property="og:description" content="([^"]*)"', raw)
    if og_m:
        old = og_m.group(1)
        if "affitt" not in old.lower()[:40]:
            new_og = f"Affitti e case in vendita a {label}. Righetto Immobiliare — vendita e locazione."
            raw = raw.replace(
                f'<meta property="og:description" content="{old}"',
                f'<meta property="og:description" content="{new_og}"',
                1,
            )

    raw = re.sub(
        r"Ultimo aggiornamento: [^<]+",
        "Ultimo aggiornamento: 9 luglio 2026",
        raw,
        count=1,
    )

    hero_m = re.search(r'<div class="hero-btns">.*?</div>', raw, re.DOTALL)
    if hero_m and 'immobili?op=affitto' not in hero_m.group(0):
        raw = re.sub(
            r'(<div class="hero-btns">\s*<a href="immobili" class="btn-gold">[^<]+</a>)',
            r'\1\n      <a href="immobili?op=affitto" class="btn-outline">Affitti in zona</a>',
            raw,
            count=1,
        )

    if raw != orig:
        path.write_text(raw, encoding="utf-8")
        return True
    return False


def main() -> None:
    n = 0
    for fname, (label, _) in ZONES.items():
        p = ROOT / fname
        if not p.exists():
            print(f"SKIP missing {fname}")
            continue
        if patch_file(p, label):
            print(f"OK {fname}")
            n += 1
        else:
            print(f"-- {fname} (no change)")
    print(f"\nAggiornate {n} zone page")


if __name__ == "__main__":
    main()
