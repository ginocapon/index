# Articoli nuovi: leggeri, leggibili, stesso stile

Regola richiesta da Gino l'11 ottobre 2026. Si applica ai PROSSIMI articoli e alle loro anteprime negli elenchi. Nessuna correzione in massa dei vecchi articoli.

## Identità intoccabile

- Carta crepata e marchio R/RI nello scorrimento: non cambiare forma, posizione, trasparenza, animazione o comportamento.
- Nessun nuovo riassetto estetico: stessi colori, font e stile del sito.
- Non togliere pesi o corsivi realmente usati per risparmiare file. Usare font locali e, se già verificato, il foglio `css/fonts-main.css?v=1` con subset e fallback. Non caricare insieme questo foglio e `fonts.css`.

## Immagini: file diversi per usi diversi

- WebP. Non trasformare ogni card in una foto grande da articolo.
- Hero: proporzione 19:9 e sorgente adeguata allo schermo. Target desktop massimo 150 KiB, mobile massimo 80 KiB. Se la qualità non regge, fermarsi e segnalare il motivo, non comprimere alla cieca.
- Card nell'elenco blog: copia dedicata fino a 900 px di larghezza, target massimo 100 KiB. Se servono testi minuti nella grafica, controllare che restino leggibili alla dimensione della card.
- Foto nel corpo: target massimo 120 KiB ciascuna. Dimensioni coerenti con lo spazio reale, eventuali varianti tramite `srcset` e `sizes`.
- Conservare l'originale. Le copie dell'elenco non sostituiscono gli originali negli articoli, nelle schede o nei tour.
- `width` e `height` espliciti; alt descrittivo e pertinente per le foto informative, alt vuoto per elementi davvero decorativi.
- Hero visibile subito: non `loading="lazy"`. Foto sotto la prima schermata: `loading="lazy" decoding="async"`.
- Conservare le indicazioni sulla provenienza delle immagini previste dal sito, senza applicarle a foto reali come se fossero generate.

## Scritture, lettura, grafici

- Riutilizzare i fogli condivisi: `blog-rich.css`, `blog-lead-form.css`, poi `rig-blog-article.css`, con versione. Non aggiungere un nuovo sistema di font per ogni articolo.
- Corpo almeno 16 px, riga ariosa; H1/H2 e testi secondari secondo `skill-design.md` §14.
- Nessun testo tagliato e nessuno scorrimento orizzontale a 360 e 390 px. Numeri in griglia con `minmax(0,1fr)` e figli `min-width:0`.
- Grafici: testo leggibile dentro i box, frecce separate dal testo, note lunghe sotto. Blu/arancione del sito, contrasto sufficiente.
- CTA e campi facilmente utilizzabili da telefono: almeno 44 px per i bersagli; input almeno 16 px.
- Nessuno script pesante aggiuntivo senza motivo. Non ritardare script necessari ai moduli senza controllarne le dipendenze.

## Informazioni precise, non date finte

- Norme, cifre e scadenze: fonti verificate, distinguere fatti da stime. Nessun dato inventato.
- La data dei contenuti cambia solo se i contenuti sono davvero rivisti. Una verifica grafica si indica separatamente.
- Le regole di fonti, qualità, originalità, immagini pertinenti e registrazione nei quattro punti restano valide.
- Queste soglie sostituiscono il vecchio limite generico di 500 KiB per le nuove immagini blog. Non sono un ordine di intervenire sull'archivio.

## Controllo obbligatorio prima di proporre la pubblicazione

1. Test locale a 360, 390 e 1280 px: apertura, scorrimento, FAQ, CTA, moduli senza inviare richieste reali.
2. Guardare screenshot effettivi: carta e RI invariati, testi interi, immagini nitide, grafici e tabelle leggibili.
3. Misurare i file effettivamente scaricati, non solo quelli presenti nella cartella; confrontare prima/dopo con cache vuota.
4. `node scripts/validate-page.js blog-NOME.html` e audit grafico della pagina. Segnalare controlli impossibili o difetti già presenti.
5. Registrare articolo in admin, elenco blog, homepage e sitemap, secondo la procedura esistente.
6. Mostrare a Gino le modifiche. Niente pubblicazione senza il suo ok specifico; questa regola non concede invii, push o attività automatiche.
