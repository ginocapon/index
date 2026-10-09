# Prompt operativo — design premium → conversione → Nord Star 1M€/12 mesi

> **Origine:** video `Downloads/Video.mov` (trascrizione 2026-10-09). Idee estratte: (1) skill di design con regole su tipografia, spaziatura, layout, animazioni (nel video: «Emil Kowalski», «Impeccable»); (2) skill «taste» contro il look generico da AI; (3) collegare Figma MCP + Playwright per progettare, costruire, testare e fare screenshot.
> **I nomi nel video sono trascritti a orecchio:** verificare repo/autore prima di installare qualsiasi skill o MCP di terze parti (rischio supply-chain: leggere il contenuto, nessun codice remoto eseguito alla cieca).
> **Vincoli Righetto (non negoziabili):** HTML/CSS/JS vanilla, zero CDN/framework, URL senza `.html`, WCAG AA (mai `#FF6B35` con testo bianco), no `filter: blur` animato, no `will-change` permanente, claim solo verificati, mai percentuali di mediazione online, trasparenza AI Act. Le skill di design esterne spesso assumono React/Tailwind: **estrarre i principi, non il codice/stack.**
> **Collegamento Nord Star:** `data/strategy-nord-star-12m-acquisizione.json` · il design serve a un solo KPI: più sopralluoghi/mandati da proprietari (fascia alta ≥300k inclusa). Il design da solo non produce 1M€: lo produce il funnel (visita → lead → sopralluogo → incarico).

---

## PROMPT DA INCOLLARE IN CHAT

```
Leggi prima: SKILL-2.0.md, TEST-SKILL/skill-massimo-punteggio.md, skill-premortem-righetto.md,
skill-acquisizione-proprietari.md, skill-design.md, skill-strategia-nord-star-12m-acquisizione.md,
data/strategy-nord-star-12m-acquisizione.json, data/acquisition-kpi-template.json.

OBIETTIVO: portare il design del sito Righetto a livello "da studio professionale" per aumentare
conversione proprietari → sopralluogo → incarico (Nord Star 1M€ in 12 mesi, tolleranza KPI ±1%).
Stack invariato: HTML/CSS/JS vanilla, zero CDN, mobile-first, WCAG AA.

FASE 0 — Baseline (non toccare nulla prima)
1. Con il browser integrato (o Playwright se già disponibile) fai screenshot mobile (390px) e desktop
   (1440px) di: home, proprietario-immobile, landing-valutazione, landing-consulenza-immobiliare-gratuita,
   servizio-vendita, servizio-valutazioni, un blog owner (blog-casa-non-si-vende-padova-strategia-2026).
2. Per ognuna misura: LCP/CLS (Performance.getMetrics via CDP), contrasto CTA, dimensione touch target,
   gerarchia tipografica, spaziatura, coerenza con skill-design.md. Tabella: pagina | problema | file:riga | gravità.
3. NON inventare numeri di conversione: se manca il baseline (GA4/GSC/admin), segnalalo e chiedi i dati.

FASE 1 — Design system minimo (estrai principi, non copiare stack)
Crea/aggiorna UN solo file css/design-tokens.css (con ?v=N) con:
- scala tipografica (clamp, max 2 famiglie già self-hosted in /fonts), interlinea, misura max 65–75ch
- scala di spaziatura a 8px, raggi, ombre sobrie, palette già esistente (var(--nero/--blu/--oro))
- regole animazione: solo opacity/transform, durata 150–250ms, easing coerente,
  rispetto di prefers-reduced-motion, nessuna animazione decorativa sopra la piega mobile
- anti-"look AI generico": niente gradienti viola, niente card identiche ripetute, niente emoji come
  icone principali, niente stock vuoti — usa foto reali Righetto (img/team, img/immobili) o grafica sobria
Applica prima a proprietario-immobile e landing-valutazione, poi estendi.

FASE 2 — Pagine funnel (priorità assoluta, in quest'ordine)
Per ogni pagina: 1 sola CTA primaria sopra la piega, prova sociale verificata (127 recensioni 4.9/5,
350+ immobili, 101 comuni, dal 2000), form in pagina (SERVIZI_CONFIG.sendNotifica + insert Supabase
richieste con provenienza), messaggio "chi vende trova un alleato", nessuna percentuale mediazione.
Pagine: proprietario-immobile → landing-valutazione → landing-consulenza-immobiliare-gratuita →
servizio-vendita → valutazione-vendita-riservata-padova (fascia alta, tono riservato/premium).
Scrivi per ciascuna: ipotesi di miglioramento + cosa misurare (kpi) — non promettere % di uplift.

FASE 3 — Verifica automatica (loop finché passa)
Dopo ogni pagina: screenshot mobile+desktop prima/dopo, node scripts/validate-page.js --file <pagina>,
controllo contrasto, overflow orizzontale 0, nessuna richiesta a domini esterni (Network).
Se un controllo fallisce: correggi e riesegui, non passare oltre.

FASE 4 — Chiusura
- Premortem (skill-premortem-righetto.md §4.2) sul diff: solo path/URL/comandi, niente chiacchere.
- Aggiorna skill-memoria-progressi.md (log) e data/acquisition-kpi-template.json (campi da misurare).
- Commit in italiano. NON fare push senza mia conferma esplicita.

REGOLE: nessun dato senza fonte; nessuna dipendenza esterna; se una scelta è mia (brand, tono, foto),
fermati e chiedi con opzioni precise. Se hai dubbi su un'installazione di skill/MCP terzi, elenca cosa
farebbe e aspetta il mio OK.
```

---

## Setup opzionale (da fare a mano, con verifica)

| Step nel video | Equivalente per noi | Note |
|---|---|---|
| Skill di design (tipografia/spaziatura/layout/animazioni) | `skill-design.md` + `css/design-tokens.css` | Meglio **estrarre regole** dalle skill pubbliche e scriverle nelle nostre, che installare codice altrui |
| Skill «taste» (anti look-AI) | Sezione anti-generico nel prompt Fase 1 | Verificare cosa contiene prima di adottarla |
| Figma MCP | Opzionale | Richiede account Figma + token; utile solo se facciamo mockup. Non necessario per partire |
| Playwright MCP | Browser integrato Cursor (screenshot + CDP) già disponibile | Sufficiente per il loop di verifica |

## Cosa NON dedurre dal video
- Che il design produca da solo il milione: serve volume di lead qualificati e tasso di incarico (vedi Nord Star, lead automation Livello A/B).
- Che le skill esterne siano sicure o compatibili col nostro stack: vanno lette prima dell'uso.
