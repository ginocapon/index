# ONE COMMAND

## Installazione

Dalla root del progetto Righetto:

```bash
npx --yes tsx ./righetto-premortem-guardian/scripts/guardian.mjs init
```

Dopo l'init, l'unico comando operativo è:

```bash
npx --yes tsx ./righetto-premortem-guardian/scripts/guardian.mjs run
```

Se il progetto non usa TypeScript/tsx, il Guardian contiene anche una modalità Node pura:

```bash
node ./righetto-premortem-guardian/scripts/guardian.mjs run
```

## Cosa fa `run`

Un'unica invocazione esegue la sequenza completa:

1. carica configurazione;
2. identifica contesto e obiettivi;
3. verifica salute tecnica;
4. verifica dati disponibili;
5. individua anomalie;
6. esegue il premortem;
7. costruisce failure modes;
8. assegna probabilità, impatto, rilevabilità e controllabilità;
9. ordina i rischi;
10. propone o esegue solo azioni consentite dalla policy;
11. verifica il risultato;
12. registra l'incidente/apprendimento;
13. calcola il prossimo controllo;
14. produce un report machine-readable e uno umano.

**Non devi lanciare dieci comandi diversi.**
Il comando `run` è il punto d'ingresso unico.

Per un cron, schedula sempre lo stesso comando e lascia che il dispatcher scelga cosa deve essere eseguito in base all'orario e alla matrice.
