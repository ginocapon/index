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

    if not src.is_file():
        return
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
    for src, dst, w, h, ay in [
        (ASSETS / "blog-hero-casa-vendibile-5-anni-padova-2026.png", IMG_DIR / HERO_WEBP, 1200, 630, 0.38),
        (ASSETS / "blog-inline-green-vs-brown-padova-2026.png", IMG_DIR / INLINE1, 960, 540, 0.45),
        (ASSETS / "blog-inline-posizione-padova-2026.png", IMG_DIR / INLINE2, 960, 540, 0.5),
    ]:
        if src.is_file():
            png_to_webp(src, dst, w, h, ay)


ARTICLE = {
    "filename": f"{SLUG}.html",
    "slug": SLUG,
    "img": f"img/blog/{HERO_WEBP}",
    "bread": "Casa vendibile tra 5 anni Padova",
    "section": "Mercato e sostenibilità",
    "html_title": "Casa vendibile tra 5 anni a Padova: APE e posizione | Righetto",
    "og_title": "Casa vendibile nel 2031: classe energetica, Case Green e quartieri richiesti nel Padovano",
    "schema_headline": "Casa vendibile tra 5 anni: prestazioni energetiche, Case Green e posizione a Padova",
    "meta_desc": "Vendibile sì, ma a che prezzo? APE, Direttiva Case Green, dati CRIF/FIAIP, microzone Padova ed esempi LP0286 e LA0317 nel portafoglio Righetto.",
    "cat_badge": "Mercato e sostenibilità",
    "alt_img": "Quartiere residenziale Padova — efficienza energetica e valore immobiliare, illustrazione editoriale Righetto",
    "breadcrumb_tail": "Casa vendibile 5 anni",
    "h1": "<strong>Casa vendibile tra 5 anni</strong>: classe energetica, Case Green e posizione nel mercato padovano",
    "cap_img": (
        '<p class="cap-img">Illustrazioni <strong>editoriali</strong> Righetto. '
        "Dati numerici con fonte nel testo (CRIF, FIAIP, UE, OMI). Aggiornato: 23 giugno 2026.</p>"
    ),
    "aeo": aeo_box(
        "Per <strong>proprietari e acquirenti nel Padovano</strong> che vogliono capire se la propria casa "
        "resterà vendibile entro il 2031 e quanto peseranno <strong>APE</strong> e <strong>posizione</strong> sul prezzo.",
        [
            "La casa resterà <strong>vendibile</strong>: la <strong>Direttiva (UE) 2024/1275</strong> (EPBD) "
            "non introduce divieti di vendita per classi basse; il tema è il <strong>valore di mercato</strong>.",
            "Due leve decisive: <strong>prestazioni energetiche</strong> (polarizzazione tra immobili efficienti "
            "ed energivori) e <strong>microzona</strong> — nelle aree più richieste i prezzi tendono a restare "
            "stabili o in crescita.",
            "CRIF (giugno 2025) segnala fino a <strong>700 €/mq</strong> di distanza tra classi A–B e F–G "
            "in media nazionale su perizie mutuo.",
            "Esempi dal portafoglio Righetto: <strong>LP0286</strong> ad Altichiero (classe C) e "
            "<strong>LA0317</strong> a Mandria (classe E).",
        ],
        [
            "Non è consulenza legale — il recepimento italiano della Direttiva Case Green è in corso.",
            "Non sostituisce <a href=\"blog-direttiva-case-green-limena-padova\">l'approfondimento normativo</a> "
            "già pubblicato sul sito.",
            "Non promette plusvalenze percentuali fisse senza valutazione comparativa sul campo.",
        ],
    ),
    "body_extra": f"""<h2>Vendibile sì, ma a che prezzo?</h2>
<p><strong>La tua casa sarà assolutamente vendibile tra 5 anni.</strong> Tuttavia, il suo valore dipenderà molto da due fattori chiave: le <strong>prestazioni energetiche</strong> dell'immobile — spinte dalle normative europee sulle «case green» — e la <strong>posizione geografica</strong>. Nelle aree più richieste i prezzi tenderanno a rimanere stabili o in crescita. È la sintesi che traiamo dalla pratica quotidiana in agenzia, incrociata con i dati istituzionali disponibili e con le dinamiche che già oggi vediamo in trattativa a Padova e provincia.</p>
<p>Da Limena operiamo su <strong>101 comuni</strong>. Ogni settimana concludiamo compravendite su appartamenti e villette in classe D, E e talvolta G: il mercato non si è bloccato. Cambiano però i <strong>tempi</strong> di assorbimento, la <strong>leva</strong> dell'acquirente in negoziazione e il <strong>confronto</strong> con annunci simili più efficienti nella stessa microzona.</p>

<h2>Cosa sta cambiando nel mercato immobiliare</h2>
<p>Il <strong>Report FIAIP Monitora Italia 2025</strong>, elaborato dal Centro Studi FIAIP con ENEA e I-Com e presentato al Senato, ha messo in evidenza per la prima volta in modo sistematico il peso della classe energetica sul valore percepito degli immobili. In parallelo, <strong>CRIF Real Estate Services</strong> ha analizzato a giugno 2025 una quota rappresentativa di unità oggetto di perizia mutuo in Italia, quantificando divari di prezzo al metro quadro tra immobili «green» (classi A–B) e «brown» (F–G).</p>
<p>Non si tratta di una moda mediatica: in sede di visita e compromesso, l'acquirente padovano chiede sempre più spesso il costo annuo delle utenze, la data dell'ultimo intervento sugli infissi e se il condominio ha in programma lavori sull'involucro. L'APE non è più un foglio da allegare per obbligo: è un parametro di confronto tra due proposte simili in <strong>Arcella</strong>, <strong>Sacrocuore</strong> o in campagna.</p>

<h2>Direttiva Case Green: cosa significa per il singolo proprietario</h2>
<p>La <strong>Direttiva (UE) 2024/1275</strong>, in vigore dal 28 maggio 2024, fissa obiettivi <em>medi</em> di riduzione del consumo energetico nel residenziale (tra cui −16% entro il 2030 a livello nazionale), non un obbligo per ogni singola unità di raggiungere una classe prefissata entro una scadenza individuale.</p>
<p>In Italia il recepimento era atteso entro il <strong>29 maggio 2026</strong>; al 23 giugno 2026 restano applicabili le norme nazionali sull'<strong>attestato di prestazione energetica</strong> in compravendita e locazione. Per chi vende nel Padovano nel 2026–2031: nessuna «data di scadenza» che renda illegale cedere un immobile in classe G, ma crescente attenzione del mercato su bollette, mutuo e perizia bancaria.</p>
<h3>Fake news da sfatare</h3>
<p>Non esiste — né è previsto — un divieto di vendere o affittare case in classe energetica bassa dal 2030. Il rischio per chi possiede un immobile energivoro è <strong>economico</strong>: tempi di vendita più lunghi, richieste di ribasso, perizie più conservative, pool di acquirenti finanziati più stretto. È un tema che affrontiamo spesso in consulenza con i proprietari che ci chiedono se conviene ristrutturare prima della messa in vendita.</p>

<h2>Classe energetica e valore: i dati verificabili</h2>
<p>Secondo l'analisi CRIF RES aggiornata a giugno 2025, a livello nazionale:</p>
<ul>
<li>gli immobili in classe <strong>A–B</strong> costano in media circa <strong>500 €/mq in più</strong> rispetto a quelli in classi intermedie (C–E);</li>
<li>il divario con le classi <strong>F–G</strong> si allarga a circa <strong>700 €/mq</strong>;</li>
<li>nei centri urbani lo scarto può superare <strong>1.000 €/mq</strong> tra estremi della scala.</li>
</ul>
<p>Su un appartamento di 90 mq, 700 €/mq equivalgono a <strong>63.000 euro</strong> di distanza teorica — prima di considerare piano, stato, box auto e spese condominiali. È un segnale nazionale da usare come bussola, non come prezzo automatico del tuo immobile: serve una <a href="servizio-valutazioni">valutazione comparativa</a> con annunci venduti e quotazioni <a href="https://www.agenziaentrate.gov.it" target="_blank" rel="noopener noreferrer">OMI</a> della microzona.</p>
<figure style="margin:1.4rem 0">
<img src="img/blog/{INLINE1}" alt="Confronto editoriale tra immobile efficiente e edificio energivoro — Padova" width="960" height="540" loading="lazy" style="width:100%;height:auto;border-radius:10px;border:1px solid var(--gc)">
<figcaption class="cap-img">Illustrazione editoriale — non rappresenta un immobile specifico in vendita.</figcaption>
</figure>

<h2>Tabella: effetti della classe energetica su prezzo e tempi</h2>
<p>La tabella sintetizza tendenze osservate nel mercato nazionale e in agenzia sul Padovano. Le percentuali non sono automaticamente applicabili al singolo caso.</p>
<table>
<thead><tr><th>Classe APE</th><th>Effetto tipico su domanda</th><th>Mutuo / perizia</th><th>Padovano: note operative</th></tr></thead>
<tbody>
<tr><td><strong>A–B</strong></td><td>Pool acquirenti ampio; marketing su efficienza</td><td>Condizioni spesso favorevoli su mutui green</td><td>Premium in centri e nuove costruzioni Limena/Cadoneghe</td></tr>
<tr><td><strong>C–D</strong></td><td>Segmento intermedio più scambiato</td><td>Perizia standard se stato impianti ok</td><td>Molte villette ristrutturate Arcella, Altichiero, Mandria</td></tr>
<tr><td><strong>E–F</strong></td><td>Trattativa su bollette e lavori futuri</td><td>Attenzione a spese e capex</td><td>Appartamenti anni '70–'80: prezzo d'ingresso se zona forte</td></tr>
<tr><td><strong>G</strong></td><td>Acquirente investitore o ristrutturatore</td><td>Perizia prudente; cash o lavori in budget</td><td>Stock campagna e bifamiliari da ripensare</td></tr>
</tbody>
</table>
<p>Il report FIAIP segnala che la polarizzazione tra immobili efficienti e obsoleti tenderà ad accentuarsi con l'avvicinarsi degli obiettivi EPBD. Sul territorio padovano traduciamo questo scenario in scelte concrete: allineare prezzo richiesto, documentazione e messaggio dell'annuncio alla classe energetica reale, senza nascondere costi futuri all'acquirente.</p>

<h2>Posizione geografica: spesso pesa più dell'APE</h2>
<p>Microzona, servizi, collegamenti e offerta concorrente restano i driver primari. A Padova, <strong>Altichiero</strong> e <strong>Mandria</strong> attirano famiglie per verde e tranquillità; <strong>Sacrocuore</strong> e <strong>Arcella</strong> per servizi e domanda consolidata; <strong>Limena</strong>, <strong>Vigonza</strong> e <strong>Albignasego</strong> per chi cerca cintura con prezzi spesso inferiori al capoluogo pur restando vicino alla tangenziale.</p>
<figure style="margin:1.4rem 0">
<img src="img/blog/{INLINE2}" alt="Area Padova — quartieri e contesto urbano per valutazione immobiliare" width="960" height="540" loading="lazy" style="width:100%;height:auto;border-radius:10px;border:1px solid var(--gc)">
<figcaption class="cap-img">Posizione e contesto urbano — rappresentazione concettuale, non catastale.</figcaption>
</figure>
<p>Dove la domanda resta sostenuta e l'offerta è limitata, un immobile in classe E può assorbirsi in pochi mesi se il prezzo è coerente con gli <strong>OMI</strong> e con gli ultimi rogiti comparabili. In zone periferiche o con eccesso di stock simile, invece, anche una classe C può richiedere mesi se il prezzo iniziale è sopra mercato. Per approfondire i rioni: <a href="blog-quartieri-padova-2026">quartieri Padova 2026</a> e schede zona del sito.</p>
<p>La <a href="https://www.bancaditalia.it" target="_blank" rel="noopener noreferrer">Banca d'Italia</a> e l'<a href="https://www.istat.it" target="_blank" rel="noopener noreferrer">ISTAT</a> descrivono un mercato residenziale italiano con andamenti differenziati per area nel 2025–2026. Il Veneto resta tra le regioni con scambi attivi; Padova città e hinterland confermano transazioni regolari (vedi <a href="blog-compravendite-italia-q1-agenzia-entrate-2026-padova">dati compravendite Q1 Agenzia Entrate</a>).</p>""",
    "body_mid": f"""<h2>Orizzonte 2031: cosa aspettarsi</h2>
<p>Entro cinque anni possiamo ragionevolmente prevedere:</p>
<ol>
<li><strong>APE più visibile</strong> in annunci, perizie e comparazioni online tra immobili simili.</li>
<li><strong>Condomini F/G</strong> sotto pressione per interventi sull'involucro, senza bloccare la vendita della singola unità.</li>
<li><strong>Microzone servite</strong> (scuole, tangenziale, verde) che mantengono o aumentano attrattività, come suggeriscono le serie OMI semestrali.</li>
<li><strong>Incentivi</strong> alla riqualificazione — vedi <a href="blog-bonus-edilizi-2026-incentivi-casa-padova">bonus edilizi 2026</a> — utili solo dove il conto economico chiude.</li>
</ol>
<p>Ristrutturare prima di vendere non è obbligatorio. Conviene quando il costo dell'intervento è inferiore al maggiore prezzo ottenibile e al tempo risparmiato; altrimenti è più razionale vendere trasparentemente sullo stato attuale e lasciare al compratore le scelte di efficientamento, eventualmente con <a href="blog-bonus-edilizi-2026-incentivi-casa-padova">detrazioni</a> a suo nome.</p>

<h2>Due esempi dal portafoglio Righetto</h2>
<p>Per rendere concreti i due fattori — energia e posizione — due proposte attive a giugno 2026.</p>

<article style="border:1px solid var(--gc);border-radius:12px;padding:1.2rem 1.3rem;margin:1.5rem 0;background:var(--sfondo)">
<h3 style="margin-top:0;color:var(--blu)">Villetta LP0286 — Altichiero</h3>
<img src="https://qwkwkemuabfwvwuqrxlu.supabase.co/storage/v1/object/public/foto-immobili/1779963017206-casa-singola-altichiero-4-.jpg" alt="Casa singola ristrutturata Altichiero Padova LP0286" width="820" height="340" loading="lazy" style="width:100%;height:auto;border-radius:8px;margin:.8rem 0">
<p><strong>€365.000</strong> · circa <strong>230 mq</strong> · 8 locali · <strong>ristrutturata</strong> · classe <strong>C</strong> (IPE 122,39 kWh/m²a) · garage e giardino · <strong>Altichiero</strong>.</p>
<p>Profilo «pronto abitare» con metrature generose: unisce <strong>quartiere residenziale richiesto</strong> (Padova nord, tangenziale, servizi) a <strong>prestazione energetica intermedia-alta</strong> dopo ristrutturazione. Per l'orizzonte 2031 l'acquirente valuta assenza cantieri, spese prevedibili e confronto con villette F/G da ripensare nella stessa area.</p>
<p><a class="cta-deep" href="immobile?s=villetta-vendita-padova-lp0286">Apri scheda LP0286</a></p>
</article>

<article style="border:1px solid var(--gc);border-radius:12px;padding:1.2rem 1.3rem;margin:1.5rem 0;background:#fff">
<h3 style="margin-top:0;color:var(--blu)">Quadrilocale LA0317 — Mandria</h3>
<img src="https://qwkwkemuabfwvwuqrxlu.supabase.co/storage/v1/object/public/foto-immobili/1777994309447-000-appartamento-2-piano-mandria-padova-righetto-immobiliare-1-wmk-0.jpg" alt="Quadrilocale Mandria Padova LA0317" width="820" height="340" loading="lazy" style="width:100%;height:auto;border-radius:8px;margin:.8rem 0">
<p><strong>€200.000</strong> · circa <strong>90 mq</strong> · 5 locali · secondo piano · <strong>ristrutturato</strong> · classe <strong>E</strong> (IPE 112,53 kWh/m²a) · <strong>Mandria</strong>.</p>
<p>Qui domina la <strong>posizione</strong>: zona tranquilla del comune di Padova, domanda di famiglie e coppie. Ristrutturato per ingresso rapido; la classe E spinge a simulare bollette e interventi leggeri (infissi, pompa di calore) rispetto a un A/B in centro a prezzo superiore. Resta vendibile — la domanda locale lo conferma —; il prezzo finale dipenderà dal confronto con comparabili in <a href="zona-sacra-famiglia-padova">Sacrocuore</a> e dintorni.</p>
<p><a class="cta-deep" href="immobile?s=appartamento-vendita-padova-la0317">Apri scheda LA0317</a></p>
</article>

<p>LP0286 e LA0317 mostrano la stessa regola: <strong>entrambi vendibili</strong>, con leve diverse. La villetta punta su metrature, pertinenze ed energia post-intervento; l'appartamento su prezzo di ingresso, quartiere e finiture, con APE migliorabile. Nessuna scheda garantisce plusvalenza: servono visita, documenti e strategia di prezzo fondata su comparabili.</p>

<h2>Tempi di vendita nel Padovano</h2>
<p>In agenzia osserviamo che l'efficienza energetica incide sui tempi soprattutto quando due immobili simili competono nello stesso quartiere. Un bilocale in <a href="zona-universitaria-padova">zona universitaria</a> in classe mediocre può chiudersi in settimane se il prezzo riflette il canone da locazione studenti; una villa classe G in campagna può restare mesi in vetrina se la domanda è di nicchia.</p>
<p>Fattori che contano quanto l'APE: <strong>allineamento prezzo/OMI</strong>, qualità foto e planimetrie, visibilità dell'attestato in annuncio, assenza di sorprese in perizia mutuo. Per il tema mutuo: <a href="blog-ape-prestazione-energetica-acquisto-padova-2026">APE e acquisto</a> e <a href="landing-mutuo">simulazione</a>.</p>

<h2>Checklist per il proprietario che vende</h2>
<ul>
<li>Leggere l'APE e confrontarlo con comparabili <strong>venduti</strong>, non solo in annuncio.</li>
<li>Verificare microzona con <strong>OMI</strong> e articoli zona del sito.</li>
<li>Stimare costi di efficientamento vs beneficio atteso — con tecnico abilitato.</li>
<li>Scegliere timing: vendere ora con messaggio trasparente, o intervenire con bonus se il conto chiude.</li>
<li>Preparare pacchetto documenti: APE, planimetria, libretti impianti (<a href="blog-documenti-vendita-casa">checklist vendita</a>).</li>
</ul>

<h2>Checklist per l'acquirente</h2>
<ul>
<li>Simulare spesa energetica annua oltre al prezzo di acquisto.</li>
<li>Chiedere preventivi per salto di classe se l'immobile è E/F/G.</li>
<li>Verificare delibere condominiali su lavori energetici.</li>
<li>Valutare mutuo green solo se l'unità rientra nei criteri bancari.</li>
<li>Considerare immobili «brown» come opportunità se il capex è nel budget — con occhio ai <a href="blog-bonus-edilizi-2026-incentivi-casa-padova">bonus</a>.</li>
</ul>""",
    "body_tail": """<h2>Sintesi</h2>
<p>Tra cinque anni la compravendita resterà possibile per quasi tutte le classi energetiche. Il valore seguirà due binari: <strong>quanto costa vivere lì</strong> (bollette, mutuo, condominio) e <strong>dove si trova</strong> (domanda, servizi, concorrenza). CRIF quantifica a livello nazionale distanze fino a 700 €/mq tra green e brown; FIAIP documenta la crescente rilevanza dell'APE nelle valutazioni di mercato; sul Padovano contano microzona e comparabili reali.</p>
<p>Per una valutazione ad Altichiero, Mandria o altrove nel nostro raggio: <a href="landing-valutazione">valutazione gratuita 24h</a> o <a href="landing-consulenza-immobiliare-gratuita">consulenza senza impegno</a>.</p>
<div class="warn"><strong>Fonti:</strong> Direttiva (UE) 2024/1275; CRIF Real Estate Services (giu. 2025); Report FIAIP Monitora Italia 2025 (ENEA, I-Com); OMI Agenzia delle Entrate; Banca d'Italia; ISTAT. I dati €/mq sono nazionali — non sostituiscono perizia o valutazione comparativa sul singolo immobile.</div>""",
    "sources": sources_table([
        ("Divario €/mq green vs brown", "CRIF Real Estate Services, giu. 2025", "Benchmark nazionale in trattativa"),
        ("Polarizzazione classe energetica", "FIAIP Monitora Italia 2025 + ENEA + I-Com", "Contesto di mercato"),
        ("Obiettivi EPBD 2030", "Direttiva (UE) 2024/1275", "Riduzione consumo residenziale media UE"),
        ("Quotazioni microzona", "OMI Agenzia delle Entrate", "Range semestrali per zona"),
        ("Pratica vendite Padova", "Righetto Immobiliare — 101 comuni", "Comparabili e tempi osservati"),
    ]),
    "topic": "",
    "anchors": [],
    "body_n": 0,
    "faqs": [
        (
            "Tra 5 anni potrò vendere una casa in classe G?",
            "Sì. La normativa europea e italiana non prevede divieti di vendita per classi basse; il rischio è economico (tempi e trattativa sul prezzo), non legale.",
        ),
        (
            "Quanto incide la classe energetica sul valore?",
            "CRIF (giu. 2025) stima fino a 700 €/mq di divario tra immobili A–B e F–G in media nazionale; a Padova serve confronto OMI e comparabili reali.",
        ),
        (
            "La posizione può compensare un APE basso?",
            "Spesso sì, in microzone ad alta domanda. Stato manutentivo, prezzo iniziale e concorrenza locale restano determinanti.",
        ),
        (
            "Conviene ristrutturare prima di vendere?",
            "Solo se il costo dell'intervento è inferiore al maggiore prezzo ottenibile e al tempo risparmiato. Altrimenti conviene vendere con trasparenza sullo stato attuale.",
        ),
        (
            "Cosa sono LP0286 e LA0317?",
            "Due immobili in vendita su righettoimmobiliare.it: villetta ristrutturata ad Altichiero (classe C) e quadrilocale a Mandria (classe E).",
        ),
        (
            "Righetto garantisce il valore futuro del mio immobile?",
            "No. Offriamo valutazioni comparative, marketing e assistenza alla vendita; le proiezioni dipendono da mercato, normativa e caratteristiche dell'unità.",
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
        "contenuto": "Vendibile sì, valore legato ad APE e posizione: CRIF, FIAIP, orizzonte 2031 ed esempi LP0286 e LA0317.",
        "evidenza": True,
        "emoji": "🏡",
    },
}


def main() -> int:
    gen_images()
    html, wc = build_article(ARTICLE)
    html = html.replace("rig-lead-form.js?v=3", "rig-lead-form.js?v=3")
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
