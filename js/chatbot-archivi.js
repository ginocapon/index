/**
 * Archivi FAQ A/B, flusso apertura chat, inventario incongruenze (v1)
 * Caricato da js/chatbot.js — disattiva: window.RIGHETTO_CHAT_ARCHIVI = false
 */
(function () {
  'use strict';
  if (window.RIGHETTO_CHAT_ARCHIVI === false) return;

  var BASE = 'data/chatbot/';
  var store = { a: [], b: [], flusso: null, inventario: {}, ready: null };
  var RE_CODICE = /\b([A-Za-z]{1,4}\d{3,5})\b/;
  var RE_LIVE = /\b(prezzo|costa|disponib|disponibile|annuncio|catalogo|avete|vedete|cerco|affitt|vendit|compr|canone)\b/i;

  function loadJson(url) {
    return fetch(url, { cache: 'no-cache' }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
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
      store.a = (all[0] && all[0].voci) || [];
      store.b = (all[1] && all[1].voci) || [];
      store.flusso = all[2] || {};
      store.inventario = all[3] || {};
      return store;
    }).catch(function () {
      store.a = [];
      store.b = [];
      store.flusso = {};
      store.inventario = {};
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
      chatAvviata: false,
      ricerca: { tipo_op: null, zona: null, budget: null, tipologia: null, mq: null },
    };
  }

  function ensureSession(engine) {
    if (!engine.chatSession) engine.chatSession = defaultSession();
    return engine.chatSession;
  }

  function formatFonte(fonte) {
    if (!fonte || !fonte.url) return '';
    var u = String(fonte.url).trim();
    if (!/^https:\/\//i.test(u)) return '';
    var t = String(fonte.titolo || 'Fonte').replace(/[\[\]()]/g, '').slice(0, 120);
    return '\n\n**Fonte:** [' + t + '](' + u + ')';
  }

  function formatArchivioA(faq) {
    return faq.r + formatFonte(faq.fonte);
  }

  function formatArchivioB(faq) {
    return faq.r + (faq.fonte && faq.fonte.url ? formatFonte(faq.fonte) : '');
  }

  function scoreFaq(low, faq) {
    if (!faq || !faq.k) return 0;
    var dom = String(faq.domanda || '').toLowerCase();
    var corpus = dom + ' ' + faq.k.join(' ').toLowerCase();
    var stop = /^(che|per|con|del|della|dei|una|sono|quali|come|gli|hai|avete|vorrei|solo|sapere|dove|quando)$/;
    var words = low.replace(/[?.,!'"]/g, ' ').split(/\s+/).filter(function (w) {
      return w.length > 2 && !stop.test(w);
    });
    if (!words.length) return 0;
    var hits = 0;
    words.forEach(function (w) { if (corpus.indexOf(w) >= 0) hits++; });
    if (hits < 2) return 0;
    return Math.round((hits / words.length) * 80 + hits * 8);
  }

  function searchArchivio(voci, low, minScore) {
    var best = null, bestS = minScore || 28;
    for (var i = 0; i < voci.length; i++) {
      var s = scoreFaq(low, voci[i]);
      if (s >= bestS) { best = voci[i]; bestS = s; }
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
    if (/\b(rogito|preliminare|ape\b|catast|visura|conformit|documenti|mutuo|imu\b|cedolare)\b/.test(low)) return 'tecnico';
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
    var budget = low.match(/(?:fino a|max|massimo|budget)\s*(\d{2,5})\s*(?:€|euro)?/);
    if (!budget) budget = low.match(/(\d{3,4})\s*(?:€|euro)/);
    if (budget) r.budget = parseInt(budget[1], 10);
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

  function messaggioAP01() {
    var p = passaggio('AP-01');
    return p ? p.messaggio : 'Di cosa vorresti parlare?';
  }

  function getIncongruenze(codice) {
    var list = (store.inventario && store.inventario.incongruenze) || [];
    codice = String(codice || '').toUpperCase();
    return list.filter(function (x) { return x.codice === codice; });
  }

  function testoIncongruenze(codice, campo) {
    var rows = getIncongruenze(codice);
    if (!rows.length) return '';
    var out = '\n\n⚠️ **Nota di verifica (' + codice + '):**';
    rows.forEach(function (row) {
      if (campo && row.campi && row.campi.indexOf(campo) < 0 && row.campi.indexOf(campo.replace(/i$/, 'o')) < 0) return;
      out += '\n• ' + row.descrizione;
    });
    return out.indexOf('•') >= 0 ? out : '';
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
      if (r.budget) recap += ', canone massimo **€ ' + r.budget + '**';
      recap += '.\n\n**Quale superficie preferisci?** (mq)';
      return recap;
    }
    return null;
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
      var inc = testoIncongruenze(m[1].toUpperCase());
      if (inc && resp.indexOf('Nota di verifica') < 0) resp += inc;
      if (/\bbagn/i.test(low) && inc.indexOf('bagn') >= 0) {
        var p6 = passaggio('AP-06');
        if (p6 && !session.nonRiproporreContatti) {
          engine.state = 'archivi_riassunto_modulo';
          resp += '\n\n' + p6.messaggio;
        }
      }
    }

    if (session.argomento && !session.promemoriaMostrato && !session.nonRiproporreContatti && !/^ciao|salve|buongiorno/.test(low)) {
      resp += promemoriaContatti(session);
    }

    var isFallback = /far verificare questo punto da un nostro consulente|Per non darle un'informazione inesatta/.test(resp);
    if (isFallback && !session.invitoNovitaMostrato) resp += invitoNovita(session);

    if (session.argomento === 'valutazione' && !session.comune && engine.state === 'idle' && /valutaz|stim/.test(low)) {
      var p4 = passaggio('AP-04');
      if (p4) resp += '\n\n' + p4.messaggio;
    }

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
    var fa = searchArchivio(store.a, low, 28);
    if (fa) return formatArchivioA(fa);
    if (!isLiveCatalogQuery(low)) {
      var fb = searchArchivio(store.b, low, 28);
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
    version: 1,
  };
})();
