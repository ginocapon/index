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
3. Agent: `--check`, probe un cliente, aggiorna config, batch con dry-run poi ok per produzione.
