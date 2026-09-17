# -*- coding: utf-8 -*-
"""Rebuild blog mutuo under 36 + zona Imma — template standard (no scroll 3D).
python scripts/rebuild_blog_3d_standard_sep14.py
"""
from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATE_IT = "14 settembre 2026"
DATE_ISO = "2026-09-14"
TIME_TS = "2026-09-14T10:00:00+02:00"

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
_batch.STYLE_BLOCK = _batch.STYLE_BLOCK + CHART_WRAP_CSS

wc = _batch.wc
aeo_box = _batch.aeo_box
sol_box = _batch.sol_box
faq_html = _batch.faq_html
build_html = _batch.build_html
CLAIM_FOOT = _batch.CLAIM_FOOT
OMI_URL = _batch.OMI_URL
ISTAT_URL = _batch.ISTAT_URL
ADE_OSSERVATORIO = _batch.ADE_OSSERVATORIO
MIN_BODY_WORDS = _batch.MIN_BODY_WORDS
CAP_BLOG_AI = _batch.CAP_BLOG_AI


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


def svg_fisso_variabile() -> str:
    return """<figure class="chart-wrap" aria-label="Schema fisso vs variabile mutuo under 36">
<svg viewBox="0 0 820 320" width="100%" height="280" role="img">
<title>Fisso vs variabile — schema decisionale under 36</title>
<text x="410" y="36" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Fisso vs variabile — schema decisionale under 36</text>
<text x="410" y="58" text-anchor="middle" font-size="11" fill="#6B7A8D">Illustrazione editoriale Righetto — non simulazione rata</text>
<line x1="80" y1="260" x2="760" y2="260" stroke="#2C4A6E" stroke-width="2"/>
<line x1="80" y1="260" x2="80" y2="80" stroke="#2C4A6E" stroke-width="2"/>
<text x="420" y="290" text-anchor="middle" font-size="12" fill="#152435">Prevedibilità rata →</text>
<rect x="120" y="120" width="140" height="140" rx="8" fill="#4a90d9" opacity=".88"/>
<text x="190" y="175" text-anchor="middle" fill="#fff" font-size="14" font-weight="700">FISSO</text>
<text x="190" y="200" text-anchor="middle" fill="#fff" font-size="11">Rata stabile</text>
<text x="190" y="218" text-anchor="middle" fill="#c9e4ff" font-size="10">IRS + spread</text>
<rect x="340" y="140" width="140" height="120" rx="8" fill="#ff6b35" opacity=".88"/>
<text x="410" y="195" text-anchor="middle" fill="#152435" font-size="14" font-weight="700">VARIABILE</text>
<text x="410" y="218" text-anchor="middle" fill="#152435" font-size="11">Rata oscillante</text>
<text x="410" y="236" text-anchor="middle" fill="#152435" font-size="10">Euribor + spread</text>
<rect x="560" y="160" width="140" height="100" rx="8" fill="#c9a84c" opacity=".85"/>
<text x="630" y="205" text-anchor="middle" fill="#152435" font-size="13" font-weight="600">CONSAP</text>
<text x="630" y="225" text-anchor="middle" fill="#152435" font-size="10">Garanzia pubblica</text>
</svg>
<figcaption>Il CONSAP riduce il rischio per la banca, non elimina la scelta tra fisso e variabile.</figcaption>
</figure>"""


def svg_percorso_mutuo() -> str:
    return """<figure class="chart-wrap" aria-label="Timeline percorso mutuo under 36 2027">
<svg viewBox="0 0 820 200" width="100%" height="200" role="img">
<title>Percorso under 36 — ordine consigliato</title>
<line x1="60" y1="100" x2="760" y2="100" stroke="#E1DBD1" stroke-width="3"/>
<circle cx="140" cy="100" r="10" fill="#4a90d9"/>
<text x="140" y="135" text-anchor="middle" font-size="11" fill="#152435" font-weight="600">Preventivo</text>
<circle cx="300" cy="100" r="10" fill="#2C4A6E"/>
<text x="300" y="135" text-anchor="middle" font-size="11" fill="#152435" font-weight="600">Fisso/Var</text>
<circle cx="460" cy="100" r="10" fill="#c9a84c"/>
<text x="460" y="135" text-anchor="middle" font-size="11" fill="#152435" font-weight="600">CONSAP</text>
<circle cx="620" cy="100" r="12" fill="#ff6b35"/>
<text x="620" y="135" text-anchor="middle" font-size="11" fill="#152435" font-weight="700">Immobile</text>
<text x="410" y="30" text-anchor="middle" font-family="Cormorant Garamond, serif" font-size="20" fill="#2C4A6E">Percorso under 36 — ordine consigliato</text>
<text x="410" y="175" text-anchor="middle" font-size="10" fill="#6B7A8D">Prima il mutuo, poi la casa — non il contrario</text>
</svg>
<figcaption>Sequenza operativa consigliata nel Padovano: pre-qualificazione, scelta tasso, verifica CONSAP, ricerca immobile.</figcaption>
</figure>"""


def svg_domanda_offerta_imma() -> str:
    return """<figure class="chart-wrap" aria-label="Grafico domanda e offerta zona Imma Limena">
<svg viewBox="0 0 820 320" width="100%" height="280" role="img">
<title>Squilibrio qualitativo — zona Imma / Limena (2026)</title>
<text x="410" y="36" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">Squilibrio qualitativo — zona Imma / Limena (2026)</text>
<text x="410" y="58" text-anchor="middle" font-size="11" fill="#6B7A8D">Illustrazione editoriale Righetto — non dato ISTAT</text>
<line x1="80" y1="260" x2="760" y2="260" stroke="#2C4A6E" stroke-width="2"/>
<line x1="80" y1="260" x2="80" y2="80" stroke="#2C4A6E" stroke-width="2"/>
<text x="420" y="290" text-anchor="middle" font-size="12" fill="#152435">Intensità di mercato →</text>
<rect x="140" y="180" width="120" height="80" rx="6" fill="#2C4A6E" opacity=".85"/>
<text x="200" y="225" text-anchor="middle" fill="#fff" font-size="13" font-weight="600">Offerta</text>
<text x="200" y="245" text-anchor="middle" fill="#c9a84c" font-size="11">limitata</text>
<rect x="380" y="100" width="120" height="160" rx="6" fill="#FF6B35" opacity=".88"/>
<text x="440" y="175" text-anchor="middle" fill="#152435" font-size="13" font-weight="700">Domanda</text>
<text x="440" y="195" text-anchor="middle" fill="#152435" font-size="11">elevata</text>
<rect x="560" y="140" width="120" height="120" rx="6" fill="#c9a84c" opacity=".75"/>
<text x="620" y="195" text-anchor="middle" fill="#152435" font-size="12" font-weight="600">Prezzi</text>
<text x="620" y="215" text-anchor="middle" fill="#152435" font-size="11">in tensione</text>
</svg>
<figcaption>Schema concettuale: pochi annunci in fascia accessibile vs domanda strutturale da famiglie e pendolari padovani.</figcaption>
</figure>"""


def svg_outlook_imma() -> str:
    return """<figure class="chart-wrap" aria-label="Timeline outlook mercato Limena 2026-2027">
<svg viewBox="0 0 820 200" width="100%" height="200" role="img">
<title>Outlook qualitativo — Limena / zona Imma</title>
<line x1="60" y1="100" x2="760" y2="100" stroke="#E1DBD1" stroke-width="3"/>
<circle cx="180" cy="100" r="10" fill="#2C4A6E"/>
<text x="180" y="135" text-anchor="middle" font-size="12" fill="#152435" font-weight="600">2026</text>
<text x="180" y="155" text-anchor="middle" font-size="10" fill="#6B7A8D">Domanda &gt; offerta</text>
<circle cx="420" cy="100" r="10" fill="#c9a84c"/>
<text x="420" y="135" text-anchor="middle" font-size="12" fill="#152435" font-weight="600">H2 2026</text>
<text x="420" y="155" text-anchor="middle" font-size="10" fill="#6B7A8D">Nuovi cantieri in vendita</text>
<circle cx="640" cy="100" r="12" fill="#FF6B35"/>
<text x="640" y="135" text-anchor="middle" font-size="12" fill="#152435" font-weight="700">2027</text>
<text x="640" y="155" text-anchor="middle" font-size="10" fill="#6B7A8D">Consegne · domanda ancora alta*</text>
<text x="410" y="30" text-anchor="middle" font-family="Cormorant Garamond, serif" font-size="20" fill="#2C4A6E">Outlook qualitativo — Limena / zona Imma</text>
<text x="410" y="185" text-anchor="middle" font-size="10" fill="#6B7A8D">*Previsione editoriale — non previsione OMI</text>
</svg>
<figcaption>Proiezione qualitativa: tensione sulle fasce medie anche con nuove consegne edilizie nel comune.</figcaption>
</figure>"""


def body_mutuo_under36() -> str:
    return f"""
{aeo_box("In sintesi", "<strong>Mutuo under 36 nel 2027:</strong> incrociare <strong>garanzia CONSAP</strong> (prorogata al 31/12/2027), <strong>contesto tassi BCE</strong> e scelta <strong>fisso vs variabile</strong>. Non pubblichiamo TAEG online — verificare sempre il foglio informativo bancario. Integra le guide su <a href=\"blog-prima-casa-under-36-consap-padova-2026\">CONSAP</a>, <a href=\"blog-mutuo-fisso-variabile-padova-2026\">fisso/variabile</a> e <a href=\"blog-tassi-euribor-mutui-padova-agosto-2026\">Euribor</a>.")}

<p><strong>Risposta diretta:</strong> se hai meno di 36 anni e compri la prima casa nel Padovano, nel 2027 devi incrociare tre fili: la <strong>garanzia CONSAP</strong> (prorogata al 31/12/2027), il <strong>contesto tassi</strong> guidato da BCE e mercato interbancario, e la scelta tra <strong>mutuo fisso</strong> (rata prevedibile) e <strong>variabile</strong> (legato a Euribor + spread). Non esiste una risposta universale: dipende da reddito, durata, liquidità e tolleranza al rischio.</p>

<p><strong>Distinzione editoriale:</strong> <em>Fatto</em> — norme CONSAP, bonus fiscale scaduto, fonti BCE/Banca d'Italia. <em>Analisi</em> — framework operativo Righetto per under 36 nel Padovano. <em>Previsione</em> — outlook 2027 su costo credito e domanda prima casa, non certezza sui tassi.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#perimetro">Chi rientra nel perimetro under 36</a></li>
<li><a href="#strumenti">Cosa resta attivo e cosa no</a></li>
<li><a href="#contesto-tassi">Tassi in aumento: cosa significa</a></li>
<li><a href="#fisso-variabile">Fisso o variabile: framework</a></li>
<li><a href="#consap">CONSAP nel mix</a></li>
<li><a href="#sequenza">Sequenza operativa 2027</a></li>
<li><a href="#cintura">Padova, Limena e cintura</a></li>
<li><a href="#errori">Errori frequenti</a></li>
<li><a href="#outlook-2027">Outlook 2027</a></li>
</ol></nav>

<div class="kpi-strip" aria-label="Contesto mutuo under 36">
<div><strong>31/12/2027</strong><span>CONSAP attivo</span></div>
<div><strong>80%</strong><span>Copertura max*</span></div>
<div><strong>BCE</strong><span>Fonte tassi</span></div>
<div><strong>TAEG</strong><span>Solo in banca</span></div>
</div>
<p style="font-size:.72rem;color:var(--grigio)">*Garanzia CONSAP — Legge 207/2024, requisiti under 36 e prima casa.</p>

{sol_box("Under 36: come scelgo mutuo e immobile nel Padovano?", [
    ("Consulenza mutuo", "Orientamento su documenti, tempi e coordinamento banca", "servizio mutuo", "servizio-mutuo"),
    ("Prima casa CONSAP", "Requisiti garanzia e percorso documentale", "CONSAP under 36", "blog-prima-casa-under-36-consap-padova-2026"),
    ("Ricerca immobile", "Trilocali e cintura Padova con budget verificato", "immobili vendita", "immobili?op=vendita"),
    ("Consulenza gratuita", "Valutazione percorso acquisto e mutuo", "landing consulenza", "landing-consulenza-immobiliare-gratuita"),
])}

<h2>Perché questo articolo è diverso dagli altri sul mutuo</h2>
<p>Sul sito Righetto esistono già tre pezzi verticali: <a href="blog-prima-casa-under-36-consap-padova-2026">CONSAP e requisiti under 36</a>, <a href="blog-mutuo-fisso-variabile-padova-2026">confronto fisso vs variabile con simulazioni</a>, <a href="blog-tassi-euribor-mutui-padova-agosto-2026">Euribor e mutui a Padova</a>. Qui uniamo i tre fili in un <strong>percorso decisionale</strong> per chi deve scegliere nel 2027.</p>
<p>L'angolo è pratico: non «quale tasso conviene oggi» (non lo promettiamo online), ma <em>in che ordine</em> affrontare budget, tipo mutuo, garanzia e ricerca immobile nel Padovano.</p>

{blog_fig("img/blog/blog-mutuo-under-36-tassi-fisso-variabile-2027-consap.webp", "Mutuo prima casa under 36 Padova — garanzia CONSAP e percorso bancario")}

<h2 id="perimetro">Chi rientra nel perimetro under 36</h2>
<p>Per la garanzia CONSAP e per molte misure «giovani», la soglia è aver compiuto 36 anni alla data del rogito o del contratto preliminare — verificare sempre il testo normativo aggiornato e la circolare CONSAP. Requisiti tipici: prima casa, residenza in Italia, ISEE entro le soglie previste, assenza di altre proprietà abitative in quota rilevante.</p>
<p>La banca valuta comunque il merito creditizio: CONSAP copre fino all'80% del mutuo ma non sostituisce la valutazione del reddito, del rapporto rata/reddito e della perizia sull'immobile. Per il percorso documentale completo, vedi anche <a href="blog-mutuo-documenti-tempi-prima-casa-padova-2026">mutuo prima casa: documenti e tempi</a>.</p>

<h2 id="strumenti">Cosa resta attivo e cosa no (2026–2027)</h2>
<table>
<caption>Strumenti under 36 — stato al 2026</caption>
<thead><tr><th>Strumento</th><th>Stato</th><th>Nota operativa</th></tr></thead>
<tbody>
<tr><td>Garanzia CONSAP under 36</td><td>Attiva fino 31/12/2027</td><td>Legge 207/2024 — richiesta tramite banca</td></tr>
<tr><td>Bonus fiscale under 36 acquisto</td><td>Scaduto 31/12/2024</td><td>Non confondere con CONSAP</td></tr>
<tr><td>Detrazioni ristrutturazione / bonus edilizi</td><td>Verificare normativa vigente</td><td>Vedi <a href="blog-bonus-edilizi-2026-incentivi-casa-padova">bonus edilizi 2026</a></td></tr>
<tr><td>Imposte prima casa</td><td>Agevolazioni ordinarie se requisiti</td><td>Conferma con commercialista/notaio</td></tr>
</tbody>
</table>

<h2 id="contesto-tassi">Tassi in aumento (o comunque «alti»): cosa significa per te</h2>
<p>Dopo il ciclo di rialzo avviato dalla BCE per contrastare l'inflazione, il costo del denaro è tornato al centro delle decisioni delle famiglie. Non pubblichiamo qui valori puntuali di Euribor, IRS o TAEG: cambiano continuamente e ogni banca applica spread diversi. Le fonti corrette sono il foglio informativo del mutuo, la <a href="https://www.ecb.europa.eu/stats/policy_and_exchange_rates/key_ecb_interest_rates/html/index.en.html" target="_blank" rel="noopener noreferrer">BCE</a> per i tassi di riferimento e la <a href="https://www.bancaditalia.it/pubblicazioni/indagine-fam-imprese/index.html" target="_blank" rel="noopener noreferrer">Banca d'Italia</a> per l'andamento del credito alle famiglie.</p>
<p>Per un mutuo <strong>variabile</strong>, la rata si aggiorna seguendo l'indice contrattuale (spesso Euribor 3 mesi) più lo spread. Per un mutuo <strong>fisso</strong>, il tasso resta bloccato per la durata concordata, con rata nota fin dall'inizio — utile per pianificare il budget familiare.</p>
<p>In un contesto in cui i tassi di riferimento sono sensibilmente più alti rispetto al minimo storico del 2020–2021, l'effetto marginale di ogni oscillazione pesa di più su chi finanzia l'80–90% del prezzo e ha poco risparmio oltre al mutuo.</p>

{svg_fisso_variabile()}

<h2>Perché i tassi pesano di più sugli under 36</h2>
<p>Quattro motivi ricorrenti in agenzia, allineati ai dati macro della Banca d'Italia sul credito alle famiglie:</p>
<ol>
<li><strong>Reddito medio più basso</strong> — il rapporto rata/reddito è più vicino ai limiti bancari; poco margine per assorbire revisioni al rialzo.</li>
<li><strong>Anticipo limitato</strong> — LTV più alto significa capitale finanziato maggiore: a parità di punti percentuali, l'impatto in euro sulla rata è più forte.</li>
<li><strong>Orizzonte incerto</strong> — carriera, trasferimenti, nascita figli: un variabile «conveniente oggi» può diventare stressante in 24 mesi.</li>
<li><strong>Competizione sul mercato</strong> — nel Padovano la domanda residenziale resta sostenuta (<a href="blog-domanda-residenziale-supera-offerta-2026-padova">domanda vs offerta 2026</a>); ritardare l'acquisto per «aspettare tassi più bassi» può significare perdere l'immobile giusto.</li>
</ol>

{blog_fig("img/blog/blog-mutuo-under-36-tassi-fisso-variabile-2027-tassi.webp", "Contesto tassi mutuo Padova — decisione fisso o variabile under 36")}

<h2 id="fisso-variabile">Tasso fisso o variabile: framework per decidere</h2>
<p>Non esiste la scelta «giusta» in assoluto. Esiste la scelta coerente con il tuo profilo. Il confronto tecnico con simulazioni di rata su trilocale padovano è in <a href="blog-mutuo-fisso-variabile-padova-2026">mutuo fisso o variabile 2026</a>; qui riassumiamo il framework operativo.</p>

<h3>Quando valutare il fisso</h3>
<ul>
<li>Reddito essenzialmente fisso (dipendente pubblico/privato stabile).</li>
<li>Poco risparmio oltre al fondo emergenze — non reggi revisioni +50–100 €/mese.</li>
<li>Durata lunga (25–30 anni) e avversione al rischio.</li>
<li>Vuoi allineare rata mutuo e pianificazione familiare senza sorprese.</li>
</ul>

<h3>Quando valutare il variabile</h3>
<ul>
<li>Reddito in crescita o variabile ma con bonus/significativi margini.</li>
<li>Liquidità per coprire almeno 12–24 mesi di possibile rialzo rata (stress test personale).</li>
<li>Orizzonte di detenzione medio-breve (5–10 anni) con possibile estinzione anticipata.</li>
<li>Accetti di monitorare Euribor e BCE — vedi <a href="blog-tassi-euribor-mutui-padova-agosto-2026">guida Euribor</a>.</li>
</ul>

<h3>Soluzioni ibride</h3>
<p>Molte banche propongono mutui a tasso fisso per i primi anni e variabile dopo, o viceversa. Vanno confrontate sul <strong>TAEG</strong> e sulle penali di estinzione anticipata, non solo sulla rata iniziale. Chiedi sempre il piano di ammortamento completo e lo scenario «peggiore plausibile» per il variabile.</p>

<table>
<caption>Confronto operativo fisso vs variabile</caption>
<thead><tr><th>Criterio</th><th>Fisso</th><th>Variabile</th></tr></thead>
<tbody>
<tr><td>Prevedibilità rata</td><td>Alta</td><td>Bassa — segue indice</td></tr>
<tr><td>Riferimento tipico</td><td>IRS + spread</td><td>Euribor + spread</td></tr>
<tr><td>Rischio rialzo tassi</td><td>Assorbito dalla banca (nel periodo fisso)</td><td>A carico mutuatario</td></tr>
<tr><td>Adatto se budget stretto</td><td>Spesso sì</td><td>Solo con cuscinetto liquido</td></tr>
<tr><td>Fonte condizioni</td><td>Foglio informativo banca</td><td>Foglio informativo banca</td></tr>
</tbody>
</table>

<h2 id="consap">CONSAP nel mix: cosa cambia (e cosa no)</h2>
<p>La garanzia del Fondo CONSAP per under 36 permette alla banca di erogare mutui con copertura pubblica fino all'80% dell'importo, a condizioni che il mutuatario rispetti i requisiti. In pratica può facilitare l'accesso al credito e, in alcuni casi, condizioni più favorevoli — ma la banca resta libera di pricing e merito creditizio.</p>
<p><strong>CONSAP non sceglie al posto tuo</strong> tra fisso e variabile. Non sostituisce la perizia: se l'immobile è valutato sotto il prezzo di acquisto, il gap va coperto con equity aggiuntiva. Per approfondire requisiti e tempi, rimandiamo alla guida dedicata <a href="blog-prima-casa-under-36-consap-padova-2026">prima casa under 36 CONSAP Padova</a>.</p>

{blog_fig("img/blog/blog-mutuo-under-36-tassi-fisso-variabile-2027-percorso.webp", "Percorso mutuo under 36 — preventivo banca e ricerca immobile Padova")}

<h2 id="sequenza">Sequenza operativa consigliata (2027)</h2>
<p>Ordine che usiamo in sede con acquirenti under 36 nel Padovano:</p>
<ol>
<li><strong>Pre-qualificazione mutuo</strong> — due preventivi scritti con TAEG, durata, tipo tasso, assicurazioni obbligatorie/volontarie (<a href="servizio-mutuo">servizio mutuo</a>).</li>
<li><strong>Calcolo budget reale</strong> — rata + spese condominiali + IMU eventuale + manutenzione + trasporti (Limena vs Padova centro: <a href="blog-limena-vs-padova-centro-dove-comprare-2026">confronto zone</a>).</li>
<li><strong>Scelta fisso/variabile</strong> — con stress test personale, non con titoli di giornale.</li>
<li><strong>Verifica CONSAP</strong> — età, ISEE, prima casa, documenti.</li>
<li><strong>Ricerca immobile</strong> — solo dopo i punti 1–4; evita compromessi su immobili fuori perizia (<a href="blog-checklist-verifiche-prima-compromesso-padova-2026">checklist pre-compromesso</a>).</li>
<li><strong>Perizia e rogito</strong> — timeline in <a href="blog-mutuo-documenti-tempi-prima-casa-padova-2026">documenti e tempi mutuo</a>.</li>
</ol>

{svg_percorso_mutuo()}

<h2 id="cintura">Padova, Limena e prima cintura: implicazioni pratiche</h2>
<p>Nel Padovano un trilocale in cintura (Limena, Vigonza, Rubano) spesso offre metrature superiori a parità di rata rispetto al centro — ma va calcolato il costo totale mensile inclusi spostamenti. Per profili under 36 pendolari, la cintura resta attrattiva se il mutuo è sostenibile sul lungo periodo, non solo al primo preventivo.</p>
<p>Le quotazioni ufficiali per il confronto prezzo/perizia sono nelle tabelle <a href="{OMI_URL}" target="_blank" rel="noopener noreferrer">OMI dell'Agenzia delle Entrate</a>, aggiornate semestralmente. Per Limena e zone limitrofe, vedi anche <a href="zona-limena">scheda zona Limena</a> e <a href="blog-zona-imma-limena-domanda-offerta-2027">mercato zona Imma</a>.</p>

<h2>Stress test personale e merito creditizio bancario</h2>
<p>La banca non valuta solo il tasso che preferisci: applica <strong>stress test</strong> sul rapporto rata/reddito e su scenari di rialzo per i mutui variabili. Anche con CONSAP attivo, un reddito instabile o un LTV oltre soglia interna può ridurre l'importo erogabile. Portate in filiale buste paga recenti, CUD/730, estratto conto senza insoluti e — se applicabile — documentazione ISEE per la garanzia giovani.</p>
<p>Due preventivi scritti da banche diverse non sono «optional»: permettono di confrontare TAEG, costi assicurativi obbligatori, penali di estinzione anticipata e tempi di perizia. Chiedete esplicitamente se il mutuo include polizze vita/incendio/scoppio obbligatorie e quanto incidono sul costo totale. Righetto non negozia spread al posto vostro, ma aiuta a incrociare massimale mutuo e prezzo immobile prima di firmare un compromesso.</p>

<h3>Perizia, LTV e gap di prezzo</h3>
<p>Se l'immobile è periziato sotto il prezzo di acquisto, la banca finanzia sul minore tra prezzo e perizia (salvo eccezioni contrattuali). Il gap va coperto con equity aggiuntiva — problema frequente su annunci «sostenibili» in cintura dove la domanda spinge il listino sopra comparabili chiusi. Incrociate sempre <a href="{OMI_URL}" target="_blank" rel="noopener noreferrer">OMI</a> e perizia bancaria prima dell'offerta vincolante.</p>
<p>Per trilocali Limena/Vigonza/Rubano, la perizia considera stato conservativo, APE, pertinenze e microzona OMI del comune — non la singola via Imma. Un box documentato con subalterno catastale può migliorare il profilo dell'immobile agli occhi dell'istituto di credito.</p>

<h3>Assicurazioni e costi «nascosti» del mutuo</h3>
<p>Oltre al tasso nominale, controllate nel foglio informativo: spese istruttoria, perizia, imposta sostitutiva, polizze obbligatorie, costi di gestione pratica. Su un orizzonte 25–30 anni, differenze apparentemente piccole sul TAEG si traducono in migliaia di euro. Non confrontate solo la rata del primo mese.</p>

<h2 id="errori">Cosa evitare (errori frequenti under 36)</h2>
<ul>
<li><strong>Fissare il compromesso prima del mutuo</strong> — clausola sospensiva mal scritta o assente = rischio caparra.</li>
<li><strong>Credere ai tassi «da sito»</strong> — TAEG reale solo in banca, con il tuo profilo.</li>
<li><strong>Confondere CONSAP e bonus fiscale</strong> — strumenti diversi, uno attivo e uno scaduto.</li>
<li><strong>Scegliere variabile senza stress test</strong> — simula +100 €/mese e chiediti se reggi 24 mesi così.</li>
<li><strong>Trascurare spese accessorie</strong> — notaio, imposte, arredo, impianti: vedi <a href="blog-costi-proprieta-acquisto-possesso-vendita-padova-2026">costi acquisto e possesso</a>.</li>
<li><strong>Ignorare il costo totale mensile</strong> — rata + condominio + trasporti + manutenzione; la cintura «conveniente» può non esserlo se pendolarismo costa.</li>
<li><strong>Non leggere il piano di ammortamento</strong> — capire quota capitale vs interessi nei primi anni evita sorprese in estinzione anticipata.</li>
</ul>

<h2>Domande da fare in banca (checklist under 36)</h2>
<ol>
<li>TAEG completo e durata esatta del tasso fisso (se scelto).</li>
<li>Indice di riferimento, spread e frequenza revisione (se variabile).</li>
<li>Compatibilità con garanzia CONSAP e documenti ISEE richiesti.</li>
<li>Penali estinzione anticipata e possibilità di rinegoziazione.</li>
<li>Tempi medi perizia e erogazione sul comune di acquisto (Limena/Padova).</li>
<li>Assicurazioni obbligatorie vs facoltative — impatto su rata.</li>
</ol>
<p>Approfondimenti verticali già sul sito: <a href="blog-mutuo-documenti-tempi-prima-casa-padova-2026">documenti e tempi</a>, <a href="blog-comprare-casa-padova-guida-2026">guida acquisto Padova</a>, <a href="blog-checklist-verifiche-prima-compromesso-padova-2026">checklist pre-compromesso</a>.</p>

<h2 id="outlook-2027">Outlook 2027: previsione editoriale</h2>
<p><strong>Previsione (analisi Righetto, settembre 2026):</strong> nel 2027 il segmento under 36 nel Padovano resterà attivo grazie a CONSAP e alla domanda di prima casa in cintura. Il costo del credito dipenderà dal ciclo BCE — non pronosticabile con certezza qui. Chi entra nel mercato con mutuo pre-approvato e tipo tasso scelto consapevolmente avrà vantaggio competitivo sulle trattative rispetto a chi cerca casa «a sentimento» senza budget verificato.</p>
<p>Scenario alternativo: un allentamento monetario europeo potrebbe rendere il variabile più competitivo; un nuovo tightening lo renderebbe più rischioso. Monitorare comunicazioni BCE e preventivi bancari trimestrali, non blog generici.</p>

<h2>Mutuo e trattativa immobiliare: tempi da sincronizzare</h2>
<p>Un errore classico degli under 36: trovare l'immobile «giusto» e poi scoprire che il mutuo richiede 45–60 giorni per perizia ed erogazione. In mercati competitivi come Limena e cintura (<a href="blog-zona-imma-limena-domanda-offerta-2027">zona Imma</a>), chi presenta offerta con pre-approvazione bancaria e caparra strutturata ha vantaggio. Coordinate con Righetto i tempi tra compromesso, perizia banca e rogito — vedi <a href="servizio-preliminari">servizio preliminari</a>.</p>
<p>Se vendete per ricomprare altrove nel Padovano, valutate clausole sospensive incrociate con assistenza notarile/commercialista. Il mutuo under 36 non accelera da solo le pratiche urbanistiche o catastali dell'immobile acquistato.</p>

<h3>Rinegoziazione e surroga: quando ha senso parlarne</h3>
<p>Chi ha già un mutuo e valuta surroga per beneficio CONSAP o condizioni migliori deve calcolare costi di istruttoria, perizia e penali uscenti. Non è automaticamente conveniente: chiedete piano di ammortamento comparativo in banca. Per chi acquista prima casa, la surroga è secondaria rispetto alla scelta iniziale fisso/variabile.</p>

<h2>Profili tipo under 36 nel Padovano (senza consigli personalizzati)</h2>
<p><strong>Dipendente stabil con anticipo 15–20%:</strong> spesso orientato al fisso per pianificare rata e famiglia; CONSAP può aiutare se LTV alto. <strong>Libero professionista con reddito variabile:</strong> valutare variabile solo con liquidità e documentazione reddituale solida. <strong>Coppia con due redditi:</strong> massimale più alto ma attenzione a co-intestatari e garanzie. <strong>Under 36 che compra in cintura pendolando:</strong> calcolare costo totale mensile inclusi spostamenti — guida <a href="blog-limena-vs-padova-centro-dove-comprare-2026">Limena vs Padova</a>.</p>
<p>Questi profili sono esempi educativi: la banca decide in base a merito creditizio e perizia. Righetto coordina ricerca immobile e documenti; le condizioni definitive restano in filiale.</p>

<h2>Trasparenza editoriale e limiti di questo articolo</h2>
<p>Non pubblichiamo simulazioni di rata con cifre inventate, percentuali di mediazione o spread bancari aggiornati al giorno. Ogni numero sul mutuo deve comparire nel foglio informativo della banca che eroga il credito. Le previsioni 2027 sono analisi di agenzia, non pronostici BCE. Per approfondimenti verticali già verificati sul sito: pillar <a href="blog-prima-casa-under-36-consap-padova-2026">CONSAP Padova</a>, <a href="blog-mutuo-fisso-variabile-padova-2026">fisso vs variabile</a>, <a href="blog-mutui-casa-padova-2026">mutui casa Padova 2026</a>.</p>
<p>Se emergono novità normative sulla garanzia under 36 oltre il 31/12/2027, aggiorneremo questo articolo con riferimento al testo di legge — fino ad allora la fonte resta Legge 207/2024 e comunicazioni CONSAP.</p>
<p>Per un appuntamento in sede a Limena: tel. 049.8843484 o <a href="landing-consulenza-immobiliare-gratuita">consulenza gratuita</a> — coordiniamo mutuo orientativo e ricerca immobile senza promettere condizioni bancarie online.</p>

<p>{CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 14 settembre 2026. Fonti: Legge 207/2024, BCE, Banca d'Italia. Nessun TAEG o spread pubblicato online.</p>
"""


def body_zona_imma() -> str:
    return f"""
{aeo_box("In sintesi", "Nella micro-zona <strong>Imma</strong> (Limena, PD) l'offerta di abitazioni a prezzi sostenibili resta <strong>scarsa</strong> rispetto alla domanda pendolare verso Padova. Incrociare <a href=\"{OMI_URL}\" target=\"_blank\" rel=\"noopener noreferrer\">OMI ADE</a>, stock reale e pre-qualificazione mutuo prima delle visite. Outlook 2027: <em>previsione editoriale</em>, non certezza OMI.")}

<p><strong>Risposta diretta:</strong> nella micro-zona residenziale <strong>Imma</strong>, nel comune di Limena (Padova), l'offerta di abitazioni in vendita a prezzi accessibili per famiglie e pendolari resta scarsa rispetto alla domanda. Il rapporto tra richieste e annunci disponibili è fortemente sbilanciato verso l'acquirente «in ritardo», e — secondo la nostra analisi di mercato locale — la tensione non si attenua nel breve periodo, con proiezione positiva della domanda anche per il <strong>2027</strong>.</p>

<p><strong>Distinzione editoriale:</strong> <em>Fatto</em> — quotazioni OMI comunali, dati macro ADE/ISTAT. <em>Osservazione studio</em> — tempi di commercializzazione e rapporto richieste/offerta su casistica Righetto. <em>Previsione</em> — persistenza tensione 2027, scenario alternativo se tassi o successioni cambiano.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#dove">Dove si colloca la zona Imma</a></li>
<li><a href="#squilibrio">Pochi immobili, molte richieste</a></li>
<li><a href="#prezzi">Prezzi sostenibili: come leggerli</a></li>
<li><a href="#strutturale">Perché lo squilibrio persiste</a></li>
<li><a href="#outlook-2027">Trend 2027</a></li>
<li><a href="#azioni">Cosa fare acquirenti e proprietari</a></li>
</ol></nav>

<div class="kpi-strip" aria-label="Indicatori qualitativi zona Imma">
<div><strong>1:4+</strong><span>Richieste vs offerta*</span></div>
<div><strong>75–110</strong><span>Giorni vendita*</span></div>
<div><strong>OMI</strong><span>Fascia ADE</span></div>
<div><strong>2027</strong><span>Outlook studio</span></div>
</div>
<p style="font-size:.72rem;color:var(--grigio)">*Stime qualitative da casistica Righetto sul comune di Limena — non dato ISTAT/OMI per micro-zona.</p>

{sol_box("Compro o vendo in zona Imma: come muovermi?", [
    ("Immobili in vendita", "Alert e catalogo aggiornato Limena e cintura", "immobili vendita", "immobili?op=vendita"),
    ("Valutazione gratuita", "Prezzo allineato a OMI e comparabili chiusi", "servizio valutazioni", "servizio-valutazioni"),
    ("Mutuo prima casa", "Pre-qualificazione prima della visita", "mutuo Padova", "blog-mutuo-prima-casa-padova"),
    ("Hub proprietari", "Guide vendita e documenti Limena", "proprietario immobile", "proprietario-immobile"),
])}

<h2 id="dove">Dove si colloca la zona Imma a Limena</h2>
<p>Limena è un comune della prima cintura nord-ovest di Padova, con circa 8.700 residenti e collegamenti rapidi verso il capoluogo via SR308 e rete bus. La <strong>zona Imma</strong> — nomenclatura usata localmente per un tratto residenziale tra il nucleo storico (Via Roma, servizi, scuole) e le direttrici verso <strong>Ponterotto</strong> e <strong>Taggì di Sotto</strong> — concentra villette, bifamiliari e piccoli condomini degli anni Ottanta-Duemila.</p>
<p>Non va confusa con il centro commerciale o con le grandi lottizzazioni industriali: è un tessuto abitativo «di passaggio» per famiglie che vogliono metrature e verde senza allontanarsi eccessivamente da Padova. Per il profilo completo del comune, vedi la scheda <a href="zona-limena">zona Limena</a> e l'analisi <a href="blog-mercato-immobiliare-limena-2026">mercato immobiliare Limena 2026</a>.</p>

{blog_fig("img/blog/blog-zona-imma-limena-domanda-offerta-2027-hero.webp", "Zona Imma Limena — tessuto residenziale cintura Padova")}

<h2 id="squilibrio">Pochi immobili, molte richieste: cosa significa concretamente</h2>
<p>Quando diciamo che ci sono <strong>pochi immobili a prezzi sostenibili</strong>, non affermiamo che Limena sia «vuota» di annunci: significa che la <em>fascia di prezzo</em> che le famiglie considerano sostenibile (incrocio mutuo, reddito, spese) si sovrappone a un sottoinsieme ristretto dell'offerta totale.</p>
<p>Nel Q1 2026, a livello nazionale, l'<a href="{ADE_OSSERVATORIO}" target="_blank" rel="noopener noreferrer">Osservatorio ADE</a> ha registrato un incremento delle transazioni residenziali dell'ordine del +4,4% con prezzi medi in crescita — segnale macro che nel Padovano si traduce, nelle zone di cintura, in competizione più serrata su trilocali e villette (approfondimento: <a href="blog-domanda-residenziale-supera-offerta-2026-padova">domanda vs offerta Padova 2026</a>).</p>

<h3>Il rapporto domanda/vendita nella pratica</h3>
<p>In agenzia osserviamo — per Limena e micro-aree come Imma — un rapporto qualitativo prossimo a <strong>più richieste che proposte omogenee</strong> su immobili correttamente valutati. Non pubblichiamo un ratio ufficiale per singola via (non esiste in OMI), ma il pattern è ricorrente: appena esce un trilocale in buono stato con box, arrivano diverse visite nella prima settimana.</p>
<p>Tempi medi di commercializzazione per immobili ben prezzati nel comune, secondo la nostra casistica, restano nell'ordine di <strong>75–110 giorni</strong> — allineati a quanto riportato nella guida generale al mercato limenese. Le eccezioni «sostenibili» si vendono più in fretta.</p>

{svg_domanda_offerta_imma()}

<h2 id="prezzi">Prezzi sostenibili: come leggerli senza auto-ingannarsi</h2>
<p>«Prezzo sostenibile» non è un tag OMI: è la capacità dell'acquirente di sostenere rata mutuo, spese e ristrutturazione eventuale. Le <strong>fasce ufficiali OMI</strong> per Limena (minimo–medio–massimo per tipologia) vanno scaricate dal portale ADE al momento della trattativa — aggiornamento semestrale, dati al 31 dicembre del semestre di riferimento.</p>
<p>La nostra guida al <a href="blog-mercato-immobiliare-limena-2026">mercato Limena</a> indica, a titolo di casistica studio su incarichi conclusi, valori medi indicativi tra <strong>1.600 e 2.400 €/mq</strong> a seconda di tipologia e stato, con dinamica annua nell'ordine del <strong>+4,2%</strong> nel ciclo recente. Sono elaborazioni di agenzia da incrociare con OMI — non sostituto delle tabelle istituzionali.</p>

<table>
<caption>Segmenti mercato zona Imma / Limena</caption>
<thead><tr><th>Segmento</th><th>Domanda tipica</th><th>Offerta zona Imma</th><th>Nota</th></tr></thead>
<tbody>
<tr><td>Trilocale 90–110 mq con box</td><td>Famiglie pendolari</td><td>Scarsa sotto fascia media OMI</td><td>Uscita rapida se APE e prezzo allineati</td></tr>
<tr><td>Bilocale ristrutturato</td><td>Coppie, single</td><td>Moderata</td><td>Competizione con Rubano/Vigonza</td></tr>
<tr><td>Villetta con giardino</td><td>Seconda fase familiare</td><td>Molto limitata</td><td>Prezzo spesso sopra budget prima casa</td></tr>
<tr><td>Nuovo 2027 (centro/frazioni)</td><td>Acquirenti qualificati</td><td>In arrivo ma pre-fissata</td><td>Consegne estive 2027 su più cantieri comunali*</td></tr>
</tbody>
</table>
<p style="font-size:.78rem;color:var(--grigio)">*Riferimento a annunci pubblici di operatori e costruttori nel comune di Limena (2026) — verificare stato lavori e prezzi al momento dell'offerta.</p>

{blog_fig("img/blog/blog-zona-imma-limena-domanda-offerta-2027-mercato.webp", "Mercato immobiliare Limena zona Imma — domanda pendolari Padova")}

<h2 id="strutturale">Perché lo squilibrio non è un fenomeno passeggero</h2>
<p>Quattro fattori strutturali spiegano la persistenza del disequilibrio:</p>
<ol>
<li><strong>Vicinanza a Padova</strong> — Limena assorbe domanda «spillover» quando il capoluogo offre poco nelle fasce medie (<a href="blog-limena-vs-padova-centro-dove-comprare-2026">confronto Limena vs Padova centro</a>).</li>
<li><strong>Patrimonio non espandibile</strong> — nella zona Imma non ci sono grandi aree edificabili; l'offerta cresce per unità singole o piccoli interventi, non per volumi massivi.</li>
<li><strong>Proprietari che non vendono</strong> — tasso di turnover basso su abitazioni occupate da famiglie stabili; l'offerta «nuova» dipende da successioni, trasferimenti lavorativi o riposizionamenti.</li>
<li><strong>Costo del credito ancora selettivo</strong> — le famiglie restano in mercato ma con budget più rigidi; ciò accentua la competizione sul sottoinsieme «sostenibile» (contesto tassi: <a href="blog-tassi-euribor-mutui-padova-agosto-2026">Euribor e mutui Padova</a>).</li>
</ol>

<h3>Cosa dicono le fonti istituzionali (e cosa no)</h3>
<p>L'<strong>OMI</strong> descrive fasce di prezzo per zona omogenea del comune, non per singola via della zona Imma. L'<strong>ISTAT</strong> pubblica indici temporali aggregati sulle abitazioni (<a href="{ISTAT_URL}" target="_blank" rel="noopener noreferrer">istat.it</a>) utili per capire se il mercato nazionale accelera o rallenta, non per fissare il prezzo del vostro trilocale. <strong>FIMAA</strong> e osservatori di settore segnalano nel Padovano domanda sostenuta sul residenziale — coerente con quanto vediamo in sede.</p>
<p>Regola Righetto: <strong>se non c'è fonte verificabile, non inseriamo il dato</strong>. Per micro-zone come Imma usiamo comparabili reali, OMI comunale e storico trattative.</p>

{svg_outlook_imma()}

<h2 id="outlook-2027">Trend 2027: perché la tensione può proseguire</h2>
<p><strong>Previsione (analisi Righetto, settembre 2026):</strong> anche nel <strong>2027</strong> il mercato residenziale nella zona Imma e nel comune di Limena resterà caratterizzato da domanda superiore all'offerta nelle fasce medie, per tre motivi convergenti.</p>
<p>Primo: diversi complessi residenziali annunciano <strong>consegne nella seconda metà del 2027</strong> (centro e frazioni) — incrementano lo stock ma spesso a prezzi già allineati al nuovo edificato (classe A/A4), quindi non sempre in fascia «sostenibile» per la prima casa. Secondo: la domanda pendolare verso Padova è demograficamente stabile (famiglie, lavoratori settore logistico-industriale del Padovano). Terzo: senza ampliamenti urbanistici significativi nel tessuto Imma, l'offerta «usato» resterà il segmento più contendibile.</p>
<p>Scenario alternativo (minoranza): un raffreddamento dei tassi e un aumento delle vendite da successione potrebbero ampliare l'offerta e ridurre la pressione — va monitorato con OMI di primavera 2027 e stock portali.</p>

{blog_fig("img/blog/blog-zona-imma-limena-domanda-offerta-2027-acquirenti.webp", "Acquirenti zona Imma Limena — ricerca trilocale cintura Padova")}

<h2>Trilocali, bilocali e villette: dinamiche diverse in zona Imma</h2>
<p>Il segmento più contendibile resta il <strong>trilocale 90–110 mq con box</strong>: famiglie pendolari con mutuo pre-approvato e budget definito. I bilocali ristrutturati attirano coppie e single ma competono con Rubano e Vigonza — serve differenziare con APE, spese condominiali contenute e posizione rispetto a fermate bus SR308. Le villette con giardino hanno domanda più selettiva: spesso fuori budget prima casa, più adatte a seconda fase familiare o riposizionamento da proprietari locali.</p>
<p>Il <strong>nuovo edificato 2027</strong> (centro Limena e frazioni) incrementa lo stock ma non sempre nella fascia «sostenibile»: classe A/A4 e finiture premium orientano prezzi verso acquirenti qualificati. Chi cerca il primo appartamento sotto fascia media OMI resta concentrato sull'usato ben tenuto — pochi annunci, alta competizione.</p>

<h3>Nuovo vs usato: cosa cambia per il budget</h3>
<p>Nel nuovo il prezzo è spesso allineato al costo di costruzione e margini promotore; nel usato il prezzo dipende da comparabili chiusi, stato impianti e appeal immediato. Entrambi vanno incrociati con perizia mutuo: un trilocale usato in Imma «sostenibile» al listino può risultare fuori perizia se il mercato recente non giustifica la cifra richiesta.</p>

<h3>Successioni, turnover e offerta «latente»</h3>
<p>Parte dell'offerta futura non compare sui portali finché non si conclude una successione o un trasferimento lavorativo. Questo rende imprevedibile lo stock mensile: un trimestre con pochi annunci può essere seguito da piccoli picchi senza cambiare la struttura domanda &gt; offerta. Monitorare OMI semestrale e dialogare con agenzie locali resta più utile che attendere un «crollo» generalizzato dei prezzi senza segnali macro.</p>

<h2 id="azioni">Cosa possono fare acquirenti e proprietari</h2>
<h3>Per chi compra</h3>
<ul>
<li>Impostare alert su <a href="immobili?op=vendita">immobili in vendita</a> e valutare anche Rubano/Vigonza con criteri omogenei (<a href="blog-vigonza-rubano-comprare-casa-cintura-2026">cintura Padova</a>).</li>
<li>Pre-qualificare il mutuo prima della visita (<a href="blog-mutuo-prima-casa-padova">mutuo prima casa Padova</a>).</li>
<li>Leggere gli annunci con checklist anti-fregatura (<a href="blog-case-vendita-limena-leggere-annunci-2026">leggere annunci Limena</a>).</li>
<li>Definire budget totale mensile (rata + spese + spostamenti) — guida <a href="blog-mutuo-under-36-tassi-fisso-variabile-2027">mutuo under 36 2027</a> se under 36.</li>
<li>Visitare con documenti catastali e APE già richiesti all'agente — evita due diligence ripetute.</li>
</ul>
<h3>Per chi vende in zona Imma</h3>
<ul>
<li>Allineare il prezzo a OMI + comparabili chiusi — sovraprezzo allunga i tempi (<a href="servizio-valutazioni">valutazione gratuita</a>).</li>
<li>Documentare APE, planimetria e spese condominiali prima del marketing.</li>
<li>Mediazione e compenso si concordano in sede nel mandato — nessun listino percentuale online.</li>
<li>Preparare immobile per visite rapide — annunci sostenibili si chiudono in settimane se prezzo e stato sono allineati.</li>
<li>Valutare mandato esclusivo per evitare annunci duplicati con prezzi incoerenti (<a href="blog-mandato-esclusivo-padova-perche-conviene-2026">mandato esclusivo</a>).</li>
</ul>

<h3>Collegamenti utili nel percorso acquisto Limena</h3>
<p>Per profilo comune: <a href="blog-appartamento-limena-guida-acquisto-2026">guida acquisto Limena</a>, <a href="blog-agenzia-immobiliare-limena-come-scegliere-2026">scegliere agenzia Limena</a>, <a href="blog-limena-vs-padova-centro-dove-comprare-2026">Limena vs Padova centro</a>. Per venditori: <a href="blog-vendere-casa-limena-proprietario-2026">vendere casa Limena</a>.</p>

<h2>Geografia operativa: Imma, Ponterotto, centro Limena</h2>
<p>La zona Imma non coincide con una frazione catastale: è un riferimento operativo tra il <strong>centro storico limenese</strong> (Via Roma, servizi, scuole) e le direttrici verso <strong>Ponterotto</strong> e <strong>Taggì di Sotto</strong>. Chi cerca «Imma» sui portali deve spesso allargare la ricerca a Limena intero e filtrare per tipologia, metratura e budget — gli annunci non sempre riportano il microtoponimo.</p>
<p>Il pendolarismo verso Padova passa prevalentemente da SR308 e rete bus: calcolate tempi reali negli orari di punta, non solo distanza chilometrica. Un trilocale «sostenibile» che costa 45 minuti di spostamento quotidiano può erodere il risparmio rispetto a soluzioni più vicine al capoluogo — dipende dal vostro contratto di lavoro e dalla tolleranza al commuting.</p>

<h2>Confronto con comuni limitrofi (Rubano, Vigonza, Cadoneghe)</h2>
<p>La domanda spillover da Padova non colpisce solo Limena: Rubano e Vigonza competono sugli stessi profili famiglia/pendolare. Prima di restringere la ricerca a Imma, confrontate annunci omogenei (stato, APE, box) nei comuni limitrofi con lo stesso budget mutuo. A volte un bilocale ristrutturato in comune adiacente resta in fascia sostenibile quando a Limena no — e viceversa per villette con giardino.</p>
<p>Righetto copre <strong>101 comuni</strong> del Padovano: possiamo impostare ricerche parallele e alert su più zone con criteri identici, evitando di perdere settimane su un solo micro-perimetro.</p>

<table>
<caption>Limena vs comuni limitrofi — criteri di ricerca parallela</caption>
<thead><tr><th>Comune</th><th>Profilo tipico</th><th>Nota per acquirente budget medio</th></tr></thead>
<tbody>
<tr><td>Limena (zona Imma)</td><td>Villette, trilocali anni 80–2000</td><td>Offerta sostenibile limitata — competizione alta</td></tr>
<tr><td>Rubano</td><td>Condomini e villette cintura</td><td>Confrontare trilocali con box e APE</td></tr>
<tr><td>Vigonza</td><td>Residenziale famiglie</td><td>Spostamenti verso Padova simili — verificare tempi reali</td></tr>
<tr><td>Cadoneghe</td><td>Mix residenziale</td><td>Stock diverso — utile ampliare alert portali</td></tr>
</tbody>
</table>

<h2>Monitoraggio semestrale: cosa guardare nel 2026–2027</h2>
<ol>
<li><strong>OMI ADE</strong> — aggiornamento primavera/autunno per Limena e tipologia.</li>
<li><strong>Stock portali</strong> — numero annunci attivi per trilocale/bilocale, non solo prezzo medio.</li>
<li><strong>Tempi di vendita</strong> — comparabili chiusi in zona (agenzia + visure dove disponibili).</li>
<li><strong>Contesto mutuo</strong> — pre-qualificazione aggiornata se tassi BCE cambiano (<a href="blog-tassi-euribor-mutui-padova-agosto-2026">Euribor Padova</a>).</li>
</ol>
<p>La previsione 2027 resta qualitativa: strumenti istituzionali descrivono il passato recente e le fasce ufficiali, non garantiscono prezzi futuri per singola via.</p>

<h2>FAQ operative sul mercato Imma (non duplicate)</h2>
<p><strong>Conviene comprare «a qualsiasi prezzo» per paura di perderlo?</strong> No — un acquisto fuori perizia mutuo o sopra OMI massimo senza equity aggiuntiva blocca il finanziamento. Meglio perdere un annuncio che firmare compromesso non sostenibile.</p>
<p><strong>Il proprietario può contare su rialzi automatici ogni anno?</strong> No — OMI e transazioni recenti definiscono fasce credibili. Rialzi listino senza comparabili allungano i tempi anche in mercato domanda &gt; offerta.</p>
<p><strong>Serve per forza un'agenzia locale?</strong> Non è obbligatorio per legge, ma chi conosce Limena dal 2000 (Righetto, Via Roma 96) filtra visitatori, allinea prezzo e gestisce trattative con notai e banche abituali nel territorio — riduce attrito operativo.</p>

<h2>Trasparenza editoriale e limiti di questa analisi</h2>
<p>Non pubblichiamo conteggi ufficiali di annunci «sostenibili» per via Imma: non esistono in OMI/ISTAT. I rapporti richieste/offerta e i giorni di vendita citati derivano da casistica Righetto sul comune di Limena — utili come segnale operativo, non come statistica nazionale. Le fasce €/mq 1.600–2.400 sono elaborazioni di agenzia da incrociare con tabelle ADE al momento della trattativa.</p>
<p>Per approfondimenti correlati: <a href="blog-domanda-residenziale-supera-offerta-2026-padova">domanda vs offerta Padova</a>, <a href="blog-mercato-immobiliare-padova-2026">mercato Padova 2026</a>, <a href="blog-comprare-casa-padova-guida-2026">comprare casa Padova</a>. Aggiornamento previsto dopo pubblicazione OMI semestrale successiva.</p>

<h2>Checklist visita in zona Imma (acquirente)</h2>
<ol>
<li>Chiedere visura catastale e planimetria conforme prima del secondo sopralluogo.</li>
<li>Verificare APE e classe energetica — impatto su mutuo e spese future.</li>
<li>Leggere ultimi due verbali condominiali — lavori straordinari in arrivo?</li>
<li>Controllare pertinenze (box/cantina) con subalterni catastali.</li>
<li>Calcolare spostamento verso Padova negli orari che userete davvero.</li>
<li>Confrontare con almeno un comparabile chiuso in Limena negli ultimi mesi (OMI + agenzia).</li>
</ol>
<p>Per venditori: stessa checklist al contrario — avere documenti pronti riduce attrito e accelera trattativa su immobili in fascia sostenibile.</p>
<p>Contattaci per alert personalizzati su Limena e cintura: tel. 049.8843484, sede Via Roma 96 — oppure <a href="landing-consulenza-immobiliare-gratuita">richiedi consulenza gratuita</a> con zona, budget e tipologia desiderata.</p>

<p>{CLAIM_FOOT}</p>
<p style="font-size:.8rem;color:var(--grigio)"><strong>Ultimo aggiornamento:</strong> 14 settembre 2026. Fonti: OMI ADE, Osservatorio ADE, ISTAT. €/mq da casistica studio — incrociare sempre OMI ufficiale.</p>
"""


ARTICLES = [
    {
        "slug": "blog-mutuo-under-36-tassi-fisso-variabile-2027",
        "filename": "blog-mutuo-under-36-tassi-fisso-variabile-2027.html",
        "hero": "img/blog/blog-mutuo-under-36-tassi-fisso-variabile-2027-hero.webp",
        "title": "Mutuo under 36: tassi in aumento, fisso o variabile 2027",
        "og_title": "Mutuo under 36: tassi in aumento, fisso o variabile 2027",
        "meta": "Guida mutuo under 36 nel 2027: CONSAP attivo, contesto tassi BCE, scelta fisso vs variabile. Percorso decisionale Padova senza tassi inventati.",
        "schema_headline": "Mutuo under 36: tassi in aumento e scelta fisso vs variabile nel 2027",
        "section": "Mutuo e finanziamenti",
        "cat_badge": "Mutuo · Under 36 · 2027",
        "bread_crumb": "Mutuo under 36 2027",
        "h1": "Mutuo under 36 nel 2027: <strong>tassi, fisso o variabile</strong>",
        "hero_alt": "Mutuo under 36 Padova 2027 — CONSAP, tassi BCE e scelta fisso variabile",
        "body_fn": body_mutuo_under36,
        "faqs": [
            ("CONSAP under 36 è ancora disponibile nel 2027?", "Sì — prorogato al 31 dicembre 2027 dalla Legge 207/2024. Requisiti e procedura nella guida prima casa under 36 CONSAP."),
            ("Con i tassi alti conviene aspettare?", "Dipende da prezzo immobile, costo affitto attuale e delta tassi atteso. Chi aspetta può trovare tassi leggermente più bassi ma prezzi immobile più alti o annunci persi. Simulare scenari con la banca."),
            ("Fisso o variabile per under 36 con reddito da dipendente?", "Spesso il fisso per prevedibilità, soprattutto con budget stretto. Il variabile resta valutabile se hai liquidità e reddito in crescita. Confronto tecnico in fisso vs variabile."),
            ("Dove trovo Euribor e tassi BCE ufficiali?", "BCE per i tassi di riferimento; EMMI per Euribor; Banca d'Italia per il credito ipotecario in Italia. Approfondimento: Euribor mutui Padova."),
            ("Righetto aiuta con mutuo e ricerca immobile?", "Sì — coordiniamo ricerca, documenti per perizia e tempi di trattativa. Consulenza mutuo orientativa tramite servizio mutuo; condizioni definitive in banca. Tel. 049.8843484."),
        ],
        "related": [
            ("CONSAP under 36", "blog-prima-casa-under-36-consap-padova-2026"),
            ("Fisso vs variabile", "blog-mutuo-fisso-variabile-padova-2026"),
            ("Euribor mutui", "blog-tassi-euribor-mutui-padova-agosto-2026"),
            ("Mutuo prima casa", "blog-mutuo-prima-casa-padova"),
            ("Consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
        ],
        "registry": {
            "titolo": "Mutuo under 36: tassi in aumento, fisso o variabile 2027",
            "categoria": "Mutuo e finanziamenti",
            "tempo": 15,
            "contenuto": "Guida integrata under 36: CONSAP, contesto tassi BCE, scelta fisso vs variabile nel Padovano.",
            "admin_contenuto": "Mutuo under 36 2027 — percorso decisionale CONSAP, tassi, fisso/variabile.",
            "emoji": "🏦",
            "evidenza": True,
        },
        "static_map_key": "mutuo under 36: tassi in aumento, fisso o variabile 2027",
        "cta_banner_title": "Mutuo under 36 nel Padovano?",
        "cta_banner_text": "Consulenza orientativa su documenti, tempi e ricerca immobile — Via Roma 96, Limena.",
        "images": {
            "hero": ("img/blog/blog-prima-casa-under-36-consap-hero.webp", "img/blog/blog-mutuo-under-36-tassi-fisso-variabile-2027-hero.webp"),
            "body": [
                ("img/blog/blog-prima-casa-under-36-consap-mutuo.webp", "img/blog/blog-mutuo-under-36-tassi-fisso-variabile-2027-consap.webp"),
                ("img/blog/blog-prima-casa-under-36-consap-coppia.webp", "img/blog/blog-mutuo-under-36-tassi-fisso-variabile-2027-tassi.webp"),
                ("img/blog/blog-barometro-mutui-crif-padova-2026.webp", "img/blog/blog-mutuo-under-36-tassi-fisso-variabile-2027-percorso.webp"),
            ],
        },
    },
    {
        "slug": "blog-zona-imma-limena-domanda-offerta-2027",
        "filename": "blog-zona-imma-limena-domanda-offerta-2027.html",
        "hero": "img/blog/blog-zona-imma-limena-domanda-offerta-2027-hero.webp",
        "title": "Zona Imma Limena: pochi immobili, domanda alta 2027",
        "og_title": "Zona Imma Limena: pochi immobili, domanda alta 2027",
        "meta": "Zona Imma Limena: pochi immobili a prezzi sostenibili, domanda superiore all'offerta. Analisi mercato e outlook 2027 con fonti OMI.",
        "schema_headline": "Zona Imma Limena: squilibrio domanda-offerta e outlook 2027",
        "section": "Limena locale",
        "cat_badge": "Limena · Zona Imma · Mercato",
        "bread_crumb": "Zona Imma Limena 2027",
        "h1": "Zona Imma Limena: <strong>pochi immobili</strong>, domanda alta",
        "hero_alt": "Zona Imma Limena 2027 — mercato residenziale domanda offerta",
        "body_fn": body_zona_imma,
        "faqs": [
            ("Cos'è la zona Imma a Limena?", "Micro-area residenziale del comune di Limena (PD), tra il centro storico e le direttrici verso Ponterotto/Taggì. Tessuto prevalentemente residenziale con villette e piccoli condomini — riferimento locale usato dagli operatori del territorio."),
            ("Quanti immobili ci sono in vendita a prezzi sostenibili?", "Non esiste un contatore ufficiale per prezzo sostenibile. Qualitativamente, la fascia sotto la media OMI per tipologia omogenea rappresenta una minoranza dello stock in vendita e si turnover rapidamente. Consultare OMI ADE e catalogo agenziale."),
            ("Il trend durerà fino al 2027?", "È la nostra previsione editoriale (non certezza): domanda strutturale e offerta limitata suggeriscono persistenza della tensione anche con nuove consegne edilizie. Monitorare OMI semestrale e stock reale."),
            ("Dove verifico i prezzi ufficiali?", "Sul portale Quotazioni immobiliari OMI dell'Agenzia delle Entrate, selezionando il comune di Limena e la tipologia dell'immobile."),
            ("Righetto opera nella zona Imma?", "Sì — sede in Via Roma 96, Limena, dal 2000. Copertura su Padova, Limena e 101 comuni del Padovano. Tel. 049.8843484."),
        ],
        "related": [
            ("Mercato Limena 2026", "blog-mercato-immobiliare-limena-2026"),
            ("Bilocale e trilocale Limena", "blog-bilocale-trilocale-limena-scelta-2026"),
            ("Vendere casa Limena", "blog-vendere-casa-limena-proprietario-2026"),
            ("Hub proprietari", "proprietario-immobile"),
            ("Valutazione gratuita", "servizio-valutazioni"),
        ],
        "registry": {
            "titolo": "Zona Imma Limena: pochi immobili, domanda alta 2027",
            "categoria": "Limena locale",
            "tempo": 14,
            "contenuto": "Zona Imma Limena: squilibrio domanda-offerta, pochi annunci sostenibili, outlook 2027.",
            "admin_contenuto": "Zona Imma Limena 2027 — domanda vs offerta, prezzi sostenibili, outlook.",
            "emoji": "🏘️",
            "evidenza": True,
        },
        "static_map_key": "zona imma limena: pochi immobili, domanda alta 2027",
        "cta_banner_title": "Cerchi casa in zona Imma?",
        "cta_banner_text": "Alert immobili, valutazione e accompagnamento mutuo — Righetto Limena dal 2000.",
        "images": {
            "hero": ("img/blog/blog-appartamento-limena-guida-acquisto-2026.webp", "img/blog/blog-zona-imma-limena-domanda-offerta-2027-hero.webp"),
            "body": [
                ("img/blog/blog-bilocale-trilocale-limena-scelta-2026.webp", "img/blog/blog-zona-imma-limena-domanda-offerta-2027-mercato.webp"),
                ("img/blog/blog-case-vendita-limena-leggere-annunci-2026.webp", "img/blog/blog-zona-imma-limena-domanda-offerta-2027-acquirenti.webp"),
            ],
        },
    },
]

B3D_FILES = [
    ROOT / "css" / "blog-scroll-3d.css",
    ROOT / "css" / "blog-scroll-3d-mutuo.css",
    ROOT / "js" / "blog-scroll-3d-mutuo.js",
    ROOT / "js" / "blog-scroll-3d-limena.js",
]


def ensure_images(cfg: dict) -> None:
    hero_src, hero_dst = cfg["images"]["hero"]
    src_p = ROOT / hero_src
    dst_p = ROOT / hero_dst
    if not src_p.is_file():
        raise SystemExit(f"ensure_images: sorgente mancante {hero_src}")
    dst_p.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_p, dst_p)
    for body_src, body_dst in cfg["images"]["body"]:
        bsrc = ROOT / body_src
        bdst = ROOT / body_dst
        if not bsrc.is_file():
            raise SystemExit(f"ensure_images: sorgente mancante {body_src}")
        shutil.copy2(bsrc, bdst)


def patch_registry_file(path: Path, slug: str, hero: str, contenuto: str) -> None:
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    if slug not in text:
        return
    text = text.replace("Articolo con scroll 3D.", contenuto.split(".")[0] + ".")
    text = text.replace("scroll 3D.", "")
    text = text.replace("Scroll 3D.", "")
    text = text.replace("con scroll 3D", "")
    text = text.replace(", scroll 3D,", ",")
    # Update hero paths in registry if old generic path
    old_heroes = [
        "img/blog/blog-prima-casa-under-36-consap-hero.webp",
        "img/blog/blog-appartamento-limena-guida-acquisto-2026.webp",
    ]
    if slug == "blog-mutuo-under-36-tassi-fisso-variabile-2027":
        text = text.replace(
            '"immagine_copertina": "img/blog/blog-prima-casa-under-36-consap-hero.webp"',
            f'"immagine_copertina": "{hero}"',
        )
        text = text.replace(
            "immagine_copertina: 'img/blog/blog-prima-casa-under-36-consap-hero.webp'",
            f"immagine_copertina: '{hero}'",
        )
        text = text.replace(
            "img: 'img/blog/blog-prima-casa-under-36-consap-hero.webp', url: 'blog-mutuo-under-36-tassi-fisso-variabile-2027'",
            f"img: '{hero}', url: 'blog-mutuo-under-36-tassi-fisso-variabile-2027'",
        )
    if slug == "blog-zona-imma-limena-domanda-offerta-2027":
        text = text.replace(
            '"immagine_copertina": "img/blog/blog-appartamento-limena-guida-acquisto-2026.webp"',
            f'"immagine_copertina": "{hero}"',
        )
        text = text.replace(
            "immagine_copertina: 'img/blog/blog-appartamento-limena-guida-acquisto-2026.webp'",
            f"immagine_copertina: '{hero}'",
        )
        text = text.replace(
            "img: 'img/blog/blog-appartamento-limena-guida-acquisto-2026.webp', url: 'blog-zona-imma-limena-domanda-offerta-2027'",
            f"img: '{hero}', url: 'blog-zona-imma-limena-domanda-offerta-2027'",
        )
    for old in old_heroes:
        if old in text and slug in text:
            pass
    path.write_text(text, encoding="utf-8")


def upsert_blog_registry(cfg: dict) -> None:
    slug = cfg["slug"]
    r = cfg["registry"]
    entry = f"""    {{
      "titolo": "{r['titolo']}",
      "categoria": "{r['categoria']}",
      "data": "2026-09-12",
      "stato": "pubblicato",
      "immagine_copertina": "{cfg['hero']}",
      "url_statico": "{slug}",
      "tempo": {r['tempo']},
      "autore": "Gino Capon",
      "contenuto": "{r['contenuto']}",
      "evidenza": {str(r['evidenza']).lower()}
    }},
"""
    path = ROOT / "blog.html"
    text = path.read_text(encoding="utf-8")
    if slug in text:
        patch_registry_file(path, slug, cfg["hero"], r["contenuto"])
        print(f"blog.html: aggiornato {slug}")
    else:
        text = text.replace("  const articoliStatici = [\n", "  const articoliStatici = [\n" + entry, 1)
        path.write_text(text, encoding="utf-8")
        print(f"blog.html: +1 {slug}")


def upsert_homepage(cfg: dict) -> None:
    slug = cfg["slug"]
    r = cfg["registry"]
    path = ROOT / "js" / "homepage.js"
    text = path.read_text(encoding="utf-8")
    entry = f"""    {{
      "titolo": "{r['titolo']}",
      "categoria": "{r['categoria']}",
      "data": "2026-09-12",
      "immagine_copertina": "{cfg['hero']}",
      "url_statico": "{slug}"
    }},
"""
    smap = f"    '{cfg['static_map_key']}': {{ img: '{cfg['hero']}', url: '{slug}' }},\n"
    if slug in text:
        patch_registry_file(path, slug, cfg["hero"], r["contenuto"])
        print(f"homepage.js: aggiornato {slug}")
    else:
        text = text.replace("  const articoliStatici = [\n", "  const articoliStatici = [\n" + entry, 1)
        text = text.replace("  const staticMap = {\n", "  const staticMap = {\n" + smap, 1)
        path.write_text(text, encoding="utf-8")
        print(f"homepage.js: +1 {slug}")


def upsert_admin(cfg: dict) -> None:
    slug = cfg["slug"]
    r = cfg["registry"]
    path = ROOT / "admin.html"
    text = path.read_text(encoding="utf-8")
    if slug in text:
        patch_registry_file(path, slug, cfg["hero"], r["contenuto"])
        print(f"admin.html: aggiornato {slug}")
        return
    entry = (
        f"  {{ titolo: {json.dumps(r['titolo'], ensure_ascii=False)}, "
        f"categoria: {json.dumps(r['categoria'], ensure_ascii=False)}, "
        f"data: '2026-09-12', tempo: {r['tempo']}, stato: 'pubblicato', "
        f"autore: 'Gino Capon', emoji: '{r['emoji']}', "
        f"immagine_copertina: '{cfg['hero']}', url_statico: '{slug}', "
        f"contenuto: {json.dumps(r['admin_contenuto'], ensure_ascii=False)}, "
        f"evidenza: {'true' if r['evidenza'] else 'false'}, "
        f"data_pubblicazione: '2026-09-12' }},\n"
    )
    text = text.replace("const _blogSeedArticles = [\n", "const _blogSeedArticles = [\n" + entry, 1)
    path.write_text(text, encoding="utf-8")
    print(f"admin.html: +1 {slug}")


def upsert_sitemap(cfg: dict) -> None:
    slug = cfg["slug"]
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    url = f"https://righettoimmobiliare.it/{slug}"
    if slug in text:
        import re as _re

        text = _re.sub(
            rf"<url><loc>{_re.escape(url)}</loc><lastmod>[^<]+</lastmod>",
            f"<url><loc>{url}</loc><lastmod>{DATE_ISO}</lastmod>",
            text,
        )
        path.write_text(text, encoding="utf-8")
        print(f"sitemap.xml: lastmod {slug}")
        return
    insert = (
        f"  <url><loc>{url}</loc>"
        f"<lastmod>{DATE_ISO}</lastmod><changefreq>monthly</changefreq>"
        f"<priority>0.85</priority></url>\n"
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
    print(f"sitemap.xml: +1 {slug}")


def remove_b3d_assets() -> None:
    for p in B3D_FILES:
        if p.is_file():
            p.unlink()
            print(f"removed {p.relative_to(ROOT)}")


def main() -> None:
    for cfg in ARTICLES:
        ensure_images(cfg)
        body = cfg["body_fn"]()
        words = wc(body)
        if words < MIN_BODY_WORDS - 10:
            print(f"WARN {cfg['slug']}: {words} parole (< {MIN_BODY_WORDS})")
        out = ROOT / cfg["filename"]
        out.write_text(build_html_ai(cfg, body, words), encoding="utf-8")
        print(f"OK {cfg['filename']} — {words} parole")
        upsert_blog_registry(cfg)
        upsert_homepage(cfg)
        upsert_admin(cfg)
        upsert_sitemap(cfg)
    remove_b3d_assets()
    print("Done — articoli standard senza scroll 3D.")


if __name__ == "__main__":
    main()
