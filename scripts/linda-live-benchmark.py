#!/usr/bin/env python3
"""
Live benchmark Linda — classifica route attesa vs simulata (FAQ keyword + agent intent).
Output: data/linda-live-benchmark-latest.json
"""
from __future__ import annotations

import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUERIES = ROOT / "data/linda-benchmark-queries.json"
CHATBOT = ROOT / "js/chatbot.js"
OUT = ROOT / "data/linda-live-benchmark-latest.json"
REPORT = ROOT / "linda-live-benchmark-report.md"

AGENT_CHECK = """
const fs=require('fs');const vm=require('vm');
const sandbox={window:{}};
vm.runInNewContext(fs.readFileSync('js/linda-agent.js','utf8'),sandbox);
const LA=sandbox.window.LindaAgent;
const q=process.argv[1];
const i=LA.parseSearchIntent(q);
const ok=i.isPropertySearch&&(i.location||i.budget_max||i.rooms||i.property_type||i.operation);
process.stdout.write(ok?'search':'');
"""


def load_faq_keywords() -> list[tuple[list[str], str]]:
    text = CHATBOT.read_text(encoding="utf-8")
    if "const FAQ_DATA" not in text:
        return []
    block = text.split("const FAQ_DATA")[1].split("];")[0]
    entries = []
    for m in re.finditer(r"k:\s*\[([^\]]+)\]", block):
        keys = re.findall(r"'([^']+)'", m.group(1))
        if keys:
            entries.append((keys, keys[0]))
    return entries


def fuzzy_match_keyword(low: str, keywords: list[str]) -> bool:
    if any(k in low for k in keywords):
        return True
    words = [w for w in low.split() if len(w) >= 3]
    for kw in keywords:
        for w in words:
            if len(w) <= 2:
                continue
            if kw == w or (len(kw) > 4 and kw in low):
                return True
    return False


def is_agent_search(q: str) -> bool:
    agent = subprocess.run(
        ["node", "-e", AGENT_CHECK, q],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return agent.stdout.strip() == "search"


def classify_route(q: str, faq_entries: list[tuple[list[str], str]]) -> str:
    low = q.lower().strip()
    if re.match(r"^(ciao|salve|buongiorno|buonasera|hey|hi|hello)", low):
        return "saluto"
    if re.search(r"contatt|chiamat|appuntam|richiama|voglio essere contattato", low):
        return "contatto"
    if re.search(r"stim|valut", low) and "cerco" not in low and "immobil" not in low:
        return "stima"
    if is_agent_search(q):
        return "search"
    for keys, _ in faq_entries:
        if fuzzy_match_keyword(low, keys):
            return "faq"
    if re.search(r"cerca|trov|immobi|annunci|vedete|avete|list|casa|appartam|villa|bilocale", low):
        return "ricerca_guidata"
    return "default"


def main() -> int:
    queries = json.loads(QUERIES.read_text(encoding="utf-8"))["queries"]
    faq_entries = load_faq_keywords()
    results = []
    passed = 0

    for item in queries:
        q = item["q"]
        expected = item["expect"]
        actual = classify_route(q, faq_entries)
        ok = actual == expected
        if ok:
            passed += 1
        results.append({"q": q, "expect": expected, "actual": actual, "pass": ok, "topic": item.get("topic")})

    total = len(results)
    pass_rate = round(100 * passed / max(total, 1), 1)

    out = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "pass_rate_pct": pass_rate,
        "passed": passed,
        "total": total,
        "results": results,
        "policy": "green_report",
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Linda Live Benchmark",
        f"\n**Pass rate:** {pass_rate}% ({passed}/{total})\n",
        "| Query | Expected | Actual | OK |",
        "|---|---|---|---|",
    ]
    for r in results:
        lines.append(f"| {r['q'][:40]} | {r['expect']} | {r['actual']} | {'✓' if r['pass'] else '✗'} |")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"OK: live benchmark {pass_rate}% ({passed}/{total})")
    return 0 if pass_rate >= 70 else 1


if __name__ == "__main__":
    raise SystemExit(main())
