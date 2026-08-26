/**
 * LINDA Learning Bridge — A. Event Collector (client)
 * Modulo opzionale: disattivare con window.LINDA_LEARNING_BRIDGE = false prima del load.
 */
(function () {
  'use strict';

  if (window.LINDA_LEARNING_BRIDGE === false) return;

  var SUPABASE_URL = 'https://qwkwkemuabfwvwuqrxlu.supabase.co';
  var SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3a3drZW11YWJmd3Z3dXFyeGx1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE1OTk5NjEsImV4cCI6MjA4NzE3NTk2MX0.JxEYiWVPEOiwjZtbWAZRlMUdKXcupjw7filvrERCiqc';

  var ENABLED = true;
  var sessionId = 'lb_' + Date.now() + '_' + Math.random().toString(36).slice(2, 8);
  var currentSearchId = null;
  var lastActivity = Date.now();
  var supabase = null;
  var queue = [];
  var flushTimer = null;

  function initSupabase() {
    if (window.supabase && window.supabase.createClient) {
      supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
    }
  }

  function hashMsg(text) {
    if (!text) return null;
    var s = String(text).toLowerCase().trim().replace(/\s+/g, ' ');
    var h = 0;
    for (var i = 0; i < s.length; i++) h = ((h << 5) - h + s.charCodeAt(i)) | 0;
    return 'h' + Math.abs(h).toString(16);
  }

  function trackGa(eventType, payload) {
    if (typeof window.trackEvent === 'function') {
      window.trackEvent('linda_learning', eventType, payload.intent || 'chat', payload);
    } else if (window.gtag) {
      window.gtag('event', eventType, Object.assign({ event_category: 'linda_learning' }, payload));
    }
  }

  function enqueue(eventType, payload) {
    if (!ENABLED) return;
    lastActivity = Date.now();
    var row = {
      event_type: eventType,
      session_id: sessionId,
      search_id: currentSearchId,
      page_path: location.pathname,
      source: 'linda_chatbot',
      payload: payload || {},
      created_at: new Date().toISOString()
    };
    queue.push(row);
    trackGa(eventType, row.payload);
    if (!flushTimer) flushTimer = setTimeout(flush, 800);
  }

  function flushLocalBackup(rows) {
    try {
      var key = 'linda_lb_buffer';
      var prev = JSON.parse(localStorage.getItem(key) || '[]');
      localStorage.setItem(key, JSON.stringify(prev.concat(rows).slice(-200)));
    } catch (e) { /* ignore */ }
  }

  async function flush() {
    flushTimer = null;
    if (!queue.length) return;
    var batch = queue.splice(0, queue.length);
    flushLocalBackup(batch);
    if (!supabase) initSupabase();
    if (supabase) {
      try {
        await supabase.from('linda_learning_events').insert(batch);
      } catch (e) {
        queue = batch.concat(queue);
      }
    }
  }

  function newSearch(criteria) {
    currentSearchId = 's_' + Date.now() + '_' + Math.random().toString(36).slice(2, 6);
    enqueue('search_started', {
      search_id: currentSearchId,
      criteria: criteria || {},
      ranking_version: 'baseline_v1'
    });
    return currentSearchId;
  }

  function attachChat(engine, rigChat) {
    if (!engine || !rigChat) return;

    var origProcess = engine.process.bind(engine);
    engine.process = async function (userMsg) {
      var resp = await origProcess(userMsg);
      var low = (userMsg || '').toLowerCase();
      var isDefault = resp.indexOf('Capito — forse non ho colto') >= 0;
      if (isDefault) {
        enqueue('question_unanswered', { user_message_hash: hashMsg(userMsg) });
      }
      if (/lead inviata|richiesta inviata/i.test(resp)) {
        enqueue('lead_created', { criteria: engine.ricercaData || {}, intent: 'contact' });
        enqueue('conversation_completed', { intent: 'lead' });
      }
      if (/visita|appuntament/i.test(low) && engine.state === 'contatto_nome') {
        enqueue('visit_requested', { criteria: engine.ricercaData || {} });
      }
      return resp;
    };

    var origCatalogo = engine.cercaImmobiliCatalogo.bind(engine);
    engine.cercaImmobiliCatalogo = async function (tipoOp, zona) {
      newSearch({
        tipo_operazione: tipoOp || null,
        comune: zona || null,
        zona: zona || null
      });
      var msg = await origCatalogo(tipoOp, zona);
      if (/non ho immobili|mi dispiace/i.test(msg)) {
        enqueue('search_no_result', { criteria: { tipo_operazione: tipoOp, comune: zona } });
      } else if (/Ecco gli immobili/i.test(msg)) {
        var ids = [];
        var re = /immobile\.html\?s=([^"'\)]+)/g;
        var m;
        while ((m = re.exec(msg))) ids.push(decodeURIComponent(m[1]));
        enqueue('property_results_shown', {
          criteria: { tipo_operazione: tipoOp, comune: zona },
          property_ids: ids,
          result_count: ids.length
        });
      }
      return msg;
    };

    var origSend = rigChat.send.bind(rigChat);
    rigChat.send = async function (text) {
      await origSend(text);
    };

    document.getElementById('rig-chat-msgs')?.addEventListener('click', function (ev) {
      var a = ev.target.closest('a[href*="immobile.html"]');
      if (!a) return;
      var href = a.getAttribute('href') || '';
      var slugMatch = href.match(/[?&]s=([^&]+)/);
      enqueue('property_clicked', {
        property_slug: slugMatch ? decodeURIComponent(slugMatch[1]) : null,
        criteria: engine.ricercaData || {}
      });
    });

    rigChat.toggle = (function (orig) {
      return function () {
        var wasOpen = rigChat.open;
        orig.apply(rigChat, arguments);
        if (wasOpen && !rigChat.open && rigChat.msgCount > 0) {
          enqueue('conversation_abandoned', { messages: rigChat.msgCount });
        }
        if (!wasOpen && rigChat.open) {
          enqueue('search_started', { intent: 'chat_open', criteria: {} });
        }
      };
    })(rigChat.toggle);
  }

  function waitForChat(retries) {
    retries = retries || 0;
    if (window.rigChat && window.rigChat.engine) {
      attachChat(window.rigChat.engine, window.rigChat);
      return;
    }
    if (retries < 40) setTimeout(function () { waitForChat(retries + 1); }, 250);
  }

  initSupabase();
  waitForChat();

  window.LindaLearningBridge = {
    enabled: ENABLED,
    track: enqueue,
    newSearch: newSearch,
    flush: flush,
    getSessionId: function () { return sessionId; }
  };
})();
