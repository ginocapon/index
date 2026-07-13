# -*- coding: utf-8 -*-
"""Sostituisce blocchi gtag inline con js/ga-consent.js (Consent Mode v2)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPLACEMENT = '<!-- Google tag (gtag.js) + Consent Mode -->\n<script src="js/ga-consent.js?v=1"></script>'
BLOCK = re.compile(
    r"<!-- Google tag \(gtag\.js\)(?:\s*\+\s*Consent Mode)? -->\s*"
    r"<script async src=\"https://www\.googletagmanager\.com/gtag/js\?id=G-PHEL8KXLBX\"></script>\s*"
    r"<script>[\s\S]*?gtag\(\s*'config'\s*,\s*'G-PHEL8KXLBX'\s*\);?\s*</script>",
    re.M,
)
COMPACT = re.compile(
    r"<script async src=\"https://www\.googletagmanager\.com/gtag/js\?id=G-PHEL8KXLBX\"></script>\s*"
    r"<script>[\s\S]*?gtag\(\s*'config'\s*,\s*'G-PHEL8KXLBX'\s*\);?\s*</script>",
    re.M,
)


def patch_file(path: Path) -> bool:
    if path.name == "index.html":
        return False
    text = path.read_text(encoding="utf-8")
    new = BLOCK.sub(REPLACEMENT, text)
    new = COMPACT.sub(REPLACEMENT, new)
    if new == text:
        return False
    path.write_text(new, encoding="utf-8", newline="\n")
    return True


def main() -> None:
    n = 0
    for path in ROOT.rglob("*.html"):
        if "TEST-SKILL" in str(path) or "node_modules" in str(path):
            continue
        if patch_file(path):
            n += 1
            print("+", path.relative_to(ROOT))
    print(f"OK: {n} file aggiornati")


if __name__ == "__main__":
    main()
