#!/usr/bin/env node
/**
 * Genera data/chatbot/archivio-a-100-faq.json, archivio-b-100-faq.json,
 * inventario_immobili.json (incongruenze documentate) e flusso-apertura-chat.json
 * da linda-kb-seed-300.csv + metadati verificati in repo.
 *
 * Uso: node scripts/build-chatbot-archivi.cjs
 */
'use strict';
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const outDir = path.join(root, 'data', 'chatbot');

function parseCsvSemicolon(text) {
  const rows = [];
  let row = [];
  let field = '';
  let inQ = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQ) {
      if (c === '"') {
        if (text[i + 1] === '"') { field += '"'; i++; }
        else inQ = false;
      } else field += c;
      continue;
    }
    if (c === '"') { inQ = true; continue; }
    if (c === ';') { row.push(field); field = ''; continue; }
    if (c === '\n' || c === '\r') {
      if (c === '\r' && text[i + 1] === '\n') i++;
      row.push(field);
      field = '';
      if (row.some((x) => x.length)) rows.push(row);
      row = [];
      continue;
    }
    field += c;
  }
  if (field.length || row.length) { row.push(field); rows.push(row); }
  return rows;
}

const csvPath = path.join(root, 'data', 'linda-kb-seed-300.csv');
const raw = fs.readFileSync(csvPath, 'utf8').replace(/^\uFEFF/, '');
const table = parseCsvSemicolon(raw);
const header = table[0];
const idx = (n) => header.indexOf(n);
const records = table.slice(1).map((r) => ({
  domanda: r[idx('domanda')] || '',
  varianti: (r[idx('varianti')] || '').split('|').filter(Boolean),
  risposta: r[idx('risposta')] || '',
  categoria: (r[idx('categoria')] || '').trim(),
  fonte_titolo: r[idx('fonte_titolo')] || '',
  fonte_url: r[idx('fonte_url')] || '',
}));

const CAT_A = new Set(['mutui', 'fiscale', 'documenti', 'procedure', 'territorio', 'vendita', 'acquisto']);
const CAT_B = new Set(['affitto', 'azienda']);

function toFaq(row, id) {
  const keys = [row.domanda.replace(/^Domanda su:\s*/i, '').trim()]
    .concat(row.varianti)
    .filter(Boolean);
  const fonte = row.fonte_titolo
    ? { titolo: row.fonte_titolo, url: row.fonte_url || null }
    : (row.fonte_url ? { titolo: 'Fonte', url: row.fonte_url } : null);
  return {
    id,
    k: keys.slice(0, 12),
    domanda: row.domanda,
    r: row.risposta,
    categoria: row.categoria,
    fonte,
  };
}

const poolA = records.filter((r) => CAT_A.has(r.categoria));
const poolB = records.filter((r) => CAT_B.has(r.categoria));
const restA = records.filter((r) => !CAT_B.has(r.categoria) && !poolA.includes(r));
const restB = records.filter((r) => !CAT_A.has(r.categoria) && !poolB.includes(r));

const faqA = poolA.concat(restA).slice(0, 100).map((r, i) => toFaq(r, 'A-' + String(i + 1).padStart(3, '0')));
const usedA = new Set(faqA.map((f) => f.domanda));
const faqB = poolB.concat(restB.filter((r) => !usedA.has(r.domanda))).slice(0, 100).map((r, i) => toFaq(r, 'B-' + String(i + 1).padStart(3, '0')));

const inventario = {
  schema_version: '1.0',
  titolo: 'Inventario immobili — incongruenze e note di verifica (chat)',
  data_verifica: '2026-10-11',
  origine: 'Integrazione chatbot: flusso_apertura_chat + confronto titolo/slug/comune in data/og-immobili.json',
  nota: 'Non usare questo file per prezzi o disponibilità: solo segnalazione incongruenze. Dati live da Supabase.',
  incongruenze: [
    {
      codice: 'LF0242',
      campi: ['comune', 'ubicazione'],
      descrizione:
        'Il titolo pubblico dell\'annuncio indica Limena, mentre slug SEO e metadati share riportano Padova: prima di escludere o proporre l\'immobile in una ricerca per comune, verificare l\'ubicazione con l\'agenzia.',
      evidenze: [
        'Titolo: «AFFITTASI APPARTAMENTO A LIMENA…» (og-immobili.json)',
        'Slug/share: appartamento-affitto-residenziale-padova-lf0242',
      ],
    },
    {
      codice: 'LO0287',
      campi: ['bagni'],
      descrizione:
        'I dati dell\'annuncio risultano discordanti sul numero di bagni. Non confermare un valore definitivo in chat: indicare che serve verifica agenziale.',
      evidenze: ['Esempio operativo in flusso_apertura_chat (2026-10-11)'],
    },
  ],
};

const flussoPath = path.join(outDir, 'flusso-apertura-chat.json');
const flussoDefault = {
  schema_version: '1.0',
  titolo: 'Apertura, coinvolgimento e passaggio all\'agenzia',
  data_verifica: '2026-10-11',
  stato: 'integrato',
  passaggi: [],
};

fs.mkdirSync(outDir, { recursive: true });
if (!fs.existsSync(flussoPath)) {
  fs.writeFileSync(flussoPath, JSON.stringify(flussoDefault, null, 2), 'utf8');
}

fs.writeFileSync(
  path.join(outDir, 'archivio-a-100-faq.json'),
  JSON.stringify(
    {
      schema_version: '1.0',
      titolo: 'Archivio A — normative e mercato (100 FAQ)',
      data_verifica: '2026-10-11',
      fonte_seed: 'data/linda-kb-seed-300.csv',
      voci: faqA,
    },
    null,
    2
  ),
  'utf8'
);

fs.writeFileSync(
  path.join(outDir, 'archivio-b-100-faq.json'),
  JSON.stringify(
    {
      schema_version: '1.0',
      titolo: 'Archivio B — immobili e servizi collegati (100 FAQ)',
      data_verifica: '2026-10-11',
      fonte_seed: 'data/linda-kb-seed-300.csv',
      nota: 'Non usare per prezzo/disponibilità annuncio: solo Supabase live attivo=true venduto=false affittato=false.',
      voci: faqB,
    },
    null,
    2
  ),
  'utf8'
);

fs.writeFileSync(path.join(outDir, 'inventario_immobili.json'), JSON.stringify(inventario, null, 2), 'utf8');

console.log('Archivio A:', faqA.length, 'voci');
console.log('Archivio B:', faqB.length, 'voci');
console.log('Incongruenze inventario:', inventario.incongruenze.length);
