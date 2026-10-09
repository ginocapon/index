# Lead automation Righetto — Livello A + B (2026-10-09)

**Obiettivo:** alert lead caldi in minuti (deterministico), arricchimento async (RAG/LLM), funnel tracciabile — **senza** sostituire form vanilla né frontend Crestview.

## Architettura

| Livello | Dove | Cosa |
|---------|------|------|
| **A** | Supabase `richieste` + Edge `score-lead-righetto` | Score 0–100, temperatura, `owner_path`, dedup, evento `lead_events`, Telegram HOT |
| **B** | n8n (self-host o cloud) | RAG su `kb_documents`, email draft, Meta — **async**, mai bloccare invio form |

Config: `data/lead-automation-config.json` · SQL: `sql/righetto-lead-automation-extension.sql` · Regole allineate: `data/lead-scoring-rules.json`.

## Deploy (ordine)

1. Eseguire SQL in Supabase (staging → produzione con OK esplicito).
2. `supabase functions deploy score-lead-righetto` — secrets: `WEBHOOK_SECRET`, opz. `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`.
3. Database Webhook: tabella `richieste`, evento `INSERT` → URL function + header `x-righetto-webhook-secret`.
4. n8n: adattare workflow da repo analizzato `karl22puday-eng/real-estate-lead-automation` (no commit del clone `_tmp_*` senza licenza). KB testi: `automation/kb-righetto/`.

## Vincoli

- **GDPR / AI Act:** nessun LLM in browser; riassunti AI solo server-side; Linda già coperta da `skill-ai-act-compliance.md`.
- **No percentuali mediazione** in automazioni email.
- **Claim sito:** solo verificati (350+ immobili, 101 comuni, ecc.).
- **KPI Nord Star:** tolleranza ±1% — automation non sostituisce compilazione manuale `acquisition-kpi-template.json`.

## Segnali score (Livello A)

Vedi `lead-automation-config.json` → `signals_deterministic`. Hot ≥ 70 → Telegram + priorità admin `richieste`.

## Funnel eventi

Tabella `lead_events`: `ricevuto` → `contattato` → `appuntamento` → `incarico` → `rogito` → `provvigione_maturata`. Admin: estendere UI quando colonne presenti.

## Riferimenti cron

Venerdì fase 0: verificare webhook attivo, conteggio HOT/settimana, dedup rate. Skill: `skill-acquisizione-cron-venerdi.md` + `skill-strategia-nord-star-12m-acquisizione.md`.
