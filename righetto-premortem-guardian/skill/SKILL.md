---
name: righetto-premortem-guardian
description: Sistema di prevenzione del fallimento, verifica, automazione e apprendimento per il sito Righetto Immobiliare. Usa una sequenza unica OBSERVE→VERIFY→PREMORTEM→PRIORITIZE→ACT→VERIFY→LEARN→NEXT CHECK.
---

# Righetto Premortem Guardian

## Quando usarlo

Usalo per:
- controlli del sito;
- SEO;
- lead;
- contenuti;
- AI/Linda;
- immobili;
- analytics;
- automazioni;
- sicurezza;
- decisioni strategiche;
- incidenti;
- modifiche al sistema.

## Sequenza obbligatoria

Segui `../sequences/master-sequence.md`.

Non sostituire il premortem con una lista generica di "pro e contro".

## Output

Produci sempre un risultato strutturato secondo lo schema definito nella master sequence.

## Regole

1. fatti separati da ipotesi;
2. niente dati inventati;
3. ogni rischio deve avere almeno un segnale;
4. ogni segnale deve avere un test;
5. ogni azione deve avere una verifica;
6. ogni incidente rilevante deve produrre un apprendimento;
7. le azioni distruttive o ad alto impatto richiedono approvazione;
8. non modificare soglie solo per eliminare alert;
9. evitare loop automatici;
10. preferire azioni reversibili.

## Applicazione al sito

Le categorie predefinite sono:
- availability;
- forms/leads;
- database;
- API;
- SEO;
- content freshness;
- structured data;
- performance;
- AI quality;
- analytics;
- security;
- backups;
- cost;
- business conversion;
- reputation.

## Promemoria ogni 15 giorni (automatico, senza API a pagamento)

**Cron GitHub:** `.github/workflows/guardian-learning-bridge-biweekly.yml`  
**Schedule:** 1° e 16° di ogni mese, ore 09:00 CEST (07:00 UTC).

Cosa succede in automatico:
1. `guardian.mjs learning biweekly` + `guardian.mjs run`
2. Email a **info@righettoimmobiliare.it** con promemoria operativo (stesso relay del venerdì: `send-mail.php` + secret `EMAIL_RELAY_KEY`)
3. Issue GitHub con label `guardian-learning` (backup se l'email fallisce)

**Comando utente in Cursor (quando riceve l'email o vuole fare il giro):**

Scrivi **`GUARDIAN`** oppure **`LEARNING BRIDGE`**.

L'agente deve:
1. Leggere `data/learning-bridge/*.json` e `righetto-premortem-guardian/reports/`
2. Riassumere insight, zero-result, domande senza risposta, KPI
3. Proporre azioni concrete (FAQ Linda, articolo blog, SEO) — **senza** modificare ranking live senza approvazione
4. Suggerire sul PC: `node righetto-premortem-guardian/scripts/guardian.mjs learning biweekly`

Script email: `scripts/guardian-biweekly-reminder-email.py`

## Obiettivo

Non massimizzare l'automazione.
Massimizzare la probabilità che un problema venga:
**anticipato → rilevato → contenuto → corretto → ricordato.**
