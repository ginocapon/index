# -*- coding: utf-8 -*-
"""Pillar eq-sep18-001 — gestione locazione delegata Padova 2026.
python scripts/build_blog_gestione_locazione_delegata_sep18.py
"""
from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE_IT = "18 settembre 2026"
DATE_ISO = "2026-09-18"
TIME_TS = "2026-09-18T10:00:00+02:00"
QUEUE_ID = "eq-sep18-001"

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
SLUG = "blog-gestione-locazione-delegata-padova-2026"

IMAGE_SOURCES: dict[str, tuple[str, str] | list[tuple[str, str]]] = {
    "hero": (
        "img/blog/blog-affittare-casa-padova-proprietario-2026-hero.webp",
        "img/blog/blog-gestione-locazione-delegata-padova-2026-hero.webp",
    ),
    "body": [
        (
            "img/blog/blog-affittare-casa-padova-proprietario-2026-gestione.webp",
            "img/blog/blog-gestione-locazione-delegata-padova-2026-servizi.webp",
        ),
        (
            "img/blog/blog-affittare-casa-padova-proprietario-2026-contratto.webp",
            "img/blog/blog-gestione-locazione-delegata-padova-2026-contratto.webp",
        ),
        (
            "img/blog/blog-rendimento-affitto-padova-hero.webp",
            "img/blog/blog-gestione-locazione-delegata-padova-2026-rendimento.webp",
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


def svg_percorso_gestione() -> str:
    return """<figure class="chart-wrap" aria-label="Percorso gestione locazione delegata">
<svg viewBox="0 0 580 280" width="100%" height="280" role="img">
<title>Gestione locazione delegata Padova — 6 fasi operative</title>
<text x="290" y="24" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Gestione delegata — ciclo operativo</text>
<rect x="20" y="55" width="78" height="36" rx="8" fill="#2C4A6E"/><text x="59" y="77" text-anchor="middle" font-size="7" fill="#fff">1. Mandato</text>
<path d="M98 73 L112 73" stroke="#FF6B35" stroke-width="2"/>
<rect x="115" y="55" width="78" height="36" rx="8" fill="#3A5F8C"/><text x="154" y="77" text-anchor="middle" font-size="7" fill="#fff">2. Inquilino</text>
<path d="M193 73 L207 73" stroke="#FF6B35" stroke-width="2"/>
<rect x="210" y="55" width="78" height="36" rx="8" fill="#FF6B35" opacity="0.9"/><text x="249" y="77" text-anchor="middle" font-size="7" fill="#152435">3. Contratto</text>
<path d="M288 73 L302 73" stroke="#FF6B35" stroke-width="2"/>
<rect x="305" y="55" width="78" height="36" rx="8" fill="#2C4A6E"/><text x="344" y="77" text-anchor="middle" font-size="7" fill="#fff">4. Incassi</text>
<path d="M383 73 L397 73" stroke="#FF6B35" stroke-width="2"/>
<rect x="400" y="55" width="78" height="36" rx="8" fill="#3A5F8C"/><text x="439" y="77" text-anchor="middle" font-size="7" fill="#fff">5. Manutenz.</text>
<path d="M478 73 L492 73" stroke="#FF6B35" stroke-width="2"/>
<rect x="495" y="55" width="65" height="36" rx="8" fill="#2C4A6E"/><text x="527" y="77" text-anchor="middle" font-size="6" fill="#fff">Report</text>
<text x="290" y="130" text-anchor="middle" font-size="9" fill="#6B7A8D">Padova e provincia — referente unico, rendicontazione periodica al proprietario</text>
<text x="290" y="200" text-anchor="middle" font-size="8" fill="#6B7A8D">Compenso e servizi definiti nel mandato firmato in agenzia</text>
</svg>
<figcaption>Schema qualitativo del ciclo gestione delegata: dal mandato alla rendicontazione, con Righetto come unico interlocutore.</figcaption>
</figure>"""


def svg_confronto_diretta_delegata() -> str:
    return """<figure class="chart-wrap" aria-label="Confronto gestione diretta e delegata">
<svg viewBox="0 0 520 240" width="100%" height="240" role="img">
<title>Gestione diretta vs gestione delegata locazione Padova</title>
<text x="260" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Diretta vs delegata — cosa cambia</text>
<rect x="30" y="45" width="210" height="85" rx="10" fill="#E1DBD1"/>
<text x="135" y="68" text-anchor="middle" font-size="10" fill="#152435" font-weight="600">Gestione diretta</text>
<text x="135" y="86" text-anchor="middle" font-size="8" fill="#6B7A8D">Tempo e presidio locale</text>
<text x="135" y="102" text-anchor="middle" font-size="7" fill="#6B7A8D">Risparmio commissioni · rischio operativo</text>
<rect x="280" y="45" width="210" height="85" rx="10" fill="#2C4A6E"/>
<text x="385" y="68" text-anchor="middle" font-size="10" fill="#fff" font-weight="600">Gestione delegata</text>
<text x="385" y="86" text-anchor="middle" font-size="8" fill="rgba(255,255,255,.85)">Referente unico · manutenzione</text>
<text x="385" y="102" text-anchor="middle" font-size="7" fill="rgba(255,255,255,.7)">Morosità · rinnovi · report</text>
<text x="260" y="165" text-anchor="middle" font-size="9" fill="#6B7A8D">Scelta dipende da distanza, numero unità e tempo disponibile</text>
<text x="260" y="210" text-anchor="middle" font-size="8" fill="#6B7A8D">Compenso gestione concordato in sede — nessun listino online</text>
</svg>
<figcaption>Confronto qualitativo: la delega ha senso quando il costo opportunità del tempo supera il compenso concordato con l'agenzia.</figcaption>
</figure>"""


def body_gestione_delegata() -> str:
    return f"""
{aeo_box("In sintesi", "La <strong>gestione locazione delegata a Padova</strong> affida a un'agenzia incassi, rapporto con l'inquilino, manutenzione, rinnovi contrattuali e rendicontazione. Righetto integra <a href=\"servizio-locazioni\">locazione</a> (ricerca inquilino) e <a href=\"servizio-gestione\">gestione patrimonio</a> con mandato e compenso <strong>concordati in sede</strong>. Diverso da <a href=\"blog-affittare-casa-padova-proprietario-2026\">affittare casa Padova</a> (percorso pre-locazione) e da <a href=\"blog-rendimento-affitto-padova\">rendimento affitto</a> (calcolo resa).")}

<p><strong>Distinzione editoriale:</strong> <em>Fatto</em> — registrazione contratti entro 30 giorni ADE, obblighi locatore artt. 1575-1585 c.c., fasce OMI locazioni ufficiali. <em>Analisi</em> — quando la delega conviene a proprietari padovani con immobile lontano, portafoglio multiplo o poco tempo. <em>Previsione</em> — nessuna garanzia su tempi di locazione o assenza morosità: dipende da mercato, canone e qualifica inquilino.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#cos-e">Cos'è la gestione locazione delegata</a></li>
<li><a href="#include">Cosa include il servizio</a></li>
<li><a href="#locazione-vs-gestione">Locazione vs gestione continuativa</a></li>
<li><a href="#quando-conviene">Quando conviene delegare</a></li>
<li><a href="#quando-no">Quando restare in gestione diretta</a></li>
<li><a href="#padova">Contesto Padova e provincia</a></li>
<li><a href="#mandato">Mandato, compenso e trasparenza</a></li>
<li><a href="#inquilino">Selezione inquilino e contratti</a></li>
<li><a href="#incassi">Incassi, cauzioni e rivalutazioni</a></li>
<li><a href="#manutenzione">Manutenzione ordinaria e straordinaria</a></li>
<li><a href="#morosita">Morosità e tutele legali</a></li>
<li><a href="#fiscalita">Fiscalità e rendicontazione</a></li>
<li><a href="#portafoglio">Più immobili e patrimoni ereditari</a></li>
<li><a href="#errori">Errori da evitare</a></li>
<li><a href="#prossimi-passi">Prossimi passi con Righetto</a></li>
</ol></nav>

<div class="kpi-strip" aria-label="Contesto gestione locazione Padova">
<div><strong>200+</strong><span>Immobili gestiti</span></div>
<div><strong>101</strong><span>Comuni serviti</span></div>
<div><strong>30 gg</strong><span>Registrazione ADE</span></div>
<div><strong>2000</strong><span>Righetto dal</span></div>
</div>

{sol_box("Voglio delegare la gestione del mio affitto a Padova — da dove inizio?", [
    ("Servizio gestione", "Incassi, manutenzione, rendicontazione patrimonio", "servizio gestione", "servizio-gestione"),
    ("Servizio locazioni", "Ricerca inquilino, contratto e registrazione", "servizio locazioni", "servizio-locazioni"),
    ("Valutazione locativa", "Canone orientativo e fascia OMI", "landing valutazione", "landing-valutazione"),
    ("Hub proprietari", "Guide vendita, affitto e documenti", "proprietario immobile", "proprietario-immobile"),
])}

<h2 id="cos-e">Cos'è la gestione locazione delegata</h2>
<p>La <strong>gestione locazione delegata</strong> (o gestione immobiliare in locazione) è il rapporto con cui il proprietario affida a un'agenzia professionale l'amministrazione quotidiana di un immobile locato: non solo la ricerca dell'inquilino, ma l'intero ciclo post-contratto. In pratica voi mantenete la proprietà e incassate i canoni (direttamente o tramite rendicontazione); l'agenzia gestisce operatività, comunicazioni e criticità.</p>
<p>A Padova e in provincia molti proprietari conoscono la mediazione per la <em>prima locazione</em>, ma sottovalutano quanto tempo richieda la fase successiva: solleciti di pagamento, guasti idraulici un sabato sera, rinnovi con rivalutazione ISTAT, disdetta e restituzione cauzione con verbale di consegna. Delegare significa trasferire queste attività a un referente con processi, rete artigiani e competenza normativa.</p>
<p>Righetto Immobiliare — sede in <strong>Via Roma 96, Limena</strong> — offre gestione su Padova città, cintura (Limena, Rubano, Vigonza, Cadoneghe…) e oltre <strong>101 comuni</strong> del territorio. Il modello è descritto in pagina <a href=\"servizio-gestione\">servizio gestione</a>; questo articolo approfondisce <em>cosa include</em>, <em>quando conviene</em> e come integrarlo con la locazione iniziale.</p>

<div class="cta-row">
<a class="cta-deep" href="servizio-gestione">Scopri il servizio gestione</a>
<a class="cta-deep-outline" href="landing-consulenza-immobiliare-gratuita">Consulenza gratuita</a>
</div>

<h2 id="include">Cosa include la gestione delegata: elenco operativo</h2>
<p>Un servizio di gestione serio a Padova copre almeno queste aree — verificate sempre nel mandato scritto prima della firma:</p>
<ul>
<li><strong>Relazione con l'inquilino</strong> — Canale unico per richieste, comunicazioni formali, preavvisi e rinnovi.</li>
<li><strong>Incasso canoni</strong> — Solleciti, tracciamento pagamenti, gestione cauzione e restituzione a fine locazione.</li>
<li><strong>Contratti e ADE</strong> — Registrazione entro 30 giorni, proroghe, eventuali addendum e adeguamenti contrattuali.</li>
<li><strong>Manutenzione</strong> — Coordinamento interventi ordinari (rubinetti, serrature, caldaie) e straordinari con preventivi condivisi.</li>
<li><strong>Condominio</strong> — Interlocuzione con amministratore per spese, lavori e accessi.</li>
<li><strong>Morosità</strong> — Iter strutturato di sollecito, diffida e attivazione legale se necessario.</li>
<li><strong>Rendicontazione</strong> — Report periodico di incassi, spese e stato locazione.</li>
</ul>
<p>Non tutti i mandati includono tutto: esistono pacchetti «solo incasso e rinnovo» oppure gestione «full» con manutenzione predittiva e analisi redditività. Righetto definisce scope e compenso <strong>in sede</strong>, senza listini percentuali pubblicati online — coerente con deontologia FIMAA e trasparenza contrattuale.</p>

{blog_fig("img/blog/blog-gestione-locazione-delegata-padova-2026-servizi.webp", "Gestione locazione delegata Padova — servizi agenzia immobiliare proprietario")}

<h2 id="locazione-vs-gestione">Servizio locazioni vs gestione continuativa</h2>
<p>Confusione frequente: <strong>locazione</strong> e <strong>gestione</strong> non sono sinonimi. Il <a href=\"servizio-locazioni\">servizio locazioni</a> Righetto si concentra sulla fase di <em>ingresso</em>: marketing immobile, selezione inquilino, redazione contratto, registrazione ADE, consegna chiavi. Una volta locato, molti proprietari proseguono da soli — finché non compare la prima emergenza.</p>
<p>Il <a href=\"servizio-gestione\">servizio gestione</a> copre invece il <em>ciclo di vita</em> della locazione: mesi e anni di rapporto con conduttore, manutenzione, fiscalità di base e report al proprietario. In pratica potete:</p>
<ol>
<li><strong>Solo locazione</strong> — Affidate la messa in locazione e poi gestite in autonomia.</li>
<li><strong>Locazione + gestione</strong> — Stesso referente dall'annuncio al rinnovo del quarto anno.</li>
<li><strong>Gestione immobile già locato</strong> — Subentro su contratto esistente (con verifica clausole e stato documentale).</li>
</ol>
<p>Se state ancora definendo <em>se affittare</em>, partite da <a href=\"blog-vendere-o-affittare-padova-2026\">vendere o affittare Padova 2026</a>. Se avete già scelto la locazione ma non il modello operativo, leggete <a href=\"blog-affittare-casa-padova-proprietario-2026\">affittare casa Padova proprietario</a> e tornate qui per la delega.</p>

{svg_percorso_gestione()}

<h2 id="quando-conviene">Quando conviene la gestione delegata a Padova</h2>
<p>La delega ha senso economico e operativo quando il <strong>costo opportunità</strong> del vostro tempo supera il compenso concordato con l'agenzia. Situazioni tipiche nel padovano:</p>
<ul>
<li><strong>Proprietario non residente</strong> — Vivete in altra città o regione; l'immobile è a Padova, Limena o in cintura.</li>
<li><strong>Portafoglio multiplo</strong> — Due o più unità locates: centralizzare su un referente riduce errori e ritardi.</li>
<li><strong>Carico lavorativo elevato</strong> — Professionisti, imprenditori, medici con turni: non potete correre per ogni guasto.</li>
<li><strong>Patrimonio ereditato</strong> — Coeredi distanti che preferiscono reddito regolare senza gestione quotidiana.</li>
<li><strong>Locazione a studenti</strong> — Turnover e co-inquilini richiedono presidio che in autunno si intensifica (approfondimento: <a href=\"blog-affitto-studenti-padova\">affitto studenti Padova</a>).</li>
<li><strong>Prima esperienza locativa</strong> — Preferite affiancamento su contratto, registrazione e morosità.</li>
</ul>
<p>Il mercato locativo padovano resta sostenuto da domanda universitaria e lavorativa — si legge su <a href="{OMI_URL}" target="_blank" rel="noopener noreferrer">OMI locazioni ADE</a> e osservatori FIMAA quando disponibili — ma <em>domanda alta non elimina rischi operativi</em>: un inquilino in ritardo o un impianto da rifare restano oneri di gestione.</p>

{svg_confronto_diretta_delegata()}

<h2 id="quando-no">Quando ha senso restare in gestione diretta</h2>
<p>Delegare non è sempre la scelta migliore. Gestione diretta può funzionare se:</p>
<ul>
<li>Abiate <strong>vicinanza geografica</strong> e tempo per visite e urgenze.</li>
<li>Locata a <strong>familiare o inquilino storico</strong> con rapporto fiduciario consolidato.</li>
<li>Disponete di <strong>rete artigiani</strong> personale e familiarità con regolamento condominiale.</li>
<li>Volete <strong>massimizzare il netto</strong> accettando il rischio operativo (compenso agenzia zero, tempo vostro alto).</li>
</ul>
<p>Anche in gestione diretta restano obblighi non delegabili verso il Fisco: la scelta del regime (cedolare secca vs IRPEF) va fatta con commercialista. Righetto non sostituisce consulenza fiscale personalizzata — orienta su adempimenti locativi e documentali.</p>

<table>
<thead><tr><th>Aspetto</th><th>Gestione diretta</th><th>Gestione delegata Righetto</th></tr></thead>
<tbody>
<tr><td>Tempo richiesto</td><td>Alto — urgenze e comunicazioni a vostro carico</td><td>Basso — referente unico filtra e risolve</td></tr>
<tr><td>Competenze</td><td>Contratti, ADE, manutenzione imparate sul campo</td><td>Processi agenzia, rete artigiani, iter morosità</td></tr>
<tr><td>Costo economico</td><td>Nessun compenso agenzia ricorrente</td><td>Compenso concordato in sede nel mandato</td></tr>
<tr><td>Rischio operativo</td><td>Morosità e guasti gestiti personalmente</td><td>Documentazione e solleciti strutturati</td></tr>
<tr><td>Ideale per</td><td>Residenti vicini, un solo immobile, inquilino fidato</td><td>Non residenti, portafoglio, studenti, eredità</td></tr>
</tbody>
</table>

<h2 id="padova">Padova e provincia: specificità locali</h2>
<p>Padova non è un mercato unico. Zona universitaria (Via VIII Febbraio, Portello, Savonarola) ha dinamiche studentesche diverse da Arcella familiare o da Limena/Vigonza pendolari. Una gestione delegata efficace conosce:</p>
<ul>
<li><strong>Stagionalità</strong> — Picco domanda studenti agosto-settembre; preavvisi spesso a giugno.</li>
<li><strong>Tipologie contrattuali</strong> — 4+4 libero, 3+2 concordato (<a href=\"blog-contratto-affitto-padova\">contratto affitto Padova</a>), transitorio per lavoro/studio.</li>
<li><strong>Canoni di riferimento</strong> — OMI per zona omogenea, non numeri inventati in annuncio.</li>
<li><strong>Condomini storici vs recenti</strong> — Tempi diversi per approvazioni lavori e spese straordinarie.</li>
</ul>
<p>Per immobili in cintura (Limena, Rubano, Cadoneghe) il proprietario spesso affitta a famiglie o lavoratori padovani: manutenzione e comunicazione con amministratore restano centrali anche se il canone è inferiore al centro. Guide zona: <a href=\"zona-limena\">Limena</a>, <a href=\"blog-affitti-limena-2026\">affitti Limena 2026</a>.</p>

<h2 id="mandato">Mandato di gestione, compenso e trasparenza</h2>
<p>Il <strong>mandato di gestione</strong> è il documento che delimita servizi, durata, modalità di pagamento del compenso e responsabilità. Elementi da verificare prima di firmare:</p>
<table>
<thead><tr><th>Voce</th><th>Cosa chiedere</th></tr></thead>
<tbody>
<tr><td>Scope servizi</td><td>Incasso, manutenzione, morosità, rinnovi — cosa è incluso e cosa extra</td></tr>
<tr><td>Durata e recesso</td><td>Tempi di preavviso per disdetta mandato da entrambe le parti</td></tr>
<tr><td>Compenso</td><td>Importo o formula concordati <strong>in sede</strong> — nessun obbligo di accettare listini web</td></tr>
<tr><td>Spese manutenzione</td><td>Soglia di spesa senza preventivo vs interventi da approvare</td></tr>
<tr><td>Reportistica</td><td>Periodicità e formato (email, area riservata, PDF)</td></tr>
<tr><td>Assicurazioni</td><td>Eventuali polizze consigliate per immobile locato</td></tr>
</tbody>
</table>
<p>Righetto applica la stessa regola della mediazione: <strong>compenso concordato in sede</strong>, nessuna percentuale pubblicata sul sito. Confrontate più proposte non solo sul prezzo, ma su rete manutentiva, tempi di risposta e referente dedicato.</p>

{blog_fig("img/blog/blog-gestione-locazione-delegata-padova-2026-contratto.webp", "Mandato gestione locazione Padova — contratto e documenti proprietario")}

<h2 id="inquilino">Selezione inquilino, contratto e registrazione</h2>
<p>Se la gestione inizia <em>prima</em> della locazione, la qualifica dell'inquilino è il primo filtro anti-morosità: documenti reddito, referenze, garanzie (fideiussione bancaria, assicurativa o garante). Righetto applica checklist coerente con <a href=\"blog-affittare-casa-padova-proprietario-2026\">guida affitto proprietario</a>.</p>
<p>Il contratto va redatto in conformità al tipo scelto (4+4, concordato, transitorio), con clausole su spese, manutenzioni ordinarie e modalità pagamento. La <strong>registrazione presso ADE entro 30 giorni</strong> è obbligatoria — sanzioni e problemi fiscali colpiscono proprietario e conduttore se omessa.</p>
<p>In gestione delegata l'agenzia custodisce copie contrattuali, ricevute di registrazione e calendario scadenze (fine locazione, preavvisi, opzione rinnovo). A ogni cambio inquilino il ciclo riparte: stato immobile, eventuale ripasso pittura, nuovo APE se scaduto.</p>

<h3>Subentro su locazione esistente</h3>
<p>Spesso ci contattate con contratto già in essere. In subentro verifichiamo: registrazione ADE, conformità canone, deposito cauzionale, stato pagamenti e clausole recesso. Solo dopo si firma mandato di gestione — non si «delega» un conflitto già aperto senza mappa chiara delle partite.</p>

<h2 id="incassi">Incassi, cauzioni e rivalutazioni ISTAT</h2>
<p>La gestione ordinaria dei flussi monetari include:</p>
<ul>
<li><strong>Canone mensile</strong> — Incasso, registrazione contabile, sollecito se ritardo oltre soglia concordata.</li>
<li><strong>Spese accessorie</strong> — Condominio, TARI, utenze se a carico conduttore per contratto.</li>
<li><strong>Deposito cauzionale</strong> — Versamento, custodia documentata, restituzione a fine locazione con eventuali trattenute motivate.</li>
<li><strong>Rivalutazione annuale</strong> — Se prevista da contratto (indice ISTAT o parametro concordato), applicazione e comunicazione formale.</li>
</ul>
<p>Trasparenza sui flussi riduce litigi in famiglia e tra coeredi: report mensile o trimestrale con entrate, uscite e saldo netto è standard nel servizio Righetto descritto in <a href=\"servizio-gestione\">servizio gestione</a>.</p>

<h2 id="manutenzione">Manutenzione ordinaria e straordinaria</h2>
<p>Artt. 1575-1585 del Codice Civile ripartiscono riparazioni tra locatore e conduttore. In pratica il proprietario delegato riceve chiamate filtrate: l'agenzia apre ticket, convoca artigiano, ottiene preventivo se sopra soglia e comunica esito. Rete di artigiani verificati a Padova riduce tempi morti — idraulico per perdita, elettricista per quadro, fabbro per serratura bloccata.</p>
<p>Manutenzione <strong>predittiva</strong> (controllo caldaia, grondaie, rubinetteria stagionale) preserva valore immobile e evita danni a conduttore e vicini. Per immobili vuoti tra un inquilino e l'altro, preparazione per nuova locazione: piccoli interventi, pulizia, fotografie aggiornate.</p>
<p>Interventi straordinari (tetto, facciata, ascensore) restano in capo al condominio o al proprietario secondo tabelle legali — la gestione delegata coordina accesso tecnici e comunicazione con amministratore, non sostituisce delibere assembleari.</p>

<h2 id="morosita">Morosità: prevenzione e iter strutturato</h2>
<p>Nessuna agenzia può garantire zero morosità. La differenza è <strong>processo</strong>: sollecito scritto, diffida raccomandata, tentativo di mediazione, attivazione supporto legale per sfratto o recupero crediti se necessario. Anticipare è meglio di ignorare: due mensilità insolute richiedono azione immediata.</p>
<p>Documentazione ordinata (estratti conto, PEC, ricevute raccomandate) è decisiva in sede giudiziaria. Il proprietario delegato deve ricevere copia di ogni passaggio — nessuna sorpresa a distanza di mesi.</p>
<p>Per prevenzione: qualifica iniziale rigorosa, canone allineato al mercato (non «scontato» per riempire velocemente), garanzie coerenti con profilo inquilino. Analisi canoni: <a href=\"blog-affitti-padova-canoni-2026\">affitti Padova canoni 2026</a> e metodo resa in <a href=\"blog-rendimento-affitto-padova\">rendimento affitto Padova</a>.</p>

{blog_fig("img/blog/blog-gestione-locazione-delegata-padova-2026-rendimento.webp", "Rendimento affitto Padova — gestione delegata e redditività patrimonio")}

<h2 id="fiscalita">Fiscalità locazione e rendicontazione annuale</h2>
<p>Il reddito da locazione va dichiarato secondo regime scelto (cedolare secca o IRPEF ordinaria) — scelta che va fatta con commercialista in funzione di altri redditi e detrazioni. Righetto fornisce riepilogo incassi e spese documentate per semplificare il lavoro del professionista; non è sostituto di consulenza fiscale.</p>
<p>A fine anno utile un <strong>report unico</strong> con: canoni percepiti, spese deducibili, registrazioni ADE, eventuali crediti verso conduttore. Per chi possiede più unità, consolidamento per immobile facilita controllo redditività lorda/netta senza inventare benchmark di quartiere.</p>
<p>Contesto macro Veneto consultabile su <a href="{ISTAT_URL}" target="_blank" rel="noopener noreferrer">ISTAT prezzi abitazioni</a> e <a href="{ADE_OSSERVATORIO}" target="_blank" rel="noopener noreferrer">Osservatorio ADE</a> — utili per orientamento patrimoniale, non per calcolare imposta singola unità.</p>

<h2 id="portafoglio">Portafoglio multiplo, eredità e immobili commerciali</h2>
<p>Proprietari con <strong>più appartamenti</strong> a Padova beneficiano di un unico referente: stesso formato report, stessa rete manutentiva, stesso standard qualitativo selezione inquilini. Analisi trimestrale redditività (lordo, spese, vacancy) aiuta decisioni su ristrutturare, vendere o rilanciare canone — collegamento con <a href=\"blog-investire-immobiliare-padova\">investire immobiliare Padova</a> per angolo patrimoniale.</p>
<p>Su <strong>immobili ereditati</strong>, spesso coeredi vogliono locazione senza gestione quotidiana: mandato unico con rendicontazione pro-quota semplifica rapporti familiari. Verificare prima catasto, conformità urbanistica e eventuali vincoli testamentari.</p>
<p>Unità <strong>commerciali o uffici</strong> seguono logiche diverse (orari, destinazione d'uso, contratti commerciali): valutazione caso per caso in consulenza — pagina <a href=\"servizi\">servizi Righetto</a>.</p>

<h2 id="errori">Errori frequenti nella scelta della gestione</h2>
<ul>
<li><strong>Scegliere solo in base al compenso più basso</strong> — Tempi risposta e rete artigiani contano quanto il prezzo.</li>
<li><strong>Mandato generico</strong> — Servizi non elencati generano litigi su «extra» a consuntivo.</li>
<li><strong>Nessun report</strong> — Proprietario lontano senza visibilità incassi è un rischio.</li>
<li><strong>Delegare e poi interferire</strong> — Doppio canale con inquilino crea confusione; fidatevi del referente.</li>
<li><strong>Canone sottostimato per locare in fretta</strong> — Attira profili incompatibili con sostenibilità pagamento.</li>
<li><strong>Tralasciare assicurazione immobile</strong> — Valutare coperture con broker; danni e responsabilità civile non dormono.</li>
</ul>
<p>Checklist documenti pre-locazione resta valida anche in delega: <a href=\"blog-affittare-casa-padova-proprietario-2026\">affittare casa Padova</a> e hub <a href=\"proprietario-immobile\">proprietario immobile</a>.</p>

<h2 id="prossimi-passi">Prossimi passi con Righetto</h2>
<ol>
<li><strong>Consulenza iniziale</strong> — Telefono 049.8843484 o <a href=\"landing-consulenza-immobiliare-gratuita\">consulenza gratuita</a>: raccontate immobile, stato locazione, obiettivi.</li>
<li><strong>Sopralluogo e dossier</strong> — Verifica documenti, contratto in essere, criticità aperte.</li>
<li><strong>Proposta mandato</strong> — Servizi, compenso e reportistica concordati in sede.</li>
<li><strong>Attivazione</strong> — Incasso, manutenzione, rapporto inquilino secondo scope firmato.</li>
<li><strong>Monitoraggio</strong> — Report periodici; a ogni rinnovo rivalutare canone con OMI e comparabili.</li>
</ol>
<p>Approfondimenti correlati: <a href=\"servizio-locazioni\">servizio locazioni</a> · <a href=\"servizio-gestione\">servizio gestione</a> · <a href=\"landing-valutazione\">valutazione gratuita</a> · <a href=\"agenzia-immobiliare-padova\">agenzia immobiliare Padova</a> · <a href=\"blog-squilibrio-domanda-offerta-affitti-padova\">domanda-offerta affitti</a>.</p>

<h3>Domande da portare in agenzia</h3>
<p>Arrivare preparati accelera la consulenza. Chiedete: quanti immobili gestiti in zona mia, referente dedicato o pool, tempi medi intervento manutenzione, esempio report (anonimizzato), come gestite morosità fase 1-2-3, subentro su contratto esistente sì/no e costi. Risposte chiare prima del mandato valgono più di promesse generiche «ci pensiamo noi a tutto».</p>

<h3>Studenti, famiglie e transitorio: profili diversi</h3>
<p>La gestione delegata si adatta al profilo dell'inquilino target. Con <strong>studenti</strong>, spesso servono turni di co-inquilini, contratti transitori o 4+4 con uscita a giugno: l'agenzia coordina preavvisi e preparazione immobile per il semestre successivo. Con <strong>famiglie</strong>, i rinnovi quadriennali e le richieste di manutenzione ordinaria sono più prevedibili, ma occorre attenzione a scuole e servizi in zona. Il <strong>transitorio</strong> per lavoratori richiede verifica requisiti di legge — non ogni immobile o conduttore è idoneo. Per orientamento contrattuale: <a href=\"blog-affitto-transitorio-padova-durata-2026\">affitto transitorio Padova</a>.</p>

<p>{CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 18 settembre 2026. Fonti: OMI e Osservatorio ADE, ISTAT, Codice Civile artt. 1575-1585, L. 431/1998. Nessun dato €/mq o percentuale compenso inventato.</p>
"""


CFG = {
    "slug": SLUG,
    "filename": f"{SLUG}.html",
    "hero": "img/blog/blog-gestione-locazione-delegata-padova-2026-hero.webp",
    "title": "Gestione locazione delegata Padova 2026",
    "og_title": "Gestione locazione delegata Padova: cosa include e quando conviene",
    "meta": "Gestione locazione delegata Padova: incassi, manutenzione, morosità e rendicontazione. Cosa include, quando conviene e servizio Righetto.",
    "schema_headline": "Gestione locazione delegata Padova: cosa include e quando conviene",
    "section": "Guida proprietari",
    "cat_badge": "Proprietari · Gestione locazione",
    "bread_crumb": "Gestione locazione delegata Padova",
    "h1": "<strong>Gestione locazione delegata</strong> a Padova",
    "hero_alt": "Gestione locazione delegata Padova 2026 — servizio agenzia immobiliare proprietario",
    "body_fn": body_gestione_delegata,
    "faqs": [
        (
            "Cosa significa gestione locazione delegata?",
            "Affidare a un'agenzia l'amministrazione dell'immobile locato: incassi, rapporto inquilino, manutenzione, rinnovi e rendicontazione al proprietario.",
        ),
        (
            "Qual è la differenza tra servizio locazioni e gestione?",
            "La locazione copre ricerca inquilino e contratto iniziale; la gestione continuativa segue incassi, manutenzione e morosità per tutta la durata del rapporto.",
        ),
        (
            "Quando conviene delegare la gestione a Padova?",
            "Se non siete residenti in zona, avete più immobili, poco tempo o preferite un referente unico per manutenzione e inquilini.",
        ),
        (
            "Quanto costa la gestione immobiliare con Righetto?",
            "Il compenso si concorda in sede nel mandato — nessun listino percentuale pubblicato online. Dipende da servizi richiesti e numero unità.",
        ),
        (
            "Righetto gestisce anche immobili già locati?",
            "Sì, con subentro dopo verifica contratto, registrazione ADE e stato pagamenti. Scope definito in consulenza iniziale.",
        ),
        (
            "Come viene gestita la morosità?",
            "Con iter strutturato: sollecito, diffida, mediazione e supporto legale se necessario. Documentazione condivisa con il proprietario.",
        ),
    ],
    "related": [
        ("Affittare casa Padova", "blog-affittare-casa-padova-proprietario-2026"),
        ("Servizio gestione", "servizio-gestione"),
        ("Servizio locazioni", "servizio-locazioni"),
        ("Rendimento affitto", "blog-rendimento-affitto-padova"),
        ("Hub proprietari", "proprietario-immobile"),
        ("Valutazione gratuita", "landing-valutazione"),
    ],
    "registry": {
        "titolo": "Gestione locazione delegata Padova: cosa include e quando conviene",
        "categoria": "Guida proprietari",
        "tempo": 14,
        "contenuto": "Pillar owner gestione delegata Padova: servizi, mandato, morosità, fiscalità. CTA servizio-gestione.",
        "admin_contenuto": "Pillar eq-sep18-001 — gestione locazione delegata Padova.",
        "emoji": "🔑",
        "evidenza": True,
    },
    "static_map_key": "gestione locazione delegata padova 2026",
    "cta_banner_title": "Vuoi delegare la gestione del tuo affitto?",
    "cta_banner_text": "Consulenza gratuita — Padova, Limena e provincia. Tel. 049.8843484.",
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


def patch_llms() -> None:
    path = ROOT / "llms.txt"
    text = path.read_text(encoding="utf-8")
    if CFG["slug"] in text:
        print("llms.txt: già presente")
        return
    line = (
        f"- [Gestione locazione delegata Padova 2026]"
        f"(https://righettoimmobiliare.it/{CFG['slug']})\n"
    )
    marker = "- [Affitto studenti Padova](https://righettoimmobiliare.it/blog-affitto-studenti-padova)\n"
    if marker not in text:
        raise RuntimeError("Sezione Affitti e Locazioni non trovata in llms.txt")
    path.write_text(text.replace(marker, marker + line, 1), encoding="utf-8")
    print("llms.txt: +1 riga Affitti e Locazioni")


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
    patch_llms()
    patch_editorial_queue()


if __name__ == "__main__":
    main()
