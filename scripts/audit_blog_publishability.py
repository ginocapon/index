#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit pubblicabilità blog — nessun residuo AI/template visibile (skill-editoriale-visivo §18)."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Titoli / pattern vietati nel contenuto visibile (case-insensitive)
FORBIDDEN_HEADINGS = re.compile(
    r"<h[23][^>]*>\s*("
    r"Further reading|Note operative|Note interne|Istruzioni|Prompt|TODO|Da verificare|"
    r"Da completare|Related content|Additional notes|Internal references|Read more|"
    r"Approfondimento\s+\d+"
    r")\s*</h[23]>",
    re.I,
)

FORBIDDEN_PATTERNS = [
    (re.compile(r"\bFurther reading\b", re.I), "Further reading"),
    (re.compile(r"<h[23][^>]*>\s*Note operative\s*</h[23]>", re.I), "H2/H3 Note operative"),
    (re.compile(r"<h[23][^>]*>\s*Note interne\s*</h[23]>", re.I), "H2/H3 Note interne"),
    (re.compile(r"\bTODO\b|\[DATO\]|\[ZONA\]|\[FONTE\]", re.I), "placeholder/TODO"),
    (re.compile(r"\bApprofondimento\s+\d+\b", re.I), "Approfondimento numerato"),
    (re.compile(r"id=[\"']note-operative[\"']", re.I), "id=note-operative (sezione template)"),
    (re.compile(r"\b(prompt|system:\s|<!--\s*AI)", re.I), "istruzione AI/prompt"),
]

# Solo corpo articolo — esclude head/script/style
ARTICLE_RE = re.compile(
    r'<(?:article|main)[^>]*class="[^"]*art-body[^"]*"[^>]*>([\s\S]*?)</(?:article|main)>',
    re.I,
)
FALLBACK_BODY = re.compile(
    r'<div[^>]*class="[^"]*blog-content[^"]*"[^>]*>([\s\S]*?)</div>',
    re.I,
)


def extract_visible(html: str) -> str:
    m = ARTICLE_RE.search(html)
    if m:
        return m.group(1)
    m = FALLBACK_BODY.search(html)
    if m:
        return m.group(1)
    # fallback: tutto dopo art-hero
    idx = html.find('class="art-body"')
    if idx >= 0:
        start = html.find(">", idx) + 1
        end = html.rfind("</article>")
        if end > start:
            return html[start:end]
    return html


def audit_html(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    visible = extract_visible(raw)
    issues: list[str] = []

    if FORBIDDEN_HEADINGS.search(visible):
        issues.append("titolo sezione vietato (Further reading / Note operative / Approfondimento N…)")

    for pat, label in FORBIDDEN_PATTERNS:
        if pat.search(visible):
            issues.append(label)

    # Paragrafi identici ripetuti ≥3 volte (filler template)
    paras = re.findall(r"<p[^>]*>([\s\S]*?)</p>", visible, re.I)
    seen: dict[str, int] = {}
    for p in paras:
        text = re.sub(r"<[^>]+>", " ", p).strip()
        if len(text) < 40:
            continue
        key = text[:120]
        seen[key] = seen.get(key, 0) + 1
        if seen[key] >= 3:
            issues.append(f"paragrafo ripetuto ≥3 volte: «{text[:60]}…»")
            break

    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit pubblicabilità blog §18")
    ap.add_argument("--file", help="Singolo blog-*.html")
    ap.add_argument("--all", action="store_true", help="Tutti i blog-*.html in root")
    ap.add_argument("--report", action="store_true", help="Solo elenco file con problemi")
    args = ap.parse_args()

    if args.file:
        paths = [ROOT / args.file if not Path(args.file).is_absolute() else Path(args.file)]
    elif args.all:
        paths = sorted(ROOT.glob("blog-*.html"))
    else:
        ap.print_help()
        return 2

    total_fail = 0
    for path in paths:
        if not path.is_file():
            print(f"ERR: {path} non trovato")
            total_fail += 1
            continue
        issues = audit_html(path)
        if issues:
            total_fail += 1
            if args.report:
                print(path.name)
            else:
                print(f"FAIL {path.name}:")
                for iss in issues:
                    print(f"  - {iss}")
        elif not args.report:
            print(f"OK   {path.name}")

    if total_fail:
        print(f"\nESITO: {total_fail} file con residui non pubblicabili")
        print("Vedi skill-editoriale-visivo.md §18 — bonifica prima di publish")
        return 1
    print(f"\nESITO: OK — {len(paths)} file pubblicabili")
    return 0


if __name__ == "__main__":
    sys.exit(main())
