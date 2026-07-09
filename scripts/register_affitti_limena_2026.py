# -*- coding: utf-8 -*-
"""Registra blog-affitti-limena-2026 in blog.html, sitemap.xml, llms.txt.
Esegui: python scripts/register_affitti_limena_2026.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "blog-affitti-limena-2026"
DATE = "2026-07-09"
TITLE = "Affitti Limena 2026: Canoni, Quartieri e Guida Completa"
HERO = "img/blog/blog-affitti-canoni-fimaa-q1-2026-padova.webp"
SUMMARY = (
    "Guida affitti Limena 2026: OMI locazione ADE, quartieri, tipologie e ricerca "
    "appartamento in affitto con agenzia immobiliare Limena."
)

BLOG_ENTRY = {
    "titolo": TITLE,
    "categoria": "Mercato locazione",
    "data": DATE,
    "stato": "pubblicato",
    "immagine_copertina": HERO,
    "url_statico": SLUG,
    "tempo": 13,
    "autore": "Gino Capon",
    "contenuto": SUMMARY,
    "evidenza": True,
}

LLMS_LINE = (
    f"- [Affitti Limena 2026: canoni e quartieri]"
    f"(https://righettoimmobiliare.it/{SLUG})"
)


def js_obj(d: dict, indent: int = 6) -> str:
    pad = " " * indent
    lines = ["{"]
    keys = list(d.keys())
    for i, k in enumerate(keys):
        v = d[k]
        comma = "," if i < len(keys) - 1 else ""
        if isinstance(v, bool):
            sv = "true" if v else "false"
        elif isinstance(v, (int, float)):
            sv = str(v)
        else:
            sv = json.dumps(v, ensure_ascii=False)
        lines.append(f"{pad}{json.dumps(k, ensure_ascii=False)}: {sv}{comma}")
    lines.append(" " * (indent - 2) + "}")
    return "\n".join(lines)


def register_blog_html() -> None:
    path = ROOT / "blog.html"
    text = path.read_text(encoding="utf-8")
    if SLUG in text:
        print("blog.html: già registrato")
        return
    needle = "  const articoliStatici = [\n"
    block = js_obj(BLOG_ENTRY, indent=6) + ",\n"
    if needle not in text:
        raise RuntimeError("Marker articoliStatici non trovato in blog.html")
    path.write_text(text.replace(needle, needle + block, 1), encoding="utf-8")
    print("blog.html: +1 articolo (in testa, evidenza: true)")


def register_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    if SLUG in text:
        print("sitemap.xml: già registrato")
        return
    marker = (
        "  <url><loc>https://righettoimmobiliare.it/blog-mercato-immobiliare-limena-2026</loc>"
        "<lastmod>2026-04-01</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n"
    )
    url_line = (
        f"  <url><loc>https://righettoimmobiliare.it/{SLUG}</loc>"
        f"<lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n"
    )
    if marker not in text:
        raise RuntimeError("Marker blog-mercato-immobiliare-limena non trovato in sitemap.xml")
    path.write_text(text.replace(marker, marker + url_line, 1), encoding="utf-8")
    print("sitemap.xml: +1 URL dopo mercato Limena")


def register_llms() -> None:
    path = ROOT / "llms.txt"
    text = path.read_text(encoding="utf-8")
    if SLUG in text:
        print("llms.txt: già registrato")
        return
    marker = (
        "- [Mercato immobiliare Limena 2026]"
        "(https://righettoimmobiliare.it/blog-mercato-immobiliare-limena-2026)\n"
    )
    if marker not in text:
        raise RuntimeError("Sezione Limena (mercato) non trovata in llms.txt")
    path.write_text(text.replace(marker, marker + LLMS_LINE + "\n", 1), encoding="utf-8")
    print("llms.txt: +1 riga sezione Limena")


def main() -> None:
    register_blog_html()
    register_sitemap()
    register_llms()
    print("Registrazione completata.")


if __name__ == "__main__":
    main()
