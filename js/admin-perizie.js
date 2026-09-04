/* Admin — Archivio perizie immobiliari (PDF) */
(function () {
  'use strict';

  var perizieCache = [];
  var perizieFilter = '';

  function esc(s) {
    if (typeof escHtml === 'function') return escHtml(s);
    return String(s || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function fmtData(iso) {
    if (!iso) return '—';
    var p = String(iso).split('-');
    if (p.length !== 3) return iso;
    return p[2] + '/' + p[1] + '/' + p[0];
  }

  function fmtEuro(n) {
    if (n == null || n === '') return '—';
    return '€ ' + Number(n).toLocaleString('it-IT');
  }

  function matchFilter(row, q) {
    if (!q) return true;
    var hay = [
      row.proprietario,
      row.indirizzo,
      row.tipologia,
      row.note,
      row.data,
      fmtData(row.data)
    ].join(' ').toLowerCase();
    return hay.indexOf(q) >= 0;
  }

  function renderPerizie() {
    var el = document.getElementById('perizieTableBody');
    var empty = document.getElementById('perizieEmpty');
    var stat = document.getElementById('statPerizieCount');
    if (!el) return;

    var q = perizieFilter.trim().toLowerCase();
    var rows = perizieCache.filter(function (r) { return matchFilter(r, q); });
    if (stat) stat.textContent = String(perizieCache.length);

    if (!rows.length) {
      el.innerHTML = '';
      if (empty) {
        empty.style.display = 'block';
        empty.querySelector('p').textContent = q
          ? 'Nessuna perizia corrisponde alla ricerca.'
          : 'Nessuna perizia in archivio.';
      }
      return;
    }
    if (empty) empty.style.display = 'none';

    el.innerHTML = rows.map(function (r) {
      var pdfBase = r.pdf || '';
      var pdfVer = r.pdf_version ? String(r.pdf_version) : '';
      var pdf = esc(pdfBase + (pdfVer ? ('?v=' + encodeURIComponent(pdfVer)) : ''));
      var nomeFile = pdfBase.split('/').pop() || 'perizia.pdf';
      return (
        '<tr>' +
          '<td><strong>' + esc(fmtData(r.data)) + '</strong></td>' +
          '<td>' + esc(r.proprietario) + '</td>' +
          '<td>' + esc(r.indirizzo) + '</td>' +
          '<td>' + esc(r.tipologia || '—') + '</td>' +
          '<td>' + esc(fmtEuro(r.valore_vendita)) + '</td>' +
          '<td class="perizie-actions">' +
            '<a class="btn btn-primary btn-sm" href="' + pdf + '" download="' + esc(nomeFile) + '" target="_blank" rel="noopener">⬇ Scarica PDF</a>' +
            '<a class="btn btn-secondary btn-sm" href="' + pdf + '" target="_blank" rel="noopener">👁 Anteprima</a>' +
          '</td>' +
        '</tr>'
      );
    }).join('');
  }

  function loadPerizie() {
    var el = document.getElementById('perizieTableBody');
    if (el) el.innerHTML = '<tr><td colspan="6" style="padding:24px;text-align:center;color:var(--caffe2)">Caricamento archivio…</td></tr>';

    fetch('data/perizie-index.json?v=13')
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .then(function (data) {
        perizieCache = (data && data.perizie) ? data.perizie.slice() : [];
        perizieCache.sort(function (a, b) {
          return String(b.data || '').localeCompare(String(a.data || ''));
        });
        renderPerizie();
      })
      .catch(function (err) {
        perizieCache = [];
        if (el) {
          el.innerHTML = '<tr><td colspan="6" style="padding:24px;text-align:center;color:var(--rosso)">Errore caricamento: ' + esc(err.message) + '</td></tr>';
        }
      });
  }

  window.loadPerizie = loadPerizie;
  window.perizieFilterList = function () {
    var inp = document.getElementById('perizieSearch');
    perizieFilter = inp ? inp.value : '';
    renderPerizie();
  };
})();
