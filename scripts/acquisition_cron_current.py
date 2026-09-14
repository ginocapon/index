#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Restituisce settimana corrente e task pending del cron acquisizione venerdì."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CRON_JSON = ROOT / "data" / "acquisition-roadmap-cron.json"


def main() -> int:
    data = json.loads(CRON_JSON.read_text(encoding="utf-8"))
    anchor = date.fromisoformat(data["anchor_start"])
    hold_until = data.get("do_not_execute_before")
    hold_date = date.fromisoformat(hold_until) if hold_until else anchor
    today = date.today()
    days = (today - anchor).days
    week_num = max(1, min(data["cycle_weeks"], days // 7 + 1 if days >= 0 else 1))
    execution_allowed = today >= hold_date

    weeks = data.get("weeks", [])
    by_week = {w["week"]: w for w in weeks}

    def pick_task() -> dict:
        if week_num in by_week and by_week[week_num].get("status") == "pending":
            return by_week[week_num]
        for w in weeks:
            if w.get("week", 0) >= week_num and w.get("status") == "pending":
                return w
        for w in weeks:
            if w.get("status") == "pending":
                return w
        return by_week.get(week_num, weeks[-1] if weeks else {})

    task = pick_task()
    out = {
        "today": today.isoformat(),
        "anchor_start": data["anchor_start"],
        "execution_allowed": execution_allowed,
        "hold_until": hold_date.isoformat(),
        "calendar_week": week_num,
        "cycle_weeks": data["cycle_weeks"],
        "current_task": task,
        "skill_ref": data.get("skill_ref"),
    }
    if not execution_allowed:
        out["message"] = "Preview only — esecuzione task acquisizione dal " + hold_date.isoformat()
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
