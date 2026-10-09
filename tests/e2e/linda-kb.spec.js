// Test "Righetto Virtual Colleague": Linda + base di conoscenza approvata.
// Nessuna rete reale: Supabase è simulato. Ogni test dichiara la risposta ATTESA.
const { test, expect } = require('@playwright/test');
const { mockBackends, dismissCookies } = require('./helpers');

const CORS = { 'access-control-allow-origin': '*', 'access-control-allow-headers': '*', 'access-control-allow-methods': '*' };
const J = { ...CORS, 'content-type': 'application/json' };

const VOCE = {
  id: '11111111-1111-1111-1111-111111111111',
  domanda: 'Quali documenti servono per vendere casa?',
  risposta: 'Servono atto di provenienza, visura catastale, planimetria e attestato di prestazione energetica.',
  fonti: [{ titolo: 'Agenzia delle Entrate', url: 'https://www.agenziaentrate.gov.it/' }, { titolo: 'Scheda interna', url: 'javascript:alert(1)' }],
  condizioni: 'Elenco indicativo: la lista completa si definisce in sede.',
  categoria: 'documenti', aggiornata_il: '2026-10-01', score: 0.92,
};

const IMM = {
  codice: 'CAP1628', titolo: 'Capannone a Villafranca', slug: 'capannone-villafranca', tipo_operazione: 'affitto_commerciale', tipologia: 'capannone',
  comune: 'VILLAFRANCA PADOVANA', prezzo: 1100, superficie: 180, locali: 3, bagni: 1, piano: 'Piano Terra', anno_costruzione: 1970, stato: 'buono',
  classe_energetica: 'G', ipe_kwh: 223, garage: false, giardino: false, terrazzo: false, cantina: false, ascensore: false, arredato: false,
  spese_condominio: null, attivo: true, venduto: false, affittato: false, updated_at: '2026-10-06T00:15:00Z',
};

// Prepara pagina + simulazione backend. cfg: { rpcSearch, immobili, rpcStatus }
async function avvia(page, cfg = {}) {
  const calls = { search: 0, logs: [], feedback: [], immobiliUrls: [] };
  await mockBackends(page);
  await page.route('**/rest/v1/**', (route) => {
    const req = route.request();
    const u = new URL(req.url());
    if (req.method() === 'OPTIONS') return route.fulfill({ status: 204, headers: CORS });
    const body = () => { try { return req.postDataJSON(); } catch (_) { return null; } };
    if (u.pathname.endsWith('/rpc/linda_kb_search')) {
      calls.search++;
      if (cfg.rpcMissing) return route.fulfill({ status: 404, headers: J, body: '{"code":"PGRST202","message":"Could not find the function public.linda_kb_search"}' });
      if (cfg.rpcSlow) return; // non risponde mai: deve scattare il timeout
      return route.fulfill({ status: 200, headers: J, body: JSON.stringify(cfg.rpcSearch || []) });
    }
    if (u.pathname.endsWith('/rpc/linda_log_question')) { calls.logs.push(body()); return route.fulfill({ status: 200, headers: J, body: '42' }); }
    if (u.pathname.endsWith('/rpc/linda_feedback')) { calls.feedback.push(body()); return route.fulfill({ status: 200, headers: J, body: 'null' }); }
    if (u.pathname.endsWith('/immobili')) {
      calls.immobiliUrls.push(u.search);
      return route.fulfill({ status: 200, headers: J, body: JSON.stringify(cfg.immobili || []) });
    }
    return route.fulfill({ status: 200, headers: J, body: '[]' });
  });
  await page.goto('/');
  await dismissCookies(page);
  await page.mouse.move(20, 20); // attiva il caricamento lazy di chatbot.js
  await page.waitForFunction(() => window.rigChat && window.rigChat.engine && window.rigChat.engine.__lindaKb === true, null, { timeout: 15000 });
  await page.evaluate(() => { if (!window.rigChat.open) window.rigChat.toggle(); window.rigChat.startChat(); });
  await expect(page.locator('#rig-chat-box')).toBeVisible();
  return calls;
}
const chiedi = (page, testo) => page.evaluate((t) => window.rigChat.send(t), testo);
const ultima = (page) => page.locator('#rig-chat-msgs .chat-msg.bot .chat-bubble').last();

test.describe('Linda KB — risposte da conoscenza approvata', () => {
  test('KB: risponde con testo approvato, fonti sicure, data e feedback', async ({ page }) => {
    const calls = await avvia(page, { rpcSearch: [VOCE] });
    await chiedi(page, 'quali documenti servono per vendere casa');
    const b = ultima(page);
    await expect(b).toContainText('Servono atto di provenienza');          // risposta approvata
    await expect(b).toContainText('Elenco indicativo');                    // condizioni
    await expect(b).toContainText('Informazione aggiornata al');           // data
    await expect(b.locator('a[href^="https://www.agenziaentrate.gov.it"]')).toHaveCount(1);
    expect(await b.locator('a[href^="javascript"]').count()).toBe(0);      // URL non https scartato
    await expect(b.locator('.linda-fb button')).toHaveCount(2);
    expect(calls.logs.at(-1)).toMatchObject({ p_trovata: true, p_kb: VOCE.id });
  });

  test('KB: feedback 👍 viene registrato', async ({ page }) => {
    const calls = await avvia(page, { rpcSearch: [VOCE] });
    await chiedi(page, 'documenti per vendere casa');
    await ultima(page).locator('.linda-fb button[data-v="1"]').click();
    await expect.poll(() => calls.feedback.length).toBe(1);
    expect(calls.feedback[0]).toMatchObject({ p_id: 42, p_utile: true });
  });

  test('KB: HTML nel testo approvato viene neutralizzato (no XSS)', async ({ page }) => {
    await avvia(page, { rpcSearch: [{ ...VOCE, risposta: 'Ok <img src=x onerror="window.__xss=1"> <script>window.__xss=1</script> fine', fonti: [] }] });
    await chiedi(page, 'documenti vendita');
    await expect(ultima(page)).toContainText('<img');                      // mostrato come testo
    expect(await ultima(page).locator('img').count()).toBe(0);
    expect(await page.evaluate(() => window.__xss)).toBeUndefined();
  });

  test('KB: punteggio sotto soglia → NON risponde dalla KB (niente invenzioni)', async ({ page }) => {
    await avvia(page, { rpcSearch: [{ ...VOCE, score: 0.2 }] });
    await chiedi(page, 'xqzv blorf grumpf');
    await expect(ultima(page)).not.toContainText('Servono atto di provenienza');
    await expect(ultima(page)).toContainText('far verificare questo punto da un nostro consulente'); // frase decisa dal titolare
    await expect(ultima(page)).toContainText('049.8843484');
  });

  test('Privacy: email e telefono vengono rimossi PRIMA del log', async ({ page }) => {
    const calls = await avvia(page, { rpcSearch: [] });
    await chiedi(page, 'xqzv blorf 333 1234567 mario.rossi@example.it');
    await expect.poll(() => calls.logs.length).toBeGreaterThan(0);
    const dom = calls.logs.at(-1).p_domanda;
    expect(dom).toContain('[telefono]');
    expect(dom).toContain('[email]');
    expect(dom).not.toMatch(/1234567|mario\.rossi/);
    expect(calls.logs.at(-1).p_trovata).toBe(false);                        // finisce nel rapporto lacune
  });

  test('Resilienza: RPC non installata → Linda continua con le regole storiche e smette di chiamarla', async ({ page }) => {
    const calls = await avvia(page, { rpcMissing: true });
    await chiedi(page, 'orari di apertura');
    await expect(ultima(page)).toContainText('Orari Righetto Immobiliare');
    await chiedi(page, 'dove siete');
    await expect(ultima(page)).toContainText('Limena');
    expect(calls.search).toBe(1);
  });

  test('Resilienza: KB non risponde (timeout) → risposta storica entro pochi secondi', async ({ page }) => {
    await avvia(page, { rpcSlow: true });
    const t0 = Date.now();
    await chiedi(page, 'orari di apertura');
    await expect(ultima(page)).toContainText('Orari Righetto Immobiliare');
    expect(Date.now() - t0).toBeLessThan(9000);
  });
});

test.describe('Linda — dati live di un annuncio', () => {
  test('Prezzo canone da scheda; spese non indicate → ammette di non saperle', async ({ page }) => {
    const calls = await avvia(page, { immobili: [IMM] });
    await chiedi(page, 'CAP1628 quanto costa e quali sono le spese condominiali?');
    await expect(ultima(page)).toContainText('€ 1.100 al mese');
    await expect(ultima(page)).toContainText('non riporta un\'informazione verificata');
    await expect(ultima(page)).toContainText('049.8843484');
    // privacy: la query NON deve chiedere dati dei proprietari né colonne interne
    // (la home carica altre liste con select=*: qui si controlla solo la query di Linda, filtrata per codice)
    const q = decodeURIComponent(calls.immobiliUrls.filter((s) => /codice=ilike/.test(s)).join(' '));
    expect(q).toContain('codice=ilike.CAP1628');
    expect(q).not.toMatch(/proprietario|note_interne|prezzo_reale|select=\*/);
  });

  test('Immobile venduto → "non più disponibile", nessun prezzo', async ({ page }) => {
    await avvia(page, { immobili: [{ ...IMM, venduto: true }] });
    await chiedi(page, 'immobile CAP1628 prezzo');
    await expect(ultima(page)).toContainText('non risulta più disponibile');
    await expect(ultima(page)).not.toContainText('1.100');
  });

  test('Codice inesistente → dichiara di non trovarlo', async ({ page }) => {
    await avvia(page, { immobili: [] });
    await chiedi(page, 'annuncio codice ZZ9999 prezzo');
    await expect(ultima(page)).toContainText('Non trovo un annuncio con codice');
  });

  test('"IMU2025" non viene scambiato per un codice annuncio', async ({ page }) => {
    await avvia(page, { immobili: [] });
    await chiedi(page, 'novità IMU2025');
    await expect(ultima(page)).not.toContainText('Non trovo un annuncio');
  });
});

test.describe('Linda — layout mobile/desktop', () => {
  test('Nessun overflow orizzontale e pulsanti feedback ≥ 44px', async ({ page }) => {
    await avvia(page, { rpcSearch: [VOCE] });
    await chiedi(page, 'documenti per vendere casa');
    const ov = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    expect(ov).toBeLessThanOrEqual(1);
    const box = await ultima(page).locator('.linda-fb button').first().boundingBox();
    expect(box.width).toBeGreaterThanOrEqual(43.5);
    expect(box.height).toBeGreaterThanOrEqual(43.5);
  });
});
