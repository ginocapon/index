/**
 * Simula flusso Consent Mode + hit GA4 (page_view) in Node senza browser.
 */
const https = require('https');
const fs = require('fs');
const path = require('path');

const GA_ID = 'G-PHEL8KXLBX';
const dataLayer = [];

function gtag() {
  dataLayer.push(Array.from(arguments));
}

const gaSrc = fs.readFileSync(path.join(__dirname, '..', 'js', 'ga-consent.js'), 'utf8');

global.window = {
  dataLayer,
  localStorage: {
    _v: null,
    getItem() { return this._v; },
    setItem(k, v) { this._v = v; }
  },
  rigGaConsentUpdate: null
};
global.document = {
  createElement() { return { async: true, src: '' }; },
  head: { appendChild() {} },
  body: { appendChild() {} },
  addEventListener() {},
  getElementById() { return null; },
  querySelectorAll() { return []; }
};
global.localStorage = window.localStorage;
global.gtag = gtag;

eval(gaSrc);

const defaultConsent = dataLayer.find(x => x[0] === 'consent' && x[1] === 'default');
const denied = defaultConsent && defaultConsent[2].analytics_storage === 'denied';

window.rigGaConsentUpdate({ necessary: true, analytics: true, marketing: false });
const updateConsent = dataLayer.filter(x => x[0] === 'consent' && x[1] === 'update').pop();
const granted = updateConsent && updateConsent[2].analytics_storage === 'granted';

const config = dataLayer.find(x => x[0] === 'config');
const hasConfig = config && config[1] === GA_ID;

function head(url) {
  return new Promise((resolve) => {
    https.get(url, { timeout: 15000 }, (res) => {
      res.resume();
      resolve(res.statusCode);
    }).on('error', () => resolve(0));
  });
}

(async () => {
  const gtagStatus = await head(`https://www.googletagmanager.com/gtag/js?id=${GA_ID}`);
  const pass = denied && granted && hasConfig && gtagStatus === 200;
  console.log(JSON.stringify({
    pass,
    measurementId: GA_ID,
    consent_default_denied: denied,
    consent_update_granted: granted,
    gtag_config_called: hasConfig,
    gtag_js_endpoint_status: gtagStatus,
    dataLayer_events: dataLayer.length,
    note: pass
      ? 'Flusso OK: eventi page_view arriveranno in GA4 Realtime dopo consenso analitici nel browser'
      : 'Verifica fallita'
  }, null, 2));
  process.exit(pass ? 0 : 1);
})();
