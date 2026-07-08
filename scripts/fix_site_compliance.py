# -*- coding: utf-8 -*-
"""Allinea telefono, sede e testi GDPR form su html/js/json del sito."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "node_modules", "scripts/_tmp_perizia", "documenti"}

TEL_DISPLAY = "049.8843484"
TEL_HREF = "+390498843484"
SEDE = "Via Roma n.96, 35010 Limena (PD)"

GDPR_REQUIRED = (
    'Ho preso visione dell\'<a href="privacy" target="_blank" rel="noopener">informativa privacy</a> '
    "(Reg. UE 2016/679) e acconsento al trattamento per finalità contrattuali e di legge "
    "(punti a) e b)). *"
)

GDPR_MARKETING = (
    'Acconsento al trattamento per finalità di marketing, soddisfazione clienti e comunicazioni '
    "commerciali (punti c), d) ed e) dell'informativa — <em>facoltativo</em>, revocabile in qualsiasi momento."
)

PHONE_PATTERNS = [
    (re.compile(r"049\.049\.8843484"), TEL_DISPLAY),
    (re.compile(r"049\s*8755543"), TEL_DISPLAY),
    (re.compile(r"049\s*7808\s*888"), TEL_DISPLAY),
    (re.compile(r"0497808888"), TEL_DISPLAY),
    (re.compile(r"049\s*88\.43\.484"), TEL_DISPLAY),
    (re.compile(r"049\.88\.43\.484"), TEL_DISPLAY),
    (re.compile(r"049\s884\s3484"), TEL_DISPLAY),
    (re.compile(r"049\s8843484"), TEL_DISPLAY),
    (re.compile(r"(?<![\d.])8843484(?![\d])"), TEL_DISPLAY),
]

ADDR_PATTERNS = [
    (re.compile(r"Via Fratelli Cervi\s*37,?\s*35129\s*Padova", re.I), SEDE),
    (re.compile(r"Via Fratelli Cervi 37"), "Via Roma n.96, 35010 Limena (PD)"),
]

GDPR_LABEL_RES = [
    re.compile(
        r"Acconsento al trattamento dei dati[^<]*(?:\(GDPR\)[^<]*)?\.\s*"
        r'(?:<a href="privacy(?:-policy)?"[^>]*>[^<]+</a>)?',
        re.I,
    ),
    re.compile(
        r'Accetto la\s*<a href="privacy(?:-policy)?">[^<]+</a>',
        re.I,
    ),
    re.compile(
        r"Acconsento al trattamento dei dati personali ai sensi del Regolamento UE 2016/679[^<]*",
        re.I,
    ),
    re.compile(
        r"Acconsento al trattamento dei dati personali\.\s*"
        r'<a href="privacy"[^>]*>Privacy</a>',
        re.I,
    ),
    re.compile(
        r"Acconsento al trattamento dei dati\.\s*"
        r'<a href="privacy"[^>]*>Privacy</a>',
        re.I,
    ),
]

MARKETING_SNIPPET = (
    f'<label class="bl-chk bl-chk-opt"><input type="checkbox" class="rig-gdpr-marketing" '
    f'name="gdpr_marketing"> {GDPR_MARKETING}</label>'
)

FCHK_MARKETING = (
    f'<div class="fchk fchk-opt"><input type="checkbox" id="f-gdpr-marketing" '
    f'class="rig-gdpr-marketing" name="gdpr_marketing">'
    f'<label for="f-gdpr-marketing">{GDPR_MARKETING}</label></div>'
)

CONTATTI_MARKETING = (
    f'<div class="fg-chk fg-chk-opt" style="margin-top:.5rem">'
    f'<input type="checkbox" id="f-gdpr-marketing" class="rig-gdpr-marketing" name="gdpr_marketing">'
    f'<label for="f-gdpr-marketing">{GDPR_MARKETING}</label></div>'
)

LANDING_NEWS_OLD = re.compile(
    r'<label for="(?:a|v|l)-news">Desidero ricevere aggiornamenti[^<]+</label>',
    re.I,
)


def iter_files():
    for ext in ("*.html", "*.js", "*.json", "*.md"):
        for p in ROOT.rglob(ext):
            if any(s in p.parts for s in SKIP_DIRS):
                continue
            if p.name == "fix_site_compliance.py":
                continue
            yield p


def fix_phones(text: str) -> str:
    for rx, repl in PHONE_PATTERNS:
        text = rx.sub(repl, text)
    return text


def fix_addresses(text: str) -> str:
    for rx, repl in ADDR_PATTERNS:
        text = rx.sub(repl, text)
    return text


def fix_gdpr_labels(text: str) -> str:
    for rx in GDPR_LABEL_RES:
        text = rx.sub(GDPR_REQUIRED, text)
    text = re.sub(
        r'(<div class="fchk"><input type="checkbox" id="f-gdpr"[^>]*><label for="f-gdpr">)[^<]+(</label></div>)',
        r"\1" + GDPR_REQUIRED + r"\2",
        text,
        flags=re.I,
    )
    text = re.sub(
        r'(<label for="f-gdpr">)(?!Ho preso visione dell\'<a href="privacy")[^<]+(?:<[^>]+>[^<]*)*(</label>)',
        r"\1" + GDPR_REQUIRED + r"\2",
        text,
        flags=re.I,
    )
    return text


def fix_landing_news_labels(text: str) -> str:
    return LANDING_NEWS_OLD.sub(GDPR_MARKETING, text)


def add_marketing_checkbox(html: str) -> str:
    if "rig-gdpr-marketing" not in html and "f-gdpr-marketing" not in html:
        def repl_bl(m: re.Match) -> str:
            block = m.group(0)
            if "rig-gdpr-marketing" in block:
                return block
            return block + "\n      " + MARKETING_SNIPPET

        html = re.sub(
            r'<label class="bl-chk"[^>]*>.*?<input[^>]*(?:bl-gdpr|f-gdpr|id="gdpr")[^>]*required[^>]*>.*?</label>',
            repl_bl,
            html,
            flags=re.I | re.S,
        )
        if 'id="f-gdpr"' in html and "f-gdpr-marketing" not in html:
            html = re.sub(
                r'(<div class="fchk"><input type="checkbox" id="f-gdpr"[^>]*><label for="f-gdpr">.*?</label></div>)',
                r"\1\n      " + FCHK_MARKETING,
                html,
                count=1,
                flags=re.I | re.S,
            )
        if (
            'id="gdpr"' in html
            and "rig-gdpr-marketing" not in html
            and "landing-consulenza-immobiliare-gratuita" in html
        ):
            html = html.replace(
                '<button type="submit" class="v-submit">',
                '    <label class="v-chk v-chk-opt"><input type="checkbox" class="rig-gdpr-marketing" name="gdpr_marketing"> '
                + f"<span>{GDPR_MARKETING}</span></label>\n    "
                + '<button type="submit" class="v-submit">',
                1,
            )
        if 'id="f-gdpr"' in html and "f-gdpr-marketing" not in html and "contact-form" in html:
            html = html.replace(
                '</div>\n      <button type="submit"',
                CONTATTI_MARKETING + '\n      <button type="submit"',
                1,
            )

    for prefix in ("a", "v", "l"):
        rid = f"{prefix}-news"
        if f'id="{rid}"' in html and 'class="rig-gdpr-marketing"' not in html:
            html = re.sub(
                rf'(<input type="checkbox" id="{rid}"[^>]*)>',
                rf'\1 class="rig-gdpr-marketing" name="gdpr_marketing">',
                html,
                count=1,
            )
    return html


def process_file(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return False
    orig = text
    if path.suffix in {".html", ".js", ".json", ".md"}:
        text = fix_phones(text)
        text = fix_addresses(text)
    if path.suffix == ".html":
        text = fix_gdpr_labels(text)
        text = fix_landing_news_labels(text)
        if "checkbox" in text and ("gdpr" in text.lower() or "privacy" in text.lower()):
            text = add_marketing_checkbox(text)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def bump_asset_version(asset: str, version: str) -> int:
    n = 0
    rx = re.compile(re.escape(asset) + r"\?v=\d+")
    repl = f"{asset}?v={version}"
    for p in ROOT.rglob("*.html"):
        if any(s in p.parts for s in SKIP_DIRS):
            continue
        t = p.read_text(encoding="utf-8")
        if asset + "?v=" in t:
            t2 = rx.sub(repl, t)
            if t2 != t:
                p.write_text(t2, encoding="utf-8")
                n += 1
    return n


def main() -> None:
    changed = []
    for p in iter_files():
        if process_file(p):
            changed.append(p.relative_to(ROOT))
    bumped_js = bump_asset_version("rig-lead-form.js", "2")
    bumped_css = bump_asset_version("blog-lead-form.css", "2")
    print(f"File aggiornati: {len(changed)}")
    print(f"rig-lead-form.js?v=3 in {bumped_js} pagine")
    print(f"blog-lead-form.css?v=2 in {bumped_css} pagine")
    for c in changed[:40]:
        print(f"  - {c}")
    if len(changed) > 40:
        print(f"  ... e altri {len(changed) - 40}")


if __name__ == "__main__":
    main()
