# -*- coding: utf-8 -*-
"""Genera blog-rubano-limena-affitto-lavoratori-2026.html — affitti lavoratori Rubano/Limena.
Esegui da repo root: python scripts/build_blog_rubano_limena_2026.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "blog-rubano-limena-affitto-lavoratori-2026"
FILENAME = f"{SLUG}.html"
DATE_IT = "9 luglio 2026"
DATE_ISO = "2026-07-09"
TIME_TS = "2026-07-09T09:00:00+02:00"
MIN_BODY_WORDS = 2500
HERO = "img/blog/blog-loft-aziende-cucina-condivisa-padova-vicenza-2026.webp"
TITLE = "Affitto Rubano e Limena per Lavoratori 2026: Guida Cintura Padova"
META = (
    "Affitti Rubano e Limena per lavoratori 2026: pendolari, settore edile e industriale "
    "padovano. Guida locazioni cintura Padova — OMI ADE, senza €/mq inventati."
)

OMI_URL = (
    "https://www.agenziaentrate.gov.it/portale/schede/fabbricatiterreni/"
    "omi/banche-dati/quotazioni-immobiliari"
)
ISTAT_URL = "https://www.istat.it/it/archivio/prezzi+immobili"

FAQS = [
    (
        "Rubano o Limena: dove conviene affittare da lavoratore nel 2026?",
        "Dipende da dove lavorate e da come vi spostate. Rubano (circa 7 km da Padova) "
        "è più vicina al capoluogo e alle aree produttive tra Vigodarzere e Cadoneghe; "
        "Limena (circa 8 km) offre servizi consolidati e collegamenti verso nord. "
        "Confrontate tempi reali di percorrenza e canoni con OMI locazione su entrambi "
        "i comuni — senza fidarvi di €/mq non verificati.",
    ),
    (
        "Quanto costa affittare a Rubano o Limena per un lavoratore?",
        "Non pubblichiamo cifre al metro quadro inventate: le fasce ufficiali sono sul "
        "portale OMI dell'Agenzia delle Entrate, selezionando Rubano o Limena e finalità "
        "locazione. Il canone effettivo dipende da tipologia, stato, arredi e vicinanza "
        "al luogo di lavoro.",
    ),
    (
        "Il mercato affitti lavoratori è uguale a quello studentesco padovano?",
        "No. Il segmento studentesco concentra domanda in zona universitaria e cicli "
        "settembre–giugno. Rubano e Limena attirano soprattutto dipendenti industriali, "
        "logistica, edilizia e pendolari stabili — contratti più lunghi e meno stagionalità.",
    ),
    (
        "Corporate housing e affitto residenziale: qual è la differenza?",
        "L'affitto residenziale 4+4 o concordato è per nuclei familiari o singoli che "
        "vivono stabilmente nell'appartamento. Il corporate housing (loft aziendali, "
        "cucina condivisa, soluzioni HR) risponde a trasferte e team — vedi la guida "
        "loft aziende Padova-Vicenza, distinta da questo articolo.",
    ),
    (
        "Edilcassa e housing edile: cosa c'entra con Rubano e Limena?",
        "Edilcassa Veneto riguarda garanzie e strumenti per imprese edili e cantieri — "
        "tema trattato nel blog housing lavoratori Edilcassa 2026, complementare a questa "
        "guida sugli affitti residenziali per operai e tecnici in cintura padovana.",
    ),
    (
        "Come cerco subito appartamenti in affitto Rubano o Limena?",
        "Filtrate il catalogo Righetto con op=affitto, indicate comune preferito e "
        "contattate l'agenzia in Via Roma 96 Limena per alert su nuove proposte. "
        "La sede serve anche il territorio di Rubano.",
    ),
]

STYLE_BLOCK = r"""<style>
    *,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
    :root{--nero:#152435;--bianco:#F7F5F1;--oro:#FF6B35;--grigio:#6B7A8D;--gc:#E1DBD1;--sfondo:#ECE7DF;--blu:#2C4A6E;--blu2:#3A5F8C;--oro2:#FF8F5E;--testo:#152435;--carta:#F2EDE7}
    body{font-family:'Montserrat',sans-serif;background:var(--bianco);color:var(--testo)}
    a{text-decoration:none;color:inherit}
    header{background:var(--nero);position:sticky;top:0;z-index:100}
    .hi{max-width:1380px;margin:0 auto;padding:0 1.5rem;height:74px;display:flex;align-items:center;gap:2rem}
    .logo{font-family:'Cormorant Garamond',serif;font-size:1.3rem;font-weight:600;color:#fff}
    .logo span{color:var(--oro);font-style:italic}
    nav{display:flex;gap:.2rem;flex:1}nav a{color:rgba(255,255,255,.7);font-size:.82rem;padding:.4rem .75rem}nav a.active{color:var(--oro)}
    .h-cta{display:flex;gap:.65rem;align-items:center}.h-tel{color:rgba(255,255,255,.75);font-size:.78rem}
    .h-btn{background:var(--oro);color:var(--nero);padding:.38rem .85rem;border-radius:6px;font-size:.76rem;font-weight:500}
    .art-hero{position:relative;overflow:hidden}
    .art-hero-img{width:100%;height:480px;object-fit:cover;display:block;filter:brightness(.42)}
    .art-hero-overlay{position:absolute;bottom:0;left:0;right:0;padding:3rem 1.5rem 2.5rem;background:linear-gradient(transparent,rgba(21,36,53,.95) 40%)}
    .art-hero-inner{max-width:820px;margin:0 auto}
    .breadcrumb{font-size:.72rem;color:rgba(255,255,255,.45);margin-bottom:1rem}.breadcrumb a{color:rgba(255,255,255,.55)}
    .cat-badge{font-size:.58rem;letter-spacing:.12em;text-transform:uppercase;background:rgba(255,107,53,.2);color:var(--oro);padding:.25rem .7rem;font-weight:700;margin-bottom:.8rem;display:inline-block}
    .art-hero h1{font-family:'Cormorant Garamond',serif;font-size:2.2rem;font-weight:300;color:#fff;line-height:1.2;margin-bottom:1rem}
    .art-hero h1 strong{font-weight:600;font-style:italic}
    .art-hero-meta{display:flex;gap:1rem;font-size:.8rem;color:rgba(255,255,255,.5);flex-wrap:wrap;align-items:center}
    .av{width:36px;height:36px;border-radius:50%;background:var(--oro);display:flex;align-items:center;justify-content:center;font-weight:700;color:var(--nero)}
    .art-container{max-width:820px;margin:0 auto;padding:2.5rem 1.5rem 4rem}
    .art-content{font-size:.92rem;line-height:1.9}
    .art-content h2{font-family:'Cormorant Garamond',serif;font-size:1.75rem;margin:2.5rem 0 .8rem;padding-bottom:.4rem;border-bottom:2px solid var(--oro);color:var(--nero)}
    .art-content h3{font-family:'Cormorant Garamond',serif;font-size:1.28rem;color:var(--blu);margin:1.4rem 0 .5rem}
    .art-content p{margin-bottom:1.1rem}
    .art-content ul{margin:0 0 1rem 1.4rem}
    .art-content a{color:var(--blu);text-decoration:underline}
    .art-content table{width:100%;border-collapse:collapse;margin:1.2rem 0;font-size:.84rem}
    .art-content th,.art-content td{padding:.65rem;border:1px solid var(--gc)}
    .art-content th{background:var(--sfondo);text-transform:uppercase;font-size:.74rem}
    .toc{background:var(--sfondo);border:1px solid var(--gc);border-radius:10px;padding:1.2rem;margin-bottom:2rem}
    .toc-title{font-weight:600;font-family:'Cormorant Garamond',serif;font-size:1.1rem;margin-bottom:.5rem}
    .toc ol{font-size:.84rem;margin-left:1.2rem}
    .cta-row{display:flex;flex-wrap:wrap;gap:1rem;margin:2rem 0}
    .cta-deep{display:inline-flex;background:linear-gradient(180deg,var(--oro2),var(--oro));color:var(--nero);padding:.85rem 1.75rem;border-radius:10px;font-weight:800;font-size:.82rem;box-shadow:0 4px 0 rgba(153,65,20,.45),0 10px 28px rgba(255,107,53,.28);transition:transform .2s}
    .cta-deep:hover{transform:translateY(-2px)}
    .cta-deep-outline{padding:.8rem 1.55rem;border-radius:10px;border:2px solid var(--blu);color:var(--blu);font-weight:700;font-size:.8rem;box-shadow:0 3px 0 var(--blu2)}
    .faq-item{border:1px solid var(--gc);border-radius:8px;margin-bottom:.6rem}
    .faq-q{padding:1rem;font-weight:600;cursor:pointer;display:flex;justify-content:space-between}
    .faq-q::after{content:'+';color:var(--oro)}
    .faq-a{max-height:0;overflow:hidden;transition:max-height .35s;background:var(--sfondo)}
    .faq-item.open .faq-a{max-height:480px}
    .faq-a-inner{padding:0 1rem 1rem;font-size:.86rem;color:var(--grigio);line-height:1.8}
    .cta-banner{background:linear-gradient(135deg,var(--nero),var(--blu));border-radius:14px;padding:2rem;margin:2.5rem 0;display:flex;flex-wrap:wrap;gap:1.5rem;align-items:center}
    .cta-banner h3{font-family:'Cormorant Garamond',serif;color:#fff;font-size:1.4rem;margin-bottom:.4rem}
    .cta-banner p{color:rgba(255,255,255,.55);font-size:.84rem}
    .cta-banner-btn{background:linear-gradient(180deg,var(--oro2),var(--oro));color:var(--nero);padding:.75rem 1.8rem;border-radius:10px;font-weight:800;box-shadow:0 4px 0 rgba(153,65,20,.45)}
    .share-bar{border-top:1px solid var(--gc);padding:1rem 0;margin:2rem 0;display:flex;gap:1rem;flex-wrap:wrap}
    .share-btn{padding:.4rem 1rem;border:1px solid var(--gc);border-radius:20px;background:#fff;font-size:.76rem;cursor:pointer;font-family:inherit}
    .related{background:var(--sfondo);border:1px solid var(--gc);padding:1.5rem;border-radius:10px;margin-top:2rem}
    .related a{color:var(--blu);text-decoration:underline}
    .author-bio{display:flex;gap:1.2rem;border:1px solid rgba(44,74,110,.12);padding:1.5rem;border-radius:12px;margin:2rem 0}
    .author-bio img{width:64px;height:64px;border-radius:50%;object-fit:cover}
    footer{background:linear-gradient(180deg,var(--nero),#0d1a2a);padding:2.5rem 1.5rem;color:rgba(255,255,255,.65);font-size:.78rem}
    .fi{max-width:1380px;margin:0 auto}
    .fgrid{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:2rem;margin-bottom:1.5rem}
    .flogo{font-family:'Cormorant Garamond',serif;color:#fff;font-size:1.1rem}.flogo span{color:var(--oro);font-style:italic}
    @media(max-width:768px){.art-hero-img{height:300px}.art-hero h1{font-size:1.75rem}}
    .skip-link{position:absolute;top:-100%;background:var(--oro);color:var(--nero);padding:.5rem 1rem;z-index:9999}.skip-link:focus{top:0}
  </style>
  <link rel="stylesheet" href="css/blog-rich.css?v=3">
  <link rel="stylesheet" href="css/blog-lead-form.css?v=2">"""


def wc(html: str) -> int:
    text = re.sub(r"<[^>]+>", " ", html)
    return len(re.sub(r"\s+", " ", text).strip().split())


def body() -> str:
    return f"""
<div class="blog-rich-callout"><strong>In sintesi</strong><p>Gli <strong>affitti Rubano e Limena</strong> per <strong>lavoratori</strong> nel 2026 si leggono con <strong>OMI locazione</strong> (Agenzia delle Entrate), senza inventare €/mq. Rubano (circa 7 km da Padova) e Limena (circa 8 km) attirano pendolari del settore industriale, logistico ed edile padovano — mercato distinto da quello studentesco. Per corporate housing e loft aziendali vedi guida dedicata; per Edilcassa e housing edile il blog complementare sul Veneto.</p></div>

<p>Cercare casa in locazione come lavoratore nella cintura padovana significa muoversi tra due comuni contigui ma con profili diversi: <strong>Rubano</strong>, a circa sette chilometri dal capoluogo, e <strong>Limena</strong>, a circa otto chilometri, lungo gli assi che collegano Padova a Vigonza, Camposampiero e l'hinterland veneto. In questa guida non troverete cifre al metro quadro «inventate»: le uniche fasce ufficiali sono quelle pubblicate dall'<a href="{OMI_URL}" target="_blank" rel="noopener noreferrer">Osservatorio del Mercato Immobiliare (OMI)</a> dell'Agenzia delle Entrate. Il nostro ruolo, come agenzia con <a href="zona-limena">sede in Via Roma 96 a Limena</a> che serve anche il territorio di <a href="zona-rubano">Rubano</a>, è tradurre quei riferimenti in proposte concrete per inquilini e proprietari del comparto produttivo.</p>

<nav class="toc" aria-label="Indice"><div class="toc-title">Indice</div><ol>
<li><a href="#contesto">Contesto affitti lavoratori Rubano e Limena</a></li>
<li><a href="#rubano">Rubano: geografia e domanda industriale</a></li>
<li><a href="#limena">Limena: prossimità e servizi</a></li>
<li><a href="#confronto">Rubano vs Limena per chi lavora</a></li>
<li><a href="#omi">OMI locazione: consultazione ufficiale</a></li>
<li><a href="#segmenti">Lavoratori vs studenti vs corporate housing</a></li>
<li><a href="#checklist">Checklist inquilino lavoratore</a></li>
</ol></nav>

<div class="righetto-sol">
<h2>Cosa può fare Righetto</h2>
<p class="righetto-sol-quesito"><strong>Il quesito:</strong> Lavoro in cintura Padova e cerco affitto Rubano o Limena — come mi aiuta l'agenzia?</p>
<ul>
<li><strong>Ricerca appartamento per lavoratori</strong> — Selezione annunci allineati a budget, turni e prossimità al luogo di lavoro (<a href="servizio-locazioni">servizio locazioni</a>)</li>
<li><strong>Qualifica inquilino e contratto</strong> — Redazione, caparra documentata, registrazione telematica (<a href="servizio-locazioni">servizio locazioni</a>)</li>
<li><strong>Allineamento canone</strong> — Incrocio OMI locazione, comparabili recenti e domanda effettiva sul territorio</li>
<li><strong>Visite e consegna chiavi</strong> — Appuntamenti in sede Via Roma 96 Limena o sul campo in Rubano e Limena (<a href="zona-rubano">zona Rubano</a> · <a href="zona-limena">zona Limena</a> · <a href="contatti">contatti</a>)</li>
</ul>
<p class="righetto-sol-foot"><em>Mediazione e compenso concordati in sede nel mandato — nessun listino percentuale online. Tel. 049.8843484 · <a href="landing-consulenza-immobiliare-gratuita">consulenza gratuita</a>.</em></p>
</div>

<h2 id="contesto">Qual è il contesto degli affitti per lavoratori a Rubano e Limena nel 2026?</h2>
<p>La domanda locativa in questi due comuni non replica quella «da campus» del centro universitario padovano. Qui prevalgono <strong>dipendenti industriali</strong>, operatori della <strong>logistica</strong>, tecnici dell'<strong>edilizia</strong> e pendolari che accettano pochi minuti in auto per avere metrature più generose rispetto a Prato della Valle o al Sacro Cuore. Rubano e Limena si affacciano sullo stesso corridoio produttivo tra Padova nord, Vigodarzere, Cadoneghe e le direttrici verso Vicenza — un tessuto dove molte imprese assumono personale da fuori provincia e da fuori regione.</p>
<p>Quando un portale generalista scrive «affitti +5%», la domanda utile per un operaio o un capo cantiere è: <em>su quale campione e in quale comune?</em> Per Rubano e Limena la risposta passa da OMI semestrale e da osservazioni qualitative sul Padovano, integrate da ciò che vediamo in agenzia sui rinnovi contrattuali. Non confondiamo slogan nazionali con il singolo bilocale vicino a un'area artigianale o con il trilocale a due passi dal Centro commerciale Limena.</p>
<p>Per il quadro locativo generale su Limena — canoni, quartieri, tipologie — rimandiamo alla guida <a href="blog-affitti-limena-2026">affitti Limena 2026</a>, che resta il riferimento approfondito sul singolo comune. Questo articolo invece incrocia <strong>Rubano e Limena</strong> con la prospettiva del <strong>lavoratore</strong>, senza duplicare pagina per pagina quel contenuto.</p>

<h3>Perché la cintura padovana attira chi lavora nell'industria e nell'edilizia?</h3>
<p>Oltre al canone, contano tempi di spostamento verso stabilimenti e cantieri, disponibilità di parcheggio per auto o furgone aziendale, vicinanza a supermercati aperti anche dopo il turno e percezione di sicurezza residenziale. Molti inquilini arrivano da passaparola di colleghi che lavorano nelle aree produttive tra Rubano, Limena, Vigodarzere e Mestrino. Un <strong>appartamento in affitto</strong> ben posizionato — con box o posto auto scoperto — esce dal mercato in poche settimane se APE, contratto e referenze sono in ordine.</p>

<h2 id="rubano">Come si presenta Rubano per chi cerca affitto da lavoratore?</h2>
<p><strong>Rubano</strong> (circa 16.000 abitanti) si colloca a ovest del capoluogo, a circa <strong>7 km da Padova</strong>, lungo la SR516 e gli accessi al tangenziale. Il comune mescola nucleo storico intorno a piazze e chiese, frazioni come <strong>Sarmeola</strong> e <strong>Villaguattera</strong>, e aree residenziali sviluppate negli ultimi decenni vicino a zone produttive. Per chi lavora in stabilimenti tra Rubano, Vigodarzere e il polo logistico padovano, abitare qui riduce i tragitti mattutini rispetto a comuni più distanti.</p>
<p>La domanda locativa a Rubano è sostenuta da famiglie stabili e da lavoratori singoli o in coppia impiegati in officine, magazzini e imprese di servizi. Non esiste un «quartiere studenti» come in zona universitaria: i contratti tendono a essere più lunghi e meno legati al calendario accademico. Per approfondire il territorio: <a href="zona-rubano">pagina zona Rubano</a>.</p>

<h3>Rubano e settore edile: cosa osserviamo sul campo</h3>
<p>Il comparto edile nel Padovano genera flussi di personale — muratori, carpentieri, installatori — che spesso cercano alloggio temporaneo o semi-stabile per mesi o anni. L'affitto residenziale classico resta la soluzione più frequente per nuclei familiari; per strumenti specifici del settore (garanzie, fondi, housing dedicato) vedi il blog complementare <a href="blog-housing-lavoratori-veneto-edilcassa-2026">housing lavoratori Veneto Edilcassa 2026</a> — argomento <strong>distinto</strong>, non duplicato qui.</p>

<h2 id="limena">Limena: prossimità a Padova e servizi per pendolari</h2>
<p><strong>Limena</strong> (circa 8.700 abitanti) si trova a nord-ovest di Padova, a circa <strong>8 km dal centro</strong>, lungo assi che collegano il capoluogo a Vigonza e Camposampiero. Il nucleo intorno a Via Roma — dove ha sede Righetto Immobiliare — offre servizi consolidati: scuole, supermercati, farmacie e collegamenti extraurbani verso Padova. Il <strong>Centro commerciale Limena</strong> è un riferimento per chi rientra dal lavoro e deve fare la spesa senza entrare in ZTL padovana.</p>
<p>Per i lavoratori, Limena compete con Rubano quando il criterio è equilibrio tra canone, metratura e tempo verso il posto di lavoro. Chi è impiegato a nord del capoluogo o lungo la direttrice verso Vicenza può trovare Limena strategicamente comoda; chi lavora a sud-ovest verso Vigodarzere può preferire Rubano. La scelta va fatta su percorsi reali, non su mappe statiche.</p>
<p>Guida dedicata al mercato locativo limenese: <a href="blog-affitti-limena-2026">affitti Limena 2026</a>. Pagina territorio: <a href="zona-limena">zona Limena</a>.</p>

<h2 id="confronto">Rubano vs Limena: tabella comparativa per lavoratori</h2>
<p>Il confronto seguente è <strong>qualitativo</strong>: non sostituisce OMI locazione né comparabili su singoli annunci. Serve a orientare la ricerca prima di visitare.</p>

<table>
<thead><tr><th>Criterio</th><th>Rubano</th><th>Limena</th></tr></thead>
<tbody>
<tr><td>Distanza da Padova centro</td><td>circa 7 km</td><td>circa 8 km</td></tr>
<tr><td>Profilo domanda locativa</td><td>Industriale, logistico, famiglie</td><td>Pendolari, famiglie, comparto produttivo nord</td></tr>
<tr><td>Collegamenti principali</td><td>SR516, tangenziale, bus extraurbani</td><td>SR308/SR516, bus verso Padova</td></tr>
<tr><td>Tipologie richieste</td><td>Bilocali, trilocali, villette a schiera</td><td>Bilocali, trilocali, villette con giardino</td></tr>
<tr><td>Parcheggio / auto</td><td>Importante per turni e furgoni</td><td>Box o posto auto molto richiesto</td></tr>
<tr><td>Stagionalità contratti</td><td>Bassa (vs mercato studentesco)</td><td>Bassa, picchi primavera-estate</td></tr>
<tr><td>Canone di riferimento</td><td>OMI locazione comune Rubano (ADE)</td><td>OMI locazione comune Limena (ADE)</td></tr>
</tbody>
</table>

<p>Prima di scegliere, testate il tragitto casa-lavoro negli orari di punta. Un appartamento «più economico» ma con venti minuti in più ogni mattina può costare più del risparmio sul canone. Per il rendimento locativo nel capoluogo e in cintura: <a href="blog-rendimento-affitto-padova">rendimento affitto Padova</a>.</p>

<figure style="margin:1.5rem 0">
<img src="img/foto-servizi/gestioni-immobili-padova.webp" alt="Gestione locazioni affitti lavoratori Rubano Limena — agenzia immobiliare Padova" width="1200" height="800" loading="lazy" style="width:100%;border-radius:12px;box-shadow:0 8px 28px rgba(0,0,0,.1)">
<figcaption style="text-align:center;font-size:.78rem;color:var(--grigio);margin-top:.5rem">Gestione locazioni: selezione inquilino, contratto e allineamento canone al mercato cintura Padova.</figcaption>
</figure>

<h2 id="omi">Dove trovo le quotazioni ufficiali OMI per affitti Rubano e Limena?</h2>
<p>L'OMI pubblica, per ogni comune, fasce minimo-medio-massimo separate per <strong>locazione</strong> e per stato dell'immobile (normale, ottimo, ecc.). Per Rubano o Limena dovete aprire il <a href="{OMI_URL}" target="_blank" rel="noopener noreferrer">portale quotazioni immobiliari ADE</a>, selezionare il comune, la tipologia (abitazione civile, villetta, ecc.) e la finalità locazione. Il PDF o l'export Excel riportano valori semestrali aggiornati: sono riferimenti statistici, non il canone certo del vostro terzo piano con box.</p>
<p>Per imparare a leggere OMI insieme agli indici ISTAT sulle abitazioni, usate la guida <a href="blog-quotazioni-locazioni-omi-istat-padova-2026">quotazioni e locazioni OMI e ISTAT Padova</a>. Lì spieghiamo differenza tra indice macro ISTAT (<a href="{ISTAT_URL}" target="_blank" rel="noopener noreferrer">archivio prezzi immobili ISTAT</a>) e micro-zona OMI — strumenti complementari, non sostitutivi.</p>

<h3>Perché non pubblichiamo €/mq OMI per Rubano e Limena in questo articolo?</h3>
<p>Perché le tabelle OMI cambiano semestralmente e dipendono da sottozone omogenee che vanno verificate sul portale ufficiale al momento della trattativa. Citare cifre statiche in un blog rischia di essere fuorviante entro pochi mesi. La regola Righetto: <strong>se non c'è fonte verificabile aggiornata, non inseriamo il dato</strong>. Vi indichiamo dove trovarlo e come usarlo con un professionista.</p>

<figure style="margin:1.5rem 0">
<img src="img/blog/blog-costi-costruzione-istat-padova-2026.webp" alt="Contesto costi costruzione e mercato immobiliare ISTAT Padova cintura" width="1200" height="800" loading="lazy" style="width:100%;border-radius:12px;box-shadow:0 8px 28px rgba(0,0,0,.1)">
<figcaption style="text-align:center;font-size:.78rem;color:var(--grigio);margin-top:.5rem">Contesto macro: ISTAT e OMI aiutano a leggere il mercato; il canone operativo resta sul singolo immobile.</figcaption>
</figure>

<h2 id="segmenti">Lavoratori, studenti e corporate housing: tre mercati distinti</h2>
<p>Confondere questi segmenti porta a scelte sbagliate di zona, tipologia contrattuale e budget.</p>

<h3>Mercato studentesco padovano</h3>
<p>Concentra domanda in <strong>zona universitaria</strong>, Arcella, zone vicine a Policlinico e Stazione. Contratti spesso legati all'anno accademico, domanda picco a settembre, offerta di monolocali e stanze. Rubano e Limena restano <strong>fuori</strong> da questo nucleo: chi studia a Padova raramente sceglie la cintura salvo casi familiari o auto propria.</p>

<h3>Affitto residenziale per lavoratori</h3>
<p>È il cuore di questa guida: contratti 4+4 o concordato, nuclei familiari o singoli stabili, priorità a parcheggio, APE accettabile e prossimità al luogo di lavoro. Tipologie richieste: bilocali e trilocali con cucina abitabile, villette a schiera per famiglie con figli. Catalogo: <a href="immobili?op=affitto">immobili in affitto</a>.</p>

<h3>Corporate housing e loft aziendali</h3>
<p>Quando l'impresa deve ospitare team in trasferta, consulenti o personale distaccato, entrano in gioco soluzioni <strong>HR</strong> diverse dall'affitto residenziale classico: loft adiacenti allo stabilimento, cucina condivisa, contratti corporate. È un mercato <strong>distinto</strong>, trattato nella guida <a href="blog-loft-aziende-cucina-condivisa-padova-vicenza-2026">loft aziende cucina condivisa Padova-Vicenza 2026</a> — complementare a questo articolo, non sostitutivo.</p>

<h3>Edilcassa e housing edile nel Veneto</h3>
<p>Per garanzie, fondi e strumenti legati al comparto edile — cantieri, imprese, lavoratori distaccati con esigenze specifiche — rimandiamo al blog <a href="blog-housing-lavoratori-veneto-edilcassa-2026">housing lavoratori Veneto Edilcassa 2026</a>. Quel contenuto affronta Edilcassa e co-housing edile; qui restiamo sull'<strong>affitto residenziale</strong> per operai, tecnici e pendolari a Rubano e Limena.</p>

<h2>Domanda industriale e logistica: cosa spinge gli affitti in cintura</h2>
<p>Il Padovano ospita poli manifatturieri, distretti meccanici, hub logistici e imprese edili che attingono a manodopera da comuni limitrofi e da altre regioni. Rubano e Limena beneficiano di questa geografia: non sono «periferie dormitorio» generiche, ma comuni con servizi e offerta abitativa che risponde a chi lavora nelle vicine aree produttive. La domanda da <strong>lavoratori</strong> è più stabile del segmento studentesco e meno volatile degli affitti brevi turistici.</p>
<p>Proprietari che locano a Rubano o Limena possono puntare su inquilini con reddito da lavoro dipendente documentato, referenze del datore di lavoro o del precedente locatore, e permanenza media superiore a un anno accademico. Investitori: calcolate il rendimento con OMI vendita + OMI locazione sullo stesso semestre — metodo in <a href="blog-rendimento-affitto-padova">rendimento affitto Padova</a>.</p>

<h2>Tipologie più richieste da lavoratori a Rubano e Limena</h2>
<p><strong>Bilocali e trilocali</strong> con cucina abitabile e almeno un posto auto coperto o box dominano le richieste da coppie e famiglie giovani. I monolocali hanno mercato per single impiegati in stabilimento, soprattutto se ristrutturati e con spese contenute. Le <strong>villette a schiera</strong> con giardino attirano famiglie con bambini — verificare regolamento condominiale e contratto su animali. Gli immobili di recente costruzione (classe energetica migliore) possono giustificare canoni nella fascia alta OMI se arredati e con bollette recenti.</p>

<h3>Arredato, semi-arredato o vuoto: cosa preferisce il mercato lavoratori?</h3>
<p>Chi si trasferisce per lavoro da altra provincia spesso preferisce <strong>semi-arredato</strong> (cucina equipaggiata, climatizzazione) per ridurre costi e tempi. Chi resta a lungo tende a portare i mobili. La scelta influenza deposito cauzionale e tempi di locazione: un arredo di qualità può accorciare i giorni di vacanza, ma richiede inventario fotografico.</p>

<h2>Contratti, fiscalità e registrazione</h2>
<p>Il Padovano applica gli accordi territoriali per la locazione a canone concordato (tipicamente 3+2) con vantaggi fiscali, e il contratto libero 4+4 per canoni negoziati. Non esiste un «regime speciale Rubano» o «Limena»: valgono le norme nazionali e gli accordi provinciali. Prima di firmare, verificate: APE valido, conformità catastale, regolamento condominiale, importo caparra vs deposito cauzionale, clausole su manutenzione ordinaria.</p>
<p>Un'agenzia con esperienza sulla cintura riduce errori su registrazione tardiva o canone fuori fascia concordato. Supporto completo: <a href="servizio-locazioni">servizio locazioni</a>.</p>

<h3>Quanto incide l'APE sul canone per chi lavora a turni?</h3>
<p>Con turni mattutini e serali, inquilini attenti chiedono classe E o migliore e bollette recenti — riscaldamento e climatizzazione incidono sul budget oltre al canone. Un immobile G con infissi datati resta in affitto solo se il canone sconta il rischio bolletta. Proprietari: un intervento mirato può spostare la trattativa verso la fascia media OMI senza inventare prezzi — documentate i lavori e aggiornate l'APE.</p>

<div class="cta-row">
  <a class="cta-deep" href="immobili?op=affitto">Cerca affitti in catalogo</a>
  <a class="cta-deep-outline" href="servizio-locazioni">Servizio locazioni</a>
</div>

<h2 id="checklist">Checklist: cerco appartamento in affitto da lavoratore</h2>
<ul>
<li>Definire budget canone + spese (condominio, riscaldamento, TARI).</li>
<li>Mappare tempi di spostamento verso stabilimento, cantiere o ufficio — orari di punta inclusi.</li>
<li>Scegliere tra Rubano e Limena in base al luogo di lavoro, non solo al canone indicativo.</li>
<li>Verificare parcheggio per auto personale o aziendale (box, scoperto, regolamento).</li>
<li>Controllare APE, planimetria e regolamento condominiale in visita.</li>
<li>Chiedere referenze precedenti locatore e documenti reddito da lavoro.</li>
<li>Confrontare canone richiesto con OMI locazione ufficiale sul comune scelto.</li>
<li>Registrare contratto entro i termini e conservare ricevuta ADE.</li>
</ul>

<h2>Checklist: sono proprietario e voglio affittare a lavoratori</h2>
<ul>
<li>Consultare OMI locazione sul portale ADE per Rubano o Limena, semestre corrente.</li>
<li>Aggiornare APE e sistemare difetti che allungano i tempi (infiltrazioni, impianti).</li>
<li>Scegliere tipologia contrattuale con professionista (concordato vs libero).</li>
<li>Qualificare inquilino: buste paga, contratto di lavoro, referenze.</li>
<li>Evidenziare in annuncio prossimità a aree produttive e parcheggio — leva per il segmento lavoratori.</li>
<li>Affidare registrazione e caparra documentata (<a href="servizio-locazioni">servizio locazioni</a>).</li>
</ul>

<h3>Quando contattare l'agenzia Righetto?</h3>
<p>Quando avete poco tempo per filtrare annunci, quando arrivate da fuori regione per un nuovo impiego, quando serve contratto blindato o quando il precedente inquilino ha lasciato situazioni complesse. Righetto Immobiliare opera dal <strong>2000</strong> su <strong>101 comuni</strong>, con oltre <strong>350 immobili</strong> gestiti e <strong>98% di soddisfazione</strong> clienti (127 recensioni Google, media 4,9/5). Sede in <strong>Via Roma 96, Limena</strong>, con operatività su <strong>Rubano</strong> e cintura padovana. Il compenso di mediazione si concorda <strong>in sede</strong> — nessun listino online.</p>

<h2>Mobilità: quanto conta la distanza da Padova per i pendolari?</h2>
<p>In auto, Rubano e Limena distano pochi chilometri dal tangenziale padovano; in bus, le linee extraurbani collegano al capoluogo con frequenza da verificare su orari aggiornati. Pendolari in auto spesso accettano il canone cintura per evitare ZTL e parcheggi del centro; chi usa bici valuta percorsi ciclabili ancora discontinui. La domanda «quanto tempo per il Policlinico o per Vigodarzere?» va risposta con onestà — non con promesse di «centro in cinque minuti».</p>

<h2>Errori frequenti di inquilini lavoratori e proprietari</h2>
<p><strong>Inquilini:</strong> scegliere solo in base al canone senza testare il tragitto; firmare senza leggere regolamento su furgoni o attrezzi in cortile; pagare caparra senza ricevuta. <strong>Proprietari:</strong> fissare canoni copiati da annunci vecchi; sottovalutare la domanda da lavoratori con auto; saltare la registrazione. Entrambi: confondere corporate housing con affitto residenziale — sono mercati e contratti diversi.</p>

<h2>Come prepararsi alla visita di un appartamento in affitto</h2>
<p>Prima della visita raccogliete documenti utili: ultime buste paga o CUD, referenze del precedente locatore, documento d'identità. Portate un elenco di domande: spese condominiali reali, tipo di riscaldamento, regole su animali, disponibilità box. In visita, verificate pressione acqua, rumori da vicini, luce naturale e stato infissi — dettagli che non compaiono in OMI ma pesano sul canone negoziabile.</p>
<p>Se l'annuncio promette «Padova in dieci minuti», chiedete di testare il percorso negli orari di punta. Un'agenzia seria indica distanze verificabili e propone, se possibile, una seconda visita in orario diverso per valutare esposizione e rumore da traffico su SR516 o SR308.</p>

<h3>Caparra, deposito e registrazione</h3>
<p>La caparra confirmatoria e il deposito cauzionale hanno funzioni diverse: chiarite importi, scadenze e condizioni di restituzione. La registrazione del contratto presso l'Agenzia delle Entrate va effettuata nei termini di legge. Non versate somme senza ricevuta e senza aver letto tutte le clausole.</p>

<h2>Proprietari: tempi medi di locazione nel 2026</h2>
<p>Immobili in buono stato, classe energetica accettabile e canone allineato a OMI locazione si locano in genere entro quattro-dodici settimane. Proposte sopra la fascia massima OMI senza plusvalenze oggettive restano ferme più a lungo. La stagionalità è meno marcata che in zona universitaria: picchi in primavera-estate per trasferimenti lavorativi.</p>

<h2>Collegamenti utili e prossimi passi</h2>
<p>Per Limena nel dettaglio: <a href="blog-affitti-limena-2026">affitti Limena 2026</a>. Per Rubano: <a href="zona-rubano">zona Rubano</a>. Per corporate housing: <a href="blog-loft-aziende-cucina-condivisa-padova-vicenza-2026">loft aziende Padova-Vicenza</a>. Per Edilcassa e housing edile: <a href="blog-housing-lavoratori-veneto-edilcassa-2026">housing lavoratori Edilcassa</a> (complementare). Per rendimento: <a href="blog-rendimento-affitto-padova">rendimento affitto Padova</a>. Per proposte: <a href="immobili?op=affitto">immobili in affitto</a> e <a href="contatti">contatti</a> in sede Limena.</p>

<p style="font-size:.8rem;color:var(--grigio);margin-top:2rem"><strong>Ultimo aggiornamento:</strong> {DATE_IT}. Consultare sempre OMI ADE e ISTAT nelle versioni aggiornate sui portali ufficiali.</p>
"""


def faq_html() -> str:
    items = "".join(
        f'<div class="faq-item"><div class="faq-q">{q}</div>'
        f'<div class="faq-a"><div class="faq-a-inner">{a}</div></div></div>'
        for q, a in FAQS
    )
    return (
        f'<div class="faq-section" id="faq"><h2 style="font-family:\'Cormorant Garamond\',serif;'
        f'font-size:1.7rem;border-bottom:2px solid var(--oro);margin-bottom:1rem;padding-bottom:.35rem">FAQ</h2>'
        f"{items}</div>"
    )


def lead_form() -> str:
    return f"""
<section class="blog-lead-wrap" id="richiedi-consulenza" aria-labelledby="blog-lead-title">
  <h2 id="blog-lead-title">Richiedi informazioni su affitti Rubano e Limena</h2>
  <form data-rig-lead-form data-provenienza="{SLUG}" data-pagina="{SLUG}" data-msg-prefix="[Blog]" novalidate>
    <div class="bl-fields">
      <label for="bl-nome">Nome e cognome *</label>
      <input type="text" id="bl-nome" required autocomplete="name" placeholder="Mario Rossi">
      <label for="bl-tel">Telefono *</label>
      <input type="tel" id="bl-tel" required autocomplete="tel" placeholder="333 123 4567">
      <label for="bl-email">Email</label>
      <input type="email" id="bl-email" autocomplete="email" placeholder="mario@email.it">
      <label for="bl-msg">Messaggio (opzionale)</label>
      <textarea id="bl-msg" placeholder="Rubano o Limena, luogo di lavoro, tipologia…"></textarea>
      <label class="bl-chk"><input type="checkbox" id="bl-gdpr" required> Ho preso visione dell'<a href="privacy" target="_blank" rel="noopener">informativa privacy</a> (Reg. UE 2016/679) e acconsento al trattamento per finalità contrattuali e di legge (punti a) e b)). *</label>
      <label class="bl-chk bl-chk-opt"><input type="checkbox" class="rig-gdpr-marketing" name="gdpr_marketing"> Acconsento al trattamento per finalità di marketing — <em>facoltativo</em>.</label>
      <button type="submit">Invia richiesta</button>
    </div>
    <div class="rig-lead-success">
      <h3>Messaggio inviato!</h3>
      <p>Grazie. Ti ricontattiamo entro pochi minuti negli orari di apertura.</p>
    </div>
  </form>
</section>"""


def build_html(content: str, words: int) -> str:
    blog_ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": TITLE,
        "description": META,
        "image": [f"https://righettoimmobiliare.it/{HERO}"],
        "author": {"@type": "Person", "name": "Gino Capon"},
        "publisher": {
            "@type": "Organization",
            "name": "Righetto Immobiliare",
            "url": "https://righettoimmobiliare.it",
            "logo": {
                "@type": "ImageObject",
                "url": "https://righettoimmobiliare.it/img/og-default.webp",
            },
        },
        "datePublished": DATE_ISO,
        "dateModified": DATE_ISO,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"https://righettoimmobiliare.it/{SLUG}",
        },
        "articleSection": "Mercato locazione",
        "wordCount": words,
        "inLanguage": "it-IT",
    }
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in FAQS
        ],
    }
    bread_ld = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://righettoimmobiliare.it/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://righettoimmobiliare.it/blog"},
            {"@type": "ListItem", "position": 3, "name": "Affitto Rubano Limena lavoratori 2026"},
        ],
    }
    rea_ld = {
        "@context": "https://schema.org",
        "@type": "RealEstateAgent",
        "name": "Gruppo Immobiliare Righetto di Capon Gino",
        "url": "https://righettoimmobiliare.it",
        "telephone": "+390498843484",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Via Roma n.96",
            "addressLocality": "Limena",
            "postalCode": "35010",
            "addressRegion": "PD",
            "addressCountry": "IT",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": 45.476956, "longitude": 11.845762},
        "sameAs": [
            "https://www.facebook.com/righettoimmobiliare",
            "https://www.instagram.com/righettoimmobiliare",
            "https://www.linkedin.com/company/righetto-immobiliare",
        ],
        "hasMap": "https://maps.google.com/?q=45.476956,11.845762",
        "areaServed": [
            {"@type": "City", "name": "Padova"},
            {"@type": "City", "name": "Limena"},
            {"@type": "City", "name": "Rubano"},
        ],
        "foundingDate": "2000",
        "priceRange": "$$",
    }
    related = [
        ("Affitti Limena 2026", "blog-affitti-limena-2026"),
        ("Housing lavoratori Edilcassa", "blog-housing-lavoratori-veneto-edilcassa-2026"),
        ("Loft aziende Padova-Vicenza", "blog-loft-aziende-cucina-condivisa-padova-vicenza-2026"),
        ("Rendimento affitto Padova", "blog-rendimento-affitto-padova"),
        ("Zona Rubano", "zona-rubano"),
        ("Zona Limena", "zona-limena"),
    ]
    rel_h = "".join(f"<li><a href=\"{u}\">{t}</a></li>" for t, u in related)

    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9MHDHHES26"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9MHDHHES26');</script>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="theme-color" content="#2C4A6E">
  <title>{TITLE}</title>
  <meta name="robots" content="index, follow, max-image-preview:large"><link rel="dns-prefetch" href="https://qwkwkemuabfwvwuqrxlu.supabase.co">  <link rel="preload" href="fonts/montserrat-400.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="fonts/cormorant-garamond-700.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="canonical" href="https://righettoimmobiliare.it/{SLUG}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{TITLE}">
  <meta property="og:description" content="{META}">
  <meta property="og:url" content="https://righettoimmobiliare.it/{SLUG}">
  <meta property="og:image" content="https://righettoimmobiliare.it/{HERO}">
  <meta property="article:published_time" content="{TIME_TS}">
  <meta property="article:author" content="Gino Capon">
  <meta property="article:section" content="Mercato locazione">
  <meta name="description" content="{META}">
  <link rel="stylesheet" href="css/fonts.css?v=3"><link rel="stylesheet" href="css/nav-mobile.css?v=4">
  <link rel="stylesheet" href="css/scroll-reveal.css?v=3" media="print" onload="this.media='all'">
  <link rel="stylesheet" href="css/welcome-popup.css?v=3" media="print" onload="this.media='all'">
  <script type="application/ld+json">{json.dumps(blog_ld, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(bread_ld, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(rea_ld, ensure_ascii=False)}</script>
{STYLE_BLOCK}
</head>
<body>
<a href="#main-content" class="skip-link">Vai al contenuto</a>
<header><div class="hi">
  <a href="/" class="logo">Righetto <span>Immobiliare</span></a>
  <nav><a href="/">Home</a><a href="immobili">Immobili</a><a href="servizi">Servizi</a><a href="gino-capon">Profilo autore</a><a href="blog" class="active">Blog</a><a href="contatti">Contatti</a><a href="faq">FAQ</a></nav>
  <div class="h-cta"><a class="h-tel" href="tel:+390498843484">049.8843484</a><a class="h-btn" href="contatti">Valutazione gratuita</a></div>
</div><button class="nav-burger" id="burgerBtn" aria-label="Menu"><span></span><span></span><span></span></button></header>
<div class="nav-mobile" id="navMobile"><a href="/">Home</a><a href="immobili">Immobili</a><a href="servizi">Servizi</a><a href="blog">Blog</a><a href="contatti" class="nav-mobile-cta">Contatti</a></div>

<main id="main-content">
<div class="art-hero">
  <img class="art-hero-img" src="{HERO}" alt="Affitti Rubano e Limena per lavoratori 2026 — cintura Padova settore industriale" width="1200" height="630" fetchpriority="high">
  <div class="art-hero-overlay"><div class="art-hero-inner">
    <div class="breadcrumb"><a href="/">Home</a> / <a href="blog">Blog</a> / Affitto Rubano Limena lavoratori</div>
    <span class="cat-badge">Mercato locazione</span>
    <h1><strong>Affitto Rubano e Limena</strong> per lavoratori 2026: guida cintura Padova</h1>
    <div class="art-hero-meta"><div class="av">G</div><span>Gino Capon</span><span>&middot;</span><span>{DATE_IT}</span></div>
  </div></div>
</div>

<div class="art-container"><div class="art-content">
{content}
{faq_html()}

<div class="cta-banner"><div><h3>Cerchi un appartamento in affitto a Rubano o Limena?</h3><p>Filtra il catalogo o richiedi alert personalizzati — sede Via Roma 96 Limena, operatività su Rubano.</p></div><a href="immobili?op=affitto" class="cta-banner-btn">Affitti disponibili</a></div>

<div class="share-bar"><span style="font-weight:600;font-size:.78rem;color:var(--grigio)">Condividi:</span>
<button type="button" class="share-btn" onclick="navigator.clipboard.writeText('https://righettoimmobiliare.it/{SLUG}');this.textContent='Copiato!'">Copia link</button>
<a class="share-btn" href="https://wa.me/?text=Affitto%20Rubano%20Limena%20lavoratori%202026%20https%3A%2F%2Frighettoimmobiliare.it%2F{SLUG}" target="_blank" rel="noopener noreferrer">WhatsApp</a></div>

<div class="author-bio"><img src="img/team/titolari.webp" alt="Gino Capon" width="64" height="64" loading="lazy"><div><strong>Gino Capon</strong><p style="font-size:.82rem;color:#555;margin:.3rem 0 0">Righetto Immobiliare — Limena, Rubano e Padova.</p></div></div>

<div class="related"><h3 style="font-family:'Cormorant Garamond',serif;margin-bottom:.6rem">Correlati</h3><ul style="margin-left:1.2rem">{rel_h}</ul></div>
</div></div>

<section class="blog-rich-cta-strip" aria-label="Recensioni e contatti">
  <div class="blog-rich-cta-inner">
    <h2>Ti e' stato utile? <em>Lascia una recensione</em></h2>
    <p class="blog-rich-cta-text">Le recensioni Google aiutano altre famiglie sul territorio.</p>
    <a class="blog-rich-btn" href="https://maps.app.goo.gl/xuCiRGDCSKskpTSf6?g_st=ic" target="_blank" rel="noopener noreferrer">Recensione su Google</a>
    <span class="blog-rich-cta-sub"><a href="contatti" style="color:rgba(247,245,241,0.88);text-decoration:underline">Richiedi consulenza immobiliare</a></span>
  </div>
</section>

{lead_form()}
</main>
<footer><div class="fi"><div class="fgrid"><div><div class="flogo">Righetto <span>Immobiliare</span></div>Via Roma 96, Limena (PD)</div><div><a href="blog" style="color:rgba(255,255,255,.7)">Blog</a></div><div><a href="contatti" style="color:rgba(255,255,255,.7)">Contatti</a></div></div><div style="border-top:1px solid rgba(255,255,255,.1);padding-top:1rem">&copy; 2026 Gruppo Immobiliare Righetto — P.IVA 05182390285</div></div></footer>
<script>document.querySelectorAll('.faq-q').forEach(function(q){{q.addEventListener('click',function(){{var p=this.parentElement,o=p.classList.contains('open');document.querySelectorAll('.faq-item.open').forEach(function(x){{x.classList.remove('open');}});if(!o)p.classList.add('open');}});}});</script>
<script src="js/vendor/supabase.min.js" defer></script>
<script src="js/config.js?v=4"></script>
<script src="js/rig-lead-form.js?v=3"></script>
<script src="js/nav-mobile.js?v=3" defer></script>
<script src="js/cookie-consent.js?v=3" defer></script><script src="js/scroll-reveal.js?v=3" defer></script><script src="js/welcome-popup.js?v=3" defer></script>
</body>
</html>"""


def main() -> None:
    content = body()
    words = wc(content)
    if words < MIN_BODY_WORDS:
        raise SystemExit(f"Corpo {words} parole < {MIN_BODY_WORDS} richieste")
    out = ROOT / FILENAME
    out.write_text(build_html(content, words), encoding="utf-8")
    print(f"OK {out.name}: {words} parole corpo")


if __name__ == "__main__":
    main()
