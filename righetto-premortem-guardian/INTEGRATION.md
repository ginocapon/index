# Integrazione Guardian — Righetto Immobiliare

Documento di riferimento post-analisi (A–G) e piano operativo.

## A. Architettura attuale

| Layer | Componenti | Path chiave |
|-------|------------|-------------|
| Frontend | HTML/CSS/JS vanilla, GitHub Pages | `*.html`, `js/`, `css/` |
| Dev server | Express static | `server.js` |
| Email prod | cPanel PHP relay | `api/send-mail.php` |
| Backend dati | Supabase Postgres + Storage + Edge | `supabase/`, `sql/` |
| Lead | `rig-lead-form.js`, `richieste` | `js/rig-lead-form.js`, `js/config.js` |
| Linda/AI | Rules-based chatbot | `js/chatbot.js` |
| Immobili | Admin + sync 6h | `admin.html`, `sync-media-github.yml` |
| Social/Reel | Windows cron locale | `righetto_social/` |
| Audit frammentato | 8 workflow GHA + ~20 script | `scripts/`, `.github/workflows/` |
| Analytics | GA4 consent + snapshot manuali | `js/ga-consent.js`, `data/analytics-dashboard.json` |

## B. Riutilizzato dal Guardian

- Script audit: `probe_live_urls.py`, `mini-seo-check.sh`, `security-check.sh`, `audit-skill.sh`
- AI: `audit_chatbot_faq.py`
- Analytics: `verify_ga_consent_live.py`, ingest `data/*.json`
- Lead: `guardian-leads-snapshot.py` (nuovo, thin wrapper Supabase)
- Media: `verify_media_migration.py` (se `SUPABASE_KEY`)
- Performance/GEO: `audit_geo_ai_postdeploy.py`
- Content: `check_doppioni_sito.py`
- Policy/cron/sequenza dal pacchetto ONE_COMMAND

## C. Adattato

- Path `righetto-premortem-guardian/` (da ZIP originale)
- `guardian.mjs` → dispatcher reale con adapter registry
- `cron-dispatch.mjs` → dedupe via `memory/state.json`
- Workflow esistenti → chiamano Guardian prima degli script (Issue/email invariati)
- Nuovo `guardian-dispatcher.yml` → entry point orario

## D. Integrazioni disponibili

- Supabase REST (`SUPABASE_KEY` in GHA)
- PHP email relay HEAD/POST test
- Live URL probe → `righettoimmobiliare.it`
- GitHub Issues/artifact da workflow
- File machine-readable in `data/*-latest.json`

## E. Integrazioni mancanti (adapter stub / documentate)

| Area | Gap |
|------|-----|
| GA4 | No Data API — solo `append-analytics-snapshot.yml` manuale |
| GSC | Solo `data/gsc-*.json` statici |
| Social | `righetto_social` su Windows — no heartbeat cloud |
| Backup | No script verifica export Supabase |
| CWV | No Lighthouse in CI |
| RLS | `check_rls_exposure.py` solo locale con `.env` |

## F. Rischi implementazione

1. **Duplicazione Friday 06:00** — mitigato: `state.json` salta job già eseguiti nell'intervallo
2. **SUPABASE_KEY assente** — lead/media check degradati, non simulati
3. **Exit code 1** su warning — workflow Guardian apre Issue `guardian`
4. **YELLOW actions** — non pubblicano; solo report
5. **Path drift** — `doctor` verifica file richiesti

## G. Premortem integrazione

| Causa futura fallimento | Segnale | Controllo | Azione | Verifica |
|------------------------|---------|-----------|--------|----------|
| Guardian ignorato, audit vecchi soli | Issue solo `audit` senza `guardian` | Confronto label Issues | Documentare entry point in skill | `doctor` + GHA |
| Doppio run costoso Friday | Log GHA > 30 min | `state.json` last_run | `--ingest-only` su workflow secondari | events.jsonl |
| Falso OK senza SUPABASE_KEY | `missing_integrations` vuoto erroneamente | Report JSON field | Adapter segnala SKIP esplicito | guardian-leads senza key |
| Auto-modifica contenuti | PR non approvati | policy RED | Solo `generate_report` GREEN | actions[].executed |

## Piano implementazione (eseguito)

1. ✅ Rinomina pacchetto → `righetto-premortem-guardian/`
2. ✅ Dispatcher + adapter registry + policy
3. ✅ `guardian-leads-snapshot.py`
4. ✅ `guardian-dispatcher.yml` + wire audit/seo/security
5. ✅ Skill Cursor `/guardian` token-light
6. ✅ `context-map.json` aggiornato

## Entry point unico

```bash
node righetto-premortem-guardian/scripts/guardian.mjs run
```

Cron esterno: schedulare **solo** questo comando; il dispatcher legge `config/cron-matrix.yaml`.

## Cron: mantenuti vs unificati

| Mantenuto | Ruolo |
|-----------|--------|
| `sync-media-github.yml` | Sync foto (dominio diverso) |
| `static.yml` | Deploy Pages |
| `venerdi-contenuti-freschezza.yml` | SKIMM email/PDF (da migrare gradualmente) |
| `append-analytics-snapshot.yml` | Input manuale GA4/GSC |
| `venerdi-righetto-piano.yml` | Piano editoriale Issue |

| Unificato via Guardian | Prima |
|------------------------|-------|
| `guardian-dispatcher.yml` | Nuovo hub orario |
| `audit-settimanale.yml` | Solo `audit-skill.sh` |
| `mini-seo-check.yml` | Solo `mini-seo-check.sh` |
| `security-check-bisettimanale.yml` | Solo `security-check.sh` |
