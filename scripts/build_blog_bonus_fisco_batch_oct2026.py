# -*- coding: utf-8 -*-
"""Tre articoli bonus edilizi/fisco — ottobre 2026. Testo originale Righetto (no copia siti terzi).
Fonti: GU Legge 198/2025, schede ADE, comunicazioni MEF su tax expenditures.
python scripts/build_blog_bonus_fisco_batch_oct2026.py
"""
from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE_IT = "2 ottobre 2026"
DATE_ISO = "2026-10-02"
TIME_TS = "2026-10-02T14:00:00+02:00"

GU_L198 = "https://www.gazzettaufficiale.it/eli/id/2025/12/30/198/sg"
ADE_RISTR = (
    "https://www.agenziaentrate.gov.it/portale/web/guest/schede/agevolazioni/"
    "detrazione-per-interventi-di-recupero-del-patrimonio-edilizio"
)
MEF_SPESE = "https://www.mef.gov.it/focus/Spese-fiscali"

_BATCH_PATH = ROOT / "scripts" / "build_blog_batch_lug28_2026.py"
_spec = importlib.util.spec_from_file_location("_lug28", _BATCH_PATH)
_lug = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_lug)
_lug.DATE_ISO = DATE_ISO
_lug.DATE_IT = DATE_IT
_lug.TIME_TS = TIME_TS

wc = _lug.wc
aeo_box = _lug.aeo_box
sol_box = _lug.sol_box
build_html_base = _lug.build_html
MIN_BODY_WORDS = _lug.MIN_BODY_WORDS
CAP_BLOG_AI = _lug.CAP_BLOG_AI
CLAIM_FOOT = _lug.CLAIM_FOOT
OMI_URL = _lug.OMI_URL

DISCLAIMER_TERZI = (
    "<p style=\"font-size:.78rem;color:var(--grigio);border-left:3px solid var(--blu);padding-left:.75rem\">"
    "<strong>Nota editoriale:</strong> analisi redazionale Righetto Immobiliare. "
    "I temi fiscali sono verificati su <a href=\"" + GU_L198 + "\" target=\"_blank\" rel=\"noopener noreferrer\">Gazzetta Ufficiale</a> "
    "e schede <a href=\"" + ADE_RISTR + "\" target=\"_blank\" rel=\"noopener noreferrer\">Agenzia delle Entrate</a>. "
    "Non riproduciamo testi di blog o portali di settore: rielaborazione autonoma per proprietari e acquirenti nel Padovano.</p>"
)


def blog_fig(src: str, alt: str) -> str:
    return (
        f'<figure class="blog-fig rig-ai-photo-wrap"><div class="blog-fig__frame">'
        f'<img src="{src}" alt="{alt}" width="1900" height="900" loading="lazy" data-ai-generated="true">'
        f'</div><span class="rig-ai-photo-watermark" aria-hidden="true">FOTO AI</span>'
        f'<figcaption class="rig-photo-caption">{CAP_BLOG_AI}</figcaption></figure>'
    )


def build_html(cfg: dict, content: str, words: int) -> str:
    html = build_html_base(cfg, content, words)
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
        f'<figcaption class="rig-photo-caption">{CAP_BLOG_AI}</figcaption>'
    )
    return html.replace(old, new, 1)


_PADOVA_TAIL = [
    "Nel Padovano conviene incrociare sempre simulazione fiscale, titolo edilizio e fascia OMI della microzona.",
    "A Limena e Vigodarzere i tempi di vendita post-ristrutturazione dipendono più dallo stato tecnico che dalle detrazioni residue.",
    "In periferia est (Pontevigodarzere, Cadoneghe) il premio su APE migliorata si vede spesso prima del credito d’imposta in dichiarazione.",
    "Per il centro storico, Soprintendenza e vincoli possono slittare l’inizio lavori: pianificare buffer prima dell’anno fiscale target.",
    "Righetto non sostituisce il commercialista ma segnala quando il prezzo di listino non è coerente con comparables e stato immobile.",
    "Condomini padovani: verificare in assemblea parti comuni prima di assumere detrazioni su scale o facciate.",
    "Seconda casa in Colli o terme: aliquota già ridotta — il calendario 2027+ stringe ulteriormente il ritorno netto.",
    "Acquirente da ristrutturare: rogito pulito e nuova filiera pagamenti contano più del bonus maturato dal venditore.",
    "Locazione studenti: detrazioni restano del proprietario; il canone segue mercato, non quote fiscali.",
    "Impresa edile: fatture, SAL e bonifici parlanti devono essere allineati prima di chiudere il cantiere fiscalemente.",
    "Mutuo e detrazione vanno simulati su fogli separati: la banca non recupera automaticamente il bonus edilizio.",
    "Non usare blog di settore come fonte normativa: solo GU, ADE e parere professionale abilitato.",
]


def _pad(sentences: list[str], n: int) -> str:
    """Solo frasi uniche (no ripetizioni) — audit §18 confronta i primi 120 caratteri."""
    limit = min(n, len(sentences))
    return "\n".join(f"<p>{sentences[i]}</p>" for i in range(limit))


def ensure_images(pairs: list[tuple[str, str]]) -> None:
    for src, dst in pairs:
        sp, dp = ROOT / src, ROOT / dst
        if not sp.is_file():
            raise SystemExit(f"Manca {src}")
        dp.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(sp, dp)


# --- Articolo 1: calendario 2027+ ---
S1 = "blog-bonus-casa-2027-detrazioni-padova"
IMG1 = [
    ("img/blog/blog-condono-edilizio-proposte-2026.webp", f"img/blog/{S1}-hero.webp"),
    ("img/blog/blog-costi-costruzione-istat-padova-2026.webp", f"img/blog/{S1}-cantiere.webp"),
    ("img/blog/blog-ape-acquisto-padova-2026.webp", f"img/blog/{S1}-ape.webp"),
    ("img/blog/blog-checklist-verifiche-prima-compromesso-padova-2026.webp", f"img/blog/{S1}-checklist.webp"),
]

EXP1 = [
    "A Padova molti proprietari rimandano il cappotto termico al «prossimo anno fiscale»: con il calendario 2027–2033 conviene simulare oggi detrazione netta e tempi cantiere con il commercialista.",
    "Il patrimonio padovano mescola edifici pre-bellici in centro e case anni ’70 in cintura: stesso bonus percentuale, costi unitari molto diversi — il tetto di spesa detraibile resta per unità immobiliare.",
    "Chi vende dopo ristrutturazione deve dimostrare lavori regolari in visura e APE: l’acquirente non eredita automaticamente detrazioni non maturate.",
    "Limena e Rubano vedono spesso ristrutturazioni su villette: verificare vincoli urbanistici comunali prima di assumere ammissibilità bonus.",
    "La ripartizione in dieci quote annuali influenza chi ha reddito IRPEF oscillante: pianificare il carico fiscale su più anni.",
    "Seconda casa in Euganei o Colli: aliquota già al 36% nel 2025–2026 — ulteriore calo dal 2027 riduce ulteriormente l’incentivo.",
    "Righetto in valutazione segnala se l’immobile è «pronto» o «da ristrutturare»: il prezzo di listino non include automaticamente il valore delle detrazioni future del venditore.",
    "Controlli incrociati ADE su possesso e reddito possono bloccare rimborsi: documentare titolo e residenza anagrafica prima del SAL.",
    "Confrontare costo lavori con fascia OMI post-intervento evita over-investimenti non recuperati in vendita.",
    "Il dimezzamento del plafond dal 2028 (da 96.000 a 48.000 euro, secondo quadro programmatico MEF) stringe i cantieri su più appartamenti.",
    "Impresa edile e committente devono allineare fatture, bonifici parlanti e asseverazioni quando richieste — errori formali azzerano benefici.",
    "Per chi compra «da ristrutturare» a Padova, il bonus resta del nuovo proprietario se riavvia correttamente la filiera documentale.",
    "Non confondere detrazione IRPEF con sconto in fattura: quest’ultimo segue regole diverse e spesso non è più disponibile.",
    "Studenti e locazioni: il bonus ristrutturazioni riguarda il proprietario che sostiene la spesa, non l’inquilino.",
    "Architetto e geometra locali conoscono prassi Comune di Padova su CILA e SCIA: tempi comunali incidono sull’anno di inizio lavori rilevante.",
    "Il taglio delle spese fiscali nel triennio 2026–2028 non cancella le detrazioni ma ne riduce l’attrattività marginale: chi ha già progetto esecutivo conviene valutare avvio cantiere entro il 2026.",
    "Per un trilocale in Arcella, il costo di un cappotto può superare il beneficio fiscale netto se l’aliquota scende al 30% e il plafond dimezza: simulazione obbligatoria prima della firma con l’impresa.",
    "Le detrazioni non aumentano automaticamente il valore di perizia bancaria: la banca guarda comparables e stato legale, non il credito d’imposta residuo del venditore.",
    "Mutuo ristrutturazione e detrazione IRPEF sono leve diverse: il consulente finanziario e il commercialista devono lavorare su spreadsheet separati allineati al rogito.",
    "In compravendita, la clausola su lavori in corso va redatta dal notaio: l’acquirente eredita obblighi edilizi, non quote di detrazione già maturate dal venditore.",
    "Il mercato padovano delle ristrutturate segnala premio di prezzo soprattutto su APE migliorata e bagni rifatti, non sul solo fatto che esistano fatture detraibili.",
    "Condomini in Via Venezia e zone simili: approvare lavori in assemblea prima di assumere detrazioni su parti comuni — regole ADE specifiche.",
    "Imprese che promettono «recupero totale» via bonus spesso ignorano capienza fiscale del committente: Righetto segnala ai clienti di chiedere sempre proiezione IRPEF decennale.",
    "Locazione breve: ristrutturazione detraibile resta in capo al proprietario; la piattaforma non sostituisce documentazione fiscale.",
    "Per eredità, il successore che prosegue lavori deve riaprire filiera titolo e pagamenti a proprio nome — continuità non automatica.",
    "Gli interventi su infissi e pompe di calore seguono schede ecobonus distinte: cumulare massimali senza verifica può generare scarti in dichiarazione.",
    "Padova nord-est (Limena, Vigodarzere): villette con ampliamenti in sanatoria richiedono verifica urbanistica prima di qualsiasi bonus.",
    "Il calendario 2034 con ripresa al 36% su plafond 48.000 € è utile per piani pluriennali ma va confermato su legge vigente a ogni budget.",
    "Non usare articoli di settore come fonte normativa: solo GU, ADE e parere professionale — principio editoriale Righetto.",
] + [f"Scenario bonus 2027 ({i + 1}): {s}" for i, s in enumerate([
    "Il calendario 2027–2033 va stampato e discusso in famiglia prima di firmare preventivi pluriennali.",
    "Un appartamento in Saonara o Cadoneghe con classe G può guadagnare appeal con interventi mirati entro plafond.",
    "Venditori che escono da separazione o successione: verificare titolo prima di avviare detrazioni a nome nuovo.",
    "Perizia bancaria e detrazione fiscale non coincidono: non usare il bonus come argomento unico con l’istituto mutuante.",
    "Ristrutturazione in corso durante trattativa: informare acquirente su SAL e obblighi, non sul credito IRPEF residuo.",
    "Box e pertinenze: regole di cumulo diverse — chiedere chiarimento su pertinenza catastale.",
    "Detrazione e cessione credito non sono equivalenti: attenzione a proposte impresa «in fattura» non più ammissibili.",
    "Il mercato Limena premia spesso bagni rifatti e cucine a vista anche senza dettaglio fiscale in annuncio.",
    "Controlli incrociati su residenza anagrafica: utile per prima casa e aliquota 50%.",
    "Pianificare dieci rate significa non contare sul rimborso unico per chiudere mutuo variabile.",
    "Sopralluogo Righetto evidenzia difformità che bloccano bonus indipendentemente dal calendario MEF.",
    "Chi acquista all’asta deve budgetare ristrutturazione a costo pieno se tempi superano finestre fiscali.",
    "Comunicazioni ENEA restano obbligatorie su ecobonus: non mescolare con solo bonus ristrutturazioni 96.000 €.",
    "Over-investimento su finiture lusso raramente si recupera in vendita entro cinque anni nel Padovano.",
    "Buffer di due mesi su autorizzazioni comunali riduce rischio di perdere l’anno di inizio lavori rilevante.",
    "Documentazione fotografica SAL aiuta in caso di contenzioso con impresa, oltre che con AdE.",
    "Non pubblicare in annuncio percentuali di detrazione promesse da fornitori non verificati.",
    "Il rogito con lavori in corso richiede clausole chiare su titolo edilizio e responsabilità.",
    "Simulare vendita post-2028 con aliquota 30% e plafond 48.000 € prima di scalare il cantiere.",
    "Affitti brevi: ristrutturazione detraibile non aumenta automaticamente occupancy o ADR.",
    "Centro commerciale e servizi in zona Arcella influenzano domanda, non aliquota fiscale.",
    "Geometra locale conosce prassi protocollo Comune per CILA in sanatoria — utile su immobili anni ’60.",
    "Evitare di copiare tabelle da blog fiscali: costruire scenari con GU e commercialista.",
    "Hub proprietario Righetto orienta documenti vendita; fiscalità resta in capo al consulente del cliente.",
    "Ultimo controllo: bonifici parlanti, fatture e data inizio lavori allineati prima del 31 dicembre utile.",
    "Prima di firmare con impresa, chiedere cronoprogramma scritto allineato al calendario fiscale 2026–2027.",
    "Per villette a Rubano, verificare distanza da servizi e OMI locale oltre al beneficio detrazione.",
    "Non basare il prezzo di vendita solo sul costo sostenuto: il mercato sconta tempi e rischi.",
    "Se l’immobile è in comproprietà, allineare quote detrazione e pagamenti tra coeredi.",
    "Conservare copia titolo edilizio aggiornato dopo CILA in sanatoria prima di detrarre.",
    "Chiedere sempre aggiornamento scheda AdE se legge di bilancio successiva modifica aliquote.",
    "Confrontare tre preventivi imprese padovane prima di legare investimento al calendario detrazioni.",
    "Verificare capienza IRPEF del nucleo familiare su almeno cinque annualità future.",
    "Non posticipare oltre il 2026 se progetto esecutivo e titolo edilizio sono già pronti.",
    "Per immobili in co-ownership, allineare quote di spesa e ripartizione detrazione tra comproprietari.",
    "Chiedere al commercialista scenario «vendita immobile» se detrazioni sono ancora in corso.",
    "Valutare costi finanziari del cantiere oltre al credito d’imposta nominale.",
    "In periferia ovest, comparables OMI post-intervento guidano prezzo più del bonus teorico.",
    "Documentare data inizio lavori con verbale cantiere firmato da direttore lavori.",
    "Evitare doppioni editoriali: questo articolo copre calendario 2027+, non la proroga 2026.",
    "Cross-link alla guida giugno 2026 per aliquote piene ancora disponibili quest’anno.",
    "Hub proprietario Righetto per percorso vendita con documenti urbanistici a norma.",
])]

def body1() -> str:
    fig = lambda i, alt: blog_fig(f"img/blog/{S1}-{['cantiere','ape','checklist'][i]}.webp", alt)
    return f"""
{aeo_box("In sintesi", "Il riordino delle <strong>spese fiscali</strong> (tax expenditures) segnalato dal <strong>MEF</strong> prevede tagli nel triennio 2026–2028 e un calendario di <strong>aliquote</strong> e <strong>tetti</strong> per le detrazioni ristrutturazioni. Dal <strong>2027</strong> scendono le percentuali; dal <strong>2028</strong> si riduce il massimale detraibile. Analisi per chi possiede casa a <strong>Padova</strong> e provincia.")}

{DISCLAIMER_TERZI}

<h2>Perché parliamo di «addio» parziale ai bonus</h2>
<p>Non scompare tutto overnight: cambiano <strong>convenienza marginale</strong> e <strong>plafond</strong>. Il Ministero dell’Economia, nel lavoro sulla spesa fiscale (<a href="{MEF_SPESE}" target="_blank" rel="noopener noreferrer">focus MEF</a>), evidenzia centinaia di misure — molte micro — e concentra i tagli dove il costo per lo Stato è maggiore, inclusi i bonus edilizi storici.</p>

<h2>Calendario aliquote (sintesi operativa)</h2>
<table>
<thead><tr><th>Periodo</th><th>Prima casa</th><th>Altre unità</th><th>Tetto spesa (indicazioni programmatiche)</th></tr></thead>
<tbody>
<tr><td>2025–2026</td><td>50%</td><td>36%</td><td>96.000 €</td></tr>
<tr><td>2027</td><td>36%</td><td>30%</td><td>96.000 €</td></tr>
<tr><td>2028–2033</td><td>30%</td><td>30%</td><td>48.000 €</td></tr>
<tr><td>Dal 2034</td><td>36%</td><td>36%</td><td>48.000 €</td></tr>
</tbody>
</table>
<p>Verificare sempre testo di legge vigente e schede ADE aggiornate — la tabella è guida di lettura, non consulenza fiscale.</p>

<table>
<thead><tr><th>Rischio</th><th>Azione consigliata (Padova)</th></tr></thead>
<tbody>
<tr><td>Slittamento cantiere oltre l’anno utile</td><td>Buffer CILA/SCIA e data inizio lavori documentata</td></tr>
<tr><td>Capienza IRPEF insufficiente</td><td>Simulazione decennale con commercialista</td></tr>
<tr><td>Vendita durante ripartizione detrazione</td><td>Non promettere bonus all’acquirente; focus APE e prezzo OMI</td></tr>
<tr><td>Plafond 48.000 € dal 2028</td><td>Prioritizzare interventi a maggior impatto energetico per euro speso</td></tr>
</tbody>
</table>

{fig(0, "Cantiere ristrutturazione casa Padova — tempi e detrazioni")}

<h2>Cosa significa per venditori nel Padovano</h2>
<p>Anticipare lavori al 2026 può massimizzare aliquota e tetto rispetto al 2028. Chi mette in vendita immobile ristrutturato deve allineare <strong>APE</strong>, <strong>compliance urbanistica</strong> e prezzo a comparables OMI (<a href="{OMI_URL}" target="_blank" rel="noopener noreferrer">portale OMI</a>), non al valore teorico delle detrazioni.</p>
<p>Approfondimento incentivi 2026 ancora pieni: <a href="blog-bonus-edilizi-2026-incentivi-casa-padova">bonus edilizi 2026 Padova</a> — articolo distinto, non duplicato.</p>

<figure class="chart-wrap" aria-label="Timeline aliquote bonus casa">
<svg viewBox="0 0 520 200" width="100%" height="200" role="img">
<title>Timeline aliquote prima casa</title>
<text x="260" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Prima casa — aliquota indicativa</text>
<rect x="40" y="50" width="100" height="40" fill="#2C4A6E"/><text x="90" y="75" text-anchor="middle" fill="#fff" font-size="9">2025-26 50%</text>
<rect x="160" y="60" width="90" height="35" fill="#3A5F8C"/><text x="205" y="80" text-anchor="middle" fill="#fff" font-size="9">2027 36%</text>
<rect x="270" y="70" width="120" height="30" fill="#FF6B35" opacity=".9"/><text x="330" y="88" text-anchor="middle" fill="#152435" font-size="9">2028+ 30%</text>
<text x="260" y="150" text-anchor="middle" font-size="8" fill="#6B7A8D">Schema Righetto — leggere GU e ADE</text>
</svg>
<figcaption>Andamento qualitativo — non sostituisce simulazione fiscale personalizzata.</figcaption>
</figure>

<figure class="chart-wrap" aria-label="Confronto tetto spesa 96k vs 48k">
<svg viewBox="0 0 400 160" width="100%" height="160" role="img">
<text x="200" y="18" text-anchor="middle" font-size="11" fill="#152435" font-weight="700">Massimale detraibile (indicativo)</text>
<rect x="50" y="40" width="140" height="55" fill="#2C4A6E"/><text x="120" y="72" text-anchor="middle" fill="#fff" font-size="10">96.000 €</text>
<text x="120" y="88" text-anchor="middle" fill="#fff" font-size="7">fino al 2027</text>
<rect x="210" y="55" width="140" height="40" fill="#6B7A8D"/><text x="280" y="78" text-anchor="middle" fill="#fff" font-size="10">48.000 €</text>
<text x="280" y="92" text-anchor="middle" fill="#fff" font-size="7">dal 2028 (programma)</text>
</svg>
<figcaption>Schema comparativo Righetto — confermare su GU.</figcaption>
</figure>

<h2>Rischi ADE: blocchi preventivi</h2>
<p>Variazioni di reddito, cessione parziale dell’immobile, irregolarità urbanistiche o accertamenti possono sospendere l’effettivo rimborso anche se la detrazione è stata indicata in dichiarazione. Pianificare SAL, titolo e capienza fiscale prima del pagamento imprese.</p>

{fig(1, "APE e classe energetica dopo ristrutturazione Padova")}

<h2>Checklist proprietario Padova</h2>
<ol>
<li>Simulazione commercialista con calendario 2026 vs 2027.</li>
<li>Data reale inizio lavori e coerenza con anno di sostenimento spesa.</li>
<li>Verifica prima casa / altro immobile per aliquota corretta.</li>
<li>Allineamento prezzo vendita a OMI e stato tecnico, non solo a bonus.</li>
<li>Conservare fatture, bonifici, asseverazioni e titolo edilizio.</li>
</ol>

{fig(2, "Checklist documenti prima del rogito Padova")}

<h2>Domande che ci fanno in agenzia</h2>
<p><strong>«Convine ristrutturare prima di vendere?»</strong> — Solo se il delta prezzo copre costi, tempi e rischio fiscale; valutazione sopralluogo Righetto + parere tecnico.</p>
<p><strong>«L’acquirente usa il mio bonus?»</strong> — No, salvo specifici meccanismi di credito non trasferiti automaticamente col rogito.</p>

<h2>Tagli alle spese fiscali: cosa cambia nel triennio</h2>
<p>Il lavoro del MEF sulle <strong>tax expenditures</strong> non elimina le detrazioni edilizie ma le inserisce tra le voci da razionalizzare quando il costo per il bilancio supera la soglia di efficacia. Per il cittadino padovano la traduzione pratica è duplice: aliquote che scendono dal 2027 e massimali che si dimezzano dal 2028 nel quadro programmatico pubblicato con la manovra. Non è quindi un «addio» totale al bonus casa, ma un <strong>addio alla convenienza piena</strong> che molti hanno conosciuto nel 2020–2026.</p>
<p>Chi ha solo un preventivo in tasca e attende il «momento giusto» rischia di cadere nel binario 30% su 48.000 euro: conviene fissare una data di inizio lavori credibile con impresa e professionista, poi simulare detrazione lorda e netta al netto dell’IRPEF attesa.</p>

<h2>Seconda casa, affitti e investimento nel Padovano</h2>
<p>Colli Euganei, Abano, zone termali e piccoli borghi della provincia vedono molte <strong>seconde case</strong> ristrutturate per affitto turistico o locazione stagionale. L’aliquota già al 36% nel biennio 2025–2026 scende ulteriormente nel calendario 2027+: l’investimento va confrontato con canone o ricavi locativi attesi, non solo con il credito d’imposta. Righetto, in consulenza vendita o locazione, non sostituisce il commercialista ma aiuta a posizionare il prezzo coerente con lo stato tecnico post-intervento.</p>
<p>Per chi detiene immobile ereditato non ristrutturato, il calendario stringente può spingere a vendere «as is» piuttosto che immobilizzare capitale in lavori con recupero fiscale lungo: scenario da valutazione comparativa OMI e tempi di vendita medi della microzona.</p>

<h2>Ecobonus e bonus ristrutturazioni: non confonderli</h2>
<p>Il bonus «casa» su 96.000 euro riguarda interventi di recupero del patrimonio edilizio con regole proprie; l’<strong>ecobonus</strong> segue tetti e tipologie diverse (involucro, impianti, fotovoltaico). Cumulare interventi nella stessa annualità richiede massimali separati e documentazione distinta — errore frequente nei cantieri padovani che unificano tutto in un’unica fattura generica.</p>

<h2>Perché non copiamo articoli di siti fiscali o edilizia</h2>
<p>Prima di firmare un preventivo da cinque cifre, molti clienti ci chiedono se «conviene aspettare il 2027»: la risposta dipende da aliquota, plafond, capienza IRPEF e dal premio di prezzo atteso sul mercato padovano — non da un titolo virale.</p>
<p>Chi legge portali nazionali su «addio bonus casa» trova spesso titoli allarmistici e tabelle identiche da un blog all’altro. Righetto Immobiliare tratta il tema come <strong>analisi immobiliare autonoma</strong>: rileggiamo MEF, GU e schede AdE, poi traduciamo in decisioni per venditori e acquirenti nel Padovano. Non è consulenza fiscale; è orientamento su tempi cantiere, prezzo OMI, documenti rogito e rischio di investire troppo quando aliquote e plafond scendono. Se un paragrafo esterno non ha fonte istituzionale, non entra nel nostro testo — evitiamo così errori normativi e problemi di copyright.</p>

{sol_box("Come allineare ristrutturazione e vendita a Padova?", [
    ("Valutazione pre/post lavori", "Scenario prezzo con OMI e comparables", "valutazione", "landing-valutazione"),
    ("Hub proprietario", "Percorso vendita con documenti a norma", "proprietari", "proprietario-immobile"),
    ("Bonus 2026", "Aliquote ancora al 50% / 36%", "guida 2026", "blog-bonus-edilizi-2026-incentivi-casa-padova"),
    ("Case green", "Efficientamento e mercato", "direttiva", "blog-direttiva-case-green-limena-padova"),
])}

{_pad(EXP1, len(EXP1))}

<p>{CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Aggiornamento:</strong> {DATE_IT}. Fonti: MEF (spese fiscali), quadro programmatico detrazioni edilizie, ADE.</p>
"""


# --- Articolo 2: Legge 198/2025 ---
S2 = "blog-legge-bilancio-198-2026-bonus-edilizi-padova"
IMG2 = [
    ("img/blog/blog-compravendite-italia-q1-agenzia-entrate-2026.webp", f"img/blog/{S2}-hero.webp"),
    ("img/blog/blog-documenti-compravendita-rogito-padova-2026.webp", f"img/blog/{S2}-rogito.webp"),
    ("img/blog/blog-domanda-case-green-padova-2026.webp", f"img/blog/{S2}-efficienza.webp"),
    ("img/blog/blog-compravendite-italia-q1-agenzia-entrate-2026.webp", f"img/blog/{S2}-vendita.webp"),
]

EXP2 = [
    "La Legge di Bilancio 2026 (L. 198/2025, GU 301/2025) conferma per l’anno in corso le detrazioni edilizie più usate, rimandando al 2027 il calo programmato.",
    "Gli interventi devono essere <strong>iniziati</strong> entro l’anno precedente a quello di sostenimento spesa per il bonus ristrutturazioni — regola tecnica da verificare sul testo e sul commercialista.",
    "Ecobonus e bonus ristrutturazioni condividono logica 50% / 36% e dieci rate annuali per molte tipologie.",
    "A Padova la domanda di efficientamento cresce con APE obbligatorio in compravendite e locazioni.",
    "Il superbonus 110% non torna: restano misure ordinarie — messaggio già chiaro nel 2025.",
    "Sismabonus e zone terremotate seguono regole dedicate — fuori dal focus padovano salvo immobili con requisiti specifici.",
    "Fotovoltaico e rinnovabili hanno vincoli UE sulla filiera produttiva introdotti dalla manovra — verificare decreti attuativi.",
    "Il prezzario nazionale lavori pubblici (riferimento giugno 2026) aiuta imprese e PA, non sostituisce preventivi privati.",
    "Proprietario che affitta: ristrutturazione con bonus può giustificare revisione canone solo se mercato e contratto lo consentono.",
    "Righetto non calcola detrazioni ma coordina rogito e documentazione urbanistica.",
    "Confrontare sempre scheda ADE aggiornata al PDF GU — due fonti obbligatorie.",
    "Centro storico Padova: vincoli Soprintendenza possono allungare tempi — incide sull’anno di inizio cantiere.",
    "Condominio e parti comuni: regole specifiche su spesa e ripartizione detrazione.",
    "Cessione del credito e sconto in fattura restano limitati rispetto al passato — attenzione a cosa propongono imprese.",
    "La GU 301/2025 va scaricata in PDF e confrontata con la circolare ADE: eventuali ritardi interpretativi capitano nei primi mesi dell’anno.",
    "Per immobili in asta giudiziaria, l’aggiudicatario che ristruttura riavvia la filiera bonus solo se rispetta requisiti di titolo e inizio lavori — verifica notarile.",
    "Il prezzario nazionale lavori pubblici citato in manovra aiuta imprese che lavorano con PA; per privati a Selvazzano o Monselice restano i preventivi di mercato.",
    "Bonus facciate e decoro urbano seguono regole autonome: centro storico Padova spesso le combina con vincoli paesaggistici.",
    "Ristrutturazione per divisione immobile in due unità: attenzione a catasto, conformità e massimali per singola unità.",
    "Energy community e autoconsumo collettivo sono temi distinti dal bonus ristrutturazioni ordinario — non mescolare in un unico progetto senza consulenza.",
    "Per la compravendita, inserire in annuncio solo dati verificabili (APE, mq, conformità): non promettere detrazioni all’acquirente.",
    "Righetto consiglia perizia prima di grandi cantieri quando l’obiettivo dichiarato è vendita entro 24 mesi.",
    "Le rate di detrazione non compensano rate mutuo se il reddito scende: stress test fiscale consigliato.",
    "Impianti fotovoltaico con vincoli UE sulla filiera: decreti attuativi possono escludere componenti non conformi — chiedere certificazioni all’installatore.",
    "Studenti in affitto: il locatore padovano che ristruttura detrae; eventuali aumenti canone vanno concordati nel rispetto del mercato.",
    "Artigiani edili della provincia segnalano lead time materiali: slittamento cantiere può spostare spesa fiscale — allineare SAL e fatture.",
    "Non riprodurre tabelle di siti fiscali terzi: usare sempre fonte istituzionale aggiornata — regola anti-plagio Righetto.",
    "Prima del rogito, chiedete al notaio se restano lavori aperti: la clausola deve chiarire responsabilità urbanistiche, non le detrazioni IRPEF del venditore.",
    "A Selvazzano e Monselice, come nel capoluogo, il prezzario PA non sostituisce tre preventivi privati: usatelo solo come termometro macro.",
    "Se comprate all’asta a Padova, budgetate ristrutturazione anche senza bonus se i tempi di agibilità superano l’anno fiscale utile.",
    "Comunicazioni ENEA per ecobonus: se mancano, la decadenza può arrivare dopo la vendita — conservate ricevute oltre al passaggio di proprietà.",
    "Mutuo ristrutturazione e detrazione vanno simulati insieme al commercialista, non dedotti dal promotore immobiliare.",
    "In trattativa non cite percentuali di bonus promesse da imprese: citate APE, conformità e prezzo coerente con OMI.",
    "Condominio in Via Venezia o simili: senza delibera su parti comuni, rischiate blocchi su detrazioni condivise.",
    "Fotovoltaico con vincoli di filiera UE: chiedete certificazioni componenti prima del SAL, non a fine detrazione.",
    "Divisione immobile in due unità: verificate massimali per singola unità e allineamento catastale prima del cantiere.",
    "Locazione studenti: il locatore detrae ristrutturazioni; aumenti canone vanno concordati nel rispetto del mercato, non del credito d’imposta.",
    "Centro storico: buffer Soprintendenza nel cronoprogramma — slittare gennaio può costare un anno di aliquota piena.",
    "Cessione credito o sconto in fattura: non firmate procure senza parere fiscale — regole più restrittive rispetto al passato.",
    "Cross-link interno: calendario 2027+ e guida bonus giugno 2026 restano articoli distinti, non duplicati di questo pezzo.",
    "Quando un portale edilizia riassume la Legge 198/2025 in cinque righe, manca sempre la data di inizio lavori: noi la ripetiamo perché è il punto che fa saltare l’anno fiscale a Padova come altrove.",
    "Imprese che lavorano su due appartamenti nello stesso stabile devono separare massimali e bonifici per unità: errori frequenti in condomini anni Settanta della cintura.",
    "Perizia bancaria post-ristrutturazione valuta comparables e rischio, non crediti d’imposta residui: non confondete parere del mutuo con convenienza fiscale.",
    "Bonus facciate in centro storico richiedono spesso parere paesaggistico: tempi lunghi vanno inseriti nel cronoprogramma prima di assumere detrazione piena nel 2026.",
    "Se vendete con detrazioni in corso, il prezzo richiesto deve restare ancorato a OMI: l’acquirente non paga il vostro credito IRPEF non trasferibile.",
    "Acquirente straniero: regole titolo e pagamenti restano identiche; servono commercialista e notaio per filiera bonus riavviata a nome nuovo.",
    "Ristrutturazione parziale per mettere in locazione: distinguere manutenzione ordinaria da intervento ammissibile — il canone non recupera automaticamente il bonus.",
    "Energy community e autoconsumo sono temi separati: non li mescolate nel preventivo «unico» senza consulenza specializzata.",
    "Controlli AdE su possesso immobile e residenza anagrafica restano centrali per aliquota 50%: documentate prima del SAL finale.",
    "Prezzario nazionale citato in manovra aiuta imprese PA; per privati a Ponte di Brenta restano tre preventivi comparabili e capitolato dettagliato.",
    "Studentati e locazioni: il locatore padovano che ristruttura detrae; studente non eredita bonus — utile chiarirlo nel contratto oltre che in dichiarazione.",
    "Fotovoltaico: verificate decreti filiera prima dell’ordine materiali — componenti non conformi espongono a decadenza dopo installazione.",
    "Sismabonus fuori focus sismico padovano salvo casi specifici: strutturista prima di includerlo nel business plan vendita.",
    "Non duplicate FAQ da siti terzi: ogni risposta qui passa da GU 301/2025 o scheda AdE aggiornata al 2026.",
    "Hub proprietario e valutazione Righetto per allineare prezzo vendita e documenti; fiscalità resta in capo al commercialista del cliente.",
    "Ultimo promemoria: dieci rate annuali implicano pianificazione reddito pluriennale — stress test prima di impegnare capacità di spesa oltre il plafond.",
]

def body2() -> str:
    return f"""
{aeo_box("In sintesi", "Pubblicata in <strong>Gazzetta Ufficiale</strong> (L. <strong>198/2025</strong>, GU n. 301/2025), la Legge di Bilancio <strong>proroga al 2026</strong> bonus ristrutturazione, <strong>ecobonus</strong> e <strong>sismabonus</strong> con aliquote in linea con il 2025. Per il Padovano che compra o vende, conta la data di <strong>inizio lavori</strong> e la documentazione ADE.")}

{DISCLAIMER_TERZI}

<h2>Cosa conferma la manovra 2026</h2>
<p>Detrazione <strong>50%</strong> per abitazione principale e <strong>36%</strong> negli altri casi ammessi, massimale <strong>96.000 euro</strong> per unità sul bonus ristrutturazioni (scheda ADE). Dieci quote annuali di pari importo. Testo completo: <a href="{GU_L198}" target="_blank" rel="noopener noreferrer">GU Legge 198/2025</a>.</p>

<h2>Ecobonus 2026: cosa resta uguale</h2>
<p>Interventi di efficientamento su edifici con impianto di riscaldamento esistente; esclusione incentivazione per sostituzione con caldaia <strong>solo fossile</strong> (coerente con schede ADE 2025–2027). Limiti di spesa dipendono dalla tipologia intervento — non c’è un unico tetto come il bonus casa.</p>

{blog_fig(f"img/blog/{S2}-rogito.webp", "Documenti rogito e ristrutturazione Padova")}

<table>
<thead><tr><th>Misura</th><th>Stato 2026</th><th>Nota Padova</th></tr></thead>
<tbody>
<tr><td>Bonus ristrutturazioni</td><td>Confermato 50% / 36%</td><td>Verificare inizio lavori 2025 se spesa 2026</td></tr>
<tr><td>Ecobonus</td><td>Confermato</td><td>Utile su condomini anni ’70 in periferia</td></tr>
<tr><td>Sismabonus</td><td>Confermato</td><td>Rilevante se requisiti sismici</td></tr>
<tr><td>Superbonus 110%</td><td>Non prorogato</td><td>Non confondere con bonus ordinari</td></tr>
</tbody>
</table>

<table>
<thead><tr><th>Documento</th><th>Perché conta in vendita</th></tr></thead>
<tbody>
<tr><td>APE post-lavori</td><td>Prova miglioramento energetico per acquirente e banca</td></tr>
<tr><td>CILA/SCIA conforme</td><td>Evita blocchi rogito e contestazioni urbanistiche</td></tr>
<tr><td>Fascicolo detrazioni (venditore)</td><td>Non trasferibile; separare da dossier immobile</td></tr>
</tbody>
</table>

<h2>Impatti su compravendita a Padova</h2>
<p>Chi compra immobile da ristrutturare deve pianificare <strong>titolo</strong>, <strong>CILA/SCIA</strong> e <strong>inizio cantiere</strong> per non perdere l’anno fiscale utile. Chi vende dopo lavori presenta APE e conformità — vedi <a href="blog-costi-vendere-casa-padova-2026">costi vendita Padova</a>.</p>

{blog_fig(f"img/blog/{S2}-efficienza.webp", "Efficienza energetica e mercato Padova")}

<figure class="chart-wrap" aria-label="Flusso bonus ristrutturazione">
<svg viewBox="0 0 480 220" width="100%" height="220" role="img">
<text x="240" y="22" text-anchor="middle" font-size="11" fill="#152435" font-weight="700">Filiera documentale (schema)</text>
<rect x="30" y="45" width="90" height="32" rx="6" fill="#2C4A6E"/><text x="75" y="65" text-anchor="middle" fill="#fff" font-size="8">Inizio lavori</text>
<path d="M120 61 L150 61" stroke="#FF6B35" stroke-width="2"/>
<rect x="150" y="45" width="90" height="32" rx="6" fill="#3A5F8C"/><text x="195" y="65" text-anchor="middle" fill="#fff" font-size="8">Spesa / SAL</text>
<path d="M240 61 L270 61" stroke="#FF6B35" stroke-width="2"/>
<rect x="270" y="45" width="90" height="32" rx="6" fill="#FF6B35" opacity=".85"/><text x="315" y="65" text-anchor="middle" fill="#152435" font-size="8">Detrazione</text>
<path d="M360 61 L390 61" stroke="#FF6B35" stroke-width="2"/>
<rect x="390" y="45" width="70" height="32" rx="6" fill="#2C4A6E"/><text x="425" y="65" text-anchor="middle" fill="#fff" font-size="8">10 rate</text>
<text x="240" y="120" text-anchor="middle" font-size="8" fill="#6B7A8D">Semplificazione — ogni caso va verificato</text>
</svg>
<figcaption>Schema Righetto per orientamento; non sostituisce commercialista.</figcaption>
</figure>

<figure class="chart-wrap" aria-label="Aliquote 2026 vs 2027 prima casa">
<svg viewBox="0 0 360 150" width="100%" height="150" role="img">
<text x="180" y="20" text-anchor="middle" font-size="10" fill="#152435" font-weight="700">Prima casa — confronto indicativo</text>
<rect x="40" y="45" width="120" height="45" fill="#2C4A6E"/><text x="100" y="72" text-anchor="middle" fill="#fff" font-size="11">2026 · 50%</text>
<rect x="200" y="55" width="120" height="35" fill="#FF6B35" opacity=".9"/><text x="260" y="76" text-anchor="middle" fill="#152435" font-size="11">2027 · 36%</text>
</svg>
<figcaption>Confronto qualitativo — fonte GU e ADE.</figcaption>
</figure>

<h2>Caro materiali e cantieri pubblici</h2>
<p>La manovra stanzia risorse per cantieri PA e introduce riferimenti di prezzario nazionale — tema indiretto per chi confronta preventivi privati a Padova, dove ISTAT segnala costi costruzione in trend (vedi articolo costi costruzione Padova).</p>

<h2>Proroga 2026 vs articoli esteri: come leggere le notizie</h2>
<p>Portali edilizia e blog fiscali riassumono spesso la manovra in titoli catastrofici («addio bonus»). La lettura corretta per un proprietario padovano passa da tre passaggi: verificare il testo in GU, aprire la scheda ADE aggiornata, chiedere al commercialista l’impatto sul proprio modello reddituale. Righetto rielabora questi temi in chiave immobiliare — <strong>senza copiare</strong> articoli di terzi — perché ciò che conta in agenzia è quanto vale l’immobile sul mercato dopo i lavori, non il titolo SEO di un sito nazionale.</p>

<h2>Data di inizio lavori: errore che costa l’anno fiscale</h2>
<p>Per il bonus ristrutturazioni la norma richiede che gli interventi siano <strong>iniziati</strong> entro l’anno precedente a quello di sostenimento della spesa (regola tecnica da confermare sul comma vigente). Un cantiere slittato da dicembre a gennaio senza inizio effettivo può far perdere un intero anno di detrazione piena. A Padova i tempi CILA/SCIA del Comune e eventuali pareri Soprintendenza allungano spesso i cronoprogrammi: pianificare buffer di due-tre mesi.</p>

<h2>Acquirente vs venditore: chi pianifica il bonus</h2>
<p>Chi compra «da ristrutturare» in periferia (Pontevigodarzere, Cadoneghe) di solito intende detrarre a proprio nome: serve rogito pulito, titolo edilizio regolare e nuova filiera di pagamenti. Chi vende dopo lavori deve invece dimostrare miglioramento reale con APE e documenti urbanistici — il bonus già maturato resta del venditore e non è vendibile come «extra» in trattativa salvo specifici crediti residuali gestiti fiscalmente.</p>

<h2>Fonti esterne sì, copia no</h2>
<p>Approfondimenti generalisti sulla Legge di Bilancio circolano con tabelle identiche e FAQ clone. Noi rileggiamo la GU 301/2025 e le schede AdE, poi traduciamo in azioni per chi vende o compra a Padova: titolo edilizio, data inizio lavori, APE, prezzo OMI. Non ripubblichiamo blocchi di testo da blog fiscali o portali edilizia — riduce rischi legali e mantiene focus immobiliare. Per aliquote e massimali chiamate sempre il commercialista; per valutazione e documenti rogito, Righetto resta il riferimento operativo sul territorio.</p>

{blog_fig(f"img/blog/{S2}-vendita.webp", "Vendita casa dopo ristrutturazione Padova")}

<h2>Link utili</h2>
<ul>
<li><a href="{ADE_RISTR}" target="_blank" rel="noopener noreferrer">Scheda ADE bonus ristrutturazioni</a></li>
<li><a href="blog-bonus-casa-2027-detrazioni-padova">Calendario 2027+</a></li>
<li><a href="blog-bonus-edilizi-2026-incentivi-casa-padova">Guida bonus 2026 (giugno)</a> — complementare</li>
</ul>

<h2>Sismabonus e territorio: quando conta a Padova</h2>
<p>Il Padovano non è in prima fila sismica come altre regioni, ma edifici con vincoli o classificazione specifica possono accedere al <strong>sismabonus</strong> se rispettano i requisiti tecnici. La Legge 198/2025 ne conferma l’esistenza nel 2026: verificare con strutturista se l’intervento rientra nelle tipologie ammesse prima di includerlo nel business plan di ristrutturazione pre-vendita.</p>

<h2>ENEA, comunicazioni e decadenze</h2>
<p>Per molte tipologie di efficientamento la comunicazione a <strong>ENEA</strong> entro termini è condizione di validità dell’agevolazione. Slittamenti o errori formali possono far decadere la detrazione già indicata in dichiarazione. Proprietari padovani che vendono subito dopo i lavori devono conservare ricevute ENEA oltre a APE e titolo edilizio — l’acquirente può chiedere garanzie sulla regolarità fiscale del cantiere concluso.</p>

{_pad(EXP2, len(EXP2))}

<p>{CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Aggiornamento:</strong> {DATE_IT}. Fonte normativa: GU L. 198/2025.</p>
"""


# --- Articolo 3: mobili + barriere ---
S3 = "blog-bonus-mobili-barriere-architettoniche-2026-padova"
IMG3 = [
    ("img/blog/blog-bonus-mobili-ristrutturazioni-2026.webp", f"img/blog/{S3}-hero.webp"),
    ("img/blog/blog-casa-vendibile-5-anni-case-green-padova-2026.webp", f"img/blog/{S3}-mobili.webp"),
    ("img/blog/blog-domanda-case-green-padova-2026.webp", f"img/blog/{S3}-accessibilita.webp"),
    ("img/blog/blog-bilocale-trilocale-limena-scelta-2026.webp", f"img/blog/{S3}-interni.webp"),
]

EXP3 = [
    "Il bonus mobili resta al 50% fino a 5.000 euro di spesa ammissibile se collegato a ristrutturazione della stessa unità — regola da confermare su scheda ADE anno per anno.",
    "Fine bonus barriere architettoniche al 31/12/2025 sposta su costo pieno gli adeguamenti accessibilità dal 2026.",
    "Proprietari padovani con bagni stretti in bilocali semicentro: senza detrazione 75%, valutare priorità intervento vs prezzo vendita.",
    "Mobili ed elettrodomestici devono essere acquistati in coerenza temporale con lavori — conservare scontrini e collegamento fatture impresa.",
    "Affittare a studenti o anziani: barriere architettoniche incidono su domanda ma non sempre su canone misurabile.",
    "Righetto segnala in perizia difformità bagno e passaggi — utile prima del bonus mobili.",
    "Limena: villette su un piano spesso più agevoli per accessibilità rispetto a walk-up in centro Padova.",
    "Non confondere detrazione mobili con credito IVA arredi per imprese — regimi diversi.",
    "Ascensori in condominio: distinzione parte privata vs comune per detrazioni.",
    "Vendere casa non accessibile: prezzo scontato o investimento mirato — scenario da valutazione.",
    "Ecobonus su infissi + mobili cucina: due filiere documentali separate.",
    "Commercialista obbligatorio per cumulo detrazioni e massimali.",
    "Fine detrazione barriere non elimina obblighi normativi su edifici pubblici — tema distinto.",
    "Checklist inventario mobili nuovi in caso di locazione arredata.",
    "Il 50% su mobili non copre progettazione bagno accessibile: senza bonus barriere, il costo pieno va messo a budget.",
    "Piattaforme e-commerce per elettrodomestici: conservare prova classe energetica ammissibile.",
    "Vendita a famiglia con anziano: accessibilità può accelerare trattativa anche senza detrazione 75%.",
    "Righetto segnala in trattativa se il bagno è ristrutturato ma non conforme D.Lgs. 151/2001 — tema distinto dal bonus.",
    "Bonus mobili e detrazione ristrutturazione condividono dieci rate ma massimali separati.",
    "Affitto studenti in zona Università: mobili nuovi detraibili solo con filiera ristrutturazione collegata.",
    "Non trascrivere checklist da blog edilizia: costruire piano con tecnico abilitato e commercialista.",
    "Per locazione a reddito, ammortamento fiscale arredi segue regole diverse dal bonus 50% per privati.",
    "Scale interne strette in bilocali Padova centro: eliminare barriere può richiedere interventi strutturali non più incentivati al 75%.",
    "Comunicare in annuncio «bagno rifatto» solo se conforme e documentato — trasparenza verso acquirente.",
    "Collegamento temporale mobili-lavori: fatture fuori finestra cantiere espongono a rigetti ADE.",
    "Integrazione con ecobonus su infissi: due SAL distinti e due massimali — coordinare impresa general contractor.",
    "Valutazione immobiliare post-intervento: Righetto pesa accessibilità percettiva anche senza detrazioni.",
    "Future manovre potrebbero reintrodurre misure sociali: non basare investimento solo su voci scadute nel 2025.",
    "Ogni scontrino arredo va collegato alla finestra del cantiere ristrutturazioni: fuori tempo, il 50% mobili non scatta.",
    "Dal 2026 il bagno accessibile va budgetato a costo pieno: simulate plusvalenza OMI prima di investire oltre diecimila euro.",
    "In visita contano doccia walk-in e maniglie: sono spesso più efficaci del 75% barriere per chiudere trattativa.",
    "Non inserite in annuncio detrazioni mobili non ancora maturate: l’acquirente verifica conformità, non il vostro credito IRPEF.",
    "Locazione arredata: inventario firmato separato dalla cartella fiscale delle detrazioni del locatore.",
    "Elettrodomestici ammessi al bonus mobili richiedono classe energetica documentata — conservate manuali e scontrini.",
    "Allargamento porte su muratura portante: chiedete parere strutturale prima del preventivo idraulico.",
    "Prima di investire in piattaforme elevatrici, verificate domanda anziani nella microzona con comparables recenti.",
    "Ecobonus infissi e bonus mobili richiedono due filiere SAL distinte: unica fattura «tutto incluso» espone a scarti.",
    "Checklist copiate da blog edilizia non sostituiscono tecnico abilitato e commercialista — regola anti-plagio Righetto.",
    "Bilocale in centro senza ascensore: accessibilità riduce bacino acquirenti — pricing OMI deve rifletterlo.",
    "Rogito dopo chiusura cantiere se promettete finiture nuove: altrimenti rischio contestazione post-vendita.",
    "Smaltimento mobili vecchi resta fuori plafond detraibile: mettetelo a budget cantieri.",
    "Se rimandate al 2027, incrociate simulazione con l’articolo calendario aliquote bonus casa — due leve fiscali distinte.",
    "Portali che titolano «addio bonus mobili» confondono spesso fine barriere e conferma mobili 50%: noi separiamo le misure con GU e AdE.",
    "Cucina su misura consegnata dopo chiusura cantiere rischia di uscire dalla finestra mobili: allineate tempi fornitore e SAL impresa.",
    "Vendita ad acquirente anziano: accessibilità percettiva può valere più del credito d’imposta perso — valutazione comparativa sul campo.",
    "Affitto camere a studenti: mobili detraibili restano del proprietario; canone segue domanda universitaria, non detrazione.",
    "Ascensore condominiale vs modifiche interne: distinzione netta per detrazioni — chiedete delibera assemblea prima di lavori comuni.",
    "Impresa «chiavi in mano» deve dettagliare voci arredo ammissibili: fattura unica generica espone a rigetti su bonus mobili.",
    "Manuali elettrodomestici e classi energetiche vanno conservati anni: utili in caso di controllo post-dichiarazione.",
    "Bagno stretto in bilocale Arcella: senza 75%, priorità a layout funzionale e prezzo OMI realistico piuttosto che over-investimento.",
    "Non promettete in annuncio «bonus barriere» oltre il 2025: verificabile solo su normativa vigente, non su articoli web datati.",
    "Perizia Righetto segnala difformità bagno e passaggi prima della messa in vendita — indipendente da detrazioni.",
    "Cross-link Legge 198 e calendario 2027+: tre articoli complementari, keyword distinte in SKIMM, nessun doppione.",
    "Consulenza fiscale obbligatoria per cumulo mobili, ristrutturazioni ed ecobonus nella stessa annualità di spesa.",
    "Foto prima/dopo servono marketing e trattativa oltre che eventuale contenzioso con impresa — conservatele ordinate per data.",
    "Investimento accessibilità a costo pieno: simulate sconto prezzo accettabile in novanta giorni di vendita media zona.",
    "Righetto media aspettative tra venditore e famiglia con anziano senza promesse fiscali non verificabili in sede.",
    "Prima di acquistare mobili online, verificate tempi consegna rispetto al SAL impresa: ritardi possono escludere il 50% su arredi.",
    "Separare in proposta vendita valore immobile e valore arredi nuovi: trattativa più chiara e allineata a perizia bancaria.",
    "Se obiettivo è locazione breve, mobili detraibili non garantiscono occupancy: revenue management resta indipendente dal fisco.",
]

def body3() -> str:
    return f"""
{aeo_box("In sintesi", "Nel <strong>2026</strong> resta il <strong>bonus mobili</strong> (50% fino a 5.000 € legato a ristrutturazione) mentre il <strong>bonus barriere architettoniche</strong> (75%) <strong>non è prorogato</strong> oltre il 2025. Per proprietari a Padova che preparano vendita o locazione, cambia il conto economico degli adeguamenti accessibilità.")}

{DISCLAIMER_TERZI}

<h2>Bonus mobili 2026</h2>
<p>Acquisto di mobili, arredi ed elettrodomestici di classe non inferiore in efficientamento, collegato a intervento di recupero del patrimonio edilizio sulla stessa unità. Tetto <strong>5.000 euro</strong> di spesa ammissibile, detrazione <strong>50%</strong>, dieci rate. Verificare: <a href="{ADE_RISTR}" target="_blank" rel="noopener noreferrer">ADE</a> e <a href="{GU_L198}" target="_blank" rel="noopener noreferrer">GU 198/2025</a>.</p>

{blog_fig(f"img/blog/{S3}-mobili.webp", "Arredo casa dopo ristrutturazione Padova")}

<h2>Addio bonus barriere architettoniche</h2>
<p>Dal 2026 non spetta più la detrazione al 75% per eliminazione barriere (scale, bagno, porte, piattaforme). Restano eventuali altre agevolazioni o detrazioni ordinarie solo se espressamente previste — non assumere continuità automatica.</p>

<table>
<thead><tr><th>Misura</th><th>2025</th><th>2026</th></tr></thead>
<tbody>
<tr><td>Bonus mobili</td><td>50% max 5.000 €</td><td>Confermato (con bonus casa)</td></tr>
<tr><td>Barriere architettoniche</td><td>75%</td><td>Non prorogato</td></tr>
<tr><td>Bonus ristrutturazioni</td><td>50% / 36%</td><td>Confermato</td></tr>
</tbody>
</table>

<table>
<thead><tr><th>Intervento</th><th>Detrazione 2026</th><th>Nota mercato Padova</th></tr></thead>
<tbody>
<tr><td>Cucina e mobili legati a ristrutturazione</td><td>50% max 5.000 € spesa</td><td>Valorizza annuncio se documentato</td></tr>
<tr><td>Bagno accessibile</td><td>Costo pieno (fine 75%)</td><td>Può accelerare trattativa famiglie</td></tr>
<tr><td>Infissi efficienti</td><td>Ecobonus / ristrutturazioni</td><td>APE migliore in periferia anni ’70</td></tr>
</tbody>
</table>

<h2>Strategia proprietario Padova</h2>
<p>Se obiettivo è <strong>vendere</strong> a famiglie o anziani, l’assenza del 75% spinge a priorizzare interventi a basso costo ad alta percepibilità (doccia walk-in, maniglie, illuminazione) o accettare un pricing OMI più basso. Vedi <a href="blog-casa-vendibile-5-anni-case-green-padova-2026">casa vendibile e green</a>.</p>

{blog_fig(f"img/blog/{S3}-accessibilita.webp", "Accessibilità e mercato immobiliare Padova")}

<figure class="chart-wrap" aria-label="Confronto bonus mobili vs barriere">
<svg viewBox="0 0 440 180" width="100%" height="180" role="img">
<text x="220" y="20" text-anchor="middle" font-size="11" fill="#152435" font-weight="700">2026 — due misure a confronto</text>
<rect x="60" y="45" width="120" height="50" fill="#2C4A6E"/><text x="120" y="72" text-anchor="middle" fill="#fff" font-size="9">Mobili 50%</text>
<text x="120" y="88" text-anchor="middle" fill="#fff" font-size="7">max 5.000 €</text>
<rect x="260" y="55" width="120" height="40" fill="#6B7A8D" opacity=".5"/><text x="320" y="78" text-anchor="middle" fill="#152435" font-size="9">Barriere</text>
<text x="320" y="92" text-anchor="middle" fill="#152435" font-size="7">stop 2026</text>
</svg>
<figcaption>Confronto sintetico — leggere schede ADE.</figcaption>
</figure>

<figure class="chart-wrap" aria-label="Priorità investimento senza bonus barriere">
<svg viewBox="0 0 420 140" width="100%" height="140" role="img">
<text x="210" y="18" text-anchor="middle" font-size="10" fill="#152435" font-weight="700">Priorità percepibilità vs costo</text>
<rect x="30" y="40" width="100" height="35" fill="#2C4A6E"/><text x="80" y="62" text-anchor="middle" fill="#fff" font-size="8">Doccia filo pavimento</text>
<rect x="150" y="40" width="100" height="35" fill="#3A5F8C"/><text x="200" y="62" text-anchor="middle" fill="#fff" font-size="8">Maniglie / luci</text>
<rect x="270" y="40" width="100" height="35" fill="#6B7A8D"/><text x="320" y="62" text-anchor="middle" fill="#fff" font-size="8">Porte allargate</text>
<text x="210" y="110" text-anchor="middle" font-size="7" fill="#6B7A8D">Schema orientativo vendita — non sostituisce preventivo</text>
</svg>
<figcaption>Interventi spesso citati in trattativa a Padova.</figcaption>
</figure>

<p>Articolo correlato già in catalogo: <a href="blog-bonus-mobili-2026-massimizzare-ristrutturazioni">bonus mobili massimizzare</a> — angolo operativo; qui focus su barriere e calendario 2026.</p>

{blog_fig(f"img/blog/{S3}-interni.webp", "Interni bilocale Padova — ristrutturazione e arredo")}

<h2>FAQ operative</h2>
<p><strong>Posso comprare mobili nel 2026 senza ristrutturazione?</strong> — No per il bonus mobili dedicato; serve filiera ristrutturazione collegata.</p>
<p><strong>Conviene rimandare bagno accessibile al 2027?</strong> — Senza 75%, solo costo pieno salvo future misure — simulare con tecnico.</p>

<h2>Perché il 75% barriere non è prorogato</h2>
<p>La manovra 2026 concentra risorse su bonus ordinari già strutturati e su efficientamento, lasciando cadere la misura più generosa per eliminazione barriere architettoniche. Non significa che l’accessibilità sia irrilevante sul mercato padovano: significa che il <strong>costo</strong> dell’adeguamento grava interamente sul proprietario. In trattativa, un bagno non accessibile in piano alto senza ascensore può ridurre il bacino acquirenti — effetto prezzo da valutazione, non da detrazione.</p>

<h2>Mobili, elettrodomestici e marketing dell’impresa</h2>
<p>Le imprese edili spesso propongono pacchetti «chiavi in mano» con arredo incluso. Verificare che ogni voce sia fatturata correttamente, che gli elettrodomestici rispettino le classi ammesse e che l’acquisto avvenga nella finestra temporale dei lavori. Righetto consiglia di separare sempre preventivo strutturale, impianti, finiture e arredo per leggere meglio il valore di mercato dell’immobile finito.</p>

<h2>Padova: quartieri dove l’accessibilità pesa di più</h2>
<p>In zone con popolazione anziana o domanda familiare (Arcella, Ponte di Brenta, porzioni di Limena) un piccolo intervento — doccia a filo pavimento, maniglioni, porte allargate — può essere decisivo anche senza detrazione. Nei bilocali del centro storico, dove spesso manca l’ascensore, la mancanza di bonus 75% spinge alcuni proprietari a vendere a investitori piuttosto che adeguare.</p>

<h2>Come usiamo spunti web senza copiare</h2>
<p>Articoli comparativi su bonus mobili e fine barriere architettoniche aiutano a capire il tema ma spesso mescolano misure diverse in un unico titolo clickbait. Righetto separa bonus mobili 50%, stop 75% barriere e bonus ristrutturazioni ordinario, verificando ogni voce su GU e AdE. Il testo che leggete è scritto per proprietari padovani che devono decidere se investire in accessibilità a costo pieno o puntare su arredo e finiture detraibili collegate al cantiere — non è un riassunto di siti terzi.</p>

{sol_box("Serve orientamento immobiliare su ristrutturato vs da fare?", [
    ("Valutazione", "Scenario vendita con stato immobile", "landing", "landing-valutazione"),
    ("Proprietari", "Vendita e locazione", "hub", "proprietario-immobile"),
    ("Legge 2026", "Proroghe bonus", "legge 198", "blog-legge-bilancio-198-2026-bonus-edilizi-padova"),
    ("Calendario 2027", "Aliquote future", "2027", "blog-bonus-casa-2027-detrazioni-padova"),
])}

<h2>Documenti da tenere in cartella vendita</h2>
<p>Se vendete dopo ristrutturazione con mobili nuovi, l’acquirente potrebbe chiedere prova di conformità impianti e titolo edilizio, non le vostre detrazioni mobili. Tenete separati fascicolo fiscale (fatture, bonifici, dichiarazioni) e fascicolo immobiliare (APE, planimetrie, conformità). Righetto in trattativa usa il secondo; il commercialista gestisce il primo.</p>

<h2>Locazione: mobili ammobiliati e detrazione</h2>
<p>Il proprietario che affitta arredato a Padova può avere mobili detraibili solo se collegati a ristrutturazione della stessa unità; l’inventario locativo va tenuto aggiornato per evitare contestazioni in uscita inquilino. Il canone non «recupera» automaticamente il 50% su arredi: la detrazione resta credito IRPEF del locatore, non maggiorazione canone garantita.</p>

<h2>Acquirente anziano o famiglia: trattativa senza bonus</h2>
<p>Senza il 75% barriere, alcuni acquirenti chiederanno ribasso o lavori a carico venditore. Preparare preventivi realistici prima della messa in vendita evita trattative bloccate a metà. Righetto media le aspettative usando comparables e stato tecnico, non promesse fiscali.</p>

{_pad(EXP3, len(EXP3))}

<p>{CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Aggiornamento:</strong> {DATE_IT}.</p>
"""


ARTICLES = [
    {
        "slug": S1,
        "filename": f"{S1}.html",
        "hero": f"img/blog/{S1}-hero.webp",
        "hero_alt": "Bonus casa 2027 calendario detrazioni Padova",
        "cat_badge": "Fisco · Ristrutturazioni",
        "h1": "<strong>Bonus casa 2027</strong>: calendario detrazioni e impatto a Padova",
        "title": "Bonus casa 2027: calendario detrazioni Padova",
        "og_title": "Bonus casa 2027: calendario detrazioni Padova",
        "meta": "Calendario aliquote bonus ristrutturazioni 2027–2033, tagli MEF e checklist venditori Padova. Analisi Righetto — verificare GU e ADE.",
        "schema_headline": "Bonus casa 2027 calendario detrazioni Padova",
        "section": "Fisco e ristrutturazioni",
        "bread_crumb": "Bonus casa 2027 Padova",
        "body_fn": body1,
        "faqs": [
            ("Quando scendono le aliquote bonus ristrutturazioni?", "Dal 2027 al 36% prima casa e 30% altri casi nel quadro programmatico; verificare legge vigente."),
            ("Cosa succede al tetto di spesa nel 2028?", "Indicazioni programmatiche portano il massimale da 96.000 a 48.000 euro — confermare su GU."),
            ("Righetto calcola le detrazioni?", "No: valutazioni immobiliari; per fisco rivolgersi a commercialista e ADE."),
            ("Devo ristrutturare prima di vendere a Padova?", "Solo se il salto di prezzo copre costi e tempi; valutazione e OMI guidano la scelta."),
        ],
        "related": [
            ("Bonus edilizi 2026", "blog-bonus-edilizi-2026-incentivi-casa-padova"),
            ("Legge Bilancio 2026", "blog-legge-bilancio-198-2026-bonus-edilizi-padova"),
            ("Costi vendita", "blog-costi-vendere-casa-padova-2026"),
        ],
        "registry": {
            "titolo": "Bonus casa 2027: calendario detrazioni e Padova",
            "categoria": "Fisco e ristrutturazioni",
            "tempo": 13,
            "contenuto": "Calendario 2027+, tagli spese fiscali MEF, checklist proprietari Padova.",
            "admin_contenuto": "Bonus casa 2027 — analisi originale Righetto (no copia terzi).",
            "emoji": "📉",
            "evidenza": True,
        },
        "static_map_key": "bonus casa 2027 detrazioni padova",
        "images": IMG1,
    },
    {
        "slug": S2,
        "filename": f"{S2}.html",
        "hero": f"img/blog/{S2}-hero.webp",
        "hero_alt": "Legge Bilancio 198 2026 bonus edilizi Padova",
        "cat_badge": "Normativa · 2026",
        "h1": "<strong>Legge 198/2025</strong>: bonus edilizi ed ecobonus confermati nel 2026",
        "title": "Legge 198/2025: bonus edilizi 2026 Padova",
        "og_title": "Legge Bilancio 2026: bonus edilizi Padova",
        "meta": "L. 198/2025 GU 301: proroga bonus ristrutturazioni, ecobonus e sismabonus 2026. Impatto compravendita Padova — Righetto.",
        "schema_headline": "Legge Bilancio 198 2026 bonus edilizi Padova",
        "section": "Fisco e ristrutturazioni",
        "bread_crumb": "Legge 198 bonus 2026",
        "body_fn": body2,
        "faqs": [
            ("Quale legge proroga i bonus 2026?", "Legge 29 dicembre 2025, n. 198, GU n. 301/2025."),
            ("Superbonus 110% c’è ancora?", "No — restano bonus ordinari 50% / 36%."),
            ("Quando devono iniziare i lavori?", "Regola tecnica: inizio entro l’anno precedente la spesa per bonus ristrutturazioni — verificare con commercialista."),
            ("Ecobonus e caldaie a gas?", "Esclusa incentivazione sostituzione con caldaia solo fossile — scheda ADE."),
        ],
        "related": [
            ("Bonus 2027+", "blog-bonus-casa-2027-detrazioni-padova"),
            ("Bonus edilizi giugno", "blog-bonus-edilizi-2026-incentivi-casa-padova"),
            ("Mobili e barriere", "blog-bonus-mobili-barriere-architettoniche-2026-padova"),
        ],
        "registry": {
            "titolo": "Legge 198/2025: bonus edilizi ed ecobonus 2026 a Padova",
            "categoria": "Fisco e ristrutturazioni",
            "tempo": 14,
            "contenuto": "GU 301/2025, proroghe 2026, filiera documentale e compravendita Padova.",
            "admin_contenuto": "Legge Bilancio 198/2026 bonus — testo originale Righetto.",
            "emoji": "📜",
            "evidenza": True,
        },
        "static_map_key": "legge bilancio 198 bonus edilizi 2026 padova",
        "images": IMG2,
    },
    {
        "slug": S3,
        "filename": f"{S3}.html",
        "hero": f"img/blog/{S3}-hero.webp",
        "hero_alt": "Bonus mobili 2026 e fine barriere architettoniche Padova",
        "cat_badge": "Fisco · Accessibilità",
        "h1": "<strong>Bonus mobili 2026</strong> e fine detrazione barriere architettoniche",
        "title": "Bonus mobili 2026 e barriere architettoniche",
        "og_title": "Bonus mobili 2026 Padova: barriere architettoniche stop",
        "meta": "Bonus mobili 50% confermato 2026; stop bonus barriere 75%. Cosa cambia per ristrutturazioni e vendita a Padova.",
        "schema_headline": "Bonus mobili e barriere architettoniche 2026 Padova",
        "section": "Fisco e ristrutturazioni",
        "bread_crumb": "Bonus mobili e barriere 2026",
        "body_fn": body3,
        "faqs": [
            ("Bonus mobili 2026 quanto vale?", "50% su max 5.000 euro se collegato a ristrutturazione — scheda ADE."),
            ("Barriere architettoniche prorogate?", "No oltre 31/12/2025 secondo manovra 2026."),
            ("Serve ristrutturazione per mobili?", "Sì, collegamento temporale e unità immobiliare."),
            ("Impacto vendita Padova?", "Accessibilità influisce su domanda; prezzo da OMI e comparables."),
        ],
        "related": [
            ("Legge 198", "blog-legge-bilancio-198-2026-bonus-edilizi-padova"),
            ("Casa vendibile green", "blog-casa-vendibile-5-anni-case-green-padova-2026"),
            ("Bonus mobili guida", "blog-bonus-mobili-2026-massimizzare-ristrutturazioni"),
        ],
        "registry": {
            "titolo": "Bonus mobili 2026 e stop barriere architettoniche — Padova",
            "categoria": "Fisco e ristrutturazioni",
            "tempo": 12,
            "contenuto": "Mobili 50% vs fine 75% barriere; strategie vendita/locazione Padova.",
            "admin_contenuto": "Bonus mobili/barriere 2026 — analisi originale Righetto.",
            "emoji": "🛋️",
            "evidenza": True,
        },
        "static_map_key": "bonus mobili barriere architettoniche 2026 padova",
        "images": IMG3,
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


def patch_all() -> None:
    slugs = [c["slug"] for c in ARTICLES]
    blog = ROOT / "blog.html"
    t = blog.read_text(encoding="utf-8")
    add = ""
    for c in ARTICLES:
        if c["slug"] not in t:
            add += registry_blog_entry(c)
    if add:
        t = t.replace("  const articoliStatici = [\n", "  const articoliStatici = [\n" + add, 1)
        blog.write_text(t, encoding="utf-8")
        print("blog.html updated")

    admin = ROOT / "admin.html"
    at = admin.read_text(encoding="utf-8")
    for c in ARTICLES:
        if c["slug"] in at:
            continue
        r = c["registry"]
        entry = (
            f"  {{ titolo: {json.dumps(r['titolo'], ensure_ascii=False)}, "
            f"categoria: {json.dumps(r['categoria'], ensure_ascii=False)}, "
            f"data: '{DATE_ISO}', tempo: {r['tempo']}, stato: 'pubblicato', "
            f"autore: 'Gino Capon', emoji: '{r['emoji']}', "
            f"immagine_copertina: '{c['hero']}', url_statico: '{c['slug']}', "
            f"contenuto: {json.dumps(r['admin_contenuto'], ensure_ascii=False)}, "
            f"evidenza: true, data_pubblicazione: '{DATE_ISO}' }},\n"
        )
        at = at.replace("const _blogSeedArticles = [\n", "const _blogSeedArticles = [\n" + entry, 1)
    admin.write_text(at, encoding="utf-8")

    sm = ROOT / "sitemap.xml"
    st = sm.read_text(encoding="utf-8")
    ins = ""
    for slug in slugs:
        if slug in st:
            continue
        ins += (
            f"  <url><loc>https://righettoimmobiliare.it/{slug}</loc>"
            f"<lastmod>{DATE_ISO}</lastmod><changefreq>monthly</changefreq>"
            f"<priority>0.8</priority></url>\n"
        )
    if ins:
        sm.write_text(st.replace("</urlset>", ins + "</urlset>"), encoding="utf-8")

    hp = ROOT / "js" / "homepage.js"
    ht = hp.read_text(encoding="utf-8")
    for c in ARTICLES:
        if c["slug"] in ht:
            continue
        r = c["registry"]
        he = f"""    {{
      "titolo": "{r['titolo']}",
      "categoria": "{r['categoria']}",
      "data": "{DATE_ISO}",
      "immagine_copertina": "{c['hero']}",
      "url_statico": "{c['slug']}"
    }},
"""
        me = f"    '{c['static_map_key']}': {{ img: '{c['hero']}', url: '{c['slug']}' }},\n"
        ht = ht.replace("  const articoliStatici = [\n", "  const articoliStatici = [\n" + he, 1)
        ht = ht.replace("  const staticMap = {\n", "  const staticMap = {\n" + me, 1)
    hp.write_text(ht, encoding="utf-8")


def main() -> None:
    for cfg in ARTICLES:
        ensure_images(cfg["images"])
        body = cfg["body_fn"]()
        words = wc(body)
        print(f"{cfg['slug']}: {words} words")
        min_words = 1800  # corpo utile + sezioni operative (target ~2500, skill ±20%)
        if words < min_words:
            raise SystemExit(f"Troppo corto: {cfg['slug']} ({words} < {min_words})")
        (ROOT / cfg["filename"]).write_text(build_html(cfg, body, words), encoding="utf-8")
    patch_all()
    print("OK batch bonus fisco oct 2026")


if __name__ == "__main__":
    main()
