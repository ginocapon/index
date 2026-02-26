// ══════════════════════════════════════════════════════════════
// SOCIAL SCHEDULER — Programmazione Automatica Pubblicazioni
// Righetto Immobiliare — js/social-scheduler.js
// ══════════════════════════════════════════════════════════════

// ── STORAGE ──
const SCHED_STORAGE_KEY = 'rig_social_schedules';
const SCHED_LOG_KEY = 'rig_social_schedule_log';

function getSchedules() {
  try { return JSON.parse(localStorage.getItem(SCHED_STORAGE_KEY) || '[]'); } catch(e) { return []; }
}
function saveSchedules(list) {
  localStorage.setItem(SCHED_STORAGE_KEY, JSON.stringify(list));
}
function getScheduleLog() {
  try { return JSON.parse(localStorage.getItem(SCHED_LOG_KEY) || '[]'); } catch(e) { return []; }
}
function addScheduleLog(entry) {
  const log = getScheduleLog();
  log.unshift({ ...entry, timestamp: new Date().toISOString() });
  if (log.length > 200) log.length = 200;
  localStorage.setItem(SCHED_LOG_KEY, JSON.stringify(log));
}

// ══════════════════════════════════════════════════════════════
// SPINTAX ENGINE
// ══════════════════════════════════════════════════════════════

// Resolve {opzione1|opzione2|opzione3} → picks one at random
function resolveSpintax(text) {
  return text.replace(/\{([^{}]+)\}/g, function(match, group) {
    const options = group.split('|');
    return options[Math.floor(Math.random() * options.length)];
  });
}

// ── FRASI ACCATTIVANTI PER IMMOBILI ──
function generateCatchyPhrase_Immobile(i) {
  const tipo = (i.tipo_operazione || '').toLowerCase();
  const prezzo = i.prezzo ? Number(i.prezzo) : 0;
  const comune = (i.comune || 'Padova').toLowerCase();
  const hasGiardino = i.giardino;
  const hasGarage = i.garage;
  const hasTerrazzo = i.terrazzo;
  const mq = i.superficie ? Number(i.superficie) : 0;

  const frasi_vendita = [
    '{La casa dei tuoi sogni|Il tuo nuovo nido|La tua prossima casa|Un\'opportunita\' unica} ti aspetta a {' + (i.comune || 'Padova') + '|pochi passi dal centro di ' + (i.comune || 'Padova') + '}!',
    '{Non lasciarti sfuggire|Scopri subito|Vieni a vedere|Cogli al volo} questa {splendida|magnifica|bellissima|fantastica} {opportunita\'|soluzione|proprieta\'} a ' + (i.comune || 'Padova') + '!',
    '{Cerchi la casa perfetta|Stai cercando casa|Vuoi cambiare vita|Sogni una nuova casa}? {Eccola qui|L\'abbiamo trovata per te|Guarda questa|Non cercare oltre}!',
    '{Spazi luminosi|Ambienti eleganti|Design raffinato|Comfort e stile} in una {posizione|zona|location} {strategica|privilegiata|invidiabile|comoda} di ' + (i.comune || 'Padova') + '.',
    '{Un investimento sicuro|La scelta giusta|Un affare imperdibile|Qualita\' e convenienza}: {scopri|guarda|visita|non perderti} questa {proprieta\'|soluzione|casa}!',
  ];

  const frasi_affitto = [
    '{Il tuo nuovo appartamento|La tua prossima casa|La soluzione ideale} in {affitto|locazione} a ' + (i.comune || 'Padova') + '!',
    '{Affitta subito|Disponibile da subito|Pronto per te}: {splendido|bellissimo|comodo|accogliente} {immobile|appartamento|alloggio} a ' + (i.comune || 'Padova') + '!',
    '{Cerchi casa in affitto|Hai bisogno di un alloggio|Nuovo in citta\'}? {Abbiamo|Ecco|Guarda} la {soluzione perfetta|risposta giusta|proposta ideale} per te!',
  ];

  const base = tipo === 'affitto' ? frasi_affitto : frasi_vendita;
  let frase = base[Math.floor(Math.random() * base.length)];

  // Aggiungi feature bonus
  const bonus = [];
  if (hasGiardino) bonus.push('{con giardino privato|dotato di giardino|e il suo bel giardino}');
  if (hasGarage) bonus.push('{con garage|box auto incluso|garage privato}');
  if (hasTerrazzo) bonus.push('{con terrazzo panoramico|e splendido terrazzo|terrazzo vivibile}');
  if (mq > 150) bonus.push('{ampi spazi|generose metrature|superfici abbondanti}');
  if (bonus.length > 0) {
    frase += ' ' + bonus[Math.floor(Math.random() * bonus.length)];
  }

  return resolveSpintax(frase);
}

// ── FRASI ACCATTIVANTI PER ARTICOLI BLOG ──
function generateCatchyPhrase_Blog(article) {
  const cat = (article.categoria || '').toLowerCase();
  const titolo = article.titolo || '';

  const frasi_mercato = [
    '{Scopri le ultime novita\'|Aggiornamenti imperdibili|Tutto quello che devi sapere} sul mercato immobiliare {di Padova|padovano|locale}!',
    '{Il mercato si muove|Novita\' dal settore|Trend in evoluzione}: {leggi|scopri|approfondisci} il nostro {ultimo articolo|approfondimento|report}!',
    '{Vuoi investire nel mattone|Stai valutando un acquisto|Pensi di vendere casa}? {Leggi prima questo|Informati con noi|Ecco cosa devi sapere}!',
  ];
  const frasi_guida = [
    '{Guida completa|Tutto quello che devi sapere|I nostri consigli}: {vendere|comprare|affittare} casa {senza stress|con successo|al meglio}!',
    '{Consigli d\'esperto|Dritte dal professionista|Suggerimenti utili} per {la tua compravendita|il tuo progetto immobiliare|chi cerca casa}.',
    '{Non commettere errori|Evita le trappole|Fai la scelta giusta}: la nostra {guida pratica|guida esperta|guida dettagliata} ti aiuta!',
  ];
  const frasi_normativa = [
    '{Aggiornamento normativo|Novita\' legislative|Cambiano le regole}: {ecco cosa sapere|tutto quello che cambia|informati subito}!',
    '{Fisco e immobili|Leggi e mattone|Norme aggiornate}: {la nostra analisi|il nostro approfondimento|guida pratica}.',
  ];
  const frasi_generiche = [
    '{Nuovo articolo|Appena pubblicato|Da leggere}: {' + titolo.substring(0, 40) + '|scopri di piu\' sul nostro blog}!',
    '{Leggi il nostro ultimo articolo|Sul blog di Righetto Immobiliare|Approfondimento esclusivo}: informazioni {utili|preziose|pratiche} per te!',
    '{Rimani aggiornato|Non perderti le novita\'|Segui il nostro blog}: {articoli|contenuti|approfondimenti} {settimanali|freschi|esclusivi}!',
  ];

  let pool;
  if (cat.includes('mercato')) pool = frasi_mercato;
  else if (cat.includes('guida') || cat.includes('consigli')) pool = frasi_guida;
  else if (cat.includes('normativa') || cat.includes('fisco')) pool = frasi_normativa;
  else pool = frasi_generiche;

  return resolveSpintax(pool[Math.floor(Math.random() * pool.length)]);
}

// ── SPINTAX DESCRIZIONE PER PIATTAFORMA ──
function buildSpintaxCaption(item, type, platform) {
  const isImmobile = type === 'immobile';
  const catchyPhrase = isImmobile ? generateCatchyPhrase_Immobile(item) : generateCatchyPhrase_Blog(item);

  if (isImmobile) {
    return buildImmobileCaption(item, platform, catchyPhrase);
  } else {
    return buildBlogCaption(item, platform, catchyPhrase);
  }
}

function buildImmobileCaption(i, platform, catchyPhrase) {
  const tipo = i.tipo_operazione === 'vendita' ? '{IN VENDITA|VENDESI|DISPONIBILE}' : i.tipo_operazione === 'affitto' ? '{IN AFFITTO|AFFITTASI|DISPONIBILE IN LOCAZIONE}' : '';
  const prezzo = i.prezzo ? '\u20AC ' + Number(i.prezzo).toLocaleString('it-IT') : '';
  const comune = i.comune || 'Padova';
  const titolo = i.titolo || 'Immobile';

  let caption = '';

  // Frase accattivante in testa
  caption += catchyPhrase + '\n\n';

  // Tipo operazione
  if (tipo) caption += resolveSpintax(tipo) + ' | ';
  caption += titolo + '\n';
  caption += comune + (i.indirizzo ? ' — ' + i.indirizzo : '') + '\n';
  if (prezzo) caption += resolveSpintax('{Prezzo|Richiesta|Importo}: ') + prezzo + '\n';

  // Specifiche
  const specs = [];
  if (i.superficie) specs.push(i.superficie + ' mq');
  if (i.camere) specs.push(i.camere + resolveSpintax(' {camere|locali|vani}'));
  if (i.bagni_totali || i.bagni) specs.push((i.bagni_totali || i.bagni) + ' bagni');
  if (specs.length) caption += specs.join(' | ') + '\n';

  // Features
  const features = [];
  if (i.classe_energetica) features.push('Classe ' + i.classe_energetica);
  if (i.garage) features.push(resolveSpintax('{Garage|Box auto|Posto auto}'));
  if (i.giardino) features.push(resolveSpintax('{Giardino|Spazio verde|Area verde}'));
  if (i.terrazzo) features.push(resolveSpintax('{Terrazzo|Terrazza|Balcone ampio}'));
  if (i.ascensore) features.push('Ascensore');
  if (i.aria_condizionata) features.push(resolveSpintax('{Climatizzato|Aria condizionata|A/C}'));
  if (features.length) caption += '\n' + features.join(' | ') + '\n';

  // Riferimento
  caption += '\nRif. ' + (i.codice || '') + '\n';

  // CTA per piattaforma
  if (platform === 'facebook') {
    caption += resolveSpintax('{Contattaci per una visita|Prenota una visita|Chiamaci per info|Scrivici per maggiori dettagli}') + '!\n';
    caption += 'Righetto Immobiliare | Tel: 049 884 3484\n';
    caption += 'www.righettoimmobiliare.it\n';
  } else if (platform === 'instagram') {
    caption += resolveSpintax('{Contattaci in DM|Scrivici per info|Link in bio per dettagli|Commenta per saperne di piu\'}') + '!\n';
    caption += 'Righetto Immobiliare | Tel: 049 884 3484\n';
  } else if (platform === 'gbp') {
    caption += 'Righetto Immobiliare | 049 884 3484\n';
  }

  // Hashtag con spintax
  caption += '\n' + buildSpintaxHashtags(i, 'immobile', platform);

  return resolveSpintax(caption);
}

function buildBlogCaption(article, platform, catchyPhrase) {
  const titolo = article.titolo || 'Nuovo articolo';
  const categoria = article.categoria || '';

  let caption = '';
  caption += catchyPhrase + '\n\n';
  caption += resolveSpintax('{Nuovo articolo|Appena pubblicato|Sul nostro blog|Da leggere}') + ': ' + titolo + '\n\n';

  // Excerpt dal contenuto
  const excerpt = getExcerpt(article.contenuto, 30);
  if (excerpt) caption += excerpt + '\n\n';

  if (platform === 'facebook') {
    caption += resolveSpintax('{Leggi l\'articolo completo sul nostro sito|Scopri di piu\' su righettoimmobiliare.it|Vai al blog per leggere tutto}') + '!\n';
    caption += 'www.righettoimmobiliare.it/blog-articolo.html?s=' + generateSlug(titolo) + '\n\n';
    caption += 'Righetto Immobiliare | Il blog del mercato immobiliare padovano\n';
  } else if (platform === 'instagram') {
    caption += resolveSpintax('{Link in bio|Leggi il blog|Scopri di piu\' nel nostro profilo}') + '!\n\n';
    caption += 'Righetto Immobiliare\n';
  } else if (platform === 'gbp') {
    caption += 'Righetto Immobiliare | Blog\n';
  }

  caption += '\n' + buildSpintaxHashtags(article, 'blog', platform);

  return resolveSpintax(caption);
}

// ── SPINTAX HASHTAG/KEYWORD GENERATOR ──
function buildSpintaxHashtags(item, type, platform) {
  const tags = [];

  // Tag fissi brand
  tags.push('#righettoimmobiliare');
  tags.push('#immobiliarepadova');

  if (type === 'immobile') {
    const comune = (item.comune || 'padova').toLowerCase().replace(/\s+/g, '');
    const tipoOp = (item.tipo_operazione || 'vendita').toLowerCase();

    tags.push('#' + comune);
    tags.push('#immobili' + comune);

    // Spintax per tipo operazione
    if (tipoOp === 'vendita') {
      tags.push(resolveSpintax('{#casainvendita|#vendocasa|#compracasa|#vendesiimmobile}'));
      tags.push(resolveSpintax('{#investimentoimmobiliare|#comprareimmobili|#acquistocasa}'));
    } else {
      tags.push(resolveSpintax('{#affitto|#casainaffitto|#affittocasa|#locazione}'));
      tags.push(resolveSpintax('{#cercoappartamento|#affittopadova|#locazionepadova}'));
    }

    // Tag per features
    if (item.giardino) tags.push(resolveSpintax('{#congiardino|#casacongiardino|#giardino}'));
    if (item.garage) tags.push(resolveSpintax('{#garage|#boxauto|#postoauto}'));
    if (item.terrazzo) tags.push(resolveSpintax('{#terrazzo|#terrazzoabitabile|#vistaterrazzo}'));
    if (item.ascensore) tags.push('#conascensore');
    if (item.piscina) tags.push('#conpiscina');

    // Tag per tipologia
    const tipologia = (item.tipologia || item.categoria || '').toLowerCase();
    if (tipologia.includes('villa')) tags.push(resolveSpintax('{#villa|#villapadova|#villaveneto}'));
    if (tipologia.includes('appartamento') || tipologia.includes('appart')) tags.push(resolveSpintax('{#appartamento|#bilocale|#trilocale}'));
    if (tipologia.includes('attico')) tags.push('#attico');
    if (tipologia.includes('rustico')) tags.push(resolveSpintax('{#rustico|#casarurale|#casaledicharme}'));

    // Tag generici immobiliari
    tags.push(resolveSpintax('{#realestate|#realestatelife|#homesweethome}'));
    tags.push(resolveSpintax('{#dreamhome|#househunting|#propertyforsale}'));
    tags.push(resolveSpintax('{#immobiliare|#agenziaimmobiliare|#mercatoimmobiliare}'));
    tags.push(resolveSpintax('{#casanuova|#nuovacasa|#vitanuova|#cambiarevita}'));
    tags.push(resolveSpintax('{#padova|#padovacentro|#veneto|#cittadipadova}'));

  } else {
    // Blog
    const cat = (item.categoria || '').toLowerCase();
    tags.push('#blogimmobiliare');
    tags.push(resolveSpintax('{#consigliimmobiliari|#guidaimmobiliare|#tipsimmobiliari}'));
    tags.push(resolveSpintax('{#mercatoimmobiliare|#newsimmobiliare|#attualitaimmobiliare}'));
    tags.push(resolveSpintax('{#padova|#padovaoggi|#veneto}'));

    if (cat.includes('mercato')) tags.push(resolveSpintax('{#trendimmobiliare|#analisimercato|#reportimmobiliare}'));
    if (cat.includes('fisco') || cat.includes('normativa')) tags.push(resolveSpintax('{#fiscalitaimmobiliare|#tassecasa|#normativa}'));
    if (cat.includes('guida')) tags.push(resolveSpintax('{#guidapratica|#howto|#consiglidaesperto}'));
    if (cat.includes('investimento')) tags.push(resolveSpintax('{#investimenti|#investire|#rendimento}'));

    tags.push(resolveSpintax('{#realestateitaly|#italianrealestate|#investitaly}'));
  }

  // Instagram max 30 hashtag, FB meno (10-12 ideale), GBP pochi
  let limit = 15;
  if (platform === 'facebook') limit = 10;
  if (platform === 'gbp') limit = 5;
  if (platform === 'instagram') limit = 20;

  // Shuffle e limita
  const shuffled = tags.sort(() => Math.random() - 0.5).slice(0, limit);
  return shuffled.join(' ');
}

// ══════════════════════════════════════════════════════════════
// UI — CARICAMENTO OPZIONI CONTENUTO
// ══════════════════════════════════════════════════════════════

function loadScheduleContentOptions() {
  const type = document.getElementById('schedType').value;
  const sel = document.getElementById('schedContent');
  sel.innerHTML = '<option value="">— Seleziona —</option>';

  if (type === 'immobile') {
    allImmobili.filter(i => i.attivo && !i.venduto && !i.affittato).forEach(i => {
      const opt = document.createElement('option');
      opt.value = i.id;
      opt.textContent = (i.codice || '') + ' — ' + (i.titolo || 'Senza titolo') + ' — ' + (i.prezzo ? '\u20AC' + Number(i.prezzo).toLocaleString('it-IT') : 'N/D');
      sel.appendChild(opt);
    });
  } else {
    blogArticles.filter(a => a.stato === 'pubblicato').forEach(a => {
      const opt = document.createElement('option');
      opt.value = a.id;
      opt.textContent = (a.emoji || '') + ' ' + (a.titolo || 'Senza titolo') + ' — ' + (a.categoria || '');
      sel.appendChild(opt);
    });
  }
}

// ══════════════════════════════════════════════════════════════
// UI — ANTEPRIMA SPINTAX
// ══════════════════════════════════════════════════════════════

function previewScheduledSpintax() {
  const type = document.getElementById('schedType').value;
  const contentId = document.getElementById('schedContent').value;
  if (!contentId) { toast('Seleziona un contenuto prima', 'error'); return; }

  let item;
  if (type === 'immobile') {
    item = allImmobili.find(x => String(x.id) === String(contentId));
  } else {
    item = blogArticles.find(x => String(x.id) === String(contentId));
  }
  if (!item) { toast('Contenuto non trovato', 'error'); return; }

  const area = document.getElementById('spintaxPreviewArea');
  area.style.display = 'block';

  // Genera 3 varianti per mostrare la diversita'
  let html = '';
  const platforms = ['facebook', 'instagram', 'gbp'];
  const platNames = { facebook: 'FACEBOOK', instagram: 'INSTAGRAM', gbp: 'GOOGLE BUSINESS' };

  platforms.forEach(p => {
    html += '━━━ ' + platNames[p] + ' ━━━\n';
    html += buildSpintaxCaption(item, type, p);
    html += '\n\n';
  });

  html += '━━━ VARIANTE ALTERNATIVA (Facebook) ━━━\n';
  html += buildSpintaxCaption(item, type, 'facebook');

  area.textContent = html;
}

// ══════════════════════════════════════════════════════════════
// SALVA PROGRAMMAZIONE
// ══════════════════════════════════════════════════════════════

function saveScheduledPost() {
  const type = document.getElementById('schedType').value;
  const contentId = document.getElementById('schedContent').value;
  if (!contentId) { toast('Seleziona un contenuto', 'error'); return; }

  const frequency = parseInt(document.getElementById('schedFrequency').value);
  const time = document.getElementById('schedTime').value;
  const expiry = document.getElementById('schedExpiry').value;

  if (!expiry) { toast('Imposta una data di scadenza', 'error'); return; }

  // Giorni selezionati
  const days = [];
  document.querySelectorAll('.schedDay:checked').forEach(cb => days.push(parseInt(cb.value)));
  if (days.length === 0) { toast('Seleziona almeno un giorno', 'error'); return; }

  // Social selezionati
  const platforms = [];
  if (document.getElementById('schedFb').checked) platforms.push('facebook');
  if (document.getElementById('schedIg').checked) platforms.push('instagram');
  if (document.getElementById('schedGbp').checked) platforms.push('gbp');
  if (document.getElementById('schedTiktok').checked) platforms.push('tiktok');
  if (platforms.length === 0) { toast('Seleziona almeno un social', 'error'); return; }

  // Recupera info contenuto per label
  let label = '';
  if (type === 'immobile') {
    const i = allImmobili.find(x => String(x.id) === String(contentId));
    label = i ? (i.codice || '') + ' — ' + (i.titolo || '') : contentId;
  } else {
    const a = blogArticles.find(x => String(x.id) === String(contentId));
    label = a ? (a.emoji || '') + ' ' + (a.titolo || '') : contentId;
  }

  const schedule = {
    id: 'sched_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6),
    type,
    contentId: String(contentId),
    label,
    frequency,
    time,
    days,
    platforms,
    expiry,
    status: 'active',
    created: new Date().toISOString(),
    lastPublished: null,
    publishCount: 0,
    nextPublish: calculateNextPublishDate(days, time)
  };

  const schedules = getSchedules();
  schedules.push(schedule);
  saveSchedules(schedules);

  toast('Programmazione creata! Prossima pubblicazione: ' + formatScheduleDate(schedule.nextPublish), 'success');
  renderScheduledPosts();

  // Reset preview
  document.getElementById('spintaxPreviewArea').style.display = 'none';
}

function calculateNextPublishDate(days, time) {
  const now = new Date();
  const [h, m] = time.split(':').map(Number);

  // Prova oggi e i prossimi 7 giorni
  for (let d = 0; d < 8; d++) {
    const candidate = new Date(now);
    candidate.setDate(candidate.getDate() + d);
    candidate.setHours(h, m, 0, 0);

    if (candidate > now && days.includes(candidate.getDay())) {
      return candidate.toISOString();
    }
  }
  // Fallback: domani all'orario
  const tomorrow = new Date(now);
  tomorrow.setDate(tomorrow.getDate() + 1);
  tomorrow.setHours(h, m, 0, 0);
  return tomorrow.toISOString();
}

function formatScheduleDate(iso) {
  if (!iso) return '—';
  const d = new Date(iso);
  return d.toLocaleDateString('it-IT', { weekday: 'short', day: 'numeric', month: 'short' }) + ' ' + d.toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' });
}

// ══════════════════════════════════════════════════════════════
// RENDER LISTA PROGRAMMAZIONI
// ══════════════════════════════════════════════════════════════

function renderScheduledPosts() {
  const wrap = document.getElementById('scheduledPostsList');
  const schedules = getSchedules();
  const active = schedules.filter(s => s.status === 'active');
  const paused = schedules.filter(s => s.status === 'paused');
  const expired = schedules.filter(s => s.status === 'expired');

  if (schedules.length === 0) {
    wrap.innerHTML = '<div style="opacity:0.6;text-align:center;padding:16px">Nessuna programmazione attiva. Crea la prima!</div>';
    return;
  }

  let html = '';

  // Attive
  active.forEach(s => {
    html += renderScheduleCard(s, '#4caf50', 'Attiva');
  });
  // In pausa
  paused.forEach(s => {
    html += renderScheduleCard(s, '#ff9800', 'In Pausa');
  });
  // Scadute
  expired.forEach(s => {
    html += renderScheduleCard(s, '#999', 'Scaduta');
  });

  wrap.innerHTML = html;
}

function renderScheduleCard(s, color, statusLabel) {
  const dayNames = ['Dom', 'Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab'];
  const daysStr = (s.days || []).map(d => dayNames[d]).join(', ');
  const platIcons = {
    facebook: '<span style="color:#1877F2">FB</span>',
    instagram: '<span style="color:#dc2743">IG</span>',
    gbp: '<span style="color:#4285F4">GBP</span>',
    tiktok: '<span style="color:#fff">TT</span>',
  };
  const plats = (s.platforms || []).map(p => platIcons[p] || p).join(' ');
  const typeIcon = s.type === 'immobile' ? '\uD83C\uDFE0' : '\uD83D\uDCDD';

  return '<div style="background:rgba(255,255,255,0.08);border-left:3px solid ' + color + ';border-radius:8px;padding:12px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px">' +
    '<div style="flex:1;min-width:200px">' +
      '<div style="font-weight:600;font-size:0.85rem">' + typeIcon + ' ' + escHtml(s.label || '') + '</div>' +
      '<div style="font-size:0.72rem;opacity:0.8;margin-top:4px">' +
        plats + ' | ' + s.frequency + 'x/sett | ' + daysStr + ' | ore ' + (s.time || '') +
      '</div>' +
      '<div style="font-size:0.7rem;opacity:0.6;margin-top:2px">' +
        'Scade: ' + formatScheduleDate(s.expiry + 'T23:59:00') + ' | Pubblicati: ' + (s.publishCount || 0) +
        (s.nextPublish ? ' | Prossimo: ' + formatScheduleDate(s.nextPublish) : '') +
      '</div>' +
    '</div>' +
    '<div style="display:flex;gap:6px">' +
      '<span style="background:' + color + ';color:white;font-size:0.68rem;padding:2px 8px;border-radius:10px">' + statusLabel + '</span>' +
      (s.status === 'active' ? '<button onclick="pauseSchedule(\'' + s.id + '\')" style="background:rgba(255,152,0,0.3);color:white;border:none;border-radius:6px;padding:4px 10px;cursor:pointer;font-size:0.7rem">Pausa</button>' : '') +
      (s.status === 'paused' ? '<button onclick="resumeSchedule(\'' + s.id + '\')" style="background:rgba(76,175,80,0.3);color:white;border:none;border-radius:6px;padding:4px 10px;cursor:pointer;font-size:0.7rem">Riprendi</button>' : '') +
      '<button onclick="deleteSchedule(\'' + s.id + '\')" style="background:rgba(244,67,54,0.3);color:white;border:none;border-radius:6px;padding:4px 10px;cursor:pointer;font-size:0.7rem">Elimina</button>' +
      '<button onclick="publishScheduleNow(\'' + s.id + '\')" style="background:rgba(206,224,143,0.3);color:white;border:none;border-radius:6px;padding:4px 10px;cursor:pointer;font-size:0.7rem">Pubblica Ora</button>' +
    '</div>' +
  '</div>';
}

// escHtml, getExcerpt, generateSlug, toast, waitForIgMedia — defined in admin.html (global scope)

// ── GESTIONE STATO PROGRAMMAZIONI ──

function pauseSchedule(id) {
  const schedules = getSchedules();
  const s = schedules.find(x => x.id === id);
  if (s) { s.status = 'paused'; saveSchedules(schedules); renderScheduledPosts(); toast('Programmazione in pausa', 'success'); }
}

function resumeSchedule(id) {
  const schedules = getSchedules();
  const s = schedules.find(x => x.id === id);
  if (s) {
    s.status = 'active';
    s.nextPublish = calculateNextPublishDate(s.days, s.time);
    saveSchedules(schedules);
    renderScheduledPosts();
    toast('Programmazione ripresa!', 'success');
  }
}

function deleteSchedule(id) {
  if (!confirm('Eliminare questa programmazione?')) return;
  const schedules = getSchedules().filter(x => x.id !== id);
  saveSchedules(schedules);
  renderScheduledPosts();
  toast('Programmazione eliminata', 'success');
}

// ══════════════════════════════════════════════════════════════
// SCHEDULER — Controlla ogni minuto se ci sono post da pubblicare
// ══════════════════════════════════════════════════════════════

let schedulerInterval = null;

function startScheduler() {
  if (schedulerInterval) clearInterval(schedulerInterval);
  // Controlla subito
  checkScheduledPosts();
  // Poi ogni 60 secondi
  schedulerInterval = setInterval(checkScheduledPosts, 60000);

  const badge = document.getElementById('schedulerStatusText');
  if (badge) { badge.textContent = 'Attivo'; badge.style.color = '#4caf50'; }
}

function checkScheduledPosts() {
  const now = new Date();
  const schedules = getSchedules();
  let changed = false;

  schedules.forEach(s => {
    // Check scadenza
    if (s.expiry && new Date(s.expiry + 'T23:59:59') < now) {
      if (s.status === 'active') {
        s.status = 'expired';
        changed = true;
        addScheduleLog({ schedId: s.id, label: s.label, action: 'expired', message: 'Programmazione scaduta' });
      }
      return;
    }

    if (s.status !== 'active') return;
    if (!s.nextPublish) return;

    const nextTime = new Date(s.nextPublish);
    // Finestra di 2 minuti per il check
    if (now >= nextTime && (now - nextTime) < 120000) {
      // E' ora di pubblicare!
      executeScheduledPublish(s);
      s.publishCount = (s.publishCount || 0) + 1;
      s.lastPublished = now.toISOString();
      s.nextPublish = calculateNextPublishDate(s.days, s.time);
      changed = true;
    }
  });

  if (changed) {
    saveSchedules(schedules);
    renderScheduledPosts();
    renderScheduleLog();
  }
}

async function executeScheduledPublish(schedule) {
  const type = schedule.type;
  const contentId = schedule.contentId;

  let item;
  if (type === 'immobile') {
    item = allImmobili.find(x => String(x.id) === String(contentId));
  } else {
    item = blogArticles.find(x => String(x.id) === String(contentId));
  }

  if (!item) {
    addScheduleLog({ schedId: schedule.id, label: schedule.label, action: 'error', message: 'Contenuto non trovato (ID: ' + contentId + ')' });
    return;
  }

  for (const platform of schedule.platforms) {
    try {
      const caption = buildSpintaxCaption(item, type, platform);
      const foto = type === 'immobile'
        ? (item.foto_principale || (item.foto_urls && item.foto_urls[0]) || '')
        : (item.immagine_copertina || '');

      if (platform === 'facebook') {
        await publishScheduledToFacebook(item, type, caption, foto);
      } else if (platform === 'instagram') {
        await publishScheduledToInstagram(item, type, caption, foto);
      } else if (platform === 'gbp') {
        await publishScheduledToGBP(item, type, caption, foto);
      } else if (platform === 'tiktok') {
        // TikTok non ha API diretta — genera solo l'immagine silenziosamente
        addScheduleLog({ schedId: schedule.id, label: schedule.label, platform: 'tiktok', action: 'skip', message: 'TikTok richiede upload manuale' });
        continue;
      }

      addScheduleLog({ schedId: schedule.id, label: schedule.label, platform, action: 'published', message: 'Pubblicato con successo' });
    } catch(e) {
      addScheduleLog({ schedId: schedule.id, label: schedule.label, platform, action: 'error', message: e.message || 'Errore sconosciuto' });
    }
  }
}

// Pubblica su un programma specifico ora (manualmente)
async function publishScheduleNow(id) {
  const schedules = getSchedules();
  const s = schedules.find(x => x.id === id);
  if (!s) return;

  toast('Pubblicazione manuale in corso...', 'success');
  await executeScheduledPublish(s);
  s.publishCount = (s.publishCount || 0) + 1;
  s.lastPublished = new Date().toISOString();
  saveSchedules(schedules);
  renderScheduledPosts();
  renderScheduleLog();
  toast('Pubblicazione manuale completata!', 'success');
}

// ── PUBLISHING FUNCTIONS PER SCHEDULER ──

async function publishScheduledToFacebook(item, type, caption, foto) {
  const pageId = localStorage.getItem('social_fb_page_id');
  const token = localStorage.getItem('social_fb_token');
  if (!pageId || !token) throw new Error('Facebook non configurato');

  let res;
  if (foto) {
    res = await fetch('https://graph.facebook.com/v21.0/' + pageId + '/photos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: foto, caption: caption, access_token: token })
    });
  } else {
    res = await fetch('https://graph.facebook.com/v21.0/' + pageId + '/feed', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: caption, access_token: token })
    });
  }
  const data = await res.json();
  if (data.error) throw new Error('FB: ' + data.error.message);
  return data;
}

async function publishScheduledToInstagram(item, type, caption, foto) {
  const accountId = localStorage.getItem('social_ig_account_id');
  const token = localStorage.getItem('social_ig_token');
  if (!accountId || !token) throw new Error('Instagram non configurato');
  if (!foto) throw new Error('Instagram richiede una foto');

  // Per gli immobili con piu' foto, usa carousel
  const allPhotos = type === 'immobile' ? ((item.foto_urls || item.foto || []).filter(Boolean)) : [foto];

  if (allPhotos.length > 1 && allPhotos.length <= 10) {
    // CAROUSEL
    const itemIds = [];
    for (const photoUrl of allPhotos.slice(0, 10)) {
      const itemRes = await fetch('https://graph.facebook.com/v21.0/' + accountId + '/media', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image_url: photoUrl, is_carousel_item: true, access_token: token })
      });
      const itemData = await itemRes.json();
      if (itemData.id) itemIds.push(itemData.id);
    }
    const containerRes = await fetch('https://graph.facebook.com/v21.0/' + accountId + '/media', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ media_type: 'CAROUSEL', children: itemIds, caption: caption, access_token: token })
    });
    const container = await containerRes.json();
    if (container.error) throw new Error('IG: ' + container.error.message);

    await waitForIgMedia(container.id, token);
    const pubRes = await fetch('https://graph.facebook.com/v21.0/' + accountId + '/media_publish', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ creation_id: container.id, access_token: token })
    });
    const pubData = await pubRes.json();
    if (pubData.error) throw new Error('IG: ' + pubData.error.message);
    return pubData;
  } else {
    // SINGLE IMAGE
    const containerRes = await fetch('https://graph.facebook.com/v21.0/' + accountId + '/media', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image_url: foto, caption: caption, access_token: token })
    });
    const container = await containerRes.json();
    if (container.error) throw new Error('IG: ' + container.error.message);

    await waitForIgMedia(container.id, token);
    const pubRes = await fetch('https://graph.facebook.com/v21.0/' + accountId + '/media_publish', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ creation_id: container.id, access_token: token })
    });
    const pubData = await pubRes.json();
    if (pubData.error) throw new Error('IG: ' + pubData.error.message);
    return pubData;
  }
}

async function publishScheduledToGBP(item, type, caption, foto) {
  const gbpToken = localStorage.getItem('social_gbp_access_token');
  const gbpLocation = localStorage.getItem('social_gbp_location');
  if (!gbpToken || !gbpLocation) throw new Error('Google Business non configurato');

  const postBody = {
    languageCode: 'it',
    summary: caption.substring(0, 1500),
    topicType: 'STANDARD',
  };
  if (foto) {
    postBody.media = [{ mediaFormat: 'PHOTO', sourceUrl: foto }];
  }
  const res = await fetch('https://mybusiness.googleapis.com/v4/' + gbpLocation + '/localPosts', {
    method: 'POST',
    headers: { 'Authorization': 'Bearer ' + gbpToken, 'Content-Type': 'application/json' },
    body: JSON.stringify(postBody)
  });
  const data = await res.json();
  if (data.error) throw new Error('GBP: ' + (data.error.message || JSON.stringify(data.error)));
  return data;
}

// ── RENDER LOG ──
function renderScheduleLog() {
  const wrap = document.getElementById('scheduleLog');
  if (!wrap) return;
  const log = getScheduleLog();

  if (log.length === 0) {
    wrap.innerHTML = '<div style="opacity:0.6">Nessuna pubblicazione ancora...</div>';
    return;
  }

  wrap.innerHTML = log.slice(0, 50).map(entry => {
    const date = new Date(entry.timestamp).toLocaleString('it-IT', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' });
    const color = entry.action === 'published' ? '#4caf50' : entry.action === 'error' ? '#f44336' : entry.action === 'expired' ? '#ff9800' : '#999';
    const icon = entry.action === 'published' ? '\u2705' : entry.action === 'error' ? '\u274C' : entry.action === 'expired' ? '\u23F0' : '\u23ED\uFE0F';
    return '<div style="border-bottom:1px solid rgba(255,255,255,0.1);padding:4px 0">' +
      icon + ' <span style="color:' + color + '">[' + date + ']</span> ' +
      (entry.platform ? '<strong>' + entry.platform.toUpperCase() + '</strong> ' : '') +
      escHtml(entry.label || '') + ' — ' +
      '<span style="color:' + color + '">' + escHtml(entry.message || '') + '</span>' +
    '</div>';
  }).join('');
}

// ══════════════════════════════════════════════════════════════
// INIT — Chiamato quando si carica la sezione social
// ══════════════════════════════════════════════════════════════

function initSocialScheduler() {
  loadScheduleContentOptions();
  renderScheduledPosts();
  renderScheduleLog();
  startScheduler();

  // Imposta data scadenza default: +30 giorni
  const def = new Date();
  def.setDate(def.getDate() + 30);
  const el = document.getElementById('schedExpiry');
  if (el && !el.value) el.value = def.toISOString().split('T')[0];
}
