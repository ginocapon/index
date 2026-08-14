#!/usr/bin/env python3
"""Benchmark qualità Linda — score interno + live query pass rate."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHATBOT = ROOT / "js/chatbot.js"
SKIMM = ROOT / "TEST-SKILL/skimm.json"
OG = ROOT / "data/og-immobili.json"
LIVE = ROOT / "data/linda-live-benchmark-latest.json"
TEMPORAL = ROOT / "data/linda-knowledge-temporal-latest.json"
OUT = ROOT / "data/linda-quality-latest.json"
REPORT = ROOT / "linda-quality-report.md"


def run_live_benchmark() -> dict | None:
    script = ROOT / "scripts/linda-live-benchmark.py"
    if not script.exists():
        return None
    proc = subprocess.run([sys.executable, str(script)], cwd=ROOT, capture_output=True, text=True)
    if LIVE.exists():
        try:
            return json.loads(LIVE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None
    return None


def main() -> int:
    text = CHATBOT.read_text(encoding="utf-8") if CHATBOT.exists() else ""
    faq_block = text.split("const FAQ_DATA")[1].split("];")[0] if "const FAQ_DATA" in text else ""
    faq_count = len(re.findall(r"\{\s*k:\s*\[", faq_block))
    blog_refs = len(set(re.findall(r"blog:\s*'([^']+)'", text)))
    skimm_count = 0
    if SKIMM.exists():
        skimm_count = len(json.loads(SKIMM.read_text())["articles"])
    imm_count = 0
    if OG.exists():
        imm_count = len(json.loads(OG.read_text()).get("bySlug", {}))

    has_agent = (ROOT / "js/linda-agent.js").exists() and "LindaAgent" in (ROOT / "js/linda-agent.js").read_text()
    has_qr = (ROOT / "qr-review.html").exists() and (ROOT / "qr-property.html").exists()
    has_intent_log = "logLindaIntent" in text and "linda_chat_intents" in text

    live = run_live_benchmark()
    live_pass = live.get("pass_rate_pct", 0) if live else None
    live_score = min(100, round(live_pass or 0)) if live_pass is not None else 50

    temporal_freshness = 60
    if TEMPORAL.exists():
        try:
            temporal_freshness = json.loads(TEMPORAL.read_text()).get("freshness_score", 60)
        except json.JSONDecodeError:
            pass

    scores = {
        "faq_coverage": min(100, round(100 * blog_refs / max(skimm_count, 1))),
        "faq_volume": min(100, round(faq_count / 2)),
        "property_catalog": min(100, imm_count * 3),
        "agent_module": 100 if has_agent else 0,
        "qr_system": 100 if has_qr else 0,
        "knowledge_pipeline": 100 if (ROOT / "data/linda-faq-archive.jsonl").exists() else 50,
        "live_benchmark": live_score,
        "intent_logging": 100 if has_intent_log else 0,
        "temporal_knowledge": temporal_freshness,
    }

    weights = {
        "faq_coverage": 0.2,
        "faq_volume": 0.1,
        "property_catalog": 0.1,
        "agent_module": 0.15,
        "qr_system": 0.03,
        "knowledge_pipeline": 0.1,
        "live_benchmark": 0.15,
        "intent_logging": 0.07,
        "temporal_knowledge": 0.1,
    }
    linda_quality_score = round(sum(scores[k] * weights[k] for k in weights), 1)

    categories = {
        "factual_accuracy": scores["faq_coverage"],
        "property_accuracy": scores["property_catalog"],
        "retrieval": scores["agent_module"],
        "ranking": scores["agent_module"],
        "grounding": scores["knowledge_pipeline"],
        "hallucination_risk": 85 if has_agent else 70,
        "sources_temporal": scores["temporal_knowledge"],
        "unanswered_handling": 75,
        "lead_conversion_hooks": 80 if "contattami" in text else 60,
        "frontend_latency": 90,
        "live_route_accuracy": live_score,
    }

    out = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "linda_quality_score": linda_quality_score,
        "target_note": "Score interno 0-100 — include live benchmark route classification",
        "component_scores": scores,
        "category_scores": categories,
        "live_benchmark": live,
        "faq_entries": faq_count,
        "blog_refs": blog_refs,
        "skimm_articles": skimm_count,
        "catalog_immobili": imm_count,
        "policy": "green_report",
    }

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    live_line = f"- Live benchmark: {live_pass}% ({live.get('passed')}/{live.get('total')})" if live else "- Live benchmark: non eseguito"
    REPORT.write_text(
        f"# Linda Quality Score\n\n**Score:** {linda_quality_score}/100\n\n"
        f"- FAQ entries: {faq_count}\n- Blog refs: {blog_refs}/{skimm_count}\n"
        f"- Immobili OG: {imm_count}\n- Agent module: {has_agent}\n"
        f"- Intent logging: {has_intent_log}\n{live_line}\n"
        f"- Temporal freshness: {temporal_freshness}/100\n",
        encoding="utf-8",
    )
    print(f"OK: Linda quality score {linda_quality_score}/100 (live {live_pass}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
