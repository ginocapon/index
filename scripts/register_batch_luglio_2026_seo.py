# -*- coding: utf-8 -*-
"""Registra blog transitorio + rubano-limena in blog.html, sitemap.xml, llms.txt."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE = "2026-07-09"

ARTICLES = [
    {
        "slug": "blog-affitto-transitorio-padova-durata-2026",
        "titolo": "Affitto Transitorio Padova 2026: Durata, Requisiti e Guida Completa",
        "categoria": "Mercato locazione",
        "hero": "img/blog/blog-affitti-canoni-fimaa-q1-2026-padova.webp",
        "summary": (
            "Affitto transitorio Padova 2026: durata 1-18 mesi, motivazioni documentate, "
            "differenza da 4+4 e 3+2, registrazione e checklist."
        ),
        "evidenza": True,
        "tempo": 12,
        "llms_label": "Affitto transitorio Padova 2026",
        "llms_after": (
            "- [Affitti Limena 2026: canoni e quartieri]"
            "(https://righettoimmobiliare.it/blog-affitti-limena-2026)\n"
        ),
        "sitemap_after": (
            "  <url><loc>https://righettoimmobiliare.it/blog-affitti-limena-2026</loc>"
            "<lastmod>2026-07-09</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n"
        ),
    },
    {
        "slug": "blog-rubano-limena-affitto-lavoratori-2026",
        "titolo": "Affitto Rubano e Limena per Lavoratori 2026: Guida Cintura Padova",
        "categoria": "Mercato locazione",
        "hero": "img/blog/blog-loft-aziende-cucina-condivisa-padova-vicenza-2026.webp",
        "summary": (
            "Affitti Rubano e Limena per lavoratori 2026: cintura Padova, pendolari, "
            "settore industriale e collegamenti con housing Edilcassa."
        ),
        "evidenza": True,
        "tempo": 12,
        "llms_label": "Affitto Rubano Limena lavoratori 2026",
        "llms_after": (
            "- [Affitto transitorio Padova 2026]"
            "(https://righettoimmobiliare.it/blog-affitto-transitorio-padova-durata-2026)\n"
        ),
        "sitemap_after": (
            "  <url><loc>https://righettoimmobiliare.it/blog-affitto-transitorio-padova-durata-2026</loc>"
            "<lastmod>2026-07-09</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n"
        ),
    },
]


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
    needle = "  const articoliStatici = [\n"
    if needle not in text:
        raise RuntimeError("Marker articoliStatici non trovato")
    blocks = ""
    for art in reversed(ARTICLES):
        if art["slug"] in text:
            print(f"blog.html: {art['slug']} già presente")
            continue
        entry = {
            "titolo": art["titolo"],
            "categoria": art["categoria"],
            "data": DATE,
            "stato": "pubblicato",
            "immagine_copertina": art["hero"],
            "url_statico": art["slug"],
            "tempo": art["tempo"],
            "autore": "Gino Capon",
            "contenuto": art["summary"],
            "evidenza": art["evidenza"],
        }
        blocks += js_obj(entry, indent=6) + ",\n"
    if blocks:
        path.write_text(text.replace(needle, needle + blocks, 1), encoding="utf-8")
        print(f"blog.html: +{len(ARTICLES)} articoli in testa")


def register_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    for art in ARTICLES:
        if art["slug"] in text:
            print(f"sitemap: {art['slug']} già presente")
            continue
        url_line = (
            f"  <url><loc>https://righettoimmobiliare.it/{art['slug']}</loc>"
            f"<lastmod>{DATE}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n"
        )
        if art["sitemap_after"] not in text:
            raise RuntimeError(f"Marker sitemap per {art['slug']} non trovato")
        text = text.replace(art["sitemap_after"], art["sitemap_after"] + url_line, 1)
        print(f"sitemap: +{art['slug']}")
    path.write_text(text, encoding="utf-8")


def register_llms() -> None:
    path = ROOT / "llms.txt"
    text = path.read_text(encoding="utf-8")
    for art in ARTICLES:
        if art["slug"] in text:
            print(f"llms: {art['slug']} già presente")
            continue
        line = (
            f"- [{art['llms_label']}]"
            f"(https://righettoimmobiliare.it/{art['slug']})\n"
        )
        if art["llms_after"] not in text:
            raise RuntimeError(f"Marker llms per {art['slug']} non trovato")
        text = text.replace(art["llms_after"], art["llms_after"] + line, 1)
        print(f"llms: +{art['slug']}")
    path.write_text(text, encoding="utf-8")


def register_admin() -> None:
    """Allinea admin da blog.html (idempotente su slug già presenti)."""
    import subprocess
    subprocess.run(["python", str(ROOT / "scripts" / "sync_admin_blog_seed.py")], check=True)


def main() -> None:
    register_blog_html()
    register_sitemap()
    register_llms()
    register_admin()
    print("Registrazione batch luglio 2026 completata.")


if __name__ == "__main__":
    main()
