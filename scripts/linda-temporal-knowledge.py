#!/usr/bin/env python3
"""
Valida knowledge temporale Linda — source, last_verified, review_date.
Output: data/linda-knowledge-temporal-latest.json + report (proposals YELLOW, no auto-publish).
"""
from __future__ import annotations

import json
from datetime import datetime, date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data/linda-knowledge-temporal.json"
OUT = ROOT / "data/linda-knowledge-temporal-latest.json"
REPORT = ROOT / "linda-temporal-knowledge-report.md"

REQUIRED = ("id", "topic", "summary", "source", "last_verified", "review_date", "status", "confidence")


def parse_date(s: str) -> date | None:
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def validate_entry(entry: dict) -> list[str]:
    issues = []
    for field in REQUIRED:
        if not entry.get(field):
            issues.append(f"missing_{field}")
    lv = parse_date(entry.get("last_verified", ""))
    rd = parse_date(entry.get("review_date", ""))
    if lv and rd and lv > rd:
        issues.append("last_verified_after_review_date")
    status = entry.get("status", "")
    if status not in ("approved", "proposal", "deprecated"):
        issues.append("invalid_status")
    if status == "approved" and not entry.get("source_url"):
        issues.append("approved_without_source_url")
    return issues


def main() -> int:
    if not SOURCE.exists():
        print("SKIP: linda-knowledge-temporal.json missing")
        return 0

    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    today = date.today()
    entries = data.get("entries", [])
    proposals = data.get("proposals", [])

    approved = []
    overdue = []
    issues_all = []

    for e in entries:
        issues = validate_entry(e)
        if issues:
            issues_all.append({"id": e.get("id"), "issues": issues})
        rd = parse_date(e.get("review_date", ""))
        if rd and rd < today and e.get("status") == "approved":
            overdue.append({
                "id": e.get("id"),
                "topic": e.get("topic"),
                "review_date": e.get("review_date"),
                "last_verified": e.get("last_verified"),
            })
        if e.get("status") == "approved" and not issues:
            approved.append(e)

    proposal_issues = []
    for p in proposals:
        pi = validate_entry(p)
        if pi:
            proposal_issues.append({"id": p.get("id"), "issues": pi})

    freshness_score = 100
    if entries:
        overdue_ratio = len(overdue) / max(len([e for e in entries if e.get("status") == "approved"]), 1)
        freshness_score = max(0, round(100 - overdue_ratio * 40))

    out = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source_file": "data/linda-knowledge-temporal.json",
        "approved_count": len(approved),
        "proposal_count": len(proposals),
        "overdue_review": overdue,
        "validation_issues": issues_all,
        "proposal_validation_issues": proposal_issues,
        "freshness_score": freshness_score,
        "policy": "yellow_proposals_green_report",
        "approved_entries": [
            {
                "id": e["id"],
                "topic": e["topic"],
                "source": e["source"],
                "last_verified": e["last_verified"],
                "review_date": e["review_date"],
                "confidence": e["confidence"],
            }
            for e in approved
        ],
    }

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Linda Temporal Knowledge",
        f"\nGenerato: {out['generated_at']}\n",
        f"- Approved: {out['approved_count']}",
        f"- Proposals (YELLOW): {out['proposal_count']}",
        f"- Freshness score: {freshness_score}/100",
        f"- Overdue review: {len(overdue)}",
    ]
    if overdue:
        lines.append("\n## Overdue review\n")
        for o in overdue:
            lines.append(f"- {o['id']}: review {o['review_date']}")
    if issues_all:
        lines.append("\n## Validation issues\n")
        for i in issues_all:
            lines.append(f"- {i['id']}: {', '.join(i['issues'])}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"OK: temporal knowledge — approved {len(approved)}, overdue {len(overdue)}, freshness {freshness_score}")
    return 0 if not issues_all else 0


if __name__ == "__main__":
    raise SystemExit(main())
