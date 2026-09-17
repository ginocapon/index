# Cron acquisizione proprietari — integrazione automatica ogni venerdì

> **Aggiornato:** 14 settembre 2026  
> **Stato machine-readable:** `data/acquisition-roadmap-cron.json`  
> **Strategia:** `skill-acquisizione-proprietari.md` · **Playbook:** `skill-acquisizione-playbook-commerciale.md`

---

## Scopo

Ogni **venerdì**, quando l'utente dà l'ordine abituale (`"SKILL"`, `/venerdi`, «piano venerdì», «cosa fare questa settimana»), l'agente **implementa automaticamente 1 task** del ciclo acquisizione proprietari (12 settimane), **in parallelo** al rituale GSC/blog già esistente.

**Non sostituisce** il macrociclo 12 settimane SEO in `righetto-venerdi-sito-90giorni` — **si affianca**: repo task #1 = acquisizione; task #2–3 = SOSTENERE / blog coda / GSC fix.

---

## Trigger (BLOCCANTE il venerdì)

| Input utente | Azione agente |
|--------------|---------------|
| `"SKILL"` (virgolette) | Piano venerdì + **esegui task acquisizione settimana corrente** |
| `/venerdi` | Idem |
| «piano venerdì» / «cosa fare questa settimana» (venerdì) | Idem |
| «venerdì Righetto» | Idem |

**Prima del 2026-09-19:** **non eseguire** task repo acquisizione — solo mostrare preview sett. 1 e attendere anchor (richiesta utente 14/09/2026).

**Fuori venerdì (dal 19/09):** se l'utente chiede esplicitamente «continua cron acquisizione» → eseguire prima settimana `pending`.

---

## Procedura agente (ogni venerdì)

1. Leggere **`data/acquisition-roadmap-cron.json`**
2. Calcolare settimana corrente:
   ```
   anchor = 2026-09-19
   N = floor((oggi - anchor).days / 7) + 1
   clamp N tra 1 e 12
   ```
3. Selezionare task:
   - Preferire settimana **N** se `status: pending`
   - Se settimana N è `done`, prendere la **prima pending** con week ≥ N, altrimenti la prima pending del ciclo
4. **Eseguire** il task nel repo (commit + push)
5. Aggiornare JSON: `status: done`, `completed_date: oggi`, `notes` breve
6. Log in **`skill-memoria-progressi.md`** (riga acquisizione cron)
7. Output utente nel formato § Output combinato (sotto)

**Regole:**
- **Max 1 task acquisizione** per venerdì
- **Anti-duplicato** — § skill-acquisizione-proprietari
- **Mai** percentuali mediazione online
- Se task richiede articolo ma c'è doppione → **refresh** pagina esistente e marcare done con nota

---

## Calendario 12 settimane

| Sett. | Fase | ID | Cosa fa l'agente automaticamente |
|------:|------|-----|----------------------------------|
| 1 | 🔥 | acq-w01 | `landing-valutazione`: educazione post-Linda + CTA sopralluogo |
| 2 | 🔥 | acq-w02 | `proprietario-immobile`: card percorsi F, H, J |
| 3 | 🔥 | acq-w03 | CTA owner su 5 blog top GSC (batch 1) |
| 4 | 🔥 | acq-w04 | Lead scoring admin + promemoria KPI venerdì |
| 5 | 🟠 | acq-w05 | Articolo owner percorso F (casa invenduta) o refresh |
| 6 | 🟠 | acq-w06 | Articolo/ampliamento percorso J (ristrutturare) |
| 7 | 🟠 | acq-w07 | Mesh link hub ↔ servizi ↔ blog (A–L) |
| 8 | 🟠 | acq-w08 | `servizio-vendita` conversione owner + link interni |
| 9 | 🟠 | acq-w09 | CTA owner batch 2 (5 blog) |
| 10 | 🟢 | acq-w10 | `landing-consulenza` per percorsi indecisi |
| 11 | 🟢 | acq-w11 | FAQ/chatbot routing owner |
| 12 | 🟢 | acq-w12 | Review KPI + audit acquisizione trimestrale |

Dettaglio file/validate per ogni settimana: **`data/acquisition-roadmap-cron.json`**.

**Dopo sett. 12:** review — riaprire solo voci non completate o nuovo ciclo concordato con utente.

---

## Output combinato venerdì (formato obbligatorio)

Integrare nel template `"SKILL"` / venerdì esistente:

```markdown
## Venerdì Righetto — [data]

### Acquisizione proprietari — Settimana [N]/12
- **Task cron:** [title] (`[id]`)
- **Stato:** [pending → done oggi | già completato]
- **Percorsi A–L:** [lista]
- **Commit:** [hash o «in corso»]

### Tu oggi (~15 min GSC + GBP)
- [ ] … (da skill venerdì / gsc-indexing-weekly next_friday_batch)

### Repo oggi (agente)
1. **[ACQUISIZIONE]** — task sett. [N] (automatico)
2. **[SOSTENERE | BLOG | FIX]** — …
3. …

### KPI acquisizione (compilazione manuale opzionale)
- Template: `data/acquisition-kpi-template.json`

### Un solo focus se poco tempo
- Task acquisizione sett. [N] (priorità assoluta strategia)

### Lunedì follow-up
- [ ] GSC batch · [ ] Lead giorno 0 (playbook)
```

---

## Cosa resta manuale (non cron agente)

| Attività | Frequenza | Riferimento |
|----------|-----------|-------------|
| Risposta lead giorno 0 | Ogni lead | playbook § Follow-up |
| GSC ispezione URL | Venerdì | skill-seo §10 |
| GBP post/recensione | Venerdì | skill venerdì |
| Compilazione KPI commerciali | Venerdì | acquisition-kpi-template.json |
| Campagne Ads | Dopo sett. 8+ | playbook § Canali |

---

## Collegamenti

- Trigger venerdì: `.cursor/skills/righetto-venerdi-sito-90giorni/SKILL.md`
- §8 piano `"SKILL"`: `skill-competitor-roadmap-q3-2026.md`
- Strategia: `skill-acquisizione-proprietari.md`
- Cursor: `.cursor/skills/righetto-acquisizione-proprietari/SKILL.md`
