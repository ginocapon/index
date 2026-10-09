# skill-linda-collega-virtuale — Righetto Immobiliare AI

> Versione 1 · 9 ott 2026 · Stato: **in test su ramo `linda/kb-v1`, non in produzione**.
> Carica insieme a `skill-essentials.md`, `skill-security.md`, `skill-ai-act-compliance.md`, `skill-forms-leads.md`.

## 1. Obiettivo

Linda diventa un **collega virtuale** che risponde su servizi, vendita, affitto, acquisto, documenti, fiscalità/mutui
(solo con fonte), territorio e **dati reali degli annunci**, e si aggiorna **senza programmare**:
chi gestisce il sito scrive/approva le risposte in `admin-kb.html`.

Principio: **Linda risponde solo con ciò che è documentato e approvato. Se non lo sa, lo dice** e rimanda a un agente
(049.8843484). Nessun dato inventato. Nessun nome/telefono/email dei proprietari, mai.

## 2. Le 8 priorità obbligatorie (ordine fisso)

1. **Sicurezza e contatti** — nessun lead perso, nessun dato personale esposto, errori Supabase mai mostrati come successo.
2. **Restyling con Playwright** — su ramo separato, screenshot prima/dopo, mai in produzione senza approvazione.
3. **Design system coerente** — marchio "RI" trasparente sullo sfondo (non toccare `rig-brand-atmosphere.*`), contrasto AA, tap target ≥ 44px.
4. **Conversione commerciale** — CTA chiare su valutazione/vendita/contatto; messaggio madre: *chi vende trova in Righetto un alleato*.
5. **Collega virtuale con KB modificabile** — vedi §4.
6. **Apprendimento controllato** — Linda non "impara da sola": le domande reali producono *proposte*, l'approvazione è umana.
7. **Controllo dei costi** — vedi §6. Nessuna spesa ricorrente senza preventivo approvato.
8. **Misurazione dei risultati** — ogni modifica ha una metrica (lead/settimana, % domande risposte, 👍/👎, tempo di risposta).

## 3. Regole di sviluppo

- Un cambiamento alla volta, **ramo separato + tag di backup + rollback scritto** prima di toccare produzione.
- Nessun push/pubblicazione senza approvazione esplicita; prima della pubblicazione **anteprima estetica** delle pagine principali.
- Ogni funzione nuova ha **test Playwright** con risposta attesa dichiarata; test visivi su 5 viewport per le modifiche grafiche.
- Mai chiavi segrete nel repo (`service_role`, token, password). La chiave `anon` è pubblica ma **non è autorizzazione**: la protezione sta nelle RLS.
- Mai colonne `proprietario_*`, `note_interne`, `prezzo_reale` in query pubbliche o nel contesto di Linda.
- Mai tariffe o percentuali di mediazione online; dati numerici/fiscali solo con fonte (OMI, FIMAA, ISTAT, Banca d'Italia, ADE).
- Trasparenza AI Act: Linda si dichiara assistente digitale automatizzato **a regole, senza IA generativa** (testo in `js/chatbot.js` / `RigAiDisclosure`). Se un giorno si aggiunge un modello generativo, aggiornare **prima** disclosure e privacy.

## 4. Architettura KB (v1)

| Pezzo | File | Note |
|---|---|---|
| Schema, RLS, RPC, cronologia, purge 90 gg | `sql/linda-kb-v1.sql` | Da applicare a mano in Supabase **dopo approvazione**. Idempotente. |
| Client chat | `js/linda-kb.js` (caricato da `js/chatbot.js`) | Ordine: codice annuncio → KB approvata → regole storiche. Spegnimento: `window.LINDA_KB=false`. |
| Pannello no-code | `admin-kb.html` + `js/admin-kb.js` | Supabase Auth + `kb_admins`. **Non** usa la password di `admin.html`. `noindex`, fuori da sitemap. |
| Seed FAQ storiche | `scripts/linda_esporta_faq.js` | 256 FAQ → CSV "da verificare" + audit numeri senza fonte. |
| Domande ipotetiche | `scripts/linda_genera_domande.py` | Da blog (risposte estrattive) + rapporto campi mancanti negli annunci. Nessun costo. |
| Test | `tests/e2e/linda-kb.spec.js`, `tests/e2e/admin-kb.spec.js` | `npx playwright test -c tests/e2e/playwright.config.js linda-kb admin-kb` |

Stati voce: `bozza → da_verificare → approvata → scaduta`. Modificare testo/domanda di una voce approvata la riporta in `da_verificare`.
Ogni modifica finisce in `kb_history` (ripristinabile; il ripristino richiede nuova approvazione).

**Flusso RAG attuale (senza LLM):** domanda → (codice annuncio? dati live) → ricerca full-text italiana + similarità trigram
sulle voci **approvate e non scadute** → se punteggio ≥ 0.45 risponde con testo approvato + fonti https + data → altrimenti
regole storiche → altrimenti "non l'ho colto" + log anonimo per il rapporto lacune.
La soglia 0.45 va **calibrata** con "Prova Linda" su domande reali dopo il primo caricamento.

## 5. Privacy domande reali

Il client rimuove email/telefoni/codici fiscali **prima** dell'invio; il trigger SQL li rimuove di nuovo; testo ≤ 400 caratteri;
nessun identificativo persona (solo sessione casuale); conservazione 90 giorni (`select linda_purge_questions();` o pg_cron);
lettura solo admin. **Da fare prima della pubblicazione:** aggiungere in privacy §trasparenza una riga sul registro anonimo delle domande
(testo da approvare dal titolare).

## 6. Costi — separazione A/B/C/D

| Voce | Costo oggi | Con questa v1 |
|---|---|---|
| **A. Sviluppo una tantum** (ore) | — | già svolto in questa sessione; calibrazione + popolamento KB = ore del titolare |
| **B. Infrastruttura ricorrente** | Supabase già in uso | 0 € aggiuntivi: tabelle piccole, nessuna estensione a pagamento (pg_trgm/unaccent incluse) |
| **C. Inferenza AI** | 0 € (nessun modello) | **0 €** (nessun LLM). Un LLM opzionale per riformulare resta **fuori scope** finché non approvato con budget |
| **D. Manutenzione umana** | — | ~15–30 min/sett. per approvare proposte e leggere il rapporto lacune |

Regola: prima di introdurre qualsiasi voce C > 0, presentare stima per 1.000 conversazioni e tetto mensile con interruttore.

## 7. Metodo operativo (7 passi, sempre)

1. **Analizza** (codice, dati live, rischi) → 2. **Definisci il risultato misurabile** → 3. **Soluzione minima**
→ 4. **Implementa in test** (ramo, mock, mai produzione) → 5. **Verifica con Playwright**
→ 6. **Mostra risultati e chiedi approvazione** (con anteprima estetica) → 7. **Misura l'impatto** dopo la pubblicazione.

## 8. Rischi aperti noti (9 ott 2026) — vedi anche `skill-security.md`

- **CRITICO** `RIG_ADMIN_RLS_SECRET` è nel sorgente pubblico di `admin.html`: con l'header `x-righetto-admin` l'API anon legge `clienti`, `richieste`, `newsletter_subscribers` e tutti gli immobili. Richiede migrazione a Supabase Auth + RLS per ruolo e **rotazione del segreto**.
- **CRITICO** La password admin è iniettata in chiaro nel `admin.html` pubblicato (workflow `static.yml`).
- **ALTO** `immobili` espone ai visitatori `proprietario_nome/tel/email` e `note_interne` (la home fa `select('*')`). Serve una vista pubblica o `GRANT` per colonne + query esplicite.
- **MEDIO** `recensioni_chatbot` non esiste: le valutazioni del chatbot oggi si perdono (corretto da `sql/linda-kb-v1.sql` §8).
- **MEDIO** 59 FAQ storiche con dati numerici senza fonte citata (`data/linda-faq-audit.json`): verificarle o rimuoverle prima di approvarle.
