# SKIMM — Blog Keyword & Intent Map (Righetto)

> **Generato:** 2026-07-03 · Script: `python scripts/build_skimm.py`
> **Uso:** prima di ogni nuovo articolo — anti-doppioni semantici + keyword per «bucare» Google senza cannibalizzare.
> **Companion:** `check_doppioni_sito.py` (tecnico) + `skill-content.md` §2.0–2.2 + `SKILL-2.0.md` §8.1a.

---

## 1. Programma regole interne (anti-doppioni + SEO)

### 1.1 Flusso obbligatorio nuovo articolo

1. Leggere **§3 catalogo** e **§4 matrice rischi** di questo file.
2. Eseguire `python scripts/check_doppioni_sito.py` (slug/titolo/canonical).
3. Eseguire `python scripts/build_skimm.py --check "slug-proposto" "kw-primaria" "cluster"` (se implementato) o verificare manualmente §3.
4. Se overlap → **STOP** → nuovo angolo + fonte istituzionale (OMI, BCE, ISTAT, FIMAA, ADE…).
5. Pubblicare con: `kw_primaria` unica · H2 domanda diverse · sezione **Cosa può fare Righetto** · foto realistiche.

### 1.2 Come «bucare» Google senza doppioni

| Strategia | Cosa fare | Esempio buono | Esempio da evitare |
|---|---|---|---|
| **Long-tail datato** | Ancorare a evento/fonte con data | `bce-giugno-2026-tassi-mutui` | Secondo «mutui 2026» generico |
| **Entità nominale** | Nome progetto/luogo univoco | `tribloc-gozzi-nzeb` | Altro «residenze green padova» |
| **Intent diverso** | Stesso tema, pubblico diverso | Checklist contratto vs dato canoni | Due guide affitto studenti |
| **Geografia variata** | Cambiare città o scala | `casa-querini-vicenza` | Terzo articolo solo «Padova studenti» |
| **Dato vs normativa vs operativo** | Un solo tipo per URL | FIMAA Q1 (dato) / decreto 66 (norma) / checklist (azione) | FIMAA + Insights nello stesso pezzo come pillar |

### 1.3 Regole slug (batch e singoli)

- **Max 2 slug** nello stesso batch con la stessa radice (`padova`, `veneto`, `2026`, `studenti`, `residenze`).
- **Keyword primaria** (colonna §3) **univoca** in tutto il catalogo.
- Slug pattern: `blog-{entità-o-dato}-{località-opzionale}-{anno-opzionale}` — preferire **entità** (`tribloc-gozzi`, `casa-querini`, `edilcassa-garanzia`) a aggettivi generici (`housing`, `residenze-universitarie`).
- **Anno nel slug** solo per articoli **legati a evento** (BCE meeting, bando, Q1 FIMAA). Guide evergreen **senza** anno in URL.
- **Non** cambiare slug live senza 301 + sitemap.

### 1.4 Keyword secondarie (title/H2/meta)

- Title: 1 keyword primaria + localizzazione + **hook numerico** se c'è fonte.
- H2: domande AEO **non copiate** da altri articoli dello stesso cluster.
- Meta description: dato verificabile + beneficio + implicit CTA.
- `article:tag`: 3–5 tag, **nessuno** già usato come `kw_primaria` di un altro articolo.

### 1.5 Cluster COMPLETI — gap consentiti

Cluster segnati COMPLETO in `skill-content.md` §1: nuovo articolo solo se:

- nuova **fonte/dato** (trimestre OMI, comunicato BCE, bando ESU), oppure
- nuova **entità** (progetto, norma, quartiere), oppure
- nuovo **intent** (checklist, confronto, corporate B2B).

### 1.6 Prossimi articoli — keyword ancora libere (opportunità)

- `affitto-transitorio-padova-durata-massima` (normativa, non duplica contratto-affitto)
- `imu-seconda-casa-padova-2026` (fisco possesso, distinto da costi-proprieta)
- `studentato-esu-bando-2026-27` (evento bando, distinto da posti-letto sistemico)
- `rubano-limena-affitto-lavoratori-cantiere` (B2B locale, distinto da edilcassa)
- `mestre-affitti-studenti-ca-foscari` (geografia diversa da Padova)

---

## 2. Stato verifica automatica

**15 avvisi** al generazione 2026-07-03:

- Intent simile `acquisto-e-prima-casa`: blog-agevolazioni-prima-casa-2026, blog-ape-prestazione-energetica-acquisto-padova-2026, blog-caparra-confirmatoria-padova, blog-checklist-verifiche-prima-compromesso-padova-2026…
- Intent simile `affitti-e-locazioni`: blog-affitto-breve-padova-2026, blog-emergenza-abitativa-padova-2026, blog-quotazioni-locazioni-omi-istat-padova-2026, blog-righetto-bilancio-2025-soluzioni-affitto-2026…
- Intent simile `fisco-e-normativa`: blog-bonus-edilizi-2026-incentivi-casa-padova, blog-bonus-mobili-2026-massimizzare-ristrutturazioni, blog-condono-edilizio-proposte-2026, blog-piano-casa-decreto-66-2026-padova
- Intent simile `investimenti`: blog-investire-immobiliare-padova, blog-trend-investimenti-immobiliari-summit-2026
- Intent simile `mercato-e-dati`: blog-bolla-immobiliare-padova-2026, blog-case-piu-vendute-tipologie-padova-2026, blog-compravendite-italia-q1-agenzia-entrate-2026-padova, blog-compravendite-padova-record-2026…
- Intent simile `mutui-e-credito`: blog-barometro-mutui-crif-padova-2026, blog-geopolitica-ucraina-prezzi-mutui-italia-veneto-2026, blog-immobiliare-geopolitica-energia-tassi-2026, blog-mutui-casa-padova-2026…
- Intent simile `servizi-e-istituzionale`: blog-permuta-immobiliare-padova-2026, blog-scegliere-agenzia-immobiliare-padova-2026, blog-successione-immobiliare-padova
- Intent simile `territorio-e-zone`: blog-appartamento-nuova-costruzione-limena, blog-direttiva-case-green-limena-padova, blog-quartieri-padova-2026, blog-scuole-istruzione-padova…
- Intent simile `vendita`: blog-casa-vendibile-5-anni-case-green-padova-2026, blog-case-vendita-padova, blog-costi-vendere-casa-padova-2026, blog-documenti-compravendita-rogito-padova-2026…
- Intent simile `vita-d'agenzia`: blog-agenzia-immobiliare-top-servizi-padova-2026, blog-ca-marcello-mestre, blog-impegno-quotidiano-agenzia-immobiliare, blog-righetto-storia-territorio-acquisizioni-2026…
- Token slug sovrausato `mercato` (9 articoli) — variare radice nei prossimi batch
- Coppia da non fondere (Insights 490 vs pillar +8%): blog-stanza-universitaria-padova-canoni-2026 ↔ blog-affitti-padova-canoni-2026
- Coppia da non fondere (Insights vs FIMAA Q1): blog-stanza-universitaria-padova-canoni-2026 ↔ blog-affitti-canoni-fimaa-q1-2026-padova
- Coppia da non fondere (Tribloc vs Case Green generico): blog-residenze-green-padova-tribloc-2026 ↔ blog-domanda-case-green-certificazione-padova-2026
- Coppia da non fondere (Evento BCE vs guida mutui): blog-bce-tassi-mutui-giugno-2026-padova ↔ blog-mutui-casa-padova-2026

**Articoli catalogati:** 99

---

## 3. Catalogo completo per cluster

### Acquisto e prima casa (14)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-agevolazioni-prima-casa-2026` | `agevolazioni-prima-casa` | Angolo da definire — verificare overlap cluster (Agevolazioni Prima Casa 2026: Bonus e Requisiti) |
| `blog-ape-prestazione-energetica-acquisto-padova-2026` | `ape-prestazione-energetica-acquisto` | Angolo da definire — verificare overlap cluster (APE e prestazione energetica nell'acquisto di casa nel Padov) |
| `blog-caparra-confirmatoria-padova` | `caparra-confirmatoria` | Angolo da definire — verificare overlap cluster (Caparra Confirmatoria: Guida Completa Compravendita Padova) |
| `blog-checklist-verifiche-prima-compromesso-padova-2026` | `checklist-verifiche-prima-compromesso` | Angolo da definire — verificare overlap cluster (Checklist verifiche prima del compromesso a Padova 2026: doc) |
| `blog-comprare-affittare-padova` | `comprare-affittare` | Angolo da definire — verificare overlap cluster (Comprare o Affittare Casa a Padova? Analisi Dati Reali su 20) |
| `blog-comprare-casa-padova-guida-2026` | `comprare-casa-guida` | Angolo da definire — verificare overlap cluster (Comprare Casa a Padova nel 2026: Guida Definitiva Passo dopo) |
| `blog-costi-proprieta-acquisto-possesso-vendita-padova-2026` | `costi-proprieta-acquisto-possesso-vendita` | Angolo da definire — verificare overlap cluster (Costi proprietà immobiliare Padova 2026: acquisto, possesso,) |
| `blog-dieci-errori-acquisto-casa-padova-2026` | `dieci-errori-acquisto-casa` | Angolo da definire — verificare overlap cluster (Dieci errori da evitare nell'acquisto casa a Padova 2026) |
| `blog-limena-vicino-padova-comprare-2026` | `limena-vicino-comprare` | Angolo da definire — verificare overlap cluster (Limena e dintorni di Padova: perché comprare vicino al capol) |
| `blog-limena-vs-padova-centro-dove-comprare-2026` | `limena-centro-dove-comprare` | Angolo da definire — verificare overlap cluster (Limena o Centro Padova? Dove Comprare Casa nel 2026: Confron) |
| `blog-planimetria-catastale-compravendita-padova-2026` | `planimetria-catastale-compravendita` | Angolo da definire — verificare overlap cluster (Planimetria catastale e compravendita nel Padovano: controll) |
| `blog-quattro-imposte-rogitio-prima-casa-padova-2026` | `quattro-imposte-rogitio-prima-casa` | Angolo da definire — verificare overlap cluster (Le quattro imposte al rogito prima casa a Padova 2026: IVA, ) |
| `blog-scegliere-immobile-giusto-padova-2026` | `scegliere-immobile-giusto` | Angolo da definire — verificare overlap cluster (Come scegliere l'immobile giusto a Padova 2026: zona, luce, ) |
| `blog-vigonza-rubano-comprare-casa-cintura-2026` | `vigonza-rubano-comprare-casa-cintura` | Angolo da definire — verificare overlap cluster (Vigonza e Rubano: guida all'acquisto nella cintura del capol) |

### Affitti e locazioni (15)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-affitti-canoni-fimaa-q1-2026-padova` | `fimaa-q1-2026-canoni-veneto` | Rilevazione trimestrale FIMAA — non Insights 490€ |
| `blog-affitti-padova-canoni-2026` | `affitti-padova-canoni-trend-2026` | Pillar canoni città +8% — non stanza singola Insights |
| `blog-affitto-breve-padova-2026` | `affitto-breve` | Angolo da definire — verificare overlap cluster (Affitto Breve a Padova 2026: Rendimenti, Regole e Opportunit) |
| `blog-affitto-studenti-padova` | `guida-affitto-studenti-padova` | Guida evergreen zone/contratti — non dato anno |
| `blog-checklist-affitto-studenti-padova-2026` | `checklist-contratto-studenti-padova` | Checklist operativa caparra/contratto — non mercato |
| `blog-contratto-affitto-padova` | `contratto-affitto-tipologie-padova` | 4+4, 3+2, transitorio, cedolare — normativa |
| `blog-emergenza-abitativa-padova-2026` | `emergenza-abitativa` | Angolo da definire — verificare overlap cluster (Emergenza Casa Padova 2026: Dati, Cause e Possibili Soluzion) |
| `blog-housing-lavoratori-veneto-edilcassa-2026` | `edilcassa-fondo-garanzia-locazione-lavoratori` | Fondo 250k€ garanzie affitto operai — non studenti né canoni |
| `blog-quotazioni-locazioni-omi-istat-padova-2026` | `quotazioni-locazioni-omi-istat` | Angolo da definire — verificare overlap cluster (Quotazioni e locazioni Padova: OMI e monitor ISTAT senza imp) |
| `blog-rendimento-affitto-padova` | `rendimento-locativo-quartieri-padova` | Yield % per quartiere investitori |
| `blog-righetto-bilancio-2025-soluzioni-affitto-2026` | `righetto-bilancio-soluzioni-affitto` | Angolo da definire — verificare overlap cluster (Righetto Immobiliare: bilancio 2025 e soluzioni affitto 2026) |
| `blog-squilibrio-domanda-offerta-affitti-padova` | `squilibrio-domanda-offerta-affitti` | Angolo da definire — verificare overlap cluster (Affitti Padova: Perch&eacute; la Domanda Supera l'Offerta ne) |
| `blog-stanza-universitaria-padova-canoni-2026` | `canone-stanza-insights-490-padova` | Dato Immobiliare.it Insights (+46% vs 2020) e periferie tram — non FIMAA Q1 |
| `blog-studentati-veneto-2026-posti-letto` | `posti-letto-esu-camplus-pnrr-veneto` | Canali offerta regionale (ESU/privati/PNRR) — non singolo canone stanza |
| `blog-vicenza-residenze-universitarie-calmierate-2026` | `casa-querini-calmierati-vicenza` | Vicenza PNRR Saudino — non Padova né Tribloc |

### Altri / trasversali (1)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-gestione-spese-casa-risparmio-padova-2026` | `gestione-spese-casa-risparmio` | Angolo da definire — verificare overlap cluster (Gestione spese casa dopo l'acquisto a Padova 2026: energia, ) |

### Fisco e normativa (4)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-bonus-edilizi-2026-incentivi-casa-padova` | `bonus-edilizi-incentivi-casa` | Angolo da definire — verificare overlap cluster (Bonus edilizi 2026 Padova: detrazioni 50% e ecobonus) |
| `blog-bonus-mobili-2026-massimizzare-ristrutturazioni` | `bonus-mobili-massimizzare-ristrutturazioni` | Angolo da definire — verificare overlap cluster (Bonus mobili e grandi elettrodomestici 2026: massimizzare la) |
| `blog-condono-edilizio-proposte-2026` | `condono-edilizio-proposte` | Angolo da definire — verificare overlap cluster (Condono edilizio 2026: proposte in Manovra / Guida Padova) |
| `blog-piano-casa-decreto-66-2026-padova` | `piano-casa-decreto` | Angolo da definire — verificare overlap cluster (Piano Casa DL 66/2026: impatto su Padova) |

### Investimenti (2)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-investire-immobiliare-padova` | `investire-immobiliare` | Angolo da definire — verificare overlap cluster (Investire in Immobili a Padova 2026: Guida Rendimenti) |
| `blog-trend-investimenti-immobiliari-summit-2026` | `trend-investimenti-immobiliari-summit` | Angolo da definire — verificare overlap cluster (Investimenti immobiliari 2026: trend da Real Estate Summit /) |

### Macro e geopolitica (2)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-eurocamera-accordo-dazi-usa-2026` | `eurocamera-accordo-dazi-sunset-2029` | Accordo istituzionale EU-USA — non filiera padovana |
| `blog-patrimonio-casa-resilienza-mercati-globali-2026` | `patrimonio-casa-resilienza-mercati-globali` | Angolo da definire — verificare overlap cluster (Patrimonio casa e resilienza urbana: lezioni dal contesto gl) |

### Mercato e dati (20)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-bolla-immobiliare-padova-2026` | `bolla-immobiliare` | Angolo da definire — verificare overlap cluster (Bolla Immobiliare a Padova nel 2026? Analisi dei Rischi Real) |
| `blog-case-piu-vendute-tipologie-padova-2026` | `case-piu-vendute-tipologie` | Angolo da definire — verificare overlap cluster (Case più vendute a Padova: tipologie e metrature 2026) |
| `blog-compravendite-italia-q1-agenzia-entrate-2026-padova` | `compravendite-agenzia-entrate` | Angolo da definire — verificare overlap cluster (Compravendite Q1 2026: dati ADE e Padova) |
| `blog-compravendite-padova-record-2026` | `compravendite-record` | Angolo da definire — verificare overlap cluster (Compravendite Padova 2026: Anno Record) |
| `blog-compravendite-veneto-cintura-padova-2026` | `compravendite-cintura` | Angolo da definire — verificare overlap cluster (Compravendite Veneto e cintura Padova: lettura dati territor) |
| `blog-costi-costruzione-istat-padova-2026` | `costi-costruzione-istat` | Angolo da definire — verificare overlap cluster (Costi costruzione ISTAT marzo 2026: +0,8% mensile, indice 11) |
| `blog-crisi-immobiliare-padova-2026` | `crisi-immobiliare` | Angolo da definire — verificare overlap cluster (Crisi Immobiliare Padova 2026: Prezzi e Compravendite) |
| `blog-dazi-usa-ue-mercato-padova-2026` | `dazi-usa-ue-filiera-veneto-padova` | Impatto occupazione/credito Padova — non cronaca Strasburgo |
| `blog-mercato-immobiliare-limena-2026` | `mercato-immobiliare-limena` | Angolo da definire — verificare overlap cluster (Mercato Immobiliare Limena 2026: Guida OMI, Territorio e Val) |
| `blog-mercato-immobiliare-padova-2026` | `mercato-immobiliare` | Angolo da definire — verificare overlap cluster (Mercato Immobiliare Padova 2026: Prezzi, Tendenze e Previsio) |
| `blog-mercato-immobiliare-padova-centro-2026` | `mercato-immobiliare-centro` | Angolo da definire — verificare overlap cluster (Immobili Centro Storico Padova 2026: Prezzi, Rendimenti e An) |
| `blog-mercato-immobiliare-piazzola-sul-brenta-2026` | `mercato-immobiliare-piazzola-sul-brenta` | Angolo da definire — verificare overlap cluster (Mercato immobiliare a Piazzola sul Brenta nel 2026: come leg) |
| `blog-mercato-italiano-tensioni-medio-oriente-2026` | `mercato-italiano-tensioni-medio-oriente` | Angolo da definire — verificare overlap cluster (Tensioni in Medio Oriente e mercato immobiliare italiano: ca) |
| `blog-mercato-sacrocuore-padova-omi-2026` | `mercato-sacrocuore-omi` | Angolo da definire — verificare overlap cluster (Mercato Immobiliare Sacro Cuore Padova 2026: Guida OMI Zona ) |
| `blog-nuove-costruzioni-mercato-veneto-2026-padova` | `nuove-costruzioni-mercato` | Angolo da definire — verificare overlap cluster (Nuove costruzioni Veneto 2026: +14,6% e cintura PD) |
| `blog-previsioni-immobiliari-scenari-geopolitica-2026` | `previsioni-immobiliari-scenari-geopolitica` | Angolo da definire — verificare overlap cluster (Previsioni immobiliari e scenari di conflitto: come usarle s) |
| `blog-prezzi-case-padova-zona-2026` | `prezzi-case-zona` | Angolo da definire — verificare overlap cluster (Prezzi Case Padova 2026 Zona per Zona: Mappa Completa e Prev) |
| `blog-prezzi-padova-provincia-fiaip-2026` | `prezzi-provincia-fiaip` | Angolo da definire — verificare overlap cluster (Prezzi case Padova 2026: -4% in città, provincia traina / FI) |
| `blog-prospettive-mercato-residenziale-italia-2026` | `prospettive-mercato-residenziale` | Angolo da definire — verificare overlap cluster (Prospettive mercato residenziale Italia: come leggere le ric) |
| `blog-sondaggio-bancaditalia-q1-2026-padova` | `sondaggio-bancaditalia` | Angolo da definire — verificare overlap cluster (Sondaggio abitativo Banca d'Italia Q1 2026: LTV 77,2% e mutu) |

### Mutui e credito (12)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-barometro-mutui-crif-padova-2026` | `barometro-mutui-crif` | Angolo da definire — verificare overlap cluster (Barometro mutui CRIF Q1 2026: domanda -12,4%, importo medio ) |
| `blog-bce-tassi-mutui-giugno-2026-padova` | `bce-giugno-2026-tassi-mutui` | Decisione BCE giugno +25bp — evento datato |
| `blog-geopolitica-ucraina-prezzi-mutui-italia-veneto-2026` | `geopolitica-ucraina-prezzi-mutui` | Angolo da definire — verificare overlap cluster (Geopolitica, energia e mutui: effetti possibili su case nel ) |
| `blog-immobiliare-geopolitica-energia-tassi-2026` | `immobiliare-geopolitica-energia-tassi` | Angolo da definire — verificare overlap cluster (Geopolitica, energia e tassi: effetti sul mercato immobiliar) |
| `blog-mutui-casa-padova-2026` | `mutui-casa` | Angolo da definire — verificare overlap cluster (Mutui Casa a Padova 2026: Tassi Aggiornati e Migliori Offert) |
| `blog-mutui-selettivi-banche-padova-2026` | `mutui-selettivi-banche` | Angolo da definire — verificare overlap cluster (Mutui più selettivi: come le banche valutano reddito e garan) |
| `blog-mutui-tasso-fisso-bancaitalia-padova-2026` | `mutui-tasso-fisso-bancaitalia` | Preferenza fisso vs variabile BdI — non BCE singolo meeting |
| `blog-mutuo-documenti-tempi-prima-casa-padova-2026` | `mutuo-documenti-tempi-prima-casa` | Angolo da definire — verificare overlap cluster (Mutuo prima casa a Padova: documenti, tempi e sequenza dal p) |
| `blog-mutuo-fisso-variabile-padova-2026` | `mutuo-fisso-variabile` | Angolo da definire — verificare overlap cluster (Mutuo Tasso Fisso o Variabile nel 2026? Guida alla Scelta a ) |
| `blog-mutuo-prima-casa-padova` | `mutuo-prima-casa` | Angolo da definire — verificare overlap cluster (Mutuo Prima Casa Padova 2026: Guida Completa, Tassi e Requis) |
| `blog-surroga-mutuo-padova-2026` | `surroga-mutuo` | Angolo da definire — verificare overlap cluster (Surroga Mutuo 2026: Quando Conviene e Come Risparmiare a Pad) |
| `blog-tassi-mutui-minimi-approfittarne-padova-2026` | `tassi-mutui-minimi-approfittarne` | Angolo da definire — verificare overlap cluster (Tassi mutui ai livelli più bassi della fase: come orientarsi) |

### Servizi e istituzionale (3)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-permuta-immobiliare-padova-2026` | `permuta-immobiliare` | Angolo da definire — verificare overlap cluster (Permuta immobiliare nel Padovano: come funziona e quali caut) |
| `blog-scegliere-agenzia-immobiliare-padova-2026` | `scegliere-agenzia-immobiliare` | Angolo da definire — verificare overlap cluster (Scegliere Agenzia Immobiliare a Padova: Guida e Checklist 20) |
| `blog-successione-immobiliare-padova` | `successione-immobiliare` | Angolo da definire — verificare overlap cluster (Casa Ereditata Padova: Successione e Vendita) |

### Sostenibilità e APE (2)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-domanda-case-green-certificazione-padova-2026` | `domanda-case-green-certificazione` | Angolo da definire — verificare overlap cluster (Domanda di case green ad alta efficienza nel Padovano: strat) |
| `blog-residenze-green-padova-tribloc-2026` | `tribloc-gozzi-nzeb-riuso-uffici` | Progetto urbano Tribloc/Gozzi — non generico green building |

### Territorio e zone (6)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-appartamento-nuova-costruzione-limena` | `appartamento-nuova-costruzione-limena` | Angolo da definire — verificare overlap cluster (Appartamento Nuova Costruzione Limena: 101 mq Classe A4) |
| `blog-direttiva-case-green-limena-padova` | `direttiva-case-green-limena` | Angolo da definire — verificare overlap cluster (Direttiva Case Green: Cosa Cambia a Padova e Limena) |
| `blog-quartieri-padova-2026` | `quartieri` | Angolo da definire — verificare overlap cluster (Guida ai Quartieri di Padova: Dove Comprare Casa nel 2026) |
| `blog-scuole-istruzione-padova` | `scuole-istruzione` | Angolo da definire — verificare overlap cluster (Scuole e Istruzione a Padova per Zone) |
| `blog-servizi-infrastrutture-padova` | `servizi-infrastrutture` | Angolo da definire — verificare overlap cluster (Servizi e Infrastrutture a Padova per Zone) |
| `blog-trasporti-mobilita-padova` | `trasporti-mobilita` | Angolo da definire — verificare overlap cluster (Trasporti e Mobilita' a Padova per Zone) |

### Vendita (12)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-casa-vendibile-5-anni-case-green-padova-2026` | `casa-vendibile-anni-case-green` | Angolo da definire — verificare overlap cluster (Casa vendibile tra 5 anni a Padova: APE e posizione) |
| `blog-case-vendita-padova` | `case-vendita` | Angolo da definire — verificare overlap cluster (Case in Vendita Padova 2026: Prezzi, Zone e Guida Esperta) |
| `blog-costi-vendere-casa-padova-2026` | `costi-vendere-casa` | Angolo da definire — verificare overlap cluster (Vendere Casa Padova 2026: Costi, Tasse e Tempi Reali) |
| `blog-documenti-compravendita-rogito-padova-2026` | `documenti-compravendita-rogito` | Angolo da definire — verificare overlap cluster (Documenti necessari per la compravendita di un immobile: gui) |
| `blog-documenti-vendita-casa` | `documenti-vendita-casa` | Angolo da definire — verificare overlap cluster (Documenti Vendita Casa 2026: Lista Completa) |
| `blog-home-staging-padova` | `home-staging` | Angolo da definire — verificare overlap cluster (Home Staging Padova: Vendere Casa Prima e Meglio) |
| `blog-imposte-registro-catasto-compravendita-padova-2026` | `imposte-registro-catasto-compravendita` | Angolo da definire — verificare overlap cluster (Imposte registro e ipotecarie in compravendita: guida Padova) |
| `blog-offerta-stock-vendita-italia-2026` | `offerta-stock-vendita` | Angolo da definire — verificare overlap cluster (Stock case in vendita Italia: -5% nel Q1 2026 / Guida Padova) |
| `blog-percorso-vendita-immobile-padova-2026` | `percorso-vendita-immobile` | Angolo da definire — verificare overlap cluster (Dal prezzo alla proposta: percorso vendita immobile Padova 2) |
| `blog-tasse-vendita-casa` | `tasse-vendita-casa` | Angolo da definire — verificare overlap cluster (Tasse Vendita Casa 2026: Plusvalenza e Imposte) |
| `blog-tempi-vendita-casa-padova` | `tempi-vendita-casa` | Angolo da definire — verificare overlap cluster (Tempi Vendita Casa Padova 2026: Quanto Ci Vuole Davvero?) |
| `blog-vendita-immobiliare-padova-strategie-2026` | `vendita-immobiliare-strategie` | Angolo da definire — verificare overlap cluster (Vendere Casa a Padova 2026: 7 Strategie per il Prezzo Top) |

### Vita d'agenzia (6)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-agenzia-immobiliare-top-servizi-padova-2026` | `agenzia-immobiliare-top-servizi` | Angolo da definire — verificare overlap cluster (Cosa distingue un'agenzia immobiliare di alto livello: rispo) |
| `blog-ca-marcello-mestre` | `marcello-mestre` | Angolo da definire — verificare overlap cluster (Ca' Marcello Mestre: Hub Turistico da 70 Milioni) |
| `blog-impegno-quotidiano-agenzia-immobiliare` | `impegno-quotidiano-agenzia-immobiliare` | Angolo da definire — verificare overlap cluster (Impegno Quotidiano di un'Agenzia: Burocrazia e Mutui) |
| `blog-righetto-storia-territorio-acquisizioni-2026` | `righetto-storia-territorio-acquisizioni` | Angolo da definire — verificare overlap cluster (Righetto Immobiliare dal 2000: storia, zone e ultime acquisi) |
| `blog-ultime-acquisizioni-commerciali-padova-giugno-2026` | `ultime-acquisizioni-commerciali-giugno` | Angolo da definire — verificare overlap cluster (Ultime 5 acquisizioni commerciali Padova 2026) |
| `blog-ultime-acquisizioni-residenziali-padova-giugno-2026` | `ultime-acquisizioni-residenziali-giugno` | Angolo da definire — verificare overlap cluster (Acquisizioni portale Righetto giugno 2026 / Case e commercia) |

---

## 4. Matrice rischi — cluster Affitti (non fondere)

| Articolo A | Articolo B | Perché restano distinti |
|---|---|---|
| `blog-affitto-studenti-padova` | `blog-checklist-affitto-studenti-padova-2026` | Guida zone vs checklist operativa |
| `blog-affitti-padova-canoni-2026` | `blog-stanza-universitaria-padova-canoni-2026` | Pillar città vs dato Insights stanza |
| `blog-affitti-canoni-fimaa-q1-2026-padova` | `blog-stanza-universitaria-padova-canoni-2026` | FIMAA trimestre vs Insights |
| `blog-studentati-veneto-2026-posti-letto` | `blog-stanza-universitaria-padova-canoni-2026` | Offerta sistemica vs prezzo stanza |
| `blog-residenze-green-padova-tribloc-2026` | `blog-domanda-case-green-certificazione-padova-2026` | Progetto Tribloc vs domanda Case Green |
| `blog-vicenza-residenze-universitarie-calmierate-2026` | `blog-studentati-veneto-2026-posti-letto` | Vicenza Querini vs panorama Veneto |
| `blog-housing-lavoratori-veneto-edilcassa-2026` | `blog-contratto-affitto-padova` | B2B edile vs contratti residenziali |

---

## 5. Aggiornamento

Dopo ogni batch blog:

1. `python scripts/build_skimm.py`
2. Aggiungere `ANGLE_OVERRIDES` in `scripts/build_skimm.py` per ogni articolo nuovo.
3. `python scripts/check_doppioni_sito.py`
4. Commit `skimm.md` + `skimm.json` insieme agli HTML.

