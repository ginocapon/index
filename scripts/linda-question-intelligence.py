#!/usr/bin/env python3
"""Question intelligence Linda — FAQ archive, GSC, intent log anonimi Supabase."""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "data/linda-faq-archive.jsonl"
GSC = ROOT / "data/gsc-keywords-priority.json"
QUEUE = ROOT / "data/editorial-queue.json"
INTENTS = ROOT / "data/linda-intents-snapshot-latest.json"
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


def load_intents_snapshot() -> dict:
    if not INTENTS.exists():
        return {}
    try:
        return json.loads(INTENTS.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


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

    intents_snap = load_intents_snapshot()
    chat_topics = intents_snap.get("top_topic_labels", [])
    chat_location = intents_snap.get("location_demand", {})
    chat_operation = intents_snap.get("operation_demand", {})
    chat_budget = intents_snap.get("budget_bands", {})
    chat_total = intents_snap.get("total_events", 0)

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

    # Merge real chat location/operation demand
    for loc, cnt in chat_location.items():
        location_demand[loc] += cnt
    for op, cnt in chat_operation.items():
        if op:
            feature_demand[f"op_{op}"] += cnt
    budget_signals += sum(chat_budget.values())

    # Chat topics as emerging if not in archive
    archive_q_lower = {q.lower() for q in questions}
    for t in chat_topics[:15]:
        label = t.get("label", "")
        if label and label not in archive_q_lower and label not in ("saluto", "unmatched", "contatto"):
            emerging.insert(0, {
                "question": f"[chat] topic: {label}",
                "source": "linda_chat_intents",
                "count": t.get("count"),
            })

    content_ops = content_ops[:40]

    note_parts = ["Aggregato da FAQ archive"]
    if chat_total:
        note_parts.append(f"intent log {chat_total} eventi (14d)")
    else:
        note_parts.append("intent log non disponibile (tabella o SUPABASE_KEY)")

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
        "chat_intents": {
            "available": intents_snap.get("available", False),
            "total_events_14d": chat_total,
            "top_topic_labels": chat_topics[:15],
            "location_demand": chat_location,
            "operation_demand": chat_operation,
            "budget_bands": chat_budget,
            "unique_msg_hashes": intents_snap.get("unique_msg_hashes"),
        },
        "content_opportunities": content_ops[:25],
        "seo_opportunities": [
            {"kw": k, "action": "pillar/refresh o nuovo angolo SKIMM"} for k in gsc_kw[:10]
        ],
        "lead_opportunities": [c for c in content_ops if c.get("lead_opportunity")][:10],
        "policy": "yellow",
        "note": " — ".join(note_parts),
    }

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Linda Question Intelligence",
        f"\nGenerato: {out['generated_at']}\n",
        f"- Archive entries: {len(archive)}",
        f"- Chat intents (14d): {chat_total}",
        f"- TOP questions: {len(out['top_questions'])}",
        f"- Location demand: {out['location_demand']}",
        f"- Feature demand: {out['feature_demand']}",
        "\n## Chat top topics\n",
    ]
    for t in chat_topics[:8]:
        lines.append(f"- {t.get('label')}: {t.get('count')}")
    lines.append("\n## Content opportunities (sample)\n")
    for c in content_ops[:10]:
        lines.append(f"- {c['question'][:80]} → {c['intent']}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"OK: question intelligence ({len(archive)} archive, {chat_total} chat intents)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
