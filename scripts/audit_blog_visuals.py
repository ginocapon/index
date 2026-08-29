#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit visivo blog — min 3 foto corpo, 2 SVG, 2 tabelle, marchio IA."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

MIN_BODY_FIGURES = 3
MIN_CHARTS = 2
MIN_TABLES = 2


def audit_file(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    issues: list[str] = []

    body_figs = len(re.findall(r'<figure[^>]*class="[^"]*blog-fig', raw, re.I))
    if body_figs < MIN_BODY_FIGURES:
        issues.append(f"figure corpo blog-fig: {body_figs}/{MIN_BODY_FIGURES}")

    charts = len(re.findall(r'class="chart-wrap"', raw, re.I))
    if charts < MIN_CHARTS:
        issues.append(f"grafici chart-wrap: {charts}/{MIN_CHARTS}")

    tables = len(re.findall(r"<table\b", raw, re.I))
    if tables < MIN_TABLES:
        issues.append(f"tabelle HTML: {tables}/{MIN_TABLES}")

    hero = bool(re.search(r'class="[^"]*art-hero', raw, re.I))
    if not hero:
        issues.append("hero art-hero assente")

    ai_marks = len(re.findall(r'data-ai-generated\s*=\s*["\']true["\']', raw, re.I))
    img_blog = len(re.findall(r'img/blog/[^"\']+\.webp', raw, re.I))
    if img_blog and ai_marks < min(img_blog, body_figs + 1):
        issues.append(f"marchio data-ai-generated: {ai_marks} su ~{img_blog} img/blog")

    if not re.search(r'rig-ai-photo-wrap', raw, re.I):
        issues.append("rig-ai-photo-wrap assente")

    figcaptions = len(re.findall(r"<figcaption", raw, re.I))
    if figcaptions < MIN_BODY_FIGURES + MIN_CHARTS:
        issues.append(f"figcaption: {figcaptions} (attesi >={MIN_BODY_FIGURES + MIN_CHARTS})")

    if re.search(r'img/immobili/', raw, re.I):
        issues.append("vietato img/immobili/ nel blog editoriale")

    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit visivo articoli blog Righetto")
    ap.add_argument("--file", help="Singolo blog-*.html")
    ap.add_argument("--all", action="store_true", help="Tutti i blog-*.html in root")
    args = ap.parse_args()

    if args.file:
        paths = [ROOT / args.file]
    elif args.all:
        paths = sorted(ROOT.glob("blog-*.html"))
    else:
        ap.print_help()
        return 2

    total_err = 0
    for p in paths:
        if not p.exists():
            print(f"ERR {p.name}: file non trovato")
            total_err += 1
            continue
        issues = audit_file(p)
        if issues:
            total_err += 1
            print(f"FAIL {p.name}:")
            for i in issues:
                print(f"  - {i}")
        else:
            print(f"OK   {p.name}")

    if total_err:
        print(f"\nESITO: {total_err} articolo/i con gap visivi")
        return 1
    print(f"\nESITO: OK — {len(paths)} articolo/i conformi")
    return 0


if __name__ == "__main__":
    sys.exit(main())
