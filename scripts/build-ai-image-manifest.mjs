#!/usr/bin/env node
/**
 * Aggiorna data/ai-generated-images.json — elenco img/blog/ + regole pathPrefixes/excludePaths.
 * Uso: node scripts/build-ai-image-manifest.mjs
 */
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const blogDir = path.join(root, 'img', 'blog');
const outPath = path.join(root, 'data', 'ai-generated-images.json');

/** Prefissi cartella: tutte le immagini sotto questi path ricevono marchio FOTO AI via JS */
const PATH_PREFIXES = [
  'img/blog/',
  'img/foto-servizi/',
  'img/guida-loft-aziende/',
  'img/demo/',
  'img/social/'
];

/** Mai marchiare: foto annunci reali, team, brand, asset OG/meta */
const EXCLUDE_PATHS = ['img/immobili/', 'img/team/', 'img/brand/', 'img/og-'];

/** Singoli file IA fuori dai prefissi sopra */
const EXTRA_AI_PATHS = [];

function walk(dir, prefix, acc = []) {
  if (!fs.existsSync(dir)) return acc;
  for (const name of fs.readdirSync(dir)) {
    const full = path.join(dir, name);
    if (fs.statSync(full).isDirectory()) walk(full, prefix, acc);
    else if (/\.(webp|jpg|jpeg|png|gif)$/i.test(name)) {
      acc.push(prefix + path.relative(dir, full).replace(/\\/g, '/'));
    }
  }
  return acc;
}

const existing = JSON.parse(fs.readFileSync(outPath, 'utf8'));
const files = walk(blogDir, 'img/blog/').sort();
const explicitPaths = [...new Set([...(existing.explicitPaths || []), ...EXTRA_AI_PATHS])]
  .filter((p) => !files.includes(p))
  .sort();

const manifest = {
  version: existing.version || 1,
  updated: new Date().toISOString().slice(0, 10),
  policy:
    'Marchio FOTO AI automatico (site-ai-disclosure.js) su pathPrefixes. Esclusi img/immobili/, img/team/, img/brand/, img/og-. Dopo nuove hero blog: node scripts/build-ai-image-manifest.mjs; audit: node scripts/audit-foto-ai.mjs',
  pathPrefixes: PATH_PREFIXES,
  excludePaths: EXCLUDE_PATHS,
  explicitPaths,
  files,
  fileCount: files.length
};

fs.writeFileSync(outPath, JSON.stringify(manifest, null, 2) + '\n');
console.log('Manifest aggiornato:', files.length, 'file img/blog/,', PATH_PREFIXES.length, 'pathPrefixes,', EXCLUDE_PATHS.length, 'excludePaths');
