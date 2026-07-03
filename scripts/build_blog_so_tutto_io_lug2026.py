# -*- coding: utf-8 -*-
"""Articolo provocatorio venditore presuntuoso — luglio 2026.
Esegui da repo root: python scripts/build_blog_so_tutto_io_lug2026.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SLUG = "blog-so-tutto-io-venditore-presuntuoso-padova-2026"
FILENAME = f"{SLUG}.html"
DATE_IT = "3 luglio 2026"
DATE_ISO = "2026-07-03"
TIME_TS = "2026-07-03T08:00:00+02:00"
MIN_BODY_WORDS = 2500

STYLE_BLOCK = r"""<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--nero:#152435;--bianco:#F7F5F1;--oro:#FF6B35;--grigio:#6B7A8D;--gc:#E1DBD1;--sfondo:#ECE7DF;--blu:#2C4A6E;--oro2:#FF8F5E}
body{font-family:'Montserrat',sans-serif;background:var(--bianco);color:var(--nero)}
header{background:var(--nero);position:sticky;top:0;z-index:100}
.hi{max-width:1380px;margin:0 auto;padding:0 1.5rem;height:74px;display:flex;align-items:center;gap:2rem}
.logo{font-family:'Cormorant Garamond',serif;color:#fff;font-size:1.28rem;font-weight:600}.logo span{color:var(--oro);font-style:italic}
nav{display:flex;flex:1;gap:.2rem}nav a{color:rgba(255,255,255,.72);font-size:.81rem;padding:.4rem .72rem}nav a.active{color:var(--oro)}
.h-btn{background:var(--oro);color:var(--nero);padding:.4rem .88rem;border-radius:6px;font-size:.76rem;font-weight:600}
.art-hero{position:relative}.art-hero-img{width:100%;height:420px;object-fit:cover;display:block;filter:brightness(.55)}
.art-hero-overlay{position:absolute;inset:auto 0 0 0;padding:2.2rem 1.5rem;background:linear-gradient(transparent,rgba(21,36,53,.94))}
.art-hero-inner{max-width:820px;margin:0 auto}
.breadcrumb{font-size:.72rem;color:rgba(255,255,255,.45);margin-bottom:.86rem}.breadcrumb a{color:rgba(255,255,255,.55)}
.cat-badge{font-size:.57rem;letter-spacing:.12em;text-transform:uppercase;background:rgba(255,107,53,.2);color:var(--oro);padding:.24rem .68rem;font-weight:700;display:inline-block;margin-bottom:.72rem}
.art-hero h1{font-family:'Cormorant Garamond',serif;font-size:2rem;font-weight:300;color:#fff;line-height:1.2}.art-hero h1 strong{font-weight:600;font-style:italic}
.art-hero-meta{display:flex;gap:1rem;align-items:center;font-size:.8rem;color:rgba(255,255,255,.5);margin-top:.92rem;flex-wrap:wrap}
.av{width:36px;height:36px;border-radius:50%;background:var(--oro);display:flex;align-items:center;justify-content:center;font-weight:700;color:var(--nero)}
.art-container{max-width:820px;margin:0 auto;padding:2.4rem 1.5rem 3.55rem}
.art-content{font-size:.91rem;line-height:1.88}
.art-content h2{font-family:'Cormorant Garamond',serif;font-size:1.68rem;margin:2.28rem 0 .68rem;border-bottom:2px solid var(--oro);padding-bottom:.34rem}
.art-content h3{font-size:1.1rem;color:var(--blu);margin:1.15rem 0 .35rem}
.art-content p{margin-bottom:1.04rem}.art-content ul,.art-content ol{margin:0 0 1rem 1.28rem}
.art-content a{color:var(--blu);text-decoration:underline}
.art-content table{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.84rem}
.art-content th,.art-content td{border:1px solid var(--gc);padding:.55rem .65rem;text-align:left}
.art-content th{background:var(--sfondo)}
.aeo-box{border:2px solid var(--blu);border-radius:12px;padding:1.15rem 1.3rem;margin-bottom:1.65rem;background:linear-gradient(135deg,rgba(44,74,110,.07),rgba(255,107,53,.06))}
.aeo-box h2{font-family:'Montserrat',sans-serif;font-size:.95rem;text-transform:uppercase;letter-spacing:.06em;color:var(--blu);margin:0 0 .55rem;border:none;padding:0}
.check-block{background:var(--sfondo);border:1px solid var(--gc);border-left:4px solid var(--blu);border-radius:0 10px 10px 0;padding:1.1rem 1.25rem;margin:1.2rem 0}
.check-block h3{font-family:'Cormorant Garamond',serif;font-size:1.15rem;color:var(--nero);margin:0 0 .55rem}
.check-block ul{margin:.4rem 0 0 1.1rem;font-size:.86rem}
.check-block li{margin-bottom:.35rem}
.highlight-box{background:linear-gradient(135deg,var(--nero),var(--blu));border-radius:12px;padding:1.4rem 1.6rem;margin:1.6rem 0;color:#fff}
.highlight-box h3{color:var(--oro);font-family:'Cormorant Garamond',serif;font-size:1.25rem;margin-bottom:.5rem}
.highlight-box p,.highlight-box li{color:rgba(255,255,255,.78);font-size:.86rem}
.highlight-box ul{margin:.5rem 0 0 1.15rem}
.chart-wrap,.vignette-wrap{background:var(--sfondo);border:1px solid var(--gc);border-radius:12px;padding:1.2rem;margin:1.4rem 0}
.chart-wrap figcaption,.vignette-wrap figcaption{font-size:.72rem;color:var(--grigio);margin-top:.6rem;text-align:center;line-height:1.5}
.blog-fig{margin:1.65rem 0;border-radius:12px;overflow:hidden;border:1px solid var(--gc);background:#fff}
.blog-fig img{width:100%;height:auto;display:block;max-height:380px;object-fit:cover}
.blog-fig figcaption{font-size:.72rem;color:var(--grigio);padding:.7rem .95rem;background:var(--sfondo);line-height:1.55}
.righetto-sol{border:2px solid var(--oro);border-radius:12px;padding:1.15rem 1.3rem;margin:1.65rem 0 2rem;background:linear-gradient(135deg,rgba(255,107,53,.08),rgba(44,74,110,.05))}
.righetto-sol h2{font-family:'Montserrat',sans-serif;font-size:.95rem;text-transform:uppercase;letter-spacing:.06em;color:var(--oro);margin:0 0 .65rem;border:none;padding:0}
.righetto-sol ul{font-size:.84rem;margin:.75rem 0 .55rem 1.15rem}
.righetto-sol li{margin-bottom:.45rem}
blockquote{border-left:4px solid var(--oro);background:var(--sfondo);padding:1rem 1.2rem;margin:1.2rem 0;border-radius:0 8px 8px 0;font-style:italic;color:var(--grigio)}
.faq-item{border:1px solid var(--gc);border-radius:8px;margin-bottom:.5rem}
.faq-q{padding:.86rem .98rem;font-weight:600;font-size:.84rem;cursor:pointer}.faq-a{max-height:0;overflow:hidden;transition:max-height .35s;background:var(--sfondo)}
.faq-item.open .faq-a{max-height:480px}.faq-a-inner{padding:0 .98rem .86rem;font-size:.83rem;color:var(--grigio)}
.author-bio{display:flex;gap:1.08rem;padding:1.38rem;border:1px solid rgba(44,74,110,.12);border-radius:12px;margin:1.68rem 0}
.related{background:var(--sfondo);border:1px solid var(--gc);padding:1.32rem;border-radius:10px}
footer{background:linear-gradient(180deg,var(--nero),#0d1a2a);color:rgba(255,255,255,.65);padding:2.35rem 1.5rem;font-size:.75rem}
.skip-link{position:absolute;top:-100%;background:var(--oro);color:var(--nero);padding:.46rem .9rem;z-index:9999}.skip-link:focus{top:0}
@media(max-width:700px){.art-hero-img{height:260px}.art-hero h1{font-size:1.55rem}}
</style>
<link rel="stylesheet" href="css/blog-rich.css?v=3">
<link rel="stylesheet" href="css/blog-lead-form.css?v=2">"""

FOOTER = """
</main>
<footer><div class="fi">&copy; 2026 Gruppo Immobiliare Righetto — P.IVA 05182390285 — Via Roma 96, Limena (PD)</div></footer>
<script>document.querySelectorAll('.faq-q').forEach(function(q){q.addEventListener('click',function(){var p=this.parentElement,o=p.classList.contains('open');document.querySelectorAll('.faq-item.open').forEach(function(x){x.classList.remove('open');});if(!o)p.classList.add('open');});});</script>
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="js/config.js?v=4"></script>
<script src="js/rig-lead-form.js?v=2"></script>
<script src="js/nav-mobile.js?v=3" defer></script>
<script src="js/cookie-consent.js?v=3" defer></script>
</body></html>
"""

FAQS = [
    (
        "Perché un venditore dice «so tutto io» e poi la casa non si vende?",
        "Spesso il proprietario sopravvaluta il prezzo, sottovaluta la presentazione e rimanda documenti e manutenzione. L'acquirente moderno confronta decine di annunci online, calcola il costo dei lavori e se il prezzo non torna se ne va in silenzio senza fare offerte. L'agente esperto traduce questi segnali in azioni concrete: staging, APE, conformità e pricing basato su comparabili.",
    ),
    (
        "Quali documenti servono per vendere casa in Italia nel 2026?",
        "Servono documenti del venditore (identità, codice fiscale, stato civile se richiesto), dell'immobile (atto di provenienza, visura e planimetria catastale conformi, APE valido, titoli edilizi, eventuale agibilità), del condominio se applicabile, del mutuo se presente e del contratto di locazione se l'unità è affittata. Lista dettagliata nella guida documenti Righetto.",
    ),
    (
        "L'APE è obbligatorio per mettere in vendita un immobile?",
        "Sì. L'Attestato di Prestazione Energetica è obbligatorio in fase di compravendita (D.Lgs. 192/2005 e s.m.i.) e va allegato all'annuncio. Senza APE valido non si chiude seriamente una trattativa: l'acquirente e il notaio lo richiederanno comunque, causando ritardi e perdita di fiducia.",
    ),
    (
        "Quanto conta l'home staging per vendere casa a Padova?",
        "La presentazione è decisiva: crepe, muffe, pavimenti rovinati e ambienti disordinati fanno scendere la percezione di valore più di quanto risparmi un intervento minimo. Anche piccoli investimenti in tinteggiatura, pulizia profonda e riordino — o staging professionale — migliorano foto, visite e trattative. Approfondimento nella guida home staging Padova.",
    ),
    (
        "Cosa succede se il prezzo di vendita è troppo alto?",
        "Le visite arrivano, ma le offerte no. Gli acquirenti confrontano OMI, annunci simili e costi di ripristino; se i conti non tornano abbandonano la trattativa senza spiegazioni. Il risultato è un immobile «bruciato» sul mercato: dopo mesi si vende spesso a un prezzo inferiore a quello che si sarebbe ottenuto con un listino corretto dall'inizio.",
    ),
    (
        "Quali dati servono per una proposta d'acquisto?",
        "Di norma: documento d'identità e codice fiscale dell'acquirente, dati catastali (foglio, particella, subalterno), prezzo offerto, eventuali condizioni (mutuo, vendita di altro immobile) e dichiarazione su vincoli noti. L'agenzia formalizza la proposta; il notaio verifica tutto in fase di compromesso e rogito.",
    ),
]


def word_count(html: str) -> int:
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text.split()) if text else 0


def vignette_presuntuoso() -> str:
    return """<figure class="vignette-wrap" aria-label="Vignetta: venditore presuntuoso contro agente esperto">
<svg viewBox="0 0 520 200" width="100%" height="200" role="img">
<title>So tutto io versus agente con centinaia di vendite</title>
<rect x="10" y="20" width="230" height="160" rx="12" fill="#fff" stroke="#E1DBD1"/>
<text x="125" y="48" text-anchor="middle" font-size="11" fill="#152435" font-weight="700">IL VENDITORE</text>
<circle cx="125" cy="85" r="28" fill="#FF8F5E"/>
<text x="125" y="92" text-anchor="middle" font-size="22">🗣</text>
<text x="125" y="130" text-anchor="middle" font-size="13" fill="#C0392B" font-weight="700">«SO TUTTO IO»</text>
<text x="125" y="152" text-anchor="middle" font-size="9" fill="#6B7A8D">Forse 1 vendita in vita</text>
<rect x="280" y="20" width="230" height="160" rx="12" fill="#152435" stroke="#2C4A6E"/>
<text x="395" y="48" text-anchor="middle" font-size="11" fill="#fff" font-weight="700">L'AGENTE ESPERTO</text>
<circle cx="395" cy="85" r="28" fill="#2C4A6E"/>
<text x="395" y="92" text-anchor="middle" font-size="22">📊</text>
<text x="395" y="128" text-anchor="middle" font-size="11" fill="#FF6B35" font-weight="700">350+ immobili · dal 2000</text>
<text x="395" y="152" text-anchor="middle" font-size="9" fill="rgba(255,255,255,.6)">Ascolta il mercato, non l'ego</text>
<path d="M245 100 H272" stroke="#FF6B35" stroke-width="3" marker-end="url(#arr)"/>
<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L8,3 L0,6 Z" fill="#FF6B35"/></marker></defs>
</svg>
<figcaption>Vignetta ironica: l'esperienza sul campo batte la presunzione. Dati agenzia verificati: 350+ immobili, 101 comuni, dal 2000.</figcaption>
</figure>"""


def vignette_staging() -> str:
    return """<figure class="vignette-wrap" aria-label="Confronto immobile mal presentato e immobile curato">
<svg viewBox="0 0 520 220" width="100%" height="220" role="img">
<title>Prima e dopo presentazione immobile</title>
<rect x="15" y="30" width="235" height="150" rx="10" fill="#3d3d3d"/>
<text x="132" y="55" text-anchor="middle" font-size="10" fill="#fff">PRIMA</text>
<path d="M40 160 L80 120 L120 150 L160 100 L200 160" stroke="#8B4513" stroke-width="2" fill="none"/>
<ellipse cx="90" cy="130" rx="25" ry="18" fill="#5D4037" opacity=".7"/>
<text x="132" y="100" text-anchor="middle" font-size="28">🦠</text>
<text x="132" y="165" text-anchor="middle" font-size="9" fill="#FF6B6B">Muffa · crepe · pavimento rovinato</text>
<rect x="270" y="30" width="235" height="150" rx="10" fill="#F7F5F1" stroke="#2C4A6E"/>
<text x="387" y="55" text-anchor="middle" font-size="10" fill="#152435">DOPO STAGING</text>
<rect x="300" y="80" width="175" height="8" fill="#E1DBD1"/>
<rect x="300" y="100" width="120" height="40" fill="#2C4A6E" opacity=".15" rx="4"/>
<rect x="430" y="100" width="45" height="40" fill="#FF6B35" opacity=".25" rx="4"/>
<text x="387" y="165" text-anchor="middle" font-size="9" fill="#2C4A6E">Pulito · luminoso · neutro</text>
<text x="260" y="115" font-size="24" fill="#FF6B35">→</text>
</svg>
<figcaption>La prima impressione in visita (e nelle foto) decide se l'acquirente resta o guarda altrove — anche con investimenti minimi.</figcaption>
</figure>"""


def vignette_prezzo_silenzioso() -> str:
    return """<figure class="chart-wrap" aria-label="Grafico: prezzo alto e acquirenti che se ne vanno in silenzio">
<svg viewBox="0 0 520 240" width="100%" height="240" role="img">
<title>Prezzo fuori mercato: visite sì, offerte no</title>
<text x="260" y="22" text-anchor="middle" font-size="12" fill="#152435" font-weight="600">Prezzo troppo alto → nessuna offerta, partenza silenziosa</text>
<rect x="60" y="50" width="400" height="28" rx="6" fill="#ECE7DF"/>
<rect x="60" y="50" width="320" height="28" rx="6" fill="#2C4A6E"/>
<text x="260" y="69" text-anchor="middle" font-size="11" fill="#fff">Visite all'annuncio</text>
<rect x="60" y="95" width="400" height="28" rx="6" fill="#ECE7DF"/>
<rect x="60" y="95" width="80" height="28" rx="6" fill="#FF6B35"/>
<text x="260" y="114" text-anchor="middle" font-size="11" fill="#152435">Richieste di seconda visita</text>
<rect x="60" y="140" width="400" height="28" rx="6" fill="#ECE7DF"/>
<rect x="60" y="140" width="12" height="28" rx="6" fill="#C0392B"/>
<text x="260" y="159" text-anchor="middle" font-size="11" fill="#152435">Proposte d'acquisto scritte</text>
<text x="420" y="200" font-size="10" fill="#6B7A8D">«Guardo altrove»</text>
<text x="420" y="215" font-size="10" fill="#6B7A8D">senza dirlo</text>
<path d="M400 185 Q430 195 455 210" stroke="#6B7A8D" stroke-width="1.5" fill="none" stroke-dasharray="4"/>
</svg>
<figcaption>Schema qualitativo: con listino fuori mercato il funnel si restringe subito. Gli acquirenti oggi confrontano annunci e fanno i conti in tasca.</figcaption>
</figure>"""


def vignette_documenti() -> str:
    return """<figure class="vignette-wrap" aria-label="Vignetta: documenti mancanti bloccano la vendita">
<svg viewBox="0 0 520 200" width="100%" height="200" role="img">
<title>Documentazione incompleta ferma il rogito</title>
<rect x="180" y="25" width="160" height="130" rx="8" fill="#fff" stroke="#2C4A6E" stroke-width="2"/>
<text x="260" y="55" text-anchor="middle" font-size="11" fill="#152435" font-weight="700">ROGITO</text>
<text x="260" y="85" text-anchor="middle" font-size="32">⏸</text>
<text x="260" y="115" text-anchor="middle" font-size="9" fill="#C0392B">BLOCCATO</text>
<rect x="30" y="60" width="70" height="90" rx="4" fill="#ECE7DF" stroke="#C0392B"/>
<text x="65" y="100" text-anchor="middle" font-size="18" fill="#C0392B">✗</text>
<text x="65" y="165" text-anchor="middle" font-size="8" fill="#6B7A8D">APE</text>
<rect x="110" y="70" width="60" height="80" rx="4" fill="#ECE7DF" stroke="#C0392B"/>
<text x="140" y="105" text-anchor="middle" font-size="18" fill="#C0392B">✗</text>
<text x="140" y="165" text-anchor="middle" font-size="8" fill="#6B7A8D">Planimetria</text>
<rect x="350" y="65" width="65" height="85" rx="4" fill="#ECE7DF" stroke="#C0392B"/>
<text x="382" y="100" text-anchor="middle" font-size="18" fill="#C0392B">✗</text>
<text x="382" y="165" text-anchor="middle" font-size="8" fill="#6B7A8D">Condominio</text>
<rect x="425" y="75" width="65" height="75" rx="4" fill="#ECE7DF" stroke="#C0392B"/>
<text x="457" y="108" text-anchor="middle" font-size="18" fill="#C0392B">✗</text>
<text x="457" y="165" text-anchor="middle" font-size="8" fill="#6B7A8D">Abusi</text>
</svg>
<figcaption>Un documento mancante o un abuso non sanato = settimane perse e brutta figura davanti all'acquirente.</figcaption>
</figure>"""


def check_block(title: str, items: list[str]) -> str:
    lis = "".join(f"<li>{i}</li>" for i in items)
    return f'<div class="check-block" id="{title.lower().replace(" ", "-")[:20]}"><h3>{title}</h3><ul>{lis}</ul></div>'


def build_body() -> str:
    return f"""
<div class="aeo-box">
<h2>In sintesi</h2>
<p><strong>Vendere casa nel 2026 non è questione di presunzione ma di preparazione.</strong> Home staging (anche minimo), documentazione completa (APE, planimetria conforme, titoli edilizi), individuazione abusi e prezzo allineato al mercato decidono se ricevi offerte o solo visite che spariscono in silenzio. L'agente immobiliare esperto non «vuole abbassare il prezzo per commissione»: traduce ciò che gli acquirenti non dicono a voce alta. Guida operativa Righetto Immobiliare — Padova e 101 comuni, dal 2000.</p>
</div>

<p>Questa mattina, in agenzia, due conversazioni quasi speculari. Due proprietari convintissimi di sapere «come funziona il mercato» — prezzo, tempi, presentazione, documenti — pur avendo alle spalle, nella migliore delle ipotesi, <strong>una sola vendita nella vita</strong>, spesso quella della casa in cui vivono da vent'anni. Chiamiamo il primo <em>Marco</em> (persona fittizia: <strong>non pubblichiamo mai dati reali di clienti</strong> in articoli o social). Marco ha un trilocale a Ponte di Brenta con pavimenti graffiati, un angolo di muffa in bagno e un prezzo che «deve essere quello del vicino, più diecimila». Il secondo, <em>Paola</em>, ha la documentazione sparsa in tre cartelle, nessun APE aggiornato e la certezza che «tanto l'agente sistema tutto dopo». In entrambi i casi la diagnosi è la stessa: <strong>non è il mercato che non capisce loro — sono loro che non leggono il mercato</strong>.</p>

<p>Se ti riconosci anche solo in parte, questo articolo fa per te. Non è un insulto: è la fotografia di ciò che vediamo ogni settimana su <strong>350+ incarichi</strong> e <strong>101 comuni</strong> del Padovano. E se preferisci un confronto diretto, <a href="landing-consulenza-immobiliare-gratuita">prenota una consulenza gratuita</a>: portiamo numeri, non opinioni.</p>

{vignette_presuntuoso()}

<h2 id="presuntuoso">«So tutto io»: la frase che allontana le offerte</h2>

<p>Il venditore presuntuoso non è cattivo. È emotivamente legato all'immobile, ha ricordi in ogni stanza e confonde <strong>valore affettivo</strong> con <strong>prezzo di mercato</strong>. Il problema nasce quando questa convinzione blocca ogni ascolto: il parere dell'agente diventa «interesse economico», il parere dell'acquirente «offerta bassa da prendere in giro», il parere del tecnico «allarmismo».</p>

<p>In realtà l'acquirente del 2026 — soprattutto a Padova, con università, ospedali e pendolarismo verso Venezia e Mestre — <strong>arriva preparato</strong>. Ha visto venti annunci sulla stessa fascia di prezzo, ha stimato i costi di tinteggiatura e pavimento, ha letto la classe energetica. Se qualcosa non torna, <strong>non discute: se ne va</strong>. E tu resti con l'annuncio online, le visite che calano e la sensazione ingiusta che «nessuno capisce quanto vale casa mia».</p>

<blockquote>«So tutto io» è la frase più costosa in una vendita immobiliare. Costa tempo, costa offerte, costa reputazione dell'annuncio.</blockquote>

<p>L'agente immobiliare esperto — quello che ha chiuso centinaia di operazioni, non una — non ha bisogno di avere ragione a voce alta. Ha bisogno che l'immobile <strong>si venda</strong>. E per farlo mette sul tavolo tre leve misurabili: presentazione, documentazione, prezzo. Ignorarne una sola basta a mandare in fumo gli sforzi sulle altre due.</p>

<h2 id="presentazione">Home staging e manutenzione: l'effetto devastante della trascuratezza</h2>

<p>Marco mi ha detto: «Ma è abitabile, che vuoi di più?». Abitabile sì. <strong>Vendibile al massimo valore percepito</strong>, no. Crepe sul soffitto, muffa in bagno, pavimenti strisciati e cucina con ante scrostate non sono «dettagli»: sono <strong>segnali di costo futuro</strong> che l'acquirente sottrae mentalmente dal prezzo — o che usano per non fare alcuna offerta.</p>

<p>L'<a href="blog-home-staging-padova">home staging</a> non è lusso da rivista. È la disciplina di presentare l'immobile in modo neutro, luminoso e curato, in foto e in visita. A volte bastano <strong>poche centinaia di euro</strong>: tinteggiatura di un muro segnato, trattamento antimuffa documentato, lavaggio professionale dei pavimenti, rimozione di mobili ingombranti e personali. Altrove serve coordinare imbianchini e piccole riparazioni — sempre con preventivo chiaro prima di spendere.</p>

{vignette_staging()}

<figure class="blog-fig">
<img src="img/blog/blog-casa-vendibile-5-anni-case-green-padova-2026.webp" alt="Appartamento curato e luminoso pronto per la vendita nel Padovano" width="820" height="460" loading="lazy">
<figcaption>Un immobile che «fa bene» in foto e in visita riduce le obiezioni sul prezzo e accorcia i tempi di trattativa.</figcaption>
</figure>

<p>La regola che ripetiamo in <a href="servizio-vendita">servizio vendita</a> è semplice e reale: <strong>ogni difetto visibile è uno sconto non scritto</strong>. Meglio investire il minimo per eliminarlo prima dell'annuncio che regalarlo all'acquirente più cinico in trattativa. E le foto professionali — non scatti col telefono con luce gialla — non sono vanity: sono la prima visita, quella che filtra il 70% degli interessati.</p>

<h3>Cosa sistemare prima di mettere in vendita (anche con budget contenuto)</h3>
<ul>
<li><strong>Muffe e umidità</strong> — trattare la causa, non coprire con la vernice; in trattativa emergono sempre.</li>
<li><strong>Crepe e scrostature</strong> — stuccatura e tinteggiatura neutra; il soggiorno «fa prezzo».</li>
<li><strong>Pavimenti graffiati o ingialliti</strong> — levigatura, sigillatura o, dove serve, zona tappeto strategica in staging.</li>
<li><strong>Odori</strong> — cucina, animali, umidità: pulizia profonda e aerazione; in visita si sentono prima di vedere.</li>
<li><strong>Disordine e personalizzazione eccessiva</strong> — meno foto di famiglia, più spazio vuoto per immaginare la propria vita.</li>
</ul>

<h2 id="documenti">Documentazione completa: niente ritardi, niente brutte figure</h2>

<p>Paola aveva l'atto di acquisto del 1998 «da qualche parte» e la planimetria «quella che aveva il geometra». Intanto aveva già rifiutato di fare l'APE perché «costa e tanto non serve». Errore doppio: <strong>senza documenti ordinati non si va a compromesso serio</strong>, e senza APE non si è in regola né con la legge né con l'acquirente informato.</p>

<p>La vendita si inceppa quasi sempre <em>dopo</em> la prima visita entusiasta, quando il notaio o l'acquirente chiedono il pacchetto completo e saltano fuori lacune: planimetria non conforme, SCIA mancante per la veranda, regolamento condominiale mai chiesto, spese straordinarie non dichiarate. Ogni settimana di ritardo è un'occasione per l'acquirente di guardare l'annuncio accanto — magari più caro ma <strong>pronto al rogito</strong>.</p>

{vignette_documenti()}

<p>Per il dettaglio normativo e i costi indicativi rimandiamo alla <a href="blog-documenti-vendita-casa">guida documenti vendita casa 2026</a>. Qui sotto la <strong>checklist a blocchi</strong> che usiamo in mandato — da spuntare prima di pubblicare l'annuncio, non dopo la prima offerta.</p>

{check_block("Blocco 1 — Documenti del venditore", [
    "Carta d'identità o passaporto in corso di validità",
    "Codice fiscale / tessera sanitaria",
    "Certificato di stato civile se richiesto dal notaio (matrimonio, separazione, divorzio, regime patrimoniale)",
])}

{check_block("Blocco 2 — Documenti dell'immobile", [
    "Atto di provenienza (rogito, successione, donazione)",
    "Visura catastale aggiornata",
    "Planimetria catastale conforme allo stato di fatto",
    "Attestato di Prestazione Energetica (APE) in corso di validità",
    "Certificato di agibilità o storico, se disponibile",
    "Titoli edilizi: licenza, concessione, permesso di costruire, SCIA/CILA, eventuali sanatorie",
    "Certificazioni impianti (dove disponibili e richieste)",
    "Visura ipotecaria (di norma richiesta dal notaio)",
])}

{check_block("Blocco 3 — Se l'immobile è in condominio", [
    "Dichiarazione dell'amministratore con spese ordinarie pagate",
    "Eventuali lavori straordinari deliberati e quote ancora da versare",
    "Regolamento condominiale e tabelle millesimali (se richiesti)",
])}

{check_block("Blocco 4 — Se è presente un mutuo", [
    "Conteggio estintivo della banca",
    "Documentazione relativa all'ipoteca da cancellare",
])}

{check_block("Blocco 5 — Se l'immobile è locato", [
    "Contratto di locazione registrato",
    "Ricevute degli ultimi pagamenti del canone",
    "Comunicazioni su disdetta o diritto di prelazione, se applicabili",
])}

<figure class="blog-fig">
<img src="img/blog/blog-documenti-compravendita-rogito-padova-2026.webp" alt="Documenti per compravendita immobiliare e rogito a Padova" width="820" height="460" loading="lazy">
<figcaption>Ordine documentale = credibilità. L'acquirente serio preferisce pagare il giusto prezzo su un fascicolo completo piuttosto che risparmiare su un immobile «misterioso».</figcaption>
</figure>

<h2 id="ape">APE: non opzionale, fondamentale per vendere sul serio</h2>

<p>L'<strong>Attestato di Prestazione Energetica</strong> è obbligatorio in compravendita (D.Lgs. 192/2005 e s.m.i.) e va comunicato negli annunci. Non è burocrazia fine a sé: è il <strong>biglietto da visita energetico</strong> dell'immobile. Classe G o F su un bilocale di Arcella non spaventa solo per le bollette — segnala investimento futuro in cappotto o infissi che l'acquirente sconta dal prezzo offerto.</p>

<p>Mettere in vendita senza APE valido significa costruire su sabbia: la prima proposta seria si fermerà al notaio, o peggio all'istruttoria mutuo dell'acquirente. Il costo dell'APE è irrisorio rispetto a settimane di annuncio fermo e al danno di immagine. In <a href="servizio-valutazioni">valutazione gratuita</a> indichiamo anche la classe energetica attesa e se conviene un intervento rapido prima della foto.</p>

<h2 id="abusi">Abusi edilizi: meglio scoprirli prima, non al rogito</h2>

<p>Veranda chiusa senza titolo, bagno spostato, tettoia in giardino «fatta anni fa» — sono scenari quotidiani nel patrimonio padovano. Il venditore spesso dice: «Ma qui si vive da sempre così». L'acquirente, il notaio e la banca <strong>non possono chiudere un occhio</strong>. Abuso non sanato = rischio di sanatoria a carico del nuovo proprietario, mutuo negato, compromesso saltato.</p>

<p>Un'agenzia strutturata segnala subito le criticità urbanistiche e propone percorsi: CILA in sanatoria dove possibile, preventivo tecnico, adeguamento planimetria. Nascondere il problema non lo fa sparire — lo fa esplodere nel momento di massima tensione emotiva, quando tutti pensavano di aver chiuso.</p>

<h2 id="prezzo">Prezzo troppo alto: nessuna offerta, partenza in silenzio</h2>

<p>Ecco la verità che il venditore presuntuoso non vuole sentire: <strong>se il prezzo è fuori mercato, la gente non contrattica — guarda altrove</strong>. Non ti manda un messaggio educato «è caro». Semplicemente apre l'annuncio successivo, confronta €/m², calcola i lavori che hai mostrato con muffa e pavimento rovinato, e chiude la scheda.</p>

<p>Oggi tutti «sanno farsi i conti in tasca»: portali, simulatori, mutui online, chat con colleghi che hanno comprato l'anno scorso. Il tuo immobile compete con decine di alternative a portata di clic. L'agente esperto non abbassa il prezzo per sadismo: <strong>allinea aspettative e realtà</strong> usando comparabili venduti, quotazioni OMI e tempo medio di esposizione. Un listino corretto al giorno uno genera più visite <em>qualificate</em> e offerte scritte; un listino gonfiato genera complimenti in visita e zero proposte.</p>

{vignette_prezzo_silenzioso()}

<div class="highlight-box">
<h3>Segnali che il prezzo è fuori mercato</h3>
<ul>
<li>Molte visite, nessuna seconda visita con familiare o tecnico</li>
<li>Domande solo su «se scende molto» senza cifra concreta</li>
<li>Annuncio online da mesi senza trattative scritte</li>
<li>Feedback tipo «bello ma caro» ripetuto da agenti colleghi</li>
<li>Comparabili simili venduti a cifre sensibilmente inferiori</li>
</ul>
</div>

<p>Per approfondire tempi e strategie: <a href="blog-tempi-vendita-casa-padova">tempi vendita casa Padova</a> e <a href="blog-percorso-vendita-casa-padova-2026">percorso vendita</a>. La mediazione Righetto si concorda <strong>in sede</strong> nel mandato — non pubblichiamo percentuali online.</p>

<h2 id="proposta">Cosa serve per una proposta d'acquisto (lato acquirente)</h2>

<p>Quando finalmente arriva l'interessato giusto, serve chiudere senza attriti. Per la <strong>proposta d'acquisto</strong> di norma bastano:</p>
<ul>
<li>Documento d'identità dell'acquirente in corso di validità</li>
<li>Codice fiscale</li>
<li>Dati catastali dell'immobile (foglio, particella, subalterno)</li>
<li>Prezzo offerto e eventuali condizioni (mutuo, vendita altro immobile)</li>
<li>Dichiarazione su vincoli o ipoteche note</li>
</ul>

<p><strong>Esempio fittizio</strong> (formato tipico, dati inventati): Mario Rossi, nato a Padova, residente in Via Example 12, CIE AB00000CD, offerta € 198.000 sul subalterno 7, foglio 45 particella 123 — condizione sospensiva mutuo 80%. L'agenzia formalizza il documento; il notaio verifica in fase di compromesso. <em>Non inserire mai in chat o social documenti reali con numeri di carta d'identità: rischio privacy e truffe.</em></p>

<figure class="blog-fig">
<img src="img/blog/blog-checklist-verifiche-prima-compromesso-padova-2026.webp" alt="Checklist verifiche prima del compromesso immobiliare a Padova" width="820" height="460" loading="lazy">
<figcaption>Proposta, compromesso, rogito: ogni fase ha la sua documentazione. Anticiparla evita che l'acquirente si penta.</figcaption>
</figure>

<h2 id="agente">Perché l'agente immobiliare esperto ha (quasi) sempre ragione</h2>

<p>Non perché sia infallibile. Perché <strong>vede il mercato in tempo reale</strong>: quante visite, quali obiezioni, quali comparabili si sono tolti dall'annuncio, quali offerte sono cadute per planimetria. Il venditore vede la propria casa; l'agente vede il <em>posizionamento</em> della casa nel mercato. Sono due ottiche diverse.</p>

<p>Righetto Immobiliare opera dal <strong>2000</strong>, con <strong>98% di soddisfazione</strong> clienti e <strong>127 recensioni Google a 4,9/5</strong> — numeri verificabili, non slogan. Il nostro lavoro non è «vendere a qualunque costo»: è vendere al <strong>miglior equilibrio</strong> tra prezzo, tempi e serenità contrattuale. Se ti diciamo di sistemare la muffa, ordinare l'APE o rivedere il listino, non stiamo criticando le tue scelte di vita — stiamo proteggendo il risultato della vendita.</p>

<div class="righetto-sol">
<h2>Cosa può fare Righetto</h2>
<p style="font-size:.86rem;margin:0 0 .5rem"><strong>Il quesito:</strong> Venditore convinto di «sapere tutto» ma immobile fermo — come sbloccare presentazione, documenti e prezzo?</p>
<ul>
<li><strong>Sopralluogo e piano staging</strong> — Priorità interventi a budget contenuto (muffa, pavimenti, tinteggiatura) prima delle foto. (<a href="blog-home-staging-padova">guida home staging</a>)</li>
<li><strong>Audit documentale</strong> — Checklist venditore, catastale, condominiale, mutuo/locazione; APE e conformità urbanistica. (<a href="blog-documenti-vendita-casa">documenti vendita</a>)</li>
<li><strong>Valutazione comparativa</strong> — Prezzo allineato a venduti reali e OMI, non a sensazioni. (<a href="servizio-valutazioni">valutazione gratuita</a>)</li>
<li><strong>Commercializzazione e trattativa</strong> — Annuncio, visite, filtro acquirenti seri, proposta e compromesso fino al rogito. (<a href="servizio-vendita">servizio vendita</a>)</li>
</ul>
<p style="font-size:.78rem;color:var(--grigio);margin:0"><em>Compenso di mediazione concordato in sede nel mandato. Tel. 049.8843484 · <a href="landing-consulenza-immobiliare-gratuita">consulenza gratuita</a>.</em></p>
</div>

<p>Se dopo questa lettura ti senti ancora dire «so tutto io», va bene: almeno porta in agenzia i comparabili che hai guardato, il preventivo del pavimento e l'APE che hai rinviato. Confrontiamo i numeri. Spesso il silenzio del mercato è la risposta più educata che avresti potuto ricevere — e la più chiara.</p>

<h2 id="social">Perché pubblichiamo questa «verità scomoda» sui social</h2>

<p>Non per umiliare nessuno. Perché ogni settimana qualcuno perde <strong>mesi di esposizione</strong> convinto di avere ragione contro dati, visite e assenza di offerte. Un post diretto su home staging, documenti e prezzo corretto raggiunge chi non leggerebbe mai una guida da 2.500 parole — ma ha bisogno di sentirsi dire, senza filtri, che <strong>la muffa in foto si vede</strong>, che <strong>l'APE mancante ferma il compratore</strong>, che <strong>il prezzo gonfiato non genera trattativa</strong>.</p>

<p>Su Instagram, Facebook e LinkedIn condividiamo estratti di questo articolo con vignette e checklist utili: non è marketing aggressivo, è <strong>educazione al venditore consapevole</strong>. Chi si offende spesso è lo stesso che poi chiama dopo sei mesi di annuncio fermo chiedendo «perché nessuno fa offerte?». La risposta era già nell'ingresso, nel bagno e nel listino — solo che nessuno gliel'ha detta chiaramente.</p>

<h3>Checklist rapida «prima di dire no all'agente»</h3>
<ol>
<li>Hai confrontato almeno <strong>cinque venduti</strong> simili negli ultimi sei mesi (non solo annunci invenduti)?</li>
<li>Le foto sono state scattate <strong>dopo</strong> pulizia, tinteggiatura e rimozione disordine?</li>
<li>APE, planimetria e visura catastale sono <strong>sul tavolo</strong> prima della prima visita?</li>
<li>Hai chiesto all'amministratore la situazione <strong>spese e straordinari</strong>?</li>
<li>Un tecnico ha verificato <strong>difformità urbanistiche</strong> evidenti (verande, tamponamenti)?</li>
<li>Se dopo tre settimane non hai <strong>proposte scritte</strong>, sei disposto a rivedere il prezzo con dati verificabili e comparabili reali, non con sensazioni?</li>
</ol>

<p>Se anche una sola risposta è «no», il problema non è il mercato né l'agente: è la preparazione. E la buona notizia è che <strong>si sistema</strong> — spesso in poche settimane e con investimenti contenuti — se si smette di confondere orgoglio con strategia.</p>

<p>Per un piano su misura sul tuo immobile a Padova, Limena, Abano, Selvazzano o in provincia: <a href="contatti">contattaci</a> o compila il form in fondo pagina. Portiamo in riunione numeri, checklist e un piano staging realistico — non slogan. Perché vendere casa è già abbastanza stressante senza aggiungere presunzione alla lista. <strong>Il mercato non aspetta</strong>: ogni giorno con annuncio mal preparato è un giorno regalato alla concorrenza.</p>
"""


def faq_html() -> str:
    items = "".join(
        f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a"><div class="faq-a-inner">{a}</div></div></div>'
        for q, a in FAQS
    )
    return f'<div id="faq" style="margin-top:2rem"><h2 style="font-family:\'Cormorant Garamond\',serif;font-size:1.62rem;border-bottom:2px solid var(--oro);margin-bottom:.9rem">Domande frequenti</h2>{items}</div>'


def lead_form() -> str:
    return f"""<section class="blog-lead-wrap" id="richiedi-consulenza" aria-labelledby="blog-lead-title">
  <h2 id="blog-lead-title">Vuoi vendere senza brutte sorprese? Parliamone</h2>
  <form data-rig-lead-form data-provenienza="{SLUG}" data-pagina="{SLUG}" data-msg-prefix="[Blog]" novalidate>
    <div class="bl-fields">
      <label for="bl-nome">Nome e cognome *</label>
      <input type="text" id="bl-nome" required autocomplete="name" placeholder="Mario Rossi">
      <label for="bl-tel">Telefono *</label>
      <input type="tel" id="bl-tel" required autocomplete="tel" placeholder="333 123 4567">
      <label for="bl-email">Email</label>
      <input type="email" id="bl-email" autocomplete="email" placeholder="mario@email.it">
      <label for="bl-msg">Messaggio (opzionale)</label>
      <textarea id="bl-msg" placeholder="Comune, obiettivo vendita, dubbi su prezzo o documenti…"></textarea>
      <label class="bl-chk"><input type="checkbox" id="bl-gdpr" required> Ho preso visione dell'<a href="privacy" target="_blank" rel="noopener">informativa privacy</a> (Reg. UE 2016/679) e acconsento al trattamento per finalità contrattuali e di legge. *</label>
      <label class="bl-chk bl-chk-opt"><input type="checkbox" class="rig-gdpr-marketing" name="gdpr_marketing"> Acconsento al trattamento per finalità di marketing — <em>facoltativo</em>.</label>
      <button type="submit">Invia richiesta</button>
    </div>
    <div class="rig-lead-success">
      <h3>Messaggio inviato!</h3>
      <p>Grazie. Ti ricontattiamo entro pochi minuti negli orari di apertura.</p>
    </div>
  </form>
</section>"""


def build_html(body: str, wc: int) -> str:
    img = "img/blog/blog-documenti-compravendita-rogito-padova-2026.webp"
    meta_desc = (
        "Venditore presuntuoso? Home staging, documenti, APE e prezzo giusto per vendere a Padova. "
        "Guida provocatoria ma professionale di Righetto Immobiliare."
    )
    blog_obj = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": "«So tutto io»: vendite, home staging, documenti e prezzo — la verità dal campo",
        "description": meta_desc,
        "image": [f"https://righettoimmobiliare.it/{img}"],
        "author": {
            "@type": "Person",
            "name": "Gino Capon",
            "jobTitle": "Agente Immobiliare",
            "worksFor": {
                "@type": "RealEstateAgent",
                "name": "Gruppo Immobiliare Righetto di Capon Gino",
                "url": "https://righettoimmobiliare.it",
            },
        },
        "publisher": {
            "@type": "Organization",
            "name": "Righetto Immobiliare",
            "url": "https://righettoimmobiliare.it",
            "logo": {"@type": "ImageObject", "url": "https://righettoimmobiliare.it/img/og-default.webp"},
        },
        "datePublished": DATE_ISO,
        "dateModified": DATE_ISO,
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"https://righettoimmobiliare.it/{SLUG}"},
        "articleSection": "Guida alla vendita",
        "wordCount": wc,
        "inLanguage": "it-IT",
    }
    faq_obj = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in FAQS
        ],
    }
    rea_obj = {
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
        "geo": {"@type": "GeoCoordinates", "latitude": 45.4447, "longitude": 11.8454},
        "sameAs": [
            "https://www.facebook.com/righettoimmobiliare",
            "https://www.instagram.com/righettoimmobiliare",
            "https://www.linkedin.com/company/righetto-immobiliare",
        ],
        "hasMap": "https://maps.google.com/?q=45.476956,11.845762",
    }
    related = [
        ("Home staging Padova", "blog-home-staging-padova"),
        ("Documenti vendita casa 2026", "blog-documenti-vendita-casa"),
        ("Tempi vendita casa Padova", "blog-tempi-vendita-casa-padova"),
        ("Servizio vendita Righetto", "servizio-vendita"),
        ("Valutazione gratuita", "servizio-valutazioni"),
        ("Consulenza immobiliare gratuita", "landing-consulenza-immobiliare-gratuita"),
    ]
    rel = "".join(f'<li><a href="{u}">{t}</a></li>' for t, u in related)
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-9MHDHHES26"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-9MHDHHES26');</script>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#2C4A6E">
<title>«So tutto io»: staging, documenti, APE | Righetto</title>
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="dns-prefetch" href="https://cdn.jsdelivr.net">
<link rel="preload" href="fonts/montserrat-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="canonical" href="https://righettoimmobiliare.it/{SLUG}">
<meta property="og:type" content="article">
<meta property="og:title" content="«So tutto io»: forse una vendita in vita — e intanto la casa parla da sola">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="https://righettoimmobiliare.it/{SLUG}">
<meta property="og:image" content="https://righettoimmobiliare.it/{img}">
<meta property="article:published_time" content="{TIME_TS}">
<meta property="article:author" content="Gino Capon">
<meta property="article:section" content="Guida alla vendita">
<meta name="description" content="{meta_desc}">
<script type="application/ld+json">{json.dumps(blog_obj, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_obj, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://righettoimmobiliare.it/"},{"@type":"ListItem","position":2,"name":"Blog","item":"https://righettoimmobiliare.it/blog"},{"@type":"ListItem","position":3,"name":"So tutto io venditore presuntuoso"}]}, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(rea_obj, ensure_ascii=False)}</script>
<link rel="stylesheet" href="css/fonts.css?v=3"><link rel="stylesheet" href="css/nav-mobile.css?v=4">
<link rel="stylesheet" href="css/scroll-reveal.css?v=3" media="print" onload="this.media='all'">
{STYLE_BLOCK}
</head>
<body>
<a href="#main-content" class="skip-link">Contenuto principale</a>
<header><div class="hi">
  <a href="/" class="logo">Righetto <span>Immobiliare</span></a>
  <nav><a href="/">Home</a><a href="immobili">Immobili</a><a href="gino-capon">Profilo autore</a><a href="blog" class="active">Blog</a><a href="contatti">Contatti</a></nav>
  <a class="h-btn" href="landing-consulenza-immobiliare-gratuita">Valutazione gratuita</a>
</div><button class="nav-burger" id="burgerBtn" aria-label="Menu"><span></span><span></span><span></span></button></header>
<div class="nav-mobile" id="navMobile"><a href="/">Home</a><a href="immobili">Immobili</a><a href="gino-capon">Profilo autore</a><a href="blog">Blog</a><a href="contatti">Contatti</a></div>
<main id="main-content">
<div class="art-hero">
  <img class="art-hero-img" src="{img}" alt="Documenti e vendita immobiliare — guida al venditore preparato a Padova" width="1280" height="420" fetchpriority="high">
  <div class="art-hero-overlay"><div class="art-hero-inner">
    <div class="breadcrumb"><a href="/">Home</a> / <a href="blog">Blog</a> / Venditore e mercato</div>
    <span class="cat-badge">Verità dal campo</span>
    <h1><strong>«So tutto io»</strong> — ma di vendite ne ha fatta forse una, e la casa parla da sola</h1>
    <div class="art-hero-meta"><div class="av">G</div><span>Gino Capon</span><span>{DATE_IT}</span><span>12 min di lettura</span></div>
  </div></div>
</div>
<div class="art-container"><div class="art-content">
{body}
{faq_html()}
<div class="author-bio"><img src="img/team/titolari.webp" alt="Gino Capon Righetto Immobiliare" width="64" height="64" loading="lazy"><div><strong>Gino Capon</strong><p style="font-size:.8rem;color:#555">Fondatore Righetto Immobiliare — mediazione immobiliare Padova e provincia dal 2000.</p><p style="font-size:.78rem;margin-top:.4rem"><a href="gino-capon">Profilo autore</a></p></div></div>
<div class="related"><h3 style="font-family:'Cormorant Garamond',serif">Articoli correlati</h3><ul style="margin-left:1.1rem;margin-top:.4rem">{rel}</ul></div>
</div></div>
{lead_form()}
{FOOTER}"""


def patch_blog_html() -> None:
    path = ROOT / "blog.html"
    text = path.read_text(encoding="utf-8")
    entry = """{
      "titolo": "«So tutto io»: staging, documenti, APE e prezzo giusto",
      "categoria": "Guida alla vendita",
      "data": "2026-07-03",
      "stato": "pubblicato",
      "immagine_copertina": "img/blog/blog-documenti-compravendita-rogito-padova-2026.webp",
      "url_statico": "blog-so-tutto-io-venditore-presuntuoso-padova-2026",
      "tempo": 12,
      "autore": "Gino Capon",
      "contenuto": "Venditore presuntuoso vs mercato: home staging, checklist documenti, APE, abusi e prezzo silenzioso.",
      "evidenza": true
    },
"""
    marker = "  const articoliStatici = [\n"
    if SLUG in text:
        print("blog.html: voce già presente")
        return
    if marker not in text:
        raise RuntimeError("Marker articoliStatici non trovato in blog.html")
    text = text.replace(marker, marker + entry, 1)
    path.write_text(text, encoding="utf-8")
    print("OK blog.html aggiornato")


def patch_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    url = f"  <url><loc>https://righettoimmobiliare.it/{SLUG}</loc><lastmod>{DATE_ISO}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n"
    if SLUG in text:
        print("sitemap.xml: URL già presente")
        return
    marker = "  <url><loc>https://righettoimmobiliare.it/blog-stanza-universitaria-padova-canoni-2026</loc>"
    if marker in text:
        text = text.replace(marker, url + marker, 1)
    else:
        text = text.replace("</urlset>", url + "</urlset>", 1)
    path.write_text(text, encoding="utf-8")
    print("OK sitemap.xml aggiornato")


def patch_skimm_override() -> None:
    path = ROOT / "scripts" / "build_skimm.py"
    text = path.read_text(encoding="utf-8")
    key = f'    "{SLUG}":'
    if key in text:
        print("build_skimm.py: override già presente")
        return
    block = f'''    "{SLUG}": {{
        "kw_primaria": "venditore-presuntuoso-staging-documenti-ape",
        "angolo": "Verità dal campo / tono provocatorio — non guida tecnica staging o solo documenti",
        "intent": "vendita-mindset-venditore",
    }},
'''
    text = text.replace("ANGLE_OVERRIDES: dict[str, dict] = {\n", "ANGLE_OVERRIDES: dict[str, dict] = {\n" + block, 1)
    path.write_text(text, encoding="utf-8")
    print("OK build_skimm.py override aggiunto")


def patch_admin_html() -> None:
    path = ROOT / "admin.html"
    text = path.read_text(encoding="utf-8")
    if SLUG in text:
        print("admin.html: voce già presente")
        return
    entry = (
        "  { titolo: \"«So tutto io»: staging, documenti, APE e prezzo giusto\", categoria: \"Guida alla vendita\", "
        "data: '2026-07-03', tempo: 12, stato: 'pubblicato', autore: 'Gino Capon', emoji: '🎯', "
        "immagine_copertina: 'img/blog/blog-documenti-compravendita-rogito-padova-2026.webp', "
        f"url_statico: '{SLUG}', "
        "contenuto: \"<p>Venditore presuntuoso vs mercato: home staging, checklist documenti, APE, abusi e prezzo silenzioso.</p>\", "
        "evidenza: true, data_pubblicazione: '2026-07-03' },\n"
    )
    marker = "const _blogSeedArticles = [\n"
    if marker not in text:
        raise RuntimeError("Marker _blogSeedArticles non trovato")
    text = text.replace(marker, marker + entry, 1)
    path.write_text(text, encoding="utf-8")
    print("OK admin.html aggiornato")


def patch_homepage_js() -> None:
    path = ROOT / "js" / "homepage.js"
    text = path.read_text(encoding="utf-8")
    map_key = "«so tutto io»: staging, documenti, ape e prezzo giusto"
    if SLUG in text and map_key in text:
        print("homepage.js: voce già presente")
        return
    static_entry = (
        "    '«so tutto io»: staging, documenti, ape e prezzo giusto': "
        "{ img: 'img/blog/blog-documenti-compravendita-rogito-padova-2026.webp', "
        f"url: '{SLUG}' }},\n"
    )
    marker = "  const staticMap = {\n"
    if marker in text and map_key not in text:
        text = text.replace(marker, marker + static_entry, 1)
    art_entry = """    {
      "titolo": "«So tutto io»: staging, documenti, APE e prezzo giusto",
      "categoria": "Guida alla vendita",
      "data": "2026-07-03",
      "stato": "pubblicato",
      "immagine_copertina": "img/blog/blog-documenti-compravendita-rogito-padova-2026.webp",
      "url_statico": "blog-so-tutto-io-venditore-presuntuoso-padova-2026"
    },
"""
    art_marker = '  const articoliStatici = [\n'
    if art_marker in text and SLUG not in text:
        text = text.replace(art_marker, art_marker + art_entry, 1)
    path.write_text(text, encoding="utf-8")
    print("OK homepage.js aggiornato")


def main() -> None:
    body = build_body()
    wc = word_count(body)
    if wc < MIN_BODY_WORDS:
        raise SystemExit(f"Corpo insufficiente: {wc} < {MIN_BODY_WORDS}")
    out = ROOT / FILENAME
    html = build_html(body, wc)
    out.write_text(html, encoding="utf-8")
    print(f"OK {FILENAME} — {wc} parole corpo")
    patch_blog_html()
    patch_sitemap()
    patch_admin_html()
    patch_homepage_js()
    patch_skimm_override()


if __name__ == "__main__":
    main()
