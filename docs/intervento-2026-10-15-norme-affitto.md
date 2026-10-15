# Correzioni APE e pubblica sicurezza nella guida affitti

Data preparazione: 15 ottobre 2026.
Stato: preparato; pubblicazione e verifica online da completare solo dopo conferma di Gino.

## Ambito

File: `blog-contratto-affitto-padova.html`.
Correzioni circoscritte alle frasi su APE e comunicazioni di pubblica sicurezza, incluse FAQ visibile e dati strutturati. Non è una revisione legale integrale dell'articolo. Titoli, descrizioni SEO, promesse sui tempi di valutazione, moduli e altre pagine invariati.

## Backup

Commit di partenza: `f3c34c5e61bfde84f7655b83567d92b9cd3c2423`.
Branch e tag: `backup-pre-norme-affitto-20261015` (creati localmente prima delle modifiche; da trasferire su GitHub al momento autorizzato).
Ripristino del solo articolo: recuperare il file da tale riferimento; non annullare interventi successivi di altre persone.

## Prima / dopo

1. APE: rimossa l'affermazione che l'allegazione è sempre obbligatoria e la fascia sanzioni non verificata. Ora è descritta la dichiarazione di ricezione della documentazione e l'eccezione all'allegazione per la locazione di singole unità immobiliari.
2. Questura: rimossa la regola universale delle 48 ore tramite Alloggiati Web. Distinte registrazione del contratto, cessione di fabbricato, obblighi riguardanti cittadini extracomunitari e campo di Alloggiati Web.
3. Errori da evitare: eliminata la ripetizione della stessa regola universale e la promessa di assenza di rischi. Ora invita a verificare gli obblighi del caso concreto con l'autorità competente.
4. FAQ visibile e corrispondente risposta JSON-LD: corrette le stesse due clausole; nessuna revisione delle altre affermazioni.
5. Data visibile: indicato il 15 ottobre 2026 precisando il perimetro della revisione. Aggiornati dateModified di articolo e FAQ.

## Fonti ufficiali consultate il 15 ottobre 2026

- Agenzia delle Entrate: https://www.agenziaentrate.gov.it/portale/schede/fabbricatiterreni/cedolare-secca/cedolare-secca-come-registrare
- Polizia di Stato, cessione di fabbricato: https://www.poliziadistato.it/articolo/cessione-di-fabbricato-1
- FAQ Alloggiati Web: https://alloggiatiweb.poliziadistato.it/PortaleAlloggiati/FAQ.aspx

Link inseriti nel testo della sezione obblighi. Non vengono dichiarate scadenze speciali non verificate.

## Controlli eseguiti in preparazione

- `node scripts/validate-page.js blog-contratto-affitto-padova.html`: superato. Title 54 caratteri, descrizione 155; non modificati.
- Parsing di tutti i blocchi JSON-LD: superato.
- `git diff --check`: superato.
- Anteprima locale prima/dopo a 390 e 1280 px: testo leggibile e identità grafica invariata.
- Nessun overflow orizzontale a 390 px. A 1280 px esiste già prima un overflow della navigazione (1356 px); non introdotto da questo intervento e non corretto fuori ambito.
- Nessun invio reale tramite moduli, nessuna modifica a database, contatti, Analytics, account o configurazione del sito.

## Da completare dopo conferma

- Confermare il punto di partenza aggiornato e la conferma di Gino.
- Pubblicare il solo intervento con backup su GitHub.
- Controllare il risultato della pubblicazione e la pagina pubblica, inclusi testi corretti e JSON-LD.
- Rimuovere le credenziali temporanee e riportare risultato e limiti.
