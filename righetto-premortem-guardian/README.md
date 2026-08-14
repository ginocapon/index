# Righetto Premortem Guardian — ONE COMMAND

## Obiettivo

Questo pacchetto è progettato per essere compreso da un agente AI una sola volta e avviato con un unico comando.

Il principio operativo è:

**OBSERVE → VERIFY → PREMORTEM → PRIORITIZE → ACT → VERIFY AGAIN → LEARN → SCHEDULE NEXT CHECK**

Il Guardian non promette di "non fallire mai". Il suo obiettivo è fare in modo che:
1. ogni failure prevedibile abbia un segnale;
2. ogni segnale abbia una verifica;
3. ogni problema abbia una risposta proporzionata;
4. ogni modifica venga verificata;
5. ogni incidente produca una nuova regola o un nuovo test.

## Struttura

```text
righetto-premortem-guardian/
├── ONE_COMMAND.md
├── README.md
├── AGENT.md
├── config/
│   ├── guardian.yaml
│   └── cron-matrix.yaml
├── policy/
│   └── autonomy.yaml
├── sequences/
│   └── master-sequence.md
├── skill/
│   └── SKILL.md
├── scripts/
│   ├── guardian.mjs
│   └── doctor.mjs
└── memory/
    └── .gitkeep
```

## Due strutture

Il pacchetto distingue volutamente due strutture:

### 1. STRUTTURA COGNITIVA
È ciò che l'agente deve capire:
- obiettivi;
- assunzioni;
- failure modes;
- segnali precoci;
- premortem;
- decisioni;
- verifiche;
- apprendimento.

### 2. STRUTTURA OPERATIVA
È ciò che il sistema deve eseguire:
- heartbeat;
- controlli;
- cron;
- scoring;
- remediation;
- verifica;
- memoria;
- report.

Le due strutture sono collegate dalla `master-sequence.md`.

## Importante

Questa è una base universale e non presume il framework del sito.
I connettori reali (GA4, Search Console, database, CRM, GitHub, email, Linda, ecc.) vengono attivati solo quando le relative variabili/adapter sono disponibili.
