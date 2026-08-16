#!/usr/bin/env node
/**
 * Premortem checks per LINDA Learning Bridge (integrato nel Guardian esistente).
 */

import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const dataDir = path.join(root, 'data', 'learning-bridge');
const cfgPath = path.join(root, 'righetto-premortem-guardian', 'learning-bridge', 'config.yaml');

export function runLearningBridgePremortem() {
  const issues = [];
  const warnings = [];

  if (!fs.existsSync(cfgPath)) {
    issues.push({ code: 'LB_CONFIG_MISSING', message: 'config.yaml Learning Bridge assente' });
    return { ok: false, issues, warnings };
  }

  const cfg = fs.readFileSync(cfgPath, 'utf8');
  if (/apply_ranking_changes:\s*true/.test(cfg) && /auto_approve_ranking:\s*true/.test(cfg)) {
    warnings.push({
      code: 'LB_AUTO_APPROVE',
      message: 'Auto-approvazione ranking attiva — verificare soglie rollback'
    });
  }

  const reportPath = path.join(dataDir, 'learning-report.json');
  if (fs.existsSync(reportPath)) {
    try {
      const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));
      if (report.total_events < (report.min_observations || 30)) {
        warnings.push({
          code: 'LB_INSUFFICIENT_DATA',
          message: `Eventi insufficienti (${report.total_events}) per modificare ranking`
        });
      }
    } catch {
      issues.push({ code: 'LB_REPORT_PARSE', message: 'learning-report.json non valido' });
    }
  }

  const evalPath = path.join(dataDir, 'evaluation-latest.json');
  if (fs.existsSync(evalPath)) {
    try {
      const ev = JSON.parse(fs.readFileSync(evalPath, 'utf8'));
      if (ev.rollback_information) {
        warnings.push({
          code: 'LB_ROLLBACK_TRIGGERED',
          message: `Rollback attivo: ${ev.rollback_information.reason}`
        });
      }
    } catch {
      issues.push({ code: 'LB_EVAL_PARSE', message: 'evaluation-latest.json non valido' });
    }
  }

  return { ok: issues.length === 0, issues, warnings };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const r = runLearningBridgePremortem();
  console.log(JSON.stringify(r, null, 2));
  if (!r.ok) process.exitCode = 1;
}
