#!/usr/bin/env python3
"""Sincronizza _blogSeedArticles in admin.html con articoliStatici in blog.html."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CATEGORY_EMOJI = {
    "Mercato locazione": "🔑",
    "Mercato locale": "🏘️",
    "Affitti": "🏠",
    "Consigli acquisto": "🏡",
    "Guida alla vendita": "🏷️",
    "Normativa": "⚖️",
    "Fisco": "🧾",
    "Mercato immobiliare": "📊",
    "Vita d'Agenzia": "💼",
    "Finanziamenti": "🏦",
    "Mutui e credito": "🏦",
    "Economia": "🌐",
    "Guida acquirenti": "🔍",
    "Fisco e ristrutturazioni": "🏗️",
    "Mercato e sostenibilità": "🌿",
    "Investimenti": "📈",
    "Nuove Costruzioni": "🏗️",
    "Analisi": "📉",
    "Mercato": "📑",
    "Mercato e famiglie": "🏛️",
}


def extract_blog_statici(text: str) -> list[dict]:
    m = re.search(r"const articoliStatici = \[([\s\S]*?)\n  \];", text)
    if not m:
        raise RuntimeError("articoliStatici non trovato in blog.html")
    block = m.group(1)
    # oggetti JS con chiavi quoted
    objs = re.findall(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", block)
    out: list[dict] = []
    for raw in objs:
        try:
            d = json.loads(raw.replace("'", '"'))
            if d.get("url_statico"):
                out.append(d)
        except json.JSONDecodeError:
            slug = re.search(r'"url_statico"\s*:\s*"([^"]+)"', raw)
            if slug:
                tit = re.search(r'"titolo"\s*:\s*"([^"]*)"', raw)
                cat = re.search(r'"categoria"\s*:\s*"([^"]*)"', raw)
                dat = re.search(r'"data"\s*:\s*"([^"]*)"', raw)
                img = re.search(r'"immagine_copertina"\s*:\s*"([^"]*)"', raw)
                tmp = re.search(r'"tempo"\s*:\s*(\d+)', raw)
                aut = re.search(r'"autore"\s*:\s*"([^"]*)"', raw)
                cnt = re.search(r'"contenuto"\s*:\s*"([^"]*)"', raw)
                ev = re.search(r'"evidenza"\s*:\s*(true|false)', raw)
                out.append({
                    "titolo": tit.group(1) if tit else "",
                    "categoria": cat.group(1) if cat else "Mercato locale",
                    "data": dat.group(1) if dat else "2026-01-01",
                    "stato": "pubblicato",
                    "immagine_copertina": img.group(1) if img else "img/og-default.webp",
                    "url_statico": slug.group(1),
                    "tempo": int(tmp.group(1)) if tmp else 10,
                    "autore": aut.group(1) if aut else "Gino Capon",
                    "contenuto": cnt.group(1) if cnt else "",
                    "evidenza": ev.group(1) == "true" if ev else False,
                })
    return out


def extract_admin_slugs(text: str) -> set[str]:
    return set(re.findall(r"url_statico:\s*'([^']+)'", text))


def to_admin_entry(d: dict) -> str:
    cat = d.get("categoria", "Mercato locale")
    emoji = CATEGORY_EMOJI.get(cat, "📄")
    titolo = d["titolo"].replace("'", "\\'")
    contenuto = d.get("contenuto", "")
    if contenuto and not contenuto.startswith("<"):
        contenuto = f"<p>{contenuto}</p>"
    contenuto = contenuto.replace("'", "\\'")
    ev = "true" if d.get("evidenza") else "false"
    data = d.get("data", "2026-01-01")
    return (
        f"  {{ titolo: \"{titolo}\", categoria: \"{cat}\", data: '{data}', "
        f"tempo: {d.get('tempo', 10)}, stato: 'pubblicato', autore: '{d.get('autore', 'Gino Capon')}', "
        f"emoji: '{emoji}', immagine_copertina: '{d.get('immagine_copertina', 'img/og-default.webp')}', "
        f"url_statico: '{d['url_statico']}', contenuto: \"{contenuto}\", evidenza: {ev}, "
        f"data_pubblicazione: '{data}' }},"
    )


def main() -> None:
    blog_path = ROOT / "blog.html"
    admin_path = ROOT / "admin.html"
    blog_text = blog_path.read_text(encoding="utf-8")
    admin_text = admin_path.read_text(encoding="utf-8")

    statici = extract_blog_statici(blog_text)
    admin_slugs = extract_admin_slugs(admin_text)
    missing = [d for d in statici if d["url_statico"] not in admin_slugs]

    if not missing:
        print("admin.html: già allineato con blog.html")
        return

    # ordine blog.html (più recente in testa) — missing in same order as blog
    entries = "\n".join(to_admin_entry(d) for d in missing)
    marker = "const _blogSeedArticles = [\n"
    if marker not in admin_text:
        raise RuntimeError("Marker _blogSeedArticles non trovato")
    admin_text = admin_text.replace(marker, marker + entries + "\n", 1)
    admin_path.write_text(admin_text, encoding="utf-8")
    print(f"admin.html: +{len(missing)} seed")
    for d in missing:
        print(f"  + {d['url_statico']}")


if __name__ == "__main__":
    main()
