# -*- coding: utf-8 -*-
"""Registra batch blog 27 maggio 2026 in blog.html, admin, homepage.js, sitemap."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REG = json.loads((ROOT / "scripts" / "may27_blog_registry.json").read_text(encoding="utf-8"))


def js_obj(d: dict, indent: int = 4) -> str:
    """Serializza dict come literal JS (semplice)."""
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
        lines.append(f'{pad}{json.dumps(k, ensure_ascii=False)}: {sv}{comma}')
    lines.append(" " * (indent - 2) + "}")
    return "\n".join(lines)


def js_static_map_entry(titolo: str, img: str, url: str) -> str:
    key = titolo.lower().replace("\\", "\\\\").replace("'", "\\'")
    return f"    '{key}': {{ img: '{img}', url: '{url}' }},"


def main() -> None:
    blog_entries = REG["blog_html_articoliStatici"]
    admin_entries = REG["admin_blogSeedArticles"]
    hp_entries = REG["homepage_js_articoliStatici"]

    # blog.html
    blog_path = ROOT / "blog.html"
    text = blog_path.read_text(encoding="utf-8")
    block = ",\n".join(js_obj(e, indent=6) for e in blog_entries)
    needle = "  const articoliStatici = [\n"
    if "blog-sondaggio-bancaditalia-q1-2026-padova" in text:
        print("blog.html: già registrato")
    else:
        text = text.replace(needle, needle + block + ",\n", 1)
        blog_path.write_text(text, encoding="utf-8")
        print("blog.html: +5 articoli")

    # admin.html
    admin_path = ROOT / "admin.html"
    atext = admin_path.read_text(encoding="utf-8")
    ablock_parts = []
    for e in admin_entries:
        parts = [
            f"  {{ titolo: {json.dumps(e['titolo'], ensure_ascii=False)}",
            f"categoria: {json.dumps(e['categoria'], ensure_ascii=False)}",
            f"data: '{e['data']}'",
            f"tempo: {e['tempo']}",
            f"stato: '{e['stato']}'",
            f"autore: '{e['autore']}'",
            f"emoji: '{e['emoji']}'",
            f"immagine_copertina: '{e['immagine_copertina']}'",
            f"url_statico: '{e['url_statico']}'",
            f"contenuto: {json.dumps(e['contenuto'], ensure_ascii=False)}",
            f"evidenza: {'true' if e.get('evidenza') else 'false'}",
            f"data_pubblicazione: '{e['data_pubblicazione']}' }}",
        ]
        ablock_parts.append(", ".join(parts))
    ablock = ",\n".join(ablock_parts)
    aneedle = "const _blogSeedArticles = [\n"
    if "blog-sondaggio-bancaditalia-q1-2026-padova" in atext:
        print("admin.html: già registrato")
    else:
        atext = atext.replace(aneedle, aneedle + ablock + ",\n", 1)
        admin_path.write_text(atext, encoding="utf-8")
        print("admin.html: +5 seed")

    # homepage.js
    hp_path = ROOT / "js" / "homepage.js"
    htext = hp_path.read_text(encoding="utf-8")
    if "blog-sondaggio-bancaditalia-q1-2026-padova" in htext:
        print("homepage.js: già registrato")
    else:
        map_lines = "\n".join(
            js_static_map_entry(e["titolo"], e["immagine_copertina"], e["url_statico"])
            for e in hp_entries
        )
        htext = htext.replace(
            "  const staticMap = {\n",
            "  const staticMap = {\n" + map_lines + "\n",
            1,
        )
        hp_block = ",\n".join(
            "    { titolo: "
            + json.dumps(e["titolo"], ensure_ascii=False)
            + f", categoria: {json.dumps(e['categoria'], ensure_ascii=False)}"
            + f", data: '{e['data']}', stato: 'pubblicato'"
            + f", immagine_copertina: '{e['immagine_copertina']}'"
            + f", url_statico: '{e['url_statico']}' }}"
            for e in hp_entries
        )
        htext = htext.replace(
            "  const articoliStatici = [\n",
            "  const articoliStatici = [\n" + hp_block + ",\n",
            1,
        )
        hp_path.write_text(htext, encoding="utf-8")
        print("homepage.js: +5 articoli")

    # sitemap.xml
    sm_path = ROOT / "sitemap.xml"
    sm = sm_path.read_text(encoding="utf-8")
    if "blog-sondaggio-bancaditalia-q1-2026-padova" in sm:
        print("sitemap.xml: già registrato")
    else:
        urls = "\n".join(
            f'  <url><loc>https://righettoimmobiliare.it/{e["url_statico"]}</loc>'
            f'<lastmod>2026-05-27</lastmod><changefreq>monthly</changefreq>'
            f"<priority>0.85</priority></url>"
            for e in blog_entries
        )
        marker = "  <!-- Articoli blog — 20 maggio 2026"
        sm = sm.replace(
            marker,
            "  <!-- Articoli blog — 27 maggio 2026 (BdI / ISTAT / CRIF / geopolitica) -->\n"
            + urls
            + "\n  "
            + marker,
            1,
        )
        sm_path.write_text(sm, encoding="utf-8")
        print("sitemap.xml: +5 URL")


if __name__ == "__main__":
    main()
