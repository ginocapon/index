/**
 * LINDA KB — "collega virtuale" Righetto Immobiliare (modulo opzionale, v1)
 *
 * Cosa fa:
 *  1. Prima delle regole storiche di Linda cerca la domanda nella base di conoscenza
 *     APPROVATA (Supabase RPC linda_kb_search). Se trova una voce affidabile risponde
 *     con il testo approvato, le fonti e la data di aggiornamento.
 *  2. Se la domanda contiene un codice annuncio (es. CAP1628) risponde con i dati
 *     LIVE della scheda, usando solo colonne pubbliche. Mai dati dei proprietari.
 *  3. Registra (ripulita da email/telefoni) le domande per il rapporto lacune.
 *
 * Non usa nessun modello AI generativo: nessun costo, nessuna "invenzione".
 * Se la KB non risponde o non è raggiungibile, tutto torna al comportamento storico.
 * Disattivare: window.LINDA_KB = false (prima del caricamento).
 * Disattivare solo il registro domande: window.LINDA_KB_LOG = false.
 */
(function () {
  'use strict';
  if (window.LINDA_KB === false) return;

  var SOGLIA = 0.45;             // punteggio minimo per rispondere dalla KB
  var TIMEOUT_MS = 4000;
  var TEL = '049.8843484';
  var DEFAULT_MARK = 'Capito — forse non ho colto';
  var SESSION = 'k' + Date.now().toString(36) + Math.random().toString(36).slice(2, 7);

  // Colonne PUBBLICHE ammesse. Non aggiungere mai proprietario_*, note_interne, prezzo_reale.
  var COLONNE_PUBBLICHE = [
    'codice', 'titolo', 'slug', 'tipo_operazione', 'tipologia', 'comune', 'prezzo', 'superficie',
    'locali', 'bagni', 'piano', 'anno_costruzione', 'stato', 'classe_energetica', 'ipe_kwh',
    'garage', 'giardino', 'terrazzo', 'cantina', 'ascensore', 'arredato', 'spese_condominio',
    'attivo', 'venduto', 'affittato', 'updated_at'
  ].join(',');

  var morta = false;             // RPC non disponibile (SQL non ancora applicato): silenzio
  var pendingFeedback = null;    // { id } dell'ultima risposta KB

  // ---------- utilità ----------
  function esc(s) {
    return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }
  function redact(t) {
    return String(t || '')
      .replace(/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g, '[email]')
      .replace(/\+?\d[\d\s./-]{7,}\d/g, '[telefono]')
      .replace(/\b[A-Za-z]{6}\d\d[A-Za-z]\d\d[A-Za-z]\d{3}[A-Za-z]\b/g, '[cf]')
      .slice(0, 400);
  }
  function safeUrl(u) {
    u = String(u || '').trim();
    return /^https:\/\/[^\s)]+$/i.test(u) || /^\/[a-z0-9][^\s)]*$/i.test(u) ? u : null;
  }
  function dataIt(iso) {
    if (!iso) return '';
    var d = new Date(iso);
    if (isNaN(d)) return String(iso).slice(0, 10).split('-').reverse().join('/');
    return d.toLocaleDateString('it-IT');
  }
  function withTimeout(p) {
    return Promise.race([p, new Promise(function (_, rej) { setTimeout(function () { rej(new Error('timeout')); }, TIMEOUT_MS); })]);
  }
  function euro(n) {
    // separatore migliaia con il punto, anche per 4 cifre (toLocaleString it-IT non raggruppa 1100)
    return String(Math.round(Number(n))).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
  }

  // ---------- risposta da KB approvata ----------
  function formatKb(r) {
    var out = esc(r.risposta);
    if (r.condizioni) out += '\n\n*' + esc(r.condizioni) + '*';
    var fonti = Array.isArray(r.fonti) ? r.fonti : [];
    var links = [];
    fonti.forEach(function (f) {
      var u = safeUrl(f && f.url);
      var titolo = String((f && f.titolo) || 'Fonte').replace(/[\[\]()]/g, '').slice(0, 80);
      if (u) links.push('[' + esc(titolo) + '](' + u + ')');
      else if (f && f.titolo) links.push(esc(titolo));
    });
    if (links.length) out += '\n\n**Fonti:** ' + links.join(' · ');
    if (r.aggiornata_il) out += '\n\n*Informazione aggiornata al ' + dataIt(r.aggiornata_il) + '.*';
    return out;
  }

  async function cercaKb(engine, domanda) {
    if (morta || !engine.supabase) return null;
    var res;
    try {
      res = await withTimeout(engine.supabase.rpc('linda_kb_search', { p_q: domanda, p_lim: 1 }));
    } catch (e) { return null; }           // timeout/rete: si torna alle regole storiche
    if (!res || res.error) {
      // funzione assente / non autorizzata: smetti di chiamarla in questa sessione
      if (res && res.error && /function|PGRST202|42883|404/i.test(res.error.code + ' ' + res.error.message)) morta = true;
      return null;
    }
    var row = Array.isArray(res.data) ? res.data[0] : null;
    if (!row || !(row.score >= SOGLIA)) return null;
    return row;
  }

  // ---------- risposta live da scheda annuncio ----------
  var RE_CODICE = /\b([A-Za-z]{1,4}\d{3,5})\b/;
  var CAMPI = [
    { re: /prezzo|costa|quanto (costa|chiede)|canone|affitto mensile/, f: 'prezzo' },
    { re: /\bmq\b|metri|superficie|grande|quanti metri/, f: 'superficie' },
    { re: /local[ei]|stanze|camere/, f: 'locali' },
    { re: /bagn/, f: 'bagni' },
    { re: /piano|ascensore/, f: 'piano' },
    { re: /class[ei] energetic|ape|ipe|consum/, f: 'classe_energetica' },
    { re: /spese|condominio/, f: 'spese_condominio' },
    { re: /garage|box|posto auto/, f: 'garage' },
    { re: /giardin/, f: 'giardino' },
    { re: /terrazz|balcon/, f: 'terrazzo' },
    { re: /cantin/, f: 'cantina' },
    { re: /anno|costruit|epoca/, f: 'anno_costruzione' },
    { re: /stato|condizion|ristruttur/, f: 'stato' },
    { re: /arredat/, f: 'arredato' }
  ];
  function mancante(label) {
    return 'Per **' + label + '** la scheda online non riporta un\'informazione verificata: te la confermiamo volentieri in agenzia, **' + TEL + '**.';
  }
  function rispostaCampo(r, f) {
    var aff = /affitt/.test(r.tipo_operazione || '');
    var ok = function (v) { return v !== null && v !== undefined && v !== '' && v !== 0 && v !== '0'; };
    switch (f) {
      case 'prezzo': return ok(r.prezzo) ? 'Il prezzo in scheda è **€ ' + euro(r.prezzo) + (aff ? ' al mese' : '') + '**.' : mancante('il prezzo');
      case 'superficie': return ok(r.superficie) ? 'La superficie indicata è di **' + euro(r.superficie) + ' mq**.' : mancante('la superficie');
      case 'locali': return ok(r.locali) ? 'Locali indicati: **' + r.locali + '**.' : mancante('i locali');
      case 'bagni': return ok(r.bagni) ? 'Bagni indicati: **' + r.bagni + '**.' : mancante('i bagni');
      case 'piano': return ok(r.piano) ? 'Piano: **' + esc(r.piano) + '**' + (r.ascensore === true ? ', con ascensore.' : '.') : mancante('il piano');
      case 'classe_energetica': return ok(r.classe_energetica) ? 'Classe energetica: **' + esc(r.classe_energetica) + '**' + (ok(r.ipe_kwh) ? ' (' + r.ipe_kwh + ' kWh/m²anno)' : '') + '.' : mancante('la classe energetica');
      case 'spese_condominio': return ok(r.spese_condominio) ? 'Spese condominiali indicate: **€ ' + euro(r.spese_condominio) + '**.' : mancante('le spese condominiali');
      case 'anno_costruzione': return ok(r.anno_costruzione) ? 'Anno di costruzione indicato: **' + r.anno_costruzione + '**.' : mancante('l\'anno di costruzione');
      case 'stato': return ok(r.stato) ? 'Stato dell\'immobile in scheda: **' + esc(r.stato) + '**.' : mancante('lo stato');
      default:   // garage, giardino, terrazzo, cantina, arredato: nel DB "false" = non indicato
        var nomi = { garage: 'garage/box', giardino: 'giardino', terrazzo: 'terrazzo/balcone', cantina: 'cantina', arredato: 'arredamento' };
        return r[f] === true ? 'Sì, la scheda indica **' + nomi[f] + '**.' : 'La scheda online non segnala ' + nomi[f] + '. Per conferma: **' + TEL + '**.';
    }
  }
  async function rispondiImmobile(engine, domanda) {
    var m = domanda.match(RE_CODICE);
    if (!m || !engine.supabase) return null;
    var codice = m[1].toUpperCase();
    var res;
    try {
      res = await withTimeout(engine.supabase.from('immobili').select(COLONNE_PUBBLICHE).ilike('codice', codice).limit(1));
    } catch (e) { return null; }
    if (!res || res.error) return null;
    var r = res.data && res.data[0];
    if (!r && !/immobil|annunci|codice|rif\b|rif\.|scheda|appartament|casa/i.test(domanda)) return null; // es. "IMU2025": non è un codice annuncio
    if (!r) return 'Non trovo un annuncio con codice **' + esc(codice) + '** nel catalogo. Controlla il codice oppure [guarda gli immobili disponibili](immobili.html), o chiama **' + TEL + '**.';
    var link = r.slug ? '[Apri la scheda](immobile.html?s=' + encodeURIComponent(r.slug) + ')' : '';
    if (r.attivo === false || r.venduto === true || r.affittato === true) {
      return 'L\'immobile **' + esc(r.codice) + '** non risulta più disponibile' + (r.venduto ? ' (venduto)' : r.affittato ? ' (affittato)' : '') +
        '.\n\nPosso aiutarti a cercarne uno simile: scrivi ad esempio *"cerca ' + esc(r.tipologia || 'appartamento') + ' ' + esc(r.comune || 'Padova') + '"*.';
    }
    var low = domanda.toLowerCase();
    var campi = [];
    CAMPI.forEach(function (c) { if (c.re.test(low) && campi.indexOf(c.f) < 0) campi.push(c.f); });
    var testo;
    if (campi.length) {
      testo = campi.map(function (f) { return rispostaCampo(r, f); }).join('\n');
    } else {
      testo = '**' + esc(r.titolo || r.codice) + '** (' + esc(r.codice) + ')' +
        (r.comune ? ' — ' + esc(r.comune) : '') +
        (r.prezzo ? '\nPrezzo: **€ ' + euro(r.prezzo) + (/affitt/.test(r.tipo_operazione || '') ? ' al mese' : '') + '**' : '') +
        (r.superficie ? '\nSuperficie: ' + euro(r.superficie) + ' mq' : '') +
        (r.locali ? ' · Locali: ' + r.locali : '') + (r.bagni ? ' · Bagni: ' + r.bagni : '');
    }
    testo += '\n\n' + link + '\n*Dati dalla scheda online, aggiornata al ' + dataIt(r.updated_at) + '. Le informazioni hanno valore orientativo: per conferme chiama **' + TEL + '**.*';
    return testo;
  }

  // ---------- registro domande / feedback ----------
  async function registra(engine, domanda, trovata, kbId, score) {
    if (window.LINDA_KB_LOG === false || morta || !engine.supabase) return null;
    try {
      var res = await withTimeout(engine.supabase.rpc('linda_log_question', {
        p_sessione: SESSION, p_pagina: location.pathname, p_domanda: redact(domanda),
        p_trovata: !!trovata, p_kb: kbId || null, p_score: score == null ? null : Number(score)
      }));
      return res && !res.error ? res.data : null;
    } catch (e) { return null; }
  }

  function aggiungiFeedback(id) {
    var bolle = document.querySelectorAll('#rig-chat-msgs .chat-msg.bot .chat-bubble');
    var ultima = bolle[bolle.length - 1];
    if (!ultima || ultima.querySelector('.linda-fb')) return;
    var box = document.createElement('div');
    box.className = 'linda-fb';
    box.setAttribute('role', 'group');
    box.setAttribute('aria-label', 'Questa risposta ti è stata utile?');
    box.innerHTML = '<span>Ti è stata utile?</span>' +
      '<button type="button" data-v="1" aria-label="Sì, utile">👍</button>' +
      '<button type="button" data-v="0" aria-label="No, non utile">👎</button>';
    box.setAttribute('data-qid', id == null ? '' : String(id));
    ultima.appendChild(box);
  }

  function stile() {
    if (document.getElementById('linda-kb-css')) return;
    var s = document.createElement('style');
    s.id = 'linda-kb-css';
    s.textContent = '.linda-fb{margin-top:8px;display:flex;gap:8px;align-items:center;font-size:12px;color:#5b5b5b}' +
      '.linda-fb button{min-width:44px;min-height:44px;border:1px solid rgba(0,0,0,.15);background:#fff;border-radius:999px;cursor:pointer;font-size:16px}' +
      '.linda-fb button:focus-visible{outline:2px solid #1a3d6d;outline-offset:2px}';
    document.head.appendChild(s);
  }

  // ---------- aggancio al motore esistente ----------
  function attach(engine, rigChat) {
    if (!engine || engine.__lindaKb) return;
    engine.__lindaKb = true;
    stile();
    var orig = engine.process.bind(engine);

    engine.process = async function (userMsg) {
      var idle = !engine.state || engine.state === 'idle';
      var domanda = String(userMsg || '').trim();
      if (!idle || domanda.length < 3) return orig(userMsg);

      // 1) codice annuncio → dati live della scheda
      try {
        var imm = await rispondiImmobile(engine, domanda);
        if (imm) { registra(engine, domanda, true, null, 1); return imm; }
      } catch (e) { /* si prosegue */ }

      // 2) KB approvata
      var row = await cercaKb(engine, domanda);
      if (row) {
        var qid = await registra(engine, domanda, true, row.id, row.score);
        pendingFeedback = { id: qid };
        return formatKb(row);
      }

      // 3) regole storiche; registra l'esito per il rapporto lacune
      var resp = await orig(userMsg);
      var trovata = String(resp).indexOf(DEFAULT_MARK) < 0;
      registra(engine, domanda, trovata, null, null);
      return resp;
    };

    if (rigChat && typeof rigChat.send === 'function') {
      var origSend = rigChat.send.bind(rigChat);
      rigChat.send = async function (text) {
        await origSend(text);
        if (pendingFeedback) { aggiungiFeedback(pendingFeedback.id); pendingFeedback = null; }
      };
    }

    var msgs = document.getElementById('rig-chat-msgs');
    if (msgs) {
      msgs.addEventListener('click', function (ev) {
        var b = ev.target.closest && ev.target.closest('.linda-fb button');
        if (!b) return;
        var box = b.parentNode;
        var qid = box.getAttribute('data-qid');
        box.innerHTML = '<span>Grazie del riscontro.</span>';
        if (qid && engine.supabase) {
          engine.supabase.rpc('linda_feedback', { p_id: Number(qid), p_sessione: SESSION, p_utile: b.getAttribute('data-v') === '1' }).then(function () {}, function () {});
        }
      });
    }
  }

  function attendi(n) {
    n = n || 0;
    if (window.rigChat && window.rigChat.engine) { attach(window.rigChat.engine, window.rigChat); return; }
    if (n < 40) setTimeout(function () { attendi(n + 1); }, 250);
  }
  attendi();

  window.LindaKB = { redact: redact, formatKb: formatKb, version: 1 };
})();
