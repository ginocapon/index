#!/usr/bin/env python3
"""Verifica doppioni blog, sitemap, admin, Supabase, agenda."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Pagine statiche collegate dal blog ma senza prefisso blog-
EXTRA_STATIC_PATTERNS = (
    "zona-*.html",
    "articolo-*.html",
    "vendere-casa-padova-errori.html",
)


def collect_static_pages() -> list[Path]:
    seen: set[str] = set()
    out: list[Path] = []
    for p in ROOT.glob("blog-*.html"):
        if p.name == "blog-articolo.html":
            continue
        if p.name not in seen:
            seen.add(p.name)
            out.append(p)
    for pattern in EXTRA_STATIC_PATTERNS:
        for p in ROOT.glob(pattern):
            if p.name not in seen:
                seen.add(p.name)
                out.append(p)
    return out


def slug_resolves_to_file(slug: str) -> bool:
    if not slug or slug == "blog-articolo":
        return True
    candidates = [
        ROOT / f"{slug}.html",
        ROOT / f"blog-{slug}.html",
    ]
    return any(c.is_file() for c in candidates)


def extract_url_statici(text: str) -> list[str]:
    """Estrae slug da url_statico: 'x' e da "url_statico": "x"."""
    slugs: list[str] = []
    slugs.extend(re.findall(r"url_statico:\s*['\"]([^'\"]+)['\"]", text))
    slugs.extend(re.findall(r'"url_statico"\s*:\s*"([^"]+)"', text))
    return slugs


def main() -> int:
    issues: list[str] = []

    static_files = collect_static_pages()
    static_stems = [p.stem for p in static_files]
    for k, v in Counter(static_stems).items():
        if v > 1:
            issues.append(f"File statico duplicato: {k} ({v}x)")

    blog_html = (ROOT / "blog.html").read_text(encoding="utf-8", errors="replace")
    slugs_bh = extract_url_statici(blog_html)
    titoli_bh = re.findall(r"titolo:\s*['\"]([^'\"]+)['\"]", blog_html)
    titoli_bh.extend(re.findall(r'"titolo"\s*:\s*"([^"]+)"', blog_html))
    for k, v in Counter(slugs_bh).items():
        if v > 1:
            issues.append(f"blog.html slug duplicato: {k} ({v}x)")
    for k, v in Counter(titoli_bh).items():
        if v > 1:
            issues.append(f"blog.html titolo duplicato: {k[:80]} ({v}x)")

    canon_by_path: dict[str, list[str]] = defaultdict(list)
    for p in static_files:
        t = p.read_text(encoding="utf-8", errors="replace")
        m = re.search(
            r'rel="canonical"\s+href="https://righettoimmobiliare\.it/([^"?]+)',
            t,
        )
        if m:
            canon_by_path[m.group(1).rstrip("/")].append(p.name)
    for path, files in canon_by_path.items():
        if len(files) > 1:
            issues.append(f"Canonical duplicato {path}: {files}")

    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8", errors="replace")
    sm_urls = re.findall(r"<loc>(https://righettoimmobiliare\.it/[^<]+)</loc>", sm)

    def norm_url(u: str) -> str:
        u = u.replace("https://righettoimmobiliare.it/", "").rstrip("/")
        if "blog-articolo?s=" in u:
            return "dyn:" + u.split("s=")[-1]
        return u

    sm_norm = [norm_url(u) for u in sm_urls if "blog" in u.lower()]
    for k, v in Counter(sm_norm).items():
        if v > 1:
            issues.append(f"sitemap duplicato: {k} ({v}x)")

    static_set = {p.stem for p in static_files}
    bh_set = set(slugs_bh)
    for s in sorted(bh_set - static_set):
        if s and s != "blog-articolo" and not slug_resolves_to_file(s):
            issues.append(f"In blog.html ma senza file HTML: {s}")
    for s in sorted(static_set - bh_set):
        if s.startswith("blog-"):
            issues.append(f"File statico non in blog.html articoliStatici: {s}")

    # Titoli simili (normalizzati)
    skimm_path = ROOT / "TEST-SKILL" / "skimm.json"

    def norm_title(t: str) -> str:
        return re.sub(r"\s+", " ", t.lower().strip())[:120]

    titles_all: list[tuple[str, str]] = []
    for p in static_files:
        t = p.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"<title>([^<]+)</title>", t)
        if m:
            titles_all.append((norm_title(m.group(1)), p.name))
    by_norm: dict[str, list[str]] = defaultdict(list)
    for nt, fn in titles_all:
        by_norm[nt].append(fn)
    for nt, files in by_norm.items():
        if len(files) > 1:
            issues.append(f"Titolo HTML identico: {files}")

    # Supabase
    try:
        import os

        from dotenv import load_dotenv
        from supabase import create_client

        load_dotenv(ROOT / "righetto_social" / ".env")
        url = os.environ.get("SUPABASE_URL", "").strip()
        key = os.environ.get("SUPABASE_KEY", "").strip()
        if url and key:
            c = create_client(url, key)
            rows = c.table("blog").select("id,titolo,stato").execute().data or []
            titoli = [str(r.get("titolo") or "").strip() for r in rows if r.get("titolo")]
            for k, v in Counter(titoli).items():
                if v > 1:
                    issues.append(f"Supabase blog titolo duplicato: {k[:80]} ({v}x)")

            # Supabase + articoliStatici: mirror intenzionale — non segnalare come errore

            prows = (
                c.table("pianificazioni")
                .select("id,data_inizio,ora,tipo,riferimento_id,titolo,note")
                .execute()
            ).data or []
            slot_keys = [
                (
                    str(r.get("data_inizio") or "")[:10],
                    str(r.get("ora") or ""),
                    str(r.get("tipo") or ""),
                    str(r.get("riferimento_id") or ""),
                )
                for r in prows
            ]
            for k, v in Counter(slot_keys).items():
                if v > 1:
                    issues.append(
                        f"Agenda slot duplicato {k[0]} {k[1]} {k[2]} ref={k[3][:8]}… ({v}x)"
                    )
            print(f"Supabase: {len(rows)} blog, {len(prows)} pianificazioni")
    except Exception as e:
        print(f"Supabase skip: {e}", file=sys.stderr)

    if skimm_path.is_file():
        try:
            skimm = json.loads(skimm_path.read_text(encoding="utf-8"))
            kws = [a.get("kw_primaria", "") for a in skimm.get("articles", []) if a.get("kw_primaria")]
            for k, v in Counter(kws).items():
                if v > 1:
                    slugs = [
                        a["slug"]
                        for a in skimm["articles"]
                        if a.get("kw_primaria") == k
                    ]
                    issues.append(f"skimm kw_primaria duplicata `{k}`: {', '.join(slugs)}")
            print(f"skimm.json: {skimm.get('count', len(skimm.get('articles', [])))} articoli catalogati")
        except Exception as e:
            print(f"skimm.json skip: {e}", file=sys.stderr)
    else:
        print("skimm.json assente — eseguire: python scripts/build_skimm.py", file=sys.stderr)

    print(f"File blog statici: {len(static_files)}")
    print(f"blog.html articoliStatici slug: {len(slugs_bh)}")
    print(f"sitemap URL blog-related: {len(sm_norm)}")
    print()
    blog_issues = [x for x in issues if not x.startswith("Agenda slot duplicato")]
    agenda_issues = [x for x in issues if x.startswith("Agenda slot duplicato")]

    if not blog_issues and not agenda_issues:
        print("OK: nessun doppione rilevato nei controlli automatici.")
        return 0

    if blog_issues:
        print(f"TROVATI {len(blog_issues)} incoerenze blog/sitemap:\n")
        for i, x in enumerate(blog_issues, 1):
            print(f"{i}. {x}")
    if agenda_issues:
        print(
            f"\nINFO: {len(agenda_issues)} slot agenda storici duplicati in Supabase "
            "(maggio 2026, non bloccante per il sito)."
        )
    return 1 if blog_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
