/* ═══════════════════════════════════════════════════════════════
   audit-blog-design.js — audit tipografia/contrasto/layout degli articoli blog
   Regola di riferimento: TEST-SKILL/skill-design.md §14 (ottobre 2026).

   USO (nessuna dipendenza, solo browser):
   1) python -m http.server 8765   (dalla root del repo)
   2) aprire http://localhost:8765/index.html, poi in console / CDP:
        const s = await (await fetch('/scripts/audit-blog-design.js')).text(); eval(s);
        const r = await rigAuditBatch(['blog-xxx','blog-yyy'], 1440);   // slug senza .html
        const m = await rigAuditBatch(['blog-xxx','blog-yyy'], 390);    // mobile
   3) r.summary = conteggi · r.pages = dettaglio per pagina (solo le non conformi hanno `issues`)

   Output compatto apposta (poche righe per pagina) → pochi token se letto da un'AI.
   ═══════════════════════════════════════════════════════════════ */
(function () {
  const SKIP = 'script,style,noscript,[class*=chat],[id*=chat],[class*=cookie],[id*=cookie],[class*=welcome],[class*=disclosure],[class*=ai-badge]';

  const parse = (c) => {
    if (!c) return null;
    // i browser moderni restituiscono anche color(srgb 0.97 0.88 0.84 / 0.5)
    const s = c.match(/color\(srgb\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)(?:\s*\/\s*([\d.]+))?\)/);
    if (s) return { r: s[1] * 255, g: s[2] * 255, b: s[3] * 255, a: s[4] !== undefined ? +s[4] : 1 };
    const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(/[,\s/]+/).filter(Boolean).map(parseFloat);
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  };
  const lum = ({ r, g, b }) => {
    const f = (c) => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const over = (fg, bg) => ({ r: fg.r * fg.a + bg.r * (1 - fg.a), g: fg.g * fg.a + bg.g * (1 - fg.a), b: fg.b * fg.a + bg.b * (1 - fg.a), a: 1 });

  function bgOf(el, win) {
    const layers = [];
    for (let e = el; e; e = e.parentElement) {
      const cs = win.getComputedStyle(e);
      const bg = parse(cs.backgroundColor);
      if (bg && bg.a > 0) { layers.push(bg); if (bg.a >= 0.99) break; }
      if (cs.backgroundImage && cs.backgroundImage !== 'none' && /gradient|url/.test(cs.backgroundImage)) {
        const m = cs.backgroundImage.match(/rgba?\([^)]+\)|color\(srgb[^)]+\)/);
        if (m) { const g = parse(m[0]); if (g) { layers.push(g); break; } }
      }
    }
    let base = { r: 247, g: 245, b: 241, a: 1 };
    for (let i = layers.length - 1; i >= 0; i--) base = over(layers[i], base);
    return base;
  }

  function auditPage(doc, win) {
    const issues = [];
    const vw = win.innerWidth;
    const px = (el) => parseFloat(win.getComputedStyle(el).fontSize);
    const fw = (el) => parseInt(win.getComputedStyle(el).fontWeight, 10);

    // ── Titoli ──
    const h1 = doc.querySelector('h1');
    // H2 "di sezione" = serif (Cormorant); gli H2 in Montserrat sono etichette di riquadri (AEO box, Righetto, FAQ)
    const h2s = [...doc.querySelectorAll('.art-content h2, article h2, main h2')]
      .filter((e) => !e.closest(SKIP) && /Cormorant/i.test(win.getComputedStyle(e).fontFamily));
    const h2 = h2s[0];
    const m = { vw };
    if (!h1) issues.push('H1 assente');
    else {
      m.h1 = Math.round(px(h1)) + '/' + fw(h1);
      // desktop ≥ 40px, mobile ≥ 28px, peso ≥ 600
      const minH1 = vw >= 768 ? 40 : 28;
      if (px(h1) < minH1) issues.push('H1 ' + Math.round(px(h1)) + 'px < ' + minH1);
      if (fw(h1) < 600) issues.push('H1 peso ' + fw(h1) + ' < 600');
    }
    if (h2) {
      m.h2 = Math.round(px(h2)) + '/' + fw(h2);
      const minH2 = vw >= 768 ? 28 : 24;
      if (px(h2) < minH2) issues.push('H2 ' + Math.round(px(h2)) + 'px < ' + minH2);
      if (fw(h2) < 600) issues.push('H2 peso ' + fw(h2) + ' < 600');
    } else issues.push('nessun H2');
    const lvls = [...doc.querySelectorAll('h1,h2,h3,h4')].filter((e) => !e.closest(SKIP) && e.getBoundingClientRect().width > 0).map((e) => +e.tagName[1]);
    for (let i = 1; i < lvls.length; i++) if (lvls[i] - lvls[i - 1] > 1) { issues.push('salto titoli H' + lvls[i - 1] + '→H' + lvls[i]); break; }

    // ── Testo corrente ──
    const p = doc.querySelector('.art-content p, article p');
    if (p) { m.p = px(p).toFixed(1); if (px(p) < 15.2) issues.push('paragrafo ' + px(p).toFixed(1) + 'px < 15,2 (0,95rem)'); }

    // ── Testi piccoli e contrasto ──
    let tiny = 0, low = 0; const lowS = [], tinyS = [];
    doc.querySelectorAll('body *').forEach((el) => {
      if (el.closest(SKIP)) return;
      if (el.closest('svg')) return; // etichette di infografiche SVG: scalano con il viewBox, non misurabili in px
      if (el.matches && el.matches('.rig-ai-photo-watermark')) return; // marchio FOTO AI sovrapposto (AI Act): badge decorativo, non testo corrente
      // testo sopra la foto dell'hero: lo sfondo è un'immagine, non misurabile → escluso (verificare a occhio)
      const overPhoto = !!el.closest('.art-hero, .hero, [class*=hero]');
      if (!([...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 2))) return;
      const r = el.getBoundingClientRect(); if (!r.width || !r.height) return;
      const cs = win.getComputedStyle(el);
      const size = parseFloat(cs.fontSize);
      if (size < 11.2) { tiny++; if (tinyS.length < 3) tinyS.push(size.toFixed(1) + ' ' + (el.className || el.tagName).toString().slice(0, 22)); } // < 0,7rem
      if (overPhoto) return;
      const fg = parse(cs.color); if (!fg) return;
      const bg = bgOf(el, win), f = over(fg, bg);
      const L1 = lum(f), L2 = lum(bg);
      const ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
      const large = size >= 24 || (size >= 18.66 && parseInt(cs.fontWeight, 10) >= 700);
      if (ratio < (large ? 3 : 4.5)) { low++; if (lowS.length < 3) lowS.push(ratio.toFixed(2) + ' ' + (el.className || el.tagName).toString().slice(0, 22)); }
    });
    m.tiny = tiny; m.low = low;
    if (tiny) issues.push(tiny + ' testi < 0,7rem (' + tinyS.join('; ') + ')');
    if (low) issues.push(low + ' contrasti < AA (' + lowS.join('; ') + ')');

    // ── Form: 16px (no zoom iOS) ──
    const ins = [...doc.querySelectorAll('input:not([type=checkbox]):not([type=radio]):not([type=hidden]),select,textarea')].filter((e) => e.getBoundingClientRect().width > 0 && !e.closest(SKIP) && !/^rig-hp/.test(e.id || e.name || ''));
    const smallInEls = ins.filter((e) => px(e) < 16);
    if (smallInEls.length) issues.push(smallInEls.length + ' campi form < 16px (' + smallInEls.slice(0, 2).map((e) => (e.id || e.name || e.tagName) + ':' + px(e).toFixed(1)).join('; ') + ')');

    // ── Overflow orizzontale ──
    if (doc.documentElement.scrollWidth > vw + 1) issues.push('overflow orizzontale ' + doc.documentElement.scrollWidth + ' > ' + vw);
    const beyond = [...doc.querySelectorAll('main *, article *, .art-content *')].filter((e) => e.children.length === 0 && !e.closest('.cats,.cats-inner,table,.tbl-wrap,pre,[class*=scroll],' + SKIP) && e.getBoundingClientRect().right > vw + 1 && e.getBoundingClientRect().width > 0).length;
    if (beyond) issues.push(beyond + ' elementi oltre il viewport');

    // ── Link interni con .html ──
    const badA = [...doc.querySelectorAll('a[href]')].filter((a) => { const h = a.getAttribute('href'); return h && !/^(https?:|mailto:|tel:|#|\/\/)/.test(h) && /\.html([?#]|$)/.test(h) && !/(^|\/)admin\.html/.test(h); }); // admin.html: link back-office iniettato da nav-mobile.js, ammesso
    if (badA.length) issues.push(badA.length + ' link interni con .html (' + badA.slice(0, 2).map((a) => a.getAttribute('href')).join('; ') + ')');

    // ── Data visibile + schema ──
    const text = doc.body.innerText;
    const hasDate = /(Ultimo aggiornamento|Aggiornamento|Aggiornato)[^\n]{0,40}(20\d\d)/i.test(text);
    if (!hasDate) issues.push('data aggiornamento non visibile');
    const ld = [...doc.querySelectorAll('script[type="application/ld+json"]')].map((s) => s.textContent).join(' ');
    if (!/dateModified/.test(ld)) issues.push('dateModified assente in JSON-LD');

    return { m, issues };
  }

  // opts.inject=true → simula l'effetto di css/rig-blog-article.css (+ blog-lead-form v3) PRIMA di misurare:
  // il risultato sono i problemi RESIDUI che il CSS condiviso non risolve (da sistemare a mano pagina per pagina).
  async function rigAuditBatch(slugs, width, opts) {
    opts = opts || {};
    const pages = {}; const summary = { total: slugs.length, ok: 0, ko: 0, byIssue: {} };
    for (const slug of slugs) {
      const f = document.createElement('iframe');
      f.style.cssText = 'position:fixed;left:0;top:0;width:' + width + 'px;height:900px;border:0;opacity:0;pointer-events:none;z-index:-1';
      f.src = '/' + slug + '.html';
      document.body.appendChild(f);
      await new Promise((r) => { f.onload = r; setTimeout(r, 7000); });
      const loads = [];
      if (opts.inject && f.contentDocument && f.contentDocument.head) {
        const d = f.contentDocument;
        ['css/rig-blog-article.css?v=2', 'css/blog-lead-form.css?v=3'].forEach((h) => {
          if (d.querySelector('link[href^="' + h.split('?')[0] + '"][href$="' + h.split('?')[1] + '"]')) return;
          const l = d.createElement('link'); l.rel = 'stylesheet'; l.href = h; d.head.appendChild(l);
          loads.push(new Promise((r) => { l.onload = r; l.onerror = r; setTimeout(r, 3000); }));
        });
        await Promise.all(loads);
      }
      // le transizioni CSS (`transition: all .2s`) falsano i colori se misurati subito dopo un cambio di stile:
      // le azzero e aspetto un frame prima di misurare
      try {
        const st = f.contentDocument.createElement('style');
        st.textContent = '*,*::before,*::after{transition:none!important;animation:none!important}';
        f.contentDocument.head.appendChild(st);
      } catch (e) { /* pagina non caricata: gestito sotto */ }
      await new Promise((r) => setTimeout(r, 1300));
      try {
        if (!f.contentDocument || !f.contentDocument.body) throw new Error('pagina non caricata (timeout o 404)');
        const res = auditPage(f.contentDocument, f.contentWindow);
        if (res.issues.length) { pages[slug] = { m: res.m, issues: res.issues }; summary.ko++; }
        else { summary.ok++; }
        res.issues.forEach((i) => { const k = i.replace(/[0-9.,]+/g, 'N').replace(/\(.*\)/, '').trim(); summary.byIssue[k] = (summary.byIssue[k] || 0) + 1; });
      } catch (e) { pages[slug] = { error: String(e) }; summary.ko++; }
      f.remove();
    }
    return { width, summary, pages };
  }

  window.rigAuditBatch = rigAuditBatch;
  window.rigAuditPage = auditPage;
})();
