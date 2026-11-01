# Intervento 2026-11-01 — Tool sync documenti gestionale

## Motivo
Completare migrazione allegati **clienti** e **immobili** dal pannello legacy verso Supabase, con accesso via **Environment secrets** (no password in chat/repo).

## File aggiunti
- `tools/sync_gestionale_documenti/` — README, `sync.py`, auth Playwright, upload Supabase

## Backup
Branch `cursor/gestionale-docs-sync-secrets-0d17` prima di merge su main.

## Verifiche
- `python3 -m py_compile tools/sync_gestionale_documenti/*.py` (sintassi)
- Esecuzione reale: **non eseguita** — in attesa secret ambiente + ok Gino; default `SYNC_DRY_RUN=1`

## Limiti
- URL pagine allegati in `config.example.json` sono **placeholder**: dopo `--probe-cliente` vanno allineati ai path reali del pannello.
- Upload massivo su Supabase solo dopo approvazione esplicita.

## Seguito
1. Gino configura Environment secrets (vedi README tool).
2. Scrive in chat: **segreti pronti**.
3. Agent: `--check`, `compare_report.py`, sync batch clienti, poi immobili (mappa `immobile_id` → codice LA).

## Stato 01/11/2026 sera (Europe/Rome)
- Login legacy OK; sessione in `storageState.json` locale (non in repo).
- API allegati allineata: `cliente_details` / `immobile_details` + `get_allegati_array` (misc/image) + cloud.
- Download file: `Referer` pannello obbligatorio su `media.gestionaleimmobiliare.it`.
- Report campione: `tools/sync_gestionale_documenti/reports/compare-*.json` (25 clienti prima pagina = spesso 0 file; immobili in lista normale ≈ tutti con allegati).
- Esempio verificato: cliente legacy **1490191** → **8 PDF** scaricabili.
- **Blocco upload:** mancano `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` in Environment secrets.
- **Da fare:** sync massivo clienti con legacy_id in note; mappa immobili legacy_id → `immobili.codice`; incrocio indice `client-attachments-v1` (GitHub ottobre).
