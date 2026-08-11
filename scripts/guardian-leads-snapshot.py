#!/usr/bin/env python3
"""Snapshot lead/richieste counts for Guardian — requires SUPABASE_KEY (service_role)."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "guardian-leads-latest.json"
SUPABASE_URL = os.environ.get(
    "SUPABASE_URL", "https://qwkwkemuabfwvwuqrxlu.supabase.co"
)
KEY = os.environ.get("SUPABASE_KEY", "")


def rest_count(filter_query: str = "") -> int | None:
    if not KEY:
        return None
    url = f"{SUPABASE_URL}/rest/v1/richieste?select=id{filter_query}"
    req = urllib.request.Request(
        url,
        headers={
            "apikey": KEY,
            "Authorization": f"Bearer {KEY}",
            "Prefer": "count=exact",
        },
        method="HEAD",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            cr = resp.headers.get("Content-Range", "")
            if "/" in cr:
                return int(cr.split("/")[-1])
    except urllib.error.HTTPError as e:
        return None
    except Exception:
        return None
    return None


def main() -> None:
    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "available": bool(KEY),
        "reason": None if KEY else "SUPABASE_KEY not set",
        "facts": [],
        "unread_count": None,
        "last_24h_count": None,
        "last_7d_count": None,
    }

    if not KEY:
        OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print("SKIP: SUPABASE_KEY not set")
        return

    unread = rest_count("&letto=eq.false")
    since_24 = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
    since_7d = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
    count_24 = rest_count(f"&created_at=gte.{since_24}")
    count_7d = rest_count(f"&created_at=gte.{since_7d}")

    result["unread_count"] = unread
    result["last_24h_count"] = count_24
    result["last_7d_count"] = count_7d
    result["facts"] = [
        {"fact": "richieste_unread", "value": unread},
        {"fact": "richieste_24h", "value": count_24},
        {"fact": "richieste_7d", "value": count_7d},
    ]

    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
