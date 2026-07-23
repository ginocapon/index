# Memoria progressi SEO — Righetto Immobiliare

> **Scopo:** cronostoria decisionale per non ripartire da zero. Leggere **prima** di rispondere a «cosa fare per migliorare il sito», «audit», «venerdì», «priorità SEO».
>
> **Aggiornare:** a ogni audit significativo, deploy SEO, fix GSC o sprint completato (1 riga in §Log + eventuale modifica §Stato / §Prossimi passi).
>
> **Collegamenti:** `data/gsc-keywords-priority.json` · `data/gsc-weekly-history.json` · `data/gsc-baseline-16m.json` · `data/gsc-indexing-weekly.json` · `data/ga4-weekly.json` · `data/geo-ai-audit-latest.json` · `data/url-probe-latest.json` · `data/internal-links-limena-2026.json`

---

## Stato sintetico (ultimo aggiornamento: 22 luglio 2026)

| KPI | Valore | Target 95% | Note |
|-----|--------|------------|------|
| Compliance repo | **100%** (0 ERR, 0 WARN) | 100% | ✅ |
| Probe URL live | **474 URL, apex OK** | 0 issue | Aggiornato 16/07 post-DNS |
| GEO / AI / GA4 | **PASS** | PASS | 108 blog in llms, Consent v2 |
| Feature vs competitor | **8/8 + Confronta** | 6/8 Q3 | +«Confronta immobili» 22/07 · resta alert ricerca — `skill-competitor-roadmap-q3-2026.md` |
| GSC Prestazioni 28 gg | **271 clic, 4.22K impr, CTR 6,4%, pos. 7,7** | Monitorare | Snapshot 16/07 sera |
| GSC indicizzazione | **94 / 330** (17/07) | Monitorare | Redirect 90 — check **22/07** |
| Blog pubblicati | **108** | — | Mandato esclusivo 17/07 |
| Score complessivo stimato | **~95%** | **95%** | On-site 10/10; gap residuo off-site (recensioni GBP, backlink) |

---

## Linea conduttrice (sempre valida)

### Cosa fare — ordine di priorità

0. **Trigger `"SKILL"`** (venerdì) → piano giornata: `skill-competitor-roadmap-q3-2026.md` §8 + `/venerdi`
0b. **Coda editoriale** → `data/editorial-queue.json` + `skill-editorial-queue.md`
1. **SOSTENERE** prima di pubblicare nuovo blog → `pages_refresh_priority` in `gsc-keywords-priority.json`
2. **1 modifica concreta/settimana** nel repo — mai solo teoria
3. **Roadmap Q3** → max 1 feature engagement/settimana (`data/competitor-roadmap-q3-2026.json`)
4. **GSC manuale 15 min/venerdì** — Prestazioni, Indicizzazione, solo `sitemap.xml`

### Cosa NON fare (errori già commessi / tempo perso)

- Non inserire **URL singole pagine** nel box Sitemap GSC (solo `sitemap.xml`)
- Non panico sulle **16 grigie** se `site:` mostra indicizzazione
- Non **Convalida correzione** senza fix deployato (eccezione: lag indicizzazione — OK una tantum)
- Non 3 blog/settimana — SKIMM max **1 AGGIUNGERE** se gap confermato
- Non aspettarsi 95% solo con codice — **CTR e tempo Google** contano
- Non «fixare» i 14 avvisi SKIMM eliminando articoli — sono **alert cluster**, non errori

### Quando fare cosa

| Frequenza | Azione | Dove |
|-----------|--------|------|
| **Venerdì 07:00** | Cron GitHub: SKIMM, audit, email **«Verifica indicizzazioni»** + PDF | Automatico — §11.6 skill-seo |
| **Venerdì ~15 min** | Aggiorna `gsc-indexing-weekly.json` + opz. `ga4-weekly.json` | Utente — abilita grafici PDF |
| **Venerdì ~45 min** | GSC + 1 fix repo **o blog da coda** | `/venerdi` + `editorial-queue.json` |
| **Settimana macrociclo** | Tema 12 settimane (ancora 31/03/2026) | `righetto-venerdi-sito-90giorni` |
| **Mar + Ven 08:00** | Security check | `security-check-bisettimanale.yml` |
| **Ogni 6 h** | Sync foto immobili | `sync-media-github.yml` (+ `SUPABASE_KEY`) |
| **Mensile** | Audit completo `audit_completo` in context-map | Questo file + compliance |

### Macrociclo 12 settimane — posizione 14/07/2026

- Ancora: **31 marzo 2026** → settimana **15** → nel ciclo riparte **settimana 3 = Blog + FAQ**
- Output settimana 3: refresh FAQ su `blog-affitto-studenti-padova` ✅ (14/07)

---

## Piano verso 95% (8 settimane da 14/07/2026)

| Sett. | Focus | Done? |
|-------|--------|-------|
| S1 (14–20 lug) | Compliance 100% + memoria skill + Convalida GSC 16 | Compliance ✅ · memoria ✅ · GSC manuale utente |
| S2 | Link interni pillar Limena (5 pagine sorgente) | ✅ 14/07 |
| S3 | 1 refresh blog FAQ/schema (macrociclo) | ✅ `blog-affitto-studenti-padova` 14/07 |
| S4 | PSI homepage + 1 blog hero (LCP documentato) | ☐ manuale pagespeed.web.dev |
| S5 | 3 avvisi SKIMM | ☐ sono alert cluster — non bloccano; monitorare |
| S6 | CTA `servizio-valutazioni` sopra piega mobile | ✅ sticky bar 14/07 |
| S7 | Export CSV GSC fresco → `data/gsc-export-*.csv` | ☐ utente venerdì |
| S8 | Review trimestrale + test 3 titoli meta | ☐ sett. 8 |

---

## Cluster SEO prioritari (non-brand)

| Query | Imp (snapshot 16/07) | Azione | Stato |
|-------|----------------------|--------|-------|
| affitti limena | 39 impr, **3 clic** | blog + zona + link interni | ✅ misurare |
| agenzia immobiliare limena | 58 impr, **5 clic** | agenzia SOSTENERE + nuovo blog Limena (S2) | ☐ |
| mandato esclusivo padova | — | **blog 17/07** conversione venditori | ✅ pubblicato |
| omi padova | 14 impr | pillar OMI AEO | ✅ 13/07 |
| blog-rendimento-affitto-padova | 139 imp, 0 click | SOSTENERE — misurare CTR | ☐ monitor |

---

## GSC — note operative

- **Proprietà:** `righettoimmobiliare.it` (senza www)
- **Canonical:** `https://righettoimmobiliare.it/...` senza `.html`
- **74 indicizzate:** nessuna azione
- **16 scansionata non indicizzata:** Convalida correzione + reinvia `sitemap.xml` (utente)
- **3 sitemap errate** (URL pagine): ignorare

---

## Automazioni e gap noti

| Sistema | Stato |
|---------|--------|
| llms.txt / ai.json / 108 blog | ✅ |
| GA4 + Consent Mode v2 | ✅ |
| Compliance 100% | ✅ |
| Link interni Limena | ✅ |
| www → apex redirect | ✅ 15/07/2026 — DNS Serverplan + GitHub Pages |
| Email venerdì + PDF GSC/GA4 | ✅ 15/07/2026 — `venerdi-report-pdf.py` + allegato MIME |
| `send-mail.php` allegati | ⚠️ ricaricare su cPanel dopo deploy repo |
| `SUPABASE_KEY` GitHub Actions | ⚠️ verificare secret |
| Blog publish automatico (agente) | ✅ coda `data/editorial-queue.json` |
| Backlink / DA | Gap off-site |

---

## Log cronologico

| Data | Cosa | Esito |
|------|------|-------|
| 09/07/2026 | Baseline GSC 16 mesi | 2470 click, impression in crescita |
| 09/07/2026 | 3 blog Limena/transitorio/rubano | Cluster affitti Limena |
| 13/07/2026 | Sprint GEO/AI + SOSTENERE 5 URL | llms 107/107, Consent Mode |
| 14/07/2026 | Compliance 100% + memoria skill | 4 WARN chiusi |
| 14/07/2026 | Sprint S2+S3+S6: link Limena, FAQ studenti, CTA valutazioni | 5 pagine, sitemap lastmod |
| 15/07/2026 | DNS apex + GitHub custom domain senza www | www→apex 301 verificato live |
| 15/07/2026 | Repo: CNAME + robots.txt sitemap allineati | Coerente con canonical |
| 15/07/2026 | Email venerdì: oggetto «Verifica indicizzazioni» + PDF + blocco 7 checklist utente | Cron + skill §11.6 |
| 16/07/2026 | Fix WCAG CTA homepage · probe apex 474 URL · GSC JSON da screenshot sera | Compliance 100% |
| 17/07/2026 | Cron venerdì email OK · GSC 271 clic / brand 154 · blog mandato esclusivo | 108 blog, kw conversione |
| 17/07/2026 | Coda editoriale automatica: editorial-queue.json + skill-editorial-queue.md | 4 blog schedulati lug-ago |
| 18/07/2026 | Audit competitor IT + roadmap Q3 in skill-competitor-roadmap-q3-2026.md | Trigger `"SKILL"` venerdì · kit autobiografico push |
| 22/07/2026 | Sprint 10/10 on-site: box AEO «In sintesi» su 37 blog → **100%** · author-bio + link autore 100% | E-E-A-T + AEO chiusi |
| 22/07/2026 | Fix 7 cover hero rotte (immagini mancanti) + img gino-capon/linda-righetto | 0 asset locali mancanti |
| 22/07/2026 | **Feature Q3 Alert ricerca** (`RigAlert`): filtri attivi + email/WhatsApp + richieste admin | Tool engagement 100% |
| 22/07/2026 | **Feature Q3 «Confronta immobili»** (fino a 3, localStorage, tabella side-by-side) su `immobili.html` | RigCompare, vanilla JS, 0 dipendenze · compliance 100% |

---

## Roadmap Q3 competitor (riferimento rapido)

Vedi **`TEST-SKILL/skill-competitor-roadmap-q3-2026.md`** + `data/competitor-roadmap-q3-2026.json`.

| Priorità | Feature | Stato |
|----------|---------|-------|
| 1 | Alert ricerca immobili | ☐ Ago |
| 2 | Confronta 3 immobili | ☐ Ago |
| 3 | Costo totale acquisto scheda | ☐ Set |
| 4 | Indice €/mq OMI trimestrale | ☐ Set |
| 5 | Retrofit box AEO blog batch | ☐ |
| 6 | Bio autore batch Gino/Linda | ☐ |
| ✅ | Visita live immobile | Fatto |

---

## Prossimi passi (per l'agente)

1. **22/07:** verifica calo «reindirizzamento» GSC (target < 70 da 90)
2. **24/07:** blog eq-002 agenzia Limena se utente «pubblica blog»
3. **25/07:** utente scrive **`"SKILL"`** → piano venerdì §8 skill-competitor-roadmap
4. **Discovery:** coda scheduled < 3 → proposte GSC + web
5. **PSI** homepage — annotare LCP

---

## Appuntamento verifica (22 luglio 2026)

```
1. Leggi §Stato sintetico + §Prossimi passi
2. Se utente chiede «cosa fare» → rispondi da §Prossimi passi, NON lista generica
3. Dopo ogni task → aggiorna Log + piano
4. Carica: skill-massimo-punteggio.md, gsc-keywords-priority.json
```

**Routing context-map:** `audit_seo`, `ottimizzazione_contenuto`, `venerdi_contenuti_skimm` → includere questo file.
