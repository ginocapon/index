import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";

export const root = process.cwd();
export const base = path.join(root, "righetto-premortem-guardian");
export const memoryDir = path.join(base, "memory");
export const reportsDir = path.join(base, "reports");
export const dataDir = path.join(root, "data");

export function ensureDirs() {
  fs.mkdirSync(memoryDir, { recursive: true });
  fs.mkdirSync(reportsDir, { recursive: true });
}

export function now() {
  return new Date().toISOString();
}

export function event(type, data = {}) {
  ensureDirs();
  fs.appendFileSync(
    path.join(memoryDir, "events.jsonl"),
    JSON.stringify({ time: now(), type, ...data }) + "\n"
  );
}

export function readJson(filePath, fallback = null) {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch {
    return fallback;
  }
}

export function writeJson(filePath, data) {
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

export function readText(filePath) {
  try {
    return fs.readFileSync(filePath, "utf8");
  } catch {
    return null;
  }
}

/** Minimal YAML reader for flat guardian config files (no nested arrays). */
export function readSimpleYaml(filePath) {
  const text = readText(filePath);
  if (!text) return {};
  const out = {};
  let currentKey = null;
  let list = null;

  for (const raw of text.split("\n")) {
    const line = raw.replace(/\r$/, "");
    if (!line.trim() || line.trim().startsWith("#")) continue;

    const listMatch = line.match(/^  - (.+)$/);
    if (listMatch && currentKey) {
      if (!Array.isArray(out[currentKey])) out[currentKey] = [];
      out[currentKey].push(listMatch[1].replace(/^["']|["']$/g, ""));
      continue;
    }

    const kv = line.match(/^([a-zA-Z0-9_-]+):\s*(.*)$/);
    if (!kv) continue;
    const [, key, val] = kv;
    currentKey = key;
    if (val === "") {
      out[key] = {};
      list = null;
    } else if (val.startsWith("[") && val.endsWith("]")) {
      out[key] = val
        .slice(1, -1)
        .split(",")
        .map((s) => s.trim().replace(/^["']|["']$/g, ""))
        .filter(Boolean);
    } else {
      out[key] = val.replace(/^["']|["']$/g, "");
    }
  }
  return out;
}

export function runCommand(cmd, args, opts = {}) {
  const result = spawnSync(cmd, args, {
    cwd: root,
    encoding: "utf8",
    timeout: opts.timeout ?? 300000,
    env: { ...process.env, ...opts.env },
  });
  return {
    ok: result.status === 0,
    status: result.status ?? 1,
    stdout: (result.stdout || "").trim(),
    stderr: (result.stderr || "").trim(),
  };
}

export function parseDurationMs(value) {
  if (!value) return null;
  const m = String(value).match(/^(\d+)(m|h|d)$/);
  if (!m) return null;
  const n = parseInt(m[1], 10);
  if (m[2] === "m") return n * 60 * 1000;
  if (m[2] === "h") return n * 60 * 60 * 1000;
  if (m[2] === "d") return n * 24 * 60 * 60 * 1000;
  return null;
}

export function riskScore(fm) {
  const p = Number(fm.probability ?? 0.3);
  const i = Number(fm.impact ?? 0.5);
  const d = Number(fm.detectability ?? 0.5);
  const c = Number(fm.controllability ?? 0.5);
  const detectionPenalty = 1 + (1 - d);
  const controllabilityPenalty = 1 + (1 - c);
  return p * i * detectionPenalty * controllabilityPenalty;
}

export function statusFromObservations(observations) {
  const critical = observations.filter((o) => o.severity === "critical");
  const warning = observations.filter((o) => o.severity === "warning");
  if (critical.length) return "critical";
  if (warning.length) return "warning";
  return "ok";
}
