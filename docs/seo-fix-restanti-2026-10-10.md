# Correzioni audit SEO, seconda tranche

10 ottobre 2026. Base: 651e2e69. Backup completo di ogni parte modificata nel branch `backup/pre-seo-restanti-20261010` e tag `backup-pre-seo-restanti-20261010`, entrambi alla base. Tutte le differenze sono reversibili con git. Nessuna modifica DB, invio lead/newsletter o cancellazione pagina test.

## Interventi

- Completamento T02: catalogo pubblico senza sorgente localStorage; deduplica per slug/ID, merge con slug statici. Lettore Blog limitato ai record pubblicati, senza fallback a bozze/localStorage.
- Completamento T06: `ev=1` filtra gli annunci in evidenza; senza op/tab esplicito include vendita e affitto.
- T07: heroTitle H1, title sintetico con riferimento annuncio, unico su 23 schede. Località dai dati, non inventata. Controllo mobile: comando foto spostato per non coprire H1.
- T09: noindex su errore conservato (esisteva già); rimosso redirect automatico dopo 4 secondi che mascherava lo stato. HTTP resta 200 per limite della scheda query su GitHub Pages, non dichiarato 404 server.
- T10: 12 URL storage sostituite attraverso il manifest verso le stesse fotografie migrate; due foto legacy LA0312 sostituite con le prime due foto del relativo record attivo. 21 immagini editoriali >1 MB ridimensionate entro 1600 px e compresse mantenendo formato e soggetto: 47.344.580 -> 2.542.822 byte complessivi. Dimensioni native aggiunte dove mancavano entrambe. Nessuna nuova foto inventata.
- T11: href servizi#... verso pagine equivalenti; aste verso immobili?tab=aste. Skip link riparati; riferimento Limena verso articolo esistente.
- T12: insertBefore nel parent reale del footer; duplicazioni config.js eliminate su pagine root. Versioni asset aggiornate per evitare cache vecchia.
- T13: esenzioni fiscali under36 separate da Consap, condizioni transitorie esplicite, data/fonte visibili; aggiornato dataset chatbot per evitare rigenerazione della risposta vecchia. Preliminare: 30 giorni, non 20. Consap non garantisce mutuo automatico al 100%.
- T14: FAQ snapshot con 43 domande complete e JSON valido, dallo stesso dataset/mappa del runtime. Rigenerare con `node scripts/build-faq-snapshot.cjs` dopo cambi alla fonte. Contenuto statico visibile senza JS.
- T15: sitemap con 23 schede attive verificate tramite lettura pubblica DB, non share noindex. lastmod aggiornato sulle pagine effettivamente cambiate; per annunci date dai record, non inventate. Inventario annunci è snapshot: richiede rigenerazione quando disponibilità cambia, nessun nuovo cron attivato.
- T16: wordCount calcolato sul testo article/main/body escluse script/style/nav/header/footer/form (150 pagine); 9 salti heading corretti. Nessuna riscrittura title per puro limite 60 caratteri, né riempimento testi. Query×pagina ancora necessaria per interventi CTR.
- T17: templates e lunedi-email-report esclusi dall'artifact Pages, non cancellati dal repository. Preview pubblica landing/email-offerta-luce noindex; placeholder unsubscribe rotto rimosso dalla preview. Il repository pubblico non è riservato: noindex/esclusione sito non danno privacy al sorgente.
- T20: apertura automatica chatbot eliminata, mantenuti pulsante e interazione manuale. Tabella mutui scorre orizzontalmente nel proprio contenitore mobile, non allarga pagina.

## Fonti fiscalità verificate

- https://www.agenziaentrate.gov.it/portale/le-agevolazioni-prima-casa-under-36
- https://www.agenziaentrate.gov.it/portale/contratto-preliminare-di-compravendita/infogen-contratto-preliminare-di-compravendita
- https://www.consap.it/fondo-prima-casa/ (pagina aggiornata 30 settembre 2026, incluse categorie dal 3 agosto 2026)

Informazione pubblica, non parere professionale su singola pratica. Revisione notaio/banca consigliata.

## Test eseguiti prima del push

- `git diff --check`: OK.
- Controllo locale link su 288 HTML: zero destinazioni interne mancanti, zero fragment mancanti dai file modificati (admin/template esclusi dal crawl clienti).
- `node --check` di 255 script inline in HTML modificati: tutti validi; JSON-LD statici modificati tutti parsabili. `node --check js/chatbot.js` e script shared corretti.
- Validator repository `--all`: 122 errori, 204 warning. Non equivalgono a difetti Google, includono template/noindex e limite parser (title con attributi). Non nascosti o riscritti per fare verde. Validator mirato 8 pagine: 1 errore (false positive title con id nel lettore), 5 warning.
- Chrome staging con metodi POST/PUT/PATCH/DELETE bloccati: 23 schede, H1 unico, 23 title distinti, canonical coerenti. Blog, FAQ, contatti, servizi e tre pagine mutuo senza pageerror; JSON-LD DOM validi. op=affitto: 10 annunci affitto. ev=1: 10 annunci realmente in evidenza.
- Un articolo pubblicato DB aperto nel lettore: `cosa-cercano-gli-acquirenti-nel-2026-trilocali-giardini-e-classe-energetica-a-pa-padova`.
- 39 immagini nei 6 articoli problematici: tutte decodificate; lazy portate eager per controllo. Contact sheet delle 21 copertine compressa controllata a pixel.
- Pixel desktop/mobile 390px di scheda, FAQ, blog, acquisizioni e mutuo; comando foto mobile corretto dopo prima verifica. Nessun overflow pagina nei 6 template ricontrollati, chat non auto-aperta.
- Lighthouse home staging mobile, una misura laboratorio: performance 72, LCP 4,0s, CLS 0,033, TBT 590ms. Non è CrUX/p75, non misura INP reale né dimostra miglioramento prima/dopo.

## Sospesi / non verificati

- T08: descrizioni T0021, NEG2173a, UFF2195a, UFF2189a e appartamento Limena senza codice; foto LF0270; comune LF0242 (titolo Limena vs campo Padova). Servono dati agenzia, DB non modificato.
- T18: finalità delle 5 landing organiche/campagne. Nessun inlink arbitrario aggiunto.
- T19: claim commerciali, percentuali, ripetizioni e unioni richiedono scelta editoriale e dati query×pagina; nessuna unione automatica.
- Google URL Inspection, robots tester, Rich Results Test, CrUX/GSC non eseguiti. Nessun risultato indicizzazione/CTR garantito.
- Newsletter e moduli non inviati; nessuna prova salvataggio/notifica/consenso end-to-end.
- Non aperti tutti i 67 articoli DB; pixel non controllati su ogni URL/viewport.
- Le 21 immagini compresse sono sufficientemente leggere, ma non aggiunta generazione srcset per tutto il sito.
