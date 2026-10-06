# -*- coding: utf-8 -*-
"""Rimuove padding EXP / Scenario bonus dai 3 articoli fisco ott 2026 e aggiorna wordCount."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "_lug28", ROOT / "scripts" / "build_blog_batch_lug28_2026.py"
)
_lug = importlib.util.module_from_spec(_spec)
assert _spec.loader
_spec.loader.exec_module(_lug)
wc = _lug.wc

FILES = [
    "blog-bonus-casa-2027-detrazioni-padova.html",
    "blog-legge-bilancio-198-2026-bonus-edilizi-padova.html",
    "blog-bonus-mobili-barriere-architettoniche-2026-padova.html",
]

# Inizio blocco filler (primo <p> dopo contenuto strutturato)
FILLER_START = re.compile(
    r"(<p>A Padova molti proprietari rimandano il cappotto|<p>La Legge di Bilancio 2026 \(L\. 198/2025|<p>Il bonus mobili resta al 50%)",
    re.I,
)

CLAIM_MARK = re.compile(
    r"<p>Gruppo Immobiliare Righetto opera dal",
    re.I,
)

SCENARIO = re.compile(r"<p>Scenario bonus 2027 \(\d+\):[^<]*</p>\s*", re.I)

LEGE_CHECKLIST = """
<h2>Checklist fisco e rogito (sintesi)</h2>
<ul>
<li><strong>Fonti:</strong> PDF GU n. 301/2025 e scheda ADE aggiornata al 2026 — non blog di terzi.</li>
<li><strong>Inizio lavori:</strong> regola tecnica sull’anno precedente alla spesa; buffer CILA/SCIA e Soprintendenza a Padova.</li>
<li><strong>Ecobonus:</strong> comunicazioni ENEA nei termini; conservare ricevute anche se vendete subito dopo i lavori.</li>
<li><strong>Condominio:</strong> delibera su parti comuni prima di detrazioni condivise.</li>
<li><strong>Trattativa:</strong> in annuncio solo APE, conformità e prezzo coerente con OMI — niente detrazioni promesse all’acquirente.</li>
<li><strong>Ruoli:</strong> Righetto coordina valutazione e documenti urbanistici; aliquote e detrazioni restano in capo al commercialista.</li>
</ul>
"""


def strip_filler(html: str, slug: str) -> str:
    html = SCENARIO.sub("", html)
    m = FILLER_START.search(html)
    if not m:
        return html
    c = CLAIM_MARK.search(html, m.start())
    if not c:
        raise SystemExit(f"{slug}: marker CLAIM non trovato dopo filler")
    before = html[: m.start()]
    after = html[c.start() :]
    if "legge-bilancio-198" in slug and "Checklist fisco e rogito" not in before:
        before = before.rstrip() + "\n\n" + LEGE_CHECKLIST.strip() + "\n\n"
    return before + after


def update_wordcount(html: str, words: int) -> str:
    def repl(m: re.Match) -> str:
        data = json.loads(m.group(1))
        if data.get("@type") == "BlogPosting":
            data["wordCount"] = words
        return "<script type=\"application/ld+json\">" + json.dumps(
            data, ensure_ascii=False
        ) + "</script>"

    return re.sub(
        r'<script type="application/ld\+json">(\{[^<]*"@type":\s*"BlogPosting"[^<]*\})</script>',
        repl,
        html,
        count=1,
    )


def body_words(html: str) -> int:
    m = re.search(r'class="art-content">\s*(.*?)\s*<div class="faq-section"', html, re.S)
    if not m:
        m = re.search(r'class="art-content">\s*(.*?)\s*<div class="cta-banner"', html, re.S)
    text = re.sub(r"<[^>]+>", " ", m.group(1) if m else html)
    return wc(text)


def main() -> None:
    for name in FILES:
        path = ROOT / name
        raw = path.read_text(encoding="utf-8")
        cleaned = strip_filler(raw, name)
        words = body_words(cleaned)
        cleaned = update_wordcount(cleaned, words)
        path.write_text(cleaned, encoding="utf-8")
        print(f"OK {name} — wordCount corpo ~{words}")


if __name__ == "__main__":
    main()
