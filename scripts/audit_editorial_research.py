#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit ricerca editoriale — gate pre-scrittura blog (skill-editoriale-visivo §8-17)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "data" / "editorial-queue.json"

REQUIRED_SCHEDULED = (
    "research_refs",
    "hype_sources_read",
    "gap_analysis",
    "value_add",
    "editorial_type",
    "monitoring_area",
    "substantive_area",
    "main_question",
    "reader_novelty",
)


def audit_item(item: dict) -> list[str]:
    issues: list[str] = []
    status = item.get("status", "")
    if status not in ("scheduled", "proposed"):
        return issues

    iid = item.get("id", "?")

    for field in REQUIRED_SCHEDULED:
        val = item.get(field)
        if val is None or val == "" or val == []:
            issues.append(f"{iid}: campo obbligatorio mancante: {field}")

    refs = item.get("research_refs") or []
    if len(refs) < 2:
        issues.append(f"{iid}: research_refs {len(refs)}/2 minimo")

    hype = item.get("hype_sources_read") or []
    if len(hype) < 1:
        issues.append(f"{iid}: hype_sources_read vuoto (analisi top web)")

    et = item.get("editorial_type", "")
    if et not in ("trend", "evergreen"):
        issues.append(f"{iid}: editorial_type deve essere 'trend' o 'evergreen'")

    ma = item.get("monitoring_area", "")
    if not ma:
        issues.append(f"{iid}: monitoring_area assente (mercato/politica/normativa)")

    va = str(item.get("value_add", "")).strip()
    if len(va) < 20:
        issues.append(f"{iid}: value_add troppo breve (<20 caratteri utili)")

    gap = str(item.get("gap_analysis", "")).strip()
    if len(gap) < 15:
        issues.append(f"{iid}: gap_analysis troppo breve")

    sa = str(item.get("substantive_area", "")).strip()
    if not sa:
        issues.append(f"{iid}: substantive_area mancante (§16-TER)")

    mq = str(item.get("main_question", "")).strip()
    if len(mq) < 15:
        issues.append(f"{iid}: main_question troppo breve (§16-TER)")

    rn = str(item.get("reader_novelty", "")).strip()
    if len(rn) < 20:
        issues.append(f"{iid}: reader_novelty troppo breve (§16-TER)")

    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit ricerca editoriale coda blog")
    ap.add_argument("--id", help="ID item eq-XXX")
    ap.add_argument("--all-scheduled", action="store_true", help="Tutti gli item scheduled")
    args = ap.parse_args()

    if not QUEUE.exists():
        print(f"ERR: {QUEUE} non trovato")
        return 1

    data = json.loads(QUEUE.read_text(encoding="utf-8"))
    items = data.get("items", [])

    if args.id:
        items = [i for i in items if i.get("id") == args.id]
        if not items:
            print(f"ERR: id {args.id} non trovato")
            return 1

    if args.all_scheduled:
        items = [i for i in items if i.get("status") == "scheduled"]

    if not args.id and not args.all_scheduled:
        ap.print_help()
        return 2

    total_err = 0
    for item in items:
        issues = audit_item(item)
        slug = item.get("slug", item.get("id", "?"))
        if issues:
            total_err += 1
            print(f"FAIL {slug}:")
            for iss in issues:
                print(f"  - {iss}")
        else:
            print(f"OK   {slug}")

    if total_err:
        print(f"\nESITO: {total_err} item con gap ricerca editoriale")
        print("Compila campi in data/editorial-queue.json (Appendice B skill-editoriale-visivo.md)")
        return 1
    print(f"\nESITO: OK — ricerca editoriale documentata")
    return 0


if __name__ == "__main__":
    sys.exit(main())
