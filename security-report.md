# Security Check — Righetto Immobiliare
**Data:** 2026-07-08 (audit manuale agente + script RLS)
**Skill:** TEST-SKILL/skill-security.md

## 1. Segreti nel repository

  ✅ `righetto_social/.env` non tracciato da git
  ✅ `admin.html` usa placeholder `__RIGHETTO_ADMIN_PW_JSON__` (password iniettata in CI da secret `ADMIN_PASSWORD`)
  ✅ Nessuna `ADMIN_PASSWORD` letterale nel repo
  ✅ Nessun `service_role` in file JS frontend tracciati
  ⚠️ `API_SECRET` di default (`RighettoMail2026!SecretKey`) in `api/send-mail.php` — ruotare su cPanel produzione
  ⚠️ Stesso fallback in `supabase/functions/send-email/index.ts` (`MAIL_RELAY_KEY`) — allineare secret Supabase

## 2. Superficie admin

  ✅ `robots.txt` contiene `Disallow: /admin.html`
  ✅ `admin.html` — aggiunto `<meta name="robots" content="noindex, nofollow">` (2026-07-08)
  ✅ Rimosso script `supabase-bridge.js` duplicato in `<head>`
  ⚠️ `RIG_ADMIN_RLS_SECRET` visibile nel sorgente client (necessario per header RLS admin) — ruotare periodicamente su Supabase + `admin.html`
  ℹ️ 2FA TOTP presente; segreto in `localStorage` (rischio XSS — consapevolezza skill §3.D)

## 3. Supabase / RLS (`python tools/check_rls_exposure.py`)

  ✅ Nessuna tabella sensibile leggibile con chiave `anon`
  ✅ `richieste`, `clienti`, `smtp_config`, `pianificazioni`, `bozze_social`, `newsletter_subscribers` — bloccate o vuote per anon
  ℹ️ `campagne_email` — HTTP 404 (tabella assente o rinominata): nessun leak

## 4. Email relay / spam

  ✅ Edge `send_test` (pubblico): destinatario forzato a `info@righettoimmobiliare.it` se non admin
  ✅ CORS `send-mail.php` limitato a domini Righetto
  ⚠️ Chiave relay prevedibile nel repo — priorità rotazione

## 5. Frontend

  ✅ Nessun `eval()` nei sorgenti HTML/JS principali
  ✅ Chiave Supabase `anon` in `js/config.js`, `blog.html`, `immobili.html` (normale con RLS attivo)
  ⚠️ `admin.html` carica `otpauth` da CDN jsDelivr (supply-chain; solo area admin)

## 6. Documentazione

  ✅ `.well-known/security.txt` presente — `Expires: 2027-03-16`
  ✅ `sql/rls-security-hardening.sql` presente
  ✅ `TEST-SKILL/skill-security.md` presente

## 7. Azioni manuali richieste (non automatizzabili da repo)

1. **Ruotare `API_SECRET`** su cPanel `api.righettoimmobiliare.it/send-mail.php` e aggiornare secret Supabase `MAIL_RELAY_KEY`
2. **Verificare secret GitHub** `ADMIN_PASSWORD` attivo nel workflow `static.yml` (deploy Pages)
3. **Allineare** `RIG_ADMIN_RLS_SECRET` in `admin.html` con `righetto_admin_secret()` in Supabase se mail di warning
4. ~~**Opzionale:** honeypot su form lead~~ — **fatto** (`rig-lead-form.js`: campo nascosto `rig_website_url`, risposta finta se compilato)

---
**Riepilogo:** ✅ 14 · ⚠️ 5 · ❌ 0

**Giudizio sintetico:** **BUONO (B+)** — nessun blocco critico aperto nel repo; password admin **non** in chiaro. Priorità: rotazione chiave email relay e monitoraggio segreto admin RLS.
