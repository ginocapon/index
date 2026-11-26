# Sync documenti: gestionale legacy → Righetto (Supabase)

Migra **allegati clienti** e **allegati immobili** dal pannello legacy verso la struttura già usata in `admin.html`:

| Origine (legacy) | Destinazione (nuovo) |
|------------------|----------------------|
| Documenti scheda cliente | `clienti.documenti_cliente[]` + bucket Storage `documenti` |
| Documenti immobile | `immobili.documenti[]` + bucket `documenti` |
| Planimetrie immobile | `immobili.planimetrie[]` + bucket `planimetrie` |

**Nessuna password nel repository né in chat.** Solo **Environment secrets** (Cursor Cloud Agent) o file `.env` locale (non committato).

---

## 1. Segreti ambiente (Cursor → Environment → Secrets)

### Obbligatori

| Nome | Contenuto |
|------|-----------|
| `SUPABASE_URL` | URL progetto Supabase |
| `SUPABASE_SERVICE_ROLE_KEY` | Chiave **service_role** (Dashboard → Settings → API) |

### Accesso pannello — scegli **A** (consigliato) **oppure** **B**

**A – Sessione salvata (consigliato)**  
1. Sul PC: `pip install -r tools/sync_gestionale_documenti/requirements.txt && playwright install chromium`  
2. `python tools/sync_gestionale_documenti/login_save_session.py` → login + 2FA nel browser → genera `storageState.json`  
3. Copia **tutto** il JSON in un unico secret: `GESTIONALE_STORAGE_STATE`  

**B – Password + TOTP** (solo se non usi A)  

| Nome | Contenuto |
|------|-----------|
| `GESTIONALE_USER` | Username pannello |
| `GESTIONALE_PASSWORD` | Password |
| `GESTIONALE_TOTP_SECRET` | Seed base32 dell’authenticator (**non** il codice a 6 cifre) |

Serve **A oppure** (B con tutti e tre i campi).

### Opzionali

| Nome | Default |
|------|---------|
| `GESTIONALE_BASE_URL` | `https://pannello.gestionaleimmobiliare.it` |
| `SYNC_DRY_RUN` | `1` = solo log, nessun upload |

Quando i secret sono salvati, scrivi in chat: **segreti pronti**.

---

## 2. Configurazione URL (prima esecuzione reale)

Copia `config.example.json` → `config.local.json` (gitignored) e adatta i path alle pagine allegati del pannello (stesso layout del vecchio gestionale).

Dopo la prima prova con `--probe-cliente LEGACY_ID` aggiorniamo i selettori CSS se serve.

---

## 3. Comandi

```bash
cd /path/to/repo
export $(grep -v '^#' .env.local 2>/dev/null | xargs)  # oppure solo secrets Cursor

# Verifica credenziali Supabase + sessione gestionale
python tools/sync_gestionale_documenti/sync.py --check

# Solo elenco clienti/immobili mappabili (nessun download)
python tools/sync_gestionale_documenti/sync.py --list

# Prova su un cliente legacy (salva HTML di debug in /tmp)
python tools/sync_gestionale_documenti/sync.py --probe-cliente 12345

# Sync batch (rispetta SYNC_DRY_RUN)
python tools/sync_gestionale_documenti/sync.py --clienti --limit 50
python tools/sync_gestionale_documenti/sync.py --immobili --limit 50
python tools/sync_gestionale_documenti/sync.py --all --limit 20
```

Log append in `tools/sync_gestionale_documenti/.sync-log.jsonl` (gitignored).

---

## 4. Regole di sicurezza

- A fine migrazione: **ruota password** gestionale e **rimuovi** i secret dall’ambiente.
- Non committare `storageState.json`, `.env.local`, `config.local.json`.
- Pubblicazione massiva su Supabase solo dopo **ok esplicito di Gino** (regola progetto).
