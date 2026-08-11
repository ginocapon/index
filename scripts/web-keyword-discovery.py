#!/usr/bin/env python3
"""
Discovery settimanale keyword/temi da articoli web istituzionali + GSC statico.
Bypass API GSC: usa data/gsc-keywords-priority.json + titoli fonti verificabili.

Output:
  - data/web-keyword-discovery-latest.json
  - web-keyword-discovery-report.md
  - aggiorna data/editorial-queue.json (status=proposed, max 5)
  - data/geo-keyword-actions-latest.json (SOSTENERE / GEO AEO)

Uso:
  python scripts/web-keyword-discovery.py
  python scripts/web-keyword-discovery.py --no-queue   # solo report
"""
from __future__ import annotations

import argparse
import json
import re
import ssl
import subprocess
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import date, timedelta
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "righetto-premortem-guardian/config/web-discovery-sources.yaml"
GSC_JSON = ROOT / "data/gsc-keywords-priority.json"
SKIMM_JSON = ROOT / "TEST-SKILL/skimm.json"
QUEUE_JSON = ROOT / "data/editorial-queue.json"
OUT_JSON = ROOT / "data/web-keyword-discovery-latest.json"
OUT_GEO = ROOT / "data/geo-keyword-actions-latest.json"
REPORT_MD = ROOT / "web-keyword-discovery-report.md"
UA = "RighettoWebKeywordDiscovery/1.0"
TIMEOUT = 18

# Proposte editoriali curate da trend web verificati (FIMAA/ISTAT/Veneto/GSC gap) — angoli unici
CURATED_PROPOSALS = [
    {
        "kw_primaria": "costi ristrutturazione usato frenano acquisto",
        "slug": "blog-costi-ristrutturazione-usato-frenano-acquisto-padova-2026",
        "title": "Usato da riqualificare: perché i costi di ristrutturazione frenano l'acquisto nel 2026",
        "intent": "acquisto-budget-operativo",
        "cluster": "acquisto-operativo",
        "web_signal": "FIMAA Q1 2026: 33% operatori — costi elevati ristrutturazione frenano usato",
        "different_from": "blog-bonus-edilizi-2026-incentivi-casa-padova",
        "research_refs": [
            "https://www.confcommercio.it/-/mercato-immobiliare",
            "https://www.simplybiz.eu/fimaa-immobiliare-previsioni-2026-sentiment-1-quadrimestre/",
        ],
        "geo_actions": ["aeo_box_costi_ristrutturazione", "faq_budget_acquirente"],
        "gsc_align": None,
    },
    {
        "kw_primaria": "mutuo tasso 3.42 accesso credito 2026",
        "slug": "blog-mutuo-tasso-342-accesso-credito-padova-2026",
        "title": "Mutuo al 3,42%: finestra di accesso al credito per chi compra nel Padovano",
        "intent": "mutuo-timing",
        "cluster": "mutui-cluster",
        "web_signal": "Confcommercio/ABI: mutui acquisto abitazioni ~3,42% feb 2026",
        "different_from": "blog-mutui-casa-padova-2026",
        "research_refs": [
            "https://www.confcommercio.it/-/mercato-immobiliare",
        ],
        "geo_actions": ["refresh_meta_mutui_casa", "faq_tasso_fisso_timing"],
        "gsc_align": None,
    },
    {
        "kw_primaria": "affitti nuovo veneto 10 percento",
        "slug": "blog-affitti-nuovo-vs-usato-veneto-2026",
        "title": "Affitti nel Veneto: nuovo +10,3% e divario con l'usato — cosa cambia per chi cerca casa",
        "intent": "affitto-nuovo-usato",
        "cluster": "affitti-cluster",
        "web_signal": "Focus Veneto 2026 / Immobiliare.it: nuovo locazione +10,3% Q1",
        "different_from": "blog-affitti-padova-canoni-2026",
        "research_refs": [
            "https://www.unioneimmobiliare.org/eventi/focus-veneto-2026/",
        ],
        "geo_actions": ["faq_nuovo_vs_usato_affitto", "link_zona_limena"],
        "gsc_align": "affitti limena",
    },
    {
        "kw_primaria": "ipab istat 5.2 prezzi abitazioni",
        "slug": "blog-ipab-istat-q1-2026-padova-interpretazione",
        "title": "Prezzi case +5,2% (ISTAT Q1 2026): cosa significa davvero se compri a Padova",
        "intent": "dato-interpretazione",
        "cluster": "analisi-scenari",
        "web_signal": "ISTAT IPAB Q1 2026 +5,2% annuo; compravendite ADE +4,4%",
        "different_from": "blog-mercato-immobiliare-padova-2026",
        "research_refs": [
            "https://www.istat.it/comunicato-stampa/prezzi-delle-abitazioni-dati-provvisori-i-trimestre-2026/",
        ],
        "geo_actions": ["aeo_dato_istat", "schema_dataset_citation"],
        "gsc_align": None,
    },
    {
        "kw_primaria": "gergo immobiliare padova",
        "slug": "blog-gergo-immobiliare-padova-guida-2026",
        "title": "Gergo immobiliare: 25 termini che sentirai in agenzia a Padova (con esempi chiari)",
        "intent": "educational-aeo",
        "cluster": "vita-agenzia-brand",
        "web_signal": "GSC: gergo immobiliare padova 3 impr 0 clic — gap AEO",
        "different_from": "blog-5-domande-appuntamento-agenzia-padova-2026",
        "research_refs": [
            "https://www.agenziaentrate.gov.it/portale/web/guest/schede/fabbricatiterreni/omi/banche-dati/quotazioni-immobiliari",
        ],
        "geo_actions": ["faq_gergo_visura_caparra", "llms_glossary_snippet"],
        "gsc_align": "gergo immobiliare padova",
    },
]


def load_yaml_sources() -> list[dict]:
    if not CONFIG.exists():
        return []
    text = CONFIG.read_text(encoding="utf-8")
    sources: list[dict] = []
    cur: dict | None = None
    for line in text.splitlines():
        if line.strip().startswith("- id:"):
            if cur:
                sources.append(cur)
            cur = {"id": line.split(":", 1)[1].strip().strip('"')}
        elif cur is not None and "url:" in line:
            m = re.search(r'url:\s*"(.+)"', line)
            if m:
                cur["url"] = m.group(1)
        elif cur is not None and "tags:" in line:
            cur["tags"] = []
    if cur:
        sources.append(cur)
    return [s for s in sources if s.get("url")]


def fetch(url: str) -> tuple[str, int]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
            return resp.read().decode("utf-8", errors="replace"), resp.status
    except urllib.error.HTTPError as e:
        return "", e.code
    except Exception:
        return "", -1


def extract_signals(html: str) -> dict:
    title_m = re.search(r"<title[^>]*>([^<]+)</title>", html, re.I)
    h1s = re.findall(r"<h1[^>]*>([^<]+)</h1>", html, re.I)
    h2s = re.findall(r"<h2[^>]*>([^<]+)</h2>", html, re.I)
    og = re.search(r'property="og:title"\s+content="([^"]+)"', html, re.I)
    text = unescape(
        " ".join([title_m.group(1) if title_m else "", *h1s[:3], *h2s[:8], og.group(1) if og else ""])
    )
    text = re.sub(r"\s+", " ", text).lower()
    words = re.findall(r"[a-zàèéìòù]{4,}", text)
    return {
        "title": title_m.group(1).strip() if title_m else "",
        "headings": [unescape(h).strip() for h in h1s[:2]],
        "term_freq": Counter(words),
        "raw_len": len(html),
    }


def load_skimm_index() -> tuple[set[str], set[str], list[dict]]:
    if not SKIMM_JSON.exists():
        return set(), set(), []
    data = json.loads(SKIMM_JSON.read_text(encoding="utf-8"))
    articles = data.get("articles", [])
    kws = {a.get("kw_primaria", "").lower() for a in articles}
    slugs = {a.get("slug", "").lower() for a in articles}
    return kws, slugs, articles


def load_gsc_gaps() -> list[dict]:
    if not GSC_JSON.exists():
        return []
    data = json.loads(GSC_JSON.read_text(encoding="utf-8"))
    gaps = []
    for q in data.get("queries_growth", []):
        if q.get("impressions", 0) >= 3 and q.get("clicks", 0) == 0:
            gaps.append(q)
    for q in data.get("queries_limena_top_volume", []):
        if q.get("status") != "published":
            gaps.append({"q": q.get("q"), "impressions": q.get("impressions", 0), "intent": q.get("intent")})
    return gaps


def skimm_check(slug: str, kw: str) -> tuple[bool, str]:
    r = subprocess.run(
        ["python3", "scripts/build_skimm.py", "--check", slug, kw, "discovery"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        return False, (r.stdout or r.stderr or "conflitto SKIMM").strip()
    return True, "OK"


def score_web_terms(all_signals: list[dict], seeds: list[str]) -> list[tuple[str, int]]:
    totals: Counter[str] = Counter()
    for sig in all_signals:
        for seed in seeds:
            if seed in sig.get("title", "").lower():
                totals[seed] += 5
            freq = sig.get("term_freq", {})
            for w, c in freq.items():
                if seed in w or w in seed:
                    totals[seed] += c
    return totals.most_common(20)


def build_geo_actions(gsc: dict, proposals: list[dict]) -> list[dict]:
    actions = []
    for page in gsc.get("pages_refresh_priority", [])[:5]:
        actions.append(
            {
                "action": "SOSTENERE",
                "url": page.get("url"),
                "reason": f"{page.get('impressions', 0)} impr, {page.get('clicks', 0)} clic",
                "geo": ["aeo_answer_box", "faq_visible", "dateModified"],
                "priority": "high" if page.get("clicks", 0) == 0 and page.get("impressions", 0) > 50 else "medium",
            }
        )
    for p in proposals:
        for ga in p.get("geo_actions", []):
            actions.append({"action": "AGGIUNGERE", "target": p["slug"], "geo": ga, "kw": p["kw_primaria"]})
    return actions


def next_queue_id(queue: dict) -> str:
    ids = [i.get("id", "") for i in queue.get("items", [])]
    n = 1
    while f"eq-web-{n:03d}" in ids:
        n += 1
    return f"eq-web-{n:03d}"


def merge_queue(proposals: list[dict], max_add: int = 5) -> list[dict]:
    queue = json.loads(QUEUE_JSON.read_text(encoding="utf-8"))
    existing_slugs = {i.get("slug") for i in queue.get("items", [])}
    existing_kw = {i.get("kw_primaria", "").lower() for i in queue.get("items", [])}
    added = []
    for prop in proposals:
        if prop["slug"] in existing_slugs or prop["kw_primaria"].lower() in existing_kw:
            prop["queue_status"] = "skipped_duplicate"
            continue
        ok, msg = skimm_check(prop["slug"], prop["kw_primaria"])
        if not ok:
            prop["queue_status"] = f"skipped_skimm: {msg}"
            continue
        if len(added) >= max_add:
            prop["queue_status"] = "skipped_limit"
            continue
        item = {
            "id": next_queue_id(queue),
            "status": "proposed",
            "priority": 10 + len(added),
            "target_week": (date.today() + timedelta(days=7 * (len(added) + 1))).isoformat(),
            "slug": prop["slug"],
            "kw_primaria": prop["kw_primaria"],
            "intent": prop["intent"],
            "title": prop["title"],
            "cluster": prop["cluster"],
            "different_from": prop.get("different_from"),
            "research_refs": prop.get("research_refs", []),
            "web_signal": prop.get("web_signal"),
            "gsc_align": prop.get("gsc_align"),
            "discovery_source": "web-keyword-discovery",
            "discovered_at": date.today().isoformat(),
        }
        queue.setdefault("items", []).append(item)
        added.append(item)
        prop["queue_status"] = "proposed"
        prop["queue_id"] = item["id"]
    queue["updated"] = date.today().isoformat()
    queue["last_web_discovery"] = date.today().isoformat()
    QUEUE_JSON.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return added


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-queue", action="store_true", help="Non aggiorna editorial-queue.json")
    args = parser.parse_args()

    sources = load_yaml_sources()
    kws, slugs, _ = load_skimm_index()
    gsc = json.loads(GSC_JSON.read_text(encoding="utf-8")) if GSC_JSON.exists() else {}
    gsc_gaps = load_gsc_gaps()

    seeds = []
    if CONFIG.exists():
        for line in CONFIG.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\s+-\s+(.+)", line)
            if m and not line.strip().startswith("- id"):
                seeds.append(m.group(1).strip())

    fetch_log = []
    all_signals = []
    for src in sources:
        html, status = fetch(src["url"])
        fetch_log.append({"id": src.get("id"), "url": src["url"], "status": status, "bytes": len(html)})
        if html:
            sig = extract_signals(html)
            sig["source_id"] = src.get("id")
            all_signals.append(sig)

    top_terms = score_web_terms(all_signals, seeds)

    proposals = []
    for curated in CURATED_PROPOSALS:
        p = dict(curated)
        if p["kw_primaria"].lower() in kws or p["slug"].lower() in slugs:
            p["validation"] = "overlap_catalog"
            continue
        ok, msg = skimm_check(p["slug"], p["kw_primaria"])
        p["validation"] = msg
        if ok:
            proposals.append(p)

    # Riempie fino a 5 con gap GSC se curated insufficienti
    if len(proposals) < 5:
        for gap in gsc_gaps:
            q = (gap.get("q") or "").strip()
            if not q or len(q) < 4:
                continue
            slug = "blog-" + re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-") + "-2026"
            if slug in slugs or q.lower() in kws:
                continue
            ok, msg = skimm_check(slug, q)
            if not ok:
                continue
            proposals.append(
                {
                    "kw_primaria": q,
                    "slug": slug,
                    "title": f"{q.capitalize()}: guida pratica nel Padovano (2026)",
                    "intent": gap.get("intent", "gsc-gap"),
                    "cluster": "gsc-discovery",
                    "web_signal": f"GSC statico: {gap.get('impressions', 0)} impr, 0 clic",
                    "different_from": "auto-gsc-gap",
                    "research_refs": [],
                    "geo_actions": ["aeo_gap_query"],
                    "gsc_align": q,
                    "validation": msg,
                }
            )
            if len(proposals) >= 5:
                break

    proposals = proposals[:5]
    added_items = [] if args.no_queue else merge_queue(proposals, max_add=5)
    geo_actions = build_geo_actions(gsc, proposals)

    result = {
        "date": date.today().isoformat(),
        "sources_fetched": fetch_log,
        "web_term_signals": top_terms[:15],
        "gsc_gaps_sample": gsc_gaps[:10],
        "proposals": proposals,
        "queue_added": [i["id"] for i in added_items],
        "geo_seo_actions": geo_actions,
        "method": "web_titles_institutional + gsc-keywords-priority.json (no API)",
    }

    OUT_JSON.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    OUT_GEO.write_text(json.dumps({"date": result["date"], "actions": geo_actions}, indent=2), encoding="utf-8")

    lines = [
        "# Web Keyword Discovery — Righetto Immobiliare",
        f"**Data:** {result['date']}",
        "",
        "## Metodo",
        "Titoli e termini da fonti istituzionali/editoriali + gap da `gsc-keywords-priority.json` (no GSC API).",
        "",
        "## Fonti fetch",
    ]
    for f in fetch_log:
        lines.append(f"- [{f['status']}] {f['id']}: {f['url']}")
    lines.extend(["", "## Termini trending (web)", ""])
    for term, score in top_terms[:10]:
        lines.append(f"- {term}: {score}")
    lines.extend(["", "## 5 proposte articolo (anti-doppioni)", ""])
    for i, p in enumerate(proposals, 1):
        lines.append(f"### {i}. {p['title']}")
        lines.append(f"- **KW:** {p['kw_primaria']}")
        lines.append(f"- **Slug:** {p['slug']}")
        lines.append(f"- **Segnale web:** {p.get('web_signal', '—')}")
        lines.append(f"- **Queue:** {p.get('queue_status', '—')}")
        lines.append("")
    lines.extend(["", "## Azioni GEO/SEO (SOSTENERE + AGGIUNGERE)", ""])
    for a in geo_actions[:12]:
        lines.append(f"- {a.get('action')} {a.get('url') or a.get('target')}: {a.get('geo')}")
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(f"Proposte: {len(proposals)} | Coda +{len(added_items)}")
    print(f"Report: {REPORT_MD.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
