---
name: righetto-linda
description: >-
  Linda collega virtuale Righetto: base di conoscenza approvata (KB), pannello admin-kb,
  domande reali, lacune, dati live annunci, costi e privacy. Usa quando l'utente parla di
  chatbot Linda, risposte del chatbot, FAQ, addestramento, base di conoscenza, "collega virtuale",
  domande senza risposta o aggiornamento delle risposte.
---

# Linda — collega virtuale

## Prima di iniziare
1. `TEST-SKILL/skill-linda-collega-virtuale.md` (fonte di verità di questo modulo)
2. `TEST-SKILL/skill-essentials.md`, `TEST-SKILL/skill-security.md`, `TEST-SKILL/skill-ai-act-compliance.md`

## Regole non negoziabili
- Linda risponde **solo** con testo approvato o dati live di scheda; altrimenti dice di non sapere.
- Mai dati dei proprietari; query annunci con colonne esplicite.
- Niente tariffe/percentuali di mediazione; numeri solo con fonte.
- Ramo separato + test Playwright (`linda-kb`, `admin-kb`) + anteprima estetica prima di qualsiasi push.
- Nessun LLM/costo ricorrente senza preventivo approvato (§6 della skill).

## Comandi
- Test: `npx playwright test -c tests/e2e/playwright.config.js linda-kb admin-kb`
- Seed FAQ: `node scripts/linda_esporta_faq.js`
- Domande ipotetiche + lacune annunci: `python scripts/linda_genera_domande.py`
