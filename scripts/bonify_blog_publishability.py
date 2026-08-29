#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bonifica blog — rimuove residui template/AI visibili (skill-editoriale-visivo §18)."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FORBIDDEN_H = re.compile(
    r"<h[23][^>]*(?:id=[\"']note-operative[\"'])?[^>]*>\s*"
    r"(?:Further reading|Note operative|Note interne|Istruzioni|Prompt|TODO|"
    r"Da verificare|Da completare|Related content|Additional notes|"
    r"Internal references|Read more|Approfondimento\s+\d+)\s*</h[23]>\s*",
    re.I,
)

P_APPROFONDIMENTO = re.compile(
    r"<p[^>]*>[\s\S]*?\bapprofondimento\s+\d+\b[\s\S]*?</p>\s*",
    re.I,
)

P_FILLER_ADE = re.compile(
    r"<p[^>]*>[\s\S]*?incrociare fonti ADE, OMI o ISTAT; distinguere fatto normativo[\s\S]*?</p>\s*",
    re.I,
)

P_PLACEHOLDER = re.compile(r"\[(?:DATO|ZONA|FONTE)\]")


def _strip_tags(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def dedupe_paragraphs(html: str) -> str:
    """Rimuove paragrafi <p> con testo identico (normalizzato)."""
    seen: set[str] = set()

    def repl(m: re.Match[str]) -> str:
        inner = m.group(1)
        key = _strip_tags(inner)[:200]
        if len(key) < 35:
            return m.group(0)
        if key in seen:
            return ""
        seen.add(key)
        return m.group(0)

    return re.sub(r"<p([^>]*)>([\s\S]*?)</p>\s*", repl, html, flags=re.I)


def bonify(html: str) -> tuple[str, int]:
    changes = 0
    orig = html

    for _ in range(50):
        new = FORBIDDEN_H.sub("", html)
        if new != html:
            changes += 1
        html = new

    for pat in (P_APPROFONDIMENTO, P_FILLER_ADE):
        new = pat.sub("", html)
        if new != html:
            changes += len(pat.findall(orig))
        html = new

    if P_PLACEHOLDER.search(html):
        changes += 1
        html = P_PLACEHOLDER.sub("", html)

    before = html
    html = dedupe_paragraphs(html)
    if html != before:
        changes += 1

    # Rimuovi blocchi vuoti multipli
    html = re.sub(r"\n{4,}", "\n\n\n", html)

    return html, changes


def main() -> int:
    ap = argparse.ArgumentParser(description="Bonifica pubblicabilità blog §18")
    ap.add_argument("--file", help="Singolo blog-*.html")
    ap.add_argument("--all", action="store_true", help="Tutti blog-*.html")
    ap.add_argument("--dry-run", action="store_true", help="Solo report, no scrittura")
    args = ap.parse_args()

    if args.file:
        paths = [ROOT / args.file]
    elif args.all:
        paths = sorted(ROOT.glob("blog-*.html"))
    else:
        ap.print_help()
        return 2

    total = 0
    for path in paths:
        if not path.is_file():
            print(f"SKIP {path.name}: non trovato")
            continue
        raw = path.read_text(encoding="utf-8", errors="replace")
        cleaned, n = bonify(raw)
        if n == 0:
            print(f"OK   {path.name} (già pulito)")
            continue
        total += 1
        if args.dry_run:
            print(f"DRY  {path.name}: {n} interventi")
        else:
            path.write_text(cleaned, encoding="utf-8")
            print(f"FIX  {path.name}: {n} interventi")

    print(f"\nBonifica: {total} file modificati su {len(paths)}")
    if not args.dry_run and total:
        print("Esegui: python scripts/audit_blog_publishability.py --all")
    return 0


if __name__ == "__main__":
    sys.exit(main())
