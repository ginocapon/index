#!/usr/bin/env python3
"""Helper condiviso per audit: testo visibile e conteggi keyword."""
from __future__ import annotations

import re
import sys
from pathlib import Path


def visible_text(html: str) -> str:
    t = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.S | re.I)
    t = re.sub(r"<style[^>]*>.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = t.replace("&nbsp;", " ").replace("&amp;", "&")
    return re.sub(r"\s+", " ", t).lower()


def counts(html: str) -> dict[str, int]:
    t = visible_text(html)
    return {
        "padova": len(re.findall(r"\ba\s+padova\b", t)) + len(re.findall(r"\bdi\s+padova\b", t)),
        "agenzia": len(re.findall(r"\bagenzia immobiliare\b", t)),
        "righetto": len(re.findall(r"\brighetto immobiliare\b", t)),
        "a_padova_only": len(re.findall(r"\ba\s+padova\b", t)),
    }


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: audit_helpers.py <file> <padova|agenzia|righetto|a_padova>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    key = sys.argv[2]
    raw = path.read_text(encoding="utf-8", errors="replace")
    c = counts(raw)
    print(c.get(key, 0))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
