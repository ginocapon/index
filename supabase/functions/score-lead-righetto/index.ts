// Righetto — Livello A: scoring deterministico lead su richieste (GDPR: service_role only)
// Deploy: supabase functions deploy score-lead-righetto
// Secrets: SUPABASE_SERVICE_ROLE_KEY (auto), WEBHOOK_SECRET, opz. TELEGRAM_*

import { serve } from "https://deno.land/std@0.177.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type, x-righetto-webhook-secret",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

const HOT = 70;
const WARM = 40;

function cyrb53(str: string, seed = 0): string {
  let h1 = 0xdeadbeef ^ seed,
    h2 = 0x41c6ce57 ^ seed;
  for (let i = 0; i < str.length; i++) {
    const ch = str.charCodeAt(i);
    h1 = Math.imul(h1 ^ ch, 2654435761);
    h2 = Math.imul(h2 ^ ch, 1597334677);
  }
  h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909);
  h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507) ^ Math.imul(h1 ^ (h1 >>> 13), 3266489909);
  return (4294967296 * (2097151 & h2) + (h1 >>> 0)).toString(36);
}

function scoreLead(row: Record<string, unknown>): {
  score: number;
  temperature: string;
  owner_path: string | null;
  dedup_key: string;
} {
  const nome = String(row.nome ?? "");
  const tel = String(row.telefono ?? "").trim();
  const msg = String(row.messaggio ?? "");
  const prov = String(row.provenienza ?? "");
  const blob = `${msg} ${prov}`.toLowerCase();

  let score = 15;
  if (tel.length >= 8) score += 10;
  if (/landing-valutazione|servizio-valutazioni|valutazione/.test(prov)) score += 20;
  if (/vend|incarico|mandato|valut/.test(blob)) score += 25;
  if (/urgent|subito|asap|3 mesi|tre mesi/.test(blob)) score += 15;
  if (/300\.?000|350\.?000|400\.?000|500\.?000|ville|centro storico|pregio/.test(blob)) score += 20;
  if (/non si vende|invendut|annuncio fermo|già in vendita/.test(blob)) score += 15;
  if (/solo curios|tra qualche anno/.test(blob)) score -= 10;

  score = Math.max(0, Math.min(100, score));
  const temperature = score >= HOT ? "hot" : score >= WARM ? "warm" : "cold";

  let owner_path: string | null = null;
  if (/non si vende|invendut|già in vendita|annuncio fermo/.test(blob)) owner_path = "F";
  else if (/quanto vale|valutazione|stima/.test(blob)) owner_path = "A";
  else if (/pens.*vendere|voglio vendere/.test(blob)) owner_path = "B";
  else if (/non so se|indecis/.test(blob)) owner_path = "L";

  const email = String(row.email ?? "").toLowerCase().trim();
  const dedup_key = cyrb53(`${email}|${tel}|${msg.slice(0, 200)}`);

  return { score, temperature, owner_path, dedup_key };
}

async function notifyTelegram(text: string) {
  const token = Deno.env.get("TELEGRAM_BOT_TOKEN");
  const chat = Deno.env.get("TELEGRAM_CHAT_ID");
  if (!token || !chat) return;
  await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: chat, text, parse_mode: "HTML" }),
  });
}

serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });

  const secret = Deno.env.get("WEBHOOK_SECRET") ?? "";
  const got = req.headers.get("x-righetto-webhook-secret") ?? "";
  if (secret && got !== secret) {
    return new Response(JSON.stringify({ error: "unauthorized" }), {
      status: 401,
      headers: { ...cors, "Content-Type": "application/json" },
    });
  }

  let body: { type?: string; record?: Record<string, unknown>; table?: string };
  try {
    body = await req.json();
  } catch {
    return new Response(JSON.stringify({ error: "invalid json" }), {
      status: 400,
      headers: { ...cors, "Content-Type": "application/json" },
    });
  }

  const row = (body.record ?? body) as Record<string, unknown>;
  const id = row.id as string | undefined;
  if (!id) {
    return new Response(JSON.stringify({ error: "missing record.id" }), {
      status: 400,
      headers: { ...cors, "Content-Type": "application/json" },
    });
  }

  const supabase = createClient(
    Deno.env.get("SUPABASE_URL") ?? "",
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "",
  );

  const { score, temperature, owner_path, dedup_key } = scoreLead(row);

  const { data: dup } = await supabase
    .from("richieste")
    .select("id")
    .eq("dedup_key", dedup_key)
    .neq("id", id)
    .maybeSingle();

  if (dup) {
    return new Response(JSON.stringify({ ok: true, duplicate: true, dedup_key }), {
      headers: { ...cors, "Content-Type": "application/json" },
    });
  }

  const { error } = await supabase
    .from("richieste")
    .update({
      lead_score: score,
      lead_temperature: temperature,
      owner_path,
      dedup_key,
      scored_at: new Date().toISOString(),
      lead_stage: row.lead_stage ?? "ricevuto",
    })
    .eq("id", id);

  if (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { ...cors, "Content-Type": "application/json" },
    });
  }

  await supabase.from("lead_events").insert({
    richiesta_id: id,
    evento: "ricevuto",
    note: `score=${score} temp=${temperature} path=${owner_path ?? "-"}`,
    created_by: "score-lead-righetto",
  });

  if (temperature === "hot") {
    const nome = String(row.nome ?? "");
    const tel = String(row.telefono ?? "");
    await notifyTelegram(
      `<b>Lead HOT (${score}/100)</b>\n${nome}\nTel: ${tel}\nProvenienza: ${row.provenienza ?? "-"}\nPercorso: ${owner_path ?? "?"}`,
    );
  }

  return new Response(
    JSON.stringify({ ok: true, score, temperature, owner_path, dedup_key }),
    { headers: { ...cors, "Content-Type": "application/json" } },
  );
});
