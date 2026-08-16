#!/usr/bin/env node

/**
 * Righetto Premortem Guardian — single command dispatcher.
 *
 * It is intentionally dependency-light. Real site adapters can be connected
 * later without changing the cognitive sequence.
 */

import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { runLearningBridgePremortem } from "../learning-bridge/engines/premortem-checks.mjs";

const root = process.cwd();
const base = path.join(root, "righetto-premortem-guardian");
const configPath = path.join(base, "config", "guardian.yaml");
const memoryDir = path.join(base, "memory");
const reportsDir = path.join(base, "reports");

function ensure() {
  fs.mkdirSync(memoryDir, { recursive: true });
  fs.mkdirSync(reportsDir, { recursive: true });
}

function now() {
  return new Date().toISOString();
}

function event(type, data = {}) {
  ensure();
  fs.appendFileSync(
    path.join(memoryDir, "events.jsonl"),
    JSON.stringify({ time: now(), type, ...data }) + "\n"
  );
}

function printSequence() {
  console.log(`
RIGHETTO PREMORTEM GUARDIAN

CONTEXT
  ↓
OBSERVE
  ↓
VERIFY
  ↓
ASSUMPTIONS
  ↓
PREMORTEM
  ↓
FAILURE MODES
  ↓
PRIORITIZE
  ↓
ACT
  ↓
VERIFY AGAIN
  ↓
LEARN
  ↓
NEXT CHECK
`);
}

function runLearningBridgeJob(jobName) {
  const script = path.join(base, "learning-bridge", "run.mjs");
  if (!fs.existsSync(script)) {
    console.error("Learning Bridge run.mjs not found");
    process.exitCode = 1;
    return null;
  }
  const r = spawnSync(process.execPath, [script, jobName], {
    cwd: root,
    encoding: "utf8",
    stdio: "inherit"
  });
  event("learning_bridge_job", { job: jobName, status: r.status });
  return r.status === 0;
}

function run() {
  ensure();

  const lbPremortem = runLearningBridgePremortem();
  const lbIssues = [...(lbPremortem.issues || []), ...(lbPremortem.warnings || [])];

  const result = {
    status: lbPremortem.ok ? "ok" : "warn",
    timestamp: now(),
    sequence: [
      "context",
      "observe",
      "verify",
      "assumptions",
      "premortem",
      "failure_modes",
      "prioritize",
      "act",
      "verify_again",
      "learn",
      "next_check"
    ],
    mode: "dispatcher-ready",
    learning_bridge: lbPremortem,
    note:
      "Core sequence loaded. LINDA Learning Bridge premortem integrato. Ranking live non modificato se apply_ranking_changes=false."
  };

  if (lbIssues.length) {
    result.note += ` Learning Bridge checks: ${lbIssues.length}.`;
  }

  fs.writeFileSync(
    path.join(reportsDir, "guardian-latest.json"),
    JSON.stringify(result, null, 2)
  );

  fs.writeFileSync(
    path.join(reportsDir, "guardian-latest.md"),
    `# Guardian Report\n\n- Status: ${result.status}\n- Time: ${result.timestamp}\n- Mode: ${result.mode}\n\nSequence executed: ${result.sequence.join(" → ")}\n\n${result.note}\n`
  );

  event("guardian_run", result);
  printSequence();
  console.log("Guardian run completed.");
  console.log(`Report: ${path.relative(root, path.join(reportsDir, "guardian-latest.md"))}`);
}

function doctor() {
  ensure();
  const required = [
    "README.md",
    "ONE_COMMAND.md",
    "AGENT.md",
    "config/guardian.yaml",
    "config/cron-matrix.yaml",
    "policy/autonomy.yaml",
    "sequences/master-sequence.md",
    "skill/SKILL.md"
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

const command = process.argv[2] || "run";
const subJob = process.argv[3];

if (command === "run") run();
else if (command === "doctor") doctor();
else if (command === "sequence") printSequence();
else if (command === "learning") {
  const job = subJob || "collect";
  const ok = runLearningBridgeJob(job);
  if (!ok) process.exitCode = 1;
} else {
  console.log("Usage: guardian.mjs [run|doctor|sequence|learning <collect|daily|weekly|biweekly|monthly|full>]");
  process.exitCode = 1;
}
