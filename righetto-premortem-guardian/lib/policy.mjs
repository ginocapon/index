import path from "node:path";
import { base, readSimpleYaml } from "./utils.mjs";

const policyPath = path.join(base, "policy", "autonomy.yaml");

const DEFAULT = {
  green: { allowed: true, approval: "none" },
  yellow: { allowed: true, approval: "human_before_publish" },
  red: { allowed: false, approval: "explicit_human" },
  black: { allowed: false, approval: "impossible" },
};

export function loadPolicy() {
  const raw = readSimpleYaml(policyPath);
  return { levels: DEFAULT, examples: raw.examples || {} };
}

export function classifyAction(actionType) {
  const GREEN = new Set([
    "generate_report",
    "create_alert",
    "retry_failed_job",
    "refresh_cache",
  ]);
  if (GREEN.has(actionType)) return "green";

  const { examples } = loadPolicy();
  for (const [level, list] of Object.entries(examples)) {
    if (Array.isArray(list) && list.includes(actionType)) return level;
  }
  return "yellow";
}

export function planAction(action) {
  const level = classifyAction(action.type);
  const meta = DEFAULT[level] || DEFAULT.yellow;
  return {
    ...action,
    autonomy_level: level,
    allowed: meta.allowed && action.autonomy_override !== "deny",
    approval: meta.approval,
    executed: false,
    reason: meta.allowed ? null : "blocked_by_policy",
  };
}

export function filterExecutableActions(actions) {
  return actions
    .map(planAction)
    .map((a) => {
      if (a.autonomy_level === "green" && a.type === "generate_report") {
        return { ...a, executed: true };
      }
      if (a.autonomy_level === "green" && a.type === "create_alert") {
        return { ...a, executed: true };
      }
      return a;
    });
}
