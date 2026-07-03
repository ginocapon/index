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

### 1.7 Freschezza contenuti — vantaggio competitivo vs portali

Obiettivo: **bucare Google** con topical authority + segnali freshness che i competitor (Tetto Rosso, RicercAttiva) non hanno a questo livello.

| Segnale Google 2026 | Obbligo Righetto | Frequenza |
|---|---|---|
| **dateModified** schema BlogPosting | Su ogni articolo + visibile «Ultimo aggiornamento» | Ogni revisione |
| **Corpo corposo** (2500+ parole utili) | No paragrafi duplicati; fonti istituzionali | Nuovi articoli |
| **Cosa può fare Righetto** | Sezione `righetto-sol` con 3–4 soluzioni linkate | Ogni articolo nuovo/refresh |
| **Foto realistiche + grafici SVG** | Min 3 foto + 2 chart a tema | Ogni articolo |
| **Hub blog aggiornato** | `blog.html` + homepage `#blog` sempre per data | Settimanale (venerdì) |
| **llms.txt / ai.json** | Nuovi slug pillar entro 48h dalla pubblicazione | Ogni batch |
| **Internal link** | 3+ link contestuali verso zone/servizi/pillar | Ogni articolo |

### 1.8 Pagine pillar — refresh obbligatorio

Verificate ogni **venerdì** da `scripts/venerdi-contenuti-freschezza.py`:

| Pagina | Minimo contenuto | Link blog richiesti |
|---|---|---|
| `/` (index) | Hero freshness + sezione blog dinamica | ≥3 articoli recenti |
| `/blog` | Hero «Ultimo aggiornamento» + N articoli | Hub completo |
| `/agenzia-immobiliare-padova` | E-E-A-T locale, FAQ | ≥2 guide mercato |
| `/servizio-locazioni` | Cluster affitti/studenti | ≥3 articoli affitti |
| `/servizio-valutazioni` | Trust + CTA valutazione | ≥2 guide vendita |
| `/chi-siamo` | Storia dal 2000, autori | Link autori + acquisizioni |
| `/immobili` | Catalogo + filtri | — |

### 1.9 Ritmo editoriale anti-cannibalizzazione

- **1 articolo nuovo/settimana** minimo (venerdì pubblicazione ideale).
- **1 refresh/mese** di un pillar esistente (dato OMI, BCE, FIMAA aggiornato).
- **Batch max 5 articoli** con radici slug diverse (vedi §1.3).
- Prima di ogni batch: `build_skimm.py` + `check_doppioni_sito.py` + questo file §3.
- Report automatico venerdì 07:00 → `info@righettoimmobiliare.it` (workflow `venerdi-contenuti-freschezza.yml`).

---

## 2. Stato verifica automatica

**13 avvisi** al generazione 2026-07-03:

- Intent simile `breakdown-costi`: blog-costi-proprieta-acquisto-possesso-vendita-padova-2026, blog-costi-costruzione-istat-padova-2026
- Intent simile `territorio-limena`: blog-limena-vicino-padova-comprare-2026, blog-mercato-immobiliare-limena-2026, blog-appartamento-nuova-costruzione-limena, blog-direttiva-case-green-limena-padova
- Intent simile `fisco-normativa`: blog-quattro-imposte-rogitio-prima-casa-padova-2026, blog-bonus-mobili-2026-massimizzare-ristrutturazioni, blog-imposte-registro-catasto-compravendita-padova-2026, blog-tasse-vendita-casa
- Intent simile `analisi-scenari`: blog-bolla-immobiliare-padova-2026, blog-previsioni-immobiliari-scenari-geopolitica-2026, blog-prospettive-mercato-residenziale-italia-2026
- Intent simile `territorio-padova`: blog-prezzi-case-padova-zona-2026, blog-scuole-istruzione-padova, blog-servizi-infrastrutture-padova, blog-trasporti-mobilita-padova
- Intent simile `mutui-cluster`: blog-mutui-selettivi-banche-padova-2026, blog-mutuo-fisso-variabile-padova-2026, blog-mutuo-prima-casa-padova, blog-tassi-mutui-minimi-approfittarne-padova-2026
- Intent simile `documenti-operativi`: blog-mutuo-documenti-tempi-prima-casa-padova-2026, blog-documenti-compravendita-rogito-padova-2026, blog-documenti-vendita-casa
- Intent simile `vita-agenzia-brand`: blog-ca-marcello-mestre, blog-impegno-quotidiano-agenzia-immobiliare
- Token slug sovrausato `mercato` (9 articoli) — variare radice nei prossimi batch
- Coppia da non fondere (Insights 490 vs pillar +8%): blog-stanza-universitaria-padova-canoni-2026 ↔ blog-affitti-padova-canoni-2026
- Coppia da non fondere (Insights vs FIMAA Q1): blog-stanza-universitaria-padova-canoni-2026 ↔ blog-affitti-canoni-fimaa-q1-2026-padova
- Coppia da non fondere (Tribloc vs Case Green generico): blog-residenze-green-padova-tribloc-2026 ↔ blog-domanda-case-green-certificazione-padova-2026
- Coppia da non fondere (Evento BCE vs guida mutui): blog-bce-tassi-mutui-giugno-2026-padova ↔ blog-mutui-casa-padova-2026

**Articoli catalogati:** 101

---

## 3. Catalogo completo per cluster

### Acquisto e prima casa (14)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-agevolazioni-prima-casa-2026` | `agevolazioni-prima-casa-2026` | Bonus e requisiti prima casa — non imposte rogito |
| `blog-ape-prestazione-energetica-acquisto-padova-2026` | `ape-prestazione-energetica-acquisto` | APE in fase acquisto — non direttiva Case Green |
| `blog-caparra-confirmatoria-padova` | `caparra-confirmatoria-compravendita` | Caparra confirmatoria vs penitenziale — guida operativa rogito |
| `blog-checklist-verifiche-prima-compromesso-padova-2026` | `checklist-verifiche-prima-compromesso` | Checklist pre-compromesso operativa — non guida acquisto generica |
| `blog-comprare-affittare-padova` | `comprare-affittare-confronto-padova` | Confronto dati comprare vs affittare — decisione budget |
| `blog-comprare-casa-padova-guida-2026` | `comprare-casa-padova-guida-pillar` | Guida acquisto 10 passi — pillar prima casa Padova |
| `blog-costi-proprieta-acquisto-possesso-vendita-padova-2026` | `costi-proprieta-acquisto-possesso-vendita` | Breakdown costi numerici — fonte verificabile obbligatoria |
| `blog-dieci-errori-acquisto-casa-padova-2026` | `dieci-errori-acquisto-casa-padova` | Errori comuni acquirente — intent educativo |
| `blog-limena-vicino-padova-comprare-2026` | `limena-vicino-comprare` | Focus Limena/cintura — non generico Padova centro |
| `blog-limena-vs-padova-centro-dove-comprare-2026` | `limena-centro-confronto-acquisto` | Confronto Limena vs Centro — decisione acquirente |
| `blog-planimetria-catastale-compravendita-padova-2026` | `planimetria-catastale-verifica-rogito` | Controllo planimetria pre-rogito — non checklist generica |
| `blog-quattro-imposte-rogitio-prima-casa-padova-2026` | `quattro-imposte-rogitio-prima-casa` | Fisco/normativa — non dati mercato |
| `blog-scegliere-immobile-giusto-padova-2026` | `scegliere-immobile-zona-luce-padova` | Criteri scelta immobile (zona, luce, spese) — non guida 10 passi |
| `blog-vigonza-rubano-comprare-casa-cintura-2026` | `vigonza-rubano-comprare-casa-cintura` | Focus Vigonza/Rubano — geografia cintura |

### Affitti e locazioni (15)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-affitti-canoni-fimaa-q1-2026-padova` | `fimaa-q1-2026-canoni-veneto` | Rilevazione trimestrale FIMAA — non Insights 490€ |
| `blog-affitti-padova-canoni-2026` | `affitti-padova-canoni-trend-2026` | Pillar canoni città +8% — non stanza singola Insights |
| `blog-affitto-breve-padova-2026` | `affitto-breve-padova-rendimenti-regole` | Short-term rental rendimenti/normativa — non locazione 4+4 |
| `blog-affitto-studenti-padova` | `guida-affitto-studenti-padova` | Guida evergreen zone/contratti — non dato anno |
| `blog-checklist-affitto-studenti-padova-2026` | `checklist-contratto-studenti-padova` | Checklist operativa caparra/contratto — non mercato |
| `blog-contratto-affitto-padova` | `contratto-affitto-tipologie-padova` | 4+4, 3+2, transitorio, cedolare — normativa |
| `blog-emergenza-abitativa-padova-2026` | `emergenza-abitativa-padova-dati` | Gap domanda/offerta abitativa — non canoni singoli |
| `blog-housing-lavoratori-veneto-edilcassa-2026` | `edilcassa-fondo-garanzia-locazione-lavoratori` | Fondo 250k€ garanzie affitto operai — non studenti né canoni |
| `blog-quotazioni-locazioni-omi-istat-padova-2026` | `quotazioni-locazioni-omi-istat-padova` | Monitor OMI/ISTAT locazioni — non FIMAA né Insights |
| `blog-rendimento-affitto-padova` | `rendimento-locativo-quartieri-padova` | Yield % per quartiere investitori |
| `blog-righetto-bilancio-2025-soluzioni-affitto-2026` | `righetto-bilancio-affitto-soluzioni` | Case study agenzia + soluzioni affitto — E-E-A-T |
| `blog-squilibrio-domanda-offerta-affitti-padova` | `squilibrio-domanda-offerta-affitti` | Cluster affitti — verificare matrice §4 prima di pubblicare |
| `blog-stanza-universitaria-padova-canoni-2026` | `canone-stanza-insights-490-padova` | Dato Immobiliare.it Insights (+46% vs 2020) e periferie tram — non FIMAA Q1 |
| `blog-studentati-veneto-2026-posti-letto` | `posti-letto-esu-camplus-pnrr-veneto` | Canali offerta regionale (ESU/privati/PNRR) — non singolo canone stanza |
| `blog-vicenza-residenze-universitarie-calmierate-2026` | `casa-querini-calmierati-vicenza` | Vicenza PNRR Saudino — non Padova né Tribloc |

### Altri / trasversali (3)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-5-errori-visita-immobile-padova-2026` | `errori-visita-immobile-etichetta` | Etichetta visita / tono ironico acquirente — non checklist rogito né errori acquisto generici |
| `blog-gestione-spese-casa-risparmio-padova-2026` | `gestione-spese-casa-possesso-padova` | Spese possesso post-acquisto (energia, IMU) — non costi rogito |
| `blog-so-tutto-io-venditore-presuntuoso-padova-2026` | `venditore-presuntuoso-staging-documenti-ape` | Verità dal campo / tono provocatorio — non guida tecnica staging o solo documenti |

### Fisco e normativa (4)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-bonus-edilizi-2026-incentivi-casa-padova` | `bonus-edilizi-2026-incentivi` | Incentivi fiscali edilizia 2026 — non decreto urbanistica |
| `blog-bonus-mobili-2026-massimizzare-ristrutturazioni` | `bonus-mobili-massimizzare-ristrutturazioni` | Fisco/normativa — non dati mercato |
| `blog-condono-edilizio-proposte-2026` | `condono-edilizio-manovra-2026` | Proposte normative condono — non bonus edilizi |
| `blog-piano-casa-decreto-66-2026-padova` | `piano-casa-decreto-66-padova` | Normativa Decreto 66 edilizia — non bonus fiscali |

### Investimenti (2)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-investire-immobiliare-padova` | `investire-immobiliare-padova-rendimenti` | Investimento locativo Padova — non trend summit |
| `blog-trend-investimenti-immobiliari-summit-2026` | `trend-investimenti-summit-2026` | Evento Real Estate Summit — non investire Padova pillar |

### Macro e geopolitica (2)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-eurocamera-accordo-dazi-usa-2026` | `eurocamera-accordo-dazi-sunset-2029` | Accordo istituzionale EU-USA — non filiera padovana |
| `blog-patrimonio-casa-resilienza-mercati-globali-2026` | `patrimonio-casa-resilienza-urbana` | Resilienza patrimonio vs shock globali — macro trasversale |

### Mercato e dati (20)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-bolla-immobiliare-padova-2026` | `bolla-immobiliare` | Analisi scenari/proiezioni — citare fonte, no predizioni inventate |
| `blog-case-piu-vendute-tipologie-padova-2026` | `case-piu-vendute-tipologie-padova` | Tipologie/metrature più vendute — dato mercato locale |
| `blog-compravendite-italia-q1-agenzia-entrate-2026-padova` | `compravendite-italia-q1-ade` | Dato nazionale Q1 ADE — non record Padova locale |
| `blog-compravendite-padova-record-2026` | `compravendite-padova-record-2026` | Record transazioni territorio — non stock nazionale |
| `blog-compravendite-veneto-cintura-padova-2026` | `compravendite-veneto-cintura-padova` | Transazioni cintura Padovana — non Q1 nazionale ADE |
| `blog-costi-costruzione-istat-padova-2026` | `costi-costruzione-istat` | Breakdown costi numerici — fonte verificabile obbligatoria |
| `blog-crisi-immobiliare-padova-2026` | `crisi-immobiliare-padova-analisi` | Scenario crisi/correzione locale — fonte verificata, no allarmismo |
| `blog-dazi-usa-ue-mercato-padova-2026` | `dazi-usa-ue-filiera-veneto-padova` | Impatto occupazione/credito Padova — non cronaca Strasburgo |
| `blog-mercato-immobiliare-limena-2026` | `mercato-immobiliare-limena` | Focus Limena/cintura — non generico Padova centro |
| `blog-mercato-immobiliare-padova-2026` | `mercato-immobiliare-padova-pillar-2026` | Pillar mercato città prezzi/trend — non quartiere singolo |
| `blog-mercato-immobiliare-padova-centro-2026` | `mercato-centro-storico-padova` | Micro-mercato Centro Storico — non pillar città intera |
| `blog-mercato-immobiliare-piazzola-sul-brenta-2026` | `mercato-piazzola-sul-brenta` | Mercato Piazzola/comuni PD — geografia diversa da Padova |
| `blog-mercato-italiano-tensioni-medio-oriente-2026` | `mercato-italiano-tensioni-medio-oriente` | Macro/geopolitica — impatto locale, non cronaca |
| `blog-mercato-sacrocuore-padova-omi-2026` | `mercato-sacrocuore-omi` | Dato OMI/quotazioni ufficiali — non opinioni |
| `blog-nuove-costruzioni-mercato-veneto-2026-padova` | `nuove-costruzioni-veneto-plus-14` | Dato permessi/cantieri +14,6% Veneto — non costi costruzione ISTAT |
| `blog-previsioni-immobiliari-scenari-geopolitica-2026` | `previsioni-immobiliari-scenari-geopolitica` | Analisi scenari/proiezioni — citare fonte, no predizioni inventate |
| `blog-prezzi-case-padova-zona-2026` | `prezzi-case-zona` | Territorio Padova — internal link a pagina zona |
| `blog-prezzi-padova-provincia-fiaip-2026` | `prezzi-padova-provincia-fiaip` | FIMAA -4% città / provincia traina — non OMI quartieri |
| `blog-prospettive-mercato-residenziale-italia-2026` | `prospettive-mercato-residenziale` | Analisi scenari/proiezioni — citare fonte, no predizioni inventate |
| `blog-sondaggio-bancaditalia-q1-2026-padova` | `sondaggio-bancaditalia` | Dato trimestrale verificato — aggiornare al prossimo Q |

### Mutui e credito (12)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-barometro-mutui-crif-padova-2026` | `barometro-mutui-crif-padova` | Dato CRIF erogazioni — non BCE né guida pillar |
| `blog-bce-tassi-mutui-giugno-2026-padova` | `bce-giugno-2026-tassi-mutui` | Decisione BCE giugno +25bp — evento datato |
| `blog-geopolitica-ucraina-prezzi-mutui-italia-veneto-2026` | `geopolitica-ucraina-mutui-veneto` | Canale geopolitica→tassi Veneto — non dazi USA |
| `blog-immobiliare-geopolitica-energia-tassi-2026` | `geopolitica-energia-tassi-immobiliare` | Energia/tassi macro immobiliare — pillar trasversale |
| `blog-mutui-casa-padova-2026` | `mutui-casa-padova-guida-pillar` | Pillar mutui Padova evergreen — non singolo meeting BCE |
| `blog-mutui-selettivi-banche-padova-2026` | `mutui-selettivi-banche` | Cluster mutui — distinguere da pillar e eventi BCE |
| `blog-mutui-tasso-fisso-bancaitalia-padova-2026` | `mutui-tasso-fisso-bancaitalia` | Preferenza fisso vs variabile BdI — non BCE singolo meeting |
| `blog-mutuo-documenti-tempi-prima-casa-padova-2026` | `mutuo-documenti-tempi-prima-casa` | Documenti operativi rogito/pratica — non strategia |
| `blog-mutuo-fisso-variabile-padova-2026` | `mutuo-fisso-variabile` | Cluster mutui — distinguere da pillar e eventi BCE |
| `blog-mutuo-prima-casa-padova` | `mutuo-prima-casa` | Cluster mutui — distinguere da pillar e eventi BCE |
| `blog-surroga-mutuo-padova-2026` | `surroga-mutuo-padova-operativa` | Surroga operativa costi/tempi — non tassi BCE |
| `blog-tassi-mutui-minimi-approfittarne-padova-2026` | `tassi-mutui-minimi-approfittarne` | Cluster mutui — distinguere da pillar e eventi BCE |

### Servizi e istituzionale (3)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-permuta-immobiliare-padova-2026` | `permuta-immobiliare-padova-operativa` | Permuta operativa cautele — servizio agenzia |
| `blog-scegliere-agenzia-immobiliare-padova-2026` | `scegliere-agenzia-immobiliare-padova` | Criteri scelta agenzia — trust/conversione locale |
| `blog-successione-immobiliare-padova` | `successione-immobile-ereditato-padova` | Casa ereditata vendita/successione — non imposte rogito |

### Sostenibilità e APE (2)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-domanda-case-green-certificazione-padova-2026` | `domanda-case-green-certificazione-ape` | Domanda acquirenti su APE/green — non progetto Tribloc |
| `blog-residenze-green-padova-tribloc-2026` | `tribloc-gozzi-nzeb-riuso-uffici` | Progetto urbano Tribloc/Gozzi — non generico green building |

### Territorio e zone (6)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-appartamento-nuova-costruzione-limena` | `appartamento-nuova-costruzione-limena` | Focus Limena/cintura — non generico Padova centro |
| `blog-direttiva-case-green-limena-padova` | `direttiva-case-green-limena` | Focus Limena/cintura — non generico Padova centro |
| `blog-quartieri-padova-2026` | `quartieri-padova-prezzi-omi` | Mappa quartieri prezzi OMI — pillar territorio città |
| `blog-scuole-istruzione-padova` | `scuole-istruzione` | Territorio Padova — internal link a pagina zona |
| `blog-servizi-infrastrutture-padova` | `servizi-infrastrutture` | Territorio Padova — internal link a pagina zona |
| `blog-trasporti-mobilita-padova` | `trasporti-mobilita` | Territorio Padova — internal link a pagina zona |

### Vendita (12)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-casa-vendibile-5-anni-case-green-padova-2026` | `casa-vendibile-case-green-5-anni` | Vendibilità futura classe energetica — non Tribloc né domanda |
| `blog-case-vendita-padova` | `case-vendita-padova-guida-zone` | Guida zone/prezzi vendita evergreen — pillar acquirenti vendita |
| `blog-costi-vendere-casa-padova-2026` | `costi-vendere-casa-padova` | Breakdown costi vendita numerici — non strategie |
| `blog-documenti-compravendita-rogito-padova-2026` | `documenti-compravendita-rogito` | Documenti operativi rogito/pratica — non strategia |
| `blog-documenti-vendita-casa` | `documenti-vendita-casa` | Documenti operativi rogito/pratica — non strategia |
| `blog-home-staging-padova` | `home-staging-vendita-padova` | Home staging pre-vendita — non strategie pricing |
| `blog-imposte-registro-catasto-compravendita-padova-2026` | `imposte-registro-catasto-compravendita` | Fisco/normativa — non dati mercato |
| `blog-offerta-stock-vendita-italia-2026` | `stock-vendita-italia-q1-minus-5` | Stock nazionale -5% Q1 — non record transazioni Padova |
| `blog-percorso-vendita-immobile-padova-2026` | `percorso-vendita-immobile` | Strategia operativa vendita/acquisto — pillar intent |
| `blog-tasse-vendita-casa` | `tasse-vendita-casa` | Fisco/normativa — non dati mercato |
| `blog-tempi-vendita-casa-padova` | `tempi-vendita-casa-padova-medi` | Tempi medi vendita reali Padova — non costi vendita |
| `blog-vendita-immobiliare-padova-strategie-2026` | `vendita-immobiliare-strategie-padova` | Strategie vendita 2026 — pillar venditori |

### Vita d'agenzia (6)

| Slug | KW primaria | Angolo editoriale |
|---|---|---|
| `blog-agenzia-immobiliare-top-servizi-padova-2026` | `agenzia-immobiliare-servizi-top-padova` | Servizi differenzianti agenzia — E-E-A-T conversione |
| `blog-ca-marcello-mestre` | `marcello-mestre` | Vita d'agenzia / brand story — non guida mercato |
| `blog-impegno-quotidiano-agenzia-immobiliare` | `impegno-quotidiano-agenzia-immobiliare` | Vita d'agenzia / brand story — non guida mercato |
| `blog-righetto-storia-territorio-acquisizioni-2026` | `righetto-storia-territorio-acquisizioni` | Showcase portafoglio — E-E-A-T vita d'agenzia |
| `blog-ultime-acquisizioni-commerciali-padova-giugno-2026` | `acquisizioni-commerciali-padova-giugno` | Showcase portafoglio commerciale — distinto residenziale |
| `blog-ultime-acquisizioni-residenziali-padova-giugno-2026` | `acquisizioni-residenziali-padova-giugno` | Showcase portafoglio residenziale — vita d'agenzia |

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

