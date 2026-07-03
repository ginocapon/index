# -*- coding: utf-8 -*-
"""
Audit settimanale freschezza contenuti + SKIMM + pagine pillar.
Output: venerdi-contenuti-report.md + metriche per email GitHub Actions.
Eseguire ogni venerdì — cron 05:00 UTC (07:00 CEST).
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import date
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIMM_JSON = ROOT / "TEST-SKILL" / "skimm.json"
REPORT_MD = ROOT / "venerdi-contenuti-report.md"

PILLAR_PAGES: dict[str, dict] = {
    "index.html": {
        "label": "Homepage",
        "min_words": 800,
        "min_blog_links": 3,
        "needs_faq": False,
    },
    "blog.html": {
        "label": "Hub Blog",
        "min_words": 400,
        "min_blog_links": 5,
        "needs_faq": False,
    },
    "agenzia-immobiliare-padova.html": {
        "label": "Agenzia Padova",
        "min_words": 1200,
        "min_blog_links": 2,
        "needs_faq": True,
    },
    "servizio-locazioni.html": {
        "label": "Servizio Locazioni",
        "min_words": 900,
        "min_blog_links": 3,
        "needs_faq": True,
    },
    "servizio-valutazioni.html": {
        "label": "Servizio Valutazioni",
        "min_words": 900,
        "min_blog_links": 2,
        "needs_faq": True,
    },
    "chi-siamo.html": {
        "label": "Chi Siamo",
        "min_words": 600,
        "min_blog_links": 1,
        "needs_faq": True,
    },
    "servizi.html": {
        "label": "Servizi",
        "min_words": 500,
        "min_blog_links": 2,
        "needs_faq": True,
    },
    "immobili.html": {
        "label": "Immobili",
        "min_words": 300,
        "min_blog_links": 0,
        "needs_faq": False,
    },
    "contatti.html": {
        "label": "Contatti",
        "min_words": 200,
        "min_blog_links": 0,
        "needs_faq": True,
    },
    "faq.html": {
        "label": "FAQ",
        "min_words": 400,
        "min_blog_links": 2,
        "needs_faq": True,
    },
}

KEYWORD_OPPORTUNITIES = [
    "affitto-transitorio-padova-durata-massima",
    "imu-seconda-casa-padova-2026",
    "studentato-esu-bando-2026-27",
    "rubano-limena-affitto-lavoratori-cantiere",
    "mestre-affitti-studenti-ca-foscari",
    "surroga-mutuo-conviene-2026-padova",
    "cedolare-secca-vs-irpef-affitto-padova",
    "perizia-gratuita-vendita-padova-tempi",
]

def strip_html(text: str) -> str:
    t = re.sub(r"<script[^>]*>.*?</script>", " ", text, flags=re.S | re.I)
    t = re.sub(r"<style[^>]*>.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def word_count(text: str) -> int:
    return len(strip_html(text).split())


def run_skimm_rebuild() -> tuple[int, int]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_skimm.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode not in (0, 1):
        print(proc.stderr or proc.stdout)
    skimm = json.loads(SKIMM_JSON.read_text(encoding="utf-8"))
    return skimm["count"], len(skimm.get("risks", []))


def analyze_blog(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8", errors="replace")
    slug = path.stem
    wc = word_count(raw)
    has_faq = '"FAQPage"' in raw
    has_righetto_sol = "righetto-sol" in raw or "Cosa può fare Righetto" in raw
    has_freshness = bool(
        re.search(r"ultimo aggiornamento|dateModified|article:modified", raw, re.I)
    )
    has_author = bool(re.search(r"author|Person|linda-righetto|gino-capon", raw, re.I))
    img_count = len(re.findall(r'<img[^>]+src="img/blog/', raw, re.I))
    svg_charts = len(re.findall(r"<svg[^>]*>", raw, re.I))
    return {
        "slug": slug,
        "file": path.name,
        "words": wc,
        "faq": has_faq,
        "righetto_sol": has_righetto_sol,
        "freshness": has_freshness,
        "author": has_author,
        "blog_imgs": img_count,
        "svg_count": svg_charts,
        "thin": wc < 1500,
        "weak": wc < 2500,
    }


def analyze_pillar(filename: str, spec: dict) -> dict:
    path = ROOT / filename
    if not path.exists():
        return {"file": filename, "missing": True}
    raw = path.read_text(encoding="utf-8", errors="replace")
    wc = word_count(raw)
    blog_links = len(
        re.findall(r'href="(?:/)?blog-', raw, re.I)
    )
    has_schema = '"RealEstateAgent"' in raw
    has_faq = '"FAQPage"' in raw
    has_freshness = bool(
        re.search(
            r"ultimo aggiornamento|Ultimo aggiornamento|dateModified|2026",
            raw,
            re.I,
        )
    )
    title = re.search(r"<title>([^<]+)</title>", raw)
    meta = re.search(r'<meta name="description" content="([^"]+)"', raw)
    issues: list[str] = []
    if wc < spec["min_words"]:
        issues.append(f"corpo corto ({wc} parole, min {spec['min_words']})")
    if blog_links < spec["min_blog_links"]:
        issues.append(f"pochi link blog ({blog_links}, min {spec['min_blog_links']})")
    if spec["needs_faq"] and not has_faq:
        issues.append("FAQPage schema mancante")
    if not has_schema:
        issues.append("RealEstateAgent schema mancante")
    if filename in ("index.html", "blog.html") and not has_freshness:
        issues.append("segnale freshness assente in hero/meta")
    return {
        "file": filename,
        "label": spec["label"],
        "words": wc,
        "blog_links": blog_links,
        "faq": has_faq,
        "schema": has_schema,
        "freshness": has_freshness,
        "title": (title.group(1)[:70] if title else "?"),
        "meta_len": len(meta.group(1)) if meta else 0,
        "issues": issues,
        "ok": len(issues) == 0,
    }


def load_skimm() -> dict:
    if not SKIMM_JSON.exists():
        return {"count": 0, "risks": [], "articles": []}
    return json.loads(SKIMM_JSON.read_text(encoding="utf-8"))


def undefined_angles(skimm: dict) -> list[str]:
    return [
        a["slug"]
        for a in skimm.get("articles", [])
        if "Angolo da definire" in a.get("angolo", "")
    ]


def build_report() -> dict:
    warnings = 0
    errors = 0
    actions: list[str] = []
    lines: list[str] = [
        "# Venerdì Contenuti & Freschezza — Righetto Immobiliare",
        f"**Data:** {date.today().isoformat()}",
        "",
        "---",
        "",
        "## 1. SKIMM — Catalogo keyword/intent",
        "",
    ]

    article_count, risk_count = run_skimm_rebuild()
    skimm = load_skimm()
    undefined = undefined_angles(skimm)

    lines.append(f"- **Articoli catalogati:** {article_count}")
    lines.append(f"- **Avvisi SKIMM:** {risk_count}")
    lines.append(f"- **Angoli ancora da definire:** {len(undefined)}")
    lines.append("")

    if undefined:
        warnings += 1
        lines.append("### Angoli da completare (priorità)")
        for slug in undefined[:12]:
            lines.append(f"- `{slug}`")
        if len(undefined) > 12:
            lines.append(f"- … e altri {len(undefined) - 12}")
        lines.append("")
        actions.append(
            f"Completare {min(3, len(undefined))} angoli SKIMM in build_skimm.py"
        )

    lines.extend(["---", "", "## 2. Blog — Qualità e corposità", ""])

    blogs = [analyze_blog(p) for p in sorted(ROOT.glob("blog-*.html"))]
    total = len(blogs)
    thin = [b for b in blogs if b["thin"]]
    no_sol = [b for b in blogs if not b["righetto_sol"]]
    no_faq = [b for b in blogs if not b["faq"]]
    no_fresh = [b for b in blogs if not b["freshness"]]
    weak_imgs = [b for b in blogs if b["blog_imgs"] < 3]

    avg_words = sum(b["words"] for b in blogs) // max(total, 1)

    lines.append(f"| Metrica | Valore |")
    lines.append(f"|---|---|")
    lines.append(f"| Articoli totali | {total} |")
    lines.append(f"| Parole medie | {avg_words} |")
    lines.append(f"| Sotto 1500 parole (thin) | {len(thin)} |")
    lines.append(f"| Senza sezione Righetto | {len(no_sol)} |")
    lines.append(f"| Senza FAQPage schema | {len(no_faq)} |")
    lines.append(f"| Senza timestamp freshness | {len(no_fresh)} |")
    lines.append(f"| Meno di 3 foto blog/ | {len(weak_imgs)} |")
    lines.append("")

    if len(thin) > 15:
        warnings += 1
        actions.append(f"Rafforzare {min(2, len(thin))} articoli thin (<1500 parole)")
    if len(no_sol) > 20:
        warnings += 1
        actions.append(
            "Aggiungere sezione «Cosa può fare Righetto» a 2 articoli pillar prioritari"
        )

    if thin:
        lines.append("### Articoli più sottili (top 8)")
        for b in sorted(thin, key=lambda x: x["words"])[:8]:
            lines.append(f"- `{b['slug']}` — {b['words']} parole")
        lines.append("")

    lines.extend(["---", "", "## 3. Pagine pillar — Google 2026 / E-E-A-T", ""])
    lines.append("| Pagina | Parole | Link blog | Stato |")
    lines.append("|---|---:|---:|---|")

    pillar_results: list[dict] = []
    for fname, spec in PILLAR_PAGES.items():
        r = analyze_pillar(fname, spec)
        pillar_results.append(r)
        if r.get("missing"):
            errors += 1
            lines.append(f"| {fname} | — | — | ❌ file mancante |")
            continue
        status = "✅" if r["ok"] else "⚠️"
        if not r["ok"]:
            warnings += 1
        note = "; ".join(r["issues"]) if r["issues"] else "OK"
        lines.append(
            f"| {r['label']} | {r['words']} | {r['blog_links']} | {status} {note} |"
        )
        if r["issues"]:
            for issue in r["issues"]:
                actions.append(f"{r['label']}: {issue}")

    lines.extend(["", "---", "", "## 4. Keyword libere — opportunità SERP", ""])
    catalog_slugs = {a["slug"] for a in skimm.get("articles", [])}
    catalog_kw = {a["kw_primaria"] for a in skimm.get("articles", [])}
    free_kw: list[str] = []
    for kw in KEYWORD_OPPORTUNITIES:
        slug_guess = f"blog-{kw}"
        if slug_guess not in catalog_slugs and kw not in catalog_kw:
            free_kw.append(kw)
            lines.append(f"- `{kw}` — **ancora libera**")
    if not free_kw:
        lines.append("- Nessuna dalla lista predefinita — generare nuove da fonte OMI/BCE/FIMAA")
    lines.append("")
    if free_kw:
        actions.append(f"Valutare articolo su: {free_kw[0]}")

    lines.extend(["---", "", "## 5. Azioni prioritarie settimana prossima", ""])
    # dedupe actions
    seen_a: set[str] = set()
    unique_actions: list[str] = []
    for a in actions:
        if a not in seen_a:
            seen_a.add(a)
            unique_actions.append(a)
    if not unique_actions:
        unique_actions = [
            "1 articolo nuovo con kw da skimm.md §1.6",
            "Refresh meta/timestamp su 1 pillar",
            "3 internal link da homepage verso blog recente",
        ]
    for i, act in enumerate(unique_actions[:8], 1):
        lines.append(f"{i}. {act}")

    lines.extend(
        [
            "",
            "---",
            "",
            "## 6. Competizione — leve Righetto",
            "",
            "| Leva | Stato | vs competitor |",
            "|---|---|---|",
            f"| Volume blog ({total} articoli) | {'🟢' if total >= 90 else '🟡'} | Tetto Rosso: meno guide originali |",
            f"| Freschezza settimanale | {'🟢' if len(no_fresh) < 20 else '🟡'} | Portali: annunci sì, guide no |",
            f"| GEO (llms.txt) | {'🟢' if (ROOT / 'llms.txt').exists() else '🔴'} | Unico nel mercato locale |",
            f"| Chatbot AI Linda | 🟢 | Unico nel mercato locale |",
            f"| Sezione Righetto negli articoli | {'🟡' if no_sol else '🟢'} | Differenziatore conversione |",
            "",
            "> Report generato da `scripts/venerdi-contenuti-freschezza.py`",
            "> Cron: venerdì 07:00 CEST — email a info@righettoimmobiliare.it",
        ]
    )

    health = max(0, min(100, 100 - errors * 8 - warnings * 3))

    report_text = "\n".join(lines) + "\n"
    REPORT_MD.write_text(report_text, encoding="utf-8")

    return {
        "health": health,
        "errors": errors,
        "warnings": warnings,
        "articles": total,
        "skimm_risks": risk_count,
        "undefined_angles": len(undefined),
        "thin_articles": len(thin),
        "no_righetto_sol": len(no_sol),
        "free_keywords": len(free_kw),
        "actions": unique_actions[:5],
        "report": report_text,
    }


def write_github_output(metrics: dict) -> None:
    gh_out = os.environ.get("GITHUB_OUTPUT")
    if not gh_out:
        return
    with open(gh_out, "a", encoding="utf-8") as f:
        for key in (
            "health",
            "errors",
            "warnings",
            "articles",
            "skimm_risks",
            "undefined_angles",
            "thin_articles",
            "no_righetto_sol",
            "free_keywords",
        ):
            f.write(f"{key}={metrics[key]}\n")
        f.write("success=true\n")


def main() -> int:
    metrics = build_report()
    try:
        print(metrics["report"])
    except UnicodeEncodeError:
        print(metrics["report"].encode("ascii", errors="replace").decode("ascii"))
    print(
        f"\nOK: salute {metrics['health']}% | "
        f"{metrics['articles']} blog | {metrics['warnings']} avvisi | "
        f"{metrics['errors']} errori"
    )
    write_github_output(metrics)
    return 1 if metrics["errors"] > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
