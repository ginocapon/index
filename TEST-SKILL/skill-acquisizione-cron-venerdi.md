# Cron venerdì — acquisizione + blog owner + social proprietari

> **Aggiornato:** 22 settembre 2026  
> **Pipeline unificata:** `data/venerdi-friday-pipeline.json`  
> **Task repo acquisizione:** `data/acquisition-roadmap-cron.json`  
> **Messaggio madre:** chi vende trova in Righetto **un alleato**  
> **Skill:** `skill-acquisizione-proprietari.md` · `skill-real-estate-advisor.md` · **`skill-acquisizione-contenuti-acquisizione.md`** (articoli + post foto) · `skill-editoriale-visivo.md` · `skill-social-automation.md`  
> **Playbook telefono/email:** `skill-acquisizione-playbook-commerciale.md`

---

## Scopo

Ogni **venerdì** (`"SKILL"`, `/venerdi`, «piano venerdì») l'agente esegue **fino a 3 slot repo** in ordine fisso, oltre a GSC/GBP utente:

| Slot | Contenuto | Max/settimana |
|------|-----------|---------------|
| **#1** | Task cron acquisizione (12 sett.) | 1 obbligatorio |
| **#2** | Blog owner (specifiche settimana N) o coda `scheduled` | 1 se previsto |
| **#3** | Post social proprietari (testo + brief foto/carosello) | 1 consigliato |

Il macrociclo SEO 12 sett. (`righetto-venerdi-sito-90giorni`) resta attivo: se settimana macrociclo = **3 (Blog)** e slot #2 non ha publish dedicato → applicare `macrociclo_seo_blog_fallback` in pipeline JSON.

---

## Trigger (BLOCCANTE il venerdì)

| Input utente | Azione agente |
|--------------|---------------|
| `"SKILL"` (virgolette) | Piano venerdì + esegui slot #1–#3 secondo pipeline |
| `/venerdi` | Idem |
| «piano venerdì» / «cosa fare questa settimana» | Idem |

**Anchor acquisizione:** `2026-09-19` — prima di questa data solo preview.  
**Settimana N:** `floor((oggi - anchor).days / 7) + 1`, clamp 1–12.

---

## Procedura agente (ogni venerdì) — ordine obbligatorio

### Fase 0 — Lettura (5 min)

1. `data/venerdi-friday-pipeline.json` → `weeks_aligned_acquisition[N-1]`
2. `data/acquisition-roadmap-cron.json` → task sett. N
3. `data/editorial-queue.json` + `data/editorial-acquisition-balance.json`
4. `data/advisor-territorio-limena-10km.json` se blog/social locali
5. `TEST-SKILL/skill-memoria-progressi.md` §Prossimi passi

### Slot #1 — Acquisizione cron (BLOCCANTE)

1. Selezionare task sett. N (o prima `pending` come da regole JSON acquisizione)
2. Eseguire nel repo · validate indicati nel task
3. `status: done`, `completed_date`, nota in memoria

Regole: anti-duplicato · no tariffe online · alleato in copy se tocchi testi.

### Slot #2 — Blog proprietari (se `blog_friday` ≠ null o coda urgente GSC owner)

Applicare **`blog_publish_defaults`** in `venerdi-friday-pipeline.json`:

- Angolo da `blog_friday.angolo` / `owner_path` / `kw_seed`
- Visivo: hero IA + 3 figure + 2 tabelle + 2 SVG (`skill-editoriale-visivo.md`)
- CTA Class A + sezione «Cosa può fare Righetto»
- Gate: `check_doppioni_sito.py`, `audit_editorial_acquisition.py`, `audit_blog_visuals.py`, `audit-foto-ai.mjs`, `validate-page.js`

**Modalità per settimana:** vedi colonna «Blog venerdì» in § Calendario integrato sotto.

Se `mode: refresh_cta_only` → **nessun** nuovo slug; solo CTA batch.

### Slot #3 — Social acquisizione (proprietari)

1. Copiare brief da `weeks_aligned_acquisition[N-1].social_proprietari`
2. Scrivere caption con framework **`skill-acquisizione-contenuti-acquisizione.md`** §2
3. Salvare in `righetto_social/bozze_manuali/venerdi-{YYYY-MM-DD}-proprietari.md` (commit)
4. Indicare **media_hint** (carosello / reel / foto team) per pubblicazione manuale o agenda

Template spintax base: `righetto_social/templates/social_sezioni.json` → `proprietari_acquisizione`.

### Chiusura

- Log `skill-memoria-progressi.md`
- Output § Formato obbligatorio
- Commit (push se utente lo chiede)

---

## Calendario integrato 12 settimane (acquisizione + blog + social)

| Sett. | Slot #1 Acquisizione | Slot #2 Blog venerdì | Slot #3 Social proprietari |
|------:|----------------------|----------------------|----------------------------|
| 1 | landing-valutazione funnel | — | Valutazione / sopralluogo |
| 2 | Hub percorsi F,H,J | — | Hub indecisi |
| 3 | CTA blog batch 1 | Solo refresh CTA* | Blog owner in rotazione |
| 4 | Lead scoring KPI | — | Risposta rapida lead |
| 5 | Articolo percorso **F** invenduta | **Publish** angolo strategia oltre prezzo | Percorso F — strategia |
| 6 | Articolo **J** ristrutturare | **Publish/expand** prima/dopo lavori | Percorso J — valorizzazione |
| 7 | Mesh link A–L | **Area 2** mercato locale Limena/Vigonza | Territorio Limena |
| 8 | servizio-vendita (fatto se ally copy live) | — | Reel servizio vendita |
| 9 | CTA blog batch 2 | Refresh CTA* o coda owner | Eredità / costi vendita |
| 10 | landing-consulenza | **Publish** timing vendita 2026 | Indecisi timing |
| 11 | FAQ/chatbot owner | FAQ expand top GSC | Linda + umani |
| 12 | Review KPI trimestre | Coda/gap Area 1 | Recap trimestre |

\* Se `editorial-queue` ha `scheduled` owner con data ≤ oggi+7 → **publish** con defaults al posto di solo refresh.

Dettaglio machine-readable: **`data/venerdi-friday-pipeline.json`**.

---

## Output combinato venerdì (formato obbligatorio)

```markdown
## Venerdì Righetto — [data] · Settimana acquisizione [N]/12

**Alleato:** messaggio madre attivo su touchpoint della settimana.

### Slot #1 — Acquisizione cron
- **Task:** [title] (`[id]`) — [done | pending]
- **Percorsi A–L:** …
- **Commit:** …

### Slot #2 — Blog owner
- **Azione:** [publish | refresh CTA | skip | da coda eq-XXX]
- **Specifiche:** owner_path · angolo · territorio · gate audit OK?
- **Slug:** …

### Slot #3 — Social proprietari
- **TARGET / PROBLEMA / CTA:** …
- **Media:** [carosello | reel | foto team] — file bozza: `righetto_social/bozze_manuali/…`

### Tu oggi (~15 min)
- [ ] GSC batch (`gsc-indexing-weekly.json`)
- [ ] GBP post o recensione

### Repo oggi (agente) — riepilogo
1. Acquisizione · 2. Blog · 3. Social bozza

### KPI (opzionale)
- `data/acquisition-kpi-template.json`

### Focus se poco tempo
- Slot #1, poi #2 se publish già in coda

### Lunedì
- [ ] Lead giorno 0 · [ ] GSC follow-up
```

---

## Cosa resta manuale

| Attività | Chi | Riferimento |
|----------|-----|-------------|
| Pubblicare post IG/FB da bozza venerdì | Utente / social cron | `publish_from_agenda.py` |
| Lead giorno 0 | Agenzia | playbook |
| GSC / GBP | Utente | skill-seo §11.6 |
| Ads | Dopo sett. 8+ | playbook § Canali |

---

## Collegamenti

- `.cursor/skills/righetto-venerdi-sito-90giorni/SKILL.md`
- `skill-competitor-roadmap-q3-2026.md` §8 `"SKILL"`
- `context-map.json` → `venerdi_contenuti_skimm`
- Repo legacy (solo struttura, non copy): vedi `legacy_external_repo` in pipeline JSON
