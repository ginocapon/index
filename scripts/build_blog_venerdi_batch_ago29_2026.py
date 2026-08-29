# -*- coding: utf-8 -*-
"""Genera 5 articoli blog venerdì 29 agosto 2026 — canone concordato, gergo, Euribor, registro, visura.
Esegui da repo root: python scripts/build_blog_venerdi_batch_ago29_2026.py

Mapping immagini (ensure_images — copy da img/blog esistenti):
  blog-canone-concordato-padova-guida-2026
    hero ← blog-appartamento-affitto-limena-contratto-2026.webp
    body ← blog-rental-contract-padova-guide-2026.webp, blog-affitti-canoni-fimaa-q1-2026-padova.webp,
           blog-quattro-imposte-rogitio-prima-casa-padova-2026.webp
  blog-gergo-immobiliare-padova-spiegato-2026
    hero ← blog-5-domande-appuntamento-agenzia-padova-2026.webp
    body ← blog-scegliere-immobile-giusto-padova-2026.webp, blog-agenzia-top-servizi-padova-2026.webp,
           blog-documenti-compravendita-rogito-padova-2026.webp
  blog-tassi-euribor-mutui-padova-agosto-2026
    hero ← blog-tassi-mutui-minimi-padova-2026.webp
    body ← blog-barometro-mutui-crif-padova-2026.webp, blog-bce-tassi-mutui-giugno-2026-padova.webp,
           blog-sondaggio-bancaditalia-q1-2026.webp
  blog-registro-contratti-affitto-padova-2026
    hero ← blog-rental-contract-padova-guide-2026.webp
    body ← blog-appartamento-affitto-limena-contratto-2026.webp, blog-italy-rental-market-january-2026.webp,
           blog-affitti-canoni-fimaa-q1-2026-padova.webp
  blog-visura-catastale-acquisto-casa-padova-2026
    hero ← blog-documenti-compravendita-rogito-padova-2026.webp
    body ← blog-checklist-verifiche-prima-compromesso-padova-2026.webp, blog-dieci-errori-acquisto-casa-padova-2026.webp,
           blog-quattro-imposte-rogitio-prima-casa-padova-2026.webp
"""
from __future__ import annotations

import importlib.util
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE_IT = "29 agosto 2026"
DATE_ISO = "2026-08-29"
TIME_TS = "2026-08-29T09:00:00+02:00"

_BATCH_PATH = ROOT / "scripts" / "build_blog_batch_lug28_2026.py"
_spec = importlib.util.spec_from_file_location("_blog_batch_lug28", _BATCH_PATH)
_batch = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_batch)

_batch.DATE_ISO = DATE_ISO
_batch.DATE_IT = DATE_IT
_batch.TIME_TS = TIME_TS

CHART_WRAP_CSS = """
.chart-wrap{background:var(--sfondo);border:1px solid var(--gc);border-radius:12px;padding:1.2rem;margin:1.4rem 0}
.chart-wrap figcaption{font-size:.72rem;color:var(--grigio);margin-top:.6rem;text-align:center}
"""
STYLE_BLOCK = _batch.STYLE_BLOCK + CHART_WRAP_CSS
_batch.STYLE_BLOCK = STYLE_BLOCK

wc = _batch.wc
aeo_box = _batch.aeo_box
sol_box = _batch.sol_box
faq_html = _batch.faq_html
lead_form = _batch.lead_form
expand_body = _batch.expand_body
CLAIM_FOOT = _batch.CLAIM_FOOT
OMI_URL = _batch.OMI_URL
ISTAT_URL = _batch.ISTAT_URL
ADE_OSSERVATORIO = _batch.ADE_OSSERVATORIO
BANCA_ITALIA = _batch.BANCA_ITALIA
MIN_BODY_WORDS = _batch.MIN_BODY_WORDS
CAP_BLOG_AI = _batch.CAP_BLOG_AI

REGISTRY_PATH = ROOT / "scripts" / "venerdi_ago29_2026_registry.json"
EDITORIAL_QUEUE_PATH = ROOT / "data" / "editorial-queue.json"

ADE_REGISTRO = (
    "https://www.agenziaentrate.gov.it/portale/schede/contratti-di-locazione/"
    "registro-contratti-di-locazione"
)
GU_URL = "https://www.gazzettaufficiale.it"
ADE_CATASTO = (
    "https://www.agenziaentrate.gov.it/portale/schede/fabbricatiterreni/"
    "visure-catastali-e-planimetrie"
)
ECB_RATES = "https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html"
MEF_ACCORDI = "https://www.mef.gov.it/focus/Accordi-territoriali-per-la-locazione"
FIMAA_VENETO = "https://www.fimaaveneto.it"
NOTAI_VISURA = "https://notaionline.it/guida/visura-catastale-cosa-serve/"
CRIF_BAROMETRO = "https://www.crif.com/it/barometro-mutui/"

# sorgente → destinazione per ensure_images()
IMAGE_SOURCES: dict[str, dict[str, tuple[str, str] | list[tuple[str, str]]]] = {
    "blog-canone-concordato-padova-guida-2026": {
        "hero": (
            "img/blog/blog-appartamento-affitto-limena-contratto-2026.webp",
            "img/blog/blog-canone-concordato-padova-guida-2026-hero.webp",
        ),
        "body": [
            (
                "img/blog/blog-rental-contract-padova-guide-2026.webp",
                "img/blog/blog-canone-concordato-padova-accordo.webp",
            ),
            (
                "img/blog/blog-affitti-canoni-fimaa-q1-2026-padova.webp",
                "img/blog/blog-canone-concordato-padova-fasce.webp",
            ),
            (
                "img/blog/blog-quattro-imposte-rogitio-prima-casa-padova-2026.webp",
                "img/blog/blog-canone-concordato-padova-cedolare.webp",
            ),
        ],
    },
    "blog-gergo-immobiliare-padova-spiegato-2026": {
        "hero": (
            "img/blog/blog-5-domande-appuntamento-agenzia-padova-2026.webp",
            "img/blog/blog-gergo-immobiliare-padova-spiegato-2026-hero.webp",
        ),
        "body": [
            (
                "img/blog/blog-scegliere-immobile-giusto-padova-2026.webp",
                "img/blog/blog-gergo-immobiliare-padova-termini.webp",
            ),
            (
                "img/blog/blog-agenzia-top-servizi-padova-2026.webp",
                "img/blog/blog-gergo-immobiliare-padova-agenzia.webp",
            ),
            (
                "img/blog/blog-documenti-compravendita-rogito-padova-2026.webp",
                "img/blog/blog-gergo-immobiliare-padova-documenti.webp",
            ),
        ],
    },
    "blog-tassi-euribor-mutui-padova-agosto-2026": {
        "hero": (
            "img/blog/blog-tassi-mutui-minimi-padova-2026.webp",
            "img/blog/blog-tassi-euribor-mutui-padova-agosto-2026-hero.webp",
        ),
        "body": [
            (
                "img/blog/blog-barometro-mutui-crif-padova-2026.webp",
                "img/blog/blog-tassi-euribor-mutui-padova-grafico.webp",
            ),
            (
                "img/blog/blog-bce-tassi-mutui-giugno-2026-padova.webp",
                "img/blog/blog-tassi-euribor-mutui-padova-bce.webp",
            ),
            (
                "img/blog/blog-sondaggio-bancaditalia-q1-2026.webp",
                "img/blog/blog-tassi-euribor-mutui-padova-indagine.webp",
            ),
        ],
    },
    "blog-registro-contratti-affitto-padova-2026": {
        "hero": (
            "img/blog/blog-rental-contract-padova-guide-2026.webp",
            "img/blog/blog-registro-contratti-affitto-padova-2026-hero.webp",
        ),
        "body": [
            (
                "img/blog/blog-appartamento-affitto-limena-contratto-2026.webp",
                "img/blog/blog-registro-contratti-affitto-padova-limena.webp",
            ),
            (
                "img/blog/blog-italy-rental-market-january-2026.webp",
                "img/blog/blog-registro-contratti-affitto-padova-ade.webp",
            ),
            (
                "img/blog/blog-affitti-canoni-fimaa-q1-2026-padova.webp",
                "img/blog/blog-registro-contratti-affitto-padova-canoni.webp",
            ),
        ],
    },
    "blog-visura-catastale-acquisto-casa-padova-2026": {
        "hero": (
            "img/blog/blog-documenti-compravendita-rogito-padova-2026.webp",
            "img/blog/blog-visura-catastale-acquisto-casa-padova-2026-hero.webp",
        ),
        "body": [
            (
                "img/blog/blog-checklist-verifiche-prima-compromesso-padova-2026.webp",
                "img/blog/blog-visura-catastale-acquisto-casa-padova-checklist.webp",
            ),
            (
                "img/blog/blog-dieci-errori-acquisto-casa-padova-2026.webp",
                "img/blog/blog-visura-catastale-acquisto-casa-padova-errori.webp",
            ),
            (
                "img/blog/blog-quattro-imposte-rogitio-prima-casa-padova-2026.webp",
                "img/blog/blog-visura-catastale-acquisto-casa-padova-planimetria.webp",
            ),
        ],
    },
}


def blog_fig(src: str, alt: str, cap: str | None = None) -> str:
    caption = cap if cap is not None else CAP_BLOG_AI
    return (
        f'<figure class="blog-fig rig-ai-photo-wrap"><div class="blog-fig__frame">'
        f'<img src="{src}" alt="{alt}" width="1900" height="900" loading="lazy" data-ai-generated="true">'
        f'</div><span class="rig-ai-photo-watermark" aria-hidden="true">FOTO AI</span>'
        f'<figcaption class="rig-photo-caption">{caption}</figcaption></figure>'
    )


def build_html(cfg: dict, content: str, words: int) -> str:
    html = _batch.build_html(cfg, content, words)
    hero = cfg["hero"]
    old = (
        f'<div class="art-hero"><div class="art-hero__frame">\n'
        f'<img class="art-hero-img" src="{hero}" alt="{cfg["hero_alt"]}" '
        f'width="1200" height="630" fetchpriority="high">\n</div>'
    )
    new = (
        f'<div class="art-hero"><div class="art-hero__frame rig-ai-photo-wrap">\n'
        f'<img class="art-hero-img" src="{hero}" alt="{cfg["hero_alt"]}" '
        f'width="1900" height="900" fetchpriority="high" data-ai-generated="true">\n'
        f'<span class="rig-ai-photo-watermark" aria-hidden="true">FOTO AI</span>\n</div>'
    )
    return html.replace(old, new, 1)


def ensure_images() -> None:
    """Copia webp esistenti in img/blog verso path dedicati batch (hero + 3 body per articolo)."""
    copied = 0
    for slug, mapping in IMAGE_SOURCES.items():
        hero_src, hero_dst = mapping["hero"]
        src_p = ROOT / hero_src
        dst_p = ROOT / hero_dst
        if not src_p.is_file():
            raise SystemExit(f"ensure_images: sorgente mancante {hero_src} per {slug}")
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_p, dst_p)
        copied += 1
        for body_src, body_dst in mapping["body"]:
            bsrc = ROOT / body_src
            bdst = ROOT / body_dst
            if not bsrc.is_file():
                raise SystemExit(f"ensure_images: sorgente mancante {body_src} per {slug}")
            shutil.copy2(bsrc, bdst)
            copied += 1
    print(f"ensure_images: {copied} file webp copiati")


# ── SVG chart-wrap (≥2 per articolo) ────────────────────────────────────────


def svg_concordato_fasce() -> str:
    return f"""<figure class="chart-wrap" aria-label="Schema fasce canone concordato Padova">
<svg viewBox="0 0 540 240" width="100%" height="240" role="img">
<title>Fasce canone concordato per zona Padova — schema indicativo</title>
<text x="270" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Canone concordato Padova: zone e fasce (schema)</text>
<rect x="40" y="45" width="140" height="70" rx="8" fill="#2C4A6E" opacity="0.85"/>
<text x="110" y="72" text-anchor="middle" font-size="10" fill="#fff">Centro</text>
<text x="110" y="92" text-anchor="middle" font-size="8" fill="rgba(255,255,255,.8)">Fascia alta</text>
<rect x="200" y="55" width="140" height="60" rx="8" fill="#3A5F8C"/>
<text x="270" y="80" text-anchor="middle" font-size="10" fill="#fff">Semicentro</text>
<text x="270" y="98" text-anchor="middle" font-size="8" fill="rgba(255,255,255,.8)">Fascia media</text>
<rect x="360" y="65" width="140" height="50" rx="8" fill="#FF6B35" opacity="0.9"/>
<text x="430" y="88" text-anchor="middle" font-size="10" fill="#152435">Periferia</text>
<text x="430" y="104" text-anchor="middle" font-size="8" fill="#152435">Fascia più bassa</text>
<text x="270" y="210" text-anchor="middle" font-size="8" fill="#6B7A8D">Fonte metodo: accordo territoriale MEF/Comune — verificare testo vigente</text>
</svg>
<figcaption>Schema zone canone concordato Padova. Valori €/mq da accordo territoriale e attestazione sindacale — non da OMI vendita.</figcaption>
</figure>"""


def svg_concordato_fiscale() -> str:
    return """<figure class="chart-wrap" aria-label="Confronto cedolare concordato vs libero">
<svg viewBox="0 0 520 220" width="100%" height="220" role="img">
<title>Cedolare secca 10% concordato vs 21% libero — esempio didattico</title>
<text x="260" y="20" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Cedolare secca: concordato 10% vs libero 21% (esempio)</text>
<rect x="60" y="50" width="180" height="35" rx="6" fill="#2C4A6E"/><text x="150" y="72" text-anchor="middle" font-size="9" fill="#fff">Canone annuo 7.200 €</text>
<rect x="60" y="95" width="80" height="28" rx="6" fill="#FF6B35"/><text x="100" y="113" text-anchor="middle" font-size="8" fill="#152435">720 € (10%)</text>
<rect x="280" y="50" width="180" height="35" rx="6" fill="#6B7A8D"/><text x="370" y="72" text-anchor="middle" font-size="9" fill="#fff">Stesso canone libero</text>
<rect x="280" y="95" width="120" height="28" rx="6" fill="#E1DBD1"/><text x="340" y="113" text-anchor="middle" font-size="8" fill="#152435">1.512 € (21%)</text>
<text x="260" y="175" text-anchor="middle" font-size="8" fill="#6B7A8D">Dichiarazione: esempio didattico — aliquote da normativa ADE vigente</text>
</svg>
<figcaption>Confronto cedolare secca concordato (10%) vs libero (21%) su canone annuo esemplificativo. Verificare con commercialista.</figcaption>
</figure>"""


def svg_gergo_mappa() -> str:
    return """<figure class="chart-wrap" aria-label="Mappa termini gergo immobiliare">
<svg viewBox="0 0 540 260" width="100%" height="260" role="img">
<title>Termini immobiliari: catastale, urbanistico, contrattuale</title>
<text x="270" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Gergo immobiliare: tre famiglie di termini</text>
<rect x="30" y="45" width="150" height="90" rx="10" fill="#2C4A6E"/>
<text x="105" y="75" text-anchor="middle" font-size="10" fill="#fff">Catastale</text>
<text x="105" y="95" text-anchor="middle" font-size="7" fill="rgba(255,255,255,.85)">subalterno · categoria</text>
<text x="105" y="110" text-anchor="middle" font-size="7" fill="rgba(255,255,255,.85)">rendita · consistenza</text>
<rect x="195" y="45" width="150" height="90" rx="10" fill="#FF6B35" opacity="0.9"/>
<text x="270" y="75" text-anchor="middle" font-size="10" fill="#152435">Urbanistico</text>
<text x="270" y="95" text-anchor="middle" font-size="7" fill="#152435">APE · conformità</text>
<text x="270" y="110" text-anchor="middle" font-size="7" fill="#152435">planimetria · titolo edilizio</text>
<rect x="360" y="45" width="150" height="90" rx="10" fill="#3A5F8C"/>
<text x="435" y="75" text-anchor="middle" font-size="10" fill="#fff">Contrattuale</text>
<text x="435" y="95" text-anchor="middle" font-size="7" fill="rgba(255,255,255,.85)">4+4 · caparra</text>
<text x="435" y="110" text-anchor="middle" font-size="7" fill="rgba(255,255,255,.85)">rogito · perizia</text>
<text x="270" y="230" text-anchor="middle" font-size="8" fill="#6B7A8D">Analisi Righetto — glossario operativo Padova/Veneto 2026</text>
</svg>
<figcaption>Tre famiglie di termini nel gergo immobiliare padovano: catastale, urbanistico, contrattuale.</figcaption>
</figure>"""


def svg_gergo_flusso() -> str:
    return """<figure class="chart-wrap" aria-label="Flusso documenti compravendita">
<svg viewBox="0 0 520 280" width="100%" height="280" role="img">
<title>Visura → planimetria → rogito</title>
<text x="260" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Dal gergo alla pratica: documenti in sequenza</text>
<rect x="185" y="38" width="150" height="34" rx="17" fill="#2C4A6E"/><text x="260" y="60" text-anchor="middle" font-size="9" fill="#fff">Visura catastale</text>
<path d="M260 72 L260 88" stroke="#FF6B35" stroke-width="2"/>
<rect x="185" y="88" width="150" height="34" rx="17" fill="#2C4A6E"/><text x="260" y="110" text-anchor="middle" font-size="9" fill="#fff">Planimetria ADE</text>
<path d="M260 122 L260 138" stroke="#FF6B35" stroke-width="2"/>
<rect x="185" y="138" width="150" height="34" rx="17" fill="#FF6B35"/><text x="260" y="160" text-anchor="middle" font-size="9" fill="#152435">APE + conformità</text>
<path d="M260 172 L260 188" stroke="#FF6B35" stroke-width="2"/>
<rect x="185" y="188" width="150" height="34" rx="17" fill="#2C4A6E"/><text x="260" y="210" text-anchor="middle" font-size="9" fill="#fff">Rogito notarile</text>
<text x="260" y="255" text-anchor="middle" font-size="8" fill="#6B7A8D">Fatto: documenti obbligatori · Analisi: ordine consigliato in trattativa Padova</text>
</svg>
<figcaption>Sequenza documenti dalla visura al rogito — glossario applicato all'acquisto a Padova.</figcaption>
</figure>"""


def svg_euribor_trend() -> str:
    return f"""<figure class="chart-wrap" aria-label="Euribor e mutui schema agosto 2026">
<svg viewBox="0 0 560 240" width="100%" height="240" role="img">
<title>Euribor 3M e spread mutuo — schema</title>
<text x="280" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Euribor 3M + spread banca = tasso variabile (schema)</text>
<line x1="60" y1="180" x2="500" y2="180" stroke="#E1DBD1" stroke-width="2"/>
<rect x="80" y="120" width="60" height="60" fill="#2C4A6E" opacity="0.8"/>
<text x="110" y="115" text-anchor="middle" font-size="8" fill="#6B7A8D">Gen</text>
<rect x="160" y="100" width="60" height="80" fill="#3A5F8C"/>
<text x="190" y="95" text-anchor="middle" font-size="8" fill="#6B7A8D">Apr</text>
<rect x="240" y="90" width="60" height="90" fill="#FF6B35" opacity="0.85"/>
<text x="270" y="85" text-anchor="middle" font-size="8" fill="#6B7A8D">Lug</text>
<rect x="320" y="105" width="60" height="75" fill="#3A5F8C"/>
<text x="350" y="100" text-anchor="middle" font-size="8" fill="#6B7A8D">Ago</text>
<text x="280" y="210" text-anchor="middle" font-size="8" fill="#6B7A8D">Fonte: BCE tassi · Euribor EMMI — valori da verificare al preventivo banca</text>
</svg>
<figcaption>Schema andamento Euribor 3M (indicativo). Per mutuo a Padova: TAEG e spread da <a href="{BANCA_ITALIA}">Banca d'Italia</a> e istituto di credito.</figcaption>
</figure>"""


def svg_euribor_fisso_var() -> str:
    return """<figure class="chart-wrap" aria-label="Confronto tasso fisso vs variabile">
<svg viewBox="0 0 520 220" width="100%" height="220" role="img">
<title>Fisso prevedibile vs variabile legato a Euribor</title>
<text x="260" y="20" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Mutuo fisso vs variabile (Euribor) — profili</text>
<rect x="40" y="45" width="200" height="55" rx="8" fill="#2C4A6E"/>
<text x="140" y="68" text-anchor="middle" font-size="10" fill="#fff" font-weight="600">TASSO FISSO</text>
<text x="140" y="88" text-anchor="middle" font-size="8" fill="rgba(255,255,255,.85)">Rata stabile · spread iniziale</text>
<rect x="280" y="45" width="200" height="55" rx="8" fill="#FF6B35" opacity="0.9"/>
<text x="380" y="68" text-anchor="middle" font-size="10" fill="#152435" font-weight="600">TASSO VARIABILE</text>
<text x="380" y="88" text-anchor="middle" font-size="8" fill="#152435">Euribor + spread · rata variabile</text>
<text x="260" y="165" text-anchor="middle" font-size="8" fill="#6B7A8D">Analisi: scelta in base a orizzonte e tolleranza rischio — no promessa tasso</text>
</svg>
<figcaption>Confronto qualitativo mutuo fisso e variabile legato a Euribor. Simulazione personalizzata con banca o servizio mutuo Righetto.</figcaption>
</figure>"""


def svg_registro_flow() -> str:
    return f"""<figure class="chart-wrap" aria-label="Flusso registrazione contratto affitto ADE">
<svg viewBox="0 0 520 300" width="100%" height="300" role="img">
<title>Registro contratti locazione ADE — 30 giorni</title>
<text x="260" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Registro contratti affitto: tempistiche ADE</text>
<rect x="185" y="38" width="150" height="34" rx="17" fill="#2C4A6E"/><text x="260" y="60" text-anchor="middle" font-size="9" fill="#fff">1. Firma contratto</text>
<path d="M260 72 L260 88" stroke="#FF6B35" stroke-width="2"/>
<rect x="185" y="88" width="150" height="34" rx="17" fill="#FF6B35"/><text x="260" y="110" text-anchor="middle" font-size="9" fill="#152435">2. Entro 30 gg ADE</text>
<path d="M260 122 L260 138" stroke="#FF6B35" stroke-width="2"/>
<rect x="185" y="138" width="150" height="34" rx="17" fill="#2C4A6E"/><text x="260" y="160" text-anchor="middle" font-size="9" fill="#fff">3. Ricevuta registrazione</text>
<path d="M260 172 L260 188" stroke="#FF6B35" stroke-width="2"/>
<rect x="185" y="188" width="150" height="34" rx="17" fill="#2C4A6E"/><text x="260" y="210" text-anchor="middle" font-size="9" fill="#fff">4. Detrazioni / anagrafe</text>
<text x="260" y="265" text-anchor="middle" font-size="8" fill="#6B7A8D">Fatto: termine 30 giorni — <a href="{ADE_REGISTRO}">Registro contratti ADE</a></text>
</svg>
<figcaption>Percorso registrazione contratto di locazione presso Agenzia delle Entrate entro 30 giorni dalla stipula.</figcaption>
</figure>"""


def svg_registro_tipologie() -> str:
    return """<figure class="chart-wrap" aria-label="Tipologie contratto e registro">
<svg viewBox="0 0 540 220" width="100%" height="220" role="img">
<title>4+4 vs concordato vs transitorio — registro</title>
<text x="270" y="20" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Contratti locazione Padova: chi va in registro ADE</text>
<rect x="30" y="45" width="150" height="50" rx="8" fill="#2C4A6E"/><text x="105" y="68" text-anchor="middle" font-size="9" fill="#fff">4+4 libero</text>
<text x="105" y="85" text-anchor="middle" font-size="7" fill="rgba(255,255,255,.8)">Registro obbligatorio</text>
<rect x="195" y="45" width="150" height="50" rx="8" fill="#FF6B35" opacity="0.9"/><text x="270" y="68" text-anchor="middle" font-size="9" fill="#152435">Concordato 3+2</text>
<text x="270" y="85" text-anchor="middle" font-size="7" fill="#152435">Registro + agevolazioni</text>
<rect x="360" y="45" width="150" height="50" rx="8" fill="#3A5F8C"/><text x="435" y="68" text-anchor="middle" font-size="9" fill="#fff">Transitorio</text>
<text x="435" y="85" text-anchor="middle" font-size="7" fill="rgba(255,255,255,.8)">Requisiti specifici</text>
<text x="270" y="175" text-anchor="middle" font-size="8" fill="#6B7A8D">Tutti richiedono registrazione — imposte e detrazioni diverse</text>
</svg>
<figcaption>Tipologie contrattuali locazione a Padova: tutte vanno registrate; fiscalità e canone differiscono.</figcaption>
</figure>"""


def svg_visura_campi() -> str:
    return """<figure class="chart-wrap" aria-label="Campi visura catastale">
<svg viewBox="0 0 540 240" width="100%" height="240" role="img">
<title>Foglio particella subalterno categoria rendita</title>
<text x="270" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Visura catastale: campi essenziali</text>
<rect x="40" y="50" width="100" height="40" rx="6" fill="#2C4A6E"/><text x="90" y="75" text-anchor="middle" font-size="9" fill="#fff">Foglio</text>
<rect x="150" y="50" width="100" height="40" rx="6" fill="#3A5F8C"/><text x="200" y="75" text-anchor="middle" font-size="9" fill="#fff">Particella</text>
<rect x="260" y="50" width="100" height="40" rx="6" fill="#FF6B35"/><text x="310" y="75" text-anchor="middle" font-size="9" fill="#152435">Subalterno</text>
<rect x="370" y="50" width="130" height="40" rx="6" fill="#2C4A6E" opacity="0.85"/><text x="435" y="75" text-anchor="middle" font-size="9" fill="#fff">Categoria</text>
<rect x="40" y="110" width="220" height="40" rx="6" fill="#E1DBD1"/><text x="150" y="135" text-anchor="middle" font-size="9" fill="#152435">Consistenza (mq/vani)</text>
<rect x="280" y="110" width="220" height="40" rx="6" fill="#E1DBD1"/><text x="390" y="135" text-anchor="middle" font-size="9" fill="#152435">Rendita catastale</text>
<text x="270" y="210" text-anchor="middle" font-size="8" fill="#6B7A8D">Fatto: dati da visura ADE · Analisi: incrocio con planimetria e stato di fatto</text>
</svg>
<figcaption>Campi principali della visura catastale per immobile a Padova — base per perizia e rogito.</figcaption>
</figure>"""


def svg_visura_percorso() -> str:
    return """<figure class="chart-wrap" aria-label="Percorso visura in acquisto">
<svg viewBox="0 0 520 280" width="100%" height="280" role="img">
<title>Visura prima del compromesso</title>
<text x="260" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Visura catastale nell'acquisto casa Padova</text>
<rect x="185" y="38" width="150" height="34" rx="17" fill="#2C4A6E"/><text x="260" y="60" text-anchor="middle" font-size="9" fill="#fff">Prima visita</text>
<path d="M260 72 L260 88" stroke="#FF6B35" stroke-width="2"/>
<rect x="185" y="88" width="150" height="34" rx="17" fill="#FF6B35"/><text x="260" y="110" text-anchor="middle" font-size="9" fill="#152435">Richiesta visura</text>
<path d="M260 122 L260 138" stroke="#FF6B35" stroke-width="2"/>
<rect x="185" y="138" width="150" height="34" rx="17" fill="#2C4A6E"/><text x="260" y="160" text-anchor="middle" font-size="9" fill="#fff">Confronto planimetria</text>
<path d="M260 172 L260 188" stroke="#FF6B35" stroke-width="2"/>
<rect x="185" y="188" width="150" height="34" rx="17" fill="#2C4A6E"/><text x="260" y="210" text-anchor="middle" font-size="9" fill="#fff">Compromesso / rogito</text>
<text x="260" y="255" text-anchor="middle" font-size="8" fill="#6B7A8D">Consiglio operativo Righetto: visura aggiornata prima della caparra</text>
</svg>
<figcaption>Percorso consigliato: visura catastale e planimetria prima di impegno economico significativo.</figcaption>
</figure>"""


def _exp(prefix: str, n: int, templates: list[str]) -> list[str]:
    """Genera pool espansione con prefisso tematico + template variati."""
    base = [t.format(p=prefix) for t in templates]
    extra: list[str] = []
    idx = 1
    while len(base) + len(extra) < n:
        extra.append(
            f"{prefix}: approfondimento {idx} — incrociare fonti ADE, OMI o ISTAT; "
            f"distinguere fatto normativo, dichiarazione annuncio e analisi mercato Padova/Veneto."
        )
        idx += 1
    return base + extra


_EXP_T = [
    "{p} nel Padovano richiede distinzione tra fatto normativo (testo legge, circolari ADE), dichiarazione del locatore o venditore e analisi di mercato locale.",
    "{p}: l'accordo territoriale MEF definisce le fasce — verificare sul portale istituzionale e non su post social datati.",
    "{p} a Limena e in cintura segue le stesse regole nazionali con microzone OMI diverse dal centro storico padovano.",
    "{p}: Righetto coordina visite e contratti dal 2000 — compenso concordato in sede, nessun listino percentuale online.",
    "{p} — cross-link utili: servizio locazioni, zona Limena e guide affitti 2026 senza duplicare angoli editoriali esistenti.",
    "{p}: ISTAT e Osservatorio ADE danno contesto macro Veneto; per il singolo bilocale servono comparabili e visita.",
    "{p}: red flag — annunci senza APE, rifiuto planimetria o richiesta pagamenti non tracciati prima del contratto scritto.",
    "{p}: detrazioni fiscali richiedono contratto registrato e pagamenti tracciabili — conservare ricevute ADE.",
    "{p}: studenti e famiglie convivono nel mercato padovano — domanda universitaria e ospedaliera sostiene certe microzone.",
    "{p}: pendolari verso Mestre o Vicenza valutano Limena per metratura e canone — calcolare costo totale spostamento.",
]

EXPANSION_CANONE = _exp("Canone concordato Padova 2026", 70, _EXP_T + [
    "Canone concordato Padova 2026: la cedolare secca al 10% è fatto normativo per contratti in attestazione — la convenienza netta è analisi con commercialista.",
    "Canone concordato Padova 2026: durata 3+2 con rinnovo biennale automatico salvo disdetta — leggere termini e clausole ISTAT nel contratto tipo.",
    "Canone concordato Padova 2026: attestazione tramite organizzazioni sindacali firmatarie dell'accordo — tempi da pianificare prima del via libera locazione.",
    "Canone concordato Padova 2026: riduzione IMU 25% per proprietario è agevolazione fiscale verificabile — non confondere con canone libero 4+4.",
    "Canone concordato Padova 2026: inquilino può accedere a detrazioni IRPEF se requisiti reddituali — dichiarazione da confermare con CAF o commercialista.",
    "Canone concordato Padova 2026: differenza da blog-contratto-affitto-padova — qui focus 2026 su fasce, fiscalità e percorso pratico aggiornato.",
    "Canone concordato Padova 2026: zone Arcella e Portello hanno fasce diverse dal centro — mappa accordo territoriale è riferimento ufficiale.",
    "Canone concordato Padova 2026: proprietario che passa da libero a concordato deve ricalcolare canone entro massimali — negoziazione con inquilino documentata.",
    "Canone concordato Padova 2026: registrazione ADE entro 30 giorni vale anche per concordato — stessa ricevuta per detrazioni.",
    "Canone concordato Padova 2026: per immobile in Limena applicare accordo del Comune di riferimento — verificare se Limena aderisce a accorpamento fasce provinciale.",
    "Canone concordato Padova 2026: FIMAA Veneto pubblica commenti mercato locativo — complemento analitico, non sostituto testo accordo.",
    "Canone concordato Padova 2026: canone sotto fascia minima invalida agevolazioni — attenzione a sconti non documentati in attestazione.",
    "Canone concordato Padova 2026: transitorio e concordato convivono — scelta dipende da durata prevista e requisiti legge.",
    "Canone concordato Padova 2026: studenti fuori sede spesso in libero per flessibilità — famiglie stabili più orientate a concordato per fiscalità.",
    "Canone concordato Padova 2026: caparra confirmatoria e concordato — stesse regole civilistiche del libero, fiscalità diversa post registrazione.",
    "Canone concordato Padova 2026: aggiornamento ISTAT in concordato va letto nel contratto — impatto su budget inquilino a medio termine.",
    "Canone concordato Padova 2026: servizio locazioni Righetto supporta scelta tipologia contrattuale — senza pubblicare tariffe mediazione.",
    "Canone concordato Padova 2026: Gazzetta Ufficiale per modifiche normative — consultare GU_URL quando circolano novità su locazioni.",
    "Canone concordato Padova 2026: comparare canone concordato calcolato con fascia OMI locazione ADE — doppio controllo prudenziale.",
    "Canone concordato Padova 2026: immobile non conforme urbanisticamente può bloccare locazione regolare — planimetria prima dell'attestazione.",
    "Canone concordato Padova 2026: subentro in concordato richiede nuova registrazione e verifica attestazione — pratica da non improvvisare.",
    "Canone concordato Padova 2026: deposito cauzionale massimo tre mensilità anche in concordato — stessa tutela locazioni ordinarie.",
    "Canone concordato Padova 2026: riscaldamento centralizzato incide su costo totale — chiedere ripartizione e ultimo rendiconto condominiale.",
    "Canone concordato Padova 2026: APE obbligatorio in locazione — classe energetica influenza anche scelta inquilino attento ai consumi.",
    "Canone concordato Padova 2026: form lead in fondo pagina per consulenza locazione — indicare tipologia immobile e zona preferita.",
])

EXPANSION_GERGO = _exp("Gergo immobiliare Padova", 75, _EXP_T + [
    "Gergo immobiliare Padova: «rendita catastale» è dato ufficiale visura — non equivale a canone di mercato né a valore OMI vendita.",
    "Gergo immobiliare Padova: «superficie commerciale» in annuncio può differire da consistenza catastale — fatto da visura, dichiarazione in annuncio.",
    "Gergo immobiliare Padova: «caparra confirmatoria» vs «acconto» — distinzione giuridica che cambia tutela in caso di recesso.",
    "Gergo immobiliare Padova: «rogito» è atto notarile di compravendita — analisi costi include imposte oltre prezzo immobile.",
    "Gergo immobiliare Padova: «perizia bancaria» valuta immobile per mutuo — può essere inferiore al prezzo richiesto dal venditore.",
    "Gergo immobiliare Padova: «mandato esclusivo» vincola vendita a una agenzia — termine da leggere prima della firma.",
    "Gergo immobiliare Padova: «APE» attesta prestazione energetica — validità e classe sono fatti verificabili su documento.",
    "Gergo immobiliare Padova: «conformità urbanistica» richiede confronto planimetria/stato di fatto — analisi tecnica, non slogan annuncio.",
    "Gergo immobiliare Padova: «subalterno» identifica unità in catasto — essenziale in visura e contratto.",
    "Gergo immobiliare Padova: «categoria catastale» (A/2, A/3…) incide su imposte — dichiarazione fiscale da confermare con notaio.",
    "Gergo immobiliare Padova: «surroghe» mutuo cambia banca mantenendo ipoteca — gergo bancario distinto da acquisto.",
    "Gergo immobiliare Padova: «TAEG» include spese — confrontare TAEG tra istituti, non solo tasso nominale.",
    "Gergo immobiliare Padova: «4+4» indica durata locazione standard — rinnovo e disdetta regolati da contratto e legge.",
    "Gergo immobiliare Padova: «cedolare secca» alternativa a IRPEF su locazione — scelta irrevocabile triennio.",
    "Gergo immobiliare Padova: «compromesso» impegna parti prima del rogito — caparra e condizioni sospensive vanno capite.",
    "Gergo immobiliare Padova: «nuda proprietà» vs «usufrutto» — gergo successioni rilevante in alcune compravendite padovane.",
    "Gergo immobiliare Padova: «servitù» e «vincoli» compaiono in visura ipotecaria — notaio approfondisce in due diligence.",
    "Gergo immobiliare Padova: «box auto» con subalterno separato — due unità catastali, due visure se pertinenza distinta.",
    "Gergo immobiliare Padova: agenzia seria spiega termini in visita — Righetto in Via Roma 96 dal 2000, 127 recensioni 4,9/5.",
    "Gergo immobiliare Padova: portali usano «trilocale» commercialmente — verificare vani catastali e planimetria.",
    "Gergo immobiliare Padova: «classe energetica G» segnala riqualificazione — analisi costi oltre prezzo acquisto.",
    "Gergo immobiliare Padova: «mutuo ipotecario» vs «fondiario» — gergo banca da chiarire in preventivo scritto.",
    "Gergo immobiliare Padova: «proposta d'acquisto» può essere vincolante — leggere clausole prima della firma.",
    "Gergo immobiliare Padova: «mediazione» compenso concordato in sede Righetto — mai percentuali inventate online.",
    "Gergo immobiliare Padova: glossario utile prima di appuntamento — articolo 5 domande agenzia complementare senza overlap.",
])

EXPANSION_EURIBOR = _exp("Tassi Euribor mutui Padova agosto 2026", 75, _EXP_T + [
    "Tassi Euribor mutui Padova agosto 2026: Euribor 3 mesi è parametro mutui variabili — valore da EMMI/BCE al momento preventivo.",
    "Tassi Euribor mutui Padova agosto 2026: Banca d'Italia pubblica indagini famiglie-imprese — contesto macro, non tasso personalizzato.",
    "Tassi Euribor mutui Padova agosto 2026: spread bancario aggiunto a Euribor — analisi TAEG obbligatoria nel confronto offerte.",
    "Tassi Euribor mutui Padova agosto 2026: tasso fisso elimina rischio Euribor — dichiarazione di preferenza personale, non consiglio universale.",
    "Tassi Euribor mutui Padova agosto 2026: differenza da blog-tassi-mutui-minimi — qui angolo Euribor e variabile agosto 2026.",
    "Tassi Euribor mutui Padova agosto 2026: BCE decide tassi di riferimento — Gazzetta e comunicati istituzionali per aggiornamenti.",
    "Tassi Euribor mutui Padova agosto 2026: perizia e OMI vendita incidono su LTV — fatto bancario indipendente da Euribor.",
    "Tassi Euribor mutui Padova agosto 2026: surroga può ridurre spread — analisi costi istruttoria e perizia nuova.",
    "Tassi Euribor mutui Padova agosto 2026: under 36 CONSAP attivo fino 31/12/2027 — garanzia distinta da parametro Euribor.",
    "Tassi Euribor mutui Padova agosto 2026: Limena trilocali richiedono importi mutuo maggiori — rata sensibile a variazioni Euribor.",
    "Tassi Euribor mutui Padova agosto 2026: CRIF barometro mutui indicativo nazionale — incrociare con offerta filiale Padova.",
    "Tassi Euribor mutui Padova agosto 2026: tasso variabile con cap opzionale — leggere clausola cap nel foglio informativo.",
    "Tassi Euribor mutui Padova agosto 2026: servizio mutuo Righetto orienta verso banche partner — senza promettere tassi.",
    "Tassi Euribor mutui Padova agosto 2026: ISTAT prezzi abitazioni complementa decisione acquisto — non sostituisce simulazione rata.",
    "Tassi Euribor mutui Padova agosto 2026: durata mutuo 20 vs 30 anni cambia impatto Euribor cumulato — analisi amortamento.",
    "Tassi Euribor mutui Padova agosto 2026: tasso misto (fisso poi variabile) — gergo da spiegare in preventivo scritto.",
    "Tassi Euribor mutui Padova agosto 2026: mercato padovano competitivo su ristrutturati — velocità offerta con pre-approvazione mutuo.",
    "Tassi Euribor mutui Padova agosto 2026: non pubblicare percentuali mutuo inventate — ogni TAEG è personalizzato.",
    "Tassi Euribor mutui Padova agosto 2026: polizza CPI obbligatoria — costo assicurativo nel calcolo rata totale.",
    "Tassi Euribor mutui Padova agosto 2026: form blog per consulenza — budget, zona, fisso o variabile preferito.",
    "Tassi Euribor mutui Padova agosto 2026: Euribor negativo storico chiuso — analisi su scenari positivi e neutrali.",
    "Tassi Euribor mutui Padova agosto 2026: acquisto prima casa Limena — confronto rata mutuo vs affitto equivalente.",
    "Tassi Euribor mutui Padova agosto 2026: documenti reddito autonomi — banca applica spread indipendentemente da Euribor.",
    "Tassi Euribor mutui Padova agosto 2026: tasso variabile consigliato solo dopo stress test rata +2% — analisi prudenziale.",
    "Tassi Euribor mutui Padova agosto 2026: landing consulenza gratuita per primo appuntamento mutuo-acquisto coordinato.",
])

EXPANSION_REGISTRO = _exp("Registro contratti affitto Padova", 78, _EXP_T + [
    "Registro contratti affitto Padova: obbligo entro 30 giorni dalla stipula — fatto Art. comm. locazione e servizi ADE online.",
    "Registro contratti affitto Padova: imposta di registro 2% canone annuo locazioni ordinarie — aliquote da verificare su circolare ADE.",
    "Registro contratti affitto Padova: ricevuta registrazione necessaria per detrazione 19% canone — dichiarazione redditi inquilino.",
    "Registro contratti affitto Padova: differenza da semplice «contratto scritto» — registro è passaggio fiscale obbligatorio.",
    "Registro contratti affitto Padova: rinnovo concordato va re-registrato — analisi tempistiche con commercialista.",
    "Registro contratti affitto Padova: cedolare secca incompatibile con alcune detrazioni — scelta irrevocabile triennio proprietario.",
    "Registro contratti affitto Padova: subentro richiede nuova registrazione entro termini — pratica ADE con dati nuovo inquilino.",
    "Registro contratti affitto Padova: contratto non registrato invalida certificazione residenza in molti casi — fatto anagrafe comunale.",
    "Registro contratti affitto Padova: registrazione online F24 — servizio locazioni Righetto supporta proprietari padovani.",
    "Registro contratti affitto Padova: multe per omessa registrazione — sanzioni da normativa, non stima inventata.",
    "Registro contratti affitto Padova: canone concordato e registro — stessa piattaforma ADE con codici tributo specifici.",
    "Registro contratti affitto Padova: transitorio documentato con requisiti — registro obbligatorio anche per durate brevi.",
    "Registro contratti affitto Padova: studenti: contratto intestato per detrazioni genitori — verificare requisiti reddituali.",
    "Registro contratti affitto Padova: Limena affitti in crescita — registro corretto tutela locatore e inquilino.",
    "Registro contratti affitto Padova: conservare PDF ricevuta ADE per tutta la durata locazione e dopo.",
    "Registro contratti affitto Padova: registrazione parziale o errata — rettifica presso ADE prima del contenzioso.",
    "Registro contratti affitto Padova: locazione turistica breve regime diverso — non confondere con registro 4+4 residenziale.",
    "Registro contratti affitto Padova: proprietario non residente — registro e imposte con stesse regole nazionali.",
    "Registro contratti affitto Padova: agevolazioni under 35 non sostituiscono registro — obbligo per tutti i contratti tipici.",
    "Registro contratti affitto Padova: cross-link blog-appartamento-affitto-limena-contratto — focus deposito e caparra.",
    "Registro contratti affitto Padova: ADE registro contratti portale ufficiale — ADE_REGISTRO bookmark consigliato.",
    "Registro contratti affitto Padova: pagamento canone cash ostacola detrazioni — fatto normativo pagamenti tracciabili.",
    "Registro contratti affitto Padova: proroga tacita 4+4 — nuova registrazione solo se canone cambia oltre soglie.",
    "Registro contratto affitto Padova: mediazione Righetto include verifica registrazione — compenso concordato in sede.",
    "Registro contratti affitto Padova: GU per modifiche imposta registro — monitorare decreti locazioni.",
])

EXPANSION_VISURA = _exp("Visura catastale acquisto Padova", 78, _EXP_T + [
    "Visura catastale acquisto Padova: documento ufficiale ADE — foglio, particella, subalterno identificano immobile univocamente.",
    "Visura catastale acquisto Padova: visura storica mostra variazioni — utile per analisi difformità pluriennali.",
    "Visura catastale acquisto Padova: planimetria catastale va confrontata con stato di fatto — difformità è rischio rogito.",
    "Visura catastale acquisto Padova: rendita catastale base imposte — non prezzo di mercato OMI.",
    "Visura catastale acquisto Padova: richiesta online con SPID/CIE — fatto procedurale portale ADE catasto.",
    "Visura catastale acquisto Padova: venditore deve consegnare documentazione — dichiarazione annuncio vs obbligo reale.",
    "Visura catastale acquisto Padova: perizia bancaria usa dati catastali — incoerenza blocca mutuo.",
    "Visura catastale acquisto Padova: notaio verifica visure ipotecarie e catastali — due diligence distinte.",
    "Visura catastale acquisto Padova: immobile Limena stesso catasto provinciale — comune catastale Padova territorio.",
    "Visura catastale acquisto Padova: categoria A/2 abitazione signorile vs A/3 economica — incide imposte e percezione mercato.",
    "Visura catastale acquisto Padova: consistenza in vani o mq — leggere campo corretto in visura.",
    "Visura catastale acquisto Padova: box e cantine subalterni separati — visure multiple se pertinenze distinte.",
    "Visura catastale acquisto Padova: variazione catastale post ristrutturazione — verificare allineamento post lavori.",
    "Visura catastale acquisto Padova: servizio acquisto Righetto richiede visura prima dell'offerta — prassi ordinata.",
    "Visura catastale acquisto Padova: NotaiOnline spiega visura — riferimento didattico complementare.",
    "Visura catastale acquisto Padova: immobile ereditato — visura per quota e subalterno prima della vendita.",
    "Visura catastale acquisto Padova: compravendita usufrutto — visura con annotazioni particolari.",
    "Visura catastale acquisto Padova: terreni e fabbricati fogli diversi — attenzione in annunci rurali Colli Euganei.",
    "Visura catastale acquisto Padova: visura non sostituisce APE né conformità — documenti complementari obbligatori.",
    "Visura catastale acquisto Padova: errori comuni — subalterno errato in proposta (vedi blog dieci errori).",
    "Visura catastale acquisto Padova: OMI vendita incrociata con categoria catastale — analisi prezzo coerente.",
    "Visura catastale acquisto Padova: visura aggiornata entro 30 giorni consigliata — prassi notarile.",
    "Visura catastale acquisto Padova: costo visura modesto — investimento minimo vs rischio caparra su immobile irregolare.",
    "Visura catastale acquisto Padova: form lead per accompagnamento documentale fino al rogito — senza parere legale sostitutivo.",
    "Visura catastale acquisto Padova: ISTAT e ADE osservatorio per contesto prezzi — visura per singola unità.",
])


def body_canone_concordato() -> str:
    return f"""
{aeo_box("In sintesi", "Il <strong>canone concordato a Padova nel 2026</strong> vincola il canone entro fasce dell'<strong>accordo territoriale</strong> (<a href=\"{MEF_ACCORDI}\" target=\"_blank\" rel=\"noopener noreferrer\">MEF</a>) e offre <strong>cedolare secca al 10%</strong> e detrazioni. Diverso dalla guida generica <a href=\"blog-contratto-affitto-padova\">contratto affitto Padova</a>: qui percorso operativo aggiornato e fiscalità.")}

<p><strong>Distinzione editoriale:</strong> <em>Fatto</em> — testo accordo territoriale, registrazione ADE entro 30 giorni, durata 3+2. <em>Dichiarazione</em> — convenienza netta per proprietario/inquilino va verificata con commercialista. <em>Analisi</em> — incrocio fasce concordato con <a href=\"{OMI_URL}\" target=\"_blank\" rel=\"noopener noreferrer\">OMI locazione</a> del semestre per Padova e cintura (Limena).</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#cosa">Cos'è il canone concordato</a></li>
<li><a href="#fasce">Fasce e zone Padova</a></li>
<li><a href="#fiscale">Vantaggi fiscali</a></li>
<li><a href="#percorso">Percorso pratico 2026</a></li>
<li><a href="#limena">Padova vs Limena</a></li>
</ol></nav>

{sol_box("Conviene il canone concordato a Padova nel 2026?", [
    ("Attestazione", "Organizzazioni sindacali e fasce accordo territoriale", "MEF accordi", MEF_ACCORDI),
    ("Registrazione", "Entro 30 giorni su registro contratti ADE", "registro ADE", ADE_REGISTRO),
    ("Locazioni", "Supporto scelta contratto e qualifica inquilino", "servizio locazioni", "servizio-locazioni"),
    ("Zona Limena", "Canoni cintura e collegamenti Padova", "zona Limena", "zona-limena"),
])}

<h2 id="cosa">Cos'è il canone concordato e come differisce dal 4+4 libero?</h2>
<p>Il <strong>canone concordato</strong> (durata 3+2 anni) fissa il canone entro minimi e massimi definiti dall'accordo territoriale del Comune di Padova e delle organizzazioni firmatarie. Il contratto <strong>4+4 a canone libero</strong> lascia maggiore libertà negoziale ma fiscalità meno agevolata per il proprietario.</p>
<p>Fonte istituzionale: <a href=\"{MEF_ACCORDI}\" target=\"_blank\" rel=\"noopener noreferrer\">Ministero Economia — accordi territoriali locazione</a> e portale <a href=\"{ADE_REGISTRO}\" target=\"_blank\" rel=\"noopener noreferrer\">registro contratti ADE</a>. Per trend locazione aggregati: <a href=\"{ADE_OSSERVATORIO}\" target=\"_blank\" rel=\"noopener noreferrer\">Osservatorio ADE</a>.</p>

{svg_concordato_fasce()}

<h2 id="fasce">Come si leggono le fasce a Padova?</h2>
<p>L'accordo suddivide Padova in zone omogenee (centro, semicentro, periferia) con fasce €/mq legate a tipologia, stato manutenzione e servizi. L'<strong>attestazione di conformità</strong> del canone passa da organizzazioni sindacali aderenti — tempistica da pianificare prima della locazione.</p>

<table>
<thead><tr><th>Elemento</th><th>Canone concordato</th><th>Canone libero 4+4</th></tr></thead>
<tbody>
<tr><td>Durata</td><td>3+2 anni</td><td>4+4 anni</td></tr>
<tr><td>Canone</td><td>Entro fasce accordo</td><td>Negoziale</td></tr>
<tr><td>Cedolare secca</td><td>10% (se opta proprietario)</td><td>21% ordinaria</td></tr>
<tr><td>IMU locazione</td><td>Riduzione 25% possibile</td><td>Ordinaria</td></tr>
<tr><td>Detrazioni inquilino</td><td>Sì, con requisiti</td><td>Limitate</td></tr>
</tbody>
</table>

{blog_fig("img/blog/blog-canone-concordato-padova-accordo.webp", "Accordo territoriale canone concordato Padova — illustrazione editoriale fasce 2026")}

{svg_concordato_fiscale()}

<h2 id="fiscale">Vantaggi fiscali: cosa è fatto normativo</h2>
<p>La <strong>cedolare secca al 10%</strong> su canone concordato è prevista dalla normativa per proprietari che scelgono questo regime. La <strong>riduzione IMU del 25%</strong> su immobile locato concordato è altra agevolazione verificabile. Sono <em>fatti</em> normativi; la convenienza netta rispetto al libero dipende da canone, aliquota marginale e spese — <em>analisi</em> con commercialista.</p>

<table>
<thead><tr><th>Voce</th><th>Concordato (esempio didattico)</th><th>Libero (esempio)</th><th>Fonte</th></tr></thead>
<tbody>
<tr><td>Canone annuo</td><td>7.200 €</td><td>7.200 €</td><td>Esempio</td></tr>
<tr><td>Cedolare secca</td><td>720 € (10%)</td><td>1.512 € (21%)</td><td>Normativa ADE</td></tr>
<tr><td>Registrazione</td><td>Obbligatoria 30 gg</td><td>Obbligatoria 30 gg</td><td>ADE registro</td></tr>
<tr><td>Detrazione inquilino</td><td>Fino 19% canone</td><td>Requisiti diversi</td><td>Art. 15 TUIR</td></tr>
</tbody>
</table>

<h2 id="percorso">Percorso pratico canone concordato Padova 2026</h2>
<ol>
<li>Verificare zona immobile nell'accordo territoriale vigente.</li>
<li>Calcolare canone entro fascia con attestazione sindacale.</li>
<li>Stipulare contratto 3+2 e registrare entro 30 giorni su <a href=\"{ADE_REGISTRO}\">registro ADE</a>.</li>
<li>Optare per cedolare secca se conviene — scelta vincolante triennio.</li>
<li>Conservare ricevuta per detrazioni inquilino e adempimenti fiscali.</li>
</ol>

{blog_fig("img/blog/blog-canone-concordato-padova-fasce.webp", "Fasce canone concordato per zone Padova — schema editoriale 2026")}

<h2 id="limena">Padova centro vs Limena: stesso accordo?</h2>
<p>Molti inquilini pendolari valutano <strong>Limena</strong> per metrature e canone. Verificare se il comune aderisce alle stesse fasce o a accorpamenti provinciali — consultare testo accordo e pagina <a href=\"zona-limena\">zona Limena</a>. Righetto coordina locazioni su Padova e 101 comuni dal 2000.</p>

{blog_fig("img/blog/blog-canone-concordato-padova-cedolare.webp", "Cedolare secca e canone concordato — illustrazione fiscalità locazione Padova")}

<p>Approfondimenti correlati: <a href=\"blog-affitti-padova-canoni-2026\">canoni affitti Padova 2026</a>, <a href=\"blog-appartamento-affitto-limena-contratto-2026\">affitto Limena contratto</a>, <a href=\"servizio-locazioni\">servizio locazioni</a>.</p>

<h2 id="domande">Domande frequenti sul canone concordato nel Padovano</h2>
<p>Proprietari e inquilini ci chiedono spesso se il concordato conviene sempre: la risposta onesta è <em>analisi</em>, non slogan. Confrontate canone massimo di accordo, cedolare, IMU e detrazioni con simulazione del libero 4+4 sullo stesso immobile. A Padova, zone semicentro con domanda alta possono rendere il libero più redditizio per il locatore nonostante fiscalità; in periferia il concordato spesso allinea canone sostenibile e vantaggi fiscali per entrambi.</p>
<p>Per immobili in <strong>Limena</strong>, verificate quale accordo territoriale si applica e come si collega ai collegamenti verso Padova — pagina <a href=\"zona-limena\">zona Limena</a>. Il team Righetto supporta la scelta contrattuale senza imporre una tipologia: obiettivo è contratto registrato, canone coerente con mercato e documenti in ordine.</p>

<p>{CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 29 agosto 2026. Fonti: MEF accordi territoriali, ADE registro contratti, OMI locazione.</p>
"""


def body_gergo() -> str:
    return f"""
{aeo_box("In sintesi", "Il <strong>gergo immobiliare a Padova</strong> mescola termini <strong>catastali</strong> (visura, subalterno), <strong>urbanistici</strong> (APE, planimetria) e <strong>contrattuali</strong> (rogito, caparra). Glossario evergreen per comprare, vendere o affittare nel Padovano senza incomprensioni.")}

<p>Questa guida <strong>non sostituisce</strong> notaio o commercialista: traduce il linguaggio delle agenzie, dei portali e delle banche in concetti operativi. <em>Fatto</em>: definizioni ufficiali (catasto ADE, APE legge). <em>Dichiarazione</em>: termini in annuncio possono essere marketing. <em>Analisi</em>: come Righetto usa i termini in trattativa quotidiana a Padova e Limena.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#catastale">Termini catastali</a></li>
<li><a href="#urbanistico">Urbanistica e APE</a></li>
<li><a href="#contrattuale">Contratti e rogito</a></li>
<li><a href="#mutuo">Mutuo e perizia</a></li>
<li><a href="#errori">Errori da evitare</a></li>
</ol></nav>

{sol_box("Non capisco i termini dell'annuncio — cosa chiedo all'agenzia?", [
    ("Visura e planimetria", "Documenti catastali prima della seconda visita", "5 domande agenzia", "blog-5-domande-appuntamento-agenzia-padova-2026"),
    ("Acquisto", "Coordinamento documenti fino al rogito", "consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
    ("Mutuo", "TAEG, perizia, Euribor spiegati in sede", "servizio mutuo", "servizio-mutuo"),
    ("Limena", "Termini e prezzi in cintura nord", "zona Limena", "zona-limena"),
])}

<h2 id="catastale">Termini catastali: visura, subalterno, categoria</h2>
<p>La <strong>visura catastale</strong> (fonte <a href=\"{ADE_CATASTO}\" target=\"_blank\" rel=\"noopener noreferrer\">ADE catasto</a>) riporta foglio, particella, subalterno, categoria (A/2, A/3…), consistenza e rendita. Il <strong>subalterno</strong> identifica l'unità immobiliare — errore qui invalida contratti e visure.</p>

{svg_gergo_mappa()}

<table>
<thead><tr><th>Termine</th><th>Significato</th><th>Tipo</th></tr></thead>
<tbody>
<tr><td>Visura catastale</td><td>Scheda ufficiale unità immobiliare</td><td>Fatto (ADE)</td></tr>
<tr><td>Rendita catastale</td><td>Base imposte, non prezzo mercato</td><td>Fatto</td></tr>
<tr><td>Superficie commerciale</td><td>Spesso in annuncio agenzia</td><td>Dichiarazione — verificare</td></tr>
<tr><td>Subalterno</td><td>ID unità in mappa catastale</td><td>Fatto</td></tr>
</tbody>
</table>

{blog_fig("img/blog/blog-gergo-immobiliare-padova-termini.webp", "Gergo immobiliare Padova — termini catastali spiegati in visita agenzia")}

<h2 id="urbanistico">APE, planimetria, conformità</h2>
<p>L'<strong>APE</strong> (Attestato Prestazione Energetica) è obbligatorio in compravendita e locazione — classe da A4 a G. La <strong>planimetria catastale</strong> va confrontata con lo stato di fatto: difformità non sanate possono bloccare mutuo e rogito.</p>

{svg_gergo_flusso()}

{blog_fig("img/blog/blog-gergo-immobiliare-padova-agenzia.webp", "Agente immobiliare spiega gergo tecnico a coppia acquirenti Padova")}

<h2 id="contrattuale">Caparra, compromesso, rogito</h2>
<p><strong>Caparra confirmatoria</strong> vincola entrambe le parti; <strong>acconto</strong> ha tutela diversa. Il <strong>compromesso</strong> precede il <strong>rogito</strong> notarile. In locazione: <strong>4+4</strong>, <strong>3+2 concordato</strong>, <strong>deposito cauzionale</strong> (max tre mensilità).</p>

<table>
<thead><tr><th>Termine</th><th>Contesto</th><th>Nota Padova</th></tr></thead>
<tbody>
<tr><td>4+4</td><td>Locazione standard</td><td>Registro ADE obbligatorio</td></tr>
<tr><td>Rogito</td><td>Vendita</td><td>Notaio + imposte</td></tr>
<tr><td>Mandato esclusivo</td><td>Vendita con agenzia</td><td>Durata e penali da leggere</td></tr>
<tr><td>Perizia</td><td>Mutuo banca</td><td>Può essere &lt; prezzo richiesto</td></tr>
</tbody>
</table>

<h2 id="mutuo">TAEG, Euribor, LTV — gergo bancario</h2>
<p>Il <strong>TAEG</strong> include interessi e spese — confronto obbligatorio tra banche. <strong>Euribor</strong> + spread per mutui variabili (<a href=\"blog-tassi-euribor-mutui-padova-agosto-2026\">guida Euribor Padova agosto 2026</a>). <strong>LTV</strong>: rapporto mutuo/valore perizia. Fonte macro: <a href=\"{BANCA_ITALIA}\">Banca d'Italia</a>.</p>

{blog_fig("img/blog/blog-gergo-immobiliare-padova-documenti.webp", "Documenti compravendita e termini tecnici — glossario acquisto casa Padova")}

<h2 id="errori">Cinque errori linguistici che costano caro</h2>
<ul>
<li>Confondere rendita catastale con prezzo OMI o canone di mercato.</li>
<li>Accettare «superficie» annuncio senza planimetria.</li>
<li>Firmare caparra senza distinguere confirmatoria vs acconto.</li>
<li>Ignorare difformità planimetria perché «così è sempre stato».</li>
<li>Confrontare solo tasso nominale mutuo, non TAEG.</li>
</ul>

<h2 id="pratica">Come usare il glossario in visita a Padova</h2>
<p>Portate lista termini che non avete capito dall'annuncio: l'agente Righetto li spiega con documenti alla mano. A Limena e in cintura i termini sono gli stessi del catasto nazionale; cambiano prezzi OMI e tempi di spostamento verso il capoluogo. Per acquisto, affiancate glossario e <a href=\"blog-visura-catastale-acquisto-casa-padova-2026\">guida visura catastale</a>; per mutuo, <a href=\"servizio-mutuo\">servizio mutuo</a>.</p>

<p>{CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 29 agosto 2026. Fonti: ADE catasto, NotaiOnline, Banca d'Italia.</p>
"""


def body_euribor() -> str:
    return f"""
{aeo_box("In sintesi", "<strong>Tassi mutuo ed Euribor a Padova ad agosto 2026:</strong> mutui <strong>variabili</strong> legati a <strong>Euribor 3M + spread</strong>; <strong>fissi</strong> con rata prevedibile. Fonti <a href=\"{BANCA_ITALIA}\" target=\"_blank\" rel=\"noopener noreferrer\">Banca d'Italia</a> e BCE — <strong>nessun tasso promesso</strong>. Angolo diverso da <a href=\"blog-tassi-mutui-minimi-approfittarne-padova-2026\">tassi mutui minimi Padova</a>.")}

<p><em>Fatto:</em> Euribor pubblicato da EMMI; BCE decide tassi di riferimento. <em>Dichiarazione:</em> ogni banca applica spread propri. <em>Analisi:</em> scelta fisso/variabile in base a orizzonte, reddito e tolleranza rischio nel mercato padovano.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#euribor">Cos'è l'Euribor</a></li>
<li><a href="#fisso-var">Fisso vs variabile</a></li>
<li><a href="#padova">Mutuo a Padova e Limena</a></li>
<li><a href="#simulazione">Come simulare senza fidarsi del web</a></li>
</ol></nav>

{sol_box("Mutuo a tasso variabile Euribor conviene ad agosto 2026 a Padova?", [
    ("Preventivo", "Confronto TAEG tra almeno due istituti", "servizio mutuo", "servizio-mutuo"),
    ("Acquisto", "Immobili con documenti per perizia rapida", "catalogo", "immobili"),
    ("Limena", "Trilocali e bilocali in cintura", "zona Limena", "zona-limena"),
    ("Consulenza", "Primo appuntamento gratuito in sede", "consulenza", "landing-consulenza-immobiliare-gratuita"),
])}

<h2 id="euribor">Cos'è l'Euribor e perché conta a Padova</h2>
<p>L'<strong>Euribor</strong> (Euro Interbank Offered Rate) è il tasso al quale le banche si prestano euro. Per i mutui variabili italiani si usa spesso <strong>Euribor 3 mesi</strong> + <strong>spread</strong> bancario. Riferimenti: <a href=\"{ECB_RATES}\" target=\"_blank\" rel=\"noopener noreferrer\">BCE tassi chiave</a>, <a href=\"{BANCA_ITALIA}\">Indagine Banca d'Italia</a>.</p>

{svg_euribor_trend()}

<table>
<thead><tr><th>Componente</th><th>Descrizione</th><th>Fonte</th></tr></thead>
<tbody>
<tr><td>Euribor 3M</td><td>Indice variabile trimestrale</td><td>EMMI / mercato</td></tr>
<tr><td>Spread banca</td><td>Margine istituto di credito</td><td>Preventivo banca</td></tr>
<tr><td>TAEG</td><td>Costo totale annuo effettivo</td><td>Foglio informativo</td></tr>
<tr><td>Tasso fisso</td><td>Indipendente da Euribor</td><td>Offerta banca</td></tr>
</tbody>
</table>

<h2 id="fisso-var">Tasso fisso o variabile: analisi, non dogma</h2>
<p>Il <strong>fisso</strong> offre rata stabile — utile con budget rigido. Il <strong>variabile</strong> può costare meno all'inizio ma segue Euribor — stress test consigliato (+1-2% simulato). <a href=\"{CRIF_BAROMETRO}\" target=\"_blank\" rel=\"noopener noreferrer\">CRIF barometro mutui</a> dà contesto nazionale; la filiale Padova applica condizioni proprie.</p>

{svg_euribor_fisso_var()}

{blog_fig("img/blog/blog-tassi-euribor-mutui-padova-grafico.webp", "Grafico Euribor e mutui Padova — illustrazione editoriale agosto 2026")}

<h2 id="padova">Mutuo ed Euribor nel mercato padovano</h2>
<p>Acquisto a Padova semicentro vs <strong>Limena</strong> cambia importo mutuo e sensibilità Euribor. Incrociare prezzo con <a href=\"{OMI_URL}\">OMI vendita ADE</a> e <a href=\"{ISTAT_URL}\">ISTAT prezzi</a>. Perizia bancaria può essere inferiore al prezzo richiesto — anticipo supplementare.</p>

<table>
<thead><tr><th>Scenario</th><th>Padova centro</th><th>Limena</th></tr></thead>
<tbody>
<tr><td>Importo mutuo tipico</td><td>Più alto €/mq</td><td>Metratura maggiore, prezzo unitario minore</td></tr>
<tr><td>Rischio Euribor</td><td>Stesso indice nazionale</td><td>Stesso indice</td></tr>
<tr><td>Perizia OMI</td><td>Zone B1 centro</td><td>Zone B1/R1 cintura</td></tr>
<tr><td>Supporto Righetto</td><td>Ricerca + documenti</td><td>Sede Via Roma 96</td></tr>
</tbody>
</table>

{blog_fig("img/blog/blog-tassi-euribor-mutui-padova-bce.webp", "BCE e tassi di riferimento — contesto mutui Padova 2026")}

<h2 id="simulazione">Come simulare correttamente</h2>
<ol>
<li>Richiedere TAEG scritto a almeno due banche.</li>
<li>Per variabile: chiedere spread attuale e storico Euribor 3M.</li>
<li>Includere assicurazione, perizia, istruttoria nel costo totale.</li>
<li>Non basarsi su tassi «da internet» — sono indicativi generici.</li>
</ol>

{blog_fig("img/blog/blog-tassi-euribor-mutui-padova-indagine.webp", "Indagine Banca d'Italia famiglie — contesto finanziamenti immobiliari Veneto")}

<p>Correlati: <a href=\"servizio-mutuo\">servizio mutuo</a>, <a href=\"blog-prima-casa-under-36-consap-padova-2026\">prima casa under 36 CONSAP</a>, <a href=\"blog-appartamento-limena-guida-acquisto-2026\">acquisto Limena</a>.</p>

<h2 id="veneto">Contesto Veneto e Padova agosto 2026</h2>
<p>Il Veneto resta uno dei mercati residenziali più liquidi d'Italia secondo osservatori ADE e indagini <a href=\"{BANCA_ITALIA}\">Banca d'Italia</a>. Euribor e spread incidono sul costo del denaro per famiglie che comprano a Padova semicentro o in cintura; non sostituiscono valutazione merito creditizio e perizia. Pianificate simulazione mutuo <strong>prima</strong> della proposta d'acquisto per competere con altri acquirenti qualificati.</p>

<p>{CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 29 agosto 2026. Fonti: BCE, Banca d'Italia, CRIF. Nessun tasso garantito.</p>
"""


def body_registro() -> str:
    return f"""
{aeo_box("In sintesi", "Il <strong>registro contratti di affitto a Padova</strong> richiede registrazione entro <strong>30 giorni</strong> all'<a href=\"{ADE_REGISTRO}\" target=\"_blank\" rel=\"noopener noreferrer\">Agenzia delle Entrate</a>. Senza ricevuta: niente detrazioni canone, problemi anagrafe. Guida normativa 2026 per proprietari e inquilini nel Padovano.")}

<p><em>Fatto:</em> termine 30 giorni e imposta di registro su locazioni — normativa ADE. <em>Dichiarazione:</em> «registro fatto» va provato con PDF ricevuta. <em>Analisi:</em> costo registrazione vs rischio sanzioni e perdita detrazioni 19%.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#obbligo">Obbligo e termini</a></li>
<li><a href="#tipologie">Tipologie contratto</a></li>
<li><a href="#costi">Imposte e pagamento</a></li>
<li><a href="#pratica">Pratica online ADE</a></li>
<li><a href="#limena">Affitti Limena</a></li>
</ol></nav>

{sol_box("Ho firmato affitto a Padova — devo registrare?", [
    ("Sì entro 30 gg", "Registro contratti locazione ADE obbligatorio", "registro ADE", ADE_REGISTRO),
    ("Locazioni", "Supporto registrazione e contratto", "servizio locazioni", "servizio-locazioni"),
    ("Limena", "Affitti cintura nord Padova", "zona Limena", "zona-limena"),
    ("Canoni", "Contesto mercato locazione 2026", "canoni 2026", "blog-affitti-padova-canoni-2026"),
])}

<h2 id="obbligo">Perché il registro contratti non è opzionale</h2>
<p>Ogni contratto di locazione abitativa va registrato entro <strong>30 giorni</strong> dalla stipula. La ricevuta abilita <strong>detrazione IRPEF 19%</strong> del canore per l'inquilino (con requisiti) e certificazioni per residenza. Fonte: <a href=\"{ADE_REGISTRO}\">portale registro contratti ADE</a>.</p>

{svg_registro_flow()}

<table>
<thead><tr><th>Adempimento</th><th>Termine</th><th>Conseguenza omesso</th></tr></thead>
<tbody>
<tr><td>Registrazione locazione</td><td>30 giorni</td><td>Sanzioni + no detrazioni</td></tr>
<tr><td>Pagamento imposta registro</td><td>Con registrazione</td><td>Rateazione non valida fiscalmente</td></tr>
<tr><td>Comunicazione canone</td><td>In contratto</td><td>Base imposta errata</td></tr>
<tr><td>Conservazione ricevuta</td><td>Tutta la locazione</td><td>Problemi in 730</td></tr>
</tbody>
</table>

<h2 id="tipologie">4+4, concordato, transitorio: tutti in registro</h2>
<p>Non esiste contratto «solo privato» esente: <strong>4+4 libero</strong>, <strong>3+2 concordato</strong> e <strong>transitorio</strong> (con requisiti) vanno registrati. Differenza è nell'imposta e nelle agevolazioni, non nell'obbligo.</p>

{svg_registro_tipologie()}

{blog_fig("img/blog/blog-registro-contratti-affitto-padova-limena.webp", "Registrazione contratto affitto Limena — illustrazione editoriale ADE 2026")}

<h2 id="costi">Imposte di registro: cosa verificare</h2>
<p>L'imposta di registro sulle locazioni abitative segue aliquote previste dalla normativa (ordinariamente <strong>2% del canone annuo</strong> per locazioni 4+4 — verificare circolari ADE vigenti). Canone concordato può avere agevolazioni correlate alla cedolare secca del proprietario.</p>

<table>
<thead><tr><th>Voce</th><th>Chi paga</th><th>Nota</th></tr></thead>
<tbody>
<tr><td>Imposta registro</td><td>Inquilino (salvo patto)</td><td>2% canone annuo tipico</td></tr>
<tr><td>Bollo contratto</td><td>Parti</td><td>16 € ogni 4 pagine</td></tr>
<tr><td>Registrazione online</td><td>Proprietario/inquilino</td><td>Portale ADE</td></tr>
<tr><td>Canone concordato</td><td>Entrambi</td><td>Cedolare 10% opzionale locatore</td></tr>
</tbody>
</table>

{blog_fig("img/blog/blog-registro-contratti-affitto-padova-ade.webp", "Portale registro contratti Agenzia Entrate — guida affitto Padova")}

<h2 id="pratica">Pratica operativa agosto 2026</h2>
<ol>
<li>Firmare contratto con dati catastali corretti (subalterno).</li>
<li>Accedere a servizio registrazione locazioni ADE con SPID/CIE.</li>
<li>Compilare RLI e pagare F24 entro 30 giorni.</li>
<li>Archiviare ricevuta PDF per 730 e rinnovi.</li>
</ol>

{blog_fig("img/blog/blog-registro-contratti-affitto-padova-canoni.webp", "Canoni affitto e registro contratto — contesto mercato Padova 2026")}

<p>Contesto mercato: <a href=\"{ADE_OSSERVATORIO}\">Osservatorio ADE</a>, <a href=\"{FIMAA_VENETO}\">FIMAA Veneto</a>. Correlati: <a href=\"blog-canone-concordato-padova-guida-2026\">canone concordato Padova</a>, <a href=\"blog-contratto-affitto-padova\">contratto affitto</a>, <a href=\"servizio-locazioni\">servizio locazioni</a>.</p>

<h2 id="errori">Errori comuni sulla registrazione affitti Padova</h2>
<p>Registrare dopo 30 giorni, pagare canone in contanti senza tracciabilità, o confondere ricevuta ADE con semplice copia contratto sono errori frequenti. Inquilini studenti e famiglie perdono detrazioni; locatori espongono a sanzioni. Il servizio locazioni Righetto verifica registrazione come passaggio standard — non opzionale.</p>

<p>{CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 29 agosto 2026. Fonte: Agenzia delle Entrate registro contratti.</p>
"""


def body_visura() -> str:
    return f"""
{aeo_box("In sintesi", "La <strong>visura catastale per acquisto casa a Padova</strong> identifica l'immobile (foglio, particella, subalterno) e riporta categoria e rendita. Va richiesta <strong>prima della caparra</strong> e incrociata con planimetria. Fonte <a href=\"{ADE_CATASTO}\" target=\"_blank\" rel=\"noopener noreferrer\">ADE catasto</a> — complementare a perizia banca e rogito notarile.")}

<p><em>Fatto:</em> dati in visura sono quelli ufficiali del Catasto. <em>Dichiarazione:</em> metrature in annuncio possono differire. <em>Analisi:</em> difformità planimetria/stato di fatto è il rischio numero uno negli acquisti padovani non verificati.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#cosa">Cosa contiene la visura</a></li>
<li><a href="#quando">Quando richiederla</a></li>
<li><a href="#planimetria">Visura vs planimetria</a></li>
<li><a href="#mutuo">Visura e mutuo</a></li>
<li><a href="#checklist">Checklist acquirente</a></li>
</ol></nav>

{sol_box("Devo chiedere la visura catastale prima di comprare a Padova?", [
    ("Sì, subito", "Prima di caparra o proposta vincolante", "checklist compromesso", "blog-checklist-verifiche-prima-compromesso-padova-2026"),
    ("Acquisto", "Coordinamento visure e rogito", "consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
    ("Mutuo", "Documenti per perizia bancaria", "servizio mutuo", "servizio-mutuo"),
    ("Limena", "Visure immobili cintura", "zona Limena", "zona-limena"),
])}

<h2 id="cosa">Cosa contiene la visura catastale</h2>
<p>La visura riporta identificativi catastali, <strong>categoria</strong> (A/2 abitazione signorile, A/3 economica…), <strong>consistenza</strong> (vani o mq), <strong>rendita catastale</strong> e intestatari. Richiesta online: <a href=\"{ADE_CATASTO}\">visure e planimetrie ADE</a>. Guida didattica: <a href=\"{NOTAI_VISURA}\" target=\"_blank\" rel=\"noopener noreferrer\">NotaiOnline visura catastale</a>.</p>

{svg_visura_campi()}

<table>
<thead><tr><th>Campo visura</th><th>Utilità acquisto</th><th>Errore comune</th></tr></thead>
<tbody>
<tr><td>Subalterno</td><td>Identifica unità esatta</td><td>Confusione con box separato</td></tr>
<tr><td>Categoria</td><td>Imposte e descrizione legale</td><td>Credere equivalga a «trilocale» annuncio</td></tr>
<tr><td>Rendita</td><td>Base imposte</td><td>Confonderla con prezzo OMI</td></tr>
<tr><td>Intestatari</td><td>Verifica venditore</td><td>Non incrociare con atto provenienza</td></tr>
</tbody>
</table>

<h2 id="quando">Quando richiedere la visura a Padova</h2>
<p>Prima della <strong>seconda visita seria</strong> o subito dopo, chiedere visura aggiornata al venditore o procurarsela (costo contenuto). Non versare caparra significativa senza aver letto foglio/particella/subalterno e confrontato con planimetria.</p>

{svg_visura_percorso()}

{blog_fig("img/blog/blog-visura-catastale-acquisto-casa-padova-checklist.webp", "Checklist visura catastale acquisto casa Padova — verifiche prima del compromesso")}

<h2 id="planimetria">Visura e planimetria: coppia obbligata</h2>
<p>La visura dice <em>cosa dice il catasto</em>; la planimetria mostra <em>come è disegnato</em>. Difformità (bagno non in carta, ampliamenti) possono bloccare mutuo. Incrociare con <a href=\"{OMI_URL}\">OMI vendita</a> per coerenza prezzo/zona.</p>

<table>
<thead><tr><th>Documento</th><th>Contenuto</th><th>Chi rilascia</th></tr></thead>
<tbody>
<tr><td>Visura catastale</td><td>Dati anagrafici unità</td><td>ADE</td></tr>
<tr><td>Planimetria</td><td>Layout autorizzato</td><td>ADE</td></tr>
<tr><td>APE</td><td>Classe energetica</td><td>Certificatore</td></tr>
<tr><td>Visura ipotecaria</td><td>Gravami e pignoramenti</td><td>Conservatoria</td></tr>
</tbody>
</table>

{blog_fig("img/blog/blog-visura-catastale-acquisto-casa-padova-errori.webp", "Errori comuni visura catastale — acquisto casa Padova 2026")}

<h2 id="mutuo">Visura, perizia bancaria e mutuo</h2>
<p>La banca usa dati catastali in perizia. Incoerenza subalterno o superficie ritarda erogazione mutuo. Contesto tassi: <a href=\"blog-tassi-euribor-mutui-padova-agosto-2026\">Euribor mutui Padova</a>. Macro prezzi: <a href=\"{ISTAT_URL}\">ISTAT</a>, <a href=\"{BANCA_ITALIA}\">Banca d'Italia</a>.</p>

{blog_fig("img/blog/blog-visura-catastale-acquisto-casa-padova-planimetria.webp", "Planimetria catastale e visura — documenti acquisto immobile Padova")}

<h2 id="checklist">Checklist visura per acquirente padovano</h2>
<ol>
<li>Visura aggiornata (30 giorni) per subalterno in annuncio.</li>
<li>Planimetria conforme o percorso sanatoria documentato.</li>
<li>Confronto categoria catastale con descrizione agenzia.</li>
<li>Verifica box/cantina con subalterni separati se inclusi nel prezzo.</li>
<li>Archiviazione PDF per notaio e banca.</li>
</ol>

<p>Correlati: <a href=\"blog-dieci-errori-acquisto-casa-padova-2026\">dieci errori acquisto</a>, <a href=\"blog-documenti-compravendita-rogito-padova-2026\">documenti rogito</a>, <a href=\"blog-appartamento-limena-guida-acquisto-2026\">acquisto Limena</a>.</p>

<h2 id="notaio">Visura, notaio e percorso rogito Padova</h2>
<p>Il notaio incrocia visura catastale, planimetria, visura ipotecaria e atti precedenti. L'agenzia non sostituisce il notaio ma può anticipare incongruenze evidenti prima della caparra. A Padova, immobili centro storico e semicentro richiedono attenzione extra su vincoli e conformità; in Limena spesso prevalgono controlli su pertinenze e box separati.</p>

<p>{CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 29 agosto 2026. Fonti: ADE catasto, NotaiOnline, OMI ADE.</p>
"""


ARTICLES = [
    {
        "slug": "blog-canone-concordato-padova-guida-2026",
        "filename": "blog-canone-concordato-padova-guida-2026.html",
        "hero": "img/blog/blog-canone-concordato-padova-guida-2026-hero.webp",
        "title": "Canone concordato Padova 2026: guida",
        "og_title": "Canone concordato Padova 2026: fasce e fiscalità",
        "meta": "Canone concordato Padova 2026: fasce accordo territoriale, cedolare 10%, registrazione ADE. Guida pratica proprietari e inquilini Righetto.",
        "schema_headline": "Canone concordato a Padova: guida completa 2026",
        "section": "Locazioni Padova",
        "cat_badge": "Canone concordato · Normativa",
        "bread_crumb": "Canone concordato Padova",
        "h1": "<strong>Canone concordato Padova</strong> 2026: guida pratica",
        "hero_alt": "Canone concordato Padova — fasce locazione e fiscalità 2026",
        "body_fn": lambda: expand_body(body_canone_concordato, [], EXPANSION_CANONE),
        "faqs": [
            ("Cos'è il canone concordato a Padova?", "Contratto 3+2 con canone entro fasce dell'accordo territoriale comunale — attestazione sindacale e registrazione ADE."),
            ("Conviene al proprietario nel 2026?", "Cedolare secca 10% e riduzione IMU 25% possono compensare canone calmierato — verificare con commercialista."),
            ("Differenza dal 4+4 libero?", "Libero: canone negoziale e cedolare 21%. Concordato: fasce vincolanti e agevolazioni fiscali."),
            ("Serve la registrazione ADE?", "Sì, entro 30 giorni come ogni locazione — portale registro contratti Agenzia Entrate."),
            ("Vale a Limena?", "Verificare adesione comune alle fasce accordo — stesso catasto provinciale, regole comunali da controllare."),
            ("Righetto gestisce canone concordato?", "Sì — servizio locazioni con supporto contrattuale; compenso concordato in sede."),
            ("Dove trovo le fasce ufficiali?", "Accordo territoriale MEF e organizzazioni sindacali firmatarie — non da post social."),
        ],
        "related": [
            ("Contratto affitto Padova", "blog-contratto-affitto-padova"),
            ("Registro contratti", "blog-registro-contratti-affitto-padova-2026"),
            ("Servizio locazioni", "servizio-locazioni"),
            ("Canoni 2026", "blog-affitti-padova-canoni-2026"),
            ("Zona Limena", "zona-limena"),
        ],
        "registry": {
            "titolo": "Canone concordato Padova: Guida 2026",
            "categoria": "Locazioni Padova",
            "tempo": 14,
            "contenuto": "Canone concordato Padova 2026: fasce, cedolare 10%, percorso ADE.",
            "evidenza": False,
            "emoji": "📋",
            "admin_contenuto": "<p>Guida canone concordato Padova: accordo territoriale, fiscalità e registrazione.</p>",
        },
        "static_map_key": "canone concordato padova guida 2026",
        "editorial_id": "eq-venerdi-001",
    },
    {
        "slug": "blog-gergo-immobiliare-padova-spiegato-2026",
        "filename": "blog-gergo-immobiliare-padova-spiegato-2026.html",
        "hero": "img/blog/blog-gergo-immobiliare-padova-spiegato-2026-hero.webp",
        "title": "Gergo immobiliare Padova spiegato 2026",
        "og_title": "Gergo immobiliare Padova: glossario 2026",
        "meta": "Gergo immobiliare Padova spiegato: visura, rogito, APE, TAEG, Euribor. Glossario evergreen per comprare, vendere e affittare nel Padovano.",
        "schema_headline": "Gergo immobiliare a Padova: glossario pratico 2026",
        "section": "Guide immobiliari",
        "cat_badge": "Glossario · Evergreen",
        "bread_crumb": "Gergo immobiliare Padova",
        "h1": "<strong>Gergo immobiliare Padova</strong> spiegato semplice",
        "hero_alt": "Gergo immobiliare Padova — glossario termini compravendita e affitto",
        "body_fn": lambda: expand_body(body_gergo, [], EXPANSION_GERGO),
        "faqs": [
            ("Cos'è la visura catastale?", "Documento ADE con foglio, particella, subalterno, categoria e rendita dell'unità immobiliare."),
            ("Caparra confirmatoria o acconto?", "Caparra confirmatoria vincola entrambe le parti; acconto ha tutela civilistica diversa — leggere contratto."),
            ("Cos'è il TAEG?", "Tasso Annuo Effettivo Globale: costo totale mutuo inclusi interessi e spese — confronto obbligatorio tra banche."),
            ("APE e planimetria: differenza?", "APE = energia; planimetria = layout autorizzato in catasto — entrambi da verificare in acquisto."),
            ("Cosa significa 4+4?", "Contratto locazione 4 anni + rinnovo 4 — standard mercato padovano, con registrazione ADE."),
            ("Rendita catastale = prezzo?", "No — rendita è base imposte; prezzo mercato da OMI e comparabili locali."),
            ("Righetto spiega i termini in visita?", "Sì — trasparenza documentale dal 2000; consulenza gratuita in sede Via Roma 96 Limena."),
        ],
        "related": [
            ("5 domande agenzia", "blog-5-domande-appuntamento-agenzia-padova-2026"),
            ("Visura catastale", "blog-visura-catastale-acquisto-casa-padova-2026"),
            ("Servizio mutuo", "servizio-mutuo"),
            ("Consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
        ],
        "registry": {
            "titolo": "Gergo immobiliare Padova: Glossario 2026",
            "categoria": "Guide immobiliari",
            "tempo": 12,
            "contenuto": "Gergo immobiliare Padova: glossario catastale, contrattuale e mutuo.",
            "evidenza": False,
            "emoji": "📖",
            "admin_contenuto": "<p>Glossario gergo immobiliare Padova per acquirenti, venditori e inquilini.</p>",
        },
        "static_map_key": "gergo immobiliare padova spiegato 2026",
        "editorial_id": "eq-venerdi-002",
    },
    {
        "slug": "blog-tassi-euribor-mutui-padova-agosto-2026",
        "filename": "blog-tassi-euribor-mutui-padova-agosto-2026.html",
        "hero": "img/blog/blog-tassi-euribor-mutui-padova-agosto-2026-hero.webp",
        "title": "Tassi Euribor mutui Padova agosto 2026",
        "og_title": "Euribor e mutui Padova: guida agosto 2026",
        "meta": "Tassi mutuo ed Euribor a Padova ad agosto 2026: fisso vs variabile, BCE, Banca d'Italia. Guida senza tassi inventati — simulazione personalizzata.",
        "schema_headline": "Tassi Euribor e mutui a Padova: guida agosto 2026",
        "section": "Mutuo e finanziamenti",
        "cat_badge": "Euribor · Mutui",
        "bread_crumb": "Euribor mutui Padova",
        "h1": "<strong>Tassi Euribor mutui</strong> Padova agosto 2026",
        "hero_alt": "Euribor e mutui Padova — tassi variabili e fissi agosto 2026",
        "body_fn": lambda: expand_body(body_euribor, [], EXPANSION_EURIBOR),
        "faqs": [
            ("Cos'è l'Euribor?", "Indice interbancario usato per mutui variabili — tipicamente Euribor 3 mesi + spread banca."),
            ("Euribor e BCE: collegamento?", "BCE influenza tassi di riferimento; Euribor segue condizioni mercato interbancario."),
            ("Fisso o variabile ad agosto 2026?", "Dipende da orizzonte e tolleranza rischio — simulare TAEG e stress test rata."),
            ("Differenza da articolo tassi minimi?", "Quel pezzo tratta minimi di fase; qui focus Euribor e variabile agosto 2026."),
            ("Come simulare mutuo a Padova?", "Preventivo scritto banca con TAEG; servizio mutuo Righetto orienta senza promettere tassi."),
            ("Perizia e Euribor insieme?", "Perizia determina LTV; Euribor incide solo su mutui variabili."),
            ("Fonti affidabili?", "Banca d'Italia, BCE, foglio informativo banca — non percentuali generiche online."),
        ],
        "related": [
            ("Servizio mutuo", "servizio-mutuo"),
            ("Tassi mutui minimi", "blog-tassi-mutui-minimi-approfittarne-padova-2026"),
            ("Prima casa under 36", "blog-prima-casa-under-36-consap-padova-2026"),
            ("Acquisto Limena", "blog-appartamento-limena-guida-acquisto-2026"),
        ],
        "registry": {
            "titolo": "Euribor mutui Padova: Agosto 2026",
            "categoria": "Mutuo e finanziamenti",
            "tempo": 13,
            "contenuto": "Tassi Euribor mutui Padova agosto 2026: fisso vs variabile, fonti BCE.",
            "evidenza": False,
            "emoji": "📊",
            "admin_contenuto": "<p>Guida Euribor e mutui Padova agosto 2026 — nessun tasso promesso online.</p>",
        },
        "static_map_key": "tassi euribor mutui padova agosto 2026",
        "editorial_id": "eq-venerdi-003",
    },
    {
        "slug": "blog-registro-contratti-affitto-padova-2026",
        "filename": "blog-registro-contratti-affitto-padova-2026.html",
        "hero": "img/blog/blog-registro-contratti-affitto-padova-2026-hero.webp",
        "title": "Registro contratti affitto Padova 2026",
        "og_title": "Registro contratti affitto Padova: guida ADE",
        "meta": "Registro contratti affitto Padova 2026: obbligo 30 giorni ADE, imposte, detrazioni canone. Guida proprietari e inquilini nel Padovano.",
        "schema_headline": "Registro contratti di locazione a Padova: guida 2026",
        "section": "Locazioni Padova",
        "cat_badge": "Registro · Normativa",
        "bread_crumb": "Registro contratti affitto",
        "h1": "<strong>Registro contratti affitto</strong> Padova 2026",
        "hero_alt": "Registro contratti affitto Padova — registrazione ADE locazioni 2026",
        "body_fn": lambda: expand_body(body_registro, [], EXPANSION_REGISTRO),
        "faqs": [
            ("Entro quanto registrare affitto Padova?", "30 giorni dalla stipula — portale registro contratti Agenzia delle Entrate."),
            ("Chi paga imposta di registro?", "Salvo patto diverso, inquilino — ordinariamente 2% canone annuo locazioni abitative."),
            ("Senza registro perdo detrazioni?", "Sì — detrazione 19% canone richiede contratto registrato e pagamenti tracciabili."),
            ("Vale per canone concordato?", "Sì — stessa registrazione con codici tributo e fiscalità specifiche."),
            ("Subentro inquilino?", "Nuova registrazione entro termini con dati aggiornati."),
            ("Righetto aiuta con registro?", "Servizio locazioni include supporto contrattuale e verifica registrazione."),
            ("Dove registrare online?", "Portale ADE registro contratti locazione — SPID o CIE."),
        ],
        "related": [
            ("Canone concordato", "blog-canone-concordato-padova-guida-2026"),
            ("Contratto affitto", "blog-contratto-affitto-padova"),
            ("Affitto Limena", "blog-appartamento-affitto-limena-contratto-2026"),
            ("Servizio locazioni", "servizio-locazioni"),
        ],
        "registry": {
            "titolo": "Registro contratti affitto Padova 2026",
            "categoria": "Locazioni Padova",
            "tempo": 12,
            "contenuto": "Registro contratti affitto Padova: ADE, 30 giorni, imposte e detrazioni.",
            "evidenza": False,
            "emoji": "📝",
            "admin_contenuto": "<p>Guida registro contratti locazione Padova — obblighi ADE 2026.</p>",
        },
        "static_map_key": "registro contratti affitto padova 2026",
        "editorial_id": "eq-venerdi-004",
    },
    {
        "slug": "blog-visura-catastale-acquisto-casa-padova-2026",
        "filename": "blog-visura-catastale-acquisto-casa-padova-2026.html",
        "hero": "img/blog/blog-visura-catastale-acquisto-casa-padova-2026-hero.webp",
        "title": "Visura catastale acquisto casa Padova",
        "og_title": "Visura catastale acquisto Padova: guida",
        "meta": "Visura catastale per acquisto casa a Padova: foglio, subalterno, planimetria, mutuo. Quando richiederla e come leggerla — fonte ADE.",
        "schema_headline": "Visura catastale nell'acquisto casa a Padova: guida 2026",
        "section": "Acquisto casa",
        "cat_badge": "Visura · Evergreen",
        "bread_crumb": "Visura catastale Padova",
        "h1": "<strong>Visura catastale</strong> acquisto casa Padova",
        "hero_alt": "Visura catastale acquisto casa Padova — documenti e verifiche 2026",
        "body_fn": lambda: expand_body(body_visura, [], EXPANSION_VISURA),
        "faqs": [
            ("Quando chiedere la visura?", "Prima di caparra significativa o proposta vincolante — idealmente dopo prima visita positiva."),
            ("Visura online costo?", "Poche euro su portale ADE catasto con SPID/CIE — investimento minimo vs rischi."),
            ("Visura basta per rogito?", "No — servono anche planimetria, APE, visura ipotecaria e documenti notarili."),
            ("Rendita = prezzo immobile?", "No — rendita è base imposte; prezzo da OMI e mercato locale."),
            ("Difformità planimetria?", "Rischio mutuo e rogito — verificare sanatoria o regolarizzazione prima dell'impegno."),
            ("Visura per Limena?", "Stesso sistema catastale — subalterno identifica unità nel comune."),
            ("Righetto richiede visura?", "Sì in percorso acquisto ordinato — coordinamento documenti fino al rogito."),
        ],
        "related": [
            ("Checklist compromesso", "blog-checklist-verifiche-prima-compromesso-padova-2026"),
            ("Dieci errori acquisto", "blog-dieci-errori-acquisto-casa-padova-2026"),
            ("Documenti rogito", "blog-documenti-compravendita-rogito-padova-2026"),
            ("Servizio mutuo", "servizio-mutuo"),
            ("Zona Limena", "zona-limena"),
        ],
        "registry": {
            "titolo": "Visura catastale acquisto Padova 2026",
            "categoria": "Acquisto casa",
            "tempo": 13,
            "contenuto": "Visura catastale acquisto casa Padova: campi, planimetria, mutuo.",
            "evidenza": False,
            "emoji": "🏛️",
            "admin_contenuto": "<p>Guida visura catastale per acquisto immobile a Padova e provincia.</p>",
        },
        "static_map_key": "visura catastale acquisto casa padova 2026",
        "editorial_id": "eq-venerdi-005",
    },
]


EDITORIAL_ITEMS = [
    {
        "id": "eq-venerdi-001",
        "status": "published",
        "priority": 0,
        "target_week": "2026-08-29",
        "published_date": DATE_ISO,
        "slug": "blog-canone-concordato-padova-guida-2026",
        "kw_primaria": "canone concordato padova",
        "intent": "locazione-normativa",
        "title": "Canone concordato Padova 2026: fasce, fiscalità e percorso pratico",
        "cluster": "locazioni-normativa",
        "editorial_type": "trend",
        "monitoring_area": "normativa",
        "different_from": "blog-contratto-affitto-padova",
        "research_refs": [MEF_ACCORDI, ADE_REGISTRO],
        "hype_sources_read": [GU_URL, ADE_OSSERVATORIO, FIMAA_VENETO],
        "gap_analysis": "Contratto affitto generico esiste; manca guida 2026 su fasce concordato Padova e cedolare 10% aggiornata.",
        "value_add": "Percorso operativo Padova/Limena con distinzione fatto/dichiarazione/analisi e link servizio locazioni.",
    },
    {
        "id": "eq-venerdi-002",
        "status": "published",
        "priority": 1,
        "target_week": "2026-08-29",
        "published_date": DATE_ISO,
        "slug": "blog-gergo-immobiliare-padova-spiegato-2026",
        "kw_primaria": "gergo immobiliare padova",
        "intent": "informazione-evergreen",
        "title": "Gergo immobiliare Padova spiegato: glossario pratico 2026",
        "cluster": "guide-base",
        "editorial_type": "evergreen",
        "monitoring_area": "mercato",
        "different_from": "blog-5-domande-appuntamento-agenzia-padova-2026",
        "research_refs": [ADE_CATASTO, NOTAI_VISURA],
        "hype_sources_read": [BANCA_ITALIA, OMI_URL, ISTAT_URL],
        "gap_analysis": "Domande in visita ripetute su visura, rogito, TAEG — nessun glossario unico padovano evergreen.",
        "value_add": "Glossario tre famiglie termini con angolo Padova/Veneto e cross-link mutuo-acquisto.",
    },
    {
        "id": "eq-venerdi-003",
        "status": "published",
        "priority": 2,
        "target_week": "2026-08-29",
        "published_date": DATE_ISO,
        "slug": "blog-tassi-euribor-mutui-padova-agosto-2026",
        "kw_primaria": "tassi mutuo padova euribor",
        "intent": "finanziamento",
        "title": "Tassi Euribor e mutui a Padova: guida agosto 2026",
        "cluster": "mutuo-finanza",
        "editorial_type": "trend",
        "monitoring_area": "mercato",
        "different_from": "blog-tassi-mutui-minimi-approfittarne-padova-2026",
        "research_refs": [BANCA_ITALIA, ECB_RATES],
        "hype_sources_read": [CRIF_BAROMETRO, GU_URL, ADE_OSSERVATORIO],
        "gap_analysis": "Articolo tassi minimi copre fase BCE; gap su Euribor variabile e spread agosto 2026 Padova.",
        "value_add": "Spiegazione Euribor+spread senza tassi inventati, confronto fisso/variabile e link servizio mutuo.",
    },
    {
        "id": "eq-venerdi-004",
        "status": "published",
        "priority": 3,
        "target_week": "2026-08-29",
        "published_date": DATE_ISO,
        "slug": "blog-registro-contratti-affitto-padova-2026",
        "kw_primaria": "registro contratti affitto padova",
        "intent": "locazione-normativa",
        "title": "Registro contratti affitto Padova: obblighi ADE 2026",
        "cluster": "locazioni-normativa",
        "editorial_type": "evergreen",
        "monitoring_area": "normativa",
        "different_from": "blog-appartamento-affitto-limena-contratto-2026",
        "research_refs": [ADE_REGISTRO, GU_URL],
        "hype_sources_read": [ADE_OSSERVATORIO, MEF_ACCORDI, FIMAA_VENETO],
        "gap_analysis": "Limena contratto tratta caparra; manca pillar registro ADE 30 giorni dedicato Padova.",
        "value_add": "Flusso registrazione, imposte e detrazioni con tipologie contratto e pratica Limena.",
    },
    {
        "id": "eq-venerdi-005",
        "status": "published",
        "priority": 4,
        "target_week": "2026-08-29",
        "published_date": DATE_ISO,
        "slug": "blog-visura-catastale-acquisto-casa-padova-2026",
        "kw_primaria": "visura catastale acquisto casa padova",
        "intent": "acquisto-documenti",
        "title": "Visura catastale nell'acquisto casa a Padova: guida 2026",
        "cluster": "acquisto-documenti",
        "editorial_type": "evergreen",
        "monitoring_area": "normativa",
        "different_from": "blog-checklist-verifiche-prima-compromesso-padova-2026",
        "research_refs": [ADE_CATASTO, NOTAI_VISURA],
        "hype_sources_read": [OMI_URL, ISTAT_URL, BANCA_ITALIA],
        "gap_analysis": "Checklist compromesso cita visura; serve guida dedicata campi visura e planimetria Padova.",
        "value_add": "Lettura visura per acquirente padovano, checklist pre-caparra e collegamento mutuo-perizia.",
    },
]


def registry_blog_entry(cfg: dict) -> str:
    r = cfg["registry"]
    return f"""    {{
      "titolo": "{r['titolo']}",
      "categoria": "{r['categoria']}",
      "data": "{DATE_ISO}",
      "stato": "pubblicato",
      "immagine_copertina": "{cfg['hero']}",
      "url_statico": "{cfg['slug']}",
      "tempo": {r['tempo']},
      "autore": "Gino Capon",
      "contenuto": "{r['contenuto']}",
      "evidenza": {str(r['evidenza']).lower()}
    }},
"""


def registry_homepage_entry(cfg: dict) -> str:
    r = cfg["registry"]
    return f"""    {{
      "titolo": "{r['titolo']}",
      "categoria": "{r['categoria']}",
      "data": "{DATE_ISO}",
      "immagine_copertina": "{cfg['hero']}",
      "url_statico": "{cfg['slug']}"
    }},
"""


def registry_static_map_entry(cfg: dict) -> str:
    return f"    '{cfg['static_map_key']}': {{ img: '{cfg['hero']}', url: '{cfg['slug']}' }},\n"


def build_registry_json(results: list[dict]) -> dict:
    blog_entries = []
    admin_entries = []
    hp_entries = []
    files_meta = []
    for cfg in ARTICLES:
        r = cfg["registry"]
        base = {
            "titolo": r["titolo"],
            "categoria": r["categoria"],
            "data": DATE_ISO,
            "stato": "pubblicato",
            "immagine_copertina": cfg["hero"],
            "url_statico": cfg["slug"],
            "tempo": r["tempo"],
            "autore": "Gino Capon",
            "contenuto": r["contenuto"],
            "evidenza": r["evidenza"],
        }
        blog_entries.append(base)
        admin_entries.append({
            **base,
            "contenuto": r["admin_contenuto"],
            "emoji": r["emoji"],
            "data_pubblicazione": DATE_ISO,
        })
        hp_entries.append({
            "titolo": r["titolo"],
            "categoria": r["categoria"],
            "data": DATE_ISO,
            "stato": "pubblicato",
            "immagine_copertina": cfg["hero"],
            "url_statico": cfg["slug"],
        })
        words = next((x["words"] for x in results if x["slug"] == cfg["slug"]), 0)
        files_meta.append({
            "filename": cfg["filename"],
            "slug": cfg["slug"],
            "wordCount_body": words,
        })
    return {
        "generated": DATE_ISO,
        "date_display": DATE_IT,
        "files": files_meta,
        "blog_html_articoliStatici": blog_entries,
        "admin_blogSeedArticles": admin_entries,
        "homepage_js_articoliStatici": hp_entries,
    }


def patch_blog_html() -> None:
    path = ROOT / "blog.html"
    text = path.read_text(encoding="utf-8")
    marker = "  const articoliStatici = [\n"
    to_add = ""
    for cfg in ARTICLES:
        if cfg["slug"] not in text:
            to_add += registry_blog_entry(cfg)
    if to_add:
        text = text.replace(marker, marker + to_add, 1)
        path.write_text(text, encoding="utf-8")
        print(f"blog.html: +{to_add.count('url_statico')} articoli")


def patch_admin_html() -> None:
    path = ROOT / "admin.html"
    text = path.read_text(encoding="utf-8")
    marker = "const _blogSeedArticles = [\n"
    to_add = ""
    for cfg in ARTICLES:
        if cfg["slug"] in text:
            continue
        r = cfg["registry"]
        to_add += (
            f"  {{ titolo: {json.dumps(r['titolo'], ensure_ascii=False)}, "
            f"categoria: {json.dumps(r['categoria'], ensure_ascii=False)}, "
            f"data: '{DATE_ISO}', tempo: {r['tempo']}, stato: 'pubblicato', "
            f"autore: 'Gino Capon', emoji: '{r['emoji']}', "
            f"immagine_copertina: '{cfg['hero']}', url_statico: '{cfg['slug']}', "
            f"contenuto: {json.dumps(r['admin_contenuto'], ensure_ascii=False)}, "
            f"evidenza: {'true' if r['evidenza'] else 'false'}, "
            f"data_pubblicazione: '{DATE_ISO}' }},\n"
        )
    if to_add:
        text = text.replace(marker, marker + to_add, 1)
        path.write_text(text, encoding="utf-8")
        print(f"admin.html: +{to_add.count('url_statico')} seed")


def patch_sitemap(slugs: list[str]) -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    insert = ""
    for slug in slugs:
        if slug in text:
            continue
        insert += (
            f"  <url><loc>https://righettoimmobiliare.it/{slug}</loc>"
            f"<lastmod>{DATE_ISO}</lastmod><changefreq>monthly</changefreq>"
            f"<priority>0.8</priority></url>\n"
        )
    if not insert:
        print("sitemap.xml: già aggiornato")
        return
    anchor = "  <!-- Nuovi articoli blog -->\n"
    if anchor in text:
        text = text.replace(anchor, anchor + insert, 1)
    else:
        text = text.replace(
            "  <url><loc>https://righettoimmobiliare.it/blog</loc>",
            insert + "  <url><loc>https://righettoimmobiliare.it/blog</loc>",
            1,
        )
    path.write_text(text, encoding="utf-8")
    print(f"sitemap.xml: +{insert.count('<url>')} URL")


def patch_homepage() -> None:
    path = ROOT / "js" / "homepage.js"
    text = path.read_text(encoding="utf-8")
    art_add = ""
    map_add = ""
    for cfg in ARTICLES:
        if cfg["slug"] not in text:
            art_add += registry_homepage_entry(cfg)
            map_add += registry_static_map_entry(cfg)
    if art_add:
        text = text.replace("  const articoliStatici = [\n", "  const articoliStatici = [\n" + art_add, 1)
    if map_add:
        text = text.replace("  const staticMap = {\n", "  const staticMap = {\n" + map_add, 1)
    if art_add or map_add:
        path.write_text(text, encoding="utf-8")
        print("homepage.js: articoliStatici + staticMap aggiornati")


def patch_editorial_queue() -> None:
    if not EDITORIAL_QUEUE_PATH.exists():
        print("editorial-queue.json: file non trovato, skip")
        return
    data = json.loads(EDITORIAL_QUEUE_PATH.read_text(encoding="utf-8"))
    items = data.setdefault("items", [])
    existing_ids = {item.get("id") for item in items}
    added = 0
    updated = 0
    for eq_item in EDITORIAL_ITEMS:
        eq_id = eq_item["id"]
        found = False
        for item in items:
            if item.get("id") == eq_id:
                item.update(eq_item)
                item["status"] = "published"
                item["published_date"] = DATE_ISO
                updated += 1
                found = True
                break
        if not found:
            items.append(eq_item)
            added += 1
    data["updated"] = DATE_ISO
    EDITORIAL_QUEUE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"editorial-queue.json: +{added} nuovi, {updated} aggiornati -> published ({DATE_ISO})")


def main() -> None:
    ensure_images()
    results: list[dict] = []
    slugs: list[str] = []

    for cfg in ARTICLES:
        body = cfg["body_fn"]()
        words = wc(body)
        if words < MIN_BODY_WORDS - 10:
            raise SystemExit(f"{cfg['slug']}: corpo {words} parole < {MIN_BODY_WORDS}")
        full = build_html(cfg, body, words)
        out = ROOT / cfg["filename"]
        out.write_text(full, encoding="utf-8")
        results.append({"file": cfg["filename"], "slug": cfg["slug"], "words": words})
        slugs.append(cfg["slug"])
        print(f"OK {cfg['filename']} — {words} parole")

    reg = build_registry_json(results)
    REGISTRY_PATH.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK {REGISTRY_PATH.name}")

    patch_blog_html()
    patch_admin_html()
    patch_sitemap(slugs)
    patch_homepage()
    patch_editorial_queue()

    print("\n-- Riepilogo batch venerdì ago29 2026 --")
    for r in results:
        print(f"  • {r['file']} ({r['words']} parole)")
    print("  • blog.html, admin.html, sitemap.xml, homepage.js, editorial-queue.json")


if __name__ == "__main__":
    main()
