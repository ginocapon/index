// Guardia estetica: il monogramma RI trasparente e la grana di fondo (identità di marca)
// devono restare presenti e leggibili su tutte le pagine chiave, e la rifinitura UX deve reggere.
const { test, expect } = require('@playwright/test');
const { mockBackends, dismissCookies, calm } = require('./helpers');

const PAGES = ['/', '/proprietario-immobile', '/servizio-vendita', '/landing-valutazione', '/contatti'];

for (const url of PAGES) {
  test.describe(`brand+ux ${url}`, () => {
    test('monogramma RI trasparente + grana presenti', async ({ page }) => {
      await mockBackends(page);
      await page.goto(url);
      await page.waitForSelector('.rig-brand-watermark', { state: 'attached', timeout: 8000 });
      const info = await page.evaluate(() => {
        const w = document.querySelector('.rig-brand-watermark');
        const item = document.querySelector('.rig-brand-watermark-a');
        const cs = getComputedStyle(w);
        return {
          items: w.querySelectorAll('.rig-brand-watermark-item svg').length,
          blend: cs.mixBlendMode,
          opacity: parseFloat(getComputedStyle(item).opacity),
          grain: document.body.classList.contains('rig-sugar-paper'),
        };
      });
      expect(info.items).toBe(3);
      expect(info.blend).toBe('multiply');
      expect(info.opacity).toBeGreaterThan(0.1);
      expect(info.opacity).toBeLessThan(0.25);
      expect(info.grain).toBe(true);
    });

    test('campi >= 16px (niente zoom iOS) e CTA principale visibile', async ({ page }, testInfo) => {
      test.skip(testInfo.project.name.includes('desktop'), 'controllo solo mobile');
      await mockBackends(page);
      await page.goto(url);
      await dismissCookies(page);
      await calm(page);
      const small = await page.evaluate(() => {
        return [...document.querySelectorAll('input, select, textarea')]
          .filter((el) => el.offsetParent !== null && !['checkbox', 'radio', 'hidden', 'range'].includes(el.type) && !el.hasAttribute('data-rig-hp'))
          .filter((el) => parseFloat(getComputedStyle(el).fontSize) < 16)
          .map((el) => el.id || el.name || el.tagName);
      });
      expect(small, 'campi con font < 16px').toEqual([]);
    });
  });
}

test('home mobile: CTA "Valuta il tuo immobile" nella prima schermata', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name.includes('desktop'), 'controllo solo mobile');
  await mockBackends(page);
  await page.goto('/');
  await calm(page);
  const box = await page.locator('.hero-cta-primary').boundingBox();
  const vh = page.viewportSize().height;
  expect(box.y + box.height, 'CTA sotto la piega').toBeLessThan(vh);
});

test('hub proprietari: menu mobile apribile', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name.includes('desktop'), 'controllo solo mobile');
  await mockBackends(page);
  await page.goto('/proprietario-immobile');
  await dismissCookies(page);
  await page.locator('#burgerBtn').click();
  await expect(page.locator('#navMobile.open')).toBeVisible();
});
