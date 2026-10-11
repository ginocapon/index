/**
 * Archivi FAQ A/B, flusso apertura chat, inventario incongruenze (v1)
 * Caricato da js/chatbot.js — disattiva: window.RIGHETTO_CHAT_ARCHIVI = false
 */
(function () {
  'use strict';
  if (window.RIGHETTO_CHAT_ARCHIVI === false) return;

  var BASE = 'data/chatbot/';
  var store = { a: [], b: [], flusso: null, inventario: {}, anomalie: {}, ready: null };
  var RE_CODICE = /\b([A-Za-z]{1,4}\d{3,5}(?:-[A-Za-z]|[a-z])?)(?![A-Za-z0-9])/;
  var RE_LIVE = /\b(prezzo|costa|disponib|disponibile|annuncio|catalogo|avete|vedete|cerco|affitt|vendit|compr|canone)\b/i;

  function loadJson(url) {
    return fetch(url, { cache: 'no-cache' }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    });
  }

  // ── Normalizzazione dei file ORIGINALI (formato .faq/.risposta/.varianti_domanda/.fonti): i file non si modificano, si adatta il lettore ──
  var STOP = {};
  ('il lo la le gli un uno una di da del dello della dei degli delle al allo alla ai agli alle dal dalla nel nella nei con su per tra fra e ed o ma che chi cui non si come cosa quale quali quanto quanti quando dove sono e\u0300 ho ha hanno posso puoi puo devo deve fare fatto essere questo questa questi queste mio mia miei mie vorrei voglio sapere dimmi dirmi mi ti ci vi anche piu molto solo se in a i l d c avere spiegami spiega spiegare spiegarmi spieghi spiegate').split(' ').forEach(function (w) { STOP[w] = 1; });

  function norm(t) {
    return String(t || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9\s]/g, ' ');
  }
  function stem(w) { return w.length > 5 ? w.slice(0, 5) : w; }

  // Sinonimi/parafrasi frequenti nel dominio (radice di 5 caratteri -> radice canonica).
  // Applicati sia alla domanda dell'utente sia alle voci archiviate: i file originali non si toccano.
  var SINONIMI = {
    stima: 'valut', deter: 'calco', comput: 'calco',
    acqui: 'compr', ceder: 'vend', cedut: 'vend',
    locat: 'affit', canon: 'affit',
    abita: 'casa', appart: 'casa', allog: 'casa',
    richi: 'otten', inter: 'leggo', consu: 'leggo', legge: 'leggo',
    neces: 'serv', occur: 'serv', accer: 'verif', contr: 'verif',
    vale: 'valor', valgo: 'valor'
  };

  function tokens(t) {
    var out = [];
    norm(t).split(/\s+/).forEach(function (w) {
      if (w.length < 2 || STOP[w]) return;
      var st = stem(w);
      st = SINONIMI[st] || st;
      if (st === 'spieg') return;
      if (out.indexOf(st) < 0) out.push(st);
    });
    return out;
  }

  function normalizzaFaq(list) {
    return (list || []).map(function (f) {
      var cand = [f.domanda].concat(f.varianti_domanda || []).filter(Boolean);
      return {
        id: f.id,
        domanda: f.domanda,
        r: f.risposta,
        cand: cand.map(tokens),
        fonti: (f.fonti || []).filter(function (x) { return x && /^https:\/\//i.test(x.url || ''); }),
        live: !!f.rilettura_live_obbligatoria,
        snapshot: /snapshot|nel catalogo consultato/i.test(f.risposta || ''),
        codice: RE_CODICE.test(f.domanda || ''),
        prossima: f.prossima_domanda || null,
      };
    });
  }

  function ensureData() {
    if (store.ready) return store.ready;
    store.ready = Promise.all([
      loadJson(BASE + 'archivio-a-100-faq.json'),
      loadJson(BASE + 'archivio-b-100-faq.json'),
      loadJson(BASE + 'flusso-apertura-chat.json'),
      loadJson(BASE + 'inventario_immobili.json'),
    ]).then(function (all) {
      store.a = normalizzaFaq(all[0] && all[0].faq);
      store.b = normalizzaFaq(all[1] && all[1].faq);
      store.flusso = all[2] || {};
      store.inventario = all[3] || {};
      store.anomalie = {};
      ((store.inventario && store.inventario.immobili) || []).forEach(function (im) {
        if (im && im.riferimento && im.anomalie && im.anomalie.length) {
          store.anomalie[String(im.riferimento).toUpperCase()] = im.anomalie;
        }
      });
      return store;
    }).catch(function () {
      store.a = [];
      store.b = [];
      store.flusso = {};
      store.inventario = {};
      store.anomalie = {};
      return store;
    });
    return store.ready;
  }

  function passaggio(id) {
    var ps = (store.flusso && store.flusso.passaggi) || [];
    for (var i = 0; i < ps.length; i++) if (ps[i].id === id) return ps[i];
    return null;
  }

  function defaultSession() {
    return {
      argomento: null,
      operazione: null,
      comune: null,
      quesito_tecnico: null,
      promemoriaMostrato: false,
      invitoNovitaMostrato: false,
      nonRiproporreContatti: false,
      ap08Mostrato: false,
      recensioneMostrata: false,
      chatAvviata: false,
      ricerca: { tipo_op: null, zona: null, budget: null, tipologia: null, mq: null },
    };
  }

  function ensureSession(engine) {
    if (!engine.chatSession) engine.chatSession = defaultSession();
    return engine.chatSession;
  }

  function formatFonti(fonti) {
    if (!fonti || !fonti.length) return '';
    var righe = [];
    fonti.slice(0, 3).forEach(function (f) {
      var t = String(f.fonte || f.titolo || f.ente || 'Fonte').replace(/[\[\]()]/g, '').slice(0, 120);
      righe.push('[' + t + '](' + String(f.url).trim() + ')');
    });
    return '\n\n**Fonte:** ' + righe.join(' · ');
  }

  function formatArchivioA(faq) {
    return faq.r + formatFonti(faq.fonti);
  }

  function formatArchivioB(faq) {
    return faq.r + formatFonti(faq.fonti);
  }

  // Punteggio: copertura delle parole della domanda archiviata E della domanda dell'utente (parole radicate, senza stopword).
  function scoreFaq(qtok, faq, lax) {
    if (!faq || !faq.cand || !qtok.length) return 0;
    var best = 0;
    for (var c = 0; c < faq.cand.length; c++) {
      var ct = faq.cand[c];
      if (!ct.length) continue;
      var hits = 0;
      qtok.forEach(function (w) { if (ct.indexOf(w) >= 0) hits++; });
      if (hits < 2 && !(hits === 1 && qtok.length <= 2 && ct.length <= 2)) continue;
      var covQ = hits / qtok.length, covC = hits / ct.length;
      // Regola stretta: copertura >=75% in entrambe le direzioni (sempre attiva).
      var ok = (covQ >= 0.75 && covC >= 0.75);
      // Varianti controllate, solo in modalita' rilassata (tryArchiviFaq la usa dopo il giro stretto
      // e mai per domande di disponibilita'/catalogo, che restano al percorso live):
      //  a) voce lunga ma sovrapposizione forte (>=3 parole, utente coperto al 75%, voce al 60%)
      //  b) domanda utente interamente coperta e voce coperta almeno a meta'
      //  c) voce brevissima (<=2 parole) interamente coperta, utente coperto almeno a meta'
      if (!ok && lax) {
        ok = (covQ >= 0.75 && hits >= 3 && covC >= 0.6)
          || (covQ === 1 && hits >= 2 && covC >= 0.5)
          || (covQ >= 0.66 && hits >= 2 && covC >= 0.75)
          || (hits === 1 && ct.length <= 2 && covC === 1 && covQ >= 0.5);
      }
      if (!ok) continue;
      var sc = Math.round((covQ + covC) * 50);
      if (sc > best) best = sc;
    }
    return best;
  }

  function searchArchivio(voci, low, minScore, lax) {
    var qtok = tokens(low);
    var best = null, bestS = minScore || 60;
    for (var i = 0; i < voci.length; i++) {
      var sc = scoreFaq(qtok, voci[i], lax);
      if (sc >= bestS) { best = voci[i]; bestS = sc; }
    }
    return best;
  }

  function isLiveCatalogQuery(low) {
    return RE_LIVE.test(low) || RE_CODICE.test(low);
  }

  function isAvailabilityPriceOnly(low) {
    return /\b(prezzo|costa|disponib|canone|quanto)\b/.test(low) && RE_CODICE.test(low);
  }

  function parseArgomento(low, msg) {
    if (/\b(cerco|cerca|cercare|trovare|annunc|immobil|bilocale|trilocale|monolocale|appartament|villa|uffici|ufficio)\b/.test(low) &&
        !/\b(vendere|vendo|valut)\b/.test(low)) return 'ricerca_immobile';
    if (/\b(vendo|vendere|mandato|incarico)\b/.test(low)) return 'vendere';
    if (/\b(affitto la mia|affittare la m|locare la m|mettere in affitto)\b/.test(low)) return 'affittare_proprieta';
    if (/\b(valutaz|stimare|quanto vale)\b/.test(low)) return 'valutazione';
    if (/\b(rogito|preliminare|ape\b|catast|visura|conformit|documenti|mutuo|imu\b|cedolare)\b|\btecnic\w*/.test(low)) return 'tecnico';
    if (/\b(uffici|ufficio)\b/.test(low) && !/\b(cerco|affitt|compr)\b/.test(low)) return 'ricerca_immobile';
    return null;
  }

  function parseRicercaFromMsg(low, msg, session) {
    var r = session.ricerca;
    if (/affitt|locaz/.test(low)) r.tipo_op = 'affitto';
    if (/acquist|compr|vendita/.test(low)) r.tipo_op = 'vendita';
    if (/appartament/.test(low)) r.tipologia = 'appartamento';
    if (/bilocale/.test(low)) r.tipologia = 'bilocale';
    if (/trilocale/.test(low)) r.tipologia = 'trilocale';
    if (/villa/.test(low)) r.tipologia = 'villa';
    if (/uffici|ufficio/.test(low)) r.tipologia = 'ufficio';
    var budget = low.match(/(?:fino a|entro|max|massimo|budget)\s*(?:di\s*)?(\d{1,3}(?:[.\s]\d{3})+|\d{3,7})(?!\d)\s*(?:€|euro)?/);
    if (!budget) budget = low.match(/(\d{1,3}(?:[.\s]\d{3})+|\d{3,7})(?![\d])\s*(?:€|euro)/);
    if (budget) r.budget = parseInt(budget[1].replace(/[.\s]/g, ''), 10);
    var comuni = ['limena', 'padova', 'abano', 'vigonza', 'cittadella', 'limena', 'rubano', 'mestrino'];
    for (var i = 0; i < comuni.length; i++) {
      if (low.includes(comuni[i])) { r.zona = comuni[i]; break; }
    }
    var mq = low.match(/(\d{2,4})\s*(?:mq|m2|m²)/);
    if (mq) r.mq = parseFloat(mq[1]);
  }

  function promemoriaContatti(session) {
    if (session.nonRiproporreContatti || session.promemoriaMostrato) return '';
    session.promemoriaMostrato = true;
    var p = passaggio('AP-02');
    return p ? '\n\n---\n' + p.messaggio : '';
  }

  function invitoNovita(session) {
    if (session.invitoNovitaMostrato) return '';
    session.invitoNovitaMostrato = true;
    var p = passaggio('AP-07');
    if (!p) return '';
    var link = p.link_verificato ? '\n\n👉 [Catalogo immobili](/immobili)' : '';
    return '\n\n---\n' + p.messaggio + link;
  }

  // Scheda Google dell agenzia (destinazione del link verificata: Gruppo Immobiliare Righetto, Via Roma 96, Limena PD)
  var LINK_RECENSIONE = 'https://maps.app.goo.gl/Yg451gpKsFf9u3Fd7';
  function invitoRecensione(session) {
    if (!session || session.recensioneMostrata) return '';
    session.recensioneMostrata = true;
    return '\n\n---\nSe l\'esperienza con questa chat ti \u00e8 stata utile, puoi lasciare una recensione su Google: aiuta altre persone a scegliere con pi\u00f9 sicurezza.\n[Lascia una recensione su Google](' + LINK_RECENSIONE + ')';
  }

  function messaggioAP01() {
    var p = passaggio('AP-01');
    return p ? p.messaggio : 'Di cosa vorresti parlare?';
  }

  function getIncongruenze(codice) {
    return (store.anomalie && store.anomalie[String(codice || '').toUpperCase()]) || [];
  }

  var CAMPO_RE = {
    bagni: /bagn/i, prezzo: /prezz|canone|vendita|locazione|\d\s*euro/i, superficie: /\bmq\b|superficie/i,
    comune: /comune|zona|titolo/i, piano: /piano|livell/i, camere: /camer/i, locali: /locali/i,
    giardino: /giardin/i, spese_condominio: /spese/i, arredato: /arred/i, consegna: /liber|consegn|occupat|locat/i,
  };

  function testoIncongruenze(codice, campo) {
    var rows = getIncongruenze(codice);
    if (!rows.length) return '';
    var pick = rows;
    if (campo && CAMPO_RE[campo]) {
      var f = rows.filter(function (x) { return CAMPO_RE[campo].test(x); });
      pick = f;
    } else if (campo) { pick = []; }
    if (!pick.length) return '';
    var out = '\n\n⚠️ **Nota di verifica (' + String(codice).toUpperCase() + '):**';
    pick.forEach(function (x) { out += '\n• ' + x; });
    return out;
  }

  function attach(engine, rigChat) {
    if (!engine || engine.__archiviOuter) return;
    engine.__archiviOuter = true;
    ensureSession(engine);
    var orig = engine.process.bind(engine);

    if (rigChat && typeof rigChat.startChat === 'function') {
      var origStart = rigChat.startChat.bind(rigChat);
      rigChat.startChat = function () {
        origStart();
        ensureSession(engine);
        engine.chatSession.chatAvviata = true;
        var msgs = document.getElementById('rig-chat-msgs');
        if (msgs && msgs.querySelectorAll('.chat-msg.bot .chat-bubble').length) {
          var bubbles = msgs.querySelectorAll('.chat-msg.bot .chat-bubble');
          var last = bubbles[bubbles.length - 1];
          if (last) last.innerHTML = rigChat.renderMarkdown(messaggioAP01());
        }
      };
    }

    engine.process = async function (userMsg) {
      await ensureData();
      var msg = String(userMsg || '').trim();
      var low = msg.toLowerCase();
      var session = ensureSession(engine);

      if (/non voglio lasciare|senza telefono|senza recapit|no modulo|non desidero lasciare|senza dare il telefono/.test(low)) {
        session.nonRiproporreContatti = true;
      }

      if (engine.state === 'archivi_riassunto_modulo') {
        engine.state = 'idle';
        if (/^s(i|ì)|certo|ok|va bene|yes/.test(low)) {
          return 'Puoi scrivere nel modulo, ad esempio:\n• Codice annuncio (se presente)\n• Domanda precisa (es. numero bagni, ubicazione)\n• Eventuale fascia oraria per un ricontatto\n\nPuoi usare il modulo nella scheda dell\'immobile o la pagina [Contatti](/contatti).';
        }
        return 'Va bene. Se ti serve altro, scrivi pure.';
      }

      if (engine.state === 'archivi_ricerca_superficie') {
        var n = parseFloat(msg.replace(/[^0-9,.]/g, '').replace(',', '.'));
        engine.state = 'idle';
        if (isNaN(n) || n < 1) return 'Indica i metri quadri con un numero (es. 75).';
        session.ricerca.mq = n;
        return engine.cercaImmobiliCatalogo(
          session.ricerca.tipo_op,
          session.ricerca.zona,
          { maxPrezzo: session.ricerca.budget, tipologia: session.ricerca.tipologia, mq: session.ricerca.mq }
        );
      }

      if (engine.state === 'archivi_ricerca_operazione') {
        if (/affitt|locaz/.test(low)) session.ricerca.tipo_op = 'affitto';
        else if (/acquist|compr|vendit/.test(low)) session.ricerca.tipo_op = 'vendita';
        else return passaggio('AP-03') ? passaggio('AP-03').messaggio : 'Cerchi acquisto o locazione?';
        engine.state = 'idle';
        return nextRicercaStep(engine, session);
      }

      if (engine.state !== 'idle' && !String(engine.state).startsWith('archivi_')) {
        return orig(userMsg);
      }

      if (!session.argomento) {
        var a = parseArgomento(low, msg);
        if (a) session.argomento = a;
      }
      if (session.argomento === 'ricerca_immobile') parseRicercaFromMsg(low, msg, session);
      if (!session.argomento) {
        var parsed = parseArgomento(low, msg);
        if (parsed) session.argomento = parsed;
        if (session.argomento === 'ricerca_immobile') parseRicercaFromMsg(low, msg, session);
      }

      if (engine.state === 'idle' && session.argomento === 'ricerca_immobile' && /\b(cerco|affitt|appartament|bilocale|trilocale)\b/.test(low)) {
        var rr = session.ricerca;
        if (rr.zona || rr.budget || rr.mq) {
          var stepR = nextRicercaStep(engine, session);
          if (stepR) return stepR + promemoriaContatti(session);
        }
      }

      if (engine.state === 'idle' && /uffici|ufficio/.test(low) && !session.ricerca.tipo_op && !/\b(vendere|vendo)\b/.test(low)) {
        session.argomento = 'ricerca_immobile';
        session.ricerca.tipologia = 'ufficio';
        engine.state = 'archivi_ricerca_operazione';
        var uffMsg2 = 'Cerchi un **ufficio** da acquistare oppure da prendere in affitto?';
        if (session.nonRiproporreContatti && !session.ap08Mostrato) {
          session.ap08Mostrato = true;
          var p8u2 = passaggio('AP-08');
          if (p8u2) uffMsg2 = p8u2.messaggio + '\n\n' + uffMsg2;
        }
        return uffMsg2;
      }

      if (RE_CODICE.test(msg) || (isLiveCatalogQuery(low) && session.argomento === 'ricerca_immobile' && /\b(cerco|avete|vedete)\b/.test(low) && !session.ricerca.budget && !session.ricerca.zona && !/uffici|ufficio/.test(low))) {
        var liveResp = await orig(userMsg);
        liveResp = await enrichResponse(engine, session, msg, liveResp);
        return liveResp;
      }

      var resp = await orig(userMsg);
      if (session.nonRiproporreContatti && /senza telefono|senza dare il telefono/.test(low)) {
        var p8b = passaggio('AP-08');
        if (p8b && resp.indexOf(p8b.messaggio.slice(0, 20)) < 0) resp = p8b.messaggio + '\n\n' + resp;
      }
      return enrichResponse(engine, session, msg, resp);
    };
  }

  function nextRicercaStep(engine, session) {
    var r = session.ricerca;
    if (!r.tipo_op) {
      engine.state = 'archivi_ricerca_operazione';
      var p3 = passaggio('AP-03');
      return p3 ? p3.messaggio : 'Cerchi acquisto o locazione?';
    }
    if (!r.mq && (r.zona || r.budget || r.tipologia)) {
      engine.state = 'archivi_ricerca_superficie';
      var recap = 'Uso i requisiti che hai già indicato';
      if (r.tipologia) recap += ': **' + r.tipologia + '**';
      if (r.tipo_op) recap += ', **' + r.tipo_op + '**';
      if (r.zona) recap += ', **' + r.zona.charAt(0).toUpperCase() + r.zona.slice(1) + '**';
      if (r.budget) recap += (r.tipo_op === 'affitto' ? ', canone massimo **€ ' : ', budget massimo **€ ') + String(r.budget).replace(/\B(?=(\d{3})+(?!\d))/g, '.') + '**';
      recap += '.\n\n**Quale superficie preferisci?** (mq)';
      return recap;
    }
    return null;
  }

  // Messaggio che indica solo l'argomento tecnico, senza un quesito preciso (es. "una questione tecnica", "mutuo")
  function isSoloArgomentoTecnico(low) {
    var t = tokens(low);
    return t.length <= 3 && /\b(tecnic|mutuo|catast|visura|rogito|preliminare|conformit|documenti)\w*/.test(low) && !/\?/.test(low);
  }

  function isChiusura(low) {
    return /^(grazie|ok grazie|grazie mille|va bene cos[iì]|e tutto|è tutto|basta cos[iì]|niente altro|nient'altro|no grazie|a posto|arrivederci|ciao ciao|ci sentiamo|alla prossima)\b/.test(low.trim());
  }

  async function enrichResponse(engine, session, msg, resp) {
    var low = msg.toLowerCase();
    if (session.nonRiproporreContatti && !session.ap08Mostrato) {
      session.ap08Mostrato = true;
      var p8 = passaggio('AP-08');
      if (p8) resp = p8.messaggio + '\n\n' + resp;
    }
    if (!session.argomento) {
      var a = parseArgomento(low, msg);
      if (a) session.argomento = a;
    }

    var m = msg.match(RE_CODICE);
    if (m) {
      var campoQ = null;
      var QRE = { bagni: /bagn/, prezzo: /prezz|costa|canone|quanto/, superficie: /\bmq\b|metri|superfic/, camere: /camer/, giardino: /giardin/, spese_condominio: /spese/, consegna: /libero|liber|disponibil|consegn/, piano: /\bpiano\b/ };
      Object.keys(QRE).forEach(function (k) { if (!campoQ && QRE[k].test(low)) campoQ = k; });
      var inc = testoIncongruenze(m[1].toUpperCase(), campoQ);
      if (inc && resp.indexOf('Nota di verifica') < 0) resp += inc;
      if (/\bbagn/i.test(low) && inc.indexOf('bagn') >= 0) {
        var p6 = passaggio('AP-06');
        if (p6 && !session.nonRiproporreContatti) {
          engine.state = 'archivi_riassunto_modulo';
          resp += '\n\n' + p6.messaggio;
        }
      }
    }

    var promemoriaAggiunto = false;
    if (session.argomento && !session.promemoriaMostrato && !session.nonRiproporreContatti && !/^ciao|salve|buongiorno/.test(low)) {
      var _prom = promemoriaContatti(session);
      promemoriaAggiunto = !!_prom;
      resp += _prom;
    }

    var soloTecnico = false;
    if (session.argomento === 'tecnico' && !session.quesito_tecnico && engine.state === 'idle' && isSoloArgomentoTecnico(low)) {
      var p5 = passaggio('AP-05');
      if (p5) {
        session.quesito_tecnico = 'richiesto';
        soloTecnico = true;
        resp = /far verificare questo punto da un nostro consulente|Per non darle un'informazione inesatta/.test(resp)
          ? p5.messaggio : resp + (resp.indexOf('?') < 0 ? '\n\n' + p5.messaggio : '');
      }
    }

    if (isChiusura(low) && !session.invitoNovitaMostrato) resp += invitoNovita(session);

    var isFallback = /far verificare questo punto da un nostro consulente|Per non darle un'informazione inesatta/.test(resp);
    if (isFallback && !session.invitoNovitaMostrato) resp += invitoNovita(session);

    if (session.argomento === 'valutazione' && !session.comune && engine.state === 'idle' && /valutaz|stim/.test(low)) {
      var p4 = passaggio('AP-04');
      if (p4) resp += '\n\n' + p4.messaggio;
    }

    // Invito alla recensione Google nei momenti di chiusura verso i contatti (una volta a sessione)
    if (isFallback || isChiusura(low) || promemoriaAggiunto) resp += invitoRecensione(session);

    return resp;
  }

  function waitAttach(n) {
    n = n || 0;
    if (window.rigChat && window.rigChat.engine && window.rigChat.engine.__lindaKb) {
      attach(window.rigChat.engine, window.rigChat);
      return;
    }
    if (n < 60) setTimeout(function () { waitAttach(n + 1); }, 250);
  }

  ensureData();
  waitAttach();

  async function tryArchiviFaq(engine, userMsg) {
    await ensureData();
    var low = String(userMsg || '').toLowerCase();
    if (isAvailabilityPriceOnly(low)) return null;
    if (/\b(stim|valut|quanto vale|quanto potrebbe valere)\b/.test(low) && /\b(mio|miei|immobile|casa|appartament)\b/.test(low)) {
      return null;
    }
    if (/\b(appuntament|contatt|richiam|essere chiamat|farmi chiamare|voglio essere contattato|fissare un appuntamento)\b/.test(low)) {
      return null;
    }
    // Domande di disponibilita'/catalogo: solo il giro stretto; le parafrasi rilassate
    // rischierebbero di rispondere con una FAQ di metodo a chi chiede gli annunci (percorso live).
    var RE_DISPONIBILITA = /\b(avete|vedete|ci sono|in vendita|in affitto|in locazione|disponibil\w*|catalogo)\b/i;
    var fa = searchArchivio(store.a, low, 60);
    if (!fa && !RE_DISPONIBILITA.test(low)) fa = searchArchivio(store.a, low, 60, true);
    if (fa) return formatArchivioA(fa);
    // Archivio B: tutte le voci richiedono rilettura del catalogo live. Si usano solo le risposte
    // non legate a una scheda e che non sono istantanee di disponibilità (quelle vanno al catalogo live).
    if (!isLiveCatalogQuery(low)) {
      var usabili = store.b.filter(function (x) { return !x.snapshot && !x.codice && !RE_CODICE.test(x.r.split('http')[0]); });
      var fb = searchArchivio(usabili, low, 60);
      if (fb) return formatArchivioB(fb);
    }
    return null;
  }

  window.RighettoChatArchivi = {
    ensureData: ensureData,
    getIncongruenze: getIncongruenze,
    testoIncongruenze: testoIncongruenze,
    searchArchivio: searchArchivio,
    tryArchiviFaq: tryArchiviFaq,
    formatArchivioA: formatArchivioA,
    promemoriaContatti: promemoriaContatti,
    enrichResponse: enrichResponse,
    messaggioAP01: messaggioAP01,
    version: 2,
  };
})();
