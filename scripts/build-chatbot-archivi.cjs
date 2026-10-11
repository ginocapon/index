#!/usr/bin/env node
/**
 * NON rigenera nulla. I 4 file in data/chatbot/ sono gli ORIGINALI forniti dal titolare
 * (archivio A 100 FAQ, archivio B 100 FAQ, inventario 23 annunci, flusso apertura chat)
 * e vanno copiati tali e quali. Questo script li verifica soltanto (conteggi e struttura).
 *
 * Uso: node scripts/build-chatbot-archivi.cjs          (verifica)
 *      node scripts/build-chatbot-archivi.cjs --copy A.json B.json INV.json FLUSSO.json
 *        (copia byte per byte gli originali nei 4 file di destinazione, poi verifica)
 */
'use strict';
const fs = require('fs');
const path = require('path');
const out = path.resolve(__dirname, '..', 'data', 'chatbot');
const NAMES = ['archivio-a-100-faq.json', 'archivio-b-100-faq.json', 'inventario_immobili.json', 'flusso-apertura-chat.json'];

const args = process.argv.slice(2);
if (args[0] === '--copy') {
  if (args.length !== 5) { console.error('Servono 4 file originali: A B INVENTARIO FLUSSO'); process.exit(1); }
  NAMES.forEach((n, i) => fs.copyFileSync(args[i + 1], path.join(out, n)));
}
const read = (n) => JSON.parse(fs.readFileSync(path.join(out, n), 'utf8'));
const a = read(NAMES[0]), b = read(NAMES[1]), inv = read(NAMES[2]), fl = read(NAMES[3]);
const c = read('archivio-c-200-faq.json');
const errs = [];
if (!Array.isArray(c.faq) || c.faq.length !== 200) errs.push('archivio C: attese 200 FAQ');
(c.faq || []).forEach((f, i) => {
 if (f.id !== 'C' + String(i + 1).padStart(3, '0')) errs.push('ID C fuori sequenza: ' + f.id);
 if (!(f.fonti || []).some(x => /^https:\/\//.test(x.url || ''))) errs.push('C senza fonte: ' + f.id);
});
if (!Array.isArray(a.faq) || a.faq.length !== 100) errs.push('archivio A: attese 100 FAQ, trovate ' + (a.faq || []).length);
if (!Array.isArray(b.faq) || b.faq.length !== 100) errs.push('archivio B: attese 100 FAQ, trovate ' + (b.faq || []).length);
if (!Array.isArray(inv.immobili) || inv.immobili.length !== 23) errs.push('inventario: attesi 23 immobili, trovati ' + (inv.immobili || []).length);
if (!Array.isArray(fl.passaggi) || fl.passaggi.length !== 8) errs.push('flusso: attesi 8 passaggi AP-01..AP-08');
a.faq.forEach((f) => { if (!(f.fonti || []).some((x) => /^https:\/\//.test(x.url || ''))) errs.push('A senza fonte url: ' + f.id); });
if (errs.length) { console.error(errs.join('\n')); process.exit(1); }
console.log('OK: A=' + a.faq.length + ' B=' + b.faq.length + ' C=' + c.faq.length + ' inventario=' + inv.immobili.length + ' passaggi=' + fl.passaggi.length);
