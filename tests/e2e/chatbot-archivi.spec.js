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

const UFF2247 = {
  codice: 'UFF2247', titolo: 'Ufficio a Padova', slug: 'ufficio-affitto-padova-uff2247',
  tipo_operazione: 'affitto', tipologia: 'ufficio', comune: 'Padova', prezzo: 900,
  superficie: 70, locali: 3, bagni: 1, attivo: true, venduto: false, affittato: false, updated_at: '2026-10-06T00:00:00Z',
};

const LF0242 = {
  codice: 'LF0242', titolo: 'AFFITTASI APPARTAMENTO A LIMENA', slug: 'appartamento-affitto-residenziale-padova-lf0242',
  tipo_operazione: 'affitto', tipologia: 'appartamento', comune: 'Padova', prezzo: 800,
  superficie: 80, locali: 3, bagni: 1, attivo: true, venduto: false, affittato: false, updated_at: '2026-10-06T00:00:00Z',
};

async function avvia(page, cfg = {}) {
  const calls = { immobiliUrls: [] };
  await mockBackends(page);
  for (const f of ['archivio-a-100-faq.json', 'archivio-b-100-faq.json', 'archivio-c-200-faq.json', 'flusso-apertura-chat.json', 'inventario_immobili.json']) {
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

test.describe('Chatbot archivi - correttezza delle risposte', () => {
  test('1 AP-01: apertura chat chiede argomento', async ({ page }) => {
    await avvia(page, {});
    await expect(ultima(page)).toContainText('Di cosa vorresti parlare');
  });

  test('2 Archivio A: risposta originale + fonte con link', async ({ page }) => {
    await avvia(page, {});
    await chiedi(page, 'Come si leggono le quotazioni OMI?');
    await expect(ultima(page)).toContainText('Si selezionano semestre, Provincia, Comune, zona OMI');
    await expect(ultima(page)).toContainText('Fonte:');
    await expect(ultima(page).locator('a[href^="https://"]').first()).toBeVisible();
  });

  test('3 Tutte le 100 FAQ di A: risposta identica all\'originale e sempre con fonte', async ({ page }) => {
    await avvia(page, {});
    const A = JSON.parse(fs.readFileSync(path.join(DATA, 'archivio-a-100-faq.json'), 'utf8')).faq;
    const out = await page.evaluate(async (faq) => {
      const bad = [];
      for (const f of faq) {
        const r = await window.RighettoChatArchivi.tryArchiviFaq(window.rigChat.engine, f.domanda);
        if (!r || r.indexOf(f.risposta) !== 0 || r.indexOf('**Fonte:** [') < 0) bad.push(f.id);
      }
      return bad;
    }, A);
    expect(out).toEqual([]);
  });

  test('4 Mutuo prima casa: nessuna risposta fuori tema, nessun form nome', async ({ page }) => {
    await avvia(page, {});
    await chiedi(page, 'Come funziona il mutuo prima casa?');
    const t = await ultima(page).innerText();
    expect(t).toContain('TAEG');
    expect(t).toContain('perizia');
    expect(t).toContain('Fonte:');
    expect(t).not.toMatch(/Come ti chiami/);
    expect(t).not.toMatch(/dimostrare i pagamenti|senza mutuo/i);
  });

  test('5 LO0287 bagni: discordanza segnalata, niente certezza', async ({ page }) => {
    await avvia(page, { immobili: [LO0287] });
    await chiedi(page, 'Quanti bagni ha LO0287?');
    await expect(ultima(page)).toContainText('discordant');
    await expect(ultima(page)).toContainText('bagni=2, bagni_totali=1');
  });

  test('6 UFF2247 canone: nota 900 contro 800 + IVA', async ({ page }) => {
    await avvia(page, { immobili: [UFF2247] });
    await chiedi(page, 'Quanto costa UFF2247?');
    await expect(ultima(page)).toContainText('900');
    await expect(ultima(page)).toContainText('800 più IVA');
  });

  test('7 UFF2247-V: nota propria, distinta da UFF2247', async ({ page }) => {
    await avvia(page, { immobili: [{ ...UFF2247, codice: 'UFF2247-V', tipo_operazione: 'vendita', prezzo: 180000 }] });
    await chiedi(page, 'Quanto costa UFF2247-V?');
    await expect(ultima(page)).toContainText('180.000');
    await expect(ultima(page)).toContainText('Vendita 180.000 nel campo contro testo di locazione');
  });

  test('8 Affitto Limena 800: usa i requisiti, una sola domanda (superficie)', async ({ page }) => {
    await avvia(page, { immobili: [LF0242] });
    await chiedi(page, 'Cerco un appartamento in affitto a Limena fino a 800 euro.');
    const t = await ultima(page).innerText();
    expect(t).toContain('Quale superficie');
    expect(t).not.toMatch(/Come ti chiami/);
    expect(t).not.toMatch(/acquistare oppure|acquisto o locazione/);
    expect((t.match(/\?/g) || []).length).toBe(1);
  });

  test('9 Budget 250000 euro letto come 250.000', async ({ page }) => {
    await avvia(page, { immobili: [] });
    await chiedi(page, 'Cerco una casa in vendita a Padova fino a 250000 euro');
    const t = await ultima(page).innerText();
    expect(t).toContain('250.000');
    expect(t).not.toMatch(/25\.000(?!0)/);
  });

  test('10 Uffici senza telefono: AP-08 + domanda operazione', async ({ page }) => {
    await avvia(page, {});
    await chiedi(page, 'Vorrei solo sapere quali uffici avete, senza dare il telefono.');
    await expect(ultima(page)).toContainText('continuiamo qui');
    await expect(ultima(page)).toContainText('acquistare oppure');
  });

  test('11 AP-05: argomento tecnico generico chiede il dubbio', async ({ page }) => {
    await avvia(page, {});
    await chiedi(page, 'Ho una questione tecnica');
    await expect(ultima(page)).toContainText('Qual è il dubbio');
  });

  test('12 AP-07: invito novità a fine chat, una volta sola, senza promesse di alert', async ({ page }) => {
    await avvia(page, {});
    await chiedi(page, 'xqzv blorf grumpf nonsense');
    await expect(ultima(page)).toContainText('consultare il catalogo');
    const t = await ultima(page).innerText();
    expect(t).not.toMatch(/ti avviser|notifica|anteprima/i);
    await chiedi(page, 'xqzv altro nonsense blorf');
    expect(await ultima(page).innerText()).not.toContain('consultare il catalogo');
  });

  test('13 Domanda disponibilità: mai istantanee archivio B, sempre catalogo live', async ({ page }) => {
    const calls = await avvia(page, { immobili: [] });
    await chiedi(page, 'Avete immobili in vendita a Limena?');
    const t = await ultima(page).innerText();
    expect(t).not.toMatch(/snapshot|11\/10\/2026/i);
    expect(decodeURIComponent(calls.immobiliUrls.join(' '))).toMatch(/attivo=eq\.true/);
  });

  test('14 Query catalogo: attivo, non venduto, non affittato', async ({ page }) => {
    const calls = await avvia(page, { immobili: [] });
    await chiedi(page, 'cerco bilocale in affitto padova');
    await page.waitForTimeout(2500);
    const q = decodeURIComponent(calls.immobiliUrls.join(' '));
    expect(q).toMatch(/attivo=eq\.true/);
    expect(q).toMatch(/venduto=eq\.false/);
    expect(q).toMatch(/affittato=eq\.false/);
  });

  test('15 Immobile venduto: non disponibile', async ({ page }) => {
    await avvia(page, { immobili: [{ ...LO0287, venduto: true }] });
    await chiedi(page, 'LO0287 prezzo');
    await expect(ultima(page)).toContainText('non risulta più disponibile');
  });
});

 test('C: 200 risposte originali corrette, con fonti e limiti', async ({ page }) => {
  await avvia(page);
  const C = JSON.parse(fs.readFileSync(path.join(DATA, 'archivio-c-200-faq.json'), 'utf8')).faq;
  const bad = await page.evaluate(async (faq) => {
    const out = [];
    for (const f of faq) {
      const r = await window.RighettoChatArchivi.tryArchiviFaq(window.rigChat.engine, f.domanda);
      if (!r || !r.startsWith(f.risposta) || !r.includes(f.fonti[0].url) || !r.includes(f.limiti_interpretativi)) out.push({ id: f.id, domanda: f.domanda, risposta: r });
    }
    return out;
  }, C);
  expect(bad).toEqual([]);
 });
 test('C: campione di tutti i temi nel percorso completo e link visibili', async ({ page }, testInfo) => {
  await avvia(page);
  const C = JSON.parse(fs.readFileSync(path.join(DATA, 'archivio-c-200-faq.json'), 'utf8')).faq;
  const seen = new Set();
  for (const f of C.filter(f => { if(seen.has(f.categoria)) return false; seen.add(f.categoria); return true; })) {
    await page.evaluate(() => { window.rigChat.engine.state = 'idle'; window.rigChat.engine.chatSession = null; });
    await chiedi(page, f.domanda);
    await expect(ultima(page)).toContainText(f.risposta);
    await expect(ultima(page).locator('a[href="' + f.fonti[0].url + '"]').first()).toBeVisible();
  }
  await page.screenshot({path: '/downloads/chatbot-c-' + testInfo.project.name + '.png', fullPage: false});
 });
