"""Bump cache-bust query on rig-lead-form.js references."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAT = re.compile(r"rig-lead-form\.js\?v=\d+")
NEW = "rig-lead-form.js?v=3"
GLOBS = ("*.html", "scripts/*.py", "tools/*.py", "TEST-SKILL/*.md")

changed = 0
for pattern in GLOBS:
    for path in ROOT.glob(pattern):
        text = path.read_text(encoding="utf-8")
        if not PAT.search(text):
            continue
        updated = PAT.sub(NEW, text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
            print(path.relative_to(ROOT))

print(f"Updated {changed} files")
