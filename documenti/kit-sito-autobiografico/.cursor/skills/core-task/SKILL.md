---
name: core-task
description: >-
  Task generico sul sito autobiografico (persona + palestra + blog).
  Carica essentials e gate Google. Usa per modifiche pagine, fix, contenuti
  quando non serve skill più specifica (/blog, /seo, /chi-sono).
---

# Task generico sito

## Prima di iniziare
1. `TEST-SKILL/skill-essentials.md`
2. `TEST-SKILL/skill-massimo-punteggio.md`
3. `TEST-SKILL/context-map.json` → moduli del task

## Regole non negoziabili
- Mobile-first + WCAG
- CSS/JS `?v=N`
- Dati veri — no inventare biografia
- sitemap.xml se nuova URL
- Commit/push solo se richiesto

## Routing skill
| Task | Command |
|------|---------|
| SEO / GSC | `/seo` |
| Blog | `/blog` |
| Mobile | `/mobile` |
| Venerdì Google | `/venerdi` |
| Chi sono / storia | `/chi-sono` |
