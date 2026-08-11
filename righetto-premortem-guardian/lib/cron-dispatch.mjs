import fs from "node:fs";
import path from "node:path";
import {
  base,
  memoryDir,
  readJson,
  writeJson,
  readSimpleYaml,
  parseDurationMs,
  now,
} from "./utils.mjs";

const statePath = path.join(memoryDir, "state.json");
const matrixPath = path.join(base, "config", "cron-matrix.yaml");

const JOB_SCOPES = {
  heartbeat: ["availability", "api", "workers"],
  transaction_sentinel: ["leads", "forms", "conversion"],
  anomaly_engine: ["analytics", "seo", "business", "performance"],
  ai_quality: ["ai_quality"],
  site_integrity: ["seo", "performance", "structured_data", "links"],
  content_freshness: ["content", "seo"],
  daily_premortem: ["all"],
  weekly_strategy: ["business", "seo", "content", "competition", "web_keywords"],
  web_keyword_discovery: ["content", "seo", "business", "web_keywords"],
  linda_faq_discovery: ["ai_quality", "content"],
  weekly_red_team: ["strategy", "assumptions", "business", "security"],
  monthly_full_premortem: ["all"],
  quarterly_future_scenarios: ["strategy", "business", "technology"],
  security_check: ["security"],
  weekly_audit: ["all"],
};

function loadMatrixJobs() {
  const raw = readSimpleYaml(matrixPath);
  const jobs = raw.jobs || {};
  if (typeof jobs !== "object" || !Object.keys(jobs).length) {
    return {
      heartbeat: { every: "5m" },
      transaction_sentinel: { every: "15m" },
      anomaly_engine: { every: "1h" },
      ai_quality: { every: "4h" },
      site_integrity: { every: "4h" },
      content_freshness: { every: "1d" },
      daily_premortem: { at: "18:00" },
      weekly_strategy: { on: "monday", at: "08:00" },
      weekly_red_team: { on: "friday", at: "17:00" },
      monthly_full_premortem: { day: 1, at: "08:00" },
      quarterly_future_scenarios: { months: [1, 4, 7, 10], day: 1, at: "08:00" },
    };
  }
  return jobs;
}

function dayName(d) {
  return ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"][d.getDay()];
}

function isScheduledNow(jobName, cfg, date = new Date()) {
  const at = cfg.at || "08:00";
  const [hh, mm] = at.split(":").map((x) => parseInt(x, 10));
  const hourMatch = date.getHours() === hh;
  const minuteMatch = date.getMinutes() < 15;

  if (cfg.every) {
    const ms = parseDurationMs(cfg.every);
    if (!ms) return false;
    const state = readJson(statePath, { last_run: {} });
    const last = state.last_run?.[jobName];
    if (!last) return true;
    return Date.now() - new Date(last).getTime() >= ms;
  }

  if (cfg.on && dayName(date) !== String(cfg.on).toLowerCase()) return false;
  if (cfg.day && date.getDate() !== parseInt(cfg.day, 10)) return false;
  if (cfg.months) {
    const months = Array.isArray(cfg.months) ? cfg.months : String(cfg.months).split(",").map((x) => parseInt(x.trim(), 10));
    if (!months.includes(date.getMonth() + 1)) return false;
  }

  if (cfg.at) return hourMatch && minuteMatch;
  return false;
}

export function scopesForJobs(jobNames) {
  const scopes = new Set();
  for (const name of jobNames) {
    const list = JOB_SCOPES[name] || [];
    for (const s of list) {
      if (s === "all") {
        ["availability", "leads", "database", "api", "seo", "content", "performance", "ai_quality", "analytics", "security", "business"].forEach((x) => scopes.add(x));
      } else scopes.add(s);
    }
  }
  return [...scopes];
}

export function dispatchJobs(options = {}) {
  const forceJobs = options.forceJobs || [];
  const forceAll = options.forceAll || false;
  const matrix = loadMatrixJobs();

  if (forceAll) {
    return Object.keys(JOB_SCOPES);
  }

  if (forceJobs.length) {
    return forceJobs.filter((j) => JOB_SCOPES[j] || j === "ingest_only");
  }

  const due = [];
  for (const [name, cfg] of Object.entries(matrix)) {
    if (typeof cfg !== "object") continue;
    if (isScheduledNow(name, cfg)) due.push(name);
  }

  if (!due.length) {
    due.push("heartbeat");
  }

  return due;
}

export function markJobsRan(jobNames) {
  const state = readJson(statePath, { last_run: {}, version: 1 });
  const t = now();
  for (const j of jobNames) state.last_run[j] = t;
  fs.mkdirSync(memoryDir, { recursive: true });
  writeJson(statePath, state);
}

export function getJobScopes(jobNames) {
  return scopesForJobs(jobNames);
}
