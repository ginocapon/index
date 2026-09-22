# Acquisizione proprietari e incarichi — strategia sito (PRIORITÀ ASSOLUTA)

> **Precedenza:** questo modulo prevale su istruzioni SEO/blog/UI **in contrasto** con l'obiettivo commerciale. Restano valide se **compatibili**.
>
> **Aggiornato:** 14 settembre 2026 · Audit: `documenti/Audit-Strategico-Acquisizione-Incarichi-Righetto-2026-08-29.pdf`
>
> **Playbook commerciale** (script, follow-up, canali fuori sito): `skill-acquisizione-playbook-commerciale.md` — **non** duplicare qui.
>
> **Mentalità advisor + territorio 10 km Limena:** `TEST-SKILL/skill-real-estate-advisor.md` · `data/advisor-territorio-limena-10km.json` · Cursor `/advisor`

---

## Concetto fondamentale — **UN ALLEATO** (FONDAMENTALE)

**Tutto il sito parte da qui:** chi vende (o sta per vendere) deve percepire Righetto come **un alleato**, non come un portale o un venditore di incarichi.

- Copy, CTA, blog owner, servizi, chat e GEO/AEO devono comunicare **fiducia, competenza locale e accompagnamento**.
- Il funnel (sotto) è lo strumento; l’**alleato** è il messaggio madre.
- Dettaglio operativo tono, GEO e master prompt: **`skill-real-estate-advisor.md`** § «UN ALLEATO».

---

## Obiettivo principale (non negoziabile)

**Acquisire nuovi immobili e nuovi proprietari** — vendita, valutazione, locazione, gestione, reddito, consulenza patrimoniale — presentando Righetto come **alleato** del proprietario in ogni passo.

Funzioni da **mantenere** (non penalizzare): annunci, ricerca immobili, acquirenti, inquilini, visibilità portfolio.

**Strumenti secondari:** visite, articoli, keyword, SEO generica — utili solo se supportano l'acquisizione.

### Funnel commerciale (obiettivo finale)

Il sito non serve solo visite o richieste generiche. Ogni modifica deve avvicinare a:

```
VISITATORE
  → PROPRIETARIO INTERESSATO
  → CONTATTO (form / telefono / WhatsApp)
  → CONVERSAZIONE
  → SOPRALLUOGO
  → VALUTAZIONE PROFESSIONALE
  → PROPOSTA DI INCARICO
  → POSSIBILMENTE INCARICO IN ESCLUSIVA
```

**Regola compenso:** mediazione e percentuali **sempre da concordare in sede** nel mandato — **mai** listini o percentuali online (sito, blog, script, landing).

---

## Regola decisionale (ogni modifica)

Prima di ogni modifica significativa:

0. **Il venditore si sente alleato** da questo testo/UI? (FONDAMENTALE)
1. **Cosa** è stato modificato?
2. **Quale problema** strategico corregge?
3. **Quale proprietario** viene aiutato (percorso A–L)?
4. **Quale passo** del funnel avanza?
5. **Come** può portare a contatto, sopralluogo o incarico?

Se non si risponde a (0) e (5) → modifica **secondaria** o da rivedere.

**In caso di parità:** privilegiare ciò che intercetta proprietari, dimostra competenza, costruisce fiducia, favorisce contatto.

### Regola anti-duplicato (obbligatoria)

Prima di creare **nuova pagina, landing o strumento**:

1. Verificare inventario asset (§ Inventario asset esistenti).
2. Preferire **estendere** pagina/form/hub già presente.
3. Nuova URL solo se percorso A–L **non coperto** e coda editoriale lo giustifica (`acquisition_contribution: direct`).
4. **Vietato:** seconda landing valutazione, secondo hub proprietari, form parallelo che fa la stessa cosa.

---

## Sistema proprietari — mappa operativa

```
PUBBLICITÀ / GOOGLE / SOCIAL / CONTENUTI / CONTATTI LOCALI / REFERRAL
        ↓
LANDING O PAGINA DEL SITO (hub, servizio, blog owner, landing-valutazione)
        ↓
STRUMENTO GRATUITO (stima Linda, guida, checklist, consulenza orientativa)
        ↓
RACCOLTA CONTATTO (form con provenienza, telefono, WhatsApp post-stima)
        ↓
QUALIFICAZIONE (lead scoring § Lead scoring)
        ↓
CONTATTO AGENZIA (telefono / WhatsApp / email — playbook §)
        ↓
SOPRALLUOGO
        ↓
VALUTAZIONE PROFESSIONALE
        ↓
PROPOSTA DI INCARICO (condizioni e compenso in sede)
```

Hub centrale: **`proprietario-immobile.html`**.

---

## Inventario asset esistenti (non duplicare)

| Asset | Ruolo funnel | Note |
|-------|--------------|------|
| `proprietario-immobile.html` | Hub decisionale — 6 percorsi card | Punto di smistamento A–L |
| `landing-valutazione.html` | Conversione valore + Linda + PDF | Generatore appuntamenti (§ Calcolatore) |
| `landing-consulenza-immobiliare-gratuita.html` | Indecisi / confronto / seconda opinione | Percorsi B, C, G, L |
| `servizio-vendita.html` | Vendita + form `#richiedi` | Percorsi B, F |
| `servizio-locazioni.html` | Locazione + form | Percorsi D, I |
| `servizio-gestione.html` | Delega locazione | Percorsi I, K |
| `servizio-valutazioni.html` | Pagina servizio perizia | Supporto fiducia, link da landing |
| `vendere-casa-padova-errori.html` | Educazione vendita da privato | Percorso E — CTA verso consulenza, non form primario |
| `landing-vendere-casa-padova.html` | Landing vendita (campagna) | Solo campagne mirate |
| `landing-chat-valutazione.html` / `landing-chat-vendita.html` | Chat entry point | Collegare a funnel, non sostituire form |
| Blog owner (`blog-*-proprietario-*`, successione, costi vendita, mandato…) | Acquisizione organica | CTA Class A (§ CTA) |
| Supabase `richieste` + `newsletter_subscribers` | Lead + provenienza | `skill-forms-leads.md` |
| Chatbot / FAQ | Qualificazione e routing | `scripts/audit_chatbot_faq.py` |

**Evitare** come unica destinazione owner: `contatti` generico (ok come fallback secondario).

---

## Percorsi proprietario A–L (12 porte d'ingresso)

Ogni riga indica **asset già presente** o **gap** (articolo/coda — non nuova landing duplicata).

| ID | Situazione | Messaggio chiave | Pagina / asset ideale | CTA | Info da raccogliere (progressive) | Obiettivo funnel |
|----|------------|------------------|----------------------|-----|-----------------------------------|------------------|
| **A** | Quanto vale casa mia? | «Prima stima online, valutazione reale con sopralluogo» | `landing-valutazione` · `blog-valutazione-casa-padova-guida-2026` | Richiedi valutazione / sopralluogo | Comune, tipologia, mq, stato — **telefono dopo** stima | Sopralluogo |
| **B** | Sto pensando di vendere | «Capire tempi, documenti e strategia senza impegno» | `proprietario-immobile` · `servizio-vendita` · `landing-consulenza` | Consulenza gratuita / servizio vendita | Motivo vendita, tempistica indicativa, zona | Conversazione → sopralluogo |
| **C** | Vorrei vendere ma non so quando | «Pianificare con dati di mercato, non urgenza artificiale» | `landing-consulenza` · `blog-percorso-vendita-immobile-padova-2026` | Prenota consulenza orientativa | Orizzonte temporale (3–6–12 mesi), vincoli | Lead nurturing |
| **D** | Vendere o affittare? | «Confronto numeri su Padova/provincia» | `blog-rendimento-affitto-padova` · card hub «Metterlo a reddito» | `landing-valutazione` + `servizio-locazioni` | Uso futuro, mutuo, reddito atteso | Valutazione + scelta servizio |
| **E** | Voglio vendere da privato | «Cosa rischi e quando l'agenzia conviene davvero» | `vendere-casa-padova-errori` · blog owner vendita | `landing-consulenza` (non pressione) | Da quanto prova, difficoltà incontrate | Consulenza → valutazione comparativa |
| **F** | Già in vendita, non vendo | «Non solo prezzo: strategia, comparabili, visibilità» | `landing-consulenza` · `servizio-vendita` | Analisi strategia gratuita | Prezzo richiesto, tempo sul mercato, portali usati | Sopralluogo + revisione strategia |
| **G** | Valutazione altra agenzia | «Secondo parere su comparabili e posizionamento» | `landing-valutazione` · `blog-valutazione-casa-padova-guida-2026` | Richiedi seconda valutazione | Range ricevuto, dubbi specifici | Sopralluogo → fiducia |
| **H** | Ereditato immobile | «Successione, vacant property, vendita o locazione» | `blog-successione-immobiliare-padova` · `landing-consulenza` | Consulenza patrimoniale | Stato pratica, coeredi, urgenza fiscale | Consulenza → percorso vendita/locazione |
| **I** | Immobile vuoto | «Metterlo a reddito o vendere: gestione chiavi in mano» | `servizio-locazioni` · `servizio-gestione` | Gestione / locazione | Stato immobile, distanza dal proprietario | Incarico gestione o locazione |
| **J** | Da ristrutturare | «Valore prima/dopo lavori e tempi di vendita» | `blog-bonus-mobili-2026-massimizzare-ristrutturazioni` · **gap coda** articolo owner ristrutturazione | `landing-valutazione` | Lavori previsti, budget, tempi | Valutazione post/analisi investimento |
| **K** | Più immobili | «Strategia patrimonio: vendita, locazione, mix» | `landing-consulenza` · `servizio-gestione` | Consulenza patrimoniale | N. immobili, obiettivi, zone | Mandato multiplo / gestione |
| **L** | Non so ancora | «Orientamento senza impegno» | `proprietario-immobile` · `landing-consulenza` | Scegli percorso / consulenza | Situazione generica, domanda aperta | Qualificazione → percorso A–K |

### Campi coda editoriale (estensione)

Aggiungere quando applicabile:

| Campo | Valore |
|-------|--------|
| `owner_path` | A–L (uno o più) |
| `funnel_step` | awareness · considerazione · decisione · post-vendita-fallita |
| `form_fields_min` | elenco campi minimi per quella fase |

---

## Calcolatore valutazione → generatore appuntamenti

**Asset:** `landing-valutazione.html` · `js/valutazione-pdf.js` · Linda (stima AI) · insert Supabase `provenienza: landing-valutazione`.

Non è «metti dati → numero definitivo». Percorso obbligatorio:

1. **Input** — comune, tipologia, mq, piano, stato (progressive disclosure).
2. **Prima indicazione** — range/stima Linda + disclaimer «stima orientativa».
3. **Educazione** — perché due immobili simili valgono diversamente: piano, esposizione, luminosità, condominio, manutenzioni, pertinenze, posizione precisa, APE, qualità fabbricato, lavori, interni, comparabili reali (allineare copy a `blog-valutazione-casa-padova-guida-2026`).
4. **Invito sopralluogo** — «Valutazione professionale gratuita con sopralluogo» (CTA primaria, non chiusura con numero secco).
5. **Raccolta contatto** — nome, email, telefono, motivo; checkbox GDPR; WhatsApp opzionale post-invio.
6. **Follow-up** — playbook commerciale giorno 0–1.

**Modifiche future:** arricchire step 3–4 **nella landing esistente** — non creare `landing-valutazione-v2`.

**Obiezione «basta la stima online»:** risposta in pagina + FAQ — «serve vedere stato reale e comparabili verificabili sul posto».

---

## Equilibrio editoriale (4 aree)

| Area | Priorità | Esempi |
|------|----------|--------|
| **1 — Proprietari e acquisizione** | **Costante** | vendita, valutazione, locazione, gestione, reddito, decisioni patrimoniali |
| **2 — Mercato locale** | Alta | Padova, provincia, Veneto — dati con significato per il proprietario |
| **3 — Normativa/economia con impatto** | Media | solo se lega immobili/proprietari/locazioni/fisco |
| **4 — Acquirenti/ricerca** | Mantenuta | acquisto, mutuo, affitto inquilino — **non monopolizzare** il calendario |

**Regola ciclo:** almeno **1 articolo Area 1** ogni **2 settimane** (`acquisition_priority: true`).

**Alternanza indicativa:** 50% Area 1+2 owner / 50% Area 3+4 — verificare con `data/editorial-acquisition-balance.json`.

### Contenuti che portano proprietari (esempi titolo — no «come comprare casa»)

Priorità coda — verificare anti-doppioni (`check_doppioni_sito.py`) prima di scrivere:

| Intent owner | Esempi titolo | Percorso |
|--------------|---------------|----------|
| Valore / prezzo | Quanto vale davvero un appartamento a Padova? · Perché due appartamenti nello stesso condominio valgono diversamente? | A, G |
| Vendita bloccata | Ho messo casa in vendita ma nessuno compra: cosa sto sbagliando? · Meglio abbassare il prezzo o cambiare strategia? | F |
| Costi / decisione | Quanto costa davvero vendere casa? · Vendere da soli: quando conviene e quando no? | B, E |
| Fiducia agenzia | Come capire se una valutazione immobiliare è realistica? · Perché tre agenzie stimano diversamente? | G |
| Locazione vs vendita | Conviene affittare o vendere nel 2026 a Padova? | D |
| Patrimonio / eredità | Cosa fare con un immobile ereditato a Padova | H |
| Ristrutturazione | Vendere prima o dopo i lavori: come decidere | J |

**Blog già allineati (mantenere e interlinkare):** `blog-vendere-casa-limena-proprietario-2026`, `blog-affittare-casa-padova-proprietario-2026`, `blog-valutazione-casa-padova-guida-2026`, `blog-costi-vendere-casa-padova-2026`, `blog-mandato-esclusivo-padova-perche-conviene-2026`, `blog-successione-immobiliare-padova`, `blog-percorso-vendita-immobile-padova-2026`.

---

## Classificazione obbligatoria pre-pubblicazione

Ogni articolo/pagina nuova — campi coda:

| Campo | Descrizione |
|-------|-------------|
| `primary_audience` | proprietario_vendita · proprietario_locazione · acquirente · inquilino · investitore · misto |
| `owner_problem` | Domanda/esigenza reale |
| `owner_path` | A–L se applicabile |
| `search_intent` | Perché cerca quell'info |
| `concrete_value` | Risposta utile (non SEO filler) |
| `acquisition_contribution` | direct · indirect · none — + spiegazione |
| `traffic_type` | strategic · generic |
| `acquisition_priority` | true/false — Area 1 owner |
| `funnel_step` | awareness · considerazione · decisione |

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
| Vendita fallita / già in annuncio | `landing-consulenza` |
| Eredità / patrimonio | `landing-consulenza` |

Pattern: **risposta utile → competenza → comprensione problema → approfondimento → contatto**.

### Cosa chiedere e quando (form)

| Fase | Campi ok | Evitare troppo presto |
|------|----------|------------------------|
| Prima stima (A) | comune, tipologia, mq, email | telefono obbligatorio, documenti catastali |
| Consulenza (B, C, L) | nome, telefono o email, motivo, tempistica | mandato, exclusiva, prezzo desiderato tassativo |
| Servizio vendita (F) | zona, da quanto in vendita, canali usati | — |
| Gestione/locazione (I, K) | indirizzo/zona, stato immobile | — |

Implementazione: `skill-forms-leads.md` · `data-rig-lead-form` · provenienza univoca.

---

## Homepage e pagine principali

> **Prompt Chirurgo:** `skill-prompt-chirurgo-homepage-editoriale.md` — hero owner-first, doppio percorso.

- **Dual audience:** ricerca immobili **+** percorso «Hai un immobile?»
- CTA owner hero → **`landing-valutazione`**
- Hub → **`proprietario-immobile`**
- Servizi grid → **`servizio-vendita`**, **`landing-valutazione`**, **`servizio-locazioni`**
- Sticky mobile → **`landing-valutazione`**
- Modal blog → **`landing-valutazione`** o **`servizio-vendita`**, non `contatti` generico

### Audit sito — dove si perdono proprietari (checklist)

| Punto | Rischio | Azione |
|-------|---------|--------|
| Hero solo acquirenti | Owner non vede percorso | Sezione «Hai un immobile?» + CTA valutazione |
| CTA generico «Contatti» | Lead non qualificato | CTA contestuale per percorso |
| Stima Linda senza invito sopralluogo | Lead freddo, abbandono | Step educazione + CTA sopralluogo (§ Calcolatore) |
| Blog senza CTA owner | Traffico senza conversione | Class A verso landing/servizio |
| Form con troppi campi | Abbandono | Progressive disclosure |
| `servizio-vendita` non indicizzato | Perdita funnel B/F | GSC follow-up (skill-seo §10) |
| Educazione (`vendere-casa-padova-errori`) senza uscita | Lettura senza contatto | Box consulenza a fine pagina |

---

## Differenziazione Righetto → motivazioni concrete

Trasformare asset esistenti in argomenti commerciali (in sede, non percentuali online):

| Asset | Motivazione per il proprietario |
|-------|----------------------------------|
| Dal 2000 · 350+ immobili · 101 comuni | Conoscenza reale del mercato locale, non stime generiche |
| 127 recensioni 4.9/5 | Trasparenza e referenze verificabili |
| Valutazione gratuita + sopralluogo | Decisione informata prima di qualsiasi impegno |
| Comparabili OMI / database annunci | Prezzo basato su dati, non sensazioni |
| Virtual tour · drone · video | Maggiore visibilità vs annuncio amateur |
| Gestione locazione · preliminari · utenze | Un interlocutore per tutta la filiera |
| Hub proprietario + guide owner | Aiuto prima della vendita, non solo mandato |
| Linda / strumenti digitali | Primo passo immediato, poi umano sul sopralluogo |
| Compenso concordato in sede | Chiarezza contrattuale personalizzata |

---

## Lead scoring (0–100)

**Riferimento dati:** `data/lead-scoring-rules.json` · annotare punteggio in admin/note interna su `richieste` (campo `messaggio` prefisso `[score:NN]` fino a colonna dedicata).

| Segnale | Punti |
|---------|------:|
| Ha già deciso di vendere | +30 |
| Ha richiesto valutazione / sopralluogo | +20 |
| Ha indicato tempistica (≤6 mesi) | +15 |
| Ha fornito telefono | +10 |
| Ha accettato appuntamento sopralluogo | +25 |
| Confronta altre agenzie (G) | +10 |
| Solo curiosità / «tra un anno» | +5 |
| Dice «non ho fretta» | −10 |
| Solo email, rifiuta telefono | −5 |
| Richiesta generica senza immobile | −15 |

**Utilizzo:**

- **≥70** — contatto entro 24 h, priorità sopralluogo
- **40–69** — contatto 48 h + contenuto utile (percorso C, L)
- **<40** — nurturing email/WhatsApp (playbook), no pressione

---

## KPI dashboard settimanale

**Template:** `data/acquisition-kpi-template.json` · integrare nel report venerdì quando disponibili i dati manuali.

| Metrica | Fonte | Obiettivo |
|---------|-------|-----------|
| Sessioni pagine owner (hub, landing-valutazione, servizi) | GA4 | Trend ↑ |
| Richieste valutazione | Supabase `richieste` provenienza landing-valutazione | Conteggio settimanale |
| Lead totali owner | Supabase per provenienza owner | — |
| Telefonate / WhatsApp | Registro manuale agenzia | — |
| Appuntamenti sopralluogo | CRM / registro | — |
| Valutazioni effettuate | Registro | — |
| Incarichi firmati | Registro | — |
| Incarichi esclusivi | Registro | — |
| Tasso lead → sopralluogo | Calcolo | Individuare collo di bottiglia |
| Tasso sopralluogo → incarico | Calcolo | — |

**Domanda chiave ogni venerdì:** «Dove abbiamo perso proprietari questa settimana?» (pagina, form, tempi risposta, follow-up).

---

## Cron venerdì — esecuzione automatica (12 settimane)

> **Dettaglio completo:** `skill-acquisizione-cron-venerdi.md` · **Stato:** `data/acquisition-roadmap-cron.json`

Ogni **venerdì**, con ordine `"SKILL"` / `/venerdi` / «piano venerdì», l'agente implementa **1 task** del ciclo (repo #1) senza ridiscutere la scaletta.

| Sett. | Task automatico |
|------:|-----------------|
| 1 | `landing-valutazione` → sopralluogo |
| 2 | Hub card F, H, J |
| 3 | CTA blog batch 1 (5 articoli GSC) |
| 4 | Lead scoring + KPI |
| 5–12 | Articoli gap, mesh, servizi, consulenza, FAQ, review |

**Anchor ciclo:** 2026-09-19 (primo venerdì). Dopo completamento: aggiornare JSON + `skill-memoria-progressi.md`.

---

## Piano operativo — priorità

### 🔥 DA FARE SUBITO (sito + processo)

*(Settimane 1–4 coperte dal cron venerdì — esecuzione automatica.)*

1. Verificare funnel post-Linda su `landing-valutazione` (step educazione + CTA sopralluogo).
2. Interlink hub `proprietario-immobile` ↔ percorsi A–L (card mancanti: F, H, J se assenti).
3. CTA Class A su blog owner top GSC.
4. Follow-up GSC `servizio-vendita` e pillar owner.
5. Lead scoring su nuove `richieste` in admin.
6. Risposta lead **giorno 0** (playbook).

### 🟠 DA FARE DOPO

1. Articolo gap percorso **J** (ristrutturare e vendere).
2. Articolo gap percorso **F** (casa invenduta — strategia oltre il prezzo).
3. Estendere hub con card «Immobile ereditato» / «Già in vendita» se traffico lo giustifica.
4. KPI owner nel PDF venerdì.
5. Campagne locali mirate (percorsi A, B, F) → landing esistenti.

### 🟢 QUANDO IL SISTEMA È AVVIATO

1. Automazione follow-up 7–90 gg (consenso GDPR).
2. Google Ads / Meta su percorsi ad alto intent.
3. Referral professionisti (notai, geometri, CAF) — solo modalità lecite.
4. A/B test CTA hub e hero.

**Fasi operative complete:** sito → campagne → contenuti → acquisizione contatti → contatto → sopralluogo → presentazione valutazione → proposta incarico → follow-up → misurazione — dettaglio script e canali in **`skill-acquisizione-playbook-commerciale.md`**.

---

## FAQ

Dopo publish/aggiornamento: nuove domande owner per percorso A–L? FAQ obsolete? Collegare a hub e landing.

Script: `scripts/audit_chatbot_faq.py`.

---

## Divieti

- Considerare completato il pivot con solo articoli vendita + un pulsante
- Prioritizzare traffico generico vs acquisizione senza giustificazione
- Trasformare il sito in **solo** proprietari (penalizza acquirenti)
- Modificare indiscriminatamente pagine che funzionano
- Cambiamento **apparente** senza verifica percorso proprietario
- **Duplicare** landing/hub/form già esistenti
- **Pubblicare** percentuali o listini mediazione online
- Database proprietari / successioni con modalità non lecite o senza base GDPR

---

## Test finale (dopo ogni fase)

Simula proprietario Padova/Veneto (scegli un percorso A–L):

- [ ] Capisce che l'azienda può aiutarlo?
- [ ] Trova il percorso adatto senza passare da Contatti generico?
- [ ] Info dimostrano competenza?
- [ ] Capisce servizi utili?
- [ ] Motivo concreto per contattare / sopralluogo?
- [ ] Potrebbe affidare l'immobile?
- [ ] Nessuna promessa di prezzo definitivo online?

Se **no** → correggere prima di proseguire.

---

## Verifica periodica

Controllare squilibrio verso acquirenti/inquilini: blog recenti, homepage feed, GSC intent, coda `proposed`.

Memoria: **`data/editorial-acquisition-balance.json`** · audit: **`scripts/audit_editorial_acquisition.py`**.

---

## Collegamenti

- **Cron venerdì automatico:** **`skill-acquisizione-cron-venerdi.md`** · `data/acquisition-roadmap-cron.json`
- Playbook commerciale: **`skill-acquisizione-playbook-commerciale.md`**
- Form lead: **`skill-forms-leads.md`**
- Audit strategico: `documenti/Audit-Strategico-Acquisizione-Incarichi-Righetto-2026-08-29.pdf`
- Editoriale: `skill-editoriale-visivo.md` · `skill-editorial-queue.md`
- Social / fuori sito: `skill-social-automation.md`
- Hub: `proprietario-immobile.html`
- Lead scoring: `data/lead-scoring-rules.json`
- KPI: `data/acquisition-kpi-template.json`
- Cursor: `.cursor/skills/righetto-acquisizione-proprietari/SKILL.md`
