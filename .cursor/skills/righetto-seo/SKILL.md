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

1. `TEST-SKILL/skill-essentials.md` + `TEST-SKILL/skill-massimo-punteggio.md`
2. `TEST-SKILL/skill-seo.md` (framework completo)
3. Per refresh contenuti: anche `TEST-SKILL/skill-content.md`

## Audit automatico (target 100%)

```bash
python scripts/google-compliance-check.py
bash scripts/mini-seo-check.sh
bash scripts/audit-skill.sh
python scripts/probe_live_urls.py
```

Patch batch se WARN: `patch_compliance_warns.py`, `patch_audit_warns.py`, `patch_cdn_local.py`

## Gate on-page (ogni pagina toccata)

- Title ≤60 (max 70), meta 120–155 (max 160)
- H1 unico, diverso da title/meta
- Canonical + OG **senza** `.html` e **senza** `www`
- `node scripts/validate-page.js --file pagina.html`

## GEO / AEO

- Prime 2 righe dichiarative con entità (Padova, servizio, dato fonte)
- `llms.txt` aggiornato dopo nuovi pillar/blog/zone
- `robots.txt`: non bloccare GPTBot, ClaudeBot, Google-Extended, PerplexityBot

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
