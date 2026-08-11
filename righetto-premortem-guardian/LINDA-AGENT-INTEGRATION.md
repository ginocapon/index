# Linda Agent × Guardian — integrazione

## Entry point unico background

```bash
python3 scripts/linda-agent-cycle.py
```

Guardian job: `linda_agent_cycle` (cron-matrix) — **non** duplica `web_keyword_discovery` né `audit-settimanale`.

## Adapter

`adapters/registry.mjs` → `lindaAgentAdapter` ingesta:

- `data/linda-quality-latest.json`
- `data/linda-question-intelligence-latest.json`
- `data/linda-faq-proposals-latest.json`
- `data/linda-property-index-latest.json`

## Frontend

1. `js/linda-agent.js` (contesto + intent + ranking)
2. `js/chatbot.js` (UI + Supabase + FAQ + lead)

Caricamento: lazy loader carica linda-agent poi chatbot.

## Premortem mensile Linda

Usa `monthly_full_premortem` Guardian + checklist in `skill-linda-agent.md` §12.

Failure modes: immobili obsoleti, keyword shadowing FAQ, ranking senza match, lead non salvati, score quality < 60.
