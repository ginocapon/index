#!/usr/bin/env node
/**
 * LINDA Learning Bridge — orchestratore job (integrato nel Guardian dispatcher).
 *
 * Usage:
 *   node righetto-premortem-guardian/learning-bridge/run.mjs collect
 *   node righetto-premortem-guardian/learning-bridge/run.mjs daily|weekly|biweekly|monthly|full
 */

import fs from 'node:fs';
import path from 'node:path';
import { collectEvents } from './engines/event-collector.mjs';
import { runLearningEngine } from './engines/learning-engine.mjs';
import { runRankingInsightEngine } from './engines/ranking-insight-engine.mjs';
import { runEvaluationEngine } from './engines/evaluation-engine.mjs';

const root = process.cwd();
const reportsDir = path.join(root, 'data', 'learning-bridge');
const memoryDir = path.join(root, 'righetto-premortem-guardian', 'learning-bridge', 'memory');

function ensure() {
  fs.mkdirSync(reportsDir, { recursive: true });
  fs.mkdirSync(memoryDir, { recursive: true });
}

function logEvent(type, data = {}) {
  ensure();
  fs.appendFileSync(
    path.join(memoryDir, 'bridge-runs.jsonl'),
    JSON.stringify({ time: new Date().toISOString(), type, ...data }) + '\n'
  );
}

async function dailyQuality() {
  const { report } = await collectEvents();
  logEvent('daily_quality', report);
  return { job: 'daily_quality', report };
}

async function weeklyAggregate() {
  const learning = await runLearningEngine();
  logEvent('weekly_aggregate', { total_events: learning.total_events });
  return { job: 'weekly_aggregate', learning };
}

async function biweeklyAnalysis() {
  const insights = await runRankingInsightEngine();
  logEvent('biweekly_analysis', { insights: insights.ranking_insights.length });
  return { job: 'biweekly_analysis', insights };
}

async function monthlyEvaluation() {
  const evaluation = await runEvaluationEngine();
  logEvent('monthly_evaluation', { recommendation: evaluation.recommendation });
  return { job: 'monthly_evaluation', evaluation };
}

async function fullPipeline() {
  await dailyQuality();
  const learning = await weeklyAggregate();
  const insights = await biweeklyAnalysis();
  const evaluation = await monthlyEvaluation();

  const bundle = {
    generated_at: new Date().toISOString(),
    learning_report: learning.learning,
    ranking_insights: insights.insights.ranking_insights,
    unanswered_questions: insights.insights.unanswered_questions,
    emerging_preferences: insights.insights.emerging_preferences,
    property_demand_patterns: learning.learning?.property_demand_patterns,
    seo_opportunities: insights.insights.seo_opportunities,
    candidate_ranking_changes: evaluation.evaluation.candidate_ranking_changes,
    evaluation_metrics: evaluation.evaluation.evaluation_metrics,
    confidence: evaluation.evaluation.confidence,
    rollback_information: evaluation.evaluation.rollback_information
  };

  fs.writeFileSync(path.join(reportsDir, 'learning-bridge-full-report.json'), JSON.stringify(bundle, null, 2));
  logEvent('full_pipeline', { ok: true });
  return bundle;
}

const job = process.argv[2] || 'collect';

const runners = {
  collect: () => collectEvents(),
  daily: dailyQuality,
  weekly: weeklyAggregate,
  biweekly: biweeklyAnalysis,
  monthly: monthlyEvaluation,
  full: fullPipeline
};

(runners[job] || runners.collect)()
  .then((result) => {
    console.log(`LINDA Learning Bridge [${job}] completed.`);
    if (result?.report) console.log(JSON.stringify(result.report, null, 2));
  })
  .catch((err) => {
    console.error('Learning Bridge error:', err.message);
    process.exitCode = 1;
  });
