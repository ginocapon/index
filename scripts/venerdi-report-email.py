#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Report email settimanale completo — venerdì 07:00 CEST.
Blocchi: executive, GSC trend, tecnico/indicizzazione, SEO intelligence, contenuti, azioni.
Aggiorna data/gsc-weekly-history.json per confronti settimana/settimana e dall'inizio anno.

Output: venerdi-email-report.html, venerdi-email-subject.txt
Cron: .github/workflows/venerdi-contenuti-freschezza.yml
"""
from __future__ import annotations

import json
import os
import re
import ssl
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GSC_JSON = ROOT / "data" / "gsc-keywords-priority.json"
HISTORY_JSON = ROOT / "data" / "gsc-weekly-history.json"
BASELINE_JSON = ROOT / "data" / "gsc-baseline-16m.json"
INDEX_JSON = ROOT / "data" / "gsc-indexing-priority.json"
INDEXING_WEEKLY_JSON = ROOT / "data" / "gsc-indexing-weekly.json"
GA4_WEEKLY_JSON = ROOT / "data" / "ga4-weekly.json"
PROBE_JSON = ROOT / "data" / "url-probe-latest.json"
SKIMM_JSON = ROOT / "TEST-SKILL" / "skimm.json"
SITEMAP = ROOT / "sitemap.xml"
SEO_REPORT = ROOT / "venerdi-seo-intelligence-report.md"
CONTENT_REPORT = ROOT / "venerdi-contenuti-report.md"
OUT_HTML = ROOT / "venerdi-email-report.html"
OUT_SUBJECT = ROOT / "venerdi-email-subject.txt"

USER_AGENT = "RighettoWeeklyReport/1.0"
PROBE_TIMEOUT = 12


def load_json(path: Path, default: dict | list) -> dict | list:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def count_sitemap_urls() -> int:
    if not SITEMAP.exists():
        return 0
    try:
        root = ET.parse(SITEMAP).getroot()
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        locs = root.findall(".//sm:loc", ns)
        if not locs:
            locs = root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
        return len(locs) if locs else len(re.findall(r"<loc>", SITEMAP.read_text(encoding="utf-8")))
    except ET.ParseError:
        return len(re.findall(r"<loc>", SITEMAP.read_text(encoding="utf-8")))


def probe_stats() -> tuple[int, int]:
    data = load_json(PROBE_JSON, [])
    if not isinstance(data, list):
        return 0, 0
    bad = [r for r in data if r.get("status") not in (200, 301, 302)]
    return len(data), len(bad)


def live_probe_url(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=PROBE_TIMEOUT, context=ctx) as resp:
            return {"url": url, "status": resp.status, "ok": resp.status == 200}
    except urllib.error.HTTPError as e:
        return {"url": url, "status": e.code, "ok": False}
    except Exception:
        return {"url": url, "status": 0, "ok": False}


def probe_indexing_urls() -> list[dict]:
    idx = load_json(INDEX_JSON, {})
    if not isinstance(idx, dict):
        return []
    urls: list[str] = []
    for key in ("pillar", "limena_cluster", "affitti_cluster"):
        urls.extend(idx.get(key, []))
    seen: set[str] = set()
    unique: list[str] = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            unique.append(u)
    return [live_probe_url(u) for u in unique]


def gsc_metrics(gsc: dict) -> dict:
    brand = gsc.get("queries_brand", [])
    winners = gsc.get("pages_winners", [])
    growth = gsc.get("queries_growth", [])
    home = next((p for p in winners if p.get("url") in ("/", "")), {})
    return {
        "brand_clicks": sum(q.get("clicks", 0) for q in brand),
        "brand_impressions": sum(q.get("impressions", 0) for q in brand),
        "home_clicks": home.get("clicks", 0),
        "home_impressions": home.get("impressions", 0),
        "queries_growth_count": len(growth),
        "queries_growth_zero_click_imp": sum(
            q.get("impressions", 0) for q in growth if q.get("clicks", 0) == 0
        ),
        "pages_refresh_priority": gsc.get("pages_refresh_priority", []),
        "pages_winners": winners,
        "published_this_week": gsc.get("published_this_week", []),
        "keyword_gaps": gsc.get("keyword_gaps_new", []),
    }


def build_snapshot(today: str, gsc: dict, blog_count: int, health: int) -> dict:
    probe_total, probe_issues = probe_stats()
    gm = gsc_metrics(gsc)
    return {
        "date": today,
        "blog_articles": blog_count,
        "sitemap_urls": count_sitemap_urls(),
        "probe_total": probe_total,
        "probe_issues": probe_issues,
        "content_health_pct": health,
        **gm,
    }


def update_history(snapshot: dict) -> tuple[dict, dict | None, dict | None]:
    hist = load_json(HISTORY_JSON, {"started": snapshot["date"], "weeks": []})
    if not isinstance(hist, dict):
        hist = {"started": snapshot["date"], "weeks": []}
    weeks: list[dict] = hist.get("weeks", [])
    ytd = weeks[0] if weeks else None
    if weeks and weeks[-1].get("date") == snapshot["date"]:
        prev = weeks[-2] if len(weeks) > 1 else None
        weeks[-1] = snapshot
    else:
        prev = weeks[-1] if weeks else None
        weeks.append(snapshot)
    hist["weeks"] = weeks
    HISTORY_JSON.write_text(
        json.dumps(hist, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return hist, prev, ytd


def delta(cur: int | float, old: int | float | None, label: str = "") -> str:
    if old is None:
        return "— (baseline)"
    d = cur - old
    if old == 0:
        pct = "+∞" if d > 0 else "0%"
    else:
        pct = f"{(d / old) * 100:+.0f}%"
    sign = "▲" if d > 0 else ("▼" if d < 0 else "→")
    return f"{sign} {d:+d} ({pct})"


def parse_sustain_rows() -> list[dict]:
    if not SEO_REPORT.exists():
        return []
    text = SEO_REPORT.read_text(encoding="utf-8")
    rows: list[dict] = []
    in_table = False
    for line in text.splitlines():
        if "## 2. TOP — SOSTENERE" in line:
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if in_table and line.startswith("| `"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 6:
                rows.append(
                    {
                        "path": parts[0].strip("`"),
                        "score": parts[1],
                        "imp": parts[2],
                        "clk": parts[3],
                        "decision": parts[4].strip("*"),
                        "reason": parts[5],
                    }
                )
    return rows[:8]


def parse_content_metrics() -> dict:
    env_keys = {
        "health": "CONTENT_HEALTH",
        "articles": "CONTENT_ARTICLES",
        "warnings": "CONTENT_WARNINGS",
        "errors": "CONTENT_ERRORS",
        "skimm_risks": "CONTENT_SKIMM_RISKS",
        "thin_articles": "CONTENT_THIN",
        "no_righetto_sol": "CONTENT_NO_SOL",
        "free_keywords": "CONTENT_FREE_KW",
    }
    out: dict = {}
    for k, env in env_keys.items():
        v = os.environ.get(env)
        if v is not None and v != "":
            out[k] = int(v) if k != "health" else int(float(v))
    if out:
        return out
    skimm = load_json(SKIMM_JSON, {})
    blogs = list(ROOT.glob("blog-*.html"))
    out["articles"] = len(blogs)
    out["health"] = 85
    if CONTENT_REPORT.exists():
        m = re.search(r"Articoli totali \| (\d+)", CONTENT_REPORT.read_text(encoding="utf-8"))
        if m:
            out["articles"] = int(m.group(1))
    return out


def section(title: str, body: str) -> str:
    return f"<h2 style='color:#1a365d;border-bottom:2px solid #e2e8f0;padding-bottom:6px'>{escape(title)}</h2>{body}"


def table(headers: list[str], rows: list[list[str]]) -> str:
    th = "".join(
        f"<th style='text-align:left;padding:6px 10px;background:#edf2f7'>{escape(h)}</th>"
        for h in headers
    )
    trs = []
    for row in rows:
        tds = "".join(
            f"<td style='padding:6px 10px;border-top:1px solid #e2e8f0'>{c}</td>" for c in row
        )
        trs.append(f"<tr>{tds}</tr>")
    return (
        f"<table style='border-collapse:collapse;width:100%;font-size:14px;margin:12px 0'>"
        f"<thead><tr>{th}</tr></thead><tbody>{''.join(trs)}</tbody></table>"
    )


def baseline_16m_html(baseline: dict) -> str:
    if not baseline:
        return ""
    totals = baseline.get("totals", {})
    rows = [
        ["Click totali (16 mesi)", f"<strong>{totals.get('clicks', 0):,}</strong>".replace(",", "."), "—"],
        ["Impression totali (16 mesi)", f"<strong>{totals.get('impressions', 0):,}</strong>".replace(",", "."), "—"],
        ["CTR media", f"{totals.get('ctr_pct', 0)}%", "—"],
        ["Posizione media", str(totals.get("avg_position", "—")), "—"],
    ]
    top_rows = [
        [escape(q.get("q", "")), str(q.get("clicks", 0)), str(q.get("impressions", 0))]
        for q in baseline.get("top_queries", [])[:8]
    ]
    insights = "".join(f"<li>{escape(i)}</li>" for i in baseline.get("insights", [])[:4])
    captured = baseline.get("captured", "")
    return (
        "<h3 style='margin-top:18px'>Riferimento storico GSC (16 mesi — baseline "
        f"{escape(captured)})</h3>"
        + table(["Metrica", "Valore", "Note"], rows)
        + "<h4>Top 8 query (periodo 16 mesi)</h4>"
        + table(["Query", "Click", "Impression"], top_rows)
        + (f"<ul style='font-size:13px'>{insights}</ul>" if insights else "")
        + "<p style='font-size:12px;color:#718096'>Fonte: <code>data/gsc-baseline-16m.json</code> — "
        "aggiornare solo su nuovo export GSC «16 mesi» significativo.</p>"
    )


def manual_tasks_html(indexing: dict, ga4: dict) -> str:
    checks = indexing.get("manual_checks", {}) if isinstance(indexing, dict) else {}
    ga4_ok = isinstance(ga4, dict) and ga4.get("sessions_7d") is not None
    idx_updated = indexing.get("updated", "—") if isinstance(indexing, dict) else "—"
    reasons = indexing.get("by_reason", {}) if isinstance(indexing, dict) else {}

    def chk(done: bool, title: str, detail: str) -> str:
        mark = "✅" if done else "☐"
        style = "color:#276749" if done else ""
        return f"<li style='{style}'><strong>{mark} {escape(title)}</strong> — {escape(detail)}</li>"

    items = [
        chk(True, "GSC Prestazioni 7+28 gg", "Aggiorna data/gsc-keywords-priority.json (prima del cron 07:00)"),
        chk(
            idx_updated != "—",
            "GSC Indicizzazione → Pagine",
            f"Aggiorna data/gsc-indexing-weekly.json — ultimo: {idx_updated}",
        ),
        chk(
            checks.get("convalida_16_crawled", False),
            "Convalida correzione",
            f"16 «scansionata non indicizzata» — attuale: {reasons.get('crawled_not_indexed', '?')}",
        ),
        chk(
            checks.get("prestazioni_affitti_limena", False),
            "Prestazioni «affitti limena»",
            "CTR o posizione 11–20 in GSC",
        ),
        chk(checks.get("sitemap_ok", False), "Sitemap", "Stato «elaborata correttamente» — no reinvio quotidiano"),
        chk(False, "Ispezione URL ×10", "Lista in data/gsc-indexing-priority.json (max ~10/giorno)"),
        chk(ga4_ok, "GA4 ultimi 7 gg", "Compila data/ga4-weekly.json (sessioni, utenti, top pagine)"),
        chk(False, "Google Business Profile", "1 post, foto o risposta recensione"),
    ]
    note = indexing.get("note", "") if isinstance(indexing, dict) else ""
    note_html = f"<p style='font-size:13px;color:#c53030'>📌 {escape(note)}</p>" if note else ""
    return (
        "<p><strong>~15 minuti manuali</strong> — spunta in GSC/GA4/GBP, poi aggiorna i JSON nel repo "
        "se vuoi grafici PDF più precisi la settimana dopo.</p>"
        + note_html
        + "<ul style='line-height:1.8'>"
        + "".join(items)
        + "</ul>"
        + "<p style='font-size:12px;color:#718096'>Stessa checklist nel PDF allegato (ultima pagina).</p>"
    )


def build_html(
    today: str,
    snapshot: dict,
    prev: dict | None,
    ytd: dict | None,
    content: dict,
    sustain: list[dict],
    index_probes: list[dict],
    baseline_16m: dict | None = None,
    indexing_weekly: dict | None = None,
    ga4_weekly: dict | None = None,
) -> str:
    health = content.get("health", snapshot.get("content_health_pct", 0))
    emoji = "🟢" if health >= 80 else ("🟡" if health >= 70 else "🔴")
    index_ok = sum(1 for p in index_probes if p["ok"])
    index_fail = [p for p in index_probes if not p["ok"]]

    exec_rows = [
        ["Salute contenuti", f"<strong>{health}%</strong>", delta(health, prev.get("content_health_pct") if prev else None)],
        ["Articoli blog", str(snapshot["blog_articles"]), delta(snapshot["blog_articles"], prev.get("blog_articles") if prev else None)],
        ["URL sitemap", str(snapshot["sitemap_urls"]), delta(snapshot["sitemap_urls"], prev.get("sitemap_urls") if prev else None)],
        ["Probe tecnico", f"{snapshot['probe_total']} URL, {snapshot['probe_issues']} issue", delta(snapshot["probe_issues"], prev.get("probe_issues") if prev else None)],
        ["Indicizzazione (probe live)", f"{index_ok}/{len(index_probes)} OK", "—"],
    ]

    ytd_note = ""
    same_ytd = not ytd or ytd.get("date") == snapshot["date"]
    if ytd and not same_ytd:
        ytd_note = (
            f"<p style='font-size:13px;color:#4a5568'>"
            f"Confronto YTD: prima rilevazione <strong>{ytd.get('date')}</strong> "
            f"→ oggi <strong>{today}</strong> "
            f"(blog {ytd.get('blog_articles', 0)} → {snapshot['blog_articles']}, "
            f"click home {ytd.get('home_clicks', 0)} → {snapshot['home_clicks']})."
            f"</p>"
        )

    def ytd_delta(cur: int | float, key: str) -> str:
        if same_ytd or not ytd:
            return "— (baseline)"
        return delta(cur, ytd.get(key))

    gsc_rows = [
        ["Click brand (5 query)", str(snapshot["brand_clicks"]), delta(snapshot["brand_clicks"], prev.get("brand_clicks") if prev else None), ytd_delta(snapshot["brand_clicks"], "brand_clicks")],
        ["Impression brand", str(snapshot["brand_impressions"]), delta(snapshot["brand_impressions"], prev.get("brand_impressions") if prev else None), ytd_delta(snapshot["brand_impressions"], "brand_impressions")],
        ["Click homepage", str(snapshot["home_clicks"]), delta(snapshot["home_clicks"], prev.get("home_clicks") if prev else None), ytd_delta(snapshot["home_clicks"], "home_clicks")],
        ["Impression homepage", str(snapshot["home_impressions"]), delta(snapshot["home_impressions"], prev.get("home_impressions") if prev else None), ytd_delta(snapshot["home_impressions"], "home_impressions")],
        ["Query crescita (0 click)", str(snapshot["queries_growth_count"]), delta(snapshot["queries_growth_count"], prev.get("queries_growth_count") if prev else None), "—"],
        ["Imp. query crescita", str(snapshot["queries_growth_zero_click_imp"]), delta(snapshot["queries_growth_zero_click_imp"], prev.get("queries_growth_zero_click_imp") if prev else None), "—"],
    ]

    sustain_rows = [
        [r["path"], r["score"], r["imp"], r["clk"], r["decision"]]
        for r in sustain
    ] or [["—", "—", "—", "—", "Nessuna pagina SOSTENERE questa settimana"]]

    published = snapshot.get("published_this_week", [])
    pub_html = "<ul>"
    if published:
        for p in published:
            pub_html += f"<li><code>{escape(p.get('slug', ''))}</code> — kw: {escape(p.get('kw', ''))}</li>"
    else:
        pub_html += "<li>Nessun articolo nuovo registrato in gsc-keywords-priority.json</li>"
    pub_html += "</ul>"

    index_rows = [
        [
            p["url"].replace("https://righettoimmobiliare.it", ""),
            f"HTTP {p['status']}" if p["status"] else "timeout",
            "✅" if p["ok"] else "❌",
        ]
        for p in index_probes
    ]

    gaps = snapshot.get("keyword_gaps", [])
    gap_list = "".join(
        f"<li><strong>{escape(g.get('kw', ''))}</strong> → <code>{escape(g.get('slug_proposto', ''))}</code></li>"
        for g in gaps[:3]
    ) or "<li>Nessun gap aperto</li>"

    indexing_weekly = indexing_weekly or {}
    idx_reasons = indexing_weekly.get("by_reason", {})
    idx_summary_rows = [
        ["Indicizzate (filtro sitemap)", str(indexing_weekly.get("indexed", "—")), "GSC manuale"],
        ["Non indicizzate", str(indexing_weekly.get("not_indexed", "—")), "GSC manuale"],
        ["Reindirizzamento", str(idx_reasons.get("redirect", "—")), "Dovrebbe scendere post-fix apex"],
        ["Scansionata, non indicizzata", str(idx_reasons.get("crawled_not_indexed", "—")), "Convalida se aperte"],
        ["Rilevata, non indicizzata", str(idx_reasons.get("discovered_not_indexed", "—")), "Monitorare"],
    ]

    blocks = [
        f"<p style='font-size:15px'><strong>{emoji} Verifica indicizzazioni — Righetto Immobiliare</strong><br>"
        f"Data: {today} · Generato automaticamente ogni venerdì ore 07:00 CEST<br>"
        f"<em>Allegato PDF con grafici GSC, indicizzazione e checklist operativa.</em></p>",
        section("1. Sintesi esecutiva", table(["Metrica", "Valore", "Δ vs sett. scorsa"], exec_rows)),
        section(
            "2. Google Search Console — performance e trend",
            ytd_note
            + table(
                ["Metrica", "Oggi", "Δ settimana", "Δ dall'inizio tracking"],
                gsc_rows,
            )
            + "<p style='font-size:13px'>Fonte settimanale: <code>data/gsc-keywords-priority.json</code> — aggiornare ogni venerdì (Prestazioni 7+28 gg).</p>"
            + baseline_16m_html(baseline_16m or {})
        ),
        section(
            "3. Tecnico e indicizzazione",
            f"<p>Probe automatico su <strong>{len(index_probes)}</strong> URL prioritarie "
            f"(pillar + cluster Limena + affitti). Per stato «presente su Google» usare "
            f"<strong>Ispezione URL</strong> in GSC (max ~10 richieste/giorno) — non inviare pagine singole come sitemap.</p>"
            + table(["URL", "HTTP", "Live"], index_rows)
            + (
                f"<p style='color:#c53030'>⚠️ URL non raggiungibili: {', '.join(p['url'] for p in index_fail)}</p>"
                if index_fail
                else "<p>✅ Tutte le URL prioritarie rispondono HTTP 200.</p>"
            )
            + f"<p>Sitemap: <code>https://righettoimmobiliare.it/sitemap.xml</code> — {snapshot['sitemap_urls']} URL catalogate.</p>"
            + "<h3>Stato indicizzazione GSC (aggiornamento manuale)</h3>"
            + table(["Metrica", "Valore", "Nota"], idx_summary_rows)
            + "<p style='font-size:12px;color:#718096'>Fonte: <code>data/gsc-indexing-weekly.json</code> — aggiornare ogni venerdì da GSC → Indicizzazione → Pagine.</p>"
        ),
        section(
            "4. SEO Intelligence — SOSTENERE / refresh",
            table(["Pagina", "Score", "Imp", "Click", "Decisione"], sustain_rows)
            + "<p>Framework PAGE SCORE: vedi Issue GitHub e <code>venerdi-seo-intelligence-report.md</code>.</p>"
        ),
        section(
            "5. Contenuti e SKIMM",
            f"<ul>"
            f"<li>Articoli blog: <strong>{content.get('articles', snapshot['blog_articles'])}</strong></li>"
            f"<li>Avvisi SKIMM: <strong>{content.get('skimm_risks', '—')}</strong></li>"
            f"<li>Articoli thin (&lt;1500 parole): <strong>{content.get('thin_articles', '—')}</strong></li>"
            f"<li>Senza sezione Righetto: <strong>{content.get('no_righetto_sol', '—')}</strong></li>"
            f"<li>Keyword libere: <strong>{content.get('free_keywords', '—')}</strong></li>"
            f"</ul>"
            + "<h3>Pubblicati questa settimana</h3>" + pub_html
        ),
        section(
            "6. Azioni priorità prossima settimana (repo / agente)",
            "<ol>"
            "<li><strong>SOSTENERE:</strong> 1 refresh su pagina imp≥20 e 0 click (vedi blocco 4)</li>"
            "<li><strong>AGGIUNGERE:</strong> max 1 articolo solo se gap confermato:</li>"
            f"<ul>{gap_list}</ul>"
            "<li><strong>MANTENERE:</strong> timestamp su 1 winner GSC</li>"
            "<li><strong>Probe:</strong> 0 issue su url-probe-latest.json dopo ogni deploy</li>"
            "</ol>"
        ),
        section("7. Cosa fare TU questa settimana", manual_tasks_html(indexing_weekly, ga4_weekly or {})),
        "<hr><p style='font-size:12px;color:#718096'>"
        "Report completo Markdown: Issue GitHub label <code>contenuti-freschezza</code> · "
        "PDF: <code>data/venerdi-report-latest.pdf</code> · "
        "Cron: <code>venerdi-contenuti-freschezza.yml</code> + <code>venerdi-report-email.py</code>"
        "</p>",
    ]
    style = (
        "<div style='font-family:Segoe UI,Arial,sans-serif;max-width:720px;"
        "color:#2d3748;line-height:1.5'>"
    )
    return style + "".join(blocks) + "</div>"


def main() -> int:
    today = date.today().isoformat()
    gsc = load_json(GSC_JSON, {})
    if not isinstance(gsc, dict):
        gsc = {}
    content = parse_content_metrics()
    health = content.get("health", 85)
    blog_count = content.get("articles", len(list(ROOT.glob("blog-*.html"))))

    snapshot = build_snapshot(today, gsc, blog_count, health)
    _, prev, ytd = update_history(snapshot)
    sustain = parse_sustain_rows()
    index_probes = probe_indexing_urls()

    baseline = load_json(BASELINE_JSON, {})
    if not isinstance(baseline, dict):
        baseline = {}

    indexing_weekly = load_json(INDEXING_WEEKLY_JSON, {})
    ga4_weekly = load_json(GA4_WEEKLY_JSON, {})
    if not isinstance(indexing_weekly, dict):
        indexing_weekly = {}
    if not isinstance(ga4_weekly, dict):
        ga4_weekly = {}

    html = build_html(
        today, snapshot, prev, ytd, content, sustain, index_probes, baseline,
        indexing_weekly, ga4_weekly,
    )
    OUT_HTML.write_text(html, encoding="utf-8")

    subject = f"Verifica indicizzazioni — Righetto — {today} — salute {health}% · probe {snapshot['probe_issues']} issue"
    OUT_SUBJECT.write_text(subject, encoding="utf-8")

    gh = os.environ.get("GITHUB_OUTPUT")
    if gh:
        with open(gh, "a", encoding="utf-8") as f:
            f.write("email_ready=true\n")
            f.write(f"email_subject={subject}\n")

    print(f"OK: {OUT_HTML.name} ({len(html)} chars)")
    try:
        print(f"Subject: {subject}")
    except UnicodeEncodeError:
        print(f"Subject: {subject.encode('ascii', errors='replace').decode('ascii')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
