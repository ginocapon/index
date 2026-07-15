#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera PDF allegato al report venerdì — grafici GSC trend, indicizzazione, GA4 (se compilato).
Output: data/venerdi-report-latest.pdf

Cron: .github/workflows/venerdi-contenuti-freschezza.yml (dopo venerdi-report-email.py)
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

ROOT = Path(__file__).resolve().parent.parent
HISTORY_JSON = ROOT / "data" / "gsc-weekly-history.json"
INDEXING_JSON = ROOT / "data" / "gsc-indexing-weekly.json"
GA4_JSON = ROOT / "data" / "ga4-weekly.json"
BASELINE_JSON = ROOT / "data" / "gsc-baseline-16m.json"
GSC_JSON = ROOT / "data" / "gsc-keywords-priority.json"
OUT_PDF = ROOT / "data" / "venerdi-report-latest.pdf"

BRAND = "#1a365d"
ACCENT = "#2b6cb0"
MUTED = "#718096"


def load_json(path: Path, default: dict | list) -> dict | list:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def cover_page(pdf: PdfPages, today: str) -> None:
    fig, ax = plt.subplots(figsize=(8.27, 11.69))
    ax.axis("off")
    ax.text(
        0.5,
        0.72,
        "Righetto Immobiliare",
        ha="center",
        va="center",
        fontsize=22,
        fontweight="bold",
        color=BRAND,
    )
    ax.text(
        0.5,
        0.62,
        "Verifica indicizzazioni e performance",
        ha="center",
        va="center",
        fontsize=16,
        color=ACCENT,
    )
    ax.text(0.5, 0.52, f"Report settimanale — {today}", ha="center", va="center", fontsize=13)
    ax.text(
        0.5,
        0.38,
        "Fonti: GSC (repo + aggiornamento manuale), probe tecnico, GA4 (opzionale)\n"
        "Generato automaticamente ogni venerdì ore 07:00 CEST",
        ha="center",
        va="center",
        fontsize=10,
        color=MUTED,
    )
    ax.text(
        0.5,
        0.12,
        "righettoimmobiliare.it",
        ha="center",
        va="center",
        fontsize=9,
        color=MUTED,
    )
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def gsc_trend_page(pdf: PdfPages, hist: dict) -> None:
    weeks = hist.get("weeks", [])
    if len(weeks) < 1:
        return
    dates = [w.get("date", "")[-5:] for w in weeks]
    brand = [w.get("brand_clicks", 0) for w in weeks]
    home = [w.get("home_clicks", 0) for w in weeks]
    health = [w.get("content_health_pct", 0) for w in weeks]

    fig, axes = plt.subplots(2, 1, figsize=(8.27, 8), gridspec_kw={"height_ratios": [2, 1]})
    fig.suptitle("Google Search Console — trend settimanale", fontsize=14, fontweight="bold", color=BRAND)

    ax1 = axes[0]
    x = range(len(dates))
    ax1.plot(x, brand, marker="o", label="Click brand (5 query)", color=ACCENT, linewidth=2)
    ax1.plot(x, home, marker="s", label="Click homepage", color="#38a169", linewidth=2)
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(dates, rotation=45, ha="right")
    ax1.set_ylabel("Click")
    ax1.legend(loc="upper left")
    ax1.grid(axis="y", alpha=0.3)

    ax2 = axes[1]
    ax2.bar(x, health, color="#ed8936", alpha=0.85, label="Salute contenuti %")
    ax2.set_xticks(list(x))
    ax2.set_xticklabels(dates, rotation=45, ha="right")
    ax2.set_ylabel("%")
    ax2.set_ylim(0, 100)
    ax2.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def indexing_page(pdf: PdfPages, indexing: dict) -> None:
    reasons = indexing.get("by_reason", {})
    labels = []
    values = []
    color_map = {
        "redirect": "#e53e3e",
        "discovered_not_indexed": "#dd6b20",
        "crawled_not_indexed": "#d69e2e",
        "indexed": "#38a169",
        "not_indexed": "#718096",
    }
    colors = []
    for key, label in [
        ("redirect", "Reindirizzamento"),
        ("discovered_not_indexed", "Rilevata, non indicizzata"),
        ("crawled_not_indexed", "Scansionata, non indicizzata"),
    ]:
        if key in reasons:
            labels.append(label)
            values.append(reasons[key])
            colors.append(color_map[key])

    fig, axes = plt.subplots(1, 2, figsize=(8.27, 5))
    fig.suptitle(
        f"Indicizzazione GSC — aggiornato {indexing.get('updated', '—')}",
        fontsize=13,
        fontweight="bold",
        color=BRAND,
    )

    if labels:
        axes[0].barh(labels, values, color=colors)
        axes[0].set_xlabel("Pagine (filtro sitemap)")
        axes[0].invert_yaxis()
    else:
        axes[0].text(0.5, 0.5, "Dati non ancora compilati", ha="center", va="center")
        axes[0].axis("off")

    summary = [
        f"Sitemap URL: {indexing.get('sitemap_urls', '—')}",
        f"Indicizzate (filtro sitemap): {indexing.get('indexed', '—')}",
        f"Non indicizzate: {indexing.get('not_indexed', '—')}",
    ]
    note = indexing.get("note", "")
    axes[1].axis("off")
    axes[1].text(0.05, 0.85, "Riepilogo", fontsize=12, fontweight="bold", color=BRAND)
    for i, line in enumerate(summary):
        axes[1].text(0.05, 0.72 - i * 0.1, line, fontsize=11)
    if note:
        axes[1].text(0.05, 0.25, note, fontsize=9, color=MUTED, wrap=True)

    plt.tight_layout()
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def ga4_page(pdf: PdfPages, ga4: dict) -> None:
    fig, ax = plt.subplots(figsize=(8.27, 6))
    fig.suptitle("Google Analytics 4 — ultimi 7 giorni", fontsize=13, fontweight="bold", color=BRAND)

    sessions = ga4.get("sessions_7d")
    users = ga4.get("users_7d")
    pageviews = ga4.get("pageviews_7d")
    updated = ga4.get("updated")

    if sessions is not None and users is not None:
        metrics = ["Sessioni", "Utenti", "Pagine viste"]
        vals = [sessions or 0, users or 0, pageviews or 0]
        ax.bar(metrics, vals, color=[ACCENT, "#38a169", "#ed8936"])
        ax.set_ylabel("Conteggio")
        ax.text(0.5, -0.15, f"Aggiornato: {updated}", ha="center", transform=ax.transAxes, fontsize=9, color=MUTED)
        top = ga4.get("top_pages", [])[:5]
        if top:
            note = "Top pagine:\n" + "\n".join(
                f"  • {p.get('path', p.get('page', '?'))}: {p.get('views', p.get('pageviews', '—'))}"
                for p in top
            )
            ax.text(1.02, 0.5, note, transform=ax.transAxes, fontsize=9, va="center")
    else:
        ax.axis("off")
        ax.text(
            0.5,
            0.55,
            "GA4 non ancora compilato questa settimana",
            ha="center",
            va="center",
            fontsize=12,
            color=ACCENT,
        )
        ax.text(
            0.5,
            0.35,
            "Compila data/ga4-weekly.json ogni venerdì\n"
            "(sessioni, utenti, pageview 7 gg da GA4 → Prestazioni)",
            ha="center",
            va="center",
            fontsize=10,
            color=MUTED,
        )

    plt.tight_layout()
    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def baseline_page(pdf: PdfPages, baseline: dict, gsc: dict) -> None:
    fig, ax = plt.subplots(figsize=(8.27, 6))
    ax.axis("off")
    fig.suptitle("Riferimento GSC 16 mesi vs settimana corrente", fontsize=13, fontweight="bold", color=BRAND)

    totals = baseline.get("totals", {})
    hist_note = baseline.get("captured", "—")
    brand = sum(q.get("clicks", 0) for q in gsc.get("queries_brand", []))
    home = next((p for p in gsc.get("pages_winners", []) if p.get("url") in ("/", "")), {})
    home_clk = home.get("clicks", 0)

    lines = [
        f"Baseline 16 mesi (catturata {hist_note}):",
        f"  • Click totali: {totals.get('clicks', 0):,}".replace(",", "."),
        f"  • Impression: {totals.get('impressions', 0):,}".replace(",", "."),
        f"  • CTR media: {totals.get('ctr_pct', 0)}%",
        f"  • Posizione media: {totals.get('avg_position', '—')}",
        "",
        "Settimana corrente (gsc-keywords-priority.json):",
        f"  • Click brand: {brand}",
        f"  • Click homepage: {home_clk}",
        "",
        "Probe tecnico: vedi email HTML blocco 3",
    ]
    ax.text(0.05, 0.9, "\n".join(lines), va="top", fontsize=11, family="monospace")

    top = baseline.get("top_queries", [])[:6]
    if top:
        ax.text(0.05, 0.35, "Top query baseline:", fontsize=11, fontweight="bold", color=BRAND)
        for i, q in enumerate(top):
            ax.text(
                0.05,
                0.28 - i * 0.05,
                f"{q.get('q', '')}: {q.get('clicks', 0)} click",
                fontsize=10,
            )

    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def manual_tasks_page(pdf: PdfPages, indexing: dict) -> None:
    checks = indexing.get("manual_checks", {})
    fig, ax = plt.subplots(figsize=(8.27, 8))
    ax.axis("off")
    fig.suptitle("Cosa fare TU — checklist venerdì (~15 min)", fontsize=13, fontweight="bold", color=BRAND)

    tasks = [
        ("GSC Prestazioni 7+28 gg", "Aggiorna data/gsc-keywords-priority.json", True),
        ("GSC Indicizzazione → Pagine", "Aggiorna data/gsc-indexing-weekly.json (conteggi + motivi)", True),
        ("Convalida correzione 16 «scansionata»", "Se ancora aperte in GSC", not checks.get("convalida_16_crawled", False)),
        ("Prestazioni query «affitti limena»", "CTR / posizione 11–20", not checks.get("prestazioni_affitti_limena", False)),
        ("Sitemap", "Verifica «elaborata correttamente» (no reinvio quotidiano)", checks.get("sitemap_ok", False)),
        ("Ispezione URL ×10", "Lista in data/gsc-indexing-priority.json", False),
        ("GA4 ultimi 7 gg", "Compila data/ga4-weekly.json", False),
        ("Google Business Profile", "1 post o risposta recensione", False),
    ]

    y = 0.88
    for title, detail, done in tasks:
        mark = "☑" if done else "☐"
        ax.text(0.05, y, f"{mark} {title}", fontsize=11, fontweight="bold")
        ax.text(0.08, y - 0.04, detail, fontsize=9, color=MUTED)
        y -= 0.1

    ax.text(
        0.05,
        0.08,
        "Dopo il fix DNS apex (15/07): monitorare se «reindirizzamento» scende entro 22/07.",
        fontsize=9,
        color="#c53030",
    )

    pdf.savefig(fig, bbox_inches="tight")
    plt.close(fig)


def main() -> int:
    today = date.today().isoformat()
    hist = load_json(HISTORY_JSON, {"weeks": []})
    indexing = load_json(INDEXING_JSON, {})
    ga4 = load_json(GA4_JSON, {})
    baseline = load_json(BASELINE_JSON, {})
    gsc = load_json(GSC_JSON, {})

    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    with PdfPages(OUT_PDF) as pdf:
        cover_page(pdf, today)
        gsc_trend_page(pdf, hist if isinstance(hist, dict) else {})
        indexing_page(pdf, indexing if isinstance(indexing, dict) else {})
        ga4_page(pdf, ga4 if isinstance(ga4, dict) else {})
        if isinstance(baseline, dict) and baseline:
            baseline_page(pdf, baseline, gsc if isinstance(gsc, dict) else {})
        manual_tasks_page(pdf, indexing if isinstance(indexing, dict) else {})

    print(f"OK: {OUT_PDF} ({OUT_PDF.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
