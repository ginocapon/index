#!/usr/bin/env python3
"""Merge proposte Linda FAQ in js/chatbot.js FAQ_DATA."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHATBOT = ROOT / "js/chatbot.js"
PROPOSALS = ROOT / "data/linda-faq-proposals-latest.json"

GENERIC_WORDS = {
    "quali", "sono", "requisiti", "per", "come", "cosa", "dove", "quando",
    "che", "del", "della", "dei", "nel", "nella", "the", "what", "when",
    "essere", "vecchio", "puo", "puo'", "l'ape", "serve", "posso",
}


def js_str(s: str) -> str:
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n") + "'"


def refine_keys(p: dict) -> list[str]:
    raw = p.get("k", [])
    keys: list[str] = []
    for k in raw:
        k = k.strip().lower()
        if not k or k in GENERIC_WORDS or len(k) < 3:
            continue
        if k not in keys:
            keys.append(k)
    codice = (p.get("immobile_codice") or "").lower()
    if codice and codice not in keys:
        keys.insert(0, codice)
    q = p.get("question", "")
    if q and len(q) <= 55:
        ql = q.lower().strip()
        if ql not in keys:
            keys.insert(0, ql)
    blog = p.get("blog", "")
    if blog:
        slug_part = blog.replace("blog-", "").replace("-2026", "")
        if slug_part and slug_part not in keys and len(slug_part) > 8:
            keys.append(slug_part[:40])
    return keys[:6]


def format_entry(p: dict) -> str:
    keys = refine_keys(p)
    if len(keys) < 2:
        keys = p.get("k", [])[:6]
    lines = ["  {", f"    k: [{', '.join(js_str(k) for k in keys)}],"]
    lines.append(f"    r: {js_str(p['r'])},")
    if p.get("blog"):
        lines.append(f"    blog: {js_str(p['blog'])},")
        lines.append(f"    blogTitle: {js_str(p.get('blogTitle', ''))}")
    lines.append("  },")
    return "\n".join(lines)


def main():
    text = CHATBOT.read_text(encoding="utf-8")
    block = text.split("const FAQ_DATA")[1].split("];")[0]
    existing_kw = set(re.findall(r"'([^']+)'", block))

    props = json.loads(PROPOSALS.read_text(encoding="utf-8"))["proposals"]
    # Priorità: FAQ schema > immobili > heading > gap
    order = {"blog_faq_schema": 0, "immobile_catalog": 1, "blog_heading": 2, "skimm_gap": 3}
    props.sort(key=lambda x: order.get(x.get("source"), 9))

    merged = []
    seen_blogs_schema: set[str] = set()

    for p in props:
        src = p.get("source", "")
        blog = p.get("blog")
        if src == "blog_heading" and blog and blog in seen_blogs_schema:
            continue
        keys = refine_keys(p)
        if not keys:
            continue
        if any(k in existing_kw for k in keys):
            continue
        merged.append(p)
        for k in keys:
            existing_kw.add(k)
        if src == "blog_faq_schema" and blog:
            seen_blogs_schema.add(blog)

    if not merged:
        print("Nothing to merge")
        return 1

    section_comment = (
        "\n\n  // ── DISCOVERY BI-QUINDICINALE 2026-08-11 (linda-faq-biweekly-discovery) ──\n"
    )
    entries_js = section_comment + "\n".join(format_entry(p) for p in merged)

    close_idx = text.rfind("];", 0, text.find("window.RIGHETTO_FAQ_DATA"))
    if close_idx < 0:
        raise SystemExit("FAQ_DATA close not found")

    # Virgola sull'ultima voce esistente prima dell'inserimento
    prefix = text[:close_idx].rstrip()
    if not prefix.endswith(","):
        prefix = prefix + ","

    new_text = prefix + entries_js + "\n" + text[close_idx:]
    CHATBOT.write_text(new_text, encoding="utf-8")
    print(f"Merged {len(merged)} FAQ entries into chatbot.js")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
