#!/usr/bin/env python3
"""Snapshot aggregati intent Linda da Supabase (service_role) per question intelligence."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "linda-intents-snapshot-latest.json"
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://qwkwkemuabfwvwuqrxlu.supabase.co")
KEY = os.environ.get("SUPABASE_KEY", "")


def fetch_rows(since_iso: str, limit: int = 2000) -> list[dict]:
    if not KEY:
        return []
    url = (
        f"{SUPABASE_URL}/rest/v1/linda_chat_intents"
        f"?select=intent_type,topic_label,operation,location,budget_band,rooms_min,property_type,msg_hash,created_at"
        f"&created_at=gte.{since_iso}"
        f"&order=created_at.desc"
        f"&limit={limit}"
    )
    req = urllib.request.Request(
        url,
        headers={"apikey": KEY, "Authorization": f"Bearer {KEY}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        if e.code == 404 or "does not exist" in body:
            return []
        raise
    except Exception:
        return []


def main() -> int:
    since = (datetime.now(timezone.utc) - timedelta(days=14)).isoformat()
    rows = fetch_rows(since)

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "available": bool(KEY),
        "reason": None if KEY else "SUPABASE_KEY not set",
        "window_days": 14,
        "total_events": len(rows),
        "by_intent_type": dict(Counter(r.get("intent_type") for r in rows)),
        "top_topic_labels": [
            {"label": k, "count": v}
            for k, v in Counter(r.get("topic_label") for r in rows if r.get("topic_label")).most_common(25)
        ],
        "location_demand": dict(Counter(r.get("location") for r in rows if r.get("location")).most_common(15)),
        "operation_demand": dict(Counter(r.get("operation") for r in rows if r.get("operation")).most_common(10)),
        "budget_bands": dict(Counter(r.get("budget_band") for r in rows if r.get("budget_band")).most_common(10)),
        "unique_msg_hashes": len({r.get("msg_hash") for r in rows if r.get("msg_hash")}),
    }

    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"total": len(rows), "available": result["available"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
