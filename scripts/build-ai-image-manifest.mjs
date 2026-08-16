#!/usr/bin/env node
/**
 * Aggiorna data/ai-generated-images.json con elenco file in img/blog/ (editoriali IA).
 * Uso: node scripts/build-ai-image-manifest.mjs
 */
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const blogDir = path.join(root, 'img', 'blog');
const outPath = path.join(root, 'data', 'ai-generated-images.json');

function walk(dir, acc = []) {
  if (!fs.existsSync(dir)) return acc;
  for (const name of fs.readdirSync(dir)) {
    const full = path.join(dir, name);
    if (fs.statSync(full).isDirectory()) walk(full, acc);
    else if (/\.(webp|jpg|jpeg|png|gif)$/i.test(name)) {
      acc.push('img/blog/' + path.relative(blogDir, full).replace(/\\/g, '/'));
    }
  }
  return acc;
}

const existing = JSON.parse(fs.readFileSync(outPath, 'utf8'));
const files = walk(blogDir).sort();
const manifest = {
  ...existing,
  updated: new Date().toISOString().slice(0, 10),
  files,
  fileCount: files.length
};

fs.writeFileSync(outPath, JSON.stringify(manifest, null, 2) + '\n');
console.log('Manifest aggiornato:', files.length, 'file in img/blog/');
