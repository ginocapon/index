# -*- coding: utf-8 -*-
"""Sincronizza llms.txt, llms-full.txt (sezione blog) e metadati ai.json con blog-*.html."""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://righettoimmobiliare.it"
BLOG_MARKER = "## Articoli Blog e Guide"


def extract_title(html: str, slug: str) -> str:
    m = re.search(r'<meta\s+property="og:title"\s+content="([^"]+)"', html, re.I)
    if m:
        return m.group(1).strip()
    m = re.search(r"<title>([^<|]+)", html, re.I)
    if m:
        t = m.group(1).strip()
        if "Reindirizzamento" not in t:
            return t
    return slug.replace("blog-", "").replace("-", " ").title()


def collect_blogs() -> list[tuple[str, str]]:
    rows = []
    for path in sorted(ROOT.glob("blog-*.html")):
        slug = path.stem
        if slug == "blog-articolo":
            continue
        html = path.read_text(encoding="utf-8", errors="replace")
        if "Reindirizzamento" in html[:800] or 'http-equiv="refresh"' in html[:1200].lower():
            continue
        title = extract_title(html, slug)
        rows.append((slug, title))
    return rows


def blog_lines(slugs: list[tuple[str, str]]) -> list[str]:
    return [
        f"- [{title}]({SITE}/{slug})"
        for slug, title in slugs
    ]


def patch_llms(path: Path, slugs: list[tuple[str, str]]) -> None:
    text = path.read_text(encoding="utf-8")
    lines = blog_lines(slugs)
    block = BLOG_MARKER + "\n\n" + "\n".join(lines) + "\n"
    if BLOG_MARKER in text:
        pre, _ = text.split(BLOG_MARKER, 1)
        # drop old blog tail until next ## section or end markers
        rest = text.split(BLOG_MARKER, 1)[1]
        m = re.search(r"\n---\n\n## (?!Articoli)", rest)
        if m:
            tail = rest[m.start() + 1 :]
        else:
            tail = ""
        text = pre.rstrip() + "\n\n" + block
        if tail.strip():
            text += "\n---\n" + tail.lstrip("\n")
    else:
        text = text.rstrip() + "\n\n" + block
    path.write_text(text, encoding="utf-8", newline="\n")


def patch_ai_json(count: int) -> None:
    path = ROOT / "ai.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["lastUpdated"] = date.today().isoformat()
    data["contentIndex"] = {
        "blogArticles": count,
        "llmsTxt": f"{SITE}/llms.txt",
        "llmsFullTxt": f"{SITE}/llms-full.txt",
        "measurementId": "G-PHEL8KXLBX",
        "consentMode": "v2-custom-banner"
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    slugs = collect_blogs()
    patch_llms(ROOT / "llms.txt", slugs)
    patch_llms(ROOT / "llms-full.txt", slugs)
    patch_ai_json(len(slugs))
    print(f"OK: {len(slugs)} blog in llms.txt + llms-full.txt; ai.json aggiornato")


if __name__ == "__main__":
    main()
