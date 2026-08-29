# Skill — Comando editoriale fisso blog (PERMANENTE · PRIORITÀ ALTA)

> **Comando editoriale permanente** — ricerca strategica, selezione argomenti, immagini, grafiche e composizione di ogni articolo/post blog.  
> **Carica sempre** con: `skill-editorial-queue.md`, `skill-content.md`, `skill-ai-act-compliance.md`, `skill-efficienza-sito.md`  
> **Routing:** `context-map.json` → `nuovo_articolo_blog`, `venerdi_contenuti_skimm`, `ottimizzazione_contenuto`

---

## Regola di precedenza

| Ambito | Prevale |
|--------|---------|
| Ricerca/verifica fonti, selezione argomento, valore aggiunto, ripartizione 50/50 trend/evergreen | **Questa skill §8–17** |
| Numero minimo immagini, grafiche, pertinenza visiva, linea editoriale | **Questa skill §1–7** |
| Trasparenza AI Act UE (marchio, didascalie, barra sito) | **`skill-ai-act-compliance.md`** |
| Diff minimo, anti-filler, gate media WebP, GA4 unico, zero sprechi operativi | **`skill-efficienza-sito.md`** |
| Title/meta, schema, anti-doppioni, 2500+ parole | **`skill-essentials.md`**, **`skill-content.md`**, **`SKILL-2.0.md` §8.1a/8.1c |

Non ignorare istruzioni di livello superiore né vincoli tecnici. La skill efficienza Musk resta valida su filler e sprechi operativi.

---

# PARTE A — VISIVO (§1–7)

## 1. Pubblicazioni del venerdì

Ogni post **creato, programmato o pubblicato di venerdì**:

- [ ] Immagini IA: marchio **FOTO AI** + `data-ai-generated="true"` + didascalia trasparenza
- [ ] `node scripts/build-ai-image-manifest.mjs` + `node scripts/audit-foto-ai.mjs` → exit 0
- [ ] Nessuna marchiatura falsa; solo obblighi **effettivamente applicabili** (Reg. UE 2024/1689 art. 50)
- [ ] Controllo extra: questa skill §7 + §17 + `righetto-venerdi-sito-90giorni` §0

Riferimento: **`skill-ai-act-compliance.md`** §3.4.

---

## 2. Coerenza assoluta articolo ↔ immagini

**Vietato:** immagini casuali, stock generico, riempimento estetico senza legame col testo.

**Prima** di generare o selezionare un'immagine:

1. Leggere il paragrafo/sezione H2 che accompagna
2. Definire soggetto concreto (edificio, quartiere, scenario, concetto visivo)
3. Verificare pertinenza a Padova/Veneto/immobiliare e tono professionale Righetto
4. Didascalia che collega immagine al contenuto (non slogan)

| Obbligatorio | Vietato |
|---|---|
| Soggetto legato al paragrafo adiacente | Immagini «belle ma generiche» |
| Coerenza tono editoriale | Foto da `img/immobili/` annunci reali nel blog |
| Utilità alla comprensione | CDN esterni / Unsplash |

---

## 3. Numero minimo elementi visivi (BLOCCANTE)

| Tipo | Minimo | Note |
|------|--------|------|
| **Immagini fotografiche editoriali** | **≥3 nel corpo** + **1 hero** | Generate ex novo IA, WebP 19:9, `img/blog/` |
| **Grafici / infografici** | **≥2** | SVG `class="chart-wrap"`, funzione informativa |
| **Tabelle dati** | **≥2** | HTML con fonte verificata (oltre alle foto) |

Le **≥3 foto corpo** non includono la hero. I grafici **non** sostituiscono le foto.

---

## 4. Le grafiche devono spiegare l'articolo

**Processo obbligatorio (ordine):**

1. Scrivere o analizzare il contenuto
2. Estrarre concetti chiave, dati, confronti, processi
3. Progettare ≥2 visualizzazioni (percentuali, cronologie, pro/contro, scenari…)
4. Inserire ogni grafica **nel punto** in cui aiuta la comprensione
5. `figcaption` + fonte verificata sotto ogni chart/tabella

**Vietato:** grafiche decorative senza dati o concetti presenti nel testo.

Dettaglio tecnico: **`skill-content.md`** §2.1e.

---

## 5. Linea editoriale visiva

- Proporzione **19:9** uniforme (hero + figure corpo)
- Palette brand nei SVG (blu `#1a365d`, accenti coerenti)
- WebP hero ≤500 KiB dove possibile (`skill-efficienza-sito.md` §3.1)
- Equilibrio foto + chart/tabelle; leggibilità mobile WCAG AA

---

## 6. Applicazione automatica (visivo)

Senza richiesta utente su: `/blog`, coda `editorial-queue.json`, refresh, venerdì, `"SKILL"`.

L'agente **non** chiude il task blog finché §7 e §17 non sono superati.

---

## 7. Controllo finale visivo

```bash
python scripts/audit_blog_visuals.py --file blog-{slug}.html
node scripts/build-ai-image-manifest.mjs
node scripts/audit-foto-ai.mjs
```

- [ ] ≥3 figure IA pertinenti + 1 hero
- [ ] ≥2 SVG informativi + ≥2 tabelle con fonte
- [ ] Zero elementi visivi solo estetici
- [ ] Post venerdì: audit AI Act OK

---

# PARTE B — RICERCA E SELEZIONE STRATEGICA (§8–17)

## 8. Principio generale: niente articoli casuali

Prima di pianificare, scrivere o generare un nuovo articolo → **ricerca approfondita, aggiornata e comparativa**.

Il blog opera come **redazione digitale**, analizzando:

- cosa sta accadendo e quali notizie emergono;
- cambiamenti rilevanti per il settore;
- cosa cercano gli utenti (GSC, Trends);
- conseguenze per mercato immobiliare, **Padova**, **provincia di Padova**, **Veneto**.

**Vietato:** idee generiche, argomenti scelti a caso, publish senza fase ricerca (§15).

Gate: `python scripts/audit_editorial_research.py --id eq-XXX` prima dello writing.

---

## 9. Tre aree di monitoraggio (prioritarie)

### Area 1 — Economia, immobiliare, Padova e Veneto

Mercato IT, prezzi, compravendite, domanda/offerta, mutui, tassi, affitti, fiscalità, investimenti, edilizia, urbanistica; focus **Veneto → provincia Padova → Padova città**.

Ogni notizia nazionale rilevante → valutare **conseguenze locali**.

### Area 2 — Politica italiana ed economia reale

Solo quando produce effetti concreti su: casa, fiscalità, famiglie, imprese, locazioni, mutui, edilizia, patrimonio.

**Non** selezionare per polemica mediatica — solo impatto pratico su cittadini/proprietari/acquirenti/venditori/investitori/locatori.

### Area 3 — Leggi, decreti, novità normative

Monitorare: leggi, DL, D.Lgs., conversioni, regolamenti, circolari ADE, modifiche fiscali, casa, locazioni, condominio, edilizia.

**Per ogni novità verificare:**

1. Approvata o solo proposta?
2. Già in vigore?
3. DL convertito?
4. Modifiche in corso?
5. Conseguenze pratiche?

| Vietato | Obbligatorio |
|---------|--------------|
| Progetto di legge = legge | Fonte primaria (Gazzetta Ufficiale, ADE, ministeri) |
| Annuncio politico = effetto certo | Distinzione fatto / dichiarazione / analisi / previsione |

Fonte primaria norme: [Gazzetta Ufficiale](https://www.gazzettaufficiale.it/)

---

## 10. Scansione fonti (ogni ciclo editoriale)

### Fonti istituzionali e primarie (priorità)

Gazzetta Ufficiale · Agenzia delle Entrate · Ministeri · ISTAT · Banca d'Italia · Parlamento · Regioni/Comuni · UE · OMI · FIMAA.

Su norme, tasse, provvedimenti, dati ufficiali, scadenze → **fonte primaria prima** del giornalismo.

### Fonti economiche autorevoli (analisi, non sostituto norme)

Il Sole 24 Ore · Milano Finanza · ANSA Economia/Veneto (RSS in `skill-editorial-queue.md`).

Per interpretazione e scenari — **mai** come unica fonte su provvedimenti ufficiali.

---

## 11. Verifica obbligatoria informazioni

- Confrontare almeno **fonte primaria + seconda fonte indipendente** quando possibile
- **Vietato** presentare come certo: voci, previsioni, ipotesi, opinioni, dichiarazioni non tradotte in atto

**Distinzione esplicita nel testo:**

| Tipo | Come presentarlo |
|------|------------------|
| Fatto accertato / dato ufficiale | Con link fonte primaria |
| Dichiarazione politica | «Il ministro ha annunciato…» — non effetto già in vigore |
| Analisi / previsione | «Secondo [fonte], potrebbe…» |

Regola d'oro Righetto: se non hai fonte verificabile, **non inserire il dato**.

---

## 12. Analisi settimanale ricerche utenti

### Google Trends

Indicatori: argomenti in crescita, query emergenti, correlati, interesse nel tempo, geo **Italia / Veneto / Padova**.

Trends = interesse di ricerca, **non** prova di correttezza notizia.  
[Google Trends](https://trends.google.com/trends/?hl=it-it)

### Google Search Console

Settimanalmente (`data/gsc-keywords-priority.json`, export utente):

- query con più clic/impression;
- pagine in crescita;
- query ad alto impatto / basso CTR → SOSTENERE o nuovo articolo;
- opportunità long-tail Padova/Limena.

[GSC](https://search.google.com/search-console/) — dati reali del sito, parte stabile della strategia.

---

## 13. Cinque contenuti rilevanti sul web + regola 50%

Per ogni cluster tematico → individuare **5 contenuti più rilevanti/visibili** (SERP, copertura autorevole, Trends, GSC — **non inventare clic concorrenti**).

**Obiettivo editoriale indicativo:** ~**50%** articoli su argomenti con **forte interesse pubblico** (trend + ricerca + visibilità).

**Vietato:** copiare testi, riscrivere articoli concorrenti, imitare struttura, contenuti derivativi senza valore.

**Obiettivo:** COSA INTERESSA + COSA MANCA + ANALISI ORIGINALE Righetto.

Registrare in coda: `hype_sources_read` (5 URL/titoli), `gap_analysis`, `value_add`.

---

## 14. Valore aggiunto originale (BLOCCANTE)

Ogni articolo su tema già trattato deve offrire **almeno uno**:

- analisi Padova / Veneto / Limena;
- spiegazione pratica; conseguenze; confronto scenari;
- approfondimento normativo verificato;
- dati aggiornati OMI/ISTAT/FIMAA;
- risposta a domande concrete per proprietari / acquirenti / venditori / investitori / locatori.

**Obiettivo:** «Cosa sta succedendo e cosa significa per chi vive, acquista, vende o investe **qui**.»

Campo coda: `value_add` (testo breve obbligatorio su item `scheduled`).

---

## 15. Procedura editoriale obbligatoria (7 fasi)

| Fase | Azione |
|------|--------|
| **1 — Scansione** | Notizie recenti nelle 3 aree (§9) |
| **2 — Verifica fonti** | Primarie istituzionali; stato provvedimenti |
| **3 — Impatto settore** | IT → Veneto → Padova → stakeholder |
| **4 — Domanda** | GSC + Trends + query emergenti |
| **5 — Top 5 web** | Cosa coprono / cosa manca / gap |
| **6 — Punteggio** | Attualità, interesse, KW, rilevanza locale, fonti, impatto pratico, originalità |
| **7 — Selezione** | Solo argomento con miglior equilibrio **INTERESSE + ATTUALITÀ + AFFIDABILITÀ + UTILITÀ + TERRITORIO + VALORE AGGIUNTO** |

**Non scrivere** finché fasi 1–7 non documentate in `editorial-queue.json` (item `scheduled` o `proposed`).

Script: `python scripts/audit_editorial_research.py --id {id}`

---

## 16. Ripartizione piano editoriale (~50/50)

| ~50% | ~50% |
|------|------|
| Trend / forte interesse pubblico (Trends, GSC, fonti autorevoli, visibilità SERP) | Evergreen strategico: guide, analisi locali, norme spiegate, opportunità emergenti |

Campo coda: `editorial_type`: `"trend"` | `"evergreen"`.

Percentuale **indicativa** — notizia eccezionalmente importante può derogare.

---

## 17. Controllo editoriale finale (completo)

Prima di approvare pubblicazione:

**Ricerca e strategia**

- [ ] Argomento da ricerca reale e aggiornata (§15)
- [ ] Tre macro-aree considerate
- [ ] Fonti affidabili; norme verificate su primaria
- [ ] Interesse reale (GSC/Trends dove possibile)
- [ ] Top 5 web analizzati; nessuna copia sostanziale
- [ ] `value_add` documentato; impatto Padova/Veneto se pertinente
- [ ] `python scripts/audit_editorial_research.py --id {id}` → OK

**Visivo (§7)**

- [ ] `audit_blog_visuals.py` + `audit-foto-ai.mjs` → OK

**Tecnico**

- [ ] `validate-page.js` · anti-doppioni · 2500+ parole utili
- [ ] Nessun conflitto con `skill-efficienza-sito.md`

---

## Obiettivo editoriale finale

Redazione specializzata basata su **ricerca → verifica → strategia → scrittura → impaginazione visiva**.

Ogni settimana:

**COSA ACCADE → COSA CAMBIA → COSA CERCANO → COSA PUBBLICANO LE FONTI → COSA SIGNIFICA PER L'IMMOBILIARE → COSA SIGNIFICA PER PADOVA/VENETO → POI si scrive.**

---

## Appendice A — Markup visivo

```html
<div class="art-hero">
  <div class="art-hero__frame rig-ai-photo-wrap" data-ai-generated="true">
    <img class="art-hero-img" src="img/blog/blog-{slug}-hero.webp" alt="…" width="1900" height="900">
  </div>
</div>
<figure class="blog-fig">
  <div class="blog-fig__frame rig-ai-photo-wrap" data-ai-generated="true">
    <img src="img/blog/blog-{slug}-sezione-1.webp" alt="…" width="1900" height="900" loading="lazy">
  </div>
  <figcaption>… — immagine generata con IA.</figcaption>
</figure>
<figure class="chart-wrap" aria-label="…">
  <svg …></svg>
  <figcaption>Fonte: OMI 2026 T2 — …</figcaption>
</figure>
```

---

## Appendice B — Campi coda (`editorial-queue.json`)

| Campo | Obbligatorio (scheduled) | Descrizione |
|-------|--------------------------|-------------|
| `research_refs` | sì (≥2) | URL o riferimento fonte primaria/indipendente |
| `hype_sources_read` | sì (≤5) | Top contenuti web analizzati |
| `gap_analysis` | sì | Cosa manca negli articoli esistenti |
| `value_add` | sì | Valore originale Righetto |
| `editorial_type` | sì | `trend` o `evergreen` |
| `monitoring_area` | sì | `mercato` \| `politica` \| `normativa` \| combinazione |
| `gsc_signal` | se disponibile | Query/impression da GSC |
| `different_from` | se tema simile | Slug articolo esistente da non duplicare |

---

## Collegamenti

- `TEST-SKILL/skill-editorial-queue.md`
- `TEST-SKILL/skill-content.md` §2.1, §2.1e
- `data/editorial-queue.json` · `data/gsc-keywords-priority.json`
- `scripts/audit_blog_visuals.py` · `scripts/audit_editorial_research.py`
- `.cursor/rules/righetto-blog-publish.mdc`

---

*Aggiornato: 29 agosto 2026 — comando editoriale fisso completo (visivo + ricerca strategica).*
