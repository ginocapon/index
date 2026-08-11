import fs from "node:fs";
import path from "node:path";
import {
  root,
  dataDir,
  readJson,
  readText,
  runCommand,
} from "../lib/utils.mjs";

function obs(id, category, message, severity = "info", evidence = {}) {
  return { id, category, message, severity, evidence, time: new Date().toISOString() };
}

function ingestJson(relPath, maxAgeMs = 6 * 60 * 60 * 1000) {
  const p = path.join(root, relPath);
  if (!fs.existsSync(p)) return { available: false, path: relPath };
  const stat = fs.statSync(p);
  const age = Date.now() - stat.mtimeMs;
  const data = readJson(p);
  return { available: true, path: relPath, age_ms: age, fresh: age <= maxAgeMs, data };
}

async function availabilityAdapter(ctx) {
  const out = { observations: [], verified_facts: [], missing_integrations: [] };
  let ran = false;

  if (!ctx.ingestOnly) {
    const probe = runCommand("python3", ["scripts/probe_live_urls.py"]);
    ran = true;
    if (!probe.ok) {
      out.observations.push(obs("avail-probe-fail", "availability", "probe_live_urls.py fallito", "warning", { stderr: probe.stderr }));
    }
  }

  const probeData = ingestJson("data/url-probe-latest.json", ctx.ingestOnly ? Infinity : 2 * 60 * 60 * 1000);
  if (probeData.available && probeData.data) {
    const bad = probeData.data.filter((r) => r.status >= 400 || r.status < 0);
    out.verified_facts.push({ fact: "url_probe_count", value: probeData.data.length });
    out.verified_facts.push({ fact: "url_probe_issues", value: bad.length });
    if (bad.length) {
      out.observations.push(
        obs("avail-url-bad", "availability", `${bad.length} URL con status errato`, bad.length > 3 ? "critical" : "warning", { sample: bad.slice(0, 5) })
      );
    }
  } else if (!ran) {
    out.missing_integrations.push("url_probe — eseguire probe_live_urls.py");
  }

  const api = runCommand("curl", ["-s", "-o", "/dev/null", "-w", "%{http_code}", "-I", "https://api.righettoimmobiliare.it/send-mail.php"], { timeout: 20000 });
  const code = parseInt(api.stdout, 10);
  if (code === 405 || code === 200) {
    out.verified_facts.push({ fact: "api_relay_reachable", value: true, http: code });
  } else {
    out.observations.push(obs("avail-api", "api", `API relay HTTP ${api.stdout || "error"}`, "warning"));
  }

  return out;
}

async function leadsAdapter(ctx) {
  const out = { observations: [], verified_facts: [], missing_integrations: [] };

  if (!ctx.ingestOnly) {
    const snap = runCommand("python3", ["scripts/guardian-leads-snapshot.py"], {
      env: { SUPABASE_KEY: process.env.SUPABASE_KEY || "" },
    });
    if (!snap.ok) {
      out.observations.push(obs("leads-snap-fail", "leads", "guardian-leads-snapshot.py fallito", "warning", { stderr: snap.stderr }));
    }
  }

  const data = ingestJson("data/guardian-leads-latest.json", Infinity);
  if (data.available && data.data) {
    out.verified_facts.push(...(data.data.facts || []));
    if (data.data.unread_count > 50) {
      out.observations.push(obs("leads-unread", "leads", `${data.data.unread_count} richieste non lette`, "warning"));
    }
    if (!data.data.available) {
      out.missing_integrations.push(data.data.reason || "Supabase leads — SUPABASE_KEY non configurato");
    }
  } else {
    out.missing_integrations.push("leads snapshot — data/guardian-leads-latest.json");
  }

  const formJs = path.join(root, "js/rig-lead-form.js");
  if (fs.existsSync(formJs)) {
    const txt = readText(formJs);
    if (txt && txt.includes("sendNotifica") && txt.includes("richieste")) {
      out.verified_facts.push({ fact: "lead_form_module", value: "rig-lead-form.js OK" });
    } else {
      out.observations.push(obs("leads-form", "forms", "rig-lead-form.js incompleto", "critical"));
    }
  }

  return out;
}

async function seoAdapter(ctx) {
  const out = { observations: [], verified_facts: [], missing_integrations: [] };

  if (!ctx.ingestOnly && ctx.scopes.includes("seo")) {
    runCommand("bash", ["scripts/mini-seo-check.sh", "mini-seo-report.md"]);
    runCommand("python3", ["scripts/google-compliance-check.py"]);
  }

  const mini = ingestJson("mini-seo-report.md", Infinity);
  if (mini.available) {
    const txt = readText(path.join(root, "mini-seo-report.md"));
    const errMatch = txt?.match(/Errori:\s*(\d+)/i);
    const warnMatch = txt?.match(/Avvisi:\s*(\d+)/i);
    if (errMatch) {
      const errors = parseInt(errMatch[1], 10);
      out.verified_facts.push({ fact: "mini_seo_errors", value: errors });
      if (errors > 0) out.observations.push(obs("seo-errors", "seo", `${errors} errori mini-seo-check`, "critical"));
    }
    if (warnMatch) out.verified_facts.push({ fact: "mini_seo_warnings", value: parseInt(warnMatch[1], 10) });
  }

  const geo = ingestJson("data/geo-ai-audit-latest.json", 24 * 60 * 60 * 1000);
  if (geo.available && geo.data?.issues?.length) {
    out.observations.push(obs("seo-geo", "seo", `${geo.data.issues.length} issue GEO/AI audit`, "warning", { issues: geo.data.issues.slice(0, 3) }));
  }

  return out;
}

async function contentAdapter(ctx) {
  const out = { observations: [], verified_facts: [], missing_integrations: [] };

  if (!ctx.ingestOnly) {
  const dup = runCommand("python3", ["scripts/check_doppioni_sito.py"]);
    if (dup.stdout.includes("DOPPIONI") || dup.stdout.includes("doppion")) {
      out.observations.push(obs("content-dup", "content", "Possibili doppioni blog rilevati", "warning", { excerpt: dup.stdout.slice(0, 500) }));
    }
  }

  const editorial = ingestJson("data/editorial-queue.json", Infinity);
  if (editorial.available) {
    const scheduled = (editorial.data?.items || editorial.data?.queue || []).filter?.((i) => i.status === "scheduled") || [];
    out.verified_facts.push({ fact: "editorial_scheduled", value: scheduled.length || editorial.data?.scheduled?.length || 0 });
  }

  return out;
}

async function securityAdapter(ctx) {
  const out = { observations: [], verified_facts: [], missing_integrations: [] };

  if (!ctx.ingestOnly) {
    runCommand("bash", ["scripts/security-check.sh", "security-report.md"]);
  }

  const sec = readText(path.join(root, "security-report.md"));
  if (sec) {
    const errs = (sec.match(/❌/g) || []).length;
    const warns = (sec.match(/⚠️/g) || []).length;
    out.verified_facts.push({ fact: "security_errors", value: errs });
    out.verified_facts.push({ fact: "security_warnings", value: warns });
    if (errs > 0) out.observations.push(obs("sec-err", "security", `${errs} errori security-check`, "critical"));
    else if (warns > 3) out.observations.push(obs("sec-warn", "security", `${warns} avvisi security-check`, "warning"));
  }

  if (!process.env.SUPABASE_KEY) {
    out.missing_integrations.push("RLS probe — tools/check_rls_exposure.py richiede righetto_social/.env locale");
  }

  return out;
}

async function aiQualityAdapter(ctx) {
  const out = { observations: [], verified_facts: [], missing_integrations: [] };

  if (!ctx.ingestOnly) {
    const audit = runCommand("python3", ["scripts/audit_chatbot_faq.py"]);
    if (!audit.ok || audit.stdout.toLowerCase().includes("fail")) {
      out.observations.push(obs("ai-faq", "ai_quality", "audit_chatbot_faq segnala problemi", "warning", { excerpt: audit.stdout.slice(0, 400) }));
    } else {
      out.verified_facts.push({ fact: "chatbot_faq_audit", value: "ok" });
    }
  }

  const chatbot = path.join(root, "js/chatbot.js");
  if (fs.existsSync(chatbot)) {
    out.verified_facts.push({ fact: "linda_chatbot", value: "js/chatbot.js presente (rules-based)" });
  }

  return out;
}

async function analyticsAdapter(ctx) {
  const out = { observations: [], verified_facts: [], missing_integrations: [] };

  const dash = ingestJson("data/analytics-dashboard.json", Infinity);
  if (dash.available) {
    out.verified_facts.push({ fact: "analytics_snapshot", value: "data/analytics-dashboard.json", updated: dash.age_ms });
  } else {
    out.missing_integrations.push("GA4 Data API — solo snapshot manuale append-analytics-snapshot.yml");
  }

  const ga = ingestJson("data/ga-consent-verify-latest.json", 7 * 24 * 60 * 60 * 1000);
  if (!ctx.ingestOnly && !ga.fresh) {
    runCommand("python3", ["scripts/verify_ga_consent_live.py"]);
  }
  const ga2 = ingestJson("data/ga-consent-verify-latest.json", Infinity);
  if (ga2.available && ga2.data?.ok === false) {
    out.observations.push(obs("analytics-consent", "analytics", "GA consent verify non OK", "warning", ga2.data));
  }

  out.missing_integrations.push("Search Console API — dati in data/gsc-*.json manuali");

  return out;
}

async function databaseAdapter(ctx) {
  const out = { observations: [], verified_facts: [], missing_integrations: [] };

  const manifest = ingestJson("data/media-manifest.json", Infinity);
  if (manifest.available) {
    const count = manifest.data?.immobili?.length ?? manifest.data?.count ?? Object.keys(manifest.data || {}).length;
    out.verified_facts.push({ fact: "media_manifest_entries", value: count });
  }

  if (process.env.SUPABASE_KEY && !ctx.ingestOnly) {
    const verify = runCommand("python3", ["scripts/verify_media_migration.py"], {
      env: { SUPABASE_KEY: process.env.SUPABASE_KEY },
      timeout: 120000,
    });
    if (!verify.ok) {
      out.observations.push(obs("db-media", "database", "verify_media_migration fallito", "warning", { stderr: verify.stderr.slice(0, 300) }));
    }
  } else {
    out.missing_integrations.push("Media migration verify — richiede SUPABASE_KEY");
  }

  out.missing_integrations.push("Backup Supabase — verifica manuale dashboard, no script automatizzato");

  return out;
}

async function performanceAdapter(ctx) {
  const out = { observations: [], verified_facts: [], missing_integrations: [] };

  if (!ctx.ingestOnly) {
    runCommand("python3", ["scripts/audit_geo_ai_postdeploy.py"]);
  }

  const geo = ingestJson("data/geo-ai-audit-latest.json", Infinity);
  if (geo.available) {
    out.verified_facts.push({ fact: "geo_ai_audit", value: geo.data?.status || "present" });
  }

  out.missing_integrations.push("Lighthouse/CWV — non presente in repo");

  return out;
}

async function businessAdapter(ctx) {
  const out = { observations: [], verified_facts: [], missing_integrations: [] };

  const gsc = ingestJson("data/gsc-keywords-priority.json", Infinity);
  if (gsc.available) {
    out.verified_facts.push({ fact: "gsc_priority_keywords", value: (gsc.data?.keywords || gsc.data).length ?? "n/a" });
  }

  out.missing_integrations.push("Social heartbeat — righetto_social su Windows, non GHA");

  return out;
}

async function weeklyAuditAdapter(ctx) {
  const out = { observations: [], verified_facts: [], missing_integrations: [] };

  if (!ctx.ingestOnly) {
    const audit = runCommand("bash", ["scripts/audit-skill.sh", "audit-report.md"], { timeout: 600000 });
    if (!audit.ok) {
      out.observations.push(obs("audit-skill", "business", "audit-skill.sh con errori", "warning"));
    }
  }

  const report = readText(path.join(root, "audit-report.md"));
  if (report) {
    const health = report.match(/Salute:\s*(\d+)%/);
    if (health) out.verified_facts.push({ fact: "audit_health_pct", value: parseInt(health[1], 10) });
  }

  return out;
}

const ADAPTERS = {
  availability: availabilityAdapter,
  api: availabilityAdapter,
  workers: availabilityAdapter,
  leads: leadsAdapter,
  forms: leadsAdapter,
  conversion: leadsAdapter,
  seo: seoAdapter,
  structured_data: seoAdapter,
  links: seoAdapter,
  content: contentAdapter,
  security: securityAdapter,
  ai_quality: aiQualityAdapter,
  analytics: analyticsAdapter,
  database: databaseAdapter,
  performance: performanceAdapter,
  business: businessAdapter,
  competition: businessAdapter,
  strategy: businessAdapter,
  assumptions: securityAdapter,
  technology: businessAdapter,
};

export async function runAdapters(scopes, ctx) {
  const results = [];
  const seen = new Set();

  for (const scope of scopes) {
    const fn = ADAPTERS[scope];
    if (!fn || seen.has(fn)) continue;
    seen.add(fn);
    try {
      const r = await fn({ ...ctx, scopes });
      results.push({ scope, ...r });
    } catch (e) {
      results.push({
        scope,
        observations: [obs(`adapter-${scope}`, scope, `Adapter error: ${e.message}`, "warning")],
        verified_facts: [],
        missing_integrations: [],
      });
    }
  }

  if (ctx.jobs?.includes("weekly_audit") || ctx.jobs?.includes("monthly_full_premortem")) {
    const r = await weeklyAuditAdapter(ctx);
    results.push({ scope: "weekly_audit", ...r });
  }

  return results;
}
