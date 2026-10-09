// Helper test: blocca ogni richiesta verso l'esterno e registra cosa il sito avrebbe inviato.
const CORS = {
  'access-control-allow-origin': '*',
  'access-control-allow-headers': '*',
  'access-control-allow-methods': '*',
};

// Dati di test: dominio .invalid, mai raggiungibile. Nessun dato personale reale.
const TEST_LEAD = { nome: 'TEST Playwright', cognome: 'Automatico', tel: '3330000000', email: 'test-playwright@example.invalid' };

// opts.insertFail: simula il rifiuto (RLS/HTTP) su `richieste`; opts.mailFail: errore dell'Edge Function send-email.
async function mockBackends(page, opts = {}) {
  const calls = { insert: [], mail: [], upsert: [], external: [] };
  await page.route('**/*', (route) => {
    const req = route.request();
    const u = new URL(req.url());
    if (u.hostname === 'localhost' || u.hostname === '127.0.0.1') return route.continue();

    if (u.hostname.endsWith('.supabase.co')) {
      if (req.method() === 'OPTIONS') return route.fulfill({ status: 204, headers: CORS });
      const json = () => { try { return req.postDataJSON(); } catch (_) { return null; } };
      if (u.pathname.startsWith('/functions/v1/send-email')) {
        calls.mail.push(json());
        if (opts.mailFail) return route.fulfill({ status: 500, headers: { ...CORS, 'content-type': 'application/json' }, body: '{"ok":false}' });
        return route.fulfill({ status: 200, headers: { ...CORS, 'content-type': 'application/json' }, body: '{"ok":true}' });
      }
      if (u.pathname.startsWith('/rest/v1/richieste') && req.method() === 'POST') {
        calls.insert.push(json());
        if (opts.insertFail) return route.fulfill({ status: 401, headers: { ...CORS, 'content-type': 'application/json' }, body: '{"code":"42501","message":"new row violates row-level security policy"}' });
        return route.fulfill({ status: 201, headers: CORS, body: '' });
      }
      if (u.pathname.startsWith('/rest/v1/newsletter_subscribers')) {
        calls.upsert.push(json());
        return route.fulfill({ status: 201, headers: CORS, body: '' });
      }
      return route.fulfill({ status: 200, headers: { ...CORS, 'content-type': 'application/json' }, body: '[]' });
    }

    // Analytics, mappe, font esterni: non escono. Li registriamo per il controllo "zero CDN".
    calls.external.push({ host: u.hostname, type: req.resourceType(), method: req.method() });
    return route.fulfill({ status: 204, headers: CORS, body: '' });
  });
  return calls;
}

// Spegne animazioni/transizioni: i test devono misurare funzioni, non attendere reveal e popup.
async function calm(page) {
  await page.addStyleTag({ content: '*,*::before,*::after{animation:none!important;transition:none!important;scroll-behavior:auto!important}' }).catch(() => {});
}

async function dismissCookies(page) {
  await calm(page);
  const btn = page.getByRole('button', { name: /ho capito|accetta/i }).first();
  if (await btn.isVisible().catch(() => false)) await btn.click({ timeout: 3000 }).catch(() => {});
}

function collectErrors(page) {
  const errors = [];
  page.on('pageerror', (e) => errors.push('pageerror: ' + e.message));
  page.on('console', (m) => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  return errors;
}

module.exports = { mockBackends, dismissCookies, collectErrors, calm, TEST_LEAD };
