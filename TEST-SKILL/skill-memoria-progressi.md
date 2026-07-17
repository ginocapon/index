# Memoria progressi SEO — Righetto Immobiliare

> **Scopo:** cronostoria decisionale per non ripartire da zero. Leggere **prima** di rispondere a «cosa fare per migliorare il sito», «audit», «venerdì», «priorità SEO».
>
> **Aggiornare:** a ogni audit significativo, deploy SEO, fix GSC o sprint completato (1 riga in §Log + eventuale modifica §Stato / §Prossimi passi).
>
> **Collegamenti:** `data/gsc-keywords-priority.json` · `data/gsc-weekly-history.json` · `data/gsc-baseline-16m.json` · `data/gsc-indexing-weekly.json` · `data/ga4-weekly.json` · `data/geo-ai-audit-latest.json` · `data/url-probe-latest.json` · `data/internal-links-limena-2026.json`

---

## Stato sintetico (ultimo aggiornamento: 17 luglio 2026, mattina)

| KPI | Valore | Target 95% | Note |
|-----|--------|------------|------|
| Compliance repo | **100%** (0 ERR, 0 WARN) | 100% | ✅ |
| Probe URL live | **474 URL, apex OK** | 0 issue | Aggiornato 16/07 post-DNS |
| GEO / AI / GA4 | **PASS** | PASS | 108 blog in llms, Consent v2 |
| Link interni cluster Limena | **5 pagine sorgente** | Fatto | `internal-links-limena-2026.json` |
| GSC Prestazioni 28 gg | **271 clic, 4.22K impr, CTR 6,4%, pos. 7,7** | Monitorare | Snapshot 16/07 sera (screenshot) |
| GSC brand query | **154 clic** (6 query) | Crescita | vs 43 sett. precedente |
| affitti limena | **3 clic / 39 impr** | Crescita | Primi clic non-brand Limena |
| GSC indicizzazione | **7/166** (snapshot 15/07) | Monitorare | Verificare post-DNS ~22/07 |
| Content health (cron) | **85%** | 95% | 14 avvisi SKIMM = cluster |
| Score complessivo stimato | **~90%** | **95%** | +A11y fix CTA 16/07 |

---

## Linea conduttrice (sempre valida)

### Cosa fare — ordine di priorità

1. **SOSTENERE** prima di pubblicare nuovo blog → `pages_refresh_priority` in `gsc-keywords-priority.json`
2. **1 modifica concreta/settimana** nel repo (venerdì) — mai solo teoria
3. **Compliance 0 ERR** prima di nuovi contenuti massivi
4. **Query non-brand Limena** → link interni fatti 14/07; ora **misurare** in GSC Prestazioni
5. **GSC manuale 15 min/venerdì** — Prestazioni 28 gg, sitemap `sitemap.xml` sola, Ispezione URL max 10/giorno

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
| **Venerdì ~45 min** | GSC + 1 fix repo | `/venerdi` skill |
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
| GBP post settimanale | Manuale utente |
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

---

Dopo fix DNS apex (15/07): **controllare in GSC** se il bucket **«pagina con reindirizzamento»** (era ~74 nel filtro sitemap) è sceso. Aggiornare `data/gsc-indexing-weekly.json` → il PDF del venerdì 18/07 e 25/07 mostrerà il trend a barre.

---

## Prossimi passi (per l'agente)

1. **Utente GSC:** aggiorna Indicizzazione post-venerdì 17/07 + Convalida 16
2. **22/07:** verifica calo «reindirizzamento» GSC post-fix apex
3. **Blog S2:** agenzia immobiliare Limena (se GSC conferma crescita)
4. **PSI** su `/` e 1 blog — annotare LCP
5. **Opzionale:** `ga4-weekly.json` + export CSV GSC

---

## Appuntamento verifica (22 luglio 2026)

```
1. Leggi §Stato sintetico + §Prossimi passi
2. Se utente chiede «cosa fare» → rispondi da §Prossimi passi, NON lista generica
3. Dopo ogni task → aggiorna Log + piano
4. Carica: skill-massimo-punteggio.md, gsc-keywords-priority.json
```

**Routing context-map:** `audit_seo`, `ottimizzazione_contenuto`, `venerdi_contenuti_skimm` → includere questo file.
