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
4. **GA4** — `non_configurato` finché non esiste il secret `GA4_PROPERTY_ID` (Data API non ancora implementata: va dichiarato, non simulato).

## 3. Ciclo settimanale (comando unico)

```bash
python3 scripts/seo_auto/seo_auto.py apply     # pubblica SOLO ciò che è approvato in approvals.json
python3 scripts/seo_auto/seo_auto.py weekly    # ingest → audit → verify → evaluate → select → dashboard → report
python3 scripts/seo_auto/seo_auto.py rollback --id SEO-2026W41-slug
```

Output: `data/seo-auto/snapshots/AAAA-MM-GG.json`, `audit-latest.json`, `selection-latest.json`, `proposals/`, `registry.jsonl` (append-only, `EV-xxxxx`), `backups/<ID>/` (`.before`, `.after`, `diff.patch`), `dashboard.html` (noindex, robots `Disallow: /data/seo-auto/`), `reports/AAAA-MM-GG.md`, email a info@.

## 4. Punteggio di selezione (trasparente, nel JSON di ogni pagina)

`ctr_gap` (CTR < 70% del benchmark per posizione — **stima**) · `zero_click` · `striking` (posizione 4–15, ≥30 impressioni) · `decline` (clic −max(5, 20%)) · `sitemap` (noindex, canonical altrove, template) · `technical` (title/meta/H1/canonical) · `underlinked` (<10 link interni verso pagine owner/pillar) → × moltiplicatore di tier. Peso GSC dimezzato se i dati sono `stale`. Esclusioni salvate (`excluded_cooldown`, `below_threshold`).

**ID intervento:** `SEO-{AAAAWss}-{slug}` (stabile nel ciclo; suffisso `-linkN` per i link in entrata).

## 5. Op consentite (atomiche e reversibili)

`set_title` (sincronizza og/twitter) · `set_meta` (sincronizza og/twitter) · `replace` / `insert_before` / `insert_after` con ancora **univoca**. Su HTML: canonical, form, numero di JSON-LD e H1 devono restare invariati, JSON-LD valido, `validate-page.js` OK, altrimenti **ripristino automatico**. Su `sitemap.xml`: XML ben formato.

**Vietato in automatico:** riscrivere il corpo, aggiungere numeri senza fonte, cambiare URL, redirect o canonical tra pagine owner (cannibalizzazione → decisione umana con dati di query), toccare form e lead.

## 6. Approvazione

- **Fase attuale: `approval_mode: "manuale"`.** L'agente propone; Gino approva in chat; l'agente scrive `approvals.json` con `approved_by` e `approved_on`.
- **Passaggio all'automatico** solo per op tecniche (sitemap, meta >160, title troncato) dopo **4 cicli consecutivi senza rollback** e con l'API GSC attiva → `auto_publish_allowed_ops` in config. Title e contenuti restano manuali.

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
