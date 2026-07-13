#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit compliance Google 2026 — tutte le regole, strumento repo gratuito."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS = 0
WARNINGS = 0
OK = 0
REPORT: list[str] = []

PILLAR = [
    "index.html",
    "blog.html",
    "agenzia-immobiliare-padova.html",
    "servizio-locazioni.html",
    "servizio-valutazioni.html",
    "chi-siamo.html",
    "servizi.html",
    "contatti.html",
    "faq.html",
]

SKIP_HTML = {
    "admin.html",
    "blog-articolo.html",
    "404.html",
    "bookmarklet-helper.html",
    "unsubscribe.html",
    "scraping.html",
    "immobile.html",
    "landing-demo-loft-adiacenti-padova-vicenza.html",
}


def is_redirect_stub(raw: str) -> bool:
    low = raw.lower()
    if "reindirizzamento" in low and ('http-equiv="refresh"' in low or "location.replace" in low):
        return True
    return False


def is_demo_noindex(raw: str, name: str) -> bool:
    if not name.startswith("landing-demo-"):
        return False
    return "noindex" in raw.lower() and "nofollow" in raw.lower()

SKIP_PREFIXES = ("share-immobile-", "google")


def log_ok(msg: str) -> None:
    global OK
    OK += 1
    REPORT.append(f"  OK {msg}")


def log_warn(msg: str) -> None:
    global WARNINGS
    WARNINGS += 1
    REPORT.append(f"  WARN {msg}")


def log_err(msg: str) -> None:
    global ERRORS
    ERRORS += 1
    REPORT.append(f"  ERR {msg}")


def visible_text(html: str) -> str:
    t = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.S | re.I)
    t = re.sub(r"<style[^>]*>.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", t).lower()


def check_global() -> None:
    REPORT.append("## 1. Globali")
    for name in ("robots.txt", "sitemap.xml", "llms.txt", "ai.json"):
        if (ROOT / name).exists():
            log_ok(f"{name} presente")
        else:
            log_err(f"{name} mancante")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8", errors="replace") if (ROOT / "robots.txt").exists() else ""
    for bot in ("GPTBot", "Google-Extended", "PerplexityBot"):
        block = re.search(rf"User-agent:\s*{bot}.*?Disallow:\s*/", robots, re.S | re.I)
        if block:
            log_err(f"robots.txt blocca {bot}")


def check_page(path: Path) -> None:
    name = path.name
    raw = path.read_text(encoding="utf-8", errors="replace")

    title = re.search(r"<title>([^<]+)</title>", raw, re.I)
    if not title:
        log_err(f"{name}: title mancante")
    elif len(title.group(1)) > 70:
        log_warn(f"{name}: title lungo ({len(title.group(1))} char)")

    desc = re.search(r'<meta name="description" content="([^"]*)"', raw, re.I)
    if not desc or not desc.group(1).strip():
        log_err(f"{name}: meta description mancante")
    elif len(desc.group(1)) > 160:
        log_warn(f"{name}: meta description lunga")

    canon = re.search(r'<link rel="canonical" href="([^"]+)"', raw, re.I)
    if not canon:
        log_warn(f"{name}: canonical mancante")
    elif ".html" in canon.group(1):
        log_err(f"{name}: canonical con .html")

    if '"RealEstateAgent"' not in raw:
        if name.startswith("blog-"):
            if '"BlogPosting"' not in raw and '"@type": "BlogPosting"' not in raw:
                log_err(f"{name}: BlogPosting schema mancante")
        else:
            log_err(f"{name}: schema RealEstateAgent mancante")

    if '"GeoCoordinates"' not in raw:
        log_warn(f"{name}: GeoCoordinates mancante")

    if name != "index.html" and '"BreadcrumbList"' not in raw:
        log_warn(f"{name}: BreadcrumbList mancante")

    if name.startswith("blog-") or name.startswith("zona-"):
        if '"FAQPage"' not in raw:
            log_err(f"{name}: FAQPage mancante")

    if name.startswith("blog-"):
        if "ultimo aggiornamento" not in raw.lower() and "datemodified" not in raw.lower():
            log_warn(f"{name}: freshness timestamp assente")
        if "righetto-sol" not in raw and "Cosa può fare Righetto" not in raw:
            log_warn(f"{name}: sezione Righetto assente")

    bad_href = re.findall(r'href="([^"]*\.html[^"]*)"', raw)
    internal_bad = [h for h in bad_href if not h.startswith("http")]
    if internal_bad:
        log_warn(f"{name}: {len(internal_bad)} link interni con .html")

    text = visible_text(raw)
    if text.count("agenzia immobiliare") > 5:
        log_warn(f"{name}: possibile stuffing 'agenzia immobiliare'")
    padova_hits = len(re.findall(r"\ba\s+padova\b", text)) + len(re.findall(r"\bdi\s+padova\b", text))
    if padova_hits > 10:
        log_warn(f"{name}: possibile stuffing 'a/di Padova'")


def check_skimm() -> None:
    REPORT.append("\n## 2. SKIMM")
    p = ROOT / "TEST-SKILL" / "skimm.json"
    if not p.exists():
        log_err("skimm.json mancante — eseguire build_skimm.py")
        return
    data = json.loads(p.read_text(encoding="utf-8"))
    undefined = [
        a["slug"]
        for a in data.get("articles", [])
        if "da definire" in a.get("angolo", "").lower()
    ]
    dup_kw: dict[str, list[str]] = {}
    for a in data.get("articles", []):
        dup_kw.setdefault(a["kw_primaria"], []).append(a["slug"])
    dups = {k: v for k, v in dup_kw.items() if len(v) > 1}

    log_ok(f"{data.get('count', 0)} articoli catalogati")
    if undefined:
        log_warn(f"{len(undefined)} angoli ancora generici")
    else:
        log_ok("Tutti gli angoli editoriali definiti")
    if dups:
        for kw, slugs in dups.items():
            log_err(f"kw_primaria duplicata `{kw}`: {', '.join(slugs)}")


def check_pillar_links() -> None:
    REPORT.append("\n## 3. Pillar — link blog")
    targets = {
        "servizio-locazioni.html": 3,
        "servizio-valutazioni.html": 2,
        "servizi.html": 2,
        "chi-siamo.html": 1,
    }
    for fname, min_links in targets.items():
        path = ROOT / fname
        if not path.exists():
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        n = len(re.findall(r'href="(?:/)?blog-', raw, re.I))
        if n >= min_links:
            log_ok(f"{fname}: {n} link blog")
        else:
            log_warn(f"{fname}: solo {n} link blog (min {min_links})")


def main() -> int:
    check_global()
    pages = sorted(
        p
        for p in ROOT.glob("*.html")
        if p.name not in SKIP_HTML
        and not any(p.name.startswith(pref) for pref in SKIP_PREFIXES)
    )
    REPORT.append(f"\n## 4. Pagine HTML ({len(pages)})")
    for p in pages:
        raw = p.read_text(encoding="utf-8", errors="replace")
        if is_redirect_stub(raw) or is_demo_noindex(raw, p.name):
            continue
        check_page(p)

    check_skimm()
    check_pillar_links()

    total = OK + WARNINGS + ERRORS
    health = (OK * 100 // total) if total else 100

    header = [
        "# Google Compliance Check — Righetto",
        f"Salute: {health}% | OK {OK} | WARN {WARNINGS} | ERR {ERRORS}",
        "",
    ]
    out = "\n".join(header + REPORT) + "\n"
    out_path = ROOT / "google-compliance-report.md"
    out_path.write_text(out, encoding="utf-8")

    try:
        print(out)
    except UnicodeEncodeError:
        print(out.encode("ascii", errors="replace").decode("ascii"))

    gh = os.environ.get("GITHUB_OUTPUT")
    if gh:
        with open(gh, "a", encoding="utf-8") as f:
            f.write(f"health={health}\nerrors={ERRORS}\nwarnings={WARNINGS}\nok={OK}\n")

    print(f"\nReport: {out_path}")
    return 1 if ERRORS > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
