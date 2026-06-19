# -*- coding: utf-8 -*-
"""Genera articolo blog Bonus edilizi 2026 — 18 giugno 2026. Esegui da repo root:
python scripts/build_bonus_edilizi_giugno18.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

import build_giugno03_blog_batch as g03  # noqa: E402

g03.DATE_IT = "18 giugno 2026"
g03.DATE_ISO = "2026-06-18"
g03.TIME_TS = "2026-06-18T09:00:00+02:00"

from build_giugno03_blog_batch import (  # noqa: E402
    FOOTER,
    aeo_box,
    build_article,
    faq_html,
    sources_table,
)

ROOT = _SCRIPT_DIR.parent
OUT_IMG = ROOT / "img" / "blog" / "blog-bonus-edilizi-2026-incentivi-casa-padova.webp"
HERO_SRC = Path(
    r"C:\Users\Utente\.cursor\projects\c-Users-Utente-progetti-index\assets\blog-hero-bonus-edilizi-2026.png"
)

ARTICLE = {
    "filename": "blog-bonus-edilizi-2026-incentivi-casa-padova.html",
    "slug": "blog-bonus-edilizi-2026-incentivi-casa-padova",
    "img": "img/blog/blog-bonus-edilizi-2026-incentivi-casa-padova.webp",
    "bread": "Bonus edilizi 2026 Padova",
    "section": "Fisco e ristrutturazioni",
    "html_title": "Bonus edilizi 2026 Padova: detrazioni 50% e ecobonus | Righetto",
    "og_title": "Legge 199/2025: bonus ristrutturazione 50% prima casa, ecobonus e sismabonus nel Padovano",
    "schema_headline": "Bonus edilizi 2026: detrazioni casa, ecobonus e sismabonus — guida per Padova",
    "meta_desc": "Legge 199/2025: detrazione 50% prima casa e 36% altrove fino al 2026, max 96.000€. Ecobonus, sismabonus e impatto su vendita a Padova.",
    "cat_badge": "Fisco e ristrutturazioni",
    "alt_img": "Ristrutturazione edilizia e incentivi fiscali 2026 — illustrazione editoriale bonus casa ed efficienza energetica Padova",
    "breadcrumb_tail": "Bonus edilizi 2026",
    "h1": "<strong>Bonus edilizi 2026</strong>: detrazioni 50% e 36%, ecobonus e sismabonus per chi compra o ristruttura a Padova",
    "cap_img": (
        '<p class="cap-img">Immagine <strong>illustrativa</strong> su ristrutturazioni e agevolazioni fiscali — '
        'non è un documento ufficiale. Percentuali e massimali da '
        '<a href="https://www.agenziaentrate.gov.it/portale/la-misura-della-detrazione-limiti-detraibilita" '
        'target="_blank" rel="noopener noreferrer">Agenzia delle Entrate</a> e '
        '<a href="https://www.gazzettaufficiale.it" target="_blank" rel="noopener noreferrer">Legge 199/2025</a> '
        '(G.U. n. 301 del 30 dicembre 2025).</p>'
    ),
    "aeo": aeo_box(
        "Per <strong>proprietari, acquirenti e venditori nel Padovano</strong> che nel 2026 valutano "
        "ristrutturazioni, efficientamento energetico o messa a norma sismica prima di vendere o dopo l'acquisto.",
        [
            "La <strong>Legge di Bilancio 2026 (L. 199/2025)</strong> conferma per le spese del 2026 "
            "detrazione <strong>50%</strong> sull'abitazione principale e <strong>36%</strong> negli altri casi "
            "per bonus ristrutturazione, ecobonus e sismabonus.",
            "Il <strong>massimale agevolabile</strong> per il bonus ristrutturazioni è "
            "<strong>96.000 euro</strong> per unità immobiliare (fonte ADE).",
            "Sono <strong>cessati</strong> superbonus e bonus verde; il bonus barriere architettoniche "
            "è confluito nel bonus ristrutturazioni.",
            "Per l'ecobonus dal 2025-2027 <strong>non</strong> spettano incentivi sulla sostituzione "
            "con caldaie a combustibili fossili (ADE).",
        ],
        [
            "Non è consulenza fiscale personalizzata — verificare con commercialista.",
            "Non duplica l'articolo su <a href=\"blog-bonus-mobili-2026-massimizzare-ristrutturazioni\">bonus mobili</a> "
            "(focus arredi ed elettrodomestici).",
            "Non promette aumento automatico del prezzo di vendita post bonus.",
        ],
    ),
    "body_extra": """<h2>Cosa cambia con la Legge di Bilancio 2026</h2>
<p>La <strong>Legge 30 dicembre 2025, n. 199</strong> (Legge di Bilancio 2026), pubblicata in Gazzetta Ufficiale n. 301 del 30 dicembre 2025, conferma un sistema di bonus edilizi «ordinari» più stabile rispetto al biennio del superbonus. Restano attivi il <strong>bonus ristrutturazioni</strong> (art. 16-bis TUIR), l'<strong>ecobonus</strong> (art. 14 D.L. 63/2013) e il <strong>sismabonus</strong> (art. 16 D.L. 63/2013), con due aliquote differenziate già applicate nel 2025 e prorogate per tutto il 2026. Per chi possiede o acquista un immobile a <strong>Padova</strong>, in <strong>Limena</strong> o nei <strong>101 comuni</strong> del nostro raggio operativo, la scelta tra ristrutturare prima della vendita o subito dopo l'acquisto passa da queste percentuali, dai massimali e dagli obblighi documentali — non da slogan pubblicitari.</p>
<h2>Tabella comparativa bonus edilizi 2026 — aliquote e massimali</h2>
<table>
<thead><tr><th>Agevolazione</th><th>Prima casa 2026</th><th>Altre abitazioni 2026</th><th>Massimale / nota</th><th>Fonte</th></tr></thead>
<tbody>
<tr><td>Bonus ristrutturazioni</td><td>50% IRPEF</td><td>36% IRPEF</td><td>96.000 € per unità</td><td><a href="https://www.agenziaentrate.gov.it/portale/la-misura-della-detrazione-limiti-detraibilita" target="_blank" rel="noopener noreferrer">ADE</a></td></tr>
<tr><td>Ecobonus</td><td>50%</td><td>36%</td><td>Variabile per tipologia intervento</td><td>L. 199/2025 + ADE</td></tr>
<tr><td>Sismabonus</td><td>50%</td><td>36%</td><td>Variabile per classe rischio e intervento</td><td>L. 199/2025 + ADE</td></tr>
<tr><td>Bonus mobili / elettrodomestici</td><td>50% (se collegato a ristrutturazione)</td><td>—</td><td>5.000 € — vedi articolo dedicato</td><td><a href="blog-bonus-mobili-2026-massimizzare-ristrutturazioni">Bonus mobili 2026</a></td></tr>
<tr><td>Superbonus 110%</td><td>—</td><td>—</td><td><strong>Cessato</strong></td><td>L. 199/2025</td></tr>
<tr><td>Bonus verde</td><td>—</td><td>—</td><td><strong>Cessato</strong></td><td>L. 199/2025</td></tr>
</tbody>
</table>
<p>La detrazione si ripartisce in <strong>10 quote annuali</strong> di pari importo nell'imposta lorda (disciplina generale bonus edilizi, portale ADE). Dal 2027 le aliquote sono destinate a scendere (36% / 30% secondo quadro normativo aggiornato dalla manovra): chi pianifica lavori nel Padovano nel 2026 opera nell'ultimo anno del biennio al 50% sull'abitazione principale.</p>
<h2>Bonus ristrutturazioni: chi può accedere al 50%</h2>
<p>L'<a href="https://www.agenziaentrate.gov.it" target="_blank" rel="noopener noreferrer">Agenzia delle Entrate</a> chiarisce che per le spese del 2025-2026 la detrazione del <strong>50%</strong>, con limite di spesa agevolabile di <strong>96.000 euro</strong>, spetta per interventi sull'unità immobiliare adibita ad <strong>abitazione principale</strong> dai titolari di diritto di proprietà o di diritto reale di godimento. Negli altri casi in cui l'agevolazione è ammessa, l'aliquota è del <strong>36%</strong> con lo stesso massimale. Interventi tipici: manutenzione straordinaria, restauro conservativo, ristrutturazione edilizia, adeguamento impianti, opere su parti comuni. In semicentro padovano e in edifici anni '60-'80 di <strong>Arcella</strong> o <strong>Mandria</strong>, spesso si incrociano bonus ristrutturazione e necessità di aggiornare impianti: documentare il cantiere prima del marketing è parte della valorizzazione in vendita.</p>
<h3>Requisito abitazione principale e acquisti recenti</h3>
<p>Per usufruire dell'aliquota maggiorata, l'unità deve essere abitazione principale del contribuente. Per interventi su fabbricati interi acquistati da ristrutturare, l'ADE richiede che l'immobile sia adibito ad abitazione principale entro il termine di presentazione della dichiarazione dei redditi relativa all'anno in cui si fruisce per la prima volta della detrazione. Chi compra da ristrutturare in <a href="zona-arcella-padova">zona Arcella</a> o in periferia deve coordinare rogito, residenza anagrafica e tempi fiscali con il commercialista — noi supportiamo la parte urbanistica e di mercato, non la pianificazione fiscale.</p>""",
    "body_mid": """<h2>Ecobonus 2026: efficienza energetica e vincoli tecnici</h2>
<p>L'ecobonus mantiene nel 2026 le stesse aliquote del bonus ristrutturazioni: <strong>50%</strong> sull'abitazione principale, <strong>36%</strong> altrove. Gli interventi riguardano isolamento, sostituzione impianti con tecnologie efficienti, infissi, schermature solari e altre tipologie elencate nelle guide ADE e ENEA. Novità rilevante: per le spese 2025-2027 <strong>non</strong> sono più incentivati gli interventi di sostituzione di impianti di climatizzazione invernale con caldaie uniche alimentate a combustibili fossili (fonte ADE, aggiornamenti 2025-2026). A Padova, dove la <a href="blog-direttiva-case-green-limena-padova">Direttiva Case Green</a> spinge verso classi energetiche migliori, l'ecobonus resta uno strumento per chi vuole migliorare l'APE prima di vendere o locare — ma l'obbligo di comunicazione dati a <strong>ENEA</strong> è stringente: l'omissione comporta decadenza dall'agevolazione, con possibilità di remissione in bonis secondo le regole vigenti.</p>
<h3>APE, mercato e percezione dell'acquirente</h3>
<p>Un intervento ecobonus documentato non garantisce da solo un premio di prezzo: l'acquirente confronta comparabili OMI, stato impianti e costi condominiali. Tuttavia, in trattativa su bilocali del <strong>centro universitario</strong> o su villette in <a href="zona-limena">Limena</a>, un APE migliorato e fatture in ordine riducono richieste di ribasso. Incrociare bonus fiscale e strategia di vendita è tema dell'articolo <a href="blog-tasse-vendita-casa">tasse e vendita casa</a>.</p>
<h2>Sismabonus: rilevanza nel Padovano</h2>
<p>Il territorio padovano non è sismicità estrema come altre aree italiane, ma il sismabonus resta utile per adeguamenti strutturali su edifici vulnerabili, ampliamenti e interventi previsti dalla normativa antisismica. Aliquote 2026: 50% / 36% come gli altri bonus ordinari. Prima di avviare lavori strutturali verificare classificazione del comune, tipologia intervento e massimali con tecnico abilitato e commercialista.</p>
<h2>Cosa non c'è più nel 2026</h2>
<ul>
<li><strong>Superbonus 110%</strong> — definitivamente fuori dal quadro 2026 (L. 199/2025).</li>
<li><strong>Bonus verde</strong> (sistemazione aree verdi) — cessato.</li>
<li><strong>Bonus barriere architettoniche al 75%</strong> — interventi rientrano nel bonus ristrutturazioni con aliquote ordinarie.</li>
<li><strong>Ecobonus su caldaie a fossili</strong> — escluso per spese 2025-2027 (ADE).</li>
</ul>
<p>Chi aveva pianificato lavori «in stile superbonus» deve ricalibrare su detrazioni ordinarie e tempi di detrazione in 10 anni, non su crediti cedibili.</p>
<h2>Plafond detrazioni per redditi elevati</h2>
<p>La Legge di Bilancio 2025 (L. 207/2024, art. 1 comma 10) ha introdotto dall'anno d'imposta 2025 un <strong>limite complessivo</strong> agli oneri detraibili per contribuenti con reddito complessivo superiore a <strong>75.000 euro</strong> (art. 16-ter TUIR). Le rate residue di bonus pagate fino al 31 dicembre 2024 restano escluse dal calcolo del plafond (ADE). Famiglie ad alto reddito nel Padovano che ristrutturano ville in campagna o attici in centro devono simulare l'impatto con il commercialista prima di firmare preventivi.</p>""",
    "body_tail": """<h2>Bonus edilizi e compravendita: timing a Padova</h2>
<p><strong>Per chi vende:</strong> completare lavori, aggiornare APE e planimetrie catastali prima del caricamento su portali evita trattative congelate da perizie bancarie o da richieste di sconto. Le detrazioni già fruite non si trasferiscono automaticamente al compratore come «valore aggiunto» in rogito: conta la qualità percepita dell'immobile. <strong>Per chi compra:</strong> un appartamento «da ristrutturare» in <strong>Saoneria</strong> o <strong>Torre</strong> può essere opportunità se il prezzo di acquisto sconta i lavori; verificare vincoli del centro storico e costi reali prima di contare sulla detrazione.</p>
<h3>Documenti e pagamenti tracciabili</h3>
<p>Le agevolazioni richiedono in genere <strong>pagamenti tracciabili</strong> (bonifico con causale, assegni bancari o postali dove previsto), fatture e conservazione documentale per tutta la durata degli obblighi fiscali. Per l'ecobonus, comunicazione ENEA. In parallelo, per la vendita servono conformità urbanistico-catastale e libretti impianti — vedi <a href="blog-documenti-vendita-casa">documenti per la vendita</a>.</p>
<h2>Collegamento con mutuo e ristrutturazione</h2>
<p>Chi finanzia acquisto + lavori con mutuo deve distinguere costo immobile, costo ristrutturazione e capacità di detrazione annua sulle 10 quote. La Banca d'Italia monitora condizioni di credito; i tassi seguono anche le decisioni BCE (<a href="blog-bce-tassi-mutui-giugno-2026-padova">mutui giugno 2026</a>). Una consulenza immobiliare gratuita aiuta a capire se conviene comprare già ristrutturato o intervenire dopo il rogito — senza sostituire il piano fiscale.</p>
<h2>Checklist operativa proprietario padovano 2026</h2>
<ol>
<li>Verificare su portale ADE aliquote e massimali aggiornati per l'anno di sostenimento della spesa.</li>
<li>Definire se l'immobile è o sarà abitazione principale (50% vs 36%).</li>
<li>Scegliere impresa con DURC e contratti chiari; evitare lavori in nero se si punta alla detrazione.</li>
<li>Per ecobonus: pianificare invio dati ENEA e aggiornamento APE post-intervento.</li>
<li>Se obiettivo è vendita entro 24 mesi: allineare fine cantiere, certificazioni e <a href="servizio-vendita">strategia di messa in vendita</a>.</li>
<li>Per mobili ed elettrodomestici dopo ristrutturazione: leggere <a href="blog-bonus-mobili-2026-massimizzare-ristrutturazioni">bonus mobili 2026</a>.</li>
</ol>
<h2>Sintesi per il mercato padovano</h2>
<p>Il 2026 chiude un biennio favorevole per chi ristruttura l'abitazione principale al <strong>50%</strong>, con massimale <strong>96.000 euro</strong> sul bonus ristrutturazioni. Ecobonus e sismabonus seguono la stessa logica prima casa / altro; superbonus e bonus verde sono storia. Nel Padovano, dove convivono stock anni '70 da efficientare e nuove costruzioni già in classe A, il bonus è leva fiscale — non sostituto di una valutazione di mercato fondata su OMI e comparabili reali. Per orientamento sulla vendita o sull'acquisto con lavori: <a href="landing-consulenza-immobiliare-gratuita">consulenza gratuita</a> in agenzia; per percentuali e dichiarazioni: commercialista e <a href="https://www.agenziaentrate.gov.it" target="_blank" rel="noopener noreferrer">Agenzia delle Entrate</a>.</p>
<div class="warn"><strong>Fonti:</strong> Legge 199/2025 (G.U. 301/2025), portale Agenzia delle Entrate (misura detrazione e limiti), comunicazioni ENEA per ecobonus. Percentuali riferite alle spese sostenute nel 2026; verificare aggiornamenti legislativi successivi.</div>""",
    "sources": sources_table([
        ("Aliquote 50% / 36% 2026", "Agenzia delle Entrate — bonus ristrutturazioni", "Massimale 96.000 €, prima casa"),
        ("Legge di Bilancio 2026", "Legge 199/2025 — Gazzetta Ufficiale", "Proroghe e cessazioni bonus"),
        ("Ecobonus e caldaie fossili", "Agenzia delle Entrate — guide 2025-2026", "Esclusioni e comunicazione ENEA"),
        ("Plafond redditi > 75.000 €", "L. 207/2024 art. 16-ter TUIR", "Limite detrazioni complessive"),
        ("Mercato locale post-lavori", "OMI + pratica agenziale Padova", "Pricing realistico post ristrutturazione"),
    ]),
    "topic": "bonus edilizi 2026 detrazioni ristrutturazione ecobonus sismabonus Padova abitazione principale",
    "anchors": [
        ("bonus mobili ristrutturazioni", "blog-bonus-mobili-2026-massimizzare-ristrutturazioni"),
        ("tasse vendita casa", "blog-tasse-vendita-casa"),
        ("direttiva case green", "blog-direttiva-case-green-limena-padova"),
        ("documenti vendita", "blog-documenti-vendita-casa"),
        ("consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
    ],
    "body_n": 14,
    "faqs": [
        (
            "Quali aliquote bonus edilizi nel 2026?",
            "Per spese sostenute nel 2026: detrazione IRPEF del 50% sull'abitazione principale e del 36% negli altri casi ammessi, per bonus ristrutturazioni, ecobonus e sismabonus (fonte Agenzia delle Entrate e Legge 199/2025).",
        ),
        (
            "Qual è il massimale bonus ristrutturazioni?",
            "96.000 euro per unità immobiliare secondo la scheda ADE sulla misura della detrazione; ripartizione in 10 quote annuali.",
        ),
        (
            "Il superbonus esiste ancora nel 2026?",
            "No. La Legge di Bilancio 2026 non proroga il superbonus 110%; restano i bonus ordinari con aliquote 50% / 36%.",
        ),
        (
            "Ecobonus e caldaie a gas: cosa cambia?",
            "Per spese 2025-2027 non sono incentivati interventi di sostituzione con caldaie uniche a combustibili fossili (Agenzia delle Entrate).",
        ),
        (
            "I bonus aumentano il prezzo di vendita a Padova?",
            "Non automaticamente. Contano qualità dei lavori, APE aggiornato e confronto con immobili simili venduti (OMI e comparabili).",
        ),
        (
            "Righetto fornisce assistenza fiscale sui bonus?",
            "No: supportiamo compravendita, valutazioni e coordinamento documentale immobiliare; per detrazioni rivolgersi a commercialista e ADE.",
        ),
    ],
    "related": [
        ("Bonus mobili 2026", "blog-bonus-mobili-2026-massimizzare-ristrutturazioni"),
        ("Tasse sulla vendita casa", "blog-tasse-vendita-casa"),
        ("Direttiva Case Green Limena", "blog-direttiva-case-green-limena-padova"),
    ],
    "cta_primary": ("Consulenza gratuita", "landing-consulenza-immobiliare-gratuita"),
    "cta_secondary": ("Valutazione immobile", "landing-valutazione"),
    "registry": {
        "titolo": "Bonus edilizi 2026: detrazioni 50% e ecobonus per Padova",
        "categoria": "Fisco e ristrutturazioni",
        "tempo": 12,
        "contenuto": "Legge 199/2025: 50% prima casa, 36% altrove, max 96.000€. Ecobonus, sismabonus e checklist per il Padovano.",
        "evidenza": True,
        "emoji": "🏗️",
    },
}


def hero_to_webp() -> None:
    from PIL import Image

    if not HERO_SRC.is_file():
        raise SystemExit(f"Manca hero PNG: {HERO_SRC}")
    OUT_IMG.parent.mkdir(parents=True, exist_ok=True)
    tw, th = 1200, 630

    def cover(img: Image.Image) -> Image.Image:
        sw, sh = img.size
        scale = max(tw / sw, th / sh)
        nw, nh = int(sw * scale), int(sh * scale)
        img = img.resize((nw, nh), Image.Resampling.LANCZOS)
        left = (nw - tw) // 2
        top = int((nh - th) * 0.38)
        return img.crop((left, top, left + tw, top + th))

    with Image.open(HERO_SRC) as im:
        rgb = im.convert("RGB") if im.mode != "RGB" else im
        out = cover(rgb)
    out.save(OUT_IMG, "WEBP", quality=86, method=6)
    print(f"Hero WebP: {OUT_IMG} ({OUT_IMG.stat().st_size // 1024} KB)")


def main() -> int:
    hero_to_webp()
    html, wc = build_article(ARTICLE)
    out_path = ROOT / ARTICLE["filename"]
    out_path.write_text(html, encoding="utf-8")
    print(f"OK {out_path.name} — body ~{wc} parole")

    reg = {
        "generated": "2026-06-18",
        "blog_html_articoliStatici": [
            {
                "titolo": ARTICLE["registry"]["titolo"],
                "categoria": ARTICLE["registry"]["categoria"],
                "data": "2026-06-18",
                "stato": "pubblicato",
                "immagine_copertina": ARTICLE["img"],
                "url_statico": ARTICLE["slug"],
                "tempo": ARTICLE["registry"]["tempo"],
                "autore": "Gino Capon",
                "contenuto": ARTICLE["registry"]["contenuto"],
                "evidenza": ARTICLE["registry"]["evidenza"],
            }
        ],
        "admin_blogSeedArticles": [
            {
                **ARTICLE["registry"],
                "data": "2026-06-18",
                "stato": "pubblicato",
                "autore": "Gino Capon",
                "immagine_copertina": ARTICLE["img"],
                "url_statico": ARTICLE["slug"],
                "data_pubblicazione": "2026-06-18T09:00:00+02:00",
            }
        ],
        "homepage_js_articoliStatici": [
            {
                "titolo": ARTICLE["registry"]["titolo"],
                "categoria": ARTICLE["registry"]["categoria"],
                "data": "2026-06-18",
                "stato": "pubblicato",
                "immagine_copertina": ARTICLE["img"],
                "url_statico": ARTICLE["slug"],
            }
        ],
    }
    reg_path = ROOT / "scripts" / "bonus_edilizi_giugno18_registry.json"
    reg_path.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Registry: {reg_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
