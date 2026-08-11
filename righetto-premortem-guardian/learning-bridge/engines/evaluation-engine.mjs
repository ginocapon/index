#!/usr/bin/env node
/**
 * D. EVALUATION ENGINE — backtest baseline vs candidato, rollback automatico.
 */

import fs from 'node:fs';
import path from 'node:path';
import { collectEvents } from './event-collector.mjs';

const root = process.cwd();
const outDir = path.join(root, 'data', 'learning-bridge');
const versionsPath = path.join(outDir, 'ranking-versions.json');

function readConfig() {
  const cfgPath = path.join(root, 'righetto-premortem-guardian', 'learning-bridge', 'config.yaml');
  const raw = fs.readFileSync(cfgPath, 'utf8');
  const rollbackMatch = raw.match(/rollback_regression_pct:\s*([\d.]+)/);
  const minConfMatch = raw.match(/min_confidence:\s*([\d.]+)/);
  return {
    rollback_regression_pct: rollbackMatch ? parseFloat(rollbackMatch[1]) : 0.08,
    min_confidence: minConfMatch ? parseFloat(minConfMatch[1]) : 0.55,
    apply_ranking_changes: /apply_ranking_changes:\s*true/.test(raw)
  };
}

function computeKpis(events) {
  const shown = events.filter((e) => e.event_type === 'property_results_shown');
  const clicks = events.filter((e) => e.event_type === 'property_clicked');
  const leads = events.filter((e) => e.event_type === 'lead_created');
  const noResult = events.filter((e) => e.event_type === 'search_no_result');
  const searches = events.filter((e) => e.event_type === 'search_started');

  const impressions = shown.reduce((n, e) => n + (e.payload?.property_ids?.length || e.payload?.result_count || 0), 0);
  const ctr = impressions > 0 ? clicks.length / impressions : 0;
  const conversionRate = searches.length > 0 ? leads.length / searches.length : 0;
  const zeroResultRate = searches.length > 0 ? noResult.length / searches.length : 0;

  return {
    property_ctr: Number(ctr.toFixed(4)),
    property_detail_views: clicks.length,
    visit_requests: events.filter((e) => e.event_type === 'visit_requested').length,
    leads: leads.length,
    conversion_rate: Number(conversionRate.toFixed(4)),
    zero_result_rate: Number(zeroResultRate.toFixed(4)),
    searches: searches.length
  };
}

function loadVersions() {
  if (!fs.existsSync(versionsPath)) {
    return {
      active: 'baseline_v1',
      versions: [{
        ranking_version: 'baseline_v1',
        created_at: new Date().toISOString(),
        features: { sort: 'created_at_desc' },
        weights: {},
        sample_size: 0,
        confidence: 1,
        status: 'active',
        metrics_before: null,
        metrics_after: null
      }]
    };
  }
  return JSON.parse(fs.readFileSync(versionsPath, 'utf8'));
}

function saveVersions(data) {
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(versionsPath, JSON.stringify(data, null, 2));
}

export async function runEvaluationEngine() {
  const cfg = readConfig();
  const { events } = await collectEvents();
  const baselineMetrics = computeKpis(events.filter((e) => (e.payload?.ranking_version || 'baseline_v1') === 'baseline_v1'));
  const candidateMetrics = computeKpis(events.filter((e) => e.payload?.ranking_version && e.payload.ranking_version !== 'baseline_v1'));

  const store = loadVersions();
  const active = store.versions.find((v) => v.ranking_version === store.active) || store.versions[0];

  const candidate = {
    ranking_version: `candidate_${Date.now()}`,
    created_at: new Date().toISOString(),
    features: { sort: 'engagement_weighted_v1', boost_clicked_features: true },
    weights: { garage_match: 0.12, terrazzo_soft: 0.06, recency: 0.4 },
    sample_size: events.length,
    confidence: events.length >= 30 ? 0.6 : 0.3,
    status: 'proposed',
    metrics_before: baselineMetrics,
    metrics_after: candidateMetrics
  };

  let rollback = null;
  const activeCandidate = store.versions.find((v) => v.status === 'active' && v.ranking_version !== 'baseline_v1');
  if (activeCandidate?.metrics_after && baselineMetrics) {
    const regress =
      baselineMetrics.conversion_rate > 0 &&
      candidateMetrics.conversion_rate < baselineMetrics.conversion_rate * (1 - cfg.rollback_regression_pct);
    if (regress) {
      rollback = {
        from: activeCandidate.ranking_version,
        to: 'baseline_v1',
        reason: 'conversion_rate_regression',
        threshold: cfg.rollback_regression_pct,
        at: new Date().toISOString()
      };
      activeCandidate.status = 'rolled_back';
      store.active = 'baseline_v1';
    }
  }

  const improved =
    candidateMetrics.property_ctr > baselineMetrics.property_ctr ||
    candidateMetrics.conversion_rate > baselineMetrics.conversion_rate;

  if (cfg.apply_ranking_changes && improved && candidate.confidence >= cfg.min_confidence && !rollback) {
    candidate.status = 'active';
    store.active = candidate.ranking_version;
    store.versions.push(candidate);
  } else {
    candidate.status = 'proposed_only';
    store.versions.push(candidate);
  }

  saveVersions(store);

  const evaluation = {
    generated_at: new Date().toISOString(),
    active_ranking: store.active,
    evaluation_metrics: { baseline: baselineMetrics, candidate: candidateMetrics },
    candidate_ranking_changes: [candidate],
    confidence: candidate.confidence,
    rollback_information: rollback,
    apply_ranking_changes: cfg.apply_ranking_changes,
    recommendation: rollback
      ? 'rollback_to_baseline'
      : improved
        ? 'review_candidate'
        : 'keep_baseline'
  };

  fs.writeFileSync(path.join(outDir, 'evaluation-latest.json'), JSON.stringify(evaluation, null, 2));
  return evaluation;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  runEvaluationEngine().then((e) => console.log('Evaluation:', e.recommendation));
}
