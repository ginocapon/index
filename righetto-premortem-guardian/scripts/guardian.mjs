#!/usr/bin/env node
/**
 * Righetto Premortem Guardian — single entry point dispatcher.
 * CONTEXT → OBSERVE → VERIFY → ASSUMPTIONS → PREMORTEM → FAILURE MODES →
 * PRIORITIZE → ACT → VERIFY AGAIN → LEARN → NEXT CHECK
 */

import fs from "node:fs";
import path from "node:path";
import { runAdapters } from "../adapters/registry.mjs";
import { dispatchJobs, getJobScopes, markJobsRan } from "../lib/cron-dispatch.mjs";
import { filterExecutableActions } from "../lib/policy.mjs";
import {
  base,
  ensureDirs,
  event,
  now,
  readSimpleYaml,
  reportsDir,
  riskScore,
  statusFromObservations,
  writeJson,
} from "../lib/utils.mjs";

function parseArgs(argv) {
  const opts = { command: "run", forceJobs: [], forceAll: false, ingestOnly: false };
  const args = [...argv];
  opts.command = args[0] || "run";
  for (let i = 1; i < args.length; i++) {
    if (args[i] === "--force=all") opts.forceAll = true;
    if (args[i] === "--ingest-only") opts.ingestOnly = true;
    if (args[i]?.startsWith("--jobs=")) {
      opts.forceJobs = args[i].slice(7).split(",").map((s) => s.trim()).filter(Boolean);
    }
  }
  return opts;
}

function buildContext(config) {
  return {
    objective: "Salute operativa righettoimmobiliare.it — anticipare, rilevare, contenere, correggere",
    system: "Righetto Immobiliare — GitHub Pages + Supabase + cPanel relay",
    constraints: ["vanilla stack", "no CDN esterni", "autonomy policy", "no invented data"],
    categories: config.categories || [],
    timestamp: now(),
  };
}

function buildAssumptions(verifiedFacts, missing) {
  const assumptions = [
    {
      id: "a-github-pages",
      statement: "GitHub Pages serve il sito senza errori di build",
      confidence: 0.85,
      evidence: verifiedFacts.some((f) => f.fact === "url_probe_issues"),
    },
    {
      id: "a-supabase",
      statement: "Supabase REST risponde per catalogo e lead",
      confidence: missing.some((m) => m.includes("SUPABASE")) ? 0.4 : 0.8,
      test: "guardian-leads-snapshot con SUPABASE_KEY",
    },
    {
      id: "a-analytics",
      statement: "GA4/GSC snapshot riflette il traffico reale",
      confidence: missing.some((m) => m.includes("GA4")) ? 0.5 : 0.7,
      test: "append-analytics-snapshot manuale o GA4 Data API",
    },
  ];
  return assumptions;
}

function buildPremortem(assumptions, observations) {
  const causes = [];
  if (observations.some((o) => o.category === "availability")) {
    causes.push("URL critici offline o redirect errati non rilevati prima del deploy");
  }
  if (observations.some((o) => o.category === "leads")) {
    causes.push("Lead persi: form OK ma email relay o Edge Function fallisce silenziosamente");
  }
  if (observations.some((o) => o.category === "security")) {
    causes.push("Segreto esposto o RLS misconfigurato — accesso dati non autorizzato");
  }
  assumptions.filter((a) => a.confidence < 0.6).forEach((a) => {
    causes.push(`Assunzione debole: ${a.statement}`);
  });
  if (!causes.length) {
    causes.push("Monitoraggio frammentato — issue rilevata solo dal cliente");
  }
  return causes;
}

function buildFailureModes(premortemCauses, observations) {
  const modes = [];
  for (const cause of premortemCauses) {
    modes.push({
      event: cause.slice(0, 80),
      cause,
      consequence: "Conversione, reputazione o dati compromessi",
      probability: 0.35,
      impact: 0.7,
      detectability: observations.length ? 0.75 : 0.4,
      controllability: 0.6,
      early_signals: observations.slice(0, 2).map((o) => o.message),
      risk_score: 0,
    });
  }
  for (const m of modes) m.risk_score = riskScore(m);
  return modes.sort((a, b) => b.risk_score - a.risk_score);
}

function buildActions(failureModes, observations) {
  const actions = [
    { type: "generate_report", description: "Report Guardian machine + human", autonomy_override: "allow" },
  ];
  if (observations.some((o) => o.severity === "critical")) {
    actions.push({
      type: "create_alert",
      description: "Segnalare osservazioni critical nel report Guardian",
      autonomy_override: "allow",
    });
  }
  for (const fm of failureModes.slice(0, 3)) {
    actions.push({
      type: "modify_content",
      description: `Remediation proposta: ${fm.cause}`,
      proposed: true,
    });
  }
  return filterExecutableActions(actions);
}

function buildNextChecks(jobs, failureModes) {
  const checks = [];
  for (const j of jobs) {
    checks.push({ job: j, when: "next scheduled interval", threshold: "no new critical observations" });
  }
  for (const fm of failureModes.slice(0, 2)) {
    checks.push({ check: fm.event, threshold: "risk_score < 0.3", automate: false });
  }
  return checks;
}

function buildLearnings(observations, actions) {
  const learnings = [];
  if (observations.length) {
    learnings.push({
      incident: "observations_recorded",
      count: observations.length,
      new_rule: "Ripetere controllo con doppio segnale per eventi critical",
    });
  }
  const blocked = actions.filter((a) => !a.executed && a.approval !== "none");
  if (blocked.length) {
    learnings.push({
      incident: "actions_need_approval",
      items: blocked.map((a) => a.description),
      new_rule: "YELLOW/RED — approvazione umana prima di publish",
    });
  }
  return learnings;
}

async function runGuardian(opts) {
  ensureDirs();
  const configPath = path.join(base, "config", "guardian.yaml");
  const config = readSimpleYaml(configPath);

  const jobs = dispatchJobs(opts);
  const scopes = getJobScopes(jobs);

  event("guardian_start", { jobs, scopes, ingestOnly: opts.ingestOnly });

  const context = buildContext(config);

  const adapterResults = await runAdapters(scopes, {
    ingestOnly: opts.ingestOnly,
    jobs,
    scopes,
  });

  const observations = adapterResults.flatMap((r) => r.observations || []);
  const verified_facts = adapterResults.flatMap((r) => r.verified_facts || []);
  const missing_integrations = [...new Set(adapterResults.flatMap((r) => r.missing_integrations || []))];

  const assumptions = buildAssumptions(verified_facts, missing_integrations);
  const premortem_causes = buildPremortem(assumptions, observations);
  const failure_modes = buildFailureModes(premortem_causes, observations);
  const signals = observations.map((o) => ({ signal: o.message, severity: o.severity, category: o.category }));
  const actions = buildActions(failure_modes, observations);
  const verification = [
    { check: "reports_written", expected: true },
    { check: "no_auto_publish", expected: true, note: "solo GREEN eseguito" },
    { check: "observations_count", value: observations.length },
  ];
  const learnings = buildLearnings(observations, actions);
  const next_checks = buildNextChecks(jobs, failure_modes);
  const human_approval_required = actions.filter((a) => a.approval && a.approval !== "none").map((a) => a.description);

  const status = statusFromObservations(observations);

  const result = {
    status,
    objective: context.objective,
    timestamp: context.timestamp,
    jobs_executed: jobs,
    scopes_executed: scopes,
    sequence: config.sequence || [],
    context,
    observations,
    verified_facts,
    assumptions,
    premortem_causes,
    failure_modes,
    signals,
    actions,
    verification,
    learnings,
    next_checks,
    human_approval_required,
    missing_integrations,
    mode: opts.ingestOnly ? "ingest-only" : "live-adapters",
  };

  const jsonPath = path.join(reportsDir, "guardian-latest.json");
  const mdPath = path.join(reportsDir, "guardian-latest.md");

  writeJson(jsonPath, result);

  const md = [
    "# Guardian Report — Righetto Immobiliare",
    "",
    `- **Status:** ${status}`,
    `- **Time:** ${result.timestamp}`,
    `- **Jobs:** ${jobs.join(", ")}`,
    `- **Scopes:** ${scopes.join(", ")}`,
    `- **Mode:** ${result.mode}`,
    "",
    "## Osservazioni",
    observations.length
      ? observations.map((o) => `- [${o.severity}] ${o.category}: ${o.message}`).join("\n")
      : "- Nessuna osservazione critica",
    "",
    "## Failure modes (top 3)",
    failure_modes.slice(0, 3).map((f) => `- ${f.cause} (risk ${f.risk_score.toFixed(3)})`).join("\n") || "- n/a",
    "",
    "## Integrazioni mancanti",
    missing_integrations.map((m) => `- ${m}`).join("\n") || "- n/a",
    "",
    "## Approvazione umana richiesta",
    human_approval_required.map((h) => `- ${h}`).join("\n") || "- n/a",
    "",
    "## Next checks",
    next_checks.map((c) => `- ${JSON.stringify(c)}`).join("\n"),
    "",
    "_Sequenza: CONTEXT → OBSERVE → VERIFY → ASSUMPTIONS → PREMORTEM → FAILURE MODES → PRIORITIZE → ACT → VERIFY AGAIN → LEARN → NEXT CHECK_",
  ].join("\n");

  fs.writeFileSync(mdPath, md);

  markJobsRan(jobs);
  event("guardian_run", { status, jobs, observations: observations.length });

  console.log(`Guardian status: ${status}`);
  console.log(`Jobs: ${jobs.join(", ")}`);
  console.log(`Report: righetto-premortem-guardian/reports/guardian-latest.md`);
  if (status !== "ok") process.exitCode = 1;
}

function doctor() {
  ensureDirs();
  const required = [
    "README.md",
    "ONE_COMMAND.md",
    "AGENT.md",
    "config/guardian.yaml",
    "config/cron-matrix.yaml",
    "policy/autonomy.yaml",
    "sequences/master-sequence.md",
    "skill/SKILL.md",
    "adapters/registry.mjs",
    "lib/cron-dispatch.mjs",
  ];

  const missing = required.filter((f) => !fs.existsSync(path.join(base, f)));
  console.log("Righetto Guardian Doctor");
  console.log(missing.length ? "FAIL" : "OK");
  if (missing.length) {
    console.log("Missing:");
    missing.forEach((x) => console.log(`- ${x}`));
    process.exitCode = 1;
  }
}

function printSequence() {
  console.log(`
RIGHETTO PREMORTEM GUARDIAN

CONTEXT → OBSERVE → VERIFY → ASSUMPTIONS → PREMORTEM → FAILURE MODES →
PRIORITIZE → ACT → VERIFY AGAIN → LEARN → NEXT CHECK
`);
}

const opts = parseArgs(process.argv.slice(2));
const cmd = opts.command;

if (cmd === "run") runGuardian(opts);
else if (cmd === "doctor") doctor();
else if (cmd === "sequence") printSequence();
else if (cmd === "init") {
  ensureDirs();
  console.log("Guardian initialized. Run: node righetto-premortem-guardian/scripts/guardian.mjs run");
} else {
  console.log("Usage: guardian.mjs [run|doctor|sequence|init] [--jobs=name,...] [--force=all] [--ingest-only]");
  process.exitCode = 1;
}
