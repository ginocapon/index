# SKILL KILLER - Prompt Operativo per righettoimmobiliare.it
### (Il nome e' ironico, ma il contenuto e' serissimo)

> **Versione:** 1.0 - 2 Marzo 2026
> **Ultimo aggiornamento Google verificato:** Marzo 2026
> **Prossima verifica consigliata:** Aprile 2026

---

## ISTRUZIONI PER CLAUDE

Quando ricevi questo prompt, segui SEMPRE queste regole:

### 1. VERIFICA AGGIORNAMENTI GOOGLE (OBBLIGATORIA)
Prima di ogni sessione di lavoro sul sito, DEVI:
- Fare una ricerca web per: `"Google Search updates [mese corrente] [anno corrente]"`
- Fare una ricerca web per: `"Core Web Vitals updates [anno corrente]"`
- Fare una ricerca web per: `"Google Search Console new features [anno corrente]"`
- Confrontare i risultati con la sezione "STATO AGGIORNAMENTI GOOGLE" qui sotto
- Se trovi novita', AGGIORNA questo file aggiungendo le nuove informazioni nella sezione apposita
- Comunica all'utente cosa e' cambiato rispetto all'ultima volta

### 2. AGGIORNA QUESTO PROMPT
Ogni volta che trovi aggiornamenti rilevanti:
- Aggiungi la data e il contenuto nella sezione "CHANGELOG AGGIORNAMENTI"
- Aggiorna i parametri tecnici se sono cambiati (soglie Core Web Vitals, nuovi meta tag, ecc.)
- Fai commit e push delle modifiche a questo file

---

## CONTESTO PROGETTO

### Informazioni Generali
- **Dominio:** righettoimmobiliare.it / www.righettoimmobiliare.it
- **Hosting sito:** GitHub Pages (deploy automatico da branch `main`)
- **Hosting dominio/email:** cPanel su cpanel.righettoimmobiliare.it
- **Utente cPanel:** wyrighet
- **Home directory cPanel:** /home3/wyrighet
- **Tech Stack:** HTML statico + CSS + JavaScript + Express.js (dev)
- **Database:** Supabase (esterno)
- **Newsletter:** Brevo (Sendinblue)
- **Form contatti:** Formspree
- **Analytics:** Google Analytics 4 (G-9MHDHHES26)
- **Chatbot AI:** "Sara" - assistente virtuale integrata
- **Repository:** GitHub - ginocapon/index

### Architettura DNS (NON TOCCARE MAI)
- **Record A:** punta a GitHub Pages (185.199.108.153, etc.)
- **CNAME www:** punta a ginocapon.github.io
- **Record MX:** gestione email su cPanel (NON MODIFICARE)
- **Google Site Verification:** meta tag nel `<head>` di index.html

### File Principali del Sito
```
index.html          - Homepage (1.1 MB, canvas animato)
immobili.html       - Lista immobili
immobile.html       - Dettaglio immobile
servizi.html        - Pagina servizi
chi-siamo.html      - Chi siamo
contatti.html       - Form contatti
blog.html           - Blog
faq.html            - FAQ
admin.html          - Pannello admin
js/chatbot.js       - Chatbot Sara (1,595 righe)
js/config.js        - Configurazioni API
js/welcome-popup.js - Popup benvenuto
js/cookie-consent.js - Cookie consent
sitemap.xml         - Sitemap per Google
robots.txt          - Direttive crawler
CNAME               - Dominio GitHub Pages
```

---

## GESTIONE cPanel - COSA ELIMINARE E COSA TENERE

### DA ELIMINARE (per liberare spazio)
| File/Cartella | Dimensione | Motivo |
|---|---|---|
| `backup-3.2.2026_10-53-22_wyrighet.tar.gz` | **37.04 GB** | Backup completo - scaricato in locale, eliminare dal server |
| `public_htmlcopia140422.zip` | **11.37 GB** | Backup vecchio sito WordPress del 2022 - obsoleto |
| `error_log` | variabile | Log errori - non servono piu' |
| `error_log-*.gz` | ~13 KB totali | Log errori compressi vecchi |
| `error_log_php` | variabile | Log errori PHP |
| `error_log_php-*.gz` | ~65 KB totali | Log errori PHP compressi |
| `sp_mysql_bk/` | variabile | Backup MySQL vecchi (WordPress non c'e' piu') |
| `public_html/` contenuto | variabile | Vecchio sito WordPress - ora il sito e' su GitHub Pages |
| **Database MySQL** | variabile | Database WordPress - non piu' necessari |
| **Email non utilizzate** | fino a 17 GB | Account email vecchi e messaggi non necessari |

### DA TENERE ASSOLUTAMENTE (NON TOCCARE)
| Elemento | Motivo |
|---|---|
| **Record DNS** | A, CNAME, MX - fanno funzionare sito e email |
| **Dominio** | righettoimmobiliare.it registrato qui |
| **Account email attivi** | Email che usi quotidianamente |
| **Certificato SSL** | Per HTTPS |
| **Cartella `mail/`** | Contiene le caselle email attive |
| **Cartella `etc/`** | Configurazioni del server |
| **Cartella `ssl/`** | Certificati SSL |
| **cPanel stesso** | Pannello di controllo |

### Cartelle di Sistema cPanel (NON ELIMINARE)
- `cache/` - Cache di sistema
- `etc/` - Configurazioni
- `logs/` - Log attivi (si auto-puliscono)
- `mail/` - Caselle email
- `perl5/` - Moduli Perl di sistema
- `php_sessions/` - Sessioni PHP
- `public_ftp/` - FTP pubblico
- `ssl/` - Certificati
- `tmp/` - File temporanei (si auto-puliscono)
- `access-logs` - Symlink ai log

---

## REQUISITI SEO GOOGLE - AGGIORNATI MARZO 2026

### Google Search Console - Configurazione
- [x] Verifica proprieta' tramite meta tag HTML nel `<head>`
- [x] Sitemap XML inviata (`sitemap.xml`)
- [x] robots.txt configurato
- [x] Google Analytics 4 attivo (G-9MHDHHES26)
- [ ] Verifica proprieta' dominio anche via DNS TXT (consigliato come backup)

### Core Web Vitals - Soglie 2026
| Metrica | Buono | Da migliorare | Scarso |
|---|---|---|---|
| **LCP** (Largest Contentful Paint) | < 2.5s | 2.5s - 4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | < 200ms | 200ms - 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | < 0.1 | 0.1 - 0.25 | > 0.25 |
| **SVT** (Smooth Visual Transitions) - NUOVO 2026 | Penalizza caricamenti "scattosi" |
| **VSI** (Visual Stability Index) - NUOVO 2026 | Misura stabilita' durante tutta la sessione |

### Fattori di Ranking Principali 2026
1. **Qualita' del contenuto** - E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)
2. **Rilevanza semantica** - Contenuto che risponde all'intento di ricerca
3. **Core Web Vitals** - Performance come fattore decisivo a parita' di contenuto
4. **Mobile-first** - Google indicizza prima la versione mobile
5. **Dati strutturati** - Schema.org per rich snippets
6. **Link interni** - Ogni pagina importante deve essere collegata internamente
7. **HTTPS** - Obbligatorio
8. **Contenuto originale** - Penalizzazione per clickbait e contenuti superficiali

### Novita' Google Marzo 2026
- **AI Analysis Tools** in Search Console - analisi con linguaggio naturale
- **Query Groups** in Search Console Insights - raggruppamento query simili
- **Discover Core Update** (5 Feb 2026) - algoritmo separato per Google Discover
- **SVT e VSI** - Nuove metriche per stabilita' visiva
- **Soglie INP piu' strette** - Google ha reso piu' severi i requisiti di interattivita'
- Rimosso supporto per **practice problem** e **dataset structured data**

### Checklist SEO per Ogni Pagina
- [ ] Title tag unico (max 60 caratteri)
- [ ] Meta description unica (max 160 caratteri)
- [ ] H1 unico per pagina
- [ ] Alt text su tutte le immagini
- [ ] URL SEO-friendly (slug descrittivi)
- [ ] Link interni verso pagine correlate
- [ ] Open Graph tags per condivisione social
- [ ] Canonical URL impostato
- [ ] Dati strutturati Schema.org (LocalBusiness, RealEstateListing)
- [ ] Immagini ottimizzate (WebP + lazy loading)

### Routine di Monitoraggio
- **Settimanale:** Controllare report performance in Search Console
- **Mensile:** Analisi dettagliata metriche SEO e Core Web Vitals
- **Trimestrale:** Audit completo contenuti e struttura sito
- **Ad ogni aggiornamento Google:** Verificare impatto sul sito

---

## REGOLE OPERATIVE PER CLAUDE

### Quando lavori sul sito, SEMPRE:
1. **Leggi prima** il file che vuoi modificare - mai proporre modifiche al buio
2. **Testa** che le modifiche non rompano niente
3. **Ottimizza** per mobile-first
4. **Mantieni** la coerenza del design esistente
5. **Non aggiungere** librerie/framework non necessari - il sito e' volutamente leggero
6. **Commit** chiari e descrittivi in italiano
7. **Mai toccare** la configurazione DNS o i record MX
8. **Controlla** Core Web Vitals dopo modifiche significative
9. **Aggiorna** sitemap.xml quando aggiungi/rimuovi pagine
10. **Verifica** che tutte le pagine abbiano meta tag SEO completi

### Quando lavori sulle email/cPanel:
1. **NON eliminare** mai account email senza conferma esplicita
2. **NON modificare** record DNS senza conferma esplicita
3. **Suggerisci** sempre prima e aspetta il via libera
4. **Backup** prima di eliminazioni importanti

### Stile di Comunicazione:
- Rispondi in italiano
- Sii diretto e pratico
- Usa termini tecnici ma spiega quando necessario
- Proponi sempre prima di agire su operazioni irreversibili

---

## CHANGELOG AGGIORNAMENTI

### v1.0 - 2 Marzo 2026 (Creazione)
- Creato prompt iniziale con stato aggiornamenti Google Marzo 2026
- Documentate soglie Core Web Vitals 2026 (LCP, INP, CLS, SVT, VSI)
- Registrate novita': AI Analysis Tools in GSC, Query Groups, Discover Core Update
- Mappata struttura completa del progetto
- Documentata gestione cPanel con lista eliminazioni/mantenimento
- Impostate regole operative per Claude

---

## NOTE PER L'UTENTE

### Come usare questo prompt:
1. **All'inizio di ogni sessione** con Claude, copia/incolla questo file come contesto
2. Claude fara' automaticamente una verifica web degli aggiornamenti Google
3. Se ci sono novita', Claude aggiornera' questo file
4. Controlla il CHANGELOG per vedere cosa e' cambiato nel tempo

### Questo file si trova in:
- **Nel repository:** `/SKILL-KILLER.md`
- **Scaricalo** e tienine una copia anche in locale

### Per emergenze:
- Il sito e' su GitHub Pages - se qualcosa va storto, basta fare rollback del commit
- Le email sono su cPanel - completamente separate dal sito
- Il dominio e il DNS sono su cPanel - NON toccarli mai senza sapere cosa fai

---

*"Skill Killer" - Perche' con le competenze giuste, si ammazzano i problemi prima che nascano* 😄
