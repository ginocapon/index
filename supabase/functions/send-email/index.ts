// ═══════════════════════════════════════════════════════════════
// RIGHETTO IMMOBILIARE — Email Sending Edge Function
// Invia email via Brevo (Sendinblue) API — Compatibile Supabase Edge
// Deploy: supabase functions deploy send-email
// Secrets: BREVO_API_KEY, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
// ═══════════════════════════════════════════════════════════════

import { serve } from "https://deno.land/std@0.177.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS, GET",
};

// ═══ BREVO (SENDINBLUE) EMAIL SENDER ═══
async function sendViaBrevo(options: {
  from: string;
  fromName?: string;
  to: string;
  toName?: string;
  subject: string;
  html: string;
  replyTo?: string;
  headers?: Record<string, string>;
}) {
  const BREVO_API_KEY = Deno.env.get("BREVO_API_KEY");
  if (!BREVO_API_KEY) {
    throw new Error("BREVO_API_KEY non configurata. Vai su Supabase Dashboard > Edge Functions > send-email > Secrets e aggiungi BREVO_API_KEY.");
  }

  const fromEmail = options.from?.trim();
  const fromName = options.fromName?.trim() || "Righetto Immobiliare";

  if (!fromEmail || !fromEmail.includes("@")) {
    throw new Error("Email mittente non valida: '" + fromEmail + "'. Configura un mittente valido.");
  }

  console.log("Brevo: Invio a", options.to, "da", fromName, "<" + fromEmail + ">");

  const payload: any = {
    sender: {
      name: fromName,
      email: fromEmail,
    },
    to: [{
      email: options.to,
      name: options.toName || options.to,
    }],
    subject: options.subject,
    htmlContent: options.html,
  };

  if (options.replyTo) {
    payload.replyTo = {
      email: options.replyTo,
    };
  }

  if (options.headers) {
    payload.headers = options.headers;
  }

  const resp = await fetch("https://api.brevo.com/v3/smtp/email", {
    method: "POST",
    headers: {
      "api-key": BREVO_API_KEY,
      "Content-Type": "application/json",
      "Accept": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const result = await resp.json();

  if (!resp.ok) {
    const errorMsg = result.message || result.error || JSON.stringify(result);
    throw new Error("Brevo API errore: " + errorMsg);
  }

  console.log("Brevo: Email inviata a", options.to, "MessageId:", result.messageId);
  return result;
}

// ═══ MAIN HANDLER ═══
serve(async (req) => {
  // Handle CORS preflight
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  // Handle GET requests (tracking pixel, click tracking, unsubscribe)
  if (req.method === "GET") {
    const url = new URL(req.url);
    const action = url.searchParams.get("action");
    const id = url.searchParams.get("id");

    const supabase = createClient(
      Deno.env.get("SUPABASE_URL") ?? "",
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? ""
    );

    if (action === "track_open" && id) {
      return await trackOpen(supabase, { id });
    }
    if (action === "track_click") {
      return await trackClick(supabase, {
        queue_id: id,
        url: url.searchParams.get("url") || "https://righetto-immobiliare.it",
      });
    }
    if (action === "unsubscribe") {
      const email = url.searchParams.get("email");
      if (email) {
        return await handleUnsubscribe(supabase, { email, queue_id: id });
      }
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

    if (!error && data && data.length > 0) {
      return data[0];
    }
  } catch (_) { /* tabella potrebbe non esistere */ }

  return {
    mittente_email: Deno.env.get("SENDER_EMAIL") || "info@righettoimmobiliare.it",
    mittente_nome: Deno.env.get("SENDER_NAME") || "Righetto Immobiliare",
    max_per_ora: 300,
    max_per_giorno: 2000,
  };
}

// ═══ INVIO SINGOLA EMAIL ═══
async function sendSingleEmail(supabase: any, body: any) {
  const { to_email, to_name, subject, html_body, campaign_id, queue_id, sender_email, sender_name } = body;

  if (!to_email || !to_email.includes("@")) {
    return jsonResponse({ status: "error", error: "Email destinatario non valida" }, 400);
  }

  // Controlla blacklist
  try {
    const { data: blacklisted } = await supabase
      .from("email_blacklist")
      .select("id")
      .eq("email", to_email.toLowerCase().trim())
      .limit(1);

    if (blacklisted && blacklisted.length > 0) {
      return jsonResponse({ status: "skipped", reason: "blacklisted" });
    }
  } catch (_) { /* tabella potrebbe non esistere */ }

  const config = await getEmailConfig(supabase);

  const canSend = await checkRateLimits(supabase, config);
  if (!canSend) {
    return jsonResponse({ status: "rate_limited", reason: "Limite orario/giornaliero raggiunto" });
  }

  // Tracking pixel
  let finalHtml = html_body || "";
  if (queue_id) {
    finalHtml += `<img src="${Deno.env.get("SUPABASE_URL")}/functions/v1/send-email?action=track_open&id=${queue_id}" width="1" height="1" style="display:none" alt="">`;
  }

  // Header anti-spam
  const headers: Record<string, string> = {
    "X-Mailer": "RighettoImmobiliare/1.0",
    "List-Unsubscribe": `<${Deno.env.get("SUPABASE_URL")}/functions/v1/send-email?action=unsubscribe&email=${encodeURIComponent(to_email)}>`,
    "List-Unsubscribe-Post": "List-Unsubscribe=One-Click",
  };

  const fromEmail = sender_email || config.mittente_email;
  const fromName = sender_name || config.mittente_nome;

  try {
    await sendViaBrevo({
      from: fromEmail,
      fromName: fromName,
      to: to_email,
      toName: to_name || "",
      subject: subject,
      html: finalHtml,
      replyTo: body.reply_to || fromEmail,
      headers: headers,
    });

    if (queue_id) {
      await supabase
        .from("coda_email")
        .update({ stato: "inviata", inviata_il: new Date().toISOString() })
        .eq("id", queue_id);
    }

    if (campaign_id) {
      try {
        const { data } = await supabase
          .from("campagne_email")
          .select("inviati")
          .eq("id", campaign_id)
          .single();
        if (data) {
          await supabase
            .from("campagne_email")
            .update({ inviati: (data.inviati || 0) + 1 })
            .eq("id", campaign_id);
        }
      } catch (_) { /* ignore */ }
    }

    return jsonResponse({ status: "sent", to: to_email });

  } catch (err) {
    if (queue_id) {
      await supabase
        .from("coda_email")
        .update({ stato: "errore", errore_msg: err.message, tentativo: (body.tentativo || 0) + 1 })
        .eq("id", queue_id);
    }

    if (err.message?.includes("550") || err.message?.includes("User unknown") || err.message?.includes("does not exist")) {
      await supabase
        .from("email_blacklist")
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
    .from("coda_email")
    .select("*")
    .eq("campagna_id", campaign_id)
    .eq("stato", "in_coda")
    .order("id")
    .limit(batch_size);

  if (error || !queue || queue.length === 0) {
    await supabase
      .from("campagne_email")
      .update({ stato: "completata", completata_il: new Date().toISOString() })
      .eq("id", campaign_id);
    return jsonResponse({ status: "completed", processed: 0 });
  }

  let sent = 0;
  let errors = 0;
  const results: any[] = [];

  for (const item of queue) {
    try {
      const { data: bl } = await supabase
        .from("email_blacklist")
        .select("id")
        .eq("email", item.destinatario_email.toLowerCase().trim())
        .limit(1);

      if (bl && bl.length > 0) {
        await supabase.from("coda_email").delete().eq("id", item.id);
        continue;
      }
    } catch (_) { /* ignore */ }

    const canSend = await checkRateLimits(supabase, config);
    if (!canSend) {
      results.push({ email: item.destinatario_email, status: "rate_limited" });
      break;
    }

    try {
      const trackPixel = `<img src="${Deno.env.get("SUPABASE_URL")}/functions/v1/send-email?action=track_open&id=${item.id}" width="1" height="1" style="display:none" alt="">`;

      await sendViaBrevo({
        from: config.mittente_email,
        fromName: config.mittente_nome,
        to: item.destinatario_email,
        toName: item.destinatario_nome || "",
        subject: item.oggetto,
        html: (item.corpo_html || "") + trackPixel,
        replyTo: config.mittente_email,
        headers: {
          "List-Unsubscribe": `<${Deno.env.get("SUPABASE_URL")}/functions/v1/send-email?action=unsubscribe&email=${encodeURIComponent(item.destinatario_email)}>`,
          "List-Unsubscribe-Post": "List-Unsubscribe=One-Click",
          "X-Mailer": "RighettoImmobiliare/1.0",
        },
      });

      await supabase
        .from("coda_email")
        .update({ stato: "inviata", inviata_il: new Date().toISOString() })
        .eq("id", item.id);

      sent++;
      results.push({ email: item.destinatario_email, status: "sent" });

      // Delay tra email (1-2 sec)
      const delay = 1000 + Math.random() * 1000;
      await new Promise((r) => setTimeout(r, delay));

    } catch (err) {
      errors++;
      await supabase
        .from("coda_email")
        .update({ stato: "errore", errore_msg: err.message, tentativo: (item.tentativo || 0) + 1 })
        .eq("id", item.id);

      if (err.message?.includes("550") || err.message?.includes("User unknown")) {
        await supabase
          .from("email_blacklist")
          .upsert({ email: item.destinatario_email.toLowerCase().trim(), motivo: "bounce" });
      }

      results.push({ email: item.destinatario_email, status: "error", error: err.message });
    }
  }

  await supabase
    .from("campagne_email")
    .update({ inviati: sent, errori: errors })
    .eq("id", campaign_id);

  return jsonResponse({ status: "batch_done", sent, errors, results });
}

// ═══ EMAIL DI TEST ═══
async function sendTestEmail(supabase: any, body: any) {
  const { to_email, subject, html_body, sender_email, sender_name, reply_to } = body;
  const config = await getEmailConfig(supabase);

  if (!to_email || !to_email.includes("@")) {
    return jsonResponse({ status: "error", error: "Email destinatario non valida" }, 400);
  }

  const fromEmail = sender_email || config.mittente_email;
  const fromName = sender_name || config.mittente_nome;

  console.log("Test email — From:", fromEmail, "Name:", fromName, "To:", to_email);

  try {
    await sendViaBrevo({
      from: fromEmail,
      fromName: fromName,
      to: to_email,
      subject: "[TEST] " + (subject || "Email di prova"),
      html: html_body || "<h1>Email di test</h1><p>Questa è un'email di prova da Righetto Immobiliare.</p>",
      replyTo: reply_to || fromEmail,
    });

    return jsonResponse({ status: "sent", message: "Email di test inviata a " + to_email });
  } catch (err) {
    console.error("Errore invio test:", err);
    return jsonResponse({ status: "error", error: err.message });
  }
}

// ═══ DISISCRIZIONE ═══
async function handleUnsubscribe(supabase: any, body: any) {
  const { email, queue_id } = body;

  if (!email) {
    return jsonResponse({ error: "Email mancante" }, 400);
  }

  await supabase
    .from("email_blacklist")
    .upsert({ email: email.toLowerCase().trim(), motivo: "disiscrizione" });

  if (queue_id) {
    try {
      await supabase
        .from("email_tracking")
        .insert({ coda_email_id: queue_id, tipo: "disiscrizione" });
    } catch (_) { /* ignore */ }
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

  return new Response(html, {
    headers: { ...corsHeaders, "Content-Type": "text/html" },
  });
}

// ═══ TRACCIAMENTO ═══
async function trackOpen(supabase: any, body: any) {
  const queueId = body.id;

  if (queueId) {
    try {
      await supabase.from("coda_email").update({ aperta_il: new Date().toISOString() }).eq("id", queueId);
      await supabase.from("email_tracking").insert({ coda_email_id: queueId, tipo: "apertura" });
    } catch (_) { /* ignore */ }
  }

  // Pixel trasparente 1x1 GIF
  const pixel = new Uint8Array([
    0x47, 0x49, 0x46, 0x38, 0x39, 0x61, 0x01, 0x00, 0x01, 0x00,
    0x80, 0x00, 0x00, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x21,
    0xf9, 0x04, 0x01, 0x00, 0x00, 0x00, 0x00, 0x2c, 0x00, 0x00,
    0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, 0x02, 0x02, 0x44,
    0x01, 0x00, 0x3b,
  ]);

  return new Response(pixel, {
    headers: { ...corsHeaders, "Content-Type": "image/gif", "Cache-Control": "no-cache" },
  });
}

async function trackClick(supabase: any, body: any) {
  const { queue_id, url } = body;

  if (queue_id) {
    try {
      await supabase.from("coda_email").update({ click_il: new Date().toISOString() }).eq("id", queue_id);
      await supabase.from("email_tracking").insert({ coda_email_id: queue_id, tipo: "click", url_cliccato: url });
    } catch (_) { /* ignore */ }
  }

  return new Response(null, {
    status: 302,
    headers: { ...corsHeaders, Location: url || "https://righetto-immobiliare.it" },
  });
}

// ═══ RATE LIMITING ═══
async function checkRateLimits(supabase: any, config: any): Promise<boolean> {
  try {
    const now = new Date();
    const oneHourAgo = new Date(now.getTime() - 60 * 60 * 1000);
    const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());

    const { count: hourCount } = await supabase
      .from("coda_email")
      .select("id", { count: "exact", head: true })
      .eq("stato", "inviata")
      .gte("inviata_il", oneHourAgo.toISOString());

    if ((hourCount || 0) >= (config.max_per_ora || 300)) return false;

    const { count: dayCount } = await supabase
      .from("coda_email")
      .select("id", { count: "exact", head: true })
      .eq("stato", "inviata")
      .gte("inviata_il", todayStart.toISOString());

    if ((dayCount || 0) >= (config.max_per_giorno || 2000)) return false;
  } catch (_) {
    // Se la tabella non esiste, permetti l'invio
  }

  return true;
}

// ═══ UTILS ═══
function jsonResponse(data: any, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { ...corsHeaders, "Content-Type": "application/json" },
  });
}
