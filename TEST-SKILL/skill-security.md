# SKILL-SECURITY — Righetto Immobiliare
> Revisione sicurezza generale contro attacchi comuni (defacement, furto dati, spam, abuso API).
> **Carica questo file** per audit sicurezza, hardening Supabase/admin, o dopo incidenti sospetti.

---

## 1. CADENZA OBBLIGATORIA — 2 VOLTE A SETTIMANA

| Giorno | Orario consigliato | Azione |
|--------|-------------------|--------|
| **Martedì** | mattina (es. 08:00 CET) | Revisione sicurezza completa (checklist §3) |
| **Venerdì** | dopo audit SEO (07:00+) | Seconda revisione + confronto con issue `security` |

**Chi esegue:** agente Cursor/Claude su richiesta («revisione sicurezza») oppure maintainer manuale.

**Automazione GitHub (statica):** `.github/workflows/security-check-bisettimanale.yml` — martedì e venerdì 06:00 UTC → issue label `security`.

**Automazione locale (dinamica, richiede `.env`):**
```bash
bash scripts/security-check.sh
python tools/check_rls_exposure.py
python tools/check_live_admin_secret.py   # opzionale: allineamento segreto admin
```

---

## 2. PERIMETRO DEL SITO

| Superficie | File / servizio | Rischio tipico |
|------------|-----------------|----------------|
| Sito pubblico | `*.html`, `js/*.js` | XSS, open redirect, leak chiavi client |
| Admin | `admin.html` | Brute force, session hijack, RLS bypass |
| Supabase | RLS, Edge Functions | Data leak anon, spam email |
| Email relay | `api/send-mail.php`, Edge `send-email` | Relay spam, API key abuse |
| Social worker | `righetto_social/.env` | Token Meta/GBP leak |
| CI/CD | GitHub Actions secrets | Password admin in build |

**Contatto disclosure:** `.well-known/security.txt` → `info@righettoimmobiliare.it`

---

## 3. CHECKLIST REVISIONE (2×/settimana)

### A. Segreti e repository
- [ ] `git status` — nessun `.env`, `credentials.json`, token Meta committati
- [ ] `bash scripts/security-check.sh` — zero errori bloccanti
- [ ] `admin.html`: password admin **non** in chiaro nel repo (preferire `__RIGHETTO_ADMIN_PW_JSON__` + secret GitHub `ADMIN_PASSWORD`)
- [ ] `RIG_ADMIN_RLS_SECRET` in `admin.html` allineato a `righetto_admin_secret()` in Supabase (`sql/rls-security-hardening.sql`)
- [ ] `api/send-mail.php`: `API_SECRET` ruotata e **solo** su cPanel (non valore di default in repo se deployato)
- [ ] `righetto_social/.env` solo locale; `.env.example` senza valori reali

### B. Supabase / RLS
- [ ] `python tools/check_rls_exposure.py` — tabelle sensibili **non** leggibili con chiave `anon`
- [ ] Policy attive: `immobili` (solo attivi), `blog` (solo pubblicato), `richieste` (solo INSERT anon)
- [ ] Tabelle marketing (`campagne_email`, `smtp_config`, `clienti`, …) **senza** policy «Allow all for anon»
- [ ] Nessun `service_role` nel frontend o in file tracciati da git

### C. Form, email, spam
- [ ] Edge `send-email`: `send_test` accetta solo destinatario fisso `info@righettoimmobiliare.it` (non email arbitraria da body)
- [ ] Form lead: honeypot / validazione base; insert `richieste` senza campi HTML non sanitizzati in admin
- [ ] Rate limit relay PHP / Edge (max_per_ora in `smtp_config`)

### D. Admin e accesso
- [ ] `robots.txt` contiene `Disallow: /admin.html`
- [ ] `admin.html` con `noindex` (meta robots)
- [ ] 2FA TOTP attivo per sessioni admin (`rig_2fa_secret` in localStorage — consapevolezza XSS)
- [ ] Tentativi login falliti non rivelano se utente esiste

### E. Frontend / attacchi comuni
- [ ] Nessun `eval()`, `document.write` con input utente
- [ ] `innerHTML` solo con dati escapati (`escProp` / `escAttr`) su titoli blog, immobili, chat
- [ ] YouTube iframe solo da URL fissi o slug controllati (no URL da querystring utente)
- [ ] Nessuna chiave `service_role` in `js/config.js`, `homepage.js`, `chatbot.js`

### F. Infrastruttura
- [ ] `security.txt` presente e `Expires` futuro
- [ ] Dipendenze CDN: solo Supabase client (già in uso) — monitorare supply-chain
- [ ] GitHub: branch `main` protetto; secret scan attivo
- [ ] Backup Supabase / export periodico immobili+lead (policy disaster recovery)

### G. Post-incidente (se sospetto attacco)
- [ ] Ruotare: password admin, `RIG_ADMIN_RLS_SECRET`, `API_SECRET` PHP, token Meta, service_role Supabase
- [ ] Revisione log Supabase + email relay per volumi anomali
- [ ] Verificare immobili/blog non alterati (contenuti, link esterni)
- [ ] Documentare in issue GitHub label `security-incident`

---

## 4. AUDIT DEL 27 MAGGIO 2026 — ESITO

| Livello | Rilevazione | Stato | Remediation |
|---------|-------------|-------|-------------|
| 🔴 Critico | `ADMIN_PASSWORD` in chiaro in `admin.html` (repo pubblico GitHub) | **Risolto** | Placeholder `__RIGHETTO_ADMIN_PW_JSON__` + secret GitHub `ADMIN_PASSWORD` |
| 🔴 Critico | `API_SECRET` default in `api/send-mail.php` nel repo | **Aperto** | Ruotare su cPanel; non committare valore produzione |
| 🟠 Alto | `RIG_ADMIN_RLS_SECRET` nel client admin (chiunque legge il sorgente) | **Mitigato** | Necessario per RLS header; ruotare periodicamente; preferire RPC admin (`rig-admin-rpc-immobili.sql`) |
| 🟠 Alto | Edge `send_test` invocabile con anon key; body può teorizzare destinatario custom | **Risolto** | `send_test` pubblico → solo `info@righettoimmobiliare.it`; admin con header `x-righetto-admin` + secret Edge `RIG_ADMIN_RLS_SECRET` |
| 🟡 Medio | Chiave Supabase `anon` in molti JS (normale) | **OK se RLS** | Eseguire `check_rls_exposure.py` ogni revisione |
| 🟡 Medio | CORS `*` su `send-mail.php` | **Risolto** | CORS limitato a domini Righetto |
| 🟢 OK | `robots.txt` blocca `/admin.html` | OK | — |
| 🟢 OK | `sql/rls-security-hardening.sql` documentato | OK | Verificare applicato in progetto live |
| 🟢 OK | `.gitignore` esclude `.env` | OK | — |
| 🟢 OK | `.well-known/security.txt` | OK | Rinnovare `Expires` annualmente |

---

## 5. HARDENING PRIORITARIO (backlog)

1. ~~**Password admin fuori dal repo**~~ — fatto: verificare secret `ADMIN_PASSWORD` in GitHub Actions.
2. ~~**Edge `sendTestEmail`**~~ — fatto: deploy Edge + secret Supabase `RIG_ADMIN_RLS_SECRET` = valore in `admin.html`.
3. **RLS live** — rieseguire `sql/rls-security-hardening.sql` se mail Supabase segnala «publicly accessible».
4. **Deploy Edge `send-email`** dopo modifica sicurezza: `supabase secrets set RIG_ADMIN_RLS_SECRET=<stesso valore di admin.html>` poi `supabase functions deploy send-email`.
5. **GitHub** — secret `ADMIN_PASSWORD` obbligatorio (workflow `static.yml` inietta in `admin.html`).
4. **CSP header** — valutare Content-Security-Policy su GitHub Pages (via meta o proxy futuro).
5. **WAF** — non bloccare Google-Agent / bot AI legittimi (vedi SKILL-2.0 §1.1b).

---

## 6. COSA NON COMMITTARE MAI

- `righetto_social/.env`, token Meta, `SUPABASE_KEY` service_role
- Password admin in chiaro
- API relay production secret
- Output di `check_live_admin_secret.py` con segreti
- Chiavi private 2FA seed

---

## 7. RIFERIMENTI

- `sql/rls-security-hardening.sql`, `sql/rls-security-hardening-safe.sql`
- `tools/check_rls_exposure.py`, `tools/check_live_admin_secret.py`
- `scripts/security-check.sh`
- `.github/workflows/security-check-bisettimanale.yml`
- `TEST-SKILL/skill-forms-leads.md` (flusso email)
- `TEST-SKILL/skill-context.md` (architettura Supabase)
