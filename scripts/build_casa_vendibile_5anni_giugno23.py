# -*- coding: utf-8 -*-
"""Articolo blog: casa vendibile tra 5 anni — case green e posizione a Padova.
python scripts/build_casa_vendibile_5anni_giugno23.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

import build_giugno03_blog_batch as g03  # noqa: E402

g03.DATE_IT = "23 giugno 2026"
g03.DATE_ISO = "2026-06-23"
g03.TIME_TS = "2026-06-23T09:00:00+02:00"

from build_giugno03_blog_batch import (  # noqa: E402
    aeo_box,
    build_article,
    faq_html,
    sources_table,
)

ROOT = _SCRIPT_DIR.parent
ASSETS = Path(r"C:\Users\Utente\.cursor\projects\c-Users-Utente-progetti-index\assets")
IMG_DIR = ROOT / "img" / "blog"
HERO_WEBP = "blog-casa-vendibile-5-anni-case-green-padova-2026.webp"
INLINE1 = "blog-inline-green-vs-brown-padova-2026.webp"
INLINE2 = "blog-inline-posizione-padova-2026.webp"

SLUG = "blog-casa-vendibile-5-anni-case-green-padova-2026"


def png_to_webp(src: Path, dst: Path, tw: int = 1200, th: int = 630, ay: float = 0.38) -> None:
    from PIL import Image

    dst.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        rgb = im.convert("RGB") if im.mode != "RGB" else im
        sw, sh = rgb.size
        scale = max(tw / sw, th / sh)
        nw, nh = int(sw * scale), int(sh * scale)
        rgb = rgb.resize((nw, nh), Image.Resampling.LANCZOS)
        left = (nw - tw) // 2
        top = int((nh - th) * ay)
        out = rgb.crop((left, top, left + tw, top + th))
    out.save(dst, "WEBP", quality=86, method=6)


def gen_images() -> None:
    png_to_webp(ASSETS / "blog-hero-casa-vendibile-5-anni-padova-2026.png", IMG_DIR / HERO_WEBP)
    png_to_webp(ASSETS / "blog-inline-green-vs-brown-padova-2026.png", IMG_DIR / INLINE1, 960, 540, 0.45)
    png_to_webp(ASSETS / "blog-inline-posizione-padova-2026.png", IMG_DIR / INLINE2, 960, 540, 0.5)
    print("Immagini WebP:", HERO_WEBP, INLINE1, INLINE2)


ARTICLE = {
    "filename": f"{SLUG}.html",
    "slug": SLUG,
    "img": f"img/blog/{HERO_WEBP}",
    "bread": "Casa vendibile tra 5 anni Padova",
    "section": "Mercato e sostenibilità",
    "html_title": "Casa vendibile tra 5 anni a Padova: APE e posizione | Righetto",
    "og_title": "La tua casa sarà vendibile nel 2031? Classe energetica, Case Green e quartieri richiesti nel Padovano",
    "schema_headline": "Casa vendibile tra 5 anni: prestazioni energetiche, Case Green e posizione a Padova",
    "meta_desc": "Analisi dei 5 temi più citati online: nessun divieto di vendita, brown discount CRIF, posizione e due esempi LP0286 e LA0317 nel Padovano.",
    "cat_badge": "Mercato e sostenibilità",
    "alt_img": "Quartiere residenziale Padova — efficienza energetica e valore immobiliare nel 2031, illustrazione editoriale Righetto",
    "breadcrumb_tail": "Casa vendibile 5 anni",
    "h1": "<strong>Casa vendibile tra 5 anni</strong>: cosa dicono i 5 articoli più gettonati su Google, e come valutare APE e posizione a Padova",
    "cap_img": (
        '<p class="cap-img">Copertina e illustrazioni <strong>editoriali</strong> Righetto — non fotografie degli immobili citati. '
        "Dati numerici da fonti citate nel testo (CRIF, FIAIP, UE). Ultimo aggiornamento: 23 giugno 2026.</p>"
    ),
    "aeo": aeo_box(
        "Per <strong>proprietari e acquirenti nel Padovano</strong> che si chiedono se la propria casa resterà "
        "vendibile entro il 2031 e quanto incideranno <strong>classe energetica (APE)</strong> e "
        "<strong>posizione geografica</strong> sul prezzo.",
        [
            "La tua casa resterà <strong>assolutamente vendibile</strong> tra 5 anni: non esiste un divieto "
            "di vendita per classi basse, come confermano le analisi più visibili online e la "
            "<strong>Direttiva (UE) 2024/1275</strong> (EPBD).",
            "Il <strong>valore di mercato</strong> dipenderà sempre più da due leve: prestazioni energetiche "
            "(polarizzazione green vs brown) e <strong>microzona</strong> — nelle aree più richieste i prezzi "
            "tendono a restare stabili o in crescita (OMI e pratica locale).",
            "Il mercato applica già <strong>premi e sconti</strong> misurabili: CRIF segnala fino a "
            "<strong>700 €/mq</strong> di divario tra immobili green (A–B) e brown (F–G) in media nazionale "
            "(giugno 2025).",
            "Due esempi concreti nel nostro portafoglio: villetta <strong>LP0286</strong> ad Altichiero "
            "(classe C, ristrutturata) e quadrilocale <strong>LA0317</strong> a Mandria (classe E).",
        ],
        [
            "Non è consulenza legale sulla Direttiva Case Green — il recepimento italiano è ancora in corso.",
            "Non duplica l'articolo <a href=\"blog-direttiva-case-green-limena-padova\">Direttiva Case Green Limena</a> "
            "(focus normativo approfondito).",
            "Non promette plusvalenze percentuali fisse su singoli immobili senza perizia e comparabili.",
        ],
    ),
    "body_extra": f"""<h2>La tesi di partenza: vendibile sì, ma a che prezzo?</h2>
<p><strong>La tua casa sarà assolutamente vendibile tra 5 anni.</strong> Tuttavia, il suo valore dipenderà molto da due fattori chiave: le <strong>prestazioni energetiche</strong> dell'immobile — spinte dalle normative europee sulle «case green» — e la <strong>posizione geografica</strong>. Nelle aree più richieste i prezzi tenderanno a rimanere stabili o in crescita. Questa frase sintetizza ciò che emerge incrociando le cinque analisi più citate online nel 2026, la pratica delle trattative nel Padovano e i dati verificabili di CRIF e FIMAA.</p>
<p>In agenzia, a Limena e sui <strong>101 comuni</strong> del nostro raggio, vediamo ogni settimana compravendite su immobili in classe D, E e anche G: il mercato non si è fermato. Cambia invece il <em>tempo</em> di vendita, la <em>leva</em> negoziale dell'acquirente e il <em>confronto</em> con comparabili più efficienti nella stessa microzona.</p>

<h2>I 5 articoli più visibili su Google: cosa ripetono (e cosa no)</h2>
<p>Abbiamo analizzato le pagine che oggi dominano le ricerche su «case green», «classe energetica valore immobile» e «vendere casa 2030». Non sono ranking ufficiali Google, ma i contenuti che più spesso compaiono in SERP e social nel primo semestre 2026. Ecco la sintesi editoriale per tema.</p>
<table>
<thead><tr><th>Fonte (visibilità 2026)</th><th>Messaggio chiave</th><th>Dato citato</th><th>Implicazione per Padova</th></tr></thead>
<tbody>
<tr><td><a href="https://www.ilsottosopra.info/2026/02/19/case-green-e-valore-immobiliare-perche-lefficienza-energetica-decide-prezzo-e-tempi-di-vendita/" target="_blank" rel="noopener noreferrer">ilSottosopra</a></td><td>Efficienza = prezzo + tempi</td><td>Immobile efficiente 3–4 mesi vs energivoro 8–10 mesi (stima autore)</td><td>In quartieri saturi (Arcella, Sacrocuore) la velocità pesa quanto il prezzo</td></tr>
<tr><td><a href="https://www.lastampa.it/tuttosoldi/2026/03/31/news/casa_e_compravendite_quanto_vale_la_classe_energetica_migliore_i_rischi_per_chi_non_si_adegua-15566322/" target="_blank" rel="noopener noreferrer">La Stampa / FIAIP Monitora</a></td><td>Polarizzazione green vs obsoleti</td><td>Report FIAIP + ENEA + I-Com al Senato 2025</td><td>Allinea le trattative padovane al tema APE in perizia mutuo</td></tr>
<tr><td><a href="https://ideeimmobili.com/blog/direttiva-case-green-2026-proprietari-italiani/" target="_blank" rel="noopener noreferrer">Idee Immobili</a></td><td>Nessun divieto vendita; rischio economico</td><td>Brown discount 15–30% (range editoriale)</td><td>Utile per gestire aspettative su immobili da ristrutturare</td></tr>
<tr><td><a href="https://www.mohogroup.it/direttiva-case-green-vendere-comprare-casa/" target="_blank" rel="noopener noreferrer">Mode Home Group</a></td><td>Posizione + stato + energia</td><td>Recepimento UE entro 29/05/2026 ancora in corso</td><td>Conferma: microzona resta driver primario</td></tr>
<tr><td><a href="https://www.flimmobiliare.it/le-case-green-valgono-piu-di-quelle-brown-ecco-di-quanto-e-il-divario/" target="_blank" rel="noopener noreferrer">FL Immobiliare / CRIF</a></td><td>Gap €/mq green vs brown</td><td>+500 €/mq vs intermedi; +700 €/mq vs brown (giu. 2025)</td><td>Benchmark nazionale — non sostituisce OMI di zona</td></tr>
</tbody>
</table>
<p><strong>Convergenza:</strong> tutti e cinque descrivono una transizione <em>di mercato</em>, non un blocco delle compravendite. <strong>Divergenza:</strong> le percentuali di sconto variano per città, tipologia e campione; a Milano CRIF ha stimato fino al 34% tra green e brown (<a href="https://valumetrica.it/blog/impatto-direttiva-case-green-prezzi-case-milano/" target="_blank" rel="noopener noreferrer">ValuMetrica</a>, riferimento CRIF giugno 2025). Sul Padovano non pubblichiamo percentuali fisse senza campione locale verificabile: usiamo <a href="https://www.agenziaentrate.gov.it" target="_blank" rel="noopener noreferrer">OMI</a> e comparabili reali.</p>

<h2>Direttiva Case Green (EPBD): cosa sappiamo con certezza</h2>
<p>La <strong>Direttiva (UE) 2024/1275</strong>, in vigore dal 28 maggio 2024, impone agli Stati membri obiettivi <em>medi</em> di riduzione del consumo energetico nel residenziale (tra cui −16% entro il 2030), non un obbligo individuale di raggiungere classe A entro una data fissa per ogni singola unità — come chiariscono <a href="https://www.immobiliare.it/news/economia/tasse-imposte-e-normative/direttiva-case-green-quali-sono-gli-edifici-che-non-dovranno-essere-riqualificati-498655/" target="_blank" rel="noopener noreferrer">Immobiliare.it News</a> e le guide citate sopra.</p>
<p>In Italia il recepimento era atteso entro il <strong>29 maggio 2026</strong>; al 23 giugno 2026 valgono le norme nazionali già in vigore sull'<strong>APE</strong> in compravendita e locazione. Di conseguenza, per chi vende a Padova nel 2026–2031: documentazione energetica ordinata, onestà in annuncio, nessuna «scadenza» che renda illegale la vendita di una classe G.</p>
<h3>Cosa cambia nella testa dell'acquirente</h3>
<p>Il mutuo e le bollette hanno reso l'APE un foglio di calcolo, non un adempimento burocratico. Idee Immobili stima che una classe G possa costare <strong>2.000–3.000 euro l'anno</strong> in più di bollette rispetto a una C o B (ordine di grandezza editoriale, utile in trattativa). In parallelo, i mutui «green» possono offrire condizioni migliori quando l'immobile rientra nei criteri bancari — tema già trattato nel nostro articolo su <a href="blog-domanda-case-green-certificazione-padova-2026">domanda case green Padova</a>.</p>

<h2>Classe energetica: green premium e brown discount</h2>
<p>CRIF Real Estate Services, citata da FL Immobiliare a giugno 2025, ha analizzato immobili oggetto di perizia mutuo in Italia e ha quantificato:</p>
<ul>
<li><strong>+500 €/mq</strong> in media per immobili green (classe A–B) rispetto a classi intermedie (C–E);</li>
<li><strong>+700 €/mq</strong> di divario tra green e brown (F–G);</li>
<li>Nei centri urbani fino a <strong>1.000 €/mq</strong> e <strong>40%</strong> di scarto percentuale tra estremi della scala.</li>
</ul>
<p>Su un trilocale di 90 mq, 700 €/mq equivalgono a <strong>63.000 euro</strong> di distanza teorica — prima di considerare stato, piano, condominio e parcheggio. È un segnale nazionale, non il prezzo del tuo immobile: serve la <a href="servizio-valutazioni">valutazione comparativa</a> sul campo.</p>
<figure style="margin:1.4rem 0">
<img src="img/blog/{INLINE1}" alt="Confronto editoriale immobile efficiente vs edificio energivoro — tema green premium e brown discount Padova" width="960" height="540" loading="lazy" style="width:100%;height:auto;border-radius:10px;border:1px solid var(--gc)">
<figcaption class="cap-img">Illustrazione editoriale sul divario green/brown — non rappresenta un immobile specifico in vendita.</figcaption>
</figure>
<p>ilSottosopra riporta inoltre stime di mercato urbano: −15%/−20% di valore per energivori vs +30%/+40% per efficienti in area metropolitana (tabella autore, febbraio 2026). Trattiamo questi range come <strong>ordini di grandezza</strong> da verificare caso per caso, non come automatico aggiustamento del prezzo richiesto.</p>

<h2>Posizione geografica: il secondo fattore (e spesso il primo)</h2>
<p>Mode Home Group conclude che «posizione, dimensioni e stato manutentivo continueranno a essere fondamentali». Nel Padovano la regola si traduce in microzone: <strong>Altichiero</strong>, <strong>Mandria</strong>, <strong>Sacrocuore</strong>, <strong>Limena</strong>, comuni della cintura come <strong>Vigonza</strong> e <strong>Albignasego</strong> hanno dinamiche OMI distinte. Dove la domanda familiare resta alta e l'offerta è limitata, un immobile in classe E può comunque assorbirsi in pochi mesi se prezzo e stato sono coerenti.</p>
<figure style="margin:1.4rem 0">
<img src="img/blog/{INLINE2}" alt="Mappa editoriale area Padova — centrale storico e quartieri residenziali per valutazione posizione immobile" width="960" height="540" loading="lazy" style="width:100%;height:auto;border-radius:10px;border:1px solid var(--gc)">
<figcaption class="cap-img">Posizione e contesto urbano incidono sul valore a 5 anni — mappa concettuale, non catastale.</figcaption>
</figure>
<p>La Banca d'Italia e ISTAT descrivono un mercato residenziale italiano che nel 2025–2026 ha mostrato resilienza differenziata per area. Padova città e hinterland nord-est restano tra i contesti veneti con transazioni attive (vedi anche <a href="blog-compravendite-italia-q1-agenzia-entrate-2026-padova">compravendite Q1 Agenzia Entrate</a>). In sintesi: <strong>zona richiesta + immobile coerente con la domanda locale</strong> attenua il rischio di sconto energetico; zona debole + classe G amplifica la trattativa a favore dell'acquirente.</p>""",
    "body_mid": f"""<h2>Orizzonte 5 anni: scenario 2031 per chi vende o compra</h2>
<p>La Stampa cita esplicitamente il rischio che «nei prossimi cinque anni la Direttiva Green accelererà la polarizzazione». Operativamente, entro il <strong>2031</strong> possiamo ragionevolmente attenderci:</p>
<ol>
<li><strong>Maggiore peso dell'APE</strong> in perizia, mutuo e comparazione online tra annunci simili.</li>
<li><strong>Pressione su edifici F/G</strong> in condomini (interventi sul involucro e impianti) senza bloccare la vendita dell'unità singola.</li>
<li><strong>Premio di posizione</strong> stabile o crescente in quartieri serviti (scuole, tangenziale, verde) come documentano le schede OMI semestrali.</li>
<li><strong>Incentivi</strong> legati a riqualificazione — vedi <a href="blog-bonus-edilizi-2026-incentivi-casa-padova">bonus edilizi 2026</a> — ma solo dove il conto economico chiude.</li>
</ol>
<p>Non è obbligatorio ristrutturare prima di vendere. Idee Immobili suggerisce due strategie: vendere subito se i costi di efficientamento sono sproporzionati rispetto al valore, oppure riqualificare se gli incentivi e i tempi lo permettono. Entrambe restano valide a Padova.</p>

<h2>Due immobili del portafoglio Righetto: APE e posizione a confronto</h2>
<p>Per rendere concreta la tesi, incrociamo due proposte attive sul nostro portale — dati da scheda aggiornata a giugno 2026.</p>

<article style="border:1px solid var(--gc);border-radius:12px;padding:1.2rem 1.3rem;margin:1.5rem 0;background:var(--sfondo)">
<h3 style="margin-top:0;color:var(--blu)">Villetta LP0286 — Altichiero (Padova nord)</h3>
<img src="https://qwkwkemuabfwvwuqrxlu.supabase.co/storage/v1/object/public/foto-immobili/1779963017206-casa-singola-altichiero-4-.jpg" alt="Casa singola ristrutturata Altichiero Padova LP0286 — foto portale Righetto" width="820" height="340" loading="lazy" style="width:100%;height:auto;border-radius:8px;margin:.8rem 0">
<p><strong>€365.000</strong> · circa <strong>230 mq</strong> · 8 locali · <strong>ristrutturata</strong> · classe <strong>C</strong> (IPE 122,39 kWh/m²a) · garage e giardino · quartiere verde <strong>Altichiero</strong>.</p>
<p>Profilo «pronto abitare» con metrature ampie: combina <strong>posizione residenziale richiesta</strong> (Padova nord, servizi e tangenziale) con <strong>prestazione energetica intermedia-alta</strong> post-intervento. Per l'orizzonte 2031, un acquirente valuta soprattutto assenza cantieri, spese prevedibili e comparazione con villette simili in zona — dove la classe C oggi resta competitiva rispetto a stock F/G da ristrutturare.</p>
<p><a class="cta-deep" href="immobile?s=villetta-vendita-padova-lp0286">Apri scheda LP0286 — foto e planimetrie</a></p>
</article>

<article style="border:1px solid var(--gc);border-radius:12px;padding:1.2rem 1.3rem;margin:1.5rem 0;background:#fff">
<h3 style="margin-top:0;color:var(--blu)">Quadrilocale LA0317 — Mandria (Padova)</h3>
<img src="https://qwkwkemuabfwvwuqrxlu.supabase.co/storage/v1/object/public/foto-immobili/1777994309447-000-appartamento-2-piano-mandria-padova-righetto-immobiliare-1-wmk-0.jpg" alt="Appartamento quadrilocale Mandria Padova LA0317 — foto portale Righetto" width="820" height="340" loading="lazy" style="width:100%;height:auto;border-radius:8px;margin:.8rem 0">
<p><strong>€200.000</strong> · circa <strong>90 mq</strong> · 5 locali · secondo piano · <strong>ristrutturato</strong> · classe <strong>E</strong> (IPE 112,53 kWh/m²a) · zona <strong>Mandria</strong>.</p>
<p>Qui la leva dominante è la <strong>posizione</strong>: Mandria è tra le zone residenziali tranquille del comune di Padova, con domanda di famiglie e coppie. L'immobile è già ristrutturato (ingresso rapido), ma la classe E invita l'acquirente a simulare bollette e possibili interventi leggeri (infissi, pompa di calore) rispetto a un A/B in centro a prezzo maggiore. Entro 5 anni resterà vendibile — la domanda locale lo conferma —; il prezzo finale dipenderà da quanto il mercato premierà un salto di classe rispetto a comparabili in <a href="zona-sacra-famiglia-padova">Sacrocuore</a> o in periferia.</p>
<p><a class="cta-deep" href="immobile?s=appartamento-vendita-padova-la0317">Apri scheda LA0317 — foto e planimetrie</a></p>
</article>

<p>Il confronto LP0286 vs LA0317 illustra la tesi iniziale: <strong>entrambi vendibili</strong>, con leve diverse. La villetta punta su metrature, pertinenze ed energia post-ristrutturazione; l'appartamento su prezzo di ingresso, quartiere e finiture, accettando un APE migliorabile. Nessuna delle due schede « garantisce » plusvalenza: servono visita, documenti e strategia di prezzo.</p>

<h2>Tempi di vendita: oltre il prezzo al metro quadro</h2>
<p>ilSottosopra stima che gli immobili efficienti restino in media <strong>3–4 mesi</strong> contro <strong>8–10 mesi</strong> per energivori in contesto urbano. Nel Padovano, Righetto osserva tempi fortemente legati al <strong>allineamento prezzo/OMI</strong> e alla qualità del marketing (foto, planimetrie, APE visibile). Un bilocale in <a href="zona-universitaria-padova">zona universitaria</a> in classe mediocre può vendere in settimane se il canone implicito da locazione studenti giustifica il prezzo; una villa in campagna classe G può richiedere mesi anche se grande — perché la domanda è più sottile.</p>
<h3>Mutuo, perizia e trattativa</h3>
<p>La polarizzazione descritta da FIAIP si manifesta in banca: perizie più conservative su F/G e maggiore appetite su A–C possono restringere il pool di acquirenti finanziati. Non è un divieto di vendita, ma un filtro reale. Per approfondire: <a href="blog-ape-prestazione-energetica-acquisto-padova-2026">APE e acquisto Padova</a> e <a href="landing-mutuo">simulazione mutuo</a>.</p>

<h2>Cosa fare adesso: checklist proprietario padovano</h2>
<ul>
<li><strong>Leggere l'APE</strong> e confrontarlo con comparabili venduti (non solo annunci online).</li>
<li><strong>Mappare la microzona</strong> con OMI e articoli zona (<a href="blog-quartieri-padova-2026">quartieri Padova 2026</a>).</li>
<li><strong>Stimare costi</strong> di intervento vs brown discount atteso — con tecnico e, se serve, commercialista per bonus.</li>
<li><strong>Decidere timing</strong>: vendere ora con strategia trasparente su energia, o investire in efficientamento mirato.</li>
<li><strong>Preparare documenti</strong>: APE, planimetria, libretti impianti (<a href="blog-documenti-vendita-casa">documenti vendita</a>).</li>
</ul>""",
    "body_tail": """<h2>Acquirente: opportunità brown e rischi da calcolare</h2>
<p>Mode Home Group ricorda che una casa in classe bassa «può rappresentare un'opportunità» se si conoscono costi futuri. Nel Padovano, bifamiliari da ristrutturare in comuni della cintura restano richieste da chi ha budget lavori. L'errore è sottostimare il capex energetico: un salto da G a C può richiedere decine di migliaia di euro — da incrociare con <a href="blog-bonus-edilizi-2026-incentivi-casa-padova">incentivi 2026</a>, non con wishful thinking.</p>

<h2>Sintesi per il mercato padovano</h2>
<p>Tra 5 anni la compravendita resterà possibile per quasi tutte le classi energetiche. Il valore, però, seguirà due binari: <strong>quanto costa vivere lì</strong> (bollette, mutuo green, obblighi futuri del condominio) e <strong>dove si trova</strong> (domanda locale, servizi, offerta concorrente). Le analisi più cliccate online convergono su questo dualismo; CRIF ne quantifica la distanza in euro al metro quadro a livello nazionale; FIAIP ne documenta la crescente rilevanza nelle perizie.</p>
<p>Se stai valutando vendita o acquisto ad Altichiero, Mandria o altrove nel nostro raggio: <a href="landing-valutazione">valutazione gratuita 24h</a> o <a href="landing-consulenza-immobiliare-gratuita">consulenza senza impegno</a>. Per LP0286 e LA0317, le schede complete sono linkate sopra.</p>

<div class="warn"><strong>Fonti editoriali analizzate:</strong> ilSottosopra (feb. 2026), La Stampa / FIAIP Monitora (mar. 2026), Idee Immobili, Mode Home Group, FL Immobiliare / CRIF RES (giu. 2025). Normativa: Direttiva (UE) 2024/1275. Dati OMI: Agenzia delle Entrate. Percentuali e €/mq sono riferiti alle fonti indicate; non costituiscono stima automatica del tuo immobile.</div>""",
    "sources": sources_table([
        ("Divario €/mq green vs brown", "CRIF Real Estate Services via FL Immobiliare, giu. 2025", "Benchmark nazionale per trattativa"),
        ("Polarizzazione classe energetica", "FIAIP Monitora Italia 2025 + ENEA + I-Com", "Contesto istituzionale"),
        ("Obiettivi EPBD 2030", "Direttiva (UE) 2024/1275", "−16% consumo residenziale medio UE"),
        ("Nessun divieto vendita G", "Immobiliare.it News / Idee Immobili 2026", "Chiarimento normativo"),
        ("Microzone Padova", "OMI Agenzia Entrate + pratica Righetto", "Prezzo e domanda locale"),
    ]),
    "topic": "casa vendibile cinque anni prestazioni energetiche case green posizione Padova Altichiero Mandria",
    "anchors": [
        ("direttiva case green", "blog-direttiva-case-green-limena-padova"),
        ("bonus edilizi 2026", "blog-bonus-edilizi-2026-incentivi-casa-padova"),
        ("documenti vendita", "blog-documenti-vendita-casa"),
        ("valutazione gratuita", "landing-valutazione"),
        ("quartieri Padova", "blog-quartieri-padova-2026"),
    ],
    "body_n": 0,
    "faqs": [
        (
            "Tra 5 anni potrò vendere una casa in classe G?",
            "Sì. Le fonti più visibili online e la Direttiva UE 2024/1275 non prevedono un divieto di vendita per classi basse; il rischio è economico (tempi di vendita e trattativa sul prezzo), non legale.",
        ),
        (
            "Quanto incide la classe energetica sul valore?",
            "CRIF (giu. 2025) stima fino a 700 €/mq di divario tra immobili green (A–B) e brown (F–G) in media nazionale; su Padova serve confronto OMI e comparabili reali.",
        ),
        (
            "La posizione può compensare un APE basso?",
            "Spesso sì, in microzone ad alta domanda (quartieri serviti di Padova e comuni limitrofi). Stato manutentivo e prezzo iniziale restano determinanti.",
        ),
        (
            "Conviene ristrutturare prima di vendere?",
            "Solo se il costo dell'intervento è inferiore al maggiore prezzo ottenibile e ai tempi risparmiati. Idee Immobili e Mode Home Group suggeriscono analisi caso per caso.",
        ),
        (
            "Cosa sono LP0286 e LA0317?",
            "Due immobili in vendita su righettoimmobiliare.it: villetta ristrutturata ad Altichiero (classe C) e quadrilocale a Mandria (classe E), citati come esempi nel Padovano.",
        ),
        (
            "Righetto garantisce il valore futuro del mio immobile?",
            "No. Offriamo valutazioni comparative, marketing e assistenza alla vendita su 101 comuni; le proiezioni dipendono da mercato, normativa e caratteristiche dell'unità.",
        ),
    ],
    "related": [
        ("Direttiva Case Green Limena", "blog-direttiva-case-green-limena-padova"),
        ("Domanda case green Padova", "blog-domanda-case-green-certificazione-padova-2026"),
        ("Bonus edilizi 2026", "blog-bonus-edilizi-2026-incentivi-casa-padova"),
    ],
    "cta_primary": ("Valutazione gratuita", "landing-valutazione"),
    "cta_secondary": ("Consulenza immobiliare", "landing-consulenza-immobiliare-gratuita"),
    "registry": {
        "titolo": "Casa vendibile tra 5 anni: APE, Case Green e posizione a Padova",
        "categoria": "Mercato e sostenibilità",
        "tempo": 14,
        "contenuto": "Analisi 5 articoli top su Google, CRIF/FIAIP, orizzonte 2031 e esempi LP0286 Altichiero e LA0317 Mandria.",
        "evidenza": True,
        "emoji": "🏡",
    },
}


def main() -> int:
    gen_images()
    html, wc = build_article(ARTICLE)
    html = html.replace("rig-lead-form.js?v=1", "rig-lead-form.js?v=2")
    html = html.replace("blog-lead-form.css?v=1", "blog-lead-form.css?v=2")
    out = ROOT / ARTICLE["filename"]
    out.write_text(html, encoding="utf-8")
    print(f"OK {out.name} — ~{wc} parole")

    reg = {
        "generated": g03.DATE_ISO,
        "blog_html_articoliStatici": [
            {
                "titolo": ARTICLE["registry"]["titolo"],
                "categoria": ARTICLE["registry"]["categoria"],
                "data": g03.DATE_ISO,
                "stato": "pubblicato",
                "immagine_copertina": ARTICLE["img"],
                "url_statico": SLUG,
                "tempo": ARTICLE["registry"]["tempo"],
                "autore": "Gino Capon",
                "contenuto": ARTICLE["registry"]["contenuto"],
                "evidenza": ARTICLE["registry"]["evidenza"],
            }
        ],
        "admin_blogSeedArticles": [
            {
                **ARTICLE["registry"],
                "data": g03.DATE_ISO,
                "stato": "pubblicato",
                "autore": "Gino Capon",
                "immagine_copertina": ARTICLE["img"],
                "url_statico": SLUG,
                "contenuto": f"<p>{ARTICLE['registry']['contenuto']}</p>",
                "data_pubblicazione": g03.TIME_TS,
            }
        ],
        "homepage_js_articoliStatici": [
            {
                "titolo": ARTICLE["registry"]["titolo"],
                "categoria": ARTICLE["registry"]["categoria"],
                "data": g03.DATE_ISO,
                "stato": "pubblicato",
                "immagine_copertina": ARTICLE["img"],
                "url_statico": SLUG,
            }
        ],
    }
    reg_path = ROOT / "scripts" / "casa_vendibile_5anni_registry.json"
    reg_path.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Registry: {reg_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
