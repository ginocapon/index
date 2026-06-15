# -*- coding: utf-8 -*-
"""Registra batch acquisizioni giugno 16 in blog.html, admin, homepage.js, sitemap."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REG = json.loads((ROOT / "scripts" / "acquisizioni_giugno16_registry.json").read_text(encoding="utf-8"))
MARKER = "blog-ultime-acquisizioni-residenziali-padova-giugno-2026"


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


def js_static_map_entry(titolo: str, img: str, url: str) -> str:
    key = titolo.lower().replace("\\", "\\\\").replace("'", "\\'")
    return f"    '{key}': {{ img: '{img}', url: '{url}' }},"


def main() -> None:
    blog_entries = REG["blog_html_articoliStatici"]
    admin_entries = REG["admin_blogSeedArticles"]
    hp_entries = REG["homepage_js_articoliStatici"]

    blog_path = ROOT / "blog.html"
    text = blog_path.read_text(encoding="utf-8")
    if MARKER in text:
        print("blog.html: già registrato")
    else:
        block = ",\n".join(js_obj(e) for e in blog_entries)
        text = text.replace("  const articoliStatici = [\n", "  const articoliStatici = [\n" + block + ",\n", 1)
        blog_path.write_text(text, encoding="utf-8")
        print(f"blog.html: +{len(blog_entries)} articoli")

    admin_path = ROOT / "admin.html"
    atext = admin_path.read_text(encoding="utf-8")
    if MARKER in atext:
        print("admin.html: già registrato")
    else:
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
        atext = atext.replace("const _blogSeedArticles = [\n", "const _blogSeedArticles = [\n" + ",\n".join(ablock_parts) + ",\n", 1)
        admin_path.write_text(atext, encoding="utf-8")
        print(f"admin.html: +{len(admin_entries)} seed")

    hp_path = ROOT / "js" / "homepage.js"
    htext = hp_path.read_text(encoding="utf-8")
    if MARKER in htext:
        print("homepage.js: già registrato")
    else:
        hp_block = ",\n".join(js_obj(e) for e in hp_entries)
        htext = htext.replace("  const articoliStatici = [\n", "  const articoliStatici = [\n" + hp_block + ",\n", 1)
        map_lines = [js_static_map_entry(e["titolo"], e["immagine_copertina"], e["url_statico"]) for e in blog_entries]
        htext = htext.replace("  const staticMap = {\n", "  const staticMap = {\n" + "\n".join(map_lines) + "\n", 1)
        hp_path.write_text(htext, encoding="utf-8")
        print(f"homepage.js: +{len(hp_entries)} articoli + staticMap")

    sm_path = ROOT / "sitemap.xml"
    sm = sm_path.read_text(encoding="utf-8")
    added = 0
    for e in blog_entries:
        slug = e["url_statico"]
        if slug in sm:
            continue
        url = f"  <url><loc>https://righettoimmobiliare.it/{slug}</loc><lastmod>{e['data']}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n"
        sm = sm.replace("</urlset>\n", url + "</urlset>\n", 1)
        added += 1
    if added:
        sm_path.write_text(sm, encoding="utf-8")
        print(f"sitemap.xml: +{added} URL")
    else:
        print("sitemap.xml: già aggiornato")


if __name__ == "__main__":
    main()
