#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Memoria visiva articoli recenti — struttura, immagini, grafiche (§16-QUATER)."""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG_HTML = ROOT / "blog.html"
OUT = ROOT / "data" / "editorial-visual-memory.json"
WINDOW = 15

STRUCTURE_TYPES = (
    "ANALITICA",
    "GUIDA",
    "NOTIZIA_IMPATTO",
    "DOMANDA_RISPOSTA",
    "CONFRONTO",
    "TERRITORIALE",
    "MISTO",
)

# Segnali H2 per classificazione struttura
STRUCTURE_SIGNALS: dict[str, list[str]] = {
    "NOTIZIA_IMPATTO": ["cosa è successo", "cosa cambia", "impatto", "novità", "aggiornamento"],
    "GUIDA": ["passaggi", "come fare", "guida", "errori", "checklist", "passo"],
    "CONFRONTO": ["confronto", "prima e dopo", "vs ", " rispetto a", "differenz"],
    "TERRITORIALE": ["padova", "veneto", "limena", "provincia", "locale", "cintura"],
    "DOMANDA_RISPOSTA": ["domande frequenti", "faq", "in sintesi", "risposta"],
    "ANALITICA": ["analisi", "dati", "scenario", "prospettiv", "mercato", "trend"],
}


def _field(block: str, name: str) -> str:
    for pat in (
        rf'"{name}":\s*"([^"]*)"',
        rf"{name}:\s*'([^']*)'",
    ):
        m = re.search(pat, block)
        if m:
            return m.group(1)
    return ""


def extract_slugs() -> list[str]:
    raw = BLOG_HTML.read_text(encoding="utf-8", errors="replace")
    start = raw.find("const articoliStatici = [")
    end = raw.find("\n  ];", start)
    if start < 0:
        return []
    section = raw[start:end]
    slugs: list[str] = []
    for m in re.finditer(r'url_statico:\s*["\'](blog-[^"\']+)["\']', section):
        s = m.group(1)
        if s not in slugs and s != "blog-articolo":
            slugs.append(s)
    return slugs[:WINDOW]


def file_hash(path: Path) -> str:
    if not path.is_file():
        return ""
    h = hashlib.md5()
    h.update(path.read_bytes()[:65536])
    return h.hexdigest()


def classify_structure(h2_texts: list[str], has_faq: bool) -> str:
    blob = " ".join(h2_texts).lower()
    scores: dict[str, int] = {k: 0 for k in STRUCTURE_TYPES if k != "MISTO"}
    for stype, keys in STRUCTURE_SIGNALS.items():
        for k in keys:
            if k in blob:
                scores[stype] += 1
    if has_faq:
        scores["DOMANDA_RISPOSTA"] += 1
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    if not ranked or ranked[0][1] == 0:
        return "GUIDA"
    if ranked[0][1] == ranked[1][1] if len(ranked) > 1 else False:
        return "MISTO"
    return ranked[0][0]


def analyze_article(slug: str) -> dict | None:
    path = ROOT / f"{slug}.html"
    if not path.is_file():
        return None
    raw = path.read_text(encoding="utf-8", errors="replace")
    h2s = [
        re.sub(r"<[^>]+>", " ", m).strip()
        for m in re.findall(r"<h2[^>]*>([\s\S]*?)</h2>", raw, re.I)
    ]
    h2_ids = re.findall(r'<h2[^>]*id=["\']([^"\']+)["\']', raw, re.I)
    imgs = list(dict.fromkeys(re.findall(r'src=["\'](img/blog/[^"\']+\.webp)["\']', raw, re.I)))
    charts = re.findall(r'class="chart-wrap"[^>]*aria-label=["\']([^"\']*)["\']', raw, re.I)
    if not charts:
        charts = re.findall(r"<title>([^<]{10,80})</title>", raw)
    tables = len(re.findall(r"<table\b", raw, re.I))
    lists = len(re.findall(r"<(?:ul|ol)\b", raw, re.I))
    has_faq = "FAQPage" in raw or "domande frequenti" in raw.lower()
    img_hashes = {img: file_hash(ROOT / img) for img in imgs}

    return {
        "slug": slug,
        "structure_type": classify_structure(h2s, has_faq),
        "h2_sequence": h2_ids[:12] or [h[:40] for h in h2s[:12]],
        "h2_count": len(h2s),
        "images": imgs,
        "image_hashes": img_hashes,
        "chart_labels": charts[:6],
        "chart_count": len(re.findall(r'class="chart-wrap"', raw, re.I)),
        "table_count": tables,
        "list_count": lists,
        "has_faq_block": has_faq,
    }


def saturation_report(articles: list[dict]) -> dict:
    window = articles[:8]
    struct: dict[str, int] = {}
    for a in window:
        st = a.get("structure_type", "MISTO")
        struct[st] = struct.get(st, 0) + 1
    return {k: v for k, v in struct.items() if v >= 2}


def main() -> int:
    slugs = extract_slugs()
    articles = [a for s in slugs if (a := analyze_article(s))]
    sat = saturation_report(articles)

    # Mappa hash → slug (riuso immagini)
    hash_to_slugs: dict[str, list[str]] = {}
    for a in articles:
        for img, ih in a.get("image_hashes", {}).items():
            if ih:
                hash_to_slugs.setdefault(ih, []).append(a["slug"])

    reuse = {h: slugs for h, slugs in hash_to_slugs.items() if len(set(slugs)) > 1}

    doc = {
        "updated": datetime.now().strftime("%Y-%m-%d"),
        "skill_ref": "TEST-SKILL/skill-editoriale-visivo.md §16-QUATER",
        "window_size": WINDOW,
        "structure_types": list(STRUCTURE_TYPES),
        "structure_saturation_last_8": sat,
        "image_hash_reuse_detected": {
            h: slugs for h, slugs in list(reuse.items())[:20]
        },
        "recent_articles": articles,
        "approval_visual": [
            "Struttura diversa dagli ultimi se stessa tipologia ≥2 volte?",
            "Immagini path unici e hash non già usati in altri articoli recenti?",
            "Grafiche con layout/aria-label diversi dagli ultimi?",
            "Sequenza H2 non clone del batch precedente?",
        ],
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK {OUT.relative_to(ROOT)} — {len(articles)} articoli")
    if sat:
        print("Strutture saturate (ultimi 8):")
        for k, v in sat.items():
            print(f"  {k}: {v}")
    if reuse:
        print(f"ATTENZIONE: {len(reuse)} hash immagine condivisi tra articoli (bonifica/IA ex novo)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
