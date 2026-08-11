# SKILL — Linda Real Estate Agent (digitale rule-based)

> Evoluzione organica di `js/chatbot.js` + Guardian. **Non** seconda chatbot. **Non** LLM generativo in frontend (AI Act).

## 1. Architettura attuale (audit)

| Layer | Componente | Tipo |
|-------|------------|------|
| Frontend | `js/linda-agent.js` + `js/chatbot.js` | Rule-based agent + UI |
| Immobili | Supabase `immobili` (live) + `data/og-immobili.json` (OG/QR) | Fonte verità DB |
| Knowledge statica | `FAQ_DATA` in chatbot | Keyword + blog ref |
| Knowledge dinamica | Query Supabase + ranking client | No inventare annunci |
| Knowledge temporale | Blog + `data/linda-knowledge-temporal.json` (proposte) | Source + review_date |
| Lead | `richieste` + `SERVIZI_CONFIG.sendNotifica()` | Stesso stack form |
| Background | `scripts/linda-agent-cycle.py` | FAQ + QI + quality + index |
| Guardian | `linda_agent_cycle` job → adapter | Orchestra, no duplicati |
| QR | `qr-review.html`, `qr-property.html` | Redirect configurabile |
| Google review | `https://maps.app.goo.gl/xuCiRGDCSKskpTSf6` | Verificato in repo |

**Non presente:** RAG/embeddings, transcript chat persistenti, GSC/GA4 API live.

## 2. Architettura target

```
Utente → Linda UI → Intent (hard/soft) → Supabase retrieval → Ranking spiegabile → Risposta + lead opzionale
                              ↓
                    FAQ_DATA (fallback keyword)
Background (14 gg): FAQ discovery → Question intelligence → Quality score → Property index
                              ↓
                    Guardian ingest → report / Issue (YELLOW proposte)
```

## 3. Tre livelli conoscenza

- **Statica:** FAQ, servizi, orari, territorio — `FAQ_DATA`, pillar HTML
- **Dinamica:** Solo immobili `attivo=true`, `venduto=false` da Supabase
- **Temporale:** Blog, GSC statico, fonti istituzionali — metadati in proposte JSON (policy YELLOW)

## 4. Ricerca conversazionale

Esempio: *«Cerco casa a Padova, massimo 350.000, tre camere, garage se possibile»*

- Hard: budget max, camere min, operazione
- Soft: garage, giardino, terrazzo (non eliminano, influenzano score)
- Implementazione: `LindaAgent.parseSearchIntent()` + `cercaImmobiliAgent()`

## 5. Se non c'è match

Ordine in risposta: match ≥75 → quasi-match 55–74 → altre opzioni → CTA richiesta personalizzata Righetto.

## 6. Lead

Segnali: visita, contatto, interesse codice. Usa `contatto_*` + `salvaRichiesta()` con note da contesto ricerca. **No** CRM parallelo.

## 7. Ciclo bi-quindicinale (Guardian)

```bash
python3 scripts/linda-agent-cycle.py          # gate 14 gg
python3 scripts/linda-agent-cycle.py --force
```

Sub-script: `linda-faq-biweekly-discovery`, `linda-question-intelligence`, `linda-quality-benchmark`, `linda-property-index`.

Output: `data/linda-*-latest.json`, report `.md`.

## 8. Quality score

`data/linda-quality-latest.json` — score interno 0–100. **Non** claim «99,9%» senza benchmark live.

## 9. QR

| URL | Uso |
|-----|-----|
| `/qr-review` | Recensione Google (destinazione modificabile) |
| `/qr-property?s={slug}` o `?c={codice}` | Scheda immobile |

## 10. Policy Guardian (autonomy.yaml)

- **GREEN:** report, alert, benchmark, index refresh
- **YELLOW:** merge FAQ, publish contenuti, soglie
- **RED:** privacy, DB production, credenziali

## 11. Comandi agente

```bash
python3 scripts/merge_linda_faq_proposals.py   # dopo discovery YELLOW
python3 scripts/audit_chatbot_faq.py
node --check js/chatbot.js
```

Bump `linda-agent.js?v=N` e `chatbot.js?v=N` dopo modifiche.

## 12. Integrazione Guardian

Job cron-matrix: `linda_agent_cycle` (venerdì 05:00 UTC, gate 14 gg nel cycle script).

Sequenza: CONTEXT → OBSERVE (ingest `data/linda-*`) → VERIFY → ACT (solo GREEN) → LEARN (archive FAQ).

Dettaglio: `righetto-premortem-guardian/INTEGRATION.md` + `LINDA-AGENT-INTEGRATION.md`.

## 13. Phase 2 — Intent log, live benchmark, knowledge temporale

### Intent log anonimo (Supabase)

- Tabella: `sql/linda-chat-intents.sql` → eseguire in Supabase SQL Editor
- Frontend: `logLindaIntent()` in `js/chatbot.js` — **no testo messaggio**, solo `msg_hash` + metadati
- Snapshot: `scripts/linda-intents-snapshot.py` → `data/linda-intents-snapshot-latest.json` (richiede `SUPABASE_KEY` service_role in CI)

### Live benchmark

- Query: `data/linda-benchmark-queries.json`
- Script: `scripts/linda-live-benchmark.py` → `data/linda-live-benchmark-latest.json`
- Integrato in quality score (`live_benchmark` weight 15%)

### Knowledge temporale strutturato

- Fonte approvata: `data/linda-knowledge-temporal.json` (`source`, `last_verified`, `review_date`, `status`)
- Solo `status=approved` in FAQ/risposte; `proposals` = YELLOW (no auto-publish)
- Validazione: `scripts/linda-temporal-knowledge.py` → `data/linda-knowledge-temporal-latest.json`

### Ciclo aggiornato

Sub-script in `linda-agent-cycle.py`: discovery → intents_snapshot → question_intelligence → live_benchmark → temporal_knowledge → quality_benchmark → property_index.

Bump `chatbot.js?v=N` dopo modifiche intent logging.
