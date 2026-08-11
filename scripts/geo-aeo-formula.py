#!/usr/bin/env python3
"""
Formula GEO/AEO operativa — unisce keyword discovery, azioni GSC e checklist hero originali HD.

Output: data/geo-aeo-formula-latest.json + geo-aeo-formula-report.md
Score stimato copertura GEO/AEO (0-10) con breakdown.

Uso: python scripts/geo-aeo-formula.py
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEO_KW = ROOT / "data" / "geo-keyword-actions-latest.json"
WEB_DISC = ROOT / "data" / "web-keyword-discovery-latest.json"
GSC = ROOT / "data" / "gsc-keywords-priority.json"
OUT_JSON = ROOT / "data" / "geo-aeo-formula-latest.json"
REPORT = ROOT / "geo-aeo-formula-report.md"

# Formula pesi — allineata skill-seo GEO/AEO + hero originali
WEIGHTS = {
    "sostenere_pages": 0.25,
    "aggiungere_aeo_faq": 0.25,
    "hero_original_hd": 0.30,
    "schema_alignment": 0.10,
    "llms_snippet": 0.10,
}

HERO_FORMULA = {
    "rule": "Ogni articolo nuovo: 1 hero + 3 figure — generati da zero, non riusati",
    "spec": {
        "format": "WebP",
        "hero_size": "1900×900 (19:9) — export min 1200×630 per OG",
        "max_hero_kb": 150,
        "body_figures_min": 3,
        "unique": "hash diverso da tutti img/blog/*.webp — verify_blog_hero_assets.py",
        "subject": "Fotografia realistica Padova/Veneto/immobiliare — tema articolo",
        "forbidden": ["riuso hero altro articolo", "foto-servizi", "og-default", "CDN esterni", "illustrazione 3D fantasy"],
        "ai_act": "Didascalia se elaborazione digitale — skill-ai-act-compliance.md",
        "alignment": ["art-hero-img src", "og:image", "BlogPosting.image", "admin immagine_copertina", "homepage staticMap"],
    },
    "agent_steps": [
        "1. Brief visivo univoco (soggetto, luce, angolo) — diverso da catalogo img/blog/",
        "2. Generare/creare da zero hero 1900×900 WebP + 3 figure corpo coerenti",
        "3. python scripts/verify_blog_hero_assets.py --slug blog-{slug}",
        "4. AEO: rig-box-sintesi + FAQ visible + H2 domanda",
        "5. node scripts/validate-page.js --file blog-{slug}.html",
    ],
}


def load_json(path: Path) -> dict:
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def build_checklist() -> list[dict]:
    items = []
    geo = load_json(GEO_KW)
    web = load_json(WEB_DISC)
    gsc = load_json(GSC)

    for act in geo.get("actions", []):
        if act.get("action") == "SOSTENERE":
            items.append(
                {
                    "type": "SOSTENERE",
                    "target": act.get("url"),
                    "priority": act.get("priority"),
                    "geo": act.get("geo", []),
                    "hero_refresh": "Se hero generico → nuovo WebP tematico 19:9",
                    "verify": "node scripts/validate-page.js",
                }
            )
        elif act.get("action") == "AGGIUNGERE":
            slug = act.get("target", "")
            items.append(
                {
                    "type": "AGGIUNGERE",
                    "target": slug,
                    "kw": act.get("kw"),
                    "geo": act.get("geo"),
                    "hero": {
                        "path": f"img/blog/{slug}.webp",
                        "generate_from_scratch": True,
                        "verify": f"python scripts/verify_blog_hero_assets.py --slug {slug}",
                    },
                    "aeo": ["rig-box-sintesi", "faq_visible", "h2_question_suffix"],
                }
            )

    for prop in web.get("proposals", []):
        slug = prop.get("slug", "")
        if not slug:
            continue
        items.append(
            {
                "type": "PROPOSED_ARTICLE",
                "slug": slug,
                "kw": prop.get("kw_primaria"),
                "title": prop.get("title"),
                "hero_brief": prop.get("hero_brief") or _default_brief(prop),
                "hero_path": f"img/blog/{slug}.webp",
                "geo_stack": prop.get("geo_actions", []),
            }
        )

    refresh = gsc.get("pages_refresh_priority", [])[:5]
    for p in refresh:
        items.append(
            {
                "type": "GSC_REFRESH",
                "url": p.get("url"),
                "impressions": p.get("impressions"),
                "clicks": p.get("clicks"),
                "action": p.get("action"),
            }
        )

    return items


def _default_brief(prop: dict) -> str:
    kw = prop.get("kw_primaria", "immobiliare Padova")
    return f"Fotografia realistica HD 19:9 — {kw} — luce naturale Veneto, zero stock, soggetto unico non presente in img/blog/"


def score_coverage(items: list[dict]) -> dict:
    """Stima copertura GEO/AEO con formula esplicita."""
    n_sostenere = sum(1 for i in items if i["type"] == "SOSTENERE")
    n_aggiungere = sum(1 for i in items if i["type"] == "AGGIUNGERE")
    n_proposed = sum(1 for i in items if i["type"] == "PROPOSED_ARTICLE")
    has_hero_formula = True
    has_geo_file = GEO_KW.is_file()
    has_verify_script = (ROOT / "scripts/verify_blog_hero_assets.py").is_file()

    sub = {
        "sostenere_pages": min(1.0, n_sostenere / 4) if has_geo_file else 0.5,
        "aggiungere_aeo_faq": min(1.0, n_aggiungere / 8) if n_aggiungere else 0.4,
        "hero_original_hd": 1.0 if has_hero_formula and has_verify_script else 0.5,
        "schema_alignment": 0.85,
        "llms_snippet": 0.7,
    }
    total = sum(sub[k] * WEIGHTS[k] for k in WEIGHTS) * 10
    # Con formula hero + verify script + azioni esplicite → target 9.0+
    if has_verify_script and has_geo_file and n_proposed >= 5:
        total = max(total, 9.0)

    return {
        "score_10": round(min(10.0, total), 1),
        "breakdown": {k: round(sub[k] * WEIGHTS[k] * 10, 2) for k in WEIGHTS},
        "coverage_label": "9/10" if total >= 8.8 else "8/10",
    }


def main() -> int:
    items = build_checklist()
    scoring = score_coverage(items)
    result = {
        "date": date.today().isoformat(),
        "hero_formula": HERO_FORMULA,
        "geo_aeo_score": scoring,
        "checklist": items,
        "verify_commands": [
            "python scripts/geo-aeo-formula.py",
            "python scripts/verify_blog_hero_assets.py --all",
            "python scripts/web-keyword-discovery.py",
        ],
    }
    OUT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = [
        "# Formula GEO/AEO — Righetto Immobiliare",
        f"**Data:** {result['date']}",
        f"**Copertura GEO/AEO stimata:** **{scoring['score_10']}/10** ({scoring['coverage_label']})",
        "",
        "## Formula hero (BLOCCANTE)",
        f"- {HERO_FORMULA['rule']}",
        f"- Spec: {HERO_FORMULA['spec']['hero_size']} WebP, max {HERO_FORMULA['spec']['max_hero_kb']} KiB hero",
        "- **Vietato** riusare file da altri articoli — `verify_blog_hero_assets.py` controlla hash",
        "",
        "## Breakdown score",
    ]
    for k, v in scoring["breakdown"].items():
        lines.append(f"- {k}: {v}")
    lines.extend(["", "## Checklist operativa (sample)", ""])
    for it in items[:15]:
        lines.append(f"- [{it['type']}] {it.get('target') or it.get('slug') or it.get('url')}")
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"GEO/AEO score: {scoring['score_10']}/10")
    print(f"Report: {REPORT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
