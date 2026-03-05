/**
 * RIGHETTO IMMOBILIARE — Configurazione Servizi Esterni
 *
 * Istruzioni:
 * 1. FORMSPREE: Registrati su https://formspree.io → Crea un form → Copia il Form ID
 * 2. BREVO: Registrati su https://brevo.com → Crea lista contatti → Crea form iscrizione
 */

const SERVIZI_CONFIG = {
  // ── FORMSPREE ──────────────────────────────────────────
  // Ricevi un'email ogni volta che qualcuno compila il form di contatto
  // Vai su https://formspree.io → New Form → copia l'ID (es: "xrgjayzk")
  FORMSPREE_ID: 'IL_TUO_FORM_ID',

  // ── BREVO (ex Sendinblue) ──────────────────────────────
  // Newsletter per nuovi immobili e articoli del blog
  BREVO_API_KEY: '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',
  BREVO_LIST_ID: 11,
  BREVO_FORM_URL: '',

  // ── EMAILJS (Email Marketing) ────────────────────────────
  // Vai su https://emailjs.com → Account → Public Key
  // Poi Services → copia Service ID
  // Poi Email Templates → crea template marketing → copia Template ID
  // Variabili template: {{to_email}}, {{to_name}}, {{subject}}, {{message}}
  EMAILJS_PUBLIC_KEY: '',
  EMAILJS_SERVICE_ID: '',
  EMAILJS_MARKETING_TEMPLATE_ID: ''
};
