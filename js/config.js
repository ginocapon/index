/**
 * RIGHETTO IMMOBILIARE — Configurazione Servizi Esterni
 *
 * Istruzioni:
 * 1. FORMSPREE: Registrati su https://formspree.io → Crea un form → Copia il Form ID
 * 2. EMAILJS: Registrati su https://www.emailjs.com → Crea servizio email → Crea template
 */

const SERVIZI_CONFIG = {
  // ── FORMSPREE ──────────────────────────────────────────
  // Ricevi un'email ogni volta che qualcuno compila il form di contatto
  // Vai su https://formspree.io → New Form → copia l'ID (es: "xrgjayzk")
  FORMSPREE_ID: 'IL_TUO_FORM_ID',

  // ── EMAILJS (sostituto di Brevo) ───────────────────────
  // 200 email/mese gratis — per notifiche e newsletter
  // Vai su https://www.emailjs.com → Registrati gratis
  // 1. Email Services → Add New Service (es. Gmail) → copia Service ID
  // 2. Email Templates → Create New Template → copia Template ID
  // 3. Account → copia la Public Key
  EMAILJS_PUBLIC_KEY: '',
  EMAILJS_SERVICE_ID: '',
  EMAILJS_TEMPLATE_ID: '',

  // ── EMAILJS MARKETING (per invio landing page) ────────
  // Crea un SECONDO template su EmailJS per le email marketing
  // Variabili template: {{to_email}}, {{to_name}}, {{title}}, {{message}}
  // Se vuoto, usa lo stesso EMAILJS_TEMPLATE_ID
  EMAILJS_MARKETING_TEMPLATE_ID: ''
};
