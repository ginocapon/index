#!/usr/bin/env node
import {
  buildIdealistaJson,
  buildImmobiliareXml,
  isFeedEligible,
  mandateAlertRows,
} from '../js/portal-feeds-core.mjs';

const base = {
  id: '1',
  codice: 'TEST01',
  titolo: 'Appartamento prova',
  comune: 'Limena',
  tipo_operazione: 'vendita',
  tipologia: 'appartamento',
  prezzo: 200000,
  superficie: 90,
  camere: 3,
  bagni: 1,
  attivo: true,
  venduto: false,
  affittato: false,
  cestino: false,
  foto: ['img/immobili/test.jpg'],
  pubblica_immobiliare_it: true,
  pubblica_idealista: true,
  incarico_scadenza: '2099-01-15',
};

let failed = 0;
function assert(cond, msg) {
  if (!cond) {
    console.error('FAIL:', msg);
    failed++;
  } else console.log('OK:', msg);
}

assert(isFeedEligible(base, 'immobiliare'), 'eligible immobiliare');
assert(!isFeedEligible({ ...base, venduto: true }, 'immobiliare'), 'venduto escluso');
assert(!isFeedEligible({ ...base, pubblica_immobiliare_it: false }, 'immobiliare'), 'flag off');

const xml = buildImmobiliareXml([base]);
assert(xml.includes('TEST01') && xml.includes('<feed>'), 'xml contiene codice');
assert(xml.includes('https://righettoimmobiliare.it/img/immobili/test.jpg'), 'foto assoluta');

const js = buildIdealistaJson([base]);
assert(js.properties.length === 1 && js.properties[0].reference === 'TEST01', 'json idealista');

const alerts = mandateAlertRows(
  [
    { ...base, codice: 'OLD', incarico_scadenza: '2020-01-01' },
    { ...base, codice: 'SOON', incarico_scadenza: new Date().toISOString().slice(0, 10) },
  ],
  { today: new Date('2026-11-24T12:00:00Z'), warnDays: 30 }
);
assert(alerts.expired.some((x) => x.codice === 'OLD'), 'alert scaduto');
assert(alerts.expiring.some((x) => x.codice === 'SOON'), 'alert in scadenza');

if (failed) {
  console.error(failed + ' test falliti');
  process.exit(1);
}
console.log('Tutti i test portal-feeds-core OK');
