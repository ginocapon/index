# Acquisizione proprietari e incarichi — strategia sito (PRIORITÀ ASSOLUTA)

> **Precedenza:** questo modulo prevale su istruzioni SEO/blog/UI **in contrasto** con l'obiettivo commerciale. Restano valide se **compatibili**.
>
> **Aggiornato:** 29 agosto 2026 · Audit: `documenti/Audit-Strategico-Acquisizione-Incarichi-Righetto-2026-08-29.pdf`

---

## Obiettivo principale (non negoziabile)

**Acquisire nuovi immobili e nuovi proprietari** — vendita, valutazione, locazione, gestione, reddito, consulenza patrimoniale.

Funzioni da **mantenere** (non penalizzare): annunci, ricerca immobili, acquirenti, inquilini, visibilità portfolio.

**Strumenti secondari:** visite, articoli, keyword, SEO generica — utili solo se supportano l'acquisizione.

---

## Regola decisionale (ogni modifica)

Prima di ogni modifica significativa:

1. **Cosa** è stato modificato?
2. **Quale problema** strategico corregge?
3. **Quale proprietario** viene aiutato?
4. **Quale comportamento** si favorisce?
5. **Come** può portare a contatto o incarico?

Se non si risponde → modifica **secondaria**.

**In caso di parità:** privilegiare ciò che intercetta proprietari, dimostra competenza, costruisce fiducia, favorisce contatto.

---

## Percorso proprietario (ecosistema)

```
HO UN IMMOBILE → devo capire cosa conviene → cerco info → risposte concrete
→ valore/rischi/opportunità → riconosco competenza → capisco come aiutano
→ consulenza/contatto → possibile incarico
```

Hub centrale: **`proprietario-immobile.html`** · conversione: **`landing-valutazione`**, **`servizio-vendita`**, **`servizio-locazioni`**, **`servizio-gestione`**, **`landing-consulenza-immobiliare-gratuita`**.

---

## Equilibrio editoriale (4 aree)

| Area | Priorità | Esempi |
|------|----------|--------|
| **1 — Proprietari e acquisizione** | **Costante** | vendita, valutazione, locazione, gestione, reddito, decisioni patrimoniali |
| **2 — Mercato locale** | Alta | Padova, provincia, Veneto — dati con significato per il proprietario |
| **3 — Normativa/economia con impatto** | Media | solo se lega immobili/proprietari/locazioni/fisco |
| **4 — Acquirenti/ricerca** | Mantenuta | acquisto, mutuo, affitto inquilino — **non monopolizzare** il calendario |

**Regola ciclo:** almeno **1 articolo Area 1** ogni **2 settimane** (campo `acquisition_priority: true` in coda).

**Alternanza indicativa:** 50% Area 1+2 owner / 50% Area 3+4 — verificare con `data/editorial-acquisition-balance.json`.

---

## Classificazione obbligatoria pre-pubblicazione

Ogni articolo/pagina nuova — campi coda:

| Campo | Descrizione |
|-------|-------------|
| `primary_audience` | proprietario_vendita · proprietario_locazione · acquirente · inquilino · investitore · misto |
| `owner_problem` | Domanda/esigenza reale |
| `search_intent` | Perché cerca quell'info |
| `concrete_value` | Risposta utile (non SEO filler) |
| `acquisition_contribution` | direct · indirect · none — + spiegazione |
| `traffic_type` | strategic · generic |
| `acquisition_priority` | true/false — Area 1 owner |

**Gate:** `python scripts/audit_editorial_acquisition.py --id eq-XXX`

Articolo con `acquisition_contribution: none` e `traffic_type: generic` → **non prioritario** salvo refresh SOSTENERE GSC owner.

---

## CTA contestuali (no «Contattaci subito» generico)

| Dopo contenuto su… | CTA naturale |
|--------------------|--------------|
| Valore / mercato | `landing-valutazione` |
| Vendita / errori | `servizio-vendita#richiedi` o `landing-consulenza` |
| Locazione / canoni | `servizio-locazioni#richiedi` |
| Gestione / contratti | `servizio-gestione` / `servizio-preliminari` |
| Decisione incerta | `proprietario-immobile` / `landing-consulenza` |

Pattern: **risposta utile → competenza → comprensione problema → approfondimento → contatto**.

---

## Homepage e pagine principali

- **Dual audience:** ricerca immobili **+** percorso «Hai un immobile?»
- CTA owner hero → **`landing-valutazione`** (non solo contenuto educativo)
- Hub → **`proprietario-immobile`**
- Servizi grid → link diretti **`servizio-vendita`**, **`landing-valutazione`**, **`servizio-locazioni`**
- Sticky mobile → **`landing-valutazione`**
- Modal blog → **`landing-valutazione`** o **`servizio-vendita`**, non `contatti` generico

---

## FAQ

Dopo publish/aggiornamento: nuove domande owner? FAQ obsolete? Collegare a hub e landing.

Script: `scripts/audit_chatbot_faq.py` (aggiornamento globale).

---

## Divieti

- Considerare completato il pivot con solo articoli vendita + un pulsante
- Prioritizzare traffico generico vs acquisizione senza giustificazione
- Trasformare il sito in **solo** proprietari (penalizza acquirenti)
- Modificare indiscriminatamente pagine che funzionano
- Cambiamento **apparente** senza verifica percorso proprietario

---

## Test finale (dopo ogni fase)

Simula proprietario Padova/Veneto:

- [ ] Capisce che l'azienda può aiutarlo?
- [ ] Trova il percorso adatto?
- [ ] Info dimostrano competenza?
- [ ] Capisce servizi utili?
- [ ] Motivo concreto per contattare?
- [ ] Potrebbe affidare l'immobile?

Se **no** → correggere prima di proseguire.

---

## Verifica periodica

Controllare squilibrio verso acquirenti/inquilini: blog recenti, homepage feed, GSC intent, coda `proposed`.

Memoria: **`data/editorial-acquisition-balance.json`** · audit: **`scripts/audit_editorial_acquisition.py`**.

---

## Collegamenti

- Audit: `documenti/Audit-Strategico-Acquisizione-Incarichi-Righetto-2026-08-29.pdf`
- Editoriale: `skill-editoriale-visivo.md` · `skill-editorial-queue.md`
- Hub: `proprietario-immobile.html`
- Cursor: `.cursor/skills/righetto-acquisizione-proprietari/SKILL.md`
