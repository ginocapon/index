"""
Finestre orarie indicative per pubblicazione (Europe/Rome).
Usa --dry-run per vedere se l'ora attuale cade in una finestra.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent


def load_settings() -> dict:
    path = ROOT / "config" / "settings.json"
    if not path.exists():
        path = ROOT / "config" / "settings.example.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def window_times(pair: list[str]) -> tuple[time, time]:
    h1, m1 = map(int, pair[0].split(":"))
    h2, m2 = map(int, pair[1].split(":"))
    return time(h1, m1), time(h2, m2)


def within_any_window(now_local: datetime, windows: list[list[str]]) -> bool:
    t = now_local.timetz().replace(tzinfo=None) if now_local.tzinfo else now_local.time()
    for pair in windows:
        if len(pair) != 2:
            continue
        start, end = window_times(pair)
        if start <= t <= end:
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Controllo finestra oraria pubblicazione social")
    parser.add_argument("--dry-run", action="store_true", help="Stampa stato e esci")
    args = parser.parse_args()

    cfg = load_settings()
    tz_name = cfg.get("scheduler", {}).get("timezone", "Europe/Rome")
    tz = ZoneInfo(tz_name)
    now = datetime.now(tz)
    raw = cfg.get("scheduler", {}).get("run_windows_local_time", [["09:30", "11:30"]])
    ok = within_any_window(now, raw)

    if args.dry_run:
        print(f"Ora locale {tz_name}: {now.isoformat(timespec='minutes')}")
        print(f"Finestra OK per pubblicare: {ok}")
        return 0 if ok else 1

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
