#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera/aggiorna data/editorial-memory.json — memoria sostanziale articoli recenti (§16-TER)."""
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG_HTML = ROOT / "blog.html"
OUT = ROOT / "data" / "editorial-memory.json"
WINDOW = 20
SATURATION_WINDOW = 8
SATURATION_THRESHOLD = 2

# Aree sostanziali — non solo keyword SEO
AREAS: dict[str, list[str]] = {
    "VALORE_MERCATO": [
        "prezzi-case", "prezzi-padova", "mercato-immobiliare", "quotazioni",
        "omi-istat", "housing-market", "domanda-residenziale", "offerta-stock",
        "conviene-vendere", "valutaz", "worth", "outlook-living", "prospettive-mercato",
        "prospettive-mercato", "previsioni-immobiliari", "patrimonio-casa", "stock-vendita",
        "prezzi case", "mercato residenziale", "mercato immobiliare",
    ],
    "AFFITTI_CANONI": [
        "affitt", "canone", "locazion", "rental", "caro-affitti", "canoni-fimaa",
        "affitto-studenti", "affitto-transitorio", "affitto-breve", "rendimento-affitto",
    ],
    "MUTUI_TASSI": [
        "mutuo", "euribor", "tassi", "bce", "barometro-mutui", "surroga", "crif",
        "mutui-selettivi", "geopolitica-ucraina-prezzi-mutui", "mutui piu selettivi",
    ],
    "NORMATIVA_FISCALE": [
        "registro-contratti", "visura-catastale", "canone-concordato", "documenti-vendita",
        "documenti-compravendita", "rogito", "tasse-vendita", "caparra", "mandato-esclusivo",
        "bonus-edilizi", "case-green", "direttiva-case-green", "condono-edilizio",
        "registro contratti",
    ],
    "ACQUISTO_PRIMO_CASA": [
        "prima-casa", "under-36", "under-35", "consap", "agevolazioni-prima-casa",
        "comprare-casa", "guida-acquisto", "checklist-verifiche", "compromesso",
        "acquisto casa", "acquisto padova",
    ],
    "VENDITA_PROCESSO": [
        "vendere-casa", "vendita-immobiliare", "tempi-vendita", "costi-vendere",
        "home-staging", "5-errori-visita", "vendere casa",
    ],
    "AGENZIA_SERVIZI": [
        "agenzia-immobiliare", "5-domande-appuntamento", "scegliere-agenzia",
        "servizi-padova", "gruppo-immobiliare-righetto", "drone-sopralluoghi",
        "sopralluoghi-drone",
    ],
    "LOCALE_LIMENA": [
        "limena", "rubano-limena", "vigonza-rubano", "rubano",
    ],
    "GUIDA_LEXICO": [
        "gergo-immobiliare", "gergo", "lexico", "glossario",
    ],
    "TREND_ABITATIVO": [
        "coliving", "loft-aziende", "student-rentals", "coliving",
    ],
    "COMPRAVENDITE_DATI": [
        "compravendite", "agenzia-entrate", "sondaggio-bancaditalia",
    ],
    "INVESTIMENTO": [
        "investiment", "rendimento-affitto", "real-estate", "summit",
    ],
}


def classify(text: str) -> tuple[str, list[str]]:
    low = text.lower()
    scores: Counter[str] = Counter()
    for area, keys in AREAS.items():
        for k in keys:
            if k in low:
                scores[area] += 1
    if not scores:
        return "ALTRO", []
    ranked = scores.most_common()
    primary = ranked[0][0]
    secondary = [a for a, _ in ranked[1:3] if a != primary]
    return primary, secondary


def _field(block: str, name: str) -> str:
    for pat in (
        rf'"{name}":\s*"([^"]*)"',
        rf'"{name}":\s*\'([^\']*)\'',
        rf"{name}:\s*'([^']*)'",
        rf'{name}:\s*"([^"]*)"',
    ):
        m = re.search(pat, block)
        if m:
            return m.group(1)
    return ""


def extract_articles() -> list[dict]:
    raw = BLOG_HTML.read_text(encoding="utf-8", errors="replace")
    start = raw.find("const articoliStatici = [")
    if start < 0:
        return []
    end = raw.find("\n  ];", start)
    if end < 0:
        return []
    section = raw[start:end]
    blocks = re.split(r"\n    \},?\n", section)

    queue_meta: dict[str, dict] = {}
    qpath = ROOT / "data" / "editorial-queue.json"
    if qpath.is_file():
        qdata = json.loads(qpath.read_text(encoding="utf-8"))
        for it in qdata.get("items", []):
            slug = it.get("slug", "")
            if slug:
                queue_meta[slug] = it

    articles: list[dict] = []
    for block in blocks:
        slug = _field(block, "url_statico")
        if not slug or slug == "blog-articolo":
            continue
        titolo = _field(block, "titolo")
        data = _field(block, "data")
        contenuto = _field(block, "contenuto")
        categoria = _field(block, "categoria")
        path = ROOT / f"{slug}.html"
        meta = ""
        h1 = ""
        if path.is_file():
            html = path.read_text(encoding="utf-8", errors="replace")
            mm = re.search(r'<meta name="description" content="([^"]+)"', html)
            if mm:
                meta = mm.group(1)
            mm = re.search(r"<h1[^>]*>([\s\S]*?)</h1>", html, re.I)
            if mm:
                h1 = re.sub(r"<[^>]+>", " ", mm.group(1)).strip()
        blob = f"{slug} {titolo} {categoria} {contenuto} {meta} {h1}"
        primary, secondary = classify(blob)
        qm = queue_meta.get(slug, {})
        main_q = qm.get("main_question") or _guess_question(primary, titolo)
        articles.append(
            {
                "slug": slug,
                "title": titolo,
                "published_date": data,
                "substantive_area": qm.get("substantive_area") or primary,
                "secondary_areas": secondary,
                "main_question": main_q,
                "geo": "Padova/Veneto" if "limena" in blob.lower() or "padova" in blob.lower() else "Padova",
                "editorial_type": qm.get("editorial_type", ""),
            }
        )
    return articles[:WINDOW]


def _guess_question(area: str, title: str) -> str:
    templates = {
        "VALORE_MERCATO": "Quanto vale / come si muove il mercato?",
        "AFFITTI_CANONI": "Quanto costa affittare e come funzionano i canoni?",
        "MUTUI_TASSI": "Quali tassi e condizioni di mutuo?",
        "NORMATIVA_FISCALE": "Quali obblighi normativi e documenti?",
        "ACQUISTO_PRIMO_CASA": "Come acquistare prima casa con agevolazioni?",
        "VENDITA_PROCESSO": "Come vendere casa e quali passi?",
        "AGENZIA_SERVIZI": "Come scegliere agenzia e servizi?",
        "LOCALE_LIMENA": "Cosa sapere su Limena/cintura?",
        "GUIDA_LEXICO": "Cosa significano i termini immobiliari?",
        "TREND_ABITATIVO": "Quali modelli abitativi emergenti?",
        "COMPRAVENDITE_DATI": "Cosa dicono i dati ufficiali sulle transazioni?",
        "INVESTIMENTO": "Conviene investire in immobili nel contesto attuale?",
    }
    return templates.get(area, title[:80])


def saturation(recent: list[dict]) -> dict[str, int]:
    window = recent[:SATURATION_WINDOW]
    c: Counter[str] = Counter()
    for a in window:
        c[a["substantive_area"]] += 1
    return dict(c.most_common())


def main() -> int:
    articles = extract_articles()
    sat = saturation(articles)
    saturated = {k: v for k, v in sat.items() if v >= SATURATION_THRESHOLD}

    doc = {
        "updated": datetime.now().strftime("%Y-%m-%d"),
        "skill_ref": "TEST-SKILL/skill-editoriale-visivo.md §16-TER",
        "window_size": WINDOW,
        "saturation_window": SATURATION_WINDOW,
        "saturation_threshold": SATURATION_THRESHOLD,
        "areas_taxonomy": list(AREAS.keys()) + ["ALTRO"],
        "saturation_current": saturated,
        "saturation_counts_last_8": sat,
        "recent_articles": articles,
        "approval_questions": [
            "Aggiunge nuovo argomento/informazione/conseguenza rispetto ai recenti?",
            "Un lettore abituale lo percepirebbe come contenuto nuovo?",
            "Se area gia trattata: cosa e cambiato dall'ultima volta (dato/norma/contesto)?",
        ],
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK {OUT.relative_to(ROOT)} — {len(articles)} articoli in memoria")
    if saturated:
        print("Aree saturate (ultimi 8):")
        for k, v in saturated.items():
            print(f"  {k}: {v} articoli — preferire altra area salvo update_reason")
    else:
        print("Nessuna area oltre soglia saturazione negli ultimi 8.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
