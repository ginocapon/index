/**
 * Alert scadenze incarico (mandato) nella home admin Immobili.
 * Usa allImmobili già caricato (select *): nessuna query extra.
 */
(function () {
  'use strict';

  var WARN_DAYS = 30;

  function todayUtc() {
    var n = new Date();
    return new Date(Date.UTC(n.getUTCFullYear(), n.getUTCMonth(), n.getUTCDate()));
  }

  function parseDay(raw) {
    if (!raw) return null;
    var s = String(raw).slice(0, 10);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(s)) return null;
    var d = new Date(s + 'T12:00:00Z');
    return Number.isNaN(+d) ? null : d;
  }

  function classify(rows) {
    var start = todayUtc();
    var warnUntil = new Date(start);
    warnUntil.setUTCDate(warnUntil.getUTCDate() + WARN_DAYS);
    var expired = [];
    var expiring = [];
    (rows || []).forEach(function (row) {
      if (!row || row.cestino === true) return;
      if (row.venduto === true || row.affittato === true) return;
      var d = parseDay(row.incarico_scadenza);
      if (!d) return;
      var item = {
        id: row.id,
        codice: row.codice || '—',
        titolo: row.titolo || '',
        comune: row.comune || '',
        scadenza: String(row.incarico_scadenza).slice(0, 10),
        attivo: row.attivo === true,
      };
      if (d < start) expired.push(item);
      else if (d <= warnUntil) expiring.push(item);
    });
    expired.sort(function (a, b) {
      return a.scadenza.localeCompare(b.scadenza);
    });
    expiring.sort(function (a, b) {
      return a.scadenza.localeCompare(b.scadenza);
    });
    return { expired: expired, expiring: expiring };
  }

  function esc(s) {
    return String(s || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function rowHtml(item) {
    return (
      '<li><button type="button" class="mandate-alert-link" data-id="' +
      esc(item.id) +
      '"><strong>' +
      esc(item.codice) +
      '</strong> · ' +
      esc(item.comune) +
      ' · scadenza <time datetime="' +
      esc(item.scadenza) +
      '">' +
      esc(item.scadenza) +
      '</time>' +
      (item.attivo ? '' : ' <em>(non attivo sul sito)</em>') +
      '</button></li>'
    );
  }

  function ensureBox() {
    var box = document.getElementById('mandateAlerts');
    if (box) return box;
    var stats = document.getElementById('statsGrid');
    if (!stats || !stats.parentNode) return null;
    box = document.createElement('div');
    box.id = 'mandateAlerts';
    box.className = 'mandate-alerts';
    box.setAttribute('aria-live', 'polite');
    stats.parentNode.insertBefore(box, stats.nextSibling);
    box.addEventListener('click', function (ev) {
      var btn = ev.target.closest('[data-id]');
      if (!btn || !window.editImmobile) return;
      window.editImmobile(btn.getAttribute('data-id'));
    });
    return box;
  }

  function render(data) {
    var box = ensureBox();
    if (!box) return;
    var c = classify(data);
    if (!c.expired.length && !c.expiring.length) {
      box.innerHTML =
        '<div class="mandate-alerts-ok">Nessun incarico scaduto o in scadenza nei prossimi ' +
        WARN_DAYS +
        ' giorni (tra gli immobili in elenco).</div>';
      return;
    }
    var html = '<div class="mandate-alerts-head">Scadenze incarico (mandato)</div>';
    if (c.expired.length) {
      html +=
        '<div class="mandate-alerts-block mandate-expired"><div class="mandate-alerts-title">Scaduti (' +
        c.expired.length +
        ')</div><ul>' +
        c.expired
          .slice(0, 40)
          .map(rowHtml)
          .join('') +
        '</ul></div>';
    }
    if (c.expiring.length) {
      html +=
        '<div class="mandate-alerts-block mandate-expiring"><div class="mandate-alerts-title">In scadenza entro ' +
        WARN_DAYS +
        ' giorni (' +
        c.expiring.length +
        ')</div><ul>' +
        c.expiring
          .slice(0, 40)
          .map(rowHtml)
          .join('') +
        '</ul></div>';
    }
    box.innerHTML = html;
  }

  function hook() {
    if (typeof window.updateStats === 'function' && !window.updateStats.__mandateHooked) {
      var orig = window.updateStats;
      window.updateStats = function (data) {
        orig(data);
        render(data);
      };
      window.updateStats.__mandateHooked = true;
    }
    render(window.allImmobili || []);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', hook);
  } else {
    hook();
  }
  window.addEventListener('righetto:catalogue-state', function () {
    render(window.allImmobili || []);
  });
})();
