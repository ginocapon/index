#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit varietà visiva e struttura blog (skill-editoriale-visivo §16-QUATER)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VISUAL_MEMORY = ROOT / "data" / "editorial-visual-memory.json"
QUEUE = ROOT / "data" / "editorial-queue.json"

VALID_STRUCTURES = {
    "ANALITICA",
    "GUIDA",
    "NOTIZIA_IMPATTO",
    "DOMANDA_RISPOSTA",
    "CONFRONTO",
    "TERRITORIALE",
    "MISTO",
}


def load_memory() -> dict:
    if not VISUAL_MEMORY.exists():
        return {"recent_articles": [], "structure_saturation_last_8": {}}
    return json.loads(VISUAL_MEMORY.read_text(encoding="utf-8"))


def analyze_file(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8", errors="replace")
    slug = path.stem
    h2_ids = re.findall(r'<h2[^>]*id=["\']([^"\']+)["\']', raw, re.I)
    imgs = list(dict.fromkeys(re.findall(r'src=["\'](img/blog/[^"\']+\.webp)["\']', raw, re.I)))
    charts = re.findall(r'class="chart-wrap"[^>]*aria-label=["\']([^"\']*)["\']', raw, re.I)
    return {"slug": slug, "h2_sequence": h2_ids, "images": imgs, "chart_labels": charts}


def slug_prefixes(slug: str) -> list[str]:
    """Stem slug per path immagine dedicati (con o senza anno -2026)."""
    stems = [slug]
    no_year = re.sub(r"-20\d{2}$", "", slug)
    if no_year != slug:
        stems.append(no_year)
    return stems


def is_dedicated_image(img: str, slug: str) -> bool:
    name = Path(img).stem.lower()
    return any(name.startswith(s.lower()) or s.lower() in name for s in slug_prefixes(slug))


def jaccard(a: list[str], b: list[str]) -> float:
    if not a or not b:
        return 0.0
    sa, sb = set(a), set(b)
    return len(sa & sb) / len(sa | sb)


def audit_html(path: Path, memory: dict, declared_structure: str = "") -> list[str]:
    issues: list[str] = []
    slug = path.stem
    cur = analyze_file(path)
    recent = [a for a in memory.get("recent_articles", []) if a.get("slug") != slug][:8]

    st = declared_structure or ""
    if st and st not in VALID_STRUCTURES:
        issues.append(f"structure_type '{st}' non valido (Appendice D §16-QUATER)")

    # Saturazione struttura
    sat = memory.get("structure_saturation_last_8", {})
    if st and sat.get(st, 0) >= 2:
        issues.append(
            f"structure_type {st} già {sat[st]}x negli ultimi 8 — "
            f"scegliere altra organizzazione (ANALITICA/GUIDA/CONFRONTO/…)"
        )

    # Sequenza H2 troppo simile
    for old in recent:
        sim = jaccard(cur["h2_sequence"], old.get("h2_sequence", []))
        if sim >= 0.75 and len(cur["h2_sequence"]) >= 4:
            issues.append(
                f"sequenza H2 troppo simile a {old['slug']} (overlap {sim:.0%}) — variare impaginazione"
            )
            break

    # Riuso immagini (path o già in altro articolo)
    all_imgs: dict[str, str] = {}
    for old in memory.get("recent_articles", []):
        if old.get("slug") == slug:
            continue
        for img in old.get("images", []):
            all_imgs[img] = old["slug"]

    for img in cur["images"]:
        if img in all_imgs:
            issues.append(f"immagine riutilizzata {img} (già in {all_imgs[img]})")
        # path copiato da altro slug nel nome sorgente batch
        for other in recent:
            other_slug = other.get("slug", "")
            if other_slug and other_slug in img and other_slug != slug:
                issues.append(f"path immagine sembra derivato da {other_slug}: {img}")

    # Grafiche identiche (aria-label)
    all_charts: dict[str, str] = {}
    for old in recent:
        for cl in old.get("chart_labels", []):
            if cl:
                all_charts[cl.lower()] = old["slug"]
    for cl in cur["chart_labels"]:
        if cl.lower() in all_charts:
            issues.append(f"chart aria-label duplicato vs {all_charts[cl.lower()]}: «{cl[:50]}»")

    # Percorso immagine deve includere slug articolo (no generic reuse)
    for img in cur["images"]:
        if not is_dedicated_image(img, slug):
            issues.append(f"immagine non dedicata allo slug (path generico?): {img}")

    return issues


def audit_queue_item(item: dict, memory: dict) -> list[str]:
    issues: list[str] = []
    iid = item.get("id", "?")
    st = str(item.get("structure_type", "")).strip()
    if not st:
        issues.append(f"{iid}: structure_type mancante (§16-QUATER)")
    orv = item.get("owner_relevance")
    if orv is None:
        issues.append(f"{iid}: owner_relevance mancante (true/false — §16-QUINQUIES)")

    faq = str(item.get("faq_candidates", "")).strip()
    if len(faq) < 15:
        issues.append(f"{iid}: faq_candidates breve — quali domande reali emergeranno?")

    geo = str(item.get("geo_focus", "")).strip()
    if not geo:
        issues.append(f"{iid}: geo_focus mancante (Padova/provincia/Veneto/Italia)")

    slug = item.get("slug", "")
    if slug:
        path = ROOT / f"{slug}.html"
        if path.is_file():
            issues.extend(audit_html(path, memory, st))
    return issues


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit varietà visiva §16-QUATER")
    ap.add_argument("--file", help="blog-*.html")
    ap.add_argument("--id", help="ID coda eq-XXX")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--rebuild", action="store_true")
    args = ap.parse_args()

    if args.rebuild:
        import subprocess

        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "build_editorial_visual_memory.py")],
            cwd=str(ROOT),
        )
        if r.returncode != 0:
            return r.returncode

    memory = load_memory()

    if args.report:
        print("=== Saturazione struttura (ultimi 8) ===")
        for k, v in memory.get("structure_saturation_last_8", {}).items():
            print(f"  {k}: {v} SATURATA")
        reuse = memory.get("image_hash_reuse_detected", {})
        if reuse:
            print(f"\nRiuso hash immagini: {len(reuse)} gruppi — generare WebP ex novo")
        print(f"\nMemoria: {len(memory.get('recent_articles', []))} articoli")
        return 0

    if args.file:
        path = ROOT / args.file if not Path(args.file).is_absolute() else Path(args.file)
        issues = audit_html(path, memory)
        if issues:
            print(f"FAIL {path.name}:")
            for i in issues:
                print(f"  - {i}")
            return 1
        print(f"OK   {path.name}")
        return 0

    if args.id and QUEUE.exists():
        data = json.loads(QUEUE.read_text(encoding="utf-8"))
        items = [i for i in data.get("items", []) if i.get("id") == args.id]
        if not items:
            print(f"ERR: {args.id} non trovato")
            return 1
        issues = audit_queue_item(items[0], memory)
        if issues:
            print(f"FAIL {args.id}:")
            for i in issues:
                print(f"  - {i}")
            return 1
        print(f"OK   {args.id}")
        return 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
