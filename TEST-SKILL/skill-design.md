# SKILL-DESIGN — Righetto Immobiliare
> Carica per: creare/modificare HTML, CSS, componenti UI, layout, animazioni.
> Versione estratta da SKILL-2.0.md — Marzo 2026

---

## 1. VARIABILI CSS

```css
:root {
  /* COLORI BRAND */
  --primario:    #2C4A6E;
  --primario-2:  #3A5F8C;   /* hover */
  --primario-3:  #4E789A;   /* accento light */

  /* CTA ARANCIONE (SOLO con testo scuro — mai con white) */
  --oro:         #FF6B35;   /* var(--oro) = arancione conversione */
  --accent:      #FF6B35;
  --accent-2:    #FF8F5E;   /* hover CTA */
  --accent-3:    #FFB899;

  /* NEUTRALI */
  --nero:        #152435;   /* testo principale */
  --bianco:      #F7F5F1;   /* background principale */
  --sfondo:      #ECE7DF;   /* sezioni alternate */
  --sfondo-2:    #E1DBD1;   /* card backgrounds */
  --carta:       #F2EDE7;   /* input/form */

  /* TESTO */
  --testo:       #152435;
  --grigio:      #6B7A8D;   /* secondario */
  --grigio-2:    #9AACBD;   /* disabled/hint */

  /* STATUS */
  --verde:       #1E8449;
  --rosso:       #C0392B;

  /* LAYOUT */
  --nav-h:       74px;
  --max-w:       1200px;
  --max-w-lg:    1400px;
  --radius:      12px;
  --radius-sm:   8px;
  --radius-pill: 50px;
}
@media (max-width: 768px) { :root { --nav-h: 64px; } }
```

> **REGOLA colore:** `var(--oro)` / `#FF6B35` — SOLO con `var(--nero)` #152435 come testo. MAI con `color: white` (ratio 1.54:1 = FAIL WCAG).

### Sfondo brand (site-wide)

- **CSS:** `css/rig-brand-atmosphere.css` · **JS:** `js/rig-brand-atmosphere.js`
- Caricati da `js/ga-consent.js` su tutte le pagine pubbliche (no admin)
- `body.rig-sugar-paper` — grain + monogramma **RI** (Righetto Immobiliare) in watermark fisso
- Stesso linguaggio di Solar Time (`sugar-paper` + tre istanze ruotate)
- **Vietato** `body > * { position: relative }` per lo stacking: stacca `position:fixed` da `.nav-mobile` / overlay e crea un buco vuoto sopra l'hero. Alzare solo `main`, `footer`, `article`.
- Watermark RI: `.rig-brand-watermark` a **z-index 3** + `mix-blend-mode: multiply` (sopra main z-index 2, sotto grain z-index 20–21). Menu/header a z-index ≥100.

---

## 2. TIPOGRAFIA

| Elemento | Font | Size | Weight | Line-height |
|---|---|---|---|---|
| H1 (hero) | Cormorant Garamond | clamp(2.5rem, 6vw, 5rem) | 700 | 1.05 |
| H2 (sezione) | Cormorant Garamond | clamp(2rem, 3.5vw, 3rem) | 700 | 1.15 |
| H3 (card/sub) | Cormorant Garamond | 1.35rem | 600 | 1.3 |
| Body | Montserrat | 0.9rem–1.05rem | 400 | 1.85 |
| Label/Tag | Montserrat | 0.62rem–0.78rem | 600–800 | 1.4 |
| CTA button | Montserrat | 0.78rem–0.85rem | 800 | 1.2 |

- Label/tag: SEMPRE `text-transform: uppercase; letter-spacing: 1.5px–3.5px`
- H1 accent: `<strong>` con `font-weight: 600; font-style: italic`
- Hero text su sfondo scuro: `text-shadow: 0 2px 24px rgba(8,16,30,0.55)`

---

## 3. SPACING SYSTEM

| Contesto | Desktop | Tablet | Mobile |
|---|---|---|---|
| Sezione padding | 90px 44px | 60px 28px | 60px 20px |
| Card padding | 28px 24px | 24px 20px | 20px 16px |
| Grid gap | 24px | 24px | 16px |
| Eyebrow → Heading | 12px–22px | — | — |
| Content → CTA | 40px | — | — |

---

## 4. BREAKPOINT RESPONSIVE

| Breakpoint | Target | Azione |
|---|---|---|
| `max-width: 1024px` | Laptop | Grid 3→2 colonne |
| `max-width: 900px` | Tablet landscape | Footer/form collapse |
| **`max-width: 768px`** | **Tablet portrait** | **Navbar → hamburger, grid → 1 col** |
| `max-width: 600px` | Mobile grande | Card → 1 col, padding ridotto |
| `max-width: 520px` | Mobile piccolo | Popup/modal compatti |

---

## 5. SHADOW SYSTEM

```css
--shadow-xs:  0 2px 16px rgba(21,36,53,0.05);
--shadow-sm:  0 6px 20px rgba(21,36,53,0.08);
--shadow-md:  0 20px 50px rgba(21,36,53,0.14);
--shadow-lg:  0 30px 100px rgba(0,0,0,0.4);
--shadow-cta: 0 6px 20px rgba(184,212,74,0.35);
```

---

## 6. ANIMAZIONI

```css
--ease-out:    cubic-bezier(0.16, 1, 0.3, 1);
--ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
--ease-smooth: cubic-bezier(0.22, 1, 0.36, 1);

/* Scroll Reveal */
.sr       { opacity:0; transform: translateY(28px);  transition: all 0.7s var(--ease-out); }
.sr-left  { opacity:0; transform: translateX(-32px); transition: all 0.7s var(--ease-out); }
.sr-right { opacity:0; transform: translateX(32px);  transition: all 0.7s var(--ease-out); }
.sr-scale { opacity:0; transform: scale(0.88);       transition: all 0.7s var(--ease-out); }
.sr.visible, .sr-left.visible, .sr-right.visible, .sr-scale.visible { opacity:1; transform:none; }

/* Stagger delays */
.sr-d1 { transition-delay: 0.08s; } .sr-d2 { transition-delay: 0.16s; }
.sr-d3 { transition-delay: 0.24s; } .sr-d4 { transition-delay: 0.32s; }

@keyframes slowZoom { from { transform: scale(1.05); } to { transform: scale(1.10); } }
@keyframes fadeUp   { from { opacity:0; transform: translateY(36px); } to { opacity:1; transform:none; } }

.card-lift { transition: transform 0.3s var(--ease-bounce), box-shadow 0.3s ease; }
.card-lift:hover { transform: translateY(-6px); box-shadow: var(--shadow-md); }

@media (prefers-reduced-motion: reduce) {
  .sr, .sr-left, .sr-right, .sr-scale { opacity:1; transform:none; transition:none; }
}
```

> **REGOLA animazioni:** No `filter: blur` — solo `opacity` e `transform`. No `will-change` permanente.

---

## 7. COMPONENTI HTML

### Card Grid
```html
<div class="card-grid">
  <div class="card card-lift sr sr-d1">
    <div class="card-icon">[emoji/svg]</div>
    <h3 class="card-title">[Titolo]</h3>
    <p class="card-desc">[Descrizione]</p>
    <a href="/pagina" class="card-link link-reveal">Scopri di più →</a>
  </div>
</div>
```
```css
.card-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:24px; }
@media(max-width:900px) { .card-grid { grid-template-columns:repeat(2,1fr); } }
@media(max-width:600px) { .card-grid { grid-template-columns:1fr; } }
.card { background:var(--bianco); border:1px solid rgba(44,74,110,0.08); border-radius:var(--radius); padding:28px 24px; }
.card-title { font-family:'Cormorant Garamond',serif; font-size:1.35rem; font-weight:600; margin-bottom:8px; }
.card-desc { font-size:0.85rem; color:var(--grigio); line-height:1.75; margin-bottom:16px; }
```

### CTA Buttons
```css
/* Primario — arancione su sfondo scuro */
.btn-accent {
  display:inline-block; background:var(--accent); color:var(--nero);
  padding:15px 32px; border-radius:var(--radius-sm);
  font-family:'Montserrat',sans-serif; font-weight:800; font-size:0.78rem;
  letter-spacing:1px; text-transform:uppercase; transition:all 0.25s;
}
.btn-accent:hover { background:var(--accent-2); transform:translateY(-2px); box-shadow:var(--shadow-cta); }

/* Secondario — outline su sfondo scuro */
.btn-outline {
  display:inline-block; border:1px solid rgba(255,255,255,0.2); color:#fff;
  padding:15px 32px; border-radius:var(--radius-sm);
  font-family:'Montserrat',sans-serif; font-weight:600; font-size:0.78rem;
  letter-spacing:1px; text-transform:uppercase; transition:all 0.25s;
}
.btn-outline:hover { border-color:var(--accent); color:var(--accent); }

/* Terziario — scuro su sfondo chiaro */
.btn-dark {
  display:inline-block; background:var(--nero); color:#fff;
  padding:15px 32px; border-radius:var(--radius-sm);
  font-family:'Montserrat',sans-serif; font-weight:700; font-size:0.78rem;
  letter-spacing:1px; text-transform:uppercase; transition:all 0.25s;
}
.btn-dark:hover { background:var(--accent); color:var(--nero); transform:translateY(-2px); }
```

### FAQ / Accordion
```html
<div class="faq-list">
  <div class="faq-item sr">
    <button class="faq-btn" aria-expanded="false">
      <span class="faq-q">[Domanda]</span>
      <span class="faq-icon">+</span>
    </button>
    <div class="faq-answer"><p>[Risposta]</p></div>
  </div>
</div>
```
```css
.faq-item { background:var(--bianco); border-radius:var(--radius); border:1px solid rgba(44,74,110,0.09); margin-bottom:12px; overflow:hidden; }
.faq-btn { width:100%; text-align:left; padding:20px 22px; cursor:pointer; display:flex; justify-content:space-between; align-items:center; gap:14px; background:none; border:none; font-family:'Montserrat',sans-serif; font-size:0.92rem; font-weight:600; color:var(--testo); }
.faq-icon { width:28px; height:28px; border-radius:50%; background:var(--sfondo); border:1px solid rgba(44,74,110,0.12); display:flex; align-items:center; justify-content:center; transition:all 0.3s; flex-shrink:0; }
.faq-item.open .faq-icon { background:var(--accent); color:var(--nero); transform:rotate(45deg); }
.faq-answer { max-height:0; overflow:hidden; transition:max-height 0.4s ease, padding 0.3s ease; padding:0 22px; font-size:0.85rem; color:var(--grigio); line-height:1.75; }
.faq-item.open .faq-answer { max-height:500px; padding:0 22px 20px; }
```
```javascript
document.querySelectorAll('.faq-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const item = btn.closest('.faq-item');
    const wasOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
    if (!wasOpen) item.classList.add('open');
    btn.setAttribute('aria-expanded', !wasOpen);
  });
});
```

---

## 7c. HERO LANDING — MOBILE (iPhone)

Pattern validato su `landing-costi-locazione-inquilino.html` (luglio 2026).

**Problema tipico:** testo bianco illeggibile — il blocco copy con `margin-top` negativo finisce sullo sfondo chiaro del body, non sulla foto.

**Layout mobile obbligatorio (split, non overlap):**

| Elemento | Regola |
|----------|--------|
| `.v-hero` | `min-height: auto`, `background: var(--nero)` |
| `.v-hero-media` | Altezza fissa ~38–44vh, `flex: none` |
| `.v-hero-copy` | **Sotto** la foto, `margin-top: 0`, `background: var(--nero)` |
| Viewport | `viewport-fit=cover` + safe-area su body/footer |
| Input form | `font-size: 16px` minimo (no zoom Safari) |
| Tabelle | Hint scroll + `-webkit-overflow-scrolling: touch` |

**Vietato su mobile:** testo bianco che si estende oltre l'overlay scuro della foto verso il body chiaro.

**Tabelle larghe:** prima di `.tbl-wrap` inserire `<p class="tbl-hint" aria-hidden="true">↔ Scorri la tabella…</p>` (visibile solo `@media max-width 767px`); su `.tbl-wrap` usare `-webkit-overflow-scrolling: touch`.

Skill operativa: `.cursor/skills/righetto-fix-mobile/SKILL.md` (lezione consolidata).

---

## 7b. FORM LEAD (landing / servizi)

Ogni landing con modulo contatto deve rispettare **`skill-forms-leads.md`** (logica) e questo blocco UI:

- Wrapper `.v-form` o `.fbox-body` + `onsubmit` che blocca submit nativo
- Checkbox GDPR `.v-chk` / `.fchk` con `required`
- Pulsante submit full-width, stato disabled + testo «Invio in corso...»
- Success box `.v-success` / `.fsuccess` — sfondo `#e8f5e9`, titolo serif, nascondere campi con `.is-sent .v-form-fields { display:none }`
- **Un solo passaggio** — niente CTA «Continua su Contatti» come unico invio

Script in fondo pagina: `config.js` + Supabase **senza defer** se handler inline subito sotto (vedi skill-forms-leads).

---

## 8. CACHE E PERFORMANCE (Regole tecniche)

```apache
# .htaccess — cache standard (per hosting cPanel, NON GitHub Pages)
ExpiresByType image/webp "access plus 1 year"
ExpiresByType font/woff2 "access plus 1 year"
ExpiresByType text/css "access plus 1 year"
ExpiresByType application/javascript "access plus 1 year"
Header set Cache-Control "public, max-age=31536000, immutable"
ExpiresByType text/html "access plus 0 seconds"
Header set Cache-Control "no-cache, must-revalidate"  # Solo per HTML
AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml
```

**Checklist performance per ogni nuova pagina:**
- [ ] CSS/JS con `?v=N` (cache-busting obbligatorio)
- [ ] Immagini in formato WebP
- [ ] Font con `font-display: swap` + preload above-fold
- [ ] CSS critical inline, rest deferred (`media="print" onload="this.media='all'"`)
- [ ] JS con `defer` (non `async` se dipendenze tra script) — **eccezione:** pagine con form lead inline → `config.js` + Supabase senza defer (skill-forms-leads)
- [ ] Nessun `loading="lazy"` above-the-fold
- [ ] Security headers: `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`

---

## 14. ARTICOLI BLOG — SCALA TIPOGRAFICA E CONTRASTI (ottobre 2026)

**Fonte unica:** `css/rig-blog-article.css` (linkato in **ogni** `blog-*.html`, DOPO `blog-rich.css` e `blog-lead-form.css`, con `?v=N`). Allinea gli articoli ai token delle pagine principali (`css/rig-type-scale.css`). **Non** ridefinire H1/H2/colori grigi nello `<style>` inline del singolo articolo.
**Misura:** `scripts/audit-blog-design.js` (browser, nessuna dipendenza) · **Applica:** `python scripts/apply-blog-article-css.py --all`.

### 14.1 Soglie misurabili (desktop 1440 e mobile 390)
| Elemento | Regola |
|---|---|
| H1 articolo | ≥ 40px desktop · ≥ 28px mobile · peso **≥ 600** (mai 300 su foto) · `clamp(1.9rem,3.6vw,2.8rem)` |
| H2 di sezione (serif) | ≥ 28px desktop · ≥ 24px mobile · peso ≥ 600 · `clamp(1.55rem,2.6vw,2rem)` |
| Gerarchia titoli | un solo H1 · nessun salto (H2→H4 vietato) |
| Paragrafi e liste | **≥ 1rem** (minimo assoluto 0.95rem) · line-height ≥ 1.8 |
| Testi secondari (label, didascalie, badge, fonti) | **≥ 0.7rem (11.2px)** — mai 0.5–0.68rem. Eccezione: marchio sovrapposto «FOTO AI» (AI Act) |
| Campi form (`input/select/textarea`) | **16px** (sotto, iOS Safari zooma) |
| Contrasto testo | ≥ **4.5:1** (≥ 3:1 solo se ≥ 24px o ≥ 18.66px bold) |
| `--grigio` | **`#556578`** (5,48:1 su bianco · 4,85:1 su sfondo). Vietato `#6B7A8D` (≈4,0:1 ✗) |
| Arancio `#FF6B35` | **solo** come sfondo con testo `#152435` (5,55:1) o come filetto/icona. Mai come colore di testo su fondo chiaro (2,3:1 ✗) né testo bianco su arancio (2,9:1 ✗) |
| Testo con alpha | `rgba(255,255,255,.5)` ecc. vietato sotto `.75` su fondi scuri |
| Overflow | nessuno scroll orizzontale a 390px (griglie: `minmax(0,1fr)` + `min-width:0`) |
| Link interni | senza `.html` (eccezione ammessa: `admin.html` iniettato da `nav-mobile.js`) |
| Data | «Aggiornamento: …» visibile **e** `dateModified` nel JSON-LD, coerenti |

### 14.2 Componenti SCURI con testo chiaro (fonte di bug ricorrenti)
`.cta-banner`, `.blog-rich-cta-strip`, `.stat-card`, `.highlight-box` hanno sfondo `--nero/--blu` e testo bianco.
- **Vietato** inserirli in regole che azzerano o schiariscono lo sfondo (`unset`, `color-mix(...bianco...)`) — vedi `css/rig-brand-atmosphere.css`: lì devono comparire **solo** componenti con fondo chiaro.
- Ogni `<div>` deve essere **chiuso**: un `.stat-card` aperto fa ereditare `color:#fff` ai riquadri successivi (testo bianco su fondo pesca, 1,1:1). Il CSS condiviso ha una protezione (`.righetto-sol{color:var(--nero)}`) ma l'HTML va corretto.
- Dopo ogni modifica a un CSS globale: controllare **un articolo con banner CTA e uno con `.stat-card`** a occhio (screenshot), non solo con il validatore.

### 14.3 Checklist prima del commit di un articolo nuovo o modificato
1. `<link rel="stylesheet" href="css/rig-blog-article.css?v=N">` presente, dopo `blog-lead-form.css`.
2. Nessun `font-size` < `.7rem`, nessun `color:#6B7A8D`, nessun `h1{font-weight:300}` nello `<style>` inline.
3. Audit: aprire la pagina via `python -m http.server 8765` e lanciare `rigAuditBatch(['blog-xxx'],1440)` e `…,390)` → **0 issues** (istruzioni in testa a `scripts/audit-blog-design.js`).
4. Gli script `scripts/build_blog_*.py` devono emettere il link al punto 1 (template `HEAD`/`CSS`): in caso contrario l'articolo nasce non conforme.

### 14.4 Grafici editoriali (`figure.chart-wrap`)
- Stile condiviso in **`rig-blog-article.css`**: min-height SVG **220–320px**, didascalia ≥ **0.78rem**.
- SVG inline: titolo **≥ 16px**, testo box **≥ 13px**, rettangoli **allungati** (non etichette microscopiche).
- Flussi e confronti: frecce **`#FF6B35`** con **`marker-end`**, `stroke-width` **≥ 3.5**; confronti a 2 box → freccia «vs» tra i blocchi.
- Batch esistenti: `python scripts/rebuild_blog_chart_svg.py` (rigenera layout, testo **15–16px grassetto centrato** nei box; non scalare SVG a caso). Alias: `upgrade_blog_chart_svg.py`.
- KPI e statistiche: **`.kpi-strip`**, **`.stats-grid`**, **`.stat-card`**, **`.hero-stats-row`**, **`.aeo-box`** — tipografia e padding solo in **`rig-blog-article.css`** (no micro-font inline).

**Stato 5 ott 2026:** con il CSS condiviso 97/147 articoli sono a 0 issues; i residui (≈50) sono casi per-pagina elencati in `data/blog-design-audit-2026-10-05.json`; prompt di esecuzione per un'altra AI: `TEST-SKILL/prompt-fix-blog-design-2026-10.md`.
