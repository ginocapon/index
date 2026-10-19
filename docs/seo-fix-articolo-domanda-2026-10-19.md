# Articolo "Una domanda non costa nulla" — 2026-10-19

## Motivo
Richiesta di Gino (WhatsApp, 19/10/2026): articolo blog simpatico, in stile landing page, con immagini a fumetto, da promuovere quotidianamente su Facebook/Instagram (post, storie, reel) nelle fasce orarie principali. Messaggio: chiedere una semplice informazione all'agenzia è gratuito, cordiale e può cambiare la vita.

## File aggiunti
- `blog-una-domanda-non-costa-nulla.html` (articolo statico, categoria "Vita d'agenzia", autore Gino Capon, 19/10/2026, 6 min lettura, wordCount reale 1189)
- `img/blog/blog-una-domanda-non-costa-nulla-hero.webp` (1900×900, 122 KiB)
- `img/blog/blog-una-domanda-non-costa-nulla-hero-mobile.webp` (1080×512, 67 KiB)
- `img/blog/blog-una-domanda-non-costa-nulla-card.webp` (900×427, 53 KiB)
- `img/blog/blog-una-domanda-non-costa-nulla-telefonata.webp` / `-chiavi.webp` / `-caffe.webp` (1000×667, ~75 KiB cad.)

## File modificati
- `blog.html` (articoliStatici, in cima per data)
- `admin.html` (`_blogSeedArticles` + `data_pubblicazione: 2026-10-19`)
- `js/homepage.js` (staticMap + articoliStatici)
- `sitemap.xml` (URL senza .html, lastmod 2026-10-19)
- `llms.txt` (sezione "Storie e Progetti")
- `js/chatbot.js` (voce FAQ_DATA "domanda/informazione" → link articolo)
- 98 pagine `*.html`: bump `chatbot.js?v=17` → `?v=18` per la nuova voce chatbot

## Contenuto e conformità
- Solo claim consentiti (dal 2000, 350+ immobili, 101 comuni, 127 recensioni 4,9/5); nessun compenso pubblicato; orari presi da contatti.html; telefono 049.8843484 e WhatsApp 349 736 5930.
- Immagini: illustrazioni a fumetto generate con IA su richiesta esplicita di Gino; trasparenza gestita dal sistema del sito (badge FOTO AI + didascalia automatica) + nota sotto l'hero.
- Form lead in pagina (rig-lead-form), provenienza `blog-una-domanda-non-costa-nulla`, GDPR come da modulo condiviso.
- JSON-LD: BlogPosting + FAQPage (6 FAQ) + BreadcrumbList + RealEstateAgent.

## Verifiche eseguite
- `scripts/check_doppioni_sito.py`: nessun doppione nuovo (resta l'incoerenza preesistente blog-prova-mercato-limena-zona-imma-2027).
- `node scripts/validate-page.js`: tutto OK (title 50, meta 149, registrazione 4 punti OK).
- `scripts/google-compliance-check.py`: nessuna nuova segnalazione sulla pagina.
- Screenshot locali headless a 1280 e 390 px: hero, corpo, FAQ, form, footer corretti; nessuno scroll orizzontale; immagini caricate.
- NON testato l'invio reale del form (avrebbe creato una richiesta di prova).

## Limiti e seguito
- Pubblicazione solo dopo ok di Gino + codice GitHub (procedura device code), backup branch/tag prima del push, verifica live e rimozione credenziali dopo.
- L'invio del form non è stato testato end-to-end.
