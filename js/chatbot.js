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
    k: ['tempo vendita', 'quanto tempo', 'tempistica vendita', 'velocità'],
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
    k: ['rogito', 'atto', 'notaio', 'notarile'],
    r: '🏛️ **Il rogito notarile**\n\nIl rogito è l\'atto definitivo di compravendita stipulato dal notaio. Il notaio è scelto generalmente dall\'acquirente. I costi notarili (onorario + imposte) variano dal 2% al 4% del prezzo di acquisto. Noi vi accompagniamo fino alla firma e al passaggio delle chiavi!'
  },
  // ── ACQUISTO ──
  {
    k: ['prima casa', 'agevolazioni', 'under 36', 'giovani'],
    r: '🏡 **Agevolazioni prima casa**\n\n**Requisiti:**\n• Non possedere altri immobili nello stesso comune\n• Residenza nel comune entro 18 mesi\n• Non aver già usufruito del bonus\n\n**Vantaggi:**\n• Imposta di registro al 2% (anziché 9%)\n• Per under 36: esenzione totale imposte e credito IVA\n• Detrazioni interessi mutuo fino a €4.000/anno'
  },
  {
    k: ['caparra', 'deposito', 'anticipo', 'acconto'],
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
    k: ['documenti', 'ape', 'certificato', 'pratiche', 'catasto'],
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
    k: ['conformità', 'abuso', 'abusivismo', 'sanatoria', 'condono'],
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
