# -*- coding: utf-8 -*-
"""Genera 5 articoli blog Limena GSC agosto 2026.
Esegui da repo root: python scripts/build_blog_limena_gsc_ago2026.py
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent.parent
DATE_IT = "5 agosto 2026"
DATE_ISO = "2026-08-05"
TIME_TS = "2026-08-05T09:00:00+02:00"

_BATCH_PATH = ROOT / "scripts" / "build_blog_batch_lug28_2026.py"
_spec = importlib.util.spec_from_file_location("_blog_batch_lug28", _BATCH_PATH)
_batch = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_batch)

_batch.DATE_ISO = DATE_ISO
_batch.DATE_IT = DATE_IT
_batch.TIME_TS = TIME_TS

build_html = _batch.build_html
STYLE_BLOCK = _batch.STYLE_BLOCK
wc = _batch.wc
aeo_box = _batch.aeo_box
sol_box = _batch.sol_box
faq_html = _batch.faq_html
lead_form = _batch.lead_form
expand_body = _batch.expand_body
blog_fig = _batch.blog_fig
CLAIM_FOOT = _batch.CLAIM_FOOT
OMI_URL = _batch.OMI_URL
ISTAT_URL = _batch.ISTAT_URL
ADE_OSSERVATORIO = _batch.ADE_OSSERVATORIO
MIN_BODY_WORDS = _batch.MIN_BODY_WORDS

REGISTRY_PATH = ROOT / "scripts" / "limena_gsc_ago2026_registry.json"

EXPANSION_LIMENA = [
    "Limena si colloca nella prima cintura nord-ovest di Padova: famiglie e pendolari valutano il comune per metrature più ampie rispetto al centro storico, sempre incrociando le fasce OMI vendita e locazione sul portale ADE del semestre in corso.",
    "Le zone omogenee OMI per Limena vanno lette nel contesto padovano: non esiste un unico prezzo al metro quadro comunale — servono tipologia (abitazione civile), stato conservativo e posizione micro-zonale prima di confrontare annunci.",
    "Un appartamento in classe energetica A o B in cintura può giustificare un posizionamento nella fascia medio-alta OMI se impianti, infissi e isolamento sono documentati con APE recente e fatture lavori verificabili.",
    "La checklist visita a Limena include parcheggio (box, posto auto o libero), rumore da assi viari, umidità in seminterrati, conformità planimetria-cantiere e spese condominiali con delibere straordinarie in corso.",
    "Confrontare almeno tre annunci attivi e due comparabili venduti o locati negli ultimi mesi riduce il rischio di pagare un premium non supportato da OMI o da difetti nascosti dell'immobile.",
    "Il mutuo per acquisto in cintura segue le stesse regole del capoluogo: preventivo banca, LTV, spese notarili e imposte vanno sommati al prezzo richiesto — non basta il listino in vetrina per capire il budget totale.",
    "Per gli affitti, la registrazione del contratto presso l'Agenzia delle Entrate entro i termini di legge tutela locatore e inquilino: senza registrazione, problemi con residenza anagrafica e detrazioni fiscali.",
    "Il deposito cauzionale (caparra confirmatoria o cauzione) va documentato per iscritto nel contratto o in appendice: mai versare somme senza ricevuta e senza aver letto tutte le clausole.",
    "Bilocale e trilocale a Limena rispondono a target diversi: coppie e smart worker spesso orientano al bilocale; famiglie con bambini e home office tendono al trilocale con doppio servizio e spazio esterno.",
    "I pendolari verso Padova centro valutano tempi reali su SR308, tangenziale e linee extraurbane: otto chilometri in mappa non equivalgono a venti minuti se gli orari di punta penalizzano l'accesso al capoluogo.",
    "Case in vendita con foto professionali e planimetria catastale allegata ricevono visite più qualificate: annunci con una sola foto smartphone e descrizione generica attirano curiosi, non acquirenti pronti al compromesso.",
    "Red flag negli annunci: prezzo sotto mercato senza spiegazione, assenza APE, rifiuto visite con tecnico, richiesta bonifici anticipati senza contratto, planimetria non conforme non dichiarata.",
    "Il prezzo richiesto va confrontato con fascia OMI minimo-medio-massimo del semestre: un listino sopra il massimo OMI richiede difendibilità (ristrutturazione recente, classe A, pertinenze) verificabile in visita.",
    "Gruppo Immobiliare Righetto in Via Roma 96 opera dal 2000 su 101 comuni con oltre 350 immobili gestiti: la presenza fisica sul territorio limenese supporta visite, valutazioni e contratti senza intermediari anonimi.",
    "Le 127 recensioni Google con media 4,9 su 5 sono verificabili pubblicamente: segnale E-E-A-T per chi cerca un referente locale su acquisto, vendita o locazione a Limena e in provincia.",
    "Il compenso di mediazione Righetto si concorda in sede nel mandato — nessun listino percentuale online, in linea con deontologia FIMAA e policy editoriale del sito.",
    "Cross-link utili: mercato Limena 2026, confronto Limena vs Padova centro, guida affitti generali e pagina zona-limena completano la lettura senza duplicare angoli editoriali già coperti.",
    "Nuova costruzione vs usato ristrutturato a Limena: il primo offre garanzie strutturali e classe energetica; il secondo può vincere su posizione consolidata e tempi di consegna immediati — confronto caso per caso con OMI.",
    "Spese condominiali e fondo lavori straordinari incidono sul costo mensile reale: in visita chiedere ultimi tre verbali assemblea e stato pagamenti per evitare sorprese post-acquisto.",
    "Per venditori limenesi, home staging minimo (pulizia, tinteggiatura, ordine) e APE aggiornato accelerano la trattativa quando la domanda seleziona solo immobili credibili e documentati.",
    "L'Osservatorio del Mercato Immobiliare ADE pubblica trend semestrali aggregati: utili per contesto macro, da incrociare sempre con microzona OMI del singolo annuncio — mai copiare €/mq nazionali su Limena.",
    "ISTAT monitora l'andamento temporale dei prezzi abitazioni a livello territoriale: complementare a OMI per capire direzione, non per quotare il singolo bilocale in Via Roma.",
    "Visite per inquilini: verificare contatore gas/luce intestato, stato infissi, pressione acqua, cellulare in alloggio e regole condominiali su animali e orari silenzio prima di firmare.",
    "Contratto 4+4 libero vs canone concordato: il primo lascia più margine negoziale ma fiscalità diversa; il secondo vincola il canone ma offre agevolazioni — scelta con consulenza e lettura normativa aggiornata.",
    "Trilocale con terrazzo o giardino comune: famiglie con bambini piccoli privilegiano spazio esterno sicuro; bilocale ultimo piano con ascensore attira coppie senza figli e lavoratori remoti.",
    "Confronto annunci sullo stesso portale: filtrare per metratura ±10%, stesso piano indicativo e pertinenze simili — altrimenti si confrontano immobili non comparabili e si sbaglia valutazione.",
    "Servizio valutazioni Righetto incrocia OMI, transazioni recenti e stato dell'immobile per listino difendibile — utile sia in acquisto (offerta) sia in vendita (uscita mercato).",
    "Limena vs Rubano vs Vigonza: tre comuni contigui con profili domanda simili ma microzone OMI distinte — la scelta va fatta su percorrenza lavoro, servizi e singola proposta, non su slogan generici.",
    "Ultimo aggiornamento consigliato: verificare semestre OMI ADE alla data di lettura; articolo redatto 5 agosto 2026 con fonti istituzionali — nessun dato €/mq inventato per Limena.",
    "Form lead in fondo pagina con provenienza slug permette follow-up personalizzato: indicare tipologia, budget indicativo e tempistiche accelera la risposta in orario di apertura 049.8843484.",
    "Acquirenti prima casa: agevolazioni fiscali e requisiti mutuo vanno verificati con banca e commercialista — l'agenzia immobiliare coordina documenti immobile, non sostituisce consulenza fiscale.",
    "Vendita con proposta condizionata a mutuo: normale in mercato ordinato; acquirente serio presenta lettera banca o broker — diffidate da offerte senza qualifica finanziaria in mercato competitivo.",
]

def svg_omi_zone() -> str:
    return """<figure class="blog-fig" style="padding:1rem;background:var(--sfondo)">
<svg viewBox="0 0 520 240" width="100%" height="240" role="img" aria-labelledby="omi-limena-title">
<title id="omi-limena-title">Lettura fasce OMI Limena — confronto qualitativo zone B1 e R1</title>
<text x="260" y="24" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Fasce OMI Limena (schema qualitativo — fonte: portale ADE)</text>
<rect x="30" y="45" width="200" height="70" rx="8" fill="#2C4A6E" opacity="0.9"/>
<text x="130" y="72" text-anchor="middle" font-size="11" fill="#fff" font-weight="600">Zona B1 (centrale)</text>
<text x="130" y="92" text-anchor="middle" font-size="9" fill="rgba(255,255,255,.85)">Min · Med · Max</text>
<text x="130" y="108" text-anchor="middle" font-size="8" fill="rgba(255,255,255,.7)">Semestre ADE corrente</text>
<rect x="290" y="45" width="200" height="70" rx="8" fill="#FF6B35" opacity="0.85"/>
<text x="390" y="72" text-anchor="middle" font-size="11" fill="#152435" font-weight="600">Zona R1 (residenziale)</text>
<text x="390" y="92" text-anchor="middle" font-size="9" fill="#152435">Min · Med · Max</text>
<text x="390" y="108" text-anchor="middle" font-size="8" fill="#152435">Verificare su OMI</text>
<rect x="60" y="135" width="400" height="85" rx="8" fill="#fff" stroke="#E1DBD1"/>
<text x="260" y="158" text-anchor="middle" font-size="10" fill="#6B7A8D">Non pubblichiamo €/mq inventati</text>
<text x="260" y="178" text-anchor="middle" font-size="9" fill="#2C4A6E">Consultare: agenziaentrate.gov.it → OMI → Limena</text>
<text x="260" y="198" text-anchor="middle" font-size="8" fill="#6B7A8D">Tipologia, stato e pertinenze modificano la fascia effettiva</text>
</svg>
<figcaption>Schema lettura zone OMI B1/R1 a Limena. Valori ufficiali solo sul portale ADE — semestre in corso.</figcaption>
</figure>"""


def svg_buyer_steps() -> str:
    return """<figure class="blog-fig" style="padding:1rem;background:var(--sfondo)">
<svg viewBox="0 0 520 280" width="100%" height="280" role="img" aria-labelledby="buyer-steps-title">
<title id="buyer-steps-title">Percorso acquirente appartamento Limena 2026</title>
<text x="260" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Percorso acquirente — Limena 2026</text>
<rect x="185" y="38" width="150" height="36" rx="18" fill="#2C4A6E"/><text x="260" y="61" text-anchor="middle" font-size="10" fill="#fff">1. Budget + mutuo</text>
<path d="M260 74 L260 92" stroke="#FF6B35" stroke-width="2"/>
<rect x="185" y="92" width="150" height="36" rx="18" fill="#2C4A6E"/><text x="260" y="115" text-anchor="middle" font-size="10" fill="#fff">2. OMI + annunci</text>
<path d="M260 128 L260 146" stroke="#FF6B35" stroke-width="2"/>
<rect x="185" y="146" width="150" height="36" rx="18" fill="#FF6B35"/><text x="260" y="169" text-anchor="middle" font-size="10" fill="#152435">3. Visite + checklist</text>
<path d="M260 182 L260 200" stroke="#FF6B35" stroke-width="2"/>
<rect x="185" y="200" width="150" height="36" rx="18" fill="#2C4A6E"/><text x="260" y="223" text-anchor="middle" font-size="10" fill="#fff">4. Proposta + rogito</text>
<text x="260" y="262" text-anchor="middle" font-size="8" fill="#6B7A8D">Fonte metodo: Righetto Immobiliare — consulenza Via Roma 96</text>
</svg>
<figcaption>Percorso operativo per acquisto appartamento a Limena: budget, OMI, visite documentate, proposta e rogito.</figcaption>
</figure>"""


def body_appartamento_acquisto() -> str:
    hero = "img/blog/blog-appartamento-limena-guida-acquisto-2026.webp"
    return f"""
{aeo_box("In sintesi", "Acquistare un <strong>appartamento a Limena</strong> nel 2026 richiede lettura delle <strong>fasce OMI ADE</strong> (zone B1/R1), attenzione alla <strong>classe energetica</strong>, checklist visita strutturata e confronto tra annunci comparabili. Non pubblichiamo €/mq inventati: fonte ufficiale il <a href=\"{OMI_URL}\" target=\"_blank\" rel=\"noopener noreferrer\">portale OMI</a>.")}

<p>Cercare un <strong>appartamento Limena</strong> significa entrare in un mercato di prima cintura padovana dove convivono famiglie stabili, pendolari verso il capoluogo e chi cerca metrature più generose rispetto al centro storico. Questa guida non duplica la panoramica generale del <a href=\"blog-mercato-immobiliare-limena-2026\">mercato immobiliare Limena 2026</a> né il confronto <a href=\"blog-limena-vs-padova-centro-dove-comprare-2026\">Limena vs Padova centro</a>: qui focalizziamo il <strong>percorso d'acquisto</strong> — budget, OMI, visite, mutuo e trattativa — con tono operativo Righetto.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#omi">Zone OMI B1 e R1 a Limena</a></li>
<li><a href="#classe-a">Classe energetica e costi futuri</a></li>
<li><a href="#checklist">Checklist visita appartamento</a></li>
<li><a href="#confronto">Confrontare annunci senza errori</a></li>
<li><a href="#mutuo">Mutuo e budget totale</a></li>
<li><a href="#rogito">Dalla proposta al rogito</a></li>
</ol></nav>

{sol_box("Voglio comprare appartamento a Limena — da dove inizio nel 2026?", [
    ("Valutazione comparativa", "Incrocio OMI vendita, annunci attivi e difetti da scontare in trattativa", "servizio valutazioni", "servizio-valutazioni"),
    ("Ricerca mirata", "Filtri tipologia, budget e zona Limena con alert nuove proposte", "catalogo immobili", "immobili"),
    ("Visite accompagnate", "Checklist tecnica e documentale in sopralluogo", "zona Limena", "zona-limena"),
    ("Coordinamento mutuo", "Tempistiche proposta, compromesso e rogito con banca", "consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
])}

<h2 id="omi">Come leggere le zone OMI B1 e R1 a Limena?</h2>
<p>L'<strong>Osservatorio del Mercato Immobiliare</strong> dell'Agenzia delle Entrate suddivide ogni comune in zone omogenee con fasce <em>minimo, medio e massimo</em> per tipologia e finalità (vendita o locazione). A Limena troverete designazioni come <strong>B1</strong> (aree centrali/servite) e <strong>R1</strong> (residenziale diffusa): non sono ranking di qualità assoluta, ma classificazioni statistiche per comparabili. Consultate il portale <a href=\"{OMI_URL}\" target=\"_blank\" rel=\"noopener noreferrer\">OMI quotazioni immobiliari</a> selezionando il comune, il semestre vigente e la tipologia abitativa.</p>
<p>L'errore più frequente è copiare un €/mq da un articolo generico o da un altro comune. Per Limena servono il semestre ADE corrente e la microzona dell'annuncio. Per il contesto macro provinciale: <a href=\"{ADE_OSSERVATORIO}\" target=\"_blank\" rel=\"noopener noreferrer\">Osservatorio ADE</a> e archivio <a href=\"{ISTAT_URL}\" target=\"_blank\" rel=\"noopener noreferrer\">ISTAT prezzi abitazioni</a>.</p>

{svg_omi_zone()}

<h2 id="classe-a">Perché la classe energetica conta nell'acquisto?</h2>
<p>Un appartamento in <strong>classe A</strong> (o B) riduce i costi di bolletta e migliora l'accesso al mutuo verde, ma il premium di prezzo va giustificato con APE valido, interventi documentati e confronto con comparabili classe inferiore nella stessa zona OMI. In cintura, molti edifici anni '80–'90 offrono potenziale di riqualificazione: l'acquirente deve stimare investimento futuro oltre il prezzo richiesto.</p>
<p>Approfondimenti correlati: <a href=\"blog-direttiva-case-green-limena-padova\">direttiva Case Green Limena-Padova</a> e <a href=\"blog-appartamento-nuova-costruzione-limena\">appartamento nuova costruzione Limena</a> — angoli distinti da questa guida acquisto.</p>

<h2 id="checklist">Checklist visita per appartamento Limena</h2>
<ol>
<li><strong>Planimetria catastale</strong> conforme allo stato di fatto — difformità non sanate bloccano mutuo e rogito.</li>
<li><strong>APE</strong> valido e coerente con infissi, caldaia e cappotto visibili.</li>
<li><strong>Condominio</strong>: ultimi verbali, spese ordinarie/straordinarie, fondo lavori.</li>
<li><strong>Acustica e luce</strong>: esposizione, rumore da viabilità, umidità in piani bassi.</li>
<li><strong>Pertinenze</strong>: box, cantina, posto auto — verificare titolarità in visura.</li>
<li><strong>Collegamenti</strong>: tempi reali verso Padova lavoro/studio nei giorni feriali.</li>
</ol>
<p>Lista errori comuni in visita: <a href=\"blog-5-errori-visita-immobile-padova-2026\">5 errori visita immobile Padova</a>.</p>

{blog_fig(hero, "Appartamento in vendita Limena — guida acquisto 2026", "Contesto acquisto residenziale Limena: prima cintura padovana, sede Righetto Via Roma 96.")}

{svg_buyer_steps()}

<h2 id="confronto">Come confrontare annunci senza confronti falsi?</h2>
<p>Filtrate per metratura commerciale ±10%, stessa tipologia (bilocale/trilocale), pertinenze simili e zona OMI comparabile. Un trilocale ristrutturato con box non si confronta con un bilocale al primo piano senza ascensore. Incrociate prezzo richiesto con fascia OMI e chiedete motivazione scritta del listino al venditore o all'agenzia.</p>
<p>Per chi legge solo portali: guida complementare <a href=\"blog-case-vendita-limena-leggere-annunci-2026\">case vendita Limena — leggere annunci</a>.</p>

{blog_fig("img/blog/blog-inline-posizione-padova-2026.webp", "Limena nella cintura nord Padova", "Posizione Limena rispetto al capoluogo — utile per valutare spostamenti quotidiani.")}

<h2 id="mutuo">Mutuo e budget totale</h2>
<p>Il prezzo in annuncio non è il costo totale: aggiungete imposte, notaio, perizia, eventuali lavori e arredo. Ottenete preventivo mutuo con lettera di fideiussione o pre-approvazione prima dell'offerta vincolante. La banca perizia l'immobile: se il valore OMI/perizia è inferiore al prezzo, l'anticipo sale.</p>

<h2 id="rogito">Dalla proposta al rogito</h2>
<p>Proposta scritta, compromesso con caparra, due diligence documentale (visure, APE, conformità), rogito notarile. Righetto coordina venditori e acquirenti sul territorio limenese dal 2000. {CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 5 agosto 2026.</p>
"""


def body_case_vendita_annunci() -> str:
    return f"""
{aeo_box("In sintesi", "Le <strong>case in vendita Limena</strong> si leggono annuncio per annuncio: titolo, foto, planimetria, <strong>prezzo vs OMI</strong> e segnali d'allarme. Questa guida non è un'analisi di mercato generale — per quella vedi <a href=\"blog-mercato-immobiliare-limena-2026\">mercato Limena 2026</a> — ma un manuale per <strong>decodificare le schede</strong> sui portali.")}

<p>Chi cerca <strong>casa vendita Limena</strong> su Idealista, Immobiliare.it o agenzie locali affronta decine di schede con linguaggi marketing, foto wide-angle e descrizioni copy-paste. Imparare a leggere un annuncio riduce visite inutili e trattative fallite. Fonte prezzi ufficiale: <a href=\"{OMI_URL}\" target=\"_blank\" rel=\"noopener noreferrer\">portale OMI ADE</a>.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#anatomia">Anatomia di un annuncio</a></li>
<li><a href="#redflag">Red flag e truffe</a></li>
<li><a href="#omi-prezzo">Prezzo richiesto vs OMI</a></li>
<li><a href="#foto">Foto e planimetria</a></li>
<li><a href="#agenzia">Annuncio agenzia vs privato</a></li>
</ol></nav>

{sol_box("Come capisco se un annuncio Limena è serio?", [
    ("Verifica documenti", "APE, planimetria e visura prima della caparra", "servizio valutazioni", "servizio-valutazioni"),
    ("Comparabili OMI", "Incrocio fascia min-med-max semestre corrente", "zona Limena", "zona-limena"),
    ("Visita qualificata", "Checklist tecnica in sopralluogo", "guida acquisto Limena", "blog-appartamento-limena-guida-acquisto-2026"),
    ("Supporto trattativa", "Proposta e coordinamento con venditore", "contatti", "contatti"),
])}

<h2 id="anatomia">Anatomia di un annuncio immobiliare</h2>
<p>Titolo efficace: tipologia + metratura + elemento distintivo reale (es. «Trilocale 95 mq con terrazzo — Limena centro»). Descrizione utile: anno costruzione/ristrutturazione, piano, ascensore, spese condominiali, stato impianti, distanza servizi. Mancanza di dati oggettivi è primo campanello.</p>

<h2 id="redflag">Red flag: quando diffidare</h2>
<ul>
<li>Prezzo nettamente sotto comparabili senza spiegazione (eredità, aste, problemi strutturali).</li>
<li>Rifiuto di mostrare planimetria catastale o APE prima della visita.</li>
<li>Richiesta bonifici prima di contratto registrato.</li>
<li>Foto che non includono bagno, cantina o lati mancanti dell'edificio.</li>
<li>«Trattativa riservata» senza range indicativo né motivazione.</li>
</ul>

<h2 id="omi-prezzo">Prezzo richiesto vs fascia OMI</h2>
<p>Scaricate la fascia OMI vendita per zona e tipologia. Listino sopra il <strong>massimo</strong> OMI richiede difendibilità (classe A, ristrutturazione completa, pertinenze). Listino sotto il <strong>minimo</strong> merita scetticismo: verificare vizi, occupazioni o errori materiale. Dati macro: <a href=\"{ADE_OSSERVATORIO}\" target=\"_blank\" rel=\"noopener noreferrer\">Osservatorio ADE</a>.</p>

<table>
<thead><tr><th>Segnale annuncio</th><th>Azione acquirente</th></tr></thead>
<tbody>
<tr><td>Prezzo in fascia OMI medio-alta</td><td>Chiedere comparabili venduti e motivazione lavori</td></tr>
<tr><td>Prezzo sopra massimo OMI</td><td>Richiedere elenco lavori + APE post-intervento</td></tr>
<tr><td>Prezzo sotto minimo OMI</td><td>Visita tecnica approfondita, visure complete</td></tr>
<tr><td>Dati catastali assenti</td><td>Non procedere senza foglio/particella/subalterno</td></tr>
</tbody>
</table>

{blog_fig("img/blog/blog-case-vendita-limena-leggere-annunci-2026.webp", "Case in vendita Limena — leggere annunci 2026")}

<h2 id="foto">Foto e planimetria: cosa guardare</h2>
<p>Foto professionali non nascondono difetti se la visita è completa. Controllate angoli soffitto, davanzali, pavimenti e vista da finestre. Planimetria catastale sovrapposta allo stato di fatto: cucine spostate, verande chiuse abusive, box non censiti sono rischi rogito.</p>

<h2 id="agenzia">Annuncio agenzia vs privato</h2>
<p>L'agenzia qualifica acquirenti, verifica mandato e centralizza documenti. Il privato può offrire risparmio su commissioni ma richiede più due diligence all'acquirente. In entrambi i casi: nessuna caparra senza contratto. Per acquisto strutturato: <a href=\"blog-appartamento-limena-guida-acquisto-2026\">guida acquisto appartamento Limena</a>. {CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 5 agosto 2026.</p>
"""


def body_affitto_contratto() -> str:
    return f"""
{aeo_box("In sintesi", "L'<strong>appartamento affitto Limena contratto</strong> nel 2026 si regola su <strong>4+4</strong> o canone concordato, <strong>deposito</strong> documentato, <strong>registrazione ADE</strong> e visite mirate. Diverso dalla guida generale <a href=\"blog-affitti-limena-2026\">affitti Limena 2026</a> (canoni e quartieri): qui focus <strong>documenti e obblighi</strong>.")}

<p>Affittare a Limena implica leggere il contratto riga per riga, non solo il canone in vetrina. Fonte ufficiale fasce locazione: <a href=\"{OMI_URL}\" target=\"_blank\" rel=\"noopener noreferrer\">OMI locazione ADE</a>. Per contratti nel capoluogo: <a href=\"blog-contratto-affitto-padova\">guida contratto affitto Padova</a>.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#tipi">Tipi di contratto</a></li>
<li><a href="#deposito">Deposito e caparra</a></li>
<li><a href="#registrazione">Registrazione telematica</a></li>
<li><a href="#visite">Visite per inquilini</a></li>
<li><a href="#uscita">Recesso e rinnovo</a></li>
</ol></nav>

{sol_box("Devo firmare contratto affitto Limena — cosa verifico?", [
    ("Redazione contratto", "4+4, 3+2, transitorio o concordato — clausole chiare", "servizio locazioni", "servizio-locazioni"),
    ("Registrazione ADE", "Entro 30 giorni — ricevuta a entrambe le parti", "servizio locazioni", "servizio-locazioni"),
    ("Inventario e foto", "Stato immobile a ingresso per evitare contestazioni", "affitti Limena", "blog-affitti-limena-2026"),
    ("Qualifica inquilino", "Referenze e documenti per proprietari", "contatti", "contatti"),
])}

<h2 id="tipi">Tipi di contratto più usati</h2>
<p><strong>4+4 a canone libero</strong>: standard residenziale, rinnovo tacito, recesso inquilino con preavviso. <strong>Canone concordato</strong>: canone vincolato, agevolazioni fiscali, requisiti zona e tipologia. <strong>3+2</strong> e <strong>transitorio</strong>: casi specifici — non usare transitorio se non ricorrono i presupposti di legge.</p>

<h2 id="deposito">Deposito cauzionale e caparra</h2>
<p>La <strong>cauzione</strong> (max tre mensilità per uso abitativo) va restituita a fine locazione se immobile restituito in ordine. La <strong>caparra confirmatoria</strong> ha effetti diversi in caso di inadempimento — leggete la clausola con attenzione. Mai versare contanti senza ricevuta intestata.</p>

<h2 id="registrazione">Registrazione presso l'Agenzia delle Entrate</h2>
<p>Il contratto va registrato telematicamente entro 30 giorni dalla stipula. Senza registrazione: problemi con detrazioni, contestazioni e certificazione residenza. Il locatore è obbligato primario; in pratica spesso si ripartiscono costi come da accordo scritto.</p>

{blog_fig("img/blog/blog-appartamento-affitto-limena-contratto-2026.webp", "Contratto affitto appartamento Limena 2026", "Documentazione e registrazione: tappa obbligata per locazione seria.")}

<h2 id="visite">Visite mirate per inquilini</h2>
<ul>
<li>Verificare pressione acqua, scarichi, caldaia e caldaia/libretto impianti.</li>
<li>Chiedere regolamento condominiale (animali, orari, box).</li>
<li>Testare cellulare in ogni stanza se lavorate da remoto.</li>
<li>Confermare spese incluse/escluse (riscaldamento, condominio, TARI).</li>
</ul>

<h2 id="uscita">Recesso, rinnovo e proroghe</h2>
<p>Preavviso per recesso inquilino: termini per legge nel 4+4. Rinnovo tacito al termine primo quadriennio. Per proroghe COVID o eccezioni: verificare normativa vigente alla data di firma. {CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 5 agosto 2026.</p>
"""


def body_bilocale_trilocale() -> str:
    return f"""
{aeo_box("In sintesi", "Scegliere tra <strong>bilocale e trilocale Limena</strong> nel 2026 dipende da nucleo familiare, budget legato a <strong>OMI</strong>, spostamenti verso Padova e bisogno di spazio studio. Confronto operativo per famiglie e pendolari — non ranking assoluto.")}

<p>La query <strong>bilocale trilocale limena</strong> riflette un dilemma concreto: risparmiare metratura o investire in una camera in più. Limena, a circa 8 km da Padova, attira chi accetta pochi minuti in auto per avere soggiorno più ampio e terrazzo. Dati ufficiali: <a href=\"{OMI_URL}\" target=\"_blank\" rel=\"noopener noreferrer\">OMI ADE</a>.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#profili">Profili acquirente/inquilino</a></li>
<li><a href="#tabella">Tabella comparativa</a></li>
<li><a href="#famiglie">Famiglie con bambini</a></li>
<li><a href="#pendolari">Pendolari e smart worker</a></li>
<li><a href="#costi">Costi totali oltre il canone/prezzo</a></li>
</ol></nav>

{sol_box("Bilocale o trilocale a Limena per la mia famiglia?", [
    ("Analisi fabbisogno", "Stanze, remote work, bambini — scenario 5 anni", "consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
    ("Comparabili OMI", "Fasce per tipologia sullo stesso semestre", "mercato Limena", "blog-mercato-immobiliare-limena-2026"),
    ("Visite mirate", "Solo immobili coerenti con budget reale", "immobili", "immobili"),
    ("Limena vs centro", "Trade-off metratura/spostamento", "Limena vs Padova", "blog-limena-vs-padova-centro-dove-comprare-2026"),
])}

<h2 id="profili">Chi sceglie il bilocale e chi il trilocale?</h2>
<p><strong>Bilocale</strong>: coppie, single, coppie senza figli, investitori locazione a inquilini giovani. <strong>Trilocale</strong>: famiglie con uno o due figli, coppie con studio permanente, genitori ospiti frequenti. A Limena il trilocale con giardino o terrazzo ha domanda familiare stabile.</p>

<h2 id="tabella">Tabella comparativa qualitativa</h2>
<table>
<thead><tr><th>Criterio</th><th>Bilocale Limena</th><th>Trilocale Limena</th></tr></thead>
<tbody>
<tr><td>Target</td><td>Coppie, pendolari singoli</td><td>Famiglie, smart worker con figli</td></tr>
<tr><td>Metratura tipica</td><td>55–75 mq circa</td><td>80–110 mq circa</td></tr>
<tr><td>Budget (OMI)</td><td>Fascia inferiore stessa zona</td><td>Fascia superiore — verificare ADE</td></tr>
<tr><td>Spostamenti</td><td>Spesso più vicino servizi</td><td>Spesso zone residenziali con auto</td></tr>
<tr><td>Locazione</td><td>Turnover potenzialmente più alto</td><td>Contratti più lunghi famiglia</td></tr>
</tbody>
</table>

{blog_fig("img/blog/blog-bilocale-trilocale-limena-scelta-2026.webp", "Bilocale vs trilocale Limena 2026", "Confronto tipologie per famiglie e pendolari nella cintura padovana.")}

<h2 id="famiglie">Famiglie: quando il trilocale è quasi obbligato</h2>
<p>Camera bambini, zona giorno separata e secondo bagno riducono stress quotidiano. Il bilocale funziona con bambino piccolo solo se accettate open space notturno. Verificate scuole e asili nel raggio — Limena offre servizi consolidati.</p>

<h2 id="pendolari">Pendolari: bilocale può bastare</h2>
<p>Chi passa le giornate a Padova e rientra la sera spesso privilegia bilocale ben servito vicino a fermate bus o accesso tangenziale. Il risparmio su rata o canone può finanziare auto o abbonamenti.</p>

<h2 id="costi">Costi totali: oltre la tipologia</h2>
<p>Condominio, riscaldamento, IMU (se proprietario), manutenzione: un trilocale costa più del bilocale non solo in acquisto. Calcolate scenario 7–10 anni. Guida acquisto: <a href=\"blog-appartamento-limena-guida-acquisto-2026\">appartamento Limena acquisto</a>. {CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 5 agosto 2026.</p>
"""


def body_gruppo_righetto() -> str:
    return f"""
{aeo_box("In sintesi", "<strong>Gruppo Immobiliare Righetto Limena</strong>: sede <strong>Via Roma 96</strong>, dal <strong>2000</strong>, <strong>350+ immobili</strong> in <strong>101 comuni</strong>, <strong>127 recensioni Google 4,9/5</strong>, <strong>98% soddisfazione</strong>. Diverso da <a href=\"blog-righetto-storia-territorio-acquisizioni-2026\">storia e acquisizioni</a> e da <a href=\"blog-agenzia-immobiliare-limena-come-scegliere-2026\">come scegliere agenzia Limena</a>: qui <strong>brand e servizi</strong> verificabili.")}

<p>Chi cerca <strong>gruppo immobiliare righetto limena</strong> vuole un referente locale con tracciabilità: indirizzo fisico, recensioni, anni di attività e servizi chiari. Non pubblichiamo percentuali di mediazione online — si concordano in sede nel mandato.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#sede">Via Roma 96 e territorio</a></li>
<li><a href="#numeri">Numeri verificabili</a></li>
<li><a href="#servizi">Servizi acquisto, vendita, locazione</a></li>
<li><a href="#recensioni">Recensioni e E-E-A-T</a></li>
<li><a href="#differenze">Cosa non è questo articolo</a></li>
</ol></nav>

{sol_box("Perché scegliere Righetto a Limena nel 2026?", [
    ("Valutazioni immobiliari", "OMI e comparabili per vendita o acquisto", "servizio valutazioni", "servizio-valutazioni"),
    ("Vendita immobile", "Marketing, visite, trattativa fino al rogito", "servizio vendita", "servizio-vendita"),
    ("Locazioni", "Contratti registrati, qualifica inquilini", "servizio locazioni", "servizio-locazioni"),
    ("Consulenza gratuita", "Appuntamento in sede Limena", "landing", "landing-consulenza-immobiliare-gratuita"),
])}

<h2 id="sede">Sede Limena: Via Roma 96</h2>
<p>La sede operativa in <strong>Via Roma 96, 35010 Limena (PD)</strong> non è un call center anonimo: è il punto di incontro per valutazioni, firme mandato, consegna chiavi e consulenze. Coordinate verificabili su Google Maps e recensioni. Pagina territorio: <a href=\"zona-limena\">zona Limena</a>.</p>

<div class="kpi-strip">
<div><strong>2000</strong><span>Dal</span></div>
<div><strong>350+</strong><span>Immobili</span></div>
<div><strong>101</strong><span>Comuni</span></div>
<div><strong>4,9/5</strong><span>127 recensioni</span></div>
</div>

<h2 id="numeri">Numeri che possiamo citare</h2>
<p>Oltre <strong>350 immobili</strong> gestiti nel corso dell'attività, copertura su <strong>101 comuni</strong> del Padovano e oltre, <strong>98% di soddisfazione</strong> clienti dichiarata con <strong>127 recensioni Google</strong> a media <strong>4,9 su 5</strong> (verificabile su Google Business Profile). Non aggiungiamo claim non supportati.</p>

<h2 id="servizi">Servizi per proprietari e acquirenti</h2>
<ul>
<li><strong>Acquisto</strong>: ricerca, visite, proposta, coordinamento notarile — <a href=\"blog-appartamento-limena-guida-acquisto-2026\">guida acquisto Limena</a>.</li>
<li><strong>Vendita</strong>: valutazione OMI, piano marketing, trattativa — <a href=\"servizio-vendita\">servizio vendita</a>.</li>
<li><strong>Locazione</strong>: contratto, registrazione, selezione inquilini — <a href=\"servizio-locazioni\">servizio locazioni</a>.</li>
<li><strong>Valutazioni</strong>: stima comparativa documentata — <a href=\"servizio-valutazioni\">servizio valutazioni</a>.</li>
</ul>

{blog_fig("img/blog/blog-gruppo-immobiliare-righetto-limena-2026.webp", "Gruppo Immobiliare Righetto Limena", "Sede Via Roma 96 — agenzia immobiliare dal 2000.")}

<h2 id="recensioni">Recensioni, esperienza e trasparenza</h2>
<p>L'E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) per Google passa da contenuti firmati, dati verificabili e presenza reale. Gino Capon e il team pubblicano guide locali (mercato Limena, affitti, confronti Padova) con fonti ADE/OMI, senza inventare prezzi.</p>

<h2 id="differenze">Cosa trovate altrove sul blog</h2>
<p><a href=\"blog-righetto-storia-territorio-acquisizioni-2026\">Storia territorio e acquisizioni</a>: racconto portafoglio e vita d'agenzia. <a href=\"blog-agenzia-immobiliare-limena-come-scegliere-2026\">Come scegliere agenzia Limena</a>: checklist per venditori/acquirenti. Questo articolo è la scheda istituzionale <strong>gruppo immobiliare Righetto Limena</strong>.</p>

<p>Tel. <a href=\"tel:+390498843484\">049.8843484</a> · <a href=\"contatti\">contatti</a> · <a href=\"immobili\">catalogo immobili</a>. {CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 5 agosto 2026.</p>
"""


ARTICLES: list[dict] = [
    {
        "slug": "blog-appartamento-limena-guida-acquisto-2026",
        "filename": "blog-appartamento-limena-guida-acquisto-2026.html",
        "hero": "img/blog/blog-appartamento-limena-guida-acquisto-2026.webp",
        "lang": "it",
        "title": "Appartamento Limena: Guida acquisto 2026",
        "og_title": "Appartamento a Limena: come acquistare senza errori (2026)",
        "meta": "Guida acquisto appartamento Limena 2026: OMI ADE, classe A, checklist visita e mutuo. Righetto Via Roma 96 — senza €/mq inventati.",
        "schema_headline": "Appartamento Limena: guida acquisto 2026 senza errori",
        "section": "Limena locale",
        "cat_badge": "Limena · Acquisto",
        "bread_crumb": "Appartamento Limena acquisto",
        "h1": "<strong>Appartamento Limena</strong>: guida acquisto 2026",
        "hero_alt": "Appartamento in vendita Limena guida acquisto 2026",
        "body_fn": lambda: expand_body(body_appartamento_acquisto, EXPANSION_LIMENA, _batch.EXPANSION_IT_DOMANDA),
        "faqs": [
            ("Come acquistare appartamento a Limena nel 2026?", "Definire budget e mutuo, consultare OMI ADE per zona e tipologia, visitare con checklist documentale, confrontare comparabili e presentare proposta scritta."),
            ("Dove trovo i prezzi ufficiali Limena?", "Sul portale OMI dell'Agenzia delle Entrate, semestre corrente, selezionando comune Limena e tipologia abitativa vendita."),
            ("Cosa sono zone OMI B1 e R1?", "Zone omogenee statistiche ADE: B1 aree centrali/servite, R1 residenziale. Non sono giudizi di qualità assoluta ma fasce min-med-max per comparabili."),
            ("Serve classe energetica A?", "Non obbligatoria per comprare, ma incide su bollette, mutuo verde e rivendita. Verificare APE e coerenza con impianti visibili."),
            ("Righetto aiuta nell'acquisto?", "Sì — ricerca, visite, valutazione OMI e coordinamento trattativa da Via Roma 96 Limena dal 2000. Compenso concordato in sede."),
            ("Differenza vs mercato Limena generale?", "Questa guida è percorso acquirente; l'articolo mercato Limena 2026 tratta trend e contesto comunale."),
        ],
        "related": [
            ("Mercato Limena 2026", "blog-mercato-immobiliare-limena-2026"),
            ("Limena vs Padova centro", "blog-limena-vs-padova-centro-dove-comprare-2026"),
            ("Zona Limena", "zona-limena"),
            ("Valutazioni", "servizio-valutazioni"),
        ],
        "registry": {
            "titolo": "Appartamento Limena: Guida acquisto 2026",
            "categoria": "Limena locale",
            "tempo": 14,
            "contenuto": "Acquisto appartamento Limena: OMI B1/R1, classe A, checklist visita, mutuo e confronto annunci.",
            "evidenza": False,
            "emoji": "🏠",
            "admin_contenuto": "<p>Guida acquisto appartamento Limena 2026: OMI ADE, energia, visite e mutuo.</p>",
        },
        "static_map_key": "appartamento limena: guida acquisto 2026",
    },
    {
        "slug": "blog-case-vendita-limena-leggere-annunci-2026",
        "filename": "blog-case-vendita-limena-leggere-annunci-2026.html",
        "hero": "img/blog/blog-case-vendita-limena-leggere-annunci-2026.webp",
        "lang": "it",
        "title": "Case vendita Limena: Leggere annunci 2026",
        "og_title": "Case in vendita Limena: come leggere annunci e red flag (2026)",
        "meta": "Case vendita Limena: leggere annunci, red flag, prezzo OMI vs richiesta. Guida 2026 Righetto — senza €/mq inventati né tariffe online.",
        "schema_headline": "Case vendita Limena: come leggere annunci nel 2026",
        "section": "Limena locale",
        "cat_badge": "Limena · Annunci",
        "bread_crumb": "Case vendita annunci",
        "h1": "<strong>Case vendita Limena</strong>: leggere annunci 2026",
        "hero_alt": "Case in vendita Limena leggere annunci 2026",
        "body_fn": lambda: expand_body(body_case_vendita_annunci, EXPANSION_LIMENA, _batch.EXPANSION_IT_DOMANDA),
        "faqs": [
            ("Come leggere un annuncio vendita Limena?", "Verificare tipologia, metratura, piano, APE, planimetria, prezzo vs OMI e coerenza foto-descrizione."),
            ("Quali red flag negli annunci?", "Prezzo anomalo, assenza documenti, bonifici anticipati, foto incomplete, rifiuto visite tecniche."),
            ("Prezzo richiesto vs OMI?", "Confrontare con fascia min-med-max semestre ADE per zona e tipologia; premium va giustificato."),
            ("Meglio agenzia o privato?", "Entrambi validi; agenzia centralizza documenti e qualifica. Due diligence sempre all'acquirente."),
            ("Dove consulto OMI?", "Portale Agenzia delle Entrate, banche dati quotazioni immobiliari, comune Limena."),
            ("Articolo diverso da mercato Limena?", "Sì — qui focus lettura schede annuncio, non panoramica mercato generale."),
        ],
        "related": [
            ("Guida acquisto Limena", "blog-appartamento-limena-guida-acquisto-2026"),
            ("Mercato Limena", "blog-mercato-immobiliare-limena-2026"),
            ("Errori in visita", "blog-5-errori-visita-immobile-padova-2026"),
            ("Valutazioni", "servizio-valutazioni"),
        ],
        "registry": {
            "titolo": "Case vendita Limena: Leggere annunci 2026",
            "categoria": "Limena locale",
            "tempo": 13,
            "contenuto": "Decodificare annunci vendita Limena: red flag, OMI vs prezzo, foto e planimetria.",
            "evidenza": False,
            "emoji": "📋",
            "admin_contenuto": "<p>Come leggere annunci case vendita Limena: OMI, red flag e comparabili.</p>",
        },
        "static_map_key": "case vendita limena: leggere annunci 2026",
    },
    {
        "slug": "blog-appartamento-affitto-limena-contratto-2026",
        "filename": "blog-appartamento-affitto-limena-contratto-2026.html",
        "hero": "img/blog/blog-appartamento-affitto-limena-contratto-2026.webp",
        "lang": "it",
        "title": "Appartamento affitto Limena: Contratto 2026",
        "og_title": "Affitto Limena: contratto, deposito e registrazione (2026)",
        "meta": "Appartamento affitto Limena contratto 2026: 4+4, deposito, registrazione ADE e visite inquilini. Diverso da guida affitti generale.",
        "schema_headline": "Appartamento affitto Limena: guida contratto 2026",
        "section": "Limena locale",
        "cat_badge": "Limena · Affitto",
        "bread_crumb": "Affitto contratto Limena",
        "h1": "<strong>Appartamento affitto Limena</strong>: contratto 2026",
        "hero_alt": "Contratto affitto appartamento Limena 2026",
        "body_fn": lambda: expand_body(body_affitto_contratto, EXPANSION_LIMENA, _batch.EXPANSION_IT_DOMANDA),
        "faqs": [
            ("Che contratto per affitto Limena?", "4+4 canone libero è lo standard; canone concordato, 3+2 e transitorio per casi specifici con requisiti di legge."),
            ("Quanto deposito cauzionale?", "Fino a tre mensilità per uso abitativo; restituzione a fine locazione se immobile in ordine."),
            ("Registrazione obbligatoria?", "Sì, entro 30 giorni all'Agenzia delle Entrate; ricevuta necessaria per detrazioni e certificazioni."),
            ("Differenza da affitti Limena 2026?", "Quell'articolo tratta canoni e quartieri; questo focus contratto, deposito, registrazione e visite."),
            ("Visite cosa controllare?", "Impianti, acqua, condominio, cellulare, spese incluse/escluse, inventario fotografico ingresso."),
            ("Righetto gestisce locazioni?", "Sì — redazione, registrazione, qualifica inquilini. Compenso concordato in sede."),
        ],
        "related": [
            ("Affitti Limena 2026", "blog-affitti-limena-2026"),
            ("Contratto affitto Padova", "blog-contratto-affitto-padova"),
            ("Servizio locazioni", "servizio-locazioni"),
            ("Zona Limena", "zona-limena"),
        ],
        "registry": {
            "titolo": "Appartamento affitto Limena: Contratto 2026",
            "categoria": "Limena locale",
            "tempo": 13,
            "contenuto": "Contratto affitto Limena: 4+4, deposito, registrazione ADE e checklist visite inquilini.",
            "evidenza": False,
            "emoji": "📝",
            "admin_contenuto": "<p>Affitto Limena: contratto, caparra, registrazione e visite per inquilini.</p>",
        },
        "static_map_key": "appartamento affitto limena: contratto 2026",
    },
    {
        "slug": "blog-bilocale-trilocale-limena-scelta-2026",
        "filename": "blog-bilocale-trilocale-limena-scelta-2026.html",
        "hero": "img/blog/blog-bilocale-trilocale-limena-scelta-2026.webp",
        "lang": "it",
        "title": "Bilocale trilocale Limena: Scelta 2026",
        "og_title": "Bilocale o trilocale Limena? Guida famiglie e pendolari 2026",
        "meta": "Bilocale vs trilocale Limena 2026: confronto famiglie e pendolari Padova, budget OMI, metrature. Guida Righetto senza prezzi inventati.",
        "schema_headline": "Bilocale o trilocale Limena: guida scelta 2026",
        "section": "Limena locale",
        "cat_badge": "Limena · Tipologie",
        "bread_crumb": "Bilocale trilocale Limena",
        "h1": "<strong>Bilocale o trilocale Limena</strong>: guida scelta 2026",
        "hero_alt": "Bilocale vs trilocale Limena confronto 2026",
        "body_fn": lambda: expand_body(body_bilocale_trilocale, EXPANSION_LIMENA, _batch.EXPANSION_IT_DOMANDA),
        "faqs": [
            ("Meglio bilocale o trilocale Limena?", "Bilocale per coppie/pendolari; trilocale per famiglie con figli o bisogno studio separato. Dipende da budget OMI e abitudini."),
            ("Famiglia con un figlio: basta bilocale?", "Possibile fino a 3–4 anni; poi camera separata migliora qualità vita. Valutare orizzonte 5–7 anni."),
            ("Pendolare: conviene bilocale?", "Spesso sì — risparmio su rata/canone e prossimità fermate o tangenziale."),
            ("Dove verifico prezzi per tipologia?", "OMI ADE per comune Limena, stesso semestre, tipologia abitativa vendita o locazione."),
            ("Limena vs Padova centro metrature?", "Limena offre spazi più ampi a parità budget — vedi confronto Limena vs centro."),
            ("Righetto aiuta a scegliere?", "Consulenza gratuita in sede per scenario familiare e comparabili."),
        ],
        "related": [
            ("Guida acquisto Limena", "blog-appartamento-limena-guida-acquisto-2026"),
            ("Limena vs Padova", "blog-limena-vs-padova-centro-dove-comprare-2026"),
            ("Mercato Limena", "blog-mercato-immobiliare-limena-2026"),
            ("Immobili", "immobili"),
        ],
        "registry": {
            "titolo": "Bilocale trilocale Limena: Scelta 2026",
            "categoria": "Limena locale",
            "tempo": 12,
            "contenuto": "Confronto bilocale vs trilocale Limena per famiglie e pendolari: OMI, metrature, costi.",
            "evidenza": False,
            "emoji": "📐",
            "admin_contenuto": "<p>Bilocale o trilocale Limena: guida scelta per famiglie e pendolari 2026.</p>",
        },
        "static_map_key": "bilocale trilocale limena: scelta 2026",
    },
    {
        "slug": "blog-gruppo-immobiliare-righetto-limena-2026",
        "filename": "blog-gruppo-immobiliare-righetto-limena-2026.html",
        "hero": "img/blog/blog-gruppo-immobiliare-righetto-limena-2026.webp",
        "lang": "it",
        "title": "Gruppo Immobiliare Righetto Limena 2026",
        "og_title": "Gruppo Immobiliare Righetto Limena: Via Roma 96, dal 2000",
        "meta": "Gruppo Immobiliare Righetto Limena: Via Roma 96, 350+ immobili, 127 recensioni 4,9/5 dal 2000. Servizi acquisto, vendita e locazione.",
        "schema_headline": "Gruppo Immobiliare Righetto Limena: sede, servizi e recensioni",
        "section": "Limena locale",
        "cat_badge": "Righetto · Limena",
        "bread_crumb": "Gruppo Righetto Limena",
        "h1": "<strong>Gruppo Immobiliare Righetto</strong> a Limena nel 2026",
        "hero_alt": "Gruppo Immobiliare Righetto Limena Via Roma 96",
        "body_fn": lambda: expand_body(body_gruppo_righetto, EXPANSION_LIMENA, _batch.EXPANSION_IT_DOMANDA),
        "faqs": [
            ("Dove si trova Righetto a Limena?", "Via Roma 96, 35010 Limena (PD) — sede operativa verificabile su mappe e recensioni."),
            ("Da quando opera Righetto?", "Dal 2000 su Padova e provincia, 101 comuni coperti."),
            ("Quante recensioni Google?", "127 recensioni con media 4,9 su 5 — verificabile su Google Business Profile."),
            ("Pubblicate commissioni online?", "No — compenso di mediazione concordato in sede nel mandato."),
            ("Differenza vs storia territorio?", "Storia/acquisizioni è racconto portafoglio; questo articolo è scheda istituzionale servizi Limena."),
            ("Servizi offerti?", "Acquisto, vendita, locazione, valutazioni — catalogo immobili online e consulenza in sede."),
        ],
        "related": [
            ("Agenzia Limena come scegliere", "blog-agenzia-immobiliare-limena-come-scegliere-2026"),
            ("Storia e acquisizioni", "blog-righetto-storia-territorio-acquisizioni-2026"),
            ("Zona Limena", "zona-limena"),
            ("Contatti", "contatti"),
        ],
        "registry": {
            "titolo": "Gruppo Immobiliare Righetto Limena 2026",
            "categoria": "Limena locale",
            "tempo": 11,
            "contenuto": "Brand Righetto Limena: Via Roma 96, 350+ immobili, 127 recensioni 4,9/5, servizi dal 2000.",
            "evidenza": False,
            "emoji": "🏢",
            "admin_contenuto": "<p>Gruppo Immobiliare Righetto Limena: sede, numeri verificabili e servizi E-E-A-T.</p>",
        },
        "static_map_key": "gruppo immobiliare righetto limena 2026",
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


def main() -> None:
    results: list[dict] = []
    slugs: list[str] = []

    for cfg in ARTICLES:
        body = cfg["body_fn"]()
        words = wc(body)
        if words < MIN_BODY_WORDS:
            raise SystemExit(f"{cfg['slug']}: corpo {words} parole < {MIN_BODY_WORDS}")
        out = ROOT / cfg["filename"]
        out.write_text(build_html(cfg, body, words), encoding="utf-8")
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

    print("\n-- Riepilogo Limena GSC ago 2026 --")
    for r in results:
        print(f"  • {r['file']} ({r['words']} parole)")
    print("  • blog.html, admin.html, sitemap.xml, homepage.js")


if __name__ == "__main__":
    main()
