#!/usr/bin/env node
/**
 * Esporta le FAQ storiche di Linda (js/chatbot.js → FAQ_DATA) in un CSV importabile
 * dal pannello admin-kb.html, e produce un audit dei dati numerici senza fonte.
 *
 * Uso:  node scripts/linda_esporta_faq.js
 * Output: data/linda-kb-seed-faq.csv  (tutte le voci arrivano come "Da verificare")
 *         data/linda-faq-audit.json   (voci con numeri/percentuali/date da verificare)
 * Nessuna rete, nessun segreto.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const root = path.resolve(__dirname, '..');
const src = fs.readFileSync(path.join(root, 'js', 'chatbot.js'), 'utf8');

const start = src.indexOf('const FAQ_DATA = [');
if (start < 0) { console.error('FAQ_DATA non trovato'); process.exit(1); }
let depth = 0, end = -1, inStr = null, esc = false;
for (let i = src.indexOf('[', start); i < src.length; i++) {
  const c = src[i];
  if (inStr) { if (esc) esc = false; else if (c === '\\') esc = true; else if (c === inStr) inStr = null; continue; }
  if (c === '\'' || c === '"' || c === '`') { inStr = c; continue; }
  if (c === '[') depth++;
  else if (c === ']') { depth--; if (depth === 0) { end = i; break; } }
}
if (end < 0) { console.error('Fine di FAQ_DATA non trovata'); process.exit(1); }
const faq = vm.runInNewContext('(' + src.slice(src.indexOf('[', start), end + 1) + ')', {});

const categoria = (t) => {
  t = t.toLowerCase();
  if (/mutu/.test(t)) return 'mutui';
  if (/\bimu\b|tasi|cedolare|fiscal|tass[ae]|agevolaz/.test(t)) return 'fiscale';
  if (/rogito|document|catast|ape\b|visura|planimetri/.test(t)) return 'documenti';
  if (/affitt|locaz|inquilin/.test(t)) return 'affitto';
  if (/vender|vendita|valutaz|stima/.test(t)) return 'vendita';
  if (/acquist|compr/.test(t)) return 'acquisto';
  if (/orari|sede|indirizzo|telefon|contatt/.test(t)) return 'azienda';
  return 'servizi';
};
const q = (s) => { s = String(s == null ? '' : s); return /[;"\n\r]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };
// numeri che richiedono una fonte: percentuali, euro, giorni/mesi/anni, anni 20xx
const RE_NUM = /(\d+[.,]?\d*\s*(%|€|euro|giorni|mesi|anni|mq|m2))|\b20\d\d\b|€\s*\d/gi;

const righe = ['domanda;varianti;risposta;categoria;fonte_titolo;fonte_url;scade_il'];
const audit = [];
let troppoLunghe = 0, saltate = 0;
faq.forEach((e, i) => {
  if (!e || !Array.isArray(e.k) || typeof e.r !== 'string') { saltate++; return; }
  const dom = 'Domanda su: ' + e.k.slice(0, 3).join(', ');
  const ris = e.r.length > 2500 ? e.r.slice(0, 2490) + '…' : e.r;
  if (e.r.length > 2500) troppoLunghe++;
  righe.push([dom, e.k.join('|'), ris, categoria(e.k.join(' ') + ' ' + e.r), '', '', ''].map(q).join(';'));
  const num = e.r.match(RE_NUM);
  if (num) audit.push({ indice: i, parole_chiave: e.k.slice(0, 4), numeri_trovati: [...new Set(num.map((s) => s.trim()))].slice(0, 8), ha_fonte_citata: /fonte|omi|istat|fimaa|agenzia delle entrate|banca d'italia/i.test(e.r) });
});

fs.mkdirSync(path.join(root, 'data'), { recursive: true });
fs.writeFileSync(path.join(root, 'data', 'linda-kb-seed-faq.csv'), '\uFEFF' + righe.join('\r\n'), 'utf8');
fs.writeFileSync(path.join(root, 'data', 'linda-faq-audit.json'), JSON.stringify({ totale_voci: faq.length, con_dati_numerici: audit.length, senza_fonte: audit.filter((a) => !a.ha_fonte_citata).length, voci: audit }, null, 2), 'utf8');
console.log(`FAQ esportate: ${righe.length - 1}/${faq.length} (saltate ${saltate}, troncate ${troppoLunghe})`);
console.log(`Voci con dati numerici: ${audit.length} — di cui SENZA fonte citata: ${audit.filter((a) => !a.ha_fonte_citata).length}`);
