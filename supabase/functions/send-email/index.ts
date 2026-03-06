// ═══════════════════════════════════════════════════════════════
// RIGHETTO IMMOBILIARE — Email Sending Edge Function
// Invia email via PHP relay sul tuo cPanel — Zero servizi esterni
// Deploy: supabase functions deploy send-email
// Secrets necessari su Supabase:
//   MAIL_RELAY_URL = https://righetto-immobiliare.it/api/send-mail.php
//   MAIL_RELAY_KEY = RighettoMail2026!SecretKey  (stessa del PHP)
// ═══════════════════════════════════════════════════════════════

import { serve } from "https://deno.land/std@0.177.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS, GET",
};

// ═══ INVIO VIA PHP RELAY (tuo cPanel) ═══
async function sendViaRelay(options: {
  action: string;
  to_email: string;
  to_name?: string;
  sender_email: string;
  sender_name?: string;
  subject: string;
  html_body: string;
  reply_to?: string;
}) {
  const RELAY_URL = Deno.env.get("MAIL_RELAY_URL");
  const RELAY_KEY = Deno.env.get("MAIL_RELAY_KEY");

  if (!RELAY_URL || !RELAY_KEY) {
    throw new Error(
      "MAIL_RELAY_URL o MAIL_RELAY_KEY non configurati. " +
      "Vai su Supabase Dashboard > Edge Functions > send-email > Secrets."
    );
  }

  console.log("Relay:", options.action, "→", options.to_email, "da", options.sender_email);

  const resp = await fetch(RELAY_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-Key": RELAY_KEY,
    },
    body: JSON.stringify(options),
  });

  const result = await resp.json();

  if (result.status === "error") {
    throw new Error(result.error || "Errore dal relay PHP");
  }

  return result;
}

// ═══ MAIN HANDLER ═══
serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  // GET: tracking pixel, click, unsubscribe
  if (req.method === "GET") {
    const url = new URL(req.url);
    const action = url.searchParams.get("action");
    const id = url.searchParams.get("id");

    const supabase = createClient(
      Deno.env.get("SUPABASE_URL") ?? "",
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? ""
    );

    if (action === "track_open" && id) return await trackOpen(supabase, { id });
    if (action === "track_click") {
      return await trackClick(supabase, {
        queue_id: id,
        url: url.searchParams.get("url") || "https://righetto-immobiliare.it",
      });
    }
    if (action === "unsubscribe") {
      const email = url.searchParams.get("email");
      if (email) return await handleUnsubscribe(supabase, { email, queue_id: id });
    }

    return jsonResponse({ error: "Azione GET non riconosciuta" }, 400);
  }

  try {
    const supabase = createClient(
      Deno.env.get("SUPABASE_URL") ?? "",
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? ""
    );

    const body = await req.json();
    const { action } = body;

    if (action === "send_single") return await sendSingleEmail(supabase, body);
    if (action === "process_queue") return await processQueue(supabase, body);
    if (action === "send_test") return await sendTestEmail(supabase, body);
    if (action === "unsubscribe") return await handleUnsubscribe(supabase, body);
    if (action === "track_open") return await trackOpen(supabase, body);
    if (action === "track_click") return await trackClick(supabase, body);

    return jsonResponse({ error: "Azione non riconosciuta: " + action }, 400);
  } catch (error) {
    console.error("Errore:", error);
    return jsonResponse({ error: error.message }, 500);
  }
});

// ═══ GET EMAIL CONFIG ═══
async function getEmailConfig(supabase: any) {
  try {
    const { data, error } = await supabase
      .from("smtp_config")
      .select("*")
      .eq("attivo", true)
      .limit(1);
    if (!error && data && data.length > 0) return data[0];
  } catch (_) {}

  return {
    mittente_email: "info@righettoimmobiliare.it",
    mittente_nome: "Righetto Immobiliare",
    max_per_ora: 300,
    max_per_giorno: 2000,
  };
}

// ═══ VALIDAZIONE EMAIL ═══
function isValidEmail(email: string): boolean {
  if (!email || typeof email !== "string") return false;
  const trimmed = email.trim();
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmed);
}

// ═══ INVIO SINGOLA EMAIL ═══
async function sendSingleEmail(supabase: any, body: any) {
  const { to_email, to_name, subject, html_body, campaign_id, queue_id, sender_email, sender_name } = body;

  if (!to_email || !isValidEmail(to_email)) {
    return jsonResponse({ status: "error", error: "Email destinatario non valida: " + (to_email || "(vuoto)") }, 400);
  }

  // Blacklist
  try {
    const { data: bl } = await supabase
      .from("email_blacklist")
      .select("id")
      .eq("email", to_email.toLowerCase().trim())
      .limit(1);
    if (bl && bl.length > 0) return jsonResponse({ status: "skipped", reason: "blacklisted" });
  } catch (_) {}

  const config = await getEmailConfig(supabase);

  const canSend = await checkRateLimits(supabase, config);
  if (!canSend) return jsonResponse({ status: "rate_limited", reason: "Limite raggiunto" });

  // Tracking pixel
  let finalHtml = html_body || "";
  if (queue_id) {
    finalHtml += `<img src="${Deno.env.get("SUPABASE_URL")}/functions/v1/send-email?action=track_open&id=${queue_id}" width="1" height="1" style="display:none" alt="">`;
  }

  // Validazione mittente: usa config come fallback se sender_email è vuoto o non valido
  const fromEmail = (sender_email && isValidEmail(sender_email)) ? sender_email.trim() : config.mittente_email;
  const fromName = sender_name || config.mittente_nome;

  console.log("sendSingleEmail: from=" + fromEmail + ", to=" + to_email);

  try {
    await sendViaRelay({
      action: "send_single",
      to_email,
      to_name: to_name || "",
      sender_email: fromEmail,
      sender_name: fromName,
      subject,
      html_body: finalHtml,
      reply_to: body.reply_to || fromEmail,
    });

    if (queue_id) {
      await supabase.from("coda_email")
        .update({ stato: "inviata", inviata_il: new Date().toISOString() })
        .eq("id", queue_id);
    }

    if (campaign_id) {
      try {
        const { data } = await supabase
          .from("campagne_email").select("inviati").eq("id", campaign_id).single();
        if (data) {
          await supabase.from("campagne_email")
            .update({ inviati: (data.inviati || 0) + 1 }).eq("id", campaign_id);
        }
      } catch (_) {}
    }

    return jsonResponse({ status: "sent", to: to_email });

  } catch (err) {
    if (queue_id) {
      await supabase.from("coda_email")
        .update({ stato: "errore", errore_msg: err.message, tentativo: (body.tentativo || 0) + 1 })
        .eq("id", queue_id);
    }

    if (err.message?.includes("550") || err.message?.includes("unknown")) {
      await supabase.from("email_blacklist")
        .upsert({ email: to_email.toLowerCase().trim(), motivo: "bounce" });
    }

    return jsonResponse({ status: "error", error: err.message, to: to_email });
  }
}

// ═══ PROCESSA CODA ═══
async function processQueue(supabase: any, body: any) {
  const { campaign_id, batch_size = 10 } = body;
  const config = await getEmailConfig(supabase);

  const { data: queue, error } = await supabase
    .from("coda_email").select("*")
    .eq("campagna_id", campaign_id).eq("stato", "in_coda")
    .order("id").limit(batch_size);

  if (error || !queue || queue.length === 0) {
    await supabase.from("campagne_email")
      .update({ stato: "completata", completata_il: new Date().toISOString() })
      .eq("id", campaign_id);
    return jsonResponse({ status: "completed", processed: 0 });
  }

  let sent = 0, errors = 0;
  const results: any[] = [];

  for (const item of queue) {
    try {
      const { data: bl } = await supabase.from("email_blacklist")
        .select("id").eq("email", item.destinatario_email.toLowerCase().trim()).limit(1);
      if (bl && bl.length > 0) {
        await supabase.from("coda_email").delete().eq("id", item.id);
        continue;
      }
    } catch (_) {}

    const canSend = await checkRateLimits(supabase, config);
    if (!canSend) { results.push({ email: item.destinatario_email, status: "rate_limited" }); break; }

    try {
      const trackPixel = `<img src="${Deno.env.get("SUPABASE_URL")}/functions/v1/send-email?action=track_open&id=${item.id}" width="1" height="1" style="display:none" alt="">`;

      await sendViaRelay({
        action: "send_single",
        to_email: item.destinatario_email,
        to_name: item.destinatario_nome || "",
        sender_email: config.mittente_email,
        sender_name: config.mittente_nome,
        subject: item.oggetto,
        html_body: (item.corpo_html || "") + trackPixel,
        reply_to: config.mittente_email,
      });

      await supabase.from("coda_email")
        .update({ stato: "inviata", inviata_il: new Date().toISOString() }).eq("id", item.id);
      sent++;
      results.push({ email: item.destinatario_email, status: "sent" });

      // 3 sec tra email
      await new Promise((r) => setTimeout(r, 3000));
    } catch (err) {
      errors++;
      await supabase.from("coda_email")
        .update({ stato: "errore", errore_msg: err.message, tentativo: (item.tentativo || 0) + 1 })
        .eq("id", item.id);
      results.push({ email: item.destinatario_email, status: "error", error: err.message });
    }
  }

  await supabase.from("campagne_email")
    .update({ inviati: sent, errori: errors }).eq("id", campaign_id);

  return jsonResponse({ status: "batch_done", sent, errors, results });
}

// ═══ EMAIL DI TEST ═══
async function sendTestEmail(supabase: any, body: any) {
  const { to_email, subject, html_body, sender_email, sender_name, reply_to } = body;
  const config = await getEmailConfig(supabase);

  if (!to_email || !isValidEmail(to_email)) {
    return jsonResponse({ status: "error", error: "Email destinatario non valida: " + (to_email || "(vuoto)") }, 400);
  }

  // Validazione mittente: usa config come fallback se sender_email è vuoto o non valido
  const fromEmail = (sender_email && isValidEmail(sender_email)) ? sender_email.trim() : config.mittente_email;
  const fromName = sender_name || config.mittente_nome;
  const replyToEmail = (reply_to && isValidEmail(reply_to)) ? reply_to.trim() : fromEmail;

  console.log("sendTestEmail: from=" + fromEmail + ", to=" + to_email);

  try {
    await sendViaRelay({
      action: "send_test",
      to_email: to_email.trim(),
      sender_email: fromEmail,
      sender_name: fromName,
      subject: subject || "Email di prova",
      html_body: html_body || "<h1>Test</h1><p>Email di prova da Righetto Immobiliare.</p>",
      reply_to: replyToEmail,
    });

    return jsonResponse({ status: "sent", message: "Email di test inviata a " + to_email });
  } catch (err) {
    return jsonResponse({ status: "error", error: err.message });
  }
}

// ═══ DISISCRIZIONE ═══
async function handleUnsubscribe(supabase: any, body: any) {
  const { email, queue_id } = body;
  if (!email) return jsonResponse({ error: "Email mancante" }, 400);

  await supabase.from("email_blacklist")
    .upsert({ email: email.toLowerCase().trim(), motivo: "disiscrizione" });

  if (queue_id) {
    try { await supabase.from("email_tracking").insert({ coda_email_id: queue_id, tipo: "disiscrizione" }); } catch (_) {}
  }

  const html = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>Disiscrizione</title></head>
  <body style="font-family:Arial;text-align:center;padding:60px 20px;background:#f5f5f5">
    <div style="max-width:500px;margin:0 auto;background:#fff;padding:40px;border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,0.1)">
      <h2 style="color:#2d7a3a">Disiscrizione completata</h2>
      <p>La tua email <strong>${email}</strong> è stata rimossa dalla nostra mailing list.</p>
      <p style="color:#666;font-size:0.9rem">Non riceverai più comunicazioni da Righetto Immobiliare.</p>
      <p style="margin-top:20px"><a href="https://righetto-immobiliare.it" style="color:#b8860b">Torna al sito</a></p>
    </div>
  </body></html>`;

  return new Response(html, { headers: { ...corsHeaders, "Content-Type": "text/html" } });
}

// ═══ TRACCIAMENTO ═══
async function trackOpen(supabase: any, body: any) {
  if (body.id) {
    try {
      await supabase.from("coda_email").update({ aperta_il: new Date().toISOString() }).eq("id", body.id);
      await supabase.from("email_tracking").insert({ coda_email_id: body.id, tipo: "apertura" });
    } catch (_) {}
  }

  const pixel = new Uint8Array([
    0x47,0x49,0x46,0x38,0x39,0x61,0x01,0x00,0x01,0x00,
    0x80,0x00,0x00,0xff,0xff,0xff,0x00,0x00,0x00,0x21,
    0xf9,0x04,0x01,0x00,0x00,0x00,0x00,0x2c,0x00,0x00,
    0x00,0x00,0x01,0x00,0x01,0x00,0x00,0x02,0x02,0x44,
    0x01,0x00,0x3b,
  ]);

  return new Response(pixel, {
    headers: { ...corsHeaders, "Content-Type": "image/gif", "Cache-Control": "no-cache" },
  });
}

async function trackClick(supabase: any, body: any) {
  if (body.queue_id) {
    try {
      await supabase.from("coda_email").update({ click_il: new Date().toISOString() }).eq("id", body.queue_id);
      await supabase.from("email_tracking").insert({ coda_email_id: body.queue_id, tipo: "click", url_cliccato: body.url });
    } catch (_) {}
  }

  return new Response(null, {
    status: 302,
    headers: { ...corsHeaders, Location: body.url || "https://righetto-immobiliare.it" },
  });
}

// ═══ RATE LIMITING ═══
async function checkRateLimits(supabase: any, config: any): Promise<boolean> {
  try {
    const now = new Date();
    const oneHourAgo = new Date(now.getTime() - 3600000);
    const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());

    const { count: hc } = await supabase.from("coda_email")
      .select("id", { count: "exact", head: true })
      .eq("stato", "inviata").gte("inviata_il", oneHourAgo.toISOString());
    if ((hc || 0) >= (config.max_per_ora || 300)) return false;

    const { count: dc } = await supabase.from("coda_email")
      .select("id", { count: "exact", head: true })
      .eq("stato", "inviata").gte("inviata_il", todayStart.toISOString());
    if ((dc || 0) >= (config.max_per_giorno || 2000)) return false;
  } catch (_) {}

  return true;
}

// ═══ UTILS ═══
function jsonResponse(data: any, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { ...corsHeaders, "Content-Type": "application/json" },
  });
}
