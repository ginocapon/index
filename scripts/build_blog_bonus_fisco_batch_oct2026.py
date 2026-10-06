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
    """VIETATO — skill-content §2.0d / righetto-blog-publish (no filler a elenco di <p>)."""
    raise RuntimeError("_pad() disabilitato: usare H2/H3, ul/ol o FAQ — non liste EXP*")


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

# Liste EXP rimosse — skill-content §2.0d (no padding a <p>)

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

# Liste EXP rimosse — skill-content §2.0d (no padding a <p>)
# Liste EXP rimosse — skill-content §2.0d (no padding a <p>)
