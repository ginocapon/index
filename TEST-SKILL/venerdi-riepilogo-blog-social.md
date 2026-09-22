# Venerdì — Blog e social: cosa è nuovo, cosa è già online

> **Per l’utente e l’agente.** Regola madre: **chi vende trova in Righetto un alleato.**  
> Dati aggiornati: `data/venerdi-friday-pipeline.json` · `data/editorial-queue.json` · `data/acquisition-roadmap-cron.json`

---

## In sintesi (3 flussi distinti)

| Flusso | Quando | Cosa |
|--------|--------|------|
| **A — Blog sito** | Venerdì slot #2 (se previsto) + max **1 nuovo articolo/settimana** | Nuovo HTML **oppure** solo CTA su articoli **già pubblicati** |
| **B — Social proprietari** | Venerdì slot #3 | **1 post dedicato** (caption nuova + foto/carosello) → landing/hub/servizio o copertina blog esistente |
| **C — Social catalogo** | Dom–ven cron `righetto_social` | Rotazione **annunci + blog + landing** già nel sito (titolo pari pari, **non** sostituisce il post B) |

---

## Blog — articoli GIÀ ESISTENTI (da promuovere / rinforzare, non riscrivere)

### Batch 1 — settimana acquisizione **3** (solo aggiunta CTA Class A)

| Slug | Percorsi owner |
|------|----------------|
| `blog-rendimento-affitto-padova` | D |
| `blog-valutazione-casa-padova-guida-2026` | A, G |
| `blog-vendere-casa-limena-proprietario-2026` | B |
| `blog-affittare-casa-padova-proprietario-2026` | D, I |
| `blog-mandato-esclusivo-padova-perche-conviene-2026` | B, F |

**Social sett. 3:** in post proprietari usare **copertina** di uno di questi (rotazione) + link articolo + CTA `landing-valutazione`.

### Batch 2 — settimana acquisizione **9** (solo CTA)

| Slug | Percorsi owner |
|------|----------------|
| `blog-successione-immobiliare-padova` | H |
| `blog-costi-vendere-casa-padova-2026` | B, E |
| `blog-percorso-vendita-immobile-padova-2026` | B, C |
| `blog-so-tutto-io-venditore-presuntuoso-padova-2026` | E |
| `blog-agenzia-immobiliare-limena-come-scegliere-2026` | G, B |

**Social sett. 9:** carosello che rimanda a **successione** o **costi vendita** (già online).

### Pillar owner (link interni + social quando serve prova)

`blog-valutazione-casa-padova-guida-2026` · `blog-costi-vendere-casa-padova-2026` · `blog-percorso-vendita-immobile-padova-2026` · `blog-vendere-casa-limena-proprietario-2026` · `vendere-casa-padova-errori` · `servizio-vendita` · `landing-valutazione` · `proprietario-immobile`

---

## Blog — articoli DA REALIZZARE (nuovi o ampliamento forte)

| Sett. acq | Azione | Contenuto |
|----------:|--------|-----------|
| **5** | **Nuovo** (se anti-doppioni OK) | Percorso **F** — casa invenduta, strategia oltre il prezzo |
| **6** | **Ampliare** preferito | `blog-bonus-mobili-2026-massimizzare-ristrutturazioni.html` — angolo vendere prima/dopo lavori |
| **7** | **Nuovo** Area 2 | Mercato locale proprietario **Limena / Vigonza** (OMI/FIMAA) |
| **10** | **Nuovo** | Percorsi **B, C, L** — quando vendere, pianificazione 2026 |
| **12** | **Da coda** | Prossimo `scheduled` / gap Area 1 in `editorial-acquisition-balance.json` |

### Coda editoriale (scheduled)

| ID | Target | Slug previsto |
|----|--------|----------------|
| `eq-sep25-001` | 2026-09-25 | `blog-affitti-studenti-settembre-padova-proprietario-2026` |

**Regola:** se la data coda coincide con un venerdì senza altro publish obbligatorio → **pubblicare la coda** (owner, trend settembre) al posto di “solo CTA”. Max 1 articolo nuovo/settimana.

### Settimane SENZA nuovo articolo blog (solo sito + social B)

1, 2, 4, 8 — lavoro su landing, hub, KPI, servizio-vendita; social proprietari sì, blog nuovo no.

---

## Social — cosa postare dove

### B — Post proprietari (venerdì, manuale/bozza)

- **File bozza:** `righetto_social/bozze_manuali/venerdi-YYYY-MM-DD-proprietari.md`
- **Template:** `proprietari_acquisizione` in `social_sezioni.json`
- **Framework:** TARGET → PROBLEMA → PROMESSA → PROVA → CTA → link
- **Media:** carosello 3–5 slide **oppure** foto team **oppure** copertina blog **già esistente** **oppure** reel 9:16
- **Link tipici:** `landing-valutazione` · `servizio-vendita` · `proprietario-immobile` · `landing-consulenza` (vedi settimana N in pipeline JSON)

| Sett. acq | Tema post B | Blog/landing da linkare |
|----------:|-------------|-------------------------|
| 1 | Valutazione / sopralluogo | `landing-valutazione` |
| 2 | Hub indecisi | `proprietario-immobile` |
| 3 | Da blog owner batch 1 | Uno dei 5 slug batch 1 |
| 4 | Risposta rapida | `contatti` + telefono |
| 5 | Casa invenduta | `landing-consulenza` (+ nuovo blog se pubblicato) |
| 6 | Ristrutturare e vendere | `landing-valutazione` (+ blog bonus ampliato) |
| 7 | Territorio Limena | `zona-limena` / `servizio-vendita` |
| 8 | Alleato vendita | `servizio-vendita` |
| 9 | Eredità / costi | `blog-successione` o `blog-costi-vendere` |
| 10 | Timing vendita | `landing-consulenza` |
| 11 | Linda + umani | `landing-chat-valutazione` |
| 12 | Recap trimestre | `proprietario-immobile` |

### C — Social automatico (catalogo sito)

- **Script:** `righetto_social/genera_bozze_settimanali.py` (~16 bozze/sett.)
- **Cosa ruota:** immobili attivi · **tutti i blog già pubblicati** · landing · pagine agenzia · 2 notizie RSS
- **Non confondere:** il reel del martedì su un annuncio **non** è il post “alleato venditori” del venerdì

---

## Checklist agente ogni venerdì

1. Calcola settimana acquisizione **N** (anchor 2026-09-19).
2. Slot #1 → task in `acquisition-roadmap-cron.json`.
3. Slot #2 → tabella «DA REALIZZARE» / «GIÀ ESISTENTI» sopra + coda `scheduled`.
4. Slot #3 → scrivi bozza social + indica foto (team / carosello / copertina blog esistente).
5. Output piano con le tre righe compilate per l’utente.

---

## Riferimenti skill

`skill-acquisizione-cron-venerdi.md` · `skill-acquisizione-contenuti-acquisizione.md` · `skill-social-automation.md` §2b · `skill-editoriale-visivo.md`
