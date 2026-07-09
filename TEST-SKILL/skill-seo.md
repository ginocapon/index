# SKILL-SEO — Righetto Immobiliare
> Carica per: audit SEO, nuove zone page, ottimizzazioni SERP, analisi competitor, KPI.
> Versione estratta da SKILL-2.0.md — Marzo 2026

---

## 1. PUNTEGGIO SITO (Audit 3 Luglio 2026)

| Area | Punteggio | Note |
|---|---|---|
| SEO on-page | **10/10** | `mini-seo-check.sh` — 0 ERR, 0 WARN |
| Schema.org | **10/10** | RealEstateAgent + FAQPage + BreadcrumbList + dateModified |
| Compliance Google | **10/10** | `google-compliance-check.py` — 0 ERR, 0 WARN |
| Audit SKILL-2.0 | **10/10** | `audit-skill.sh` — 0 ERR, 0 WARN (luglio 2026) |
| Contenuti/Blog | 9.8/10 | 102 articoli SKIMM, timestamp visibile |
| GEO/AEO | 10/10 | llms.txt + ai.json + bot AI non bloccati |
| Core Web Vitals | 9/10 | Font preload, vendor locale, no CDN jsdelivr/cdnjs |
| **TOTALE on-site** | **10/10** | Batch: `patch_cdn_local.py` + `patch_compliance_warns.py` + `patch_audit_warns.py` |

### Verifica automatica (luglio 2026)
```bash
python3 scripts/google-compliance-check.py   # 100%
bash scripts/mini-seo-check.sh             # 100%
bash scripts/audit-skill.sh                  # 100%
```

**Keyword stuffing:** conteggi solo su **testo visibile** (esclusi `<script>`/`<style>`), con **word boundary** (`\ba Padova\b` — non substring tipo «casa Padova»). Script: `audit_helpers.py`.

---

## 2. PERFORMANCE REALI (Google Search Console — 11 Marzo 2026)

| Metrica | Valore |
|---|---|
| Clic totali (28gg) | 150 |
| Impressioni | 1.590 |
| CTR media | **9,4%** (media settore: 3-5%) |
| Posizione media | 8,1 |

**Top query:**
| Query | Posizione | CTR |
|---|---|---|
| agenzia righetto limena | **1,3** | 48,6% |
| agenzia immobiliare padova | ~28,5 | 1,1% |
| vendere casa padova | ~14,7 | 4,2% |

---

## 3. STATO SERP COMPETITOR (7 Marzo 2026)

| Feature | Righetto | Tetto Rosso | RicercAttiva |
|---|---|---|---|
| FAQ Pages | Si (top) | Si | No |
| Schema.org | Esteso (top) | Buono | Buono |
| Recensioni | ~127 | ~256 | Poche |
| Chatbot AI | **Unico** | No | No |
| GEO/AEO | **Unico** | No | No |
| Appare in SERP | NO | SI | SI |

---

## 4. REQUISITI GOOGLE 2026

### Core Web Vitals — Soglie
| Metrica | Buono | Scarso |
|---|---|---|
| LCP | < 2.5s (target competitivo: <2s) | > 4.0s |
| INP | < 200ms | > 500ms |
| CLS | < 0.1 | > 0.25 |
| SVT/VSI/ER | Nuove metriche stabilità (March 2026 Core Update) | — |

### E-E-A-T (Cruciale 2026)
- [x] Pagina autore Gino Capon (`/gino-capon`) e Linda Righetto (`/linda-righetto`) — Person schema, FAQ
- [ ] Author bio blog con link pagina autore (patch: `scripts/patch_author_bio_links.py`)
- [ ] Author bio visibile su ogni articolo blog
- [ ] Person schema con `jobTitle`, `worksFor`, `sameAs`
- [ ] Chi siamo dettagliato con storia brand e case study
- [ ] Coerenza brand cross-platform (sito, GBP, LinkedIn, Instagram, portali)

### Fattori di Ranking 2026
1. E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)
2. Rilevanza semantica (search intent > keyword volume)
3. Core Web Vitals (hard ranking factor)
4. Mobile-first indexing
5. Dati strutturati (Schema.org + GeoCoordinates)
6. GEO (citazioni AI: Gemini, ChatGPT, Perplexity)
7. AEO (featured snippets)
8. Topical Authority
9. Local Relevance
10. Page Experience Consistency

### Schema Markup — Regole
- Tipo: `RealEstateAgent` (MAI generico `LocalBusiness` da solo)
- Formato: JSON-LD
- **GeoCoordinates obbligatorio** su ogni schema RealEstateAgent:
```json
"geo": {"@type": "GeoCoordinates", "latitude": 45.476956, "longitude": 11.845762},
"hasMap": "https://maps.google.com/?q=45.476956,11.845762"
```
- **sameAs obbligatorio:**
```json
"sameAs": ["https://www.instagram.com/righettoimmobiliare/", "https://www.facebook.com/righettoimmobiliare/", "https://www.linkedin.com/company/righettoimmobiliare/"]
```
- **Layering:** RealEstateAgent + FAQPage + BreadcrumbList + Person (agente) + RealEstateListing (immobile)

---

## 5. GEO — Generative Engine Optimization

> 58% dei consumatori usa AI nel 2026. GEO converte 4.4x vs SEO tradizionale.
> **Aggiornamento giu 2026 (Google ufficiale):** per **Google Search / AI Overviews** valgono le stesse regole SEO — `llms.txt` **non obbligatorio** per Google; evitare farm citazioni e micro-chunking. Vedi `SKILL-2.0.md` §**4.4b**.

**Regole per ogni contenuto:**
1. Frasi **dichiarative** nelle prime 2 righe di ogni sezione (AI estraggono da qui)
2. **Dati numerici specifici** verificabili (prezzi/mq, anni, N. immobili)
3. Formato: **Domanda H2 → Risposta diretta 40-60 parole → Approfondimento**
4. Liste, tabelle, definizioni chiare
5. Citare fonti ufficiali (Agenzia Entrate, OMI, FIMAA)
6. Frasi auto-contenute (ogni claim deve avere senso isolatamente)
7. Timestamp "Ultimo aggiornamento" su contenuti cornerstone
8. `llms.txt` + `ai.json` — **consigliati** per ChatGPT/Perplexity/Claude; opzionali per Google (§4.4b)

**AEO per featured snippet:**
1. Risposta 40-60 parole come primo paragrafo dopo ogni H2
2. Formato: "[Keyword] è [definizione/risposta]"
3. Min 5 FAQ con Schema FAQPage per pagina
4. Tabelle comparative per dati numerici

---

## 6. VISUAL SALIENCY — Regole Above-the-Fold

**LCP Element:**
- Hero image: `<link rel="preload" href="..." as="image" fetchpriority="high">`
- MAI `loading="lazy"` above-the-fold
- Animazioni LCP: `animation-play-state: paused`, avviare dopo primo render

**Font Loading:**
- Preload: Montserrat 400/700 + Cormorant Garamond 600/700
- `font-display: swap` su tutti i `@font-face`
- Self-hosted WOFF2 (no Google Fonts esterni = GDPR + velocità)

**CLS Prevention:**
- TUTTE le immagini con `width` + `height` espliciti
- Mai contenuto asincrono above-the-fold senza placeholder dimensionato

**Palette CTA (contrast-safe):**
| Elemento | BG | Testo | Ratio |
|---|---|---|---|
| CTA primario | `var(--oro)` #FF6B35 | `var(--nero)` #152435 | ~5.0:1 ✅ |
| CTA secondario | `var(--blu)` #2C4A6E | white | ~5:1 ✅ |
| **VIETATO** | #FF6B35 | white | 1.54:1 ❌ FAIL |

---

## 7. PRIORITÀ STRATEGICHE OFF-SITE

**PRIORITÀ 1 — Google Business Profile**
- Categoria primaria: "Agenzia Immobiliare" + secondarie: "Consulente Immobiliare", "Valutatore Immobiliare"
- Google Posts OGNI SETTIMANA (nuovi immobili, articoli blog, offerte)
- 5+ foto/settimana (MAI stock) — interni ufficio, esterni, team, esempi immobili
- UTM tags sul link sito (`?utm_source=gbp&utm_medium=organic`)

**PRIORITÀ 2 — Recensioni Google (127 vs 256 Tetto Rosso — gap critico)**
- Script WhatsApp post-rogito: *"Gentile [nome], grazie per aver scelto Righetto Immobiliare! Ci farebbe piacere una tua recensione: [link]"*
- Obiettivo: +30 recensioni/anno
- MAI recensioni false — penalità = rimozione tutte + sospensione GBP + multa AGCM

**PRIORITÀ 3 — Backlink Locali (Domain Authority ~5 → target 20+)**
- PadovaOggi / IlGazzettino (come fonte esperta)
- Directory: PagineGialle, Yelp, Cylex, TuttoCittà
- Camera di Commercio Padova (registrazione con link)
- Collaborazioni geometri, notai, architetti (scambio link)
- Profilo FIMAA con link sito

---

## 8. KPI E OBIETTIVI

| Metrica | Attuale (Mar 2026) | 3 mesi | 6 mesi | 12 mesi |
|---|---|---|---|---|
| Clic GSC/mese | 150 | 400 | 1.000 | 3.000 |
| Utenti settimanali GA | 96 | 300 | 800 | 2.000 |
| "ag. imm. padova" pos. | ~28 | Top 15 | Top 10 | Top 3 |
| Recensioni Google | ~127 | 142 | 172 | 200+ |
| Domain Authority | ~5 | 10 | 15 | 20+ |
| Pagine indicizzate | ~55 | 65 | 80 | 120 |

### Roadmap
- **Fase 1 (Mar-Mag 2026):** Dominare Limena/cintura → 400 clic/mese
- **Fase 2 (Giu-Set 2026):** Conquistare Padova → 1.000 clic/mese, top 10 keyword padova
- **Fase 3 (Ott 2026-Mar 2027):** Portale regionale → 3.000 clic/mese

### Routine monitoraggio
- **Settimanale (venerdì 07:00 CEST):** `venerdi-contenuti-freschezza.py` — SKIMM + blog + pillar + email `info@`; compliance: **`skill-massimo-punteggio.md` §4**
- **Settimanale (venerdì, manuale GSC):** checklist **`§10`** — 10 URL chiave, sitemap, 404/5xx
- **Lunedì (follow-up GSC):** verifica esito richieste indicizzazione + trend 404/5xx — **`§10.3`**
- **Settimanale:** GSC Performance Report + Google Posts
- **Mensile:** Core Web Vitals + citazioni AI
- **Trimestrale:** Audit completo + competitor + dati OMI aggiornati

### Vantaggio competitivo contenuti (luglio 2026)

| Leva | Righetto | Tetto Rosso / portali |
|---|---|---|
| Guide originali blog | 99+ articoli corposi | Poche guide generiche |
| Freschezza settimanale | Cron + timestamp visibile | Solo annunci |
| Anti-doppioni SKIMM | Catalogo keyword/intent | — |
| GEO / llms.txt | Sì | No |
| Chatbot AI | Linda 24/7 | No |
| Sezione soluzioni agenzia | «Cosa può fare Righetto» | No |

Pagine pillar da refreshare ogni settimana (verificate dal cron): `/`, `/blog`, `/agenzia-immobiliare-padova`, `/servizio-locazioni`, `/servizio-valutazioni`, `/chi-siamo`.

---

## 9. TODO SEO TECNICO APERTI

- [ ] LCP sotto 2 secondi su tutte le pagine
- [ ] Contenuti immobili UNICI vs portali (rischio duplicate content — deindexing)
- [ ] Internal linking blog posts ↔ zone pages (min 3 cross-link contestuali)
- [ ] UTM tags su link GBP per tracciare traffico in GA4
- [ ] Verificare recensioni Google non sparite (nuove policies Marzo 2026)
- [ ] Bollino "Verificato Righetto" sugli annunci

---

## 10. SEARCH CONSOLE — ROUTINE SETTIMANALE (venerdì + lunedì)

> **Proprietà:** `righettoimmobiliare.it` (tipo **Dominio**) — include www e non-www. Non serve una seconda proprietà con `www`.  
> **URL da usare in ispezione e canonical:** `https://righettoimmobiliare.it/...` (senza `www`, senza `.html`).  
> **Skill operativa venerdì:** `.cursor/skills/righetto-venerdi-sito-90giorni/SKILL.md` § Search Console.

### 10.1 Dieci pagine chiave (indicizzazione manuale / verifica)

| # | URL |
|---|---|
| 1 | `https://righettoimmobiliare.it/` |
| 2 | `https://righettoimmobiliare.it/servizio-vendita` |
| 3 | `https://righettoimmobiliare.it/agenzia-immobiliare-padova` |
| 4 | `https://righettoimmobiliare.it/zona-limena` |
| 5 | `https://righettoimmobiliare.it/immobili` |
| 6 | `https://righettoimmobiliare.it/blog-limena-vs-padova-centro-dove-comprare-2026` |
| 7 | `https://righettoimmobiliare.it/blog-mercato-immobiliare-limena-2026` |
| 8 | `https://righettoimmobiliare.it/blog-appartamento-nuova-costruzione-limena` |
| 9 | `https://righettoimmobiliare.it/blog-scegliere-agenzia-immobiliare-padova-2026` |
| 10 | `https://righettoimmobiliare.it/blog` |

**Priorità query (da Prestazioni 3 mesi):** cluster Limena + brand Righetto — allineare blog 6–8 al traffico locale.

### 10.2 Checklist venerdì (~15 min, utente in GSC)

1. **Prestazioni** (7 + 28 gg): 1 opportunità (CTR basso o pos. 11–20) + 1 anomalia.
2. **Indicizzazione → Pagine:** se fix SEO deployati → **Convalida correzione** su report **404** e **5xx** aperti.
3. **Sitemap:** inviare/reinviare `sitemap.xml` (stato **Operazione riuscita**).
4. **Ispezione URL** (barra in alto): per ogni URL §10.1 — se non indicizzata e nessuna richiesta recente → **Richiedi indicizzazione** (max ~10/giorno).
5. **Non indicizzare manualmente** URL legacy: `/home`, `/agenzia`, `/blog-articolo?s=...`, `/api/send-mail.php`.

**Procedura ispezione:** barra «Controlla qualsiasi URL» → incolla URL §10.1 → Invio → **Richiedi indicizzazione** → Invia.

### 10.3 Follow-up lunedì (~10 min)

- [ ] Tutte e 10 le URL §10.1: «URL presente su Google» **oppure** «Richiesta di indicizzazione inviata il …»
- [ ] Canonical in ispezione = stesso URL senza `www`
- [ ] Report 404/5xx: conteggio in calo vs settimana precedente
- [ ] Agente repo: `python scripts/probe_live_urls.py` → `data/url-probe-latest.json` (target **0 issue**); committare snapshot se deploy recente

### 10.4 Probe e redirect (agente, venerdì o post-deploy)

```bash
python scripts/build_seo_redirects.py   # rigenera 404.html, js/redirects-404.js, stub
python scripts/probe_live_urls.py       # audit live ~460 URL
```

Asset: `404.html`, `js/redirects-404.js`, `data/redirects-301.json`, `data/url-probe-latest.json` (snapshot sempre in repo).

---

## 11. PAGE SCORE — framework decisionale (cron venerdì)

> **Script:** `python scripts/venerdi-seo-intelligence.py`  
> **Dati:** `data/gsc-keywords-priority.json` (+ opz. `data/gsc-export-queries.csv`, `data/gsc-export-pages.csv`)  
> **Output:** `venerdi-seo-intelligence-report.md` (unito al report Issue `contenuti-freschezza`)

### 11.1 Formula PAGE SCORE (0–100)

| Fattore | Peso | Cosa misura |
|---|---:|---|
| **GSC potential** | 25% | Impressioni alte + CTR basso = opportunità refresh |
| **Content depth** | 20% | Parole utili (soglia 1500 / 2500) |
| **Freshness + GEO** | 20% | FAQPage, righetto-sol, dateModified, box AEO |
| **Internal mesh** | 15% | Link verso blog/zone/servizi |
| **Keyword fit** | 20% | Title/meta allineati a query GSC (es. affitti Limena) |

### 11.2 Decisioni automatiche

| Etichetta | Significato | Azione settimana |
|---|---|---|
| **SOSTENERE** | imp ≥ 20, 0 click **oppure** thin content | Rifare title/meta + 1 sezione + 3 link interni |
| **GEO** | Manca FAQ/box sintesi su pagina strategica | FAQ schema + allineamento Linda (`audit_chatbot_faq.py`) |
| **AGGIUNGERE** | Keyword in `keyword_gaps_new` senza slug | 1 articolo nuovo (dopo `check_doppioni_sito.py`) |
| **MANTENERE** | Score alto + click stabili | Solo timestamp / dato mensile |
| **CONSOLIDARE** | 2+ URL SKIMM stesso intent | Redirect 301 + internal link (no terzo articolo) |
| **MONITORARE** | Nessun trigger | Nessuna azione |

### 11.3 Ritmo venerdì (utente + agente)

1. **Utente (10 min):** GSC → Prestazioni 7+28 gg → aggiorna `data/gsc-keywords-priority.json` (o CSV in `data/`).
2. **Cron 07:00 CEST:** `venerdi-contenuti-freschezza.py` + `venerdi-seo-intelligence.py` + `probe_live_urls.py`.
3. **Agente:** esegue **priorità 1 SOSTENERE** dalla Issue; **max 1 AGGIUNGERE** se gap confermato.
4. **Lunedì:** verifica GSC §10.3 + confronto report settimana precedente.

### 11.4 Cluster editoriali 2026 (da GSC + screening)

| Cluster | Stato | Prossima mossa |
|---|---|---|
| **Affitti Padova** | 🟢 winner (`affitto-studenti`, `contratto-affitto`) | SOSTENERE `rendimento-affitto` (139 imp, 0 click) |
| **Limena locale** | 🟢 articolo `blog-affitti-limena-2026` live | MANTENERE + mesh link; refresh canoni se FIMAA/OMI nuovo semestre |
| **OMI / dati ufficiali** | 🟢 title «OMI Padova» aggiornato | MANTENERE; refresh dato al prossimo semestre ADE |
| **Brand Righetto** | 🟢 90%+ click | MANTENERE — non cannibalizzare con articoli generici |
| **Zone pages (14)** | 🟢 batch luglio 2026: vendita **e** affitto in title/meta + CTA affitti | MANTENERE; mesh verso `blog-affitti-limena-2026` |
| **Transitorio Padova** | 🟢 `blog-affitto-transitorio-padova-durata-2026` live | MANTENERE + link da `blog-contratto-affitto-padova` |
| **B2B cintura** | 🟢 `blog-rubano-limena-affitto-lavoratori-2026` live | MANTENERE + mesh Edilcassa / `zona-rubano` |

### 11.5 Idee GEO originali (rotazione — non tutte insieme)

1. **Risposta in 40 parole** in cima agli articoli money (snippet AI / Linda).
2. **Mesh Limena:** 6 articoli territorio-limena ↔ `zona-limena` ↔ `immobili?zona=limena`.
3. **Widget acquisizioni zona** da Supabase nelle `zona-*.html` (contenuto unico vs portali).
4. **FAQ Linda = FAQ schema** — stessa risposta su sito e chatbot (`audit_chatbot_faq.py`).
5. **llms.txt dinamico:** top 10 URL GSC winner aggiornati mensilmente.
6. **Gergo immobiliare Padova** — glossario AEO (query GSC 3 imp, bassa competizione).
7. **Università → affitto** bridge da query medicina/università verso `affitto-studenti`.
8. **Tour 360 / visita live** in evidenza su card Limena (contenuto non duplicabile dai portali).

