# Anteprima locale, 11 ottobre 2026

Base: 61b3f4d8168bd24fe685ef8c9d54875be3912798.
Nessuna pubblicazione, nessun push. Backup locale: branch e tag backup-pre-seo-mobile-leggero-20261011.

## Cambiamenti proposti
- Home: quattro numeri disposti 2x2 su telefono, desktop invariato.
- Servizi: etichetta COMPRAVENDUTI leggibile, senza cambiare i valori.
- Immobili: campi ricerca in due colonne su telefono, zona a tutta larghezza.
- Cookie sulle pagine principali: meno spazio verticale, stessi testi, stessi pulsanti e stessa logica. Scorrimento aggiuntivo quando il banner è visibile, per raggiungere anche gli ultimi campi.
- Font: stessi file di origine, stessi pesi e corsivi. Copie con subset latino e simboli, fallback originale per altre scritture. Solo otto pagine principali adottano il nuovo foglio; originali invariati.
- Elenchi Blog e Immobili: otto copie WebP fino a 900 px per le anteprime pesanti. Originali invariati, nessun articolo vecchio modificato.
- Date: contenuti ancora indicati come Marzo 2026, con verifica grafica separata del giorno reale. La data di revisione dei contenuti non viene inventata.
- Regola nuovi articoli in TEST-SKILL/skill-blog-leggero.md, richiamata dall'indice e dalla regola Cursor blog. Soglie più precise, non nuovo design.

## Misure locali, cache nuova
Chrome, 360/390/1280 x 844, non un test su una rete telefonica reale.
- Numeri Home prima fuori dal bordo (-32 fino a 422 px su 390); dopo tutti dentro.
- Ricerca Immobili: altezza circa 598 -> 360 px su 390.
- Banner: circa 122 -> 110 px su 390, altezza pulsanti >=44 px.
- Otto immagini: 1.731.756 -> 725.382 byte, -58%. Risparmio effettivo dipende dalle card caricate durante lo scorrimento.
- Font scaricati: Blog 398.248 -> 277.288 byte; Immobili 416.488 -> 292.948; Servizi 433.324 -> 346.596; Chi siamo 509.692 -> 399.448; Contatti 398.248 -> 319.380. Home circa 324-361 KB prima, 306-334 KB dopo a seconda dei simboli e delle parti visibili. Non promettere 5-6 file o 200 KB: sarebbe cambiamento dell'aspetto o stima non raggiunta.
- Zero overflow orizzontale nelle otto pagine a tutte le larghezze testate.
- Screenshot ispezionati: Home, Servizi, Contatti, Immobili e Blog; carta e RI rimasti visibili.

## Test
- validate-page.js sulle sette pagine pubbliche: tutto OK, prima e dopo.
- Sintassi cookie-consent-main.js e script inline HTML: OK.
- Preferenze cookie aperte e rifiuto non necessari: necessario true, analytics false, marketing false. Nessun invio form reale.
- Filtri Immobili: prezzo e apertura avanzati funzionano. FAQ provate, nessun invio reale.
- Audit generale: identico prima/dopo, 4 errori e 12 avvisi PREESISTENTI. Errori riferiti a admin-kb.html e lunedi-email-report.html; avvisi anche su due articoli e FAQ. Non espandere questa modifica per correggerli.
- Accedi: errori gapiLoaded/gisLoaded preesistenti nel test locale; login non provato, non dichiarato funzionante.
- Verifica completa DB media non eseguita: nessuna chiave amministrativa disponibile né necessaria, e nessun originale/DB modificato.

## Rischi prima della pubblicazione
- Pubblicare anche tutti i nuovi asset, non solo gli HTML: altrimenti font e miniature mancano.
- Confermare che le miniature con testo restino accettabili: le due copertine fumetto sono già dense nell'originale.
- Il banner fisso occupa ancora circa il 13% dello schermo: non può lasciare sempre scoperta ogni zona. I campi sono raggiungibili scorrendo e il banner è chiudibile. Non promettere zero sovrapposizione.
- Le date della grafica andranno cambiate se la pubblicazione avverrà un altro giorno; mantenere distinta la revisione dei contenuti.
- Rebase/confronto con main aggiornato necessario prima di applicare: Gino o altri strumenti possono aver modificato il sito intanto.
- Non certifica tutti i ~200 URL né i singoli annunci/articoli. Archivio blog non corretto, come richiesto.
