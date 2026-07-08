# -*- coding: utf-8 -*-
"""Articolo blog: case più vendute — tipologie e metrature nel Padovano.
python scripts/build_case_piu_vendute_giugno24.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

import build_giugno03_blog_batch as g03  # noqa: E402

g03.DATE_IT = "24 giugno 2026"
g03.DATE_ISO = "2026-06-24"
g03.TIME_TS = "2026-06-24T09:00:00+02:00"

from build_giugno03_blog_batch import (  # noqa: E402
    aeo_box,
    build_article,
    sources_table,
)

ROOT = _SCRIPT_DIR.parent
ASSETS = Path(r"C:\Users\Utente\.cursor\projects\c-Users-Utente-progetti-index\assets")
IMG_DIR = ROOT / "img" / "blog"
HERO = "blog-case-piu-vendute-padova-2026.webp"
INLINE1 = "blog-inline-tipologie-case-vendute-padova-2026.webp"
INLINE2 = "blog-inline-superfici-case-vendute-padova-2026.webp"
SLUG = "blog-case-piu-vendute-tipologie-padova-2026"

LISTINGS = {
    "LA0319": {
        "url": "immobile?s=appartamento-vendita-padova-la0319",
        "foto": "https://qwkwkemuabfwvwuqrxlu.supabase.co/storage/v1/object/public/foto-immobili/1782493221609-000-appartamento-altichiero-primo-piano-16-wmk-0.png",
        "alt": "Quadrilocale con terrazzo Sacro Cuore Padova LA0319",
    },
    "LP0286": {
        "url": "immobile?s=villetta-vendita-padova-lp0286",
        "foto": "https://qwkwkemuabfwvwuqrxlu.supabase.co/storage/v1/object/public/foto-immobili/1779963017206-casa-singola-altichiero-4-.jpg",
        "alt": "Villetta ristrutturata Altichiero Padova LP0286",
    },
    "LP0285-V": {
        "url": "immobile?s=villetta-vendita-grisignano-di-zocco-lp0285-v",
        "foto": "https://qwkwkemuabfwvwuqrxlu.supabase.co/storage/v1/object/public/foto-immobili/1779730032024-casa-singola-piccola-21-.png",
        "alt": "Casa singola da ristrutturare Grisignano di Zocco LP0285-V",
    },
}


def png_to_webp(src: Path, dst: Path, tw: int = 1200, th: int = 630, ay: float = 0.4) -> None:
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
        (ASSETS / "blog-hero-case-piu-vendute-padova-2026.png", IMG_DIR / HERO, 1200, 630, 0.42),
        (ASSETS / "blog-inline-tipologie-case-vendute-padova-2026.png", IMG_DIR / INLINE1, 960, 540, 0.45),
        (ASSETS / "blog-inline-superfici-case-vendute-padova-2026.png", IMG_DIR / INLINE2, 960, 540, 0.5),
    ]:
        if src.is_file():
            png_to_webp(src, dst, w, h, ay)


ARTICLE = {
    "filename": f"{SLUG}.html",
    "slug": SLUG,
    "img": f"img/blog/{HERO}",
    "bread": "Case più vendute Padova",
    "section": "Mercato locale",
    "html_title": "Case più vendute a Padova: tipologie e metrature 2026 | Righetto",
    "og_title": "Quali case si vendono di più nel Padovano? Dati OMI e FIMAA + tre novità in portafoglio",
    "schema_headline": "Case più vendute nel Padovano: tipologie, metrature e domanda nel 2026",
    "meta_desc": "Bilocali, trilocali e fascia 50–85 mq guidano il mercato. Dati OMI 2024 e FIMAA Q1 2026, lettura Padova e novità LA0319, LP0286, LP0285-V.",
    "cat_badge": "Mercato locale",
    "alt_img": "Mercato residenziale Padova — tipologie abitative più richieste, illustrazione editoriale Righetto",
    "breadcrumb_tail": "Case più vendute",
    "h1": "<strong>Case più vendute</strong> nel Padovano: tipologie, metrature e cosa chiede il mercato nel 2026",
    "cap_img": (
        '<p class="cap-img">Illustrazioni <strong>editoriali</strong> Righetto. '
        "Dati numerici con fonte nel testo (OMI, Agenzia delle Entrate, FIMAA). Aggiornato: 24 giugno 2026.</p>"
    ),
    "aeo": aeo_box(
        "Per <strong>acquirenti e venditori nel Padovano</strong> che vogliono capire quali tipologie di casa "
        "assorbono più velocemente il mercato e come posizionare il proprio immobile.",
        [
            "A livello nazionale la fascia <strong>50–85 mq</strong> resta la più intensa nelle compravendite "
            "residenziali (Rapporto OMI 2025 su dati 2024).",
            "Gli agenti FIMAA segnalano <strong>bilocali e trilocali</strong> come unità più richieste nel 2026, "
            "con domanda orientata a spese contenute e servizi di prossimità.",
            "Il segmento <strong>usato</strong> traina gli scambi: poco più del <strong>16%</strong> degli appartamenti "
            "venduti è nuovo (indagine FIMAA).",
            "Nel portafoglio Righetto: <strong>LA0319</strong> (trilocale Sacro Cuore), "
            "<strong>LP0286</strong> (villetta Altichiero), <strong>LP0285-V</strong> (casa da ristrutturare in campagna).",
        ],
        [
            "Non è consulenza investimento — ogni immobile va valutato con comparabili locali.",
            "Non promette tempi di vendita fissi per tipologia senza prezzo e stato reali.",
            "I dati nazionali non sostituiscono quotazioni OMI della singola microzona.",
        ],
    ),
    "body_extra": f"""<h2>Quali case si vendono di più in Italia?</h2>
<p>Il <strong>Rapporto Immobiliare 2025</strong> dell'Osservatorio del Mercato Immobiliare (OMI) dell'<a href="https://www.agenziaentrate.gov.it" target="_blank" rel="noopener noreferrer">Agenzia delle Entrate</a>, basato sui consuntivi 2024, registra <strong>719.578</strong> abitazioni compravendute a livello nazionale, con una crescita dell'<strong>1,3%</strong> rispetto al 2023. La distribuzione per superficie mostra che il segmento tra <strong>50 e 85 metri quadri</strong> concentra la maggiore intensità di mercato (IMI) in tutte le aree geografiche — la fascia che corrisponde, in pratica, a bilocali e trilocali nelle città medio-piccole e alle prime case delle famiglie.</p>
<p>Subito dopo si colloca la banda <strong>85–115 mq</strong>, tipica dei quadrilocali e delle villette compatte. Monolocali e unità oltre i cinque locali restano nicchie: utili in contesti specifici (studenti, investitori, famiglie numerose), ma con pool di acquirenti più ristretto. Questo quadro nazionale si riflette nel Padovano, dove la domanda quotidiana in agenzia punta soprattutto su appartamenti pronti o ristrutturati tra <strong>70 e 110 mq</strong> e su villette in cintura quando il prezzo al metro quadro resta competitivo rispetto al capoluogo.</p>

<h2>Cosa dicono gli agenti FIAA nel 2026</h2>
<p>Il <strong>Sentiment FIMAA Italia-Confcommercio</strong> relativo al primo quadrimestre 2026, riportato da fonti come <a href="https://tg24.sky.it/economia/2026/06/06/mercato-immobiliare-compravendite-prezzi-dati-2026" target="_blank" rel="noopener noreferrer">Sky TG24</a>, prevede compravendite in crescita tra l'<strong>1% e l'1,5%</strong> e prezzi in aumento di circa il <strong>2%</strong>, con transazioni che potrebbero superare le 770.000 registrate nel 2025. Gli operatori segnalano carenza di prodotto nuovo o rigenerato e una domanda spostata verso soluzioni flessibili, costi di gestione contenuti e servizi vicini.</p>
<p>In particolare, <strong>bilocali e trilocali</strong> sono indicati come le tipologie più richieste da lavoratori mobili, studenti, famiglie non più numerose e over 65. L'acquisto della <strong>prima casa</strong> resta il motore principale (circa il <strong>30%</strong> delle operazioni), con mutuo ancora presente in quasi la metà degli acquisti nel primo trimestre 2026 secondo i dati Agenzia delle Entrate commentati nel nostro articolo sulle <a href="blog-compravendite-italia-q1-agenzia-entrate-2026-padova">compravendite Q1</a>.</p>
<figure style="margin:1.4rem 0">
<img src="img/blog/{INLINE1}" alt="Illustrazione editoriale bilocali trilocali quadrilocali — tipologie più richieste" width="960" height="540" loading="lazy" style="width:100%;height:auto;border-radius:10px;border:1px solid var(--gc)">
<figcaption class="cap-img">Rappresentazione concettuale delle tipologie più scambiate — non planimetria catastale.</figcaption>
</figure>

<h2>Tabella: tipologie e domanda nel 2026</h2>
<p>Sintesi da indagini FIMAA e pratica di mercato nel Padovano. Non è una legge automatica per ogni annuncio.</p>
<table>
<thead><tr><th>Tipologia</th><th>Domanda nazionale (FIMAA)</th><th>Padovano: dove la vediamo</th><th>Leva prezzo</th></tr></thead>
<tbody>
<tr><td><strong>Bilocale</strong></td><td>Alta — studenti, coppie, investimento locazione</td><td><a href="zona-universitaria-padova">Zona universitaria</a>, Arcella, centro</td><td>Canone locazione e stato impianti</td></tr>
<tr><td><strong>Trilocale</strong></td><td>Alta — famiglie piccole, smart working</td><td>Sacrocuore, Mandria, Limena</td><td>Terrazzo, luce, classe energetica</td></tr>
<tr><td><strong>Quadrilocale</strong></td><td>Media-alta — famiglie con figli</td><td>Altichiero, Ponte di Brenta, Selvazzano</td><td>Metrature, doppi servizi, box</td></tr>
<tr><td><strong>Villetta / casa singola</strong></td><td>Selezionata — chi cerca spazio e verde</td><td>Altichiero, Sacrocuore, campagna</td><td>Stato (ristrutturato vs da fare), APE</td></tr>
<tr><td><strong>Monolocale / 5+ locali</strong></td><td>Bassa / di nicchia</td><td>Centro (mono), periferia (grandi metrature)</td><td>Prezzo d'ingresso o exclusivity</td></tr>
</tbody>
</table>

<h2>Superficie: la fascia 50–85 mq domina gli scambi</h2>
<p>L'OMI classifica le abitazioni compravendute per classi di superficie. Nel 2024, a livello nazionale, la fascia <strong>50–85 mq</strong> registra l'IMI (indice di mercato immobiliare) più elevato — segnale che proportionally più transazioni avvengono in questa dimensione. Nei capoluoghi l'intensità può salire ulteriormente nelle classi più piccole.</p>
<figure style="margin:1.4rem 0">
<img src="img/blog/{INLINE2}" alt="Illustrazione editoriale fasce di superficie abitativa negli scambi immobiliari" width="960" height="540" loading="lazy" style="width:100%;height:auto;border-radius:10px;border:1px solid var(--gc)">
<figcaption class="cap-img">Visualizzazione concettuale delle fasce mq — fonte numerica: Rapporto OMI 2025.</figcaption>
</figure>
<p>A Padova, un trilocale di <strong>85–95 mq</strong> in quartiere servito resta spesso il «sweet spot» tra budget familiare, mutuo bancabile e costi condominiali gestibili. Villette oltre <strong>180 mq</strong> richiedono acquirente più selettivo: famiglie che cercano giardino e pertinenze, spesso disposte a pagare un premium se l'immobile è <strong>ristrutturato</strong> e in classe energetica difendibile.</p>

<h2>Nuovo, recente o usato: cosa passa di più</h2>
<p>Secondo l'indagine FIMAA citata da <a href="https://www.iconacasa.com/index.php/news/item/890-sondaggio-agenti-fimaa-momento-favorevole-per-comprare-casa" target="_blank" rel="noopener noreferrer">Iconacasa</a>, solo il <strong>16%</strong> degli appartamenti venduti è nuovo; il <strong>31%</strong> è «recente» e circa il <strong>53%</strong> appartiene allo stock più datato. Il mercato dell'usato resta quindi il vero motore — coerente con la scarsità di nuove costruzioni documentata nel Veneto (+14,6% nel segmento nuovo al Q1 2026, ma da base limitata).</p>
<p>Per il venditore padovano significa competere soprattutto con comparabili ristrutturati o «pronti abitare». Per l'acquirente, l'usato da ristrutturare può offrire prezzo d'ingresso inferiore, ma i costi di riqualificazione (33% degli agenti FIMAA li indica come freno) vanno simulati prima del compromesso — vedi <a href="blog-bonus-edilizi-2026-incentivi-casa-padova">bonus edilizi 2026</a>.</p>""",
    "body_mid": f"""<h2>Padova e provincia: tradurre i dati sul territorio</h2>
<p>Il capoluogo e l'hinterland non replicano Milano o Roma, ma condividono la preferenza per <strong>trilocali serviti</strong> e per l'usato riqualificato. Zone come <strong>Sacro Cuore</strong>, <strong>Arcella</strong>, <strong>Mandria</strong> e <strong>Altichiero</strong> concentrano domanda familiare; la cintura (<strong>Limena</strong>, <strong>Vigonza</strong>, <strong>Grisignano di Zocco</strong>) attira chi cerca metrature e scoperto a prezzi inferiori al centro. L'università sostiene bilocali e monolocali in location vicine ai poli — tema affrontato in <a href="blog-affitto-studenti-padova">affitto studenti Padova</a>.</p>
<p>In agenzia, da Limena, osserviamo tre profili ricorrenti tra gli acquirenti che chiudono più rapidamente: coppia con figlio che cerca trilocale con outdoor; famiglia che vuole villetta ristrutturata con giardino; investitore o ristrutturatore che valuta usato da ripensare se il conto lavori chiude. Nessuno di questi profili «garantisce» vendita: servono prezzo allineato agli <strong>OMI</strong>, documentazione e marketing coerente.</p>

<h2>Tre novità in portafoglio: esempi concreti</h2>
<p>Per collegare l'analisi alle proposte appena inserite o aggiornate sul sito — tre immobili che incarnano tipologie diverse ma tutte coerenti con la domanda descritta sopra.</p>

<article style="border:1px solid var(--gc);border-radius:12px;padding:1.2rem 1.3rem;margin:1.5rem 0;background:var(--sfondo)">
<h3 style="margin-top:0;color:var(--blu)">LA0319 — Trilocale con terrazzo, Sacro Cuore</h3>
<img src="{LISTINGS['LA0319']['foto']}" alt="{LISTINGS['LA0319']['alt']}" width="820" height="340" loading="lazy" style="width:100%;height:auto;border-radius:8px;margin:.8rem 0">
<p><strong>€195.000</strong> · circa <strong>90 mq</strong> · 5 locali · piano alto · stato <strong>ottimo</strong> · classe <strong>C</strong> · <strong>Sacro Cuore</strong>, Padova.</p>
<p>Incarna la tipologia più «gettonata» del 2026: <strong>trilocale/quadrilocale</strong> in fascia 85–95 mq, con <strong>ampio terrazzo</strong> e finiture curate. Sacro Cuore offre servizi, collegamenti e domanda consolidata — profilo ideale per famiglie che vogliono outdoor senza villette in campagna. Classe C e stato ottimo riducono il rischio percepito su bollette e lavori immediati.</p>
<p><a class="cta-deep" href="{LISTINGS['LA0319']['url']}">Apri scheda LA0319</a></p>
</article>

<article style="border:1px solid var(--gc);border-radius:12px;padding:1.2rem 1.3rem;margin:1.5rem 0;background:#fff">
<h3 style="margin-top:0;color:var(--blu)">LP0286 — Villetta ristrutturata, Altichiero</h3>
<img src="{LISTINGS['LP0286']['foto']}" alt="{LISTINGS['LP0286']['alt']}" width="820" height="340" loading="lazy" style="width:100%;height:auto;border-radius:8px;margin:.8rem 0">
<p><strong>€365.000</strong> · circa <strong>230 mq</strong> · 8 locali · <strong>ristrutturata</strong> · classe <strong>C</strong> · garage e giardino · <strong>Altichiero</strong>.</p>
<p>Rappresenta il segmento <strong>usato rigenerato</strong>: metrature generose, pronta abitazione, prestazione energetica intermedia dopo interventi. È la risposta per chi supera i 115 mq e cerca privacy — meno liquido del trilocale, ma con domanda stabile in Padova nord quando il prezzo riflette OMI e comparabili venduti.</p>
<p><a class="cta-deep" href="{LISTINGS['LP0286']['url']}">Apri scheda LP0286</a></p>
</article>

<article style="border:1px solid var(--gc);border-radius:12px;padding:1.2rem 1.3rem;margin:1.5rem 0;background:var(--sfondo)">
<h3 style="margin-top:0;color:var(--blu)">LP0285-V — Casa da ristrutturare, Grisignano di Zocco</h3>
<img src="{LISTINGS['LP0285-V']['foto']}" alt="{LISTINGS['LP0285-V']['alt']}" width="820" height="340" loading="lazy" style="width:100%;height:auto;border-radius:8px;margin:.8rem 0">
<p><strong>€110.000</strong> · circa <strong>140 mq</strong> · 6 locali · <strong>da ristrutturare</strong> · classe <strong>F</strong> · ampio scoperto · <strong>Grisignano di Zocco</strong>.</p>
<p>Profilo <strong>stock datato</strong> (53% del mercato FIMAA): prezzo d'ingresso basso, capex da pianificare, appeal per ristrutturatore o famiglia con budget lavori. Classe F richiede simulazione energetica e preventivi prima dell'offerta — ma in campagna padovana resta uno dei modi per accedere a metrature e giardino dove il nuovo è raro.</p>
<p><a class="cta-deep" href="{LISTINGS['LP0285-V']['url']}">Apri scheda LP0285-V</a></p>
</article>

<h2>Come usare questa analisi se vendi o compri</h2>
<h3>Se vendi</h3>
<ul>
<li>Confronta tipologia e mq con la tabella OMI e con annunci <strong>venduti</strong>, non solo in vetrina.</li>
<li>Se hai un trilocale, valorizza terrazzo, luce e APE in foto e descrizione — sono le leve che oggi contano.</li>
<li>Se vendi usato datato, prezzo iniziale trasparente sui lavori evita perdite di tempo in trattativa.</li>
<li>Richiedi una <a href="landing-valutazione">valutazione gratuita</a> allineata ai comparabili reali.</li>
</ul>
<h3>Se compri</h3>
<ul>
<li>Definisci fascia mq e quartiere prima del tour — evita dispersione su monolocali e grandi villette se non servono.</li>
<li>Simula mutuo e costi totali: trilocale classe C vs da ristrutturare classe F.</li>
<li>Visita le schede LA0319, LP0286 e LP0285-V come esempi di tre strategie di acquisto diverse.</li>
</ul>

<h2>Trend 2026 da monitorare</h2>
<p>Oltre a tipologia e superficie, tre fattori modulano tempi e prezzo nel Padovano:</p>
<ol>
<li><strong>Classe energetica</strong> — polarizzazione green/brown (vedi <a href="blog-casa-vendibile-5-anni-case-green-padova-2026">casa vendibile tra 5 anni</a>).</li>
<li><strong>Outdoor</strong> — terrazzi e giardini post-pandemia restano discriminanti nelle visite.</li>
<li><strong>Mutuo selettivo</strong> — banche prudenti su immobili energivori o con difformità (vedi <a href="blog-mutui-selettivi-banche-padova-2026">mutui selettivi</a>).</li>
</ol>
<p>Il Q1 2026 ha mostrato +4,4% compravendite in Italia: se la tendenza FIMAA si conferma, il 2026 resterà un anno di scambi attivi, soprattutto sulle tipologie medie che questo articolo riassume.</p>""",
    "body_tail": """<h2>Sintesi</h2>
<p>Le <strong>case più vendute</strong> in Italia nel 2024–2026 non sono villette di lusso né monolocali d'élite: sono soprattutto abitazioni tra <strong>50 e 115 mq</strong>, con <strong>bilocali e trilocali</strong> in testa alle preferenze FIMAA. L'<strong>usato</strong> domina gli scambi; ristrutturato o con outdoor competitivo assorbe più velocemente. A Padova, Sacro Cuore, Altichiero e la campagna immediata offrono esempi concreti — come LA0319, LP0286 e LP0285-V nel nostro portafoglio.</p>
<p>Per orientamento personalizzato: <a href="landing-consulenza-immobiliare-gratuita">consulenza gratuita</a> o <a href="immobili">sfoglia il catalogo</a>.</p>
<div class="warn"><strong>Fonti:</strong> Rapporto Immobiliare 2025 OMI (Agenzia delle Entrate, consuntivo 2024); Sentiment FIMAA Q1 2026; dati compravendite Q1 2026 Agenzia delle Entrate. Percentuali nazionali — non sostituiscono valutazione sul singolo immobile.</div>""",
    "sources": sources_table([
        ("Volume compravendite 2024", "OMI — Rapporto Immobiliare 2025", "719.578 abitazioni, +1,3%"),
        ("Fasce di superficie", "OMI — distribuzione IMI 2024", "50–85 mq massima intensità"),
        ("Tipologie richieste 2026", "FIMAA Sentiment Q1 2026", "Bilocali e trilocali in testa"),
        ("Nuovo vs usato", "Indagine agenti FIMAA", "16% nuovo, 53% stock datato"),
        ("Compravendite Q1 2026", "Agenzia delle Entrate", "+4,4% trimestre"),
    ]),
    "topic": "",
    "anchors": [],
    "body_n": 0,
    "faqs": [
        (
            "Qual è la tipologia di casa più venduta in Italia?",
            "Bilocali e trilocali sono le più richieste nel 2026 secondo FIMAA; per superficie domina la fascia 50–85 mq (OMI 2024).",
        ),
        (
            "A Padova conviene vendere un trilocale o una villetta?",
            "Il trilocale in quartiere servito assorbe in genere più rapidamente; la villetta richiede prezzo coerente e target famiglie — dipende da microzona e stato.",
        ),
        (
            "Quanto pesa l'usato sul mercato?",
            "Circa il 53% degli appartamenti venduti è classificato come stock datato; solo il 16% è nuovo (FIMAA).",
        ),
        (
            "Cosa sono LA0319, LP0286 e LP0285-V?",
            "Tre immobili attivi su righettoimmobiliare.it: trilocale Sacro Cuore, villetta Altichiero e casa da ristrutturare a Grisignano.",
        ),
        (
            "Il terrazzo fa aumentare le chance di vendita?",
            "Nel 2026 outdoor e spazi esterni sono leve forti su trilocali in città — non garantiscono prezzo premium automatico senza comparabili.",
        ),
        (
            "Righetto garantisce la vendita in X mesi?",
            "No. Offriamo valutazione, marketing e assistenza; i tempi dipendono da prezzo, tipologia, stato e domanda locale.",
        ),
    ],
    "related": [
        ("Compravendite Q1 2026 Padova", "blog-compravendite-italia-q1-agenzia-entrate-2026-padova"),
        ("Quartieri Padova 2026", "blog-quartieri-padova-2026"),
        ("Case in vendita Padova", "blog-case-vendita-padova"),
    ],
    "cta_primary": ("Valutazione gratuita", "landing-valutazione"),
    "cta_secondary": ("Vedi immobili", "immobili"),
    "registry": {
        "titolo": "Case più vendute nel Padovano: tipologie e metrature nel 2026",
        "categoria": "Mercato locale",
        "tempo": 13,
        "contenuto": "Dati OMI e FIMAA su tipologie e mq più scambiati, lettura Padova e novità LA0319, LP0286, LP0285-V.",
        "evidenza": True,
        "emoji": "📊",
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
    reg_path = ROOT / "scripts" / "case_piu_vendute_registry.json"
    reg_path.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Registry: {reg_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
