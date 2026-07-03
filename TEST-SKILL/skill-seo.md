# SKILL-SEO — Righetto Immobiliare
> Carica per: audit SEO, nuove zone page, ottimizzazioni SERP, analisi competitor, KPI.
> Versione estratta da SKILL-2.0.md — Marzo 2026

---

## 1. PUNTEGGIO SITO (Audit 16 Marzo 2026)

| Area | Punteggio | Note |
|---|---|---|
| SEO on-page | 9.8/10 | 18 meta desc corrette, canonical OK, OG completi |
| Schema.org | 9.8/10 | RealEstateAgent+FAQPage+BreadcrumbList+Person su 95%+ pagine |
| Contenuti/Blog | 9.8/10 | 40+ articoli, 4 cluster completi, timestamp visibile |
| GEO/AEO | 10/10 | Unico ad ottimizzare per AI — llms.txt completo |
| Core Web Vitals | 9/10 | Font preload completo, CSS critical/below-fold separato |
| Zone Pages | 9.5/10 | 14 zone con Pro/Contro, 5 FAQ schema, tabelle OMI |
| Chatbot AI | 10/10 | Unico nel mercato locale |
| Conversione/Lead | 9.9/10 | 10 sistemi su 14 pagine (A/B, exit intent, sticky CTA) |
| Recensioni Google | 6/10 | ~127 vs 256 Tetto Rosso — gap critico |
| Domain Authority | 4/10 | Problema #1 — nessun backlink significativo |
| Apparizione SERP | 3/10 | Brand OK (pos. 1.3), non-brand deboli |
| **TOTALE** | **9.2/10** | Off-site unico collo di bottiglia |

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
