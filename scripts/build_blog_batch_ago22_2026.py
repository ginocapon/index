# -*- coding: utf-8 -*-
"""Genera 3 articoli blog agosto 2026 — under-35 affitti, coliving, prima casa CONSAP.
Esegui da repo root: python scripts/build_blog_batch_ago22_2026.py
"""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE_IT = "22 agosto 2026"
DATE_ISO = "2026-08-22"
TIME_TS = "2026-08-22T09:00:00+02:00"

_BATCH_PATH = ROOT / "scripts" / "build_blog_batch_lug28_2026.py"
_spec = importlib.util.spec_from_file_location("_blog_batch_lug28", _BATCH_PATH)
_batch = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_batch)

_batch.DATE_ISO = DATE_ISO
_batch.DATE_IT = DATE_IT
_batch.TIME_TS = TIME_TS

STYLE_BLOCK = _batch.STYLE_BLOCK
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
MIN_BODY_WORDS = _batch.MIN_BODY_WORDS
CAP_BLOG_AI = _batch.CAP_BLOG_AI

REGISTRY_PATH = ROOT / "scripts" / "ago22_2026_registry.json"
EDITORIAL_QUEUE_PATH = ROOT / "data" / "editorial-queue.json"

CNA_PADOVA_URL = "https://www.cnapadova.it"
IMMOBILIARE_INSIGHTS = "https://www.immobiliare.it/insights/"
GAZZETTINO_AFFITTI = (
    "https://www.ilgazzettino.it/nordest/padova/"
    "affitti_prezzi_stanze_studenti_aumenti-9522717.html"
)
WIRED_COLIVING = "https://www.wired.it/article/coliving-startup-habyt/"
DISTRETTO_COLIVING = "https://distrettocasainvestimenti.com/co-living-in-italia/"
MONEY_UNDER36 = "https://www.money.it/mutuo-giovani-under-36-garanzia-statale-requisiti-e-come-funziona"
NOTAI_ONLINE = "https://notaionline.it/guida/mutuo-prima-casa-under-36-agevolazioni/"


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


EXPANSION_AFFITTI_UNDER35 = [
    "Il caro affitti a Padova colpisce soprattutto chi ha meno di 35 anni e stipendio medio: il rapporto canone/reddito diventa il primo filtro prima ancora della metratura desiderata.",
    "La CNA Padova ha segnalato un incremento degli affitti del +43% tra il 2019 e il 2025 nel territorio provinciale: dato da incrociare con le fasce OMI locazione ADE, non con prezzi inventati per singole vie.",
    "Per un bilocale da 70 mq il riferimento CNA indica canoni intorno a 1.090 euro mensili nel 2026: utile come ordine di grandezza, da verificare su microzona e stato dell'immobile.",
    "Le stanze in affitto a Padova, secondo Immobiliare.it Insights e riprese de Il Gazzettino (marzo 2026), si collocano tra 335 e 490 euro al mese a seconda di zona, arredo e vicinanza all'università.",
    "Gli under 35 spesso scelgono tra monolocale in semicentro, stanza in appartamento condiviso o spostamento verso Limena, Rubano e Vigodarzere per abbassare il canone mensile.",
    "Il contratto 4+4 resta lo standard per famiglie e coppie; per giovani lavoratori il transitorio può essere opzione se documentata la necessità temporanea — leggere sempre durata e clausole recesso.",
    "La registrazione del contratto presso l'Agenzia delle Entrate entro 30 giorni tutela detrazioni fiscali e certificazioni di residenza: senza registrazione, problemi con anagrafe e bonus.",
    "Il deposito cauzionale massimo è di tre mensilità per contratti abitativi ordinari: versare solo dopo aver letto inventario, stato impianti e regole condominiali su animali e orari.",
    "Confrontare almeno tre annunci comparabili (stessa metratura ±10%, stesso piano indicativo) evita di accettare un canone fuori mercato rispetto alla fascia OMI del semestre.",
    "Zone universitarie (Via VIII Febbraio, Portello, Arcella) mantengono domanda elevata: chi cerca stanza deve preparare documenti reddito, garanzie e referenze prima della visita.",
    "Il tram e le linee extraurbane influenzano il budget: risparmiare 150 euro di affitto spendendo 80 in mezzi può convenire solo se i tempi di percorrenza sono sostenibili ogni giorno.",
    "Per smart worker under 35 conta la stabilità della connessione mobile in appartamento: verificare in visita segnale e presenza fibra o ADSL prima di firmare.",
    "Il canone concordato vincola il prezzo ma offre agevolazioni fiscali; il libero 4+4 lascia più margine negoziale — scelta da valutare con commercialista e lettura normativa aggiornata.",
    "Spese condominiali e riscaldamento centralizzato possono aggiungere 80–150 euro al mese: chiedere ultimo rendiconto e ripartizione quote prima di calcolare il budget totale.",
    "Gli studenti fuori sede spesso cercano secondo semestre: anticipare la ricerca di marzo–aprile riduce il rischio di accettare stanze sovraprezzate a settembre.",
    "Limena e la prima cintura nord attraggono giovani coppie che lavorano a Padova: otto chilometri in mappa non equivalgono a venti minuti se la tangenziale è congestionata alle 8.",
    "Red flag per under 35: annunci senza foto interni, richiesta bonifico senza contratto, assenza APE, rifiuto di mostrare planimetria catastale o contratto tipo prima della caparra.",
    "Il reddito netto mensile dovrebbe rispettare la regola prudenziale canone ≤ 30–35% del netto: con 1.400 euro netti, un affitto sopra 490 euro lascia poco margine per spese fisse.",
    "Coabitazione con coinquilino riduce il costo per metro quadro ma introduce regole di convivenza: preferire contratti con nominativi chiari e ripartizione spese scritta.",
    "L'Osservatorio del Mercato Immobiliare ADE pubblica trend semestrali aggregati utili al contesto macro; per il singolo bilocale servono le fasce OMI del comune e della microzona.",
    "ISTAT monitora l'andamento temporale dei prezzi abitazioni: complementare a OMI per capire direzione del mercato, non per quotare il monolocale in Via Savonarola.",
    "Per chi esce dalla casa familiare, il primo affitto richiede anche budget per arredo minimo, utenze allacciamento e assicurazione RC: sommare tutto al canone prima di decidere.",
    "Le agevolazioni per giovani in locazione variano nel tempo: verificare sempre normativa vigente e non affidarsi a post social datati — fonte ufficiale Agenzia delle Entrate.",
    "Righetto coordina locazioni tradizionali su Padova e provincia dal 2000: visite qualificate, contratti registrati e qualifica inquilino — compenso concordato in sede, nessun listino online.",
    "Cross-link utili: guida affitti studenti Padova, canoni 2026, rendimento affitto e servizio locazioni completano la lettura senza duplicare l'angolo under 35.",
    "Ultimo controllo prima della firma: inventario fotografico, lettura regolamento condominiale, verifica contatori e intestazione utenze — checklist che evita contestazioni al recesso.",
    "Il mercato padovano nel 2026 premia chi si muove con documenti pronti: busta paga, contratto lavoro o lettera università, garanzie e referenze accelerano la selezione del locatore.",
    "Non confondere emergenza abitativa con caro affitti strutturale: per il secondo tema esiste contenuto dedicato; qui focus su strategie pratiche per under 35 con reddito da lavoro o studio.",
    "Per approfondire zone limitrofe meno costose del centro, la pagina zona Limena offre contesto su servizi, collegamenti e profilo domanda nella prima cintura nord-ovest.",
    "Form lead in fondo pagina con provenienza slug permette follow-up personalizzato: indicare budget massimo, zona preferita e data ingresso accelera la risposta in orario 049.8843484.",
    "La detrazione per canoni di locazione richiede contratto registrato e pagamenti tracciabili: conservare ricevute bonifico e modello di registrazione ADE per la dichiarazione dei redditi.",
    "Gli under 35 con contratto a tempo determinato possono affrontare maggiore scrutinio del locatore: presentare lettera datore di lavoro, eventuale garante e storico pagamenti precedenti.",
    "Il mercato delle stanze a Padova in zona ESU e vicinanze ospedali tiene canoni sostenuti per domanda costante: prenotare visite in settimana per evitare code nel weekend di inizio semestre.",
    "Per coppie under 35 il bilocale in cintura con due posti auto evita conflitti logistici quando entrambi lavorano in direzioni opposte — verificare box o parcheggio incluso nel canone.",
    "La clausola di aggiornamento ISTAT nel contratto 4+4 impatta il budget a medio termine: leggere percentuale e frequenza prima di firmare, soprattutto con stipendio fisso.",
    "Chi esce da un affitto condiviso deve gestire disdetta, restituzione deposito e inventario: pianificare il passaggio al nuovo contratto con almeno 30-45 giorni di margine.",
    "I portali segnalano tempi medi di assorbimento più brevi per immobili arredati e fotografati professionalmente: come inquilino, privilegiate annunci completi per evitare sorprese in visita.",
    "Il riscaldamento autonomo vs centralizzato cambia la bolletta invernale di decine di euro: chiedere storico consumi o visura contatori prima di impegnarsi su un canone limite.",
    "Per neolaureati padovani il primo contratto spesso richiede garanzia parentale: preparare documenti del garante con lo stesso livello di cura dei propri.",
    "La mediazione Righetto su locazioni include qualifica inquilino e verifica mandato proprietario: riduce rischi per entrambe le parti rispetto a trattative solo via messaggistica.",
    "Confrontare il costo totale mensile tra Padova centro e Limena includendo abbonamento mezzi, carburante e tempo: un risparmio di 200 euro di affitto può azzerarsi con due ore giornaliere in traffico.",
    "Le agevolazioni per giovani inserimento lavorativo non sostituiscono un canone sostenibile: il budget abitativo resta ancorato al reddito netto e alle spese non negoziabili.",
    "In caso di lavoro ibrido, valutare una stanza più grande o angolo studio rispetto al solo dormitorio: il risparmio su uno spazio inadeguato si paga in produttività e stress.",
    "Prima di accettare subentro in contratto esistente, verificare consenso scritto del locatore e stato del deposito: subentri mal gestiti generano contenziosi frequenti tra coinquilini.",
]

EXPANSION_COLIVING = [
    "Il coliving nel Padovano è un trend informativo per giovani professionisti: spazi condivisi con servizi inclusi, diverso dalla locazione tradizionale gestita da agenzia immobiliare.",
    "Articoli su Wired e startup come Habyt descrivono modelli di coliving in grandi città: riferimento utile al concetto, non promessa che Righetto offra coliving — qui guida informativa.",
    "Distretto Casa Investimenti analizza il co-living in Italia come asset per investitori: utile per capire il fenomeno, non per confondere operatore hospitality con mediazione locazioni classiche.",
    "Righetto Immobiliare non gestisce strutture coliving: per affitti residenziali tradizionali (bilocale, trilocale, stanze in appartamento) il servizio locazioni resta il canale corretto.",
    "Il coliving tipico include camera privata, aree comuni curate, Wi-Fi e pulizie: il canone può essere più alto della stanza in coinquilinato ma include servizi che altrimenti si pagano a parte.",
    "Il coinquilino in appartamento privato offre il minor costo per metro quadro ma massima variabilità nella convivenza: contratto e regole vanno chiariti prima dell'ingresso.",
    "Il monolocale tradizionale garantisce privacy totale a prezzo generalmente superiore alla stanza: scelta frequente per professionisti con reddito stabile e smart working frequente.",
    "Limena e la cintura padovana attirano professionisti che lavorano in area industriale nord-est: coliving urbano resta concentrato in capoluoghi — verificare offerta reale prima di aspettative da articoli nazionali.",
    "Prima di firmare un contratto coliving, leggere durata minima, recesso, deposito, regolamento ospiti e cosa è incluso nel canone (pulizie, utenze, parcheggio).",
    "Il contratto coliving può avere natura locazione, ospitalità o mista: impatto fiscale e tutela diverso — consultare commercialista per il proprio caso, non solo il marketing dell'operatore.",
    "Per giovani under 35 in trasferta breve, il coliving può ridurre attrito burocratico; per famiglie o coppie stabili resta più adatta la locazione 4+4 su appartamento intero.",
    "Coworking integrato nel coliving attira freelance e remote worker: verificare orari accesso, posti lavoro e rumore nelle aree comuni in visita reale, non solo su render.",
    "Il confronto costi va fatto su canone totale mensile inclusivo: una stanza a 450 euro con utenze escluse può costare come coliving a 550 con tutto incluso.",
    "Padova universitaria mantiene domanda stanze classica: il coliving professionale convive con mercato studentesco — target e posizione micro-zonale determinano quale soluzione ha senso.",
    "Non promettiamo disponibilità coliving Righetto: se cercate bilocale o trilocale in affitto tradizionale, servizio locazioni e catalogo immobili sono i riferimenti operativi.",
    "Red flag coliving: assenza contratto scritto, richiesta pagamenti in contanti, promesse servizi non elencati nel regolamento, strutture senza conformità urbanistica verificabile.",
    "Il profilo giovane professionista valuta anche tempi di spostamento verso ospedale, università o zona industriale: coliving in periferia con bus limitati può non compensare il risparmio.",
    "Co-living e coinquilinato condividono aree comuni ma governance diversa: nel coliving un operatore gestisce regole; nel coinquilinato dipende da accordi tra privati.",
    "Per investitori il coliving è asset alternativo; per inquilino è scelta abitativa: non confondere rendimento atteso dell'investitore con convenienza per chi cerca casa stabile.",
    "Verificare recensioni verificabili e presenza fisica della struttura: startup e operatori hospitality vanno valutati come qualsiasi fornitore di servizi abitativi.",
    "Il mercato padovano 2026 resta dominato da locazioni tradizionali: coliving è nicchia informativa — utile conoscere, non unico percorso per under 35.",
    "Cross-link: loft aziende cucina condivisa tratta angolo corporate diverso; affitti Limena e guida affitti studenti completano senza sovrapposizione tematica.",
    "Righetto in Via Roma 96 dal 2000: 350+ immobili, 101 comuni, 127 recensioni 4,9/5 — mediazione locazioni classiche con compenso concordato in sede.",
    "Prima visita a struttura coliving: chiedere planimetria, regolamento, esempio contratto tipo e policy su ospiti — stessa prudenza di una visita appartamento tradizionale.",
    "Limena come base per professionisti padovani: coliving in capoluogo vs affitto tradizionale in cintura è scelta budget-tempo — calcolare costo totale e percorrenza reale.",
    "Ultimo aggiornamento consigliato: verificare offerta coliving disponibile alla data di lettura; articolo redatto 22 agosto 2026 con fonti informative — nessuna promessa servizi Righetto coliving.",
    "Form consulenza in fondo pagina: per locazioni tradizionali indicare tipologia, budget e zona; Righetto risponde in orario di apertura senza pubblicare tariffe mediazione online.",
    "Giovani professionisti in cerca di flessibilità possono valutare transitorio + mobiliario essenziale come alternativa intermedia tra stanza e monolocale arredato.",
    "La trasparenza AI Act su immagini editoriali di questo articolo non implica che le strutture fotografate esistano: illustrazioni informative, non documentazione fotografica di immobili reali.",
    "Per approfondire canoni e zone Padova 2026, leggere articolo affitti canoni e confronto rendimento locativo — angoli complementari a questa guida coliving.",
    "Operatori coliving nazionali citati da Wired possono non avere sede nel Veneto: verificare indirizzo legale e recapiti italiani prima di versare caparre.",
    "Il coworking in abbonamento separato costa 150-300 euro al mese in città medie: nel coliving può essere incluso — confrontare pacchetti reali, non solo headline marketing.",
    "Giovani medici e infermieri in turnazione ospedaliera valutano distanza da Policlinico e Ospedale Giustinianeo: coliving urbano vince su tempistica, cintura su budget.",
    "La durata minima di soggiorno in strutture hospitality può penalizzare chi trova lavoro stabile altrove: leggere penali recesso anticipate rispetto al 4+4 classico.",
    "Per coppie under 35 il monolocale tradizionale resta spesso la scelta più prevedibile fiscalmente: Righetto supporta ricerca con visite e contratto registrato.",
    "Annunci che usano parola coliving per stanze in appartamento privato creano confusione: chiedere sempre chi è il locatore e quale contratto si firma.",
    "Il deposito in strutture gestite può superare tre mensilità se in forma di membership: distinguere da cauzione locazione abitativa ordinaria.",
    "Limena offre collegamenti bus verso Padova con frequenze da verificare su orari serali: professionisti con turni notturni devono testare rientro reale.",
    "La domanda di affitti tradizionali a Limena resta trainata da famiglie e pendolari: non aspettarsi offerta coliving strutturata come a Milano o Roma.",
    "Cross-selling servizi (lavanderia, eventi, community manager) nel coliving ha costo: chiedere listino servizi opzionali non inclusi nel canone base.",
    "Per investitori il rendimento coliving è tema distinto: inquilino deve valutare solo convenienza abitativa e tutela contrattuale, non ROI del fondo.",
    "Righetto può affiancare nella ricerca bilocale per due professionisti che hanno valutato e scartato coliving per costi o rigidità contrattuale.",
    "Verificare conformità urbanistica e certificazioni sicurezza in strutture condivise: stessi standard attesi per affitto tradizionale in condominio.",
    "Il mercato padovano resta trasparente sulle locazioni classiche tramite OMI: coliving richiede due diligence aggiuntiva su operatore e contratto.",
    "Professionisti in trasferta breve a Padova possono valutare residence o appartamenti serviti oltre al coliving: confrontare costo settimanale e flessibilità uscita.",
    "La community events calendar in alcune strutture coliving è inclusa nel canone: per chi lavora lungo orario può essere valore aggiunto o costo inutile — valutare abitudini reali.",
    "Gli under 35 con animali domestici devono verificare regolamento coliving: molte strutture hospitality limitano pets, diversamente da alcuni contratti 4+4 negoziabili.",
    "La posizione micro-zonale a Padova (Arcella, Portello, Stanga) cambia accesso a servizi e rumore: coliving in zona trafficata non compensa se si cerca quiete per smart working.",
    "Righetto in Via Roma 96 offre consulenza su affitto tradizionale anche a chi ha valutato coliving e preferisce percorso documentale consolidato con registrazione ADE.",
    "Il coinquilino scelto con criterio e contratto chiaro batte coliving costoso per chi ha già rete sociale stabile a Padova — costo non è l'unico driver.",
    "Per neolaureati che entrano in azienda padovana, il primo anno può essere transitorio in stanza: pianificare passaggio a bilocale quando reddito si stabilizza.",
    "Chiedere sempre referenze verificabili dell'operatore coliving e storico recensioni su piattaforme indipendenti prima di impegnare caparra significativa.",
    "Il contratto coliving con clausola arbitrale estera complica tutela consumatore: preferire foro italiano e legge italiana per residenti che lavorano a Padova.",
]

EXPANSION_PRIMA_CASA = [
    "La prima casa under 36 a Padova nel 2026 richiede distinzione netta tra agevolazioni ancora attive e misure scadute: errore frequente è citare bonus 2024 come se fossero validi oggi.",
    "La Legge 207/2024 ha prorogato la garanzia CONSAP sul mutuo prima casa per under 36 fino al 31 dicembre 2027: fonte da verificare su testo normativo e comunicati istituzionali.",
    "Il bonus fiscale prima casa under 36 è scaduto il 31 dicembre 2024 secondo sintesi Money.it e NotaiOnline: non pianificare acquisto nel 2026 contando su quella misura.",
    "CONSAP garantisce fino all'80% dell'importo del mutuo per giovani che rispettano requisiti ISEE, età e prima casa: la banca valuta comunque merito creditizio e perizia immobile.",
    "Under 36 significa aver compiuto 36 anni nell'anno in corso secondo interpretazioni consolidate: verificare con banca e notaio la data limite alla firma del rogito.",
    "Il mutuo prima casa a Padova segue le stesse regole nazionali: prezzo immobile, anticipo, spese notarili e imposte vanno sommati — non basta il listino in annuncio.",
    "Le fasce OMI ADE per Padova e comuni limitrofi (Limena, Rubano) servono a banca e perito per valutare coerenza prezzo richiesto vs mercato — consultare portale OMI semestre corrente.",
    "Prima casa implica requisito di non proprietà di altre abitazioni ad uso abitativo nel territorio dello Stato: attenzione a quote ereditate o nuda proprietà.",
    "L'ISEE aggiornato è documento chiave per accesso garanzia CONSAP: prepararlo prima del preventivo mutuo evita ritardi quando si trova l'immobile giusto.",
    "Spese notarili e imposte di registro agevolate per prima casa hanno regole proprie distinte dal bonus fiscale scaduto: commercialista e notaio confermano aliquote applicabili.",
    "Un bilocale in semicentro padovano vs trilocale a Limena cambia prezzo, mutuo e spese: confrontare costo totale mensile (rata + condominio + bollette), non solo rata mutuo.",
    "La perizia bancaria può essere inferiore al prezzo richiesto: in quel caso aumenta l'anticipo necessario — comune in mercato competitivo per immobili ristrutturati.",
    "Proposta d'acquisto condizionata a mutuo è prassi normale: presentare lettera banca o broker serio accelera la trattativa con venditore e agenzia.",
    "Documenti immobile per rogito: APE, visure, planimetria conforme, certificazioni impianti — Righetto coordina il percorso documentale, non sostituisce consulenza fiscale.",
    "Giovani coppie under 36 possono acquistare con redditi combinati: banca valuta capacità di rimborso congiunta e garanzie — verificare policy istituto di credito.",
    "Non confondere articolo agevolazioni prima casa generico con questa guida CONSAP Padova 2026: angoli editoriali distinti nel catalogo blog Righetto.",
    "Il mercato padovano 2026 mostra domanda su ristrutturati pronti: under 36 competitivi se hanno anticipo e garanzia CONSAP già qualificati prima della visita.",
    "Limena e cintura offrono metrature più ampie a parità rata: pendolari accettano spostamento per giardino o terzo vano — calcolare costi auto o mezzi pubblici.",
    "Red flag acquisto: prezzo sotto OMI minimo senza spiegazione, assenza APE, difformità planimetria non sanata, venditore che rifiuta compromesso registrato.",
    "ISTAT e Osservatorio ADE danno contesto macro prezzi: per offerta su singolo appartamento servono comparabili locali e visita con checklist tecnica.",
    "Righetto dal 2000 su 101 comuni: consulenza acquisto prima casa, ricerca immobili, coordinamento rogito — compenso mediazione concordato in sede, nessun listino online.",
    "Cross-link: servizio mutuo, landing consulenza gratuita, zona Limena e guida acquisto Limena completano il percorso under 36 senza duplicare contenuti.",
    "Tempistiche tipiche: preventivo mutuo 2–4 settimane, ricerca immobile variabile, compromesso, perizia, rogito — pianificare senza scadenze fiscali 2024 ormai chiuse.",
    "Under 36 che attendono ulteriori bonus rischiano di perdere opportunità su immobile giusto: focus su CONSAP attivo e imposte prima casa vigenti, non su misure scadute.",
    "Ultimo aggiornamento: 22 agosto 2026 — verificare normativa e circolari CONSAP alla data di lettura; nessun dato €/mq inventato per Padova in questo articolo.",
    "Form lead in fondo pagina: indicare budget, zona preferita e se garanzia CONSAP già in valutazione in banca — risposta personalizzata in orario apertura.",
    "Perizia immobile e mutuo verde (classe A/B) possono offrire condizioni banca migliori: APE valido e documentazione lavori supportano la trattativa con istituto di credito.",
    "Acquisto prima casa under 36 con genitori garanti: prassi ancora diffusa dove CONSAP non copre interamente il fabbisogno — policy bancarie da verificare caso per caso.",
    "Trasparenza editoriale: immagini AI in questo articolo illustrano scenari tipo mutuo e coppia acquirente, non fotografie di clienti o immobili specifici Righetto.",
    "Padova resta mercato con domanda studentesca e familiare: under 36 in acquisto competono con investitori su bilocali ristrutturati — velocità e documenti fanno la differenza.",
    "Il mutuo a tasso fisso offre rata prevedibile per under 36 con primo impiego: confrontare TAEG e spese istruttoria tra almeno due istituti prima di scegliere.",
    "La surroga mutuo può intervenire dopo rogito se condizioni migliorano: non bloccare acquisto per piccoli spread se immobile e prezzo sono quelli giusti.",
    "Le imposte di registro agevolate prima casa non vanno confuse con detrazioni ristrutturazione: calcolare costo fiscale totale al rogito con notaio.",
    "Un immobile con classe energetica G può essere scontato in trattativa ma costare in riqualificazione: stimare interventi oltre rata mutuo per under 36 con budget limitato.",
    "La proposta con prezzo legato a esito perizia protegge l'acquirente under 36: clausola standard in mercato ordinato quando si usa garanzia CONSAP.",
    "Compromesso registrato con caparra confirmatoria vincola entrambe le parti: verificare termini uscita se mutuo viene negato nonostante pre-approvazione.",
    "Per under 36 in convivenza non matrimoniale, banca può richiedere entrambi come coobbligati: chiarire quote proprietà e responsabilità prima del rogito.",
    "Il mercato Limena per prima casa under 36 premia trilocali con spazio smart working: confrontare rata mutuo con costo affitto equivalente per capire convenienza acquisto.",
    "Documenti catastali aggiornati e APE valido accelerano perizia: venditori che posticipano consegna documenti allungano tempi e rischiano perdere acquirente qualificato.",
    "La consulenza Righetto gratuita in sede chiarisce passi tra ricerca, offerta e rogito senza pubblicare tariffe mediazione: indicare budget e zona per appuntamento mirato.",
    "Non affidarsi a post social che promettono bonus 2025 under 36: verificare solo Legge 207/2024, sito CONSAP e comunicati Ministero Economia.",
    "Gli under 36 che attendono ulteriori proroghe bonus fiscale possono perdere immobile idoneo: focus su CONSAP e condizioni mutuo disponibili oggi.",
    "Il rogito con mutuo ipotecario richiede polizza incendio e scelta tra ipotecaria e non: costi assicurativi vanno nel calcolo rata totale mensile.",
    "Perizia bancaria inferiore al prezzo è frequente su immobili sopra OMI massimo: negoziare riduzione o aumentare anticipo prima di procedere.",
    "La surroga dopo rogito non recupera bonus fiscale scaduto: pianificare fiscalità al momento dell'acquisto, non a posteriori.",
    "Gli under 36 con reddito variabile (provvigioni, partita IVA) devono documentare storico triennale per banca: preparare bilanci o dichiarazioni anticipate.",
    "Il compromesso con penale caparra protegge venditore e acquirente: importi e termini vanno concordati con notaio prima della firma.",
    "Acquistare in asta con CONSAP richiede due diligence extra su stato occupazione e passività: percorso distinto da compravendita ordinaria.",
    "La scelta tra tasso fisso e variabile impatta il budget under 36 per tutta la durata mutuo: simulare scenari con banca prima di vincolarsi.",
    "Righetto segnala immobili con documentazione completa agli acquirenti under 36 qualificati: velocità in trattativa quando CONSAP e anticipo sono pronti.",
    "Verificare alla data di rogito — non solo alla domanda mutuo — di avere ancora meno di 36 anni se la banca condiziona garanzia CONSAP all'età anagrafica.",
]


def svg_affitti_trend() -> str:
    return """<figure class="blog-fig" style="padding:1rem;background:var(--sfondo)">
<svg viewBox="0 0 560 260" width="100%" height="260" role="img" aria-labelledby="affitti-trend-title">
<title id="affitti-trend-title">Trend affitti Padova 2019-2025 — CNA +43%</title>
<text x="280" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Affitti provincia Padova: +43% (2019-2025) — fonte CNA Padova</text>
<line x1="60" y1="200" x2="500" y2="200" stroke="#E1DBD1" stroke-width="2"/>
<line x1="60" y1="50" x2="60" y2="200" stroke="#E1DBD1" stroke-width="2"/>
<rect x="90" y="165" width="50" height="35" fill="#2C4A6E" opacity="0.75"/>
<text x="115" y="158" text-anchor="middle" font-size="8" fill="#6B7A8D">2019</text>
<rect x="170" y="150" width="50" height="50" fill="#2C4A6E" opacity="0.8"/>
<text x="195" y="143" text-anchor="middle" font-size="8" fill="#6B7A8D">2021</text>
<rect x="250" y="130" width="50" height="70" fill="#3A5F8C"/>
<text x="275" y="123" text-anchor="middle" font-size="8" fill="#6B7A8D">2023</text>
<rect x="330" y="95" width="50" height="105" fill="#FF6B35"/>
<text x="355" y="88" text-anchor="middle" font-size="8" fill="#6B7A8D">2025</text>
<text x="355" y="110" text-anchor="middle" font-size="9" fill="#152435" font-weight="700">+43%</text>
<rect x="410" y="115" width="50" height="85" fill="#FF8F5E"/>
<text x="435" y="108" text-anchor="middle" font-size="8" fill="#6B7A8D">2026</text>
<text x="280" y="235" text-anchor="middle" font-size="9" fill="#6B7A8D">Schema indicativo — valori assoluti su OMI ADE e portali</text>
</svg>
<figcaption>Trend affitti nel Padovano secondo CNA Padova (+43% 2019-2025). Confrontare sempre con fasce OMI locazione ADE del semestre corrente.</figcaption>
</figure>"""


def svg_affitto_stipendio() -> str:
    return """<figure class="blog-fig" style="padding:1rem;background:var(--sfondo)">
<svg viewBox="0 0 520 220" width="100%" height="220" role="img" aria-labelledby="affitto-stip-title">
<title id="affitto-stip-title">Rapporto canone vs stipendio netto under 35</title>
<text x="260" y="20" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Regola prudenziale: canone ≤ 30-35% del netto mensile</text>
<rect x="40" y="50" width="200" height="28" rx="6" fill="#2C4A6E"/><text x="140" y="68" text-anchor="middle" font-size="10" fill="#fff">Stipendio netto 1.400 €</text>
<rect x="40" y="90" width="70" height="28" rx="6" fill="#FF6B35"/><text x="75" y="108" text-anchor="middle" font-size="9" fill="#152435">490 € (35%)</text>
<rect x="40" y="130" width="200" height="28" rx="6" fill="#E1DBD1"/><text x="140" y="148" text-anchor="middle" font-size="9" fill="#6B7A8D">Resto: utenze, cibo, trasporti</text>
<rect x="280" y="50" width="200" height="28" rx="6" fill="#2C4A6E"/><text x="380" y="68" text-anchor="middle" font-size="10" fill="#fff">Stipendio netto 1.800 €</text>
<rect x="280" y="90" width="90" height="28" rx="6" fill="#FF6B35"/><text x="325" y="108" text-anchor="middle" font-size="9" fill="#152435">630 € (35%)</text>
<rect x="280" y="130" width="200" height="28" rx="6" fill="#E1DBD1"/><text x="380" y="148" text-anchor="middle" font-size="9" fill="#6B7A8D">Margine maggiore per risparmio</text>
<text x="260" y="195" text-anchor="middle" font-size="8" fill="#6B7A8D">Esempio didattico — adattare al proprio reddito e canone zona</text>
</svg>
<figcaption>Schema rapporto affitto/stipendio per under 35. Con canone CNA ~1.090 € su bilocale 70 mq servono due redditi o zone più economiche.</figcaption>
</figure>"""


def svg_coliving_confronto() -> str:
    return """<figure class="blog-fig" style="padding:1rem;background:var(--sfondo)">
<svg viewBox="0 0 540 250" width="100%" height="250" role="img" aria-labelledby="coliving-cmp-title">
<title id="coliving-cmp-title">Coliving vs coinquilino vs monolocale — schema costi</title>
<text x="270" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Confronto qualitativo soluzioni abitative giovani professionisti</text>
<rect x="30" y="45" width="150" height="120" rx="10" fill="#2C4A6E" opacity="0.9"/>
<text x="105" y="72" text-anchor="middle" font-size="11" fill="#fff" font-weight="600">Coliving</text>
<text x="105" y="92" text-anchor="middle" font-size="8" fill="rgba(255,255,255,.85)">Servizi inclusi</text>
<text x="105" y="108" text-anchor="middle" font-size="8" fill="rgba(255,255,255,.85)">Operatore gestisce</text>
<text x="105" y="140" text-anchor="middle" font-size="9" fill="#FF8F5E">Canone medio-alto</text>
<rect x="195" y="45" width="150" height="120" rx="10" fill="#FF6B35" opacity="0.85"/>
<text x="270" y="72" text-anchor="middle" font-size="11" fill="#152435" font-weight="600">Coinquilino</text>
<text x="270" y="92" text-anchor="middle" font-size="8" fill="#152435">Costo più basso</text>
<text x="270" y="108" text-anchor="middle" font-size="8" fill="#152435">Regole tra privati</text>
<text x="270" y="140" text-anchor="middle" font-size="9" fill="#152435">Variabilità alta</text>
<rect x="360" y="45" width="150" height="120" rx="10" fill="#3A5F8C"/>
<text x="435" y="72" text-anchor="middle" font-size="11" fill="#fff" font-weight="600">Monolocale</text>
<text x="435" y="92" text-anchor="middle" font-size="8" fill="rgba(255,255,255,.85)">Privacy totale</text>
<text x="435" y="108" text-anchor="middle" font-size="8" fill="rgba(255,255,255,.85)">Contratto 4+4</text>
<text x="435" y="140" text-anchor="middle" font-size="9" fill="#FF8F5E">Canone più alto</text>
<text x="270" y="225" text-anchor="middle" font-size="8" fill="#6B7A8D">Fonte metodo: guida informativa Righetto — no servizio coliving</text>
</svg>
<figcaption>Schema confronto coliving, coinquilino e monolocale. Righetto gestisce locazioni tradizionali, non strutture coliving.</figcaption>
</figure>"""


def svg_coliving_padova() -> str:
    return """<figure class="blog-fig" style="padding:1rem;background:var(--sfondo)">
<svg viewBox="0 0 520 200" width="100%" height="200" role="img" aria-labelledby="coliving-map-title">
<title id="coliving-map-title">Coliving urbano vs affitto cintura Padova</title>
<text x="260" y="20" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Dove si colloca l'offerta coliving vs locazioni classiche</text>
<circle cx="260" cy="100" r="55" fill="none" stroke="#2C4A6E" stroke-width="2"/>
<text x="260" y="95" text-anchor="middle" font-size="10" fill="#2C4A6E" font-weight="600">Padova centro</text>
<text x="260" y="112" text-anchor="middle" font-size="8" fill="#6B7A8D">Coliving nicchia</text>
<circle cx="260" cy="100" r="85" fill="none" stroke="#FF6B35" stroke-width="1.5" stroke-dasharray="4,3"/>
<text x="360" y="55" font-size="9" fill="#FF6B35">Limena · Rubano</text>
<text x="360" y="68" font-size="8" fill="#6B7A8D">Affitti tradizionali</text>
<text x="260" y="175" text-anchor="middle" font-size="8" fill="#6B7A8D">Riferimenti: Wired/Habyt (trend) · Righetto locazioni classiche</text>
</svg>
<figcaption>Coliving concentrato in capoluoghi; cintura padovana resta mercato affitti tradizionali — servizio Righetto locazioni.</figcaption>
</figure>"""


def svg_mutuo_flow() -> str:
    return """<figure class="blog-fig" style="padding:1rem;background:var(--sfondo)">
<svg viewBox="0 0 520 300" width="100%" height="300" role="img" aria-labelledby="mutuo-flow-title">
<title id="mutuo-flow-title">Percorso mutuo prima casa under 36 CONSAP</title>
<text x="260" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Percorso mutuo under 36 con garanzia CONSAP (fino 31/12/2027)</text>
<rect x="185" y="38" width="150" height="34" rx="17" fill="#2C4A6E"/><text x="260" y="60" text-anchor="middle" font-size="9" fill="#fff">1. ISEE + requisiti</text>
<path d="M260 72 L260 88" stroke="#FF6B35" stroke-width="2"/>
<rect x="185" y="88" width="150" height="34" rx="17" fill="#2C4A6E"/><text x="260" y="110" text-anchor="middle" font-size="9" fill="#fff">2. Preventivo banca</text>
<path d="M260 122 L260 138" stroke="#FF6B35" stroke-width="2"/>
<rect x="185" y="138" width="150" height="34" rx="17" fill="#FF6B35"/><text x="260" y="160" text-anchor="middle" font-size="9" fill="#152435">3. CONSAP 80%</text>
<path d="M260 172 L260 188" stroke="#FF6B35" stroke-width="2"/>
<rect x="185" y="188" width="150" height="34" rx="17" fill="#2C4A6E"/><text x="260" y="210" text-anchor="middle" font-size="9" fill="#fff">4. Ricerca + perizia</text>
<path d="M260 222 L260 238" stroke="#FF6B35" stroke-width="2"/>
<rect x="185" y="238" width="150" height="34" rx="17" fill="#2C4A6E"/><text x="260" y="260" text-anchor="middle" font-size="9" fill="#fff">5. Rogito notarile</text>
<text x="260" y="290" text-anchor="middle" font-size="8" fill="#6B7A8D">Legge 207/2024 — bonus fiscale under 36 scaduto 31/12/2024</text>
</svg>
<figcaption>Percorso mutuo prima casa under 36: CONSAP attivo fino al 31/12/2027; bonus fiscale dedicato non più valido dal 2025.</figcaption>
</figure>"""


def svg_agevolazioni_stato() -> str:
    return """<figure class="blog-fig" style="padding:1rem;background:var(--sfondo)">
<svg viewBox="0 0 520 220" width="100%" height="220" role="img" aria-labelledby="agev-stato-title">
<title id="agev-stato-title">Agevolazioni attive vs scadute under 36</title>
<text x="260" y="20" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Stato misure prima casa under 36 (agosto 2026)</text>
<rect x="40" y="45" width="200" height="55" rx="8" fill="#2C4A6E"/>
<text x="140" y="68" text-anchor="middle" font-size="10" fill="#fff" font-weight="600">ATTIVA</text>
<text x="140" y="88" text-anchor="middle" font-size="8" fill="rgba(255,255,255,.9)">Garanzia CONSAP 80%</text>
<text x="140" y="102" text-anchor="middle" font-size="8" fill="rgba(255,255,255,.75)">fino 31/12/2027</text>
<rect x="280" y="45" width="200" height="55" rx="8" fill="#6B7A8D" opacity="0.7"/>
<text x="380" y="68" text-anchor="middle" font-size="10" fill="#fff" font-weight="600">SCADUTA</text>
<text x="380" y="88" text-anchor="middle" font-size="8" fill="rgba(255,255,255,.9)">Bonus fiscale under 36</text>
<text x="380" y="102" text-anchor="middle" font-size="8" fill="rgba(255,255,255,.75)">31/12/2024</text>
<rect x="40" y="120" width="440" height="70" rx="8" fill="#fff" stroke="#E1DBD1"/>
<text x="260" y="145" text-anchor="middle" font-size="9" fill="#2C4A6E">Fonti: Legge 207/2024 · Money.it · NotaiOnline</text>
<text x="260" y="165" text-anchor="middle" font-size="8" fill="#6B7A8D">Verificare sempre testo normativo e circolari alla data di acquisto</text>
</svg>
<figcaption>Confronto visivo agevolazioni attive (CONSAP) e scadute (bonus fiscale). Aggiornare con commercialista e banca.</figcaption>
</figure>"""


def body_caro_affitti() -> str:
    return f"""
{aeo_box("In sintesi", "Il <strong>caro affitti a Padova</strong> per under 35 nel 2026 si legge con dati <strong>CNA Padova (+43% 2019-2025)</strong>, stanze <strong>335-490 €</strong> (Immobiliare.it Insights, <em>Il Gazzettino</em> mar 2026) e fasce <a href=\"{OMI_URL}\" target=\"_blank\" rel=\"noopener noreferrer\">OMI locazione ADE</a>. Strategie: budget canone/stipendio, cintura (Limena) e contratto registrato.")}

<p>Se hai meno di 35 anni e cerchi casa in affitto a Padova, il primo ostacolo non è solo trovare l'annuncio giusto: è far quadrare <strong>canone, stipendio e spese fisse</strong>. Questa guida non duplica l'emergenza abitativa generica né la panoramica studentesca — angoli distinti nel blog — ma offre un percorso operativo per giovani lavoratori e neolaureati nel capoluogo e in provincia.</p>

<div class="kpi-strip">
<div><strong>+43%</strong><span>Affitti CNA 2019-25</span></div>
<div><strong>335-490 €</strong><span>Stanze/mese</span></div>
<div><strong>~1.090 €</strong><span>Bilocale 70 mq (CNA)</span></div>
<div><strong>≤35%</strong><span>Regola canone/netto</span></div>
</div>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#dati">Dati CNA e portali 2026</a></li>
<li><a href="#rapporto">Affitto vs stipendio under 35</a></li>
<li><a href="#zone">Zone e alternative in cintura</a></li>
<li><a href="#contratto">Contratto, deposito, registrazione</a></li>
<li><a href="#strategie">Strategie pratiche per ridurre il carico</a></li>
</ol></nav>

{sol_box("Come affitto a Padova con meno di 35 anni senza spendere tutto lo stipendio?", [
    ("Ricerca mirata", "Filtri zona, budget e tipologia con comparabili OMI locazione", "affitti studenti Padova", "blog-affitto-studenti-padova"),
    ("Cintura nord", "Limena e comuni limitrofi per canoni più sostenibili", "zona Limena", "zona-limena"),
    ("Contratto in regola", "Registrazione ADE, deposito documentato, inventario", "servizio locazioni", "servizio-locazioni"),
    ("Consulenza budget", "Valutazione rapporto canone/reddito prima della visita", "canoni 2026", "blog-affitti-padova-canoni-2026"),
])}

<h2 id="dati">Cosa dicono CNA Padova e i portali nel 2026?</h2>
<p>La <strong>CNA Padova</strong> ha evidenziato un incremento degli affitti del <strong>+43% tra il 2019 e il 2025</strong> nel territorio provinciale. Per un bilocale da circa 70 mq il riferimento indicativo è intorno a <strong>1.090 euro al mese</strong> — ordine di grandezza da incrociare con le <a href=\"{OMI_URL}\" target=\"_blank\" rel=\"noopener noreferrer\">fasce OMI locazione</a> del semestre ADE in corso, non da copiare come prezzo della singola via.</p>
<p>Per le <strong>stanze</strong>, <strong>Immobiliare.it Insights</strong> e articoli de <a href=\"{GAZZETTINO_AFFITTI}\" target=\"_blank\" rel=\"noopener noreferrer\"><em>Il Gazzettino</em></a> (marzo 2026) collocano i canoni tra <strong>335 e 490 euro</strong> mensili a seconda di quartiere, arredo e distanza dall'università. Sono dati di mercato pubblicati da fonti terze: vanno letti come range, non come garanzia sul singolo annuncio.</p>
<p>Contesto macro: <a href=\"{ADE_OSSERVATORIO}\" target=\"_blank\" rel=\"noopener noreferrer\">Osservatorio ADE</a> e <a href=\"{ISTAT_URL}\" target=\"_blank\" rel=\"noopener noreferrer\">ISTAT prezzi abitazioni</a> per trend aggregati; microzona e stato dell'immobile determinano il canone effettivo in visita.</p>

{svg_affitti_trend()}

<h2 id="rapporto">Come confrontare affitto e stipendio se hai meno di 35 anni?</h2>
<p>La regola prudenziale usata da molti consulenti prevede un <strong>canone massimo del 30-35% del reddito netto mensile</strong>. Con 1.400 euro netti, 490 euro di affitto consumano il tetto; un bilocale a 1.090 euro richiede due redditi o spostamento verso zone più economiche.</p>

<table>
<thead><tr><th>Reddito netto mensile</th><th>Canone max 35%</th><th>Scenario Padova 2026</th></tr></thead>
<tbody>
<tr><td>1.200 €</td><td>420 €</td><td>Stanze in fascia bassa Insights (335 €+) o coinquilino</td></tr>
<tr><td>1.400 €</td><td>490 €</td><td>Massimo stanza singola in zona media; monolocale difficile</td></tr>
<tr><td>1.800 € (coppia)</td><td>630 € ciascuno</td><td>Bilocale possibile in cintura o semicentro selettivo</td></tr>
<tr><td>2.400 € (coppia)</td><td>840 € ciascuno</td><td>Bilocale 70 mq più realistico con margini</td></tr>
</tbody>
</table>

{svg_affitto_stipendio()}

<h2 id="zone">Quali zone e alternative per abbassare il canone?</h2>
<p>Il centro storico e le aree universitarie (Portello, Via VIII Febbraio, Arcella) mantengono domanda elevata. Gli under 35 spesso spostano la ricerca verso <strong>Sacro Cuore, Ponte di Brenta, Chirignago</strong> o la prima cintura — <strong>Limena, Rubano, Vigodarzere</strong> — dove il canone per metro quadro può essere più sostenibile a parità di metratura.</p>
<p>Approfondimenti correlati senza duplicare questo angolo: <a href=\"blog-affitto-studenti-padova\">affitto studenti Padova</a>, <a href=\"blog-affitti-padova-canoni-2026\">canoni affitti Padova 2026</a>, <a href=\"blog-rendimento-affitto-padova\">rendimento affitto Padova</a> (per chi valuta anche l'investimento locativo) e <a href=\"zona-limena\">pagina zona Limena</a>.</p>

{blog_fig("img/blog/blog-caro-affitti-padova-under-35-coppia.webp", "Giovane coppia under 35 valuta affitto a Padova — confronto budget e zone")}

<table>
<thead><tr><th>Zona / soluzione</th><th>Profilo under 35</th><th>Nota costo</th></tr></thead>
<tbody>
<tr><td>Centro / università</td><td>Studenti, neolaureati</td><td>Stanze 335-490 € (fonti portali 2026)</td></tr>
<tr><td>Semicentro ben servito</td><td>Lavoratori single</td><td>Monolocali sopra budget medio</td></tr>
<tr><td>Cintura nord (Limena)</td><td>Coppie pendolari</td><td>Metrature ampie, spostamento auto/mezzi</td></tr>
<tr><td>Coinquilino</td><td>Primo affitto</td><td>Costo stanza minore, regole condivise</td></tr>
</tbody>
</table>

<h2 id="contratto">Contratto, deposito e registrazione: cosa non saltare</h2>
<p>Il contratto <strong>4+4</strong> resta lo standard. Deposito massimo <strong>tre mensilità</strong> per locazioni ordinarie. Registrazione presso l'Agenzia delle Entrate entro i termini di legge: senza, problemi con residenza e detrazioni. Leggere regolamento condominiale, inventario e ripartizione spese prima di versare caparra.</p>
<p>Dettaglio contrattuale generale: <a href=\"blog-contratto-affitto-padova\">guida contratto affitto Padova</a>. Per supporto su locazioni tradizionali: <a href=\"servizio-locazioni\">servizio locazioni Righetto</a>.</p>

<h2 id="strategie">Strategie pratiche per il caro affitti padova giovani</h2>
<ul>
<li>Preparare documenti (busta paga, contratto, garanzie) prima delle visite — i locatori selezionano in fretta.</li>
<li>Confrontare almeno tre annunci comparabili con OMI locazione del semestre.</li>
<li>Sommare utenze, condominio e trasporti al canone — non guardare solo il numero in vetrina.</li>
<li>Valutare cintura se il lavoro lo consente: <a href=\"zona-limena\">Limena</a> è a pochi chilometri dal capoluogo.</li>
<li>Evitare bonifici senza contratto e annunci senza APE o planimetria.</li>
</ul>

{blog_fig("img/blog/blog-caro-affitti-padova-under-35-skyline.webp", "Skyline Padova — contesto mercato affitti under 35 2026")}

<h2 id="fonti">Fonti ufficiali e portali da consultare</h2>
<p>Oltre ai dati CNA e ai portali citati, ogni under 35 dovrebbe salvare tra i preferiti il <a href=\"{OMI_URL}\" target=\"_blank\" rel=\"noopener noreferrer\">portale OMI</a> (selezionando Padova, semestre vigente, locazione), l'<a href=\"{ADE_OSSERVATORIO}\" target=\"_blank\" rel=\"noopener noreferrer\">Osservatorio ADE</a> per trend macro e l'archivio <a href=\"{ISTAT_URL}\" target=\"_blank\" rel=\"noopener noreferrer\">ISTAT</a> per l'andamento temporale. Nessun articolo sostituisce la scheda dell'annuncio che state per firmare: visita, documenti e contratto restano il filtro finale.</p>

<p>{CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 22 agosto 2026. Fonti: CNA Padova, Immobiliare.it Insights, Il Gazzettino mar 2026, OMI ADE.</p>
"""


def body_coliving() -> str:
    return f"""
{aeo_box("In sintesi", "Il <strong>coliving Padova Limena</strong> è un <strong>trend informativo</strong> per giovani professionisti (riferimenti <a href=\"{WIRED_COLIVING}\" target=\"_blank\" rel=\"noopener noreferrer\">Wired/Habyt</a>, <a href=\"{DISTRETTO_COLIVING}\" target=\"_blank\" rel=\"noopener noreferrer\">Distretto Casa Investimenti</a>). <strong>Righetto non offre coliving</strong>: questa guida confronta modelli; per affitti tradizionali → <a href=\"servizio-locazioni\">servizio locazioni</a>.")}

<p><strong>Nota editoriale:</strong> Gruppo Immobiliare Righetto gestisce <strong>locazioni residenziali classiche</strong> (bilocali, trilocali, stanze in appartamento privato) — <em>non</em> strutture coliving gestite da operatori hospitality. Quanto segue è guida informativa per capire il fenomeno e confrontarlo con coinquilino e monolocale nel Padovano.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#cosa">Cos'è il coliving (e cosa non è)</a></li>
<li><a href="#confronto">Coliving vs coinquilino vs monolocale</a></li>
<li><a href="#padova">Coliving a Padova e Limena nel 2026</a></li>
<li><a href="#checklist">Checklist prima di firmare</a></li>
<li><a href="#righetto">Cosa fa Righetto (locazioni tradizionali)</a></li>
</ol></nav>

{sol_box("Cerco coliving a Padova — Righetto lo gestisce?", [
    ("Risposta chiara", "No coliving Righetto — guida informativa su trend nazionale", "servizio locazioni", "servizio-locazioni"),
    ("Affitto classico", "Bilocale, trilocale e stanze con contratto 4+4 registrato", "affitti Limena", "blog-affitti-limena-2026"),
    ("Consulenza zona", "Limena e cintura per professionisti pendolari", "zona Limena", "zona-limena"),
    ("Contatti", "Indicare tipologia e budget per locazione tradizionale", "contatti", "contatti"),
])}

<h2 id="cosa">Cos'è il coliving e perché ne parlano Wired e gli investitori?</h2>
<p>Il <strong>coliving</strong> combina camera privata, aree comuni curate e servizi (Wi-Fi, pulizie, talvolta coworking) in struttura gestita da un operatore. Articoli su <a href=\"{WIRED_COLIVING}\" target=\"_blank\" rel=\"noopener noreferrer\">Wired</a> descrivono startup come Habyt in grandi città; <a href=\"{DISTRETTO_COLIVING}\" target=\"_blank\" rel=\"noopener noreferrer\">Distretto Casa Investimenti</a> analizza il co-living come asset per investitori. Sono <strong>riferimenti informativi</strong> sul trend — non catalogo offerte Righetto.</p>
<p>È diverso dal <strong>coinquilino</strong> in appartamento privato (contratto tra privati, regole autogestite) e dal <strong>monolocale tradizionale</strong> (privacy totale, canone generalmente più alto della stanza).</p>

{svg_coliving_confronto()}

<h2 id="confronto">Tabella comparativa: coliving, coinquilino, monolocale</h2>
<table>
<thead><tr><th>Soluzione</th><th>Costo indicativo</th><th>Privacy</th><th>Gestione</th><th>Righetto</th></tr></thead>
<tbody>
<tr><td>Coliving operatore</td><td>Medio-alto (servizi inclusi)</td><td>Camera sì, spazi comuni no</td><td>Operatore hospitality</td><td>Non gestito</td></tr>
<tr><td>Coinquilino</td><td>Basso per stanza</td><td>Media</td><td>Tra inquilini privati</td><td>Locazioni classiche</td></tr>
<tr><td>Monolocale 4+4</td><td>Alto</td><td>Alta</td><td>Contratto locazione standard</td><td>Sì — servizio locazioni</td></tr>
<tr><td>Bilocale cintura</td><td>Medio</td><td>Alta (coppia)</td><td>Contratto locazione standard</td><td>Sì — Limena/Padova</td></tr>
</tbody>
</table>

<h2 id="padova">Coliving Padova e Limena: offerta reale vs aspettative</h2>
<p>A Padova l'offerta coliving resta <strong>nicchia</strong> rispetto alle locazioni tradizionali che dominano portali e agenzie. Limena e la cintura attraggono professionisti che lavorano in area padovana con <strong>affitti classici</strong> più che strutture hospitality — percorrenza verso ospedale, università o zone industriali va calcolata caso per caso.</p>

{svg_coliving_padova()}

{blog_fig("img/blog/blog-coliving-padova-limena-cowork.webp", "Area coworking in contesto coliving — illustrazione informativa trend professionisti")}

<p>Non promettiamo disponibilità coliving in portafoglio Righetto. Se cercate <strong>affitto tradizionale</strong>, consultate <a href=\"servizio-locazioni\">servizio locazioni</a>, <a href=\"blog-affitti-limena-2026\">affitti Limena 2026</a> e <a href=\"zona-limena\">zona Limena</a>. Angolo corporate diverso: <a href=\"blog-loft-aziende-cucina-condivisa-padova-vicenza-2026\">loft e cucine condivise aziendali</a>.</p>

{blog_fig("img/blog/blog-coliving-padova-limena-limena.webp", "Limena nella cintura padovana — alternativa affitti tradizionali per professionisti")}

<h2 id="checklist">Checklist prima di scegliere coliving o affitto classico</h2>
<ol>
<li>Leggere contratto: natura locazione/ospitalità, durata minima, recesso.</li>
<li>Verificare cosa è incluso nel canone (utenze, pulizie, parcheggio).</li>
<li>Visitare struttura reale — non affidarsi solo a render o articoli nazionali.</li>
<li>Confrontare costo totale mensile con stanza in coinquilino o bilocale in cintura.</li>
<li>Consultare commercialista su implicazioni fiscali del contratto specifico.</li>
</ol>

<table>
<thead><tr><th>Domanda</th><th>Coliving</th><th>Affitto Righetto (tradizionale)</th></tr></thead>
<tbody>
<tr><td>Chi gestisce l'immobile?</td><td>Operatore hospitality</td><td>Proprietario + mediazione agenzia</td></tr>
<tr><td>Contratto tipico</td><td>Variabile per operatore</td><td>4+4 o concordato registrato ADE</td></tr>
<tr><td>Target</td><td>Giovani professionisti flessibili</td><td>Famiglie, coppie, lavoratori, studenti</td></tr>
<tr><td>Supporto Righetto</td><td>No — solo guida informativa</td><td>Sì — visite, contratto, qualifica inquilino</td></tr>
</tbody>
</table>

<h2 id="righetto">Cosa può fare Righetto (locazioni tradizionali, non coliving)</h2>
<p>Righetto opera dal 2000 su Padova e 101 comuni con oltre 350 immobili gestiti. Per giovani professionisti che preferiscono <strong>bilocale, trilocale o stanza in appartamento privato</strong>, il percorso passa da <a href=\"servizio-locazioni\">servizio locazioni</a> e catalogo immobili — compenso di mediazione concordato <strong>in sede</strong>, nessun listino online.</p>

<h2 id="trend">Trend nazionale vs realtà padovana</h2>
<p>Il coliving è spesso raccontato come risposta alla crisi abitativa nelle metro italiane ed europee. Padova, con forte componente universitaria e ospedaliera, ha già un mercato maturo di <strong>stanze e coinquilinato</strong> che assorbe gran parte della domanda giovane. Il coliving professionale si inserisce come alternativa di nicchia per chi cerca servizi hotel-style con contratto flessibile — non come sostituto automatico dell'affitto tradizionale in provincia.</p>
<p>Prima di orientarsi verso operatori citati in articoli nazionali, confrontate almeno due soluzioni locali: stanza in appartamento privato tramite agenzia, monolocale in semicentro e — se esiste offerta verificabile — struttura coliving con visita e contratto letto integralmente. La scelta migliore dipende da reddito, orari di lavoro e tolleranza alla condivisione degli spazi comuni.</p>
<p>Se dopo il confronto preferite un <strong>affitto tradizionale registrato</strong>, il team Righetto a Limena risponde con disponibilità in catalogo, visite accompagnate e supporto contrattuale — senza promettere servizi coliving che non fanno parte del portafoglio agenzia.</p>

<p>{CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 22 agosto 2026. Riferimenti informativi: Wired/Habyt, Distretto Casa Investimenti. Nessun servizio coliving Righetto.</p>
"""


def body_prima_casa() -> str:
    return f"""
{aeo_box("In sintesi", "<strong>Prima casa under 36 Padova 2026:</strong> <strong>garanzia CONSAP fino al 31/12/2027</strong> (Legge 207/2024, fino all'80% mutuo). <strong>Bonus fiscale under 36 scaduto il 31/12/2024</strong> (Money.it, NotaiOnline). Incrociare <a href=\"{OMI_URL}\" target=\"_blank\" rel=\"noopener noreferrer\">OMI ADE</a> e preventivo banca prima dell'offerta.")}

<p>Acquistare la prima casa a Padova avendo meno di 36 anni nel 2026 significa distinguere con precisione cosa è ancora valido e cosa è scaduto. Questo articolo non duplica la guida generale <a href=\"blog-agevolazioni-prima-casa-2026\">agevolazioni prima casa 2026</a>: qui focus su <strong>CONSAP attivo</strong>, bonus fiscale chiuso e percorso operativo nel capoluogo e in cintura (Limena).</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#attive">Agevolazioni attive vs scadute</a></li>
<li><a href="#consap">Garanzia CONSAP Legge 207/2024</a></li>
<li><a href="#mutuo">Percorso mutuo e documenti</a></li>
<li><a href="#padova">Prima casa a Padova e Limena</a></li>
<li><a href="#errori">Errori da evitare under 36</a></li>
</ol></nav>

{sol_box("Voglio comprare prima casa under 36 a Padova — da dove inizio?", [
    ("Qualifica CONSAP", "Verifica requisiti ISEE, età e prima casa con banca", "servizio mutuo", "servizio-mutuo"),
    ("Ricerca immobili", "Bilocali e trilocali Padova/Limena con documenti in ordine", "catalogo", "immobili"),
    ("Valutazione OMI", "Confronto prezzo richiesto vs fascia ADE semestre corrente", "zona Limena", "zona-limena"),
    ("Consulenza gratuita", "Coordinamento visita, proposta e rogito", "consulenza", "landing-consulenza-immobiliare-gratuita"),
])}

<h2 id="attive">Quali agevolazioni under 36 sono attive e quali scadute?</h2>
<p>Errore frequente nel 2026: citare il <strong>bonus fiscale prima casa under 36</strong> come se fosse ancora disponibile. Secondo sintesi su <a href=\"{MONEY_UNDER36}\" target=\"_blank\" rel=\"noopener noreferrer\">Money.it</a> e <a href=\"{NOTAI_ONLINE}\" target=\"_blank\" rel=\"noopener noreferrer\">NotaiOnline</a>, la misura è <strong>scaduta il 31 dicembre 2024</strong>. Pianificare l'acquisto contando su quella agevolazione è un rischio documentale.</p>
<p>Rimane attiva la <strong>garanzia statale CONSAP</strong> per giovani under 36, prorogata dalla <strong>Legge 207/2024 fino al 31 dicembre 2027</strong>, con copertura fino all'<strong>80%</strong> dell'importo del mutuo per chi rispetta requisiti di età, ISEE e prima casa.</p>

{svg_agevolazioni_stato()}

<table>
<thead><tr><th>Misura</th><th>Stato agosto 2026</th><th>Scadenza / nota</th><th>Fonte</th></tr></thead>
<tbody>
<tr><td>Garanzia CONSAP mutuo under 36</td><td><strong>Attiva</strong></td><td>Fino 31/12/2027</td><td>Legge 207/2024</td></tr>
<tr><td>Bonus fiscale prima casa under 36</td><td><strong>Scaduta</strong></td><td>31/12/2024</td><td>Money.it, NotaiOnline</td></tr>
<tr><td>Imposte prima casa (registro)</td><td>Attive con requisiti</td><td>Normativa ordinaria</td><td>Notaio / commercialista</td></tr>
<tr><td>Detrazioni ristrutturazione</td><td>Da verificare</td><td>Normativa vigente</td><td>Agenzia Entrate</td></tr>
</tbody>
</table>

<h2 id="consap">Come funziona la garanzia CONSAP per under 36?</h2>
<p>CONSAP interviene a garanzia del mutuo fino all'80% per giovani che non possiedono altre abitazioni ad uso abitativo in Italia e rispettano soglie ISEE. La <strong>banca</strong> valuta comunque merito creditizio, stabilità reddituale e <strong>perizia</strong> sull'immobile — la garanzia non sostituisce l'analisi del rischio.</p>
<p>Preparare <strong>ISEE aggiornato</strong>, documenti reddito e certificazione stato di famiglia prima del preventivo mutuo accelera la qualifica. Dettaglio requisiti: <a href=\"{MONEY_UNDER36}\" target=\"_blank\" rel=\"noopener noreferrer\">Money.it mutuo giovani under 36</a> e <a href=\"{NOTAI_ONLINE}\" target=\"_blank\" rel=\"noopener noreferrer\">NotaiOnline guida agevolazioni</a>.</p>

{svg_mutuo_flow()}

<h2 id="mutuo">Percorso mutuo: dalla banca al rogito</h2>
<ol>
<li><strong>Preventivo e pre-approvazione</strong> con banca o broker — indicare interesse garanzia CONSAP.</li>
<li><strong>Ricerca immobile</strong> con confronto prezzo vs <a href=\"{OMI_URL}\" target=\"_blank\" rel=\"noopener noreferrer\">fascia OMI</a> del semestre ADE.</li>
<li><strong>Proposta d'acquisto</strong> condizionata a mutuo e perizia favorevole.</li>
<li><strong>Compromesso</strong> con caparra e due diligence documentale (APE, visure, planimetria).</li>
<li><strong>Rogito notarile</strong> con erogazione mutuo.</li>
</ol>
<p>Contesto macro prezzi: <a href=\"{ADE_OSSERVATORIO}\" target=\"_blank\" rel=\"noopener noreferrer\">Osservatorio ADE</a> e <a href=\"{ISTAT_URL}\" target=\"_blank\" rel=\"noopener noreferrer\">ISTAT</a>. Per immobili in cintura: <a href=\"blog-appartamento-limena-guida-acquisto-2026\">guida acquisto Limena</a>.</p>

{blog_fig("img/blog/blog-prima-casa-under-36-consap-coppia.webp", "Coppia under 36 valuta prima casa a Padova con garanzia CONSAP")}

<h2 id="padova">Prima casa under 36 a Padova e in cintura</h2>
<p>Il mercato padovano nel 2026 premia immobili ristrutturati con APE valido e documenti in ordine. Gli under 36 competono con famiglie e investitori su bilocali in semicentro: avere <strong>garanzia CONSAP qualificata</strong> e anticipo definito prima della visita aumenta credibilità in trattativa.</p>
<p><strong>Limena</strong> e comuni limitrofi offrono trilocali più ampi a parità budget rata: utile per coppie che accettano pendolarismo. Pagina territorio: <a href=\"zona-limena\">zona Limena</a>.</p>

<table>
<thead><tr><th>Scenario</th><th>Padova semicentro</th><th>Limena / cintura</th></tr></thead>
<tbody>
<tr><td>Tipologia tipica under 36</td><td>Bilocale ristrutturato</td><td>Trilocale o bilocale con giardino</td></tr>
<tr><td>Perizia banca</td><td>Confronto OMI zone centrali</td><td>Confronto OMI B1/R1 Limena</td></tr>
<tr><td>Spostamento lavoro</td><td>Tram, bici, piedi</td><td>Auto / bus extraurbano</td></tr>
<tr><td>Supporto Righetto</td><td>Ricerca + trattativa</td><td>Sede Via Roma 96 — territorio locale</td></tr>
</tbody>
</table>

{blog_fig("img/blog/blog-prima-casa-under-36-consap-mutuo.webp", "Percorso mutuo prima casa under 36 — illustrazione informativa documenti e banca")}

<h2 id="errori">Errori da evitare nel 2026</h2>
<ul>
<li>Contare sul bonus fiscale under 36 scaduto a dicembre 2024.</li>
<li>Firmare proposta senza lettera banca o pre-approvazione mutuo.</li>
<li>Ignorare perizia inferiore al prezzo — serve più anticipo.</li>
<li>Acquistare senza verificare conformità planimetria e APE.</li>
<li>Confondere consulenza agenzia con parere fiscale — commercialista e notaio restano i riferimenti.</li>
</ul>

<h2 id="checklist">Checklist documenti under 36 prima dell'offerta</h2>
<ol>
<li>ISEE aggiornato e certificazione stato di famiglia.</li>
<li>Ultime buste paga o dichiarazione redditi per lavoratori autonomi.</li>
<li>Lettera di pre-approvazione mutuo con indicazione garanzia CONSAP.</li>
<li>Documento identità e codice fiscale di tutti i coobbligati.</li>
<li>Bozza proposta con prezzo, termini e condizione sospensiva mutuo.</li>
</ol>
<p>Per il lato immobile, Righetto verifica in anticipo APE, visure e planimetria catastale per ridurre sorprese in perizia e rogito — coordinamento operativo, non sostituzione parere legale o fiscale.</p>
<p>Per approfondire il contesto comunale, consultate anche <a href=\"blog-appartamento-limena-guida-acquisto-2026\">guida acquisto Limena</a> e la pagina <a href=\"servizio-mutuo\">servizio mutuo</a> Righetto: percorsi complementari senza duplicare l'angolo CONSAP trattato qui.</p>

<p>{CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 22 agosto 2026. Fonti: Legge 207/2024, Money.it, NotaiOnline, OMI ADE.</p>
"""


ARTICLES = [
    {
        "slug": "blog-caro-affitti-padova-under-35-guida-2026",
        "filename": "blog-caro-affitti-padova-under-35-guida-2026.html",
        "hero": "img/blog/blog-caro-affitti-padova-under-35-hero.webp",
        "title": "Caro affitti Padova 2026: guida under 35",
        "og_title": "Caro affitti Padova 2026: sopravvivere under 35",
        "meta": "Caro affitti Padova per under 35: CNA +43%, stanze 335-490 €, rapporto canone/stipendio, zone e cintura Limena. Guida 2026 Righetto.",
        "schema_headline": "Caro affitti Padova 2026: guida pratica per under 35",
        "section": "Affitti Padova",
        "cat_badge": "Affitti · Under 35",
        "bread_crumb": "Caro affitti under 35",
        "h1": "<strong>Caro affitti Padova</strong> 2026: guida under 35",
        "hero_alt": "Caro affitti Padova under 35 — skyline e budget giovani 2026",
        "body_fn": lambda: expand_body(body_caro_affitti, [], EXPANSION_AFFITTI_UNDER35),
        "faqs": [
            ("Quanto sono aumentati gli affitti a Padova?", "La CNA Padova segnala +43% tra 2019 e 2025. Per il singolo annuncio consultare OMI locazione ADE del semestre corrente."),
            ("Quanto costa una stanza a Padova nel 2026?", "Immobiliare.it Insights e Il Gazzettino (mar 2026) indicano 335-490 € al mese a seconda di zona e arredo."),
            ("Quale percentuale dello stipendio per l'affitto?", "Regola prudenziale: canone ≤ 30-35% del reddito netto mensile, utenze e trasporti a parte."),
            ("Dove conviene affittare under 35 nel Padovano?", "Semicentro e università costano di più; cintura nord (Limena, Rubano) offre metrature maggiori con spostamento."),
            ("Cosa fa Righetto per giovani in affitto?", "Locazioni tradizionali con visite, contratto registrato e qualifica inquilino — compenso concordato in sede."),
            ("Bilocale 70 mq: quanto canone indicativo CNA?", "Circa 1.090 €/mese come ordine di grandezza CNA — verificare su OMI e annunci comparabili."),
            ("Come evitare truffe in affitto?", "Mai bonifici senza contratto; richiedere APE, planimetria e registrazione ADE; diffidare di prezzi sotto mercato senza spiegazione."),
        ],
        "related": [
            ("Affitto studenti Padova", "blog-affitto-studenti-padova"),
            ("Canoni affitti 2026", "blog-affitti-padova-canoni-2026"),
            ("Rendimento affitto", "blog-rendimento-affitto-padova"),
            ("Servizio locazioni", "servizio-locazioni"),
            ("Zona Limena", "zona-limena"),
        ],
        "registry": {
            "titolo": "Caro affitti Padova under 35: Guida 2026",
            "categoria": "Affitti Padova",
            "tempo": 14,
            "contenuto": "Caro affitti Padova under 35: CNA +43%, stanze 335-490 €, budget e zone.",
            "evidenza": False,
            "emoji": "🏠",
            "admin_contenuto": "<p>Guida caro affitti Padova under 35: dati CNA, rapporto stipendio, strategie cintura.</p>",
        },
        "static_map_key": "caro affitti padova under 35 guida 2026",
        "editorial_id": "eq-003",
    },
    {
        "slug": "blog-coliving-padova-limena-giovani-professionisti-2026",
        "filename": "blog-coliving-padova-limena-giovani-professionisti-2026.html",
        "hero": "img/blog/blog-coliving-padova-limena-hero.webp",
        "title": "Coliving Padova Limena 2026: guida giovani",
        "og_title": "Coliving Padova Limena: guida professionisti 2026",
        "meta": "Coliving Padova e Limena per giovani professionisti: confronto con coinquilino e monolocale. Guida informativa — Righetto locazioni tradizionali.",
        "schema_headline": "Coliving nel Padovano: guida per giovani professionisti 2026",
        "section": "Trend abitativo",
        "cat_badge": "Coliving · Guida",
        "bread_crumb": "Coliving Padova Limena",
        "h1": "<strong>Coliving Padova Limena</strong> 2026: guida professionisti",
        "hero_alt": "Coliving Padova Limena — spazi condivisi giovani professionisti 2026",
        "body_fn": lambda: expand_body(body_coliving, [], EXPANSION_COLIVING),
        "faqs": [
            ("Righetto offre coliving a Padova?", "No. Righetto gestisce locazioni tradizionali (bilocale, trilocale, stanze). Questa è guida informativa sul trend."),
            ("Cos'è il coliving?", "Camera privata e aree comuni gestite da operatore, spesso con servizi inclusi (Wi-Fi, pulizie). Diverso dal coinquilino privato."),
            ("Coliving o coinquilino: cosa costa meno?", "Il coinquilino in appartamento privato costa generalmente meno; il coliving include servizi nel canone."),
            ("Esiste coliving a Limena?", "L'offerta coliving è nicchia nel capoluogo; Limena resta mercato affitti classici — servizio locazioni Righetto."),
            ("Quali fonti consultare sul coliving?", "Wired/Habyt e Distretto Casa Investimenti per trend — non promessa servizi Righetto."),
            ("Come affittare in modo tradizionale a Padova?", "Servizio locazioni Righetto: contratto 4+4 registrato, visite e qualifica inquilino."),
        ],
        "related": [
            ("Servizio locazioni", "servizio-locazioni"),
            ("Affitti Limena 2026", "blog-affitti-limena-2026"),
            ("Zona Limena", "zona-limena"),
            ("Affitti studenti", "blog-affitto-studenti-padova"),
        ],
        "registry": {
            "titolo": "Coliving Padova Limena: Guida 2026",
            "categoria": "Trend abitativo",
            "tempo": 12,
            "contenuto": "Coliving Padova Limena: guida informativa vs locazioni tradizionali Righetto.",
            "evidenza": False,
            "emoji": "🏢",
            "admin_contenuto": "<p>Coliving Padova Limena: confronto modelli abitativi — no servizio coliving Righetto.</p>",
        },
        "static_map_key": "coliving padova limena giovani professionisti 2026",
        "editorial_id": "eq-004",
    },
    {
        "slug": "blog-prima-casa-under-36-consap-padova-2026",
        "filename": "blog-prima-casa-under-36-consap-padova-2026.html",
        "hero": "img/blog/blog-prima-casa-under-36-consap-hero.webp",
        "title": "Prima casa under 36 Padova 2026: CONSAP",
        "og_title": "Prima casa under 36 Padova: CONSAP e agevolazioni 2026",
        "meta": "Prima casa under 36 Padova 2026: garanzia CONSAP fino 31/12/2027, bonus fiscale scaduto 31/12/2024. Percorso mutuo e OMI ADE. Guida Righetto.",
        "schema_headline": "Prima casa under 36 a Padova: CONSAP attivo e misure scadute",
        "section": "Mutuo e acquisto",
        "cat_badge": "Prima casa · Under 36",
        "bread_crumb": "Prima casa under 36",
        "h1": "<strong>Prima casa under 36</strong> Padova 2026: CONSAP",
        "hero_alt": "Prima casa under 36 Padova — garanzia CONSAP e mutuo 2026",
        "body_fn": lambda: expand_body(body_prima_casa, [], EXPANSION_PRIMA_CASA),
        "faqs": [
            ("CONSAP under 36 è ancora attivo nel 2026?", "Sì, prorogato dalla Legge 207/2024 fino al 31 dicembre 2027, fino all'80% del mutuo con requisiti."),
            ("Il bonus fiscale under 36 vale ancora?", "No — scaduto il 31 dicembre 2024 secondo Money.it e NotaiOnline."),
            ("Cosa serve per la garanzia CONSAP?", "Requisiti under 36, prima casa, ISEE entro soglie — la banca valuta comunque merito creditizio."),
            ("Come si usa OMI per la prima casa a Padova?", "Confrontare prezzo richiesto con fascia min-med-max locazione/vendita ADE del semestre per microzona."),
            ("Convince comprare a Limena under 36?", "Spesso metrature maggiori a parità rata; calcolare spostamenti e costo totale mensile."),
            ("Righetto aiuta con mutuo e rogito?", "Coordina ricerca, documenti immobile e trattativa — consulenza fiscale con commercialista e notaio."),
        ],
        "related": [
            ("Servizio mutuo", "servizio-mutuo"),
            ("Agevolazioni prima casa", "blog-agevolazioni-prima-casa-2026"),
            ("Acquisto Limena", "blog-appartamento-limena-guida-acquisto-2026"),
            ("Consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
        ],
        "registry": {
            "titolo": "Prima casa under 36 Padova: CONSAP 2026",
            "categoria": "Mutuo e acquisto",
            "tempo": 13,
            "contenuto": "Prima casa under 36 Padova: CONSAP fino 2027, bonus scaduto, percorso mutuo.",
            "evidenza": False,
            "emoji": "🔑",
            "admin_contenuto": "<p>Prima casa under 36 Padova: CONSAP attivo, bonus fiscale scaduto, guida mutuo 2026.</p>",
        },
        "static_map_key": "prima casa under 36 consap padova 2026",
        "editorial_id": "eq-005",
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
    ids = {cfg["editorial_id"] for cfg in ARTICLES}
    updated = 0
    for item in data.get("items", []):
        if item.get("id") in ids:
            item["status"] = "published"
            item["published_date"] = DATE_ISO
            updated += 1
    data["updated"] = DATE_ISO
    EDITORIAL_QUEUE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"editorial-queue.json: {updated} item → published ({DATE_ISO})")


def main() -> None:
    results: list[dict] = []
    slugs: list[str] = []

    for cfg in ARTICLES:
        body = cfg["body_fn"]()
        words = wc(body)
        if words < MIN_BODY_WORDS - 10:
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
    patch_editorial_queue()

    print("\n-- Riepilogo batch ago22 2026 --")
    for r in results:
        print(f"  • {r['file']} ({r['words']} parole)")
    print("  • blog.html, admin.html, sitemap.xml, homepage.js, editorial-queue.json")


if __name__ == "__main__":
    main()
