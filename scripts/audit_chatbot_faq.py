#!/usr/bin/env python3
"""Confronta slug blog in skimm.json con riferimenti blog: in js/chatbot.js."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
skimm = json.loads((ROOT / "TEST-SKILL/skimm.json").read_text(encoding="utf-8"))
text = (ROOT / "js/chatbot.js").read_text(encoding="utf-8")

slugs = {a["slug"] for a in skimm["articles"]}
faq_blogs = set(re.findall(r"blog:\s*'([^']+)'", text))
missing = sorted(slugs - faq_blogs - {"blog"})

print(f"skimm articles: {len(slugs)}")
print(f"FAQ blog refs (unique): {len(faq_blogs)}")
print(f"Missing in FAQ_DATA: {len(missing)}\n")
for s in missing:
    art = next(a for a in skimm["articles"] if a["slug"] == s)
    print(f"  {s}")
    print(f"    -> {art.get('title', '')[:70]}")

# duplicate keyword roots (first match wins)
faq_blocks = re.findall(
    r"\{\s*k:\s*\[([^\]]+)\]", text.split("const FAQ_DATA")[1].split("];")[0]
)
seen = {}
for block in faq_blocks:
    keys = re.findall(r"'([^']+)'", block)
    for k in keys:
        if k in seen:
            print(f"\nDUPLICATE kw: '{k}' (also in entry ~{seen[k]})")
        else:
            seen[k] = keys[0]
