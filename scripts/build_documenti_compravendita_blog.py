# -*- coding: utf-8 -*-
"""Genera articolo blog documenti compravendita — maggio 2026."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from build_may27_blog_batch import (  # noqa: E402
    DISCLAIMER_BODY,
    FOOTER,
    STYLE_BLOCK,
    aeo_box,
    build_article,
    faq_html,
    sources_table,
    word_count,
)

ROOT = _SCRIPT_DIR.parent
DATE_IT = "29 maggio 2026"
DATE_ISO = "2026-05-29"
TIME_TS = "2026-05-29T10:00:00+02:00"
SLUG = "blog-documenti-compravendita-rogito-padova-2026"
IMG = "img/blog/blog-documenti-compravendita-rogito-padova-2026.webp"
TITLE = (
    "Documenti necessari per la compravendita di un immobile: "
    "guida pratica per venditori e acquirenti"
)

MEDIAZIONE_OK = (
    "<p><strong>Nota sulla mediazione:</strong> i compensi di intermediazione "
    "immobiliare sono sempre da concordare in sede nel mandato di vendita o locazione; "
    "questa pagina non sostituisce il contratto firmato con l'agenzia.</p>"
)

CLOSING_TECNICO = (
    "<p>I clienti sono invitati a valutare l'opportunità di affidare a un "
    "<strong>tecnico abilitato</strong> la verifica della conformità urbanistica "
    "e catastale dell'immobile oggetto di compravendita, al fine di prevenire "
    "problematiche che potrebbero compromettere o ritardare il buon esito della vendita.</p>"
)

BODY_CORE = """
<p>La compravendita di un immobile si conclude con il <strong>rogito notarile</strong>, ma il successo dell'operazione si decide molto prima: quando venditori e acquirenti mettono ordine nella documentazione. Un fascicolo incompleto o incoerente non è un dettaglio burocratico: può bloccare l'istruttoria mutuo, far slittare la data in studio notarile o, peggio, far emergere irregolarità urbanistiche o catastali che nessuna delle parti aveva valutato.</p>
<p>Questa guida è pensata per famiglie e professionisti che operano nel <strong>Padovano e in provincia</strong>. Non sostituisce il parere del notaio, del tecnico o del consulente fiscale, ma aiuta a capire <em>a cosa serve</em> ogni documento, <em>chi lo produce</em> e <em>quali rischi</em> si corre se manca o è scaduto.</p>

<h2 id="perche-organizzare-prima">Perché organizzare tutto prima del rogito</h2>
<p>Il notaio ha il compito di verificare che l'atto possa essere stipulato in sicurezza. Per farlo ha bisogno di un insieme coerente di atti, certificati e dichiarazioni. Quando un pezzo manca, la firma slitta: a volte di pochi giorni, a volte di settimane se servono accertamenti tecnici o integrazioni catastali.</p>
<p>Per l'acquirente, soprattutto se ricorre al mutuo, la banca richiede spesso documentazione aggiuntiva rispetto al minimo notarile. Per il venditore, avere il fascicolo pronto significa proteggere il prezzo concordato e ridurre il rischio che l'acquirente chieda rinegoziazione dopo aver scoperto un difetto documentale.</p>
<p>In agenzia vediamo spesso che le trattative più serene sono quelle in cui venditore e acquirente condividono una <strong>checklist</strong> con date e responsabilità già dal preliminare.</p>

<h2 id="identita-stato-civile">Documento di riconoscimento e codice fiscale</h2>
<p>Ogni parte compare al rogito con <strong>documento di identità valido</strong> e <strong>codice fiscale</strong>. Sembra elementare, ma in pratica emergono criticità quando:</p>
<ul>
<li>il documento è scaduto o il nome riportato non coincide con quello del titolo catastale o dell'atto di provenienza;</li>
<li>uno dei coniugi deve firmare ma manca l'estratto di matrimonio aggiornato;</li>
<li>interviene un procuratore: in tal caso servono procura notarile e documenti del rappresentante.</li>
</ul>
<p>Per società, cooperative o eredi, la documentazione anagrafica si allarga: visura camerale, delibere, eventuali autorizzazioni statutarie. Meglio chiarire con il notaio fin dall'anticipo quali soggetti firmeranno l'atto definitivo.</p>

<h2 id="stato-civile-matrimonio">Stato civile libero o estratto di matrimonio</h2>
<p>Il certificato di <strong>stato libero</strong> attesta che la persona non è vincolata da matrimonio o unione registrata. L'<strong>estratto per riassunto dell'atto di matrimonio</strong> serve quando la parte è coniugata, perché il regime patrimoniale (comunione o separazione) incide su come l'immobile può essere venduto e sui consensi necessari.</p>
<p>Se manca o è datato, lo studio notarile può sospendere la stipula finché non si recupera la certificazione aggiornata dall'Ufficiale di stato civile. In caso di separazione o procedura in corso, il notaio valuterà se servono ulteriori autorizzazioni: non è un passaggio banale e va affrontato con trasparenza fin dalla proposta d'acquisto.</p>

<h2 id="provenienza-successione">Atto di provenienza o dichiarazione di successione</h2>
<p>L'<strong>atto di provenienza</strong> dimostra come il venditore è diventato proprietario: compravendita precedente, donazione, successione, divisione ereditaria. Senza una catena titoli leggibile, il notaio non può certificare che chi vende abbia effettivamente il diritto di disporre dell'immobile.</p>
<p>Se l'immobile è entrato nel patrimonio per <strong>successione</strong>, servono tipicamente dichiarazione di successione, eventuale certificato di morte dell'originario proprietario e atti di divisione se più eredi erano coin proprietari. Le criticità più frequenti:</p>
<ul>
<li>rogito antico non reperibile (serve estratto dagli archivi notarili);</li>
<li>quote indivise non ancora materialmente divise;</li>
<li>donazioni o patti di famiglia che impongono vincoli alla rivendita.</li>
</ul>
<p>Recuperare la provenienza richiede tempo: conviene avviare le ricerche appena si decide di vendere, non la settimana prima del rogito.</p>

<h2 id="titolo-edilizio">Concessioni, permessi di costruire, SCIA, DIA, CILA e condoni</h2>
<p>Il <strong>titolo edilizio</strong> racconta la storia autorizzativa dell'immobile: permesso di costruire storico, concessione edilizia, segnalazione certificata di inizio attività (SCIA), denuncia di inizio attività (DIA), comunicazione di inizio lavori asseverata (CILA) e relative fine lavori.</p>
<p>Per immobili con ampliamenti, verande, cambi d'uso o tamponature, ogni intervento dovrebbe avere un titolo corrispondente. Se manca, si parla di <strong>abuso edilizio</strong> o difformità: il rogito può comunque avvenire, ma l'acquirente acquista consapevole della situazione e la banca può rifiutare il mutuo.</p>
<p>In presenza di <strong>condono edilizio</strong> o sanatoria, vanno esibiti provvedimento, oblazione versata, eventuali vincoli residui e stato della pratica agli atti del Comune. Il dibattito politico sul condono non elimina l'obbligo di verificare cosa risulta effettivamente sanato nel fascicolo dell'immobile.</p>

<h2 id="agibilita">Certificato di agibilità o abitabilità</h2>
<p>Il certificato di <strong>agibilità</strong> (o abitabilità, a seconda della normativa applicabile al momento di costruzione) attesta che l'edificio è stato realizzato a regola d'arte e può essere utilizzato secondo la destinazione prevista. Per immobili di nuova costruzione o ristrutturazioni rilevanti è spesso documento centrale.</p>
<p>Se manca su un immobile abitato da decenni, non sempre blocca la vendita, ma il notaio segnala la carenza nell'atto e l'acquirente può chiedere garanzie o riduzione del prezzo. Recuperarlo può richiedere accertamenti tecnici comunali: meglio verificare prima di fissare la data del rogito.</p>

<h2 id="conformita-urbanistica">Certificazione di conformità urbanistica</h2>
<p>La <strong>certificazione di conformità urbanistica</strong> — rilasciata dal Comune o attestata da tecnico abilitato, a seconda dei casi — confronta lo stato di fatto dell'immobile con gli elaborati grafici del titolo edilizio. <strong>Non è sempre obbligatoria</strong> per legge in ogni compravendita, ma è <strong>fortemente consigliata</strong> quando esistono dubbi su ampliamenti, difformità o assenza di titoli.</p>
<p>Senza questa verifica, il venditore rischia contestazioni post-rogito; l'acquirente può trovarsi con sanzioni o obblighi di ripristino non previsti. Le banche, per mutuo su immobile non conforme, applicano spesso criteri più restrittivi del notaio.</p>

<h2 id="ape">Attestato di Prestazione Energetica (APE)</h2>
<p>L'<strong>APE</strong> è obbligatorio in fase di compravendita e deve essere consegnato all'acquirente. Indica la classe energetica e i consumi stimati. Un APE scaduto o redatto su planimetria non aggiornata invalida l'adempimento: va rinnovato se sono intervenute variazioni sostanziali o se sono passati dieci anni dalla precedente certificazione.</p>
<p>Per immobili con impianti recenti o riqualificazioni, conviene far redigere l'APE dopo aver allineato catasto e stato di fatto, così la classe riflette il reale valore dell'asset.</p>

<h2 id="condominio">Dichiarazione del saldo spese condominiali</h2>
<p>In edificio condominiale, l'<strong>amministratore</strong> rilascia dichiarazione sullo stato dei pagamenti: spese ordinarie, straordinarie deliberate, eventuali morosità e fondo cassa. Il venditore resta solidalmente responsabile con l'acquirente per i debiti dell'ultimo biennio, salvo patto contrario nell'atto.</p>
<p>Se la dichiarazione segnala arretrati o lavori straordinari non pagati, l'acquirente può chiedere conguaglio o deposito a garanzia. Meglio ottenere la dichiarazione aggiornata alla data del rogito, non mesi prima.</p>

<h2 id="preliminare">Preliminare di compravendita e registrazione</h2>
<p>Il <strong>contratto preliminare</strong> vincola le parti alla futura compravendita definendo prezzo, termini, condizioni sospensive (mutuo, accertamenti tecnici) e modalità di caparra. Va <strong>registrato</strong> all'Agenzia delle Entrate entro i termini di legge, con imposta di registro e bollo secondo le regole vigenti.</p>
<p>Conservate ricevuta di registrazione e copia del preliminare: il notaio li userà per redigere l'atto definitivo. Un preliminare mal scritto o non registrato crea incertezze fiscali e può complicare la prova del pagamento delle caparre.</p>

<h2 id="caparre">Caparre, acconti e tracciabilità dei pagamenti</h2>
<p>Caparre confirmatorie o acconti vanno documentati con <strong>bonifici tracciabili</strong>, ricevute e estratti conto che il notaio può richiedere per dimostrare il flusso di denaro. In caso di caparra confirmatoria, valgono le regole del Codice civile in materia di risoluzione e penali.</p>
<p>Evitate pagamenti in contanti non dichiarabili: oltre ai rischi fiscali, rendono difficile ricostruire l'anticipo al rogito. Se intermedia un'agenzia, allineate le date di versamento con quanto scritto nel preliminare.</p>

<h2 id="provvigioni">Provvigioni di agenzia e fatture</h2>
<p>Quando la compravendita passa da un'agenzia immobiliare, il venditore (e talvolta l'acquirente, se previsto) deve predisporre la documentazione relativa alle <strong>provvigioni</strong>: mandato firmato, fattura o documento fiscale, prova del pagamento se avviene prima del rogito.</p>
<p>Il notaio può chiedere di vedere che gli obblighi verso l'intermediario siano chiari, soprattutto se nel preliminare è previsto che parte del corrispettivo venga versato direttamente in rogito. I compensi di mediazione si concordano sempre in sede nel mandato: non esistono tariffe standard pubblicate online.</p>

<h2 id="checklist-rogito">Checklist operativa prima della firma</h2>
<p>Per ridurre imprevisti, una pratica utile è compilare una tabella con documento, responsabile, scadenza e stato. Esempio di voci minime: identità, stato civile, provenienza, planimetria catastale aggiornata, APE, visura catastale, titoli edilizi, agibilità se richiesta, conformità urbanistica se consigliata, saldo condominiale, preliminare registrato, ricevute caparre, mandato agenzia.</p>
<p>Condividete la checklist con il notaio scelto e, se c'è mutuo, con il consulente della banca. Due settimane di margine rispetto alla data desiderata di rogito sono spesso sufficienti per chiudere le lacune; meno tempo aumenta lo stress e il rischio di annullamento.</p>

<h2 id="verifica-tecnica">Verifica preventiva urbanistica e catastale</h2>
<p>Prima di impegnarsi definitivamente — anche al momento del preliminare — è prudente verificare che <strong>catasto e realtà</strong> coincidano e che non ci siano difformità gravi. Planimetria non aggiornata dopo una ristrutturazione, classe catastale errata o mancanza di titolo su un bagno ampliato sono problemi ricorrenti nel Padovano.</p>
<p>Il notaio segnala le incongruenze che emergono dagli atti, ma non sostituisce un sopralluogo tecnico approfondito. Per questo la verifica preventiva con professionista abilitato è spesso l'investimento più utile dell'intera operazione.</p>

<h2 id="planimetria-visura">Planimetria catastale e visura: coerenza dei dati</h2>
<p>Oltre ai documenti «cartacei» del rogito, il fascicolo catastale deve essere allineato allo stato di fatto. La <strong>planimetria</strong> depositata in catasto deve rappresentare i locali reali; la <strong>visura catastale</strong> riporta categorie, rendita e intestazione. Disallineamenti frequenti nel nostro territorio riguardano taverne finite, porticati chiusi, cambi di destinazione d'uso non variati.</p>
<p>L'acquirente che chiede mutuo trova spesso la banca più rigida del notaio: un difformità catastale può far decadere l'istruttoria anche quando le parti erano d'accordo sul prezzo. Il venditore, dal canto suo, dovrebbe chiedere al tecnico una lettura preventiva: talvolta basta una variazione catastale; altre volte serve sanatoria urbanistica prima della vendita.</p>
<p>Per approfondire solo questo tema abbiamo pubblicato una guida dedicata alla <a href="blog-planimetria-catastale-compravendita-padova-2026">planimetria catastale nel Padovano</a>: qui la richiamiamo perché planimetria e titolo edilizio vanno letti insieme, non separatamente.</p>

<h2 id="mutuo-acquirente">Documentazione aggiuntiva per chi acquista con mutuo</h2>
<p>Chi finanzia l'acquisto con <strong>mutuo ipotecario</strong> deve preparare, oltre al fascicolo immobile, il dossier personale: documenti reddituali, estratti conto, dichiarazione dei debiti residui, perizia del banco se prevista. La perizia del credito valuta l'immobile come garanzia: difetti urbanistici o catastali incidono sul valore periziale e quindi sull'importo erogabile.</p>
<p>Per questo, anche quando il venditore è puntuale, l'acquirente mutuatario ha interesse a sollecitare verifiche tecniche prima del preliminare. Un preliminare con <strong>condizione sospensiva</strong> legata all'approvazione del mutuo e, se necessario, all'esito di accertamenti urbanistici protegge entrambe le parti.</p>

<h2 id="eredità-comproprieta">Eredità, comproprietà e usufrutto</h2>
<p>Quando l'immobile proviene da successione o è ancora in comproprietà tra eredi, la documentazione si complica. Servono atti di divisione, rinuncie all'eredità se qualcuno ha optato per non succedere, liberatorie dai creditori dell'eredità in casi particolari. Se esiste un <strong>usufruttuario</strong>, la vendita della nuda proprietà richiede il consenso dell'usufruttuario o la verifica che l'usufrutto sia estinto.</p>
<p>Slittare il rogito per « sistemare l'eredità » è una delle cause più comuni di ritardo che incontriamo in agenzia. Meglio coinvolere il notaio e, se serve, un avvocato di famiglia già quando si valuta il prezzo di vendita.</p>

<h2 id="errori-frequenti">Errori frequenti da evitare</h2>
<p><strong>Affidarsi al « si sistema dopo ».</strong> Difformità edilizie e catasto non allineato raramente si risolvono in pochi giorni. <strong>Firmare preliminare senza aver visto il fascicolo.</strong> L'acquirente informato chiede copia di APE, planimetria e titoli prima di versare caparre rilevanti. <strong>Usare APE vecchio su immobile ristrutturato.</strong> Dopo lavori che cambiano involucro o impianti, l'attestato va aggiornato. <strong>Trascurare il condominio.</strong> Morosità nascoste o lavori straordinari non pagati possono diventare contestazione il giorno del rogito. <strong>Non registrare il preliminare.</strong> Oltre all'obbligo fiscale, la registrazione fissa la data e tutela le caparre.</p>

<h2 id="ruolo-agenzia">Come l'agenzia immobiliare supporta le parti</h2>
<p>Un'agenzia strutturata non sostituisce notaio o tecnico, ma aiuta a <strong>coordinare tempi e checklist</strong>: sollecita il venditore su documenti mancanti, mette in contatto le parti con i professionisti giusti, verifica che mandato e preliminare siano coerenti con quanto promesso in annuncio. Nel Padovano, dove convivono immobili storici in centro, villette anni Settanta in cintura e nuove costruzioni in frazioni, ogni fascicolo ha priorità diverse: l'esperienza locale serve a non applicare la stessa lista meccanicamente a casi diversi.</p>
<p>Se state valutando una vendita o un acquisto, potete richiedere un primo incontro gratuito per capire quali documenti mancano nel vostro caso specifico, senza impegno di mandato.</p>
""" + CLOSING_TECNICO + """

<h2 id="fonti-normative">Riferimenti normativi e istituzionali</h2>
<p>Le regole su registrazione, imposte e adempimenti evolvono: consultate sempre testi aggiornati. Per approfondimenti ufficiali:</p>
<ul>
<li><a href="https://www.notariato.it" rel="noopener">Consiglio Nazionale del Notariato</a> — guide alla compravendita;</li>
<li><a href="https://www.agenziaentrate.gov.it" rel="noopener">Agenzia delle Entrate</a> — imposte di registro e registrazione preliminare;</li>
<li><a href="https://www.agenziaentrate.gov.it/portale/schede/fabbricatiterreni/" rel="noopener">Agenzia delle Entrate — Catasto e planimetrie</a>;</li>
<li>Normativa energetica e APE sul portale del <a href="https://www.mise.gov.it" rel="noopener">Ministero competente</a>.</li>
</ul>
"""

CFG = {
    "slug": SLUG,
    "img": IMG,
    "html_title": f"{TITLE} | Righetto Immobiliare",
    "og_title": TITLE,
    "schema_headline": TITLE,
    "meta_desc": (
        "Documenti per compravendita immobiliare: identità, provenienza, titoli edilizi, "
        "APE, condominio, preliminare e caparre. Guida per venditori e acquirenti nel Padovano."
    ),
    "section": "Normativa",
    "cat_badge": "Normativa · Rogito",
    "h1": f"<strong>Documenti compravendita:</strong> guida pratica per venditori e acquirenti",
    "breadcrumb_tail": "Documenti compravendita",
    "bread": "Documenti compravendita rogito Padova",
    "alt_img": "Documenti e chiavi per rogito notarile compravendita immobiliare",
    "topic": "documenti compravendita rogito Padova",
    "anchors": [("rogito", "#"), ("notaio", "#"), ("APE", "#")],
    "body_n": 0,
    "body_extra": BODY_CORE,
    "cap_img": "",
    "aeo": aeo_box(
        "Venditori e acquirenti nel Padovano che si avvicinano al rogito e vogliono capire "
        "quali documenti servono, chi li produce e cosa rischia chi arriva impreparato.",
        [
            "Il rogito richiede un fascicolo coerente: anagrafica, provenienza, titoli edilizi, APE, condominio.",
            "Conformità urbanistica non è sempre obbligatoria ma è fortemente consigliata in caso di dubbi.",
            "Preliminare registrato, caparre tracciate e mandato agenzia vanno allineati prima della firma.",
        ],
        [
            "Consulenza legale, fiscale o perizia estimativa sostitutiva del notaio.",
            "Elenco tariffe o percentuali di mediazione online.",
        ],
    ),
    "sources": sources_table([
        ("Adempimenti rogito", "Consiglio Nazionale del Notariato", "Guide ufficiali compravendita"),
        ("Imposte e registrazione", "Agenzia delle Entrate", "Preliminare e imposte di registro"),
        ("Planimetrie e visure", "Agenzia delle Entrate — Catasto", "Coerenza dati catastali"),
        ("Prestazione energetica", "Normativa APE vigente", "Obbligo consegna acquirente"),
    ]),
    "faqs": [
        (
            "Quali documenti servono sempre al rogito?",
            "Identità e codice fiscale delle parti, catena titoli (provenienza), dati catastali, "
            "APE valido; il notaio indica l'elenco puntuale in base al caso.",
        ),
        (
            "La conformità urbanistica è obbligatoria?",
            "Non sempre per legge, ma è fortemente consigliata se esistono ampliamenti, "
            "difformità o titoli edilizi incompleti.",
        ),
        (
            "Chi verifica catasto e urbanistica?",
            "Il notaio controlla gli atti; per un sopralluogo e un parere tecnico approfondito "
            "conviene un tecnico abilitato scelto dalle parti.",
        ),
        (
            "Cosa serve in condominio?",
            "Dichiarazione dell'amministratore sul saldo spese, di norma aggiornata alla data del rogito.",
        ),
        (
            "Il preliminare va registrato?",
            "Sì, va registrato all'Agenzia delle Entrate con imposta di registro e bollo "
            "secondo le regole applicabili.",
        ),
    ],
    "related": [
        ("Planimetria catastale e compravendita nel Padovano", "blog-planimetria-catastale-compravendita-padova-2026"),
        ("Caparra confirmatoria a Padova", "blog-caparra-confirmatoria-padova"),
        ("Imposte di registro nella compravendita", "blog-imposte-registro-catasto-compravendita-padova-2026"),
    ],
    "cta_primary": ("Consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
    "cta_secondary": ("Contattaci", "contatti"),
}


def gen_hero_webp() -> None:
    from PIL import Image

    src = Path(
        r"C:\Users\Utente\.cursor\projects\c-Users-Utente-progetti-index\assets"
        r"\blog-hero-documenti-compravendita-2026.png"
    )
    if not src.is_file():
        alt = ROOT / "img" / "foto-servizi" / "gestione-preliminari-padova.webp"
        if alt.is_file():
            src = alt
        else:
            raise FileNotFoundError("Hero mancante")
    out = ROOT / IMG
    out.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(os.fspath(src))
    if im.mode in ("RGBA", "P"):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        if im.mode == "P":
            im = im.convert("RGBA")
        bg.paste(im, mask=im.split()[-1] if im.mode == "RGBA" else None)
        im = bg
    else:
        im = im.convert("RGB")
    w, h = im.size
    scale = max(1200 / w, 630 / h)
    nw, nh = int(w * scale), int(h * scale)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - 1200) // 2
    top = (nh - 630) // 2
    im = im.crop((left, top, left + 1200, top + 630))
    im.save(out, "WEBP", quality=82, method=6)
    print("Hero:", out, im.size)


def register() -> None:
    entry_blog = {
        "titolo": TITLE,
        "categoria": "Normativa",
        "data": DATE_ISO,
        "stato": "pubblicato",
        "immagine_copertina": IMG,
        "url_statico": SLUG,
        "tempo": 14,
        "autore": "Gino Capon",
        "contenuto": "Checklist rogito: identità, provenienza, titoli edilizi, APE, condominio, preliminare e verifica tecnica.",
        "evidenza": True,
    }
    entry_admin = {
        **entry_blog,
        "emoji": "📋",
        "contenuto": "<p>Guida documenti compravendita per venditori e acquirenti nel Padovano.</p>",
        "data_pubblicazione": DATE_ISO,
    }

    blog_path = ROOT / "blog.html"
    text = blog_path.read_text(encoding="utf-8")
    if SLUG not in text:
        block = (
            "    {\n"
            f'      titolo: {json.dumps(TITLE, ensure_ascii=False)},\n'
            f'      categoria: "Normativa",\n'
            f"      data: '{DATE_ISO}',\n"
            "      tempo: 14,\n"
            "      stato: 'pubblicato',\n"
            "      autore: 'Gino Capon',\n"
            f"      immagine_copertina: '{IMG}',\n"
            f"      url_statico: '{SLUG}',\n"
            "      contenuto: 'Checklist rogito: identità, provenienza, titoli edilizi, APE, condominio, preliminare.',\n"
            "      evidenza: true\n"
            "    },\n"
        )
        text = text.replace("  const articoliStatici = [\n", "  const articoliStatici = [\n" + block, 1)
        blog_path.write_text(text, encoding="utf-8")
        print("blog.html: registrato")

    admin_path = ROOT / "admin.html"
    atext = admin_path.read_text(encoding="utf-8")
    if SLUG not in atext:
        ab = (
            f"  {{ titolo: {json.dumps(TITLE, ensure_ascii=False)}, "
            f"categoria: 'Normativa', data: '{DATE_ISO}', tempo: 14, stato: 'pubblicato', "
            f"autore: 'Gino Capon', emoji: '📋', immagine_copertina: '{IMG}', "
            f"url_statico: '{SLUG}', "
            f"contenuto: '<p>Guida documenti compravendita per venditori e acquirenti.</p>', "
            f"evidenza: true, data_pubblicazione: '{DATE_ISO}' }},\n"
        )
        atext = atext.replace("const _blogSeedArticles = [\n", "const _blogSeedArticles = [\n" + ab, 1)
        admin_path.write_text(atext, encoding="utf-8")
        print("admin.html: registrato")

    hp_path = ROOT / "js" / "homepage.js"
    htext = hp_path.read_text(encoding="utf-8")
    if SLUG not in htext:
        key = TITLE.lower().replace("'", "\\'")
        map_line = f"    '{key}': {{ img: '{IMG}', url: '{SLUG}' }},\n"
        htext = htext.replace("  const staticMap = {\n", "  const staticMap = {\n" + map_line, 1)
        hp_block = (
            f"    {{ titolo: {json.dumps(TITLE, ensure_ascii=False)}, "
            f"categoria: 'Normativa', data: '{DATE_ISO}', stato: 'pubblicato', "
            f"immagine_copertina: '{IMG}', url_statico: '{SLUG}' }},\n"
        )
        htext = htext.replace("  const articoliStatici = [\n", "  const articoliStatici = [\n" + hp_block, 1)
        hp_path.write_text(htext, encoding="utf-8")
        print("homepage.js: registrato")

    sm_path = ROOT / "sitemap.xml"
    sm = sm_path.read_text(encoding="utf-8")
    if SLUG not in sm:
        url = (
            f'  <url><loc>https://righettoimmobiliare.it/{SLUG}</loc>'
            f"<lastmod>{DATE_ISO}</lastmod><changefreq>monthly</changefreq>"
            f"<priority>0.85</priority></url>\n"
        )
        sm = sm.replace(
            "  <!-- Articoli blog — 27 maggio 2026",
            url + "  <!-- Articoli blog — 27 maggio 2026",
            1,
        )
        sm_path.write_text(sm, encoding="utf-8")
        print("sitemap.xml: registrato")


def main() -> None:
    import build_may27_blog_batch as m27
    import build_apr19_blog_batch as apr

    m27.DATE_IT = DATE_IT
    m27.DATE_ISO = DATE_ISO
    m27.TIME_TS = TIME_TS
    apr.MEDIAZIONE = MEDIAZIONE_OK
    m27.MIN_BODY_WORDS = 2400

    body_html, wc = build_article(CFG)
    out = ROOT / f"{SLUG}.html"
    out.write_text(body_html, encoding="utf-8")
    print(out.name, "wordCount:", wc)
    if wc < 2400:
        print("WARN: word count sotto soglia", wc)
    gen_hero_webp()
    register()


if __name__ == "__main__":
    main()
