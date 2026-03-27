/**
 * RIGHETTO IMMOBILIARE — Configurazione Servizi Esterni
 */

const SERVIZI_CONFIG = {
  // ── NOTIFICHE EMAIL — Supabase Edge Function ────────────
  // Stessa API usata dall'admin per le email massive.
  // Non richiede send-mail.php su cPanel.
  EMAIL_NOTIFY_TO: 'info@righettoimmobiliare.it',

  // Invia una email di notifica tramite la Edge Function send-email.
  // opts: { subject, html_body, reply_to (opzionale) }
  // Ritorna true se inviata, false in caso di errore.
  sendNotifica: async function(opts) {
    try {
      const r = await fetch(
        'https://qwkwkemuabfwvwuqrxlu.supabase.co/functions/v1/send-email',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3a3drZW11YWJmd3Z3dXFyeGx1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE1OTk5NjEsImV4cCI6MjA4NzE3NTk2MX0.JxEYiWVPEOiwjZtbWAZRlMUdKXcupjw7filvrERCiqc'
          },
          body: JSON.stringify({
            action: 'send_test',
            to_email: this.EMAIL_NOTIFY_TO,
            sender_email: 'info@righettoimmobiliare.it',
            sender_name: 'Righetto Immobiliare',
            subject: opts.subject,
            html_body: opts.html_body,
            reply_to: opts.reply_to || undefined
          })
        }
      );
      return r.ok;
    } catch(e) { return false; }
  },

  // ── EMAILJS (Email Marketing) ────────────────────────────
  EMAILJS_PUBLIC_KEY: 'n3XE6MEEie7ZxPw-z',
  EMAILJS_SERVICE_ID: 'service_60lyfuu',
  EMAILJS_MARKETING_TEMPLATE_ID: 'template_1gpdcuq'
};
