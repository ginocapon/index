// ══════════════════════════════════════════════════════════════
// SOCIAL SCHEDULER — Programmazione Automatica Pubblicazioni
// Righetto Immobiliare — js/social-scheduler.js
// ══════════════════════════════════════════════════════════════

// ── STORAGE (Supabase + localStorage fallback) ──
const SCHED_STORAGE_KEY = 'rig_social_schedules';
const SCHED_LOG_KEY = 'rig_social_schedule_log';

async function getSchedules() {
  try {
    const { data, error } = await sb.from('social_schedules').select('*').order('created', { ascending: false });
    if (error) throw error;
    if (data) { localStorage.setItem(SCHED_STORAGE_KEY, JSON.stringify(data)); return data; }
  } catch(e) {
    console.warn('Supabase social_schedules non disponibile, uso localStorage:', e.message);
  }
  try { return JSON.parse(localStorage.getItem(SCHED_STORAGE_KEY) || '[]'); } catch(e) { return []; }
}

async function saveSchedule(schedule) {
  // Save to Supabase
  try {
    const { error } = await sb.from('social_schedules').upsert(schedule, { onConflict: 'id' });
    if (error) throw error;
  } catch(e) {
    console.warn('Salvataggio Supabase fallito, salvo solo in locale:', e.message);
  }
  // Always save to localStorage as backup
  const all = JSON.parse(localStorage.getItem(SCHED_STORAGE_KEY) || '[]');
  const idx = all.findIndex(x => x.id === schedule.id);
  if (idx >= 0) all[idx] = schedule; else all.push(schedule);
  localStorage.setItem(SCHED_STORAGE_KEY, JSON.stringify(all));
}

async function saveAllSchedules(list) {
  localStorage.setItem(SCHED_STORAGE_KEY, JSON.stringify(list));
  try {
    for (const s of list) {
      await sb.from('social_schedules').upsert(s, { onConflict: 'id' });
    }
  } catch(e) { console.warn('Sync Supabase fallito:', e.message); }
}

async function deleteScheduleFromDb(id) {
  try { await sb.from('social_schedules').delete().eq('id', id); } catch(e) {}
  const all = JSON.parse(localStorage.getItem(SCHED_STORAGE_KEY) || '[]');
  localStorage.setItem(SCHED_STORAGE_KEY, JSON.stringify(all.filter(x => x.id !== id)));
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

function resolveSpintax(text) {
  return text.replace(/\{([^{}]+)\}/g, function(match, group) {
    const options = group.split('|');
    return options[Math.floor(Math.random() * options.length)];
  });
}

// ── FRASI ACCATTIVANTI PER IMMOBILI ──
function generateCatchyPhrase_Immobile(i) {
  const tipo = (i.tipo_operazione || '').toLowerCase();
  const comune = i.comune || 'Padova';
  const mq = i.superficie ? Number(i.superficie) : 0;

  const frasi_vendita = [
    '{La casa dei tuoi sogni|Il tuo nuovo nido|La tua prossima casa|Un\'opportunita\' unica} ti aspetta a {' + comune + '|pochi passi dal centro di ' + comune + '}!',
    '{Non lasciarti sfuggire|Scopri subito|Vieni a vedere|Cogli al volo} questa {splendida|magnifica|bellissima|fantastica} {opportunita\'|soluzione|proprieta\'} a ' + comune + '!',
    '{Cerchi la casa perfetta|Stai cercando casa|Vuoi cambiare vita|Sogni una nuova casa}? {Eccola qui|L\'abbiamo trovata per te|Guarda questa|Non cercare oltre}!',
    '{Spazi luminosi|Ambienti eleganti|Design raffinato|Comfort e stile} in una {posizione|zona|location} {strategica|privilegiata|invidiabile|comoda} di ' + comune + '.',
    '{Un investimento sicuro|La scelta giusta|Un affare imperdibile|Qualita\' e convenienza}: {scopri|guarda|visita|non perderti} questa {proprieta\'|soluzione|casa}!',
    'A ' + comune + ' {c\'e\' una casa che ti aspetta|abbiamo trovato la soluzione perfetta|una nuova opportunita\' ti attende}!',
    '{Eleganza e comfort|Stile e praticita\'|Lusso accessibile}: {ecco|scopri} la tua {nuova casa|prossima dimora} a ' + comune + '.',
  ];

  const frasi_affitto = [
    '{Il tuo nuovo appartamento|La tua prossima casa|La soluzione ideale} in {affitto|locazione} a ' + comune + '!',
    '{Affitta subito|Disponibile da subito|Pronto per te}: {splendido|bellissimo|comodo|accogliente} {immobile|appartamento|alloggio} a ' + comune + '!',
    '{Cerchi casa in affitto|Hai bisogno di un alloggio|Nuovo in citta\'}? {Abbiamo|Ecco|Guarda} la {soluzione perfetta|risposta giusta|proposta ideale} per te!',
    '{Vivere a ' + comune + '|Trasferirsi a ' + comune + '} {non e\' mai stato cosi\' facile|e\' un\'opportunita\' unica|al prezzo giusto}!',
  ];

  const base = tipo === 'affitto' ? frasi_affitto : frasi_vendita;
  let frase = base[Math.floor(Math.random() * base.length)];

  const bonus = [];
  if (i.giardino) bonus.push('{con giardino privato|dotato di giardino|e il suo bel giardino}');
  if (i.garage) bonus.push('{con garage|box auto incluso|garage privato}');
  if (i.terrazzo) bonus.push('{con terrazzo panoramico|e splendido terrazzo|terrazzo vivibile}');
  if (mq > 150) bonus.push('{ampi spazi|generose metrature|superfici abbondanti}');
  if (bonus.length > 0) frase += ' ' + bonus[Math.floor(Math.random() * bonus.length)];

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
    '{Nuovo articolo|Appena pubblicato|Da leggere}: ' + titolo.substring(0, 40) + '!',
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

// ── CAPTION PER PIATTAFORMA CON SPINTAX ──
function buildSpintaxCaption(item, type, platform) {
  const isImmobile = type === 'immobile';
  const catchyPhrase = isImmobile ? generateCatchyPhrase_Immobile(item) : generateCatchyPhrase_Blog(item);
  return isImmobile ? _buildImmobileCaption(item, platform, catchyPhrase) : _buildBlogCaption(item, platform, catchyPhrase);
}

function _buildImmobileCaption(i, platform, catchyPhrase) {
  const tipo = i.tipo_operazione === 'vendita' ? '{IN VENDITA|VENDESI|DISPONIBILE}' : i.tipo_operazione === 'affitto' ? '{IN AFFITTO|AFFITTASI|DISPONIBILE IN LOCAZIONE}' : '';
  const prezzo = i.prezzo ? '\u20AC ' + Number(i.prezzo).toLocaleString('it-IT') : '';
  const comune = i.comune || 'Padova';

  let c = catchyPhrase + '\n\n';
  if (tipo) c += resolveSpintax(tipo) + ' | ';
  c += (i.titolo || 'Immobile') + '\n';
  c += comune + (i.indirizzo ? ' — ' + i.indirizzo : '') + '\n';
  if (prezzo) c += resolveSpintax('{Prezzo|Richiesta|Importo}: ') + prezzo + '\n';

  const specs = [];
  if (i.superficie) specs.push(i.superficie + ' mq');
  if (i.camere) specs.push(i.camere + resolveSpintax(' {camere|locali|vani}'));
  if (i.bagni_totali || i.bagni) specs.push((i.bagni_totali || i.bagni) + ' bagni');
  if (specs.length) c += specs.join(' | ') + '\n';

  const feat = [];
  if (i.classe_energetica) feat.push('Classe ' + i.classe_energetica);
  if (i.garage) feat.push(resolveSpintax('{Garage|Box auto|Posto auto}'));
  if (i.giardino) feat.push(resolveSpintax('{Giardino|Spazio verde|Area verde}'));
  if (i.terrazzo) feat.push(resolveSpintax('{Terrazzo|Terrazza|Balcone ampio}'));
  if (i.ascensore) feat.push('Ascensore');
  if (i.aria_condizionata) feat.push(resolveSpintax('{Climatizzato|Aria condizionata|A/C}'));
  if (feat.length) c += '\n' + feat.join(' | ') + '\n';

  c += '\nRif. ' + (i.codice || '') + '\n';
  if (platform === 'facebook') {
    c += resolveSpintax('{Contattaci per una visita|Prenota una visita|Chiamaci per info|Scrivici per maggiori dettagli}') + '!\n';
    c += 'Righetto Immobiliare | Tel: 049 884 3484\nwww.righettoimmobiliare.it\n';
  } else if (platform === 'instagram') {
    c += resolveSpintax('{Contattaci in DM|Scrivici per info|Link in bio per dettagli|Commenta per saperne di piu\'}') + '!\n';
    c += 'Righetto Immobiliare | Tel: 049 884 3484\n';
  } else if (platform === 'gbp') {
    c += 'Righetto Immobiliare | 049 884 3484\n';
  }

  c += '\n' + _buildHashtags(i, 'immobile', platform);
  return resolveSpintax(c);
}

function _buildBlogCaption(article, platform, catchyPhrase) {
  const titolo = article.titolo || 'Nuovo articolo';
  let c = catchyPhrase + '\n\n';
  c += resolveSpintax('{Nuovo articolo|Appena pubblicato|Sul nostro blog|Da leggere}') + ': ' + titolo + '\n\n';

  const excerpt = getExcerpt(article.contenuto, 30);
  if (excerpt) c += excerpt + '\n\n';

  if (platform === 'facebook') {
    c += resolveSpintax('{Leggi l\'articolo completo sul nostro sito|Scopri di piu\' su righettoimmobiliare.it|Vai al blog per leggere tutto}') + '!\n';
    c += 'www.righettoimmobiliare.it/blog-articolo.html?s=' + generateSlug(titolo) + '\n\n';
    c += 'Righetto Immobiliare | Il blog del mercato immobiliare padovano\n';
  } else if (platform === 'instagram') {
    c += resolveSpintax('{Link in bio|Leggi il blog|Scopri di piu\' nel nostro profilo}') + '!\n\nRighetto Immobiliare\n';
  } else if (platform === 'gbp') {
    c += 'Righetto Immobiliare | Blog\n';
  }

  c += '\n' + _buildHashtags(article, 'blog', platform);
  return resolveSpintax(c);
}

// ── SPINTAX HASHTAG/KEYWORD GENERATOR ──
function _buildHashtags(item, type, platform) {
  const tags = ['#righettoimmobiliare', '#immobiliarepadova'];

  if (type === 'immobile') {
    const comune = (item.comune || 'padova').toLowerCase().replace(/\s+/g, '');
    const tipoOp = (item.tipo_operazione || 'vendita').toLowerCase();
    tags.push('#' + comune, '#immobili' + comune);

    if (tipoOp === 'vendita') {
      tags.push(resolveSpintax('{#casainvendita|#vendocasa|#compracasa|#vendesiimmobile}'));
      tags.push(resolveSpintax('{#investimentoimmobiliare|#comprareimmobili|#acquistocasa}'));
    } else {
      tags.push(resolveSpintax('{#affitto|#casainaffitto|#affittocasa|#locazione}'));
      tags.push(resolveSpintax('{#cercoappartamento|#affittopadova|#locazionepadova}'));
    }
    if (item.giardino) tags.push(resolveSpintax('{#congiardino|#casacongiardino|#giardino}'));
    if (item.garage) tags.push(resolveSpintax('{#garage|#boxauto|#postoauto}'));
    if (item.terrazzo) tags.push(resolveSpintax('{#terrazzo|#terrazzoabitabile|#vistaterrazzo}'));
    if (item.piscina) tags.push('#conpiscina');

    const tipologia = (item.tipologia || item.categoria || '').toLowerCase();
    if (tipologia.includes('villa')) tags.push(resolveSpintax('{#villa|#villapadova|#villaveneto}'));
    if (tipologia.includes('appartamento') || tipologia.includes('appart')) tags.push(resolveSpintax('{#appartamento|#bilocale|#trilocale}'));
    if (tipologia.includes('attico')) tags.push('#attico');
    if (tipologia.includes('rustico')) tags.push(resolveSpintax('{#rustico|#casarurale|#casaledicharme}'));

    tags.push(resolveSpintax('{#realestate|#realestatelife|#homesweethome}'));
    tags.push(resolveSpintax('{#dreamhome|#househunting|#propertyforsale}'));
    tags.push(resolveSpintax('{#immobiliare|#agenziaimmobiliare|#mercatoimmobiliare}'));
    tags.push(resolveSpintax('{#casanuova|#nuovacasa|#vitanuova|#cambiarevita}'));
    tags.push(resolveSpintax('{#padova|#padovacentro|#veneto|#cittadipadova}'));
  } else {
    tags.push('#blogimmobiliare');
    tags.push(resolveSpintax('{#consigliimmobiliari|#guidaimmobiliare|#tipsimmobiliari}'));
    tags.push(resolveSpintax('{#mercatoimmobiliare|#newsimmobiliare|#attualitaimmobiliare}'));
    tags.push(resolveSpintax('{#padova|#padovaoggi|#veneto}'));
    const cat = (item.categoria || '').toLowerCase();
    if (cat.includes('mercato')) tags.push(resolveSpintax('{#trendimmobiliare|#analisimercato|#reportimmobiliare}'));
    if (cat.includes('fisco') || cat.includes('normativa')) tags.push(resolveSpintax('{#fiscalitaimmobiliare|#tassecasa|#normativa}'));
    if (cat.includes('guida')) tags.push(resolveSpintax('{#guidapratica|#howto|#consiglidaesperto}'));
    tags.push(resolveSpintax('{#realestateitaly|#italianrealestate|#investitaly}'));
  }

  let limit = platform === 'gbp' ? 5 : platform === 'facebook' ? 10 : platform === 'instagram' ? 20 : 15;
  return tags.sort(() => Math.random() - 0.5).slice(0, limit).join(' ');
}

// ══════════════════════════════════════════════════════════════
// UI — LOAD SCHEDULE CONTENT OPTIONS
// ══════════════════════════════════════════════════════════════

function loadScheduleContentOptions() {
  const type = document.getElementById('schedType').value;
  const sel = document.getElementById('schedContent');
  sel.innerHTML = '<option value="">-- Seleziona --</option>';
  if (type === 'immobile') {
    allImmobili.filter(i => i.attivo && !i.venduto && !i.affittato).forEach(i => {
      const o = document.createElement('option');
      o.value = i.id;
      o.textContent = (i.codice || '') + ' - ' + (i.titolo || 'Senza titolo') + ' - ' + (i.prezzo ? '\u20AC' + Number(i.prezzo).toLocaleString('it-IT') : 'N/D');
      sel.appendChild(o);
    });
  } else {
    blogArticles.filter(a => a.stato === 'pubblicato').forEach(a => {
      const o = document.createElement('option');
      o.value = a.id;
      o.textContent = (a.emoji || '') + ' ' + (a.titolo || 'Senza titolo') + ' - ' + (a.categoria || '');
      sel.appendChild(o);
    });
  }
}

// ══════════════════════════════════════════════════════════════
// ANTEPRIMA SPINTAX
// ══════════════════════════════════════════════════════════════

function previewScheduledSpintax() {
  const type = document.getElementById('schedType').value;
  const contentId = document.getElementById('schedContent').value;
  if (!contentId) { toast('Seleziona un contenuto prima', 'error'); return; }

  let item;
  if (type === 'immobile') item = allImmobili.find(x => String(x.id) === String(contentId));
  else item = blogArticles.find(x => String(x.id) === String(contentId));
  if (!item) { toast('Contenuto non trovato', 'error'); return; }

  const area = document.getElementById('spintaxPreviewArea');
  area.style.display = 'block';

  const platNames = { facebook: 'FACEBOOK', instagram: 'INSTAGRAM', gbp: 'GOOGLE BUSINESS' };
  let html = '';
  ['facebook', 'instagram', 'gbp'].forEach(p => {
    html += '\u2501\u2501\u2501 ' + platNames[p] + ' \u2501\u2501\u2501\n';
    html += buildSpintaxCaption(item, type, p) + '\n\n';
  });
  html += '\u2501\u2501\u2501 VARIANTE ALTERNATIVA (Facebook) \u2501\u2501\u2501\n';
  html += buildSpintaxCaption(item, type, 'facebook');
  area.textContent = html;
}

// ══════════════════════════════════════════════════════════════
// SALVA PROGRAMMAZIONE
// ══════════════════════════════════════════════════════════════

async function saveScheduledPost() {
  const type = document.getElementById('schedType').value;
  const contentId = document.getElementById('schedContent').value;
  if (!contentId) { toast('Seleziona un contenuto', 'error'); return; }
  const frequency = parseInt(document.getElementById('schedFrequency').value);
  const time = document.getElementById('schedTime').value;
  const expiry = document.getElementById('schedExpiry').value;
  if (!expiry) { toast('Imposta una data di scadenza', 'error'); return; }

  const days = [];
  document.querySelectorAll('.schedDay:checked').forEach(cb => days.push(parseInt(cb.value)));
  if (days.length === 0) { toast('Seleziona almeno un giorno', 'error'); return; }

  const platforms = [];
  if (document.getElementById('schedFb').checked) platforms.push('facebook');
  if (document.getElementById('schedIg').checked) platforms.push('instagram');
  if (document.getElementById('schedGbp').checked) platforms.push('gbp');
  if (document.getElementById('schedTiktok').checked) platforms.push('tiktok');
  if (platforms.length === 0) { toast('Seleziona almeno un social', 'error'); return; }

  let label = '';
  if (type === 'immobile') {
    const i = allImmobili.find(x => String(x.id) === String(contentId));
    label = i ? (i.codice || '') + ' - ' + (i.titolo || '') : contentId;
  } else {
    const a = blogArticles.find(x => String(x.id) === String(contentId));
    label = a ? (a.emoji || '') + ' ' + (a.titolo || '') : contentId;
  }

  const schedule = {
    id: 'sched_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6),
    type, content_id: String(contentId), label, frequency, time,
    days, platforms, expiry, status: 'active',
    created: new Date().toISOString(), last_published: null,
    publish_count: 0, next_publish: _calcNextPublish(days, time)
  };

  await saveSchedule(schedule);
  toast('Programmazione creata! Prossima: ' + _fmtSchedDate(schedule.next_publish), 'success');
  await renderScheduledPosts();
  renderWeeklyCalendar();
  document.getElementById('spintaxPreviewArea').style.display = 'none';
}

function _calcNextPublish(days, time) {
  const now = new Date();
  const [h, m] = time.split(':').map(Number);
  for (let d = 0; d < 8; d++) {
    const c = new Date(now); c.setDate(c.getDate() + d); c.setHours(h, m, 0, 0);
    if (c > now && days.includes(c.getDay())) return c.toISOString();
  }
  const tmr = new Date(now); tmr.setDate(tmr.getDate() + 1); tmr.setHours(h, m, 0, 0);
  return tmr.toISOString();
}

function _fmtSchedDate(iso) {
  if (!iso) return '--';
  const d = new Date(iso);
  return d.toLocaleDateString('it-IT', { weekday: 'short', day: 'numeric', month: 'short' }) + ' ' + d.toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' });
}

// ══════════════════════════════════════════════════════════════
// RENDER PROGRAMMAZIONI ATTIVE
// ══════════════════════════════════════════════════════════════

async function renderScheduledPosts() {
  const wrap = document.getElementById('scheduledPostsList');
  if (!wrap) return;
  const schedules = await getSchedules();

  if (schedules.length === 0) {
    wrap.innerHTML = '<div style="opacity:0.6;text-align:center;padding:16px">Nessuna programmazione attiva. Crea la prima!</div>';
    return;
  }

  const dayNames = ['Dom', 'Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab'];
  const platColors = { facebook: '#1877F2', instagram: '#dc2743', gbp: '#4285F4', tiktok: '#fff' };
  const platLabels = { facebook: 'FB', instagram: 'IG', gbp: 'GBP', tiktok: 'TT' };
  const statusInfo = { active: ['#4caf50', 'Attiva'], paused: ['#ff9800', 'In Pausa'], expired: ['#999', 'Scaduta'] };

  wrap.innerHTML = schedules.map(s => {
    const [col, lab] = statusInfo[s.status] || ['#999', s.status];
    const daysStr = (s.days || []).map(d => dayNames[d]).join(', ');
    const plats = (s.platforms || []).map(p => '<span style="color:' + (platColors[p] || '#fff') + ';font-weight:600">' + (platLabels[p] || p) + '</span>').join(' ');
    const icon = s.type === 'immobile' ? '\uD83C\uDFE0' : '\uD83D\uDCDD';

    return '<div style="background:rgba(255,255,255,0.08);border-left:3px solid ' + col + ';border-radius:8px;padding:12px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px">' +
      '<div style="flex:1;min-width:200px">' +
        '<div style="font-weight:600;font-size:0.85rem">' + icon + ' ' + escHtml(s.label || '') + '</div>' +
        '<div style="font-size:0.72rem;opacity:0.8;margin-top:4px">' + plats + ' | ' + s.frequency + 'x/sett | ' + daysStr + ' | ore ' + (s.time || '') + '</div>' +
        '<div style="font-size:0.7rem;opacity:0.6;margin-top:2px">Scade: ' + _fmtSchedDate(s.expiry + 'T23:59:00') + ' | Pubblicati: ' + (s.publish_count || 0) + (s.next_publish ? ' | Prossimo: ' + _fmtSchedDate(s.next_publish) : '') + '</div>' +
      '</div>' +
      '<div style="display:flex;gap:6px;flex-wrap:wrap">' +
        '<span style="background:' + col + ';color:white;font-size:0.68rem;padding:2px 8px;border-radius:10px">' + lab + '</span>' +
        (s.status === 'active' ? '<button onclick="pauseSchedule(\'' + s.id + '\')" style="background:rgba(255,152,0,0.3);color:white;border:none;border-radius:6px;padding:4px 10px;cursor:pointer;font-size:0.7rem">Pausa</button>' : '') +
        (s.status === 'paused' ? '<button onclick="resumeSchedule(\'' + s.id + '\')" style="background:rgba(76,175,80,0.3);color:white;border:none;border-radius:6px;padding:4px 10px;cursor:pointer;font-size:0.7rem">Riprendi</button>' : '') +
        '<button onclick="deleteSchedule(\'' + s.id + '\')" style="background:rgba(244,67,54,0.3);color:white;border:none;border-radius:6px;padding:4px 10px;cursor:pointer;font-size:0.7rem">Elimina</button>' +
        '<button onclick="publishScheduleNow(\'' + s.id + '\')" style="background:rgba(206,224,143,0.3);color:white;border:none;border-radius:6px;padding:4px 10px;cursor:pointer;font-size:0.7rem">Pubblica Ora</button>' +
      '</div></div>';
  }).join('');
}

// ── GESTIONE STATO ──

async function pauseSchedule(id) {
  const all = await getSchedules();
  const s = all.find(x => x.id === id);
  if (s) { s.status = 'paused'; await saveSchedule(s); await renderScheduledPosts(); renderWeeklyCalendar(); toast('In pausa', 'success'); }
}

async function resumeSchedule(id) {
  const all = await getSchedules();
  const s = all.find(x => x.id === id);
  if (s) { s.status = 'active'; s.next_publish = _calcNextPublish(s.days, s.time); await saveSchedule(s); await renderScheduledPosts(); renderWeeklyCalendar(); toast('Ripresa!', 'success'); }
}

async function deleteSchedule(id) {
  if (!confirm('Eliminare questa programmazione?')) return;
  await deleteScheduleFromDb(id);
  await renderScheduledPosts();
  renderWeeklyCalendar();
  toast('Eliminata', 'success');
}

// ══════════════════════════════════════════════════════════════
// CALENDARIO SETTIMANALE (stile Publer)
// ══════════════════════════════════════════════════════════════

async function renderWeeklyCalendar() {
  const wrap = document.getElementById('weeklyCalendarGrid');
  if (!wrap) return;

  const schedules = await getSchedules();
  const log = getScheduleLog();
  const today = new Date();
  const startOfWeek = new Date(today);
  startOfWeek.setDate(today.getDate() - today.getDay() + 1); // Lunedi
  startOfWeek.setHours(0, 0, 0, 0);

  const dayNames = ['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom'];
  const timeSlots = ['09:00', '12:00', '14:00', '17:00', '18:30', '20:00', '21:00'];
  const platIcons = { facebook: '\uD83D\uDD35', instagram: '\uD83D\uDFE3', gbp: '\uD83D\uDD34', tiktok: '\u26AB' };

  // Header
  let html = '<div style="display:grid;grid-template-columns:60px repeat(7,1fr);gap:1px;background:rgba(255,255,255,0.1);border-radius:10px;overflow:hidden;font-size:0.72rem">';

  // Day headers
  html += '<div style="background:rgba(255,255,255,0.15);padding:8px;text-align:center;font-weight:700">Ora</div>';
  for (let d = 0; d < 7; d++) {
    const date = new Date(startOfWeek);
    date.setDate(startOfWeek.getDate() + d);
    const isToday = date.toDateString() === today.toDateString();
    html += '<div style="background:' + (isToday ? 'rgba(206,224,143,0.3)' : 'rgba(255,255,255,0.15)') + ';padding:8px;text-align:center;font-weight:700">' +
      dayNames[d] + '<br><span style="font-size:0.65rem;opacity:0.7">' + date.getDate() + '/' + (date.getMonth() + 1) + '</span></div>';
  }

  // Time slot rows
  timeSlots.forEach(slot => {
    html += '<div style="background:rgba(255,255,255,0.05);padding:6px;text-align:center;font-weight:600;display:flex;align-items:center;justify-content:center">' + slot + '</div>';

    for (let d = 0; d < 7; d++) {
      const date = new Date(startOfWeek);
      date.setDate(startOfWeek.getDate() + d);
      const dayOfWeek = date.getDay();
      const isToday = date.toDateString() === today.toDateString();
      const isPast = date < today && !isToday;

      // Find schedules for this day+time
      const matching = schedules.filter(s =>
        s.status === 'active' &&
        (s.days || []).includes(dayOfWeek) &&
        s.time === slot &&
        new Date(s.expiry + 'T23:59:59') >= date
      );

      // Check if already published (from log)
      const dateStr = date.toISOString().split('T')[0];
      const published = log.filter(l =>
        l.action === 'published' &&
        l.timestamp && l.timestamp.startsWith(dateStr)
      );

      let cellContent = '';
      if (matching.length > 0) {
        matching.forEach(s => {
          const icon = s.type === 'immobile' ? '\uD83C\uDFE0' : '\uD83D\uDCDD';
          const plats = (s.platforms || []).map(p => platIcons[p] || '').join('');
          // Check if this specific schedule was published on this date
          const wasPublished = published.some(l => l.schedId === s.id);
          const statusDot = wasPublished ? '\u2705' : (isPast ? '\u274C' : '\u23F3');
          cellContent += '<div style="background:rgba(206,224,143,0.2);border-radius:4px;padding:3px 4px;margin:1px 0;line-height:1.2;cursor:default" title="' + escHtml(s.label) + '">' +
            statusDot + ' ' + icon + '<br><span style="font-size:0.6rem">' + escHtml((s.label || '').substring(0, 15)) + '</span><br>' +
            '<span style="font-size:0.58rem">' + plats + '</span></div>';
        });
      }

      html += '<div style="background:' + (isToday ? 'rgba(206,224,143,0.08)' : 'rgba(255,255,255,0.03)') + ';padding:3px;min-height:48px;vertical-align:top">' +
        cellContent + '</div>';
    }
  });

  html += '</div>';

  // Legenda
  html += '<div style="display:flex;gap:16px;margin-top:10px;font-size:0.68rem;opacity:0.7;justify-content:center">' +
    '<span>\u2705 Pubblicato</span><span>\u23F3 Programmato</span><span>\u274C Mancato</span>' +
    '<span>\uD83C\uDFE0 Immobile</span><span>\uD83D\uDCDD Blog</span>' +
    '<span>\uD83D\uDD35 FB</span><span>\uD83D\uDFE3 IG</span><span>\uD83D\uDD34 GBP</span><span>\u26AB TT</span>' +
  '</div>';

  wrap.innerHTML = html;
}

// ══════════════════════════════════════════════════════════════
// SCHEDULER — Controlla ogni 60 secondi
// ══════════════════════════════════════════════════════════════

let _schedulerInterval = null;

function startScheduler() {
  if (_schedulerInterval) clearInterval(_schedulerInterval);
  checkScheduledPosts();
  _schedulerInterval = setInterval(checkScheduledPosts, 60000);
  const el = document.getElementById('schedulerStatusText');
  if (el) { el.textContent = 'Attivo'; el.style.color = '#4caf50'; }
}

async function checkScheduledPosts() {
  const now = new Date();
  const schedules = await getSchedules();
  let changed = false;

  for (const s of schedules) {
    // Check expiry
    if (s.expiry && new Date(s.expiry + 'T23:59:59') < now) {
      if (s.status === 'active') {
        s.status = 'expired'; changed = true;
        addScheduleLog({ schedId: s.id, label: s.label, action: 'expired', message: 'Programmazione scaduta' });
      }
      continue;
    }
    if (s.status !== 'active' || !s.next_publish) continue;

    const nextTime = new Date(s.next_publish);
    if (now >= nextTime && (now - nextTime) < 120000) {
      await _executeScheduledPublish(s);
      s.publish_count = (s.publish_count || 0) + 1;
      s.last_published = now.toISOString();
      s.next_publish = _calcNextPublish(s.days, s.time);
      changed = true;
    }
  }

  if (changed) {
    await saveAllSchedules(schedules);
    await renderScheduledPosts();
    renderWeeklyCalendar();
    _renderScheduleLog();
  }
}

async function _executeScheduledPublish(schedule) {
  let item;
  if (schedule.type === 'immobile') item = allImmobili.find(x => String(x.id) === String(schedule.content_id));
  else item = blogArticles.find(x => String(x.id) === String(schedule.content_id));

  if (!item) {
    addScheduleLog({ schedId: schedule.id, label: schedule.label, action: 'error', message: 'Contenuto non trovato' });
    return;
  }

  for (const platform of schedule.platforms) {
    try {
      const caption = buildSpintaxCaption(item, schedule.type, platform);
      const foto = schedule.type === 'immobile'
        ? (item.foto_principale || (item.foto_urls && item.foto_urls[0]) || '')
        : (item.immagine_copertina || '');

      if (platform === 'facebook') await _pubFb(item, schedule.type, caption, foto);
      else if (platform === 'instagram') await _pubIg(item, schedule.type, caption, foto);
      else if (platform === 'gbp') await _pubGbp(caption, foto);
      else if (platform === 'tiktok') {
        addScheduleLog({ schedId: schedule.id, label: schedule.label, platform: 'tiktok', action: 'skip', message: 'TikTok richiede upload manuale' });
        continue;
      }
      addScheduleLog({ schedId: schedule.id, label: schedule.label, platform, action: 'published', message: 'Pubblicato con successo' });
      toast('Auto-pubblicato su ' + platform.toUpperCase() + ': ' + (schedule.label || '').substring(0, 30), 'success');
    } catch(e) {
      addScheduleLog({ schedId: schedule.id, label: schedule.label, platform, action: 'error', message: e.message || 'Errore' });
    }
  }
}

async function publishScheduleNow(id) {
  const all = await getSchedules();
  const s = all.find(x => x.id === id);
  if (!s) return;
  toast('Pubblicazione manuale...', 'success');
  await _executeScheduledPublish(s);
  s.publish_count = (s.publish_count || 0) + 1;
  s.last_published = new Date().toISOString();
  await saveSchedule(s);
  await renderScheduledPosts();
  renderWeeklyCalendar();
  _renderScheduleLog();
  toast('Pubblicazione completata!', 'success');
}

// ── PUBLISHING HELPERS ──

async function _pubFb(item, type, caption, foto) {
  const pageId = localStorage.getItem('social_fb_page_id');
  const token = localStorage.getItem('social_fb_token');
  if (!pageId || !token) throw new Error('Facebook non configurato');
  const endpoint = foto
    ? 'https://graph.facebook.com/v21.0/' + pageId + '/photos'
    : 'https://graph.facebook.com/v21.0/' + pageId + '/feed';
  const body = foto
    ? { url: foto, caption: caption, access_token: token }
    : { message: caption, access_token: token };
  const res = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  const data = await res.json();
  if (data.error) throw new Error('FB: ' + data.error.message);
}

async function _pubIg(item, type, caption, foto) {
  const accountId = localStorage.getItem('social_ig_account_id');
  const token = localStorage.getItem('social_ig_token');
  if (!accountId || !token) throw new Error('Instagram non configurato');
  if (!foto) throw new Error('Instagram richiede una foto');

  const allPhotos = type === 'immobile' ? ((item.foto_urls || item.foto || []).filter(Boolean)) : [foto];

  if (allPhotos.length > 1 && allPhotos.length <= 10) {
    const itemIds = [];
    for (const photoUrl of allPhotos.slice(0, 10)) {
      const r = await fetch('https://graph.facebook.com/v21.0/' + accountId + '/media', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ image_url: photoUrl, is_carousel_item: true, access_token: token }) });
      const d = await r.json(); if (d.id) itemIds.push(d.id);
    }
    const cRes = await fetch('https://graph.facebook.com/v21.0/' + accountId + '/media', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ media_type: 'CAROUSEL', children: itemIds, caption, access_token: token }) });
    const container = await cRes.json();
    if (container.error) throw new Error('IG: ' + container.error.message);
    await waitForIgMedia(container.id, token);
    const pRes = await fetch('https://graph.facebook.com/v21.0/' + accountId + '/media_publish', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ creation_id: container.id, access_token: token }) });
    const pData = await pRes.json();
    if (pData.error) throw new Error('IG: ' + pData.error.message);
  } else {
    const cRes = await fetch('https://graph.facebook.com/v21.0/' + accountId + '/media', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ image_url: foto, caption, access_token: token }) });
    const container = await cRes.json();
    if (container.error) throw new Error('IG: ' + container.error.message);
    await waitForIgMedia(container.id, token);
    const pRes = await fetch('https://graph.facebook.com/v21.0/' + accountId + '/media_publish', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ creation_id: container.id, access_token: token }) });
    const pData = await pRes.json();
    if (pData.error) throw new Error('IG: ' + pData.error.message);
  }
}

async function _pubGbp(caption, foto) {
  const gbpToken = localStorage.getItem('social_gbp_access_token');
  const gbpLocation = localStorage.getItem('social_gbp_location');
  if (!gbpToken || !gbpLocation) throw new Error('Google Business non configurato');
  const body = { languageCode: 'it', summary: caption.substring(0, 1500), topicType: 'STANDARD' };
  if (foto) body.media = [{ mediaFormat: 'PHOTO', sourceUrl: foto }];
  const res = await fetch('https://mybusiness.googleapis.com/v4/' + gbpLocation + '/localPosts', { method: 'POST', headers: { 'Authorization': 'Bearer ' + gbpToken, 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  const data = await res.json();
  if (data.error) throw new Error('GBP: ' + (data.error.message || JSON.stringify(data.error)));
}

// ── CATCH-UP: recupera pubblicazioni mancate ──
async function checkMissedPublications() {
  const schedules = await getSchedules();
  const now = new Date();
  const missed = [];

  for (const s of schedules) {
    if (s.status !== 'active') continue;
    if (!s.next_publish) continue;
    const next = new Date(s.next_publish);
    // Se next_publish e' nel passato di piu' di 2 minuti, e' stato mancato
    if (now - next > 120000) {
      missed.push(s);
      // Aggiorna next_publish al prossimo slot valido
      s.next_publish = _calcNextPublish(s.days, s.time);
    }
  }

  if (missed.length > 0) {
    await saveAllSchedules(schedules);
    const labels = missed.map(s => (s.type === 'immobile' ? '\uD83C\uDFE0' : '\uD83D\uDCDD') + ' ' + (s.label || '')).join('\n');
    const doPublish = confirm(
      'Pubblicazioni mancate trovate!\n\n' +
      'Mentre la pagina era chiusa, queste pubblicazioni non sono partite:\n\n' +
      labels + '\n\n' +
      'Vuoi pubblicarle adesso?'
    );
    if (doPublish) {
      for (const s of missed) {
        await _executeScheduledPublish(s);
        s.publish_count = (s.publish_count || 0) + 1;
        s.last_published = now.toISOString();
        addScheduleLog({ schedId: s.id, label: s.label, action: 'published', message: 'Recupero pubblicazione mancata' });
      }
      await saveAllSchedules(schedules);
      toast(missed.length + ' pubblicazioni recuperate!', 'success');
    } else {
      for (const s of missed) {
        addScheduleLog({ schedId: s.id, label: s.label, action: 'skip', message: 'Pubblicazione mancata - non recuperata' });
      }
    }
  }
}

// ── LOG ──
function _renderScheduleLog() {
  const wrap = document.getElementById('scheduleLog');
  if (!wrap) return;
  const log = getScheduleLog();
  if (log.length === 0) { wrap.innerHTML = '<div style="opacity:0.6">Nessuna pubblicazione ancora...</div>'; return; }
  wrap.innerHTML = log.slice(0, 50).map(e => {
    const date = new Date(e.timestamp).toLocaleString('it-IT', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' });
    const col = e.action === 'published' ? '#4caf50' : e.action === 'error' ? '#f44336' : e.action === 'expired' ? '#ff9800' : '#999';
    const ico = e.action === 'published' ? '\u2705' : e.action === 'error' ? '\u274C' : e.action === 'expired' ? '\u23F0' : '\u23ED\uFE0F';
    return '<div style="border-bottom:1px solid rgba(255,255,255,0.1);padding:4px 0">' +
      ico + ' <span style="color:' + col + '">[' + date + ']</span> ' +
      (e.platform ? '<strong>' + e.platform.toUpperCase() + '</strong> ' : '') +
      escHtml(e.label || '') + ' - ' +
      '<span style="color:' + col + '">' + escHtml(e.message || '') + '</span></div>';
  }).join('');
}

// ══════════════════════════════════════════════════════════════
// INIT
// ══════════════════════════════════════════════════════════════

async function initSocialScheduler() {
  loadScheduleContentOptions();
  await renderScheduledPosts();
  await renderWeeklyCalendar();
  _renderScheduleLog();
  startScheduler();

  // Default expiry: +30 days
  const el = document.getElementById('schedExpiry');
  if (el && !el.value) {
    const def = new Date(); def.setDate(def.getDate() + 30);
    el.value = def.toISOString().split('T')[0];
  }

  // Check missed publications
  await checkMissedPublications();
}
