# Guida sito autobiografico — SEO e Google (semplice)

> **Cos'è questo file:** istruzioni per te e per l'assistente AI (Cursor) quando lavori sul **tuo sito personale** — chi sei, la tua storia, la palestra, contatti, blog.  
> **Cosa fare:** copia tutto in un file `GUIDA-SITO.md` nel progetto del nuovo sito. Compila la sezione 1 una sola volta.

---

## 1. I tuoi dati (compila qui)

```
Nome e cognome:     _________________________________
Nome palestra (se c'è): _____________________________
Sito (dominio):     https://_________________________.it
Città:              _________________________________
Telefono:           _________________________________
Email:              _________________________________
Instagram:          _________________________________
Anno in cui hai iniziato (palestra / carriera): ______
Recensioni Google:  _____ recensioni, voto _____/5
Certificazioni:     _________________________________
```

**Regola importante:** scrivi sul sito **solo cose vere** che puoi dimostrare. Niente «il migliore», «numero 1», numeri inventati.

---

## 2. Che tipo di sito è (autobiografico)

Il sito racconta **te** e quello che fai. Di solito ha queste pagine:

| Pagina | A cosa serve |
|--------|----------------|
| **Home** | Chi sei in 10 secondi + foto + pulsante contatto |
| **Chi sono / La mia storia** | Biografia, percorso, valori, foto |
| **Palestra / Attività** | Cosa offri (corsi, personal, orari) |
| **Contatti** | Indirizzo, mappa, form, telefono |
| **Blog** (opzionale) | Articoli su fitness, vita, consigli |

Ogni pagina deve rispondere a una domanda del visitatore: *«Chi è? Cosa fa? Dove si trova? Come lo contatto?»*

---

## 3. Cosa deve fare l'AI quando modifica il sito

Prima di cambiare qualsiasi file:

1. Leggere il file che va modificato
2. Controllare che funzioni su **telefono** (schermo stretto)
3. Non inventare dati — usare solo la sezione 1
4. Se aggiunge una pagina nuova → metterla in **sitemap.xml**
5. **Commit** solo se tu lo chiedi; **push** solo se lo chiedi esplicitamente

---

## 4. Titolo e descrizione di ogni pagina (Google)

Ogni pagina HTML ha due campi che Google legge:

| Campo | Dove | Quanto lungo |
|-------|------|--------------|
| **Title** | `<title>` | massimo **60 caratteri** (idealmente) |
| **Meta description** | `meta name="description"` | **120–155 caratteri** |

**Esempi per sito autobiografico:**

- **Home title:** `Marco Rossi — Personal trainer Padova | Palestra X`
- **Home meta:** `Sono Marco Rossi, personal trainer a Padova dal 2010. Allenamento su misura, functional e nutrizione. Prenota una prova gratuita.`
- **Chi sono title:** `Chi sono — Marco Rossi, trainer e fondatore Palestra X`
- **Storia title:** `La mia storia — da […] a oggi | Marco Rossi`

**Attenzione:** il title e il titolo H1 della pagina **non devono essere identici** — simili ma diversi.

---

## 5. Testo che piace a Google e alle AI (GEO)

Scrivi così:

1. **Prima frase di ogni sezione** = chiaro e completo da solo  
   *Esempio:* «Marco Rossi è personal trainer certificato CONI a Padova e fondatore della palestra [Nome] dal 2012.»

2. **Titoli H2 a forma di domanda** quando ha senso  
   *Esempio:* «Come posso prenotare una lezione di prova?»

3. **Subito sotto l'H2**, 2–3 frasi che rispondono alla domanda (40–60 parole)

4. **FAQ in fondo pagina** — almeno 5 domande vere (orari, prezzi indicativi se li pubblich, parcheggio, prima lezione…)

5. **Foto tue reali** con testo alternativo descrittivo  
   *Esempio alt:* «Marco Rossi durante un allenamento functional in palestra»

---

## 6. Dati strutturati (Schema) — spiegazione semplice

Sono blocchi invisibili nel codice che dicono a Google *«questo è una persona, questa è una palestra, questo è l'indirizzo»*.

**Sul sito autobiografico servono:**

- **Person** (tu) — pagina Chi sono / bio
- **LocalBusiness** o **SportsActivityLocation** — pagina palestra / contatti
- **FAQPage** — dove ci sono le domande frequenti
- **BreadcrumbList** — «Home > Chi sono» ecc.

L'AI deve inserirli in JSON-LD nel `<head>` o prima di `</body>`. Coordinate GPS reali della palestra se c'è sede fisica.

---

## 7. Google Search Console — cosa fare tu (semplice)

### Setup (una volta sola)
- Aggiungi il sito su https://search.google.com/search-console
- Tipo **Dominio** (es. `tuosito.it`)
- Invia **solo** questa sitemap: `https://tuosito.it/sitemap.xml`  
  **Non** inviare link singoli tipo `/blog` o `/chi-sono` — danno errore.

### Ogni venerdì (15 minuti)

1. **Prestazioni** → guarda quali ricerche portano click (ultimi 28 giorni)
2. **Indicizzazione → Pagine** → quante pagine sono «Indicizzate» vs «Non indicizzate»
3. **Sitemap** → deve dire **Riuscita** / Operazione riuscita
4. **Ispezione URL** (barra in alto) — controlla **solo l'URL ufficiale senza www**:

```
https://tuosito.it/
https://tuosito.it/chi-sono
https://tuosito.it/palestra   (o come si chiama la pagina attività)
https://tuosito.it/contatti
https://tuosito.it/blog
```

Se dice **«URL non presente su Google»** → clic **Richiedi indicizzazione** (max ~10 al giorno).

### Cosa significano i messaggi (in italiano vero)

| Google dice | Cosa vuol dire | Devi preoccuparti? |
|-------------|----------------|---------------------|
| **URL presente su Google** | Ok, la pagina può uscire nelle ricerche | No, bene |
| **Pagina alternativa con canonical** | Hai controllato la versione con **www**; Google usa quella **senza www** | No, normale |
| **Pagina con reindirizzamento** | Google deve rileggere dopo un cambio dominio | Aspetta 1–2 settimane |
| **Scansionata, non indicizzata** | Google ha letto ma non l'ha messa in indice (priorità bassa) | Migliora testo e link interni |
| **404 non trovata** | Pagina che non esiste più | Serve redirect o rimuovere link |

**Non fare:** reinviare pagine singole nella casella «Inserisci URL sitemap».

---

## 8. Google Business Profile (scheda Google Maps)

Se hai palestra o studio con indirizzo:

- **Stesso nome, indirizzo e telefono** del sito (identici, lettera per lettera)
- Foto reali, post ogni settimana, rispondi alle recensioni
- Link al sito = stesso dominio del sito ufficiale

---

## 9. Checklist quando pubblichi una pagina nuova

- [ ] Title ≤ 60 caratteri, meta 120–155 caratteri
- [ ] Un solo H1 (titolo principale)
- [ ] Funziona bene su telefono
- [ ] Pulsante contatto / WhatsApp visibile
- [ ] Almeno 3 link verso altre pagine tue (es. da blog → chi sono → contatti)
- [ ] Pagina aggiunta in **sitemap.xml**
- [ ] Foto con testo alt
- [ ] Niente promesse false («risultati garantiti»)

---

## 10. Blog — se scrivi articoli

**Prima di scrivere un articolo nuovo:** cerca se ne hai già uno uguale sul sito. Non duplicare «come dimagrire» tre volte.

**Un articolo buono ha:**
- titolo chiaro con città o tema se serve localmente
- 1500+ parole utili (non ripetere lo stesso paragrafo)
- la tua firma / bio in fondo con link a Chi sono
- data «ultimo aggiornamento» se modifichi

**Ritmo:** max **1 articolo a settimana** — meglio pochi e buoni.

**Idee per sito autobiografico:**
- La mia storia nel fitness
- Perché ho aperto la palestra
- Cosa aspettarsi dalla prima lezione
- Allenamento a [città]: guida per principianti
- Il mio metodo di lavoro

---

## 11. Cosa chiedere all'AI in Cursor (frasi pronte)

Copia-incolla in chat quando serve:

| Tu scrivi | L'AI fa |
|-----------|---------|
| «Leggi GUIDA-SITO.md e sistemami la pagina chi-sono» | Modifica rispettando questa guida |
| «Controlla title e meta di tutte le pagine» | Audit SEO on-page |
| «Aggiungi FAQ schema su pagina palestra» | JSON-LD + testo visibile |
| «Cosa faccio questo venerdì su Google?» | Checklist §7 |
| «Scrivi articolo blog su [tema] senza inventare dati» | Contenuto + anti-doppioni |
| «Il sito su iPhone si legge male» | Fix mobile |

---

## 12. Piano semplice — prime 4 settimane

| Settimana | Tu fai | AI / sito |
|-----------|--------|-----------|
| **1** | Compila sezione 1; collega Search Console; invia sitemap | Home + Chi sono + Contatti online |
| **2** | Richiedi indicizzazione 5 pagine chiave | Pagina palestra/attività + FAQ |
| **3** | Post su Google Maps + 1 foto | 1 articolo blog o ampliamento storia |
| **4** | Rileggi Prestazioni GSC | Sistemare title delle pagine con 0 click |

Poi ogni **venerdì** ripeti il paragrafo §7.

---

## 13. Errori da evitare

1. Scrivere numeri e percentuali non veri  
2. Inviare `/blog` come sitemap in GSC  
3. Avere sito con **www** e **senza www** entrambi indicizzati senza regole  
4. Testi copiati identici da altri siti  
5. Pagine «Chi sono» vuote o generiche («appassionato di fitness» senza storia)  
6. Nessun modo per contattarti (form, tel, WhatsApp)

---

## 14. File utili da creare nel progetto (opzionale)

```
GUIDA-SITO.md              ← questo file (compilato)
sitemap.xml                ← elenco pagine per Google
data/gsc-note.json         ← appunti venerdì (indicizzate, problemi)
```

**Esempio `data/gsc-note.json`:**

```json
{
  "data": "2026-07-18",
  "pagine_indicizzate": 0,
  "pagine_non_indicizzate": 0,
  "sitemap_ok": true,
  "note": "Prima settimana — richiesta indicizzazione home e chi-sono"
}
```

---

## 15. Riepilogo in 5 righe

1. Sito autobiografico = **tu + storia + attività + contatti**.  
2. Ogni pagina: **title corto, testo chiaro, foto vere, mobile ok**.  
3. Google: **solo sitemap.xml** + **Ispezione URL** per le pagine importanti.  
4. **Venerdì** 15 min in Search Console; **non** panico sui messaggi «reindirizzamento» se hai appena cambiato dominio.  
5. L'AI legge **questo file** e **non inventa** nulla sulla tua vita.

---

*File pronto da copiare nel progetto del sito autobiografico. Adattato da workflow Righetto Immobiliare — versione semplificata luglio 2026.*
