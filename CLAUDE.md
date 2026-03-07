# CLAUDE.md — Istruzioni per lo sviluppo

## Regole per la pubblicazione di articoli blog

Quando si crea un nuovo articolo blog (file HTML), bisogna **sempre** registrarlo in tutti e tre i punti seguenti, altrimenti non comparira' nel sito:

1. **`admin.html`** — array `_blogSeedArticles` (circa riga 6115): aggiungere l'oggetto articolo con titolo, categoria, data, tempo, stato, autore, emoji, immagine_copertina, url_statico, contenuto, evidenza
2. **`blog.html`** — array `articoliStatici` (circa riga 305): aggiungere l'oggetto articolo con gli stessi dati
3. **`js/homepage.js`** — due punti:
   - `staticMap` (circa riga 331): aggiungere la chiave (titolo in minuscolo) con img e url
   - `articoliStatici` (circa riga 347): aggiungere l'oggetto articolo

### Checklist verifica pubblicazione

Dopo ogni push di nuovi articoli, verificare che:
- [ ] Il file HTML dell'articolo esiste nella root
- [ ] L'articolo e' presente in `admin.html` `_blogSeedArticles`
- [ ] L'articolo e' presente in `blog.html` `articoliStatici`
- [ ] L'articolo e' presente in `js/homepage.js` `staticMap`
- [ ] L'articolo e' presente in `js/homepage.js` `articoliStatici`
- [ ] L'articolo e' presente in `sitemap.xml`
- [ ] L'articolo compare nell'admin panel come "Pubblicato"
- [ ] L'articolo compare nella pagina blog del sito

### Struttura dati articolo

```javascript
{
  titolo: 'Titolo Articolo',
  categoria: 'Categoria',       // es: 'Guida alla vendita', 'Consigli acquisto', 'Affitti', 'Fisco', 'Normativa', 'Mercato locale'
  data: '2026-03-07',           // formato ISO
  tempo: 10,                    // minuti di lettura
  stato: 'pubblicato',          // oppure 'bozza'
  autore: 'Gino Capon',
  emoji: '📋',                  // solo in admin.html
  immagine_copertina: 'img/...',
  url_statico: 'blog-nome-articolo',  // senza .html
  contenuto: '<p>Descrizione breve...</p>',  // in admin.html, testo breve in blog.html
  evidenza: true                // articolo in evidenza o no
}
```

## Link partner

Quando si aggiungono link a partner esterni, usare sempre `rel="noopener"` e `target="_blank"`.
Partner attivi:
- serviziimmobiliaripadova.it
- raasautomazioni.it
