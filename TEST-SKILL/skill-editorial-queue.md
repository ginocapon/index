# Coda editoriale blog — Righetto Immobiliare

> **Scopo:** l'agente **non chiede ogni volta** «che articolo scriviamo?». Legge la coda, pubblica il prossimo `scheduled`, rifornisce proposte con ricerca web + GSC.
>
> **File dati:** `data/editorial-queue.json` (macchina) · questo file (processo umano/agente)
>
> **Aggiornare:** dopo ogni publish, dopo discovery venerdì, dopo input screenshot GSC utente.

---

## Sequenza automatica (agente — BLOCCANTE)

```
1. Leggi skill-memoria-progressi.md §Stato + §Prossimi passi
2. Leggi data/editorial-queue.json
3. Leggi data/gsc-keywords-priority.json → pages_refresh_priority (SOSTENERE prima?)
4. python scripts/check_doppioni_sito.py  → se KO, STOP
5. Se SOSTENERE urgente (0 click, >100 impr, no refresh 14 gg) → refresh, NON nuovo blog
6. Altrimenti: prendi item scheduled con priority minima e target_week ≤ oggi+7
7. Web search: 3–5 articoli hype sul tema → rielabora (MAI copiare)
8. Scrivi blog (skill-content + righetto-blog SKILL)
9. Registra: blog.html, homepage.js, admin, sitemap, llms, ai.json
10. validate-page.js + build_skimm.py + google-compliance-check.py
11. Aggiorna editorial-queue (status=published) + gsc-keywords published_this_week + skill-memoria §Log
12. Commit se utente chiede commit/push (default: commit a fine task blog se richiesto esplicitamente)
```

---

## Trigger — quando eseguire senza che l'utente ripeta

| Trigger | Azione agente |
|---------|----------------|
| Utente scrive **`"SKILL"`** (virgolette, tip. venerdì) | Piano giornata: `skill-competitor-roadmap-q3-2026.md` §8 + memoria + coda + GSC JSON |
| Utente dice «pubblica blog» / «prossimo articolo» / venerdì + modifica repo | Esegui sequenza § sopra |
| Utente manda screenshot GSC sera | Salva in `gsc-keywords-priority.json` + `gsc-captures/` — **non** pubblicare blog quella sera |
| Cron venerdì 07:00 | Email automatica — **non** pubblica blog (solo audit) |
| Coda `scheduled` < 3 item | **Discovery:** 2–3 proposte nuove da GSC + web → status `proposed` |
| Utente chiede «cosa fare questa settimana» | `/venerdi` + prossimo item da coda + checklist GSC |

---

## Discovery nuovi temi (ogni settimana o coda bassa)

1. **GSC** `queries_growth` con impr > 10 e clic = 0 → candidato
2. **SKIMM** §4 avvisi cluster → nuovo angolo, non duplicare slug esistente
3. **Web search** (IT, 2026): `affitti padova`, `mutuo giovani`, `mercato immobiliare veneto` + fonte istituzionale
4. **Anti-doppioni:** grep slug + `check_doppioni_sito.py` + intent diverso da articolo esistente
5. Aggiungi in `editorial-queue.json` con `status: "proposed"`, `research_refs`, `different_from`
6. **Max 1 publish/settimana** — proposte possono accumularsi

---

## Stati coda

| status | Significato |
|--------|-------------|
| `proposed` | Idea validata, non ancora in calendario |
| `scheduled` | Data target settimana, pronto a pubblicare |
| `published` | Live — slug in sitemap |
| `cancelled` | Doppione o GSC non conferma — motivo in `notes` |
| `sostenere_instead` | Meglio refresh pagina esistente |

---

## Coda attuale (snapshot 24/07/2026)

| Settimana | Slug | KW | Stato |
|-----------|------|-----|-------|
| 17/07 ✅ | blog-mandato-esclusivo-padova-perche-conviene-2026 | mandato esclusivo padova | published |
| 24/07 ⏳ | blog-agenzia-immobiliare-limena-come-scegliere-2026 | agenzia immobiliare limena | **scheduled — non ancora pubblicato** |
| 31/07 | blog-caro-affitti-padova-under-35-guida-2026 | caro affitti padova giovani | scheduled |
| 07/08 | blog-coliving-padova-limena-giovani-professionisti-2026 | coliving padova limena | scheduled |
| 14/08 | blog-prima-casa-under-36-consap-padova-2026 | prima casa under 36 consap | scheduled |

Dettaglio completo: `data/editorial-queue.json`

---

## Automazioni GitHub (verificate 17/07/2026)

| Ora CEST | Workflow | Pubblica blog? |
|----------|----------|----------------|
| 07:00 | `venerdi-contenuti-freschezza.yml` | ❌ audit + email PDF |
| 07:00 | `audit-settimanale.yml` | ❌ Issue audit |
| 07:00 | `mini-seo-check.yml` | ❌ Issue SEO |
| ~07:30 | `venerdi-righetto-piano.yml` | ❌ Issue macrociclo |
| ogni 6h | `sync-media-github.yml` | ❌ foto immobili |

**Blog publish = agente** seguendo questa skill (non c'è Action che scrive HTML — per design).

---

## Input utente ricorrente (minimal)

- **Giovedì sera:** screenshot GSC Prestazioni 28 gg → agente salva JSON
- **Venerdì opzionale:** screenshot Indicizzazione → `gsc-indexing-weekly.json`
- **Resto:** agente autonomo da coda + discovery

---

## Collegamenti

- `TEST-SKILL/skill-content.md` §2.0 anti-doppioni
- `TEST-SKILL/skill-memoria-progressi.md`
- `.cursor/skills/righetto-blog/SKILL.md`
- `.cursor/skills/righetto-venerdi-sito-90giorni/SKILL.md`
