# LINDA Learning Bridge

Modulo di integrazione **opzionale e reversibile** per LINDA (`js/chatbot.js`) e Premortem Guardian (`righetto-premortem-guardian/`).

## Principio

**OSSERVA → IMPARA → PROPONE → TESTA → MISURA → APPLICA → VERIFICA → ROLLBACK**

Non modifica prezzi, disponibilità o caratteristiche immobiliari.

## Architettura

| Livello | File | Ruolo |
|---------|------|-------|
| A. Event Collector | `js/linda-learning-bridge.js` + `engines/event-collector.mjs` | Normalizza eventi, no PII |
| B. Learning Engine | `engines/learning-engine.mjs` | Aggregazione statistica |
| C. Ranking Insight Engine | `engines/ranking-insight-engine.mjs` | Insight con sample_size/confidence |
| D. Evaluation Engine | `engines/evaluation-engine.mjs` | Backtest, candidati, rollback |

## Comandi (via Guardian dispatcher)

```bash
node righetto-premortem-guardian/scripts/guardian.mjs learning collect
node righetto-premortem-guardian/scripts/guardian.mjs learning daily
node righetto-premortem-guardian/scripts/guardian.mjs learning weekly
node righetto-premortem-guardian/scripts/guardian.mjs learning biweekly
node righetto-premortem-guardian/scripts/guardian.mjs learning monthly
node righetto-premortem-guardian/scripts/guardian.mjs learning full
```

## Disattivazione

```html
<script>window.LINDA_LEARNING_BRIDGE = false;</script>
```

LINDA resta pienamente funzionante.

## Database

Eseguire `sql/linda-learning-bridge.sql` su Supabase.

## Output

Report in `data/learning-bridge/`:

- `learning-report.json`
- `ranking-insights.json`
- `evaluation-latest.json`
- `ranking-versions.json`
- `learning-bridge-full-report.json`

## Rollback ranking

`config.yaml` → `apply_ranking_changes: false` (default).  
Se un ranking candidato peggiora i KPI oltre `rollback_regression_pct`, `evaluation-engine` ripristina `baseline_v1`.
