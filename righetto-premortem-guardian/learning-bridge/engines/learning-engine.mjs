#!/usr/bin/env node
/**
 * B. LEARNING ENGINE — aggregazione statistica (no ML).
 */

import fs from 'node:fs';
import path from 'node:path';
import { collectEvents } from './event-collector.mjs';

const root = process.cwd();
const outDir = path.join(root, 'data', 'learning-bridge');
const configPath = path.join(root, 'righetto-premortem-guardian', 'learning-bridge', 'config.yaml');

function readMinObs() {
  try {
    const raw = fs.readFileSync(configPath, 'utf8');
    const m = raw.match(/min_observations:\s*(\d+)/);
    return m ? parseInt(m[1], 10) : 30;
  } catch {
    return 30;
  }
}

function bucketKey(criteria) {
  const parts = [
    criteria.tipo_operazione || 'any',
    criteria.comune || criteria.zona || 'any',
    criteria.tipologia || 'any'
  ];
  return parts.join('|').toLowerCase();
}

export async function runLearningEngine() {
  const minObs = readMinObs();
  const { events } = await collectEvents();
  const periodStart = events.length ? events[events.length - 1].created_at : null;
  const periodEnd = events.length ? events[0].created_at : null;

  const aggregates = {
    feature_frequency: {},
    zone_frequency: {},
    budget_bands: {},
    combinations: {},
    clicked_properties: {},
    lead_properties: {},
    zero_result_queries: [],
    unanswered_questions: []
  };

  const searches = new Map();

  for (const ev of events) {
    const c = ev.payload?.criteria || {};

    if (ev.event_type === 'search_started') {
      searches.set(ev.search_id || ev.session_id, { criteria: c, shown: [], clicked: [], lead: false });
    }

    if (['search_started', 'property_results_shown'].includes(ev.event_type)) {
      for (const f of ['garage', 'giardino', 'terrazzo', 'camere', 'tipologia']) {
        if (c[f]) aggregates.feature_frequency[f] = (aggregates.feature_frequency[f] || 0) + 1;
      }
      const zone = c.comune || c.zona;
      if (zone) aggregates.zone_frequency[zone.toLowerCase()] = (aggregates.zone_frequency[zone.toLowerCase()] || 0) + 1;
      if (c.budget_min || c.budget_max) {
        const band = `${c.budget_min || 0}-${c.budget_max || 'inf'}`;
        aggregates.budget_bands[band] = (aggregates.budget_bands[band] || 0) + 1;
      }
      const combo = bucketKey(c);
      aggregates.combinations[combo] = (aggregates.combinations[combo] || 0) + 1;
    }

    if (ev.event_type === 'property_clicked' && ev.payload?.property_id) {
      const id = String(ev.payload.property_id);
      aggregates.clicked_properties[id] = (aggregates.clicked_properties[id] || 0) + 1;
      const s = searches.get(ev.search_id);
      if (s) s.clicked.push(id);
    }

    if (ev.event_type === 'lead_created') {
      const s = searches.get(ev.search_id);
      if (s) s.lead = true;
      if (ev.payload?.property_id) {
        const id = String(ev.payload.property_id);
        aggregates.lead_properties[id] = (aggregates.lead_properties[id] || 0) + 1;
      }
    }

    if (ev.event_type === 'search_no_result') {
      aggregates.zero_result_queries.push({ criteria: c, at: ev.created_at });
    }

    if (ev.event_type === 'question_unanswered') {
      aggregates.unanswered_questions.push({
        hash: ev.payload?.user_message_hash,
        at: ev.created_at
      });
    }
  }

  const sufficient = Object.entries(aggregates.combinations)
    .filter(([, n]) => n >= minObs)
    .map(([k, n]) => ({ bucket: k, count: n }));

  const report = {
    generated_at: new Date().toISOString(),
    period: { start: periodStart, end: periodEnd },
    min_observations: minObs,
    total_events: events.length,
    sufficient_buckets: sufficient.length,
    emerging_preferences: Object.entries(aggregates.feature_frequency)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([feature, count]) => ({ feature, count })),
    property_demand_patterns: {
      top_zones: Object.entries(aggregates.zone_frequency).sort((a, b) => b[1] - a[1]).slice(0, 15),
      top_combinations: sufficient.slice(0, 20)
    },
    aggregates
  };

  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(path.join(outDir, 'learning-report.json'), JSON.stringify(report, null, 2));
  return report;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  runLearningEngine().then((r) => console.log('Learning Engine OK — events:', r.total_events));
}
