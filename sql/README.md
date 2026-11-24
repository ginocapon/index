# SQL Righetto — come applicare

Gli script in questa cartella sono **versionati su GitHub** ma vanno **eseguiti manualmente** nel progetto Supabase:

**Dashboard → SQL Editor → New query → incolla il file → Run**

Non esiste (al momento) pipeline CI che applichi automaticamente le migration al database live.

## P0 sicurezza 24/11/2026 (priorità)

Dopo merge del PR P0, eseguire **una volta** sul progetto live:

1. **`p0-security-2026-11-24.sql`** — RLS WhatsApp + REVOKE RPC admin da `anon`  
2. Istruzioni italiane e test: **`docs/p0-security-2026-11-24.md`**

> Non usare più `security-advisor-function-grants-2026.sql` così com’è: concedeva ancora `EXECUTE` a `anon` su RPC admin. Il file P0 lo sostituisce per quel pezzo.

## Ordine consigliato (nuovo progetto)

1. `rls-security-hardening-safe.sql` — base RLS + tabelle agenda/cache se mancano  
2. `rig-admin-rpc-immobili.sql` — RPC admin immobili (opzionale)  
3. `clienti-ruolo-rubrica.sql` — colonna rubrica Cliente/Proprietario  
4. **`security-advisor-splinter-2026-public.sql`** — CLI o SQL Editor (search_path + RLS)  
5. **`security-advisor-splinter-2026-storage.sql`** — policy bucket (**CLI** `supabase db query -f … --linked`, **non** SQL Editor → errore 42501)  
6. **`security-advisor-splinter-2026-storage-buckets-only.sql`** — solo se serve: SQL Editor, rende privati `documenti` / `planimetrie`  
7. **`p0-security-2026-11-24.sql`** — RLS WhatsApp + revoke anon su RPC admin (sostituisce il vecchio grants-2026 per le RPC admin)

## Security Advisor (2026)

File: **`security-advisor-splinter-2026.sql`**

| Avviso Supabase | Cosa fa lo script |
|-----------------|-------------------|
| Function search_path mutable | `SET search_path` su funzioni admin/trigger |
| RLS policy always true | Policy form con validazione email/campi (non `true`) |
| Public bucket allows listing | `documenti` / `planimetrie` privati + policy solo admin; `foto-immobili` policy più strette |

**Dopo l’esecuzione:** Advisors → Security → **Rerun linter**  
**Test locale:** `python tools/check_rls_exposure.py` + invio form contatti/newsletter

### Attenzione storage privato

Dopo lo script, i bucket **`documenti`** e **`planimetrie`** non sono più pubblici. L’admin carica ancora con header `x-righetto-admin`, ma i link `getPublicUrl()` salvati in passato **non sono più accessibili anonimamente** (comportamento desiderato per PDF riservati). Se serve anteprima in admin, step successivo: `createSignedUrl()` in `admin.html`.

### foto-immobili

Resta un bucket **public** per URL legacy (blog, staging prima del sync su GitHub Pages). Il linter può segnalare ancora il listing finché il bucket è public; mitigazione definitiva: bucket privato + solo `img/immobili/` sul sito (vedi `skill-media-migration.md`).

## Altri script

| File | Uso |
|------|-----|
| `rls-security-hardening.sql` | Versione “completa” (fallisce se mancano tabelle) |
| `rls-drop-legacy-policies.sql` | Pulizia policy vecchie |
| `linda-learning-bridge.sql` | Tabelle LINDA (poi esegui splinter-2026 per policy) |
