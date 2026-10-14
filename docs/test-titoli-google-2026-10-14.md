# Test titoli Google: studenti e rendimento affitti

Data preparazione: 14 ottobre 2026.
Stato iniziale: preparato e approvato per la pubblicazione; la verifica del deploy va registrata quando conclusa.

## Ambito approvato

Solo i campi title e meta description dei due HTML qui sotto. Corpo, H1, immagini, CSS, JavaScript, URL, canonical e date editoriali invariati. Metadati social e dati strutturati non riscritti: sono un test circoscritto, non una revisione dell'articolo.

### Studenti
URL: https://righettoimmobiliare.it/blog-affitto-studenti-padova
- Prima title: Affitto Studenti Padova 2026: Zone, Prezzi e Guida Completa
- Dopo title: Affitto studenti Padova: prezzi, zone e contratti 2026
- Prima description: Affitto per studenti a Padova 2026: zone vicine alle sedi universitarie, prezzi indicativi di stanze singole e doppie, contratti e consigli pratici.
- Dopo description: Cerchi una stanza a Padova? Confronta zone universitarie, prezzi indicativi di singole e doppie, contratti e consigli per cercare casa nel 2026.

### Rendimento
URL: https://righettoimmobiliare.it/blog-rendimento-affitto-padova
- Prima title: Quanto rende affittare a Padova 2026: calcolo quartieri
- Dopo title: Rendimento affitto Padova: come calcolare il netto
- Prima description: Quanto rende affittare casa a Padova e Limena nel 2026? Calcolo rendimento lordo e netto per quartiere e cintura. Guida proprietari Righetto.
- Dopo description: Quanto resta di un affitto a Padova e Limena? Formula del rendimento lordo e netto, costi da sottrarre e confronto tra quartieri per i proprietari.

## Baseline e limiti

Fonte: export Search Console 12 mesi consegnato dal proprietario il 14 ottobre 2026; stesso percorso con e senza www aggregato.
- Studenti: 103 clic, 5.281 impressioni, CTR 1,95%.
- Rendimento: 20 clic, 2.373 impressioni, CTR 0,84%.
- Totale due pagine: 123 clic, 7.654 impressioni.

Non è una baseline degli ultimi 28 giorni. Il file non contiene query per singola pagina. Il CTR annuale non prova che il titolo attuale sia la causa dei pochi clic. Non equiparare clic a utenti, clienti o incarichi. Nessun aumento garantito.

## Backup e ripristino

Commit originale: faf15e6313687bd032d363e735c048d7e4f791eb.
Branch e tag creati prima delle modifiche: backup-pre-ctr-20261014.
Prima del push su main verificare che il riferimento backup sia presente sul remoto.
Per annullare i soli testi: ripristinare i due HTML dal backup in un nuovo commit approvato, senza reset forzati di main. Conservare il registro e la regola di approvazione, salvo nuova istruzione di Gino.

## Istruzioni e registro

Aggiornati CLAUDE.md, indice SKILL-2.0.md, TEST-SKILL/SKILL-2.0.md, TEST-SKILL/skill-essentials.md e regola core Cursor per sostituire le indicazioni contraddittorie di push automatico con prima/dopo, ok di Gino, backup, autorizzazione temporanea e rimozione credenziali. Nessun cambiamento alle automazioni o workflow esistenti.

## Verifiche locali

- git diff --check senza errori.
- Validatore mirato dei due HTML: title/meta entro soglie, H1 unico, canonical e JSON-LD presenti, registrazioni esistenti rilevate.
- Il flag --file nel comando documentato dal repo viene interpretato dal validatore come un nome file inesistente: eseguito nuovamente con i soli percorsi per il controllo corretto.
- Controllo mirato indipendente: corpo HTML e tutti i contenuti diversi dai due campi autorizzati invariati rispetto al backup.
- Nessun invio di moduli, nessun contatto finto e nessun cambiamento estetico. Nessun nuovo controllo visuale dichiarato: il corpo delle pagine è identico byte per byte.

## Seguito

Nel prossimo export già previsto, conservare per ciascuna pagina gli ultimi 28 giorni e le query pertinenti, distinguendo quelle con il marchio dalle altre. Dopo circa 28 giorni dalla rilettura di Google confrontare clic, impressioni e CTR tenendo conto di posizione, stagionalità e cambi di domanda. Non attribuire automaticamente ogni differenza al titolo e non avviare un nuovo riepilogo duplicato.

Riferimenti Google:
- https://developers.google.com/search/docs/appearance/title-link
- https://developers.google.com/search/docs/appearance/snippet

Google può scegliere altri titoli o descrizioni e la rielaborazione può richiedere giorni o settimane.
