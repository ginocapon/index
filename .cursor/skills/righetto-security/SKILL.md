---
name: righetto-security
description: >-
  Audit sicurezza Righetto Immobiliare: RLS Supabase, admin, segreti, form spam,
  XSS, email relay. Usa quando l'utente chiede revisione sicurezza, hardening,
  check RLS, audit martedì/venerdì, o dopo sospetto attacco/defacement.
---

# Sicurezza Righetto

## Prima di iniziare

1. `TEST-SKILL/skill-essentials.md`
2. `TEST-SKILL/skill-security.md` (checklist completa §3)
3. `TEST-SKILL/skill-context.md` (architettura Supabase)

## Cadenza obbligatoria

| Giorno | Azione |
|--------|--------|
| **Martedì** | Revisione sicurezza completa |
| **Venerdì** | Seconda revisione + confronto issue `security` |

Workflow CI: `.github/workflows/security-check-bisettimanale.yml`

## Script locali (richiede `.env`)

```bash
bash scripts/security-check.sh
python tools/check_rls_exposure.py
python tools/check_live_admin_secret.py
```

## Checklist rapida (§3)

### Segreti
- [ ] Nessun `.env`, token Meta, service_role in git
- [ ] `admin.html`: password via `__RIGHETTO_ADMIN_PW_JSON__` + secret GitHub
- [ ] `RIG_ADMIN_RLS_SECRET` allineato a Supabase

### Supabase / RLS
- [ ] `check_rls_exposure.py` — anon non legge tabelle sensibili
- [ ] `richieste`: solo INSERT anon; `immobili`: solo attivi

### Form / email
- [ ] Edge `send-email`: `send_test` solo verso `info@righettoimmobiliare.it`
- [ ] Nessun `service_role` nel frontend

### Frontend
- [ ] `innerHTML` solo con dati escapati
- [ ] Nessun `eval()` con input utente
- [ ] `robots.txt` → `Disallow: /admin.html`

## Mai committare

- `righetto_social/.env`, password admin in chiaro, API relay production secret

## Rule Cursor

`.cursor/rules/righetto-supabase-admin.mdc`

## Output atteso

Report checklist con ✅/❌, fix nel repo se necessario, issue `security` se bloccanti
