# Per Gino — clienti esteri: riassunto e bozza della pagina `/en`

**Documento interno** · 25/11/2026 · **non pubblicare** · nessuna pagina del sito è stata modificata  
**Da approvare:** solo dopo prima/dopo e ok esplicito di Gino

---

## A. Riassunto semplice (da leggere a voce)

### Cosa vogliamo
Allargare l’agenzia ai clienti esteri (soprattutto USA, Germania, Regno Unito, Austria) senza cambiare mestiere e senza creare un sito nuovo.

### Come funziona la visibilità su Google
- Se uno straniero cerca in **inglese** o **tedesco**, Google mostra una pagina **scritta in quella lingua**.
- Se sul nostro sito c’è solo l’italiano, **non usciamo** (o usciamo male) in quelle ricerche.
- Il pulsante per cambiare lingua (come su Green-Acres) è utile, ma **da solo non basta**: serve una pagina dedicata.

### Cosa fare (e cosa no)
- **Sì:** pagine sullo **stesso sito** `righettoimmobiliare.it`, per esempio `/en` e `/de`.
- **No:** nuovi domini (tipo `righetto.com`).
- **No:** redirect automatico «sei americano → ti mando in inglese».
- **No:** tradurre tutto il sito italiano. Bastano poche pagine mirate.

### Struttura proposta
1. **Homepage inglese** `/en` — accoglienza + ricerca + immobili selezionati.
2. **Buy** `/en/buy` — chi vuole comprare.
3. **Sell** `/en/sell` — chi vuole vendere (anche da remoto / eredità).
4. **Rent** `/en/rent` — chi arriva per lavoro o studio.
5. Selettore lingua **IT / EN / DE** su tutte queste pagine.

Buy e Sell sono **separati**: domande diverse, moduli diversi. La homepage EN li presenta entrambi.

### Messaggio
- Agli stranieri: *vi accompagniamo e semplifichiamo le pratiche italiane*.
- Ai proprietari: *chi vende trova in Righetto un alleato* (anche se vive all’estero).
- **Mai** pubblicare tariffe o percentuali. Compenso da concordare in sede.
- Solo claim verificati: 350+ immobili · 101 comuni · 98% soddisfazione · 127 recensioni 4.9/5 · dal 2000.

### Esempi da cui prendere spunto (già guardati)
- Locale simile a noi: [I.V.S (EN)](https://www.immobiliareivs.it/en)
- FAQ per stranieri: [Garda Dream (DE)](https://gardadreamrealestate.com/de/kontakt/)
- Percorso Buy: [Case Bibione To Buy](https://casebibione.it/to-buy/?lang=en)
- Nicchia USA Vicenza: [Schiavo](https://www.schiavorealestate.com/housing-usag-vicenza/)
- Barra di ricerca / lingue: [Green-Acres](https://www.green-acres.it/it)
- Menu Buy–Sell–Rent: [Engel & Völkers Padova EN](https://www.engelvoelkers.com/it/en/shops/padua)

### Prossimo passo (solo se Gino dice sì)
1. Ok su questa bozza di struttura.
2. Bozza grafica prima/dopo (telefono e desktop).
3. Solo dopo: realizzazione HTML, senza pubblicare finché non c’è nuovo ok.

---

## B. Bozza di struttura — pagina `/en`

**URL:** `https://www.righettoimmobiliare.it/en`  
**Title (bozza, ≤60 caratteri):** `Real estate agency in Padua & Veneto | Righetto`  
**Lingua pagina:** `lang="en"` + `hreflang` verso IT (e poi DE)

### 1. Menu in alto (più corto dell’italiano)

Non copiare Blog / FAQ / Servizi dell’homepage italiana.

| Voce | Porta a | Note |
|---|---|---|
| **Buy** | `/en/buy` | Comprare |
| **Sell** | `/en/sell` | Vendere |
| **Rent** | `/en/rent` | Affittare |
| **How it works** | ancora nella `/en` o `/en/how-it-works` | Passi dell’acquisto in Italia |
| **About us** | ancora nella `/en` | Chi siamo, dal 2000 |
| **Contact** | modulo / telefono / WhatsApp | |
| **IT \| EN \| DE** | selettore lingua | Sempre visibile |

### 2. Hero (primo schermo)

- Marchio **Righetto Immobiliare** ben visibile.
- Titolo breve, es.: *Your local ally for buying and selling in Padua & Veneto*.
- Una frase: agenzia dal 2000, Padova e hinterland, assistenza in inglese.
- **Niente** listini, percentuali, numeri inventati.

### 3. Barra di ricerca (stile semplice, tipo Booking / Green-Acres)

Campi:
1. **I want to:** Buy / Sell / Rent  
2. **Area:** Padua · Limena · Vicenza area · Euganean Hills · Other  
3. **Property type:** Apartment · House · Shop / Office · Other  
4. Pulsante **Search**

Comportamento:
- **Buy / Rent** → elenco immobili filtrati (o pagina risultati EN).
- **Sell** → modulo «I want to sell» (non una lista di annunci).

**Se i filtri tecnici non sono ancora pronti:** in prima versione bastano **3 grandi pulsanti** Buy / Sell / Rent; la barra completa arriva dopo.

### 4. Blocchi sotto la ricerca (in ordine)

**Blocco A — Immobili selezionati**  
4–8 annunci con titolo e descrizione in inglese (non tutto il catalogo all’inizio).  
Pulsante: *View all properties*.

**Blocco B — Buy / Sell / Rent (tre card)**  
- **Buy a home** → `/en/buy`  
- **Sell your property** → `/en/sell`  
- **Rent near Padua** → `/en/rent`  

**Blocco C — How buying in Italy works** (5 passi, linguaggio semplice)  
1. Tell us what you need  
2. We shortlist properties  
3. Viewings (also by video)  
4. Offer, notary, contract  
5. After the purchase: help with utilities / rental if needed  

Link: *Read the full guide* (FAQ / articolo EN già esistenti o da fare).

**Blocco D — Why Righetto**  
Solo claim consentiti + «local agency since 2000» + «we guide you through Italian paperwork».  
Niente tariffe.

**Blocco E — Who we help** (scelte tipiche)  
- Expats and families already in Veneto  
- Buyers from USA, UK, Germany, Austria  
- Owners living abroad (including Veneti abroad)  
- Relocating for work or university  

**Blocco F — Meet your contact**  
Foto, nome, lingue parlate, telefono / WhatsApp / email.  
*(Persona da definire con Gino.)*

**Blocco G — Contact form**  
Campi minimi: Name · Email · Country · I want to (Buy / Sell / Rent) · Message · privacy.  
`provenienza` dedicata, es. `estero-en`.

**Blocco H — Footer**  
Indirizzo Limena/Padova · telefono · link IT / EN / DE · privacy · claim AI Act se già presenti sul sito.

### 5. Pagine figlie (solo struttura, non grafiche)

**`/en/buy`**
- Guida breve all’acquisto per stranieri  
- Immobili in vendita (EN)  
- Modulo «I’m looking for a property»  
- Link a FAQ legali (codice fiscale, notary, etc.) senza inventare dati  

**`/en/sell`**
- Messaggio: *selling from abroad — we handle it locally*  
- Cosa facciamo: valuation, listing, viewings, updates remotely  
- Modulo «I want to sell»  
- Collegamento con acquisizione proprietari (alleato di chi vende)  

**`/en/rent`**
- Affitti per chi arriva per lavoro / studio / base Vicenza  
- Immobili in affitto selezionati  
- Modulo «I need a rental»  

### 6. Cosa non mettere nella `/en`
- Menu italiano completo (troppo confusionario)  
- Blog lungo in primo piano (si collega dopo, se serve)  
- Capannoni / grandi fondi  
- Tariffe, percentuali, rendimenti promessi  
- Traduzione automatica di tutto il sito  

### 7. Criteri di ok per Gino (checklist)
- [ ] Struttura menu e blocchi ok  
- [ ] Barra di ricerca ora, oppure solo 3 pulsanti in v1  
- [ ] Persona di riferimento EN definita  
- [ ] Prima/dopo telefono + desktop approvati  
- [ ] Ok esplicito prima di qualsiasi pubblicazione  

---

## C. Collegamento con i documenti già fatti

- Visibilità internazionale: `docs/percorso-visibilita-internazionale-2026-11-16.md`  
- Esempi agenzie: `docs/esempi-agenzie-italiane-clienti-esteri-2026-11-16.md`  
- Target e immobili: `docs/riassunto-target-immobili-clienti-esteri-2026-11-17.md`  
- Questioni legali (base FAQ): `docs/questioni-legali-clienti-esteri-2026-11-16.md`  

Questo file è solo la **bozza da discutere**. Nessuna modifica al sito finché Gino non dà l’ok.
