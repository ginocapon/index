/* ══════════════════════════════════════════════════════════════
   VALUTAZIONE PDF — Genera scheda risultato con QR WhatsApp
   ══════════════════════════════════════════════════════════════ */

/* --- Prezzi al mq per comune (stessi di homepage.js) --- */
const V_PREZZI = {
  'padova centro storico':3500,'padova centro':3500,'padova':2500,
  'padova arcella':1950,'padova guizza':1750,
  'selvazzano dentro':2100,'selvazzano':2100,
  'albignasego':1950,'noventa padovana':2200,'vigonza':1900,
  'rubano':2000,'limena':1700,'cadoneghe':1850,'saccolongo':1650,
  'cittadella':3200,'abano terme':2100,'montegrotto terme':1900,
  'galzignano terme':1450,'battaglia terme':1350,'arquà petrarca':1600,
  'teolo':1700,'due carrare':1550,'camposampiero':1750,
  'trebaseleghe':1600,'borgoricco':1500,'piombino dese':1450,
  'piove di sacco':1600,'conselve':1350,'este':1100,
  'monselice':1050,'montagnana':950,'default':1200
};
const V_TIPO_MULT = {
  'appartamento':1.0,'villa / villetta':1.15,'villa':1.20,
  'casa indipendente':1.10,'bifamiliare':1.10,
  'rustico / casale':0.85,'terreno':3.8,
  'commerciale / ufficio':0.70
};
const V_STATO_MULT = {
  'nuovo / ristrutturato':1.25,'buone condizioni':1.0,'da ristrutturare':0.75
};

function calcolaValutazione(comune, tipo, mq, stato) {
  const key = (comune || '').toLowerCase().trim();
  let basePrice = V_PREZZI['default'];
  // fuzzy match: cerca la chiave piu' lunga che matcha
  let bestLen = 0;
  for (const k in V_PREZZI) {
    if (key.includes(k) || k.includes(key)) {
      if (k.length > bestLen) { basePrice = V_PREZZI[k]; bestLen = k.length; }
    }
  }
  const tMult = V_TIPO_MULT[(tipo || '').toLowerCase()] || 1.0;
  const sMult = V_STATO_MULT[(stato || '').toLowerCase()] || 1.0;
  let scaleMult = 1;
  if (mq > 200) scaleMult = 0.91;
  else if (mq > 150) scaleMult = 0.96;
  else if (mq < 40) scaleMult = 1.10;
  else if (mq < 60) scaleMult = 1.05;

  const pricePerMq = basePrice * tMult * sMult * scaleMult;
  const totale = mq * pricePerMq;
  return {
    min: Math.round(totale * 0.88 / 1000) * 1000,
    med: Math.round(totale / 1000) * 1000,
    max: Math.round(totale * 1.12 / 1000) * 1000,
    euroMq: Math.round(pricePerMq)
  };
}

/* --- QR Code minimo (genera SVG) --- */
function generateQRSvg(text, size) {
  // Usa la libreria QRCode se caricata, altrimenti fallback a immagine API
  if (typeof QRCode !== 'undefined') {
    const div = document.createElement('div');
    new QRCode(div, { text: text, width: size, height: size, correctLevel: QRCode.CorrectLevel.M });
    return div.querySelector('canvas');
  }
  return null;
}

/* --- Carica immagine come base64 per jsPDF --- */
function loadImgBase64(url) {
  return new Promise((resolve) => {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = function () {
      const c = document.createElement('canvas');
      c.width = img.naturalWidth; c.height = img.naturalHeight;
      c.getContext('2d').drawImage(img, 0, 0);
      try { resolve(c.toDataURL('image/jpeg', 0.85)); } catch (e) { resolve(null); }
    };
    img.onerror = function () { resolve(null); };
    img.src = url;
  });
}

/* --- Genera PDF valutazione --- */
async function generaValutazionePDF(dati) {
  /* dati = { comune, tipo, mq, stato, vani, piano, garage, nome, stima } */
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF({ unit: 'mm', format: 'a4' });
  const W = 210, H = 297;
  const fmt = n => new Intl.NumberFormat('it-IT', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(n);

  /* --- Colori brand --- */
  const purple = [108, 99, 255];
  const purpleDeep = [45, 27, 105];
  const fire = [255, 107, 53];
  const dark = [17, 24, 39];
  const gray = [107, 114, 128];
  const mint = [0, 229, 160];

  /* === HEADER === */
  doc.setFillColor(...purpleDeep);
  doc.rect(0, 0, W, 52, 'F');
  // Gradient line
  doc.setFillColor(...purple);
  doc.rect(0, 52, W, 3, 'F');
  doc.setFillColor(...fire);
  doc.rect(W / 2, 52, W / 2, 3, 'F');

  doc.setTextColor(255, 255, 255);
  doc.setFontSize(22);
  doc.setFont('helvetica', 'bold');
  doc.text('RIGHETTO IMMOBILIARE', W / 2, 18, { align: 'center' });
  doc.setFontSize(10);
  doc.setFont('helvetica', 'normal');
  doc.text('Gruppo Immobiliare dal 2000 — Padova e Provincia', W / 2, 26, { align: 'center' });
  doc.setFontSize(14);
  doc.setFont('helvetica', 'bold');
  doc.setTextColor(...[255, 210, 63]); // sun
  doc.text('SCHEDA VALUTAZIONE IMMOBILIARE', W / 2, 40, { align: 'center' });
  doc.setFontSize(8);
  doc.setTextColor(200, 200, 220);
  doc.text('Valutazione indicativa generata il ' + new Date().toLocaleDateString('it-IT', { day: 'numeric', month: 'long', year: 'numeric' }), W / 2, 47, { align: 'center' });

  /* === DATI IMMOBILE === */
  let y = 65;
  doc.setFillColor(245, 245, 252);
  doc.roundedRect(15, y - 6, W - 30, 50, 4, 4, 'F');
  doc.setDrawColor(...purple);
  doc.setLineWidth(0.5);
  doc.roundedRect(15, y - 6, W - 30, 50, 4, 4, 'S');

  doc.setTextColor(...purpleDeep);
  doc.setFontSize(12);
  doc.setFont('helvetica', 'bold');
  doc.text('DATI DELL\'IMMOBILE', 22, y + 2);
  y += 10;

  doc.setFontSize(9);
  doc.setFont('helvetica', 'normal');
  doc.setTextColor(...dark);

  const righe = [
    ['Zona / Comune', dati.comune || '-'],
    ['Tipologia', dati.tipo || '-'],
    ['Superficie', (dati.mq || '-') + ' mq'],
    ['Stato', dati.stato || '-']
  ];
  if (dati.vani) righe.push(['Vani', dati.vani]);
  if (dati.piano) righe.push(['Piano', dati.piano]);
  if (dati.garage) righe.push(['Garage', dati.garage]);

  // 2 colonne
  const col1X = 22, col2X = 112;
  for (let i = 0; i < righe.length; i++) {
    const x = i % 2 === 0 ? col1X : col2X;
    const rowY = y + Math.floor(i / 2) * 8;
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(...gray);
    doc.text(righe[i][0] + ':', x, rowY);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(...dark);
    doc.text(righe[i][1], x + 32, rowY);
  }

  /* === RISULTATO STIMA === */
  y = 125;
  // Box grande con stima
  doc.setFillColor(...purpleDeep);
  doc.roundedRect(15, y, W - 30, 55, 4, 4, 'F');

  doc.setTextColor(255, 255, 255);
  doc.setFontSize(11);
  doc.setFont('helvetica', 'bold');
  doc.text('STIMA DEL VALORE DI MERCATO', W / 2, y + 12, { align: 'center' });

  // Valore centrale grande
  doc.setFontSize(28);
  doc.setTextColor(...[255, 210, 63]);
  doc.text(fmt(dati.stima.med), W / 2, y + 30, { align: 'center' });

  // Range
  doc.setFontSize(10);
  doc.setTextColor(200, 200, 220);
  doc.text('Range: ' + fmt(dati.stima.min) + ' — ' + fmt(dati.stima.max), W / 2, y + 39, { align: 'center' });

  // Euro/mq
  doc.setFontSize(9);
  doc.setTextColor(...mint);
  doc.text(fmt(dati.stima.euroMq) + ' / mq', W / 2, y + 48, { align: 'center' });

  /* === DISCLAIMER === */
  y = 188;
  doc.setFontSize(7.5);
  doc.setTextColor(...gray);
  doc.setFont('helvetica', 'italic');
  const disclaimer = 'Questa stima e\' indicativa e basata su dati medi di mercato della provincia di Padova. Il valore effettivo puo\' variare in base a caratteristiche specifiche dell\'immobile (esposizione, luminosita\', piano, rifiniture, pertinenze, stato manutentivo reale) che solo un sopralluogo professionale puo\' determinare. Per una valutazione precisa e certificata, contattaci per un sopralluogo gratuito.';
  doc.text(disclaimer, W / 2, y, { align: 'center', maxWidth: W - 40 });

  /* === SEZIONE LINDA + CTA === */
  y = 210;
  doc.setFillColor(250, 248, 255);
  doc.roundedRect(15, y, W - 30, 60, 4, 4, 'F');
  doc.setDrawColor(...purple);
  doc.setLineWidth(0.3);
  doc.roundedRect(15, y, W - 30, 60, 4, 4, 'S');

  // Foto Linda
  try {
    const lindaImg = await loadImgBase64('img/team/foto-linda-righetto-viola.webp');
    if (lindaImg) {
      // Cerchio clip simulato con immagine quadrata
      doc.addImage(lindaImg, 'JPEG', 22, y + 5, 40, 50);
    }
  } catch (e) {}

  // Testo CTA
  const ctaX = 70;
  doc.setTextColor(...purpleDeep);
  doc.setFontSize(16);
  doc.setFont('helvetica', 'bold');
  doc.text('Ricordati di contattarci!', ctaX, y + 14);

  doc.setFontSize(9);
  doc.setFont('helvetica', 'normal');
  doc.setTextColor(...dark);
  doc.text('Vuoi sapere il valore esatto della tua casa?', ctaX, y + 23);
  doc.text('Prenota un sopralluogo gratuito con i nostri esperti.', ctaX, y + 30);

  doc.setFontSize(10);
  doc.setFont('helvetica', 'bold');
  doc.setTextColor(...purple);
  doc.text('049.88.43.484', ctaX, y + 41);
  doc.setTextColor(...fire);
  doc.text('WhatsApp: 349 736 5930', ctaX, y + 49);

  // QR Code WhatsApp
  const waUrl = 'https://wa.me/393497365930?text=' + encodeURIComponent('Ciao! Ho appena fatto una valutazione online del mio immobile a ' + (dati.comune || 'Padova') + '. Vorrei saperne di piu\'!');
  try {
    const qrCanvas = generateQRSvg(waUrl, 150);
    if (qrCanvas) {
      const qrData = qrCanvas.toDataURL('image/png');
      doc.addImage(qrData, 'PNG', W - 55, y + 5, 35, 35);
      doc.setFontSize(6.5);
      doc.setTextColor(...gray);
      doc.text('Inquadra per WhatsApp', W - 37.5, y + 44, { align: 'center' });
    }
  } catch (e) {}

  /* === FOOTER === */
  doc.setFillColor(...dark);
  doc.rect(0, H - 18, W, 18, 'F');
  doc.setFontSize(7);
  doc.setTextColor(180, 180, 190);
  doc.text('Righetto Immobiliare — Via Roma 96, Limena (PD) — P.IVA 05182390285', W / 2, H - 11, { align: 'center' });
  doc.text('righettoimmobiliare.it  |  info@righettoimmobiliare.it  |  049.88.43.484', W / 2, H - 6, { align: 'center' });

  /* === SALVA === */
  const nomeFile = 'Valutazione-' + (dati.comune || 'Immobile').replace(/[^a-zA-Z0-9àèéìòù ]/g, '').replace(/ +/g, '-') + '.pdf';
  doc.save(nomeFile);
}
