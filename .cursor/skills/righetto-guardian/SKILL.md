---
name: righetto-guardian
description: >-
  Premortem Guardian Righetto — un solo entry point per monitoraggio, premortem,
  failure modes e remediation con policy GREEN/YELLOW/RED/BLACK. Usa quando
  l'utente chiede Guardian, premortem, health check sito, anomalie, dispatcher cron.
---

# Guardian — indice operativo (token-light)

**Entry point:** `node righetto-premortem-guardian/scripts/guardian.mjs run`

**Sequenza obbligatoria:** `righetto-premortem-guardian/sequences/master-sequence.md`

## Prima di agire

1. Leggi `TEST-SKILL/skill-essentials.md` (claim, stack, no dati inventati)
2. Leggi `righetto-premortem-guardian/AGENT.md` (contratto agente)
3. Policy autonomia: `righetto-premortem-guardian/policy/autonomy.yaml`

## Comandi

| Comando | Uso |
|---------|-----|
| `run` | Dispatcher auto (cron-matrix + state) |
| `run --jobs=site_integrity,security_check` | Job forzati |
| `run --ingest-only` | Solo ingest `data/*` |
| `doctor` | Verifica pacchetto |
| `sequence` | Stampa sequenza canonica |

## Adapter esistenti (no paralleli)

Guardian **riusa** script repo: `probe_live_urls.py`, `mini-seo-check.sh`, `security-check.sh`, `audit-skill.sh`, `audit_chatbot_faq.py`, `verify_ga_consent_live.py`, `guardian-leads-snapshot.py`, `verify_media_migration.py`.

Report: `righetto-premortem-guardian/reports/guardian-latest.{json,md}`

## Integrazioni NON disponibili (non inventare)

- GA4 Data API live · GSC API · Social heartbeat Windows · Backup Supabase auto · Lighthouse/CWV

## Regole

- GREEN = solo report/alert · YELLOW = proponi, no publish · RED/BLACK = stop
- Ogni failure mode → segnale + test + verifica
- No loop automatici · No soglie alterate per silenziare alert

Dettaglio architettura: `righetto-premortem-guardian/INTEGRATION.md`
