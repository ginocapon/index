#!/usr/bin/env python3
"""
Verifica asset hero blog: file dedicato, non duplicato, HD, coerente collo slug.
BLOCCANTE prima di publish — vedi TEST-SKILL/skill-content.md §2.1 E.

Uso:
  python scripts/verify_blog_hero_assets.py --slug blog-esempio-2026
  python scripts/verify_blog_hero_assets.py --all
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG_BLOG = ROOT / "img" / "blog"
MIN_W, MIN_H = 1200, 630
TARGET_W, TARGET_H = 1900, 900


def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def webp_dims(path: Path) -> tuple[int, int] | None:
    try:
        from PIL import Image

        with Image.open(path) as im:
            return im.size
    except Exception:
        return None


def hero_from_html(path: Path) -> str | None:
    raw = path.read_text(encoding="utf-8", errors="replace")
    m = re.search(r'class="art-hero-img"[^>]+src="([^"]+)"', raw)
    if m:
        return m.group(1)
    m = re.search(r'<meta property="og:image" content="https://righettoimmobiliare\.it/([^"]+)"', raw)
    return m.group(1) if m else None


def collect_blog_files() -> list[Path]:
    return sorted(ROOT.glob("blog-*.html"), key=lambda p: p.name)


def verify_slug(slug: str, check_html: bool = True) -> dict:
    issues: list[str] = []
    html = ROOT / f"{slug}.html"
    if not html.is_file():
        issues.append(f"HTML mancante: {slug}.html")
        return {"slug": slug, "ok": False, "issues": issues}

    hero_rel = hero_from_html(html) if check_html else f"img/blog/{slug}.webp"
    if not hero_rel:
        issues.append("Hero src non trovato in HTML (art-hero-img o og:image)")
        hero_rel = f"img/blog/{slug}.webp"

    raw = html.read_text(encoding="utf-8", errors="replace")
    hero_path = ROOT / hero_rel

    if not hero_path.is_file():
        issues.append(f"File hero mancante: {hero_rel}")
    else:
        if "foto-servizi" in hero_rel or "og-default" in hero_rel:
            issues.append("VIETATO: hero generico foto-servizi o og-default")
        if not slug.replace("blog-", "") in hero_rel.replace("blog-", "") and slug not in hero_rel:
            issues.append(f"Hero path non allineato allo slug: {hero_rel}")

        dims = webp_dims(hero_path)
        if dims:
            w, h = dims
            if w < MIN_W or h < MIN_H:
                issues.append(f"Risoluzione insufficiente: {w}×{h} (min {MIN_W}×{MIN_H})")
            ratio = w / h if h else 0
            if ratio < 1.8 or ratio > 2.2:
                issues.append(f"Proporzione non 19:9 circa: {w}×{h} (ratio {ratio:.2f})")
        else:
            issues.append("Impossibile leggere dimensioni WebP (installa Pillow)")

        size_kb = hero_path.stat().st_size // 1024
        if size_kb > 350:
            issues.append(f"Hero troppo pesante: {size_kb} KiB (target <150, max 350)")

    # Duplicati hash tra tutti hero blog
    hashes: dict[str, list[str]] = {}
    for p in IMG_BLOG.glob("*.webp"):
        hashes.setdefault(file_hash(p), []).append(p.name)
    if hero_path.is_file():
        h = file_hash(hero_path)
        dupes = [x for x in hashes.get(h, []) if x != hero_path.name]
        if dupes:
            issues.append(f"Hero DUPLICATO (stesso file di): {', '.join(dupes)}")

    body_imgs = len(re.findall(r'<figure class="blog-fig"', raw))
    if body_imgs < 3:
        issues.append(f"Solo {body_imgs} figure corpo (min 3 richieste)")

    return {"slug": slug, "ok": len(issues) == 0, "issues": issues, "hero": hero_rel}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", help="blog-slug senza .html")
    parser.add_argument("--all", action="store_true", help="Verifica tutti blog-*.html")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    results = []
    if args.all:
        for p in collect_blog_files():
            results.append(verify_slug(p.stem))
    elif args.slug:
        results.append(verify_slug(args.slug.replace(".html", "")))
    else:
        parser.print_help()
        return 1

    out_path = ROOT / "data" / "blog-hero-verify-latest.json"
    out_path.write_text(json.dumps({"results": results}, indent=2), encoding="utf-8")

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            status = "OK" if r["ok"] else "FAIL"
            print(f"[{status}] {r['slug']}")
            for i in r.get("issues", []):
                print(f"  - {i}")

    failed = sum(1 for r in results if not r["ok"])
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
