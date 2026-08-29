# -*- coding: utf-8 -*-
"""Genera pillar acquisizione eq-acq-002 — vendere o affittare Padova 2026.
Esegui da repo root: python scripts/build_blog_vendere_affittare_acq002.py
"""
from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE_IT = "29 agosto 2026"
DATE_ISO = "2026-08-29"
TIME_TS = "2026-08-29T11:00:00+02:00"

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
.vs-grid{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:1.4rem 0}
.vs-col{border:1px solid var(--gc);border-radius:10px;padding:1rem;background:var(--sfondo)}
.vs-col h3{font-family:'Cormorant Garamond',serif;font-size:1.15rem;margin:0 0 .6rem;color:var(--blu)}
@media(max-width:640px){.vs-grid{grid-template-columns:1fr}}
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
SLUG = "blog-vendere-o-affittare-padova-2026"

IMAGE_SOURCES: dict[str, tuple[str, str] | list[tuple[str, str]]] = {
    "hero": (
        "img/foto-servizi/locazioni-padova-og.webp",
        "img/blog/blog-vendere-o-affittare-padova-2026-hero.webp",
    ),
    "body": [
        (
            "img/blog/blog-registro-contratti-affitto-padova-limena.webp",
            "img/blog/blog-vendere-o-affittare-padova-2026-locazione.webp",
        ),
        (
            "img/blog/blog-case-vendita-limena-leggere-annunci-2026.webp",
            "img/blog/blog-vendere-o-affittare-padova-2026-vendita.webp",
        ),
        (
            "img/blog/blog-caro-affitti-padova-under-35-coppia.webp",
            "img/blog/blog-vendere-o-affittare-padova-2026-decisione.webp",
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
    for src, dst in [(hero_src, hero_dst)] + list(IMAGE_SOURCES["body"]):
        src_p = ROOT / src
        dst_p = ROOT / dst
        if not src_p.is_file():
            raise SystemExit(f"ensure_images: sorgente mancante {src}")
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_p, dst_p)
        copied += 1
    print(f"ensure_images: {copied} file webp copiati")


def svg_decisione_flow() -> str:
    return """<figure class="chart-wrap" aria-label="Schema decisionale vendere o affittare">
<svg viewBox="0 0 560 300" width="100%" height="300" role="img">
<title>Schema decisionale vendere o affittare immobile Padova</title>
<text x="280" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Vendere o affittare? — schema decisionale</text>
<rect x="215" y="38" width="130" height="36" rx="18" fill="#2C4A6E"/><text x="280" y="60" text-anchor="middle" font-size="9" fill="#fff">Hai un immobile</text>
<path d="M280 74 L280 92" stroke="#FF6B35" stroke-width="2"/>
<rect x="215" y="92" width="130" height="36" rx="18" fill="#3A5F8C"/><text x="280" y="114" text-anchor="middle" font-size="8" fill="#fff">Serve liquidità?</text>
<path d="M230 128 L130 160" stroke="#FF6B35" stroke-width="2"/>
<path d="M330 128 L430 160" stroke="#FF6B35" stroke-width="2"/>
<rect x="55" y="160" width="150" height="40" rx="8" fill="#FF6B35" opacity="0.9"/><text x="130" y="178" text-anchor="middle" font-size="8" fill="#152435">Sì → vendita</text>
<text x="130" y="192" text-anchor="middle" font-size="7" fill="#152435">rogito, capitale libero</text>
<rect x="355" y="160" width="150" height="40" rx="8" fill="#2C4A6E"/><text x="430" y="178" text-anchor="middle" font-size="8" fill="#fff">No → affitto</text>
<text x="430" y="192" text-anchor="middle" font-size="7" fill="rgba(255,255,255,.85)">canone ricorrente</text>
<text x="280" y="245" text-anchor="middle" font-size="9" fill="#6B7A8D">Incrociare sempre valutazione OMI, fiscalità e obiettivo patrimoniale</text>
<text x="280" y="278" text-anchor="middle" font-size="8" fill="#6B7A8D">Analisi Righetto — non sostituisce consulenza fiscale personalizzata</text>
</svg>
<figcaption>Schema semplificato: liquidità immediata orienta verso vendita; reddito ricorrente verso locazione — da calibrare su caso concreto.</figcaption>
</figure>"""


def svg_confronto_assi() -> str:
    return """<figure class="chart-wrap" aria-label="Confronto assi vendita vs locazione">
<svg viewBox="0 0 540 240" width="100%" height="240" role="img">
<title>Confronto vendita e locazione su quattro assi</title>
<text x="270" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Vendita vs locazione — quattro assi</text>
<text x="80" y="55" font-size="8" fill="#152435">Liquidità</text>
<rect x="130" y="45" width="160" height="14" rx="4" fill="#FF6B35" opacity="0.85"/>
<rect x="130" y="45" width="90" height="14" rx="4" fill="#2C4A6E" opacity="0.5"/>
<text x="80" y="85" font-size="8" fill="#152435">Reddito</text>
<rect x="130" y="75" width="90" height="14" rx="4" fill="#FF6B35" opacity="0.5"/>
<rect x="130" y="75" width="160" height="14" rx="4" fill="#2C4A6E" opacity="0.85"/>
<text x="80" y="115" font-size="8" fill="#152435">Gestione</text>
<rect x="130" y="105" width="170" height="14" rx="4" fill="#FF6B35" opacity="0.85"/>
<rect x="130" y="105" width="70" height="14" rx="4" fill="#2C4A6E" opacity="0.5"/>
<text x="80" y="145" font-size="8" fill="#152435">Flessibilità</text>
<rect x="130" y="135" width="100" height="14" rx="4" fill="#FF6B35" opacity="0.6"/>
<rect x="130" y="135" width="130" height="14" rx="4" fill="#2C4A6E" opacity="0.7"/>
<rect x="300" y="168" width="12" height="12" fill="#FF6B35" opacity="0.85"/><text x="318" y="178" font-size="8" fill="#6B7A8D">Vendita</text>
<rect x="380" y="168" width="12" height="12" fill="#2C4A6E" opacity="0.85"/><text x="398" y="178" font-size="8" fill="#6B7A8D">Locazione</text>
<text x="270" y="215" text-anchor="middle" font-size="8" fill="#6B7A8D">Confronto qualitativo — non percentuali di mercato inventate</text>
</svg>
<figcaption>Confronto qualitativo su liquidità, reddito ricorrente, carico gestionale e flessibilità patrimoniale.</figcaption>
</figure>"""


def _exp(prefix: str, n: int, templates: list[str]) -> list[str]:
    base = [t.format(p=prefix) for t in templates]
    if len(base) >= n:
        return base[:n]
    extra: list[str] = []
    variants = [
        "{p}: incrociare OMI vendita e locazione del semestre ADE prima di decidere.",
        "{p}: distinguere obiettivo patrimoniale (liquidità vs reddito) da emozione di mercato.",
        "{p}: consulenza fiscale personalizzata obbligatoria su plusvalenza e cedolare secca.",
        "{p}: valutazione gratuita Righetto come primo passo numerico — vendita o affitto.",
        "{p}: Limena e Padova hanno domanda diversa su vendita e locazione — microzone OMI.",
    ]
    vi = 0
    while len(base) + len(extra) < n:
        extra.append(variants[vi % len(variants)].format(p=prefix))
        vi += 1
    return base + extra


_EXP_T = [
    "{p} nel Padovano richiede numeri locali — non medie nazionali da portali generici.",
    "{p}: Righetto coordina vendita e locazione dal 2000 — mediazione concordata in sede.",
    "{p} — diverso da blog-comprare-affittare-padova: qui proprietario che possiede già, non acquirente in affitto.",
    "{p}: diverso da blog-rendimento-affitto-padova: qui decisione strategica, non solo calcolo resa per quartiere.",
    "{p}: ISTAT e Osservatorio ADE danno contesto Veneto; il singolo caso decide tempi e fiscalità.",
    "{p}: mutuo residuo sul immobile incide su convenienza vendita immediata vs locazione transitoria.",
    "{p}: eredità o co-proprietà richiedono accordo tra eredi prima di mandato vendita o locazione.",
]

EXPANSION_VENDERE_AFFITTARE = _exp("Vendere o affittare Padova 2026", 58, _EXP_T + [
    "Vendere o affittare Padova 2026: liquidità immediata al rogito vs canone mensile ricorrente — obiettivi opposti da chiarire.",
    "Vendere o affittare Padova 2026: plusvalenza tassabile se vendete sopra prezzo di acquisto — aliquote da verificare con commercialista.",
    "Vendere o affittare Padova 2026: locazione 4+4 o transitorio — scelta incide su turnover inquilino e gestione.",
    "Vendere o affittare Padova 2026: cedolare secca alternativa IRPEF su locazione — convenienza caso per caso.",
    "Vendere o affittare Padova 2026: immobile da ristrutturare — vendere as-is o locare dopo lavori cambia fascia prezzo/canone.",
    "Vendere o affittare Padova 2026: zona universitaria Padova — domanda affitti studenti vs vendita a famiglie.",
    "Vendere o affittare Padova 2026: Limena trilocali — famiglie pendolari comprano; affitto meno volatile che centro storico.",
    "Vendere o affittare Padova 2026: OMI locazioni e vendita sul portale ADE — due fasce da incrociare.",
    "Vendere o affittare Padova 2026: non inventare yield medio percentuale — calcolo in blog-rendimento-affitto-padova con dati verificabili.",
    "Vendere o affittare Padova 2026: costi vendita in blog-costi-vendere-casa-padova-2026 — tasse e spese distinte da reddito affitto.",
    "Vendere o affittare Padova 2026: gestione locazione Righetto — qualifica inquilini, contratto registrato ADE.",
    "Vendere o affittare Padova 2026: mandato vendita esclusivo vs locazione temporanea in attesa mercato — strategia ibrida possibile.",
    "Vendere o affittare Padova 2026: affitti brevi regolamentati — non trattati qui; servizio dedicato e normativa locale.",
    "Vendere o affittare Padova 2026: immobile ereditato — valutazione gratuita per decidere senza fretta emotiva.",
    "Vendere o affittare Padova 2026: mutuo in essere — estinguere con vendita o mantenere con locazione copertura rata.",
    "Vendere o affittare Padova 2026: seconda casa vs prima abitazione — fiscalità diversa in vendita.",
    "Vendere o affittare Padova 2026: mercato 2026 selettivo — immobili pronti vendono; locazione richiede conformità contrattuale.",
    "Vendere o affittare Padova 2026: hub proprietario-immobile — percorsi paralleli vendita e locazione.",
    "Vendere o affittare Padova 2026: landing-valutazione — report comparativo utile per entrambe le strade.",
    "Vendere o affittare Padova 2026: blog-valutazione-casa-padova-guida-2026 — metodo stima prima della decisione.",
    "Vendere o affittare Padova 2026: FIMAA e osservatori affitti Veneto — contesto canoni, non previsioni certe.",
    "Vendere o affittare Padova 2026: Banca d'Italia — condizioni credito acquirenti incidono su velocità vendita.",
    "Vendere o affittare Padova 2026: form lead blog — indicare se valutate vendita, affitto o entrambi.",
    "Vendere o affittare Padova 2026: Via Roma 96 Limena — consulenza gratuita senza impegno mandato.",
    "Vendere o affittare Padova 2026: 127 recensioni Google 4,9/5 — verificabile prima dell'appuntamento.",
    "Vendere o affittare Padova 2026: non pubblicare percentuali commissione agenzia online.",
    "Vendere o affittare Padova 2026: documenti vendita vs contratto locazione registrato — due percorsi amministrativi.",
    "Vendere o affittare Padova 2026: APE e classe energetica incidono su entrambe le scelte — mercato green più selettivo.",
    "Vendere o affittare Padova 2026: ultimo consiglio — decidere con numeri locali, fiscalità e orizzonte temporale, non sensazione.",
    "Vendere o affittare Padova 2026: contratto 4+4 standard — tacito rinnovo salvo disdetta nei termini di legge.",
    "Vendere o affittare Padova 2026: transitorio studenti o lavoro — durata massima e causale da verificare con contratto.",
    "Vendere o affittare Padova 2026: deposito cauzionale e registro ADE — adempimenti locatore prima consegna chiavi.",
    "Vendere o affittare Padova 2026: vendita con proposta vincolante — caparra e compromesso come in blog-proposta-acquisto-negoziazione-padova-2026 lato acquirente.",
    "Vendere o affittare Padova 2026: immobile occupato da inquilino — vendita con contratto in corso richiede coordinamento.",
    "Vendere o affittare Padova 2026: riqualificazione energetica — bonus edilizi possono spostare convenienza vendita post-lavori.",
    "Vendere o affittare Padova 2026: stock annunci portali — domanda filtra prezzi fuori OMI sia vendita che locazione.",
    "Vendere o affittare Padova 2026: consulenza gratuita Limena — portare visura e ultimo APE se disponibili.",
    "Vendere o affittare Padova 2026: WhatsApp e telefono 049.8843484 per fissare appuntamento valutazione.",
])


def body_vendere_affittare() -> str:
    return f"""
{aeo_box("In sintesi", "<strong>Vendere o affittare a Padova</strong> nel 2026 dipende da <strong>liquidità</strong>, <strong>reddito ricorrente</strong>, <strong>fiscalità</strong> e <strong>tempo</strong> — non da una regola universale. Incrociate OMI vendita/locazione e una <a href=\"landing-valutazione\">valutazione gratuita</a>. Diverso da <a href=\"blog-comprare-affittare-padova\">comprare vs affittare</a> (acquirente) e da <a href=\"blog-rendimento-affitto-padova\">rendimento affitto</a> (solo calcolo resa).")}

<p><strong>Distinzione editoriale:</strong> <em>Fatto</em> — fasce OMI, normativa locazione e plusvalenza (fonti ADE, Codice Civile). <em>Dichiarazione</em> — annunci e stime online. <em>Analisi</em> — scenario proprietario Padova/Veneto con obiettivi patrimoniali diversi.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#domanda">La domanda giusta</a></li>
<li><a href="#vendere">Quando ha senso vendere</a></li>
<li><a href="#affittare">Quando ha senso affittare</a></li>
<li><a href="#confronto">Confronto diretto</a></li>
<li><a href="#fiscalita">Fiscalità essenziale</a></li>
<li><a href="#tempi">Tempi e liquidità</a></li>
<li><a href="#mercato">Mercato Padova 2026</a></li>
<li><a href="#rendimento">Reddito vs plusvalenza</a></li>
<li><a href="#mutuo">Mutuo e vincoli</a></li>
<li><a href="#scenari">Scenari tipici</a></li>
<li><a href="#decisione">Come decidere in pratica</a></li>
</ol></nav>

{sol_box("Non so se conviene vendere o affittare il mio immobile a Padova — da dove inizio?", [
    ("Valutazione gratuita", "Stima vendita e confronto canone locazione stimato", "landing valutazione", "landing-valutazione"),
    ("Servizio vendita", "Percorso da listino al rogito", "servizio vendita", "servizio-vendita"),
    ("Servizio locazioni", "Contratto registrato, qualifica inquilini", "servizio locazioni", "servizio-locazioni"),
    ("Hub proprietari", "Guide e FAQ per chi possiede immobile", "proprietario immobile", "proprietario-immobile"),
])}

<h2 id="domanda">Vendere o affittare: la domanda giusta da porsi</h2>
<p>«Conviene vendere o affittare?» è la domanda più frequente che riceviamo in sede da proprietari padovani. La risposta onesta non è mai sì/no assoluto: dipende da <strong>quanto capitale vi serve ora</strong>, da <strong>quanto reddito mensile</strong> vi aspettate, da <strong>vincoli fiscali e mutuo</strong> e da <strong>quanto tempo</strong> volete dedicare alla gestione.</p>
<p>Primo passo condiviso: <a href=\"blog-valutazione-casa-padova-guida-2026\">valutazione immobile Padova 2026</a> — stima vendita e contesto OMI. Per il calcolo resa locativa per quartiere: <a href=\"blog-rendimento-affitto-padova\">rendimento affitto Padova</a>. Per chi non possiede ancora casa: <a href=\"blog-comprare-affittare-padova\">comprare o affittare</a> (angolo acquirente).</p>

{svg_decisione_flow()}

<h2 id="vendere">Quando ha senso vendere a Padova</h2>
<p>La <strong>vendita</strong> libera capitale al rogito — utile se dovete acquistare altrove, estinguere debiti, ripartire eredità tra coeredi o reinvestire. In mercato 2026 nel Veneto la domanda seleziona immobili <strong>documentati e priced</strong>: listino allineato a OMI e comparabili converte più visite.</p>
<ul>
<li><strong>Liquidità immediata</strong> — capitale disponibile post-rogito (meno costi e imposte).</li>
<li><strong>Semplificazione patrimoniale</strong> — niente gestione inquilini, condomini, manutenzione ordinaria.</li>
<li><strong>Rilocazione</strong> — trasferimento fuori Padova o acquisto abitazione principale.</li>
<li><strong>Eredità</strong> — divisione tra eredi spesso richiede vendita se non c'è accordo su locazione.</li>
</ul>
<p>Percorso: <a href=\"servizio-vendita\">servizio vendita</a>, <a href=\"blog-costi-vendere-casa-padova-2026\">costi vendita Padova</a>, <a href=\"vendere-casa-padova-errori\">7 errori vendita</a>.</p>

{blog_fig("img/blog/blog-vendere-o-affittare-padova-2026-vendita.webp", "Vendita immobile Padova — annuncio e trattativa mercato 2026")}

<h2 id="affittare">Quando ha senso affittare a Padova</h2>
<p>La <strong>locazione</strong> genera canone ricorrente — adatta se non avete urgenza di liquidità, volete mantenere l'asset nel patrimonio o attendete condizioni di mercato migliori per vendere. Padova ha domanda affitti strutturata: <strong>università</strong>, <strong>ospedali</strong>, <strong>pendolari</strong> verso Mestre e Vicenza.</p>
<ul>
<li><strong>Reddito mensile</strong> — flusso cassa dopo spese, IMU (se applicabile) e gestione.</li>
<li><strong>Attesa strategica</strong> — locazione transitoria in attesa ristrutturazione o mercato.</li>
<li><strong>Patrimonio familiare</strong> — mantenere immobile per figli o successione futura.</li>
<li><strong>Copertura mutuo</strong> — canone che copre rata (da verificare con commercialista).</li>
</ul>
<p>Percorso: <a href=\"servizio-locazioni\">servizio locazioni</a>, <a href=\"blog-quotazioni-locazioni-omi-istat-padova-2026\">quotazioni OMI affitti</a>, <a href=\"blog-registro-contratti-affitto-padova-2026\">registro contratti affitto</a>.</p>

{blog_fig("img/blog/blog-vendere-o-affittare-padova-2026-locazione.webp", "Locazione immobile Padova — contratto affitto e gestione 2026")}

<h2 id="confronto">Confronto diretto: vendita vs locazione</h2>

<div class="vs-grid">
<div class="vs-col"><h3>Vendere</h3><ul>
<li>Capitale lump-sum al rogito</li>
<li>Fine gestione inquilini</li>
<li>Plusvalenza tassabile se applicabile</li>
<li>Tempo medio vendita variabile per zona</li>
<li>Costi: agenzia, notaio, imposte (vedi guida costi)</li>
</ul></div>
<div class="vs-col"><h3>Affittare</h3><ul>
<li>Canone mensile ricorrente</li>
<li>Gestione contratto, inquilino, manutenzione</li>
<li>Cedolare secca o IRPEF — scelta fiscale</li>
<li>Registrazione contratto ADE obbligatoria</li>
<li>Immobile resta nel patrimonio</li>
</ul></div>
</div>

<table>
<caption>Vendita vs locazione — quattro dimensioni</caption>
<thead><tr><th>Dimensione</th><th>Vendita</th><th>Locazione</th></tr></thead>
<tbody>
<tr><td>Obiettivo principale</td><td>Liquidità e uscita patrimonio</td><td>Reddito ricorrente</td></tr>
<tr><td>Impegno gestionale</td><td>Concentrato in fase vendita</td><td>Continuo (condominio, inquilino)</td></tr>
<tr><td>Rischio mercato</td><td>Prezzo fissato al rogito</td><td>Canone e vacanza locativa</td></tr>
<tr><td>Fiscalità</td><td>Plusvalenza, imposte rogito</td><td>Redditi fondiari, cedolare secca</td></tr>
<tr><td>Fonte dati locali</td><td><a href="{OMI_URL}" target="_blank" rel="noopener noreferrer">OMI vendita ADE</a></td><td><a href="{OMI_URL}" target="_blank" rel="noopener noreferrer">OMI locazioni ADE</a></td></tr>
</tbody>
</table>

{svg_confronto_assi()}

<h2 id="fiscalita">Fiscalità: cosa chiedere al commercialista (senza numeri inventati)</h2>
<p>Non pubblichiamo aliquote o percentuali fiscali statiche — si aggiornano e dipendono dal vostro caso. In vendita: <strong>plusvalenza</strong> se prezzo superiore al costo di acquisto (con regole e detrazioni specifiche). In locazione: <strong>cedolare secca</strong> alternativa all'IRPEF ordinaria, <strong>registrazione contratto</strong> con Agenzia delle Entrate entro termini di legge.</p>
<p>Per imposte di rogito e costi vendita: <a href=\"blog-costi-vendere-casa-padova-2026\">costi vendere casa Padova</a>. Per locazione: <a href=\"blog-quotazioni-locazioni-omi-istat-padova-2026\">OMI affitti</a>. Righetto coordina la parte commerciale — <strong>non sostituisce</strong> consulenza fiscale personalizzata.</p>

<h2 id="tempi">Tempi e liquidità: il fattore spesso decisivo</h2>
<p>Se dovete liberare capitale entro mesi — acquisto altra casa, eredità da ripartire, estinzione mutuo — la <strong>vendita</strong> è spesso l'unica strada realistica, con tempi che dipendono da prezzo, zona e completezza documenti. Se l'orizzonte è <strong>5–10 anni</strong>, la locazione può avere senso mentre monitorate mercato e ristrutturazioni.</p>
<p>Documenti pronti accelerano entrambe le strade: <a href=\"blog-documenti-vendita-casa\">documenti vendita</a> per il rogito; visura, APE e regolamento condominiale per locazione.</p>

<h2 id="mercato">Mercato Padova e Veneto nel 2026</h2>
<p>Contesto macro verificabile: <a href="{ADE_OSSERVATORIO}" target="_blank" rel="noopener noreferrer">Osservatorio immobiliare ADE</a>, <a href="{ISTAT_URL}" target="_blank" rel="noopener noreferrer">ISTAT prezzi abitazioni</a>, <a href="{BANCA_ITALIA}" target="_blank" rel="noopener noreferrer">Banca d'Italia</a>. A Padova città e provincia convivono domanda <strong>famiglie</strong> (cintura Limena, Rubano), <strong>studenti</strong> (zone universitarie) e <strong>investitori</strong> attenti al rendimento — senza generalizzare percentuali inventate per quartiere.</p>
<p>Approfondimenti: <a href=\"blog-mercato-immobiliare-padova-2026\">mercato immobiliare Padova 2026</a>, <a href=\"blog-affitti-limena-2026\">affitti Limena</a>, <a href=\"zona-limena\">zona Limena</a>.</p>

{blog_fig("img/blog/blog-vendere-o-affittare-padova-2026-decisione.webp", "Decisione vendere o affittare Padova — confronto scenari proprietario 2026")}

<h2 id="rendimento">Reddito da affitto vs plusvalenza da vendita</h2>
<p>Il <strong>rendimento locativo</strong> si calcola incrociando canone annuo e valore immobile — metodologia dettagliata in <a href=\"blog-rendimento-affitto-padova\">rendimento affitto Padova</a>, con distinzione lordo/netto e per quartiere. La <strong>plusvalenza</strong> dalla vendita è la differenza (al netto di costi) tra prezzo di cessione e costo di acquisto — fiscalità da calcolare con professionista.</p>
<p>Non esiste «soglia magica» universale: un bilocale in zona universitaria può orientare all'affitto; un trilocale ristrutturato in Limena può orientare alla vendita a famiglia — dipende dai vostri obiettivi, non da un titolo di giornale.</p>

<h2 id="mutuo">Mutuo in essere e altri vincoli</h2>
<p>Con <strong>mutuo residuo</strong>, vendere estingue (o riduce) il debito con il ricavato; affittare può coprire la rata se il canone lo consente — verificare clausole banca e copertura assicurativa. Co-proprietà, usufrutto, vincoli urbanistici o lavori deliberati in condominio possono limitare una delle due opzioni fino a regolarizzazione.</p>

<h2 id="scenari">Scenari tipici nel Padovano</h2>
<table>
<caption>Scenari proprietario — orientamento (non consulenza personalizzata)</caption>
<thead><tr><th>Situazione</th><th>Orientamento</th><th>Verificare con</th></tr></thead>
<tbody>
<tr><td>Eredità, più eredi</td><td>Vendita o locazione concordata</td><td>Notaio, commercialista, valutazione</td></tr>
<tr><td>Trasferimento lavoro</td><td>Vendita o affitto transitorio</td><td>Tempi, mutuo, domanda locazione zona</td></tr>
<tr><td>Seconda casa vuota</td><td>Affitto o vendita se costi IMU/gestione pesanti</td><td>Fiscalità, OMI locazione</td></tr>
<tr><td>Immobile da ristrutturare</td><td>Vendere as-is vs locare post-lavori</td><td>Valutazione prima/dopo, budget cantiere</td></tr>
<tr><td>Attesa mercato migliore</td><td>Locazione temporanea</td><td>Canone vs costi fissi, orizzonte temporale</td></tr>
</tbody>
</table>

<h2 id="decisione">Come decidere in pratica — passi consigliati</h2>
<ol>
<li><strong>Valutazione gratuita</strong> — <a href=\"landing-valutazione\">landing valutazione</a>: fascia vendita + stima canone orientativa.</li>
<li><strong>Simulazione fiscale</strong> — commercialista su plusvalenza vs reddito affitto.</li>
<li><strong>Verifica mutuo/vincoli</strong> — banca e documenti urbanistici.</li>
<li><strong>Scelta mandato</strong> — vendita (<a href=\"servizio-vendita\">servizio vendita</a>) o locazione (<a href=\"servizio-locazioni\">servizio locazioni</a>), compenso concordato in sede.</li>
<li><strong>Monitoraggio</strong> — aggiornare decisione se cambia OMI semestrale o situazione personale.</li>
</ol>

<p>Prima di firmare mandato vendita o contratto locazione, incrociate sempre la valutazione scritta con il vostro commercialista: la scelta migliore nel 2026 resta quella documentata, non quella dettata da un titolo generico sui social.</p>

<div class="cta-row">
<a class="cta-deep" href="landing-valutazione">Valutazione gratuita — vendita e affitto</a>
<a class="cta-deep-outline" href="proprietario-immobile">Hub proprietari</a>
</div>

<p>{CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 29 agosto 2026. Fonti: OMI ADE, Osservatorio immobiliare, ISTAT, Banca d'Italia. Fiscalità: consultare commercialista.</p>
"""


CFG = {
    "slug": SLUG,
    "filename": f"{SLUG}.html",
    "hero": "img/blog/blog-vendere-o-affittare-padova-2026-hero.webp",
    "title": "Vendere o affittare Padova 2026: come decidere",
    "og_title": "Vendere o affittare a Padova 2026: guida decisionale",
    "meta": "Vendere o affittare casa a Padova 2026: confronto scenari, fiscalità, tempi e mercato. Guida proprietari con valutazione gratuita Righetto.",
    "schema_headline": "Vendere o affittare a Padova nel 2026: come decidere",
    "section": "Guida proprietari",
    "cat_badge": "Proprietari · Confronto",
    "bread_crumb": "Vendere o affittare Padova",
    "h1": "<strong>Vendere o affittare</strong> a Padova: guida 2026",
    "hero_alt": "Vendere o affittare immobile Padova 2026 — confronto scenari proprietario",
    "body_fn": body_vendere_affittare,
    "faqs": [
        ("Conviene vendere o affittare a Padova nel 2026?", "Dipende da liquidità, reddito atteso, fiscalità e tempo — non c'è risposta unica; serve valutazione e scenario personalizzato."),
        ("Quanto rende affittare rispetto a vendere?", "Il rendimento locativo si calcola con canone e valore — vedi guida rendimento affitto; la vendita realizza plusvalenza al rogito con fiscalità diversa."),
        ("Devo pagare tasse se affitto?", "Sì — redditi da locazione con cedolare secca o IRPEF; registrazione contratto ADE. Dettaglio con commercialista."),
        ("Posso affittare mentre aspetto di vendere?", "Sì, strategia comune — locazione temporanea con uscita per vendita concordata in contratto."),
        ("La valutazione Righetto è gratuita?", "Sì — sopralluogo e report scritto senza impegno, utile per entrambe le decisioni."),
        ("Differenza da comprare vs affittare?", "Quell'articolo è per chi non possiede casa; qui decide il proprietario che ha già l'immobile."),
    ],
    "related": [
        ("Valutazione immobile", "blog-valutazione-casa-padova-guida-2026"),
        ("Rendimento affitto", "blog-rendimento-affitto-padova"),
        ("Costi vendita", "blog-costi-vendere-casa-padova-2026"),
        ("Quotazioni OMI affitti", "blog-quotazioni-locazioni-omi-istat-padova-2026"),
        ("Servizio locazioni", "servizio-locazioni"),
        ("Valutazione gratuita", "landing-valutazione"),
    ],
    "registry": {
        "titolo": "Vendere o affittare a Padova 2026: come decidere",
        "categoria": "Guida proprietari",
        "tempo": 15,
        "contenuto": "Confronto vendita vs locazione Padova: liquidità, fiscalità, tempi, mercato. CTA valutazione gratuita.",
        "admin_contenuto": "Pillar acquisizione eq-acq-002 — vendere o affittare Padova struttura CONFRONTO.",
        "emoji": "⚖️",
        "evidenza": True,
    },
    "static_map_key": "vendere o affittare padova 2026",
    "cta_banner_title": "Non sai se vendere o affittare?",
    "cta_banner_text": "Valutazione gratuita con scenario vendita e locazione — Limena, Padova e provincia.",
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
    text = text.replace("  const articoliStatici = [\n", "  const articoliStatici = [\n" + registry_blog_entry(CFG), 1)
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
    text = text.replace(anchor, anchor + insert, 1) if anchor in text else text.replace(
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
    text = text.replace("  const articoliStatici = [\n", "  const articoliStatici = [\n" + registry_homepage_entry(CFG), 1)
    text = text.replace("  const staticMap = {\n", "  const staticMap = {\n" + registry_static_map_entry(CFG), 1)
    path.write_text(text, encoding="utf-8")
    print("homepage.js: articoliStatici + staticMap aggiornati")


def patch_editorial_queue() -> None:
    if not EDITORIAL_QUEUE_PATH.exists():
        return
    data = json.loads(EDITORIAL_QUEUE_PATH.read_text(encoding="utf-8"))
    for item in data.get("items", []):
        if item.get("id") == "eq-acq-002":
            item["status"] = "published"
            item["published_date"] = DATE_ISO
            item["substantive_area"] = "INVESTIMENTO"
            item["different_from"] = "blog-rendimento-affitto-padova"
            item["gap_analysis"] = (
                "Rendimento affitto e comprare-vs-affittare esistono; gap decisione proprietario vendere vs locare."
            )
            item["value_add"] = "Confronto CONFRONTO owner: liquidità, fiscalità, tempi, scenari Padova senza yield inventati."
            break
    data["updated"] = DATE_ISO
    EDITORIAL_QUEUE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("editorial-queue.json: eq-acq-002 -> published")


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

    print("\n-- Pillar eq-acq-002 vendere/affittare Padova 2026 --")
    print(f"  • {CFG['filename']} ({words} parole)")


if __name__ == "__main__":
    main()
