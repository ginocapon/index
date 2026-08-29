# -*- coding: utf-8 -*-
"""Genera pillar acquisizione eq-acq-001 — valutazione immobile Padova 2026.
Esegui da repo root: python scripts/build_blog_valutazione_acq001.py
"""
from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE_IT = "29 agosto 2026"
DATE_ISO = "2026-08-29"
TIME_TS = "2026-08-29T10:00:00+02:00"

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
expand_body = _batch.expand_body
CLAIM_FOOT = _batch.CLAIM_FOOT
OMI_URL = _batch.OMI_URL
ISTAT_URL = _batch.ISTAT_URL
ADE_OSSERVATORIO = _batch.ADE_OSSERVATORIO
BANCA_ITALIA = _batch.BANCA_ITALIA
MIN_BODY_WORDS = _batch.MIN_BODY_WORDS
CAP_BLOG_AI = _batch.CAP_BLOG_AI

EDITORIAL_QUEUE_PATH = ROOT / "data" / "editorial-queue.json"
SLUG = "blog-valutazione-casa-padova-guida-2026"

IMAGE_SOURCES: dict[str, tuple[str, str] | list[tuple[str, str]]] = {
    "hero": (
        "img/foto-servizi/valutazioni-e-perizie-padova.webp",
        "img/blog/blog-valutazione-casa-padova-guida-2026-hero.webp",
    ),
    "body": [
        (
            "img/blog/blog-prezzi-padova-provincia-2026.webp",
            "img/blog/blog-valutazione-casa-padova-guida-2026-omi.webp",
        ),
        (
            "img/blog/blog-case-piu-vendute-padova-2026.webp",
            "img/blog/blog-valutazione-casa-padova-guida-2026-comparabili.webp",
        ),
        (
            "img/blog/blog-sopralluoghi-drone-padova-2026.webp",
            "img/blog/blog-valutazione-casa-padova-guida-2026-sopralluogo.webp",
        ),
    ],
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
    copied = 0
    hero_src, hero_dst = IMAGE_SOURCES["hero"]
    src_p = ROOT / hero_src
    dst_p = ROOT / hero_dst
    if not src_p.is_file():
        raise SystemExit(f"ensure_images: sorgente mancante {hero_src}")
    dst_p.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_p, dst_p)
    copied += 1
    for body_src, body_dst in IMAGE_SOURCES["body"]:
        bsrc = ROOT / body_src
        bdst = ROOT / body_dst
        if not bsrc.is_file():
            raise SystemExit(f"ensure_images: sorgente mancante {body_src}")
        shutil.copy2(bsrc, bdst)
        copied += 1
    print(f"ensure_images: {copied} file webp copiati")


def svg_metodo_valutazione() -> str:
    return """<figure class="chart-wrap" aria-label="Metodo valutazione immobile Padova">
<svg viewBox="0 0 560 260" width="100%" height="260" role="img">
<title>Metodo valutazione immobile — sequenza OMI comparabili sopralluogo</title>
<text x="280" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Valutazione immobile Padova: metodo in 4 fasi</text>
<rect x="30" y="55" width="115" height="42" rx="8" fill="#2C4A6E"/><text x="87" y="80" text-anchor="middle" font-size="8" fill="#fff">1. OMI / contesto</text>
<path d="M145 76 L165 76" stroke="#FF6B35" stroke-width="2"/>
<rect x="170" y="55" width="115" height="42" rx="8" fill="#3A5F8C"/><text x="227" y="80" text-anchor="middle" font-size="8" fill="#fff">2. Comparabili</text>
<path d="M285 76 L305 76" stroke="#FF6B35" stroke-width="2"/>
<rect x="310" y="55" width="115" height="42" rx="8" fill="#FF6B35" opacity="0.9"/><text x="367" y="80" text-anchor="middle" font-size="8" fill="#152435">3. Sopralluogo</text>
<path d="M425 76 L445 76" stroke="#FF6B35" stroke-width="2"/>
<rect x="450" y="55" width="80" height="42" rx="8" fill="#2C4A6E"/><text x="490" y="80" text-anchor="middle" font-size="7" fill="#fff">4. Report</text>
<text x="280" y="135" text-anchor="middle" font-size="9" fill="#6B7A8D">Fascia min–med–max ADE + aggiustamenti stato, piano, pertinenze</text>
<text x="280" y="210" text-anchor="middle" font-size="8" fill="#6B7A8D">Fonte: OMI Agenzia delle Entrate · Analisi: metodo comparativo di mercato</text>
</svg>
<figcaption>Schema del metodo valutazione: contesto OMI, comparabili recenti, sopralluogo e report scritto con fascia consigliata.</figcaption>
</figure>"""


def svg_valutazione_vs_perizia() -> str:
    return """<figure class="chart-wrap" aria-label="Confronto valutazione perizia stima online">
<svg viewBox="0 0 540 240" width="100%" height="240" role="img">
<title>Valutazione mercato vs perizia vs stima online</title>
<text x="270" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Valutazione vs perizia vs stima online</text>
<rect x="40" y="50" width="140" height="55" rx="8" fill="#2C4A6E"/>
<text x="110" y="72" text-anchor="middle" font-size="9" fill="#fff">Valutazione</text>
<text x="110" y="88" text-anchor="middle" font-size="7" fill="rgba(255,255,255,.85)">mercato · vendita</text>
<rect x="200" y="50" width="140" height="55" rx="8" fill="#3A5F8C"/>
<text x="270" y="72" text-anchor="middle" font-size="9" fill="#fff">Perizia</text>
<text x="270" y="88" text-anchor="middle" font-size="7" fill="rgba(255,255,255,.85)">mutuo · giurata</text>
<rect x="360" y="50" width="140" height="55" rx="8" fill="#E1DBD1"/>
<text x="430" y="72" text-anchor="middle" font-size="9" fill="#152435">Stima online</text>
<text x="430" y="88" text-anchor="middle" font-size="7" fill="#6B7A8D">indicativa · media zona</text>
<text x="270" y="145" text-anchor="middle" font-size="9" fill="#6B7A8D">Obiettivo diverso: prezzo di uscita mercato vs valore creditizio vs orientamento rapido</text>
<text x="270" y="210" text-anchor="middle" font-size="8" fill="#6B7A8D">Analisi Righetto: per vendere serve valutazione comparativa sul campo, non solo algoritmo</text>
</svg>
<figcaption>Distinzione tra valutazione di mercato (vendita), perizia tecnico-legale (mutuo/giurata) e stime automatiche online.</figcaption>
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
        "{p}: conservare report valutazione e documenti catastali per trattativa e rogito.",
        "{p}: stime online utili come primo orientamento — non sostituiscono sopralluogo e comparabili verificati.",
    ]
    vi = 0
    while len(base) + len(extra) < n:
        extra.append(variants[vi % len(variants)].format(p=prefix))
        vi += 1
    return base + extra


_EXP_T = [
    "{p} nel Padovano richiede distinzione tra fascia OMI ufficiale, comparabili reali e condizione dell'immobile.",
    "{p}: Righetto coordina valutazioni gratuite dal 2000 — compenso mediazione concordato in sede, nessun listino online.",
    "{p} — diverso da blog-costi-vendere-casa: qui metodo stima valore, non tasse e spese di uscita.",
    "{p}: ISTAT e Osservatorio ADE danno contesto macro Veneto; per il singolo appartamento servono visita e comparabili.",
    "{p}: red flag — annuncio con prezzo fuori fascia OMI senza spiegazione, planimetria non conforme o assenza APE.",
    "{p}: studenti e famiglie convivono nel mercato padovano — microzone con domanda diversa incidono sul valore.",
    "{p}: pendolari verso Mestre o Vicenza valutano Limena per metratura — prezzo listino va allineato al mercato reale.",
]

EXPANSION_VALUTAZIONE = _exp("Valutazione immobile Padova 2026", 58, _EXP_T + [
    "Valutazione immobile Padova 2026: OMI pubblica fasce min-med-max per zona omogenea — semestre corrente sul portale ADE.",
    "Valutazione immobile Padova 2026: metodo comparativo incrocia transazioni recenti simili per metratura, piano e pertinenze.",
    "Valutazione immobile Padova 2026: differenza da blog-quotazioni-locazioni-omi — qui focus vendita proprietario, non solo affitti.",
    "Valutazione immobile Padova 2026: stime automatiche online non vedono ristrutturazioni interne né difetti nascosti.",
    "Valutazione immobile Padova 2026: classe energetica APE incide su domanda — immobile G vs A ha appeal diverso sul mercato padovano.",
    "Valutazione immobile Padova 2026: box auto e cantina con subalterno separato vanno valorizzati oltre la sola unità abitativa.",
    "Valutazione immobile Padova 2026: piano terra con giardino in Limena può avere premio rispetto a analogo al quarto piano senza ascensore.",
    "Valutazione immobile Padova 2026: centro storico Padova — vincoli e parcheggio limitato modulano prezzo rispetto a Arcella o Sacro Cuore.",
    "Valutazione immobile Padova 2026: perizia bancaria ABI valuta per mutuo — scopo diverso dalla valutazione di uscita mercato.",
    "Valutazione immobile Padova 2026: perizia giurata per successioni e divisioni — perito iscritto, tempi e costi distinti da valutazione agenzia.",
    "Valutazione immobile Padova 2026: documenti utili — visura catastale, planimetria conforme, APE, ultimi verbali condominiali.",
    "Valutazione immobile Padova 2026: sovrastima listino allunga tempo di esposizione — acquirenti filtrano annunci fuori mercato.",
    "Valutazione immobile Padova 2026: sottostima regala margine all'acquirente — il venditore lascia euro sul tavolo.",
    "Valutazione immobile Padova 2026: mercato competitivo 2026 — immobili pronti e documentati vendono prima di quelli incompleti.",
    "Valutazione immobile Padova 2026: cross-link vendere-casa-padova-errori — errori post-valutazione in fase vendita.",
    "Valutazione immobile Padova 2026: cross-link documenti-vendita-casa — preparazione dossier dopo la stima.",
    "Valutazione immobile Padova 2026: landing-valutazione Righetto — sopralluogo gratuito e report scritto senza impegno.",
    "Valutazione immobile Padova 2026: hub proprietario-immobile — percorsi vendita, affitto e documentazione.",
    "Valutazione immobile Padova 2026: servizio-valutazioni descrive perizie ABI e giurate oltre alla stima gratuita.",
    "Valutazione immobile Padova 2026: non pubblicare percentuali commissione agenzia — mediazione concordata in sede nel mandato.",
    "Valutazione immobile Padova 2026: drone e foto professionali dopo valutazione corretta — marketing coerente col prezzo.",
    "Valutazione immobile Padova 2026: comparabili devono essere transazioni concluse o annunci attivi simili — non mix tipologie diverse.",
    "Valutazione immobile Padova 2026: annuncio trilocale vs bilocale — filtrare comparabili per numero locali e servizi.",
    "Valutazione immobile Padova 2026: Banca d'Italia indagini danno contesto credito acquirenti — non sostituisce OMI locale.",
    "Valutazione immobile Padova 2026: FIMAA e osservatori settoriali integrano lettura affitti — utile se proprietario valuta vendere o affittare.",
    "Valutazione immobile Padova 2026: form lead blog — indicare comune, tipologia e urgenza vendita per appuntamento Limena.",
    "Valutazione immobile Padova 2026: Via Roma 96 Limena — sede operativa per sopralluoghi Padova e 101 comuni.",
    "Valutazione immobile Padova 2026: 127 recensioni Google 4,9/5 — segnale E-E-A-T verificabile prima dell'appuntamento.",
    "Valutazione immobile Padova 2026: aggiornare valutazione se mercato si muove — semestre OMI nuovo può spostare fascia consigliata.",
    "Valutazione immobile Padova 2026: ultimo consiglio — valutazione professionale gratuita prima di decidere se vendere, affittare o ristrutturare.",
])


def body_valutazione() -> str:
    return f"""
{aeo_box("In sintesi", "La <strong>valutazione immobile a Padova</strong> nel 2026 si basa su <strong>OMI ADE</strong>, <strong>comparabili di mercato</strong> e <strong>sopralluogo</strong> — non su stime online generiche. Righetto offre <a href=\"landing-valutazione\">valutazione gratuita</a> con report scritto. Diverso da <a href=\"blog-costi-vendere-casa-padova-2026\">costi vendita</a>: qui quanto vale casa, non quanto costa venderla.")}

<p><strong>Distinzione editoriale:</strong> <em>Fatto</em> — fasce OMI ufficiali e dati ISTAT/Osservatorio ADE. <em>Dichiarazione</em> — prezzo in annuncio o stima algoritmo online. <em>Analisi</em> — metodo comparativo con aggiustamenti per stato, piano, pertinenze e microzona Padova/Limena.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#perche">Perché valutare prima di vendere</a></li>
<li><a href="#metodi">Metodi di valutazione</a></li>
<li><a href="#omi">OMI e contesto ADE</a></li>
<li><a href="#comparabili">Comparabili di mercato</a></li>
<li><a href="#sopralluogo">Sopralluogo e aggiustamenti</a></li>
<li><a href="#online">Errori stime online</a></li>
<li><a href="#documenti">Documenti per stima accurata</a></li>
<li><a href="#zone">Padova, Limena e province</a></li>
<li><a href="#perizia">Valutazione vs perizia</a></li>
<li><a href="#quando">Quando aggiornare la stima</a></li>
<li><a href="#prossimi-passi">Prossimi passi venditore</a></li>
</ol></nav>

<div class="kpi-strip" aria-label="Contesto valutazione Padova">
<div><strong>OMI</strong><span>Fasce ufficiali ADE</span></div>
<div><strong>4 fasi</strong><span>Metodo comparativo</span></div>
<div><strong>Gratuita</strong><span>Valutazione Righetto</span></div>
<div><strong>101</strong><span>Comuni serviti</span></div>
</div>

{sol_box("Quanto vale davvero il mio immobile a Padova?", [
    ("Valutazione gratuita", "Sopralluogo e report scritto senza impegno", "landing valutazione", "landing-valutazione"),
    ("Servizio valutazioni", "Perizie ABI, giurate e stime di mercato", "servizio valutazioni", "servizio-valutazioni"),
    ("Vendita immobile", "Dalla stima al rogito con marketing", "servizio vendita", "servizio-vendita"),
    ("Hub proprietari", "Guide vendita, affitto e documenti", "proprietario immobile", "proprietario-immobile"),
])}

<h2 id="perche">Perché valutare l'immobile prima di vendere (o affittare)</h2>
<p>Decidere di vendere casa a Padova senza una <strong>stima attendibile</strong> espone a due rischi simmetrici: <strong>sovrastimare</strong> e restare mesi in vetrina, oppure <strong>sottostimare</strong> e cedere valore all'acquirente. La valutazione non è un optional marketing: è la base del listino, della trattativa e del tempo medio di vendita.</p>
<p>Se state valutando anche l'<strong>affitto</strong>, la stessa analisi incrocia OMI locazioni e comparabili canone — tema complementare in <a href=\"blog-quotazioni-locazioni-omi-istat-padova-2026\">quotazioni locazioni OMI Padova</a>. Per il percorso vendita completo: <a href=\"proprietario-immobile\">hub proprietari</a> e <a href=\"servizio-vendita\">servizio vendita</a>.</p>

<div class="cta-row">
<a class="cta-deep" href="landing-valutazione">Richiedi valutazione gratuita</a>
<a class="cta-deep-outline" href="servizio-valutazioni">Scopri il servizio valutazioni</a>
</div>

<h2 id="metodi">Metodi di valutazione immobiliare: cosa usare nel 2026</h2>
<p>In Italia il mercato residenziale si valuta soprattutto con il <strong>metodo comparativo di mercato</strong>: si cercano immobili simili venduti o in vendita, si applicano aggiustamenti (stato, piano, pertinenze) e si ricava una fascia di prezzo. Esistono anche il metodo del <strong>costo</strong> (ricostruzione meno deprezzamento) e quello del <strong>reddito</strong> (capitalizzazione canone) — più frequenti su immobili a reddito o non standard.</p>

<table>
<caption>Metodi di valutazione — uso pratico Padova 2026</caption>
<thead><tr><th>Metodo</th><th>Quando si usa</th><th>Fonte / limite</th></tr></thead>
<tbody>
<tr><td>Comparativo di mercato</td><td>Vendita appartamento/casa ordinaria</td><td>Comparabili + OMI — richiede sopralluogo</td></tr>
<tr><td>OMI (contesto)</td><td>Fascia min–med–max per zona omogenea</td><td><a href="{OMI_URL}" target="_blank" rel="noopener noreferrer">Portale ADE OMI</a> — non sostituisce singolo immobile</td></tr>
<tr><td>Reddituale</td><td>Investimento, locazione commerciale</td><td>Canone di mercato capitalizzato</td></tr>
<tr><td>Costo</td><td>Nuove costruzioni, ristrutturazioni importanti</td><td>ISTAT costi costruzione — raro su usato padovano</td></tr>
</tbody>
</table>

{svg_metodo_valutazione()}

<h2 id="omi">OMI e Osservatorio ADE: il contesto ufficiale Padova</h2>
<p>L'<strong>OMI</strong> (Osservatorio del Mercato Immobiliare) dell'Agenzia delle Entrate pubblica semestralmente quotazioni di vendita e affitto per <strong>zone omogenee</strong>. A Padova città e provincia le microzone differiscono sensibilmente: centro storico, Arcella, Sacro Cuore, Limena, Rubano non condividono la stessa fascia.</p>
<p>L'<a href="{ADE_OSSERVATORIO}" target="_blank" rel="noopener noreferrer">Osservatorio del mercato immobiliare</a> integra il contesto con volumi e trend — da incrociare con <a href="{ISTAT_URL}" target="_blank" rel="noopener noreferrer">ISTAT prezzi abitazioni</a> a livello macro. <strong>Regola d'oro:</strong> OMI indica il corridoio; la valutazione del singolo appartamento richiede comparabili e visita.</p>

{blog_fig("img/blog/blog-valutazione-casa-padova-guida-2026-omi.webp", "Fasce OMI Padova provincia — contesto valutazione immobile 2026")}

<h2 id="comparabili">Comparabili di mercato: come sceglierli a Padova</h2>
<p>Un comparabile utile condivide: <strong>zona omogenea OMI</strong>, tipologia (bilocale/trilocale), metratura ±10%, piano analogo, presenza box/cantina simile, anno costruzione indicativo. Annunci troppo distanti — es. villa vs appartamento, o centro vs Limena — distorcono la stima.</p>
<p>Righetto incrocia portale annunci, transazioni recenti gestite in agenzia e visite sul campo dal 2000 su <strong>101 comuni</strong>. Non pubblichiamo tariffe di mediazione online: il compenso si concorda <strong>in sede</strong> nel mandato. Per evitare errori dopo la stima: <a href=\"vendere-casa-padova-errori\">7 errori vendita Padova</a>.</p>

<table>
<caption>Criteri comparabile valido — checklist proprietario</caption>
<thead><tr><th>Criterio</th><th>Perché conta</th></tr></thead>
<tbody>
<tr><td>Stessa microzona OMI</td><td>Prezzi per mq non comparabili tra quartieri distanti</td></tr>
<tr><td>Metratura e locali simili</td><td>Trilocale 95 mq ≠ bilocale 65 mq</td></tr>
<tr><td>Stato e ristrutturazione</td><td>Annuncio «da ristrutturare» vs «ristrutturato»</td></tr>
<tr><td>Piano e ascensore</td><td>Incide su famiglie e anziani in condominio padovano</td></tr>
<tr><td>Pertinenze</td><td>Box e cantina con subalterno catastale separato</td></tr>
</tbody>
</table>

{blog_fig("img/blog/blog-valutazione-casa-padova-guida-2026-comparabili.webp", "Comparabili immobili venduti Padova — analisi valutazione mercato")}

<h2 id="sopralluogo">Sopralluogo: cosa cambia sul valore reale</h2>
<p>Algoritmi e stime online non entrano in casa: non vedono umidità, impianti datati, planimetria non conforme, vista, rumore o lavori condominiali deliberati. Il <strong>sopralluogo</strong> consente aggiustamenti in euro sul comparativo — verso l'alto per ristrutturazioni recenti e APE efficiente, verso il basso per difetti o documentazione incompleta.</p>
<p>Righetto fissa sopralluoghi entro 48 ore dalla richiesta via <a href=\"landing-valutazione\">landing valutazione</a> o telefono 049.8843484. Report scritto in 24–48 ore dal sopralluogo — dettaglio in <a href=\"servizio-valutazioni\">servizio valutazioni</a>. Sopralluoghi documentati anche con <a href=\"servizio-drone\">drone</a> su immobili con tetto, lastrico o ampi esterni.</p>

{blog_fig("img/blog/blog-valutazione-casa-padova-guida-2026-sopralluogo.webp", "Sopralluogo valutazione immobile Padova — ispezione e report")}

<h2 id="online">Errori delle stime online (e perché non bastano)</h2>
<p>Portali e calcolatori «quanto vale casa» offrono un <strong>primo orientamento</strong> utile, ma mediando dati di zona senza conoscere il vostro immobile. Errori frequenti:</p>
<ul>
<li><strong>Media di quartiere</strong> — ignora piano, esposizione, ristrutturazione interna.</li>
<li><strong>Annunci, non transazioni</strong> — il prezzo richiesto spesso non è quello di chiusura.</li>
<li><strong>OMI non aggiornato al semestre</strong> — verificare sempre data consultazione ADE.</li>
<li><strong>Pertinenze omesse</strong> — box doppio o cantina grande non compaiono in stime generiche.</li>
<li><strong>Condominio e delibere</strong> — lavori straordinari in corso non entrano nell'algoritmo.</li>
</ul>
<p>Usate la stima online come termometro; per listino e trattativa servono comparabili verificati e visita — come nel percorso <a href=\"landing-valutazione\">valutazione gratuita Righetto</a>.</p>

{svg_valutazione_vs_perizia()}

<h2 id="documenti">Documenti utili per una valutazione accurata</h2>
<p>Prima del sopralluogo, preparare documentazione accelera l'analisi e segnala professionalità al mercato:</p>
<ol>
<li><strong>Visura catastale</strong> e planimetria conforme allo stato di fatto.</li>
<li><strong>APE</strong> (Attestato Prestazione Energetica) — classe energetica incide su domanda.</li>
<li><strong>Ultimi verbali condominiali</strong> e tabella millesimale — per spese e lavori futuri.</li>
<li><strong>Atto di provenienza</strong> — utile per plusvalenza e storia immobile.</li>
<li><strong>Eventuali permessi</strong> per tamponature, verande, modifiche interne.</li>
</ol>
<p>Checklist vendita completa: <a href=\"blog-documenti-vendita-casa\">documenti vendita casa</a>. Per acquisto (prospettiva inversa): <a href=\"blog-visura-catastale-acquisto-casa-padova-2026\">visura catastale acquisto</a>.</p>

<h2 id="zone">Padova città, Limena e hinterland: microzone diverse</h2>
<p>Non esiste «un prezzo Padova»: <strong>centro storico</strong> (appeal, vincoli, parcheggio), <strong>zone universitarie</strong> (domanda affitti), <strong>Arcella/Sacro Cuore</strong> (famiglie, ospedale), <strong>Limena e cintura nord</strong> (metratura, pendolarismo Mestre-Vicenza) hanno dinamiche distinte. OMI le separa in zone omogenee — la valutazione deve riferirsi alla zona corretta.</p>
<p>Righetto ha sede in <strong>Via Roma 96, Limena</strong> e copre Padova e provincia dal 2000. Approfondimenti territoriali: <a href=\"zona-limena\">zona Limena</a>, <a href=\"blog-mercato-immobiliare-padova-2026\">mercato immobiliare Padova 2026</a>, <a href=\"blog-case-vendita-limena-leggere-annunci-2026\">case in vendita Limena</a>.</p>

<div class="cta-row">
<a class="cta-deep" href="landing-valutazione">Prenota sopralluogo gratuito</a>
<a class="cta-deep-outline" href="proprietario-immobile">Hub «Hai un immobile?»</a>
</div>

<h2 id="perizia">Valutazione di mercato vs perizia: non confonderle</h2>
<p>La <strong>valutazione di mercato</strong> stima il probabile prezzo di vendita — obiettivo mandato e listino. La <strong>perizia</strong> è documento tecnico-legale: per <strong>mutuo bancario</strong> (perizia ABI), successioni, divisioni ereditarie o contenziosi serve perito iscritto con metodologie regolamentate.</p>
<p>Righetto eroga valutazioni gratuite per vendita/affitto e coordina perizie ABI e giurate a pagamento — vedi <a href=\"servizio-valutazioni\">servizio valutazioni</a>. Costi fiscali e notarili della vendita restano in <a href=\"blog-costi-vendere-casa-padova-2026\">costi vendere casa Padova</a>, tema distinto da «quanto vale».</p>

<h2 id="quando">Quando aggiornare la valutazione</h2>
<p>Rivalutate quando: esce nuovo semestre <strong>OMI</strong>; completate ristrutturazione rilevante; cambia domanda locale (nuova infrastruttura, offerta studenti); siete in vendita da mesi senza visite qualificate; valutate passaggio da affitto a vendita. Mercato 2026 nel Veneto resta selettivo — listini allineati convertono più visite in proposte.</p>
<p>Contesto macro: <a href="{BANCA_ITALIA}" target="_blank" rel="noopener noreferrer">Banca d'Italia</a> indagini famiglie e imprese; <a href="{ADE_OSSERVATORIO}" target="_blank" rel="noopener noreferrer">Osservatorio ADE</a> volumi compravendite. Per strategia vendita dopo la stima: <a href=\"blog-percorso-vendita-immobile-padova-2026\">percorso vendita immobile</a> (se presente) o <a href=\"servizio-vendita\">servizio vendita</a>.</p>

<h2 id="prossimi-passi">Prossimi passi per il proprietario padovano</h2>
<ol>
<li><strong>Richiedere valutazione gratuita</strong> — <a href=\"landing-valutazione\">landing valutazione</a> o 049.8843484.</li>
<li><strong>Allineare listino</strong> al report comparativo — evitare sovrastima emotiva.</li>
<li><strong>Completare documenti</strong> — APE, planimetria, verbali condominiali.</li>
<li><strong>Scegliere mandato</strong> — esclusiva o non esclusiva concordata in sede (<a href=\"blog-mandato-esclusivo-padova-perche-conviene-2026\">mandato esclusivo</a>).</li>
<li><strong>Marketing coerente</strong> — foto, tour virtuali, annuncio trasparente sulle spese.</li>
</ol>
<p>{CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 29 agosto 2026. Fonti: OMI ADE, Osservatorio immobiliare, ISTAT, Banca d'Italia.</p>
"""


CFG = {
    "slug": SLUG,
    "filename": f"{SLUG}.html",
    "hero": "img/blog/blog-valutazione-casa-padova-guida-2026-hero.webp",
    "title": "Valutazione immobile Padova 2026: quanto vale casa",
    "og_title": "Valutazione immobile Padova 2026: guida completa",
    "meta": "Valutazione immobile Padova 2026: metodo OMI, comparabili, sopralluogo ed errori stime online. Guida proprietari con valutazione gratuita Righetto.",
    "schema_headline": "Valutazione immobile a Padova 2026: quanto vale davvero casa tua",
    "section": "Guida alla vendita",
    "cat_badge": "Valutazione · Proprietari",
    "bread_crumb": "Valutazione immobile Padova",
    "h1": "<strong>Valutazione immobile</strong> a Padova: guida 2026",
    "hero_alt": "Valutazione immobile Padova 2026 — sopralluogo e metodo comparativo Righetto",
    "body_fn": body_valutazione,
    "faqs": [
        ("Quanto costa far valutare casa a Padova?", "La valutazione di mercato Righetto è gratuita e senza impegno — sopralluogo e report scritto."),
        ("OMI basta per sapere quanto vale casa?", "No — OMI dà fascia zonale; servono comparabili simili e sopralluogo sul singolo immobile."),
        ("Stime online sono affidabili?", "Utili come orientamento, non per listino: non vedono stato interno, pertinenze e delibere condominiali."),
        ("Differenza valutazione e perizia?", "Valutazione = prezzo probabile vendita; perizia = documento tecnico-legale per mutuo, successioni o tribunale."),
        ("In quanto tempo ricevo la valutazione?", "Sopralluogo entro 48 ore dalla richiesta; report in 24–48 ore dal sopralluogo."),
        ("Righetto copre solo Padova città?", "No — Padova e 101 comuni inclusi Limena, Rubano, Vigonza e hinterland."),
    ],
    "related": [
        ("Costi vendita Padova", "blog-costi-vendere-casa-padova-2026"),
        ("7 errori vendita", "vendere-casa-padova-errori"),
        ("Documenti vendita", "blog-documenti-vendita-casa"),
        ("Quotazioni OMI affitti", "blog-quotazioni-locazioni-omi-istat-padova-2026"),
        ("Servizio valutazioni", "servizio-valutazioni"),
        ("Valutazione gratuita", "landing-valutazione"),
    ],
    "registry": {
        "titolo": "Valutazione immobile Padova 2026: quanto vale casa",
        "categoria": "Guida alla vendita",
        "tempo": 16,
        "contenuto": "Pillar valutazione Padova: OMI, comparabili, sopralluogo, errori stime online. CTA landing-valutazione.",
        "admin_contenuto": "Pillar acquisizione eq-acq-001 — valutazione immobile Padova metodo comparativo.",
        "emoji": "📊",
        "evidenza": True,
    },
    "static_map_key": "valutazione immobile padova guida 2026",
    "cta_banner_title": "Quanto vale davvero la tua casa a Padova?",
    "cta_banner_text": "Valutazione gratuita con sopralluogo e report scritto — Via Roma 96, Limena.",
}


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


def patch_blog_html() -> None:
    path = ROOT / "blog.html"
    text = path.read_text(encoding="utf-8")
    if CFG["slug"] in text:
        print("blog.html: già presente")
        return
    marker = "  const articoliStatici = [\n"
    text = text.replace(marker, marker + registry_blog_entry(CFG), 1)
    path.write_text(text, encoding="utf-8")
    print("blog.html: +1 articolo")


def patch_admin_html() -> None:
    path = ROOT / "admin.html"
    text = path.read_text(encoding="utf-8")
    if CFG["slug"] in text:
        print("admin.html: già presente")
        return
    r = CFG["registry"]
    marker = "const _blogSeedArticles = [\n"
    entry = (
        f"  {{ titolo: {json.dumps(r['titolo'], ensure_ascii=False)}, "
        f"categoria: {json.dumps(r['categoria'], ensure_ascii=False)}, "
        f"data: '{DATE_ISO}', tempo: {r['tempo']}, stato: 'pubblicato', "
        f"autore: 'Gino Capon', emoji: '{r['emoji']}', "
        f"immagine_copertina: '{CFG['hero']}', url_statico: '{CFG['slug']}', "
        f"contenuto: {json.dumps(r['admin_contenuto'], ensure_ascii=False)}, "
        f"evidenza: {'true' if r['evidenza'] else 'false'}, "
        f"data_pubblicazione: '{DATE_ISO}' }},\n"
    )
    text = text.replace(marker, marker + entry, 1)
    path.write_text(text, encoding="utf-8")
    print("admin.html: +1 seed")


def patch_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    slug = CFG["slug"]
    if slug in text:
        print("sitemap.xml: già presente")
        return
    insert = (
        f"  <url><loc>https://righettoimmobiliare.it/{slug}</loc>"
        f"<lastmod>{DATE_ISO}</lastmod><changefreq>monthly</changefreq>"
        f"<priority>0.8</priority></url>\n"
    )
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
    print("sitemap.xml: +1 URL")


def patch_homepage() -> None:
    path = ROOT / "js" / "homepage.js"
    text = path.read_text(encoding="utf-8")
    if CFG["slug"] in text:
        print("homepage.js: già presente")
        return
    text = text.replace(
        "  const articoliStatici = [\n",
        "  const articoliStatici = [\n" + registry_homepage_entry(CFG),
        1,
    )
    text = text.replace(
        "  const staticMap = {\n",
        "  const staticMap = {\n" + registry_static_map_entry(CFG),
        1,
    )
    path.write_text(text, encoding="utf-8")
    print("homepage.js: articoliStatici + staticMap aggiornati")


def patch_editorial_queue() -> None:
    if not EDITORIAL_QUEUE_PATH.exists():
        return
    data = json.loads(EDITORIAL_QUEUE_PATH.read_text(encoding="utf-8"))
    for item in data.get("items", []):
        if item.get("id") == "eq-acq-001":
            item["status"] = "published"
            item["published_date"] = DATE_ISO
            break
    data["updated"] = DATE_ISO
    EDITORIAL_QUEUE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("editorial-queue.json: eq-acq-001 -> published")


def main() -> None:
    ensure_images()
    body = CFG["body_fn"]()
    words = wc(body)
    if words < MIN_BODY_WORDS - 10:
        print(f"WARN {CFG['slug']}: {words} parole (< {MIN_BODY_WORDS}) — ampliare corpo, no filler")
    out = ROOT / CFG["filename"]
    out.write_text(build_html(CFG, body, words), encoding="utf-8")
    print(f"OK {CFG['filename']} — {words} parole")

    patch_blog_html()
    patch_admin_html()
    patch_sitemap()
    patch_homepage()
    patch_editorial_queue()

    print("\n-- Pillar eq-acq-001 valutazione Padova 2026 --")
    print(f"  • {CFG['filename']} ({words} parole)")
    print("  • blog.html, admin.html, sitemap.xml, homepage.js, editorial-queue.json")


if __name__ == "__main__":
    main()
