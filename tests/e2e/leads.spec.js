// Percorso lead: ogni form deve (1) notificare via email, (2) salvare in `richieste` con provenienza,
// (3) mostrare conferma. Se il salvataggio in `richieste` manca, scoring e CRM non vedono il lead.
const { test, expect } = require('@playwright/test');
const { mockBackends, dismissCookies, TEST_LEAD } = require('./helpers');

const { FORMS } = require('./forms');

for (const f of FORMS) {
  test.describe(`form ${f.nome}`, () => {
    test('invio completo: email + salvataggio richieste + conferma', async ({ page }) => {
      const calls = await mockBackends(page);
      await page.goto(f.url);
      await dismissCookies(page);
      await page.waitForFunction(() => !!window.supabase, null, { timeout: 8000 });
      await f.fill(page);
      await page.locator(f.submit).first().scrollIntoViewIfNeeded();
      await page.locator(f.submit).first().click();

      await expect.poll(() => calls.mail.length, { message: 'notifica email non inviata' }).toBe(1);
      await expect.poll(() => calls.insert.length, { message: 'lead NON salvato in richieste' }).toBe(1);

      const row = calls.insert[0][0] || calls.insert[0];
      expect(row.telefono).toBe(TEST_LEAD.tel);
      expect(row.nome).toContain('TEST Playwright');
      if (f.provenienza) expect(row.provenienza).toBe(f.provenienza);
      expect(row.provenienza, 'provenienza obbligatoria per il tracciamento').toBeTruthy();
      await expect(page.locator(f.ok).first()).toBeVisible();
    });

    test('senza consenso privacy: nessun invio', async ({ page }) => {
      const calls = await mockBackends(page);
      const dialogs = [];
      page.on('dialog', (d) => { dialogs.push(d.message()); d.accept(); });
      await page.goto(f.url);
      await dismissCookies(page);
      await page.waitForFunction(() => !!window.supabase, null, { timeout: 8000 });
      await f.fill(page);
      await page.uncheck('input[type=checkbox][id$="gdpr"], #gdpr, #f-gdpr, #cf-gdpr, #v-gdpr');
      await page.locator(f.submit).first().click();
      await page.waitForTimeout(700);
      expect(calls.mail.length).toBe(0);
      expect(calls.insert.length).toBe(0);
      expect(dialogs.join(' ')).toMatch(/privacy|informativa/i);
    });
  });
}

test('honeypot: un bot che compila il campo nascosto non genera invii', async ({ page }) => {
  const calls = await mockBackends(page);
  await page.goto('/servizio-vendita');
  await dismissCookies(page);
  await FORMS[0].fill(page);
  await page.evaluate(() => { document.querySelector('[data-rig-hp="1"]').value = 'http://spam.invalid'; });
  await page.locator(FORMS[0].submit).first().click();
  await page.waitForTimeout(700);
  expect(calls.mail.length).toBe(0);
  expect(calls.insert.length).toBe(0);
});
