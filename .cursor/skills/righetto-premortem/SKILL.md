---
name: righetto-premortem
description: >-
  Gate premortem su tutte le pagine e sfaccettature del sito (perf, SEO, schema,
  lead, mobile, owner funnel) prima di commit/push — output con file/comandi, no
  chiacchere. Trigger Premortem, /premortem. always_load skill-premortem-righetto.md.
---

# Premortem Righetto

## Quando usare

- **Ogni** commit/push che tocca il sito pubblico (§1 skill) — non solo blog/GSC
- Classifica diff → applica solo righe pertinenti di **§4.2 matrice**
- **`Premortem`**, **`/premortem`**, *premortem questo*

## Procedura (BLOCCANTE)

1. **`TEST-SKILL/skill-premortem-righetto.md`** (§3 agente + §4.1–4.2)
2. **`skill-memoria-progressi.md`** §Prossimi passi · **`skill-efficienza-sito.md`** §2 se performance/media/form
3. Esegui comandi del diff (§3 tabella) — citare esito in §7
4. Output §7.1–7.2 (frame hindsight §3.1 — no «piano ok»); gap critici espliciti prima del push

## Prompt utente (copia da skill §2)

Vedi `TEST-SKILL/skill-premortem-righetto.md` §2 — blocco «Premortem Righetto — assume che tra 8 settimane…».

## Collegamenti

- SEO/GSC: `skill-seo.md` §12
- Gate Google: `skill-massimo-punteggio.md` §0
- Venerdì blog: `skill-acquisizione-cron-venerdi.md` — premortem su slot #2 publish
