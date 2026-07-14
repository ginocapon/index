# Memoria progressi SEO — Righetto Immobiliare

> **Scopo:** cronostoria decisionale per non ripartire da zero. Leggere **prima** di rispondere a «cosa fare per migliorare il sito», «audit», «venerdì», «priorità SEO».
>
> **Aggiornare:** a ogni audit significativo, deploy SEO, fix GSC o sprint completato (1 riga in §Log + eventuale modifica §Stato / §Prossimi passi).
>
> **Collegamenti:** `data/gsc-keywords-priority.json` · `data/gsc-weekly-history.json` · `data/gsc-baseline-16m.json` · `data/geo-ai-audit-latest.json` · `data/url-probe-latest.json`

---

## Stato sintetico (ultimo aggiornamento: 14 luglio 2026)

| KPI | Valore | Target 95% | Note |
|-----|--------|------------|------|
| Compliance repo | **100%** (0 ERR, 0 WARN) | 100% | Fix 14/07 su 3 pagine |
| Probe URL live | **494 URL, 0 errori** | 0 issue | `probe_live_urls.py` |
| GEO / AI / GA4 | **PASS** | PASS | 107 blog in llms, Consent v2 |
| GSC indicizzate | **74** pagine | Monitorare | OK |
| GSC «scansionata non indicizzata» | **16** | → 0 in report | **Lag GSC** — `site:` conferma indicizzate |
| Content health (cron) | **85%** | 95% | 14 avvisi SKIMM da smaltire |
| SERP 16 mesi | 2.470 click, CTR **7%**, pos. **9,2** | +non-brand | Baseline `gsc-baseline-16m.json` |
| Score complessivo stimato | **~84%** | **95%** | Piano §Prossimi passi |

---

## Linea conduttrice (sempre valida)

### Cosa fare — ordine di priorità

1. **SOSTENERE** prima di pubblicare nuovo blog → `pages_refresh_priority` in `gsc-keywords-priority.json`
2. **1 modifica concreta/settimana** nel repo (venerdì) — mai solo teoria
3. **Compliance 0 ERR** prima di nuovi contenuti massivi
4. **Query non-brand Limena** (`affitti limena`, `agenzia immobiliare limena`, `omi padova`) → link interni + pillar esistenti, non doppioni blog
5. **GSC manuale 15 min/venerdì** — Prestazioni 28 gg, sitemap `sitemap.xml` sola, Ispezione URL max 10/giorno

### Cosa NON fare (errori già commessi / tempo perso)

- Non inserire **URL singole pagine** nel box Sitemap GSC (solo `sitemap.xml`)
- Non panico sulle **16 grigie** se `site:` mostra indicizzazione
- Non **Convalida correzione** senza fix deployato (eccezione: lag indicizzazione senza fix codice — OK una tantum)
- Non 3 blog/settimana — SKIMM max **1 AGGIUNGERE** se gap confermato
- Non aspettarsi 95% solo con codice — **CTR e tempo Google** contano

### Quando fare cosa

| Frequenza | Azione | Dove |
|-----------|--------|------|
| **Venerdì 07:00** | Cron GitHub: SKIMM, audit, mini-seo, email | Automatico |
| **Venerdì ~45 min** | GSC + 1 fix repo | `/venerdi` skill |
| **Settimana macrociclo** | Tema 12 settimane (ancora 31/03/2026) | `righetto-venerdi-sito-90giorni` |
| **Mar + Ven 08:00** | Security check | `security-check-bisettimanale.yml` |
| **Ogni 6 h** | Sync foto immobili | `sync-media-github.yml` (+ `SUPABASE_KEY`) |
| **Mensile** | Audit completo `audit_completo` in context-map | Questo file + compliance |

### Macrociclo 12 settimane — posizione 14/07/2026

- Ancora: **31 marzo 2026** → settimana **15** → nel ciclo riparte **settimana 3 = Blog + FAQ**
- Output settimana 3: 1 articolo nuovo **oppure** refresh con FAQ/schema + `dateModified`

---

## Piano verso 95% (8 settimane da 14/07/2026)

| Sett. | Focus | Done? |
|-------|--------|-------|
| S1 (14–20 lug) | Compliance 100% + memoria skill + Convalida GSC 16 | Compliance ✅ · GSC manuale utente |
| S2 | Link interni pillar Limena (5 link da winner: home, blog-affitto-studenti) | ☐ |
| S3 | 1 refresh blog FAQ/schema (macrociclo) | ☐ |
| S4 | PSI homepage + 1 blog hero (LCP documentato) | ☐ |
| S5 | 3 avvisi SKIMM risolti → content health ~90% | ☐ |
| S6 | CTA `servizio-valutazioni` sopra piega | ☐ |
| S7 | Export CSV GSC fresco → `data/gsc-export-*.csv` | ☐ |
| S8 | Review trimestrale + test 3 titoli meta | ☐ |

---

## Cluster SEO prioritari (non-brand)

| Query | Imp (snapshot 13/07) | Azione | Stato |
|-------|----------------------|--------|-------|
| affitti limena | 12 | blog-affitti-limena-2026 + zona-limena + link interni | Pubblicato 09/07, meta refresh 13/07 |
| agenzia immobiliare limena | 13 | agenzia-immobiliare-padova SOSTENERE | Refresh 13/07 |
| omi padova | 14 | pillar blog-quotazioni-locazioni-omi-istat-padova-2026 AEO | Refresh 13/07 |
| blog-rendimento-affitto-padova | 139 imp, 0 click | SOSTENERE meta | Refresh 13/07 |

**Pagine SOSTENERE refreshate 13–14/07:** zona-limena, agenzia-immobiliare-padova, blog-rendimento-affitto-padova, blog-affitto-breve-padova-2026, pillar OMI — tutte HTTP 200, indicizzate (`index-check-sostenere-latest.json`).

---

## GSC — note operative

- **Proprietà:** `righettoimmobiliare.it` (senza www)
- **Canonical:** `https://righettoimmobiliare.it/...` senza `.html`
- **74 indicizzate:** nessuna azione
- **16 scansionata non indicizzata:** report stale (crawl mar–apr 2026); verifica `site:` = indicizzate. Azione utente: **Convalida correzione** + reinvia `sitemap.xml`
- **3 sitemap errate** (URL pagine inviate per sbaglio): ignorare o rimuovere; usare solo `sitemap.xml`

---

## Automazioni e gap noti

| Sistema | Stato |
|---------|--------|
| llms.txt / ai.json / 107 blog | ✅ |
| GA4 G-PHEL8KXLBX + Consent Mode v2 | ✅ live |
| Legacy redirect stubs rimossi | ✅ compliance da 12% a 71%+ |
| `SUPABASE_KEY` GitHub Actions | ⚠️ verificare secret per sync media |
| GBP post settimanale | Manuale utente |
| Backlink / DA | Gap off-site — PR esterno |

---

## Log cronologico

| Data | Cosa | Esito |
|------|------|-------|
| 09/07/2026 | Baseline GSC 16 mesi catturata | 2470 click, impression in crescita |
| 09/07/2026 | 3 blog Limena/transitorio/rubano pubblicati | Cluster affitti Limena |
| 13/07/2026 | Sprint GEO/AI: llms sync 107/107, Consent Mode, SOSTENERE 5 URL | Commit 4495af6, 5601f91 |
| 13/07/2026 | Refresh meta SOSTENERE + pillar OMI AEO | `gsc-keywords-priority.json` |
| 14/07/2026 | Cleanup stub redirect legacy | Compliance 71%, 0 ERR |
| 14/07/2026 | sitemap lastmod SOSTENERE 2026-07-14 | Index check OK |
| 14/07/2026 | Audit complessivo: score ~84%, piano 95% | Questo file creato |
| 14/07/2026 | Fix 4 WARN compliance → 100% | transitorio, relazione-tecnico, zona-ponte |

---

## Prossimi passi (per l'agente — non proporre altro finché non fatti)

1. **Utente GSC:** Convalida 16 + Prestazioni `affitti limena` (manuale)
2. **Repo S2:** link interni da `/` e `blog-affitto-studenti-padova` → `zona-limena` + `blog-affitti-limena-2026`
3. **Repo S5:** smaltire 3 avvisi SKIMM (prima settimana disponibile)
4. **Verifica:** `SUPABASE_KEY` in GitHub Secrets

---

## Come usare questo file (agente)

```
1. Leggi §Stato sintetico + §Prossimi passi
2. Se utente chiede «cosa fare» → rispondi da §Piano e §Prossimi passi, NON lista generica
3. Dopo ogni task completato → aggiorna Log + spunta Done nel piano
4. Carica anche: skill-massimo-punteggio.md, gsc-keywords-priority.json
```

**Routing context-map:** task `audit_seo`, `ottimizzazione_contenuto`, `venerdi_contenuti_skimm` → includere questo file.
