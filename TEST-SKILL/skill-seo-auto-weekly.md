# Skill — SEO automatico settimanale (GSC → max 10 pagine → registro → valutazione)

**Versione:** 1.0 — 10/10/2026 · **Motore:** `scripts/seo_auto/seo_auto.py` · **Cron:** `.github/workflows/seo-auto-settimanale.yml` (venerdì 08:00 Europe/Rome) · **Cursor skill:** `/seo-auto`

Versione rivista e resa operativa del «PROMPT MASTER — Sistema SEO automatico con AI» (chat 10/10/2026), con revisione critica rispetto alla north star a 12 mesi.

---

## 0. Perché esiste (north star, non vanity metrics)

- **Obiettivo a 12 mesi:** margine 1M€ → **≥4 mandati di vendita al mese su immobili ≥300k** (`data/strategy-nord-star-12m-acquisizione.json`).
- **Messaggio madre:** *Chi vende trova in Righetto un alleato.*
- Il sistema **non** ottimizza i clic in generale: ottimizza i **clic non-brand verso le pagine owner** (valutazione, vendita, gestione, locazione, hub proprietario) e la loro **indicizzazione**. Un +30% di clic su un blog per acquirenti vale meno di +5 clic su `/landing-valutazione`.
- Pesi di business in `data/seo-auto/config.json` → `business_tiers` + `tier_multiplier` (owner_conversione ×1.6, pillar ×1.3, …).

## 1. Revisione critica del prompt originale (cosa è cambiato e perché)

| Prompt originale | Problema | Versione Righetto |
|---|---|---|
| Lunedì 08:00 | Lunedì agenda piena; la pipeline di miglioramento è il venerdì | **Venerdì 08:00** (cron `0 6 * * 5`, in ora solare scatta alle 07:00) |
| «Seleziona 10 pagine» | Dieci è un tetto, non un obiettivo: forzarlo porta a modifiche inutili | **Massimo** 10 pagine, solo quelle sopra `min_score` (8) |
| Confronto 28 gg vs 28 gg | Ignora il lag GSC, la stagionalità e il trend del sito | Dati `final` con lag di 3 gg; esito **relativo all'andamento del sito** (controllo); soglia minima di 100 impressioni |
| CTR come segnale principale | Con 94 pagine indicizzate e 330 non indicizzate (luglio 2026) il collo di bottiglia è l'**indicizzazione** | URL Inspection API (max 60 URL per ciclo) + sitemap pulita prima di ritoccare title e meta |
| Tutte le query insieme | Le query brand («righetto») gonfiano il CTR e nascondono i problemi | Metriche **brand e non-brand separate** (regex `righetto`) |
| Ottimizzare ogni settimana | Cambiare spesso title e meta impedisce di misurare e crea instabilità in SERP | **Cooldown di 28 gg** per pagina; le op solo tecniche sono esenti |
| «Applica le modifiche» | Rischio di contenuti AI in serie (spam policy Google «scaled content abuse») e di claim senza fonte | Op atomiche e reversibili; **nessuna riscrittura del corpo in automatico**; claim senza fonte → segnalati, non inventati |
| GA4 per le conversioni | Le conversioni vere di Righetto sono le righe in Supabase `richieste` | GA4 opzionale; la fonte delle conversioni è `richieste.provenienza` (task 3 del martedì) |
| Dati assenti → «procedi» | Rischio di simulare | Se l'API manca: fonte `stale` dichiarata, peso dimezzato, **nessuna valutazione**, oggetto email «DATI GSC DA AGGIORNARE» |

## 2. Fonti dati (in cascata, mai simulate)

1. **API Search Console** (`GSC_SERVICE_ACCOUNT_JSON`) — `searchAnalytics.query` per page, page+query e date; periodo corrente e precedente di 28 gg; URL Inspection.
2. **CSV manuale** in `data/seo-auto/inbox/` — export «Pagine» dalla UI GSC con il confronto attivo (colonne clic, impressioni e posizione; la seconda colonna è il periodo precedente).
3. **Fallback repo** (`data/gsc-keywords-priority.json`) — marcato `stale: true` con le limitazioni scritte nello snapshot.
4. **Export Copertura → Valide** (indipendente dalle fonti 1–3) — GSC → Indicizzazione → Pagine → «Visualizza dati sulle pagine indicizzate» → Esporta → zip in `data/seo-auto/inbox/` (nome con `Coverage`/`Valid`). Il motore legge `Tabella.csv` (URL + ultima scansione) e `Grafico.csv` (trend), salva `coverage-latest.json` e marca `non_indicizzata` le URL in sitemap da ≥28 gg (`indexing_grace_days`) assenti dall'elenco. Valido per 21 gg (`coverage_max_age_days`); con l'API attiva prevale l'URL Inspection. Le varianti www/.html nell'export sono residui (www → 301, .html → canonical): non generano interventi.
5. **GA4** — `non_configurato` finché non esiste il secret `GA4_PROPERTY_ID` (Data API non ancora implementata: va dichiarato, non simulato).

## 3. Ciclo settimanale (comando unico)

```bash
python3 scripts/seo_auto/seo_auto.py apply     # pubblica SOLO ciò che è approvato in approvals.json
python3 scripts/seo_auto/seo_auto.py weekly    # ingest → audit → verify → evaluate → select → dashboard → report
python3 scripts/seo_auto/seo_auto.py rollback --id SEO-2026W41-slug
```

Output: `data/seo-auto/snapshots/AAAA-MM-GG.json`, `audit-latest.json`, `selection-latest.json`, `proposals/`, `registry.jsonl` (append-only, `EV-xxxxx`), `backups/<ID>/` (`.before`, `.after`, `diff.patch`), `dashboard.html` (noindex, robots `Disallow: /data/seo-auto/`), `reports/AAAA-MM-GG.md`, email a info@.

## 4. Punteggio di selezione (trasparente, nel JSON di ogni pagina)

`ctr_gap` (CTR < 70% del benchmark per posizione — **stima**) · `zero_click` · `striking` (posizione 4–15, ≥30 impressioni) · `decline` (clic −max(5, 20%)) · `sitemap` (noindex, canonical altrove, template) · `indicizzazione` (10 × peso tier: owner/pillar 2, owner_contenuto/zona 1.6, acquirente 0.8, contenuto 0.5 — un articolo di attualità non indicizzato non deve superare una pagina owner) · `technical` (title/meta/H1/canonical) · `underlinked` (<10 link interni verso pagine owner/pillar) → × moltiplicatore di tier. Peso GSC dimezzato se i dati sono `stale`. Esclusioni salvate (`excluded_cooldown`, `below_threshold`).

**ID intervento:** `SEO-{AAAAWss}-{slug}` (stabile nel ciclo; suffisso `-linkN` per i link in entrata).

## 5. Op consentite (atomiche e reversibili)

`set_title` (sincronizza og/twitter) · `set_meta` (sincronizza og/twitter) · `replace` / `insert_before` / `insert_after` con ancora **univoca**. Su HTML: canonical, form, numero di JSON-LD e H1 devono restare invariati, JSON-LD valido, `validate-page.js` OK, altrimenti **ripristino automatico**. Su `sitemap.xml`: XML ben formato.

**Vietato in automatico:** riscrivere il corpo, aggiungere numeri senza fonte, cambiare URL, redirect o canonical tra pagine owner (cannibalizzazione → decisione umana con dati di query), toccare form e lead.

## 6. Approvazione

- **Fase attuale (dal 10/10/2026): `approval_mode: "delegato_venerdi"`.** Delega di Gino in chat: *«da venerdì prossimo io carico i dati e tu esegui gli aggiornamenti e i testi degli articoli che ritieni necessari per aumentare le performance»*. Quando Gino carica gli export il venerdì, l'agente **esegue senza chiedere un ulteriore ok** e scrive `approvals.json` con `approved_by: "delega venerdì 10/10/2026"`.
- **Coperto dalla delega:** title e meta · link interni contestuali · pulizia della sitemap · **refresh dei testi** delle pagine selezionate: nuove sezioni H2/H3 sull'intento delle query reali, FAQ, box «In sintesi», aggiornamento dei dati **con fonte istituzionale linkata**, rimozione o riformulazione dei claim senza fonte, CTA owner coerenti con il messaggio madre.
- **Fuori dalla delega (serve l'ok esplicito in chat):** cambi di URL, redirect, canonical tra pagine, noindex, eliminazione o accorpamento di pagine, modifiche a form e lead, nuovi articoli (seguono `/blog` con il controllo anti-doppioni), tariffe o mediazione, qualsiasi cosa su DNS e server.
- **Limiti fissi anche con la delega:** max 10 pagine per ciclo · cooldown di 28 gg per pagina · ogni numero con fonte verificabile (regola d'oro) · anti-plagio (`skill-content.md` §2.0b) · niente paragrafi riempitivi (§8.1c) · `validate-page.js` + `audit_blog_publishability.py` sugli articoli toccati · backup e ID per ogni intervento · report finale con elenco ID e comando di rollback.

### 6.1 Procedura venerdì (quando Gino carica i dati in chat)

1. Copia gli export in `data/seo-auto/inbox/`:
   - **Prestazioni:** zip con «Confronta» ultimi 28 gg vs 28 gg precedenti, che contiene Pagine, Query e Date.
   - **Copertura → Valide:** lo zip.
   - Opzionale: Copertura → Non indicizzate.
   - Se arriva un export «Ultimi 3 mesi» senza confronto va bene lo stesso: il motore ricava il 28 vs 28 del sito da `Grafico.csv`, riporta le metriche di pagina a 28 gg e blocca le pagine il cui title è cambiato durante il periodo misurato (data da git).
2. `python3 scripts/seo_auto/seo_auto.py weekly`. Leggi `selection-latest.json` e il report.
3. Per ogni pagina selezionata scegli la leva più piccola che risolve il problema misurato:
   - CTR basso → title e meta;
   - posizione 4–15 → contenuto sull'intento delle query;
   - non indicizzata → link interni e richiesta di indicizzazione;
   - calo → controllo di query e concorrenza, poi refresh.
4. Scrivi le op in `approvals.json` → `apply` → validazioni → commit e push su main → deploy → `verify`.
5. In chat rispondi con:
   - cosa è cambiato (pagina, prima e dopo, motivo legato al dato);
   - ID e comando di rollback;
   - le URL da far ispezionare a Gino (max 10);
   - le decisioni fuori delega.

### 6.2 Blog: i 10 articoli peggiori a rotazione (REGOLA FISSA ogni venerdì — dal 10/10/2026)

Richiesta di Gino: *«risistemi i primi 10 articoli peggiori e venerdì prossimo i successivi — regola fissa»*. Vale in aggiunta alle max 10 pagine di §6.1 ed è coperta dalla delega.

1. `weekly` calcola già la classifica (`blog-rank`) → `data/seo-auto/blog-refresh-queue.json`, campo `next_batch` (10 articoli).
   - Punteggio: clic mancati rispetto al benchmark di posizione (tetto 60) + 0 clic con impressioni (5) + non indicizzato da ≥28 gg (15 × peso tier) + frasi alterate (×1.2 se l'articolo ha impressioni, ×0.8 se no) + 3 per ogni problema on-page; tutto × moltiplicatore del tier (owner prima).
   - Esclusi: articoli in cooldown (title cambiato da <28 gg), già sistemati negli ultimi 90 gg (`blog_refresh_repeat_days`), in `blog_refresh_hold`. Se un escluso è tra i peggiori, entra al primo venerdì utile.
2. Per ognuno dei 10:
   - `python3 scripts/seo_auto/fix_text_artifacts.py <file> --preview` → correggi le frasi alterate (op `replace` con ancora univoca, generate da `build_ops`); rileggi le correzioni nel contesto;
   - title ≤60 e meta ≤155 riscritti a mano sull'intento delle query reali (mai troncati, mai «…»);
   - dati senza fonte: aggiungi la fonte istituzionale o togli il numero (regola d'oro); niente paragrafi riempitivi;
   - `dateModified` alla data del venerdì solo se il testo è davvero cambiato.
3. Op in `approvals.json` con ID `SEO-AAAAWss-blog10-<slug>` e `batch: "blog-N"` → `apply` → `validate-page.js` + `audit_blog_publishability.py` → `blog-batch-done` → commit e push → `verify`.
4. In chat: elenco dei 10 con motivo e ID di rollback, più l'anteprima dei 10 del venerdì dopo.

**Divieto permanente (causa del testo alterato in 76 articoli):** mai sostituire in automatico «Padova», «agenzia immobiliare» o «Righetto Immobiliare» con sinonimi a rotazione («capoluogo euganeo», «territorio patavino», «lo studio», «il team»…) per abbassare la densità delle keyword. `scripts/patch_compliance_warns.py` ora segnala soltanto lo stuffing e i title/meta troppo lunghi: si correggono riscrivendo la frase a mano.

- **Passaggio al pubblicato da cron senza chat** (solo op tecniche) dopo **4 cicli consecutivi senza rollback** e con l'API GSC attiva → `auto_publish_allowed_ops` in config.

## 7. Valutazione (dopo ≥28 gg di dati reali post-pubblicazione)

`miglioramento_osservato` (pagina vs sito ≥×1.2 e CTR in aumento) · `stabile` · `peggioramento_osservato` (≤×0.8 e CTR in calo → proporre rollback) · `dati_insufficienti` (<100 impressioni o nessuno snapshot API) · `problema_tecnico` (live check fallito). È **correlazione, non causalità**: va scritto così nel report.

## 8. Report settimanale (italiano, sezioni A–H)

A. Fonte e qualità dei dati · B. Stato del sito (brand/non-brand, indicizzazione) · C. Pagine selezionate con punteggio · D. Interventi pubblicati e verificati online · E. Esiti degli interventi precedenti · F. Proposte in attesa di approvazione · G. Limiti, rischi e claim da verificare · H. Prossime azioni (max 3).

## 9. Credenziali (una volta sola — Gino)

1. Google Cloud Console → progetto → abilita **Google Search Console API**.
2. IAM → **Service account** → chiave JSON.
3. Search Console → proprietà `sc-domain:righettoimmobiliare.it` → Impostazioni → Utenti → aggiungi l'email del service account (**Limitato** basta).
4. GitHub → repo → Settings → Secrets → Actions → **`GSC_SERVICE_ACCOUNT_JSON`** = contenuto del JSON. Mai nel repo.
5. Opzionale: `GA4_PROPERTY_ID`. Già presente: `EMAIL_RELAY_KEY`.

Senza il punto 4 il sistema gira lo stesso ma in modalità `stale` (onesta, non misurabile).

## 10. Regole fisse

Regola d'oro sulle fonti · claim consentiti (350+, 101 comuni, 98%, 127 recensioni 4.9/5, dal 2000) · mediazione mai online · anti-plagio (`skill-content.md` §2.0b) · no DNS · URL senza `.html` · premortem prima del push.

## 11. Log cicli

| Ciclo | Fonte | Selezionate | Pubblicate | Note |
|---|---|---|---|---|
| 2026W41 (10/10, manuale) | repo_json_stale | 7 | 9 interventi (4 sitemap, 2 title/meta, 3 link) | `/landing-vendita` in attesa dei dati query; claim «15%» su `/vendere-casa-padova-errori` (H1, corpo, FAQ) da verificare |
| 2026W41 bis (10/10, export Copertura) | repo_json_stale + copertura 04/10 | 10 | 3 interventi link (zona-limena → 4 zone cintura; 2 link → blog-tempi-vendita) | 183/205 sitemap indicizzate (89%), trend 106→196; batch 28/09 tutto indicizzato. Non indicizzate: chi-siamo, contatti (ispezione URL manuale), 4 zone cintura, tempi-vendita; 6 articoli di attualità da non spingere; bonus-mobili aprile possibile doppione |
| 2026W41 ter (10/10, export Prestazioni 3 mesi) | gsc_csv (pagine 92 gg, sito 28 vs 28 da Grafico) | 10 | 7 interventi (6 title/meta, 1 refresh testo + link su contratto-affitto) | Sito 28 gg: 404 clic vs 329 (+23%), 7.875 impr. vs 6.737. Non-brand debole su vendita («vendere casa padova» pos. 42,6). servizio-vendita e rendimento-affitto esclusi: title cambiato da <28 gg nel periodo misurato. Cannibalizzazione contratto-affitto ↔ canone-concordato: differenziati. Tabella €/mq canoni da verificare |
| 2026W41 blog-1 (10/10, regola §6.2) | gsc_csv + copertura | 10 articoli peggiori | 10 refresh (frasi alterate corrette, title/meta su 8, dateModified) | Articoli: affitto-breve, affitti-canoni, mercato-2026, vendita-strategie, mutuo-prima-casa, vigonza-rubano, sondaggio-bancaditalia, case-vendita, mutui-casa, investire. Causa trovata e bloccata: `fix_stuffing` in `patch_compliance_warns.py`. Batch blog-2 il 16/10 (ricalcolato con i nuovi dati) |
