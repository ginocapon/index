---
name: righetto-perizia
description: >-
  Genera perizie immobiliari PDF Righetto Immobiliare con logo, brand, planimetrie
  e prospetti. Usa quando l'utente chiede perizia, stima immobiliare, relazione di
  valutazione, valutazione per proprietario o «facciamo perizia».
---

# Perizia immobiliare Righetto — template v2

## Quando attivare

- «Facciamo perizia», «perizia per…», «relazione di stima», «valutazione immobile»
- PDF con planimetrie/prospetti allegati per un proprietario

**AI Act:** la perizia PDF è documento ufficiale redatto dall'agenzia — distinta dalle **stime orientative** dell'assistente digitale Linda (`skill-ai-act-compliance.md`).

## Anteprima layout

Apri nel browser: `documenti/anteprima-perizia-righetto.html`

## Contatti (sempre nel documento)

| Campo | Valore |
|-------|--------|
| Sede | Via Roma n.96 — 35010 Limena (PD) |
| Tel | **049.8843484** (`tel:+390498843484`) |
| Cell | 349 736 5930 |
| Email | info@righettoimmobiliare.it |
| Web | righettoimmobiliare.it |
| P.IVA | 05182390285 |

Formato tel in PDF/footer: `049.8843484` oppure `049.8843484` (equivalenti).

## Brand visivo

- Logo: `img/brand/logo-righetto-ri.png`
- Colori: `#152435` nero · `#2C4A6E` blu · `#FF6B35` oro · `#ECE7DF` sfondo
- Cornice blu + barra oro in alto + footer nero su ogni pagina

## Struttura PDF (5–7 pagine)

1. **Presentazione** — vista 3D / satellite a piena pagina, tipologia, ubicazione, anteprima prezzo (obbligatoria se `vista_aerea` in config)
2. **Relazione** — logo, data, riepilogo, sezioni 1–4 (oggetto, catasto, stato, urbanistico)
3. **Valutazione** — considerazioni commerciali, box valore €, forchette, contatti agenzia
4. **Allegato A** — planimetria catastale (PDF)
5. **Allegato B** — visura / estratto catastale (PDF o screenshot)
6. **Note legali** — disclaimer in calce

**Non** ripetere la vista aerea in allegato finale se già usata in copertina (`vista_aerea_in_allegati: false`).

## Regole valutazione commerciale (BLOCCANTE)

- **Mai** citare prezzi al m² «medi di comune» o di zona (es. 1.440 €/m²) — fuorvianti su immobili con criticità; **solo** €/m² calcolato da `valore_principale ÷ superficie_commerciale`.
- **Target clientela:** per porzioni bifamiliari orizzontali multi-livello da ristrutturare → prevalentemente **acquirenti stranieri**, non imprese edili italiane generiche.
- **Valore partenza:** decisione agenzia (`valore_principale`) = **prezzo tecnico massimo di partenza**; in chiusura **non** indicare forchette basse (€ 80–120k ecc.) — spiegare che il mercato può ribassare almeno ~10% e che Righetto parte dal prezzo tecnico indicato.
- **APE:** se mancante, inserire in `obblighi_vendita[]` e in `attivita_prioritarie[]` l'incarico a tecnico certificatore (obbligatorio per vendita, D.Lgs. 192/2005).
- Campi JSON: `considerazioni_commerciali[]`, `nota_mercato`, `target_acquirente`, `nota_valore_finale`, `obblighi_vendita[]`.

## Script

```bash
# Nuovo formato JSON (consigliato — luglio 2026)
python scripts/genera_perizia.py scripts/perizia_config_ragazzo_curtarolo.json

# Legacy monolitico
python scripts/genera_perizia_turato.py
```

Output: `documenti/Perizia_<Nome>.pdf` + copia in `Downloads/`

Dipendenze: `pymupdf`, `reportlab`, `pillow`

## Config JSON (template riutilizzabile)

Copiare e adattare un file `scripts/perizia_config_<cognome>.json`:

| Campo | Obbligatorio | Descrizione |
|-------|--------------|-------------|
| `output_nome` | sì | Nome file PDF in `documenti/` |
| `data` | sì | ISO `YYYY-MM-DD` |
| `proprietario` | sì | Intestatario / erede |
| `proprietario_dettaglio` | no | Nascita, CF, visura |
| `tipologia` | sì | Es. porzione bifamiliare |
| `ubicazione` | sì | Indirizzo completo |
| `superficie_commerciale` | sì | mq |
| `valore_principale` | sì | € partenza / stima |
| `euro_mq_nota` | no | Solo incidenza calcolata agenzia — no medie zona |
| `considerazioni_commerciali` | no | Array paragrafi HTML sezione 5 |
| `nota_mercato` | no | Chiarimento €/m² (no confronto zone) |
| `nota_valore_finale` | no | Testo sotto box valore |
| `target_acquirente` | no | Clientela (preferire stranieri su orizzontali da ristrutturare) |
| `catasto` | sì | `unita[]` sub/cat/consistenza/rendita |
| `caratteristiche` | no | Elenco bullet |
| `criticita_urbanistiche` | no | Elenco |
| `obblighi_vendita` | no | Es. APE obbligatoria — incarico tecnico |
| `attivita_prioritarie` | no | Elenco |
| `allegati.planimetria_catastale` | no | Path PDF planimetria |
| `allegati.scheda_catastale` | no | Path PDF visura |
| `allegati.vista_aerea` | no | Path JPG/PNG vista 3D — **pagina 1 presentazione** |
| `allegati.vista_aerea_in_allegati` | no | `false` se già in copertina (default) |
| `valore_secondario` | no | Opzionale — di solito omesso (no forchette basse in chiusura) |
| `valore_conservativo` | no | Opzionale — scenario peggiore, solo se esplicitamente richiesto |

Esempi config: `perizia_config_turato.json`, `perizia_config_ragazzo_curtarolo.json`

## Dati da chiedere se mancanti

1. Proprietario (es. Sig. Turato Antonio)
2. Tipologia immobile
3. Valore stimato €
4. Superficie commerciale (mq) + tabella calcolo se disponibile
5. PDF planimetrie/prospetti (path file)
6. Data perizia (default: oggi)

## Regole impaginazione (apprese da feedback)

- **Mai** lasciare pagine quasi vuote: note legali vanno in calce pagina prospetti con `KeepTogether`
- Planimetrie/prospetti: ruotare da verticale a orizzontale, ritagliare bordi bianchi
- Prospetti: splittare e affiancare le due elevazioni
- Compositi verticali alla stessa larghezza per riempire la pagina
- Logo sempre in header pagina 1

## Disclaimer obbligatorio

> La presente stima ha carattere indicativo e non sostituisce una perizia tecnico-giuridica redatta da perito abilitato.

## File correlati

- `scripts/genera_perizia.py` — **generatore JSON** (consigliato)
- `scripts/genera_perizia_turato.py` — legacy monolitico
- `scripts/perizia_config_*.json` — dati per immobile
- `documenti/anteprima-perizia-righetto.html` — anteprima HTML layout v2
