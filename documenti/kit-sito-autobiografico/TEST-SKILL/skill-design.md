# SKILL-DESIGN — UI, mobile, performance

> Carica per: CSS, layout, fix iPhone, hero, CTA, accessibilità.

---

## 1. Mobile-first

- Progetta da **375px** in su
- Test obbligatorio dopo ogni modifica layout
- Menu hamburger / nav accessibile
- Form: input ≥ 16px font (evita zoom iOS)
- Touch target ≥ **44px**

---

## 2. Performance (CWV)

- Preload hero image + font critici
- **Mai** `loading="lazy"` su hero/LCP
- Immagini WebP, dimensioni esplicite (width/height)
- CSS above-fold inline o critico; resto differito
- No animazioni pesanti above-fold
- No `filter: blur` su animazioni
- No `will-change` permanente

---

## 3. Accessibilità WCAG AA

- Contrasto testo/CTA ≥ **4,5:1**
- **Vietato:** arancione `#FF6B35` (o simile) + testo bianco
- Focus visibile su link e bottoni
- `aria-label` su icon-only (menu, social)
- Skip link opzionale ma consigliato

---

## 4. Spacing (mobile)

- Padding sezione: ~60px 20px
- Gap grid: 16px
- Spazio titolo → contenuto: 22–32px
- CTA primario sopra piega su home e landing contatto

---

## 5. Tipografia autobiografica

- Titoli: serif o display coerente con brand personale
- Body: sans leggibile (16px+ mobile)
- Line-height 1.5–1.6
- Max-width testo lungo ~65–75 caratteri per riga

---

## 6. Foto

- Foto **reali** del titolare e palestra
- Alt text descrittivo
- Hero leggera (< 150 KiB target)
- Lazy load **solo** sotto piega

---

## 7. Cache-busting

Ogni modifica CSS/JS → incrementa `?v=N` nel link HTML.

---

## 8. Fix mobile — checklist rapida

- [ ] Overflow orizzontale assente
- [ ] Testo non tagliato
- [ ] CTA cliccabile
- [ ] Form inviabile
- [ ] Menu chiudibile
- [ ] Immagini non escono dallo schermo
