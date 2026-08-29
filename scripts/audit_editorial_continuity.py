#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit continuita e diversificazione sostanziale blog (skill-editoriale-visivo §16-TER)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEMORY = ROOT / "data" / "editorial-memory.json"
QUEUE = ROOT / "data" / "editorial-queue.json"

REQUIRED_PROPOSED = (
    "substantive_area",
    "main_question",
    "reader_novelty",
)


def load_memory() -> dict:
    if not MEMORY.exists():
        return {"recent_articles": [], "saturation_threshold": 2, "saturation_window": 8}
    return json.loads(MEMORY.read_text(encoding="utf-8"))


def count_area(memory: dict, area: str) -> int:
    window = memory.get("recent_articles", [])[: memory.get("saturation_window", 8)]
    return sum(1 for a in window if a.get("substantive_area") == area)


def audit_proposal(item: dict, memory: dict) -> list[str]:
    issues: list[str] = []
    iid = item.get("id", item.get("slug", "?"))
    status = item.get("status", "proposed")

    if status not in ("scheduled", "proposed"):
        return issues

    area = item.get("substantive_area", "").strip()
    if not area:
        issues.append(f"{iid}: substantive_area mancante (Appendice C skill-editoriale-visivo)")
    elif area not in memory.get("areas_taxonomy", []) and area != "ALTRO":
        issues.append(f"{iid}: substantive_area '{area}' non in tassonomia")

    mq = str(item.get("main_question", "")).strip()
    if len(mq) < 15:
        issues.append(f"{iid}: main_question troppo breve — quale domanda affronta?")

    rn = str(item.get("reader_novelty", "")).strip()
    if len(rn) < 20:
        issues.append(f"{iid}: reader_novelty mancante — perche un lettore abituale lo leggerebbe?")

    if area:
        cnt = count_area(memory, area)
        threshold = memory.get("saturation_threshold", 2)
        if cnt >= threshold:
            ur = str(item.get("update_reason", "")).strip()
            if len(ur) < 30:
                issues.append(
                    f"{iid}: area {area} gia {cnt}x negli ultimi "
                    f"{memory.get('saturation_window', 8)} — serve update_reason "
                    f"(nuovo dato/norma/cambiamento concreto)"
                )
            else:
                print(f"  INFO {iid}: rientro su {area} giustificato da update_reason")

    diff = str(item.get("different_from", "")).strip()
    slug = item.get("slug", "")
    if diff and diff.replace("blog-", "") in slug.replace("blog-", ""):
        issues.append(f"{iid}: different_from troppo simile allo slug proposto")

    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit continuita editoriale §16-TER")
    ap.add_argument("--id", help="ID item coda eq-XXX")
    ap.add_argument("--report", action="store_true", help="Solo report saturazione")
    ap.add_argument("--rebuild", action="store_true", help="Rigenera editorial-memory.json")
    args = ap.parse_args()

    if args.rebuild:
        import subprocess

        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_editorial_memory.py")],
            cwd=str(ROOT),
        )
        if r.returncode != 0:
            return r.returncode

    memory = load_memory()

    if args.report:
        print("=== Saturazione tematica (ultimi articoli) ===")
        for k, v in memory.get("saturation_counts_last_8", {}).items():
            flag = " SATURATA" if v >= memory.get("saturation_threshold", 2) else ""
            print(f"  {k}: {v}{flag}")
        print(f"\nMemoria: {len(memory.get('recent_articles', []))} articoli")
        return 0

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
    else:
        items = [i for i in items if i.get("status") in ("scheduled", "proposed")]

    if not args.id and not items:
        print("OK: nessun item scheduled/proposed da verificare")
        return 0

    total_err = 0
    for item in items:
        issues = audit_proposal(item, memory)
        slug = item.get("slug", item.get("id", "?"))
        if issues:
            total_err += 1
            print(f"FAIL {slug}:")
            for iss in issues:
                print(f"  - {iss}")
        else:
            print(f"OK   {slug}")

    if total_err:
        print(f"\nESITO: {total_err} proposta/e con gap continuita sostanziale")
        print("Leggi skill-editoriale-visivo.md §16-TER e data/editorial-memory.json")
        return 1
    print("\nESITO: OK — diversificazione sostanziale verificata")
    return 0


if __name__ == "__main__":
    sys.exit(main())
