// ═══════════════════════════════════════════════════════════════
// RIGHETTO IMMOBILIARE — Email Sending Edge Function
// Invia email via SMTP proprio — Zero dipendenze esterne
// Usa SMTP raw (Deno.connectTls) — compatibile con Supabase Edge
// Deploy: supabase functions deploy send-email
// ═══════════════════════════════════════════════════════════════

import { serve } from "https://deno.land/std@0.177.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { encode as base64Encode } from "https://deno.land/std@0.177.0/encoding/base64.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

// ═══ RAW SMTP CLIENT ═══
// Implementazione SMTP minimale che funziona in Deno Deploy
class RawSmtpClient {
  private conn: Deno.TlsConn | Deno.Conn | null = null;
  private reader: ReadableStreamDefaultReader<Uint8Array> | null = null;
  private writer: WritableStreamDefaultWriter<Uint8Array> | null = null;
  private textEncoder = new TextEncoder();
  private textDecoder = new TextDecoder();
  private buffer = "";

  async connect(hostname: string, port: number, useTls: boolean) {
    console.log(`SMTP: Connessione a ${hostname}:${port} TLS=${useTls}`);

    if (useTls || port === 465) {
      // Connessione TLS diretta (porta 465)
      this.conn = await Deno.connectTls({ hostname, port });
    } else {
      // Connessione plain (porta 587 — STARTTLS dopo)
      this.conn = await Deno.connect({ hostname, port });
    }

    this.reader = this.conn.readable.getReader();
    this.writer = this.conn.writable.getWriter();

    // Leggi il greeting del server (220)
    const greeting = await this.readResponse();
    console.log("SMTP greeting:", greeting);
    if (!greeting.startsWith("220")) {
      throw new Error("SMTP greeting inaspettato: " + greeting);
    }
  }

  private async readResponse(): Promise<string> {
    // Leggi fino a trovare una riga che indica fine risposta (es. "250 " non "250-")
    while (true) {
      // Controlla se abbiamo già una risposta completa nel buffer
      const lines = this.buffer.split("\r\n");
      for (let i = 0; i < lines.length - 1; i++) {
        // Una riga SMTP è completa se il 4° carattere è spazio (non trattino)
        if (lines[i].length >= 4 && lines[i][3] === " ") {
          const response = lines.slice(0, i + 1).join("\r\n");
          this.buffer = lines.slice(i + 1).join("\r\n");
          return response;
        }
      }
      // Se l'ultima riga (senza \r\n finale) è una riga finale
      const lastLine = lines[lines.length - 1];
      if (lastLine.length >= 4 && lastLine[3] === " " && lines.length === 1) {
        this.buffer = "";
        return lastLine;
      }

      // Leggi più dati
      const { value, done } = await this.reader!.read();
      if (done) throw new Error("Connessione SMTP chiusa inaspettatamente");
      this.buffer += this.textDecoder.decode(value);
    }
  }

  private async sendCommand(cmd: string): Promise<string> {
    const logCmd = cmd.startsWith("AUTH") || cmd.length > 50
      ? cmd.substring(0, 20) + "..."
      : cmd;
    console.log("SMTP >", logCmd);

    await this.writer!.write(this.textEncoder.encode(cmd + "\r\n"));
    const response = await this.readResponse();
    console.log("SMTP <", response.substring(0, 100));
    return response;
  }

  async authenticate(username: string, password: string) {
    // EHLO
    const ehlo = await this.sendCommand("EHLO righetto-immobiliare.it");
    if (!ehlo.startsWith("250")) {
      throw new Error("EHLO fallito: " + ehlo);
    }

    // AUTH LOGIN
    const authResp = await this.sendCommand("AUTH LOGIN");
    if (!authResp.startsWith("334")) {
      throw new Error("AUTH LOGIN fallito: " + authResp);
    }

    // Username (base64)
    const userResp = await this.sendCommand(btoa(username));
    if (!userResp.startsWith("334")) {
      throw new Error("AUTH username fallito: " + userResp);
    }

    // Password (base64)
    const passResp = await this.sendCommand(btoa(password));
    if (!passResp.startsWith("235")) {
      throw new Error("Autenticazione SMTP fallita. Controlla username e password. Risposta: " + passResp);
    }

    console.log("SMTP: Autenticazione riuscita!");
  }

  async sendMail(options: {
    from: string;
    fromName?: string;
    to: string;
    toName?: string;
    subject: string;
    html: string;
    replyTo?: string;
    headers?: Record<string, string>;
  }) {
    // MAIL FROM
    const mailFrom = await this.sendCommand(`MAIL FROM:<${options.from}>`);
    if (!mailFrom.startsWith("250")) {
      throw new Error("MAIL FROM fallito: " + mailFrom);
    }

    // RCPT TO
    const rcptTo = await this.sendCommand(`RCPT TO:<${options.to}>`);
    if (!rcptTo.startsWith("250")) {
      throw new Error("RCPT TO fallito: " + rcptTo);
    }

    // DATA
    const dataResp = await this.sendCommand("DATA");
    if (!dataResp.startsWith("354")) {
      throw new Error("DATA fallito: " + dataResp);
    }

    // Costruisci il messaggio MIME
    const boundary = "----=_Part_" + Date.now() + "_" + Math.random().toString(36).slice(2);
    const fromHeader = options.fromName
      ? `=?UTF-8?B?${btoa(unescape(encodeURIComponent(options.fromName)))}?= <${options.from}>`
      : options.from;
    const toHeader = options.toName
      ? `=?UTF-8?B?${btoa(unescape(encodeURIComponent(options.toName)))}?= <${options.to}>`
      : options.to;
    const subjectEncoded = `=?UTF-8?B?${btoa(unescape(encodeURIComponent(options.subject)))}?=`;

    let message = "";
    message += `From: ${fromHeader}\r\n`;
    message += `To: ${toHeader}\r\n`;
    message += `Subject: ${subjectEncoded}\r\n`;
    message += `Date: ${new Date().toUTCString()}\r\n`;
    message += `MIME-Version: 1.0\r\n`;
    message += `Message-ID: <${Date.now()}.${Math.random().toString(36).slice(2)}@righetto-immobiliare.it>\r\n`;

    if (options.replyTo) {
      message += `Reply-To: ${options.replyTo}\r\n`;
    }

    // Header aggiuntivi
    if (options.headers) {
      for (const [key, value] of Object.entries(options.headers)) {
        message += `${key}: ${value}\r\n`;
      }
    }

    message += `Content-Type: text/html; charset=UTF-8\r\n`;
    message += `Content-Transfer-Encoding: base64\r\n`;
    message += `\r\n`;

    // Corpo HTML in base64 (evita problemi con linee lunghe e caratteri speciali)
    const htmlBase64 = btoa(unescape(encodeURIComponent(options.html)));
    // Spezza in righe da 76 caratteri
    for (let i = 0; i < htmlBase64.length; i += 76) {
      message += htmlBase64.substring(i, i + 76) + "\r\n";
    }

    // Termina con punto singolo su riga
    message += "\r\n.\r\n";

    // Invia il messaggio
    await this.writer!.write(this.textEncoder.encode(message));
    const sendResp = await this.readResponse();
    if (!sendResp.startsWith("250")) {
      throw new Error("Invio email fallito: " + sendResp);
    }

    console.log("SMTP: Email inviata a " + options.to);
  }

  async close() {
    try {
      await this.sendCommand("QUIT");
    } catch (_) { /* ignore */ }
    try {
      this.reader?.releaseLock();
      this.writer?.releaseLock();
      this.conn?.close();
    } catch (_) { /* ignore */ }
    this.conn = null;
  }
}

// ═══ MAIN HANDLER ═══
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

    if (action === "send_single") return await sendSingleEmail(supabase, body);
    if (action === "process_queue") return await processQueue(supabase, body);
    if (action === "send_test") return await sendTestEmail(supabase, body);
    if (action === "unsubscribe") return await handleUnsubscribe(supabase, body);
    if (action === "track_open") return await trackOpen(supabase, body);
    if (action === "track_click") return await trackClick(supabase, body);

    return jsonResponse({ error: "Azione non riconosciuta" }, 400);

  } catch (error) {
    console.error("Errore:", error);
    return jsonResponse({ error: error.message }, 500);
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
    throw new Error("Nessuna configurazione SMTP attiva trovata. Errore: " + (error?.message || "nessun dato"));
  }
  return data[0];
}

async function createAndConnectSmtp(config: any): Promise<RawSmtpClient> {
  const client = new RawSmtpClient();

  // Strategia: prova 465 SSL poi 587 plain
  const attempts = [];
  if (config.porta === 465) {
    attempts.push({ hostname: config.host, port: 465, tls: true });
    attempts.push({ hostname: config.host.replace('smtps.', 'smtp.'), port: 587, tls: false });
  } else if (config.porta === 587) {
    attempts.push({ hostname: config.host, port: 587, tls: false });
    attempts.push({ hostname: config.host.replace('smtp.', 'smtps.'), port: 465, tls: true });
  } else {
    attempts.push({ hostname: config.host, port: config.porta, tls: !!config.use_tls });
  }

  let lastError: Error | null = null;
  for (const attempt of attempts) {
    try {
      const c = new RawSmtpClient();
      await c.connect(attempt.hostname, attempt.port, attempt.tls);
      await c.authenticate(config.utente, config.password);
      return c;
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

  const canSend = await checkRateLimits(supabase, config);
  if (!canSend) {
    return jsonResponse({ status: "rate_limited", reason: "Limite orario/giornaliero raggiunto" });
  }

  let client: RawSmtpClient;
  try {
    client = await createAndConnectSmtp(config);
  } catch (connErr) {
    return jsonResponse({ status: "error", error: "Connessione SMTP fallita: " + connErr.message });
  }

  // Tracking pixel
  let finalHtml = html_body;
  if (queue_id) {
    finalHtml += `<img src="${Deno.env.get("SUPABASE_URL")}/functions/v1/send-email?action=track_open&id=${queue_id}" width="1" height="1" style="display:none" alt="">`;
  }

  // Header anti-spam
  const headers: Record<string, string> = {
    "X-Mailer": "RighettoImmobiliare/1.0",
    "List-Unsubscribe": `<mailto:${config.mittente_email}?subject=CANCELLAMI>`,
    "List-Unsubscribe-Post": "List-Unsubscribe=One-Click",
    "Precedence": "bulk",
    "X-Auto-Response-Suppress": "OOF, AutoReply",
    "Feedback-ID": `campaign${campaign_id || 0}:righetto:email`,
  };

  try {
    await client.sendMail({
      from: sender_email || config.mittente_email,
      fromName: sender_name || config.mittente_nome,
      to: to_email,
      toName: to_name || "",
      subject: subject,
      html: finalHtml,
      replyTo: body.reply_to || sender_email || config.mittente_email,
      headers: headers,
    });

    await client.close();

    if (queue_id) {
      await supabase
        .from("coda_email")
        .update({ stato: "inviata", inviata_il: new Date().toISOString() })
        .eq("id", queue_id);
    }

    if (campaign_id) {
      await supabase.rpc("increment_campo", {
        p_table: "campagne_email",
        p_id: campaign_id,
        p_field: "inviati",
      }).catch(() => {
        supabase.from("campagne_email").select("inviati").eq("id", campaign_id).single()
          .then(({ data }: any) => {
            if (data) supabase.from("campagne_email").update({ inviati: data.inviati + 1 }).eq("id", campaign_id);
          });
      });
    }

    return jsonResponse({ status: "sent", to: to_email });

  } catch (err) {
    await client.close();

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
  const config = await getSmtpConfig(supabase);

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

  let client: RawSmtpClient;
  try {
    client = await createAndConnectSmtp(config);
  } catch (connErr) {
    return jsonResponse({ status: "error", error: "Connessione SMTP fallita: " + connErr.message });
  }

  let sent = 0;
  let errors = 0;
  const results: any[] = [];

  for (const item of queue) {
    const { data: bl } = await supabase
      .from("email_blacklist")
      .select("id")
      .eq("email", item.destinatario_email.toLowerCase().trim())
      .limit(1);

    if (bl && bl.length > 0) {
      await supabase.from("coda_email").delete().eq("id", item.id);
      continue;
    }

    const canSend = await checkRateLimits(supabase, config);
    if (!canSend) {
      results.push({ email: item.destinatario_email, status: "rate_limited" });
      break;
    }

    try {
      const trackPixel = `<img src="${Deno.env.get("SUPABASE_URL")}/functions/v1/send-email?action=track_open&id=${item.id}" width="1" height="1" style="display:none" alt="">`;

      await client.sendMail({
        from: config.mittente_email,
        fromName: config.mittente_nome,
        to: item.destinatario_email,
        toName: item.destinatario_nome || "",
        subject: item.oggetto,
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

      // Delay naturale tra email (2-5 sec)
      const delay = 2000 + Math.random() * 3000;
      await new Promise((r) => setTimeout(r, delay));

    } catch (err) {
      errors++;
      await supabase
        .from("coda_email")
        .update({ stato: "errore", errore_msg: err.message, tentativo: item.tentativo + 1 })
        .eq("id", item.id);

      if (err.message?.includes("550") || err.message?.includes("User unknown")) {
        await supabase
          .from("email_blacklist")
          .upsert({ email: item.destinatario_email.toLowerCase().trim(), motivo: "bounce" });
      }

      results.push({ email: item.destinatario_email, status: "error", error: err.message });
    }
  }

  await client.close();

  await supabase
    .from("campagne_email")
    .update({ inviati: sent, errori: errors })
    .eq("id", campaign_id);

  return jsonResponse({ status: "batch_done", sent, errors, results });
}

// ═══ EMAIL DI TEST ═══
async function sendTestEmail(supabase: any, body: any) {
  const { to_email, subject, html_body, sender_email, sender_name, reply_to } = body;
  const config = await getSmtpConfig(supabase);

  let client: RawSmtpClient;
  try {
    client = await createAndConnectSmtp(config);
  } catch (connErr) {
    return jsonResponse({
      status: "error",
      error: "Connessione SMTP fallita: " + connErr.message + " — Host: " + config.host + " Porta: " + config.porta
    });
  }

  try {
    await client.sendMail({
      from: sender_email || config.mittente_email,
      fromName: sender_name || config.mittente_nome,
      to: to_email,
      subject: "[TEST] " + subject,
      html: html_body,
      replyTo: reply_to || sender_email || config.mittente_email,
    });
    await client.close();
    return jsonResponse({ status: "sent", message: "Email di test inviata a " + to_email });
  } catch (err) {
    await client.close();
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
    await supabase.from("coda_email").update({ aperta_il: new Date().toISOString() }).eq("id", queueId);
    await supabase.from("email_tracking").insert({ coda_email_id: queueId, tipo: "apertura" });
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
    await supabase.from("coda_email").update({ click_il: new Date().toISOString() }).eq("id", queue_id);
    await supabase.from("email_tracking").insert({ coda_email_id: queue_id, tipo: "click", url_cliccato: url });
  }

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

  const { count: hourCount } = await supabase
    .from("coda_email")
    .select("id", { count: "exact", head: true })
    .eq("stato", "inviata")
    .gte("inviata_il", oneHourAgo.toISOString());

  if ((hourCount || 0) >= config.max_per_ora) return false;

  const { count: dayCount } = await supabase
    .from("coda_email")
    .select("id", { count: "exact", head: true })
    .eq("stato", "inviata")
    .gte("inviata_il", todayStart.toISOString());

  if ((dayCount || 0) >= config.max_per_giorno) return false;

  return true;
}

// ═══ UTILS ═══
function jsonResponse(data: any, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { ...corsHeaders, "Content-Type": "application/json" },
  });
}
