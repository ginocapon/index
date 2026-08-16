#!/usr/bin/env node
/**
 * A. EVENT COLLECTOR (server-side)
 * Normalizza eventi da Supabase o da buffer locale JSONL.
 */

import fs from 'node:fs';
import path from 'node:path';
import { normalizeEvent } from '../lib/event-schema.js';
import { hashSession } from '../lib/privacy.js';

const root = process.cwd();
const base = path.join(root, 'righetto-premortem-guardian', 'learning-bridge');
const localBuffer = path.join(base, 'memory', 'events-buffer.jsonl');
const outDir = path.join(root, 'data', 'learning-bridge');

function ensureDir(p) {
  fs.mkdirSync(p, { recursive: true });
}

function readJsonl(filePath) {
  if (!fs.existsSync(filePath)) return [];
  return fs.readFileSync(filePath, 'utf8')
    .split('\n')
    .filter(Boolean)
    .map((line) => {
      try { return JSON.parse(line); } catch { return null; }
    })
    .filter(Boolean);
}

async function fetchSupabaseEvents(sinceIso) {
  const url = process.env.SUPABASE_URL;
  const key = process.env.SUPABASE_SERVICE_KEY || process.env.SUPABASE_ANON_KEY;
  if (!url || !key) return { events: [], source: 'local_only' };

  const params = new URLSearchParams({
    select: 'id,created_at,event_type,session_id,search_id,page_path,source,payload',
    order: 'created_at.desc',
    limit: '5000'
  });
  if (sinceIso) params.set('created_at', `gte.${sinceIso}`);

  const res = await fetch(`${url}/rest/v1/linda_learning_events?${params}`, {
    headers: {
      apikey: key,
      Authorization: `Bearer ${key}`,
      'Content-Type': 'application/json'
    }
  });
  if (!res.ok) return { events: [], source: 'supabase_error', status: res.status };
  const rows = await res.json();
  return { events: rows, source: 'supabase' };
}

export async function collectEvents(options = {}) {
  ensureDir(outDir);
  const sinceIso = options.since || null;
  const remote = await fetchSupabaseEvents(sinceIso);
  const local = readJsonl(localBuffer);

  const normalized = [];
  const rejected = [];

  for (const row of [...remote.events, ...local]) {
    const n = normalizeEvent({
      ...row,
      session_id: row.session_id ? hashSession(row.session_id) : null
    });
    if (n) normalized.push({ ...n, created_at: row.created_at || row.time || new Date().toISOString() });
    else rejected.push(row);
  }

  const report = {
    collected_at: new Date().toISOString(),
    source: remote.source,
    total: normalized.length,
    rejected: rejected.length,
    by_type: normalized.reduce((acc, e) => {
      acc[e.event_type] = (acc[e.event_type] || 0) + 1;
      return acc;
    }, {})
  };

  fs.writeFileSync(path.join(outDir, 'events-normalized-latest.json'), JSON.stringify({ report, events: normalized }, null, 2));
  return { report, events: normalized };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  collectEvents().then(({ report }) => {
    console.log('Event Collector:', report);
  });
}
