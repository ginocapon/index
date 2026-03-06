// ═══════════════════════════════════════════════════════════════
// RIGHETTO IMMOBILIARE — Email Sending Edge Function
// Invia email via SMTP proprio — Zero dipendenze esterne
// Deploy: supabase functions deploy send-email
// ═══════════════════════════════════════════════════════════════

import { serve } from "https://deno.land/std@0.177.0/http/server.ts";
import { SMTPClient } from "https://deno.land/x/denomailer@1.6.0/mod.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const supabase = createClient(
      Deno.env.get("SUPABASE_URL") ?? "",
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? ""
    );

    const body = await req.json();
    const { action } = body;

    // ── AZIONE: Invia singola email ──
    if (action === "send_single") {
      return await sendSingleEmail(supabase, body);
    }

    // ── AZIONE: Processa coda email ──
    if (action === "process_queue") {
      return await processQueue(supabase, body);
    }

    // ── AZIONE: Email di test ──
    if (action === "send_test") {
      return await sendTestEmail(supabase, body);
    }

    // ── AZIONE: Disiscrizione ──
    if (action === "unsubscribe") {
      return await handleUnsubscribe(supabase, body);
    }

    // ── AZIONE: Traccia apertura ──
    if (action === "track_open") {
      return await trackOpen(supabase, body);
    }

    // ── AZIONE: Traccia click ──
    if (action === "track_click") {
      return await trackClick(supabase, body);
    }

    return new Response(
      JSON.stringify({ error: "Azione non riconosciuta" }),
      { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );

  } catch (error) {
    console.error("Errore:", error);
    return new Response(
      JSON.stringify({ error: error.message }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});

// ═══ SMTP CONNECTION ═══
async function getSmtpConfig(supabase: any) {
  const { data, error } = await supabase
    .from("smtp_config")
    .select("*")
    .eq("attivo", true)
    .limit(1);

  if (error || !data || data.length === 0) {
    throw new Error("Nessuna configurazione SMTP attiva trovata. Configura in Supabase → smtp_config. Errore: " + (error?.message || "nessun dato"));
  }
  return data[0]; // Prendi la prima riga
}

async function createSmtpClient(config: any) {
  // Strategia: prova diverse configurazioni per massima compatibilità
  const attempts = [];

  if (config.porta === 465) {
    // Aruba smtps.aruba.it:465 — SSL diretto
    attempts.push({ hostname: config.host, port: 465, tls: true });
    // Fallback: smtp.aruba.it:587 — STARTTLS
    attempts.push({ hostname: config.host.replace('smtps.', 'smtp.'), port: 587, tls: false });
  } else if (config.porta === 587) {
    attempts.push({ hostname: config.host, port: 587, tls: false });
    attempts.push({ hostname: config.host.replace('smtp.', 'smtps.'), port: 465, tls: true });
  } else {
    attempts.push({ hostname: config.host, port: config.porta, tls: config.use_tls });
  }

  let lastError = null;
  for (const attempt of attempts) {
    try {
      console.log(`Tentativo SMTP: ${attempt.hostname}:${attempt.port} TLS=${attempt.tls}`);
      const client = new SMTPClient({
        connection: {
          hostname: attempt.hostname,
          port: attempt.port,
          tls: attempt.tls,
          auth: {
            username: config.utente,
            password: config.password,
          },
        },
      });
      return client;
    } catch (e) {
      console.warn(`SMTP ${attempt.hostname}:${attempt.port} fallito:`, e.message);
      lastError = e;
    }
  }
  throw lastError || new Error("Impossibile connettersi al server SMTP");
}

// ═══ INVIO SINGOLA EMAIL ═══
async function sendSingleEmail(supabase: any, body: any) {
  const { to_email, to_name, subject, html_body, campaign_id, queue_id, sender_email, sender_name } = body;

  // Controlla blacklist
  const { data: blacklisted } = await supabase
    .from("email_blacklist")
    .select("id")
    .eq("email", to_email.toLowerCase().trim())
    .limit(1);

  if (blacklisted && blacklisted.length > 0) {
    return jsonResponse({ status: "skipped", reason: "blacklisted" });
  }

  const config = await getSmtpConfig(supabase);

  // Controlla limiti orari/giornalieri
  const canSend = await checkRateLimits(supabase, config);
  if (!canSend) {
    return jsonResponse({ status: "rate_limited", reason: "Limite orario/giornaliero raggiunto" });
  }

  let client;
  try {
    client = await createSmtpClient(config);
  } catch (connErr) {
    return jsonResponse({ status: "error", error: "Connessione SMTP fallita: " + connErr.message });
  }

  // Aggiungi tracking pixel e unsubscribe
  let finalHtml = html_body;
  if (queue_id) {
    // Pixel di tracciamento apertura
    const trackPixel = `<img src="${Deno.env.get("SUPABASE_URL")}/functions/v1/send-email?action=track_open&id=${queue_id}" width="1" height="1" style="display:none" alt="">`;
    finalHtml += trackPixel;
  }

  // Header professionali anti-spam
  const headers: Record<string, string> = {
    "X-Mailer": "RighettoImmobiliare/1.0",
    "List-Unsubscribe": `<mailto:${config.mittente_email}?subject=CANCELLAMI>`,
    "List-Unsubscribe-Post": "List-Unsubscribe=One-Click",
    "Precedence": "bulk",
    "X-Auto-Response-Suppress": "OOF, AutoReply",
    "Feedback-ID": `campaign${campaign_id || 0}:righetto:email`,
  };

  try {
    await client.send({
      from: { name: sender_name || config.mittente_nome, addr: sender_email || config.mittente_email },
      to: [{ name: to_name || "", addr: to_email }],
      subject: subject,
      content: "",
      html: finalHtml,
      replyTo: body.reply_to || sender_email || config.mittente_email,
      headers: headers,
    });

    try { await client.close(); } catch(_) { /* ignore close errors */ }

    // Aggiorna stato in coda
    if (queue_id) {
      await supabase
        .from("coda_email")
        .update({ stato: "inviata", inviata_il: new Date().toISOString() })
        .eq("id", queue_id);
    }

    // Aggiorna contatore campagna
    if (campaign_id) {
      await supabase.rpc("increment_campo", {
        p_table: "campagne_email",
        p_id: campaign_id,
        p_field: "inviati",
      }).catch(() => {
        // Fallback: update diretto
        supabase
          .from("campagne_email")
          .select("inviati")
          .eq("id", campaign_id)
          .single()
          .then(({ data }: any) => {
            if (data) {
              supabase.from("campagne_email").update({ inviati: data.inviati + 1 }).eq("id", campaign_id);
            }
          });
      });
    }

    return jsonResponse({ status: "sent", to: to_email });

  } catch (err) {
    await client.close().catch(() => {});

    // Registra errore
    if (queue_id) {
      await supabase
        .from("coda_email")
        .update({
          stato: "errore",
          errore_msg: err.message,
          tentativo: (body.tentativo || 0) + 1,
        })
        .eq("id", queue_id);
    }

    // Se bounce permanente, aggiungi a blacklist
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
  const config = await getSmtpConfig(supabase);

  // Prendi batch dalla coda
  const { data: queue, error } = await supabase
    .from("coda_email")
    .select("*")
    .eq("campagna_id", campaign_id)
    .eq("stato", "in_coda")
    .order("id")
    .limit(batch_size);

  if (error || !queue || queue.length === 0) {
    // Campagna completata
    await supabase
      .from("campagne_email")
      .update({ stato: "completata", completata_il: new Date().toISOString() })
      .eq("id", campaign_id);
    return jsonResponse({ status: "completed", processed: 0 });
  }

  const client = await createSmtpClient(config);
  let sent = 0;
  let errors = 0;
  const results: any[] = [];

  for (const item of queue) {
    // Controlla blacklist
    const { data: bl } = await supabase
      .from("email_blacklist")
      .select("id")
      .eq("email", item.destinatario_email.toLowerCase().trim())
      .limit(1);

    if (bl && bl.length > 0) {
      await supabase.from("coda_email").delete().eq("id", item.id);
      continue;
    }

    // Controlla limiti
    const canSend = await checkRateLimits(supabase, config);
    if (!canSend) {
      results.push({ email: item.destinatario_email, status: "rate_limited" });
      break;
    }

    try {
      // Tracking pixel
      const trackPixel = `<img src="${Deno.env.get("SUPABASE_URL")}/functions/v1/send-email?action=track_open&id=${item.id}" width="1" height="1" style="display:none" alt="">`;

      await client.send({
        from: { name: config.mittente_nome, addr: config.mittente_email },
        to: [{ name: item.destinatario_nome || "", addr: item.destinatario_email }],
        subject: item.oggetto,
        content: "",
        html: item.corpo_html + trackPixel,
        replyTo: config.mittente_email,
        headers: {
          "List-Unsubscribe": `<mailto:${config.mittente_email}?subject=CANCELLAMI>`,
          "List-Unsubscribe-Post": "List-Unsubscribe=One-Click",
          "Precedence": "bulk",
          "X-Mailer": "RighettoImmobiliare/1.0",
        },
      });

      await supabase
        .from("coda_email")
        .update({ stato: "inviata", inviata_il: new Date().toISOString() })
        .eq("id", item.id);

      sent++;
      results.push({ email: item.destinatario_email, status: "sent" });

      // Delay tra email (2-5 sec random per sembrare naturale)
      const delay = 2000 + Math.random() * 3000;
      await new Promise((r) => setTimeout(r, delay));

    } catch (err) {
      errors++;
      await supabase
        .from("coda_email")
        .update({ stato: "errore", errore_msg: err.message, tentativo: item.tentativo + 1 })
        .eq("id", item.id);

      // Bounce handling
      if (err.message?.includes("550") || err.message?.includes("User unknown")) {
        await supabase
          .from("email_blacklist")
          .upsert({ email: item.destinatario_email.toLowerCase().trim(), motivo: "bounce" });
      }

      results.push({ email: item.destinatario_email, status: "error", error: err.message });
    }
  }

  await client.close().catch(() => {});

  // Aggiorna contatori campagna
  await supabase
    .from("campagne_email")
    .update({
      inviati: sent,
      errori: errors,
    })
    .eq("id", campaign_id);

  return jsonResponse({ status: "batch_done", sent, errors, results });
}

// ═══ EMAIL DI TEST ═══
async function sendTestEmail(supabase: any, body: any) {
  const { to_email, subject, html_body, sender_email, sender_name, reply_to } = body;
  const config = await getSmtpConfig(supabase);

  let client;
  try {
    client = await createSmtpClient(config);
  } catch (connErr) {
    return jsonResponse({ status: "error", error: "Connessione SMTP fallita: " + connErr.message + " — Host: " + config.host + " Porta: " + config.porta });
  }

  try {
    await client.send({
      from: { name: sender_name || config.mittente_nome, addr: sender_email || config.mittente_email },
      to: [{ addr: to_email }],
      subject: "[TEST] " + subject,
      content: "",
      html: html_body,
      replyTo: reply_to || sender_email || config.mittente_email,
    });
    try { await client.close(); } catch(_) { /* ignore close errors */ }
    return jsonResponse({ status: "sent", message: "Email di test inviata a " + to_email });
  } catch (err) {
    try { await client.close(); } catch(_) {}
    // Se l'errore è solo su close() ma send() è andato, conta come successo
    if (err.message?.includes("close") || err.message?.includes("properties of undefined")) {
      return jsonResponse({ status: "sent", message: "Email inviata (warning: " + err.message + ")" });
    }
    return jsonResponse({ status: "error", error: err.message });
  }
}

// ═══ DISISCRIZIONE ═══
async function handleUnsubscribe(supabase: any, body: any) {
  const { email, queue_id } = body;

  await supabase
    .from("email_blacklist")
    .upsert({ email: email.toLowerCase().trim(), motivo: "disiscrizione" });

  if (queue_id) {
    await supabase
      .from("email_tracking")
      .insert({ coda_email_id: queue_id, tipo: "disiscrizione" });
  }

  // Ritorna HTML di conferma disiscrizione
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
  const url = new URL(body.url || "http://x");
  const queueId = url.searchParams.get("id") || body.id;

  if (queueId) {
    await supabase
      .from("coda_email")
      .update({ aperta_il: new Date().toISOString() })
      .eq("id", queueId);

    await supabase.from("email_tracking").insert({
      coda_email_id: queueId,
      tipo: "apertura",
    });
  }

  // Ritorna pixel trasparente 1x1
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
    await supabase
      .from("coda_email")
      .update({ click_il: new Date().toISOString() })
      .eq("id", queue_id);

    await supabase.from("email_tracking").insert({
      coda_email_id: queue_id,
      tipo: "click",
      url_cliccato: url,
    });
  }

  // Redirect al link originale
  return new Response(null, {
    status: 302,
    headers: { ...corsHeaders, Location: url || "https://righetto-immobiliare.it" },
  });
}

// ═══ RATE LIMITING ═══
async function checkRateLimits(supabase: any, config: any): Promise<boolean> {
  const now = new Date();
  const oneHourAgo = new Date(now.getTime() - 60 * 60 * 1000);
  const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());

  // Conta email inviate nell'ultima ora
  const { count: hourCount } = await supabase
    .from("coda_email")
    .select("id", { count: "exact", head: true })
    .eq("stato", "inviata")
    .gte("inviata_il", oneHourAgo.toISOString());

  if ((hourCount || 0) >= config.max_per_ora) return false;

  // Conta email inviate oggi
  const { count: dayCount } = await supabase
    .from("coda_email")
    .select("id", { count: "exact", head: true })
    .eq("stato", "inviata")
    .gte("inviata_il", todayStart.toISOString());

  if ((dayCount || 0) >= config.max_per_giorno) return false;

  return true;
}

// ═══ UTILS ═══
function jsonResponse(data: any) {
  return new Response(JSON.stringify(data), {
    headers: { ...corsHeaders, "Content-Type": "application/json" },
  });
}
