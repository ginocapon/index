// Regressione visiva + controlli di layout sulle pagine a maggior valore commerciale.
// Backend simulati (nessuna richiesta reale). Elementi dinamici mascherati.
const { test, expect } = require('@playwright/test');
const { mockBackends, dismissCookies, calm } = require('../e2e/helpers');

const PAGES = [
  ['home', '/'],
  ['hub-proprietari', '/proprietario-immobile'],
  ['landing-valutazione', '/landing-valutazione'],
  ['servizio-vendita', '/servizio-vendita'],
  ['servizio-valutazioni', '/servizio-valutazioni'],
  ['contatti', '/contatti'],
];

async function prepare(page, url) {
  await mockBackends(page);
  await page.goto(url, { waitUntil: 'load' });
  await dismissCookies(page);
  await calm(page);
  await page.evaluate(() => document.fonts && document.fonts.ready);
  // porta a termine reveal/lazy: scorre la pagina e torna in cima
  await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 40)); } window.scrollTo(0, 0); });
  await page.waitForLoadState('networkidle').catch(() => {});
  // La home carica sezioni dinamiche (annunci, recensioni): attendi che l'altezza della pagina si stabilizzi.
  let last = -1;
  for (let i = 0; i < 12; i++) {
    const h = await page.evaluate(() => document.documentElement.scrollHeight);
    if (h === last) break;
    last = h;
    await page.waitForTimeout(400);
  }
}

for (const [name, url] of PAGES) {
  test.describe(name, () => {
    test('nessuno scorrimento orizzontale involontario', async ({ page }) => {
      await prepare(page, url);
      const over = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      expect(over, 'px oltre il viewport').toBeLessThanOrEqual(1);
    });

    test('monogramma RI trasparente e grana presenti', async ({ page }) => {
      await prepare(page, url);
      await expect(page.locator('.rig-brand-watermark')).toHaveCount(1);
      const ok = await page.evaluate(() => getComputedStyle(document.querySelector('.rig-brand-watermark')).mixBlendMode === 'multiply' && document.body.classList.contains('rig-sugar-paper'));
      expect(ok).toBe(true);
    });

    test('screenshot di riferimento (prima schermata)', async ({ page }) => {
      await prepare(page, url);
      await expect(page).toHaveScreenshot(`${name}-fold.png`, {
        mask: [page.locator('.cu'), page.locator('video'), page.locator('.rig-carousel-track')],
      });
    });

    test('screenshot di riferimento (pagina intera)', async ({ page }) => {
      await prepare(page, url);
      await expect(page).toHaveScreenshot(`${name}-full.png`, {
        fullPage: true,
        mask: [page.locator('.cu'), page.locator('video'), page.locator('.rig-carousel-track')],
      });
    });
  });
}
