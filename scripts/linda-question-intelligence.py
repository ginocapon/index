#!/usr/bin/env python3
"""Question intelligence Linda — aggregato da FAQ archive, GSC, editorial queue (privacy-safe)."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "data/linda-faq-archive.jsonl"
GSC = ROOT / "data/gsc-keywords-priority.json"
QUEUE = ROOT / "data/editorial-queue.json"
OUT = ROOT / "data/linda-question-intelligence-latest.json"
REPORT = ROOT / "linda-question-intelligence-report.md"

INTENT_MAP = {
    "mutuo": "mutui-cluster",
    "affitto": "affitti-cluster",
    "vendita": "vendere-cluster",
    "limena": "territorio-limena",
    "documenti": "documenti-operativi",
    "rogito": "documenti-operativi",
    "ape": "green-ape-acquisto",
    "prima casa": "fisco-prima-casa",
}


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def classify_intent(q: str) -> str:
    low = q.lower()
    for kw, intent in INTENT_MAP.items():
        if kw in low:
            return intent
    return "altri-trasversali"


def main() -> int:
    archive = load_jsonl(ARCHIVE)
    questions = [a.get("question", "") for a in archive if a.get("question")]
    top = Counter(questions).most_common(30)

    emerging = []
    seen = set()
    for item in reversed(archive[-40:]):
        q = item.get("question", "")
        if q and q not in seen:
            seen.add(q)
            emerging.append({"question": q, "source": item.get("source"), "blog": item.get("blog")})

    gsc = json.loads(GSC.read_text(encoding="utf-8")) if GSC.exists() else {}
    gsc_kw = []
    if isinstance(gsc.get("keywords"), list):
        gsc_kw = [k.get("query", k) if isinstance(k, dict) else k for k in gsc["keywords"][:25]]
    elif isinstance(gsc.get("queries_limena_top_volume"), list):
        gsc_kw = gsc["queries_limena_top_volume"][:15]

    content_ops = []
    location_demand = Counter()
    feature_demand = Counter()
    budget_signals = 0

    for item in archive:
        q = item.get("question", "").lower()
        for loc in ("padova", "limena", "vigonza", "abano", "arcella", "guizza"):
            if loc in q:
                location_demand[loc] += 1
        for feat in ("garage", "giardino", "terrazzo", "camere", "mutuo", "affitto"):
            if feat in q:
                feature_demand[feat] += 1
        if "budget" in q or "massimo" in q or "€" in q:
            budget_signals += 1
        intent = classify_intent(q)
        content_ops.append({
            "question": item.get("question", "")[:120],
            "intent": intent,
            "content_opportunity": f"FAQ Linda + articolo/aggiornamento {intent}",
            "seo_opportunity": item.get("blog") or f"long-tail-{intent}",
            "lead_opportunity": "visita" in q or "contatt" in q,
        })

    # dedupe content ops
    content_ops = content_ops[:40]

    out = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "top_questions": [{"question": q, "count": c} for q, c in top[:20]],
        "emerging_questions": emerging[:20],
        "unanswered_questions": [],
        "property_demand": dict(feature_demand.most_common(10)),
        "location_demand": dict(location_demand.most_common(10)),
        "feature_demand": dict(feature_demand.most_common(10)),
        "budget_demand_signals": budget_signals,
        "gsc_priority_sample": gsc_kw[:15],
        "content_opportunities": content_ops[:25],
        "seo_opportunities": [
            {"kw": k, "action": "pillar/refresh o nuovo angolo SKIMM"} for k in gsc_kw[:10]
        ],
        "lead_opportunities": [c for c in content_ops if c.get("lead_opportunity")][:10],
        "policy": "yellow",
        "note": "Aggregato da FAQ archive — no transcript chat raw (privacy).",
    }

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Linda Question Intelligence",
        f"\nGenerato: {out['generated_at']}\n",
        f"- Archive entries: {len(archive)}",
        f"- TOP questions: {len(out['top_questions'])}",
        f"- Location demand: {out['location_demand']}",
        f"- Feature demand: {out['feature_demand']}",
        "\n## Content opportunities (sample)\n",
    ]
    for c in content_ops[:10]:
        lines.append(f"- {c['question'][:80]} → {c['intent']}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"OK: question intelligence ({len(archive)} archive rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
