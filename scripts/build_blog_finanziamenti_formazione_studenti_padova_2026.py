# -*- coding: utf-8 -*-
"""Blog finanza agevolata e formazione finanziata — angolo studenti Padova 2026.
Ispirato a temi contributi/formazione (senza citare enti o brand del volantino origine).
Esegui: python scripts/build_blog_finanziamenti_formazione_studenti_padova_2026.py
"""
from __future__ import annotations

import importlib.util
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE_IT = "2 ottobre 2026"
DATE_ISO = "2026-10-02"
TIME_TS = "2026-10-02T10:30:00+02:00"

OLD_SLUG = "blog-confcommercio-ascom-servizi-soci-padova-2026"
SLUG = "blog-finanza-agevolata-formazione-studenti-padova-2026"
HERO = f"img/blog/{SLUG}-hero.webp"

_BATCH_PATH = ROOT / "scripts" / "build_blog_batch_lug28_2026.py"
_spec = importlib.util.spec_from_file_location("_blog_batch_lug28", _BATCH_PATH)
_batch = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_batch)

_batch.DATE_ISO = DATE_ISO
_batch.DATE_IT = DATE_IT
_batch.TIME_TS = TIME_TS

wc = _batch.wc
aeo_box = _batch.aeo_box
sol_box = _batch.sol_box
build_html = _batch.build_html
MIN_BODY_WORDS = _batch.MIN_BODY_WORDS
CAP_BLOG_AI = _batch.CAP_BLOG_AI
CLAIM_FOOT = _batch.CLAIM_FOOT
OMI_URL = _batch.OMI_URL

ESU_PADOVA = "https://www.esu.pd.it"
REGIONE_VENETO = "https://www.regione.veneto.it"
MIUR_UNIVERSITA = "https://www.mur.gov.it/it/temi/universita"

IMAGE_SOURCES: dict[str, tuple[str, str] | list[tuple[str, str]]] = {
    # Sorgenti dedicate — niente riuso hero/zona del blog affitti studenti settembre 2026
    "hero": (
        "img/blog/blog-coliving-padova-limena-hero.webp",
        HERO,
    ),
    "body": [
        (
            "img/blog/blog-caro-affitti-padova-under-35-hero.webp",
            f"img/blog/{SLUG}-campus-zona.webp",
        ),
        (
            "img/blog/blog-coliving-padova-limena-cowork.webp",
            f"img/blog/{SLUG}-housing.webp",
        ),
        (
            "img/blog/blog-affitti-canoni-fimaa-q1-2026-padova.webp",
            f"img/blog/{SLUG}-budget.webp",
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


def build_html_ai(cfg: dict, content: str, words: int) -> str:
    html = build_html(cfg, content, words)
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


def svg_studenti_canali() -> str:
    return """<figure class="chart-wrap" aria-label="Canali finanziamenti e formazione studenti Padova">
<svg viewBox="0 0 520 280" width="100%" height="280" role="img">
<title>Schema canali agevolazioni studenti Padova</title>
<text x="260" y="24" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Dove orientarsi (schema — verificare bandi vigenti)</text>
<rect x="200" y="44" width="120" height="36" rx="8" fill="#2C4A6E"/><text x="260" y="66" text-anchor="middle" font-size="9" fill="#fff">Studente Padova</text>
<line x1="260" y1="80" x2="260" y2="100" stroke="#FF6B35" stroke-width="2"/>
<rect x="40" y="100" width="130" height="32" rx="6" fill="#3A5F8C"/><text x="105" y="120" text-anchor="middle" font-size="8" fill="#fff">ESU / alloggio</text>
<rect x="195" y="100" width="130" height="32" rx="6" fill="#FF6B35" opacity=".9"/><text x="260" y="120" text-anchor="middle" font-size="8" fill="#152435">Regione / PNRR</text>
<rect x="350" y="100" width="130" height="32" rx="6" fill="#3A5F8C"/><text x="415" y="120" text-anchor="middle" font-size="8" fill="#fff">Formazione finanziata</text>
<line x1="105" y1="132" x2="105" y2="160" stroke="#6B7A8D" stroke-width="1.5"/>
<line x1="260" y1="132" x2="260" y2="160" stroke="#6B7A8D" stroke-width="1.5"/>
<line x1="415" y1="132" x2="415" y2="160" stroke="#6B7A8D" stroke-width="1.5"/>
<text x="105" y="178" text-anchor="middle" font-size="7" fill="#6B7A8D">Canoni calmierati</text>
<text x="260" y="178" text-anchor="middle" font-size="7" fill="#6B7A8D">Nuovi posti letto</text>
<text x="415" y="178" text-anchor="middle" font-size="7" fill="#6B7A8D">ITS / competenze</text>
<text x="260" y="230" text-anchor="middle" font-size="8" fill="#6B7A8D">Righetto non eroga bandi — supporto ricerca stanza e contratti</text>
</svg>
<figcaption>Schema editoriale: incrociare sempre portali istituzionali prima di assumere ammissibilità.</figcaption>
</figure>"""


def svg_budget_stanza() -> str:
    return """<figure class="chart-wrap" aria-label="Voci budget studente e leve agevolazioni">
<svg viewBox="0 0 480 240" width="100%" height="240" role="img">
<title>Budget studente Padova — leve qualitative</title>
<text x="240" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Voci di spesa vs leve (qualitativo)</text>
<text x="70" y="55" font-size="8" fill="#152435">Canone</text>
<rect x="120" y="45" width="200" height="14" rx="4" fill="#FF6B35" opacity=".85"/>
<text x="70" y="85" font-size="8" fill="#152435">Formazione</text>
<rect x="120" y="75" width="80" height="14" rx="4" fill="#2C4A6E" opacity=".7"/>
<text x="70" y="115" font-size="8" fill="#152435">Trasporti</text>
<rect x="120" y="105" width="120" height="14" rx="4" fill="#3A5F8C" opacity=".75"/>
<text x="240" y="155" text-anchor="middle" font-size="8" fill="#6B7A8D">Agevolazioni alloggio/formazione liberano budget per canone — non sostituiscono contratto</text>
<text x="240" y="210" text-anchor="middle" font-size="8" fill="#6B7A8D">Illustrazione Righetto — non importi ufficiali</text>
</svg>
<figcaption>Leve pubbliche su housing e formazione incidono indirettamente sulla capacità di sostenere il mercato libero degli affitti.</figcaption>
</figure>"""


def body_main() -> str:
    fig1 = blog_fig(
        f"img/blog/{SLUG}-campus-zona.webp",
        "Studenti universitari Padova — zone e trasporti",
        "Contesto locazione studentesca nel Padovano — immagine editoriale.",
    )
    fig2 = blog_fig(
        f"img/blog/{SLUG}-housing.webp",
        "Posti letto e housing studentesco Veneto",
        "Domanda di alloggio e nuove residenze — verificare bandi su portali istituzionali.",
    )
    fig3 = blog_fig(
        f"img/blog/{SLUG}-budget.webp",
        "Budget affitto e costo della vita studente Padova",
        "Il canone resta voce centrale — agevolazioni vanno incrociate con ISEE e graduatorie.",
    )
    return f"""
{aeo_box(
    "In sintesi",
    "Nel 2026 circolano messaggi su <strong>contributi pubblici</strong> e "
    "<strong>formazione finanziata</strong> rivolti al tessuto produttivo del territorio. "
    "Per chi studia a <strong>Padova</strong>, l’effetto utile non è un «sconto brand» su un servizio "
    "commerciale, ma l’accesso a <strong>bandi verificabili</strong>: posti in college e residenze "
    "tramite <strong>ESU</strong>, investimenti <strong>PNRR</strong> su nuovi letti, percorsi "
    "<strong>ITS e formazione professionale</strong> con cofinanziamento pubblico quando previsto. "
    "Questa guida traduce quei temi in checklist per studenti e famiglie — senza elencare "
    "convenzioni private né nomi di imprese.",
)}

<div class="kpi-strip">
<div><strong>Padova</strong><span>Polo universitario</span></div>
<div><strong>ESU</strong><span>Alloggio agevolato</span></div>
<div><strong>PNRR</strong><span>Nuovi letti</span></div>
<div><strong>ITS</strong><span>Formazione</span></div>
</div>

<p>Quando si parla di «finanziamenti interessanti», la distinzione importante è tra
<strong>promozione commerciale</strong> (sconti su servizi) e
<strong>agevolazioni pubbliche</strong> con requisiti ISEE, merito, domanda entro scadenza.
"Gli studenti padovani convivono con entrambi i rumori informativi; qui restiamo sul secondo binario, "
"con fonti istituzionali e link interni già trattati da Righetto sul mercato affitti.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#finanza">Finanza agevolata: cosa significa per uno studente</a></li>
<li><a href="#formazione">Formazione finanziata e ITS</a></li>
<li><a href="#esu">ESU Padova e canoni calmierati</a></li>
<li><a href="#pnrr">PNRR e nuovi posti letto in Veneto</a></li>
<li><a href="#affitti">Mercato libero affitti: dove incidono le agevolazioni</a></li>
<li><a href="#checklist">Checklist pratica</a></li>
<li><a href="#righetto">Supporto Righetto</a></li>
</ol></nav>

{sol_box(
    "Come conciliare bandi pubblici e ricerca stanza sul mercato libero a Padova?",
    [
        (
            "Orientamento zone",
            "Tram, Arcella, Guizza e periferia — confronto canoni in guida dedicata",
            "canoni stanza Padova",
            "blog-stanza-universitaria-padova-canoni-2026",
        ),
        (
            "Ricerca locazione",
            "Annunci verificati e contratto registrato — settembre e tutto l’anno",
            "servizio locazioni",
            "servizio-locazioni",
        ),
        (
            "Calendario ESU",
            "Graduatorie e scadenze in parallelo al mercato libero",
            "ESU Padova",
            "https://www.esu.pd.it",
        ),
        (
            "Panorama Veneto",
            "Posti letto e studentati — articolo di contesto",
            "studentati Veneto",
            "blog-studentati-veneto-2026-posti-letto",
        ),
    ],
)}

<h2 id="finanza">Finanza agevolata: cosa cambia (e cosa no) per chi studia</h2>
<p>La «finanza agevolata» indica in genere <strong>contributi, finanziamenti agevolati o crediti d’imposta</strong>
legati a bandi pubblici — spesso nati per imprese, riqualificazioni, innovazione.
"Lo studente non apre un’azienda, ma può <strong>beneficiare indirettamente</strong> quando i bandi "
"finanziano nuove residenze, hub formativi o infrastrutture che aumentano l’offerta di alloggi e servizi "
"intorno al campus. Non esiste un unico «finanziamento studente» universale: ogni misura ha destinatari, "
"finestre temporali e documenti propri.</p>
<p>Errore frequente: confondere una campagna territoriale generica con un diritto automatico al canone "
"ridotto. Prima di rinunciare al mercato libero, verificare su
<a href="{ESU_PADOVA}" target="_blank" rel="noopener noreferrer">ESU Padova</a> e su
<a href="{REGIONE_VENETO}" target="_blank" rel="noopener noreferrer">Regione Veneto</a>
se esiste un bando aperto alla propria situazione (ISEE, corso di studi, merito).</p>

<h2 id="formazione">Formazione finanziata: percorsi ITS e competenze</h2>
<p>Il secondo filo del dibattito territoriale è la <strong>formazione finanziata</strong> — corsi
professionalizzanti cofinanziati quando previsto da programmi regionali o nazionali.
Per studenti universitari o diplomandi, l’interesse può essere duplice:
<strong>integrare competenze</strong> (digital, tecnico, lingue) e, in alcuni casi,
accedere a tirocinio o stage collegati al percorso. I requisiti non sono quelli dell’affitto:
consultare i portali <strong>ITS Veneto</strong> e l’ateneo, non annunci immobiliari.</p>
<p>Formazione finanziata e alloggio restano <strong>binari separati</strong>: un corso gratuito o
subordinato non paga il proprietario della stanza. Serve comunque budget o posto ESU per il canone.</p>
<p>A Padova conviene incrociare il sito dell’Università degli Studi per scadenze didattiche e sportelli del diritto allo studio con il calendario ESU: doppio binario riduce il rischio di presentare domande incomplete o fuori tempo massimo.</p>

{fig1}

<h2 id="esu">ESU Padova: il canale principale per canoni calmierati</h2>
<p>L’<strong>Ente regionale per il diritto allo studio universitario di Padova</strong> gestisce
college, residenze e graduatorie per posti a tariffa agevolata. È la risposta istituzionale
più diretta alla domanda «esiste un finanziamento pubblico sull’alloggio?».
Chi non entra in graduatoria resta sul <strong>mercato libero</strong>, dove Immobiliare.it Insights
"(citato in <a href="blog-stanza-universitaria-padova-canoni-2026">stanza universitaria Padova 2026</a>) "
"ha segnalato canoni medi intorno a <strong>490 €</strong> con dinamiche di crescita rispetto al 2020 "
"— dato di portale, da incrociare con comparabili reali.</p>
<p>Consiglio operativo: presentare domanda ESU nelle finestre ufficiali <strong>prima</strong> "
"di firmare contratti di locazione sul libero mercato, se l’obiettivo è il posto agevolato. "
"In parallelo, monitorare annunci su zone servite dal tram riduce il rischio di restare senza soluzione "
"a settembre.</p>

{svg_studenti_canali()}

<h2 id="pnrr">PNRR, nuove residenze e Veneto</h2>
<p>Investimenti <strong>PNRR</strong> su housing studentesco e rigenerazione urbana aumentano
posti letto calmierati in città del Veneto — tema approfondito in
<a href="blog-studentati-veneto-2026-posti-letto">studentati Veneto 2026</a> e
<a href="blog-vicenza-residenze-universitarie-calmierate-2026">residenze calmierate Vicenza</a>.
Non sono bonus immediati sul contratto privato: sono <strong>nuove camere</strong> con bandi e tempi
di consegna. Lo studente padovano deve distinguere «progetto approvato» da «posto disponibile domani».</p>

{fig2}

<table>
<thead><tr><th>Strumento</th><th>Destinatari tipici</th><th>Effetto sul canone</th></tr></thead>
<tbody>
<tr><td>Graduatoria ESU</td><td>Studenti ammessi con ISEE/merito</td><td>Canone calmierato in struttura convenzionata</td></tr>
<tr><td>Residenze PNRR</td><td>Secondo bando progetto</td><td>Offerta futura; non sostituisce contratto attuale</td></tr>
<tr><td>Formazione cofinanziata</td><td>ITS / percorsi professionali</td><td>Indiretto — competenze, non affitto</td></tr>
<tr><td>Mercato libero</td><td>Tutti con budget</td><td>Prezzo da trattativa; OMI locazioni come riferimento ADE</td></tr>
</tbody>
</table>

<h2>Riferimenti ufficiali sul mercato affitti (senza numeri inventati)</h2>
<p>Per capire se un canone proposto è in linea con il territorio, lo strumento verificabile resta l’<strong>Osservatorio del Mercato Immobiliare</strong> dell’Agenzia delle Entrate — fasce per comune e tipologia, consultabili sul <a href="{OMI_URL}" target="_blank" rel="noopener noreferrer">portale OMI</a>. I portali di annunci e le indagini di settore (come Immobiliare.it Insights citata altrove) descrivono <strong>trend</strong>, non il prezzo obbligatorio di una singola stanza.</p>
<p>Lo studente può usare OMI come termometro nelle trattative; non sostituisce visita, stato dell’immobile e clausole contrattuali. Righetto, in mandato locazione, allinea le proposte a comparables reali e documentazione — non a slogan su finanziamenti esterni.</p>

<h2 id="affitti">Mercato libero: dove incidono (davvero) le agevolazioni</h2>
<p>Le agevolazioni pubbliche <strong>non abbassano automaticamente</strong> ogni annuncio in Portello
o in Arcella. Riducono la pressione solo se aumentano posti ESU/PNRR o se lo studente
accede a quelle fasce. Sul libero mercato restano valide le regole già note:
contratto registrato, caparra, bollo, clausole su subentro e uscite — vedi
<a href="blog-contratto-affitto-padova">contratto affitto Padova</a>.</p>
<p>Per famiglie che co-firmano o garantiscono l’affitto, messaggi generici su contributi al tessuto produttivo
non sostituiscono il reddito documentato richiesto dal locatore.
Serve trasparenza su buste paga, garanzie fideiussorie o depositi — indipendentemente da bandi regionali.</p>

{svg_budget_stanza()}

<h2>Perché sentire parlare di contributi e formazione nel 2026</h2>
<p>Enti di rappresentanza e sportelli territoriali comunicano spesso pacchetti di
<strong>servizi al territorio</strong>: orientamento su bandi, formazione a costo contenuto, welfare.
Filtrati per lo studente, i contenuti utili sono: esistono risorse pubbliche
<strong>se</strong> si rientra nei requisiti; esistono percorsi formativi
<strong>se</strong> si candidano entro scadenza; non sostituiscono la ricerca proattiva di casa.
Righetto non administra bandi: aiuta quando serve <strong>stanza, contratto o zona</strong>
sul mercato libero o per proprietari che locano a studenti.</p>

<h2>Confronto con articoli già pubblicati (anti-doppione)</h2>
<p>Questo pezzo non ripete la guida canoni per microzona (→
<a href="blog-stanza-universitaria-padova-canoni-2026">canoni 2026</a>),
né il calendario affitti settembre proprietario (→
<a href="blog-affitti-studenti-settembre-padova-proprietario-2026">affitti settembre</a>).
Qui l’angolo è <strong>finanziamenti e formazione pubblica</strong> letti con occhio studente,
ispirati al filone «contributi e formazione finanziata» diffuso nel dibattito economico locale,
senza citare singole promo commerciali.</p>

{fig3}

<h2 id="checklist">Checklist studente e famiglia</h2>
<ol>
<li>Aprire la sezione alloggi su <a href="{ESU_PADOVA}" target="_blank" rel="noopener noreferrer">esu.pd.it</a> e segnare scadenze domanda.</li>
<li>Preparare ISEE universitario aggiornato e documentazione merito se richiesta.</li>
<li>In parallelo, definire budget massimo canone + spese (U, mensa, trasporti) sul libero mercato.</li>
<li>Consultare <a href="{REGIONE_VENETO}" target="_blank" rel="noopener noreferrer">regione.veneto.it</a> per bandi formazione/housing — solo testo ufficiale.</li>
<li>Per corsi ITS o upskilling, verificare portali regionali e scuola — non fidarsi di messaggi generici.</li>
<li>Prima del contratto: leggere registro, durata, clausole recesso (<a href="blog-registro-contratti-affitto-padova-2026">registro ADE</a>).</li>
<li>Se serve supporto ricerca stanza: <a href="servizio-locazioni">locazioni Righetto</a> — mediazione concordata in sede.</li>
</ol>

<h2>Glossario minimo</h2>
<ul>
<li><strong>Finanza agevolata</strong> — contributi o credito legati a bando pubblico, non sconto commerciale.</li>
<li><strong>Formazione finanziata</strong> — percorso con cofinanziamento pubblico se previsto dal bando.</li>
<li><strong>Canone calmierato</strong> — tariffa agevolata in strutture ESU/PNRR con graduatoria.</li>
<li><strong>Mercato libero</strong> — contratto privato; prezzo negoziato con riferimento OMI.</li>
</ul>
<p>Conservare copie delle domande inviate, ricevute caparra e contratto registrato: la tracciabilità pesa più di un messaggio promozionale generico.</p>

<table>
<thead><tr><th>Voce</th><th>Chi la gestisce</th><th>Rapporto con l’affitto</th></tr></thead>
<tbody>
<tr><td>Borsa di studio / no tax area</td><td>Ateneo, MUR/Regione (secondo bando)</td><td>Reddito utile al budget; non è canone calmierato</td></tr>
<tr><td>Posto ESU</td><td>ESU Padova</td><td>Canone agevolato in struttura convenzionata</td></tr>
<tr><td>Prestito dedicato</td><td>Istituto finanziario / programma nazionale</td><td>Debito da restituire; valutare costo totale</td></tr>
<tr><td>Formazione cofinanziata</td><td>Regione / enti accreditati</td><td>Competenze; non paga la stanza</td></tr>
</tbody>
</table>

<h2>ISEE universitario, borse e prestiti: altri «finanziamenti» da non confondere</h2>
<p>Accanto a ESU e PNRR, lo studente padovano incrocia spesso <strong>borse di studio</strong> e agevolazioni sul <strong>diritto allo studio</strong> legate a ISEE e merito. Non sono sconti su un servizio in vetrina: sono provvedimenti con graduatorie pubblicate dall’ateneo o dalla Regione. Un importo in busta può aiutare a pagare il canone, ma non sostituisce la ricerca dell’alloggio né la firma del contratto di locazione.</p>
<p>I <strong>prestiti studenteschi</strong> ( quando previsti da programmi nazionali o bancari dedicati ) hanno condizioni, garanzie e rimborso distinti dai contributi a fondo perduto. Prima di firmare, leggere il foglio informativo e confrontare con eventuale posto ESU: a volte il costo-opportunità del prestito supera l’attesa di graduatoria solo se i tempi sono realistici.</p>
<p>Per il reddito da <strong>tirocinio o collaborazione part-time</strong>, valgono contratti e tetti orari: utili al budget, ma il locatore privato chiede comunque stabilità del pagamento del canone. Documentazione ordinata (busta paga, garanzie familiari) resta decisiva sul mercato libero descritto nelle guide Righetto su <a href="zona-universitaria-padova">zona universitaria Padova</a>.</p>

<h2>Calendario consigliato: estate e autunno 2026</h2>
<p><strong>Giugno–luglio:</strong> aggiornare ISEE, raccogliere certificati per ESU, segnare scadenze su esu.pd.it. In parallelo, definire zone accettabili (tram, bike, auto) e budget massimo — vedi confronto periferie in articolo canoni.</p>
<p><strong>Agosto:</strong> monitorare annunci sul libero mercato senza attendere solo l’esito ESU; molti contratti per settembre si chiudono in questo mese. Verificare bandi Regione su formazione solo se si intende candidarsi a percorsi ITS autunnali.</p>
<p><strong>Settembre–ottobre:</strong> se il posto ESU non arriva, attivare piano B (stanza in condivisione, appartamento in periferia). Registrare contratto entro i termini ADE; conservare ricevute per eventuali agevolazioni fiscali che non riguardano il canone ma il reddito del locatore.</p>
<p>Questo calendario non promette tempi di bandi specifici — cambiano ogni anno — ma evita l’errore «aspetto il finanziamento» mentre il mercato libero assorbe le stanze migliori.</p>

<h2>Tre scenari tipo a Padova (qualitativi)</h2>
<p><strong>Scenario A — Posto ESU assegnato.</strong> Lo studente paga un canone calmierato in college o residenza convenzionata, con regolamento interno e scadenze ESU. Il mercato libero resta fuori finché non si cambia status o non scade il posto. Passaggio al privato: nuovo contratto, nuovo deposito, spesso in zona diversa.</p>
<p><strong>Scenario B — Solo mercato libero.</strong> Famiglia e studente definiscono budget; cercano stanza in periferia tram o in condivisione. Nessun «finanziamento» automatico sul canone: eventuali borse o redditi part-time integrano. Priorità: contratto registrato, inventario, regole convivenza.</p>
<p><strong>Scenario C — Formazione ITS parallelamente all’università.</strong> Possibile upskilling con bando regionale se ammissibili; l’orario va conciliato con lezioni UniPD. Il corso non garantisce alloggio: serve comunque ESU o stanza privata. Utile per curriculum, non per pagare due affitti.</p>
<p>Questi scenari aiutano a smontare l’idea «ho sentito che ci sono finanziamenti» senza piano operativo. Ogni strada ha portale, documenti e tempi propri.</p>

<h2>Per i proprietari che locano a studenti</h2>
<p>Dall’altra parte del tavolo, chi affitta una stanza beneficia indirettamente dello stesso ecosistema: più posti ESU/PNRR possono ridurre la domanda estrema su alcune microzone, ma il segmento libero resta ampio a Padova. Offrire contratto chiaro, registro e immobile conforme (APE, impianti) è la risposta professionale — indipendente da messaggi territoriali su contributi alle imprese.</p>
<p>Righetto supporta proprietari con <a href="blog-affittare-casa-padova-proprietario-2026">guida affittare Padova</a> e servizio locazioni; compenso concordato in sede.</p>

<h2>Domande frequenti nel passaggio scuola–università</h2>
<p><strong>«Il contributo pubblico copre tutto l’affitto in centro?»</strong> — Raramente sul libero mercato;
"ESU e residenze calmierate coprono una quota di studenti in graduatoria, non ogni contratto privato.</p>
<p><strong>«Formazione finanziata = stipendio?»</strong> — No: è investimento su competenze; eventuali "
"indennità di stage seguono regole del singolo progetto.</p>
<p><strong>«Devo aspettare un bando prima di cercare casa?»</strong> — No: in parallelo, con piano B sul libero "
"mercato se la graduatoria non assegna posto.</p>

<h2 id="righetto">Dove entra Righetto Immobiliare</h2>
<p>Dal <strong>2000</strong> su <strong>101 comuni</strong>, Righetto affianca studenti e famiglie
nella <strong>ricerca locazione</strong>, nella registrazione contratto e nel dialogo con proprietari
che affittano a universitari. Non eroghiamo bandi ESU, PNRR o formazione:
orientiamo su <strong>mercato reale</strong> e documentazione.
Per canoni e zone: articoli citati sopra; per appuntamento:
<a href="landing-consulenza-immobiliare-gratuita">consulenza gratuita</a> e tel. 049 8843484.</p>

<h2>Fonti e limiti</h2>
<p>Link istituzionali: ESU Padova, Regione Veneto, MUR università "
"(<a href="{MIUR_UNIVERSITA}" target="_blank" rel="noopener noreferrer">mur.gov.it</a>). "
"Dati canone da Immobiliare.it Insights come in articolo canoni — non OMI microzona. "
"Nessun importo di bando inventato; nessuna convenzione commerciale citata.</p>
<p>{CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> {DATE_IT}. "
"Contenuto editoriale Righetto — immagini FOTO AI.</p>
"""


FAQS = [
    (
        "Esistono finanziamenti pubblici per l’affitto studentesco a Padova?",
        "Il canale principale è ESU Padova con graduatorie e canoni calmierati; altri investimenti PNRR aumentano posti letto — verificare bandi vigenti.",
    ),
    (
        "Formazione finanziata paga la retta o l’affitto?",
        "No: riguarda percorsi formativi cofinanziati quando previsto; l’alloggio resta ESU o mercato libero.",
    ),
    (
        "Devo candidarmi a ESU anche se cerco stanza privata?",
        "Sì se volete un posto agevolato; in parallelo conviene monitorare il libero mercato per non restare senza casa.",
    ),
    (
        "Righetto gestisce bandi o contributi?",
        "No: mediazione e locazioni; i bandi si gestiscono su portali ESU/Regione.",
    ),
    (
        "Dove leggo i canoni medi di mercato?",
        "Nella guida Righetto su stanza universitaria Padova 2026 con fonte Immobiliare.it Insights.",
    ),
    (
        "PNRR significa stanza immediata?",
        "No: progetti e consegne hanno tempi; non sostituiscono contratto privato già firmato.",
    ),
]

CFG = {
    "slug": SLUG,
    "filename": f"{SLUG}.html",
    "hero": HERO,
    "hero_alt": "Finanza agevolata e formazione finanziata per studenti Padova 2026",
    "cat_badge": "Studenti · Guida",
    "h1": "<strong>Finanziamenti e formazione</strong> per studenti a Padova — cosa è pubblico e cosa no",
    "title": "Finanziamenti studenti Padova 2026: ESU e formazione",
    "og_title": "Finanziamenti e formazione studenti Padova 2026",
    "meta": "Contributi pubblici, ESU, PNRR e formazione finanziata: guida per studenti Padova senza promo commerciali. Affitti e checklist Righetto.",
    "schema_headline": "Finanza agevolata e formazione studenti Padova 2026",
    "section": "Studenti",
    "bread_crumb": "Finanziamenti studenti Padova",
    "faqs": FAQS,
    "related": [
        ("Canoni stanza Padova", "blog-stanza-universitaria-padova-canoni-2026"),
        ("Studentati Veneto", "blog-studentati-veneto-2026-posti-letto"),
        ("Contratto affitto", "blog-contratto-affitto-padova"),
        ("Servizio locazioni", "servizio-locazioni"),
    ],
    "registry": {
        "titolo": "Finanziamenti e formazione per studenti a Padova 2026",
        "categoria": "Studenti",
        "tempo": 11,
        "contenuto": "ESU, PNRR, formazione finanziata e mercato affitti — guida senza convenzioni commerciali.",
        "admin_contenuto": "Riscrittura angolo studenti — finanza agevolata/formazione da temi territoriali 2026.",
        "emoji": "🎓",
        "evidenza": True,
    },
    "static_map_key": "finanziamenti formazione studenti padova 2026",
    "cta_banner_title": "Cerchi stanza universitaria a Padova?",
    "cta_banner_text": "Locazioni e orientamento zone — Righetto dal 2000.",
    "body_fn": body_main,
}


def ensure_images() -> None:
    for src, dst in [IMAGE_SOURCES["hero"]] + list(IMAGE_SOURCES["body"]):
        src_p = ROOT / src
        dst_p = ROOT / dst
        if not src_p.is_file():
            raise SystemExit(f"Manca sorgente {src}")
        dst_p.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_p, dst_p)
    print("ensure_images: OK")


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


def remove_slug_from_site(slug: str) -> None:
    """Rimuove articolo obsoleto da registri e file."""
    old_html = ROOT / f"{slug}.html"
    if old_html.is_file():
        old_html.unlink()
        print(f"removed {old_html.name}")

    for prefix in [
        f"img/blog/{slug}-",
    ]:
        for p in (ROOT / "img" / "blog").glob(f"{slug}*"):
            p.unlink(missing_ok=True)
            print(f"removed {p.name}")

    blog = ROOT / "blog.html"
    text = blog.read_text(encoding="utf-8")
    text = re.sub(
        r"\n    \{[^}]*\"url_statico\": \"" + re.escape(slug) + r"\"[^}]*\},?",
        "",
        text,
        count=1,
    )
    blog.write_text(text, encoding="utf-8")

    admin = ROOT / "admin.html"
    atext = admin.read_text(encoding="utf-8")
    atext = re.sub(
        r"\n  \{ titolo:[^}]*url_statico: '" + re.escape(slug) + r"'[^}]*\},?",
        "",
        atext,
        count=1,
    )
    admin.write_text(atext, encoding="utf-8")

    sm = ROOT / "sitemap.xml"
    stext = sm.read_text(encoding="utf-8")
    stext = re.sub(
        r"\n  <url><loc>https://righettoimmobiliare.it/" + re.escape(slug) + r"</loc>[^<]*</url>",
        "",
        stext,
        count=1,
    )
    sm.write_text(stext, encoding="utf-8")

    hp = ROOT / "js" / "homepage.js"
    htext = hp.read_text(encoding="utf-8")
    htext = re.sub(
        r"\n    \{[^}]*\"url_statico\": \"" + re.escape(slug) + r"\"[^}]*\},?",
        "",
        htext,
        count=1,
    )
    htext = re.sub(
        r"\n    '[^']*': \{ img: '[^']*', url: '" + re.escape(slug) + r"' \},?",
        "",
        htext,
        count=1,
    )
    hp.write_text(htext, encoding="utf-8")
    print(f"registries cleaned for {slug}")


def patch_blog_html() -> None:
    path = ROOT / "blog.html"
    text = path.read_text(encoding="utf-8")
    if CFG["slug"] in text:
        return
    text = text.replace("  const articoliStatici = [\n", "  const articoliStatici = [\n" + registry_blog_entry(CFG), 1)
    path.write_text(text, encoding="utf-8")
    print("blog.html: +1")


def patch_admin_html() -> None:
    path = ROOT / "admin.html"
    text = path.read_text(encoding="utf-8")
    if CFG["slug"] in text:
        return
    r = CFG["registry"]
    entry = (
        f"  {{ titolo: {json.dumps(r['titolo'], ensure_ascii=False)}, "
        f"categoria: {json.dumps(r['categoria'], ensure_ascii=False)}, "
        f"data: '{DATE_ISO}', tempo: {r['tempo']}, stato: 'pubblicato', "
        f"autore: 'Gino Capon', emoji: '{r['emoji']}', "
        f"immagine_copertina: '{CFG['hero']}', url_statico: '{CFG['slug']}', "
        f"contenuto: {json.dumps(r['admin_contenuto'], ensure_ascii=False)}, "
        f"evidenza: true, data_pubblicazione: '{DATE_ISO}' }},\n"
    )
    text = text.replace("const _blogSeedArticles = [\n", "const _blogSeedArticles = [\n" + entry, 1)
    path.write_text(text, encoding="utf-8")
    print("admin.html: +1")


def patch_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    if CFG["slug"] in text:
        return
    insert = (
        f"  <url><loc>https://righettoimmobiliare.it/{CFG['slug']}</loc>"
        f"<lastmod>{DATE_ISO}</lastmod><changefreq>monthly</changefreq>"
        f"<priority>0.7</priority></url>\n"
    )
    text = text.replace("</urlset>", insert + "</urlset>")
    path.write_text(text, encoding="utf-8")
    print("sitemap.xml: +1")


def patch_homepage() -> None:
    path = ROOT / "js" / "homepage.js"
    text = path.read_text(encoding="utf-8")
    if CFG["slug"] in text:
        return
    text = text.replace("  const articoliStatici = [\n", "  const articoliStatici = [\n" + registry_homepage_entry(CFG), 1)
    text = text.replace("  const staticMap = {\n", "  const staticMap = {\n" + registry_static_map_entry(CFG), 1)
    path.write_text(text, encoding="utf-8")
    print("homepage.js: +1")


def main() -> None:
    remove_slug_from_site(OLD_SLUG)
    old_script = ROOT / "scripts" / "build_blog_confcommercio_ascom_padova_2026.py"
    if old_script.is_file():
        old_script.unlink()
        print("removed old build script")

    ensure_images()
    body = body_main()
    words = wc(body)
    print(f"Body words: {words}")
    out = ROOT / CFG["filename"]
    out.write_text(build_html_ai(CFG, body, words), encoding="utf-8")
    print(f"OK {CFG['filename']}")

    patch_blog_html()
    patch_admin_html()
    patch_sitemap()
    patch_homepage()


if __name__ == "__main__":
    main()
