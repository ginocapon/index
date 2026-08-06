# SKILL — Trasparenza AI Act UE (Reg. 2024/1689)

> **PRIORITÀ PERMANENTE** — vale per **ogni** pagina, contenuto, foto, assistente digitale e nuova pubblicazione sul sito Righetto Immobiliare.
> Caricare **sempre** insieme a `skill-essentials.md` e `skill-massimo-punteggio.md`.

---

## 1. Perché esiste

Il **Regolamento (UE) 2024/1689** (AI Act) impone trasparenza quando si interagisce con sistemi di IA o quando contenuti sintetici/manipolati possono indurre in errore l'utente (art. 50 e obblighi correlati).

**Sul sito Righetto:**

| Elemento | Natura reale | Obbligo trasparenza |
|----------|--------------|---------------------|
| **Linda** (`js/chatbot.js`) | Assistente **automatizzato a regole** — non LLM generativo | Sì: etichetta chiara, non presentarlo come persona umana in tempo reale |
| **Landing chat** (`js/chat-flow.js`) | Percorso guidato automatizzato | Sì: box informativo in apertura |
| **Foto annunci** | Immagini reali, possibile ottimizzazione digitale | Sì: nota su scheda e catalogo |
| **Hero blog / grafiche** | Possono essere elaborate digitalmente (anche IA) | Sì: barra sito + privacy §15.2 |
| **Testi editoriali** | Scritti/redatti da persone; stime orientative in chat | Barra sito + link privacy |

---

## 2. Implementazione tecnica (non duplicare)

| Asset | Ruolo |
|-------|--------|
| `css/site-ai-disclosure.css` | Stili barra footer, note foto, disclosure chat |
| `js/site-ai-disclosure.js` | Barra footer su tutte le pagine pubbliche; note catalogo/immobile; testi condivisi `RigAiDisclosure.TEXT` |
| `js/ga-consent.js` | Carica CSS+JS disclosure su pagine con analytics (copertura sito) |
| `privacy.html#trasparenza-digitale` | Informativa legale completa (§15) |
| `privacy.html#assistente-digitale` | Anchor assistente Linda |

**Non** creare disclaimer diversi per pagina: usare i testi centralizzati in `site-ai-disclosure.js` o aggiornarli lì.

---

## 3. Checklist BLOCCANTE — ogni modifica al sito

### 3.1 Pagine HTML (nuove o modificate)

- [ ] La pagina include `ga-consent.js` (o equivalente che carica `site-ai-disclosure`) — **no admin**
- [ ] Footer: barra `#rig-ai-act-bar` visibile (iniettata da JS se `ga-consent` presente)
- [ ] Title/meta invariati rispetto a §1.2 `skill-essentials.md`

### 3.2 Chatbot Linda

- [ ] Header: «Assistente digitale automatizzato (sistema a regole)» — **mai** solo «Online — rispondiamo subito»
- [ ] Welcome card: box `chat-welcome-disclosure`
- [ ] Primo messaggio dopo «Inizia a chattare»: nota `chat-msg-disclosure`
- [ ] Dopo modifica: bump `chatbot.js?v=N` su **tutte** le pagine che lo caricano

### 3.3 Landing conversazionali (`landing-chat-*.html`)

- [ ] `chat-flow.js` mostra `cf-ai-disclosure` in apertura
- [ ] Bump `chat-flow.js?v=N` se modificato

### 3.4 Foto e media

- [ ] **Catalogo** (`immobili.html`): nota `#rig-catalog-ai-note` (JS)
- [ ] **Scheda immobile** (`immobile.html`): nota `#rig-immobile-ai-note` sotto galleria (JS)
- [ ] **Blog hero** illustrativa: didascalia onesta se non foto reale del territorio (§8.2.5 SKILL-2.0)
- [ ] **Social/reel**: copy coerente con §15.2 privacy (vedi `skill-social-automation.md`)

### 3.5 Contenuti editoriali

- [ ] Articoli blog: nessun claim inventato; dati solo con fonte (regola d'oro)
- [ ] Box AEO «Cosa non è» dove previsto da §8.2.5
- [ ] Non presentare stime chat come perizie ufficiali

### 3.6 Privacy e cookie

- [ ] Modifiche assistente/media → aggiornare `privacy.html` §15 e data aggiornamento hero
- [ ] Cookie policy: «assistente digitale automatizzato», non «AI» generica senza contesto

---

## 4. Testi standard (italiano)

Usare `window.RigAiDisclosure.TEXT` — chiavi:

- `footer` — barra sito
- `photo` — scheda annuncio
- `catalog` — catalogo immobili
- `chatHeader` — sottotitolo header Linda
- `chatWelcome` — welcome card / landing chat
- `chatFirst` — primo messaggio post-avvio chat

Link informativa: **`privacy#trasparenza-digitale`**

---

## 5. Versioning cache

| File | Bump `?v=` quando |
|------|-------------------|
| `site-ai-disclosure.css` | Modifica stili |
| `site-ai-disclosure.js` | Modifica testi o logica injection |
| `ga-consent.js` | Modifica loader disclosure |
| `chatbot.js` | Qualsiasi modifica Linda |
| `chat-flow.js` | Qualsiasi modifica landing chat |

---

## 6. Cosa NON fare

- ❌ Presentare Linda come operatore umano in tempo reale
- ❌ Omettere la barra/footer disclosure su pagine pubbliche nuove
- ❌ Usare foto IA per annunci immobiliari senza dichiararlo (policy: foto reali; ottimizzazione ammessa con nota)
- ❌ Inventare conformità legali non verificate — rimandare a §15 privacy per il dettaglio
- ❌ CDN esterni per script disclosure

---

## 7. Collegamenti

- `TEST-SKILL/SKILL-2.0.md` §**8.1f**
- `TEST-SKILL/skill-content.md` — hero blog
- `TEST-SKILL/skill-forms-leads.md` — form in landing chat
- `TEST-SKILL/skill-social-automation.md` — post e reel
- `TEST-SKILL/context-map.json` → task `ai_act_compliance`

---

*Aggiornato: 6 agosto 2026 — priorità permanente su tutti i task agente.*
