#!/usr/bin/env python3
"""Sostituisce CDN jsdelivr/cdnjs con asset locali js/vendor/ (zero CDN esterni)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SUPABASE_CDN = re.compile(
    r'<script[^>]*src="https://cdn\.jsdelivr\.net/npm/@supabase/supabase-js@2[^"]*"[^>]*>\s*</script>',
    re.I,
)
JSPDF_CDN = re.compile(
    r'<script[^>]*src="https://cdnjs\.cloudflare\.com/ajax/libs/jspdf/2\.5\.1/jspdf\.umd\.min\.js"[^>]*>\s*</script>',
    re.I,
)
PREFETCH_CDN = re.compile(
    r'\s*<link rel="(?:dns-prefetch|preconnect)" href="https://cdn\.jsdelivr\.net"[^>]*>\n?',
    re.I,
)

SKIP = {
    "blog-articolo.html", "404.html", "bookmarklet-helper.html",
    "unsubscribe.html", "scraping.html",
}


def vendor_prefix(path: Path) -> str:
    depth = len(path.relative_to(ROOT).parts) - 1
    return "../" * depth if depth else ""


def patch_file(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    orig = raw
    fixes: list[str] = []
    prefix = vendor_prefix(path)

    n = len(PREFETCH_CDN.findall(raw))
    if n:
        raw = PREFETCH_CDN.sub("", raw)
        fixes.append(f"prefetch-cdn×{n}")

    if SUPABASE_CDN.search(raw):
        sup = (
            f'<script src="{prefix}js/vendor/supabase.min.js"></script>\n'
            f'<script src="{prefix}js/supabase-bridge.js?v=1"></script>'
        )
        raw = SUPABASE_CDN.sub(sup, raw)
        # dedupe identical consecutive supabase tags
        raw = re.sub(
            rf'({re.escape(sup)}\s*){{2,}}',
            sup + "\n",
            raw,
        )
        fixes.append("supabase-local")

    if JSPDF_CDN.search(raw):
        jspdf = f'<script src="{prefix}js/vendor/jspdf.umd.min.js" defer></script>'
        raw = JSPDF_CDN.sub(jspdf, raw)
        fixes.append("jspdf-local")

    if raw != orig:
        path.write_text(raw, encoding="utf-8", newline="\n")
    return fixes


def main() -> int:
    total = 0
    for p in sorted(ROOT.rglob("*.html")):
        if p.name in SKIP or p.name.startswith("google"):
            continue
        if "node_modules" in p.parts:
            continue
        fixes = patch_file(p)
        if fixes:
            print(f"  {p.relative_to(ROOT)}: {', '.join(fixes)}")
            total += 1
    print(f"\nFile aggiornati: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
