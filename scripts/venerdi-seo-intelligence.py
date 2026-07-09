#!/usr/bin/env python3
"""
Report settimanale SEO/GEO intelligence — venerdì.
Valuta ogni pagina blog/pillar/zona con PAGE SCORE e decide:
  SOSTENERE (refresh) | AGGIUNGERE (nuovo) | CONSOLIDARE (link/redirect) | GEO (AEO)

Output: venerdi-seo-intelligence-report.md (+ append opzionale a venerdi-contenuti-report.md)
Dati GSC: data/gsc-keywords-priority.json + CSV opzionali gsc-export-*.csv
"""
from __future__ import annotations

import csv
import json
import os
import re
from datetime import date
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GSC_JSON = ROOT / "data" / "gsc-keywords-priority.json"
GSC_QUERIES_CSV = ROOT / "data" / "gsc-export-queries.csv"
GSC_PAGES_CSV = ROOT / "data" / "gsc-export-pages.csv"
PROBE_JSON = ROOT / "data" / "url-probe-latest.json"
SKIMM_JSON = ROOT / "TEST-SKILL" / "skimm.json"
REPORT_MD = ROOT / "venerdi-seo-intelligence-report.md"
MERGE_INTO = ROOT / "venerdi-contenuti-report.md"

# Pesi PAGE SCORE (0-100) — vedi TEST-SKILL/skill-seo.md §11
WEIGHTS = {
    "gsc_potential": 25,
    "content_depth": 20,
    "freshness_geo": 20,
    "internal_mesh": 15,
    "keyword_fit": 20,
}


def strip_html(text: str) -> str:
    t = re.sub(r"<script[^>]*>.*?</script>", " ", text, flags=re.S | re.I)
    t = re.sub(r"<style[^>]*>.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", unescape(t)).strip()


def word_count(raw: str) -> int:
    return len(strip_html(raw).split())


def load_gsc() -> dict:
    if GSC_JSON.exists():
        return json.loads(GSC_JSON.read_text(encoding="utf-8"))
    return {}


def parse_gsc_csv(path: Path, key_field: str) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            q = row.get(key_field) or row.get("Query principale") or row.get("Pagine principali") or ""
            if not q:
                continue
            clicks = int(float(row.get("Clic") or row.get("Clicks") or 0))
            imp = int(float(row.get("Impressioni") or row.get("Impressions") or 0))
            rows.append({"key": q.strip(), "clicks": clicks, "impressions": imp})
    return rows


def path_from_url(url: str) -> str:
    u = url.replace("https://www.righettoimmobiliare.it", "").replace(
        "https://righettoimmobiliare.it", ""
    )
    return u.split("#")[0].rstrip("/") or "/"


def analyze_page(path: Path, gsc_pages: dict[str, dict]) -> dict:
    raw = path.read_text(encoding="utf-8", errors="replace")
    slug = path.stem
    rel = "/" + slug if path.suffix == ".html" and slug != "index" else "/"
    if slug == "index":
        rel = "/"

    title_m = re.search(r"<title>([^<]+)</title>", raw)
    meta_m = re.search(r'<meta name="description" content="([^"]+)"', raw)
    title = title_m.group(1) if title_m else ""
    meta = meta_m.group(1) if meta_m else ""
    wc = word_count(raw)
    has_faq = '"FAQPage"' in raw
    has_sol = "righetto-sol" in raw or "Cosa può fare Righetto" in raw
    has_fresh = bool(re.search(r"dateModified|Ultimo aggiornamento|ultimo aggiornamento", raw, re.I))
    has_aeo_box = bool(re.search(r"class=\"aeo-|rig-box-sintesi|in sintesi", raw, re.I))
    blog_links = len(re.findall(r'href="(?:/)?blog-', raw, re.I))
    zona_links = len(re.findall(r'href="(?:/)?zona-', raw, re.I))
    llms_hit = slug in (ROOT / "llms.txt").read_text(encoding="utf-8", errors="replace") if (ROOT / "llms.txt").exists() else False

    gsc = gsc_pages.get(rel, {})
    imp = gsc.get("impressions", 0)
    clk = gsc.get("clicks", 0)
    ctr = (clk / imp * 100) if imp else 0

    # --- sub-scores 0-100 ---
    if imp >= 50 and clk == 0:
        gsc_score = 95
    elif imp >= 20 and ctr < 2:
        gsc_score = 80
    elif imp >= 10:
        gsc_score = 60
    elif clk >= 5:
        gsc_score = 70
    else:
        gsc_score = 40

    depth_score = min(100, int(wc / 25)) if wc else 0
    if wc >= 2500:
        depth_score = 100
    elif wc >= 1500:
        depth_score = 75

    geo_score = sum([has_faq * 35, has_sol * 25, has_fresh * 25, has_aeo_box * 15])
    mesh_score = min(100, blog_links * 12 + zona_links * 8)

    kw_fit = 50
    title_l = title.lower()
    if "limena" in title_l and "affitt" not in title_l and slug.startswith("zona-"):
        kw_fit = 30
    if "rendimento" in title_l or "affitto" in title_l:
        kw_fit = 75

    page_score = int(
        gsc_score * WEIGHTS["gsc_potential"] / 100
        + depth_score * WEIGHTS["content_depth"] / 100
        + geo_score * WEIGHTS["freshness_geo"] / 100
        + mesh_score * WEIGHTS["internal_mesh"] / 100
        + kw_fit * WEIGHTS["keyword_fit"] / 100
    )

    if imp >= 30 and clk == 0:
        decision = "SOSTENERE"
        reason = f"{imp} imp, 0 click — ottimizzare title/meta/snippet"
    elif imp >= 10 and ctr < 3 and wc >= 1500:
        decision = "SOSTENERE"
        reason = "CTR basso su contenuto già corposo"
    elif wc < 1200 and slug.startswith("blog-"):
        decision = "SOSTENERE"
        reason = f"contenuto thin ({wc} parole)"
    elif not has_faq and slug.startswith(("blog-", "zona-", "servizio-", "agenzia")):
        decision = "GEO"
        reason = "manca FAQPage / box AEO"
    elif page_score >= 75 and clk >= 3:
        decision = "MANTENERE"
        reason = "performa — solo freshness mensile"
    else:
        decision = "MONITORARE"
        reason = "nessun trigger critico"

    return {
        "path": rel,
        "file": path.name,
        "slug": slug,
        "title": title[:55],
        "words": wc,
        "impressions": imp,
        "clicks": clk,
        "ctr": round(ctr, 1),
        "page_score": page_score,
        "decision": decision,
        "reason": reason,
        "faq": has_faq,
        "fresh": has_fresh,
        "llms": llms_hit,
    }


def match_keyword_gaps(gsc_data: dict, catalog_slugs: set[str]) -> list[dict]:
    gaps = list(gsc_data.get("keyword_gaps_new", []))
    growth = gsc_data.get("queries_growth", [])
    for q in growth:
        if q.get("impressions", 0) < 8:
            continue
        kw = q["q"]
        tokens = kw.replace(" ", "-")
        guess = f"blog-{tokens}"
        if guess not in catalog_slugs and not any(g["kw"] == kw for g in gaps):
            gaps.append(
                {
                    "kw": kw,
                    "slug_proposto": guess[:60],
                    "rationale": f"GSC: {q['impressions']} imp, {q.get('clicks', 0)} click",
                }
            )
    return gaps[:8]


def build_report() -> str:
    gsc_data = load_gsc()
    csv_queries = parse_gsc_csv(GSC_QUERIES_CSV, "Query")
    csv_pages = parse_gsc_csv(GSC_PAGES_CSV, "Pagina")

    gsc_pages: dict[str, dict] = {}
    for p in gsc_data.get("pages_refresh_priority", []) + gsc_data.get("pages_winners", []):
        gsc_pages[path_from_url(p["url"])] = p
    for p in csv_pages:
        gsc_pages[path_from_url(p["key"])] = {
            "clicks": p["clicks"],
            "impressions": p["impressions"],
        }

    catalog_slugs: set[str] = set()
    if SKIMM_JSON.exists():
        skimm = json.loads(SKIMM_JSON.read_text(encoding="utf-8"))
        catalog_slugs = {a["slug"] for a in skimm.get("articles", [])}

    targets: list[Path] = []
    targets.extend(sorted(ROOT.glob("blog-*.html")))
    targets.extend(
        [
            ROOT / f
            for f in (
                "index.html",
                "agenzia-immobiliare-padova.html",
                "servizio-vendita.html",
                "servizio-locazioni.html",
                "immobili.html",
            )
        ]
    )
    targets.extend(sorted(ROOT.glob("zona-*.html")))

    analyzed = [analyze_page(p, gsc_pages) for p in targets if p.exists()]
    sustain = sorted(
        [a for a in analyzed if a["decision"] in ("SOSTENERE", "GEO")],
        key=lambda x: (-x["impressions"], x["page_score"]),
    )[:12]
    maintain = [a for a in analyzed if a["decision"] == "MANTENERE"][:5]
    gaps = match_keyword_gaps(gsc_data, catalog_slugs)

    probe_issues = 0
    if PROBE_JSON.exists():
        probe = json.loads(PROBE_JSON.read_text(encoding="utf-8"))
        probe_issues = sum(1 for r in probe if r.get("status", 0) >= 400)

    lines = [
        "# SEO/GEO Intelligence — Report venerdì",
        f"**Data:** {date.today().isoformat()}",
        "",
        "> Framework PAGE SCORE e decisioni: `TEST-SKILL/skill-seo.md` §11",
        "",
        "---",
        "",
        "## 1. Sintesi esecutiva",
        "",
        f"- **Pagine analizzate:** {len(analyzed)}",
        f"- **Da sostenere (refresh/GEO):** {len(sustain)}",
        f"- **Keyword gap (nuovi articoli):** {len(gaps)}",
        f"- **Probe tecnico issue:** {probe_issues}",
        "",
        "### Decisione settimana (regola)",
        "",
        "| Priorità | Azione | Quando |",
        "|---|---|---|",
        "| 1 | **SOSTENERE** pagina con imp≥20 e 0 click | title + meta + 1 H2 + link interni |",
        "| 2 | **GEO** FAQ/box sintesi su pillar | schema + Linda allineata |",
        "| 3 | **AGGIUNGERE** 1 solo articolo da gap verificato | dopo check_doppioni |",
        "| 4 | **MANTENERE** winner | timestamp mensile |",
        "",
        "---",
        "",
        "## 2. TOP — SOSTENERE / GEO (refresh)",
        "",
        "| Pagina | Score | Imp | Click | Decisione | Motivo |",
        "|---|---:|---:|---:|---|---|",
    ]
    for a in sustain:
        lines.append(
            f"| `{a['path']}` | {a['page_score']} | {a['impressions']} | {a['clicks']} | **{a['decision']}** | {a['reason']} |"
        )

    lines.extend(["", "---", "", "## 3. WINNER — MANTENERE", ""])
    for a in maintain:
        lines.append(
            f"- `{a['path']}` — score {a['page_score']}, {a['clicks']} click / {a['impressions']} imp"
        )

    lines.extend(["", "---", "", "## 4. AGGIUNGERE — keyword gap (max 1/settimana)", ""])
    for i, g in enumerate(gaps[:6], 1):
        lines.append(f"{i}. **{g['kw']}** → `{g['slug_proposto']}` — {g['rationale']}")

    lines.extend(["", "---", "", "## 5. Query GSC crescita (0 click)", ""])
    growth = sorted(
        gsc_data.get("queries_growth", []),
        key=lambda x: -x.get("impressions", 0),
    )[:10]
    if csv_queries:
        growth = sorted(csv_queries, key=lambda x: -x["impressions"])[:10]
        for q in growth:
            lines.append(f"- `{q['key']}` — {q['impressions']} imp, {q['clicks']} click")
    else:
        for q in growth:
            lines.append(
                f"- `{q['q']}` — {q['impressions']} imp, {q.get('clicks', 0)} click"
            )

    lines.extend(
        [
            "",
            "---",
            "",
            "## 6. Idee originali GEO (rotazione mensile)",
            "",
            "1. **Box risposta 40 parole** in cima agli articoli affitto (AI Overviews / Linda).",
            "2. **Mesh Limena:** collegare 6 articoli territorio-limena tra loro + zona-limena + immobili filtrati.",
            "3. **Zona pages doppio intent:** title `Vendita e affitto a {zona}` (14 pagine, batch script).",
            "4. **Acquisizioni live:** blocco «ultimi incarichi zona» da Supabase nelle zone page.",
            "5. **OMI in plain language:** tabella semestre ADE su pagina che rankia per `omi padova`.",
            "6. **llms.txt:** aggiungere URL winner GSC entro 48h da ogni refresh.",
            "",
            "> Generato da `scripts/venerdi-seo-intelligence.py`",
            "> Aggiorna `data/gsc-keywords-priority.json` ogni venerdì dopo export GSC",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> int:
    report = build_report()
    REPORT_MD.write_text(report, encoding="utf-8")
    if MERGE_INTO.exists():
        merged = MERGE_INTO.read_text(encoding="utf-8").rstrip() + "\n\n---\n\n" + report
        MERGE_INTO.write_text(merged, encoding="utf-8")
    try:
        print(report)
    except UnicodeEncodeError:
        print(report.encode("ascii", errors="replace").decode("ascii"))
    gh = os.environ.get("GITHUB_OUTPUT")
    if gh:
        with open(gh, "a", encoding="utf-8") as f:
            f.write("seo_intelligence=true\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
