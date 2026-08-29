#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit equilibrio acquisizione proprietari — skill-acquisizione-proprietari.md."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE = ROOT / "data" / "editorial-queue.json"
BALANCE = ROOT / "data" / "editorial-acquisition-balance.json"

VALID_AUDIENCE = {
    "proprietario_vendita",
    "proprietario_locazione",
    "proprietario_gestione",
    "proprietario_misto",
    "acquirente",
    "inquilino",
    "investitore",
    "misto",
}
VALID_CONTRIBUTION = {"direct", "indirect", "none"}
VALID_TRAFFIC = {"strategic", "generic"}


def audit_item(item: dict) -> list[str]:
    issues: list[str] = []
    status = item.get("status", "")
    if status not in ("scheduled", "proposed"):
        return issues

    iid = item.get("id", "?")
    pa = str(item.get("primary_audience", "")).strip()
    if pa not in VALID_AUDIENCE:
        issues.append(f"{iid}: primary_audience mancante o invalido (acquisizione proprietari)")

    ac = str(item.get("acquisition_contribution", "")).strip()
    if ac not in VALID_CONTRIBUTION:
        issues.append(f"{iid}: acquisition_contribution mancante (direct/indirect/none)")

    tt = str(item.get("traffic_type", "")).strip()
    if tt not in VALID_TRAFFIC:
        issues.append(f"{iid}: traffic_type mancante (strategic/generic)")

    op = str(item.get("owner_problem", "")).strip()
    if len(op) < 12:
        issues.append(f"{iid}: owner_problem troppo breve — quale esigenza reale?")

    cv = str(item.get("concrete_value", "")).strip()
    if len(cv) < 15:
        issues.append(f"{iid}: concrete_value troppo breve")

    if ac == "none" and tt == "generic" and not item.get("gsc_sostenere"):
        issues.append(
            f"{iid}: contribution=none + traffic=generic — non prioritario per acquisizione "
            "(salvo refresh GSC owner)"
        )

    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit acquisizione proprietari coda blog")
    ap.add_argument("--id", help="eq-XXX")
    ap.add_argument("--all-scheduled", action="store_true")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()

    if args.report and BALANCE.exists():
        data = json.loads(BALANCE.read_text(encoding="utf-8"))
        print("=== Equilibrio editoriale acquisizione ===")
        print(f"Regola ciclo: {data.get('cycle_rule', '')}")
        last8 = data.get("last_8_classification", {})
        for k, v in last8.items():
            print(f"  {k}: {v}")
        if data.get("imbalance_alert"):
            print(f"ATTENZIONE: {data['imbalance_alert']}")
        gaps = data.get("owner_pillar_gaps", [])
        if gaps:
            print("\nGap pillar owner:")
            for g in gaps[:8]:
                print(f"  - {g}")
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

    if args.all_scheduled:
        items = [i for i in items if i.get("status") in ("scheduled", "proposed")]

    all_issues: list[str] = []
    for item in items:
        all_issues.extend(audit_item(item))

    if not all_issues:
        label = args.id or "scheduled/proposed"
        print(f"OK   {label}")
        return 0

    label = args.id or "coda"
    print(f"FAIL {label}:")
    for iss in all_issues:
        print(f"  - {iss}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
