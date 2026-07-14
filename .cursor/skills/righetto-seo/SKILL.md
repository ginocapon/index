---
name: righetto-seo
description: >-
  Audit SEO, ottimizzazione SERP, zone locali, GEO/AEO e compliance Google per
  Righetto Immobiliare. Usa quando l'utente chiede audit SEO, fix meta/title,
  keyword stuffing, sitemap, schema, llms.txt, GSC, PAGE SCORE, probe URL,
  o ottimizzazione contenuti esistenti per ranking.
---

# SEO Righetto

## Prima di iniziare

1. **`TEST-SKILL/skill-memoria-progressi.md`** — stato, piano 95%, prossimi passi (non ripartire da zero)
2. `TEST-SKILL/skill-essentials.md` + `TEST-SKILL/skill-massimo-punteggio.md`
2. `TEST-SKILL/skill-seo.md` (framework completo)
3. Per refresh contenuti: anche `TEST-SKILL/skill-content.md`

## Audit automatico (target 100%)

```bash
python scripts/google-compliance-check.py
bash scripts/mini-seo-check.sh
bash scripts/audit-skill.sh
python scripts/probe_live_urls.py
python scripts/audit_geo_ai_postdeploy.py
python scripts/verify_ga_consent_live.py
node scripts/simulate_ga4_consent.cjs
```

Report snapshot: `data/geo-ai-audit-latest.json`, `data/ga-consent-verify-latest.json`

Patch batch se WARN: `patch_compliance_warns.py`, `patch_audit_warns.py`, `patch_cdn_local.py`

## Gate on-page (ogni pagina toccata)

- Title ≤60 (max 70), meta 120–155 (max 160)
- H1 unico, diverso da title/meta
- Canonical + OG **senza** `.html` e **senza** `www`
- `node scripts/validate-page.js --file pagina.html`

## GEO / AEO

- Prime 2 righe dichiarative con entità (Padova, servizio, dato fonte)
- `llms.txt` aggiornato dopo nuovi pillar/blog/zone — script: `python scripts/sync_llms_catalog.py`
- `robots.txt`: non bloccare GPTBot, ClaudeBot, Google-Extended, PerplexityBot
- GA4: `G-PHEL8KXLBX` + Consent Mode v2 via `js/ga-consent.js` (banner `cookie-consent.js?v=4`)

## GSC — monitoraggio AI Mode / AIO (venerdì)

In **Prestazioni** (28 gg, confronto periodo precedente):

1. Filtro query: `omi`, `affitti limena`, `agenzia immobiliare` + varianti non-brand
2. Tab **Filtri** → se disponibile segmento **AI** / **Panoramica ricerca con AI** (account beta)
3. Annotare in `data/gsc-keywords-priority.json`: query growth, pages SOSTENERE, `refreshed_this_week`
4. Dopo refresh meta: richiedi indicizzazione max 10 URL/giorno (lista in skill venerdì)

## Entity SEO (no stuffing)

- Frase 2+ parole max 5 occorrenze/pagina
- «a Padova» max 8–10 volte — sinonimi e varianti
- Conteggi solo su testo visibile (`audit_helpers.py`)

## PAGE SCORE (priorità venerdì)

| Etichetta | Azione |
|-----------|--------|
| **SOSTENERE** | Refresh title/meta/H2 prima di articoli nuovi |
| **AGGIUNGERE** | Max 1 articolo/sett se gap keyword confermato |
| **GEO** | FAQ + box sintesi 40 parole |
| **CONSOLIDARE** | Link interni stesso cluster (SKIMM) |

Dati: `data/gsc-keywords-priority.json`, `data/gsc-weekly-history.json`

## Dopo nuove URL

- `sitemap.xml` + link interni correlati + footer zone allineato

## Rule Cursor

`.cursor/rules/righetto-seo-geo.mdc` su `zona-*`, `sitemap.xml`, `llms.txt`

## Output atteso

Report issue + fix nel repo, validate-page OK, probe 0 issue, commit in italiano
