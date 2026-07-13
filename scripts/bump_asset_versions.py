# -*- coding: utf-8 -*-
"""Bump ?v=N su asset JS indicati in tutti gli HTML."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUMPS = {
    "cookie-consent.js": 4,
}


def main() -> None:
    for path in ROOT.rglob("*.html"):
        if "TEST-SKILL" in str(path):
            continue
        text = path.read_text(encoding="utf-8")
        new = text
        for asset, ver in BUMPS.items():
            new = re.sub(
                rf"js/{re.escape(asset)}\?v=\d+",
                f"js/{asset}?v={ver}",
                new,
            )
        if new != text:
            path.write_text(new, encoding="utf-8", newline="\n")
            print("+", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
