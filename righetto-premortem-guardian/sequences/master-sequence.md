# MASTER SEQUENCE — una sequenza, un comando

Questa è la sequenza universale che qualsiasi agente deve poter comprendere senza conoscere l'implementazione interna.

## FASE 0 — CONTEXT

Definisci:
- obiettivo;
- sistema coinvolto;
- periodo;
- metriche di successo;
- vincoli;
- autorizzazioni.

## FASE 1 — OBSERVE

Raccogli:
- stato;
- eventi recenti;
- modifiche;
- metriche;
- errori;
- trend.

## FASE 2 — VERIFY

Controlla che le osservazioni siano reali.
Se possibile usa almeno due segnali indipendenti per gli eventi critici.

## FASE 3 — ASSUMPTIONS

Elenca le assunzioni implicite.
Per ciascuna:
- evidenza;
- livello di confidenza;
- test possibile.

## FASE 4 — PREMORTEM

Immagina:

> "Siamo nel futuro e il piano è fallito. Perché?"

Genera cause concrete, non consigli generici.

## FASE 5 — FAILURE MODES

Per ogni causa crea:
- evento;
- causa;
- conseguenza;
- probabilità;
- impatto;
- rilevabilità;
- controllabilità;
- segnali precoci.

## FASE 6 — PRIORITIZE

Usa:

`risk = probability × impact × detection_penalty × controllability_penalty`

Normalizza il risultato e ordina per priorità.

## FASE 7 — ACT

Per ogni rischio:
- preventivo;
- detective;
- correttivo;
- escalation.

Non superare il livello di autonomia autorizzato.

## FASE 8 — VERIFY AGAIN

Dopo ogni azione controlla:
- condizione attesa;
- regressioni;
- effetti collaterali;
- metriche.

## FASE 9 — LEARN

Registra:
- cosa è successo;
- cosa ha funzionato;
- cosa non ha funzionato;
- nuova soglia;
- nuovo test;
- nuova regola.

## FASE 10 — NEXT CHECK

Determina:
- cosa controllare;
- quando;
- con quale soglia;
- chi deve essere avvisato;
- cosa può essere automatizzato.

## Output canonico

```yaml
status: ok|warning|critical
objective: ""
observations: []
verified_facts: []
assumptions: []
failure_modes: []
signals: []
actions: []
verification: []
learnings: []
next_checks: []
human_approval_required: []
```
