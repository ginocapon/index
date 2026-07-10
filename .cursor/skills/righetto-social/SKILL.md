---
name: righetto-social
description: >-
  Automazione social Meta, Instagram, Google Business e copy post/storie/reel per
  Righetto Immobiliare. Usa quando l'utente chiede bozze social, cron pubblicazione,
  testo post Instagram/Facebook, agenda righetto_social, rotazione catalogo immobili,
  reel, token Meta, o mirror GBP.
---

# Social Righetto

## Prima di iniziare

1. `TEST-SKILL/skill-essentials.md` (claim, no tariffe online)
2. `TEST-SKILL/skill-social-automation.md` (BLOCCANTE)
3. Sintesi: `TEST-SKILL/SKILL-2.0.md` §10.4

## Copy BLOCCANTE (immobili e blog sito)

| Regola | Dettaglio |
|--------|-----------|
| **Titolo** | Identico al sito (`immobili.titolo` / `blog.titolo`) — no spintax sul titolo |
| **Caption** | Titolo + 2–4 righe + URL HTTPS + ≥10 hashtag |
| **Mediazione** | Mai tariffe o percentuali online |

## Consegna testo in chat (§2b.1)

Sempre **tre blocchi** nell'ordine:
1. **DESCRIZIONE** — spintax `{A|B}`, titolo sito in prima riga
2. **LINK** — URL `righettoimmobiliare.it` su riga dedicata
3. **KEYWORD** — hashtag con `#` (≥8–12)

## Rotazione catalogo

- **3 contenuti diversi/settimana** per sezione (immobile, blog, landing, agenzia)
- Pool immobili: `attivo=true`, non venduto/affittato, ordine codice
- Script: `righetto_social/genera_bozze_settimanali.py`

## Agenda 4 fasce (§2c)

- Orari: 10:00, 13:00, 15:00, 19:00
- 4 imm + 4 blog/giorno; 15 min tra post diversi
- `python programma_oggi_slot.py --ciclo-completo`

## Cron (Windows)

- `config/settings.json` **obbligatorio** (da `settings.example.json`)
- Domenica: `cron_settimanale.bat` (bozze)
- Lun–ven: `cron_pubblica.bat` (Meta + GBP)
- Verifica token: `python verifica_meta.py`

## Sicurezza

- **Mai** committare `righetto_social/.env` o token Meta
- Token PAGE: `estrai_token_pagina.py --scrivi-env`

## Rule Cursor

`.cursor/rules/righetto-social-automation.mdc` su `righetto_social/**`

## Output atteso

Bozze in `bozze_social/`, agenda aggiornata, o testo social in chat (3 blocchi)
