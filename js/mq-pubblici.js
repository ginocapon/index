/**
 * Overlay mq PUBBLICI per singoli immobili (dati commerciali gia' pubblici sui portali).
 * Mai persistito: il DB conserva superficie reale e superficie_portali (admin intatti);
 * qui si allinea solo il valore mostrato su schede/card/OG/JSON-LD/brochure pubbliche.
 * Ancorato a UUID + codice; applicato dopo la lettura della riga attiva.
 */
(function (global) {
  'use strict';
  var MQ_PUBBLICI = {
    '2dfc63f5-b771-4732-89af-4e8aa96eb9d4': { codice: 'LA0326', superficie: 80 }
  };
  global.applicaMqPubblici = function (rec) {
    if (!rec) return rec;
    var o = MQ_PUBBLICI[rec.id];
    if (o && (rec.codice || '').trim() === o.codice && typeof o.superficie === 'number') {
      rec.superficie = o.superficie;
    }
    return rec;
  };
})(typeof window !== 'undefined' ? window : global);
