---
name: righetto-venerdi-sito-90giorni
description: >-
  Weekly website and SEO operations for Righetto Immobiliare (righettoimmobiliare.it):
  every-Friday checklist plus a 12-week thematic roadmap. Use when the user mentions
  Friday updates, "cosa fare questa settimana", weekly site tasks, the 90-day plan,
  or Righetto marketing rhythm. When the user writes **"SKILL"** (in quotes) on Friday,
  program the day's improvement work — read skill-competitor-roadmap-q3-2026.md §8.
---

# Righetto: venerdì operativo + ciclo 12 settimane

## Trigger `"SKILL"` (BLOCCANTE — venerdì)

Quando l'utente scrive **`"SKILL"`** (virgolette incluse):

1. Leggi `TEST-SKILL/skill-competitor-roadmap-q3-2026.md` **§8**
2. Leggi `skill-memoria-progressi.md` + `data/editorial-queue.json` + `data/gsc-indexing-weekly.json` + `data/gsc-keywords-priority.json` + `data/competitor-roadmap-q3-2026.json`
3. Output piano giornata (formato §8 skill-competitor) — **max 3 task repo + 2 task utente GSC/GBP**
4. Non lista generica — scegli da SOSTENERE · blog coda · gap Q3 · macrociclo 12 sett.

Sinonimi: «SKILL», «piano SKILL», `"SKILL"` il venerdì.

---

## Contesto sito (per l'agente)

- Repo sito: `progetti/index` (static HTML, blog ricco, zone Padova, landing, Supabase per immobili/chatbot).
- Dominio: `https://righettoimmobiliare.it/`
- Obiettivo del rituale: contenuti + tecnico + misurazione, senza duplicare lavoro già fatto in settimana.
- **Orologio automatico (GitHub Actions):** ogni venerdì **07:00 CEST** il workflow `.github/workflows/venerdi-contenuti-freschezza.yml` esegue audit SKIMM + SEO intelligence + probe + **report email completo** a `info@righettoimmobiliare.it` (6 blocchi con numeri e trend settimana/settimana — vedi `TEST-SKILL/skill-seo.md` §11.6). Storico in `data/gsc-weekly-history.json`. Anche `venerdi-righetto-piano.yml` (~07:30) apre Issue settimana 1–12; `audit-settimanale.yml` e `mini-seo-check.yml` restano attivi.

## Quando applicare questa skill

0. **Utente scrive `"SKILL"`** → § Trigger sopra (priorità massima il venerdì)
0a. Leggi **`TEST-SKILL/skill-memoria-progressi.md`** — §Prossimi passi
0b. Leggi **`data/editorial-queue.json`** — prossimo blog `scheduled`
1. **È venerdì** e l'utente apre la chat: proponi "Venerdì Righetto — questa settimana fare…"
2. Utente chiede **cosa fare**, **programma settimanale**, **90 giorni**, **check sito**
3. Utente tagga **Righetto** + pianificazione

## Ancora data del programma

- **Inizio ciclo 12 settimane**: 31 marzo 2026 (settimana 1 = 31 mar – 6 apr 2026).
- Calcolo settimana corrente: `W = floor((oggi - 2026-03-31) / 7) + 1`, clamp tra 1 e 12. Se > 12, ripeti il ciclo dalla settimana 1 o chiedi all'utente se aggiornare l'ancora.

## Macrociclo 12 settimane (tema + output atteso)

| Sett. | Focus | Output minimo settimanale |
|------|--------|---------------------------|
| 1 | Baseline & Search Console | Esporta/query top pagine e query; elenco 5 URL da migliorare (CTR o posizione 11–20). |
| 2 | Link interni pillar | Da homepage e da 3 blog forti, aggiungere link verso 2 pagine "CRESCITA" o "DA MIGLIORARE". |
| 3 | Blog: aggiornamento + FAQ | 1 articolo nuovo O 1 articolo esistente con +FAQ/schema e data aggiornamento. |
| 4 | Zone locali | 1 scheda zona o ampliamento contenuto (testo unico, internal link). |
| 5 | Immagini & Core Web Vitals | Audit LCP su homepage + 2 template blog; ottimizzare 1 hero o lazy-load. |
| 6 | Landing conversione | 1 landing (valutazione / vendita / mutuo): CTA, copy sopra piega, testo unico 200 parole. |
| 7 | Schema allineamento | Pagine con 1 solo JSON-LD: portarle a set minimo (Organization/WebPage + dove serve FAQ/Local). |
| 8 | Recensioni & trust | Widget/testo recensioni Google coerente su 3 pagine chiave; verifica NAP su contatti. |
| 9 | Contenuti lunghi "money" | 1 pezzo 2000+ parole su mutuo / compravendita / costi (già in portafoglio: rafforzare internal link). |
| 10 | Stagionalità & studenti | Rafforzare cluster affitti/studenti (link da blog a servizio-locazioni e zone universitaria). |
| 11 | Sitemap & indici | Confronto sitemap vs HTML pubblicati; risolvere orphan pages o lastmod obsoleti. |
| 12 | Review trimestrale | Report: cosa ha funzionato, 3 ipotesi test A/B titoli meta, piano prossimo trimestre. |

## Checklist ricorrente (ogni venerdì, ~45–90 min)

Usa questa lista nell'output per l'utente; adatta alle priorità della settimana del macrociclo.

1. **Dati**: Search Console (ultimi 7/28 gg) — 1 opportunità e 1 anomalia. **Vedi § Search Console sotto** (checklist completa 10 URL + sitemap + 404/5xx).
2. **Pubblicato**: 1 modifica concreta nel repo — **se settimana macrociclo 3 (Blog):** pubblica prossimo item da `data/editorial-queue.json` (`scheduled`) seguendo `TEST-SKILL/skill-editorial-queue.md`; altrimenti SOSTENERE o fix tecnico.
3. **Local**: Google Business Profile — 1 post o foto o risposta a recensione (azione manuale utente). **Se attivo cron `righetto_social/`:** verificare post notizie RSS (mar/gio) e mirror Meta→GBP in `.env`.
4. **Qualità**: un URL a caso tra top traffico — mobile ok? CTA visibile senza scroll eccessivo?
5. **Prossima settimana**: 1 sola priorità numerata (la più impattante).
6. **Probe tecnico (repo):** `python scripts/probe_live_urls.py` → verificare `data/url-probe-latest.json` (target: 0 issue su ~460 URL); committare snapshot se ci sono fix deployati.
7. **Homepage visite virtuali:** aprire `/` → sezione «Visite virtuali 360°» deve mostrare **solo** immobili **attivi** con tour (max 4, più recenti in admin). Se un annuncio è disattivato non deve comparire. Nuovo acquisito con tour: entry in `data/visite-virtuali.json` + scene in admin.
8. **Admin — annunci disattivati:** venduti/ritirati → `attivo=false` in admin + `"homepage": false` in `visite-virtuali.json` (es. LA0319). **LP0286, LA0317, UFF2247** restano attivi e nel tour se in vendita.

## Search Console — verifica ogni venerdì (+ follow-up lunedì)

**Proprietà GSC:** `righettoimmobiliare.it` (dominio, **senza** www) — copre tutto il sito. **Non** serve aggiungere proprietà `www`.  
**URL canonici:** sempre `https://righettoimmobiliare.it/...` (**senza** `www`, **senza** `.html`).

**Registro ispezioni:** aggiorna `data/gsc-indexing-weekly.json` → `inspection_log` dopo ogni check utente (data, URL, esito, azione).  
**Batch prossimo venerdì:** stesso file → `next_friday_batch.urls` — **includere sempre nel output venerdì** per l'utente.

### Cosa fare letteralmente in GSC (venerdì ~15 min)

1. Apri [Search Console](https://search.google.com/search-console) → proprietà `righettoimmobiliare.it`
2. **Prestazioni** (7 + 28 gg): 1 query Limena/non-brand da migliorare → aggiorna `data/gsc-keywords-priority.json`
3. **Indicizzazione → Pagine:** controlla 404/5xx; se fix deployati → **Convalida correzione**
4. **Sitemap:** solo `https://righettoimmobiliare.it/sitemap.xml` — stato **Operazione riuscita**; **non** aggiungere URL singole come sitemap
5. **Ispezione URL** (barra in alto): per ogni URL del batch settimanale:
   - incolla URL → Invio
   - se **«URL presente su Google»** → passa al successivo (**non** richiedere di nuovo)
   - se **«URL non presente su Google»** → **Richiedi indicizzazione** (max ~10/giorno)
6. Aggiorna `inspection_log` in `gsc-indexing-weekly.json` con gli esiti

**Esito 24/07/2026 (utente):** 9/10 già su Google; **solo** [`/servizio-vendita`](https://righettoimmobiliare.it/servizio-vendita) ha ricevuto richiesta indicizzazione → follow-up **lunedì 28/07** e **venerdì 31/07**.

### Batch 24/07/2026 ✅ (completato)

```
https://righettoimmobiliare.it/
https://righettoimmobiliare.it/servizio-vendita          ← RICHIESTA inviata 24/07
https://righettoimmobiliare.it/agenzia-immobiliare-padova
https://righettoimmobiliare.it/zona-limena
https://righettoimmobiliare.it/immobili
https://righettoimmobiliare.it/blog-limena-vs-padova-centro-dove-comprare-2026
https://righettoimmobiliare.it/blog-mercato-immobiliare-limena-2026
https://righettoimmobiliare.it/blog-appartamento-nuova-costruzione-limena
https://righettoimmobiliare.it/blog-scegliere-agenzia-immobiliare-padova-2026
https://righettoimmobiliare.it/blog
```

### Batch prossimo venerdì — **31/07/2026** (promemoria obbligatorio in output)

```
https://righettoimmobiliare.it/servizio-vendita          ← FOLLOW-UP (richiesta 24/07)
https://righettoimmobiliare.it/blog-agenzia-immobiliare-limena-come-scegliere-2026   ← appena pubblicato eq-002
https://righettoimmobiliare.it/servizio-locazioni
https://righettoimmobiliare.it/servizio-valutazioni
https://righettoimmobiliare.it/blog-rendimento-affitto-padova
https://righettoimmobiliare.it/blog-affitto-studenti-padova
https://righettoimmobiliare.it/blog-contratto-affitto-padova
https://righettoimmobiliare.it/blog-mandato-esclusivo-padova-perche-conviene-2026
https://righettoimmobiliare.it/landing-consulenza-immobiliare-gratuita
https://righettoimmobiliare.it/blog-affitti-limena-2026
```

5. **Non richiedere** indicizzazione su URL legacy (`/home`, `/agenzia`, `/blog-articolo?s=...`) — reindirizzano alle pagine canoniche sopra.

**Esito atteso:** canonical = stesso URL senza www; oppure «Richiesta di indicizzazione inviata il …».

### Lunedì (follow-up, ~10 min)

> Dopo batch SEO (redirect, sitemap, richieste manuali) o ogni lunedì se il venerdì non c'è tempo.

- [ ] **Follow-up** URL con richiesta inviata il venerdì prima (es. `/servizio-vendita` dal 24/07)
- [ ] Rileggere ispezione sul batch corrente: «presente su Google» o richiesta in coda
- [ ] Report **404 / 5xx**: trend in calo vs settimana precedente
- [ ] Se canonical mostra `www` diverso dal sito → segnalare fix canonical in repo (`skill-seo.md` § GSC)
- [ ] Agente: rieseguire `python scripts/probe_live_urls.py` e confrontare con `data/url-probe-latest.json`

Dettaglio tecnico redirect/404: repo `scripts/build_seo_redirects.py`, `404.html`, `js/redirects-404.js` — vedi **`TEST-SKILL/skill-seo.md` § GSC settimanale**.

## Anti-intoppi cron venerdì (agente — BLOCCANTE)

Prima di chiudere ogni task venerdì:

1. **JSON valido:** `python -c "import json; json.load(open('data/gsc-keywords-priority.json')); json.load(open('data/gsc-weekly-history.json'))"` — se errore, **fix prima del commit**
2. **Workflow:** `.github/workflows/venerdi-contenuti-freschezza.yml` ha step validazione JSON (commitato 24/07)
3. **Probe:** file `venerdi-*.html` sono locali/gitignore — **non** devono finire in sitemap né essere contati come 404 sito (`probe_live_urls.py` esclude `venerdi-*`)
4. **Blog:** il cron **07:00 non pubblica** articoli — publish = agente su richiesta utente (`editorial-queue.json`)
5. **Email cron:** richiede secret `EMAIL_RELAY_KEY` su GitHub; se manca, Issue + commit storico GSC possono comunque procedere
6. **Output venerdì:** includere sempre `next_friday_batch` da `gsc-indexing-weekly.json` + stato blog `scheduled` in coda

**Se cron fallisce:** controllare Actions → `Venerdì Contenuti & Freschezza` → log step `Valida JSON dati GSC`; rigenerare localmente:
`python scripts/venerdi-contenuti-freschezza.py` → `venerdi-seo-intelligence.py` → `probe_live_urls.py` → `venerdi-report-email.py` → `venerdi-report-pdf.py`

## Report email settimanale (automatico)

**Ogni venerdì 07:00 CEST** → email HTML a **info@righettoimmobiliare.it** con:

1. Sintesi (salute %, blog, probe)
2. GSC con Δ vs settimana scorsa e dall'inizio tracking (`gsc-weekly-history.json`)
3. Indicizzazione: probe live 16 URL prioritarie (`gsc-indexing-priority.json`) + promemoria Ispezione URL GSC
4. SOSTENERE / refresh (PAGE SCORE)
5. SKIMM + articoli pubblicati in settimana
6. Azioni priorità

**Tu ogni venerdì (5 min prima del cron o subito dopo):** GSC → Prestazioni → aggiorna `data/gsc-keywords-priority.json` così l'email ha dati freschi.

## SEO Intelligence — cron venerdì (PAGE SCORE)

**Script:** `python scripts/venerdi-seo-intelligence.py` (dopo `venerdi-contenuti-freschezza.py`) + `venerdi-report-email.py` per invio mail.

**Tu ogni venerdì (5 min):** GSC → Prestazioni → aggiorna `data/gsc-keywords-priority.json` con top query/pagine 7+28 gg (opp. CSV in `data/gsc-export-*.csv`).

**Decisioni report:**

| Etichetta | Cosa fare |
|---|---|
| **SOSTENERE** | Refresh title/meta/H2 — **prima** di scrivere articoli nuovi |
| **AGGIUNGERE** | Max 1 articolo/settimana se gap keyword confermato |
| **GEO** | FAQ + box sintesi 40 parole + Linda allineata |
| **MANTENERE** | Winner — solo timestamp mensile |
| **CONSOLIDARE** | Link interni tra articoli stesso cluster (SKIMM risks) |

Framework completo: **`TEST-SKILL/skill-seo.md` §11** · Regola skimm: **`skimm.md` §1.10**.

## Formato risposta venerdì (obbligatorio per l'agente)

```markdown
## Venerdì Righetto — Settimana [N]/12 ([date])

**Tema fase:** [dalla tabella]

**GSC — batch URL prossima settimana ([data])**
- [ ] … (10 URL da next_friday_batch o gsc-indexing-weekly.json)

**Blog coda**
- [ ] Prossimo scheduled: [slug] — stato [scheduled/published]

**Da fare oggi / nel weekend**
- [ ] …

**Da fare lunedì–giovedì prossimi**
- [ ] …

**Un solo focus se hai poco tempo**
- …
```

## Note

- Non sostituire consulenza legale/fiscale nei testi: rimandare a professionisti dove serve.
- Commit su `main` dopo modifiche al sito, messaggio chiaro in italiano.
- **Social cron (`righetto_social/`):** domenica `cron_settimanale.bat` (bozze + rotazione catalogo 3 slot/sett. + 2 notizie RSS); lun–ven `cron_pubblica.bat` (Meta + GBP). Skill completa: **`TEST-SKILL/skill-social-automation.md`** (checklist avvio, token PAGE, reel 9007). Sintesi: `TEST-SKILL/SKILL-2.0.md` **10.4**.

### Social — check venerdì (se cron attivo)

- [ ] `python verifica_meta.py` (token PAGE OK)
- [ ] Agenda: post settimana senza `PUB_ERR` in note
- [ ] Prossima domenica: bozze generate / approvate?
- [ ] GBP: token in `.env` se OAuth completato (altrimenti solo Meta)
- **AEO / AI search:** per articoli macro-trend, seguire `TEST-SKILL/SKILL-2.0.md` sezione **8.2.5** (box sintesi, FAQ allineata, fonti istituzionali, aggiornamento `llms.txt`).
- **Landing vendita / segnalazioni (non blog):** sezione **8.2.6** (WebPage+FAQ, wiring servizi/footer/sitemap/`llms.txt`, hero WebP quando possibile).
- Se l'utente non usa Search Console, sostituire il punto 1 con "verifica manuale 5 query su Google in incognito".
