# -*- coding: utf-8 -*-
"""Pillar eq-sep11-001 — vendere casa Limena proprietario 2026.
python scripts/build_blog_vendere_casa_limena_sep11.py
"""
from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE_IT = "11 settembre 2026"
DATE_ISO = "2026-09-11"
TIME_TS = "2026-09-11T10:00:00+02:00"
QUEUE_ID = "eq-sep11-001"

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
SLUG = "blog-vendere-casa-limena-proprietario-2026"

IMAGE_SOURCES: dict[str, tuple[str, str] | list[tuple[str, str]]] = {
    "hero": (
        "img/blog/blog-case-vendita-limena-leggere-annunci-2026.webp",
        "img/blog/blog-vendere-casa-limena-proprietario-2026-hero.webp",
    ),
    "body": [
        (
            "img/blog/blog-agenzia-immobiliare-limena-come-scegliere-2026.webp",
            "img/blog/blog-vendere-casa-limena-proprietario-2026-valutazione.webp",
        ),
        (
            "img/blog/blog-appartamento-limena-guida-acquisto-2026.webp",
            "img/blog/blog-vendere-casa-limena-proprietario-2026-documenti.webp",
        ),
        (
            "img/blog/blog-gruppo-immobiliare-righetto-limena-2026.webp",
            "img/blog/blog-vendere-casa-limena-proprietario-2026-marketing.webp",
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


def svg_percorso_vendita() -> str:
    return """<figure class="chart-wrap" aria-label="Percorso vendita casa Limena proprietario">
<svg viewBox="0 0 560 280" width="100%" height="280" role="img">
<title>Percorso vendita casa Limena — 6 fasi proprietario</title>
<text x="280" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Vendere a Limena: percorso operativo 2026</text>
<rect x="20" y="50" width="80" height="36" rx="8" fill="#2C4A6E"/><text x="60" y="72" text-anchor="middle" font-size="7" fill="#fff">1. Valutazione</text>
<path d="M100 68 L115 68" stroke="#FF6B35" stroke-width="2"/>
<rect x="120" y="50" width="80" height="36" rx="8" fill="#3A5F8C"/><text x="160" y="72" text-anchor="middle" font-size="7" fill="#fff">2. Documenti</text>
<path d="M200 68 L215 68" stroke="#FF6B35" stroke-width="2"/>
<rect x="220" y="50" width="80" height="36" rx="8" fill="#FF6B35" opacity="0.9"/><text x="260" y="72" text-anchor="middle" font-size="7" fill="#152435">3. Mandato</text>
<path d="M300 68 L315 68" stroke="#FF6B35" stroke-width="2"/>
<rect x="320" y="50" width="80" height="36" rx="8" fill="#2C4A6E"/><text x="360" y="72" text-anchor="middle" font-size="7" fill="#fff">4. Marketing</text>
<path d="M400 68 L415 68" stroke="#FF6B35" stroke-width="2"/>
<rect x="420" y="50" width="60" height="36" rx="8" fill="#3A5F8C"/><text x="450" y="72" text-anchor="middle" font-size="7" fill="#fff">5. Trattativa</text>
<path d="M480 68 L495 68" stroke="#FF6B35" stroke-width="2"/>
<rect x="500" y="50" width="40" height="36" rx="8" fill="#2C4A6E"/><text x="520" y="72" text-anchor="middle" font-size="6" fill="#fff">Rogito</text>
<text x="280" y="120" text-anchor="middle" font-size="9" fill="#6B7A8D">Limena: cintura padovana — domanda famiglie e pendolari verso Padova/Mestre</text>
<text x="280" y="200" text-anchor="middle" font-size="8" fill="#6B7A8D">Fonte metodo: Righetto Immobiliare Via Roma 96 · OMI ADE per fascia zonale</text>
</svg>
<figcaption>Sequenza consigliata per il proprietario limenese: valutazione, dossier, mandato, promozione, trattativa e rogito.</figcaption>
</figure>"""


def svg_mandato_confronto() -> str:
    return """<figure class="chart-wrap" aria-label="Confronto mandato esclusivo e non esclusivo">
<svg viewBox="0 0 520 220" width="100%" height="220" role="img">
<title>Mandato esclusivo vs non esclusivo vendita Limena</title>
<text x="260" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Mandato vendita — cosa cambia per il proprietario</text>
<rect x="40" y="45" width="200" height="70" rx="10" fill="#2C4A6E"/>
<text x="140" y="68" text-anchor="middle" font-size="10" fill="#fff" font-weight="600">Esclusiva</text>
<text x="140" y="86" text-anchor="middle" font-size="8" fill="rgba(255,255,255,.85)">Un referente · piano marketing</text>
<text x="140" y="102" text-anchor="middle" font-size="7" fill="rgba(255,255,255,.7)">Coordinamento visite</text>
<rect x="280" y="45" width="200" height="70" rx="10" fill="#E1DBD1"/>
<text x="380" y="68" text-anchor="middle" font-size="10" fill="#152435" font-weight="600">Non esclusiva</text>
<text x="380" y="86" text-anchor="middle" font-size="8" fill="#6B7A8D">Più agenzie · listini diversi</text>
<text x="380" y="102" text-anchor="middle" font-size="7" fill="#6B7A8D">Rischio annunci duplicati</text>
<text x="260" y="155" text-anchor="middle" font-size="9" fill="#6B7A8D">Compenso mediazione sempre concordato in sede — nessun listino percentuale online</text>
<text x="260" y="195" text-anchor="middle" font-size="8" fill="#6B7A8D">Approfondimento: blog-mandato-esclusivo-padova-perche-conviene-2026</text>
</svg>
<figcaption>Schema qualitativo mandato esclusivo vs non esclusivo. La scelta va fatta con l'agenzia dopo valutazione dell'immobile.</figcaption>
</figure>"""


def body_vendere_limena() -> str:
    return f"""
{aeo_box("In sintesi", "Per <strong>vendere casa a Limena</strong> nel 2026 servono valutazione allineata a <strong>OMI ADE</strong>, dossier documentale completo, scelta del <strong>mandato</strong> e marketing coerente. Righetto — sede in <strong>Via Roma 96, Limena</strong> — accompagna il proprietario dalla stima al rogito. Diverso da <a href=\"blog-case-vendita-limena-leggere-annunci-2026\">leggere annunci</a>: qui il percorso di chi <em>vende</em>.")}

<p><strong>Distinzione editoriale:</strong> <em>Fatto</em> — norme catastali, APE obbligatorio, registrazione contratti. <em>Analisi</em> — tempi e appeal del mercato limenese rispetto al centro Padova. <em>Previsione</em> — nessuna garanzia su giorni di vendita: dipende da prezzo, stato immobile e domanda del semestre.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#perche-limena">Perché vendere a Limena nel 2026</a></li>
<li><a href="#quando">Quando ha senso mettere in vendita</a></li>
<li><a href="#valutazione">Valutazione e prezzo di uscita</a></li>
<li><a href="#documenti">Documenti prima dell'annuncio</a></li>
<li><a href="#mandato">Mandato e scelta agenzia</a></li>
<li><a href="#marketing">Marketing e visite</a></li>
<li><a href="#trattativa">Trattativa, compromesso e rogito</a></li>
<li><a href="#fiscalita">Fiscalità e plusvalenza</a></li>
<li><a href="#tipologie">Bilocale, trilocale o villa: cosa cambia</a></li>
<li><a href="#visite">Come prepararsi alle visite</a></li>
<li><a href="#errori">Errori frequenti del venditore</a></li>
<li><a href="#prossimi-passi">Prossimi passi</a></li>
</ol></nav>

<div class="kpi-strip" aria-label="Contesto vendita Limena">
<div><strong>Limena</strong><span>Cintura Padova</span></div>
<div><strong>OMI</strong><span>Fascia ADE ufficiale</span></div>
<div><strong>2000</strong><span>Righetto dal</span></div>
<div><strong>101</strong><span>Comuni serviti</span></div>
</div>

{sol_box("Come vendo casa a Limena senza errori?", [
    ("Valutazione gratuita", "Sopralluogo e fascia prezzo difendibile", "landing valutazione", "landing-valutazione"),
    ("Servizio vendita", "Mandato, marketing, trattativa e rogito", "servizio vendita", "servizio-vendita"),
    ("Hub proprietari", "Guide vendita, affitto e documenti", "proprietario immobile", "proprietario-immobile"),
    ("Zona Limena", "Scheda locale e contesto mercato", "zona Limena", "zona-limena"),
])}

<h2 id="perche-limena">Perché vendere casa a Limena: contesto locale</h2>
<p><strong>Limena</strong> (circa 8 km da Padova centro) attira famiglie e pendolari che cercano metrature più ampie rispetto al centro storico, mantenendo collegamenti rapidi verso SR308, tangenziale e nodi verso Mestre. Non è un clone di Padova città: microzone OMI, domanda e tempi di vendita seguono dinamiche proprie della cintura nord-ovest.</p>
<p>Se possedete un bilocale, trilocale o villa con giardino in Limena, il compratore tipo spesso confronta anche <a href=\"blog-limena-vs-padova-centro-dove-comprare-2026\">Limena vs Padova centro</a> e comuni limitrofi (Rubano, Vigonza, Cadoneghe). Il vostro listino deve reggere quel confronto — non solo «prezzo emotivo».</p>
<p>Righetto ha sede operativa in <strong>Via Roma 96</strong> dal 2000: conoscenza del territorio limenese, visite coordinate e 127 recensioni Google verificabili (media 4,9/5). Per chi valuta anche la locazione: <a href=\"blog-vendere-o-affittare-padova-2026\">vendere o affittare</a> e <a href=\"blog-affittare-casa-padova-proprietario-2026\">guida affitto proprietario Padova</a>.</p>

<div class="cta-row">
<a class="cta-deep" href="landing-valutazione">Valutazione gratuita Limena</a>
<a class="cta-deep-outline" href="servizio-vendita">Servizio vendita Righetto</a>
</div>

<h2 id="quando">Quando ha senso vendere: timing e mercato</h2>
<p>Il «momento giusto» combina <strong>fattori personali</strong> (eredi, trasferimento, ristrutturazione altrove) e <strong>contesto di mercato</strong>. L'<a href="{ADE_OSSERVATORIO}" target="_blank" rel="noopener noreferrer">Osservatorio del mercato immobiliare ADE</a> e <a href="{ISTAT_URL}" target="_blank" rel="noopener noreferrer">ISTAT</a> pubblicano trend aggregati Veneto — utili per orientamento macro, non per quotare il singolo appartamento in Via Roma.</p>
<p>A Limena la domanda residenziale resta legata a famiglie e lavoratori padovani; la primavera e l'autunno concentrano spesso più visite qualificate rispetto ad agosto. Non esiste calendario universale: un immobile ben valutato e documentato può vendere anche in periodi tradizionalmente più lenti se il prezzo è credibile.</p>
<p>Se state vendendo per <strong>ricomprare altrove</strong>, sincronizzate i tempi: un compromesso di acquisto condizionato alla vendita del vostro immobile limenese è pratica comune ma va redatto con attenzione alle scadenze. Se vendete l'abitazione principale, verificate con il commercialista le implicazioni fiscali legate al timing del nuovo acquisto — regole soggette a modifiche normative.</p>
<p>Proprietari che passano da affitto a vendita (locazione attiva) devono rispettare preavvisi contrattuali e registrazioni: non mettete in vendita un immobile ancora locato senza verificare clausole di recesso e obblighi verso l'inquilino. Guida locazione: <a href=\"blog-affittare-casa-padova-proprietario-2026\">affittare casa Padova proprietario</a>.</p>
<ul>
<li><strong>Segnale positivo:</strong> comparabili simili venduti in 60–90 giorni con pochi ribassi.</li>
<li><strong>Segnale di attenzione:</strong> annunci analoghi in zona da mesi con riduzioni progressive di prezzo.</li>
<li><strong>Segnale personale:</strong> urgenza trasferimento — meglio listino realistico subito che sovrastima lunga.</li>
</ul>

{svg_percorso_vendita()}

<h2 id="valutazione">Valutazione e prezzo di uscita a Limena</h2>
<p>Primo passo obbligatorio: <strong>stima comparativa</strong> incrociando <a href="{OMI_URL}" target="_blank" rel="noopener noreferrer">OMI ADE</a> (fasce min–med–max per zona omogenea), annunci e transazioni simili e <strong>sopralluogo</strong> sullo stato reale. OMI da solo non basta: due trilocali in zone B1 e R1 limenesi possono avere appeal e prezzi molto diversi.</p>
<p>Approfondimento metodo: <a href=\"blog-valutazione-casa-padova-guida-2026\">valutazione immobile Padova</a>. Errori tipici del venditore limenese:</p>
<ul>
<li>Listino basato su un annuncio vicino «a occhio» senza aggiustamenti per piano, ristrutturazione, box.</li>
<li>Ignorare delibere condominiali straordinarie in corso che spaventano acquirenti.</li>
<li>Confondere valutazione di mercato con perizia mutuo bancario — obiettivi diversi.</li>
</ul>
<p>Righetto eroga <a href=\"landing-valutazione\">valutazione gratuita</a> con report scritto: base per mandato e strategia marketing. Non pubblichiamo €/mq inventati per Limena: consultate sempre il semestre OMI corrente sul portale ADE.</p>
<p>Per leggere OMI in modo corretto: selezionate il comune di Limena, la tipologia (abitazione civile, ville, ecc.), lo stato conservativo e la zona omogenea indicata sulla mappa ADE. Confrontate minimo, medio e massimo con il vostro immobile — se chiedete sopra il massimo, preparate motivazioni oggettive (ristrutturazione certificata, pertinenze extra, efficienza energetica superiore alla media zona).</p>
<p>Il mercato 2026 nel Padovano resta <strong>selettivo</strong>: compratori confrontano più annunci online prima di visitare. Un prezzo iniziale credibile genera più visite nei primi 30 giorni; un prezzo gonfiato seguito da tagli periodici segnala debolezza e attira solo offerte aggressive.</p>

{blog_fig("img/blog/blog-vendere-casa-limena-proprietario-2026-valutazione.webp", "Valutazione casa Limena 2026 — metodo comparativo OMI e sopralluogo")}

<table>
<caption>Elementi che spostano il valore a Limena (checklist venditore)</caption>
<thead><tr><th>Fattore</th><th>Effetto tipico sul prezzo</th></tr></thead>
<tbody>
<tr><td>Classe energetica APE</td><td>Domanda maggiore su immobili efficienti</td></tr>
<tr><td>Piano e ascensore</td><td>Famiglie preferiscono piani serviti in condominio</td></tr>
<tr><td>Box / posto auto</td><td>Pertinenze con subalterno valorizzano l'offerta</td></tr>
<tr><td>Planimetria conforme</td><td>Difetto blocca mutuo acquirente — sconto o ritardo</td></tr>
<tr><td>Giardino / terrazzo</td><td>Premium su villette e piani terra curati</td></tr>
</tbody>
</table>

<h2 id="documenti">Documenti da preparare prima dell'annuncio</h2>
<p>Un dossier completo accelera visite, trattative e rogito. Checklist operativa:</p>
<ol>
<li><strong>Visura catastale</strong> e planimetria conforme allo stato di fatto.</li>
<li><strong>APE</strong> valido — obbligatorio in compravendita abitativa.</li>
<li><strong>Atto di provenienza</strong> e eventuali successioni già accettate.</li>
<li><strong>Ultimi verbali condominiali</strong> e tabella millesimale — spese e lavori futuri.</li>
<li><strong>Certificazioni impianti</strong> (dove richieste) e conformità urbanistica se ci sono tamponature.</li>
<li><strong>Documenti pertinenze</strong> — box, cantina, autorimesse con subalterni.</li>
</ol>

<table>
<caption>Documenti vendita Limena — chi li richiede</caption>
<thead><tr><th>Documento</th><th>Quando serve</th><th>Chi lo verifica</th></tr></thead>
<tbody>
<tr><td>Visura + planimetria</td><td>Prima annuncio</td><td>Agenzia e acquirente in due diligence</td></tr>
<tr><td>APE</td><td>Obbligatorio in contratto</td><td>Notaio al rogito</td></tr>
<tr><td>Verbali condominio</td><td>Visite e trattativa</td><td>Acquirente / banca mutuo</td></tr>
<tr><td>Atto provenienza</td><td>Compromesso e rogito</td><td>Notaio</td></tr>
</tbody>
</table>

<p>Guida trasversale: <a href=\"blog-documenti-vendita-casa\">documenti vendita casa</a>. Per immobile ereditato: verificare prima eventuali vincoli e quote con notaio o commercialista di fiducia.</p>

{blog_fig("img/blog/blog-vendere-casa-limena-proprietario-2026-documenti.webp", "Documenti vendita casa Limena — dossier catastale APE e condominio")}

<h2 id="mandato">Mandato di vendita e scelta dell'agenzia a Limena</h2>
<p>Il <strong>mandato</strong> definisce durata, obblighi di promozione, compenso e modalità di visita. In <strong>esclusiva</strong> un solo referente coordina listino, foto e trattative; in <strong>non esclusiva</strong> più agenzie possono pubblicare — rischio annunci duplicati con prezzi incoerenti. Il compenso di mediazione Righetto si concorda <strong>sempre in sede</strong> nel contratto: nessun listino percentuale online, in linea con deontologia FIMAA.</p>
<p>Per scegliere l'interlocutore locale: <a href=\"blog-agenzia-immobiliare-limena-come-scegliere-2026\">agenzia immobiliare Limena</a> e pagina <a href=\"agenzia-immobiliare-padova\">agenzia Padova</a>. Approfondimento esclusiva: <a href=\"blog-mandato-esclusivo-padova-perche-conviene-2026\">mandato esclusivo Padova</a>.</p>

{svg_mandato_confronto()}

<h2 id="marketing">Marketing, annuncio e visite sul territorio</h2>
<p>Dopo valutazione e mandato, la <strong>presentazione</strong> dell'immobile determina quante visite qualificate arrivate. Standard minimo 2026:</p>
<ul>
<li><strong>Foto professionali</strong> e planimetria leggibile — niente scatti smartphone bui.</li>
<li><strong>Descrizione onesta</strong> su spese condominiali, lavori in corso, orientamento.</li>
<li><strong>Tour virtuali</strong> dove utile — Righetto integra visite 360° su immobili selezionati.</li>
<li><strong>Orari visite</strong> flessibili ma coordinati — evitare sovrapposizioni caotiche.</li>
</ul>
<p>Pubblicare su più portali senza allineare testi e prezzo confonde il mercato. Meglio un piano unico con l'agenzia che conosce Limena e filtra curiosi da acquirenti con mutuo pre-approvato. Costi accessori della vendita (imposte, notaio): <a href=\"blog-costi-vendere-casa-padova-2026\">costi vendere casa Padova</a> — tema distinto dal listino.</p>

{blog_fig("img/blog/blog-vendere-casa-limena-proprietario-2026-marketing.webp", "Marketing vendita casa Limena — foto professionali e annuncio immobiliare")}

<h2 id="trattativa">Trattativa, compromesso e rogito</h2>
<p>Arrivata una proposta seria, verificate:</p>
<ol>
<li><strong>Qualifica finanziaria</strong> acquirente — lettera banca o broker.</li>
<li><strong>Importo e condizioni</strong> — caparra confirmatoria, termine rogito, eventuali clausole sospensive.</li>
<li><strong>Compromesso</strong> registrato con versamento caparra — tutela entrambe le parti.</li>
<li><strong>Rogito notarile</strong> — trasferimento proprietà e saldo prezzo.</li>
</ol>
<p>Per immobili con ipoteca da estinguere, coordinamento banca-venditore-notaio va pianificato in anticipo. Righetto assiste nelle fasi preliminari; il notaio scelto dall'acquirente (o concordato) formalizza l'atto. Preliminari: <a href=\"servizio-preliminari\">servizio preliminari</a>.</p>
<p>La <strong>caparra confirmatoria</strong> di norma si aggira intorno al 10–20% del prezzo concordato — cifra da definire nel compromesso, non da improvvisare a voce. Se l'acquirente chiede clausola sospensiva per mutuo, verificate che la scadenza sia realistica rispetto ai tempi bancari (spesso 30–45 giorni lavorativi dalla domanda completa).</p>
<p>Al rogito portate: documento identità valido, codice fiscale, eventuale procura se non compare personalmente, certificazioni antichieste dal notaio (stato libero, conformità urbanistica se richiesta). L'acquirente versa il saldo prezzo al netto della caparra; voi estinguete mutuo residuo se presente con delega pagamento in sede notarile.</p>
<p>Dopo il rogito: voltura utenze, comunicazione al condominio e aggiornamento catastale sono passaggi che Righetto segnala in chiusura — l'esecuzione resta in capo alle parti con i rispettivi fornitori.</p>

<h2 id="fiscalita">Fiscalità, plusvalenza e consulenza</h2>
<p>La vendita può generare <strong>plusvalenza tassabile</strong> se l'immobile non rientra in esenzioni previste dalla normativa vigente (tempi di possesso, abitazione principale, eredità…). Le aliquote e le condizioni cambiano con decreti e leggi di bilancio: <strong>non sostituiamo</strong> il commercialista o il notaio.</p>
<p>Prima del rogito chiarite con professionista: imposta di registro o IVA (se vendita da impresa), imposte cedulari, detrazioni residue su ristrutturazioni. Righetto coordina la parte immobiliare; per fiscalità personale serve consulenza dedicata.</p>
<p>Se vendete per acquistare altrove in Veneto, valutate tempistiche tra rogito di vendita e compromesso di acquisto — il vincolo di «prima vendo poi compro» va scritto con attenzione nel preliminare per non restare senza casa abitabile. Per chi eredita: accettazione eredità e eventuale divisione tra coeredi vanno concluse prima di listini incoerenti tra fratelli.</p>

<h2 id="tipologie">Bilocale, trilocale o villa: cosa cambia per chi vende</h2>
<p>Il mercato limenese non tratta tutte le tipologie allo stesso modo. Un <strong>bilocale</strong> in condominio ben servito intercetta coppie giovani e investitori locativi — competizione alta se il prezzo non è allineato a OMI. Un <strong>trilocale</strong> con doppio servizio e box è spesso il prodotto «famiglia» più richiesto: qui contano piano, luce naturale e spese condominiali contenute.</p>
<p>Le <strong>ville</strong> e le unità con giardino privato hanno bacino più ristretto ma premio sullo spazio esterno — servono foto che mostrino cura del verde, recinzioni e accessi. Approfondimenti tipologia: <a href=\"blog-bilocale-trilocale-limena-scelta-2026\">bilocale e trilocale Limena</a> (angolo acquirente utile anche al venditore per capire cosa cercano).</p>
<p>Indipendentemente dalla tipologia, il venditore limenese deve chiedersi: «Il mio immobile compete con quali annunci attivi entro 1 km?» Se la risposta include ristrutturati recenti a prezzo simile, serve differenziare con APE, pertinenze o posizione — oppure allineare il listino alla realtà.</p>

<h3>Pertinenze: box, cantina, posto auto scoperto</h3>
<p>A Limena, come in tutta la cintura padovana, <strong>box e posti auto</strong> incidono sulla velocità di vendita. Verificate che i subalterni catastali corrispondano alla realtà e che non ci siano occupazioni abusive da sanare prima dell'annuncio. Un garage doppio in contesto familiare può giustificare posizionamento nella fascia alta OMI solo se documentato e accessibile.</p>

<h3>Condominio e rapporti di vicinato</h3>
<p>In vendita, acquirenti esperti chiedono <strong>spese ordinarie</strong>, fondo lavori e eventuali contenziosi. Un condominio con ascensore recently manutenuto trasmette serenità; delibere per facciate o cappotti non eseguiti spaventano chi teme conguagli futuri. Preparate un riepilogo scritto delle spese annuali — evita sorprese in trattativa.</p>

<h2 id="visite">Come prepararsi alle visite a Limena</h2>
<p>Le visite sono il momento in cui il prezzo si difende sul campo. Checklist pratica per il proprietario:</p>
<ul>
<li><strong>Pulizia e ordine</strong> — armadi chiusi ma ambienti aerati; niente accumulo in ingresso.</li>
<li><strong>Luce</strong> — tende aperte di giorno; lampade accese se visita serale.</li>
<li><strong>Odori</strong> — evitare cibi forti prima della visita; aerare cantine umide.</li>
<li><strong>Documenti a portata</strong> — APE, planimetria, ultimo bollettino condominiale se richiesto.</li>
<li><strong>Assenza del venditore</strong> — spesso preferibile lasciare l'agente guidare la visita; meno pressione sull'acquirente.</li>
</ul>
<p>Se l'immobile è ancora abitato, concordate finestre orarie con Righetto per non saturare la famiglia. Per ristrutturazioni in corso, mostrate render o preventivi completati — la trasparenza riduce trattative aggressive.</p>
<p>Acquirenti pendolari chiederanno tempi reali verso Padova, Rubano o Mestre: non promettete minuti «da cartina» se negli orari di punta SR308 rallenta. Meglio indicare range onesti — filtra chi non accetta il compromesso cintura/traffico.</p>

<h2 id="errori">Errori che rallentano la vendita a Limena</h2>
<ul>
<li><strong>Sovrastima emotiva</strong> — mesi in vetrina, poi ribassi a rilento.</li>
<li><strong>Planimetria non conforme</strong> non dichiarata — acquirente scopre in due diligence.</li>
<li><strong>APE assente o scaduto</strong> — blocca contratto abitativo.</li>
<li><strong>Annunci multipli incoerenti</strong> — stesso immobile, prezzi diversi.</li>
<li><strong>Casa non pronta alle visite</strong> — disordine, odori, lavori visibili non spiegati.</li>
<li><strong>Trattare solo al telefono</strong> senza caparra — rischio perdita tempo.</li>
</ul>
<p>Sette errori classici padovani (validi anche a Limena): <a href=\"vendere-casa-padova-errori\">vendere casa Padova errori</a>.</p>

<h2 id="prossimi-passi">Prossimi passi per il proprietario limenese</h2>
<ol>
<li><strong>Richiedere valutazione gratuita</strong> — <a href=\"landing-valutazione\">landing valutazione</a> o 049.8843484.</li>
<li><strong>Completare dossier</strong> catastale, APE, condominio.</li>
<li><strong>Scegliere mandato</strong> e piano marketing con Righetto.</li>
<li><strong>Allineare listino</strong> al report comparativo — credibilità prima della velocità.</li>
<li><strong>Preparare immobile</strong> per visite — pulizia, luce, documenti a portata.</li>
</ol>
<p>Cross-link utili: <a href=\"zona-limena\">scheda zona Limena</a> · <a href=\"blog-mercato-immobiliare-limena-2026\">mercato Limena 2026</a> · <a href=\"blog-case-vendita-limena-leggere-annunci-2026\">case in vendita Limena annunci</a> · <a href=\"proprietario-immobile\">hub proprietario</a>.</p>

<h3>Dopo la vendita: cosa conservare</h3>
<p>Archiviate copia del mandato, del compromesso, del rogito, delle quietanze di estinzione mutuo e delle dichiarazioni fiscali. Servono per eventuali controlli o per la prossima operazione immobiliare. Righetto può fornire copia documentazione di intermediazione; per fiscalità conservate i documenti del commercialista.</p>

<h3>Perché affidarsi a un'agenzia radicata a Limena</h3>
<p>Vendere da soli (privato) risparmia il compenso di mediazione ma scarica su di voi filtro acquirenti, sicurezza visite, negoziazione e coordinamento notarile. Un'agenzia con <strong>sede fisica in Limena</strong> conosce i compratori ricorrenti del territorio, i notai abituali e le criticità urbanistiche locali — riduce attrito nelle fasi delicate.</p>
<p>Righetto unisce presenza locale (Via Roma 96) con strumenti digitali: tour virtuali su immobili selezionati, portale annunci aggiornato, integrazione con richieste da Google e form lead da <a href=\"landing-consulenza-immobiliare-gratuita\">consulenza gratuita</a>. Il compenso si concorda in sede — trasparenza prima del mandato, non sorprese a rogito.</p>

<p>{CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 11 settembre 2026. Fonti: OMI e Osservatorio ADE, ISTAT, normativa compravendita abitativa. Nessun dato €/mq inventato.</p>
"""


CFG = {
    "slug": SLUG,
    "filename": f"{SLUG}.html",
    "hero": "img/blog/blog-vendere-casa-limena-proprietario-2026-hero.webp",
    "title": "Vendere casa Limena 2026: guida proprietario",
    "og_title": "Vendere casa a Limena 2026: percorso per il proprietario",
    "meta": "Vendere casa a Limena 2026: valutazione OMI, documenti, mandato, marketing e rogito. Guida proprietari Righetto con valutazione gratuita in Via Roma 96.",
    "schema_headline": "Vendere casa a Limena nel 2026: percorso per il proprietario",
    "section": "Guida proprietari",
    "cat_badge": "Proprietari · Vendita Limena",
    "bread_crumb": "Vendere casa Limena proprietario",
    "h1": "<strong>Vendere casa</strong> a Limena: guida 2026",
    "hero_alt": "Vendere casa Limena 2026 — percorso proprietario valutazione e vendita",
    "body_fn": body_vendere_limena,
    "faqs": [
        ("Quanto tempo serve per vendere casa a Limena?", "Dipende da prezzo, stato e domanda del semestre. Immobili ben valutati e documentati tendono a chiudere più rapidamente di quelli sovrastimati."),
        ("Come si calcola il prezzo di vendita a Limena?", "Con OMI ADE per fascia zonale, comparabili simili e sopralluogo — non con stime online generiche."),
        ("Quali documenti servono prima di mettere in vendita?", "Visura catastale, planimetria conforme, APE, verbali condominiali, atto di provenienza e documentazione pertinenze."),
        ("Meglio mandato esclusivo o non esclusivo?", "L'esclusiva concentra marketing e visite su un referente; la non esclusiva moltiplica annunci ma rischia incoerenze. Scelta da concordare in sede."),
        ("Righetto è davvero a Limena?", "Sì — sede operativa Via Roma 96, Limena (PD), dal 2000. Copertura Padova e 101 comuni."),
        ("Devo pagare percentuali online per la mediazione?", "No — il compenso Righetto si concorda in sede nel mandato, senza listini pubblicati sul sito."),
    ],
    "related": [
        ("Valutazione immobile Padova", "blog-valutazione-casa-padova-guida-2026"),
        ("Agenzia Limena", "blog-agenzia-immobiliare-limena-come-scegliere-2026"),
        ("Mandato esclusivo", "blog-mandato-esclusivo-padova-perche-conviene-2026"),
        ("Documenti vendita", "blog-documenti-vendita-casa"),
        ("Servizio vendita", "servizio-vendita"),
        ("Valutazione gratuita", "landing-valutazione"),
    ],
    "registry": {
        "titolo": "Vendere casa a Limena nel 2026: percorso per il proprietario",
        "categoria": "Guida proprietari",
        "tempo": 16,
        "contenuto": "Pillar owner vendita Limena: valutazione OMI, documenti, mandato, marketing, rogito. CTA landing-valutazione.",
        "admin_contenuto": "Pillar eq-sep11-001 — vendere casa Limena percorso proprietario.",
        "emoji": "🏡",
        "evidenza": True,
    },
    "static_map_key": "vendere casa limena proprietario 2026",
    "cta_banner_title": "Vuoi vendere casa a Limena?",
    "cta_banner_text": "Valutazione gratuita in agenzia — Via Roma 96, Limena. Tel. 049.8843484.",
}


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
        if item.get("id") == QUEUE_ID:
            item["status"] = "published"
            item["published_date"] = DATE_ISO
            break
    data["updated"] = DATE_ISO
    EDITORIAL_QUEUE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"editorial-queue.json: {QUEUE_ID} -> published")


def main() -> None:
    ensure_images()
    body = CFG["body_fn"]()
    words = wc(body)
    if words < MIN_BODY_WORDS - 10:
        print(f"WARN {CFG['slug']}: {words} parole (< {MIN_BODY_WORDS})")
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
