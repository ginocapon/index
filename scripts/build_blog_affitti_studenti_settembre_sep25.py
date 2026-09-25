# -*- coding: utf-8 -*-
"""Pubblica eq-sep25-001 — affitti studenti settembre owner Padova 2026."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "blog-affitti-studenti-settembre-padova-proprietario-2026"
FILE = ROOT / f"{SLUG}.html"
DATE_ISO = "2026-09-25"
DATE_IT = "25 settembre 2026"
HERO = f"img/blog/{SLUG}-hero.webp"
MIN_WORDS = 2500

STYLE_HEAD = (ROOT / "blog-gestione-locazione-delegata-padova-2026.html").read_text(encoding="utf-8")
style_m = re.search(r"<style>.*?</style>", STYLE_HEAD, re.S)
STYLE = style_m.group(0) if style_m else ""

PARAS = [
    "Ogni settembre a Padova migliaia di studenti fuori sede cercano stanza o monolocale: per chi affitta, è il momento in cui annunci, visite e contratti si concentrano in poche settimane. Non è solo «alta stagione»: cambiano tempi di risposta, tipo di inquilino richiesto, clausole del contratto e rischio di scelte affrettate. Questa guida è scritta per il proprietario che vuole orientarsi senza farsi sorprendere dal picco autunnale.",
    "Distinzione editoriale: i fatti su obblighi locativi (registrazione entro 30 giorni presso l'Agenzia delle Entrate, APE obbligatorio, artt. 1575-1585 c.c.) sono normativi. I riferimenti al mercato studentesco si appoggiano a osservazioni FIMAA Veneto e al flusso universitario documentato dall'Università di Padova — senza inventare canoni €/mq. Le analisi su calendario e strategia annuncio sono esperienza operativa Righetto sul territorio dal 2000.",
    "Settembre non è il momento ideale per «scoprire» che manca l'APE o che il regolamento di condominio vieta certi affitti brevi: a fine agosto le richieste arrivano a raffica e chi è pronto chiude prima. Il proprietario preparato ha invece lavorato tra maggio e luglio su documenti, foto e fascia di canone coerente con OMI locazioni e comparabili reali.",
    "Il mercato studentesco padovano convive con domanda di famiglie e lavoratori: non tutto è «zona universitaria». Arcella, Porta Romana, Via VIII Febbraio, Savonarola e Portello restano cluster ad alta domanda studentesca, ma anche tratti di Via Venezia e zone semicentrali ricevono flussi quando i listini centrali si stringono. Consultate la scheda <a href=\"zona-universitaria-padova\">zona universitaria Padova</a> per il contesto locale.",
    "La domanda di settembre include matricole, trasferimenti da altre città, studenti magistrali e dottorandi, oltre a tirocinanti e lavoratori giovani. Ogni profilo ha esigenze diverse su durata, garanzie e convivenza. Un trilocale per tre co-inquilini non si gestisce come un bilocale per coppia: il contratto e la selezione devono essere coerenti con l'uso reale dell'immobile.",
    "Chi affitta per la prima volta spesso sottovaluta il turnover: l'anno accademico non coincide sempre con il calendario solare. Preavvisi a giugno, uscite a luglio-agosto e rientri a settembre creano finestre strette per manutenzione, pulizie e nuove visite. Avere un piano operativo ( anche solo una checklist ) riduce vuoti locativi.",
    "Il canone non va copiato da portali generici. La fascia corretta nasce da OMI locazioni per zona omogenea, da annunci comparabili con metratura e stato simili, e da sopralluogo. Righetto offre <a href=\"landing-valutazione\">valutazione locativa gratuita</a> con riferimento al mercato padovano — senza pubblicare listini o percentuali di mediazione online.",
    "Per locazioni a studenti universitari fuori sede, il contratto transitorio (6-36 mesi) è spesso la soluzione più aderente, quando ricorrono i requisiti di legge. In alternativa il 3+2 a canone concordato con cedolare secca al 10% sul canone concordato è molto diffuso nel Veneto per equilibrio tra tutela e fiscalità. Il 4+4 libero resta possibile ma va calibrato su garanzie e profilo inquilino.",
    "La registrazione del contratto entro 30 giorni dalla stipula è obbligatoria: senza registrazione, il rapporto fiscale e le detrazioni dell'inquilino non sono regolari. Il locatore deve conservare ricevute, comunicare dati catastali corretti e rispettare gli obblighi di consegna (APE, conformità impianti). Per il quadro generale: <a href=\"blog-affittare-casa-padova-proprietario-2026\">affittare casa Padova proprietario</a>.",
    "Settembre è anche il mese delle trattative rapide: studenti e genitori prenotano visite in serie. Rispondere in giornata lavorativa fa differenza. Annunci con foto verticali chiare, planimetria leggibile e indicazione precisa di spese condominiali e regole casa ( animali, fumo, visita ) filtrano contatti incoerenti e proteggono il vostro tempo.",
    "Attenzione alle garanzie: fideiussione bancaria, deposito cauzionale, garante. Con co-inquilini, verificate solidità del gruppo e clausole di solidarietà. Non accontentatevi di promesse verbali: tutto ciò che conta va nel contratto registrato. Per morosità e iter successivi, valutate <a href=\"servizio-gestione\">servizio gestione</a> o <a href=\"blog-gestione-locazione-delegata-padova-2026\">gestione locazione delegata</a>.",
    "L'APE deve essere valido e consegnato: senza certificazione energetica non si stipula correttamente un contratto abitativo. Verificate anche conformità urbanistica e catastale: discrepanze emergono spesso in fase di due diligence del futuro inquilino o dell'agenzia. Meglio risolvere prima del picco settembrino.",
    "Il condominio può limitare orari di trasloco, uso ascensori o modifiche interne. Leggete regolamento e ultimi verbali: lavori straordinari in corso impattano su attrattività dell'annuncio. Se l'immobile è arredato, inventario fotografico datato protegge in consegna e riconsegna chiavi.",
    "Affittare a studenti non significa accettare qualsiasi condizione: tutela del patrimonio resta prioritaria. Visite accompagnate, verifica documento identità, certificazione di iscrizione universitaria quando prevista dal contratto transitorio, e chiarezza su manutenzione ordinaria ( rubinetti, lampadine ) vs straordinaria.",
    "Se gestite da soli, preparate un file con contatti idraulico/elettricista, numeri utenze e regole per emergenze. Se delegate, un unico referente agenzia evita telefonate notturne al proprietario. Righetto integra <a href=\"servizio-locazioni\">servizio locazioni</a> ( ingresso inquilino ) e gestione continuativa — compenso concordato in sede.",
    "Errore frequente: alzare il canone solo perché «a settembre pagano di più». OMI e concordato hanno vincoli; chiedere fuori mercato allunga i giorni vuoti proprio quando vorreste chiudere in fretta. Meglio prezzo credibile e immobile impeccabile che prezzo aspirazionale e foto mediocri.",
    "Secondo errore: posticipare manutenzione estiva. Caldaia, climatizzazione, infissi e serrature vanno controllati a luglio, non il 28 agosto. Terzo errore: annuncio generico «stanza in Padova » senza metrofermata, università di riferimento o regole convivenza.",
    "Quarto errore: dimenticare fiscalità. Cedolare secca, IRPEF, concordato: scelta va fatta con commercialista prima del rinnovo massivo di settembre. Righetto orienta sugli adempimenti locativi ma non sostituisce consulenza fiscale personalizzata.",
    "Quinto errore: non prevedere uscita a giugno. Studenti possono lasciare l'alloggio a fine esame; contratto e preavviso devono essere allineati per ridurre vuoti estivi. Valutate se conviene targetizzare anche studenti magistrali con permanenza pluriennale.",
    "Dal punto di vista dell'«alleato» proprietario, Righetto non spinge incarichi con urgenza artificiale: accompagna con dati, comparabili e chiarezza contrattuale. 127 recensioni Google con media 4,9/5 e presenza dal 2000 a Limena ( Via Roma 96 ) sono riferimenti verificabili — non promesse di rendimento garantito.",
    "Per immobili fuori Padova città ma collegati all'università ( Limena, Rubano, Cadoneghe, Vigonza ) la domanda studentesca dipende da bus e treni: in annuncio indicate tempi reali verso Palazzo del Bo o poli didattici. FIMAA segnala spesso annunci in appartamento attivi fino a ottobre anche dopo il picco di settembre.",
    "Studentati e nuovi posti letto ESU modificano marginalmente la pressione sul mercato privato: ogni migliaio di posti pubblici aiuta ma non elimina picchi in zone centrali. Il proprietario privato resta rilevante per stanze singole, bilocali e trilocali condivisi.",
    "Checklist pre-settembre in sintesi: APE e documenti ok; immobile pulito e fotografato; canone calibrato; contratto scelto con professionista; regole casa scritte; calendario visite; piano manutenzione; decisione gestione diretta vs delegata.",
    "Durante settembre: rispondete rapidamente; proponete slot visite a blocchi; verificate identità e requisiti transitorio; registrate contratto subito dopo firma; consegnate chiavi con verbale e inventario. Dopo locazione: monitorate primi canoni e segnalate anomalie subito.",
    "Se l'immobile resta vuoto a fine settembre, non è necessariamente «fallimento»: valutate con agenzia se prezzo, foto o tipologia contratto vanno rivisti. A volte conviene attendere ottobre per profili lavoratori o studenti tardivi, senza abbassare indiscriminatamente il canone.",
    "Collegamento utile con guide esistenti: <a href=\"blog-affitto-studenti-padova\">affitto studenti Padova</a> ( quadro generale ), <a href=\"blog-affitti-padova-canoni-2026\">affitti Padova canoni 2026</a>, <a href=\"blog-contratto-affitto-padova\">contratto affitto Padova</a>, <a href=\"blog-rendimento-affitto-padova\">rendimento affitto</a>, <a href=\"proprietario-immobile\">hub proprietari</a>.",
    "Per chi deve scegliere se locare a studenti o famiglia, <a href=\"blog-vendere-o-affittare-padova-2026\">vendere o affittare</a> aiuta sul piano strategico. Per costi e adempimenti generali, <a href=\"blog-costi-vendere-casa-padova-2026\">costi vendere casa</a> resta utile se state valutando alternativa vendita.",
    "L'Università di Padova pubblica calendari accademici e date utili per orientare domanda: incrociate sempre con fonti ufficiali quando pianificate disponibilità. ISTAT e Banca d'Italia offrono contesto macro — non sostituiscono comparabili di zona.",
    "Domande frequenti in agenzia a settembre: « Posso affittare per nove mesi? » ( dipende da contratto ), « Serve garante? » ( consigliato con studenti ), « Posso chiedere due mensilità cauzione? » ( limiti di legge ), « Quando incasso? » ( come da contratto ). Arrivare preparati velocizza.",
    "Righetto può supportarvi con marketing immobile, selezione conduttori, redazione contratto, registrazione ADE e, se volete, gestione post-locazione. Mediazione e gestione: compenso da concordare in sede nel mandato — mai percentuali pubblicate sul sito.",
    "Infine, ricordate che locazione studentesca è servizio pubblico indiretto: qualità dell'alloggio incide su studio e permanenza in città. Manutenzione seria, rispetto privacy e contratti chiari costruiscono reputazione del proprietario e riducono conflitti.",
    "Se avete ereditato un appartamento in zona universitaria e non conoscete il mercato, partite da consulenza: <a href=\"landing-consulenza-immobiliare-gratuita\">consulenza immobiliare gratuita</a> o telefono 049.8843484. Meglio un piano prima del 1° settembre che correzioni affrettate a metà mese.",
    "Per immobili già locati con uscita a luglio, settembre è fase di rientro: pulizie, piccola manutenzione, aggiornamento foto e re-pubblicazione annuncio almeno 15-20 giorni prima dell'ondata richieste. Chi riparte tardi compete con migliaia di annunci simili.",
    "WhatsApp e telefono restano canali preferiti per studenti e genitori: numero visibile e risposta cordiale professionalizzano il primo contatto. Evitate promesse non scritte su « incluso tutto » se condominio o utenze sono esclusi.",
    "In sintesi operativa: settembre premia chi ha preparato prima, comunica chiaro, rispetta norme e tratta il locare come attività con regole — non come improvvisazione estiva. Righetto resta un alleato sul territorio padovano per chi affitta con consapevolezza.",
    "La comunicazione con i coinquilini va regolata prima della firma: turni cucina, pulizie scale interne, ospiti e orari silenzio. Un regolamento interno firmato insieme al contratto di locazione riduce attriti nei mesi successivi, soprattutto in trilocali e quadrilocali studenteschi.",
    "Per immobili parzialmente arredati, specificate nel contratto cosa resta in locazione ( elettrodomestici, mobili ) e stato d'uso accettato. Foto datate al check-in sono prova utile in caso di contestazione su danni o mancata manutenzione ordinaria da parte del conduttore.",
    "Se ricevete richieste da genitori che pagano il canone, chiarite titolarità del contratto, deleghe di pagamento e recapiti per solleciti. La solidarietà tra co-inquilini va resa esplicita quando più studenti firmano lo stesso rapporto locativo.",
    "Padova ospita anche studenti internazionali: verificate documenti, permessi di soggiorno se necessari e canali di comunicazione. L'agenzia può supportare su Questura e registrazione contratto, ma ogni caso va valutato singolarmente con attenzione alla privacy.",
    "Non dimenticate assicurazione immobile e, se prevista, polizza affitto: chiedete al broker cosa copre danni da terzi e vacanze locative. Non sostituisce deposito cauzionale ma completa la tutela patrimoniale.",
    "Infine, dopo settembre, pianificate già revisione canone al rinnovo ( rivalutazione ISTAT se prevista ) e sopralluogo semestrale. Proprietario attento mantiene valore dell'asset e relazione professionale con inquilini seri.",
    "Se compare clausola di recesso anticipato, verificatela con legale: studenti possono cambiare città per tesi o stage. Contratto equilibrato protegge entrambe le parti e evita contenziosi quando la vacanza locativa coincide con nuovo anno accademico.",
    "Per chi possiede monolocale o bilocale, valutate se locare intero appartamento a coppia studentesca o singolo professionista: meno turnover, diverso profilo rischio. La scelta influisce su durata contrattuale, importo cauzione e manutenzione programmata nel tempo.",
    "Conservate copia digitale di contratto registrato, ricevute ADE, inventario e fotografie consegna: in caso di passaggio generazionale del patrimonio o vendita futura, dossier locativo ordinato accelera due diligence e aumenta fiducia di acquirenti o eredi.",
    "Un ultimo promemoria: aggiornate dati catastali e planimetria se avete fatto lavori — studenti e agenzie competenti lo chiedono sempre prima di firmare.",
]

FAQ = [
    ("Settembre è sempre il mese migliore per affittare a studenti a Padova?", "Settembre è il picco di domanda per l'anno accademico, ma l'offerta preparata tra maggio e luglio ottiene spesso risultati migliori. Da fine agosto le richieste sono molte ma anche la concorrenza tra annunci è alta."),
    ("Quale contratto usare per studenti universitari fuori sede?", "Spesso il transitorio per studenti (6-36 mesi) se ricorrono i requisiti. Alternativa frequente: 3+2 a canone concordato con cedolare secca al 10%. Scelta va calibrata con professionista e tipologia immobile."),
    ("Devo registrare il contratto anche se affitto a studenti?", "Sì: registrazione entro 30 giorni presso l'Agenzia delle Entrate. Obbligatorio per validità fiscale e per detrazioni dell'inquilino."),
    ("Posso fissare il canone « di mercato » copiando annunci online?", "Meglio usare OMI locazioni ADE, comparabili simili e sopralluogo. Numeri generici online spesso non riflettono stato, piano e microzona del vostro immobile."),
    ("Conviene gestire da soli o delegare a settembre?", "Se avete tempo locale e esperienza, potete gestire. Se lavorate lontano, avete più immobili o volete filtrare visite e contratti in settimana intensa, delega a agenzia riduce rischi operativi."),
    ("Cosa fa Righetto per proprietari che affittano a studenti?", "Locazione (annuncio, selezione, contratto, ADE), opzionale gestione continuativa, valutazione canone. Compenso concordato in sede — contatti 049.8843484 o landing valutazione."),
]

SVG1 = """<figure class="chart-wrap" aria-label="Calendario proprietario affitti studenti">
<svg viewBox="0 0 580 260" width="100%" height="260" role="img">
<title>Calendario affitto studenti Padova — azioni proprietario</title>
<text x="290" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Anno accademico — finestre operative</text>
<rect x="40" y="50" width="100" height="40" rx="8" fill="#3A5F8C"/><text x="90" y="74" text-anchor="middle" font-size="8" fill="#fff">Mag–Lug</text>
<text x="90" y="105" text-anchor="middle" font-size="7" fill="#6B7A8D">Prep. docs/foto</text>
<rect x="160" y="50" width="100" height="40" rx="8" fill="#FF6B35"/><text x="210" y="74" text-anchor="middle" font-size="8" fill="#152435">Ago</text>
<text x="210" y="105" text-anchor="middle" font-size="7" fill="#6B7A8D">Annuncio live</text>
<rect x="280" y="50" width="100" height="40" rx="8" fill="#2C4A6E"/><text x="330" y="74" text-anchor="middle" font-size="8" fill="#fff">Set</text>
<text x="330" y="105" text-anchor="middle" font-size="7" fill="#6B7A8D">Picco visite</text>
<rect x="400" y="50" width="100" height="40" rx="8" fill="#3A5F8C"/><text x="450" y="74" text-anchor="middle" font-size="8" fill="#fff">Ott</text>
<text x="450" y="105" text-anchor="middle" font-size="7" fill="#6B7A8D">Rientri tardivi</text>
<text x="290" y="160" text-anchor="middle" font-size="9" fill="#6B7A8D">Giugno: preavvisi e manutenzione estiva</text>
<text x="290" y="210" text-anchor="middle" font-size="8" fill="#6B7A8D">Schema qualitativo — non sostituisce consulenza personalizzata</text>
</svg>
<figcaption>Calendario operativo per proprietari: preparazione prima del picco di settembre.</figcaption>
</figure>"""

SVG2 = """<figure class="chart-wrap" aria-label="Domanda studentesca per area Padova">
<svg viewBox="0 0 520 240" width="100%" height="240" role="img">
<title>Domanda locazioni studenti per area Padova — qualitativo</title>
<text x="260" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Domanda studentesca per area (qualitativa)</text>
<rect x="40" y="55" width="90" height="18" fill="#2C4A6E"/><text x="140" y="68" font-size="8" fill="#152435">Zona universitaria / Portello</text>
<rect x="40" y="85" width="75" height="18" fill="#3A5F8C"/><text x="140" y="98" font-size="8" fill="#152435">Arcella / Via Venezia</text>
<rect x="40" y="115" width="55" height="18" fill="#FF6B35"/><text x="140" y="128" font-size="8" fill="#152435">Semicentro ben servito</text>
<rect x="40" y="145" width="40" height="18" fill="#6B7A8D"/><text x="140" y="158" font-size="8" fill="#152435">Cintura (bus/treno)</text>
<text x="260" y="200" text-anchor="middle" font-size="8" fill="#6B7A8D">Lunghezza barre = intensità relativa domanda autunno, non prezzi</text>
</svg>
<figcaption>Confronto qualitativo delle aree più richieste da studenti — verificare sempre comparabili OMI e stato immobile.</figcaption>
</figure>"""

TABLE1 = """<table>
<thead><tr><th>Mese</th><th>Azione proprietario</th><th>Rischio se saltato</th></tr></thead>
<tbody>
<tr><td>Maggio–luglio</td><td>Documenti, APE, foto, canone OMI/comparabili</td><td>Annuncio incompleto o non pubblicabile</td></tr>
<tr><td>Agosto</td><td>Pubblicazione, risposta rapida, slot visite</td><td>Perdita lead verso concorrenti pronti</td></tr>
<tr><td>Settembre</td><td>Contratto, registrazione ADE, verbale consegna</td><td>Vuoti locativi o contratti affrettati</td></tr>
<tr><td>Ottobre</td><td>Follow-up tardivi, manutenzione post-traslato</td><td>Recensioni negative e danni non documentati</td></tr>
</tbody>
</table>"""

TABLE2 = """<table>
<thead><tr><th>Contratto</th><th>Quando considerarlo (studenti)</th><th>Nota</th></tr></thead>
<tbody>
<tr><td>Transitorio studenti</td><td>Fuori sede, durata 6-36 mesi, requisiti ok</td><td>Verificare legge e documentazione iscrizione</td></tr>
<tr><td>3+2 concordato</td><td>Canone calmierato, cedolare 10% spesso usata</td><td>Accordi territoriali ADE</td></tr>
<tr><td>4+4 libero</td><td>Co-inquilini stabili, garanzie solide</td><td>Canone non vincolato a tabella concordato</td></tr>
</tbody>
</table>"""


def word_count(html: str) -> int:
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text.split())


def build_body() -> str:
    chunks = [
        '<div class="aeo-box"><h2>In sintesi</h2><p>A <strong>settembre 2026</strong> a Padova la domanda di <strong>affitti per studenti</strong> è al massimo annuale: chi affitta deve avere documenti, APE, contratto e canone già allineati a <strong>OMI locazioni</strong>. Righetto supporta proprietari con <a href="servizio-locazioni">locazione</a>, <a href="servizio-gestione">gestione</a> e <a href="landing-valutazione">valutazione gratuita</a> — compenso concordato in sede. Approfondimento generale: <a href="blog-affitto-studenti-padova">affitto studenti Padova</a>.</p></div>',
        '<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>',
        '<li><a href="#perche-settembre">Perché settembre cambia tutto</a></li>',
        '<li><a href="#calendario">Calendario maggio–ottobre</a></li>',
        '<li><a href="#canone">Canone e OMI</a></li>',
        '<li><a href="#contratti">Contratti per studenti</a></li>',
        '<li><a href="#zone">Zone e domanda</a></li>',
        '<li><a href="#annuncio">Annuncio e visite</a></li>',
        '<li><a href="#documenti">Documenti e APE</a></li>',
        '<li><a href="#gestione">Diretta vs agenzia</a></li>',
        '<li><a href="#errori">Errori frequenti</a></li>',
        '<li><a href="#righetto">Cosa può fare Righetto</a></li>',
        "</ol></nav>",
        '<div class="kpi-strip" aria-label="Contesto Righetto"><div><strong>2000</strong><span>Dal</span></div><div><strong>101</strong><span>Comuni</span></div><div><strong>4,9/5</strong><span>127 recensioni</span></div><div><strong>30 gg</strong><span>Registraz. ADE</span></div></div>',
        '<div class="righetto-sol"><h2>Cosa può fare Righetto</h2><p><strong>Il quesito:</strong> Devo affittare a studenti a settembre — come non perdere tempo e soldi?</p><ul><li><a href="servizio-locazioni">Servizio locazioni</a> — Annuncio, selezione, contratto, ADE</li><li><a href="servizio-gestione">Servizio gestione</a> — Incassi, manutenzione, morosità</li><li><a href="landing-valutazione">Valutazione gratuita</a> — Canone e comparabili</li><li><a href="proprietario-immobile">Hub proprietari</a> — Percorsi vendita e locazione</li></ul></div>',
        '<h2 id="perche-settembre">Perché settembre cambia tutto per chi affitta</h2>',
    ]
    for i, p in enumerate(PARAS):
        if i == 6:
            chunks.append('<h2 id="canone">Canone: OMI e comparabili, non numeri copiati</h2>')
        if i == 7:
            chunks.append('<h2 id="contratti">Contratti: transitorio, concordato, 4+4</h2>')
        if i == 3:
            chunks.append('<h2 id="zone">Zone universitarie e cintura</h2>')
        if i == 9:
            chunks.append('<h2 id="annuncio">Annuncio, foto e visite a settembre</h2>')
        if i == 11:
            chunks.append('<h2 id="documenti">Documenti, APE e condominio</h2>')
        if i == 14:
            chunks.append('<h2 id="gestione">Gestione diretta o delegata</h2>')
        if i == 16:
            chunks.append('<h2 id="errori">Cinque errori da evitare a settembre</h2>')
        if i == 26:
            chunks.append('<h2 id="calendario">Calendario operativo maggio–ottobre</h2>')
            chunks.append(SVG1)
            chunks.append(TABLE1)
        if i == 8:
            chunks.append(
                f'<figure class="blog-fig rig-ai-photo-wrap"><img src="img/blog/{SLUG}-contratto.webp" alt="Contratto affitto studenti Padova — registrazione ADE proprietario" width="1900" height="900" loading="lazy" data-ai-generated="true"><span class="rig-ai-photo-watermark" aria-hidden="true">FOTO AI</span><figcaption class="rig-photo-caption">Immagine editoriale elaborata digitalmente (anche con intelligenza artificiale): illustrazione a scopo informativo.</figcaption></figure>'
            )
        if i == 12:
            chunks.append(
                f'<figure class="blog-fig rig-ai-photo-wrap"><img src="img/blog/{SLUG}-calendario.webp" alt="Calendario affitto studenti settembre Padova — preparazione proprietario" width="1900" height="900" loading="lazy" data-ai-generated="true"><span class="rig-ai-photo-watermark" aria-hidden="true">FOTO AI</span><figcaption class="rig-photo-caption">Immagine editoriale elaborata digitalmente (anche con intelligenza artificiale).</figcaption></figure>'
            )
        if i == 4:
            chunks.append(
                f'<figure class="blog-fig rig-ai-photo-wrap"><img src="img/blog/{SLUG}-zona.webp" alt="Zona universitaria Padova — domanda affitti studenti settembre" width="1900" height="900" loading="lazy" data-ai-generated="true"><span class="rig-ai-photo-watermark" aria-hidden="true">FOTO AI</span><figcaption class="rig-photo-caption">Immagine editoriale elaborata digitalmente (anche con intelligenza artificiale).</figcaption></figure>'
            )
        chunks.append(f"<p>{p}</p>")
    chunks.append(TABLE2)
    chunks.append(SVG2)
    chunks.append('<h2 id="righetto">Prossimi passi</h2>')
    chunks.append(
        '<div class="cta-row"><a class="cta-deep" href="servizio-locazioni">Servizio locazioni</a><a class="cta-deep-outline" href="landing-valutazione">Valutazione gratuita</a></div>'
    )
    chunks.append(
        f'<p>Gruppo Immobiliare Righetto — Limena e Padova dal 2000. <strong>Ultimo aggiornamento:</strong> {DATE_IT}. Fonti: ADE OMI locazioni, registro contratti locazione, Codice Civile, osservazioni FIMAA Veneto, calendario accademico UniPD. Nessun canone €/mq inventato.</p>'
    )
    faq_html = ['<div class="faq-section" id="faq"><h2>Domande frequenti</h2>']
    for q, a in FAQ:
        faq_html.append(f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a"><div class="faq-a-inner">{a}</div></div></div>')
    faq_html.append("</div>")
    chunks.extend(faq_html)
    chunks.append(
        '<div class="cta-banner"><div><h3>Devi affittare a studenti a Padova?</h3><p>Consulenza gratuita — tel. 049.8843484</p></div><a href="#richiedi-consulenza" class="cta-banner-btn">Scrivici</a></div>'
    )
    chunks.append(
        '<div class="related"><h3>Correlati</h3><ul><li><a href="blog-affitto-studenti-padova">Affitto studenti Padova</a></li><li><a href="blog-affittare-casa-padova-proprietario-2026">Affittare casa proprietario</a></li><li><a href="servizio-locazioni">Servizio locazioni</a></li><li><a href="zona-universitaria-padova">Zona universitaria</a></li></ul></div>'
    )
    return "\n".join(chunks)


def main() -> None:
    body = build_body()
    wc = word_count(body)
    if wc < MIN_WORDS:
        raise SystemExit(f"Body words {wc} < {MIN_WORDS}")
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ
        ],
    }
    blog_ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": "Affitti studenti Padova settembre 2026: cosa cambia per chi affitta",
        "description": "Affitti studenti Padova settembre 2026: calendario proprietario, contratti, OMI, visite e errori da evitare. Guida Righetto per chi affitta.",
        "image": [f"https://righettoimmobiliare.it/{HERO}"],
        "author": {"@type": "Person", "name": "Gino Capon"},
        "publisher": {
            "@type": "Organization",
            "name": "Righetto Immobiliare",
            "url": "https://righettoimmobiliare.it",
            "logo": {"@type": "ImageObject", "url": "https://righettoimmobiliare.it/img/og-default.webp"},
        },
        "datePublished": DATE_ISO,
        "dateModified": DATE_ISO,
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://righettoimmobiliare.it/{SLUG}"},
        "articleSection": "Guida proprietari",
        "wordCount": wc,
        "inLanguage": "it-IT",
    }
    title = "Affitti studenti Padova settembre 2026"
    meta = "Affitti studenti Padova settembre 2026: calendario proprietario, contratti, OMI e visite. Guida Righetto per chi affitta in zona universitaria."
    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
<script src="js/ga-consent.js?v=12"></script>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#2C4A6E">
<title>{title}</title>
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="preload" href="fonts/montserrat-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/cormorant-garamond-600.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{HERO}" as="image" fetchpriority="high">
<link rel="canonical" href="https://righettoimmobiliare.it/{SLUG}">
<meta property="og:type" content="article">
<meta property="og:title" content="Affitti studenti Padova settembre 2026: guida proprietario">
<meta property="og:description" content="{meta}">
<meta property="og:url" content="https://righettoimmobiliare.it/{SLUG}">
<meta property="og:image" content="https://righettoimmobiliare.it/{HERO}">
<meta property="og:site_name" content="Righetto Immobiliare">
<meta property="og:locale" content="it_IT">
<meta property="article:published_time" content="2026-09-25T10:00:00+02:00">
<meta property="article:author" content="Gino Capon">
<meta property="article:section" content="Guida proprietari">
<meta name="description" content="{meta}">
<script type="application/ld+json">{json.dumps(blog_ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
<script type="application/ld+json">{{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://righettoimmobiliare.it/"}}, {{"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://righettoimmobiliare.it/blog"}}, {{"@type": "ListItem", "position": 3, "name": "Affitti studenti settembre Padova"}}]}}</script>
<link rel="stylesheet" href="css/fonts.css?v=3">
<link rel="stylesheet" href="css/nav-mobile.css?v=7">
<link rel="stylesheet" href="css/scroll-reveal.css?v=3" media="print" onload="this.media='all'">
<link rel="stylesheet" href="css/welcome-popup.css?v=3" media="print" onload="this.media='all'">
{STYLE}
<link rel="stylesheet" href="css/blog-rich.css?v=4">
<link rel="stylesheet" href="css/blog-lead-form.css?v=2">
.chart-wrap{{background:var(--sfondo);border:1px solid var(--gc);border-radius:12px;padding:1.2rem;margin:1.4rem 0}}
.chart-wrap figcaption{{font-size:.72rem;color:var(--grigio);margin-top:.6rem;text-align:center}}
</head>
<body>
<a href="#main-content" class="skip-link">Vai al contenuto</a>
<header><div class="hi">
  <a href="/" class="logo">Righetto <span>Immobiliare</span></a>
  <nav><a href="/">Home</a><a href="immobili">Immobili</a><a href="servizi">Servizi</a><a href="gino-capon">Profilo autore</a><a href="blog" class="active">Blog</a><a href="contatti">Contatti</a></nav>
  <div class="h-cta"><a class="h-tel" href="tel:+390498843484">049.8843484</a><a class="h-btn" href="contatti">Valutazione gratuita</a></div>
</div><button class="nav-burger" id="burgerBtn" aria-label="Menu"><span></span><span></span><span></span></button></header>
<div class="nav-mobile" id="navMobile"><a href="/">Home</a><a href="immobili">Immobili</a><a href="blog">Blog</a><a href="contatti" class="nav-mobile-cta">Contatti</a></div>
<main id="main-content">
<div class="art-hero"><div class="art-hero__frame rig-ai-photo-wrap">
<img class="art-hero-img" src="{HERO}" alt="Affitti studenti Padova settembre 2026 — guida per proprietari che affittano" width="1900" height="900" fetchpriority="high" data-ai-generated="true">
<span class="rig-ai-photo-watermark" aria-hidden="true">FOTO AI</span>
</div><div class="art-hero-overlay"><div class="art-hero-inner">
<div class="breadcrumb"><a href="/">Home</a> / <a href="blog">Blog</a> / Affitti studenti settembre</div>
<span class="cat-badge">Proprietari · Affitti studenti</span>
<h1><strong>Affitti studenti</strong> Padova settembre 2026</h1>
<div class="art-hero-meta"><div class="av">G</div><span>Gino Capon</span><span>&middot;</span><span>{DATE_IT}</span></div>
</div></div></div>
<div class="art-container"><div class="art-content">
{body}
<div class="share-bar"><button type="button" class="share-btn" onclick="navigator.clipboard.writeText('https://righettoimmobiliare.it/{SLUG}');this.textContent='OK'">Copia link</button></div>
<div class="author-bio"><img src="img/team/titolari.webp" alt="Gino Capon" width="64" height="64" loading="lazy"><div><strong>Gino Capon</strong><p style="font-size:.82rem;color:#555">Righetto Immobiliare — Limena e Padova dal 2000.</p></div></div>
</div></div>
<section class="blog-rich-cta-strip" aria-label="Recensioni"><div class="blog-rich-cta-inner">
<h2>Ti è stato utile? Lascia una recensione</h2><a class="blog-rich-btn" href="https://maps.app.goo.gl/xuCiRGDCSKskpTSf6?g_st=ic" target="_blank" rel="noopener noreferrer">Google</a>
</div></section>
<section class="blog-lead-wrap" id="richiedi-consulenza" aria-labelledby="blog-lead-title">
  <h2 id="blog-lead-title">Richiedi una consulenza gratuita</h2>
  <form data-rig-lead-form data-provenienza="{SLUG}" data-pagina="{SLUG}" data-msg-prefix="[Blog]" novalidate>
    <div class="bl-fields">
      <label for="bl-nome">Nome e cognome *</label>
      <input type="text" id="bl-nome" required autocomplete="name" placeholder="Mario Rossi">
      <label for="bl-tel">Telefono *</label>
      <input type="tel" id="bl-tel" required autocomplete="tel" placeholder="333 123 4567">
      <label for="bl-email">Email</label>
      <input type="email" id="bl-email" autocomplete="email" placeholder="mario@email.it">
      <label for="bl-msg">Messaggio (opzionale)</label>
      <textarea id="bl-msg" placeholder="Zona, tipologia, urgenza settembre…"></textarea>
      <label class="bl-chk"><input type="checkbox" id="bl-gdpr" required> Ho preso visione dell'<a href="privacy" target="_blank" rel="noopener">informativa privacy</a>. *</label>
      <button type="submit">Invia richiesta</button>
    </div>
    <div class="rig-lead-success"><h3>Messaggio inviato!</h3><p>Grazie. Ti ricontattiamo entro pochi minuti negli orari di apertura.</p></div>
  </form>
</section>
</main>
<footer><div class="fi"><div class="fgrid"><div><div class="flogo">Righetto <span>Immobiliare</span></div>Via Roma 96, Limena (PD)</div><div><a href="blog" style="color:rgba(255,255,255,.7)">Blog</a></div><div><a href="contatti" style="color:rgba(255,255,255,.7)">Contatti</a></div></div><div style="border-top:1px solid rgba(255,255,255,.1);padding-top:1rem">&copy; 2026 Gruppo Immobiliare Righetto</div></div></footer>
<script>document.querySelectorAll('.faq-q').forEach(function(q){{q.addEventListener('click',function(){{var p=this.parentElement,o=p.classList.contains('open');document.querySelectorAll('.faq-item.open').forEach(function(x){{x.classList.remove('open');}});if(!o)p.classList.add('open');}});}});</script>
<script src="js/vendor/supabase.min.js" defer></script>
<script src="js/config.js?v=4"></script>
<script src="js/rig-lead-form.js?v=3"></script>
<script src="js/nav-mobile.js?v=3" defer></script>
<script src="js/cookie-consent.js?v=3" defer></script>
<script src="js/scroll-reveal.js?v=3" defer></script>
<script src="js/welcome-popup.js?v=3" defer></script>
</body></html>
"""
    FILE.write_text(html, encoding="utf-8")
    print(f"Wrote {FILE.name} words={wc}")


if __name__ == "__main__":
    main()
