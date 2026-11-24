# Feed portali (Immobiliare.it / Idealista)

Cartella di output per i file generati in locale.

- `immobiliare-feed.xml` — formato batch Immobiliare.it (UTF-8)
- `idealista-feed.json` — JSON di lavoro in attesa di omologazione Idealista (ILC)

**Non** pubblicare questi file sul sito pubblico senza token/protezione.  
Il canale consigliato in produzione è l’Edge Function `portal-feeds` (URL con token segreto).

Generazione:

```bash
node scripts/generate-portal-feeds.mjs --from-json ../backup/immobili.json
```

Documentazione operativa: `docs/p1-portali-mandati-2026-11-24.md`
