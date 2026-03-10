/**
 * RIGHETTO IMMOBILIARE — Configurazione Servizi Esterni
 *
 * Istruzioni:
 * 1. FORMSPREE: Registrati su https://formspree.io → Crea un form → Copia il Form ID
 * 2. BREVO: Registrati su https://brevo.com → Crea lista contatti → Crea form iscrizione
 */

const SERVIZI_CONFIG = {
  // ── EMAIL RELAY (send-mail.php su cPanel) ─────────────
  // Endpoint per invio email tramite mail() di cPanel
  EMAIL_RELAY_URL: 'https://api.righettoimmobiliare.it/send-mail.php',
  EMAIL_RELAY_KEY: 'RighettoMail2026!SecretKey',
  EMAIL_NOTIFY_TO: 'info@righettoimmobiliare.it',

  // ── FORMSPREE (deprecato — sostituito da email relay) ──
  FORMSPREE_ID: 'IL_TUO_FORM_ID',

  // ── EMAILJS (Email Marketing) ────────────────────────────
  // Vai su https://emailjs.com → Account → Public Key
  // Poi Services → copia Service ID
  // Poi Email Templates → crea template marketing → copia Template ID
  // Variabili template: {{to_email}}, {{to_name}}, {{subject}}, {{message}}
  EMAILJS_PUBLIC_KEY: 'n3XE6MEEie7ZxPw-z',
  EMAILJS_SERVICE_ID: 'service_60lyfuu',
  EMAILJS_MARKETING_TEMPLATE_ID: 'template_1gpdcuq'
};
