# -*- coding: utf-8 -*-
"""Genera 2 articoli blog 29 agosto 2026 — spese condominiali acquisto + proposta acquisto Padova.
Esegui da repo root: python scripts/build_blog_batch_ago29_condominio_proposta.py

Mapping immagini (ensure_images — copy da img/blog esistenti):
  ⚠ Bootstrap batch only — §16-QUATER richiede immagini IA ex novo per slug;
  l'audit hash (`build_editorial_visual_memory.py`) segnala riuso. Non usare copy in nuovi articoli.
  blog-spese-condominiali-acquisto-padova-2026
    hero ← blog-checklist-verifiche-prima-compromesso-padova-2026.webp
    body ← blog-dieci-errori-acquisto-casa-padova-2026.webp,
           blog-appartamento-limena-guida-acquisto-2026.webp,
           blog-gestione-spese-casa-padova-2026.webp
  blog-proposta-acquisto-negoziazione-padova-2026
    hero ← blog-quattro-imposte-rogitio-prima-casa-padova-2026.webp
           (proxy caparra — blog-caparra-confirmatoria-padova.webp non in img/blog)
    body ← blog-documenti-compravendita-rogito-padova-2026.webp (proxy percorso-vendita),
           blog-agenzia-top-servizi-padova-2026.webp (proxy mandato-esclusivo),
           blog-scegliere-immobile-giusto-padova-2026.webp (proxy 5-errori-visita)
"""
from __future__ import annotations

import importlib.util
import json
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

REGISTRY_PATH = ROOT / "scripts" / "ago29_condominio_proposta_registry.json"
EDITORIAL_QUEUE_PATH = ROOT / "data" / "editorial-queue.json"

GU_URL = "https://www.gazzettaufficiale.it"
NORMATTIVA_CC = "https://www.normattiva.it/dynamic/resolve/19420619"
CODICE_CIVILE_CONDO = "https://www.normattiva.it/dynamic/resolve/19420619"  # artt. 1117-1139
NOTAI_ONLINE = "https://notaionline.it"

# sorgente → destinazione per ensure_images()
IMAGE_SOURCES: dict[str, dict[str, tuple[str, str] | list[tuple[str, str]]]] = {
    "blog-spese-condominiali-acquisto-padova-2026": {
        "hero": (
            "img/blog/blog-checklist-verifiche-prima-compromesso-padova-2026.webp",
            "img/blog/blog-spese-condominiali-acquisto-padova-2026-hero.webp",
        ),
        "body": [
            (
                "img/blog/blog-dieci-errori-acquisto-casa-padova-2026.webp",
                "img/blog/blog-spese-condominiali-acquisto-padova-errori.webp",
            ),
            (
                "img/blog/blog-appartamento-limena-guida-acquisto-2026.webp",
                "img/blog/blog-spese-condominiali-acquisto-padova-limena.webp",
            ),
            (
                "img/blog/blog-gestione-spese-casa-padova-2026.webp",
                "img/blog/blog-spese-condominiali-acquisto-padova-budget.webp",
            ),
        ],
    },
    "blog-proposta-acquisto-negoziazione-padova-2026": {
        "hero": (
            "img/blog/blog-quattro-imposte-rogitio-prima-casa-padova-2026.webp",
            "img/blog/blog-proposta-acquisto-negoziazione-padova-2026-hero.webp",
        ),
        "body": [
            (
                "img/blog/blog-documenti-compravendita-rogito-padova-2026.webp",
                "img/blog/blog-proposta-acquisto-negoziazione-padova-percorso.webp",
            ),
            (
                "img/blog/blog-agenzia-top-servizi-padova-2026.webp",
                "img/blog/blog-proposta-acquisto-negoziazione-padova-agenzia.webp",
            ),
            (
                "img/blog/blog-scegliere-immobile-giusto-padova-2026.webp",
                "img/blog/blog-proposta-acquisto-negoziazione-padova-visita.webp",
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


def svg_condominio_millesimi() -> str:
    return """<figure class="chart-wrap" aria-label="Schema millesimi condominio">
<svg viewBox="0 0 540 240" width="100%" height="240" role="img">
<title>Millesimi e ripartizione spese condominiali — schema</title>
<text x="270" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Condominio: millesimi e ripartizione (schema art. 1123 c.c.)</text>
<rect x="40" y="50" width="140" height="50" rx="8" fill="#2C4A6E"/>
<text x="110" y="72" text-anchor="middle" font-size="9" fill="#fff">Unità A</text>
<text x="110" y="88" text-anchor="middle" font-size="7" fill="rgba(255,255,255,.85)">350 millesimi</text>
<rect x="200" y="50" width="140" height="50" rx="8" fill="#3A5F8C"/>
<text x="270" y="72" text-anchor="middle" font-size="9" fill="#fff">Unità B</text>
<text x="270" y="88" text-anchor="middle" font-size="7" fill="rgba(255,255,255,.85)">420 millesimi</text>
<rect x="360" y="50" width="140" height="50" rx="8" fill="#FF6B35" opacity="0.9"/>
<text x="430" y="72" text-anchor="middle" font-size="9" fill="#152435">Unità C</text>
<text x="430" y="88" text-anchor="middle" font-size="7" fill="#152435">230 millesimi</text>
<text x="270" y="145" text-anchor="middle" font-size="9" fill="#6B7A8D">Spesa totale ripartita per millesimi — tabella millesimale obbligatoria</text>
<text x="270" y="210" text-anchor="middle" font-size="8" fill="#6B7A8D">Fatto: art. 1123 Codice Civile · Analisi: verificare tabella prima dell'acquisto</text>
</svg>
<figcaption>Schema ripartizione spese condominiali per millesimi. La tabella millesimale va richiesta in fase di due diligence.</figcaption>
</figure>"""


def svg_condominio_documenti() -> str:
    return """<figure class="chart-wrap" aria-label="Flusso documenti condominio acquisto">
<svg viewBox="0 0 520 280" width="100%" height="280" role="img">
<title>Documenti condominio prima dell'offerta</title>
<text x="260" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Due diligence condominio: sequenza documenti</text>
<rect x="185" y="38" width="150" height="34" rx="17" fill="#2C4A6E"/><text x="260" y="60" text-anchor="middle" font-size="9" fill="#fff">1. Regolamento</text>
<path d="M260 72 L260 88" stroke="#FF6B35" stroke-width="2"/>
<rect x="185" y="88" width="150" height="34" rx="17" fill="#FF6B35"/><text x="260" y="110" text-anchor="middle" font-size="9" fill="#152435">2. Ultimi verbali</text>
<path d="M260 122 L260 138" stroke="#FF6B35" stroke-width="2"/>
<rect x="185" y="138" width="150" height="34" rx="17" fill="#2C4A6E"/><text x="260" y="160" text-anchor="middle" font-size="9" fill="#fff">3. Bilancio e saldo</text>
<path d="M260 172 L260 188" stroke="#FF6B35" stroke-width="2"/>
<rect x="185" y="188" width="150" height="34" rx="17" fill="#2C4A6E"/><text x="260" y="210" text-anchor="middle" font-size="9" fill="#fff">4. Proposta / caparra</text>
<text x="260" y="255" text-anchor="middle" font-size="8" fill="#6B7A8D">Consiglio Righetto: documenti condominiali prima dell'impegno economico</text>
</svg>
<figcaption>Percorso consigliato: regolamento, verbali assemblea, saldo spese e bilancio prima della proposta.</figcaption>
</figure>"""


def svg_proposta_fasi() -> str:
    return """<figure class="chart-wrap" aria-label="Fasi proposta acquisto">
<svg viewBox="0 0 540 240" width="100%" height="240" role="img">
<title>Dalla visita alla proposta accettata</title>
<text x="270" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Proposta d'acquisto: fasi negoziazione Padova</text>
<rect x="30" y="55" width="110" height="40" rx="8" fill="#2C4A6E"/><text x="85" y="80" text-anchor="middle" font-size="8" fill="#fff">Visita + comparabili</text>
<path d="M140 75 L160 75" stroke="#FF6B35" stroke-width="2" marker-end="url(#arr)"/>
<rect x="165" y="55" width="110" height="40" rx="8" fill="#3A5F8C"/><text x="220" y="80" text-anchor="middle" font-size="8" fill="#fff">Proposta scritta</text>
<path d="M275 75 L295 75" stroke="#FF6B35" stroke-width="2"/>
<rect x="300" y="55" width="110" height="40" rx="8" fill="#FF6B35"/><text x="355" y="80" text-anchor="middle" font-size="8" fill="#152435">Controproposta</text>
<path d="M410 75 L430 75" stroke="#FF6B35" stroke-width="2"/>
<rect x="435" y="55" width="75" height="40" rx="8" fill="#2C4A6E"/><text x="472" y="80" text-anchor="middle" font-size="7" fill="#fff">Accettazione</text>
<text x="270" y="145" text-anchor="middle" font-size="9" fill="#6B7A8D">Termine accettazione · condizione mutuo · caparra confirmatoria</text>
<text x="270" y="210" text-anchor="middle" font-size="8" fill="#6B7A8D">Analisi: mercato padovano competitivo — proposta chiara e documentata</text>
</svg>
<figcaption>Schema fasi dalla visita alla proposta accettata: termini, condizioni e negoziazione nel Padovano.</figcaption>
</figure>"""


def svg_proposta_elementi() -> str:
    return """<figure class="chart-wrap" aria-label="Elementi proposta d'acquisto">
<svg viewBox="0 0 520 220" width="100%" height="220" role="img">
<title>Checklist elementi proposta</title>
<text x="260" y="20" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Proposta d'acquisto: elementi essenziali</text>
<rect x="40" y="45" width="200" height="35" rx="6" fill="#2C4A6E"/><text x="140" y="67" text-anchor="middle" font-size="9" fill="#fff">Prezzo e modalità pagamento</text>
<rect x="280" y="45" width="200" height="35" rx="6" fill="#3A5F8C"/><text x="380" y="67" text-anchor="middle" font-size="9" fill="#fff">Termine accettazione</text>
<rect x="40" y="95" width="200" height="35" rx="6" fill="#FF6B35" opacity="0.9"/><text x="140" y="117" text-anchor="middle" font-size="9" fill="#152435">Condizione sospensiva mutuo</text>
<rect x="280" y="95" width="200" height="35" rx="6" fill="#E1DBD1"/><text x="380" y="117" text-anchor="middle" font-size="9" fill="#152435">Caparra confirmatoria</text>
<rect x="160" y="145" width="200" height="35" rx="6" fill="#2C4A6E" opacity="0.85"/><text x="260" y="167" text-anchor="middle" font-size="9" fill="#fff">Identificazione immobile (catasto)</text>
<text x="260" y="205" text-anchor="middle" font-size="8" fill="#6B7A8D">Fatto: art. 1326 e 1385 c.c. · Analisi: clausole su perizia e rogito</text>
</svg>
<figcaption>Elementi minimi di una proposta d'acquisto scritta — base negoziazione Padova/Limena 2026.</figcaption>
</figure>"""


def _exp(prefix: str, n: int, templates: list[str]) -> list[str]:
    base = [t.format(p=prefix) for t in templates]
    if len(base) >= n:
        return base[:n]
    extra: list[str] = []
    variants = [
        "{p}: incrociare OMI semestrale ADE con comparabili di zona e stato manutentivo dell'unità.",
        "{p}: distinguere sempre fatto normativo, dichiarazione dell'annuncio e analisi di mercato locale.",
        "{p}: per Limena e cintura padovana verificare microzone OMI diverse dal centro storico.",
        "{p}: conservare ricevute e documenti per contenziosi e adempimenti fiscali post-rogito.",
        "{p}: prima della caparra chiedere visura, planimetria conforme e APE aggiornato.",
    ]
    vi = 0
    while len(base) + len(extra) < n:
        extra.append(variants[vi % len(variants)].format(p=prefix))
        vi += 1
    return base + extra


_EXP_T = [
    "{p} nel Padovano richiede distinzione tra fatto normativo (Codice Civile, circolari), dichiarazione del venditore e analisi di mercato locale.",
    "{p}: Righetto coordina acquisti e vendite dal 2000 — compenso concordato in sede, nessun listino percentuale online.",
    "{p} — cross-link utili: checklist compromesso, guida Limena e documenti rogito senza duplicare angoli editoriali esistenti.",
    "{p}: ISTAT e Osservatorio ADE danno contesto macro Veneto; per il singolo appartamento servono comparabili e visita.",
    "{p}: red flag — rifiuto planimetria, assenza verbali condominiali o richiesta pagamenti non tracciati prima del contratto scritto.",
    "{p}: studenti e famiglie convivono nel mercato padovano — domanda universitaria e ospedaliera sostiene certe microzone.",
    "{p}: pendolari verso Mestre o Vicenza valutano Limena per metratura — calcolare costo totale spostamento oltre al prezzo.",
]

EXPANSION_CONDOMINIO = _exp("Spese condominiali acquisto Padova 2026", 58, _EXP_T + [
    "Spese condominiali acquisto Padova 2026: art. 1117 c.c. definisce parti comuni — ascensore, facciata, scale condivise incidono su budget futuro.",
    "Spese condominiali acquisto Padova 2026: art. 1123 c.c. stabilisce ripartizione per millesimi — tabella millesimale va richiesta prima dell'offerta.",
    "Spese condominiali acquisto Padova 2026: art. 1130 c.c. regola obblighi amministratore — verbali e bilancio sono fonti verificabili.",
    "Spese condominiali acquisto Padova 2026: differenza da blog-gestione-spese-casa — qui focus due diligence condominio in fase acquisto, non possesso post-rogito.",
    "Spese condominiali acquisto Padova 2026: spese ordinarie (pulizie, ascensore) vs straordinarie (tetto, facciata) — delibere assemblea documentano il secondo.",
    "Spese condominiali acquisto Padova 2026: saldo spese e regolarità contributiva del venditore — dichiarazione obbligatoria in rogito.",
    "Spese condominiali acquisto Padova 2026: morosità pregressa del venditore non si trasferisce automaticamente — verificare con amministratore.",
    "Spese condominiali acquisto Padova 2026: regolamento condominiale vincola uso (animali, affitti brevi) — leggere prima della proposta.",
    "Spese condominiali acquisto Padova 2026: fondo riserva e lavori deliberati non eseguiti — quota futura va stimata, non inventata.",
    "Spese condominiali acquisto Padova 2026: riscaldamento centralizzato incide su spese mensili — chiedere ultimo rendiconto ripartizione.",
    "Spese condominiali acquisto Padova 2026: box auto e cantina con subalterno separato — millesimi distinti da unità principale.",
    "Spese condominiali acquisto Padova 2026: condomini padovani storici spesso con ascensori datati — manutenzione straordinaria frequente.",
    "Spese condominiali acquisto Padova 2026: Limena condomini più recenti — verificare comunque delibere su efficientamento energetico.",
    "Spese condominiali acquisto Padova 2026: perizia bancaria non sostituisce analisi condominiale — due diligence parallele.",
    "Spese condominiali acquisto Padova 2026: OMI vendita indica fascia prezzo — spese condominiali incidono su costo totale mensile mutuo+condominio.",
    "Spese condominiali acquisto Padova 2026: annuncio che omette spese è red flag — chiedere cifra indicativa e ultimo verbale.",
    "Spese condominiali acquisto Padova 2026: assemblea straordinaria in corso può bloccare mutuo se importi rilevanti — trasparenza prima della caparra.",
    "Spese condominiali acquisto Padova 2026: servizio acquisto Righetto richiede documentazione condominiale in percorso ordinato.",
    "Spese condominiali acquisto Padova 2026: contenzioso tra condomini attivo segnala gestione difficile — verbali rivelano liti ricorrenti.",
    "Spese condominiali acquisto Padova 2026: assicurazione fabbricato e polizze condominiali — coperture da verificare in bilancio.",
    "Spese condominiali acquisto Padova 2026: form lead per consulenza acquisto — indicare zona e tipologia immobile.",
    "Spese condominiali acquisto Padova 2026: Gazzetta Ufficiale per riforme condominiali — monitorare novità normative.",
    "Spese condominiali acquisto Padova 2026: non pubblicare importi € inventati per spese medie — ogni stabile ha tabella propria.",
    "Spese condominiali acquisto Padova 2026: confronto comparabili deve includere spese condominiali oltre prezzo mq.",
    "Spese condominiali acquisto Padova 2026: prima casa under 36 — budget mutuo sensibile a spese fisse mensili.",
    "Spese condominiali acquisto Padova 2026: cross-link visura catastale e checklist compromesso — documenti complementari.",
    "Spese condominiali acquisto Padova 2026: amministratore professionale vs volontario — qualità rendicontazione varia.",
    "Spese condominiali acquisto Padova 2026: detrazioni fiscali riqualificazione parti comuni — agevolazioni non sostituiscono due diligence.",
    "Spese condominiali acquisto Padova 2026: acquisto all'asta — verificare debiti condominiali con curatore.",
    "Spese condominiali acquisto Padova 2026: ultimo consiglio — costo totale = rata mutuo + condominio + utenze, non solo prezzo.",
])

EXPANSION_PROPOSTA = _exp("Proposta acquisto casa Padova 2026", 58, _EXP_T + [
    "Proposta acquisto casa Padova 2026: art. 1326 c.c. — proposta vincolante se contiene termine accettazione e elementi essenziali contratto.",
    "Proposta acquisto casa Padova 2026: art. 1385 c.c. — caparra confirmatoria vincola entrambe le parti; distinta da semplice acconto.",
    "Proposta acquisto casa Padova 2026: differenza da blog-caparra-confirmatoria — qui percorso negoziazione completo, non solo istituto caparra.",
    "Proposta acquisto casa Padova 2026: proposta scritta con prezzo, termini, identificazione catastale e condizioni sospensive.",
    "Proposta acquisto casa Padova 2026: condizione sospensiva mutuo standard in mercato ordinato — lettera banca o pre-approvazione.",
    "Proposta acquisto casa Padova 2026: prezzo legato a esito perizia bancaria protegge acquirente — clausola prudente.",
    "Proposta acquisto casa Padova 2026: termine accettazione breve in mercato competitivo Padova — 48-72 ore non raro su immobili richiesti.",
    "Proposta acquisto casa Padova 2026: controproposta venditore — nuova trattativa, non accettazione tacita.",
    "Proposta acquisto casa Padova 2026: proposta verbale non sostituisce scritto — trattativa informale rischiosa.",
    "Proposta acquisto casa Padova 2026: acquirente serio presenta qualifica finanziaria — diffidare offerte senza mutuo in mercato competitivo.",
    "Proposta acquisto casa Padova 2026: venditore valuta proposte su prezzo, termini rogito, solidità acquirente, condizioni.",
    "Proposta acquisto casa Padova 2026: mediazione Righetto coordina proposta tra parti — compenso concordato in sede.",
    "Proposta acquisto casa Padova 2026: differenza da blog-percorso-vendita — qui focus negoziazione offerta acquirente, non roadmap venditore.",
    "Proposta acquisto casa Padova 2026: Limena trilocali richiesti — proposta con caparra e mutuo chiaro batte trattative infinite.",
    "Proposta acquisto casa Padova 2026: OMI vendita per comparables — offerta coerente con fascia min-med-max ADE semestre.",
    "Proposta acquisto casa Padova 2026: non inventare percentuali sconto medie — ogni trattativa è singola.",
    "Proposta acquisto casa Padova 2026: proposta su immobile con più offerenti — completezza documentale accelera scelta venditore.",
    "Proposta acquisto casa Padova 2026: clausola su conformità urbanistica e sanatoria — tutela acquirente prudente.",
    "Proposta acquisto casa Padova 2026: data rogito indicativa — coordinare mutuo, notaio e venditore.",
    "Proposta acquisto casa Padova 2026: proposta con riserva su esito visite tecniche — raro ma possibile su immobili complessi.",
    "Proposta acquisto casa Padova 2026: revoca proposta prima accettazione — regole art. 1330 c.c. se vincolante.",
    "Proposta acquisto casa Padova 2026: accettazione espressa venditore — momento in cui nasce impegno contrattuale preliminare.",
    "Proposta acquisto casa Padova 2026: dal sì alla caparra — versamento tracciato e ricevuta obbligatori.",
    "Proposta acquisto casa Padova 2026: proposta e spese condominiali — chiedere saldo prima di fissare prezzo finale.",
    "Proposta acquisto casa Padova 2026: servizio mutuo Righetto allinea tempistiche proposta e perizia banca.",
    "Proposta acquisto casa Padova 2026: form blog per consulenza — budget, zona, urgenza rogito.",
    "Proposta acquisto casa Padova 2026: Banca d'Italia indagini danno contesto credito — non sostituisce pre-approvazione.",
    "Proposta acquisto casa Padova 2026: cross-link dieci errori acquisto e 5 errori visita — complementari senza overlap.",
    "Proposta acquisto casa Padova 2026: proposta condizionata a vendita altra casa — catena compravendite frequente in famiglie.",
    "Proposta acquisto casa Padova 2026: ultimo consiglio — proposta scritta chiara con condizione mutuo e termini deposito trasparenti.",
])


def body_spese_condominiali() -> str:
    return f"""
{aeo_box("In sintesi", "Le <strong>spese condominiali nell'acquisto casa a Padova</strong> vanno verificate <strong>prima della proposta</strong>: regolamento, verbali assemblea, tabella millesimale e saldo spese del venditore. Fonte <a href=\"{CODICE_CIVILE_CONDO}\" target=\"_blank\" rel=\"noopener noreferrer\">Codice Civile artt. 1117-1139</a>. Diverso da <a href=\"blog-gestione-spese-casa-padova-2026\">gestione spese casa</a>: qui due diligence condominio in fase acquisto.")}

<p><strong>Distinzione editoriale:</strong> <em>Fatto</em> — normativa condominiale (parti comuni art. 1117, millesimi art. 1123, obblighi amministratore art. 1130). <em>Dichiarazione</em> — cifre spese in annuncio sono indicative. <em>Analisi</em> — incrocio delibere straordinarie, fondo riserva e budget mutuo+condominio per Padova e Limena.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#cosa">Cosa sono le spese condominiali</a></li>
<li><a href="#normativa">Codice Civile: parti comuni</a></li>
<li><a href="#millesimi">Millesimi e ripartizione</a></li>
<li><a href="#documenti">Documenti da chiedere</a></li>
<li><a href="#ordinarie">Ordinarie vs straordinarie</a></li>
<li><a href="#delibere">Delibere e rischi</a></li>
<li><a href="#saldo">Saldo spese venditore</a></li>
<li><a href="#padova-limena">Padova vs Limena</a></li>
<li><a href="#checklist">Checklist pre-proposta</a></li>
<li><a href="#budget">Budget totale acquirente</a></li>
<li><a href="#pratica">Percorso pratico Righetto</a></li>
</ol></nav>

{sol_box("Devo verificare le spese condominiali prima di comprare a Padova?", [
    ("Regolamento e verbali", "Documenti condominiali prima dell'offerta", "checklist compromesso", "blog-checklist-verifiche-prima-compromesso-padova-2026"),
    ("Acquisto", "Coordinamento due diligence fino al rogito", "consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
    ("Mutuo", "Budget rata + spese fisse mensili", "servizio mutuo", "servizio-mutuo"),
    ("Limena", "Condomini cintura nord Padova", "zona Limena", "zona-limena"),
])}

<h2 id="cosa">Cosa sono le spese condominiali e perché contano in acquisto</h2>
<p>Acquistare un appartamento in condominio significa entrare in un <strong>organismo con parti comuni</strong> (scale, facciate, ascensori, impianti centralizzati) con costi ripartiti tra i condomini. Le spese mensili o trimestrali incidono sul <strong>costo totale</strong> dell'abitazione — spesso quanto o più della differenza di prezzo tra due annunci simili.</p>
<p>In fase di acquisto, l'obiettivo non è stimare al centesimo la rata futura (che varia annualmente), ma verificare <strong>assenza di sorprese</strong>: lavori straordinari deliberati, morosità del venditore, contenziosi attivi, regolamento restrittivo. Fonte normativa: <a href=\"{CODICE_CIVILE_CONDO}\" target=\"_blank\" rel=\"noopener noreferrer\">Codice Civile — Libro III, Titolo VII (Condominio)</a>.</p>

{svg_condominio_millesimi()}

<h2 id="normativa">Codice Civile: parti comuni (art. 1117 e ss.)</h2>
<p>L'<strong>art. 1117 c.c.</strong> elenca le parti comuni dell'edificio: suolo, fondazioni, muri maestri, scale, ascensori, infissi e chiusure di locali comuni, ecc. Sono di proprietà indivisa dei condomini e i costi di manutenzione si ripartiscono. L'<strong>art. 1118</strong> distingue proprietà esclusiva dell'unità immobiliare da parti comuni — essenziale per capire cosa pagate in quota.</p>
<p>L'<strong>art. 1139 c.c.</strong> regola l'assemblea dei condomini: le delibere su lavori straordinari e spese rilevanti vincolano anche il futuro acquirente se regolarmente approvate. Per questo i <strong>verbali degli ultimi 12-24 mesi</strong> sono documento prioritario in due diligence.</p>

<table>
<thead><tr><th>Articolo c.c.</th><th>Contenuto</th><th>Utilità acquirente</th></tr></thead>
<tbody>
<tr><td>Art. 1117</td><td>Parti comuni edificio</td><td>Capire cosa include spesa condominiale</td></tr>
<tr><td>Art. 1123</td><td>Ripartizione per millesimi</td><td>Verificare tabella millesimale</td></tr>
<tr><td>Art. 1130</td><td>Obblighi amministratore</td><td>Richiedere bilancio e rendiconti</td></tr>
<tr><td>Art. 1139</td><td>Assemblea e delibere</td><td>Leggere lavori deliberati</td></tr>
</tbody>
</table>

<h2 id="millesimi">Millesimi e ripartizione spese (art. 1123)</h2>
<p>L'<strong>art. 1123 c.c.</strong> stabilisce che le spese per la conservazione delle parti comuni si ripartiscono in misura proporzionale al valore di ciascuna unità, salvo patto contrario nel regolamento. La <strong>tabella millesimale</strong> indica la quota di ciascun subalterno sul totale mille.</p>
<p>Un appartamento al piano alto con ascensore e terrazzo può avere millesimi superiori a uno al piano terra — stesso prezzo di acquisto, costi condominiali diversi. Chiedere sempre tabella aggiornata e incrociarla con planimetria catastale.</p>

{svg_condominio_documenti()}

<h2 id="documenti">Documenti condominiali da chiedere prima dell'offerta</h2>
<ol>
<li><strong>Regolamento di condominio</strong> — uso parti comuni, animali, affitti, modifiche interne.</li>
<li><strong>Ultimi verbali assemblea</strong> (minimo 12 mesi) — delibere lavori, contenziosi, nomina amministratore.</li>
<li><strong>Bilancio consuntivo e preventivo</strong> — spese ordinarie e straordinarie previste.</li>
<li><strong>Tabella millesimale</strong> — ripartizione quote.</li>
<li><strong>Attestazione saldo spese</strong> del venditore — regolarità contributiva.</li>
</ol>

{blog_fig("img/blog/blog-spese-condominiali-acquisto-padova-errori.webp", "Errori comuni su spese condominiali in acquisto — verifiche Padova 2026")}

<h2 id="ordinarie">Spese ordinarie vs straordinarie</h2>
<p>Le <strong>spese ordinarie</strong> coprono gestione corrente: pulizia scale, ascensore, illuminazione comune, amministratore. Le <strong>straordinarie</strong> derivano da delibere assemblea: rifacimento facciata, tetto, efficientamento energetico, adeguamento impianti.</p>
<p>Un immobile con prezzo apparentemente conveniente può avere <strong>delibere straordinarie già approvate</strong> con rateizzazione pluriennale — l'acquirente le eredita. I verbali rivelano importi deliberati anche se i lavori non sono ancora iniziati.</p>

<table>
<thead><tr><th>Tipo spesa</th><th>Esempi</th><th>Dove verificare</th><th>Rischio</th></tr></thead>
<tbody>
<tr><td>Ordinaria</td><td>Pulizie, ascensore, amministratore</td><td>Bilancio consuntivo</td><td>Basso se stabile</td></tr>
<tr><td>Straordinaria deliberata</td><td>Facciata, tetto, cappotto</td><td>Verbali assemblea</td><td>Alto — quote future</td></tr>
<tr><td>Fondo riserva</td><td>Accantonamento lavori</td><td>Bilancio</td><td>Medio — liquidità condominio</td></tr>
<tr><td>Morosità venditore</td><td>Debiti pregressi</td><td>Attestazione amministratore</td><td>Medio — verificare regole</td></tr>
</tbody>
</table>

<h2 id="delibere">Delibere assemblea e rischi per l'acquirente</h2>
<p>L'assemblea condominiale delibera su spese, lavori e regolamentazioni interne. Delibere su <strong>lavori strutturali</strong>, <strong>barriere architettoniche</strong> o <strong>impianti centralizzati</strong> possono comportare oneri significativi ripartiti per millesimi.</p>
<p>Contenziosi tra condomini (art. 1107 c.c. — azioni in giudizio) o liti con amministratore segnalati nei verbali indicano gestione complessa. Non è motivo automatico di abbandono, ma va <em>analizzato</em> e scontato in trattativa se del caso.</p>

{blog_fig("img/blog/blog-spese-condominiali-acquisto-padova-limena.webp", "Condominio in cintura padovana — due diligence spese Limena e hinterland")}

<h2 id="saldo">Saldo spese e dichiarazione del venditore</h2>
<p>In rogito, il venditore deve attestare la <strong>regolarità dei pagamenti</strong> delle spese condominiali e delle quote di lavori straordinari già deliberati. L'amministratore rilascia certificazione su richiesta — tempi 15-20 giorni lavorativi tipici.</p>
<p>L'acquirente non eredita automaticamente i debiti del venditore verso il condominio per spese anteriori al rogito, ma conviene verificare assenza di <strong>pignoramenti</strong> o contenziosi che possano ritardare la stipula. Correlato: <a href=\"blog-documenti-compravendita-rogito-padova-2026\">documenti rogito Padova</a>.</p>

<h2 id="padova-limena">Condominio a Padova centro vs Limena</h2>
<p>A <strong>Padova</strong>, palazzi storici in semicentro e zone Arcella/Portello spesso hanno ascensori datati e facciate vincolate — straordinari più frequenti. A <strong>Limena</strong>, edifici residenziali più recenti possono avere spese ordinarie contenute ma verificare comunque delibere su cappotto o fotovoltaico condominiale.</p>
<p>Incrociare con <a href=\"{OMI_URL}\" target=\"_blank\" rel=\"noopener noreferrer\">OMI vendita ADE</a> per coerenza prezzo/zona — non confondere fascia OMI con costo condominiale. Pagina <a href=\"zona-limena\">zona Limena</a> per contesto cintura nord.</p>

<h2 id="checklist">Checklist spese condominiali pre-proposta</h2>
<ul>
<li>Richiesto regolamento condominiale e tabella millesimale.</li>
<li>Letti verbali ultimi 12-24 mesi — cercare «straordinario», «facciata», «tetto».</li>
<li>Confrontato spese indicate in annuncio con bilancio consuntivo.</li>
<li>Verificato assenza morosità venditore (attestazione amministratore).</li>
<li>Stimato impatto lavori deliberati non ancora pagati sul budget futuro.</li>
<li>Incluso costo condominio stimato nel calcolo rata mutuo + spese fisse.</li>
</ul>

{blog_fig("img/blog/blog-spese-condominiali-acquisto-padova-budget.webp", "Budget totale acquisto — rata mutuo e spese condominiali Padova 2026")}

<h2 id="budget">Integrare le spese nel budget totale dell'acquirente</h2>
<p>La banca valuta il <strong>rapporto rata/reddito</strong> — le spese condominiali fisse aumentano l'uscita mensile reale anche se non sempre entra nel calcolo mutuo. Per prima casa a Padova, simulare: rata mutuo + condominio + utenze + manutenzione ordinaria.</p>
<p>Contesto macro: <a href=\"{ISTAT_URL}\" target=\"_blank\" rel=\"noopener noreferrer\">ISTAT prezzi abitazioni</a>, <a href=\"{BANCA_ITALIA}\" target=\"_blank\" rel=\"noopener noreferrer\">Banca d'Italia</a>. Per il singolo immobile: comparabili, visita e documenti — mai importi € di mercato inventati.</p>

<h2 id="pratica">Percorso pratico Righetto: acquisto con condominio ordinato</h2>
<p>Righetto Immobiliare coordina visite e documentazione dal 2000 su Padova e 101 comuni. In percorso acquisto ordinato, chiediamo documentazione condominiale <strong>prima della proposta</strong> — allineato a <a href=\"blog-dieci-errori-acquisto-casa-padova-2026\">dieci errori acquisto</a> e <a href=\"blog-appartamento-limena-guida-acquisto-2026\">guida acquisto Limena</a>.</p>
<p>Approfondimenti: <a href=\"blog-visura-catastale-acquisto-casa-padova-2026\">visura catastale</a>, <a href=\"blog-prima-casa-under-36-consap-padova-2026\">prima casa under 36</a>, <a href=\"servizio-mutuo\">servizio mutuo</a>. Compenso mediazione concordato in sede — nessun listino percentuale online.</p>

<h2 id="domande">Domande frequenti sul condominio in acquisto</h2>
<p>Acquirenti padovani ci chiedono spesso se le spese in annuncio siano vincolanti: no, sono <em>dichiarazioni</em> indicative — solo bilancio e verbali danno quadro verificabile. Un altro dubbio frequente riguarda l'ereditarietà dei lavori straordinari: se deliberati regolarmente in assemblea, le quote future gravano sul nuovo proprietario proporzionalmente ai millesimi.</p>
<p>In edifici con pochi condomini (mini-condominio) l'amministratore può mancare — in quel caso verbali e regolamento vanno richiesti direttamente ai comproprietari. A Limena, molti acquirenti pendolari sottovalutano l'impatto annuo delle spese rispetto al risparmio sul prezzo mq: calcolare costo totale quinquennale aiuta il confronto tra due proposte simili.</p>
<p>Per immobili con riscaldamento centralizzato a Padova, verificare nei verbali eventuali delibere su sostituzione caldaia o ripartizione straordinaria spese termiche — voce spesso più rilevante delle pulizie scale. Condomini con ascensore obbligatorio su edifici alti richiedono manutenzione periodica certificata: costi ricorrenti da chiedere in rendiconto annuale amministratore.</p>
<p>Prima di presentare proposta, incrociare spese condominiali con comparabili della stessa palazzina se possibile — due unità stesso stabile condividono millesimi e rendiconto. Righetto segnala immobili con documentazione condominiale già completa come plus in trattativa trasparente.</p>

<p>{CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 29 agosto 2026. Fonti: Codice Civile artt. 1117-1139, OMI ADE, normativa condominiale.</p>
"""


def body_proposta_acquisto() -> str:
    return f"""
{aeo_box("In sintesi", "La <strong>proposta d'acquisto a Padova</strong> è il documento scritto con cui l'acquirente offre prezzo e condizioni al venditore. Se accettata entro il termine, vincola le parti (<a href=\"{NORMATTIVA_CC}\" target=\"_blank\" rel=\"noopener noreferrer\">art. 1326 c.c.</a>). Caparra confirmatoria (<strong>art. 1385 c.c.</strong>) segue l'accettazione. Diverso da <a href=\"blog-caparra-confirmatoria-padova\">caparra confirmatoria</a>: qui negoziazione completa.")}

<p><strong>Distinzione editoriale:</strong> <em>Fatto</em> — requisiti proposta vincolante, istituto caparra, condizione sospensiva mutuo. <em>Dichiarazione</em> — prezzo richiesto in annuncio è punto di partenza negoziale. <em>Analisi</em> — strategia offerta in mercato padovano competitivo, Limena e semicentro.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#cosa">Cos'è la proposta d'acquisto</a></li>
<li><a href="#normativa">Base giuridica</a></li>
<li><a href="#elementi">Elementi essenziali</a></li>
<li><a href="#negoziazione">Negoziazione prezzo</a></li>
<li><a href="#mutuo">Condizione sospensiva mutuo</a></li>
<li><a href="#termini">Termini e accettazione</a></li>
<li><a href="#competitivo">Mercato competitivo Padova</a></li>
<li><a href="#agenzia">Ruolo agenzia</a></li>
<li><a href="#errori">Errori comuni</a></li>
<li><a href="#caparra">Dal sì alla caparra</a></li>
<li><a href="#limena">Proposta a Limena</a></li>
</ol></nav>

{sol_box("Come presentare una proposta d'acquisto efficace a Padova?", [
    ("Proposta scritta", "Prezzo, termini, condizione mutuo, identificazione catastale", "caparra confirmatoria", "blog-caparra-confirmatoria-padova"),
    ("Pre-approvazione", "Lettera banca o broker prima dell'offerta", "servizio mutuo", "servizio-mutuo"),
    ("Visite", "Checklist e buone pratiche in sopralluogo", "5 errori visita", "blog-5-errori-visita-immobile-padova-2026"),
    ("Consulenza", "Coordinamento trattativa fino al rogito", "consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
])}

<h2 id="cosa">Cos'è la proposta d'acquisto e quando serve</h2>
<p>La <strong>proposta d'acquisto</strong> (o «offerta d'acquisto») è l'atto con cui l'acquirente manifesta al venditore la volontà di comprare un immobile a determinate condizioni: prezzo, modalità di pagamento, termine per l'accettazione, eventuali condizioni sospensive.</p>
<p>A Padova, in mercato con domanda su trilocali Limena e bilocali semicentro, la proposta scritta e completa distingue l'acquirente serio da chi trattativa verbalmente senza qualifica finanziaria. Non sostituisce il compromesso o il rogito — è il primo impegno formale nella catena negoziale.</p>

{svg_proposta_fasi()}

<h2 id="normativa">Base giuridica: proposta vincolante e caparra</h2>
<p>L'<strong>art. 1326 c.c.</strong> prevede che la proposta vincolante per chi la fa, se contiene un termine per l'accettazione, obbliga il proponente fino a scadenza. L'<strong>art. 1330 c.c.</strong> regola revoca e incompatibilità con accettazione tardiva.</p>
<p>L'<strong>art. 1385 c.c.</strong> disciplina la <strong>caparra confirmatoria</strong>: versata all'accettazione, vincola entrambe le parti — chi recede perdendo la caparra o restituendo il doppio. Distinta dall'acconto (art. 1376 c.c.). Approfondimento: <a href=\"blog-caparra-confirmatoria-padova\">caparra confirmatoria Padova</a>.</p>

<table>
<thead><tr><th>Istituto</th><th>Articolo c.c.</th><th>Effetto</th><th>Momento</th></tr></thead>
<tbody>
<tr><td>Proposta vincolante</td><td>1326</td><td>Obbliga proponente fino a termine</td><td>Prima dell'accettazione</td></tr>
<tr><td>Accettazione</td><td>1326</td><td>Perfeziona accordo preliminare</td><td>Entro termine proposta</td></tr>
<tr><td>Caparra confirmatoria</td><td>1385</td><td>Vincola entrambe le parti</td><td>Dopo accettazione</td></tr>
<tr><td>Condizione sospensiva</td><td>1353-1354</td><td>Mutuo, permessi — effetto sospeso</td><td>In proposta/compromesso</td></tr>
</tbody>
</table>

<h2 id="elementi">Elementi essenziali della proposta scritta</h2>
<p>Una proposta efficace include: <strong>identificazione immobile</strong> (indirizzo, dati catastali foglio/particella/subalterno), <strong>prezzo offerto</strong>, <strong>modalità pagamento</strong> (caparra, saldo rogito), <strong>termine accettazione</strong>, <strong>condizioni sospensive</strong> (mutuo, perizia), <strong>data indicativa rogito</strong>, dati acquirente e venditore.</p>
<p>Clausole su <strong>conformità urbanistica</strong>, <strong>spese condominiali</strong> e <strong>stato di fatto</strong> tutelano l'acquirente prudente. Incrociare con <a href=\"blog-checklist-verifiche-prima-compromesso-padova-2026\">checklist pre-compromesso</a>.</p>

{svg_proposta_elementi()}

<h2 id="negoziazione">Negoziazione prezzo nel mercato padovano</h2>
<p>Il prezzo in annuncio è <em>dichiarazione</em> del venditore — punto di partenza. L'<em>analisi</em> usa <a href=\"{OMI_URL}\" target=\"_blank\" rel=\"noopener noreferrer\">OMI ADE</a> (fasce min-med-max per zona e tipologia), comparabili recenti e stato manutentivo. Non pubblicare percentuali di sconto medie inventate: ogni trattativa è singola.</p>
<p>A Padova, immobili in zone con domanda &gt; offerta (certi trilocali Limena, bilocali Arcella) ricevono più proposte — completezza e solidità finanziaria pesano quanto il prezzo. Controproposta del venditore apre nuova tornata negoziale.</p>

{blog_fig("img/blog/blog-proposta-acquisto-negoziazione-padova-percorso.webp", "Percorso vendita e proposta acquirente — documenti compravendita Padova 2026")}

<h2 id="mutuo">Condizione sospensiva mutuo: prassi ordinata</h2>
<p>La maggior parte degli acquirenti padovani finanzia con mutuo. La <strong>condizione sospensiva</strong> subordinat l'efficacia dell'accordo all'ottenimento del finanziamento entro termine e importo indicati — tutela civilistica standard.</p>
<p>Presentare <strong>pre-approvazione bancaria</strong> o lettera del broker con la proposta rafforza la credibilità. Servizio: <a href=\"servizio-mutuo\">mutuo Righetto</a>. Contesto tassi: <a href=\"blog-tassi-euribor-mutui-padova-agosto-2026\">Euribor mutui Padova</a>. Perizia bancaria può essere inferiore al prezzo concordato — clausola su esito perizia prudente.</p>

<table>
<thead><tr><th>Elemento proposta</th><th>Perché conta</th><th>Errore frequente</th></tr></thead>
<tbody>
<tr><td>Pre-approvazione mutuo</td><td>Credibilità acquirente</td><td>Offerta senza qualifica banca</td></tr>
<tr><td>Condizione sospensiva</td><td>Tutela se mutuo negato</td><td>Proposta senza clausola</td></tr>
<tr><td>Importo caparra</td><td>Impegno concreto</td><td>Caparra simbolica su immobile richiesto</td></tr>
<tr><td>Termine accettazione</td><td>Urgenza negoziale</td><td>Termine troppo lungo in mercato competitivo</td></tr>
</tbody>
</table>

<h2 id="termini">Termini di accettazione e controproposta</h2>
<p>Il <strong>termine per l'accettazione</strong> crea urgenza e certezza giuridica. In mercato competitivo padovano, 48-72 ore non è insolito su immobili con più visite. Scaduto il termine senza risposta, la proposta si estingue (salvo proroga scritta).</p>
<p>La <strong>controproposta</strong> del venditore (prezzo diverso, termini diversi) costituisce nuova proposta — l'acquirente decide se accettare. Non esiste accettazione tacita per immobili di valore rilevante: serve risposta espressa.</p>

{blog_fig("img/blog/blog-proposta-acquisto-negoziazione-padova-agenzia.webp", "Mediazione immobiliare e proposta d'acquisto — servizi agenzia Padova")}

<h2 id="competitivo">Proposta in mercato competitivo: Padova e cintura</h2>
<p>Quando più acquirenti convergono sullo stesso immobile, il venditore confronta: prezzo, caparra, tempi rogito, solidità mutuo, assenza condizioni eccessive. Proposta «pulita» con condizione mutuo standard e data rogito fattibile spesso preferita a offerta più alta ma incerta.</p>
<p>Contesto aggregato: <a href=\"{ADE_OSSERVATORIO}\" target=\"_blank\" rel=\"noopener noreferrer\">Osservatorio ADE</a>, <a href=\"{ISTAT_URL}\">ISTAT</a>. Per singola trattativa: documenti e visita — vedi <a href=\"blog-percorso-vendita-immobile-padova-2026\">percorso vendita</a> dal lato venditore.</p>

<h2 id="agenzia">Ruolo dell'agenzia nella negoziazione</h2>
<p>L'agenzia immobiliare media tra acquirente e venditore: consegna proposta scritta, raccoglie controproposta, coordina tempistiche caparra e compromesso. Il <strong>compenso di mediazione</strong> si concorda in sede — Righetto non pubblica listini percentuali online.</p>
<p>Trasparenza documentale prima della proposta: visura, planimetria, APE, spese condominiali — allineato a <a href=\"blog-mandato-esclusivo-padova-perche-conviene-2026\">mandato esclusivo</a> lato vendita e <a href=\"blog-5-domande-appuntamento-agenzia-padova-2026\">5 domande agenzia</a> lato acquirente.</p>

<h2 id="errori">Errori comuni in proposta e negoziazione</h2>
<ul>
<li>Proposta verbale senza conferma scritta — rischio incomprensioni.</li>
<li>Offerta senza pre-approvazione mutuo su immobile finanziato.</li>
<li>Termine accettazione assente su proposta intesa vincolante.</li>
<li>Ignorare delibere condominiali straordinarie nel prezzo offerto.</li>
<li>Chiedere sconto aggressivo in prima visita senza conviction (vedi <a href=\"blog-5-errori-visita-immobile-padova-2026\">5 errori visita</a>).</li>
<li>Firmare proposta senza leggere clausola caparra e recesso.</li>
</ul>

{blog_fig("img/blog/blog-proposta-acquisto-negoziazione-padova-visita.webp", "Visita immobile e preparazione proposta — scelta immobile giusto Padova")}

<h2 id="caparra">Dal sì alla caparra confirmatoria</h2>
<p>Accettata la proposta, le parti procedono al <strong>versamento caparra confirmatoria</strong> — importo concordato, pagamento tracciato, ricevuta. Poi compromesso registrato o rogito diretto secondo prassi concordata con notaio.</p>
<p>Se mutuo condizionato: erogazione dopo perizia favorevole. Documenti successivi: <a href=\"blog-documenti-compravendita-rogito-padova-2026\">documenti compravendita</a>, <a href=\"blog-quattro-imposte-rogitio-prima-casa-padova-2026\">imposte rogito prima casa</a>.</p>

<h2 id="limena">Proposta d'acquisto a Limena e hinterland</h2>
<p><strong>Limena</strong> e comuni cintura (Vigonza, Rubano) vedono trilocali richiesti da famiglie pendolari. Proposta con caparra, mutuo qualificato e termini rogito chiari accelera scelta del venditore. Confrontare microzone OMI — Limena ≠ centro Padova.</p>
<p>Righetto in Via Roma 96 coordina proposte su Padova e 101 comuni dal 2000. Pagina <a href=\"zona-limena\">zona Limena</a>, <a href=\"blog-appartamento-limena-guida-acquisto-2026\">guida acquisto Limena</a>, <a href=\"blog-dieci-errori-acquisto-casa-padova-2026\">dieci errori acquisto</a>.</p>

<h2 id="domande">Domande frequenti su proposta e negoziazione</h2>
<p>La proposta può essere revocata prima dell'accettazione se non contiene clausola di irrevocabilità oltre il termine — verificare con consulente prima di firmare. In mercato con più offerenti, il venditore non è obbligato ad accettare la proposta più alta se preferisce condizioni più solide su mutuo e rogito.</p>
<p>Acquirenti under 36 con garanzia CONSAP beneficiano della stessa struttura proposta, con condizione sospensiva mutuo che include l'erogazione garantita — tempistiche da allineare con banca e venditore. Evitare proposte copia-incolla da modelli online senza adattare identificativi catastali e clausole specifiche dell'immobile padovano scelto.</p>
<p>La proposta può prevedere facoltà per il venditore di accettare entro termine anche con riserva su data rogito — chiarezza su calendario notaio evita contenziosi. Per immobili con usufrutto o nuda proprietà, la proposta deve indicare chi firma e con quali poteri — situazione non rara in successioni padovane.</p>
<p>Documentare per iscritto ogni controproposta: email o PDF firmato evita dispute su quale importo fosse effettivamente concordato. In trattativa Limena-Padova, indicare disponibilità visite tecniche aggiuntive rafforza fiducia del venditore senza obbligare a sconto immediato sul prezzo richiesto.</p>
<p>Per box auto o cantina con subalterno catastale separato, la proposta deve elencare tutte le unità incluse nel prezzo — errore frequente su trilocali padovani con pertinenze non menzionate in annuncio. Allegare identità e codice fiscale acquirente evita ritardi quando il venditore accetta e deve preparare documentazione notarile.</p>

<p>{CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 29 agosto 2026. Fonti: Codice Civile artt. 1326, 1330, 1353-1354, 1385, OMI ADE.</p>
"""


ARTICLES = [
    {
        "slug": "blog-spese-condominiali-acquisto-padova-2026",
        "filename": "blog-spese-condominiali-acquisto-padova-2026.html",
        "hero": "img/blog/blog-spese-condominiali-acquisto-padova-2026-hero.webp",
        "title": "Spese condominiali acquisto Padova 2026",
        "og_title": "Spese condominiali acquisto casa Padova: guida",
        "meta": "Spese condominiali nell'acquisto casa a Padova: regolamento, millesimi, delibere, saldo venditore. Guida due diligence Codice Civile art. 1117-1139.",
        "schema_headline": "Spese condominiali nell'acquisto casa a Padova: guida 2026",
        "section": "Acquisto casa",
        "cat_badge": "Condominio · Evergreen",
        "bread_crumb": "Spese condominiali acquisto",
        "h1": "<strong>Spese condominiali</strong> acquisto casa Padova",
        "hero_alt": "Spese condominiali acquisto casa Padova — due diligence e documenti 2026",
        "body_fn": lambda: expand_body(body_spese_condominiali, EXPANSION_CONDOMINIO),
        "faqs": [
            ("Quando verificare spese condominiali?", "Prima della proposta o caparra — regolamento, verbali e saldo venditore."),
            ("Cosa chiedere all'amministratore?", "Ultimi verbali, bilancio, tabella millesimale, attestazione saldo spese venditore."),
            ("Delibere straordinarie: rischio?", "Sì — lavori deliberati vincolano anche il nuovo proprietario per quote future."),
            ("Differenza da gestione spese casa?", "Quel articolo tratta possesso post-rogito; qui due diligence condominio in acquisto."),
            ("Millesimi: cosa sono?", "Quote di ripartizione spese — art. 1123 c.c., tabella millesimale obbligatoria."),
            ("Vale a Limena?", "Sì — stesse regole Codice Civile; verificare delibere anche su condomini recenti."),
            ("Righetto chiede documenti condominiali?", "Sì in percorso acquisto ordinato — prima della proposta scritta."),
        ],
        "related": [
            ("Checklist compromesso", "blog-checklist-verifiche-prima-compromesso-padova-2026"),
            ("Dieci errori acquisto", "blog-dieci-errori-acquisto-casa-padova-2026"),
            ("Documenti rogito", "blog-documenti-compravendita-rogito-padova-2026"),
            ("Acquisto Limena", "blog-appartamento-limena-guida-acquisto-2026"),
            ("Servizio mutuo", "servizio-mutuo"),
        ],
        "registry": {
            "titolo": "Spese condominiali acquisto Padova 2026",
            "categoria": "Acquisto casa",
            "tempo": 14,
            "contenuto": "Spese condominiali acquisto Padova: millesimi, delibere, saldo venditore.",
            "evidenza": False,
            "emoji": "🏢",
            "admin_contenuto": "<p>Guida spese condominiali in fase acquisto — due diligence Codice Civile Padova.</p>",
        },
        "static_map_key": "spese condominiali acquisto padova 2026",
        "editorial_id": "eq-ago29-001",
    },
    {
        "slug": "blog-proposta-acquisto-negoziazione-padova-2026",
        "filename": "blog-proposta-acquisto-negoziazione-padova-2026.html",
        "hero": "img/blog/blog-proposta-acquisto-negoziazione-padova-2026-hero.webp",
        "title": "Proposta acquisto casa Padova 2026",
        "og_title": "Proposta d'acquisto Padova: negoziazione guida",
        "meta": "Proposta d'acquisto casa a Padova: negoziazione, condizione mutuo, caparra confirmatoria art. 1385 c.c. Guida evergreen acquirenti 2026.",
        "schema_headline": "Proposta d'acquisto e negoziazione a Padova: guida 2026",
        "section": "Acquisto casa",
        "cat_badge": "Proposta · Evergreen",
        "bread_crumb": "Proposta acquisto Padova",
        "h1": "<strong>Proposta d'acquisto</strong> casa Padova 2026",
        "hero_alt": "Proposta d'acquisto immobile Padova — negoziazione e caparra 2026",
        "body_fn": lambda: expand_body(body_proposta_acquisto, EXPANSION_PROPOSTA),
        "faqs": [
            ("Cos'è la proposta d'acquisto?", "Offerta scritta con prezzo, termini e condizioni — se accettata vincola le parti."),
            ("Proposta vincolante?", "Sì se contiene termine accettazione — art. 1326 c.c. obbliga proponente fino a scadenza."),
            ("Caparra o acconto?", "Caparra confirmatoria (art. 1385) vincola entrambe; acconto ha tutela diversa."),
            ("Serve condizione mutuo?", "Consigliata — subordina efficacia a erogazione finanziamento entro termini."),
            ("Differenza da articolo caparra?", "Caparra approfondisce istituto; qui percorso negoziazione completo."),
            ("Quanto termine accettazione?", "Negoziabile — in mercato competitivo termini brevi favoriscono venditore."),
            ("Righetto coordina proposte?", "Sì — mediazione con proposta scritta; compenso concordato in sede."),
        ],
        "related": [
            ("Caparra confirmatoria", "blog-caparra-confirmatoria-padova"),
            ("Percorso vendita", "blog-percorso-vendita-immobile-padova-2026"),
            ("5 errori visita", "blog-5-errori-visita-immobile-padova-2026"),
            ("Servizio mutuo", "servizio-mutuo"),
            ("Consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
        ],
        "registry": {
            "titolo": "Proposta acquisto Padova: Negoziazione 2026",
            "categoria": "Acquisto casa",
            "tempo": 13,
            "contenuto": "Proposta d'acquisto Padova: negoziazione, mutuo, caparra confirmatoria.",
            "evidenza": False,
            "emoji": "📝",
            "admin_contenuto": "<p>Guida proposta d'acquisto e negoziazione immobiliare Padova 2026.</p>",
        },
        "static_map_key": "proposta acquisto negoziazione padova 2026",
        "editorial_id": "eq-ago29-002",
    },
]


EDITORIAL_ITEMS = [
    {
        "id": "eq-ago29-001",
        "status": "published",
        "priority": 5,
        "target_week": "2026-08-29",
        "published_date": DATE_ISO,
        "slug": "blog-spese-condominiali-acquisto-padova-2026",
        "kw_primaria": "spese condominiali acquisto casa padova",
        "intent": "acquisto-due-diligence",
        "title": "Spese condominiali nell'acquisto casa a Padova: guida due diligence 2026",
        "cluster": "acquisto-primo-casa",
        "substantive_area": "ACQUISTO_PRIMO_CASA",
        "main_question": "Quali spese condominiali verificare prima di comprare casa a Padova?",
        "reader_novelty": "Pillar dedicato alla due diligence condominio in acquisto — distinto dalla gestione spese post-rogito.",
        "editorial_type": "evergreen",
        "monitoring_area": "normativa",
        "different_from": "blog-gestione-spese-casa-padova-2026",
        "research_refs": [CODICE_CIVILE_CONDO, OMI_URL],
        "hype_sources_read": [GU_URL, ADE_OSSERVATORIO, ISTAT_URL],
        "gap_analysis": "Gestione spese casa copre possesso; manca guida condominio in fase acquisto con art. 1117-1139.",
        "value_add": "Checklist documenti condominiali, millesimi, delibere straordinarie e integrazione budget mutuo Padova/Limena.",
    },
    {
        "id": "eq-ago29-002",
        "status": "published",
        "priority": 6,
        "target_week": "2026-08-29",
        "published_date": DATE_ISO,
        "slug": "blog-proposta-acquisto-negoziazione-padova-2026",
        "kw_primaria": "proposta acquisto casa padova",
        "intent": "acquisto-negoziazione",
        "title": "Proposta d'acquisto a Padova: negoziazione e caparra 2026",
        "cluster": "vendita-processo",
        "substantive_area": "VENDITA_PROCESSO",
        "main_question": "Come presentare una proposta d'acquisto efficace a Padova nel 2026?",
        "reader_novelty": "Percorso negoziazione completo acquirente — oltre al singolo istituto caparra confirmatoria.",
        "editorial_type": "evergreen",
        "monitoring_area": "mercato",
        "different_from": "blog-caparra-confirmatoria-padova",
        "research_refs": [NORMATTIVA_CC, OMI_URL],
        "hype_sources_read": [BANCA_ITALIA, ADE_OSSERVATORIO, ISTAT_URL],
        "gap_analysis": "Caparra e percorso vendita esistono; gap su proposta scritta, termini e negoziazione competitiva Padova.",
        "value_add": "Elementi proposta, condizione mutuo, mercato competitivo e collegamento caparra-compromesso senza percentuali inventate.",
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

    print("\n-- Riepilogo batch condominio/proposta ago29 2026 --")
    for r in results:
        print(f"  • {r['file']} ({r['words']} parole)")
    print("  • blog.html, admin.html, sitemap.xml, homepage.js, editorial-queue.json")


if __name__ == "__main__":
    main()
