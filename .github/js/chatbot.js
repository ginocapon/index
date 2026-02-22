/**
 * RIGHETTO IMMOBILIARE — Chatbot Universale
 * Versione 2.0 — Febbraio 2026
 * Include: stima prezzi, ricerca immobili, form contatto, FAQ
 * Dati prezzi: FIAIP Padova, Immobiliare.it, Idealista 2025-2026
 */

(function() {
'use strict';

// ══════════════════════════════════════════════
// CONFIG
// ══════════════════════════════════════════════
const SUPABASE_URL = 'https://qwkwkemuabfwvwuqrxlu.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3a3drZW11YWJmd3Z3dXFyeGx1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE1OTk5NjEsImV4cCI6MjA4NzE3NTk2MX0.JxEYiWVPEOiwjZtbWAZRlMUdKXcupjw7filvrERCiqc';

// ══════════════════════════════════════════════
// DATABASE PREZZI — PROVINCIA DI PADOVA 2025-2026
// Fonte: FIAIP Padova, Immobiliare.it, Idealista, OMI Agenzia Entrate
// ══════════════════════════════════════════════
const PREZZI_COMUNI = {
  // PADOVA CITTÀ — zona per zona
  'padova centro storico':     { app: 3500, villa: 4200, villa_bif: 3850, capannone: 900, terreno_edif: 650, terreno_agr: 9 },
  'padova prato della valle':  { app: 3200, villa: 3840, villa_bif: 3520, capannone: 850, terreno_edif: 580, terreno_agr: 8 },
  'padova savonarola':         { app: 2800, villa: 3360, villa_bif: 3080, capannone: 750, terreno_edif: 480, terreno_agr: 7 },
  'padova arcella':            { app: 1800, villa: 2160, villa_bif: 1980, capannone: 600, terreno_edif: 320, terreno_agr: 5 },
  'padova guizza':             { app: 2000, villa: 2400, villa_bif: 2200, capannone: 620, terreno_edif: 340, terreno_agr: 5 },
  'padova nord':               { app: 1700, villa: 2040, villa_bif: 1870, capannone: 580, terreno_edif: 290, terreno_agr: 4 },
  'padova est':                { app: 1900, villa: 2280, villa_bif: 2090, capannone: 600, terreno_edif: 310, terreno_agr: 5 },
  'padova':                    { app: 2500, villa: 3000, villa_bif: 2750, capannone: 720, terreno_edif: 450, terreno_agr: 6 },

  // COMUNI PRIMA CINTURA
  'abano terme':               { app: 2100, villa: 2520, villa_bif: 2310, capannone: 650, terreno_edif: 380, terreno_agr: 5 },
  'montegrotto terme':         { app: 1900, villa: 2280, villa_bif: 2090, capannone: 600, terreno_edif: 350, terreno_agr: 5 },
  'albignasego':               { app: 1900, villa: 2280, villa_bif: 2090, capannone: 600, terreno_edif: 300, terreno_agr: 4 },
  'selvazzano dentro':         { app: 1850, villa: 2220, villa_bif: 2035, capannone: 600, terreno_edif: 300, terreno_agr: 4 },
  'noventa padovana':          { app: 1850, villa: 2220, villa_bif: 2035, capannone: 580, terreno_edif: 290, terreno_agr: 4 },
  'vigonza':                   { app: 1700, villa: 2040, villa_bif: 1870, capannone: 560, terreno_edif: 270, terreno_agr: 4 },
  'rubano':                    { app: 1900, villa: 2280, villa_bif: 2090, capannone: 600, terreno_edif: 310, terreno_agr: 4 },
  'limena':                    { app: 1700, villa: 2040, villa_bif: 1870, capannone: 560, terreno_edif: 280, terreno_agr: 4 },
  'cadoneghe':                 { app: 1750, villa: 2100, villa_bif: 1925, capannone: 560, terreno_edif: 280, terreno_agr: 4 },
  'saccolongo':                { app: 1750, villa: 2100, villa_bif: 1925, capannone: 570, terreno_edif: 280, terreno_agr: 4 },
  'ponte san nicolo':          { app: 1650, villa: 1980, villa_bif: 1815, capannone: 540, terreno_edif: 260, terreno_agr: 4 },
  'maserà di padova':          { app: 1650, villa: 1980, villa_bif: 1815, capannone: 540, terreno_edif: 260, terreno_agr: 4 },
  'casalserugo':               { app: 1500, villa: 1800, villa_bif: 1650, capannone: 500, terreno_edif: 230, terreno_agr: 3 },
  'veggiano':                  { app: 1600, villa: 1920, villa_bif: 1760, capannone: 520, terreno_edif: 250, terreno_agr: 4 },
  'mestrino':                  { app: 1700, villa: 2040, villa_bif: 1870, capannone: 550, terreno_edif: 270, terreno_agr: 4 },
  'cervarese santa croce':     { app: 1550, villa: 1860, villa_bif: 1705, capannone: 510, terreno_edif: 240, terreno_agr: 4 },

  // AREA NORD — CAMPOSAMPIERO
  'camposampiero':             { app: 1600, villa: 1920, villa_bif: 1760, capannone: 550, terreno_edif: 270, terreno_agr: 4 },
  'loreggia':                  { app: 1500, villa: 1800, villa_bif: 1650, capannone: 500, terreno_edif: 240, terreno_agr: 3 },
  'san giorgio delle pertiche':{ app: 1450, villa: 1740, villa_bif: 1595, capannone: 490, terreno_edif: 230, terreno_agr: 3 },
  'villanova di camposampiero': { app: 1500, villa: 1800, villa_bif: 1650, capannone: 500, terreno_edif: 240, terreno_agr: 3 },
  'trebaseleghe':              { app: 1600, villa: 1920, villa_bif: 1760, capannone: 540, terreno_edif: 260, terreno_agr: 4 },
  'piombino dese':             { app: 1450, villa: 1740, villa_bif: 1595, capannone: 490, terreno_edif: 220, terreno_agr: 3 },
  'borgoricco':                { app: 1550, villa: 1860, villa_bif: 1705, capannone: 510, terreno_edif: 250, terreno_agr: 3 },
  'santa giustina in colle':   { app: 1400, villa: 1680, villa_bif: 1540, capannone: 480, terreno_edif: 210, terreno_agr: 3 },
  'massanzago':                { app: 1500, villa: 1800, villa_bif: 1650, capannone: 500, terreno_edif: 240, terreno_agr: 3 },

  // AREA CITTADELLA
  'cittadella':                { app: 3200, villa: 3840, villa_bif: 3520, capannone: 750, terreno_edif: 500, terreno_agr: 7 },
  'san martino di lupari':     { app: 1800, villa: 2160, villa_bif: 1980, capannone: 580, terreno_edif: 290, terreno_agr: 4 },
  'carmignano di brenta':      { app: 1700, villa: 2040, villa_bif: 1870, capannone: 550, terreno_edif: 270, terreno_agr: 4 },
  'tombolo':                   { app: 1600, villa: 1920, villa_bif: 1760, capannone: 520, terreno_edif: 250, terreno_agr: 3 },
  'galliera veneta':           { app: 1650, villa: 1980, villa_bif: 1815, capannone: 540, terreno_edif: 260, terreno_agr: 3 },
  'fontaniva':                 { app: 1550, villa: 1860, villa_bif: 1705, capannone: 510, terreno_edif: 240, terreno_agr: 3 },
  'gazzo padovano':            { app: 1300, villa: 1560, villa_bif: 1430, capannone: 450, terreno_edif: 200, terreno_agr: 3 },
  'onara':                     { app: 1300, villa: 1560, villa_bif: 1430, capannone: 440, terreno_edif: 190, terreno_agr: 3 },
  'curtarolo':                 { app: 1600, villa: 1920, villa_bif: 1760, capannone: 530, terreno_edif: 260, terreno_agr: 3 },

  // AREA ESTE-MONTAGNANA
  'este':                      { app: 1100, villa: 1320, villa_bif: 1210, capannone: 450, terreno_edif: 200, terreno_agr: 3 },
  'montagnana':                { app: 950,  villa: 1140, villa_bif: 1045, capannone: 400, terreno_edif: 170, terreno_agr: 3 },
  'merlara':                   { app: 900,  villa: 1080, villa_bif: 990,  capannone: 380, terreno_edif: 160, terreno_agr: 2 },
  'saletto':                   { app: 880,  villa: 1056, villa_bif: 968,  capannone: 370, terreno_edif: 155, terreno_agr: 2 },
  'casale di scodosia':        { app: 900,  villa: 1080, villa_bif: 990,  capannone: 380, terreno_edif: 160, terreno_agr: 2 },
  'castelbaldo':               { app: 850,  villa: 1020, villa_bif: 935,  capannone: 360, terreno_edif: 150, terreno_agr: 2 },
  'megliadino san fidenzio':   { app: 850,  villa: 1020, villa_bif: 935,  capannone: 360, terreno_edif: 148, terreno_agr: 2 },
  'ospedaletto euganeo':       { app: 1000, villa: 1200, villa_bif: 1100, capannone: 420, terreno_edif: 180, terreno_agr: 3 },
  'ponso':                     { app: 900,  villa: 1080, villa_bif: 990,  capannone: 380, terreno_edif: 160, terreno_agr: 2 },
  'villa estense':             { app: 900,  villa: 1080, villa_bif: 990,  capannone: 380, terreno_edif: 160, terreno_agr: 2 },

  // AREA MONSELICE — COLLI EUGANEI
  'monselice':                 { app: 1050, villa: 1260, villa_bif: 1155, capannone: 440, terreno_edif: 190, terreno_agr: 3 },
  'solesino':                  { app: 1000, villa: 1200, villa_bif: 1100, capannone: 420, terreno_edif: 180, terreno_agr: 3 },
  'baone':                     { app: 1100, villa: 1320, villa_bif: 1210, capannone: 450, terreno_edif: 200, terreno_agr: 3 },
  'arquà petrarca':            { app: 1400, villa: 1680, villa_bif: 1540, capannone: 480, terreno_edif: 250, terreno_agr: 4 },
  'galzignano terme':          { app: 1200, villa: 1440, villa_bif: 1320, capannone: 460, terreno_edif: 220, terreno_agr: 3 },
  'torreglia':                 { app: 1300, villa: 1560, villa_bif: 1430, capannone: 470, terreno_edif: 230, terreno_agr: 3 },
  'rovolon':                   { app: 1250, villa: 1500, villa_bif: 1375, capannone: 460, terreno_edif: 220, terreno_agr: 3 },
  'teolo':                     { app: 1400, villa: 1680, villa_bif: 1540, capannone: 480, terreno_edif: 240, terreno_agr: 4 },
  'cinto euganeo':             { app: 1100, villa: 1320, villa_bif: 1210, capannone: 440, terreno_edif: 200, terreno_agr: 3 },
  'battaglia terme':           { app: 1100, villa: 1320, villa_bif: 1210, capannone: 440, terreno_edif: 195, terreno_agr: 3 },
  'vo\' euganeo':              { app: 1050, villa: 1260, villa_bif: 1155, capannone: 430, terreno_edif: 185, terreno_agr: 3 },

  // AREA PIOVE DI SACCO — SACCISICA
  'piove di sacco':            { app: 1800, villa: 2160, villa_bif: 1980, capannone: 580, terreno_edif: 280, terreno_agr: 4 },
  'correzzola':                { app: 900,  villa: 1080, villa_bif: 990,  capannone: 380, terreno_edif: 155, terreno_agr: 2 },
  'agna':                      { app: 850,  villa: 1020, villa_bif: 935,  capannone: 360, terreno_edif: 150, terreno_agr: 2 },
  'bovolenta':                 { app: 1000, villa: 1200, villa_bif: 1100, capannone: 420, terreno_edif: 175, terreno_agr: 3 },
  'sant\'angelo di piove':     { app: 1500, villa: 1800, villa_bif: 1650, capannone: 500, terreno_edif: 240, terreno_agr: 3 },
  'codevigo':                  { app: 1000, villa: 1200, villa_bif: 1100, capannone: 420, terreno_edif: 175, terreno_agr: 2 },
  'candiana':                  { app: 900,  villa: 1080, villa_bif: 990,  capannone: 380, terreno_edif: 155, terreno_agr: 2 },
  'due carrare':               { app: 1500, villa: 1800, villa_bif: 1650, capannone: 500, terreno_edif: 240, terreno_agr: 3 },
  'terrassa padovana':         { app: 950,  villa: 1140, villa_bif: 1045, capannone: 390, terreno_edif: 160, terreno_agr: 2 },

  // AREA CONSELVE
  'conselve':                  { app: 1150, villa: 1380, villa_bif: 1265, capannone: 460, terreno_edif: 210, terreno_agr: 3 },
  'san pietro viminario':      { app: 1100, villa: 1320, villa_bif: 1210, capannone: 450, terreno_edif: 200, terreno_agr: 3 },
  'arre':                      { app: 1000, villa: 1200, villa_bif: 1100, capannone: 420, terreno_edif: 175, terreno_agr: 3 },
  'pontelongo':                { app: 1050, villa: 1260, villa_bif: 1155, capannone: 430, terreno_edif: 185, terreno_agr: 3 },
  'arzergrande':               { app: 1100, villa: 1320, villa_bif: 1210, capannone: 450, terreno_edif: 195, terreno_agr: 3 },
  'polverara':                 { app: 1100, villa: 1320, villa_bif: 1210, capannone: 450, terreno_edif: 195, terreno_agr: 3 },
  'cartura':                   { app: 1200, villa: 1440, villa_bif: 1320, capannone: 460, terreno_edif: 210, terreno_agr: 3 },

  // AREA ESTE — SUD PADOVANO
  'piacenza d\'adige':         { app: 400,  villa: 480,  villa_bif: 440,  capannone: 300, terreno_edif: 100, terreno_agr: 1 },
  'bagnoli di sopra':          { app: 900,  villa: 1080, villa_bif: 990,  capannone: 380, terreno_edif: 155, terreno_agr: 2 },
  'barbona':                   { app: 850,  villa: 1020, villa_bif: 935,  capannone: 360, terreno_edif: 148, terreno_agr: 2 },
  'campo san martino':         { app: 1500, villa: 1800, villa_bif: 1650, capannone: 500, terreno_edif: 240, terreno_agr: 3 },
  'cervarese':                 { app: 1500, villa: 1800, villa_bif: 1650, capannone: 510, terreno_edif: 240, terreno_agr: 4 },
  'brugine':                   { app: 1200, villa: 1440, villa_bif: 1320, capannone: 460, terreno_edif: 210, terreno_agr: 3 },

  // DEFAULT — media provinciale
  'default':                   { app: 1700, villa: 2040, villa_bif: 1870, capannone: 560, terreno_edif: 280, terreno_agr: 4 }
};

// Moltiplicatori per stato immobile
const MULT_STATO = {
  'nuovo': 1.25,
  'ristrutturato': 1.20,
  'ottimo': 1.10,
  'buono': 1.00,
  'discreto': 0.90,
  'da ristrutturare': 0.75,
  'grezzo': 0.65
};

// Moltiplicatori per tipologia specifica
const MULT_TIPOLOGIA = {
  'appartamento': 1.00,
  'bilocale': 1.05,
  'trilocale': 1.00,
  'monolocale': 1.10,
  'attico': 1.35,
  'mansarda': 1.10,
  'villa': 1.20,
  'villa singola': 1.20,
  'villa unifamiliare': 1.22,
  'villa bifamiliare': 1.10,
  'bifamiliare': 1.10,
  'villetta': 1.10,
  'duplex': 1.08,
  'rustico': 0.90,
  'cascina': 0.85
};

// ══════════════════════════════════════════════
// FAQ E RISPOSTE PREDEFINITE
// ══════════════════════════════════════════════
const FAQ_DATA = [
  {
    k: ['orari', 'apertura', 'chiuso', 'aperto', 'quando'],
    r: '🕐 **Orari Righetto Immobiliare**\nLunedì–Venerdì: 9:00–13:00 / 15:00–19:00\nSabato: 9:00–12:30\nDomenica: Chiuso\n\n📞 Tel: +39 049 000 0000\n📧 info@righettoimmobiliare.it'
  },
  {
    k: ['dove', 'sede', 'indirizzo', 'ufficio', 'trovare'],
    r: '📍 **Righetto Immobiliare**\nVia Roma, 1 — 35100 Padova\n\nSiamo nel centro di Padova, facilmente raggiungibili con i mezzi pubblici (tram linea 1, fermata Piazza Garibaldi).'
  },
  {
    k: ['commissione', 'provvigione', 'costo', 'quanto costa', 'spesa', 'percentuale'],
    r: '💰 **Provvigioni Righetto Immobiliare**\n\n**Vendita:**\n• Acquirente: 3% + IVA (min. €2.500)\n• Venditore: 3% + IVA (min. €2.500)\n\n**Affitto:**\n• Un mese di canone + IVA\n\nTutte le nostre provvigioni includono: valutazione, fotografia professionale, virtual tour 360°, gestione pratiche.'
  },
  {
    k: ['valutazione', 'valutare', 'stima', 'vale', 'valore', 'quanto vale'],
    r: '🏠 **Stima del tuo immobile**\n\nPosso fornirti una **stima automatica** basata sui dati di mercato 2025-2026!\n\nDimmi:\n1. Il **comune** (es. Padova, Abano, Cittadella...)\n2. La **tipologia** (appartamento, villa, capannone...)\n3. I **metri quadri**\n4. Lo **stato** (nuovo, buono, da ristrutturare...)\n\nEsempio: *"Stima appartamento 80mq a Selvazzano in buono stato"*'
  },
  {
    k: ['foto', 'fotografie', 'fotografo', 'servizio fotografico'],
    r: '📸 **Servizio Fotografico Professionale**\n\nOgni immobile riceve:\n• Foto professionali con reflex\n• Post-produzione colori\n• Virtual Tour 360° con Pannellum\n• Video YouTube\n• Planimetrie CAD\n\nTutto **incluso** nel nostro servizio!'
  },
  {
    k: ['mutuo', 'finanziamento', 'banca', 'prestito', 'rate'],
    r: '🏦 **Consulenza Mutuo**\n\nOffriamo consulenza gratuita per il mutuo:\n• Analisi della tua situazione finanziaria\n• Confronto offerte da 10+ banche\n• Supporto pratiche notarili\n\nContattaci per un appuntamento!'
  },
  {
    k: ['vendere', 'vendita', 'mettere in vendita', 'affidare'],
    r: '🏷️ **Vuoi vendere il tuo immobile?**\n\nEcco i nostri passi:\n1. **Valutazione gratuita** — veniamo da te senza impegno\n2. **Foto + Virtual Tour 360°** — valorizzazione massima\n3. **Pubblicazione** — Idealista, Immobiliare.it, sito nostro\n4. **Gestione visite** — noi organizziamo tutto\n5. **Trattativa + Rogito** — ti assistiamo fino alla firma\n\n👉 Vuoi un appuntamento gratuito?'
  },
  {
    k: ['affittare', 'affitto', 'mettere in affitto', 'locazione'],
    r: '🔑 **Affittare il tuo immobile**\n\nGestiamo:\n• Selezione inquilini (referenze, busta paga)\n• Contratti di locazione (4+4, transitorio, studenti)\n• Deposito cauzionale\n• Assistenza post-affitto\n\n📞 Chiamaci per un incontro gratuito!'
  },
  {
    k: ['documenti', 'ape', 'certificato', 'pratiche', 'catasto'],
    r: '📋 **Documenti per la vendita**\n\nServiranno:\n• APE (Attestato Prestazione Energetica)\n• Planimetria catastale aggiornata\n• Atto di provenienza\n• Dichiarazione di abitabilità\n• Conformità impianti\n\nNon preoccuparti — ti aiutiamo a raccogliere tutto!'
  }
];

// ══════════════════════════════════════════════
// CHATBOT ENGINE
// ══════════════════════════════════════════════
class RighettoChat {
  constructor() {
    this.messages = [];
    this.state = 'idle'; // idle | stima_comune | stima_tipo | stima_mq | stima_stato | contatto_nome | contatto_email | contatto_tel | contatto_note
    this.stimaData = {};
    this.contattoPending = null;
    this.isOpen = false;
    this.supabase = null;
    this.initSupabase();
  }

  async initSupabase() {
    if (window.supabase && window.supabase.createClient) {
      this.supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
    }
  }

  // ────── STIMA PREZZO ──────
  stimaPrezzo(comune, tipologia, mq, stato) {
    const comuneKey = this.normalizeKey(comune);
    const prezziZona = PREZZI_COMUNI[comuneKey] || PREZZI_COMUNI['default'];

    let prezzoBase;
    const tipoNorm = this.normalizeKey(tipologia);

    if (tipoNorm.includes('capannone') || tipoNorm.includes('magazzino') || tipoNorm.includes('industriale')) {
      prezzoBase = prezziZona.capannone;
    } else if (tipoNorm.includes('terreno agric') || tipoNorm.includes('agricol')) {
      return {
        min: Math.round(prezziZona.terreno_agr * mq * 0.85),
        max: Math.round(prezziZona.terreno_agr * mq * 1.15),
        medio: Math.round(prezziZona.terreno_agr * mq),
        euromq: prezziZona.terreno_agr,
        unita: '€/mq (terreno agricolo)'
      };
    } else if (tipoNorm.includes('terreno edif') || tipoNorm.includes('lotto') || tipoNorm.includes('edificab')) {
      return {
        min: Math.round(prezziZona.terreno_edif * mq * 0.85),
        max: Math.round(prezziZona.terreno_edif * mq * 1.15),
        medio: Math.round(prezziZona.terreno_edif * mq),
        euromq: prezziZona.terreno_edif,
        unita: '€/mq (terreno edificabile)'
      };
    } else if (tipoNorm.includes('villa') && tipoNorm.includes('bif') || tipoNorm.includes('bifam')) {
      prezzoBase = prezziZona.villa_bif;
    } else if (tipoNorm.includes('villa') || tipoNorm.includes('singol') || tipoNorm.includes('unifam')) {
      prezzoBase = prezziZona.villa;
    } else {
      prezzoBase = prezziZona.app; // default appartamento
    }

    // Applica moltiplicatore tipologia
    let multTipo = 1.0;
    for (const [key, val] of Object.entries(MULT_TIPOLOGIA)) {
      if (tipoNorm.includes(key)) { multTipo = val; break; }
    }

    // Applica moltiplicatore stato
    let multStato = 1.0;
    if (stato) {
      const statoNorm = this.normalizeKey(stato);
      for (const [key, val] of Object.entries(MULT_STATO)) {
        if (statoNorm.includes(key)) { multStato = val; break; }
      }
    }

    // Correttivo di scala (immobili grandi hanno €/mq leggermente inferiore)
    let multScala = 1.0;
    if (mq > 200) multScala = 0.92;
    else if (mq > 150) multScala = 0.96;
    else if (mq < 40) multScala = 1.10;
    else if (mq < 60) multScala = 1.05;

    const euromq = Math.round(prezzoBase * multTipo * multStato * multScala);
    const medio = Math.round(euromq * mq);
    return {
      min: Math.round(medio * 0.88),
      max: Math.round(medio * 1.12),
      medio,
      euromq,
      unita: '€/mq'
    };
  }

  normalizeKey(s) {
    return s.toLowerCase().trim()
      .replace(/à/g,'a').replace(/è|é/g,'e').replace(/ì/g,'i')
      .replace(/ò/g,'o').replace(/ù/g,'u')
      .replace(/[^a-z0-9\s']/g,'').replace(/\s+/g,' ');
  }

  formatPrice(n) {
    return new Intl.NumberFormat('it-IT', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(n);
  }

  // ────── RICERCA IMMOBILI CORRELATI ──────
  async cercaImmobiliCorrelati(tipo, mqTarget) {
    if (!this.supabase) return [];
    const mqMin = Math.round(mqTarget * 0.80);
    const mqMax = Math.round(mqTarget * 1.20);
    try {
      let q = this.supabase.from('immobili').select('*')
        .eq('attivo', true).eq('venduto', false)
        .gte('superficie', mqMin).lte('superficie', mqMax)
        .limit(3);
      if (tipo && !tipo.includes('terreno') && !tipo.includes('capannone')) {
        q = q.not('tipologia', 'eq', 'capannone').not('tipologia', 'eq', 'terreno');
      }
      const { data } = await q;
      return data || [];
    } catch { return []; }
  }

  // ────── SALVA RICHIESTA ──────
  async salvaRichiesta(dati) {
    if (!this.supabase) return false;
    try {
      await this.supabase.from('richieste').insert([{
        nome: dati.nome,
        email: dati.email,
        telefono: dati.telefono,
        messaggio: dati.note || dati.messaggio,
        provenienza: 'chatbot',
        letto: false,
        created_at: new Date().toISOString()
      }]);
      return true;
    } catch { return false; }
  }

  // ────── ELABORA MESSAGGIO ──────
  async process(userMsg) {
    const msg = userMsg.trim();
    const low = msg.toLowerCase();

    // ── STATO: raccolta dati stima ──
    if (this.state === 'stima_comune') {
      this.stimaData.comune = msg;
      this.state = 'stima_tipo';
      return '🏠 **Tipologia?**\nEs: appartamento, villa, bifamiliare, attico, capannone, terreno edificabile, terreno agricolo...';
    }

    if (this.state === 'stima_tipo') {
      this.stimaData.tipo = msg;
      this.state = 'stima_mq';
      return '📐 **Quanti metri quadri?**\nInserisci solo il numero (es: 85)';
    }

    if (this.state === 'stima_mq') {
      const n = parseFloat(msg.replace(/[^0-9,.]/g, '').replace(',', '.'));
      if (isNaN(n) || n < 1) return '❌ Inserisci un numero valido (es: 85)';
      this.stimaData.mq = n;
      this.state = 'stima_stato';
      return '🔧 **Stato dell\'immobile?**\nnuovo · ristrutturato · ottimo · buono · discreto · da ristrutturare';
    }

    if (this.state === 'stima_stato') {
      this.stimaData.stato = msg;
      this.state = 'idle';
      return await this.completaStima();
    }

    // ── STATO: raccolta form contatto ──
    if (this.state === 'contatto_nome') {
      this.contattoPending.nome = msg;
      this.state = 'contatto_email';
      return '📧 **Email:**';
    }
    if (this.state === 'contatto_email') {
      this.contattoPending.email = msg;
      this.state = 'contatto_tel';
      return '📞 **Telefono:**';
    }
    if (this.state === 'contatto_tel') {
      this.contattoPending.telefono = msg;
      this.state = 'contatto_note';
      return '💬 **Come possiamo aiutarti?** (puoi anche scrivere "skip"):';
    }
    if (this.state === 'contatto_note') {
      this.contattoPending.note = msg === 'skip' ? '' : msg;
      this.state = 'idle';
      return await this.inviaRichiesta();
    }

    // ── INTENT DETECTION ──

    // Stima diretta inline (es: "stima appartamento 85mq a Padova buono stato")
    const stimaInline = this.parseStimInline(msg);
    if (stimaInline) {
      this.stimaData = stimaInline;
      if (!stimaInline.stato) {
        this.state = 'stima_stato';
        return `📍 Perfetto! Ho trovato: **${stimaInline.tipo}**, **${stimaInline.mq} mq**, **${stimaInline.comune}**.\n\n🔧 **Stato dell\'immobile?**\nnuovo · ristrutturato · ottimo · buono · discreto · da ristrutturare`;
      }
      return await this.completaStima();
    }

    // Stima guidata
    if (/stim|valut|vale|valore|prezzo|quanto.*cost|calcol/.test(low)) {
      this.state = 'stima_comune';
      this.stimaData = {};
      return '🏠 **Stima Valore Immobile** — Provincia di Padova\n\nIn quale **comune** si trova l\'immobile?\n*(Es: Padova, Abano Terme, Cittadella, Monselice...)*';
    }

    // Contatto
    if (/contatt|chiamat|appuntam|richiama|visita|veder|incontr|form/.test(low)) {
      this.state = 'contatto_nome';
      this.contattoPending = { provenienza: 'chatbot' };
      return '👋 Ottimo! Ti ricontatteremo al più presto.\n\n**Come ti chiami?** (Nome e Cognome)';
    }

    // Ricerca immobili
    if (/cerca|trov|immobi|annunci|vedete|avete|list/.test(low)) {
      return this.rispostaRicerca(low);
    }

    // FAQ
    for (const faq of FAQ_DATA) {
      if (faq.k.some(k => low.includes(k))) {
        return faq.r;
      }
    }

    // Saluto
    if (/^(ciao|salve|buongiorno|buonasera|hey|hi|hello)/.test(low)) {
      return '👋 Ciao! Sono l\'assistente di **Righetto Immobiliare**.\n\nPosso aiutarti con:\n• 💰 **Stima valore** del tuo immobile\n• 🔍 **Ricerca immobili** in vendita/affitto\n• 📋 Info su **vendita**, **acquisto**, **affitto**\n• 📞 **Contattare** un agente\n\nCome posso aiutarti?';
    }

    // Default
    return '🤔 Non ho capito bene. Prova con:\n\n• **"Stima appartamento 80mq a Padova"**\n• **"Cerca bilocale in affitto"**\n• **"Voglio essere contattato"**\n• **"Orari e contatti"**';
  }

  // ────── PARSING INLINE ──────
  parseStimInline(msg) {
    const low = msg.toLowerCase();
    // es: "stima/valuta [tipo] [N]mq a/in [comune] [stato]"
    const rTipo = /(appartamento|bilocale|trilocale|monolocale|attico|villa|villetta|bifamiliare|duplex|capannone|terreno|rustico|mansarda)/i;
    const rMq = /(\d+[\.,]?\d*)\s*(mq|m2|m²|metri)/i;
    const rComune = /(?:a|in|nel comune di|a)\s+([a-zàèéìòù\s]+?)(?:\s+(?:buono|ottimo|nuovo|discreto|ristrutturato|da ristrutturare|grezzo)|$)/i;
    const rStato = /(nuovo|ristrutturato|ottimo|buono|discreto|da ristrutturare|grezzo)/i;

    const tipo = (low.match(rTipo) || [])[1];
    const mqMatch = low.match(rMq);
    const mq = mqMatch ? parseFloat(mqMatch[1].replace(',', '.')) : null;
    const comuneMatch = msg.match(rComune);
    const comune = comuneMatch ? comuneMatch[1].trim() : null;
    const stato = (low.match(rStato) || [])[1];

    if (tipo && mq && comune) return { tipo, mq, comune, stato: stato || null };
    return null;
  }

  // ────── COMPLETA STIMA ──────
  async completaStima() {
    const { comune, tipo, mq, stato } = this.stimaData;
    const stima = this.stimaPrezzo(comune, tipo, mq, stato);
    const comuni_validi = Object.keys(PREZZI_COMUNI).filter(k => k !== 'default');
    const trovato = comuni_validi.find(k => this.normalizeKey(comune).includes(k) || k.includes(this.normalizeKey(comune)));

    let msg = `📊 **STIMA DI MERCATO** *(dati 2025–2026)*\n\n`;
    msg += `📍 ${comune.charAt(0).toUpperCase() + comune.slice(1)}\n`;
    msg += `🏠 ${tipo} — ${mq} mq${stato ? ` — ${stato}` : ''}\n\n`;
    msg += `┌─────────────────────────────────┐\n`;
    msg += `│  **Valore stimato**              │\n`;
    msg += `│  Min: **${this.formatPrice(stima.min)}**        │\n`;
    msg += `│  ➡️  **${this.formatPrice(stima.medio)}** *(medio)*  │\n`;
    msg += `│  Max: **${this.formatPrice(stima.max)}**        │\n`;
    msg += `│  Prezzo/mq: ~${this.formatPrice(stima.euromq)}/mq     │\n`;
    msg += `└─────────────────────────────────┘\n\n`;
    msg += `⚠️ *Stima indicativa basata sui prezzi medi di mercato. Per una valutazione ufficiale gratuita a casa tua, contatta un nostro agente.*\n\n`;

    if (!trovato) {
      msg += `📌 *Non ho dati specifici per "${comune}" — ho usato la media provinciale.*\n\n`;
    }

    // Cerca immobili correlati
    const correlati = await this.cercaImmobiliCorrelati(tipo, mq);
    if (correlati.length > 0) {
      msg += `---\n🔍 **Immobili simili disponibili:**\n\n`;
      for (const imm of correlati) {
        const prezzo = imm.prezzo ? this.formatPrice(imm.prezzo) : 'Su richiesta';
        msg += `• **${imm.titolo}** — ${imm.superficie || '?'}mq — ${prezzo}\n`;
        if (imm.comune) msg += `  📍 ${imm.comune}\n`;
        msg += `  👉 [Vedi scheda](/immobile.html?id=${imm.id})\n\n`;
      }
    } else {
      msg += `---\n💬 **Vuoi essere contattato da un nostro agente** per una valutazione ufficiale gratuita?`;
    }

    return msg;
  }

  // ────── RISPOSTA RICERCA ──────
  rispostaRicerca(low) {
    let tipo = 'vendita';
    if (/affitto|locare|locazione/.test(low)) tipo = 'affitto';
    return `🔍 **Cerca Immobili**\n\nPuoi cercare direttamente nella pagina [Immobili](/immobili.html) con filtri avanzati per:\n• Tipo operazione (vendita/affitto)\n• Tipologia (appartamento, villa...)\n• Zona/Comune\n• Superficie\n• Prezzo\n\n👉 [Vai agli immobili](/immobili.html?tipo=${tipo})\n\nOppure dimmi cosa cerchi e ti aiuto!`;
  }

  // ────── INVIA RICHIESTA ──────
  async inviaRichiesta() {
    const ok = await this.salvaRichiesta(this.contattoPending);
    if (ok) {
      return '✅ **Richiesta inviata!**\n\nUn nostro agente ti contatterà entro **24 ore lavorative**.\n\n📞 Urgente? Chiamaci al **+39 049 000 0000**\n\nGrazie per aver scelto Righetto Immobiliare! 🏠';
    } else {
      return '⚠️ Non riesco a salvare la richiesta al momento.\n\n📞 Chiama direttamente: **+39 049 000 0000**\n📧 Email: **info@righettoimmobiliare.it**';
    }
  }
}

// ══════════════════════════════════════════════
// UI CHATBOT — iniettata in ogni pagina
// ══════════════════════════════════════════════
function initChatbotUI() {
  // Previeni doppia inizializzazione
  if (document.getElementById('rig-chat-widget')) return;

  const engine = new RighettoChat();

  const html = `
  <style>
  #rig-chat-widget {
    position: fixed; bottom: 28px; right: 28px; z-index: 9990;
    font-family: 'Montserrat', 'Segoe UI', sans-serif;
  }
  #rig-chat-btn {
    width: 62px; height: 62px; border-radius: 50%;
    background: linear-gradient(135deg, #3A5578, #5C7A9E);
    border: none; cursor: pointer;
    box-shadow: 0 6px 24px rgba(58,85,120,0.45);
    display: flex; align-items: center; justify-content: center;
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative;
  }
  #rig-chat-btn:hover { transform: scale(1.08); box-shadow: 0 10px 32px rgba(58,85,120,0.55); }
  #rig-chat-btn svg { width: 28px; height: 28px; }
  #rig-chat-pulse {
    position: absolute; top: 4px; right: 4px;
    width: 14px; height: 14px; border-radius: 50%;
    background: #CEE08F; border: 2px solid white;
    animation: pulse-chat 2s infinite;
  }
  @keyframes pulse-chat {
    0%,100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.3); opacity: 0.7; }
  }
  #rig-chat-box {
    position: fixed; bottom: 102px; right: 28px;
    width: 370px; max-width: calc(100vw - 40px);
    height: 520px; max-height: calc(100vh - 130px);
    background: #fafaf5; border-radius: 20px;
    box-shadow: 0 20px 60px rgba(30,58,92,0.25);
    display: none; flex-direction: column; overflow: hidden;
    border: 1px solid rgba(58,85,120,0.12);
    animation: slideUpChat 0.25s ease;
  }
  @keyframes slideUpChat {
    from { opacity: 0; transform: translateY(20px) scale(0.97); }
    to { opacity: 1; transform: translateY(0) scale(1); }
  }
  #rig-chat-box.open { display: flex; }
  .chat-header {
    background: linear-gradient(135deg, #3A5578 0%, #5C7A9E 100%);
    padding: 16px 18px; color: white;
    display: flex; align-items: center; gap: 12px;
    border-radius: 20px 20px 0 0; flex-shrink: 0;
  }
  .chat-header-avatar {
    width: 40px; height: 40px; border-radius: 50%;
    background: rgba(206,224,143,0.25);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem; flex-shrink: 0;
    border: 2px solid #CEE08F;
  }
  .chat-header-info { flex: 1; }
  .chat-header-info h4 { font-size: 0.88rem; font-weight: 700; }
  .chat-header-info span {
    font-size: 0.7rem; opacity: 0.8;
    display: flex; align-items: center; gap: 4px;
  }
  .chat-header-info span::before {
    content: ''; width: 7px; height: 7px; border-radius: 50%;
    background: #CEE08F; display: inline-block;
  }
  .chat-close {
    background: rgba(255,255,255,0.15); border: none; color: white;
    width: 30px; height: 30px; border-radius: 8px; cursor: pointer;
    font-size: 1.1rem; display: flex; align-items: center; justify-content: center;
    transition: background 0.2s;
  }
  .chat-close:hover { background: rgba(255,255,255,0.28); }
  .chat-msgs {
    flex: 1; overflow-y: auto; padding: 16px 14px;
    display: flex; flex-direction: column; gap: 10px;
    scrollbar-width: thin; scrollbar-color: #A8C0D6 transparent;
  }
  .chat-msgs::-webkit-scrollbar { width: 4px; }
  .chat-msgs::-webkit-scrollbar-thumb { background: #A8C0D6; border-radius: 4px; }
  .chat-msg { display: flex; gap: 8px; max-width: 90%; }
  .chat-msg.bot { align-self: flex-start; }
  .chat-msg.user { align-self: flex-end; flex-direction: row-reverse; }
  .chat-bubble {
    padding: 10px 14px; border-radius: 14px;
    font-size: 0.82rem; line-height: 1.55;
    white-space: pre-wrap; word-break: break-word;
  }
  .chat-msg.bot .chat-bubble {
    background: white; color: #1E3A5C;
    border: 1px solid rgba(58,85,120,0.1);
    border-radius: 4px 14px 14px 14px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  }
  .chat-msg.user .chat-bubble {
    background: linear-gradient(135deg, #3A5578, #5C7A9E);
    color: white; border-radius: 14px 4px 14px 14px;
  }
  .chat-avatar {
    width: 28px; height: 28px; border-radius: 50%; flex-shrink: 0;
    background: linear-gradient(135deg, #3A5578, #7A9AB8);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; color: white; font-weight: 700;
    align-self: flex-end;
  }
  .chat-typing {
    display: flex; gap: 4px; padding: 10px 14px;
    background: white; border-radius: 4px 14px 14px 14px;
    border: 1px solid rgba(58,85,120,0.1);
    align-self: flex-start; align-items: center;
  }
  .chat-typing span {
    width: 7px; height: 7px; background: #7A9AB8; border-radius: 50%;
    animation: typing-dot 1.2s infinite;
  }
  .chat-typing span:nth-child(2) { animation-delay: 0.2s; }
  .chat-typing span:nth-child(3) { animation-delay: 0.4s; }
  @keyframes typing-dot {
    0%,60%,100% { transform: translateY(0); }
    30% { transform: translateY(-6px); }
  }
  .chat-quick-btns {
    padding: 0 14px 8px; display: flex; flex-wrap: wrap; gap: 6px;
  }
  .chat-qbtn {
    background: white; border: 1.5px solid #A8C0D6; color: #3A5578;
    padding: 5px 11px; border-radius: 20px; font-size: 0.72rem;
    cursor: pointer; font-family: inherit; font-weight: 600;
    transition: all 0.18s; white-space: nowrap;
  }
  .chat-qbtn:hover { background: #3A5578; color: white; border-color: #3A5578; }
  .chat-input-row {
    padding: 12px 14px; border-top: 1px solid rgba(0,0,0,0.06);
    display: flex; gap: 8px; align-items: center; flex-shrink: 0;
    background: white;
  }
  #rig-chat-input {
    flex: 1; padding: 10px 14px;
    border: 1.5px solid #A8C0D6; border-radius: 22px;
    font-family: inherit; font-size: 0.82rem; color: #1E3A5C;
    background: #f5f0e8; outline: none; transition: border-color 0.2s;
    resize: none; max-height: 80px; min-height: 38px;
  }
  #rig-chat-input:focus { border-color: #3A5578; background: white; }
  #rig-chat-send {
    width: 38px; height: 38px; border-radius: 50%;
    background: linear-gradient(135deg, #3A5578, #5C7A9E);
    border: none; cursor: pointer; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    transition: transform 0.2s; color: white;
  }
  #rig-chat-send:hover { transform: scale(1.08); }
  #rig-chat-send svg { width: 17px; height: 17px; }
  .chat-bubble a { color: #CEE08F; text-decoration: underline; }
  .chat-msg.bot .chat-bubble a { color: #3A5578; }
  .chat-bubble strong { font-weight: 700; }
  .chat-bubble code { background: rgba(0,0,0,0.08); padding: 1px 5px; border-radius: 3px; font-family: monospace; }
  @media (max-width: 420px) {
    #rig-chat-box { width: calc(100vw - 20px); right: 10px; bottom: 90px; }
    #rig-chat-widget { right: 14px; bottom: 20px; }
  }
  </style>

  <div id="rig-chat-widget">
    <div id="rig-chat-box" role="dialog" aria-label="Chat assistente">
      <div class="chat-header">
        <div class="chat-header-avatar">🏠</div>
        <div class="chat-header-info">
          <h4>Righetto Immobiliare</h4>
          <span>Online — rispondiamo subito</span>
        </div>
        <button class="chat-close" onclick="rigChat.toggle()" aria-label="Chiudi chat">✕</button>
      </div>
      <div class="chat-msgs" id="rig-chat-msgs"></div>
      <div class="chat-quick-btns" id="rig-quick-btns">
        <button class="chat-qbtn" onclick="rigChat.send('💰 Stima immobile')">💰 Stima immobile</button>
        <button class="chat-qbtn" onclick="rigChat.send('🔍 Cerca immobili')">🔍 Cerca immobili</button>
        <button class="chat-qbtn" onclick="rigChat.send('📞 Voglio essere contattato')">📞 Contattami</button>
        <button class="chat-qbtn" onclick="rigChat.send('🕐 Orari e contatti')">🕐 Orari</button>
        <button class="chat-qbtn" onclick="rigChat.send('💡 Quanto costa vendere?')">💡 Provvigioni</button>
      </div>
      <div class="chat-input-row">
        <textarea id="rig-chat-input" placeholder="Scrivi un messaggio..." rows="1"
          onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();rigChat.sendInput()}"
          oninput="this.style.height='auto';this.style.height=this.scrollHeight+'px'"></textarea>
        <button id="rig-chat-send" onclick="rigChat.sendInput()" aria-label="Invia">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>
          </svg>
        </button>
      </div>
    </div>
    <button id="rig-chat-btn" onclick="rigChat.toggle()" aria-label="Apri chat assistente">
      <svg id="rig-chat-icon" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      </svg>
      <svg id="rig-chat-icon-close" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" style="display:none">
        <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
      </svg>
      <span id="rig-chat-pulse"></span>
    </button>
  </div>`;

  document.body.insertAdjacentHTML('beforeend', html);

  // Funzioni globali chatbot
  window.rigChat = {
    engine,
    open: false,

    toggle() {
      this.open = !this.open;
      const box = document.getElementById('rig-chat-box');
      const iconChat = document.getElementById('rig-chat-icon');
      const iconClose = document.getElementById('rig-chat-icon-close');
      const pulse = document.getElementById('rig-chat-pulse');
      box.classList.toggle('open', this.open);
      iconChat.style.display = this.open ? 'none' : 'block';
      iconClose.style.display = this.open ? 'block' : 'none';
      if (pulse) pulse.style.display = this.open ? 'none' : 'block';
      if (this.open && document.getElementById('rig-chat-msgs').children.length === 0) {
        this.addMsg('bot', '👋 Ciao! Sono l\'assistente di **Righetto Immobiliare**.\n\nPosso aiutarti con:\n• 💰 **Stima valore** del tuo immobile\n• 🔍 **Cerca immobili** in vendita o affitto\n• 📋 Info su servizi e provvigioni\n• 📞 **Contattare** un nostro agente\n\nCome posso aiutarti?');
        document.getElementById('rig-chat-input').focus();
      }
    },

    addMsg(role, text) {
      const msgs = document.getElementById('rig-chat-msgs');
      const div = document.createElement('div');
      div.className = `chat-msg ${role}`;
      const bubble = document.createElement('div');
      bubble.className = 'chat-bubble';
      bubble.innerHTML = this.renderMarkdown(text);
      if (role === 'bot') {
        const av = document.createElement('div');
        av.className = 'chat-avatar'; av.textContent = 'R';
        div.appendChild(av);
      }
      div.appendChild(bubble);
      msgs.appendChild(div);
      msgs.scrollTop = msgs.scrollHeight;
    },

    renderMarkdown(text) {
      return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/`(.*?)`/g, '<code>$1</code>')
        .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>')
        .replace(/^---$/gm, '<hr style="border:none;border-top:1px solid rgba(0,0,0,0.08);margin:8px 0">')
        .replace(/\n/g, '<br>');
    },

    showTyping() {
      const msgs = document.getElementById('rig-chat-msgs');
      const div = document.createElement('div');
      div.className = 'chat-msg bot'; div.id = 'rig-typing';
      const av = document.createElement('div');
      av.className = 'chat-avatar'; av.textContent = 'R';
      div.appendChild(av);
      const t = document.createElement('div');
      t.className = 'chat-typing';
      t.innerHTML = '<span></span><span></span><span></span>';
      div.appendChild(t);
      msgs.appendChild(div);
      msgs.scrollTop = msgs.scrollHeight;
    },

    hideTyping() {
      const t = document.getElementById('rig-typing');
      if (t) t.remove();
    },

    async send(text) {
      if (!text.trim()) return;
      // Nascondi quick buttons dopo il primo messaggio
      document.getElementById('rig-quick-btns').style.display = 'none';
      this.addMsg('user', text);
      this.showTyping();
      const delay = 600 + Math.random() * 600;
      await new Promise(r => setTimeout(r, delay));
      const resp = await this.engine.process(text);
      this.hideTyping();
      this.addMsg('bot', resp);
    },

    sendInput() {
      const inp = document.getElementById('rig-chat-input');
      const val = inp.value.trim();
      if (!val) return;
      inp.value = '';
      inp.style.height = 'auto';
      this.send(val);
    }
  };
}

// ── Auto-inizializzazione ──
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initChatbotUI);
} else {
  initChatbotUI();
}

})();
