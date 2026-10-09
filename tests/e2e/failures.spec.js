// Modalità di guasto: un errore di Supabase/email NON deve mai essere presentato come invio riuscito
// quando nessun canale ha registrato il contatto, e un contatto solo-email deve far scattare l'avviso operatore.
const { test, expect } = require('@playwright/test');
const { mockBackends, dismissCookies } = require('./helpers');
const { FORMS } = require('./forms');

// Un modulo per famiglia di codice: shared (rig-lead-form) + 3 handler inline.
const COVERED = ['servizio-vendita', 'homepage', 'contatti', 'landing-consulenza', 'landing-valutazione'];

for (const f of FORMS.filter((x) => COVERED.includes(x.nome))) {
  test.describe(`guasti ${f.nome}`, () => {
    async function open(page, opts) {
      const calls = await mockBackends(page, opts);
      const dialogs = [];
      page.on('dialog', (d) => { dialogs.push(d.message()); d.accept(); });
      await page.goto(f.url);
      await dismissCookies(page);
      await page.waitForFunction(() => !!window.supabase, null, { timeout: 8000 });
      await f.fill(page);
      await page.locator(f.submit).first().scrollIntoViewIfNeeded();
      await page.locator(f.submit).first().click();
      return { calls, dialogs };
    }

    test('DB rifiuta (RLS) ma email ok: il contatto non è perso, successo mostrato, nessuna eccezione', async ({ page }) => {
      const { calls } = await open(page, { insertFail: true });
      await expect.poll(() => calls.insert.length).toBe(1);
      await expect(page.locator(f.ok).first()).toBeVisible();
      expect(calls.mail.length).toBeGreaterThanOrEqual(1);
      if (f.nome === 'servizio-vendita' || f.nome === 'homepage') {
        // Modulo condiviso: avviso operatore "NON salvato nel CRM"
        await expect.poll(() => calls.mail.some((m) => /ATTENZIONE/.test(m.subject || ''))).toBe(true);
      }
    });

    test('DB rifiuta E email fallisce: NIENTE conferma di successo + avviso all\'utente', async ({ page }) => {
      const { calls, dialogs } = await open(page, { insertFail: true, mailFail: true });
      await expect.poll(() => calls.insert.length).toBe(1);
      await expect.poll(() => dialogs.length, { message: 'nessun messaggio di errore mostrato' }).toBeGreaterThan(0);
      expect(dialogs.join(' ')).toMatch(/errore|049/i);
      await expect(page.locator(f.ok).first()).toBeHidden();
    });
  });
}
