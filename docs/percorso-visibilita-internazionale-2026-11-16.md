# Percorso per farsi conoscere all'estero — sito, portali e canali

**Data:** 16 novembre 2026 · **Obiettivo:** far arrivare all'agenzia contatti dall'estero, oltre alla clientela locale italiana
**Paesi target** (da `ricerca-paesi-settori-esteri-2026-11-16.md`): USA e Germania (priorità 1), poi Austria, Regno Unito e Paesi Bassi
**Budget:** tetto unico di 100 €/mese · **Regola:** ogni modifica al sito si pubblica solo con prima/dopo e ok di Gino

---

## Idea guida

Lo straniero ci trova in tre punti, e il percorso li attiva in quest'ordine:

1. **Sui portali che usiamo già** (Idealista, Immobiliare.it). Molti stranieri cercano lì, con la traduzione del browser ¹. Costo: zero.
2. **Sul nostro sito**, che deve diventare una vetrina in inglese e tedesco trovabile su Google e sugli assistenti AI. Costo: zero, solo lavoro.
3. **Sui portali esteri**, che portano richieste da acquirenti di altri Paesi. Costo: si provano prima quelli con prova gratuita o preventivo basso.

---

## 1. Portali che usiamo già: renderli leggibili per gli stranieri (settimana 1)

| Azione | Dettaglio | Fonte |
|---|---|---|
| **Descrizioni in inglese e tedesco su Idealista** | Gli annunci Idealista possono avere la descrizione in più lingue (inglese, tedesco, olandese e altre) e l'app è in 18 lingue | ² ³ |
| **Annunci scritti per chi non conosce l'Italia** | Spiegare termini come «abitabile» o «rendita catastale», le distanze da aeroporti (Venezia, Treviso, Verona), Venezia, Dolomiti e Lago di Garda, e le foto della zona | ¹ |
| **Etichetta «English spoken / Wir sprechen Englisch»** | Nell'annuncio e nella scheda agenzia | — |
| **Selezione degli immobili** | Prima gli immobili più cercati dagli stranieri in Veneto: case indipendenti e ville con giardino in provincia e sui Colli Euganei, appartamenti in centro a Padova | Ricerca step 1 |

## 2. Il sito ufficiale come vetrina internazionale (settimane 2–6)

### Cosa c'è già

- 4 articoli in inglese, già collegati alle versioni italiane con l'indicazione di lingua per Google (`hreflang`): mercato immobiliare di Padova, contratti d'affitto, affitti per studenti, mercato degli affitti.
- Il file `llms.txt`, letto dagli assistenti AI, che elenca già questi articoli.

### Cosa manca

- Una **pagina principale in inglese** a cui collegare tutto.
- Pagine in **tedesco**: la Germania è priorità 1.
- Le **schede immobile in inglese** (oggi non hanno campi in lingua).
- Un modo per **misurare** i contatti dall'estero.

### Pagine da creare (bozze da approvare con Gino)

| Pagina (URL senza .html) | Lingua | A chi serve | Contenuto |
|---|---|---|---|
| `/en` — *English-speaking real estate agency in Padua & Veneto* | EN | Tutti gli stranieri | Chi siamo (dal 2000, 350+ immobili, 101 comuni, 127 recensioni 4.9/5), zona, servizi per acquirenti esteri, contatti, link alle guide |
| `/buy-property-padua-veneto` | EN | Americani e britannici che comprano | Procedimento d'acquisto per stranieri con i punti del documento legale: codice fiscale, proposta vincolante, notaio, imposte uguali agli italiani, prima casa entro 18 mesi |
| `/rent-near-caserma-ederle-vicenza` | EN | Militari e civili USA | Affitti tra Padova e Vicenza, cosa chiede l'ufficio alloggi, contratti tradotti |
| `/relocating-padua-university-hospital` | EN | Ricercatori, docenti e medici internazionali | Zone vicine all'università e all'ospedale, contratti, tempi |
| `/de` — *Immobilien in Venetien kaufen* | DE | Tedeschi e austriaci | Versione tedesca della pagina principale |
| Schede immobile in inglese | EN | Chi arriva dai portali esteri | Per gli immobili selezionati: titolo e descrizione in inglese, stesso modulo contatti |

### Regole tecniche (stack attuale, nessun cambio)

- HTML, CSS e JS vanilla. Ogni pagina con `lang="en"` o `lang="de"` e `hreflang` reciproco verso la versione italiana, come già fatto nei 4 articoli.
- Title di massimo 60 caratteri e meta description di massimo 160, nella lingua della pagina. Controllo con `node scripts/validate-page.js`.
- Nuove URL in `sitemap.xml` e una sezione «English / Deutsch» in `llms.txt`.
- **Modulo contatti con un campo «Paese»** e provenienza dedicata (per esempio `provenienza: estero-en` o `estero-de`), per contare i contatti dall'estero nel pannello admin.
- Nessuna tariffa pubblicata e solo i claim consentiti.

### Contenuti (dopo il lancio)

- **1 guida al mese in inglese**, alternata con una in tedesco, che risponda a domande vere degli stranieri. Esempi: *«Buying a house in Italy as an American: costs and steps in the Veneto»*, *«Second home near Venice and the Dolomites: Padua province»*, *«Ferienhaus in den Euganeischen Hügeln kaufen»*.
- Si traducono prima gli articoli italiani che hanno già traffico, sempre con dati e fonti.

### Google

- **Google Business Profile:** post periodici in inglese e risposte in inglese alle recensioni dei clienti stranieri.
- **Search Console:** controllare ogni mese il rapporto per **Paese** (clic da USA, Germania, Regno Unito, Austria, Paesi Bassi) sulle nuove pagine.

## 3. Portali esteri: dove iscriversi (settimane 3–12)

| Portale | Per chi | Come funziona per un'agenzia italiana | Costo e accesso | Priorità |
|---|---|---|---|---|
| **Gate-away.com** | Tutti (dal 2008, solo acquirenti esteri) | Pacchetti in abbonamento, 10 lingue, richieste da 150 Paesi. Traduce in automatico annunci e messaggi. Si collega ai gestionali immobiliari | Su preventivo, **senza rinnovo automatico** ⁴ ⁵ | **1 — chiedere un preventivo subito** |
| **Green-Acres** | Paesi Bassi (12% dei visitatori), Germania (11%), Regno Unito (10%), Belgio (9%), USA (7%) | Registrazione agenzia, annunci tradotti in automatico, il 70% dei visitatori è straniero | **Prova gratuita di 30 giorni** per le agenzie ⁶ ⁷ | **1 — attivare la prova** |
| **Rightmove Overseas** | Regno Unito | Modulo per agenti esteri, poi chiamata di un account manager (3–5 giorni lavorativi), verifica d'identità e pagamento. 26 milioni di visite l'anno per immobili all'estero | Abbonamento su preventivo ⁸ ⁹ | 2 — dopo il test |
| **ImmoScout24** (sezione estero) | Germania e Austria | Accetta immobili in Italia, ma servono un'inserzione in tedesco e qualcuno che risponda in tedesco ogni giorno. Spesso si passa da un intermediario o da un agente tedesco partner, che trattiene parte del compenso | Abbonamento tedesco o intermediario ¹⁰ ¹¹ | 2 — solo con un partner tedesco |
| **JamesEdition** | Acquirenti di fascia alta | Agenzia con sede fisica e licenza. Solo immobili residenziali **da 490.000 $** in su | Abbonamento «Elite» e promozioni del singolo annuncio di 7, 15 o 30 giorni ¹² ¹³ | 3 — solo se c'è un immobile di pregio |
| **Funda** (Paesi Bassi) | Olandesi | Un agente estero non può pubblicare direttamente. L'intermediario trovato oggi non copre l'Italia | — ¹⁴ | Per ora no: per gli olandesi si usa Green-Acres |
| **ListGlobally** | Generico | Pubblica su oltre 90 portali, ma l'esperienza riportata indica visibilità bassa per le piccole agenzie | Abbonamento ¹⁵ | No |

**Come si decide:** per 8 settimane si confrontano Gate-away (se il preventivo rientra) e Green-Acres (prova gratuita) sugli stessi immobili. Si tiene quello che porta più **contatti veri**, cioè videochiamate fatte e non solo email.

## 4. Elenchi e reti dove lo straniero cerca un agente (in parallelo, costo quasi zero)

| Canale | Perché | Fonte |
|---|---|---|
| **Elenco NAR «Find a REALTOR® Worldwide»** | Agenti e clienti USA cercano lì un agente all'estero. Righetto **non è associata FIAIP**. Le strade sono due: associarsi a **OID** (Osservatorio Immobiliare Digitale, l'altro partner NAR in Italia) per diventare REALTOR® con il profilo nell'elenco, oppure iscriversi direttamente come *subscriber*, senza marchio REALTOR®. Quote da chiedere | ¹⁶ ¹⁷ ¹⁹ ²⁰ |
| **Guide «agenti in Italia» dei portali** | Idealista pubblica articoli in inglese con elenchi di agenzie per regione | ¹⁸ |
| **InterNations e gruppi expat di Padova** | Profilo e presenza agli eventi | Documento procedimento |
| **Ufficio alloggi USAG Vicenza e Cerco Alloggio dell'Università di Padova** | Stranieri già sul posto | Documento procedimento |

## 5. Calendario di attivazione (12 settimane)

| Settimane | Azione | Costo |
|---|---|---|
| 1 | Descrizioni EN/DE su Idealista per 5–10 immobili adatti. Etichetta «English spoken». Richiesta quote a OID e a NAR (subscriber) | 0 € |
| 1 | Richiesta preventivo Gate-away. Registrazione Green-Acres con prova di 30 giorni | 0 € |
| 2–3 | Bozze delle pagine `/en`, `/buy-property-padua-veneto` e `/de`, poi prima/dopo (telefono e desktop) a Gino | 0 € |
| 3–4 | Dopo l'ok di Gino: pubblicazione, `sitemap.xml`, `llms.txt`, campo «Paese» nel modulo | 0 € |
| 4–6 | Pagine Caserma Ederle e università. Schede in inglese degli immobili selezionati | 0 € |
| 5–12 | Test Gate-away + Green-Acres sugli stessi immobili. Una guida al mese EN/DE. Post in inglese su Google | Dentro i 100 € |
| 12 | Valutazione: contatti dall'estero per canale, clic per Paese da Search Console, videochiamate, incarichi. Si tiene un portale e si valuta Rightmove o ImmoScout24 | — |

**Numeri da guardare ogni mese:** contatti dall'estero per canale (sito, Idealista, Gate-away, Green-Acres, NAR), Paese di provenienza, videochiamate e incarichi.

---

## Fonti

1. Barbara Bersini, «Dove cercano casa gli stranieri?»: https://www.yourhouseinitaly.com/it/dove-cercano-casa-gli-stranieri-molto-piu-vicino-di-quanto-pensi/
2. Esempio di annuncio Idealista multilingua: https://www.idealista.it/immobile/30538570/
3. App Idealista, lingue: https://apps.apple.com/do/app/idealista/id465958311
4. Gate-away, servizi per agenzie: https://it.gate-away.com/advertise_with_us_it_agenzie.php
5. Gate-away, vendere a stranieri: https://it.gate-away.com/advertise_with_us_it.php
6. Green-Acres, area professionisti: https://www.green-acres.it/it/pro
7. Green-Acres, registrazione agenzia: https://www.green-acres.it/it/Register/Agency
8. Rightmove Overseas per agenti: https://www.rightmove.co.uk/overseas-property/advertise/estate-agent.html
9. Rightmove, come iscriversi da agente estero: https://customerfaq.rightmove.co.uk/support/solutions/articles/7000048731-how-to-join-rightmove-as-an-overseas-estate-agent
10. ImmoScout24, immobili internazionali (API): https://api.immobilienscout24.de/api-docs/import-export/real-estate/international-real-estates/
11. Crosslist, pubblicare su ImmoScout24 dall'estero: https://crosslist.eu/guides/list-on-immoscout24-from-abroad
12. JamesEdition, requisiti venditori: https://help.jamesedition.com/en/what-are-the-requirements-to-become-a-seller-on-jamesedition
13. JamesEdition, area professionisti: https://www.jamesedition.com/professional_seller/real_estate
14. Immo Connect Europe (Funda per agenti esteri): https://immoconnecteurope.com/nl/
15. Recensione di ListGlobally: https://francescocolarieti.com/2019/11/23/listglobally-recensione-sul-portale-immobiliare-mondiale/
16. NAR, membri internazionali: https://www.nar.realtor/global/international-realtor-membership
17. FIAIP, mercati esteri: https://www.fiaip.it/estero/
18. Idealista, come trovare un agente in Italia (EN): https://www.idealista.it/en/news/property-sale-italy/2022/12/20/2157-5-tips-and-tricks-finding-best-estate-agent-italy
19. NAR, requisiti e domanda di iscrizione (anche *subscriber*): https://payment.apps.realtor/irm
20. OID, domande frequenti (iscrizione NAR tramite OID): https://www.osservatorioimmobiliaredigitale.it/faq.php
