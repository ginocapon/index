# SKILL-CONTENT — Righetto Immobiliare
> Carica per: scrivere articoli blog, creare zone page, descrizioni immobili, ottimizzazione semantica.
> Versione estratta da SKILL-2.0.md — Marzo 2026

---

## 1. CLUSTER CONTENUTI (Stato Marzo 2026)

### Cluster "Vendere Casa Padova" ✅ COMPLETO
- servizio-vendita.html, blog-costi-vendere-casa-padova-2026.html
- landing-vendere-casa-padova.html, blog-documenti-vendita-casa.html
- blog-tasse-vendita-casa.html, blog-tempi-vendita-casa-padova.html

### Cluster "Comprare Casa Padova" ✅ COMPLETO
- blog-comprare-casa-padova-guida-2026.html, blog-mutuo-prima-casa-padova.html
- blog-agevolazioni-prima-casa-2026.html, blog-successione-immobiliare-padova.html
- blog-investire-immobiliare-padova.html

### Cluster "Quartieri Padova" ✅ COMPLETO
- blog-quartieri-padova-2026.html, agenzia-immobiliare-padova.html (pillar)
- 14 pagine zona-*.html (limena, vigonza, abano-terme, selvazzano + altri 10)

### Cluster "Affitto Padova" ✅ COMPLETO
- blog-affitto-studenti-padova.html, servizio-locazioni.html
- blog-contratto-affitto-padova.html, blog-rendimento-affitto-padova.html
- blog-affitti-padova-canoni-2026.html, blog-checklist-affitto-studenti-padova-2026.html

### Sotto-cluster "Housing Veneto 2026" (studenti + lavoratori) — luglio 2026
Filone editoriale: **canoni stanze**, **studentati ESU/PNRR/privati**, **residenze green**, **Vicenza calmierati**, **housing lavoratori Edilcassa**. Fonti obbligatorie: Immobiliare.it Insights, FIMAA, ESU Padova, Università Padova, Edilcassa/Confartigianato Veneto — **non** citare titoli o testi di testate locali come fonte.
- blog-stanza-universitaria-padova-canoni-2026.html (Linda — Insights +46% vs 2020)
- blog-studentati-veneto-2026-posti-letto.html (Linda — ESU, Camplus, PNRR)
- blog-residenze-green-padova-tribloc-2026.html (Linda — riuso NZEB via Gozzi)
- blog-vicenza-residenze-universitarie-calmierate-2026.html (Linda — PNRR calmierati)
- blog-housing-lavoratori-veneto-edilcassa-2026.html (Gino — fondo garanzia contratto edile)
Script batch: `scripts/build_blog_housing_veneto_lug2026.py` + `register_housing_veneto_lug2026.py`

---

## 2. STANDARD ARTICOLI BLOG

### 2.0 Anti-doppioni — prima di scrivere (BLOCCANTE)

> Dettaglio completo: **`TEST-SKILL/SKILL-2.0.md` §8.1a**. Regola sintetica per ogni nuovo articolo.

1. **Non iniziare a scrivere** finche' non hai verificato che titolo, slug e angolo editoriale **non esistono gia'** sul sito.
2. Esegui `python scripts/check_doppioni_sito.py` e consulta `blog.html` (`articoliStatici`), i file `blog-*.html`, Supabase `blog`, cluster in **§1** di questo file.
3. **Se e' un doppione o troppo simile** (stesso macro-tema, stesse H2, stesso evento geopolitico gia' trattato): **STOP** → ricerca web su **fonte istituzionale** (OMI, Banca d'Italia, ISTAT, BCE, MEF, Agenzia Entrate, FIMAA) → scegli **altro argomento** con utilita' per Padova/hinterland.
4. Proponi 2–3 alternative con fonte se la richiesta era generica; procedi solo dopo tema univoco confermato.

### Struttura obbligatoria
- **Lunghezza:** 2.500-3.500 parole (pillar) / 1.500-2.000 (secondari)
- **H1:** unico — keyword primaria + localizzazione
- **H2:** min 5-8, formato domanda per AEO
- **H3:** sotto-sezioni, approfondimenti
- **Totale H2+H3:** min 15, max 28

### Formato GEO/AEO per ogni sezione
1. **Frase dichiarativa** nelle prime 2 righe
2. **Risposta diretta** 40-60 parole dopo ogni H2
3. **Approfondimento** con dati, tabelle, liste
4. Ogni claim auto-contenuto

### Dati e Fonti (OBBLIGATORIO)
- Ogni dato numerico DEVE avere fonte citata nel testo
- Fonti accettate: OMI, Agenzia Entrate, ISTAT, IlSole24Ore, FIMAA, Comune Padova, Regione Veneto
- MAI dati inventati — se non disponibili: "dato non pubblico" o omettere
- Aggiornare dati OMI ogni trimestre

### Meta tags articolo
| Campo | Requisito |
|---|---|
| Title | Max 60-70 char, keyword + localizzazione |
| Meta description | Max 155-160 char, con dato numerico e CTA implicita |
| article:published_time | ISO 8601 (es. 2026-03-04T09:00:00+01:00) |
| article:author | Gino Capon o Linda Righetto |
| article:section | Categoria cluster (es. "Guida alla vendita") |
| article:tag | 3-5 keyword rilevanti |

### Schema JSON-LD triplo (obbligatorio)
1. `Article` — headline, author (Person), publisher, datePublished/Modified, wordCount
2. `FAQPage` — min 5 Question/Answer (40-80 parole per risposta)
3. `BreadcrumbList` — Home → Blog → Titolo Articolo

### Elementi obbligatori nel corpo
- [ ] Author bio visibile a fine articolo (foto, nome, ruolo, link chi-siamo)
- [ ] Timestamp "Ultimo aggiornamento" visibile
- [ ] Internal links a zone pages e service pages correlate (min 3)
- [ ] CTA contestuale (valutazione, contatto, simulatore mutuo)
- [ ] **Form lead in pagina** (se presente): seguire **`skill-forms-leads.md`** — invio diretto con `sendNotifica` + `richieste`, `provenienza: blog-{slug}`; non usare solo link a Contatti come sostituto dell’invio
- [ ] Share bar (WhatsApp, Email, Copia link)
- [ ] Articoli correlati (min 2)
- [ ] Almeno 1 tabella comparativa con fonte
- [ ] **Min 3 immagini fotografiche realistiche** nel corpo (vedi §2.1) + **almeno 2 grafici SVG colorati** a tema (tabelle + chart inline)
- [ ] Copertina hero **fotografica realistica** dedicata (non stock generica con scritte decorative)

### 2.1 Blog — immagini, elenco e auto-verifica (OBBLIGATORIO — tutti gli articoli)

> Applica a **ogni** `blog-*.html` nuovo o rivisto, al seed admin e alla sezione blog in homepage. **Non** riguarda il portale immobili (vendita/affitto) né `in_evidenza` sulle schede immobile.

#### A) Foto **realistiche** — vietate immagini immaginarie

| Consentito | Vietato |
|---|---|
| Fotografie reali o photo-realistiche: appartamenti, stanze, facciate, tram/città Padova-Veneto, studenti/lavoratori in contesto **credibile** (non cartone) | Illustrazioni 3D, avatar, personaggi generati da AI, scene fantasy, volti «plastic» o stile videogioco |
| Asset in `img/blog/` dedicati per articolo (WebP 1200×630 hero, corpo ~800–1200 px larghezza) | Copertine generiche `img/foto-servizi/*` con **testo sovrapposto** o messaggio marketing che non spiega l’articolo |
| Foto scattate/fornite dal cliente o già in repo con soggetto **coerente** al titolo | Unsplash/CDN esterni (già vietati in §8.1c) |
| Didascalia breve sotto ogni `<figure>` (contesto, non claim inventati) | Watermark, slogan stock, date finte, percentuali stampate sull’immagine |

**Regola pratica:** se l’immagine non potrebbe essere scattata con una macchina fotografica in Padova/provincia o in agenzia → **non usarla**. I **grafici dati** restano **SVG/HTML colorati** (Immobiliare.it Insights, OMI, FIMAA…) — non sostituiscono le foto.

**Per articolo (minimo):**
1. **1 copertina hero** fotografica tematica
2. **≥ 3 figure nel corpo** (`<figure class="blog-fig">`) distribuite tra le sezioni H2
3. **≥ 2 chart-wrap SVG** multicolore con legenda e `figcaption` + fonte

#### B) Elenco blog e homepage — **solo ordine per data**

- **`blog.html`:** griglia unica ordinata per `data` / `data_pubblicazione` (più recente in alto). **Nessuna** sezione «In evidenza» che nasconde articoli dalla lista.
- **`js/homepage.js` (`loadBlogHome`):** ultimi 6 articoli **per data** — stesso criterio del blog.
- Il flag `evidenza` nel seed admin resta opzionale (badge in pannello); **non** deve spostare l’ordine pubblico.
- Categoria filtro blog: allineare a pulsanti esistenti (es. `Affitti`, non `Locazioni` orfana).

#### C) Secondo passaggio obbligatorio (agente — prima di dire «fatto»)

Dopo generazione o patch, l’agente **esegue sempre** (non delegare all’utente):

1. `python scripts/check_doppioni_sito.py`
2. `node scripts/validate-page.js blog-{slug}.html` (o elenco file toccati)
3. Grep: slug in `blog.html`, `admin.html`, `js/homepage.js`, `sitemap.xml`
4. Controllo manuale campione: hero + 3 figure = path sotto `img/` esistenti; **nessuna** URL esterna immagine; **nessuna** illustrazione AI/3D
5. Verifica elenco blog: nuovi articoli visibili in cima per data (no featured che li esclude)
6. Solo dopo pass 1+2: commit/push se previsto da task

Se un controllo fallisce → **correggere e ripetere pass 2** prima di chiudere il task.

### Stile di scrittura
- Tono autorevole ma accessibile — MAI accademico o burocratico
- Target: famiglie e investitori zona Padova/hinterland
- Citare fonti ufficiali nel testo (non solo in fondo)
- Transition words 30-35% (Inoltre, Infatti, Di conseguenza, In particolare, Tuttavia)
- NO contenuti generici senza localizzazione

---

## 3. STANDARD ZONE PAGE

### Struttura obbligatoria
1. **H1:** "Case in vendita a [ZONA] — Prezzi, Quartiere e Consigli"
2. **Intro dichiarativa** (GEO) — 2 frasi con dati OMI (prezzo medio €/mq, trend)
3. **Sezione "Il quartiere"** — storia, carattere, target residenti
4. **Tabella prezzi** — per tipologia (appartamento, villa, attico) con fonte OMI
5. **Servizi e infrastrutture** — scuole, trasporti, commercio, verde
6. **Pro e Contro** — lista onesta (4+4) — OBBLIGATORIO per E-E-A-T
7. **FAQ locali** (min 5) — "Quanto costa un bilocale a [ZONA]?"
8. **CTA** — valutazione gratuita specifica per la zona
9. **Link interni** — articoli blog correlati + servizi

### Schema obbligatorio zona
- `RealEstateAgent` con `areaServed` specifico + `aggregateRating`
- `FAQPage` con min 5 domande iper-locali
- `BreadcrumbList`
- `Place` con `GeoCoordinates` del centro zona

---

## 4. STANDARD DESCRIZIONI IMMOBILI

> Le descrizioni sul sito DEVONO essere DIVERSE da quelle sui portali (Idealista, Immobiliare.it, Casa.it).

### Struttura (400-600 parole)
1. **Apertura emozionale** (2-3 righe) — prima impressione, luce, sensazione
2. **Caratteristiche principali** — tipologia, superficie, locali, piano, stato, classe energetica, anno
3. **Descrizione ambienti** — stanza per stanza con metrature se rilevanti
4. **Spazi esterni e pertinenze** — giardino, terrazzo, garage, cantina (con mq)
5. **Contesto e zona** — servizi vicini, link alla zona page, distanza dal centro
6. **CTA chiusura** — "Per info o visita: 049.8843484 / info@righettoimmobiliare.it"

### Regole testi immobili
- MAI copiare dal portale — riscrivere con angolo diverso
- Prezzo con €/mq per confronto zona
- NO termini vaghi ("bello", "interessante") — specifici ("luminoso sud-ovest", "ristrutturato 2023")
- Citare dati OMI della zona per contestualizzare il prezzo
- Se presente virtual tour, segnalare con badge

### Schema JSON-LD immobile
- Tipo: `RealEstateListing`
- Campi: name, description, url, image[], price, priceCurrency, address, GeoCoordinates, floorSize, numberOfRooms
- Collegamento a `RealEstateAgent`

---

## 4.1 Articolo blog «Tour portale acquisizioni» (formato mix v2 — giugno 2026)

**Modello:** `blog-ultime-acquisizioni-residenziali-padova-giugno-2026` · generatore `scripts/build_acquisizioni_giugno16.py` (`build_mix_body`).

### Quando usarlo
- Aggiornamento periodico del **portafoglio attivo** (non duplicare articoli solo-residenziale + solo-commerciale se l’utente chiede **un unico tour**).
- Stesso `url_statico` può essere **rivisto** (titolo/H1/meta aggiornati, `dateModified` in schema).

### Contenuto obbligatorio
| Blocco | Regola |
|--------|--------|
| **5 residenziali** | Ultimi attivi da Supabase; **prima scheda = immobile in evidenza editoriale** (es. Grisignano LP0285-V), poi le altre per data acquisizione |
| **+ commerciale** | **2 uffici in affitto** + **1 capannone** in **ordine di acquisizione** (non alfabetico) |
| **Dati** | Solo da `scripts/acquisizioni_giugno16_data.json` / portale — codice incarico, prezzo, mq, APE |
| **Link scheda** | `immobile?s={slug}` senza `www` |

### Layout moderno (CSS inline articolo)
- `kpi-strip` — 4 numeri sintesi (schede, res, com, comuni)
- `portale-nav` — anchor jump (Grisignano, residenziale, commerciale, tabella, FAQ)
- `acq-card` + `seg-chip` (Residenziale / Commerciale / In evidenza)
- `is-spotlight` sulla card in apertura
- Tabella confronto **tutte** le schede (8 righe)
- FAQ + form lead `data-provenienza` = slug articolo

### Titolo / SEO (esempio rivista 16 giugno 2026)
- **H1:** «Nuove acquisizioni dal portale Righetto — 5 case, uffici in affitto e capannone»
- **Title:** «Acquisizioni portale Righetto giugno 2026 | Case e commerciali»
- **Hero:** foto primo immobile in evidenza (Grisignano), non necessariamente il più recente cronologicamente

### Checklist agente
- [ ] Grisignano (o incarico richiesto) **per primo** con badge In evidenza
- [ ] UFF2105a → CAP1609a → uff2189a (o ordine acquisizione verificato su DB)
- [ ] `blog.html`, `admin.html`, `homepage.js` titolo allineato al nuovo H1
- [ ] Articolo solo-commerciale resta come deep-dive linkato, non doppione del mix

---

## 5. ENTITY-BASED SEO + NEURAL MATCHING

> Google ragiona per entità semantiche. Ripetere la stessa keyword causa penalizzazione.
> Neural Matching = re-ranker AI che collega query e pagine a livello concettuale.

### Livello 1 — Anti-Keyword-Stuffing
| Regola | Limite |
|---|---|
| Qualsiasi frase 2+ parole | Max **5 volte** per pagina |
| "a Padova" / "di Padova" | Max **8-10 occorrenze** |
| Nome zona (in zona page) | Max **10-12 occorrenze** |
| "Righetto Immobiliare" | Max **3-4 menzioni** |
| Title, H1, meta description | Usare **varianti diverse** — mai la stessa frase |

### Mappa sinonimi obbligatoria
| Keyword esatta | Varianti da alternare |
|---|---|
| agenzia immobiliare | studio immobiliare, consulenza immobiliare, professionisti del settore |
| vendere casa | mettere in vendita, cedere la proprietà, alienare l'immobile |
| comprare casa | acquistare un immobile, trovare la casa ideale, investire nel mattone |
| a Padova | nel capoluogo euganeo, nel Padovano, nell'area metropolitana |
| mercato immobiliare | comparto residenziale, panorama immobiliare, dinamiche di mercato |
| valutazione | stima del valore, perizia, analisi comparativa di mercato |
| affitto | contratto di locazione, canone mensile, formula locativa |

### Livello 2 — Copertura Concettuale (Neural Matching)
Ogni pagina deve rispondere a TUTTI i sottotopic del suo tema:

| Topic | Concetti obbligatori |
|---|---|
| Vendita casa | processo, tempistiche, documenti, costi (notaio/agenzia/tasse), valutazione, errori da evitare |
| Mutuo prima casa | requisiti reddituali, fisso/variabile, LTV, spread, Euribor/IRS, detrazioni, tempi, perizia |
| Quartiere | confini, storia, servizi, prezzi medi, trend, pro/contro, tipologia abitanti |
| Affitto studenti | canone medio per zona, cedolare secca, contratto transitorio vs 4+4, deposito, università vicine |

### Co-occorrenze semantiche obbligatorie (min 70%)
| Topic | Coppie obbligatorie |
|---|---|
| Vendita | vendita + rogito + notaio + APE + conformità urbanistica |
| Mutuo | mutuo + tasso + banca + perizia + ipoteca + LTV |
| Affitto | affitto + contratto + deposito + registrazione + cedolare secca |
| Valutazione | valutazione + comparativa + OMI + mq + classe energetica |
| Acquisto | acquisto + proposta + caparra + compromesso + rogito |

### Checklist Neural Matching — Prima di Pubblicare
- [ ] La pagina copre almeno l'80% dei sottotopic previsti?
- [ ] L'intento è chiaro entro le prime 100 parole?
- [ ] Presenti almeno il 70% delle co-occorrenze semantiche?
- [ ] Dati numerici specifici e localizzati (non generici)?
- [ ] FAQ rispondono a domande reali e specifiche (non filler)?
- [ ] Timestamp aggiornato e coerente con dateModified nello schema?
- [ ] Pagina va in profondità su UN topic (no multi-topic superficiale)?
- [ ] Nessuna frase 2+ parole ripetuta più di 5 volte?
- [ ] Title, H1, meta description usano varianti diverse?

---

## 6. CALENDARIO EDITORIALE

| Mese | Contenuto | Stato |
|---|---|---|
| Marzo 2026 | blog-tempi-vendita-casa-padova.html | ✅ FATTO |
| Marzo 2026 | zona-vigonza, zona-abano-terme, zona-selvazzano | ✅ FATTO |
| Aprile 2026 | Video presentazione agenzia | TODO |
| Maggio 2026 | Articoli fiscali (IMU, bonus) | TODO |
| Giugno 2026 | Bollino "Verificato Righetto" | TODO |
