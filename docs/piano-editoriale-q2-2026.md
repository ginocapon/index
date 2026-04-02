# Piano editoriale Q2 2026 (aprile–giugno) — Righetto Immobiliare

Documento di allineamento tra **strategia commerciale**, **contenuti sito** e **promemoria automatici** (`.github/workflows/venerdi-righetto-piano.yml`).  
Il ciclo operativo 12 settimane resta definito nella skill `righetto-venerdi-sito-90giorni`; qui si definisce **cosa** raccontare, mese per mese.

## Regole contenuto (sito)

- Dati di mercato solo con **fonte citabile** (OMI, ISTAT, Banca d’Italia, FIMAA dove applicabile).  
- Nessun numero inventato su tempi di vendita o percentuali: per i “casi Limena in X giorni” usare solo **incarichi reali** documentabili.  
- Commissioni e claim agenzia: coerenti con `TEST-SKILL/SKILL-2.0.md` / policy interna.  
- TikTok/Reels/GBP: **azioni fuori repo**; il sito ospita hub (blog, landing, testimonianze) che rimandano o integrano.

---

## Aprile 2026 — Acquisizione immobiliare 2.0

**Filone strategico:** da contatto sporadico a **digital farming** (monitoraggio portali/social, risposta rapida, CRM).  
**Angolo da comunicare sul sito (senza overclaim):** “come lavoriamo quando arriva un’opportunità online”, importanza della **risposta in tempi brevi**, consulenza strutturata.

| Tipo | Tema suggerito | Nota |
|------|----------------|------|
| Blog lungo | Processo di acquisizione: cosa succede dopo il primo contatto (privacy, appuntamento, mandato) | Tono professionale, no promesse su “prima della concorrenza” senza prova |
| Blog / refresh | Classe energetica, EPBD e mercato: cosa può chiedere oggi un compratore e cosa può preoccupare un venditore | **Rimandi a testi ufficiali UE/MITE**; evitare allarmismi |
| Landing o FAQ | Pagina servizio “per chi vuole vendere” + link a calcolatore / contatto | Già forte social proof in home: rinforzare **CTA** e **dati** |

**Off-site (manuale):** definire 1 canale di alert (es. salvataggi ricerche) e regole di risposta entro 24 h — non va nel cron, ma va in checklist venerdì.

---

## Maggio 2026 — Visibilità online e profondità locale

**Filone:** SEO locale (quartieri Padova, comuni già presidiati es. **Limena**, **Guizza**, **universitaria**) + **autorità tramite dati**.

| Tipo | Tema suggerito | Nota |
|------|----------------|------|
| Blog | Come interpretare le **Quotazioni OMI** per [zona]: guida al proprietario | Esempi con dati OMI reali e data osservazione |
| Blog / servizio | Dalla “stima veloce” al **report di mercato**: cosa include (confronti, range, limiti) | Allinea messaggio a CMA-style; niente “gratis” fuorviante se ci sono vincoli |
| Tecnico | **Linda** (chatbot): copy e flusso per **telefono in cambio di report** / follow-up | Modifica `js/chatbot.js` o testi landing chat; test mobile |
| Zona | 1 scheda quartiere **nuova o ampliata** (testo unico, internal link da blog money) | Coerente con skill settimana “Zone locali” |

---

## Giugno 2026 — Recensioni, video, prova sociale

**Filone:** portare sul sito e in raccolta lead ciò che già funziona in video-testimonianze; **GMB** come canale parallelo.

| Tipo | Tema suggerito | Nota |
|------|----------------|------|
| Blog breve / news | Modello “caso studio” con **solo metriche vere** (giorni, prezzo, zona) | Se non ci sono numeri pubblicabili, usare formato “percorso tipo” |
| Social (manuale) | 1 reel/tiktok da clip esistente + link a pagina contatto o zona | Ripubblicare dal materiale già sul sito |
| Trust | Allineare blocco recensioni su **3 pagine chiave** (home, vendita, contatti) | Skill settimana 8 |
| GBP | 1 post/settimana o rotazione foto team/ufficio | Checklist venerdì già presente |

---

## Mercato Padova 2026 (messaggio editoriale)

Comunicare **stabilità e domanda** solo se supportato da **fonti aggiornate** (es. report trimestrali, OMI). Frase tipo: “Secondo [fonte, data], l’area di Padova mostra …” — mai numeri generici senza citazione.

---

## Automazione (cron)

| Workflow | Quando | Cosa fa |
|----------|--------|---------|
| `venerdi-righetto-piano.yml` | Venerdì ~07:30 CET | Issue con settimana 1–12 + **focus mese** da questo file |
| `audit-settimanale.yml` | Venerdì ~07:00 CET | Audit tecnico |
| `mini-seo-check.yml` | Venerdì ~07:00 CET | Check SEO |

**Non automatizzabile in modo sicuro senza revisione umana:** pubblicazione articoli, numeri di mercato, claim legali/fiscali. Il cron **promemoria**, non scrive sul sito.

---

## Revisione

A fine giugno 2026: aggiornare ancoraggio ciclo 12 settimane (skill) e creare `piano-editoriale-q3-2026.md` o estendere questo documento.
