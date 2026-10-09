# -*- coding: utf-8 -*-
"""Percorso F — casa non si vende Padova, strategia oltre il prezzo (eq-oct09-001).
python scripts/build_blog_casa_non_si_vende_padova_oct09.py
"""
from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE_IT = "9 ottobre 2026"
DATE_ISO = "2026-10-09"
TIME_TS = "2026-10-09T10:00:00+02:00"
QUEUE_ID = "eq-oct09-001"

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
CLAIM_FOOT = _batch.CLAIM_FOOT
OMI_URL = _batch.OMI_URL
ISTAT_URL = _batch.ISTAT_URL
ADE_OSSERVATORIO = _batch.ADE_OSSERVATORIO
MIN_BODY_WORDS = _batch.MIN_BODY_WORDS
CAP_BLOG_AI = _batch.CAP_BLOG_AI

EDITORIAL_QUEUE_PATH = ROOT / "data" / "editorial-queue.json"
SLUG = "blog-casa-non-si-vende-padova-strategia-2026"

IMAGE_SOURCES: dict[str, tuple[str, str] | list[tuple[str, str]]] = {
    "hero": (
        "img/foto-servizi/vendita-immobili-padova.webp",
        "img/blog/blog-casa-non-si-vende-padova-strategia-2026-hero.webp",
    ),
    "body": [
        (
            "img/blog/blog-vendere-casa-limena-proprietario-2026-valutazione.webp",
            "img/blog/blog-casa-non-si-vende-padova-strategia-2026-diagnostica.webp",
        ),
        (
            "img/blog/home-staging.webp",
            "img/blog/blog-casa-non-si-vende-padova-strategia-2026-marketing.webp",
        ),
        (
            "img/foto-servizi/vendita-immobili-padova.webp",
            "img/blog/blog-casa-non-si-vende-padova-strategia-2026-mandato.webp",
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


def svg_diagnostica() -> str:
    return """<figure class="chart-wrap" aria-label="Diagnostica immobile invenduto Padova">
<svg viewBox="0 0 540 240" width="100%" height="240" role="img">
<title>Diagnostica casa non si vende — leve oltre il prezzo</title>
<text x="270" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Percorso F: cosa verificare prima di abbassare il listino</text>
<rect x="30" y="45" width="95" height="40" rx="8" fill="#2C4A6E"/><text x="77" y="68" text-anchor="middle" font-size="7" fill="#fff">Listino vs OMI</text>
<rect x="140" y="45" width="95" height="40" rx="8" fill="#3A5F8C"/><text x="187" y="68" text-anchor="middle" font-size="7" fill="#fff">Annuncio / foto</text>
<rect x="250" y="45" width="95" height="40" rx="8" fill="#FF6B35" opacity="0.85"/><text x="297" y="68" text-anchor="middle" font-size="7" fill="#152435">Documenti</text>
<rect x="360" y="45" width="95" height="40" rx="8" fill="#2C4A6E"/><text x="407" y="68" text-anchor="middle" font-size="7" fill="#fff">Mandato</text>
<rect x="470" y="45" width="50" height="40" rx="8" fill="#3A5F8C"/><text x="495" y="68" text-anchor="middle" font-size="6" fill="#fff">Visite</text>
<text x="270" y="120" text-anchor="middle" font-size="9" fill="#6B7A8D">Strategia = sequenza, non solo taglio prezzo a rilento</text>
<text x="270" y="200" text-anchor="middle" font-size="8" fill="#6B7A8D">Righetto — consulenza percorso F: landing-consulenza-immobiliare-gratuita</text>
</svg>
<figcaption>Schema operativo: cinque leve da controllare quando l'immobile è fermo da mesi.</figcaption>
</figure>"""


def body_invenduta() -> str:
    return f"""
{aeo_box("In sintesi", "Se la <strong>casa non si vende a Padova</strong>, il listino è spesso solo uno dei fattori. Percorso <strong>F</strong> (già in vendita): diagnostica su <strong>OMI ADE</strong>, qualità annuncio, dossier documentale, mandato e visite. Righetto offre <a href=\"landing-consulenza-immobiliare-gratuita\">consulenza gratuita</a> per ripianificare — diverso da <a href=\"blog-tempi-vendita-casa-padova\">tempi medi di vendita</a> e da <a href=\"blog-home-staging-padova\">home staging</a> da solo.")}

<p><strong>Distinzione editoriale:</strong> <em>Fatto</em> — APE obbligatorio, registrazione contratti, fasce OMI pubblicate dall'ADE. <em>Analisi</em> — perché un immobile fermo segnala debolezza sul mercato padovano selettivo del 2026. <em>Previsione</em> — nessuna garanzia di giorni di vendita; dipende da prezzo credibile, prodotto e domanda del semestre.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#percorso-f">Percorso F: già in vendita</a></li>
<li><a href="#segnali">Segnali che non è solo «mercato fermo»</a></li>
<li><a href="#prezzo">Prezzo, OMI e comparabili venduti</a></li>
<li><a href="#annuncio">Annuncio, foto e coerenza multi-portale</a></li>
<li><a href="#documenti">Documenti che bloccano mutuo e trattativa</a></li>
<li><a href="#mandato">Mandato, referente unico, esclusiva</a></li>
<li><a href="#presentazione">Presentazione, staging e visite</a></li>
<li><a href="#zona">Centro storico, ville e fascia alta</a></li>
<li><a href="#piano-90">Piano 90 giorni di ripartenza</a></li>
<li><a href="#quando-consulenza">Quando chiedere consulenza esterna</a></li>
<li><a href="#prossimi-passi">Prossimi passi</a></li>
</ol></nav>

<div class="kpi-strip" aria-label="Contesto vendita Padova">
<div><strong>Padova</strong><span>Mercato selettivo 2026</span></div>
<div><strong>OMI</strong><span>Fascia ADE ufficiale</span></div>
<div><strong>350+</strong><span>Immobili gestiti</span></div>
<div><strong>101</strong><span>Comuni serviti</span></div>
</div>

{sol_box("Cosa fare se la casa non si vende?", [
    ("Consulenza gratuita", "Diagnostica percorso F con referente Righetto", "consulenza", "landing-consulenza-immobiliare-gratuita"),
    ("Valutazione", "Secondo parere su listino e comparabili", "valutazione", "landing-valutazione"),
    ("Servizio vendita", "Mandato, marketing, trattativa", "servizio vendita", "servizio-vendita"),
    ("Hub proprietari", "Percorsi A–L e guide", "proprietario", "proprietario-immobile"),
])}

<h2 id="percorso-f">Percorso F: la casa è già in vendita ma non si chiude</h2>
<p>Se avete già un annuncio attivo da settimane o mesi senza proposte serie, siete nel <strong>percorso F</strong> del funnel Righetto: non siete alla prima valutazione (A) né al «penso di vendere» (B). Avete investito tempo, forse più agenzie, e il mercato vi sembra muto. In realtà, nel Padovano del 2026, la domanda esiste ma è <strong>selettiva</strong>: compratori confrontano decine di schede online, filtrano per prezzo/mq, classe energetica e foto, e prenotano visite solo su immobili credibili.</p>
<p>Questo articolo non ripete la guida generica sui <a href=\"blog-tempi-vendita-casa-padova\">tempi di vendita a Padova</a>: qui l'obiettivo è un <strong>piano di ripartenza</strong> quando siete già sul mercato. Complementare anche a <a href=\"blog-so-tutto-io-venditore-presuntuoso-padova-2026\">venditore «so tutto io»</a> e a <a href=\"blog-vendita-immobiliare-padova-strategie-2026\">strategie vendita Padova 2026</a>, con angolo diagnostico percorso F.</p>
<p>Righetto accompagna proprietari dal 2000 con sede a <strong>Limena (Via Roma 96)</strong> e copertura su Padova città e provincia. Il compenso di mediazione si concorda <strong>sempre in sede</strong> — nessun listino percentuale online.</p>

<div class="cta-row">
<a class="cta-deep" href="landing-consulenza-immobiliare-gratuita">Consulenza gratuita — percorso F</a>
<a class="cta-deep-outline" href="landing-valutazione">Seconda valutazione listino</a>
</div>

<h2 id="segnali">Segnali che il problema non è solo «mercato lento»</h2>
<p>Alcuni indicatori oggettivi suggeriscono che serve cambiare strategia, non aspettare il prossimo trimestre:</p>
<ul>
<li><strong>Zero visite qualificate</strong> in 30–45 giorni con annuncio su portali principali.</li>
<li><strong>Solo richieste generiche</strong> («info») senza richiesta di sopralluogo o mutuo.</li>
<li><strong>Comparabili venduti</strong> in zona a prezzo inferiore al vostro con caratteristiche simili.</li>
<li><strong>Ribassi già effettuati</strong> senza aumento visite — il mercato ha «scontato» la credibilità dell'annuncio.</li>
<li><strong>Stesso immobile</strong> su più portali con testi o prezzi leggermente diversi.</li>
<li><strong>Feedback ripetuto</strong> in visita su odori, disordine, lavori visibili, planimetria non chiara.</li>
</ul>
<p>Se riconoscete almeno tre punti, passate dalla speranza passiva a una <strong>diagnostica strutturata</strong>. L'<a href="{ADE_OSSERVATORIO}" target="_blank" rel="noopener noreferrer">Osservatorio del mercato immobiliare ADE</a> e <a href="{ISTAT_URL}" target="_blank" rel="noopener noreferrer">ISTAT</a> aiutano sul contesto macro Veneto; per il singolo appartamento servono comparabili locali e sopralluogo.</p>

{svg_diagnostica()}

<h2 id="prezzo">Prezzo, OMI e comparabili: quando il listino è la leva principale</h2>
<p>Il prezzo resta la variabile più visibile, ma va calibrato con metodo — non con tagli emotivi ogni due mesi. Consultate <a href="{OMI_URL}" target="_blank" rel="noopener noreferrer">OMI ADE</a> per la zona omogenea del vostro immobile (centro storico, Arcella, Chiesanuova, cintura…): minimo, medio e massimo sono riferimenti ufficiali, non il prezzo finale di rogito.</p>
<p>Errore frequente percorso F: basarsi su <strong>annunci ancora invenduti</strong> invece che su transazioni chiuse o comparabili venduti negli ultimi 6–12 mesi. Gli annunci alti trainano verso l'alto solo sulla carta; il mercato punisce chi resta fuori cluster.</p>
<p>Guida metodo: <a href=\"blog-valutazione-casa-padova-guida-2026\">valutazione immobile Padova</a>. Se avete già avuto perizie discordanti, <a href=\"servizio-valutazioni\">servizio valutazioni Righetto</a> chiarisce obiettivi (vendita vs mutuo acquirente).</p>

<table>
<caption>Checklist prezzo — immobile fermo Padova</caption>
<thead><tr><th>Domanda</th><th>Azione se «no»</th></tr></thead>
<tbody>
<tr><td>Listino entro fascia OMI difendibile?</td><td>Rivalutazione comparativa + sopralluogo</td></tr>
<tr><td>Ultimo ribasso &lt; 60 giorni fa?</td><td>Prima sistemare annuncio/documenti, poi prezzo</td></tr>
<tr><td>Prezzo coerente su tutti i portali?</td><td>Allineare con referente unico</td></tr>
<tr><td>Acquirente tipo individuato?</td><td>Ricalibrare titolo annuncio e canali</td></tr>
</tbody>
</table>

<p>Non pubblichiamo €/mq medi inventati per Padova: ogni microzona ha dinamica propria. Per ville e immobili di pregio in centro, il confronto richiede campione ristretto — vedi sezione fascia alta.</p>

{blog_fig("img/blog/blog-casa-non-si-vende-padova-strategia-2026-diagnostica.webp", "Diagnostica casa non si vende Padova — listino OMI e comparabili")}

<h2 id="annuncio">Annuncio, foto e coerenza tra portali</h2>
<p>Un immobile invenduto spesso ha un <strong>problema di prodotto percepito</strong>, non solo di cifra. Nel 2026 la prima visita avviene sullo schermo: foto scure, pochi scatti, assenza planimetria, titolo generico («bilocale Padova») non distinguono la vostra offerta.</p>
<p>Standard minimo da verificare:</p>
<ol>
<li><strong>Copertura ambienti</strong> — soggiorno, cucina, camere, bagni, esterni, box.</li>
<li><strong>Luce e ordine</strong> — equivalente a una visita reale curata.</li>
<li><strong>Planimetria leggibile</strong> con metrature coerenti con catasto.</li>
<li><strong>Descrizione onesta</strong> — spese condominiali, lavori in corso, orientamento.</li>
<li><strong>Un solo prezzo</strong> e testo master — evitare versioni parallele.</li>
</ol>
<p>Se l'immobile è pubblicato in <strong>non esclusiva</strong> da più agenzie, è facile divergenza di prezzo e foto obsolete. Approfondimento: <a href=\"blog-mandato-esclusivo-padova-perche-conviene-2026\">mandato esclusivo Padova</a>.</p>

{blog_fig("img/blog/blog-casa-non-si-vende-padova-strategia-2026-marketing.webp", "Marketing immobile invenduto — foto e annuncio immobiliare Padova")}

<h2 id="documenti">Documenti e conformità: blocchi silenziosi</h2>
<p>Molte trattative muoiono in due diligence: <strong>planimetria non conforme</strong>, APE assente o scaduto, assenza di certificazioni impianti dove richieste, delibere condominiali non comunicate. L'acquirente con mutuo non può chiudere; quello cash chiede sconto aggressivo.</p>
<p>Checklist rapida percorso F:</p>
<ul>
<li>Visura catastale e planimetria allineate allo stato di fatto.</li>
<li>APE valido per compravendita abitativa.</li>
<li>Ultimi verbali condominiali e spese ordinarie documentate.</li>
<li>Pertinenze (box, cantina) con subalterni corretti.</li>
<li>Atto di provenienza e eventuale successione regolarizzata.</li>
</ul>
<p>Guida trasversale: <a href=\"blog-documenti-vendita-casa\">documenti vendita casa</a>. Sanare prima dell'annuncio costa meno che scoprire il difetto a compromesso.</p>

<h2 id="mandato">Mandato, referente unico e ripartenza con l'agenzia</h2>
<p>Cambiare agenzia non è obbligatorio, ma <strong>cambiare piano sì</strong>. Se il mandato attuale non prevede revisione marketing, report visite e strategia prezzo a 30/60 giorni, negoziate un reset contrattuale o valutate un nuovo incarico con obiettivi misurabili (visite/mese, feedback scritti, revisione listino).</p>
<p>L'<strong>esclusiva</strong> concentra responsabilità e messaggio; la non esclusiva moltiplica annunci ma spesso diluisce l'impegno. Scelta da concordare in sede — compenso Righetto sempre nel mandato scritto, senza percentuali pubblicate online.</p>
<p>Per chi vende da privato da mesi: <a href=\"vendere-casa-padova-errori\">errori vendita Padova</a> e passaggio a professionista con <a href=\"servizio-vendita\">servizio vendita</a>.</p>

{blog_fig("img/blog/blog-casa-non-si-vende-padova-strategia-2026-mandato.webp", "Mandato vendita Padova — ripartenza strategia percorso F")}

<h2 id="presentazione">Presentazione, home staging e qualità visite</h2>
<p>Se le visite ci sono ma non arrivano offerte, il feedback in visita è oro: chiedete all'agente un <strong>report sintetico</strong> (prezzo percepito, confronto con altri visti, ostacoli). Spesso emergono dettagli risolvibili — verniciatura, depersonalizzazione, piccoli lavori, ordine cantina.</p>
<p>L'home staging non è obbligatorio per legge, ma può accelerare la percezione di valore: guida <a href=\"blog-home-staging-padova\">home staging Padova</a>. Coordinate ditte con l'agenzia; evitate lavori strutturali non comunicati in annuncio.</p>
<p>Per visite: luce naturale, assenza odori, documenti a portata, preferibilmente <strong>venditore assente</strong> durante il sopralluogo per non pressare l'acquirente.</p>

<h2 id="zona">Centro storico, ville e immobili oltre la media</h2>
<p>A Padova, <strong>centro storico</strong> e <strong>ville</strong> hanno bacino più ristretto e cicli di vendita più lunghi se il listino non è allineato al campione di pregio. Investitori e acquirenti fascia alta chiedono trasparenza su vincoli, rendimenti locativi potenziali (senza promesse), stato impianti e costi di gestione.</p>
<p>Righetto tratta anche incarichi riservati e valutazioni dedicate: <a href=\"valutazione-vendita-riservata-padova\">valutazione vendita riservata Padova</a>. Non confondete «tempo sul mercato lungo» con «prezzo di lusso giustificato» senza comparabili omogenei.</p>

<h2 id="piano-90">Piano operativo 90 giorni di ripartenza</h2>
<p>Schema proposto ai proprietari percorso F (da adattare caso per caso):</p>
<ol>
<li><strong>Giorni 1–7:</strong> audit listino vs OMI + 5 comparabili venduti; allineamento prezzo portali.</li>
<li><strong>Giorni 8–21:</strong> refresh foto/planimetria/descrizione; dossier documentale completo.</li>
<li><strong>Giorni 22–45:</strong> campagna visite mirata; raccolta feedback scritto.</li>
<li><strong>Giorni 46–60:</strong> decisione su staging o micro-lavori; eventuale aggiustamento listino motivato.</li>
<li><strong>Giorni 61–90:</strong> valutazione mandato/esclusiva; trattativa su lead qualificati con mutuo.</li>
</ol>
<p>Se a 90 giorni non ci sono segnali (visite qualificate + almeno una trattativa), serve revisione radicale prezzo o prodotto — non un quarto ribasso simbolico.</p>

<h2 id="quando-consulenza">Quando ha senso una consulenza Righetto se avete già un'agenzia</h2>
<p>Non sostituiamo il mandato altrui senza regole deontologiche e contrattuali. Ma una <strong>consulenza gratuita</strong> può offrire secondo parere su listino, annuncio e piano — utile se siete bloccati. Percorso: <a href=\"landing-consulenza-immobiliare-gratuita\">landing consulenza immobiliare gratuita</a>, telefono 049.8843484, o hub <a href=\"proprietario-immobile\">proprietario immobile</a>.</p>
<p>Chi vende trova in Righetto un <strong>alleato</strong>: dati verificabili, accompagnamento, trasparenza sul compenso in sede — non portale anonimo.</p>

<h2 id="quartieri">Padova città e provincia: la stessa diagnosi, contesti diversi</h2>
<p>Un trilocale in <strong>Arcella</strong> non compete con uno in <strong>Centro storico</strong> né con una villetta a <strong>Abano Terme</strong> o <strong>Vigonza</strong>. Quando la casa non si vende, il primo errore è confrontarsi con annunci di zone diverse. Usate la scheda zona pertinente — esempio <a href=\"zona-arcella\">Arcella</a>, <a href=\"zona-chiesanuova\">Chiesanuova</a>, <a href=\"zona-limena\">Limena</a> — per capire domanda e tipologie ricorrenti.</p>
<p>Nella cintura nord-ovest (Limena, Cadoneghe, Rubano) compratori spesso cercano box, giardino e collegamenti verso tangenziale. In centro storico contano vincoli, accessi e costi di gestione. Se il vostro listino è calibrato su un comparabile in altra microzona OMI, il mercato vi ignora senza spiegazioni verbali.</p>
<p>Per immobili commerciali o misti la logica invenduto cambia ancora: tempi più lunghi, due diligence urbanistica più severa. In quel caso il percorso F va affiancato a consulenza dedicata, non a ribassi «residenziali» copiati da guide generiche.</p>

<h3>Costo opportunità di restare invenduti</h3>
<p>Ogni mese sul mercato non è neutro: rate mutuo, IMU, spese condominiali, assicurazione, manutenzione ordinaria e — spesso sottovalutato — <strong>usura psicologica</strong> del venditore che rimanda decisioni. Non pubblichiamo cifre medie €/mese per immobile senza campione verificabile sul vostro caso; in consulenza si costruisce un prospetto personalizzato con i vostri numeri reali.</p>
<p>Approfondimento costi accessori vendita: <a href=\"blog-costi-vendere-casa-padova-2026\">costi vendere casa Padova</a>. Distinzione importante: costi di transazione (notaio, imposte) ≠ costo di restare invenduti (holding).</p>

<h3>Trattative fantasma e curiosi</h3>
<p>Se ricevete solo messaggi generici da portali («interessato, mandi prezzo») senza visita, spesso non sono lead qualificati. Un piano percorso F include <strong>filtro telefonico</strong>: verifica budget, mutuo, tempi rogito. Righetto qualifica le richieste prima del sopralluogo per non saturare il venditore con appuntamenti improduttivi.</p>
<p>Offerte verbalmente basse senza caparra non vanno interpretate come «mercato crollato»: possono essere tentativi isolati. Valutate solo proposte con qualifica finanziaria e coerenza con comparabili recenti.</p>

<h3>Eredità, coeredi e immobile fermo</h3>
<p>Se l'immobile invenduto arriva da successione non ancora pacificata, acquirenti e banche si fermano. Percorso collegato: <a href=\"blog-successione-immobiliare-padova\">successione immobiliare Padova</a>. Allineare quote, eventuale divisione e poteri di firma prima di refresh marketing evita mesi persi.</p>

<h3>Vendere o affittare mentre l'annuncio non decolla</h3>
<p>Alcuni proprietari percorso F valutano locazione temporanea. Non è sempre la soluzione migliore: vincoli contrattuali, fiscalità, stato dell'immobile per affitto e obiettivo finale di vendita vanno modellati insieme. Guida: <a href=\"blog-vendere-o-affittare-padova-2026\">vendere o affittare Padova</a> e <a href=\"blog-rendimento-affitto-padova\">rendimento affitto</a> — senza promettere rendimenti percentuali non verificati sul vostro immobile.</p>

<table>
<caption>Feedback in visita — come interpretarlo</caption>
<thead><tr><th>Commento acquirente</th><th>Leva correttiva</th></tr></thead>
<tbody>
<tr><td>«Carino ma caro rispetto ad altri visti»</td><td>Listino o comparabili da rivedere</td></tr>
<tr><td>«Buon prezzo ma cantina umida / lavori»</td><td>Prodotto e staging, non solo prezzo</td></tr>
<tr><td>«Manca planimetria chiara»</td><td>Annuncio e dossier</td></tr>
<tr><td>«Condominio preoccupa»</td><td>Trasparenza verbali e delibere</td></tr>
<tr><td>Nessun feedback — zero visite</td><td>Annuncio, prezzo, visibilità portali</td></tr>
</tbody>
</table>

<h3>Open house e visite coordinate</h3>
<p>In alcune tipologie (ville, immobili di metratura elevata) conviene concentrare visite in finestre open house con agente presente, invece di appuntamenti singoli sparsi. Riduce no-show e permette confronto diretto tra feedback di più visitatori nello stesso giorno. La scelta dipende da zona, privacy del venditore e mandato: va scritta nel piano marketing, non improvvisata.</p>

<h3>Digital e recensioni dell'agenzia</h3>
<p>Acquirenti cercano anche la <strong>credibilità del referente</strong>: recensioni verificabili, risposta alle richieste entro 24 ore lavorative, coerenza tra sito agenzia e portali. Righetto espone 127 recensioni Google (media 4,9/5) — dato verificabile — e non promette tempi di vendita garantiti.</p>

<h2 id="privacy-dati">Privacy, dati lead e trasparenza</h2>
<p>Quando richiedete consulenza via form sul sito Righetto, i dati servono a ricontattarvi per il percorso F — non vengono venduti a terzi. Il sito rispetta Reg. UE 2024/1689 su strumenti di supporto (barra trasparenza, informativa privacy). Nessun modello linguistico sostituisce la valutazione umana in agenzia: la stima online è educativa, il sopralluogo resta il passo decisivo.</p>
<p>Per immobili di fascia alta o vendite riservate, valutate canali che limitano esposizione pubblica eccessiva: <a href=\"valutazione-vendita-riservata-padova\">valutazione vendita riservata</a>.</p>

<h2 id="checklist-finale">Checklist finale percorso F (stampabile)</h2>
<ol>
<li>Listino confrontato con OMI e almeno cinque comparabili chiusi o venduti.</li>
<li>Prezzo identico su tutti i portali e sul sito agenzia.</li>
<li>Foto aggiornate, planimetria, APE e descrizione senza omissioni rilevanti.</li>
<li>Dossier documentale pronto per due diligence mutuo.</li>
<li>Mandato con referente, report visite e revisione a 30/60 giorni.</li>
<li>Feedback visite raccolto e tradotto in azioni (prezzo vs prodotto).</li>
<li>Piano 90 giorni scritto con obiettivi misurabili.</li>
<li>Consulenza prenotata se due cicli di revisione non producono visite qualificate.</li>
</ol>
<p>Se superate la checklist e il mercato resta muto, il problema è quasi sempre <strong>posizionamento prezzo/prodotto</strong> rispetto al campione — non «mancanza assoluta di compratori» nel Padovano.</p>

<h3>Mutuo acquirente e clausole sospensive</h3>
<p>Parte delle trattative percorso F si interrompe perché l'acquirente non ottiene mutuo entro la clausola sospensiva — non perché rifiuta il prezzo. Come venditore potete chiedere lettera di interesse bancaria prima di bloccare date per compromesso. Righetto segnala la pratica in trattativa; le condizioni restano tra acquirente e istituto di credito.</p>
<p>Se il vostro immobile ha difetti che spaventano perizia bancaria (non conformità, APE basso senza piano miglioramento), sanate o prezzate il rischio <em>prima</em> del refresh annuncio — altrimenti ripetete visite che non convertono.</p>
<p>In consulenza percorso F Righetto incrocia anche segnali di domanda locale (Università, pendolarismo Mestre-Venezia, famiglie in cintura) senza promettere tempi fissi: servono per capire se il vostro immobile parla al compratore giusto o a un segmento troppo ristretto per il listino scelto. Portate in appuntamento l'elenco degli annunci comparabili che avete già consultato: accelera la diagnosi.</p>

<h2 id="prossimi-passi">Prossimi passi</h2>
<ol>
<li>Compilate la checklist prezzo e annuncio sopra.</li>
<li>Richiedete <a href=\"landing-consulenza-immobiliare-gratuita\">consulenza percorso F</a> o <a href=\"landing-valutazione\">valutazione</a>.</li>
<li>Allineate documenti prima del prossimo ribasso.</li>
<li>Leggete <a href=\"blog-tempi-vendita-casa-padova\">tempi vendita Padova</a> per aspettative realistiche sul timing totale.</li>
<li>Per mandato: <a href=\"blog-mandato-esclusivo-padova-perche-conviene-2026\">mandato esclusivo</a> e <a href=\"servizio-vendita\">servizio vendita</a>.</li>
</ol>
<p>Cross-link: <a href=\"zona-padova-centro-storico\">zona Padova centro storico</a> · <a href=\"blog-costi-vendere-casa-padova-2026\">costi vendere casa</a> · <a href=\"agenzia-immobiliare-padova\">agenzia Padova</a>.</p>

<p>{CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 9 ottobre 2026. Fonti: OMI e Osservatorio ADE, ISTAT. Nessun dato €/mq inventato; nessuna percentuale mediazione online.</p>
"""


CFG = {
    "slug": SLUG,
    "filename": f"{SLUG}.html",
    "hero": "img/blog/blog-casa-non-si-vende-padova-strategia-2026-hero.webp",
    "title": "Casa non si vende Padova 2026: strategia",
    "og_title": "Casa non si vende a Padova: strategia oltre il prezzo (2026)",
    "meta": "Casa non si vende a Padova? Diagnostica percorso F: OMI, annuncio, documenti, mandato e piano 90 giorni. Consulenza gratuita Righetto Immobiliare.",
    "schema_headline": "Casa non si vende a Padova: strategia oltre il prezzo nel 2026",
    "section": "Guida proprietari",
    "cat_badge": "Proprietari · Percorso F",
    "bread_crumb": "Casa non si vende Padova strategia",
    "h1": "<strong>Casa non si vende</strong> a Padova: strategia 2026",
    "hero_alt": "Casa non si vende Padova 2026 — strategia proprietario percorso F",
    "body_fn": body_invenduta,
    "faqs": [
        ("Cosa fare se la casa non si vende da mesi a Padova?", "Audit su listino vs OMI, qualità annuncio, documenti, mandato e feedback visite; poi piano 90 giorni con referente unico."),
        ("Basta abbassare il prezzo?", "Non sempre: annuncio incoerente, dossier incompleto o mandato frammentato possono bloccare visite anche con ribassi."),
        ("Posso chiedere consulenza se ho già un'agenzia?", "Sì per secondo parere strategico; il passaggio incarico segue regole contrattuali e deontologiche."),
        ("Quanto tempo è normale restare invenduti?", "Dipende da tipologia e prezzo; vedi guida tempi vendita Padova — oltre 90 giorni senza visite qualificate serve reset strategia."),
        ("Righetto tratta centro storico e ville?", "Sì, con valutazioni dedicate e percorsi riservati dove appropriato."),
        ("Quali documenti bloccano la vendita?", "Planimetria non conforme, APE assente, verbali condominiali mancanti, pertinenze non catastate."),
    ],
    "related": [
        ("Tempi vendita Padova", "blog-tempi-vendita-casa-padova"),
        ("Home staging", "blog-home-staging-padova"),
        ("Mandato esclusivo", "blog-mandato-esclusivo-padova-perche-conviene-2026"),
        ("Consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
        ("Valutazione", "landing-valutazione"),
        ("Hub proprietari", "proprietario-immobile"),
    ],
    "registry": {
        "titolo": "Casa non si vende a Padova: strategia oltre il prezzo (2026)",
        "categoria": "Guida proprietari",
        "tempo": 14,
        "contenuto": "Percorso F: diagnostica invenduto, piano 90gg, CTA consulenza e valutazione.",
        "admin_contenuto": "eq-oct09-001 — casa non si vende Padova strategia percorso F.",
        "emoji": "🔑",
        "evidenza": True,
    },
    "static_map_key": "casa non si vende padova strategia 2026",
    "cta_banner_title": "Immobili fermo da mesi?",
    "cta_banner_text": "Consulenza gratuita percorso F — Via Roma 96 Limena · 049.8843484.",
    "owner_path": "F",
    "acquisition_priority": True,
}


def ensure_images() -> None:
    hero_src, hero_dst = IMAGE_SOURCES["hero"]
    src_p = ROOT / hero_src
    dst_p = ROOT / hero_dst
    if not src_p.is_file():
        raise SystemExit(f"ensure_images: sorgente mancante {hero_src}")
    dst_p.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_p, dst_p)
    for body_src, body_dst in IMAGE_SOURCES["body"]:
        bsrc = ROOT / body_src
        bdst = ROOT / body_dst
        if not bsrc.is_file():
            raise SystemExit(f"ensure_images: sorgente mancante {body_src}")
        shutil.copy2(bsrc, bdst)


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
    found = False
    for item in data.get("items", []):
        if item.get("id") == QUEUE_ID:
            item["status"] = "published"
            item["published_date"] = DATE_ISO
            found = True
            break
    if not found:
        data.setdefault("items", []).append(
            {
                "id": QUEUE_ID,
                "status": "published",
                "published_date": DATE_ISO,
                "target_week": DATE_ISO,
                "slug": SLUG,
                "kw_primaria": "casa non si vende padova",
                "intent": "percorso-f-invenduto",
                "title": CFG["registry"]["titolo"],
                "owner_path": "F",
                "acquisition_priority": True,
                "acquisition_contribution": "direct",
            }
        )
    data["updated"] = DATE_ISO
    EDITORIAL_QUEUE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"editorial-queue.json: {QUEUE_ID} -> published")


def main() -> None:
    ensure_images()
    body = CFG["body_fn"]()
    words = wc(body)
    if words < MIN_BODY_WORDS - 10:
        print(f"WARN {CFG['slug']}: {words} parole (< {MIN_BODY_WORDS}) — estendere corpo")
    out = ROOT / CFG["filename"]
    out.write_text(build_html(CFG, body, words), encoding="utf-8")
    print(f"OK {CFG['filename']} — {words} parole")

    patch_blog_html()
    patch_admin_html()
    patch_sitemap()
    patch_homepage()
    patch_editorial_queue()


if __name__ == "__main__":
    main()
