#!/usr/bin/env node
/**
 * Genera feed statici in feeds/ da snapshot JSON o da Supabase (service role).
 *
 * Uso:
 *   node scripts/generate-portal-feeds.mjs --from-json path/to/immobili.json
 *   SUPABASE_URL=... SUPABASE_SERVICE_ROLE_KEY=... node scripts/generate-portal-feeds.mjs --from-supabase
 *
 * Non applica migrazioni e non pubblica sui portali: scrive solo file locali.
 */
import { mkdir, writeFile, readFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  buildIdealistaJson,
  buildImmobiliareXml,
  isFeedEligible,
} from '../js/portal-feeds-core.mjs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const outDir = join(root, 'feeds');

async function loadFromJson(path) {
  const raw = JSON.parse(await readFile(path, 'utf8'));
  return Array.isArray(raw) ? raw : raw.immobili || raw.data || [];
}

async function loadFromSupabase() {
  const url = (process.env.SUPABASE_URL || '').replace(/\/$/, '');
  const key = process.env.SUPABASE_SERVICE_ROLE_KEY || '';
  if (!url || !key) throw new Error('Mancano SUPABASE_URL o SUPABASE_SERVICE_ROLE_KEY');
  const select =
    'id,codice,titolo,tipo_operazione,categoria,tipologia,comune,indirizzo,lat,lng,prezzo,prezzo_portali,superficie,superficie_portali,locali,camere,bagni,bagni_totali,piano,classe_energetica,ipe_kwh,garage,giardino,terrazzo,cantina,ascensore,piscina,arredato,foto,foto_urls,youtube_id,virtual_tour,descrizione,descrizione_ridotta,attivo,venduto,affittato,cestino,pubblica_immobiliare_it,pubblica_idealista,updated_at';
  const rows = [];
  for (let offset = 0; offset < 5000; offset += 500) {
    const q = new URL(url + '/rest/v1/immobili');
    q.searchParams.set('select', select);
    q.searchParams.set('attivo', 'eq.true');
    q.searchParams.set('venduto', 'eq.false');
    q.searchParams.set('affittato', 'eq.false');
    q.searchParams.set('cestino', 'eq.false');
    q.searchParams.set('order', 'id');
    q.searchParams.set('offset', String(offset));
    q.searchParams.set('limit', '500');
    const r = await fetch(q, {
      headers: { apikey: key, Authorization: 'Bearer ' + key },
    });
    if (!r.ok) throw new Error('Supabase ' + r.status + ': ' + (await r.text()).slice(0, 200));
    const chunk = await r.json();
    if (!Array.isArray(chunk) || !chunk.length) break;
    rows.push(...chunk);
    if (chunk.length < 500) break;
  }
  return rows;
}

async function main() {
  const args = process.argv.slice(2);
  let rows = [];
  if (args.includes('--from-supabase')) {
    rows = await loadFromSupabase();
  } else {
    const i = args.indexOf('--from-json');
    if (i < 0 || !args[i + 1]) {
      console.error(
        'Uso: --from-json <file.json> oppure --from-supabase (con env SUPABASE_*)'
      );
      process.exit(1);
    }
    rows = await loadFromJson(args[i + 1]);
  }

  await mkdir(outDir, { recursive: true });
  const xml = buildImmobiliareXml(rows);
  const idealista = buildIdealistaJson(rows, {
    ilc: process.env.IDEALISTA_ILC || '',
  });
  await writeFile(join(outDir, 'immobiliare-feed.xml'), xml, 'utf8');
  await writeFile(join(outDir, 'idealista-feed.json'), JSON.stringify(idealista, null, 2), 'utf8');
  const nImm = rows.filter((r) => isFeedEligible(r, 'immobiliare')).length;
  const nId = rows.filter((r) => isFeedEligible(r, 'idealista')).length;
  console.log('Scritti feeds/immobiliare-feed.xml (' + nImm + ') e feeds/idealista-feed.json (' + nId + ')');
}

main().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
