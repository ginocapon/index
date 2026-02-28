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
// SEO SLUG PER IMMOBILI
// ══════════════════════════════════════════════
function generatePropertySlug(d) {
  if (!d) return '';
  const parts = [
    d.tipologia || d.categoria || 'immobile',
    d.tipo_operazione || 'vendita',
    d.comune || 'padova',
    d.codice || ''
  ];
  return parts.map(p => (p || '').toLowerCase()
    .replace(/[àáâãäå]/g,'a').replace(/[èéêë]/g,'e').replace(/[ìíîï]/g,'i')
    .replace(/[òóôõö]/g,'o').replace(/[ùúûü]/g,'u').replace(/ç/g,'c').replace(/ñ/g,'n')
    .replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')
  ).filter(Boolean).join('-');
}

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
  // ── INFO AGENZIA ──
  {
    k: ['orari', 'apertura', 'chiuso', 'aperto', 'quando'],
    r: '🕐 **Orari Righetto Immobiliare**\nLunedì–Venerdì: 9:00–13:00 / 15:00–19:00\nSabato: 9:00–12:30\nDomenica: Chiuso\n\n📞 Tel: 049 884 3484 · Cell: 348 862 1888\n📧 info@righettoimmobiliare.it'
  },
  {
    k: ['dove', 'sede', 'indirizzo', 'ufficio', 'trovare'],
    r: '📍 **Righetto Immobiliare**\nVia Roma, 96 — 35010 Limena (PD)\n\nSiamo a Limena, alle porte di Padova, con copertura su tutti i 101 comuni della provincia.'
  },
  {
    k: ['commissione', 'provvigione', 'costo agenzia', 'quanto costa', 'spesa agenzia', 'percentuale'],
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
  // ── VENDITA ──
  {
    k: ['vendere', 'vendita', 'mettere in vendita', 'affidare'],
    r: '🏷️ **Vuoi vendere il tuo immobile?**\n\nEcco i nostri passi:\n1. **Valutazione gratuita** — veniamo da te senza impegno\n2. **Foto + Virtual Tour 360°** — valorizzazione massima\n3. **Pubblicazione** — Idealista, Immobiliare.it, sito nostro\n4. **Gestione visite** — noi organizziamo tutto\n5. **Trattativa + Rogito** — ti assistiamo fino alla firma\n\n👉 Vuoi un appuntamento gratuito?'
  },
  {
    k: ['tempo vendita', 'quanto tempo vendere', 'tempistica vendita', 'velocità vendita'],
    r: '⏱️ **Tempi medi di vendita a Padova**\n\nCon la nostra strategia digitale (virtual tour 360°, pubblicazione multi-portale, social media marketing):\n• Centro storico: **45-75 giorni**\n• Prima cintura: **60-90 giorni**\n• Provincia: **90-120 giorni**\n\nUn immobile ben valorizzato si vende più velocemente!'
  },
  {
    k: ['proposta', 'offerta', 'proposta acquisto'],
    r: '📝 **Proposta di acquisto**\n\nLa proposta di acquisto è un\'offerta formale scritta con cui l\'acquirente manifesta la volontà di comprare a un prezzo definito. È accompagnata da un assegno di caparra (generalmente 5-10% del prezzo). Diventa vincolante solo quando il venditore l\'accetta. Noi vi assistiamo in ogni fase della trattativa.'
  },
  {
    k: ['compromesso', 'preliminare', 'contratto preliminare'],
    r: '📋 **Contratto preliminare (compromesso)**\n\nIl preliminare di vendita è un contratto che obbliga le parti al rogito definitivo. Prevede:\n• Caparra confirmatoria (10-20% del prezzo)\n• Termine per il rogito\n• Clausole sospensive (es. mutuo)\n• Registrazione obbligatoria entro 20 giorni\n\nNoi prepariamo e registriamo il preliminare per voi.'
  },
  {
    k: ['rogito', 'atto notarile', 'notaio', 'atto di vendita'],
    r: '🏛️ **Il rogito notarile**\n\nIl rogito è l\'atto definitivo di compravendita stipulato dal notaio. Il notaio è scelto generalmente dall\'acquirente. I costi notarili (onorario + imposte) variano dal 2% al 4% del prezzo di acquisto. Noi vi accompagniamo fino alla firma e al passaggio delle chiavi!'
  },
  // ── ACQUISTO ──
  {
    k: ['prima casa', 'agevolazioni', 'under 36', 'giovani'],
    r: '🏡 **Agevolazioni prima casa**\n\n**Requisiti:**\n• Non possedere altri immobili nello stesso comune\n• Residenza nel comune entro 18 mesi\n• Non aver già usufruito del bonus\n\n**Vantaggi:**\n• Imposta di registro al 2% (anziché 9%)\n• Per under 36: esenzione totale imposte e credito IVA\n• Detrazioni interessi mutuo fino a €4.000/anno'
  },
  {
    k: ['caparra', 'anticipo prezzo', 'acconto prezzo'],
    r: '💶 **Caparra e acconti**\n\n**Caparra confirmatoria:** somma versata al compromesso (10-20%). Se l\'acquirente si ritira, la perde; se il venditore si ritira, deve restituire il doppio.\n\n**Caparra penitenziale:** permette il recesso pagando la caparra come penale.\n\n**Acconto:** semplice anticipo sul prezzo, va restituito se l\'affare non si conclude.'
  },
  {
    k: ['spese acquisto', 'costi acquisto', 'imposte acquisto'],
    r: '🧾 **Costi per l\'acquisto di un immobile**\n\n**Da privato (prima casa):**\n• Imposta di registro: 2% del valore catastale\n• Imposta ipotecaria: €50\n• Imposta catastale: €50\n\n**Da costruttore (con IVA):**\n• IVA: 4% prima casa / 10% seconda casa\n• Imposta di registro: €200\n\n**Sempre:**\n• Notaio: €2.000-€4.000\n• Agenzia: 3% + IVA'
  },
  // ── MUTUO E FINANZIAMENTI ──
  {
    k: ['mutuo', 'finanziamento', 'banca', 'prestito', 'rate'],
    r: '🏦 **Consulenza Mutuo**\n\nOffriamo consulenza gratuita per il mutuo:\n• Analisi della tua situazione finanziaria\n• Confronto offerte da 10+ banche\n• Supporto pratiche notarili\n\nContattaci per un appuntamento!'
  },
  {
    k: ['tasso', 'fisso', 'variabile', 'spread', 'euribor'],
    r: '📊 **Tasso fisso o variabile?**\n\n**Tasso fisso:** rata costante per tutta la durata del mutuo. Ideale per chi vuole sicurezza e stabilità. Attualmente intorno al 2,5-3,5%.\n\n**Tasso variabile:** segue l\'andamento dell\'Euribor. Rata iniziale più bassa ma può crescere. Adatto a chi ha margine di flessibilità.\n\nPossiamo metterti in contatto con i nostri consulenti creditizi.'
  },
  {
    k: ['requisiti mutuo', 'ottenere mutuo', 'quanto posso chiedere', 'rata massima'],
    r: '📋 **Requisiti per ottenere un mutuo**\n\n• La rata non deve superare il **30-35% del reddito** netto mensile\n• Contratto di lavoro indeterminato (o almeno 2 anni di P.IVA)\n• Nessuna segnalazione CRIF/Centrale Rischi\n• Anticipo minimo: **20%** del valore immobile\n\nLe banche finanziano generalmente fino all\'80% del valore di perizia.'
  },
  {
    k: ['surroga', 'sostituzione mutuo', 'portabilità'],
    r: '🔄 **Surroga del mutuo**\n\nLa surroga (o portabilità) permette di trasferire il mutuo a un\'altra banca con condizioni migliori, **senza costi** per il mutuatario. È un diritto previsto dalla Legge Bersani. Conviene quando i tassi di mercato sono più bassi rispetto a quelli del tuo mutuo attuale.'
  },
  // ── AFFITTO E LOCAZIONE ──
  {
    k: ['affittare', 'affitto', 'mettere in affitto', 'locazione'],
    r: '🔑 **Affittare il tuo immobile**\n\nGestiamo:\n• Selezione inquilini (referenze, busta paga)\n• Contratti di locazione (4+4, transitorio, studenti)\n• Deposito cauzionale\n• Assistenza post-affitto\n\n📞 Chiamaci per un incontro gratuito!'
  },
  {
    k: ['contratto affitto', 'tipo contratto', '4+4', '3+2', 'transitorio', 'cedolare'],
    r: '📄 **Tipologie di contratto di locazione**\n\n• **4+4 (libero):** canone concordato liberamente, durata 4 anni rinnovabili\n• **3+2 (concordato):** canone calmierato, vantaggi fiscali per entrambi\n• **Transitorio:** da 1 a 18 mesi, per esigenze temporanee documentate\n• **Studenti:** da 6 a 36 mesi, per universitari\n\n**Cedolare secca:** tassazione sostitutiva al 21% (10% per concordati) — niente IRPEF né imposta di registro.'
  },
  {
    k: ['sfratto', 'morosità', 'inquilino moroso', 'non paga'],
    r: '⚠️ **Sfratto per morosità**\n\nSe l\'inquilino non paga, il procedimento prevede:\n1. Intimazione di sfratto tramite ufficiale giudiziario\n2. Udienza di convalida (il giudice può concedere termine di grazia di 90 giorni)\n3. Esecuzione forzata\n\nI tempi medi in Veneto sono di 6-12 mesi. Noi selezioniamo accuratamente gli inquilini per prevenire queste situazioni.'
  },
  {
    k: ['cauzione', 'deposito cauzionale', 'deposito affitto'],
    r: '💵 **Deposito cauzionale**\n\nIl deposito cauzionale (cauzione) è generalmente pari a **2-3 mensilità** di canone. Viene restituito alla fine del contratto, al netto di eventuali danni. Il proprietario è tenuto a corrispondere gli interessi legali maturati. Noi gestiamo tutta la documentazione.'
  },
  // ── TASSE E IMPOSTE ──
  {
    k: ['imu', 'tasi', 'tassa casa', 'imposta casa'],
    r: '🏛️ **IMU — Imposta Municipale Unica**\n\n• **Prima casa:** ESENTE (tranne categorie A1, A8, A9)\n• **Seconda casa:** aliquota base 0,86% (variabile per comune)\n• **Terreni:** soggetti a IMU salvo esenzioni agricoltura\n\nIl pagamento avviene in 2 rate: acconto (16 giugno) e saldo (16 dicembre). Possiamo aiutarti a calcolare l\'importo esatto.'
  },
  {
    k: ['plusvalenza', 'tassa vendita', 'guadagno vendita'],
    r: '💰 **Plusvalenza sulla vendita**\n\nSe vendi un immobile **entro 5 anni** dall\'acquisto e realizzi un guadagno, devi pagare la tassa sulla plusvalenza. Puoi scegliere:\n• Tassazione IRPEF ordinaria\n• Imposta sostitutiva del **26%**\n\n**Esenzione:** se l\'immobile è stato adibito a prima casa per la maggior parte del periodo.'
  },
  {
    k: ['spese detraibili', 'detrazioni', 'detrazione fiscale', '730'],
    r: '📊 **Detrazioni fiscali legate alla casa**\n\n• **Interessi mutuo prima casa:** detrazione 19% fino a €4.000/anno\n• **Spese notarili mutuo:** detraibili al 19%\n• **Canone affitto:** detrazione per inquilini a basso reddito\n• **Ristrutturazione:** detrazione 50% fino a €96.000\n• **Efficientamento energetico:** detrazione 50-65%\n• **Bonus mobili:** detrazione 50% fino a €5.000'
  },
  // ── DOCUMENTI ──
  {
    k: ['documenti vendita', 'documenti necessari', 'pratiche vendita', 'documentazione immobile'],
    r: '📋 **Documenti per la vendita**\n\nServiranno:\n• APE (Attestato Prestazione Energetica)\n• Planimetria catastale aggiornata\n• Atto di provenienza\n• Visura catastale\n• Certificato di abitabilità/agibilità\n• Conformità urbanistica\n• Conformità impianti\n\nNon preoccuparti — ti aiutiamo a raccogliere tutto!'
  },
  {
    k: ['classe energetica', 'energetica', 'attestato energetico', 'consumo'],
    r: '⚡ **APE — Attestato di Prestazione Energetica**\n\nL\'APE è obbligatorio per vendere o affittare. Classifica l\'immobile da **A4** (migliore) a **G** (peggiore). Ha validità di **10 anni**.\n\nCosto medio: €150-€300. Deve essere redatto da un tecnico abilitato. Noi ci occupiamo di organizzare tutto.'
  },
  {
    k: ['visura', 'ipoteca', 'ipoteche', 'gravami'],
    r: '🔍 **Visure e controlli ipotecari**\n\nPrima di ogni compravendita verifichiamo:\n• **Visura catastale:** dati catastali e proprietà\n• **Visura ipotecaria:** ipoteche, pignoramenti, gravami\n• **Conformità urbanistica:** regolarità edilizia\n• **Certificato stato civile:** per verifiche successorie\n\nTutti i controlli sono inclusi nel nostro servizio.'
  },
  // ── RISTRUTTURAZIONE E BONUS ──
  {
    k: ['ristrutturazione', 'ristrutturare', 'lavori', 'bonus ristrutturazione'],
    r: '🔨 **Bonus ristrutturazione 2025-2026**\n\n• **Detrazione 50%** per prima casa (36% per altri immobili) su spese fino a €96.000\n• Ripartita in **10 rate annuali**\n• Include: manutenzione straordinaria, restauro, risanamento conservativo, ristrutturazione edilizia\n\nPossiamo consigliarti imprese edili di fiducia nella zona di Padova.'
  },
  {
    k: ['ecobonus', 'risparmio energetico', 'cappotto', 'caldaia', 'pompa di calore'],
    r: '🌱 **Ecobonus — Risparmio energetico**\n\n• **Detrazione 50-65%** per interventi di efficientamento:\n  - Cappotto termico\n  - Sostituzione caldaia con condensazione\n  - Pompa di calore\n  - Infissi e serramenti\n  - Pannelli solari termici\n\nGli interventi aumentano la classe energetica e il valore dell\'immobile!'
  },
  {
    k: ['bonus mobili', 'arredamento', 'elettrodomestici'],
    r: '🛋️ **Bonus Mobili 2025-2026**\n\nDetrazione **50%** per l\'acquisto di mobili e grandi elettrodomestici (classe A+) destinati a immobili in ristrutturazione.\n\n• Spesa massima: **€5.000**\n• Ripartita in **10 rate annuali**\n• Requisito: aver avviato una ristrutturazione'
  },
  // ── CONDOMINIO ──
  {
    k: ['condominio', 'spese condominiali', 'amministratore', 'assemblea'],
    r: '🏢 **Spese condominiali**\n\nLe spese condominiali includono:\n• Pulizia e manutenzione parti comuni\n• Ascensore\n• Riscaldamento centralizzato (se presente)\n• Assicurazione fabbricato\n• Fondo cassa\n\nIn vendita, le spese condominiali arretrate restano a carico del venditore. Verifichiamo sempre la situazione condominiale prima del rogito.'
  },
  {
    k: ['tabelle millesimali', 'millesimi', 'ripartizione spese'],
    r: '📊 **Tabelle millesimali**\n\nI millesimi determinano la quota di partecipazione di ogni unità alle spese comuni e al diritto di voto in assemblea. Vengono calcolati in base a superficie, piano, esposizione e luminosità. La modifica richiede l\'unanimità o una sentenza del tribunale.'
  },
  // ── INVESTIMENTI IMMOBILIARI ──
  {
    k: ['investimento', 'investire', 'rendimento', 'rendita', 'reddito'],
    r: '📈 **Investire in immobili a Padova**\n\nI rendimenti medi lordi a Padova:\n• **Appartamenti centro:** 4-5% annuo\n• **Bilocali zona università:** 6-7% annuo\n• **Locali commerciali:** 6-8% annuo\n• **Box/garage:** 5-7% annuo\n\nPadova è una piazza universitaria molto dinamica con forte domanda di affitti. Contattateci per un\'analisi personalizzata.'
  },
  {
    k: ['affitto breve', 'airbnb', 'turistico', 'b&b'],
    r: '🏖️ **Affitti brevi e turistici**\n\nGli affitti brevi (< 30 giorni) sono soggetti a:\n• **Cedolare secca 21%** sui redditi\n• Obbligo di comunicazione alla Questura entro 24h\n• CIR (Codice Identificativo Regionale) obbligatorio\n• Eventuale imposta di soggiorno comunale\n\nAbano Terme e i Colli Euganei offrono ottimi rendimenti turistici.'
  },
  // ── ASTE GIUDIZIARIE ──
  {
    k: ['asta', 'aste', 'giudiziaria', 'tribunale', 'aggiudicazione'],
    r: '⚖️ **Aste giudiziarie immobiliari**\n\nOffriamo assistenza completa:\n• Analisi dell\'immobile e della perizia CTU\n• Verifica ipotecaria e situazione debitoria\n• Sopralluogo e valutazione\n• Preparazione offerta e partecipazione\n• Tutela legale fino al decreto di trasferimento\n\nSpesso è possibile acquistare al **20-40% sotto il valore** di mercato!'
  },
  // ── TERRENI E RURALI ──
  {
    k: ['terreno', 'agricolo', 'edificabile', 'lotto', 'costruire'],
    r: '🌾 **Terreni a Padova e provincia**\n\n**Terreni edificabili:**\n• Prezzo medio provincia: €250-650/mq\n• Verifiche: PRG/PAT comunale, indice di edificabilità, urbanizzazione\n\n**Terreni agricoli:**\n• Prezzo medio: €2-9/mq (zona dipendente)\n• Diritto di prelazione per coltivatori diretti\n\nGestiamo terreni in tutto il Basso Padovano e Colli Euganei.'
  },
  // ── VIRTUAL TOUR ──
  {
    k: ['virtual tour', '360', 'tour virtuale', 'visita virtuale'],
    r: '🎥 **Virtual Tour 360°**\n\nRealizziamo tour virtuali interattivi con:\n• Fotocamere professionali 360°\n• Navigazione fluida stanza per stanza\n• Pubblicazione su sito, YouTube e portali\n• Compatibile smartphone, tablet, PC e visori VR\n\nGli immobili con virtual tour ricevono il **40% di contatti in più** e visite più qualificate!'
  },
  // ── CERTIFICAZIONI E CONFORMITÀ ──
  {
    k: ['conformità urbanistica', 'abuso edilizio', 'abusivismo', 'sanatoria edilizia', 'condono edilizio'],
    r: '🏗️ **Conformità urbanistica e catastale**\n\nPrima della vendita è necessario verificare che:\n• Lo stato di fatto corrisponda alle planimetrie catastali\n• Non ci siano abusi edilizi\n• Eventuali difformità siano sanabili\n\nIn caso di abusi, è possibile presentare una **CILA in sanatoria** (costo medio €1.000-€3.000). Noi vi mettiamo in contatto con tecnici di fiducia.'
  },
  // ── SUCCESSIONE E DONAZIONE ──
  {
    k: ['successione', 'eredità', 'eredi', 'defunto', 'ereditare'],
    r: '⚖️ **Successione immobiliare**\n\nIn caso di eredità:\n• Dichiarazione di successione entro **12 mesi** dal decesso\n• Imposta di successione: 4% (coniuge/figli, franchigia €1M), 6% (fratelli, franchigia €100K), 8% (altri)\n• Voltura catastale obbligatoria\n• Se più eredi: possibilità di vendita con accordo unanime o divisione giudiziale\n\nVi assistiamo anche nella vendita di immobili ereditati.'
  },
  {
    k: ['donazione', 'donare', 'regalare casa'],
    r: '🎁 **Donazione di immobile**\n\nLa donazione richiede atto notarile. Attenzione: un immobile donato può avere **problemi di commerciabilità** perché gli eredi legittimari possono impugnare la donazione entro 20 anni. Molte banche non concedono mutui su immobili donati. Consigliamo sempre di valutare attentamente con un notaio.'
  },
  // ── CONSIGLI PRATICI ──
  {
    k: ['perizia', 'perito', 'perizia bancaria'],
    r: '🔍 **Perizia bancaria**\n\nLa perizia è richiesta dalla banca per concedere il mutuo. Un perito valuta l\'immobile e certifica il valore. Il costo è generalmente di **€250-€400** a carico dell\'acquirente. Se il valore di perizia è inferiore al prezzo, la banca riduce l\'importo finanziabile.'
  },
  {
    k: ['casa nuova', 'costruttore', 'cantiere', 'nuova costruzione'],
    r: '🏗️ **Acquisto da costruttore**\n\n**Vantaggi:**\n• Immobile personalizzabile\n• Classe energetica A o superiore\n• Garanzia decennale\n• IVA 4% prima casa\n\n**Attenzione a:**\n• Fideiussione obbligatoria sugli acconti versati\n• Polizza assicurativa decennale postuma\n• Verificare il capitolato lavori'
  },
  {
    k: ['nuda proprietà', 'usufrutto', 'diritto abitazione'],
    r: '👴 **Nuda proprietà e usufrutto**\n\nLa nuda proprietà è la proprietà senza il diritto di godimento (che resta all\'usufruttuario). Vantaggi per chi compra:\n• Prezzo ridotto del **25-50%** rispetto al valore pieno\n• Investimento a lungo termine\n• IMU a carico dell\'usufruttuario\n\nÈ una formula molto usata per investimento.'
  },
  {
    k: ['garage', 'box', 'posto auto', 'parcheggio'],
    r: '🚗 **Box e posti auto a Padova**\n\nI prezzi medi:\n• **Box singolo centro:** €25.000-€45.000\n• **Box doppio:** €35.000-€60.000\n• **Posto auto coperto:** €15.000-€25.000\n• **Posto auto scoperto:** €8.000-€15.000\n\nSe acquistato come pertinenza della prima casa, gode delle stesse agevolazioni fiscali.'
  },
  // ── PADOVA SPECIFICA ──
  {
    k: ['zona', 'quartiere', 'migliore', 'vivere', 'consiglio zona'],
    r: '📍 **Zone di Padova — Dove conviene acquistare?**\n\n🏆 **Top prezzo/qualità:**\n• Selvazzano, Rubano, Albignasego — ottimi servizi, prezzi accessibili\n• Abano/Montegrotto — termalismo e qualità della vita\n\n🎓 **Per investimento affitto studenti:**\n• Arcella, Portello, zona Stazione\n\n💎 **Premium:**\n• Centro Storico, Prato della Valle, Savonarola\n\nContattaci per una consulenza personalizzata sulla zona ideale per te!'
  },
  {
    k: ['mercato', 'andamento', 'prezzi', 'trend', 'crescita'],
    r: '📊 **Mercato immobiliare Padova 2025-2026**\n\n• Prezzi medi in **leggera crescita** (+2-3% annuo)\n• Forte domanda zona universitaria e prima cintura\n• Cittadella: mercato molto dinamico (~3.200 €/mq)\n• Centro storico stabile sui 3.500 €/mq\n• Colli Euganei: crescita per il turismo\n\nUsa la nostra **stima online** per conoscere il valore nella tua zona!'
  },
  {
    k: ['sara', 'chi sei', 'assistente', 'bot', 'intelligenza artificiale'],
    r: '👋 Ciao! Sono **Sara**, l\'assistente virtuale di Righetto Immobiliare. Sono disponibile **24/7** per rispondere alle tue domande su immobili, prezzi, servizi e procedure. Posso anche fornirti **stime di mercato** per tutti i 101 comuni della provincia di Padova!\n\nSe hai bisogno di parlare con un agente, scrivi *"contattami"* e ti richiamiamo noi.'
  },

  // ═══════════════════════════════════════════════
  // VENDITA — FAQ APPROFONDITE
  // ═══════════════════════════════════════════════
  {
    k: ['valutazione gratuita', 'senza impegno', 'valutazione gratis'],
    r: '✅ **La valutazione gratuita è davvero senza impegno.** Analizziamo il tuo immobile con comparabili reali di mercato e ti forniamo un report dettagliato per decidere se procedere con noi. Nessun vincolo, nessun costo.\n\n📞 Chiama il **049 884 3484** o scrivi *"contattami"* per prenotare.'
  },
  {
    k: ['vendere in fretta', 'vendita rapida', 'vendere veloce padova', 'tempi medi vendita'],
    r: '⏱️ **In media 45-60 giorni** con la nostra strategia multicanale. Riduciamo i tempi grazie a:\n\n• Promozione su portali leader (Immobiliare.it, Idealista, Casa.it)\n• Social geolocalizzati\n• Acquirenti già pre-qualificati nella nostra banca dati\n\nIl 98% dei nostri clienti vende entro i tempi previsti.'
  },
  {
    k: ['foto professionali', 'drone immobiliare', 'video 4k immobile', 'servizio fotografico casa'],
    r: '📸 **Investiamo nella qualità visiva del tuo immobile:**\n\n• Foto professionali con **drone**\n• Virtual tour **360°**\n• Video cinematici **4K**\n• Planimetrie **3D interattive**\n\nTutto incluso, senza anticipo. Un immobile con foto professionali riceve il **40% di contatti in più**.'
  },
  {
    k: ['selezionate acquirenti', 'acquirenti qualificati', 'curiosi', 'qualifica acquirente'],
    r: '🔍 **Selezioniamo rigorosamente ogni acquirente:**\n\n• Verifica capacità economica (pre-approvazione mutuo)\n• Analisi motivazioni e tempistiche\n• Evitiamo curiosi e perditempo\n\nPresentiamo solo acquirenti qualificati e pronti all\'acquisto.'
  },
  {
    k: ['parte legale', 'assistenza fino al rogito', 'assistenza legale vendita', 'accompagnamento rogito'],
    r: '⚖️ **Sì, ti accompagniamo dalla valutazione al passaggio chiavi:**\n\n• Contratto preliminare\n• Coordinamento mutuo acquirente\n• Rapporto con il notaio\n• Volture utenze\n\nTu firmi e non pensi a nulla. Servizio **chiavi in mano**.'
  },
  {
    k: ['immobili lusso', 'lusso', 'prestigio', 'alto spendente', 'christie', 'sotheby'],
    r: '🏛️ **Strategie dedicate per il segmento lusso:**\n\n• Marketing su **Christie\'s** e **Sotheby\'s**\n• Network investitori internazionali\n• Servizio fotografico premium\n• Target alto-spendente mirato\n\nMassima riservatezza e posizionamento esclusivo.'
  },
  {
    k: ['prezzo non raggiunto', 'non si vende', 'sotto prezzo', 'ribasso'],
    r: '📉 **Se non si raggiunge il prezzo valutato**, rinegoziamo la strategia o proponiamo soluzioni alternative come l\'affitto con riscatto. Mai forzature: **il tuo interesse viene prima di tutto**. Adattiamo il piano, non ti abbandoniamo.'
  },
  {
    k: ['esclusiva', 'mandato libero', 'mandato esclusiva', 'incarico'],
    r: '📝 **Offriamo entrambe le opzioni:**\n\n• **Esclusiva** → investimento marketing massimo, tempi più rapidi\n• **Mandato libero** → maggiore libertà\n\nL\'esclusiva ci permette di investire di più nella promozione del tuo immobile, ma rispettiamo sempre la tua scelta.'
  },
  {
    k: ['solo padova', 'zona coperta', 'dove lavorate', 'area operativa'],
    r: '📍 **Copriamo tutta la provincia di Padova e oltre:**\n\n• Padova città e prima cintura\n• Selvazzano, Abano, Montegrotto, Rubano, Limena\n• Monselice, Este, Cittadella, Camposampiero\n• Fino a Vicenza e comuni limitrofi\n\n**101 comuni** nel nostro database prezzi!'
  },
  {
    k: ['esempi venduti', 'portfolio', 'casi studio', 'immobili venduti'],
    r: '🏡 **Sì, sul nostro portfolio online trovi:**\n\n• Casi studio con foto prima/dopo\n• Tempi di vendita reali\n• Prezzi ottenuti\n\nOgni vendita è una storia di successo. Chiedici e ti mostriamo i risultati nella tua zona!'
  },
  {
    k: ['chi paga foto', 'costo foto', 'anticipo foto'],
    r: '💰 **Le foto professionali e il virtual tour li paghiamo noi**, senza anticipo. Investiamo nel tuo immobile come fosse nostro. Paghi solo a vendita conclusa.'
  },
  {
    k: ['home staging', 'staging', 'allestimento'],
    r: '🎨 **Sì, offriamo home staging:**\n\n• **Staging virtuale gratuito** nelle foto (rendering digitale)\n• **Staging fisico opzionale** per immobili vuoti\n\nL\'home staging aumenta la velocità di vendita del **+20%** e il prezzo finale fino al **+5%**.'
  },
  {
    k: ['privacy visite', 'discrezione', 'riservatezza', 'nda'],
    r: '🔒 **Massima discrezione garantita:**\n\n• Registrazione visitatori obbligatoria\n• NDA per immobili sensibili\n• Verifica identità prima di ogni visita\n\nLa tua privacy è una priorità assoluta.'
  },
  {
    k: ['vendita asta', 'asta giudiziaria', 'asta immobiliare'],
    r: '🔨 **Sì, gestiamo vendite all\'asta** con strategie dedicate per massimizzare le offerte mantenendo la riservatezza fino all\'aggiudicazione. Assistenza completa dalla perizia al decreto di trasferimento.'
  },
  {
    k: ['offerta durante esclusiva', 'offerta migliore'],
    r: '📋 **Se ricevi un\'offerta durante l\'esclusiva**, la valutiamo insieme. Se è migliore della nostra strategia, la accettiamo senza penali. Il tuo interesse è sempre al primo posto.'
  },
  {
    k: ['investitori istituzionali', 'family office', 'fondi', 'sgr'],
    r: '🏦 **Sì, collaboriamo con:**\n\n• Family office\n• SGR (Società Gestione Risparmio)\n• Fondi immobiliari\n\nPer immobili da investimento con rendimenti interessanti. Network qualificato e riservato.'
  },
  {
    k: ['valutazione mutuo', 'perizia banca', 'perizia ctu'],
    r: '🏦 **Sì, realizziamo perizie CTU accreditate** per tutte le principali banche: Intesa Sanpaolo, UniCredit, BNL, BPER, Banco BPM. Metodica OMI certificata.'
  },
  {
    k: ['promozione portali', 'immobiliare.it', 'idealista', 'casa.it'],
    r: '🌐 **Promozione multicanale massima:**\n\n• Primo posto organico su **Immobiliare.it**\n• **Idealista** e **Casa.it**\n• Google My Business ottimizzato\n• Social media geolocalizzati\n• La nostra banca dati acquirenti\n\nVisibilità totale per il tuo immobile.'
  },
  {
    k: ['immobili commerciali', 'negozio', 'ufficio', 'capannone vendita'],
    r: '🏢 **Sì, gestiamo immobili commerciali:**\n\n• Negozi e locali\n• Uffici\n• Capannoni e magazzini\n\nStrategie **B2B dedicate** con promozione su canali professionali e network imprenditoriale.'
  },
  {
    k: ['compenso agenzia', 'provvigione sul venduto', 'costo del servizio'],
    r: '💶 **Provvigione solo sul venduto**, percentuale standard di mercato. Trasparente dall\'inizio, concordata nel mandato. **Nessun costo anticipato**, nessuna sorpresa. Paghi solo quando la vendita è conclusa.'
  },

  // ═══════════════════════════════════════════════
  // LOCAZIONI — FAQ
  // ═══════════════════════════════════════════════
  {
    k: ['inquilini solvibili', 'solvibilità', 'garanzia inquilino', 'verifica inquilino'],
    r: '✅ **Verifica solvibilità completa:**\n\n• Buste paga e cedolini\n• Garanzie bancarie\n• Visura K-bis per aziende\n• Scoring solvibilità\n\nSolo inquilini affidabili e verificati.'
  },
  {
    k: ['tipo contratto locazione', 'contratto 4+4', 'contratto 3+2', 'transitorio', 'foresteria'],
    r: '📋 **Gestiamo tutti i tipi di contratto:**\n\n• **4+4** — Libero mercato\n• **3+2** — Canone concordato (vantaggi fiscali)\n• **Transitorio** — Da 1 a 18 mesi\n• **Commerciale** — Per attività\n• **Foresteria** — Per aziende\n• **Affitti brevi** — Turistici\n\nTi consigliamo la formula più vantaggiosa per la tua situazione.'
  },
  {
    k: ['registrazione contratto', 'agenzia entrate', 'registrazione locazione'],
    r: '📄 **Ci occupiamo gratuitamente della registrazione telematica** del contratto all\'Agenzia delle Entrate. Zero burocrazia per te.'
  },
  {
    k: ['airbnb', 'locazioni brevi', 'affitto breve', 'affitto turistico'],
    r: '🏖️ **Gestione completa Airbnb e affitti brevi:**\n\n• Check-in e check-out\n• Pulizie professionali\n• Gestione recensioni\n• Ottimizzazione prezzi dinamici\n• Comunicazione ospiti\n\nMassimizziamo la tua rendita senza pensieri.'
  },
  {
    k: ['inquilino non paga', 'morosità', 'sfratto', 'mancato pagamento'],
    r: '⚠️ **In caso di morosità, attiviamo:**\n\n• Procedura legale rapida\n• Recupero crediti tramite i nostri legali partner\n• Assistenza completa dallo sfratto alla riconsegna\n\nPolizze **affitto sicuro** disponibili per prevenire il problema.'
  },
  {
    k: ['rivalutazione istat', 'adeguamento istat', 'aggiornamento canone'],
    r: '📈 **Calcoliamo e notifichiamo automaticamente** la rivalutazione ISTAT ogni anno. Nessun adeguamento dimenticato, massima tutela del tuo reddito locativo.'
  },
  {
    k: ['scelgo inquilino', 'scelta inquilino', 'ultimo parola'],
    r: '👤 **Sì, hai sempre l\'ultima parola** dopo la nostra qualifica di solvibilità. Ti presentiamo i candidati migliori con tutte le informazioni, tu decidi chi ospitare nel tuo immobile.'
  },
  {
    k: ['immobili ammobiliati', 'arredato affitto', 'inventario'],
    r: '🛋️ **Sì, gestiamo immobili ammobiliati:**\n\n• Inventario iniziale dettagliato con foto\n• Stato di locazione documentato\n• Riconsegna finale verificata\n\nTutela completa del tuo arredamento.'
  },
  {
    k: ['tempo trovare inquilino', 'quanto tempo affittare'],
    r: '⏱️ **Media 18 giorni** per trovare inquilino grazie al doppio canale:\n\n• **Privati** — portali + social\n• **Aziende** — relocation multinazionali\n\nRaggiungiamo il target giusto rapidamente.'
  },
  {
    k: ['contratti expat', 'relocation', 'aziende affitto', 'multinazionali'],
    r: '🌍 **Sì, contratti relocation** con multinazionali e professionisti trasfertisti. Esperienza consolidata con aziende del territorio padovano e veronese. Contratti su misura in italiano e inglese.'
  },
  {
    k: ['polizza affitto sicuro', 'garanzia canone', 'assicurazione affitto'],
    r: '🛡️ **Partnership con compagnie assicurative** per polizze **affitto sicuro**:\n\n• Garanzia canone mensile\n• Copertura morosità\n• Tutela legale inclusa\n\nDormi tranquillo, il canone è garantito.'
  },
  {
    k: ['spese condominiali inquilino', 'chi paga condominio'],
    r: '🏢 **Chiarimento forfettario nel contratto.** Noi verifichiamo i conteggi millesimali e gestiamo la ripartizione corretta tra proprietario e inquilino secondo la legge vigente.'
  },
  {
    k: ['successione locativa', 'passaggio contratto eredi', 'subentro'],
    r: '📋 **Gestiamo il passaggio contratti agli eredi** con comunicazione all\'Agenzia delle Entrate e aggiornamento di tutte le registrazioni. Assistenza completa nella successione locativa.'
  },

  // ═══════════════════════════════════════════════
  // GESTIONE PRELIMINARI — FAQ
  // ═══════════════════════════════════════════════
  {
    k: ['regolarità edilizia', 'verifica edilizia', 'dia edilizia', 'pratiche edilizie pregresse'],
    r: '🏗️ **Verifica completa della regolarità edilizia:**\n\n• Analisi planimetrie catastali\n• Verifica SCIA/DIA\n• Controllo condoni e sanatorie\n• Identificazione eventuali abusi\n\nNessuna sorpresa dopo la firma del preliminare.'
  },
  {
    k: ['vincoli urbanistici', 'prg', 'pgt', 'vincoli edificabilità'],
    r: '📐 **Controlliamo tutti i vincoli urbanistici:**\n\n• Sopralluogo tecnico\n• Visure PRG/PGT\n• Banche dati servitù\n• Vincoli paesaggistici e idrogeologici\n\nSicurezza totale prima di firmare.'
  },
  {
    k: ['vizio occulto', 'vizi nascosti', 'difetto immobile'],
    r: '⚠️ **Tutela contrattuale contro vizi occulti:**\n\n• Clausola rescissoria\n• Caparra confirmatoria risarcitoria automatica\n• Dichiarazioni venditore dettagliate\n\nIl preliminare ti protegge da sorprese.'
  },
  {
    k: ['compromesso bilingue', 'acquirenti stranieri', 'contratto inglese'],
    r: '🌍 **Redigiamo compromessi bilingue** per acquirenti stranieri:\n\n• Italiano/Inglese\n• Italiano/Cinese\n• Italiano/Arabo\n\nAssistenza completa per compravendite internazionali.'
  },
  {
    k: ['mutuo ipotecario', 'sospensione rate', 'preventivo mutuo'],
    r: '🏦 **Assistenza mutui ipotecari completa:**\n\n• Perizia tecnica\n• Preventivo mutuo migliore\n• Sospensione rate se necessario\n• Coordinamento con la banca\n\nTi aiutiamo a ottenere le condizioni migliori.'
  },
  {
    k: ['imposta registro acquisto', 'tasse preliminare', 'imposte atto'],
    r: '💰 **Calcolo esatto delle imposte** e assistenza nel pagamento telematico:\n\n• Imposta di registro\n• Imposta ipotecaria e catastale\n• Simulazione costi totali\n\nTrasparenza totale sui costi fin dall\'inizio.'
  },
  {
    k: ['servitù prediali', 'ipoteche giudiziali', 'visure ipotecarie'],
    r: '🔍 **Verifiche ipotecarie complete:**\n\n• Analisi atti e visure\n• Servitù prediali\n• Ipoteche giudiziali\n• Cancellazioni necessarie\n\nNessun vincolo nascosto: garanzia totale.'
  },
  {
    k: ['clausole penali', 'penale contratto', 'ritiro proposta'],
    r: '⚖️ **Clausole penali personalizzate** su misura per ogni trattativa: tempistiche, ritiro, condizioni sospensive. Ogni clausola è calibrata per proteggere i tuoi interessi specifici.'
  },
  {
    k: ['coordinamento notaio', 'notaio partner', 'lista notai'],
    r: '📋 **Siamo coordinati con tutti i notai** della provincia. Lista notai partner con tariffe dedicate per i nostri clienti. Gestiamo tutti gli appuntamenti e la documentazione.'
  },
  {
    k: ['accollo mutuo', 'passaggio mutuo'],
    r: '🏦 **Gestiamo l\'accollo mutui:**\n\n• Rinegoziazione condizioni\n• Passaggio banca\n• Verifica convenienza\n\nTi seguiamo in ogni aspetto finanziario della compravendita.'
  },
  {
    k: ['donazione', 'divisione ereditaria', 'eredità immobile'],
    r: '👨‍👩‍👧 **Gestiamo donazioni e divisioni ereditarie** con i nostri commercialisti partner per ottimizzazione fiscale:\n\n• Perizie per divisione\n• Analisi donazione vs cessione\n• Calcolo imposte e plusvalenze'
  },
  {
    k: ['apostille', 'legalizzazione', 'rogito internazionale'],
    r: '🌐 **Apostille e legalizzazione atti** per rogiti internazionali. Assistenza completa per acquirenti e venditori esteri con documentazione conforme alle normative internazionali.'
  },

  // ═══════════════════════════════════════════════
  // GESTIONE PATRIMONIO — FAQ
  // ═══════════════════════════════════════════════
  {
    k: ['gestione completa', 'cosa include gestione', 'gestione patrimonio'],
    r: '🏠 **La gestione completa include:**\n\n• Selezione e gestione inquilini\n• Manutenzione ordinaria e straordinaria\n• Pagamenti e rendicontazione\n• Ottimizzazione fiscale\n• Report periodici\n\nTu incassi, noi pensiamo a tutto il resto.'
  },
  {
    k: ['app proprietari', 'dashboard', 'portale proprietario'],
    r: '📱 **Dashboard online per proprietari:**\n\n• Incassi in tempo reale\n• Stato manutenzioni\n• Documenti scaricabili **24/7**\n• Storico pagamenti\n\nControlla il tuo patrimonio ovunque ti trovi.'
  },
  {
    k: ['artigiani', 'rete artigiani', 'manutenzione urgente'],
    r: '🔧 **Rete di 40+ artigiani qualificati** con SLA (tempi di intervento garantiti):\n\n• Idraulici, elettricisti, fabbri\n• Imbianchini, muratori\n• Caldaisti, climatizzatori\n• Pronto intervento h24\n\nInterventi rapidi e prezzi concordati.'
  },
  {
    k: ['redditività portafoglio', 'rendimento immobili', 'analisi rendita'],
    r: '📊 **Report trimestrale di redditività:**\n\n• Yield lordo e netto\n• Benchmark con il mercato\n• Proiezioni a 12-24 mesi\n• Suggerimenti di ottimizzazione\n\nMassimiziamo il rendimento del tuo portafoglio.'
  },
  {
    k: ['ottimizzazione fiscale', 'cedolare secca gestione', 'tasse immobili'],
    r: '📋 **Ottimizzazione carico fiscale:**\n\n• Cedolare secca vs regime ordinario\n• Rivalutazioni OICE\n• Leasing operativo\n• Deduzioni e detrazioni applicabili\n\nRisparmi fiscali concreti sul tuo patrimonio.'
  },
  {
    k: ['manutenzione predittiva', 'check stagionale', 'prevenzione guasti'],
    r: '🔧 **Piani di manutenzione predittiva:**\n\n• Check stagionali programmati\n• Analisi costi/benefici interventi\n• Prevenzione guasti costosi\n\nMeglio prevenire che riparare: risparmi fino al **30%** sui costi di manutenzione.'
  },
  {
    k: ['patrimoni ereditari', 'immobili eredità gestione', 'divisione quote'],
    r: '👨‍👩‍👧 **Gestiamo patrimoni ereditari complessi:**\n\n• Divisioni immobiliari\n• Locazioni pro-quota\n• Gestione contenziosi tra eredi\n• Valorizzazione e vendita concordata\n\nEsperienza trentennale nelle situazioni più delicate.'
  },
  {
    k: ['assicurazione immobile', 'polizza multirischio', 'assicurazione globale'],
    r: '🛡️ **Polizze multirischio** con massimali elevati:\n\n• Incendio e scoppio\n• Danni da acqua\n• Responsabilità civile\n• Furto e atti vandalici\n\nPartnership con le migliori compagnie per coperture complete.'
  },
  {
    k: ['hotel management', 'case vacanze', 'gestione vacanze'],
    r: '🏖️ **Gestione chiavi in mano per case vacanze:**\n\n• Promozione su Booking, Airbnb\n• Check-in/check-out\n• Pulizie e biancheria\n• Manutenzione e assistenza ospiti\n\nRendita passiva garantita sul tuo immobile vacanza.'
  },
  {
    k: ['immobili strumentali', 'leasing immobile', 'cespiti bilancio'],
    r: '🏢 **Gestiamo immobili strumentali per aziende:**\n\n• Leasing finanziario e operativo\n• Rivalutazione cespiti a bilancio\n• Gestione contratti professionali\n\nSoluzioni su misura per il patrimonio aziendale.'
  },

  // ═══════════════════════════════════════════════
  // VALUTAZIONI E PERIZIE — FAQ
  // ═══════════════════════════════════════════════
  {
    k: ['perizia valida banca', 'perizia abi', 'perizia accreditata'],
    r: '🏦 **Sì, le nostre perizie sono accreditate ABI** con metodica OMI/CTU. Valide per tutte le principali banche italiane. Periti iscritti ai ruoli giudiziali dei tribunali.'
  },
  {
    k: ['tempo perizia', 'quanto tempo valutazione', 'tempi report'],
    r: '⏱️ **Tempi di consegna:**\n\n• **Valutazione gratuita:** 24-48 ore\n• **Perizia completa certificata:** 5 giorni lavorativi\n• **Perizia giurata CTU:** 7-10 giorni\n\nRapidità senza compromessi sulla qualità.'
  },
  {
    k: ['valutazione asta', 'immobile asta valore', 'stima asta'],
    r: '🔨 **Valutiamo immobili all\'asta:**\n\n• Analisi perizia del tribunale\n• Confronto con valori di mercato\n• Valutazione rischi legali\n• Gap asta/mercato\n\nTi aiutiamo a capire se conviene partecipare.'
  },
  {
    k: ['stima divisione', 'perizia ereditaria', 'perizia giurata'],
    r: '⚖️ **Perizie per divisioni ereditarie:**\n\n• Perizie giurate con valore legale\n• Assistenza CTU giudiziale\n• Valutazioni imparziali e certificate\n\nRisolviamo situazioni complesse con competenza e imparzialità.'
  },
  {
    k: ['database comparabili', 'comparabili mercato', 'transazioni recenti'],
    r: '📊 **Database di 15.000+ transazioni** nella provincia di Padova degli ultimi 24 mesi. Dati reali, non stime algoritmiche. È ciò che rende le nostre valutazioni accurate e affidabili.'
  },
  {
    k: ['valutazione rurale', 'immobile rurale', 'terreno agricolo valutazione'],
    r: '🌾 **Valutiamo immobili rurali:**\n\n• Calcolo DGRV\n• Reddito fondiario\n• Cubatura edificabile\n• Potenzialità di trasformazione\n\nConosciamo il mercato agricolo del territorio padovano.'
  },
  {
    k: ['perizia ipocatastale', 'docfa', 'accatastamento', 'frazionamento'],
    r: '📐 **Perizie ipocatastali complete:**\n\n• Pratiche DOCFA\n• Accatastamenti e variazioni\n• Frazionamenti e fusioni\n• Aggiornamento planimetrie\n\nGestiamo tutta la parte catastale.'
  },
  {
    k: ['redditività locativa', 'yield', 'break even', 'irr immobiliare'],
    r: '📊 **Analisi redditività locativa completa:**\n\n• **Yield lordo e netto**\n• **Break-even** dell\'investimento\n• **IRR** (Tasso Interno di Rendimento)\n• Confronto con alternative\n\nNumeri chiari per decidere se investire.'
  },
  {
    k: ['valutazione commerciale', 'stima negozio', 'dcf immobiliare'],
    r: '🏢 **Valutiamo immobili commerciali** con metodi professionali:\n\n• Metodo **DCF** (Discounted Cash Flow)\n• Capitalizzazione dei redditi\n• Comparazione di mercato\n\nValutazioni affidabili per ogni tipologia commerciale.'
  },
  {
    k: ['trend quartiere', 'microzona', 'proiezioni prezzi'],
    r: '📈 **Analisi trend di quartiere:**\n\n• Microzonizzazione dettagliata\n• Proiezioni a **12-24 mesi**\n• Fattori di crescita (infrastrutture, servizi, trasporti)\n• Confronto storico\n\nSapere dove investire fa la differenza.'
  },
  {
    k: ['mutuo 100', 'valutazione mutuo giovani', 'mutuo prima casa'],
    r: '🏠 **Valutazioni ex-ante per mutuo 100%:**\n\n• Simulazione banca preventiva\n• Buffer di sicurezza\n• Verifica fattibilità prima dell\'offerta\n\nTi evitiamo brutte sorprese in fase di richiesta mutuo.'
  },
  {
    k: ['passaggio generazionale', 'donazione immobile', 'cessione genitori'],
    r: '👨‍👩‍👧 **Valutazioni per passaggio generazionale:**\n\n• Analisi donazione vs cessione a titolo oneroso\n• Calcolo imposte per entrambi gli scenari\n• Ottimizzazione fiscale intergenerazionale\n\nLa scelta giusta può far risparmiare migliaia di euro.'
  },

  // ═══════════════════════════════════════════════
  // ATTIVAZIONE UTENZE E SERVIZI — FAQ
  // ═══════════════════════════════════════════════
  {
    k: ['volture luce gas', 'chi paga volture', 'costo volture'],
    r: '💡 **Le volture luce e gas le gestiamo gratis.** Nessun costo aggiuntivo per te. Ci occupiamo di tutto: documentazione, contatti con i fornitori, attivazione.'
  },
  {
    k: ['tempo attivazione', 'quanto tempo utenze', 'attivazione rapida'],
    r: '⏱️ **48 ore dalla consegna chiavi** per l\'attivazione di tutte le utenze. Tempistiche garantite grazie ai nostri rapporti diretti con i fornitori.'
  },
  {
    k: ['fornitore conveniente', 'miglior offerta luce', 'confronto fornitori', 'mercato libero'],
    r: '💰 **Confrontiamo 15+ operatori** del mercato libero per trovarti l\'offerta più conveniente:\n\n• Luce e gas\n• Tutti gli operatori nazionali\n• Analisi consumi personalizzata\n\nRisparmi reali sulla bolletta fin dal primo mese.'
  },
  {
    k: ['acqua fogna', 'utenze acqua', 'multi utility'],
    r: '🚰 **Gestiamo tutte le utenze multi-utility:**\n\n• Acqua potabile\n• Fognatura\n• Rifiuti\n\nUn unico interlocutore per tutte le attivazioni.'
  },
  {
    k: ['volture impresa', 'partita iva utenze', 'utenze ufficio'],
    r: '🏢 **Volture per partite IVA e imprese:**\n\n• Utenze business\n• Split utenze uffici\n• Potenza impegnata personalizzata\n• Orario festivo/notturno\n\nGestione professionale per le aziende.'
  },
  {
    k: ['fotovoltaico', 'bonus 110', 'gse', 'pannelli solari utenze'],
    r: '☀️ **Partnership con GSE per:**\n\n• Pratiche fotovoltaico\n• Bonus 110% e incentivi\n• Scambio sul posto\n• Comunità energetiche\n\nTi accompagniamo nell\'efficientamento energetico.'
  },
  {
    k: ['utenze temporanee', 'utenze cantiere', 'utenze evento'],
    r: '⚡ **Attivazioni utenze temporanee** per:\n\n• Cantieri edili\n• Eventi e manifestazioni\n• Locazioni brevi\n\nRapide da attivare, facili da chiudere.'
  },
  {
    k: ['bonus sociale', 'isee', 'bonus luce gas'],
    r: '👨‍👩‍👧 **Assistenza bonus sociali:**\n\n• Verifica requisiti ISEE\n• Richiesta bonus luce e gas\n• Autocertificazioni\n• Rinnovi automatici\n\nTi aiutiamo ad accedere a tutti gli sconti a cui hai diritto.'
  },
  {
    k: ['audit consumi', 'analisi bollette', 'risparmio bolletta'],
    r: '📊 **Audit consumi energetici:**\n\n• Analisi ultimi 24 mesi di bollette\n• Identificazione sprechi\n• Piano risparmio personalizzato\n• **Risparmio garantito** o ti rimborsiamo la consulenza'
  },
  {
    k: ['guasti 24', 'pronto intervento', 'emergenza utenze'],
    r: '🚨 **Assistenza guasti 24/7:**\n\n• Helpdesk dedicato\n• Pronto intervento\n• Coordinamento con tecnici\n\nUn numero diretto per ogni emergenza, giorno e notte.'
  },
  {
    k: ['utenze condominio', 'millesimi', 'contatori singoli'],
    r: '🏢 **Gestione utenze condominiali:**\n\n• Ripartizione millesimi corretta\n• Contatori singoli\n• Coordinamento con l\'amministratore\n\nNiente più discussioni sui consumi.'
  },
  {
    k: ['checklist consegna', 'protocollo consegna', 'report utenze'],
    r: '✅ **Checklist consegna utenze certificata:**\n\n• Protocollo firmato di consegna\n• Report finale con tutti i codici contratto\n• Contatti diretti fornitori\n• Scadenze e promemoria\n\nTutto documentato, nulla lasciato al caso.'
  },
  {
    k: ['efficientamento', 'classe energetica migliorare', 'ape post lavori'],
    r: '🏠 **Pratiche di efficientamento energetico:**\n\n• APE post-riqualificazione\n• Classi D1-D4\n• Coordinamento con tecnici certificati\n\nMigliora la classe energetica e aumenta il valore del tuo immobile.'
  },

  // ═══════════════════════════════════════════════
  // FAQ IMMOBILIARI — CARATTERISTICHE DELL'IMMOBILE
  // Sezione 1: Struttura e Spazi (1-20)
  // ═══════════════════════════════════════════════
  {
    k: ['quante stanze', 'numero stanze', 'stanze immobile', 'locali'],
    r: '🏠 **Quante stanze ha l\'immobile?**\n\nIl numero di stanze è indicato nella scheda dell\'immobile. Per dettagli specifici, contatta il nostro consulente.\n\n📞 **049 884 3484** oppure scrivi *"contattami"*.'
  },
  {
    k: ['quanti bagni', 'numero bagni', 'bagni immobile', 'servizi igienici'],
    r: '🚿 **Quanti bagni ci sono?**\n\nIl numero di bagni è specificato nell\'annuncio. In genere, gli appartamenti hanno da **1 a 3 bagni**. Controlla la scheda dell\'immobile per il dato esatto.'
  },
  {
    k: ['metratura', 'metri quadri', 'superficie', 'grandezza', 'dimensione immobile'],
    r: '📐 **Metratura dell\'immobile**\n\nLa metratura è indicata nella scheda. Attenzione:\n• **Mq commerciali** — includono muri e pertinenze\n• **Mq calpestabili** — superficie effettivamente vivibile\n\nPer il dato esatto, consulta l\'annuncio o chiedi al consulente.'
  },
  {
    k: ['mq commerciali', 'mq calpestabili', 'differenza mq', 'superficie commerciale', 'superficie calpestabile'],
    r: '📏 **Mq commerciali vs calpestabili**\n\n• **Mq commerciali:** includono muri perimetrali, divisori e quote di pertinenze\n• **Mq calpestabili:** la superficie effettivamente vivibile, senza muri\n\nLa differenza può essere del **15-25%**. Chiedi sempre quale dato è indicato nell\'annuncio.'
  },
  {
    k: ['balcone', 'terrazzo', 'terrazza', 'loggia'],
    r: '🌇 **Balcone o terrazzo?**\n\nVerifica nella scheda dell\'immobile. Balconi e terrazzi sono sempre indicati con le relative metrature. Un terrazzo ampio aggiunge valore significativo all\'immobile.'
  },
  {
    k: ['giardino privato', 'giardino', 'area verde', 'spazio esterno'],
    r: '🌳 **Giardino privato**\n\nSe presente, è indicato nell\'annuncio con la relativa metratura. Il giardino privato è un plus molto ricercato, soprattutto per famiglie. Chiedi al consulente per ulteriori dettagli.'
  },
  {
    k: ['garage', 'posto auto', 'parcheggio', 'autorimessa'],
    r: '🚗 **Garage o posto auto**\n\nGarage e posti auto sono indicati nella scheda. Possono essere:\n• **Inclusi** nel prezzo di vendita\n• **Venduti separatamente**\n\nIn zone residenziali di Padova, il posto auto è un valore aggiunto molto importante.'
  },
  {
    k: ['cantina', 'solaio', 'soffitta', 'pertinenze'],
    r: '📦 **Cantina e solaio**\n\nLe pertinenze come cantina e solaio sono indicate nella descrizione dell\'immobile. Chiedi al consulente per dimensioni e accessibilità. Sono spazi utili per deposito e organizzazione.'
  },
  {
    k: ['piano', 'che piano', 'quale piano', 'piano alto', 'piano basso', 'piano terra'],
    r: '🏢 **A che piano si trova?**\n\nIl piano è indicato nell\'annuncio.\n• **Piani alti** = più luce e privacy\n• **Piani bassi** = più comodi per anziani e famiglie\n• **Piano terra** = accesso diretto, spesso con giardino'
  },
  {
    k: ['ascensore', 'elevatore', 'montacarichi'],
    r: '🛗 **C\'è l\'ascensore?**\n\nLa presenza dell\'ascensore è specificata nella scheda dell\'immobile. Per condomini senza ascensore, verifica la possibilità di installazione futura.'
  },
  {
    k: ['livelli', 'piani interni', 'più piani', 'doppio livello', 'su due piani'],
    r: '🏠 **Unico livello o più piani?**\n\nÈ indicato nella descrizione. Le soluzioni su più livelli offrono **più privacy** tra zona giorno e notte, tipiche di villette e attici duplex.'
  },
  {
    k: ['esposizione', 'orientamento', 'sud', 'nord', 'est', 'ovest'],
    r: '☀️ **Esposizione dell\'immobile**\n\nL\'esposizione è indicata nella scheda:\n• **Sud/Sud-Ovest** = più luce naturale\n• **Nord** = più fresco d\'estate, meno luminoso\n• **Est** = sole al mattino\n• **Ovest** = sole al pomeriggio\n\nL\'esposizione incide su comfort e consumi energetici.'
  },
  {
    k: ['luminoso', 'luminosità', 'luce naturale', 'buio'],
    r: '💡 **L\'immobile è luminoso?**\n\nLa luminosità dipende da esposizione, piano e dimensione delle finestre. Ti consigliamo sempre una **visita di persona** per valutare la luce naturale nelle diverse ore del giorno.'
  },
  {
    k: ['armadi a muro', 'armadio incassato', 'cabina armadio'],
    r: '🚪 **Armadi a muro**\n\nSe presenti, sono indicati nella descrizione dell\'immobile. In caso contrario, verifica gli spazi disponibili per installarli. Una cabina armadio è un plus molto apprezzato.'
  },
  {
    k: ['cucina abitabile', 'angolo cottura', 'cucinotto', 'cucina separata'],
    r: '🍳 **Cucina abitabile o angolo cottura?**\n\nQuesto dettaglio è nella descrizione:\n• **Cucina abitabile** — permette di mangiare in cucina\n• **Angolo cottura** — integrato nel soggiorno, soluzione moderna open space\n• **Cucinotto** — cucina piccola separata'
  },
  {
    k: ['ripostiglio', 'sgabuzzino', 'locale deposito'],
    r: '📦 **Ripostiglio**\n\nSe presente, è indicato nella scheda. È uno spazio utile spesso sottovalutato: perfetto per scope, aspirapolvere, scorte e organizzazione domestica.'
  },
  {
    k: ['ingresso indipendente', 'accesso indipendente', 'entrata privata'],
    r: '🚪 **Ingresso indipendente**\n\nPer **ville e villette** sì, l\'ingresso è sempre indipendente. Per appartamenti, verifica nella scheda se l\'accesso è da vano scale condominiale o indipendente.'
  },
  {
    k: ['quanti posti auto', 'numero posti auto', 'posti macchina'],
    r: '🅿️ **Quanti posti auto?**\n\nSono indicati nella scheda dell\'immobile. In zone residenziali di Padova, il posto auto è un valore aggiunto importante, soprattutto in centro e zone a traffico limitato.'
  },
  {
    k: ['garage singolo', 'garage doppio', 'capienza garage', 'dimensione garage'],
    r: '🚘 **Garage singolo o doppio?**\n\nDimensione e capienza sono specificate nell\'annuncio:\n• **Garage singolo** — 1 auto + spazio deposito\n• **Garage doppio** — ospita comodamente 2 auto\n\nVerifica le dimensioni esatte nella scheda.'
  },
  {
    k: ['lavanderia', 'locale lavanderia', 'lavatrice dove'],
    r: '👕 **Lavanderia**\n\nSe presente, è indicata nell\'annuncio. In caso contrario, spesso si può ricavare uno spazio lavanderia in:\n• Bagno secondario\n• Cantina\n• Terrazzo coperto\n• Ripostiglio'
  },

  // ═══════════════════════════════════════════════
  // FAQ IMMOBILIARI — STATO E CONDIZIONI (21-34)
  // ═══════════════════════════════════════════════
  {
    k: ['immobile nuovo', 'immobile usato', 'stato immobile', 'condizioni immobile'],
    r: '🏗️ **Stato dell\'immobile**\n\nLo stato è indicato nell\'annuncio:\n• **Nuovo** — appena costruito, mai abitato\n• **Ristrutturato** — lavori recenti, come nuovo\n• **Buono stato** — ben mantenuto, abitabile subito\n• **Da ristrutturare** — richiede lavori, prezzo più basso\n\nOgni condizione ha i suoi vantaggi!'
  },
  {
    k: ['anno costruzione', 'quando costruito', 'età immobile', 'anno edificio'],
    r: '📅 **Anno di costruzione**\n\nL\'anno è indicato nella scheda.\n• **Ante 1970** — possono richiedere più interventi\n• **1970-2005** — verificare impianti e isolamento\n• **Post 2005** — generalmente più efficienti energeticamente\n\nChiedi al consulente per dettagli specifici.'
  },
  {
    k: ['da ristrutturare', 'costo ristrutturazione', 'lavori necessari'],
    r: '🔨 **Immobile da ristrutturare**\n\nSe indicato come "da ristrutturare", prevedi lavori. Puoi sfruttare i **bonus fiscali vigenti** per ridurre i costi:\n• Detrazione 50% ristrutturazione\n• Ecobonus 50-65%\n• Bonus mobili\n\nIl consulente può aiutarti a stimare i costi.'
  },
  {
    k: ['ultima ristrutturazione', 'quando ristrutturato', 'interventi fatti'],
    r: '🔧 **Ultima ristrutturazione**\n\nSe disponibile, il dato è nella scheda dell\'immobile. Chiedi al consulente per dettagli specifici sugli interventi effettuati e la relativa documentazione.'
  },
  {
    k: ['lavori fatti', 'storico lavori', 'interventi eseguiti', 'cosa è stato rifatto'],
    r: '📋 **Lavori di ristrutturazione eseguiti**\n\nIl consulente può fornirti lo storico degli interventi. Verifica sempre la **documentazione** relativa ai lavori eseguiti: permessi, fatture e certificati di conformità.'
  },
  {
    k: ['intonaco', 'facciata', 'esterno edificio', 'stato esterno'],
    r: '🏠 **Intonaco e facciata esterna**\n\nLo stato dell\'intonaco è verificabile durante il sopralluogo. Eventuali crepe o distacchi vanno valutati da un tecnico. Il rifacimento della facciata è spesa condominiale.'
  },
  {
    k: ['tetto', 'copertura', 'tetto rifatto', 'impermeabilizzazione tetto'],
    r: '🏠 **Stato del tetto**\n\nChiedi al consulente se il tetto è stato rifatto di recente. Un tetto rifatto è garanzia di:\n• Impermeabilità\n• Isolamento termico\n• Durata per molti anni\n\nÈ un elemento importante nella valutazione.'
  },
  {
    k: ['grondaie', 'pluviali', 'scarichi tetto'],
    r: '🌧️ **Stato delle grondaie**\n\nVerifica durante il sopralluogo. Grondaie in cattivo stato possono causare:\n• Infiltrazioni\n• Danni alle pareti esterne\n• Umidità nei muri\n\nLa manutenzione è generalmente a carico del condominio.'
  },
  {
    k: ['umidità', 'muffa', 'umido', 'condensa'],
    r: '💧 **Problemi di umidità**\n\nEventuali problemi sono dichiarati o verificabili durante la visita. Segnali da controllare:\n• Macchie sui muri\n• Muffa negli angoli\n• Odore di umido\n• Condensa sulle finestre\n\nSe noti qualcosa, chiedi una valutazione tecnica.'
  },
  {
    k: ['infiltrazioni', 'perdite acqua', 'infiltrazione tetto', 'infiltrazione parete'],
    r: '🌊 **Infiltrazioni**\n\nIl venditore è tenuto a dichiarare eventuali infiltrazioni. Durante la visita, controlla:\n• Soffitti per macchie di umidità\n• Angoli per segni di infiltrazione\n• Pareti perimetrali\n\nIn caso di dubbi, richiedi una perizia tecnica.'
  },
  {
    k: ['pavimento', 'pavimentazione', 'parquet', 'piastrelle', 'gres'],
    r: '🏠 **Stato del pavimento**\n\nVerifica in visita lo stato della pavimentazione. Controlla:\n• Piastrelle rotte o scheggiate\n• Parquet danneggiato o sollevato\n• Pavimenti irregolari\n\nEventuali interventi vanno valutati nel budget complessivo.'
  },
  {
    k: ['muri portanti', 'struttura', 'strutturale', 'statica edificio'],
    r: '🧱 **Muri portanti e struttura**\n\nUn tecnico può verificare lo stato dei muri portanti. Crepe significative richiedono una **valutazione strutturale** da parte di un ingegnere strutturista. Le micro-fessure da assestamento sono normali.'
  },
  {
    k: ['amianto', 'eternit', 'fibrocemento'],
    r: '⚠️ **Presenza di amianto**\n\nPer immobili costruiti **prima del 1992** è possibile la presenza di amianto (eternit). In caso di dubbi, è necessaria una **perizia specializzata**. La rimozione va affidata a ditte certificate con smaltimento a norma.'
  },
  {
    k: ['crepe', 'fessure', 'lesioni muri', 'crepa muro'],
    r: '🔍 **Crepe e fessure**\n\n• **Micro-fessure** — normali nell\'assestamento dell\'edificio\n• **Crepe diagonali o ampie** — richiedono la valutazione di un ingegnere strutturista\n\nDurante la visita, il consulente può aiutarti a valutare la situazione.'
  },

  // ═══════════════════════════════════════════════
  // FAQ IMMOBILIARI — IMPIANTI E RISCALDAMENTO (35-50)
  // ═══════════════════════════════════════════════
  {
    k: ['tipo riscaldamento', 'sistema riscaldamento', 'come si riscalda'],
    r: '🔥 **Tipo di riscaldamento**\n\nPuò essere:\n• **Autonomo** — gestisci tu consumi e costi\n• **Centralizzato** — spese condivise con il condominio\n\nIl tipo è indicato nella scheda dell\'immobile.'
  },
  {
    k: ['autonomo centralizzato', 'riscaldamento autonomo', 'riscaldamento centralizzato', 'riscaldamento condominiale'],
    r: '🌡️ **Autonomo vs Centralizzato**\n\nÈ indicato nella scheda:\n• **Autonomo** — più controllo su temperature e costi, accensione libera\n• **Centralizzato** — comodo ma meno flessibile, orari prestabiliti\n\nEntrambi hanno vantaggi, dipende dalle tue esigenze.'
  },
  {
    k: ['gas metano', 'metano', 'allaccio gas', 'riscaldamento gas'],
    r: '🔵 **Riscaldamento a gas metano**\n\nÈ il sistema più diffuso nella provincia di Padova. Verifica nella scheda dell\'immobile o chiedi al consulente. Nella maggior parte delle zone urbane il gas metano è già allacciato.'
  },
  {
    k: ['pompa di calore', 'pompa calore', 'heat pump'],
    r: '♻️ **Pompa di calore**\n\nSe presente, è indicato nella scheda. Le pompe di calore sono **molto efficienti** e possono:\n• Riscaldare d\'inverno\n• Raffreddare d\'estate\n• Ridurre i consumi fino al 40%\n\nSono un investimento che valorizza l\'immobile.'
  },
  {
    k: ['riscaldamento pavimento', 'pavimento radiante', 'radiante'],
    r: '🏠 **Riscaldamento a pavimento**\n\nSe presente, è un grande vantaggio:\n• Distribuzione **uniforme** del calore\n• **Risparmio energetico** significativo\n• Nessun radiatore a vista\n• Maggiore comfort abitativo\n\nÈ indicato nella scheda dell\'immobile.'
  },
  {
    k: ['termosifoni', 'radiatori', 'fan coil', 'caloriferi'],
    r: '🌡️ **Termosifoni o fan coil?**\n\nVerifica nella scheda:\n• **Termosifoni** — classici, affidabili\n• **Fan coil** — più moderni, possono funzionare anche per il **raffreddamento estivo**\n\nI fan coil offrono maggiore versatilità.'
  },
  {
    k: ['aria condizionata', 'climatizzatore', 'condizionatore', 'raffrescamento'],
    r: '❄️ **Aria condizionata**\n\nSe presente, è indicato nell\'annuncio. In caso contrario, verifica:\n• La **predisposizione** per l\'installazione\n• La possibilità di installare split\n• Eventuali vincoli condominiali\n\nNelle estati padovane è un comfort molto apprezzato.'
  },
  {
    k: ['impianto elettrico', 'elettrico a norma', 'certificato conformità elettrico'],
    r: '⚡ **Impianto elettrico a norma**\n\nPer impianti **post-2008** serve il certificato di conformità (DM 37/08). Per i precedenti, basta il certificato di rispondenza. Verifica con il consulente lo stato dell\'impianto.'
  },
  {
    k: ['impianto idraulico', 'tubature', 'tubi', 'idraulico a norma'],
    r: '🔧 **Impianto idraulico**\n\nVerifica con il consulente. Impianti vecchi in **piombo o ferro zincato** andrebbero sostituiti per sicurezza e qualità dell\'acqua. I moderni impianti in multistrato sono più affidabili.'
  },
  {
    k: ['gas allacciato', 'allaccio gas metano', 'rete gas'],
    r: '🔵 **Gas metano allacciato**\n\nNella maggior parte delle zone urbane di Padova sì. Per zone rurali o isolate, verifica la disponibilità dell\'allaccio alla rete del gas. In alternativa si può optare per GPL o pompa di calore.'
  },
  {
    k: ['predisposizione condizionatore', 'predisposizione clima', 'predisposizione aria condizionata'],
    r: '❄️ **Predisposizione aria condizionata**\n\nSe presente, l\'installazione è **più semplice ed economica** (tubi già passati, scarichi predisposti). Chiedi al consulente per verificare la presenza della predisposizione nell\'immobile.'
  },
  {
    k: ['caldaia recente', 'età caldaia', 'caldaia vecchia', 'impianto recente'],
    r: '🔥 **Impianto di riscaldamento recente?**\n\nChiedi al consulente l\'anno della caldaia o pompa di calore. Una **caldaia a condensazione moderna** riduce i consumi del **20-30%** rispetto ai modelli tradizionali.'
  },
  {
    k: ['caldaia condensazione', 'condensazione', 'caldaia moderna'],
    r: '🌱 **Caldaia a condensazione**\n\nSe presente è un vantaggio:\n• Consuma **meno** gas\n• Inquina meno\n• Rendimento più alto\n\nSono obbligatorie per le nuove installazioni **dal 2015**. È un elemento che valorizza l\'immobile.'
  },
  {
    k: ['pannelli solari', 'fotovoltaico', 'solare termico', 'energia solare'],
    r: '☀️ **Pannelli solari o fotovoltaici**\n\nSe presenti, sono indicati nella scheda. I vantaggi:\n• Riduzione significativa dei **costi energetici**\n• Aumento del **valore dell\'immobile**\n• Possibilità di incentivi GSE\n• Contributo alla sostenibilità ambientale'
  },
  {
    k: ['allarme', 'antifurto', 'sistema sicurezza', 'impianto allarme', 'videosorveglianza'],
    r: '🔐 **Impianto di allarme**\n\nSe presente, è indicato nella scheda. Verifica:\n• Se è **funzionante** e aggiornato\n• Il tipo (perimetrale, volumetrico, misto)\n• La presenza di videosorveglianza\n\nUn impianto di sicurezza è un valore aggiunto per l\'immobile.'
  },
  {
    k: ['tv', 'antenna', 'fibra ottica', 'internet', 'connessione'],
    r: '📡 **Impianto TV e fibra ottica**\n\nLa predisposizione TV è generalmente presente in tutti gli immobili. Per la **fibra ottica**, verifica la copertura nella zona su:\n• Sito del tuo operatore\n• Open Fiber\n\nLa fibra è un comfort sempre più importante, soprattutto per chi lavora da casa.'
  },

  // ═══════════════════════════════════════════════
  // FAQ IMMOBILIARI — IMPIANTI AGGIUNTIVI (51-53)
  // ═══════════════════════════════════════════════
  {
    k: ['videocitofono', 'citofono', 'citofono video', 'campanello smart'],
    r: '🔔 **Videocitofono**\n\nSe presente, è indicato nella scheda. I modelli moderni permettono anche la **gestione da smartphone**: vedi chi suona e apri il portone ovunque tu sia. È un comfort di sicurezza molto apprezzato.'
  },
  {
    k: ['acqua calda', 'boiler', 'scaldabagno', 'produzione acqua calda'],
    r: '🚿 **Acqua calda: caldaia o boiler?**\n\nDipende dall\'impianto:\n• **Caldaia combinata** — produce acqua calda istantanea, più efficiente\n• **Boiler elettrico** — accumula l\'acqua calda, consumi più alti\n• **Boiler a pompa di calore** — soluzione moderna e efficiente\n\nVerifica nella scheda dell\'immobile.'
  },
  {
    k: ['addolcitore', 'calcare', 'acqua dura', 'durezza acqua'],
    r: '💧 **Addolcitore d\'acqua**\n\nSe presente, è un plus importante: protegge **tubature ed elettrodomestici** dal calcare. Molto utile nella zona di Padova dove l\'acqua è mediamente dura. Allunga la vita di caldaia, lavatrice e lavastoviglie.'
  },

  // ═══════════════════════════════════════════════
  // FAQ IMMOBILIARI — INFISSI E ISOLAMENTO (54-63)
  // ═══════════════════════════════════════════════
  {
    k: ['doppi vetri', 'vetri finestre', 'vetro doppio', 'vetrocamera'],
    r: '🪟 **Doppi vetri**\n\nVerifica nella scheda. I doppi vetri migliorano:\n• **Isolamento termico** — meno dispersione di calore\n• **Isolamento acustico** — meno rumore dall\'esterno\n• **Risparmio energetico** — bollette più basse\n\nSono ormai uno standard nelle costruzioni moderne.'
  },
  {
    k: ['serramenti', 'infissi', 'finestre pvc', 'finestre legno', 'finestre alluminio'],
    r: '🪟 **Tipo di serramenti**\n\nÈ indicato nella descrizione:\n• **PVC** — ottimo rapporto qualità/prezzo, bassa manutenzione\n• **Legno** — estetica calda e naturale, richiede manutenzione\n• **Alluminio a taglio termico** — durabilità e design moderno\n\nIl tipo di infisso incide molto su isolamento e comfort.'
  },
  {
    k: ['triplo vetro', 'vetro camera', 'vetro basso emissivo'],
    r: '🪟 **Vetro camera o triplo vetro?**\n\n• **Vetro camera (doppio)** — lo standard attuale, buon isolamento\n• **Triplo vetro** — isolamento superiore, ideale per zone fredde o esposizioni a nord\n• **Basso emissivo** — trattamento che riduce la dispersione termica\n\nVerifica il tipo nella scheda dell\'immobile.'
  },
  {
    k: ['tapparelle', 'tapparelle elettriche', 'tapparelle manuali', 'avvolgibili'],
    r: '🏠 **Tapparelle elettriche o manuali?**\n\nVerifica nella scheda o in visita:\n• **Elettriche** — più comode, soprattutto per finestre grandi, gestibili anche da domotica\n• **Manuali** — più economiche, nessun costo elettrico\n\nL\'elettrificazione delle tapparelle è un intervento relativamente semplice.'
  },
  {
    k: ['zanzariere', 'zanzariera', 'anti insetti'],
    r: '🦟 **Zanzariere**\n\nSe presenti, sono indicate nell\'annuncio. In caso contrario, si installano facilmente su quasi tutti i tipi di finestre. Nelle estati padovane sono molto utili, soprattutto ai piani bassi e vicino a zone verdi.'
  },
  {
    k: ['cappotto termico', 'isolamento termico', 'coibentazione', 'isolamento esterno'],
    r: '🧱 **Isolamento termico (cappotto)**\n\nSe presente, è un grande vantaggio:\n• **Risparmio energetico** fino al 40%\n• Temperatura interna più stabile\n• Migliore classe energetica\n• Meno umidità e condensa\n\nVerifica nella scheda o chiedi al consulente.'
  },
  {
    k: ['isolamento acustico', 'rumore', 'insonorizzazione', 'fonoisolamento'],
    r: '🔇 **Isolamento acustico**\n\nDipende da anno di costruzione, materiali e infissi. Gli immobili recenti hanno **standard acustici migliori** per legge. Per quelli più datati, si può migliorare con:\n• Infissi nuovi\n• Contropareti isolanti\n• Pavimento flottante'
  },
  {
    k: ['persiane', 'scuri', 'scuretti', 'oscuranti'],
    r: '🏠 **Persiane e scuri**\n\nVerifica le condizioni in visita:\n• **In legno** — richiedono manutenzione periodica (verniciatura)\n• **In alluminio** — più durature, meno manutenzione\n• **In PVC** — buon rapporto qualità/prezzo\n\nIl consulente può valutarne lo stato durante il sopralluogo.'
  },
  {
    k: ['porta blindata', 'portoncino blindato', 'portone ingresso', 'classe sicurezza'],
    r: '🔒 **Portoncino blindato**\n\nSe presente, è indicato nell\'annuncio. Una porta blindata di **classe 3 o superiore** garantisce buona sicurezza. Verifica anche:\n• Serratura europea anti-bumping\n• Isolamento termico e acustico del portoncino\n• Cilindro di sicurezza'
  },
  {
    k: ['spifferi', 'correnti aria', 'tenuta infissi', 'guarnizioni finestre'],
    r: '💨 **Spifferi dalle finestre**\n\nSpifferi indicano serramenti vecchi o mal posati. Durante la visita:\n• Avvicina la mano agli infissi per sentire correnti d\'aria\n• Controlla le guarnizioni\n• Verifica la chiusura ermetica\n\nLa sostituzione degli infissi gode della **detrazione fiscale 50%**.'
  },

  // ═══════════════════════════════════════════════
  // FAQ IMMOBILIARI — CLASSE ENERGETICA (64-68)
  // ═══════════════════════════════════════════════
  {
    k: ['classe energetica immobile', 'quale classe energetica', 'lettera energetica'],
    r: '⚡ **Classe energetica dell\'immobile**\n\nÈ indicata nell\'**APE** (Attestato di Prestazione Energetica), obbligatorio per ogni annuncio. Le classi vanno da:\n• **A4** (migliore) — consumi minimi\n• **G** (peggiore) — consumi elevati\n\nLa classe influisce su bollette e valore dell\'immobile.'
  },
  {
    k: ['cos è ape', 'ape cosa significa', 'attestato prestazione energetica significato'],
    r: '📋 **Cos\'è l\'APE?**\n\nL\'**Attestato di Prestazione Energetica** è un documento obbligatorio che indica i consumi energetici dell\'immobile. Caratteristiche:\n• **Validità:** 10 anni\n• **Obbligatorio** per vendita e affitto\n• Redatto da un tecnico abilitato\n• Costo medio: €150-€300'
  },
  {
    k: ['classe energetica consumi', 'risparmio classe a', 'consumi classe g'],
    r: '💰 **Classe energetica e consumi**\n\nL\'impatto è enorme:\n• Una **classe A** consuma fino all\'**80% in meno** di una classe G\n• La differenza si vede subito in bolletta\n• Un appartamento in classe G può costare €2.000-€3.000/anno di riscaldamento, in classe A meno di €500\n\nInvesti nel risparmio energetico!'
  },
  {
    k: ['migliorare classe energetica', 'salire classe', 'upgrade energetico'],
    r: '📈 **Migliorare la classe energetica**\n\nSì, è possibile con:\n• **Cappotto termico** — salto di 2-3 classi\n• **Infissi nuovi** — miglioramento significativo\n• **Caldaia a condensazione o pompa di calore**\n• **Pannelli solari/fotovoltaici**\n\nEsistono **incentivi fiscali** (50-65%) per questi interventi.'
  },
  {
    k: ['costo migliorare classe', 'quanto costa efficientare', 'preventivo energetico'],
    r: '💶 **Costi indicativi per migliorare la classe energetica:**\n\n• **Infissi nuovi:** €5.000-€10.000\n• **Cappotto termico:** €15.000-€30.000\n• **Caldaia a condensazione:** €3.000-€5.000\n• **Pompa di calore:** €5.000-€10.000\n\nChiedi un preventivo dedicato al nostro consulente. Molti interventi godono di detrazioni fiscali.'
  },

  // ═══════════════════════════════════════════════
  // FAQ IMMOBILIARI — ESTERNI E PERTINENZE (69-73)
  // ═══════════════════════════════════════════════
  {
    k: ['aree verdi condominiali', 'giardino condominiale', 'verde comune'],
    r: '🌿 **Aree verdi condominiali**\n\nSe presenti, sono indicate nella scheda. Le spese di manutenzione (giardiniere, irrigazione) rientrano nelle **spese condominiali ordinarie** e sono ripartite tra tutti i condomini.'
  },
  {
    k: ['piscina condominiale', 'piscina condominio'],
    r: '🏊 **Piscina condominiale**\n\nSe presente, è un valore aggiunto importante ma comporta **spese condominiali più alte** per:\n• Manutenzione e pulizia\n• Prodotti chimici\n• Assicurazione\n• Eventuale bagnino\n\nVerifica l\'importo nelle spese condominiali.'
  },
  {
    k: ['posto bici', 'biciclette', 'rastrelliera', 'deposito bici'],
    r: '🚲 **Posti bici nel condominio**\n\nVerifica con il consulente. Molti condomini recenti prevedono spazi dedicati. A Padova, città molto ciclabile, è un **comfort importante** per la vita quotidiana.'
  },
  {
    k: ['cortile condominiale', 'cortile privato', 'cortile interno'],
    r: '🏠 **Cortile: condominiale o privato?**\n\nÈ specificato nella scheda:\n• **Cortile privato** — più libertà di utilizzo, spazio esclusivo\n• **Cortile condominiale** — uso comune, regolato dal regolamento condominiale\n\nVerifica i dettagli nell\'annuncio.'
  },
  {
    k: ['locale bici', 'locale passeggino', 'deposito carrozzine'],
    r: '👶 **Locale bici/passeggino**\n\nVerifica con il consulente. È un plus importante per **famiglie con bambini**. Molti condomini moderni hanno spazi dedicati al piano terra per biciclette, passeggini e monopattini.'
  },

  // ═══════════════════════════════════════════════
  // FAQ IMMOBILIARI — ZONA E CONTESTO (74-83)
  // ═══════════════════════════════════════════════
  {
    k: ['zona immobile', 'dove si trova', 'posizione immobile', 'localizzazione'],
    r: '📍 **Zona dell\'immobile**\n\nLa zona è indicata nell\'annuncio con mappa. Chiedi al consulente per info dettagliate su:\n• Servizi disponibili\n• Trasporti pubblici\n• Vivibilità e sicurezza\n• Prezzi medi della zona'
  },
  {
    k: ['scuole vicine', 'scuole zona', 'scuola vicina', 'asilo vicino'],
    r: '🏫 **Scuole nelle vicinanze**\n\nIl consulente può informarti sulle scuole della zona:\n• Asili nido e scuole materne\n• Scuole elementari\n• Scuole medie\n• Scuole superiori e licei\n\nLa vicinanza alle scuole è un fattore molto ricercato dalle famiglie.'
  },
  {
    k: ['mezzi pubblici', 'autobus', 'tram', 'trasporti', 'fermata bus'],
    r: '🚌 **Distanza dai mezzi pubblici**\n\nVerifica nella scheda o sulla mappa. Per Padova, la vicinanza al **tram** è un valore aggiunto importante. Le linee bus coprono bene la città e la prima cintura.'
  },
  {
    k: ['supermercato', 'negozi vicini', 'commerci zona', 'spesa'],
    r: '🛒 **Supermercato vicino?**\n\nNella maggior parte delle zone residenziali di Padova e provincia sì. Verifica sulla mappa dell\'annuncio. La vicinanza a supermercati e negozi è un comfort quotidiano importante.'
  },
  {
    k: ['zona tranquilla', 'rumorosa', 'quiete', 'silenzioso', 'traffico zona'],
    r: '🤫 **La zona è tranquilla?**\n\nIl consulente conosce bene le zone di Padova e provincia. Ti consigliamo anche una **visita in diversi orari** della giornata per valutare il livello di rumore e traffico.'
  },
  {
    k: ['parcheggi zona', 'parcheggio strada', 'strisce blu', 'ztl'],
    r: '🅿️ **Parcheggi nella zona**\n\nVaria da zona a zona:\n• **Centro Padova** — più difficile, ZTL e strisce blu\n• **Prima cintura** — generalmente buona disponibilità\n• **Provincia** — nessun problema\n\nIl garage/posto auto diventa fondamentale in centro.'
  },
  {
    k: ['allagamenti', 'rischio idrogeologico', 'esondazione', 'alluvione'],
    r: '🌊 **Rischio allagamenti**\n\nPer la zona di Padova, verifica le **mappe di rischio idrogeologico** del comune. Il consulente può consigliarti e indicarti le zone più sicure. È un aspetto importante nella scelta dell\'immobile.'
  },
  {
    k: ['cantieri zona', 'progetti urbanistici', 'nuove costruzioni zona', 'sviluppo zona'],
    r: '🏗️ **Cantieri e progetti urbanistici**\n\nChiedi al consulente per info aggiornate:\n• **Nuove infrastrutture** — possono aumentare il valore\n• **Cantieri prolungati** — possono creare disagi temporanei\n• **Piani urbanistici** — indicano lo sviluppo futuro della zona'
  },
  {
    k: ['sport zona', 'palestre vicine', 'piscina pubblica', 'parco vicino', 'ciclabile'],
    r: '🏃 **Sport e tempo libero nella zona**\n\nIl consulente può indicarti:\n• Palestre e centri fitness\n• Piscine pubbliche e private\n• Parchi e aree verdi\n• Percorsi ciclabili\n\nPadova è una città molto vivibile e sportiva.'
  },
  {
    k: ['distanza centro padova', 'quanto dista centro', 'lontano dal centro'],
    r: '📍 **Distanza dal centro di Padova**\n\nÈ indicata nell\'annuncio. Per riferimento:\n• **Limena** (nostra sede) — ~10 km dal centro\n• **Prima cintura** — 5-15 km, buoni collegamenti\n• **Provincia** — 15-40 km\n\nVerifica tempi di percorrenza in auto e con mezzi pubblici.'
  },

  // ═══════════════════════════════════════════════
  // FAQ IMMOBILIARI — CONDOMINIO (84-91)
  // ═══════════════════════════════════════════════
  {
    k: ['importo spese condominiali', 'quanto costa condominio', 'spese mensili condominio'],
    r: '💶 **Spese condominiali**\n\nL\'importo è indicato nella scheda. Includono generalmente:\n• Pulizia scale\n• Assicurazione fabbricato\n• Manutenzione ordinaria\n• Luce parti comuni\n• Ascensore (se presente)\n\nChiedi al consulente per il dettaglio esatto.'
  },
  {
    k: ['lavori straordinari', 'lavori condominio previsti', 'delibere lavori'],
    r: '🏗️ **Lavori straordinari previsti?**\n\nChiedi al consulente. È importante sapere che:\n• Lavori **deliberati prima** della vendita → a carico del **venditore**\n• Lavori deliberati dopo → a carico dell\'**acquirente**\n\nVerifichiamo sempre questo aspetto prima della compravendita.'
  },
  {
    k: ['amministratore condominio', 'chi amministra', 'gestione condominio'],
    r: '👔 **Amministratore di condominio**\n\nÈ **obbligatorio** per condomini con più di 8 unità. Per i più piccoli, la gestione può essere interna (autogestione). Il consulente può fornirti i contatti dell\'amministratore.'
  },
  {
    k: ['verbali assemblea', 'assemblee condominiali', 'delibere assemblea'],
    r: '📋 **Verbali delle assemblee**\n\nSì, è un tuo **diritto** consultarli prima dell\'acquisto. Il consulente può richiederli per tua verifica. Nei verbali trovi:\n• Delibere su lavori e spese\n• Situazione morosità\n• Problematiche in corso'
  },
  {
    k: ['venditore spese condominiali', 'arretrati condominio', 'morosità venditore'],
    r: '⚠️ **Spese condominiali del venditore**\n\nVerifichiamo **sempre** questo aspetto. Attenzione: le spese non pagate possono ricadere sull\'acquirente per l\'anno in corso e quello precedente. Chiediamo sempre la **liberatoria** dall\'amministratore.'
  },
  {
    k: ['regolamento condominiale', 'regolamento condominio', 'vincoli condominio'],
    r: '📜 **Regolamento condominiale**\n\nOgni condominio ha il suo regolamento. Verifica eventuali vincoli su:\n• Animali domestici\n• Orari di silenzio\n• Modifiche esterne (tende, condizionatori)\n• Uso delle parti comuni\n\nIl consulente può procurarti una copia.'
  },
  {
    k: ['animali condominio', 'cane condominio', 'gatto condominio', 'animali domestici casa'],
    r: '🐾 **Animali domestici in condominio**\n\nSì, la **legge lo consente** (Riforma del Condominio 2012). Il regolamento condominiale **non può vietare** la detenzione di animali domestici. Sono però richiesti rispetto delle norme igieniche e di convivenza.'
  },
  {
    k: ['costo medio condominio padova', 'spese condominiali medie', 'media condominio'],
    r: '💰 **Costi medi condominiali a Padova:**\n\n• **Base** (scale + assicurazione): €50-100/mese\n• **Con ascensore e giardino:** €100-200/mese\n• **Con portineria/piscina:** oltre €200/mese\n\nSono indicazioni medie, il costo esatto dipende dal condominio specifico.'
  },

  // ═══════════════════════════════════════════════
  // FAQ IMMOBILIARI — CERTIFICAZIONI E DOCUMENTI (92-100)
  // ═══════════════════════════════════════════════
  {
    k: ['certificazioni impianti', 'impianti certificati', 'documenti impianti'],
    r: '📋 **Certificazioni degli impianti**\n\nPer impianti **post-2008** serve la conformità (DM 37/08), per i precedenti la rispondenza. Verifichiamo **tutto prima della vendita** per garantirti la massima tranquillità.'
  },
  {
    k: ['certificato conformità', 'cos è conformità', 'dm 37', 'dichiarazione conformità'],
    r: '📄 **Certificato di conformità**\n\nAttesta che l\'impianto è stato realizzato **a regola d\'arte** secondo le norme vigenti (DM 37/2008). È obbligatorio dal 2008 e deve essere rilasciato dall\'installatore abilitato per ogni impianto.'
  },
  {
    k: ['certificato rispondenza', 'diri', 'rispondenza impianti'],
    r: '📄 **Certificato di rispondenza (DiRi)**\n\nPer impianti **pre-2008**, un tecnico abilitato certifica che l\'impianto, pur datato, rispetta i **requisiti minimi di sicurezza**. È un\'alternativa alla conformità per impianti più vecchi.'
  },
  {
    k: ['agibilità', 'abitabilità', 'certificato agibilità', 'segnalazione agibilità'],
    r: '🏠 **Agibilità/Abitabilità**\n\nÈ un documento fondamentale che certifica la conformità dell\'immobile ai requisiti di:\n• **Sicurezza** strutturale\n• **Igiene** e salubrità\n• **Risparmio energetico**\n\nDal 2016 si chiama **Segnalazione Certificata di Agibilità (SCA)**.'
  },
  {
    k: ['difformità catastali', 'errori catasto', 'planimetria non conforme'],
    r: '⚠️ **Difformità catastali**\n\nVerifichiamo sempre la **conformità catastale** prima della vendita. Eventuali difformità vanno sanate prima del rogito tramite:\n• Variazione catastale (DOCFA)\n• Aggiornamento planimetrie\n\nCosto medio: €500-€1.500.'
  },
  {
    k: ['conformità catastale cos è', 'planimetria conforme', 'catasto conforme'],
    r: '📐 **Conformità catastale**\n\nSignifica che la **planimetria catastale** corrisponde allo stato reale dell\'immobile. È **obbligatoria per il rogito** dal 2010. Il notaio la verifica prima dell\'atto. Noi la controlliamo in anticipo.'
  },
  {
    k: ['conformità urbanistica cos è', 'regolarità edilizia cos è', 'permessi edilizi'],
    r: '🏗️ **Conformità urbanistica**\n\nVerifica che l\'immobile sia stato costruito/modificato con **regolari permessi edilizi**. È la cosa **più importante da controllare** prima dell\'acquisto. Difformità urbanistiche possono bloccare la vendita.'
  },
  {
    k: ['accesso atti', 'accesso atti comune', 'verifica permessi comune'],
    r: '📋 **Accesso agli atti in comune**\n\nÈ la verifica dei **permessi edilizi** depositati in comune. Lo facciamo **sempre** per garantire la regolarità dell\'immobile. Permette di scoprire eventuali abusi o difformità prima dell\'acquisto.'
  },
  {
    k: ['progetti immobile', 'planimetrie originali', 'documenti costruzione'],
    r: '📐 **Progetti dell\'immobile**\n\nVerifichiamo la presenza di progetti e permessi originali:\n• Licenza edilizia\n• Planimetrie depositate\n• Eventuali varianti\n• Certificati di collaudo\n\nEventuali mancanze vanno risolte **prima della compravendita**.'
  },

  // ═══════════════════════════════════════════════
  // SEZIONE 2: ASPETTI LEGALI, BUROCRATICI E COMMERCIALI
  // FAQ 101-102: Visure
  // ═══════════════════════════════════════════════
  {
    k: ['visura catastale', 'dati catastali', 'rendita catastale', 'categoria catastale'],
    r: '📋 **Visura catastale**\n\nÈ il documento che riporta i dati catastali dell\'immobile:\n• **Proprietario** intestatario\n• **Rendita catastale**\n• **Categoria** (A2, A3, ecc.)\n• **Classe** e **consistenza** (vani)\n\nÈ fondamentale per calcolare le imposte e verificare la proprietà.'
  },
  {
    k: ['visura ipotecaria', 'ipoteche immobile', 'pignoramenti', 'gravami immobile'],
    r: '🔍 **Visura ipotecaria**\n\nVerifica la presenza di:\n• **Ipoteche** (volontarie o giudiziali)\n• **Pignoramenti**\n• **Altri gravami** sull\'immobile\n\nÈ **fondamentale** prima dell\'acquisto. Noi la eseguiamo sempre per garantirti un acquisto sicuro.'
  },

  // ═══════════════════════════════════════════════
  // FAQ 103-115: PROCESSO DI ACQUISTO
  // ═══════════════════════════════════════════════
  {
    k: ['processo acquisto', 'come comprare casa', 'fasi acquisto', 'iter acquisto'],
    r: '🏠 **Come funziona l\'acquisto di una casa?**\n\nLe fasi principali:\n1. **Visita** dell\'immobile\n2. **Proposta d\'acquisto** scritta\n3. **Accettazione** del venditore\n4. **Preliminare** (compromesso)\n5. **Rogito notarile** — passaggio di proprietà\n\nTi seguiamo in **ogni fase**, dalla prima visita alle chiavi.'
  },
  {
    k: ['proposta di acquisto', 'proposta vincolante', 'proposta scritta'],
    r: '📝 **Proposta d\'acquisto**\n\nÈ un\'offerta **scritta e vincolante** con cui dichiari la tua intenzione di acquistare a determinate condizioni e prezzo. È accompagnata da un assegno di caparra. Diventa efficace solo quando il venditore la accetta.'
  },
  {
    k: ['contratto preliminare di vendita', 'compromesso immobiliare', 'registrare preliminare'],
    r: '📋 **Contratto preliminare (compromesso)**\n\nÈ l\'accordo che **vincola entrambe le parti** alla compravendita. Deve essere:\n• **Registrato** entro 20 giorni all\'Agenzia delle Entrate\n• Accompagnato dalla caparra confirmatoria\n\nNoi prepariamo e registriamo il preliminare per voi.'
  },
  {
    k: ['rogito notarile', 'atto definitivo di vendita', 'trasferimento proprietà rogito'],
    r: '🏛️ **Rogito notarile**\n\nÈ l\'**atto definitivo di vendita** stipulato dal notaio. Con il rogito:\n• Si trasferisce la **proprietà**\n• Viene trascritto nei **registri immobiliari**\n• Si consegnano le **chiavi**\n\nÈ il momento finale della compravendita.'
  },
  {
    k: ['tempo proposta rogito', 'quanto dura acquisto', 'tempistica acquisto completa'],
    r: '⏱️ **Dalla proposta al rogito**\n\nIn media **2-4 mesi**. Dipende da:\n• Tempi di approvazione del **mutuo** (30-60 giorni)\n• Raccolta **documenti**\n• Accordi tra le parti\n\nNoi ci impegniamo a velocizzare ogni fase.'
  },
  {
    k: ['proposta condizionata mutuo', 'clausola sospensiva mutuo', 'condizionata al mutuo'],
    r: '🏦 **Proposta condizionata al mutuo**\n\nSì, è possibile inserire una **clausola sospensiva**: se il mutuo non viene concesso, la proposta decade e la caparra viene **restituita integralmente**. È una tutela importante per l\'acquirente.'
  },
  {
    k: ['caparra confirmatoria', 'confirmatoria', 'caparra penitenziale differenza'],
    r: '💶 **Caparra confirmatoria**\n\nÈ una somma versata a **garanzia dell\'impegno**:\n• Se l\'**acquirente** recede → perde la caparra\n• Se il **venditore** recede → deve restituire il **doppio**\n\nÈ la principale tutela economica nella compravendita.'
  },
  {
    k: ['caparra quanto versare', 'importo della caparra', 'caparra 5 10 20 percento'],
    r: '💰 **Quanto deve essere la caparra?**\n\nGeneralmente dal **5% al 20%** del prezzo di vendita. Non c\'è un obbligo di legge specifico, si concorda tra le parti. Il consulente ti aiuta a trovare l\'importo giusto per la tua situazione.'
  },
  {
    k: ['ritirare proposta', 'annullare proposta', 'revocare proposta'],
    r: '📝 **Ritirare la proposta d\'acquisto**\n\n• **Prima dell\'accettazione** del venditore → sì, senza conseguenze\n• **Dopo l\'accettazione** → perdi la caparra versata\n\nPer questo è importante fare una proposta ponderata con il supporto del consulente.'
  },
  {
    k: ['prezzo trattabile', 'negoziare prezzo', 'sconto prezzo', 'margine trattativa'],
    r: '💬 **Il prezzo è trattabile?**\n\nNella maggior parte dei casi **sì**. Il margine di trattativa dipende da:\n• Tempo sul mercato dell\'immobile\n• Motivazione del venditore\n• Stato dell\'immobile\n• Mercato locale\n\nIl consulente può consigliarti la giusta offerta.'
  },
  {
    k: ['venditore rifiuta', 'proposta rifiutata', 'offerta non accettata'],
    r: '❌ **Proposta rifiutata dal venditore**\n\nL\'assegno ti viene **restituito immediatamente**, senza alcun costo o penale. Puoi valutare se fare una nuova proposta o cercare un altro immobile.'
  },
  {
    k: ['controproposta', 'contro proposta', 'rilancio prezzo'],
    r: '🔄 **Controproposta**\n\nSì, il venditore può:\n• **Rifiutare** la tua proposta\n• **Accettarla** così com\'è\n• Fare una **controproposta** con condizioni diverse\n\nSi negozia fino a trovare un accordo. Il consulente media tra le parti.'
  },
  {
    k: ['chi sceglie notaio', 'scelta notaio', 'quale notaio'],
    r: '⚖️ **Chi sceglie il notaio?**\n\nDi norma lo sceglie l\'**acquirente**, perché è chi sostiene le spese notarili. Possiamo consigliarti notai di fiducia con tariffe competitive nella zona di Padova.'
  },

  // ═══════════════════════════════════════════════
  // FAQ 116-129: COSTI E TASSE
  // ═══════════════════════════════════════════════
  {
    k: ['costo notaio 100000', 'atto 100.000', 'spese notarili 100k'],
    r: '💶 **Costo notarile — immobile da €100.000**\n\nIndicativamente **€2.000-€3.500** tra onorario notarile e imposte. Per la **prima casa**, le imposte sono ridotte. Il costo esatto dipende dal notaio scelto e dal tipo di acquisto (privato o costruttore).'
  },
  {
    k: ['costo notaio 200000', 'atto 200.000', 'spese notarili 200k'],
    r: '💶 **Costo notarile — immobile da €200.000**\n\nIndicativamente **€3.500-€5.000** tra onorario e imposte. L\'importo varia in base al notaio e al tipo di acquisto. Chiedi sempre un **preventivo** prima di procedere.'
  },
  {
    k: ['costo notaio 300000', 'atto 300.000', 'spese notarili 300k'],
    r: '💶 **Costo notarile — immobile da €300.000**\n\nIndicativamente **€4.500-€6.500**. Per cifre precise, richiedi un preventivo al notaio scelto. Noi possiamo metterti in contatto con notai convenzionati.'
  },
  {
    k: ['tasse acquisto casa', 'imposte acquisto immobile', 'quali tasse comprare casa'],
    r: '🧾 **Tasse per l\'acquisto casa**\n\n**Da privato:**\n• Prima casa: imposta registro **2%** + €50+€50\n• Seconda casa: imposta registro **9%** + €50+€50\n\n**Da costruttore:**\n• Prima casa: IVA **4%** + €200×3\n• Seconda casa: IVA **10%** + €200×3\n\nLe imposte si calcolano sul valore catastale (da privato) o sul prezzo (da costruttore).'
  },
  {
    k: ['imposta di registro', 'imposta registro 2 9 percento', 'tassa trasferimento immobiliare'],
    r: '📊 **Imposta di registro**\n\nÈ la tassa sul trasferimento immobiliare. Si calcola sul **valore catastale**, non sul prezzo di vendita:\n• **2%** per prima casa\n• **9%** per seconda casa\n\nMinimo €1.000. È una delle voci principali nel costo di acquisto.'
  },
  {
    k: ['valore catastale', 'calcolo valore catastale', 'rendita rivalutata', 'coefficiente catastale'],
    r: '🔢 **Valore catastale**\n\nÈ la rendita catastale rivalutata × un coefficiente:\n• **×115,5** per prima casa\n• **×126** per seconda casa\n\nServe per calcolare le imposte. È quasi sempre **inferiore** al prezzo di mercato, con vantaggio fiscale per l\'acquirente.'
  },
  {
    k: ['requisiti prima casa', 'benefici prima casa', 'condizioni prima casa', 'residenza 18 mesi'],
    r: '🏡 **Agevolazioni prima casa**\n\n**Requisiti:**\n• Imposta di registro ridotta al **2%** (anziché 9%)\n• Non possedere altri immobili nello stesso comune\n• Trasferire la **residenza entro 18 mesi**\n• Non aver già usufruito del bonus\n\nUn risparmio significativo sulle imposte!'
  },
  {
    k: ['under 36 casa', 'bonus giovani acquisto', 'prima casa giovani under'],
    r: '👶 **Bonus prima casa under 36**\n\nVerifica le **agevolazioni vigenti**, poiché le condizioni possono cambiare. Il consulente ti aggiorna sempre sulle opportunità attuali per i giovani acquirenti. Contattaci per info aggiornate!'
  },
  {
    k: ['provvigione agenzia immobiliare', 'tariffe mediazione', 'onorari agente immobiliare'],
    r: '💶 **Provvigione dell\'agenzia**\n\nLa provvigione è concordata al conferimento dell\'incarico. Contattaci per un **preventivo trasparente**. Nessun costo nascosto, nessuna sorpresa.\n\n📞 **049 884 3484** oppure scrivi *"contattami"*.'
  },
  {
    k: ['chi paga agenzia', 'provvigione acquirente e venditore', 'mediazione chi paga'],
    r: '💰 **Chi paga la provvigione?**\n\nGeneralmente sia **acquirente** che **venditore**, salvo accordi diversi. Ogni agenzia ha le sue condizioni. Da noi, tutto è concordato e trasparente fin dall\'inizio.'
  },
  {
    k: ['costi nascosti acquisto', 'spese impreviste', 'costi extra acquisto'],
    r: '🔍 **Costi nascosti nell\'acquisto?**\n\nNo, se sei ben informato! Oltre al prezzo dell\'immobile, prevedi:\n• **Notaio** e imposte\n• **Agenzia**\n• Eventuale **perizia mutuo** (€200-€400)\n• **Registrazione preliminare** (€200 + 0,50% caparra)\n\nNoi ti forniamo un quadro completo fin dall\'inizio.'
  },
  {
    k: ['costo registrazione preliminare', 'registrare compromesso costo', 'tasse compromesso'],
    r: '📋 **Costo registrazione preliminare**\n\n• Imposta fissa: **€200**\n• Imposta proporzionale: **0,50%** sulla caparra\n• Imposta proporzionale: **3%** sugli acconti prezzo\n\nGli importi versati si **recuperano al rogito** come credito d\'imposta.'
  },
  {
    k: ['imu prima casa', 'esenzione imu', 'prima casa imu gratis'],
    r: '🏠 **IMU sulla prima casa**\n\nNo, la prima casa è **esente IMU**, tranne che per immobili di lusso (categorie catastali **A1, A8, A9**). L\'esenzione vale solo per l\'abitazione principale dove hai la residenza.'
  },
  {
    k: ['tari', 'tassa rifiuti', 'tassa spazzatura'],
    r: '🗑️ **TARI — Tassa rifiuti**\n\nÈ la tassa sui rifiuti. L\'importo dipende da:\n• **Metratura** dell\'immobile\n• **Numero di occupanti**\n• Tariffe del comune\n\nVa pagata dal momento in cui occupi l\'immobile. Il consulente può darti indicazioni sui costi nella tua zona.'
  },

  // ═══════════════════════════════════════════════
  // FAQ 130-138: MUTUO E FINANZIAMENTO
  // ═══════════════════════════════════════════════
  {
    k: ['come funziona il mutuo', 'mutuo spiegazione', 'mutuo ipotecario come funziona'],
    r: '🏦 **Come funziona un mutuo?**\n\nLa banca finanzia una parte del prezzo (fino all\'**80%**). Tu restituisci con **rate mensili** per 10-30 anni, con interessi. Il mutuo è garantito da ipoteca sull\'immobile acquistato.'
  },
  {
    k: ['quanto mutuo posso ottenere', 'importo massimo mutuo', 'mutuo massimo finanziabile'],
    r: '💶 **Quanto mutuo puoi ottenere?**\n\nDi norma fino all\'**80%** del valore di perizia. Regola importante:\n• La rata **non dovrebbe superare** il **30-35%** del reddito netto mensile\n\nEsempio: con €2.000 netti/mese → rata max €600-€700. Possiamo aiutarti a simulare il tuo mutuo.'
  },
  {
    k: ['fisso o variabile', 'tasso fisso o variabile', 'meglio fisso o variabile'],
    r: '📊 **Tasso fisso o variabile?**\n\n• **Fisso** — rata costante, più sicurezza, ideale per chi vuole tranquillità\n• **Variabile** — rata iniziale più bassa ma soggetta a variazioni di mercato\n\nDipende dalla tua **propensione al rischio** e dalla situazione di mercato. Il consulente ti aiuta a scegliere.'
  },
  {
    k: ['tempo ottenere mutuo', 'tempi mutuo', 'quanto tempo approvazione mutuo'],
    r: '⏱️ **Tempi per ottenere il mutuo**\n\nIn media **30-60 giorni** dalla richiesta:\n1. **Istruttoria** — verifica documenti e reddito\n2. **Perizia** — valutazione dell\'immobile\n3. **Delibera finale** — approvazione della banca\n\nNoi coordiniamo i tempi con la compravendita.'
  },
  {
    k: ['mutuo 100 percento', 'mutuo totale', 'mutuo senza anticipo'],
    r: '🏠 **Mutuo al 100%**\n\nÈ raro ma possibile con garanzie aggiuntive:\n• **Fondo Prima Casa Consap** — garanzia statale\n• Fideiussione di un familiare\n• Garanzie patrimoniali extra\n\nChiedi al consulente finanziario per valutare la tua situazione.'
  },
  {
    k: ['perizia bancaria immobile', 'perito della banca', 'perizia per il mutuo'],
    r: '🔍 **Perizia bancaria**\n\nÈ la valutazione dell\'immobile da parte di un **perito incaricato dalla banca**. Verifica che il valore sia congruo con il mutuo richiesto. Se il valore di perizia è inferiore al prezzo, la banca riduce l\'importo finanziabile.'
  },
  {
    k: ['costo perizia bancaria', 'perizia immobiliare costo', 'spesa perizia mutuo'],
    r: '💶 **Costo della perizia bancaria**\n\nGeneralmente tra **€200 e €400**, a carico dell\'acquirente. Alcune banche la includono nel pacchetto mutuo. È una spesa una tantum necessaria per l\'approvazione del finanziamento.'
  },
  {
    k: ['estinguere mutuo', 'estinzione anticipata', 'chiudere mutuo prima'],
    r: '✅ **Estinzione anticipata del mutuo**\n\nSì, **senza penali** dalla Legge Bersani (2007). Puoi estinguere:\n• **Parzialmente** — riduci la rata o la durata\n• **Totalmente** — chiudi il mutuo\n\nÈ un tuo diritto, in qualsiasi momento.'
  },
  {
    k: ['taeg', 'tasso annuo effettivo globale', 'taeg mutuo', 'costo effettivo mutuo'],
    r: '📊 **TAEG — Tasso Annuo Effettivo Globale**\n\nInclude interessi + **tutte le spese** accessorie del mutuo:\n• Spese istruttoria\n• Perizia\n• Assicurazioni obbligatorie\n\nÈ il dato **più utile** per confrontare offerte di mutuo diverse tra banche.'
  },

  // ═══════════════════════════════════════════════
  // FAQ 139-149: VENDITA
  // ═══════════════════════════════════════════════
  {
    k: ['come vendere il mio immobile', 'procedura di vendita', 'vendere casa passaggi'],
    r: '🏷️ **Come vendere il tuo immobile?**\n\nContattaci per una **valutazione gratuita**. Ci occupiamo di tutto:\n1. Valutazione professionale\n2. Foto e virtual tour 360°\n3. Pubblicazione su tutti i portali\n4. Gestione visite e trattativa\n5. Pratiche fino al rogito\n\n📞 **049 884 3484** oppure scrivi *"contattami"*.'
  },
  {
    k: ['quanto vale la mia casa', 'valore del mio immobile', 'stima della mia casa'],
    r: '🏠 **Quanto vale il tuo immobile?**\n\nRichiedi una **valutazione gratuita**. Analizziamo:\n• **Zona** e posizione\n• **Stato** e anno di costruzione\n• **Metratura** e tipologia\n• **Classe energetica**\n• **Mercato** di riferimento attuale\n\nPuoi anche provare la nostra **stima online** scrivendo *"stima"*!'
  },
  {
    k: ['tempo per vendere', 'tempi vendita immobile', 'vendita veloce'],
    r: '⏱️ **Tempi di vendita**\n\nDipende da prezzo, zona e stato. Con il giusto prezzo e una buona promozione:\n• **Centro Padova:** 2-3 mesi\n• **Prima cintura:** 3-4 mesi\n• **Provincia:** 4-6 mesi\n\nUn immobile **ben prezzato** e **ben presentato** si vende più velocemente.'
  },
  {
    k: ['lavori prima vendita', 'ristrutturare prima vendita', 'migliorare per vendere'],
    r: '🔧 **Lavori prima di vendere?**\n\nNon sempre necessari, ma piccoli interventi possono fare la differenza:\n• **Tinteggiatura** — rinfrescare le pareti\n• **Pulizia professionale** — prima impressione\n• **Home staging** — allestimento attraente\n\nPossono velocizzare la vendita e alzare il prezzo del **3-5%**.'
  },
  {
    k: ['home staging significato', 'cos è home staging', 'allestimento immobile vendita'],
    r: '🎨 **Cos\'è l\'home staging?**\n\nÈ l\'**allestimento professionale** dell\'immobile per renderlo più attraente:\n• Mobili e complementi strategici\n• Illuminazione studiata\n• Foto e visite più efficaci\n\nAumenta le possibilità di vendita e il prezzo finale. Noi offriamo anche **staging virtuale gratuito**!'
  },
  {
    k: ['vendere con mutuo', 'vendita mutuo in corso', 'casa ipotecata vendere'],
    r: '🏦 **Vendere con mutuo in corso**\n\nSì, è possibile! Il mutuo viene **estinto con il ricavato** della vendita al momento del rogito. La banca poi cancella l\'ipoteca. È una procedura standard, la gestiamo noi in coordinamento con la banca e il notaio.'
  },
  {
    k: ['documenti per vendere', 'carte per vendere casa', 'elenco documenti vendita'],
    r: '📋 **Documenti per vendere casa**\n\nServono:\n• **Atto di provenienza**\n• Visure catastali aggiornate\n• **APE** (Attestato Prestazione Energetica)\n• Certificazione impianti\n• Planimetria catastale\n• Documento d\'identità e codice fiscale\n\nNon preoccuparti, ti aiutiamo a raccogliere tutto!'
  },
  {
    k: ['tasse sulla vendita', 'pagare tasse vendita', 'fiscalità vendita'],
    r: '🧾 **Tasse sulla vendita**\n\nAttenzione se vendi **prima di 5 anni** dall\'acquisto con agevolazione prima casa senza riacquistare entro 1 anno:\n• Perdi i **benefici fiscali** goduti\n• Devi pagare la differenza di imposte + sanzioni\n\nSe vendi dopo 5 anni, generalmente nessuna tassa aggiuntiva.'
  },
  {
    k: ['plusvalenza immobiliare', 'tassa sulla plusvalenza', 'plusvalenza 26 percento'],
    r: '💰 **Plusvalenza immobiliare**\n\nÈ la differenza tra prezzo di **vendita** e prezzo di **acquisto**. Se vendi entro 5 anni (e non è prima casa):\n• Tassazione IRPEF ordinaria, oppure\n• Imposta sostitutiva del **26%**\n\n**Esente** se l\'immobile è stato adibito a prima casa per la maggior parte del periodo.'
  },
  {
    k: ['vendere prima comprare', 'sincronizzare vendita acquisto', 'prima vendere o comprare'],
    r: '🔄 **Meglio vendere prima di comprare?**\n\nDipende dalla tua situazione:\n• **Vendere prima** — più sicurezza economica, ma devi trovare un alloggio temporaneo\n• **Comprare prima** — rischio di avere due immobili temporaneamente\n\nIl consulente può aiutarti a **sincronizzare** vendita e acquisto per evitare problemi.'
  },
  {
    k: ['incarico in esclusiva', 'mandato esclusivo vendita', 'esclusiva agenzia immobiliare'],
    r: '📝 **Incarico in esclusiva**\n\nAffidi la vendita a **una sola agenzia** per un periodo concordato. Vantaggi:\n• Più **impegno** e investimento promozionale\n• Strategia di vendita **dedicata**\n• Un unico interlocutore\n\nL\'esclusiva ci permette di investire al massimo nella promozione del tuo immobile.'
  },

  // ═══════════════════════════════════════════════
  // FAQ 150-155: AFFITTO
  // ═══════════════════════════════════════════════
  {
    k: ['tipi contratto affitto', 'contratto locazione tipi', 'affitto 4+4', 'affitto 3+2', 'contratto transitorio'],
    r: '📄 **Tipi di contratto d\'affitto**\n\n• **Libero (4+4)** — canone libero, durata 4 anni + rinnovo automatico di 4\n• **Concordato (3+2)** — canone calmierato con vantaggi fiscali\n• **Transitorio (1-18 mesi)** — per esigenze temporanee documentate\n• **Studenti (6-36 mesi)** — riservato a studenti universitari fuori sede\n\nTi aiutiamo a scegliere la formula più adatta.'
  },
  {
    k: ['canone concordato cos è', 'affitto concordato vantaggi', 'contratto concordato'],
    r: '🤝 **Contratto a canone concordato**\n\nIl canone è stabilito in base ad **accordi territoriali** tra associazioni. Vantaggi:\n• **Proprietario:** cedolare secca ridotta al 10%, sconto IMU\n• **Inquilino:** canone inferiore al mercato, detrazioni fiscali\n\nConviene a entrambe le parti. Chiedi al consulente se è applicabile nella tua zona.'
  },
  {
    k: ['deposito cauzionale affitto', 'cauzione locazione', 'quante mensilità cauzione'],
    r: '💶 **Deposito cauzionale**\n\nGeneralmente **2-3 mensilità** di canone, versate all\'inizio della locazione. Il deposito:\n• Viene **restituito a fine locazione**\n• Al netto di eventuali danni documentati\n• Non può essere usato come pagamento degli ultimi mesi\n\nProduce interessi legali a favore dell\'inquilino.'
  },
  {
    k: ['aumento affitto', 'proprietario aumenta affitto', 'adeguamento istat affitto'],
    r: '📈 **Aumento dell\'affitto**\n\nIl proprietario può aumentare il canone solo:\n• Con **adeguamento ISTAT** annuale (se previsto dal contratto), generalmente al 75% dell\'indice\n• Al **rinnovo** del contratto, nei limiti di legge\n\nAumenti arbitrari non sono consentiti. Verifica sempre le clausole del tuo contratto.'
  },
  {
    k: ['preavviso affitto', 'disdetta affitto', 'lasciare affitto quanto preavviso'],
    r: '📬 **Preavviso per lasciare l\'affitto**\n\nGeneralmente **6 mesi** di preavviso, da comunicare con **raccomandata A/R** (o PEC). Attenzione:\n• Il preavviso decorre dal mese successivo alla ricezione\n• Verifica le condizioni specifiche nel tuo contratto\n• In alcuni casi (trasferimento lavoro, gravi motivi) è possibile recedere con preavviso ridotto.'
  },
  {
    k: ['spese condominiali in affitto', 'oneri accessori locazione', 'condominiali ordinarie straordinarie'],
    r: '🏢 **Spese condominiali in affitto**\n\n• **Inquilino** — spese ordinarie: pulizia scale, ascensore, luce parti comuni, giardinaggio, portineria\n• **Proprietario** — spese straordinarie: rifacimento facciata, sostituzione impianti, lavori strutturali\n\nVerifica sempre il contratto per le ripartizioni specifiche concordate.'
  },

  // ═══════════════════════════════════════════════
  // FAQ 156-165: ASPETTI LEGALI
  // ═══════════════════════════════════════════════
  {
    k: ['diritto prelazione cos è', 'prelazione immobile', 'prelazione affitto commerciale'],
    r: '⚖️ **Diritto di prelazione**\n\nÈ il diritto di essere **preferiti nell\'acquisto** a parità di condizioni. Esiste per legge:\n• Negli **immobili commerciali** in affitto\n• Per i **coeredi** in caso di vendita di quote ereditarie\n• In alcuni contratti agrari\n\nIl venditore deve notificare l\'intenzione di vendita. Noi verifichiamo sempre eventuali prelazioni.'
  },
  {
    k: ['ipoteca significato', 'garanzia ipotecaria', 'ipoteca sulla casa'],
    r: '🏦 **Ipoteca sull\'immobile**\n\nÈ una **garanzia reale** a favore della banca che finanzia il mutuo. Punti chiave:\n• Viene iscritta al momento della concessione del mutuo\n• Si cancella **automaticamente** dopo l\'estinzione del mutuo\n• Non impedisce di vivere nell\'immobile o di venderlo\n\nÈ la garanzia standard per ogni mutuo ipotecario.'
  },
  {
    k: ['comprare immobile ipoteca', 'casa con ipoteca', 'acquisto casa ipotecata'],
    r: '🔓 **Comprare un immobile con ipoteca?**\n\nSì, è possibile e abbastanza comune! L\'ipoteca viene **cancellata al rogito**: il notaio trattiene dal prezzo la somma per estinguere il mutuo residuo del venditore. Noi verifichiamo in anticipo la situazione ipotecaria completa.'
  },
  {
    k: ['donazione immobiliare rischi', 'casa donata rischi', 'impugnazione donazione', 'eredità legittimari donazione'],
    r: '⚠️ **Donazione immobiliare — Rischi**\n\nAttenzione: la donazione può essere **impugnata dagli eredi legittimari** entro 20 anni. Conseguenze:\n• Le banche spesso **non concedono mutui** su immobili donati\n• L\'acquirente rischia la restituzione\n• Esistono polizze assicurative specifiche, ma non sempre bastano\n\nSe l\'immobile che ti interessa proviene da donazione, **parlane subito con il consulente**.'
  },
  {
    k: ['nuda proprietà significato', 'comprare nuda proprietà', 'investire in nuda proprietà'],
    r: '🏠 **Nuda proprietà**\n\nAcquisti la **proprietà** ma l\'usufruttuario (spesso l\'anziano venditore) continua ad abitarci vita natural durante. Vantaggi:\n• Prezzo ridotto del **20-50%** rispetto al pieno valore\n• Buon investimento a lungo termine\n• Imposte calcolate sul valore della nuda proprietà\n\nIl prezzo dipende dall\'età dell\'usufruttuario.'
  },
  {
    k: ['servitù cosa sono', 'servitù immobiliare', 'diritto di passaggio'],
    r: '🚶 **Servitù immobiliari**\n\nSono diritti di terzi sull\'immobile, ad esempio:\n• **Servitù di passaggio** — diritto di attraversare la proprietà\n• **Servitù di veduta** — distanze minime per finestre\n• **Servitù di scarico** — tubature che attraversano il fondo\n\nVanno verificate **prima dell\'acquisto** perché vincolano la proprietà permanentemente.'
  },
  {
    k: ['usucapione cos è', 'usucapione immobile', 'proprietà per possesso'],
    r: '⏳ **Usucapione**\n\nSi diventa proprietari di un immobile dopo averlo posseduto **ininterrottamente per 20 anni**, in modo:\n• Pacifico e pubblico\n• Continuo e non contestato\n\nServe una **sentenza del tribunale** per formalizzare il passaggio di proprietà. È una procedura lunga e complessa.'
  },
  {
    k: ['comprare casa separato', 'acquisto casa divorziato', 'separazione e acquisto'],
    r: '⚖️ **Acquisto casa da separato/divorziato**\n\nSì, è possibile comprare casa. Tuttavia è consigliabile:\n• Verificare la **situazione patrimoniale** con un legale\n• Controllare eventuali vincoli da accordi di separazione\n• Valutare il regime patrimoniale (comunione/separazione dei beni)\n\nUn legale può aiutarti a evitare complicazioni future.'
  },
  {
    k: ['vizi occulti dopo acquisto', 'difetti non dichiarati', 'problemi nascosti immobile'],
    r: '🔍 **Vizi occulti dopo l\'acquisto**\n\nSe scopri difetti non dichiarati dal venditore:\n• Hai **8 giorni dalla scoperta** per denunciarli\n• **1 anno** per agire legalmente\n• Il venditore è responsabile per i vizi **non visibili** al momento dell\'acquisto\n\nPer questo noi effettuiamo sempre verifiche approfondite prima del rogito.'
  },
  {
    k: ['comunione dei beni acquisto', 'separazione beni casa', 'regime patrimoniale acquisto'],
    r: '💍 **Comunione dei beni e acquisto**\n\n• **Comunione dei beni** — l\'immobile è di entrambi i coniugi al **50%**, anche se paga uno solo\n• **Separazione dei beni** — è solo di chi lo acquista\n\nÈ importante scegliere il regime patrimoniale consapevolmente, anche in vista di futuri acquisti immobiliari.'
  },

  // ═══════════════════════════════════════════════
  // FAQ 166-173: RISTRUTTURAZIONE E BONUS
  // ═══════════════════════════════════════════════
  {
    k: ['bonus ristrutturazione esistono', 'agevolazioni ristrutturazione', 'detrazioni casa lavori'],
    r: '🏗️ **Bonus per la ristrutturazione**\n\nSì, esistono diverse agevolazioni fiscali che cambiano periodicamente:\n• Bonus ristrutturazione\n• Ecobonus (risparmio energetico)\n• Bonus mobili\n• Sismabonus\n\nLe aliquote e i limiti variano. **Chiedi al consulente** per le agevolazioni attualmente in vigore nella tua situazione.'
  },
  {
    k: ['detrazione ristrutturazione edilizia', 'bonus lavori edilizia', 'recupero fiscale ristrutturazione'],
    r: '💰 **Bonus ristrutturazione**\n\nÈ una **detrazione fiscale** sulle spese di ristrutturazione edilizia, recuperata in 10 rate annuali in dichiarazione dei redditi. L\'aliquota e i limiti di spesa variano in base alla normativa vigente.\n\nPer sfruttarlo: conserva tutte le fatture e paga con **bonifico parlante**.'
  },
  {
    k: ['ristrutturare prima rogito', 'lavori prima acquisto', 'ristrutturazione prima atto'],
    r: '⚠️ **Ristrutturare prima del rogito?**\n\nSolo con **autorizzazione scritta** del venditore. Attenzione:\n• I lavori restano sul suo immobile se la vendita salta\n• Non puoi accedere ai bonus fiscali senza essere proprietario\n\nÈ più prudente **attendere il trasferimento di proprietà**. In alternativa, inserisci accordi specifici nel preliminare.'
  },
  {
    k: ['permesso ristrutturare', 'serve permesso lavori', 'autorizzazione lavori casa'],
    r: '📋 **Permessi per ristrutturare**\n\nDipende dai lavori:\n• **Edilizia libera** — tinteggiatura, pavimenti, sanitari (nessun titolo)\n• **CILA** — manutenzione straordinaria leggera\n• **SCIA** — lavori importanti senza cambio volumetria\n• **Permesso di Costruire** — ampliamenti e modifiche strutturali\n\nIl tuo tecnico di fiducia sa consigliarti il titolo giusto.'
  },
  {
    k: ['cila', 'comunicazione inizio lavori asseverata', 'cila significato'],
    r: '📝 **CILA — Comunicazione Inizio Lavori Asseverata**\n\nServe per lavori di **manutenzione straordinaria leggera**, ad esempio:\n• Spostare tramezzi (muri non portanti)\n• Rifare impianti\n• Modificare la distribuzione interna\n\nVa presentata in Comune da un tecnico abilitato. Il costo del tecnico varia da €500 a €1.500.'
  },
  {
    k: ['scia edilizia', 'scia significato', 'segnalazione certificata inizio attività'],
    r: '📋 **SCIA — Segnalazione Certificata di Inizio Attività**\n\nServe per lavori più importanti che **non modificano la volumetria**:\n• Ristrutturazione edilizia\n• Restauro e risanamento conservativo\n• Varianti in corso d\'opera\n\nI lavori possono iniziare dalla data di presentazione. Va redatta da un tecnico abilitato.'
  },
  {
    k: ['costo ristrutturazione al mq', 'prezzo ristrutturazione completa', 'ristrutturare quanto costa'],
    r: '💶 **Costo ristrutturazione completa**\n\nA Padova, indicativamente:\n• **Ristrutturazione base:** €500-€600/mq\n• **Medio livello:** €600-€800/mq\n• **Alto livello:** €800-€1.200/mq\n\nIl costo varia molto in base a materiali, impianti e finiture scelte. Consigliamo sempre di richiedere **almeno 3 preventivi**.'
  },
  {
    k: ['abbattere muro portante', 'demolire muro portante', 'muro portante si può togliere'],
    r: '🧱 **Abbattere un muro portante**\n\nÈ possibile ma **non è un intervento banale**:\n• Serve il progetto di un **ingegnere strutturista**\n• È necessario il **Permesso di Costruire**\n• Vanno inserite travi o pilastri sostitutivi\n• Costo indicativo: €3.000-€8.000 (solo struttura)\n\nMai improvvisare: la sicurezza della struttura è prioritaria.'
  },

  // ═══════════════════════════════════════════════
  // FAQ 174-179: VALUTAZIONE E MERCATO
  // ═══════════════════════════════════════════════
  {
    k: ['come valutare immobile', 'criteri valutazione casa', 'cosa influenza prezzo casa'],
    r: '📊 **Come si valuta un immobile?**\n\nI fattori principali:\n• **Zona** e posizione nel quartiere\n• **Metratura** commerciale\n• **Stato** conservativo (ristrutturato vs da ristrutturare)\n• **Classe energetica**\n• **Piano** ed esposizione\n• **Pertinenze** (garage, cantina, giardino)\n• Andamento del **mercato locale**\n\nRichiedi la nostra valutazione gratuita per un\'analisi professionale.'
  },
  {
    k: ['prezzo metro quadro cos è', 'prezzo mq significato', 'valore mq'],
    r: '📏 **Prezzo al metro quadro**\n\nÈ il valore medio di compravendita per mq nella zona. Un riferimento utile, ma va adattato a:\n• Caratteristiche specifiche dell\'immobile\n• Piano e luminosità\n• Stato di manutenzione\n• Presenza di pertinenze\n\nDue appartamenti nella stessa via possono avere prezzi/mq molto diversi.'
  },
  {
    k: ['prezzi immobili padova', 'quanto costa casa padova', 'valore case padova zona'],
    r: '🏠 **Prezzi immobili — Zona Padova**\n\nIndicativamente (2024):\n• **Centro storico:** €2.500-€4.000/mq\n• **Semicentro:** €1.500-€2.500/mq\n• **Prima cintura:** €1.200-€2.000/mq\n• **Provincia:** €1.000-€1.800/mq\n\nI valori variano molto in base allo stato e alle caratteristiche. Per una stima precisa, chiedi la nostra **valutazione gratuita**.'
  },
  {
    k: ['dati omi cosa sono', 'quotazioni omi', 'osservatorio mercato immobiliare'],
    r: '📈 **Dati OMI**\n\nSono le quotazioni dell\'**Osservatorio del Mercato Immobiliare** dell\'Agenzia delle Entrate. Indicano:\n• Valori **minimi e massimi** per zona\n• Distinti per tipologia e stato conservativo\n• Aggiornati semestralmente\n\nSono un riferimento utile ma **non vincolante**. La valutazione reale considera molti più fattori.'
  },
  {
    k: ['momento giusto comprare', 'conviene comprare adesso', 'quando comprare casa'],
    r: '🤔 **È il momento giusto per comprare?**\n\nDipende da più fattori:\n• Le tue **esigenze personali** e familiari\n• La tua **capacità finanziaria**\n• L\'andamento dei **tassi di interesse**\n• Il mercato locale\n\nIl momento migliore è quando hai trovato la casa giusta alle condizioni giuste per te. Il consulente ti aiuta a valutare.'
  },
  {
    k: ['comprare casa investimento', 'investimento immobiliare conviene', 'rendita affitto'],
    r: '📊 **Casa come investimento**\n\nDipende da diversi fattori:\n• **Zona** — posizioni centrali rendono di più\n• **Prezzo d\'acquisto** — comprare bene è metà del guadagno\n• **Mercato affitti** — domanda e canoni medi\n• **Costi** — tasse, manutenzione, gestione\n\nA Padova, la rendita lorda da affitto si aggira sul **4-6%** annuo. Il consulente può aiutarti a valutare le opportunità.'
  },

  // ═══════════════════════════════════════════════
  // FAQ 180-200: SERVIZIO E ASSISTENZA
  // ═══════════════════════════════════════════════
  {
    k: ['contattare consulente', 'parlare con agente', 'come vi contatto'],
    r: '📞 **Contattaci!**\n\nSiamo disponibili su più canali:\n• **Telefono:** 049 884 3484\n• **WhatsApp:** scrivici direttamente\n• **Email:** dal form sul sito\n• **Di persona:** in ufficio su appuntamento\n\nTi ricontatteremo **in giornata**. Oppure scrivi *"contattami"* qui in chat!'
  },
  {
    k: ['offrite valutazione gratuita', 'stima senza impegno casa', 'valutazione gratuita immobile'],
    r: '🏠 **Valutazione gratuita**\n\nSì, offriamo una valutazione **gratuita e senza impegno** del tuo immobile. Come funziona:\n1. Ci contatti o scrivi *"stima"* in chat\n2. Fissiamo un sopralluogo\n3. Analizziamo l\'immobile e il mercato\n4. Ti consegniamo la valutazione\n\nNessun costo, nessun obbligo. 📞 **049 884 3484**'
  },
  {
    k: ['zone servite', 'comuni coperti', 'quali zone padova'],
    r: '📍 **Dove operiamo**\n\nPrincipalmente a **Padova e provincia**:\n• Padova centro e semicentro\n• Limena, Villafranca Padovana\n• Campodarsego, Vigonza\n• Noventa Padovana\n• Comuni limitrofi\n\nConosciamo il mercato locale in modo approfondito. Per zone specifiche, chiedici!'
  },
  {
    k: ['visita weekend', 'appuntamento sabato', 'visita sabato domenica'],
    r: '📅 **Visite nel weekend**\n\nSì, organizziamo visite anche il **sabato**! Contattaci per fissare un appuntamento nell\'orario più comodo per te. La flessibilità è un nostro punto di forza.\n\n📞 **049 884 3484** oppure scrivi *"contattami"* per prenotare.'
  },
  {
    k: ['tour virtuale 360', 'visita virtuale online', 'esplorare casa da remoto'],
    r: '🖥️ **Virtual tour 360°**\n\nMolti nostri immobili dispongono del virtual tour interattivo:\n• Naviga **stanza per stanza**\n• Ruota la vista a **360°**\n• Zoom sui dettagli\n• Disponibile su **smartphone e PC**\n\nPuoi esplorare la casa comodamente da casa tua, prima di decidere se visitarla di persona!'
  },
  {
    k: ['come funziona virtual tour', 'usare virtual tour', 'navigare virtual tour'],
    r: '🎯 **Come funziona il virtual tour**\n\nÈ semplicissimo:\n1. Apri il link dell\'immobile\n2. Clicca e trascina per **ruotare la vista**\n3. Usa i punti di navigazione per **cambiare stanza**\n4. Pinch o rotella per lo **zoom**\n\nÈ come essere lì di persona! Ideale per una prima selezione prima della visita.'
  },
  {
    k: ['video immobili', 'youtube immobili', 'filmati case'],
    r: '🎬 **Video degli immobili**\n\nSì, realizziamo **video professionali** per i nostri immobili:\n• Riprese interne ed esterne\n• Drone per viste aeree\n• Pubblicati sul nostro canale **YouTube**\n\nUna visione completa e realistica dell\'immobile prima ancora di visitarlo.'
  },
  {
    k: ['newsletter immobili', 'aggiornamenti nuove case', 'notifiche nuovi immobili'],
    r: '🔔 **Resta aggiornato!**\n\nPer non perdere nessuna opportunità:\n• Iscriviti alla nostra **newsletter**\n• Attiva le **notifiche** personalizzate\n• Seguici sui **social**\n\nTi avviseremo appena viene inserito un immobile che corrisponde ai tuoi criteri di ricerca. Scrivi *"contattami"* per attivare il servizio!'
  },
  {
    k: ['non trovo casa', 'immobile non trovato', 'cerco casa specifica'],
    r: '🔎 **Non trovi l\'immobile che cerchi?**\n\nNon preoccuparti! Contattaci con le tue esigenze:\n• Abbiamo anche immobili **non ancora pubblicati**\n• Possiamo cercare **attivamente** per te nella zona desiderata\n• Ti avvisiamo appena troviamo qualcosa di adatto\n\nScrivici le tue esigenze o clicca *"contattami"*. Troviamo la tua casa insieme!'
  },
  {
    k: ['durata visita immobile', 'quanto dura visita', 'tempo visita casa'],
    r: '⏱️ **Durata della visita**\n\nUna visita dura circa **20-30 minuti**. Per sfruttarla al meglio:\n• Prepara le **domande** in anticipo\n• Controlla **infissi**, impianti e umidità\n• Osserva la **luminosità** nelle diverse ore\n• Valuta il **quartiere** e i servizi vicini\n\nIl consulente è lì per rispondere a ogni tua curiosità.'
  },
  {
    k: ['portare tecnico visita', 'geometra visita', 'ingegnere sopralluogo'],
    r: '👷 **Portare un tecnico alla visita?**\n\nAssolutamente sì, anzi **lo consigliamo**! Un tecnico di fiducia può:\n• Valutare lo stato degli **impianti**\n• Verificare eventuali **problemi strutturali**\n• Stimare i costi di eventuali **lavori**\n• Controllare la **conformità** dell\'immobile\n\nÈ un investimento che può farti risparmiare molto.'
  },
  {
    k: ['cosa portare proposta acquisto', 'documenti per proposta', 'proposta cosa serve'],
    r: '📋 **Cosa portare per la proposta d\'acquisto**\n\n• **Documento d\'identità** in corso di validità\n• **Codice fiscale**\n• **Assegno bancario** (non trasferibile) per la caparra\n\nIl consulente ti guida passo passo nella compilazione. Non preoccuparti, pensiamo a tutto noi!'
  },
  {
    k: ['fate anche affitti', 'gestite locazioni', 'affitto disponibile'],
    r: '🏠 **Locazioni**\n\nSì, gestiamo sia **vendite** che **affitti**! Il nostro servizio locazioni include:\n• Ricerca inquilini qualificati\n• Verifica affidabilità\n• Contratto e registrazione\n• Assistenza continua\n\nContattaci per conoscere gli immobili disponibili in locazione. 📞 **049 884 3484**'
  },
  {
    k: ['due diligence immobiliare', 'verifica documentale completa', 'controllo completo prima acquisto'],
    r: '🔍 **Due diligence immobiliare**\n\nÈ la **verifica completa** della documentazione:\n• **Urbanistica** — conformità edilizia e permessi\n• **Catastale** — planimetrie e rendite\n• **Ipotecaria** — gravami e ipoteche\n• **Condominiale** — spese e delibere\n\nNoi la eseguiamo **sempre**, è inclusa nel nostro servizio. La tua sicurezza viene prima di tutto.'
  },
  {
    k: ['acquistare dall estero', 'comprare casa estero', 'procura notarile acquisto'],
    r: '🌍 **Acquistare dall\'estero**\n\nSì, è possibile anche con **procura notarile**: un delegato firma per tuo conto. Ti assistiamo in tutto il processo:\n• Videochiamate per le visite\n• Coordinamento con notaio e banca\n• Gestione documentale a distanza\n\nAbbiamo esperienza con acquirenti internazionali.'
  },
  {
    k: ['trascrizione del preliminare', 'preliminare trascritto registri', 'differenza registrazione trascrizione'],
    r: '📋 **Compromesso registrato vs trascritto**\n\n• **Registrato** — obbligatorio, presso l\'Agenzia delle Entrate (€200 + imposte)\n• **Trascritto** — facoltativo, nei registri immobiliari. Offre **maggiore tutela**:\n  - Protegge da ipoteche successive\n  - Protegge da vendite a terzi\n  - Costo aggiuntivo ma più sicurezza\n\nPer importi elevati, la trascrizione è fortemente consigliata.'
  },
  {
    k: ['residenza dopo acquisto', 'trasferire residenza prima casa', 'tempo residenza prima casa'],
    r: '🏠 **Trasferimento residenza — Prima casa**\n\nHai **18 mesi dalla data del rogito** per trasferire la residenza nel comune dell\'immobile. Se non lo fai:\n• Perdi le **agevolazioni fiscali** (risparmio del 7% di imposta)\n• Devi restituire la differenza + sanzioni\n\nSegna la data e non dimenticarti! Il consulente ti ricorda la scadenza.'
  },
  {
    k: ['casa intestata figlio minorenne', 'immobile minorenne', 'acquisto per figlio minore'],
    r: '👶 **Intestare casa a figlio minorenne**\n\nÈ possibile ma serve l\'**autorizzazione del Giudice Tutelare**:\n• Va presentata istanza al tribunale\n• Il giudice verifica l\'interesse del minore\n• Tempi aggiuntivi (1-3 mesi)\n\nÈ una procedura specifica che richiede l\'assistenza di un legale. Possiamo metterti in contatto con un professionista.'
  },
  {
    k: ['classe catastale significato', 'categoria a2 a3 a4', 'categorie catastali abitazione'],
    r: '🏷️ **Classe catastale**\n\nIndica la **categoria** e il livello dell\'immobile:\n• **A/1** — abitazione signorile\n• **A/2** — abitazione civile\n• **A/3** — abitazione economica\n• **A/4** — abitazione popolare\n• **A/7** — villini\n\nInfluisce sulla **rendita catastale** e quindi sulle imposte. Le categorie A/1, A/8, A/9 pagano l\'IMU anche come prima casa.'
  },
  {
    k: ['accatastato significato', 'immobile registrato al catasto', 'cosa significa accatastato'],
    r: '📋 **Immobile accatastato**\n\nSignifica che è **registrato al Catasto** con:\n• Una **planimetria** depositata\n• Una **rendita catastale** attribuita\n• Una **categoria** assegnata (A/2, A/3, ecc.)\n\nÈ obbligatorio per tutti gli immobili. Un immobile non accatastato non può essere venduto né ipotecato.'
  },
  {
    k: ['cosa controllare prima firmare', 'attenzione documenti', 'firmare documenti immobiliare'],
    r: '✍️ **Prima di firmare qualsiasi documento**\n\nRegole d\'oro:\n• **Leggi tutto** con attenzione, senza fretta\n• **Chiedi spiegazioni** su ogni punto non chiaro\n• Non firmare mai **sotto pressione**\n• Consulta il tuo **legale o consulente** in caso di dubbi\n• Conserva sempre una **copia** di tutto\n\nNoi spieghiamo ogni documento in modo chiaro e trasparente. La tua consapevolezza è la nostra priorità.'
  },

  // ═══════════════════════════════════════════════
  // SEZIONE 3: APPROFONDIMENTI PROFESSIONALI
  // FAQ 201-211: CONTRATTI DI LOCAZIONE
  // ═══════════════════════════════════════════════
  {
    k: ['contratto 4+4 spiegazione', 'locazione 4+4 come funziona', 'contratto abitativo libero'],
    r: '📄 **Contratto di locazione 4+4**\n\nÈ il contratto d\'affitto più comune per uso abitativo:\n• Dura **4 anni** + rinnovo automatico di **altri 4**\n• Il canone è **libero**, concordato tra le parti\n• Disdetta con **6 mesi di preavviso**\n\nAlla scadenza degli 8 anni, si rinnova tacitamente salvo nuova disdetta.'
  },
  {
    k: ['disdetta 4+4 prima scadenza', 'recedere contratto affitto anticipato', 'uscire dal 4+4'],
    r: '📬 **Disdire un contratto 4+4 prima della scadenza**\n\n**Inquilino:** può recedere in qualsiasi momento con **6 mesi di preavviso** e per gravi motivi (trasferimento lavoro, problemi economici documentati).\n\n**Proprietario:** può disdire solo alla **prima scadenza** (4 anni) e solo per motivi specifici previsti dalla legge (art. 3, L. 431/98).'
  },
  {
    k: ['motivi disdetta proprietario', 'quando proprietario può disdire', 'disdetta primo rinnovo'],
    r: '⚖️ **Motivi di disdetta del proprietario al primo rinnovo**\n\nIl proprietario può disdire il 4+4 alla prima scadenza solo per:\n• **Uso proprio** o di familiari stretti\n• **Vendita** dell\'immobile (se non ne possiede altri)\n• **Ristrutturazione integrale** dell\'edificio\n• Destinazione a **uso non abitativo**\n\nDeve comunicarlo con **raccomandata almeno 6 mesi prima** della scadenza.'
  },
  {
    k: ['contratto locazione commerciale', 'affitto negozio', 'locazione 6+6', 'affitto ufficio contratto'],
    r: '🏪 **Contratto di locazione commerciale**\n\nPer immobili ad uso diverso dall\'abitativo (negozi, uffici, laboratori):\n• Durata minima: **6 anni** + rinnovo di **altri 6** (6+6)\n• Per attività alberghiere: **9+9**\n• Canone libero\n\nOffre maggiori tutele all\'inquilino rispetto all\'abitativo, incluso il diritto di prelazione.'
  },
  {
    k: ['6+6 obbligatorio', 'durata minima commerciale', 'contratto commerciale meno 6 anni'],
    r: '📋 **Il contratto commerciale 6+6 è obbligatorio?**\n\nSì, la durata minima di **6 anni** è prevista dalla legge (L. 392/78). Non si può stipulare un contratto commerciale di durata inferiore, salvo:\n• Contratto **transitorio** per esigenze particolari\n• Attività con carattere **stagionale**\n\nClausole con durata inferiore sono **nulle**.'
  },
  {
    k: ['prelazione inquilino commerciale', 'diritto prelazione conduttore', 'prelazione vendita locale'],
    r: '🏷️ **Prelazione dell\'inquilino commerciale**\n\nSì, a differenza dell\'abitativo, l\'inquilino commerciale ha il **diritto di prelazione**:\n• Il proprietario deve offrire l\'immobile **alle stesse condizioni** proposte a terzi\n• L\'inquilino ha **60 giorni** per rispondere\n• Se non viene rispettata, l\'inquilino può riscattare l\'immobile dal nuovo acquirente\n\nÈ una tutela molto forte per chi ha un\'attività avviata.'
  },
  {
    k: ['indennità avviamento commerciale', 'indennità 18 mensilità', 'fine locazione commerciale indennità'],
    r: '💶 **Indennità di avviamento commerciale**\n\nSe il proprietario non rinnova il contratto commerciale alla scadenza, deve pagare all\'inquilino:\n• **18 mensilità** dell\'ultimo canone\n• **21 mensilità** per attività alberghiere\n\nÈ una tutela per l\'attività avviata dall\'inquilino. Non è dovuta se è l\'inquilino a non rinnovare.'
  },
  {
    k: ['cedere contratto commerciale', 'cessione locazione azienda', 'subentro contratto negozio'],
    r: '🔄 **Cessione del contratto commerciale**\n\nSì, è possibile cedere il contratto insieme alla **cessione o affitto dell\'azienda**:\n• Il proprietario **non può opporsi**, salvo gravi motivi\n• Deve essere **informato** per iscritto\n• Il cedente resta obbligato in solido per un anno\n\nÈ una norma che facilita il passaggio di attività commerciali.'
  },
  {
    k: ['contratto transitorio come funziona', 'locazione temporanea', 'affitto breve termine'],
    r: '⏳ **Contratto di locazione transitorio**\n\nContratto a breve termine, da **1 a 18 mesi**, per esigenze temporanee documentate:\n• Trasferimento lavorativo\n• Studio fuori sede\n• Trasloco in corso\n• Ristrutturazione della propria casa\n\n**Non si rinnova automaticamente.** L\'esigenza transitoria va dichiarata e documentata nel contratto.'
  },
  {
    k: ['quando fare transitorio', 'requisiti contratto transitorio', 'esigenza transitoria documentata'],
    r: '📋 **Quando si può fare un contratto transitorio?**\n\nSolo se c\'è un\'esigenza temporanea **reale e documentata**:\n• Trasferimento lavorativo temporaneo (lettera del datore)\n• Attesa di ristrutturazione (preventivo lavori)\n• Separazione in corso (atto legale)\n• Assistenza a familiari (certificato medico)\n\nSenza documentazione, il contratto è **nullo** e si trasforma in 4+4.'
  },
  {
    k: ['transitorio si rinnova', 'scadenza transitorio cosa succede', 'transitorio diventa 4+4'],
    r: '🔄 **Il contratto transitorio si rinnova?**\n\nNo, si conclude alla **scadenza pattuita**. Attenzione:\n• Se l\'esigenza transitoria è **cessata prima** della scadenza → si trasforma automaticamente in **4+4**\n• Se alla scadenza l\'inquilino non lascia l\'immobile → il proprietario deve agire per lo sfratto\n\nÈ importante che l\'esigenza temporanea sia reale e documentabile.'
  },
  {
    k: ['contratto concordato 3+2 dettaglio', 'locazione concordato come funziona', 'concordato territoriale affitto'],
    r: '🤝 **Contratto concordato (3+2) — Approfondimento**\n\nDura **3 anni + 2 di rinnovo automatico**. Caratteristiche:\n• Il canone è stabilito dagli **accordi territoriali**\n• Serve l\'**attestazione** di un\'associazione di categoria\n• Vantaggi fiscali per entrambe le parti\n\nÈ la formula più vantaggiosa in termini fiscali, ma il canone è calmierato.'
  },
  {
    k: ['vantaggi fiscali concordato dettaglio', 'cedolare secca 10 concordato', 'risparmio concordato'],
    r: '💰 **Vantaggi fiscali del contratto concordato**\n\n**Per il proprietario:**\n• Cedolare secca al **10%** (anziché 21%)\n• Riduzione IMU fino al **25%**\n• Base imponibile IRPEF ridotta del 30%\n\n**Per l\'inquilino:**\n• Canone inferiore al mercato\n• Possibili detrazioni sul canone\n\nUn risparmio significativo per entrambi.'
  },
  {
    k: ['comuni contratto concordato', 'accordo territoriale comune', 'alta tensione abitativa'],
    r: '🏘️ **Contratto concordato: quali comuni?**\n\nNon tutti i comuni possono applicarlo. Serve un **accordo territoriale** tra associazioni di categoria:\n• È **obbligatorio** nei comuni ad alta tensione abitativa\n• Altri comuni possono adottarlo volontariamente\n• Padova e provincia hanno accordi attivi\n\nVerifica se il tuo comune ha un accordo. Noi possiamo aiutarti a verificarlo.'
  },
  {
    k: ['calcolo canone concordato', 'tabelle canone concordato', 'come si determina canone'],
    r: '🧮 **Come si calcola il canone concordato?**\n\nIl canone è determinato da **tabelle** allegate all\'accordo territoriale, in base a:\n• **Zona** dell\'immobile (fascia A, B, C...)\n• **Metratura** e tipologia\n• **Stato** conservativo e dotazioni\n• Anno di costruzione\n\nServe l\'**attestazione** di un\'associazione di categoria. Noi collaboriamo con le associazioni locali.'
  },
  {
    k: ['attestazione conformità concordato', 'associazione attestazione affitto', 'attestazione obbligatoria concordato'],
    r: '📋 **Attestazione per il contratto concordato**\n\nÈ **obbligatoria** per accedere ai benefici fiscali:\n• Rilasciata da almeno una delle **associazioni firmatarie** dell\'accordo\n• Certifica che il canone è conforme alle tabelle\n• Costo: generalmente **€50-€150**\n\nSenza attestazione, non hai diritto alla cedolare al 10% né allo sconto IMU.'
  },

  // ═══════════════════════════════════════════════
  // FAQ 217-223: REGISTRAZIONE CONTRATTI E PRELIMINARI
  // ═══════════════════════════════════════════════
  {
    k: ['obbligo registrazione locazione', 'registrare affitto obbligatorio', 'contratto non registrato'],
    r: '⚖️ **Obbligo di registrazione del contratto di locazione**\n\nSì, **sempre obbligatorio**. Tutti i contratti con durata superiore a 30 giorni vanno registrati all\'Agenzia delle Entrate **entro 30 giorni** dalla firma.\n\nLa registrazione può essere fatta:\n• Online tramite il portale dell\'Agenzia\n• Tramite un intermediario abilitato\n• Di persona all\'ufficio territoriale'
  },
  {
    k: ['contratto non registrato conseguenze', 'sanzioni mancata registrazione', 'affitto in nero conseguenze'],
    r: '⚠️ **Contratto di locazione non registrato**\n\nLe conseguenze sono gravi:\n• Il contratto è **nullo**\n• Sanzioni fiscali dal **120% al 240%** dell\'imposta dovuta\n• L\'inquilino può chiedere la **registrazione forzata** al giudice\n• Il giudice può ridurre il canone ai parametri concordati\n\nL\'affitto in nero non conviene a nessuno. Noi gestiamo sempre contratti regolari.'
  },
  {
    k: ['costo registrazione locazione', 'quanto costa registrare affitto', 'imposta registro affitto'],
    r: '💶 **Costo registrazione contratto di locazione**\n\n**Con cedolare secca:** nessun costo di registro né bolli.\n\n**Senza cedolare secca:**\n• Imposta di registro: **2%** del canone annuo (minimo €67)\n• Bolli: **€16** ogni 4 facciate/100 righe\n• Si divide al 50% tra proprietario e inquilino\n\nCon la cedolare secca risparmi anche su questo!'
  },
  {
    k: ['cedolare secca spiegazione', 'cedolare secca come funziona', 'regime cedolare secca dettaglio'],
    r: '📊 **Cedolare secca — Come funziona**\n\nÈ un regime fiscale **opzionale** per il proprietario che sostituisce:\n• IRPEF e addizionali\n• Imposta di registro\n• Imposta di bollo\n\nCon un\'**aliquota fissa**:\n• **21%** per contratti liberi (4+4)\n• **10%** per contratti concordati (3+2)\n\nAttenzione: scegliendo la cedolare, **non puoi aumentare il canone** con l\'adeguamento ISTAT.'
  },
  {
    k: ['registrazione preliminare obbligatoria', 'registrare compromesso obbligo', 'costo registrazione compromesso dettaglio'],
    r: '📋 **Registrazione del contratto preliminare**\n\nSì, è **obbligatorio** registrarlo entro 20 giorni dalla firma:\n• Imposta fissa: **€200**\n• Imposta proporzionale: **0,50%** sulla caparra confirmatoria\n• **3%** sugli acconti prezzo\n• Bolli: €16 ogni 4 facciate\n\nLe imposte versate si **recuperano al rogito** come credito d\'imposta.'
  },
  {
    k: ['differenza registrare trascrivere preliminare', 'registrazione vs trascrizione', 'tutela preliminare acquirente'],
    r: '📝 **Registrare vs trascrivere il preliminare**\n\n**Registrazione** (obbligatoria):\n• Valore fiscale\n• Costo contenuto (€200 + imposte)\n\n**Trascrizione** (facoltativa):\n• Tutela **reale** dell\'acquirente\n• Protegge da vendite a terzi\n• Protegge da ipoteche successive\n• Costo più alto (serve il notaio)\n\nLa trascrizione è come un\'assicurazione sulla tua futura casa.'
  },
  {
    k: ['conviene trascrivere preliminare', 'trascrizione quando farla', 'tutela acquirente prima rogito'],
    r: '🛡️ **Conviene trascrivere il preliminare?**\n\nÈ consigliabile quando:\n• L\'importo è **elevato**\n• Passa **molto tempo** prima del rogito (6+ mesi)\n• Il venditore ha situazioni patrimoniali **complesse**\n• Vuoi la **massima tutela** possibile\n\nTi protegge se il venditore vende ad altri o se emergono debiti dopo la firma. Il costo in più può salvarti da grossi problemi.'
  },

  // ═══════════════════════════════════════════════
  // FAQ 224-233: MUTUI E FINANZIAMENTI
  // ═══════════════════════════════════════════════
  {
    k: ['mutuo 100 percento come', 'mutuo senza anticipo possibile', 'finanziamento totale casa'],
    r: '🏦 **Mutuo al 100% — Come funziona**\n\nÈ raro ma possibile. Alcune banche lo concedono con la **garanzia del Fondo Prima Casa Consap** (copertura statale fino all\'80%).\n\nRequisiti tipici:\n• ISEE entro i limiti previsti\n• Età e reddito compatibili\n• Immobile **non di lusso**\n\nSenza Consap, pochissime banche offrono il 100%. Il consulente può indicarti le opzioni.'
  },
  {
    k: ['fondo consap', 'fondo garanzia prima casa', 'garanzia statale mutuo'],
    r: '🏛️ **Fondo di Garanzia Prima Casa (Consap)**\n\nFondo statale che garantisce il **50-80%** del mutuo. Permette di ottenere finanziamenti fino al **100%**.\n\n**Priorità:**\n• Under 36\n• Giovani coppie\n• Famiglie numerose (3+ figli)\n• Inquilini di case popolari\n\nImporto massimo mutuo: **€250.000**. La domanda va presentata tramite la banca.'
  },
  {
    k: ['requisiti mutuo 100 percento', 'condizioni mutuo totale', 'mutuo senza acconto requisiti'],
    r: '📋 **Requisiti per il mutuo al 100%**\n\nVariano da banca a banca. Generalmente:\n• Reddito **stabile e dimostrabile**\n• Nessuna segnalazione in **CRIF**\n• Immobile **non di lusso** (no cat. A1, A8, A9)\n• Importo entro **€250.000**\n• Garanzia **Consap** quasi sempre necessaria\n\nLa rata non deve superare il 30-35% del reddito netto.'
  },
  {
    k: ['agevolazioni under 36 età limite', 'fino a che età bonus casa', 'under 36 scadenza'],
    r: '👶 **Agevolazioni under 36 — Età limite**\n\nLe agevolazioni erano riservate a chi non aveva ancora compiuto **36 anni** alla data del rogito. Attenzione:\n• Queste agevolazioni vengono **prorogate o modificate** annualmente dalla Legge di Bilancio\n• Verifica sempre la **normativa vigente**\n\nIl consulente ti aggiorna sulle opportunità attuali per la tua fascia d\'età.'
  },
  {
    k: ['agevolazioni under 36 dettaglio', 'esenzione imposte giovani', 'credito imposta iva under 36'],
    r: '💰 **Agevolazioni under 36 — Dettaglio**\n\nIncludevano (verifica le condizioni attuali):\n• **Esenzione** imposta di registro, ipotecaria e catastale\n• **Credito d\'imposta IVA** per acquisto da costruttore\n• Accesso al **Fondo Consap** con garanzia all\'80%\n• Esenzione imposta sostitutiva sul mutuo\n\nUn risparmio che poteva superare i **€5.000-€10.000**.'
  },
  {
    k: ['differenza mutuo 80 100', 'mutuo 80 vs 100', 'conviene mutuo 100 o 80'],
    r: '📊 **Mutuo 80% vs 100% — Confronto**\n\n**Mutuo all\'80%:**\n• Anticipi il **20%** di tasca tua\n• Rate più basse\n• Tassi di interesse migliori\n• Più banche disponibili\n\n**Mutuo al 100%:**\n• Non anticipi nulla\n• Rate più alte\n• Interessi maggiori\n• Serve garanzia Consap\n\nSe puoi, l\'80% è sempre più vantaggioso nel lungo periodo.'
  },
  {
    k: ['interessi mutuo cosa sono', 'come funzionano interessi', 'ammortamento mutuo spiegazione'],
    r: '💶 **Interessi del mutuo — Come funzionano**\n\nSono il costo che la banca ti addebita per prestarti i soldi. Con l\'**ammortamento alla francese** (il più comune):\n• Nei **primi anni** paghi soprattutto interessi\n• Col tempo paghi progressivamente **più capitale**\n• La rata resta costante (a tasso fisso)\n\nEsempio: su €150.000 a 25 anni al 3%, paghi circa €60.000 di interessi totali.'
  },
  {
    k: ['tasse sul mutuo', 'imposta sostitutiva mutuo', 'costi accessori mutuo'],
    r: '🧾 **Tasse e costi sul mutuo**\n\n• **Imposta sostitutiva:** 0,25% prima casa / 2% seconda casa (sul capitale finanziato)\n• **Perizia:** €200-€400\n• **Istruttoria:** €300-€800\n• **Assicurazione incendio:** obbligatoria (€200-€500/anno)\n• **Assicurazione vita:** consigliata ma non obbligatoria\n\nChiedi sempre il **TAEG** per confrontare il costo totale tra banche diverse.'
  },
  {
    k: ['detrazione interessi mutuo', 'interessi mutuo 730', 'scaricare interessi mutuo'],
    r: '📊 **Detrazione interessi del mutuo**\n\nPer la prima casa puoi detrarre il **19%** degli interessi passivi:\n• Massimo detraibile: **€4.000** annui\n• Risparmio massimo: **€760/anno** in dichiarazione dei redditi\n• Vale anche per oneri accessori (notaio mutuo, perizia)\n\nLa detrazione spetta a chi è intestatario sia del mutuo che dell\'immobile.'
  },
  {
    k: ['spread mutuo significato', 'spread banca cosa significa', 'come leggere tasso mutuo'],
    r: '📈 **Spread del mutuo**\n\nÈ il **margine di guadagno** della banca, sommato al tasso di riferimento:\n• **Tasso fisso** = IRS + spread\n• **Tasso variabile** = Euribor + spread\n\nPiù lo spread è basso, più il mutuo è conveniente. Confronta sempre lo spread tra diverse banche. Oggi si aggira tra **0,5% e 1,5%**.'
  },

  // ═══════════════════════════════════════════════
  // FAQ 234-238: PERIZIE IMMOBILIARI
  // ═══════════════════════════════════════════════
  {
    k: ['perizia immobiliare significato', 'valutazione tecnica immobile', 'stima professionale casa'],
    r: '📋 **Perizia immobiliare**\n\nÈ una **valutazione tecnica** dell\'immobile fatta da un professionista abilitato (geometra, architetto, ingegnere). Stima il valore di mercato basandosi su:\n• Zona e posizione\n• Stato conservativo\n• Metratura e caratteristiche\n• Comparabili venduti in zona\n\nÈ un documento oggettivo, diverso dalla semplice stima di mercato.'
  },
  {
    k: ['perizia asseverata significato', 'perizia giurata immobile', 'perizia valore legale'],
    r: '⚖️ **Perizia asseverata**\n\nÈ una perizia in cui il tecnico **giura sotto responsabilità penale** che i dati e le valutazioni sono veritieri. Ha **valore legale** e può essere usata:\n• In **tribunale** (cause, CTU)\n• Per pratiche **bancarie**\n• Per questioni **fiscali** (successioni, rivalutazioni)\n\nCosta di più di una perizia semplice ma ha un peso giuridico molto maggiore.'
  },
  {
    k: ['quando serve perizia asseverata', 'perizia asseverata obbligatoria', 'casi perizia giurata'],
    r: '📋 **Quando serve una perizia asseverata?**\n\nÈ necessaria per:\n• Richieste di **mutuo** (la banca la richiede sempre)\n• **Successioni** e divisioni ereditarie\n• **Cause legali** e CTU\n• Pratiche fiscali (rivalutazione terreni)\n• Conferimenti in **società**\n\nPer una semplice compravendita tra privati, basta generalmente una stima di mercato.'
  },
  {
    k: ['costo perizia immobiliare dettaglio', 'tariffe perizia casa', 'preventivo perizia'],
    r: '💶 **Costi perizia immobiliare**\n\n• **Perizia semplice:** €200-€500\n• **Perizia asseverata:** €300-€800\n• **Perizia bancaria per mutuo:** €200-€400 (spesso inclusa nelle spese di istruttoria)\n\nIl costo dipende dalla complessità dell\'immobile e dalla finalità. Chiedi sempre un preventivo prima.'
  },
  {
    k: ['chi fa perizia mutuo', 'perito incaricato banca', 'perizia mutuo come funziona'],
    r: '🏦 **Chi fa la perizia per il mutuo?**\n\nUn **perito iscritto all\'albo**, incaricato dalla banca (non puoi sceglierlo tu). Il perito verifica:\n• Il **valore** dell\'immobile\n• La **conformità catastale** e urbanistica\n• L\'assenza di abusi edilizi\n\nIl suo parere è **vincolante**: se valuta l\'immobile meno del prezzo, la banca riduce il mutuo. Noi verifichiamo tutto prima per evitare sorprese.'
  },

  // ═══════════════════════════════════════════════
  // FAQ 239-250: VENDITA, INCARICO E AGENZIA
  // ═══════════════════════════════════════════════
  {
    k: ['tempi vendita immobile dettaglio', 'quanto ci vuole per vendere', 'tempistiche vendita realistiche'],
    r: '⏱️ **Tempi realistici di vendita**\n\nCon il giusto prezzo:\n• **Prezzo corretto:** 2-4 mesi\n• **Prezzo nella media:** 4-6 mesi\n• **Prezzo sopra mercato:** 6-12 mesi o più\n\nUn buon **posizionamento di prezzo** è la chiave. Il primo mese è il più importante: è quando l\'immobile ha la massima visibilità online.'
  },
  {
    k: ['prezzo troppo alto conseguenze', 'immobile fermo mercato', 'errore prezzo vendita'],
    r: '⚠️ **Prezzo troppo alto: cosa succede?**\n\nL\'immobile resta **fermo sul mercato** e:\n• Perde attrattività per gli acquirenti\n• Viene scartato nei risultati di ricerca\n• Dopo mesi senza visite, sarai costretto a **ribassare**\n• Il prezzo finale sarà spesso **inferiore** a quello che avresti ottenuto partendo correttamente\n\nPartire col prezzo giusto è sempre la strategia migliore.'
  },
  {
    k: ['perché immobile non si vende', 'cause vendita bloccata', 'immobile non riceve visite'],
    r: '🔍 **Perché un immobile non si vende?**\n\nLe cause principali:\n• **Prezzo troppo alto** — la causa n°1\n• **Cattiva presentazione** — foto scadenti, disordine\n• **Scarsa promozione** — pochi portali, niente social\n• **Difetti non dichiarati** — creano sfiducia\n• **Zona poco richiesta** — serve più pazienza\n\nUn\'analisi onesta è il primo passo. Noi ti diamo un feedback realistico.'
  },
  {
    k: ['bruciatura immobile', 'immobile troppo tempo in vendita', 'effetto stanchezza annuncio'],
    r: '🔥 **Effetto "bruciatura" dell\'immobile**\n\nQuando un immobile resta in vendita **troppo a lungo**, gli acquirenti pensano che ci sia qualcosa che non va. Anche abbassando il prezzo:\n• La **fiducia è compromessa**\n• L\'annuncio perde visibilità nei portali\n• I contatti calano drasticamente\n\nMeglio partire col **prezzo giusto da subito**. Il consulente ti aiuta con una valutazione realistica.'
  },
  {
    k: ['ritirare incarico vendita', 'non voglio più vendere', 'recesso incarico agenzia'],
    r: '📋 **Ritirare l\'incarico di vendita**\n\nL\'incarico ha una durata concordata. Se recedi **prima della scadenza** senza giusta causa:\n• Potresti dover pagare una **penale**\n• O un **rimborso spese** per le attività svolte\n\nLeggi sempre bene le clausole prima di firmare. Noi abbiamo clausole chiare e trasparenti.'
  },
  {
    k: ['durata incarico vendita', 'quanto dura mandato agenzia', 'scadenza incarico immobiliare'],
    r: '📅 **Durata dell\'incarico di vendita**\n\nGeneralmente da **3 a 12 mesi**, concordato tra le parti. Alla scadenza:\n• Se non vuoi rinnovare, basta **comunicarlo**\n• L\'incarico decade automaticamente\n• Nessun obbligo di rinnovo\n\nDurante la validità, rispetta le condizioni firmate. Un buon agente ti tiene informato costantemente sull\'andamento.'
  },
  {
    k: ['penale ritiro incarico', 'rimborso spese agenzia', 'costo recesso anticipato agenzia'],
    r: '💶 **Penale per ritiro dell\'incarico**\n\nDipende dal contratto. La maggior parte degli incarichi prevede:\n• Una **penale** in caso di recesso anticipato\n• O un **rimborso spese** per le attività già svolte (foto, promozione, visite)\n\nVerifica sempre le condizioni **prima di firmare**. Da noi, le clausole sono spiegate chiaramente e senza sorprese.'
  },
  {
    k: ['vendere senza contratto agenzia', 'nessun incarico scritto', 'mandato verbale immobiliare'],
    r: '📝 **Vendere senza contratto scritto con l\'agenzia**\n\nSenza incarico scritto, non hai vincoli formali. Tuttavia:\n• Se l\'agenzia ti ha **presentato un acquirente** e concludi la vendita, potrebbe richiedere la provvigione\n• Vale il principio di **causalità** (art. 1755 c.c.)\n\nPer evitare controversie, è sempre meglio avere un incarico scritto con condizioni chiare.'
  },
  {
    k: ['provvigione senza incarico', 'agenzia chiede compenso senza contratto', 'mediazione senza mandato'],
    r: '⚖️ **Provvigione senza incarico scritto**\n\nSì, l\'agenzia **può chiederla** se dimostra di aver messo in relazione le parti (art. 1755 c.c.):\n• Il diritto alla provvigione nasce dalla **mediazione effettiva**\n• Non necessariamente dal contratto scritto\n• Basta provare il **nesso causale** tra l\'attività dell\'agente e la conclusione dell\'affare\n\nPer questo è meglio chiarire tutto per iscritto fin dall\'inizio.'
  },
  {
    k: ['vantaggi agente immobiliare', 'perché affidarsi agenzia', 'agente immobiliare cosa fa per me'],
    r: '🏆 **Vantaggi di affidarsi a un agente immobiliare**\n\nUn professionista ti offre:\n• **Valutazione corretta** basata sul mercato reale\n• **Verifica documentale** completa (urbanistica, catastale, ipotecaria)\n• **Marketing professionale** — foto, video, virtual tour, portali\n• **Visite selezionate** con acquirenti già qualificati\n• **Trattativa esperta** per le migliori condizioni\n• **Tutela legale** fino al rogito\n• Risparmio di **tempo, stress e rischi**'
  },
  {
    k: ['agente verifica documenti', 'controllo documentazione agenzia', 'agenzia controlla casa prima vendita'],
    r: '📋 **L\'agente verifica la documentazione?**\n\nSì, un buon agente verifica **tutto prima** della messa in vendita:\n• **Conformità urbanistica** e catastale\n• **Visure ipotecarie** aggiornate\n• **Certificazioni impianti**\n• **APE** valido\n• **Spese condominiali** regolari\n\nQuesto evita blocchi al rogito e dà sicurezza all\'acquirente. Noi lo facciamo sempre, di prassi.'
  },
  {
    k: ['agente aiuta trattativa', 'mediazione prezzo acquisto', 'ruolo agente nella trattativa'],
    r: '🤝 **L\'agente nella trattativa**\n\nAssolutamente sì, è uno dei nostri ruoli principali:\n• Facciamo da **mediatore imparziale** tra le parti\n• Gestiamo le **emozioni** (vendere/comprare casa è emotivo!)\n• Consigliamo il **giusto prezzo** basandoci sui dati\n• Troviamo le condizioni per chiudere in modo **equilibrato**\n\nUna buona trattativa è quella in cui entrambe le parti sono soddisfatte.'
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
    let supaOk = false;
    let formspreeOk = false;

    // Supabase
    if (this.supabase) {
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
        supaOk = true;
      } catch { supaOk = false; }
    }

    // Formspree — notifica email
    if (typeof SERVIZI_CONFIG !== 'undefined' && SERVIZI_CONFIG.FORMSPREE_ID && SERVIZI_CONFIG.FORMSPREE_ID !== 'IL_TUO_FORM_ID') {
      try {
        const r = await fetch('https://formspree.io/f/' + SERVIZI_CONFIG.FORMSPREE_ID, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
          body: JSON.stringify({
            nome: dati.nome,
            email: dati.email,
            telefono: dati.telefono,
            messaggio: dati.note || dati.messaggio,
            provenienza: 'chatbot',
            _subject: 'Nuovo contatto dal chatbot: ' + dati.nome
          })
        });
        formspreeOk = r.ok;
      } catch { formspreeOk = false; }
    }

    return supaOk || formspreeOk;
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
    if (/contattami|contattare|chiamatemi|appuntamento|richiamatemi|fissare visita|prenotare visita|incontrarvi|compilare form/.test(low)) {
      this.state = 'contatto_nome';
      this.contattoPending = { provenienza: 'chatbot' };
      return '👋 Ottimo! Ti ricontatteremo al più presto.\n\n**Come ti chiami?** (Nome e Cognome)';
    }

    // Ricerca immobili
    if (/cerca|trov|immobi|annunci|vedete|avete|list/.test(low)) {
      return this.rispostaRicerca(low);
    }

    // FAQ — best-score matching: prefer longer/more specific keyword matches
    let bestFaq = null;
    let bestScore = 0;
    for (const faq of FAQ_DATA) {
      let score = 0;
      for (const k of faq.k) {
        if (low.includes(k)) {
          score += k.length;
        }
      }
      if (score > bestScore) {
        bestScore = score;
        bestFaq = faq;
      }
    }
    if (bestFaq) {
      return bestFaq.r;
    }

    // Saluto
    if (/^(ciao|salve|buongiorno|buonasera|hey|hi|hello)/.test(low)) {
      return '👋 Ciao! Sono **Sara**, l\'assistente di **Righetto Immobiliare**.\n\nPosso aiutarti con:\n• 💰 **Stima valore** del tuo immobile\n• 🔍 **Ricerca immobili** in vendita/affitto\n• 📋 Info su **vendita**, **acquisto**, **affitto**, **mutui**, **tasse**\n• 📞 **Contattare** un agente\n\nCome posso aiutarti?';
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
        const immSlug = generatePropertySlug(imm);
        msg += `  👉 [Vedi scheda](immobile.html?s=${encodeURIComponent(immSlug)})\n\n`;
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
    return `🔍 **Cerca Immobili**\n\nPuoi cercare direttamente nella pagina [Immobili](immobili.html) con filtri avanzati per:\n• Tipo operazione (vendita/affitto)\n• Tipologia (appartamento, villa...)\n• Zona/Comune\n• Superficie\n• Prezzo\n\n👉 [Vai agli immobili](immobili.html?tipo=${tipo})\n\nOppure dimmi cosa cerchi e ti aiuto!`;
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

  // Avatar Sara — donna bionda con occhiali, professionale
  const SARA_AVATAR = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 120'%3E%3Cdefs%3E%3ClinearGradient id='bg' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop offset='0%25' stop-color='%233A5578'/%3E%3Cstop offset='100%25' stop-color='%235C7A9E'/%3E%3C/linearGradient%3E%3ClinearGradient id='hair' x1='0' y1='0' x2='0' y2='1'%3E%3Cstop offset='0%25' stop-color='%23F2D06B'/%3E%3Cstop offset='100%25' stop-color='%23D4A843'/%3E%3C/linearGradient%3E%3C/defs%3E%3Ccircle cx='60' cy='60' r='60' fill='url(%23bg)'/%3E%3Cellipse cx='60' cy='48' rx='35' ry='38' fill='url(%23hair)'/%3E%3Cellipse cx='60' cy='62' rx='24' ry='28' fill='%23FDDCB5'/%3E%3Cellipse cx='60' cy='45' rx='30' ry='20' fill='url(%23hair)'/%3E%3Cpath d='M30 42 Q35 20 60 18 Q85 20 90 42 Q88 35 75 32 Q60 28 45 32 Q32 35 30 42Z' fill='url(%23hair)'/%3E%3Cpath d='M25 55 Q28 70 35 78' stroke='%23D4A843' stroke-width='8' fill='none' stroke-linecap='round'/%3E%3Cpath d='M95 55 Q92 70 85 78' stroke='%23D4A843' stroke-width='8' fill='none' stroke-linecap='round'/%3E%3Cellipse cx='48' cy='58' rx='5' ry='4' fill='white'/%3E%3Cellipse cx='72' cy='58' rx='5' ry='4' fill='white'/%3E%3Ccircle cx='49' cy='58' r='2.5' fill='%232C4A6E'/%3E%3Ccircle cx='73' cy='58' r='2.5' fill='%232C4A6E'/%3E%3Ccircle cx='50' cy='57' r='0.8' fill='white'/%3E%3Ccircle cx='74' cy='57' r='0.8' fill='white'/%3E%3Crect x='38' y='55' width='14' height='9' rx='4.5' fill='none' stroke='%23556B7A' stroke-width='1.5'/%3E%3Crect x='62' y='55' width='14' height='9' rx='4.5' fill='none' stroke='%23556B7A' stroke-width='1.5'/%3E%3Cline x1='52' y1='59' x2='62' y2='59' stroke='%23556B7A' stroke-width='1.2'/%3E%3Cline x1='38' y1='59' x2='28' y2='56' stroke='%23556B7A' stroke-width='1.2'/%3E%3Cline x1='76' y1='59' x2='86' y2='56' stroke='%23556B7A' stroke-width='1.2'/%3E%3Cellipse cx='48' cy='66' rx='2' ry='0.8' fill='%23E8A090' opacity='0.5'/%3E%3Cellipse cx='72' cy='66' rx='2' ry='0.8' fill='%23E8A090' opacity='0.5'/%3E%3Cpath d='M55 72 Q60 76 65 72' stroke='%23C0756B' stroke-width='1.8' fill='none' stroke-linecap='round'/%3E%3Cpath d='M40 95 Q42 82 60 80 Q78 82 80 95' fill='%233A5578'/%3E%3Cpath d='M52 82 L55 90 L60 84 L65 90 L68 82' fill='white' opacity='0.9'/%3E%3C/svg%3E";

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
    position: relative; overflow: hidden;
  }
  #rig-chat-btn:hover { transform: scale(1.08); box-shadow: 0 10px 32px rgba(58,85,120,0.55); }
  #rig-chat-btn svg { width: 28px; height: 28px; }
  #rig-chat-btn-avatar {
    width: 100%; height: 100%; border-radius: 50%; object-fit: cover;
  }
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
    flex-shrink: 0; border: 2px solid #CEE08F;
    overflow: hidden;
  }
  .chat-header-avatar img {
    width: 100%; height: 100%; object-fit: cover; border-radius: 50%;
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
    overflow: hidden; align-self: flex-end;
  }
  .chat-avatar img {
    width: 100%; height: 100%; object-fit: cover; border-radius: 50%;
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
        <div class="chat-header-avatar"><img src="${SARA_AVATAR}" alt="Sara"></div>
        <div class="chat-header-info">
          <h4>Sara — Righetto Immobiliare</h4>
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
    <button id="rig-chat-btn" onclick="rigChat.toggle()" aria-label="Chatta con Sara">
      <img id="rig-chat-btn-avatar" src="${SARA_AVATAR}" alt="Sara" id="rig-chat-icon">
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
      const iconAvatar = document.getElementById('rig-chat-btn-avatar');
      const iconClose = document.getElementById('rig-chat-icon-close');
      const pulse = document.getElementById('rig-chat-pulse');
      box.classList.toggle('open', this.open);
      if (iconAvatar) iconAvatar.style.display = this.open ? 'none' : 'block';
      iconClose.style.display = this.open ? 'block' : 'none';
      if (pulse) pulse.style.display = this.open ? 'none' : 'block';
      if (this.open && document.getElementById('rig-chat-msgs').children.length === 0) {
        this.addMsg('bot', '👋 Ciao! Sono **Sara**, l\'assistente di **Righetto Immobiliare**.\n\nPosso aiutarti con:\n• 💰 **Stima valore** del tuo immobile\n• 🔍 **Cerca immobili** in vendita o affitto\n• 📋 Info su servizi, tasse, mutui e procedure\n• 📞 **Contattare** un nostro agente\n\nCome posso aiutarti?');
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
        av.className = 'chat-avatar';
        const avImg = document.createElement('img');
        avImg.src = SARA_AVATAR; avImg.alt = 'Sara';
        av.appendChild(avImg);
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
      av.className = 'chat-avatar';
      const avImg2 = document.createElement('img');
      avImg2.src = SARA_AVATAR; avImg2.alt = 'Sara';
      av.appendChild(avImg2);
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
