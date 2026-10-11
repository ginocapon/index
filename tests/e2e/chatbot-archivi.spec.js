// Archivi FAQ A/B, flusso apertura, inventario incongruenze — mock Supabase + JSON locali
const { test, expect } = require('@playwright/test');
const path = require('path');
const fs = require('fs');
const { mockBackends, dismissCookies } = require('./helpers');

const CORS = { 'access-control-allow-origin': '*', 'access-control-allow-headers': '*', 'access-control-allow-methods': '*' };
const J = { ...CORS, 'content-type': 'application/json' };

const DATA = path.resolve(__dirname, '../../data/chatbot');

const LO0287 = {
  codice: 'LO0287', titolo: 'Bifamiliare grezzo', slug: 'bifamiliare-vendita-villafranca-padovana-lo0287',
  tipo_operazione: 'vendita', tipologia: 'bifamiliare', comune: 'VILLAFRANCA PADOVANA', prezzo: 250000,
  superficie: 195, locali: 6, bagni: 1, attivo: true, venduto: false, affittato: false, updated_at: '2026-10-06T00:00:00Z',
};

const LF0242 = {
  codice: 'LF0242', titolo: 'AFFITTASI APPARTAMENTO A LIMENA', slug: 'appartamento-affitto-residenziale-padova-lf0242',
  tipo_operazione: 'affitto', tipologia: 'appartamento', comune: 'Padova', prezzo: 800,
  superficie: 80, locali: 3, bagni: 1, attivo: true, venduto: false, affittato: false, updated_at: '2026-10-06T00:00:00Z',
};

async function avvia(page, cfg = {}) {
  const calls = { immobiliUrls: [] };
  await mockBackends(page);
  for (const f of ['archivio-a-100-faq.json', 'archivio-b-100-faq.json', 'flusso-apertura-chat.json', 'inventario_immobili.json']) {
    const body = fs.readFileSync(path.join(DATA, f), 'utf8');
    await page.route('**/' + f, (route) => route.fulfill({ status: 200, headers: J, body }));
  }
  await page.route('**/rest/v1/**', (route) => {
    const req = route.request();
    const u = new URL(req.url());
    if (req.method() === 'OPTIONS') return route.fulfill({ status: 204, headers: CORS });
    if (u.pathname.endsWith('/rpc/linda_kb_search')) {
      return route.fulfill({ status: 200, headers: J, body: '[]' });
    }
    if (u.pathname.endsWith('/immobili')) {
      calls.immobiliUrls.push(u.search);
      const imm = cfg.immobili != null ? cfg.immobili : [];
      return route.fulfill({ status: 200, headers: J, body: JSON.stringify(imm) });
    }
    return route.fulfill({ status: 200, headers: J, body: '[]' });
  });
  await page.goto('/');
  await dismissCookies(page);
  await page.mouse.move(20, 20);
  await page.waitForFunction(() =>
    window.rigChat && window.rigChat.engine && window.rigChat.engine.__lindaKb === true &&
    window.rigChat.engine.__archiviOuter === true, null, { timeout: 20000 });
  await page.evaluate(() => { if (!window.rigChat.open) window.rigChat.toggle(); window.rigChat.startChat(); });
  await expect(page.locator('#rig-chat-box')).toBeVisible();
  return calls;
}

const chiedi = (page, testo) => page.evaluate((t) => window.rigChat.send(t), testo);
const ultima = (page) => page.locator('#rig-chat-msgs .chat-msg.bot .chat-bubble').last();

test.describe('Chatbot archivi — 10 domande reali', () => {
  test('1 AP-01: apertura chat chiede argomento', async ({ page }) => {
    await avvia(page, {});
    await expect(ultima(page)).toContainText('Di cosa vorresti parlare');
  });

  test('2 Archivio A: documenti vendita + fonte', async ({ page }) => {
    await avvia(page, {});
    await chiedi(page, 'Quali documenti servono per vendere casa?');
    await expect(ultima(page)).toContainText('provenienza');
    await expect(ultima(page)).toContainText('Fonte:');
    await expect(ultima(page)).toContainText('Notariato');
  });

  test('3 LO0287 bagni: incongruenza, niente certezza assoluta', async ({ page }) => {
    await avvia(page, { immobili: [LO0287] });
    await chiedi(page, 'Quanti bagni ha LO0287?');
    await expect(ultima(page)).toContainText('discordant');
    await expect(ultima(page)).toContainText('Nota di verifica');
  });

  test('4 Affitto Limena 800€: promemoria + una domanda superficie', async ({ page }) => {
    await avvia(page, { immobili: [LF0242] });
    await chiedi(page, 'Cerco un appartamento in affitto a Limena fino a 800 euro.');
    await expect(ultima(page)).toContainText('modulo');
    await expect(ultima(page)).toContainText('superficie');
    await expect(ultima(page)).not.toContainText('Come ti chiami');
  });

  test('5 Uffici senza telefono: AP-08 + domanda operazione', async ({ page }) => {
    await avvia(page, {});
    await chiedi(page, 'Vorrei solo sapere quali uffici avete, senza dare il telefono.');
    await expect(ultima(page)).toContainText('continuiamo qui');
    await expect(ultima(page)).toContainText('acquistare oppure');
  });

  test('6 LF0242 prezzo live da scheda', async ({ page }) => {
    await avvia(page, { immobili: [LF0242] });
    await chiedi(page, 'Quanto costa LF0242?');
    await expect(ultima(page)).toContainText('800');
    await expect(ultima(page)).toContainText('Limena');
  });

  test('7 Mutuo / Archivio A: non avvia form contatto', async ({ page }) => {
    await avvia(page, {});
    await chiedi(page, 'Come funziona il mutuo prima casa?');
    const t = await ultima(page).innerText();
    expect(t).not.toMatch(/Come ti chiami/);
  });

  test('8 Fallback + invito catalogo (AP-07)', async ({ page }) => {
    await avvia(page, {});
    await chiedi(page, 'xqzv blorf grumpf nonsense 12345');
    await expect(ultima(page)).toContainText('consultare il catalogo');
    await expect(ultima(page)).toContainText('Catalogo immobili');
  });

  test('9 Query catalogo include affittato=false', async ({ page }) => {
    const calls = await avvia(page, { immobili: [] });
    await chiedi(page, 'cerco bilocale in affitto padova');
    await page.waitForTimeout(2500);
    const q = decodeURIComponent(calls.immobiliUrls.join(' '));
    expect(q).toMatch(/affittato=eq\.false/);
  });

  test('10 Immobile venduto: non disponibile', async ({ page }) => {
    await avvia(page, { immobili: [{ ...LO0287, venduto: true }] });
    await chiedi(page, 'LO0287 prezzo');
    await expect(ultima(page)).toContainText('non risulta più disponibile');
  });
});
