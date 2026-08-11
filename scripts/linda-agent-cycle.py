#!/usr/bin/env python3
"""
Orchestratore ciclo Linda Agent (bi-quindicinale, gate 14 giorni).
Non duplica Guardian: un entry point per FAQ discovery + question intelligence + quality + index.

Uso:
  python3 scripts/linda-agent-cycle.py
  python3 scripts/linda-agent-cycle.py --force
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "data/linda-agent-cycle-state.json"
REPORT = ROOT / "linda-agent-cycle-report.md"

SCRIPTS = [
    ("faq_discovery", "scripts/linda-faq-biweekly-discovery.py", ["--force"]),
    ("question_intelligence", "scripts/linda-question-intelligence.py", []),
    ("quality_benchmark", "scripts/linda-quality-benchmark.py", []),
    ("property_index", "scripts/linda-property-index.py", []),
]

MIN_DAYS = 14


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"version": 1, "last_run_at": None}


def save_state(data):
    STATE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def should_run(force: bool) -> tuple[bool, str]:
    if force:
        return True, "force"
    st = load_state()
    last = st.get("last_run_at")
    if not last:
        return True, "first_run"
    try:
        elapsed = (datetime.now() - datetime.fromisoformat(last)).days
    except ValueError:
        return True, "invalid_state"
    if elapsed < MIN_DAYS:
        return False, f"gate {elapsed}d < {MIN_DAYS}d"
    return True, f"due {elapsed}d"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    ok, reason = should_run(args.force)
    lines = [f"# Linda Agent Cycle\n\n**{datetime.now().isoformat(timespec='seconds')}** — {reason}\n"]
    results = {}

    if not ok:
        lines.append("SKIP: gate bi-quindicinale attivo.\n")
        REPORT.write_text("\n".join(lines), encoding="utf-8")
        print(f"SKIP: {reason}")
        return 0

    extra = ["--force"] if args.force else []
    exit_code = 0

    for name, script, script_args in SCRIPTS:
        path = ROOT / script
        if not path.exists():
            lines.append(f"- **{name}**: SKIP (script missing)\n")
            continue
        cmd = [sys.executable, str(path)] + script_args + (extra if name == "faq_discovery" and args.force else [])
        if name != "faq_discovery":
            cmd = [c for c in cmd if c != "--force"]
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        results[name] = {"ok": proc.returncode == 0, "stdout": proc.stdout[-500:], "stderr": proc.stderr[-300:]}
        lines.append(f"## {name}\n- exit: {proc.returncode}\n")
        if proc.stdout.strip():
            lines.append(f"```\n{proc.stdout.strip()[-800:]}\n```\n")
        if proc.returncode != 0:
            exit_code = max(exit_code, proc.returncode)

    st = load_state()
    st["last_run_at"] = datetime.now().isoformat(timespec="seconds")
    st["last_reason"] = reason
    st["results"] = {k: v["ok"] for k, v in results.items()}
    save_state(st)

    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"OK: linda-agent-cycle ({reason})")
    return 0 if exit_code == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
