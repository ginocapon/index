// Pannello admin-kb: accesso con Supabase Auth, elenco, import CSV, anteprima. Backend simulato.
const { test, expect } = require('@playwright/test');
const { mockBackends } = require('./helpers');

const CORS = { 'access-control-allow-origin': '*', 'access-control-allow-headers': '*', 'access-control-allow-methods': '*' };
const J = { ...CORS, 'content-type': 'application/json' };

async function avvia(page, { admin = true, loginOk = true, voci = [] } = {}) {
  const calls = { insert: [], update: [] };
  await mockBackends(page);
  await page.route('**/auth/v1/**', (route) => {
    const req = route.request();
    if (req.method() === 'OPTIONS') return route.fulfill({ status: 204, headers: CORS });
    if (!loginOk) return route.fulfill({ status: 400, headers: J, body: '{"error":"invalid_grant","error_description":"Invalid login credentials"}' });
    const user = { id: '22222222-2222-2222-2222-222222222222', aud: 'authenticated', role: 'authenticated', email: 'admin@example.invalid', app_metadata: {}, user_metadata: {}, created_at: '2026-01-01T00:00:00Z' };
    return route.fulfill({ status: 200, headers: J, body: JSON.stringify({ access_token: 'x.y.z', token_type: 'bearer', expires_in: 3600, expires_at: Math.floor(Date.now() / 1000) + 3600, refresh_token: 'r', user }) });
  });
  await page.route('**/rest/v1/**', (route) => {
    const req = route.request(); const u = new URL(req.url());
    if (req.method() === 'OPTIONS') return route.fulfill({ status: 204, headers: CORS });
    if (u.pathname.endsWith('/rpc/kb_is_admin')) return route.fulfill({ status: 200, headers: J, body: JSON.stringify(admin) });
    if (u.pathname.endsWith('/kb_entries') && req.method() === 'GET') return route.fulfill({ status: 200, headers: J, body: JSON.stringify(voci) });
    if (u.pathname.endsWith('/kb_entries') && req.method() === 'POST') { calls.insert.push(req.postDataJSON()); return route.fulfill({ status: 201, headers: J, body: '[]' }); }
    return route.fulfill({ status: 200, headers: J, body: '[]' });
  });
  await page.goto('/admin-kb');
  return calls;
}
const accedi = async (page) => { await page.fill('#em', 'admin@example.invalid'); await page.fill('#pw', 'x'); await page.click('#loginForm button[type=submit]'); };

test.describe('admin-kb', () => {
  test('pagina non indicizzabile e mostra il login', async ({ page }) => {
    await avvia(page);
    await expect(page.locator('meta[name=robots]')).toHaveAttribute('content', /noindex/);
    await expect(page.locator('#login')).toBeVisible();
    await expect(page.locator('#app')).toBeHidden();
  });

  test('credenziali errate → errore, nessun accesso', async ({ page }) => {
    await avvia(page, { loginOk: false });
    await accedi(page);
    await expect(page.locator('#loginErr')).toContainText('non valide');
    await expect(page.locator('#app')).toBeHidden();
  });

  test('utente valido ma NON admin → accesso negato', async ({ page }) => {
    await avvia(page, { admin: false });
    await accedi(page);
    await expect(page.locator('#loginErr')).toContainText('non abilitato');
    await expect(page.locator('#app')).toBeHidden();
  });

  test('admin: elenco voci, HTML della domanda neutralizzato', async ({ page }) => {
    await avvia(page, { voci: [{ id: 'a', categoria: 'azienda', domanda: 'Orari <img src=x onerror="window.__x=1">?', stato: 'approvata', scade_il: null, updated_at: '2026-10-01T00:00:00Z', versione: 1 }] });
    await accedi(page);
    await expect(page.locator('#app')).toBeVisible();
    await expect(page.locator('#vociBody tr')).toHaveCount(1);
    await expect(page.locator('#vociBody')).toContainText('<img');
    expect(await page.locator('#vociBody img').count()).toBe(0);
    expect(await page.evaluate(() => window.__x)).toBeUndefined();
  });

  test('import CSV: valide in "da_verificare", duplicati e righe non valide scartate', async ({ page }) => {
    const calls = await avvia(page, { voci: [{ id: 'a', categoria: 'azienda', domanda: 'Dove si trova la sede?', stato: 'approvata', scade_il: null, updated_at: '2026-10-01T00:00:00Z', versione: 1 }] });
    await accedi(page);
    await expect(page.locator('#app')).toBeVisible();
    await page.click('.tabs button[data-t=csv]');
    const csv = [
      'domanda;varianti;risposta;categoria;fonte_titolo;fonte_url;scade_il',
      'Quanto dura un contratto 4+4?;contratto 4+4|durata affitto;Il contratto a canone libero dura 4 anni più 4 di rinnovo.;affitto;Codice civile;https://www.normattiva.it/;',
      'Dove si trova la sede?;;Siamo a Limena in via Roma 96 vicino al centro.;azienda;;;',
      'Fonte non sicura?;;Risposta lunga a sufficienza per passare.;azienda;X;http://non-https.example;',
      'Corta?;;breve;azienda;;;',
    ].join('\n');
    await page.setInputFiles('#csvFile', { name: 'k.csv', mimeType: 'text/csv', buffer: Buffer.from(csv, 'utf8') });
    await expect(page.locator('#csvMsg')).toContainText('1 da importare · 1 duplicate saltate · 2 non valide');
    await page.click('#csvGo');
    await expect.poll(() => calls.insert.length).toBe(1);
    expect(calls.insert[0]).toHaveLength(1);
    expect(calls.insert[0][0]).toMatchObject({ stato: 'da_verificare', origine: 'csv', categoria: 'affitto' });
    expect(calls.insert[0][0].varianti).toEqual(['contratto 4+4', 'durata affitto']);
  });

  test('import del file reale data/linda-kb-seed-300.csv: 300 voci valide, tutte "da_verificare"', async ({ page }) => {
    const calls = await avvia(page);
    await accedi(page);
    await expect(page.locator('#app')).toBeVisible();
    await page.click('.tabs button[data-t=csv]');
    await page.setInputFiles('#csvFile', require('path').resolve(__dirname, '..', '..', 'data', 'linda-kb-seed-300.csv'));
    await expect(page.locator('#csvMsg')).toContainText('300 da importare · 0 duplicate saltate · 0 non valide');
    await page.click('#csvGo');
    await expect.poll(() => calls.insert.length).toBe(1);
    expect(calls.insert[0]).toHaveLength(300);
    expect(calls.insert[0].every((r) => r.stato === 'da_verificare' && r.origine === 'csv')).toBe(true);
    // nessuna istruzione interna deve finire nel testo pubblico
    expect(calls.insert[0].some((r) => /Controllare mensilmente|far revisionare le risposte/.test(r.risposta))).toBe(false);
    // ogni voce con numeri/percentuali ha una fonte
    const conNumeri = calls.insert[0].filter((r) => /\d+\s*(%|giorni|mesi|anni)/.test(r.risposta + r.domanda));
    expect(conNumeri.length).toBeGreaterThan(0);
    expect(conNumeri.every((r) => r.fonti.length > 0)).toBe(true);
  });

  test('regola: risposta con percentuale di mediazione viene bloccata', async ({ page }) => {
    const calls = await avvia(page);
    await accedi(page);
    await page.click('#nuova');
    await page.fill('#vDom', 'Quanto costa la mediazione?');
    await page.fill('#vRis', 'La provvigione di mediazione è il 3% del prezzo di vendita.');
    await page.click('#bBozza');
    await expect(page.locator('#vErr')).toContainText('percentuali o tariffe');
    expect(calls.insert).toHaveLength(0);
  });

  test('regola: dati numerici senza fonte non si possono approvare', async ({ page }) => {
    const calls = await avvia(page);
    await accedi(page);
    await page.click('#nuova');
    await page.fill('#vDom', 'Quanto dura la registrazione?');
    await page.fill('#vRis', 'La registrazione va fatta entro 30 giorni dalla firma del contratto.');
    await page.click('#bApprova');
    await expect(page.locator('#vErr')).toContainText('fonte verificabile');
    expect(calls.insert).toHaveLength(0);
  });
});
