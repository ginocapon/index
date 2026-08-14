/**
 * LINDA Real Estate Agent — core (rule-based, no LLM)
 * Retrieval deterministico + ranking spiegabile + contesto conversazione.
 * Caricare prima di js/chatbot.js
 */
(function () {
  'use strict';

  var GOOGLE_REVIEW_URL = 'https://maps.app.goo.gl/xuCiRGDCSKskpTSf6?g_st=ic';

  function norm(s) {
    return (s || '').toLowerCase().trim()
      .replace(/[àáâãäå]/g, 'a').replace(/[èéêë]/g, 'e').replace(/[ìíîï]/g, 'i')
      .replace(/[òóôõö]/g, 'o').replace(/[ùúûü]/g, 'u')
      .replace(/[^a-z0-9\s']/g, ' ').replace(/\s+/g, ' ').trim();
  }

  function parseMoney(text) {
    var m = text.match(/(?:max|massimo|fino a|entro|budget|€|euro)\s*([\d.,]+)\s*(?:k|mila|000)?/i);
    if (!m) m = text.match(/([\d]{2,3})[.,]?(\d{3})?\s*(?:€|euro)/i);
    if (!m) return null;
    var raw = m[1].replace(/\./g, '').replace(',', '.');
    var n = parseFloat(raw);
    if (isNaN(n)) return null;
    if (/k|mila/i.test(text) && n < 1000) n *= 1000;
    if (n < 1000 && /000/.test(m[0])) n *= 1000;
    return Math.round(n);
  }

  function parseRooms(text) {
    var m = text.match(/(\d+)\s*(?:camere|camera|locali|stanze)/i);
    if (m) return parseInt(m[1], 10);
    if (/trilocale/i.test(text)) return 3;
    if (/bilocale/i.test(text)) return 2;
    if (/monolocale/i.test(text)) return 1;
    if (/quadrilocale/i.test(text)) return 4;
    return null;
  }

  function ConversationContext() {
    this.hard = {};
    this.soft = {};
    this.lastIntent = null;
    this.searchCount = 0;
    this.positiveInteraction = false;
  }

  ConversationContext.prototype.merge = function (intent) {
    if (!intent) return;
    var h = intent.hard || {};
    var s = intent.soft || {};
    for (var k in h) if (h[k] != null) this.hard[k] = h[k];
    for (var k2 in s) if (s[k2] != null) this.soft[k2] = s[k2];
    this.lastIntent = intent;
    if (intent.isPropertySearch) this.searchCount++;
  };

  function parseSearchIntent(text) {
    var low = norm(text);
    var intent = {
      isPropertySearch: false,
      operation: null,
      location: null,
      property_type: null,
      budget_max: null,
      budget_min: null,
      rooms: null,
      mq_min: null,
      mq_max: null,
      hard: {},
      soft: {},
      raw: text
    };

    if (/affitt|locaz|rent/.test(low)) intent.operation = 'affitto';
    if (/acquist|compr|vendita|vendere casa/.test(low)) intent.operation = 'vendita';
    if (/cerco|cerchi|vorrei|voglio|immobil|annunc|casa |appartam|villa |bilocale|trilocale|monolocale|garage|giardino|terrazzo|budget|massimo|camere|locali/.test(low)) {
      intent.isPropertySearch = true;
    }

    var loc = low.match(/(?:a|in|zona|comune|padova|limena|vigonza|abano|selvazzano|rubano|cittadella|monselice|este|camposampiero|albignasego|mestrino|cadoneghe|trebaseleghe)(?:\s+[a-z']+)?/i);
    if (loc) {
      var zoneWords = ['padova', 'limena', 'vigonza', 'abano', 'selvazzano', 'rubano', 'cittadella', 'monselice', 'este', 'camposampiero', 'albignasego', 'mestrino', 'cadoneghe', 'trebaseleghe', 'arcella', 'guizza', 'mandria', 'altichiero'];
      for (var i = 0; i < zoneWords.length; i++) {
        if (low.indexOf(zoneWords[i]) >= 0) {
          intent.location = zoneWords[i];
          break;
        }
      }
      if (!intent.location && loc[0]) intent.location = loc[0].replace(/^(a|in|zona|comune)\s+/i, '').trim();
    }

    var types = ['appartamento', 'villa', 'villetta', 'bilocale', 'trilocale', 'monolocale', 'attico', 'capannone', 'ufficio', 'terreno', 'rustico', 'mansarda'];
    for (var t = 0; t < types.length; t++) {
      if (low.indexOf(types[t]) >= 0) {
        intent.property_type = types[t];
        break;
      }
    }

    intent.budget_max = parseMoney(low);
    if (intent.budget_max) intent.hard.budget_max = intent.budget_max;

    intent.rooms = parseRooms(low);
    if (intent.rooms) intent.hard.rooms_min = intent.rooms;

    var mq = low.match(/(\d+)\s*(?:mq|m2|metri)/i);
    if (mq) {
      intent.mq_min = parseInt(mq[1], 10);
      intent.hard.mq_min = intent.mq_min;
    }

    if (/garage|box|posto auto|parcheggio/.test(low)) intent.soft.garage = true;
    if (/giardino/.test(low)) intent.soft.giardino = true;
    if (/terrazzo|balcon/.test(low)) intent.soft.terrazzo = true;
    if (/ascensore/.test(low)) intent.soft.ascensore = true;
    if (/ristruttur/.test(low)) intent.soft.ristrutturato = true;

    return intent;
  }

  function scoreProperty(imm, intent, fuzzyComune) {
    var score = 50;
    var reasons = [];
    var penalties = [];

    var prezzo = imm.prezzo ? Number(imm.prezzo) : null;
    var comune = norm(imm.comune || '');
    var tipo = norm(imm.tipologia || imm.categoria || '');
    var mq = imm.superficie ? Number(imm.superficie) : null;
    var camere = imm.camere ? Number(imm.camere) : (imm.locali ? Number(imm.locali) : null);
    var op = norm(imm.tipo_operazione || '');

    if (intent.operation && op && op.indexOf(intent.operation) < 0) {
      return { score: 0, reasons: [], eliminated: true, why: 'operazione diversa' };
    }

    if (intent.hard.budget_max && prezzo && prezzo > intent.hard.budget_max * 1.08) {
      return { score: 0, reasons: [], eliminated: true, why: 'prezzo sopra budget' };
    }

    if (intent.location) {
      var target = norm(intent.location);
      var fuzzy = fuzzyComune ? fuzzyComune(intent.location) : null;
      var want = norm(fuzzy || intent.location);
      if (comune.indexOf(want) >= 0 || want.indexOf(comune) >= 0) {
        score += 25;
        reasons.push('zona ' + (imm.comune || intent.location));
      } else {
        score -= 15;
        penalties.push('comune diverso da ' + intent.location);
      }
    }

    if (intent.property_type && tipo.indexOf(intent.property_type) >= 0) {
      score += 15;
      reasons.push('tipologia ' + (imm.tipologia || imm.categoria));
    }

    if (intent.hard.budget_max && prezzo) {
      var ratio = prezzo / intent.hard.budget_max;
      if (ratio <= 1) {
        score += 15;
        reasons.push('entro budget');
      } else if (ratio <= 1.05) {
        score += 8;
        reasons.push('vicino al budget');
      }
    }

    if (intent.hard.rooms_min && camere) {
      if (camere >= intent.hard.rooms_min) {
        score += 10;
        reasons.push(camere + ' camere/locali');
      } else {
        score -= 10;
        penalties.push('meno camere del richiesto');
      }
    }

    if (intent.hard.mq_min && mq) {
      if (mq >= intent.hard.mq_min * 0.9) {
        score += 8;
        reasons.push(mq + ' m²');
      } else {
        penalties.push('metratura inferiore');
      }
    }

    if (intent.soft.garage && (imm.garage || /garage|box/i.test(imm.titolo || ''))) {
      score += 6;
      reasons.push('garage/box');
    }
    if (intent.soft.giardino && (imm.giardino || /giardino/i.test(imm.titolo || ''))) {
      score += 6;
      reasons.push('giardino');
    }
    if (intent.soft.terrazzo && /terrazzo|balcon/i.test((imm.titolo || '') + (imm.descrizione || ''))) {
      score += 4;
      reasons.push('terrazzo/balcone');
    }

    if (imm.in_evidenza) score += 3;

    return {
      score: Math.max(0, Math.min(100, score)),
      reasons: reasons,
      penalties: penalties,
      eliminated: false
    };
  }

  function rankProperties(list, intent, helpers) {
    var fuzzy = helpers && helpers.fuzzyMatchComune;
    var ranked = [];
    for (var i = 0; i < list.length; i++) {
      var r = scoreProperty(list[i], intent, fuzzy);
      if (!r.eliminated) {
        ranked.push({ imm: list[i], score: r.score, reasons: r.reasons, penalties: r.penalties });
      }
    }
    ranked.sort(function (a, b) { return b.score - a.score; });
    return ranked;
  }

  function detectLeadIntent(text) {
    var low = norm(text);
    return /visita|appuntament|ricontatt|chiamat|contatt|mandate|mandare|permuta|valutaz|mutuo|prezzo esatto|offerta|interessato/.test(low);
  }

  function shouldOfferReview(ctx) {
    return ctx && ctx.searchCount >= 1 && ctx.positiveInteraction;
  }

  window.LindaAgent = {
    GOOGLE_REVIEW_URL: GOOGLE_REVIEW_URL,
    ConversationContext: ConversationContext,
    parseSearchIntent: parseSearchIntent,
    rankProperties: rankProperties,
    detectLeadIntent: detectLeadIntent,
    shouldOfferReview: shouldOfferReview,
    norm: norm
  };
})();
