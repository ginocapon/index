#!/usr/bin/env node
/**
 * Audit marchio FOTO AI — verifica copertura manifest vs immagini referenziate nel sito.
 * Uso: node scripts/audit-foto-ai.mjs
 * Exit 0 = OK, 1 = gap da correggere
 */
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const manifestPath = path.join(root, 'data', 'ai-generated-images.json');
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));

const pathPrefixes = manifest.pathPrefixes || ['img/blog/'];
const excludePaths = manifest.excludePaths || [];
const explicitPaths = manifest.explicitPaths || [];
const files = new Set(manifest.files || []);

function normalizeSrc(src) {
  if (!src) return '';
  let s = src.split('?')[0].split('#')[0].toLowerCase().trim();
  if (s.startsWith('http')) {
    try {
      s = new URL(s).pathname.toLowerCase();
    } catch {
      return '';
    }
  }
  return s.replace(/^\//, '');
}

function shouldWatermark(src) {
  if (!src || src.startsWith('data:')) return false;
  if (/favicon|\.svg(\?|$)|spinner|loading\.gif|pixel\.gif|1x1|youtube\.com|img\.youtube/.test(src)) {
    return false;
  }
  for (const ex of excludePaths) {
    if (src.includes(ex.toLowerCase())) return false;
  }
  for (const ex of explicitPaths) {
    if (src.includes(ex.toLowerCase())) return true;
  }
  for (const f of files) {
    if (src === f.toLowerCase() || src.endsWith('/' + f.toLowerCase())) return true;
  }
  for (const pref of pathPrefixes) {
    const p = pref.toLowerCase();
    if (src.includes(p) || src.includes('/' + p)) return true;
  }
  return false;
}

function collectFiles(dir, acc = []) {
  if (!fs.existsSync(dir)) return acc;
  for (const name of fs.readdirSync(dir)) {
    const full = path.join(dir, name);
    if (name === 'node_modules' || name === '.git') continue;
    if (fs.statSync(full).isDirectory()) collectFiles(full, acc);
    else if (/\.(html|js|css)$/i.test(name)) acc.push(full);
  }
  return acc;
}

const imgRe = /(?:src|srcset|content|url)\s*[=:]\s*["']?([^"')\s,]+)/gi;
const refs = new Map();

for (const file of collectFiles(root)) {
  const rel = path.relative(root, file);
  if (rel.startsWith('righetto-premortem-guardian/')) continue;
  const text = fs.readFileSync(file, 'utf8');
  let m;
  while ((m = imgRe.exec(text)) !== null) {
    const raw = m[1].replace(/^url\(/, '').trim();
    for (const part of raw.split(',')) {
      const piece = part.trim().split(/\s+/)[0];
      const norm = normalizeSrc(piece);
      if (!norm.startsWith('img/')) continue;
      if (!refs.has(norm)) refs.set(norm, []);
      refs.get(norm).push(rel);
    }
  }
}

const aiRefs = [];
const realRefs = [];
const unclassified = [];

for (const [src, usedIn] of refs) {
  if (shouldWatermark(src)) aiRefs.push({ src, usedIn });
  else if (excludePaths.some((ex) => src.includes(ex.toLowerCase()))) realRefs.push({ src, usedIn });
  else unclassified.push({ src, usedIn });
}

console.log('=== Audit FOTO AI ===');
console.log('pathPrefixes:', pathPrefixes.join(', '));
console.log('excludePaths:', excludePaths.join(', ') || '(nessuno)');
console.log('files manifest img/blog:', files.size);
console.log('');
console.log('Immagini IA (marchio richiesto):', aiRefs.length, 'path unici');
console.log('Immagini reali (escluse):', realRefs.length, 'path unici');
console.log('Non classificate (verificare):', unclassified.length, 'path unici');

if (unclassified.length) {
  console.log('\n--- ATTENZIONE: path non classificati ---');
  for (const { src, usedIn } of unclassified.slice(0, 30)) {
    console.log(`  ${src}`);
    console.log(`    → ${usedIn.slice(0, 3).join(', ')}${usedIn.length > 3 ? '…' : ''}`);
  }
  if (unclassified.length > 30) console.log(`  … e altri ${unclassified.length - 30}`);
}

// Verifica file su disco in cartelle IA senza prefisso manifest
const aiDirs = ['img/blog', 'img/foto-servizi', 'img/guida-loft-aziende', 'img/demo', 'img/social'];
let diskAi = 0;
for (const d of aiDirs) {
  const full = path.join(root, d);
  if (!fs.existsSync(full)) continue;
  const walk = (dir) => {
    for (const name of fs.readdirSync(dir)) {
      const p = path.join(dir, name);
      if (fs.statSync(p).isDirectory()) walk(p);
      else if (/\.(webp|jpg|jpeg|png|gif)$/i.test(name)) {
        diskAi++;
        const rel = path.relative(root, p).replace(/\\/g, '/');
        if (!shouldWatermark(rel)) {
          console.log('\nWARN file su disco IA non coperto:', rel);
        }
      }
    }
  };
  walk(full);
}
console.log('\nFile raster in cartelle IA:', diskAi);

const ok = unclassified.length === 0;
console.log(ok ? '\n✓ Audit OK' : '\n✗ Audit con gap — aggiornare pathPrefixes/excludePaths in ai-generated-images.json');
process.exit(ok ? 0 : 1);
