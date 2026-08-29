# Coda editoriale blog — Righetto Immobiliare

> **Scopo:** redazione digitale — ricerca strategica ( **`skill-editoriale-visivo.md` §8–17** ) + publish del prossimo `scheduled`.
>
> **File dati:** `data/editorial-queue.json` · questo file (processo)
>
> **Aggiornare:** dopo ogni publish, discovery venerdì, input GSC utente.

---

## Sequenza automatica (agente — BLOCCANTE)

```
1. Leggi skill-memoria-progressi.md + skill-editoriale-visivo.md (comando permanente completo)
2. Leggi data/editorial-queue.json + data/gsc-keywords-priority.json
3. python scripts/check_doppioni_sito.py → se KO, STOP
4. Se SOSTENERE urgente (0 click, >100 impr) → refresh, NON nuovo blog
5. Prendi item scheduled (priority min, target_week ≤ oggi+7)
6. FASE RICERCA §15 skill-editoriale-visivo:
   - Scansione 3 aree (mercato / politica impatto / normativa)
   - Verifica fonti primarie (GU, ADE, ISTAT, OMI…)
   - GSC + Google Trends (geo IT/Veneto/Padova)
   - Top 5 contenuti web → gap_analysis + value_add
   - Compila campi coda (Appendice B + §16-TER: substantive_area, main_question, reader_novelty)
6b. CONTINUITÀ §16-TER:
   - python scripts/build_editorial_memory.py
   - Confronta proposta con data/editorial-memory.json (saturazione tematica)
   - Se area già ≥2 negli ultimi 8 → serve update_reason o altro argomento
7. python scripts/audit_editorial_research.py --id {eq-XXX} → OK
7b. python scripts/audit_editorial_continuity.py --id {eq-XXX} → OK
8. Scrivi blog (skill-content + righetto-blog) — MAI copiare testi concorrenti
9. python scripts/audit_blog_visuals.py --file blog-{slug}.html
10. Registra: blog.html, homepage.js, admin, sitemap, llms
11. validate-page.js + build_skimm.py + audit-foto-ai.mjs
12. Aggiorna editorial-queue (published) + gsc-keywords + skill-memoria §Log
```

**Gate pre-scrittura:** `audit_editorial_research.py` + `audit_editorial_continuity.py` (§16-TER)
**Gate pre-chiusura:** `audit_blog_visuals.py` + §17 skill-editoriale-visivo
**Dopo publish:** `build_editorial_memory.py` (aggiorna memoria sostanziale)

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

Seguire **§15–16 skill-editoriale-visivo.md** (7 fasi + ripartizione ~50% trend/evergreen).

1. **GSC** `queries_growth` / `pages_refresh_priority` → candidati + SOSTENERE
2. **Google Trends** — IT, Veneto, Padova; keyword immobiliare correlate
3. **SKIMM** §4 gap cluster → angolo nuovo, intent diverso
4. **Tre aree monitoraggio** (§9): mercato Veneto/Padova · politica con impatto reale · normativa (verifica GU/ADE)
5. **RSS / fonti** (spunto angolo — mai copiare corpo):
   - **ANSA Economia:** `https://www.ansa.it/sito/notizie/economia/economia_rss.xml`
   - **ANSA Veneto:** `https://www.ansa.it/veneto/notizie/veneto_rss.xml`
   - **Sole 24 Ore Economia:** `https://www.ilsole24ore.com/rss/economia.xml`
   - **Milano Finanza** (Google News RSS): `site:milanofinanza.it` + keyword immobili/casa/mutuo
   - **Agenzia delle Entrate:** comunicati RSS ufficiali
   - **Gazzetta Ufficiale:** https://www.gazzettaufficiale.it/
   - Usare titoli come **spunto** — rielaborare con fonti primarie
6. **Top 5 contenuti web** sul tema → `hype_sources_read` + `gap_analysis` + `value_add`
7. **Anti-doppioni:** grep slug + `check_doppioni_sito.py`
8. Aggiungi in `editorial-queue.json`: `status: proposed`, campi Appendice B
9. **Max 1 publish/settimana** — proposte possono accumularsi

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
