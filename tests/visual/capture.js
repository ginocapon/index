// Cattura screenshot + metriche visive per i 5 viewport richiesti. SOLA LETTURA: non invia moduli.
// Uso: node tests/visual/capture.js <baseUrl> <outDir>      es. https://righettoimmobiliare.it test-results/visual/before
const { chromium } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

const BASE = (process.argv[2] || 'https://righettoimmobiliare.it').replace(/\/$/, '');
const OUT = process.argv[3] || 'test-results/visual/before';

const VIEWPORTS = [
  { id: 'desktop-1440', w: 1440, h: 900, mobile: false },
  { id: 'laptop-1366', w: 1366, h: 768, mobile: false },
  { id: 'tablet-768', w: 768, h: 1024, mobile: true },
  { id: 'phone-390', w: 390, h: 844, mobile: true },
  { id: 'phone-360', w: 360, h: 800, mobile: true },
];
const PAGES = [
  ['home', '/'],
  ['hub-proprietari', '/proprietario-immobile'],
  ['landing-valutazione', '/landing-valutazione'],
  ['servizio-vendita', '/servizio-vendita'],
  ['servizio-valutazioni', '/servizio-valutazioni'],
  ['contatti', '/contatti'],
  ['blog', '/blog'],
  ['blog-articolo', '/blog-casa-non-si-vende-padova-strategia-2026'],
  ['immobili', '/immobili'],
  ['scheda-immobile', null], // risolta dinamicamente dal primo annuncio
];

async function metrics(page) {
  return page.evaluate(() => {
    const vw = document.documentElement.clientWidth;
    const vis = (el) => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el); return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none'; };
    const overflowX = document.documentElement.scrollWidth - vw;
    const wide = [...document.querySelectorAll('body *')].filter((el) => vis(el) && el.getBoundingClientRect().right > vw + 2 && getComputedStyle(el).position !== 'fixed' && !el.closest('[aria-hidden="true"], .rig-brand-watermark, svg'))
      .slice(0, 5).map((el) => (el.tagName + '.' + (el.className && el.className.baseVal === undefined ? String(el.className).split(' ')[0] : '')).slice(0, 60));
    const taps = [...document.querySelectorAll('a, button, input:not([type=hidden]), select, textarea')].filter((el) => { if (!vis(el)) return false; const r = el.getBoundingClientRect(); return r.height < 40 || r.width < 40; });
    const tapsReal = taps.filter((el) => !(el.tagName === 'A' && el.closest('p, li, td, .breadcrumb, nav, footer') && el.getBoundingClientRect().height >= 20)); // link in testo esclusi
    const smallInputs = [...document.querySelectorAll('input:not([type=checkbox]):not([type=radio]):not([type=hidden]), select, textarea')].filter((el) => vis(el) && parseFloat(getComputedStyle(el).fontSize) < 16).length;
    const tinyText = [...document.querySelectorAll('p, li, span, a, label, td')].filter((el) => vis(el) && el.childNodes.length && [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 3) && parseFloat(getComputedStyle(el).fontSize) < 12).length;
    const distorted = [...document.querySelectorAll('img')].filter((im) => { if (!vis(im) || !im.naturalWidth) return false; const cs = getComputedStyle(im); if (cs.objectFit === 'cover' || cs.objectFit === 'contain') return false; const r = im.getBoundingClientRect(); const a = r.width / r.height, n = im.naturalWidth / im.naturalHeight; return Math.abs(a - n) / n > 0.08; }).map((im) => (im.getAttribute('src') || '').slice(-40)).slice(0, 4);
    const h1 = document.querySelectorAll('h1').length;
    const cookie = document.getElementById('rig-cookie-banner');
    const cookieH = cookie && vis(cookie) ? Math.round(cookie.getBoundingClientRect().height) : 0;
    const cta = [...document.querySelectorAll('a, button')].find((el) => vis(el) && /valut|richiedi|prenota|sopralluogo|chiama/i.test(el.textContent));
    const ctaBottom = cta ? Math.round(cta.getBoundingClientRect().bottom) : null;
    const wm = document.querySelector('.rig-brand-watermark');
    return { overflowX, wide, tapTargetsSmall: tapsReal.length, smallInputs, tinyText, distorted, h1, cookieH, ctaBottom, viewportH: innerHeight, watermark: !!wm, domNodes: document.getElementsByTagName('*').length };
  });
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  const results = [];
  for (const vp of VIEWPORTS) {
    const ctx = await browser.newContext({ viewport: { width: vp.w, height: vp.h }, isMobile: vp.mobile && vp.w < 800, hasTouch: vp.mobile, deviceScaleFactor: 1 });
    // Modulo/analytics in sola lettura: blocca scritture verso Supabase, GA e simili.
    await ctx.route('**/*', (route) => {
      const r = route.request(); const u = new URL(r.url());
      if (r.method() !== 'GET' && r.method() !== 'HEAD') return route.abort();
      if (/google-analytics|googletagmanager/.test(u.hostname)) return route.abort();
      return route.continue();
    });
    for (const [name, url] of PAGES) {
      const page = await ctx.newPage();
      const errors = [];
      page.on('pageerror', (e) => errors.push(e.message.slice(0, 120)));
      page.on('requestfailed', (r) => { if (!/google|gtag/.test(r.url())) errors.push('net: ' + r.url().slice(0, 90)); });
      try {
        let target = url;
        if (!target) {
          await page.goto(BASE + '/immobili', { waitUntil: 'networkidle', timeout: 45000 });
          target = await page.evaluate(() => { const a = [...document.querySelectorAll('a[href*="immobile?"]')][0]; return a ? a.getAttribute('href') : null; });
          if (!target) { results.push({ vp: vp.id, page: name, skipped: 'nessuna scheda trovata' }); await page.close(); continue; }
          if (!target.startsWith('/')) target = '/' + target;
        }
        await page.goto(BASE + target, { waitUntil: 'networkidle', timeout: 45000 });
        // 1) stato iniziale con cookie banner (come lo vede un nuovo visitatore) -> viewport
        await page.waitForTimeout(1200);
        const m = await metrics(page);
        await page.screenshot({ path: path.join(OUT, `${name}__${vp.id}__fold.png`) });
        // 2) banner chiuso + pagina intera
        const cb = page.getByRole('button', { name: /ho capito|accetta/i }).first();
        if (await cb.isVisible().catch(() => false)) await cb.click({ timeout: 2000 }).catch(() => {});
        await page.addStyleTag({ content: '*,*::before,*::after{animation:none!important;transition:none!important}' }).catch(() => {});
        await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 60)); } window.scrollTo(0, 0); });
        await page.waitForTimeout(400);
        await page.screenshot({ path: path.join(OUT, `${name}__${vp.id}__full.png`), fullPage: true });
        results.push({ vp: vp.id, page: name, url: target, ...m, errors });
      } catch (e) {
        results.push({ vp: vp.id, page: name, error: String(e.message).slice(0, 160) });
      }
      await page.close();
    }
    await ctx.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(OUT, 'metrics.json'), JSON.stringify(results, null, 1));
  console.log('Fatto:', results.length, 'combinazioni ->', OUT);
})();
