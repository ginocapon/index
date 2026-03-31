/**
 * Aggiunge uno snapshot a data/analytics-dashboard.json.
 * Variabili d'ambiente (impostate da GitHub Actions workflow_dispatch):
 * SNAP_CLICKS, SNAP_IMPRESSIONS, SNAP_CTR, SNAP_POSITION, SNAP_USERS, SNAP_EVENTS,
 * SNAP_NEWUSERS (opzionale), SNAP_INDEXED_PAGES (opzionale), SNAP_NOTE, SNAP_PERIODO
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, '..');
const filePath = path.join(root, 'data', 'analytics-dashboard.json');

function num(v) {
  if (v == null || v === '') return 0;
  const n = parseFloat(String(v).replace(',', '.'));
  return Number.isFinite(n) ? n : 0;
}

function int(v) {
  return Math.round(num(v));
}

const raw = fs.readFileSync(filePath, 'utf8');
const data = JSON.parse(raw);

const now = new Date();
const snapshotAt = now.toISOString();
const dataDate = snapshotAt.slice(0, 10);

const snap = {
  snapshotAt,
  data: dataDate,
  periodo: process.env.SNAP_PERIODO || '28gg',
  clicks: int(process.env.SNAP_CLICKS),
  impressions: int(process.env.SNAP_IMPRESSIONS),
  ctr: num(process.env.SNAP_CTR),
  position: num(process.env.SNAP_POSITION),
  users: int(process.env.SNAP_USERS),
  events: int(process.env.SNAP_EVENTS),
  note: (process.env.SNAP_NOTE || '').trim()
};

const nu = process.env.SNAP_NEWUSERS;
if (nu != null && String(nu).trim() !== '') {
  const n = int(nu);
  snap.newusers = n;
}

if (!Array.isArray(data.snapshots)) data.snapshots = [];
data.snapshots.push(snap);
data.lastUpdated = dataDate;

const indexed = process.env.SNAP_INDEXED_PAGES;
if (indexed != null && String(indexed).trim() !== '') {
  const ip = int(indexed);
  if (ip > 0) data.indexedPages = ip;
}

fs.writeFileSync(filePath, JSON.stringify(data, null, 2) + '\n', 'utf8');
console.log('OK snapshot', snapshotAt, 'clicks=', snap.clicks);
