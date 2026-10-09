/* Pannello Base di conoscenza Linda — vanilla, Supabase Auth + RLS (kb_is_admin). */
(function () {
  'use strict';
  var SUPABASE_URL = 'https://qwkwkemuabfwvwuqrxlu.supabase.co';
  var SUPABASE_ANON = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3a3drZW11YWJmd3Z3dXFyeGx1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE1OTk5NjEsImV4cCI6MjA4NzE3NTk2MX0.JxEYiWVPEOiwjZtbWAZRlMUdKXcupjw7filvrERCiqc';
  var CATEGORIE = ['azienda', 'servizi', 'vendita', 'affitto', 'acquisto', 'documenti', 'fiscale', 'mutui', 'territorio', 'procedure', 'notizie', 'immobili', 'blog'];
  var STATI = { bozza: 'Bozza', da_verificare: 'Da verificare', approvata: 'Approvata', scaduta: 'Scaduta' };

  var sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON, { auth: { persistSession: true, autoRefreshToken: true } });
  var $ = function (id) { return document.getElementById(id); };
  var voci = [];
  var csvRows = [];

  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function norm(s) { return String(s || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9 ]/g, '').replace(/\s+/g, ' ').trim(); }
  function dt(s) { return s ? new Date(s).toLocaleDateString('it-IT') : ''; }

  // ---------- accesso ----------
  async function mostra() {
    var s = await sb.auth.getSession();
    var user = s.data && s.data.session && s.data.session.user;
    $('login').hidden = !!user; $('app').hidden = true; $('esci').hidden = !user;
    if (!user) return;
    var a = await sb.rpc('kb_is_admin');
    if (a.error || a.data !== true) {
      $('login').hidden = false; $('loginErr').textContent = 'Account non abilitato come amministratore della base di conoscenza.';
      await sb.auth.signOut(); $('esci').hidden = true; return;
    }
    $('utente').textContent = user.email; $('login').hidden = true; $('app').hidden = false;
    caricaVoci();
  }
  $('loginForm').addEventListener('submit', async function (e) {
    e.preventDefault(); $('loginErr').textContent = '';
    var r = await sb.auth.signInWithPassword({ email: $('em').value.trim(), password: $('pw').value });
    if (r.error) { $('loginErr').textContent = 'Credenziali non valide.'; return; }
    $('pw').value = ''; mostra();
  });
  $('esci').addEventListener('click', async function () { await sb.auth.signOut(); location.reload(); });

  // ---------- schede ----------
  document.querySelectorAll('.tabs button').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('.tabs button').forEach(function (x) { x.setAttribute('aria-selected', x === b ? 'true' : 'false'); });
      ['voci', 'lacune', 'csv', 'prova'].forEach(function (t) { $('t-' + t).hidden = (t !== b.getAttribute('data-t')); });
      if (b.getAttribute('data-t') === 'lacune') caricaLacune();
    });
  });

  // ---------- elenco voci ----------
  async function caricaVoci() {
    $('vociMsg').textContent = 'Caricamento…';
    var q = sb.from('kb_entries').select('id,categoria,domanda,stato,scade_il,updated_at,versione').order('updated_at', { ascending: false }).limit(500);
    if ($('fStato').value) q = q.eq('stato', $('fStato').value);
    var r = await q;
    if (r.error) { $('vociMsg').innerHTML = '<span class="err">Errore: ' + esc(r.error.message) + '</span>'; return; }
    voci = r.data || [];
    disegna();
  }
  function disegna() {
    var t = norm($('fCerca').value);
    var rows = voci.filter(function (v) { return !t || norm(v.domanda).indexOf(t) >= 0; });
    $('vociMsg').textContent = rows.length + ' voci' + (rows.length ? '' : ' — crea la prima con «Nuova voce» o importa un CSV.');
    $('vociBody').innerHTML = rows.map(function (v) {
      var scaduta = v.scade_il && new Date(v.scade_il) < new Date(new Date().toDateString());
      return '<tr><td><button type="button" class="lnk" data-id="' + esc(v.id) + '" style="border:0;text-align:left;font-weight:600;min-height:44px">' + esc(v.domanda) + '</button></td>' +
        '<td><span class="badge b-' + esc(v.stato) + '">' + esc(STATI[v.stato] || v.stato) + '</span>' + (scaduta ? ' ⚠️' : '') + '</td>' +
        '<td>' + esc(v.categoria) + '</td><td>' + esc(v.scade_il || '') + '</td><td>' + esc(dt(v.updated_at)) + '</td></tr>';
    }).join('');
  }
  $('fStato').addEventListener('change', caricaVoci);
  $('fCerca').addEventListener('input', disegna);
  $('vociBody').addEventListener('click', function (e) {
    var b = e.target.closest('button[data-id]'); if (b) apri(b.getAttribute('data-id'));
  });

  // ---------- editor ----------
  $('vCat').innerHTML = CATEGORIE.map(function (c) { return '<option>' + c + '</option>'; }).join('');
  function pulisciEditor(v) {
    v = v || {};
    $('vId').value = v.id || ''; $('vDom').value = v.domanda || ''; $('vVar').value = (v.varianti || []).join('\n');
    $('vRis').value = v.risposta || ''; $('vCat').value = v.categoria || 'azienda'; $('vScad').value = v.scade_il || '';
    $('vCond').value = v.condizioni || '';
    var f = (v.fonti && v.fonti[0]) || {}; $('vFt').value = f.titolo || ''; $('vFu').value = f.url || '';
    $('vErr').textContent = ''; $('vPrev').hidden = true; $('vStoria').hidden = true;
    $('dlgTit').textContent = v.id ? 'Modifica voce (' + (STATI[v.stato] || '') + ', v' + v.versione + ')' : 'Nuova voce';
    ['bScade', 'bStoria', 'bDel'].forEach(function (id) { $(id).hidden = !v.id; });
  }
  async function apri(id) {
    var r = await sb.from('kb_entries').select('*').eq('id', id).single();
    if (r.error) { alert(r.error.message); return; }
    pulisciEditor(r.data); $('dlg').showModal();
  }
  $('nuova').addEventListener('click', function () { pulisciEditor(); $('dlg').showModal(); });
  $('bChiudi').addEventListener('click', function () { $('dlg').close(); });

  function leggiForm(stato) {
    var url = $('vFu').value.trim();
    if (url && !/^https:\/\//i.test(url)) throw new Error('La fonte deve essere un URL https://');
    if (/\d\s*%/.test($('vRis').value) && /mediazion|provvigion|commission/i.test($('vRis').value))
      throw new Error('Non pubblicare percentuali o tariffe di mediazione: «da concordare in sede».');
    var fonti = ($('vFt').value.trim() || url) ? [{ titolo: $('vFt').value.trim() || 'Fonte', url: url || null }] : [];
    if (stato === 'approvata' && /\d/.test($('vRis').value) && !fonti.length)
      throw new Error('La risposta contiene dati numerici: indica una fonte verificabile prima di approvare.');
    return {
      domanda: $('vDom').value.trim(), varianti: $('vVar').value.split('\n').map(function (s) { return s.trim(); }).filter(Boolean),
      risposta: $('vRis').value.trim(), categoria: $('vCat').value, scade_il: $('vScad').value || null,
      condizioni: $('vCond').value.trim() || null, fonti: fonti, stato: stato
    };
  }
  async function salva(stato) {
    $('vErr').textContent = '';
    try {
      if (!$('vForm').reportValidity()) return;
      var row = leggiForm(stato), id = $('vId').value, r;
      if (id) r = await sb.from('kb_entries').update(row).eq('id', id).select().single();
      else { row.origine = 'manuale'; r = await sb.from('kb_entries').insert(row).select().single(); }
      if (r.error) throw new Error(r.error.message);
      $('dlg').close(); caricaVoci();
    } catch (e) { $('vErr').textContent = e.message; }
  }
  $('bBozza').addEventListener('click', function () { salva('bozza'); });
  $('bVerifica').addEventListener('click', function () { salva('da_verificare'); });
  $('bApprova').addEventListener('click', function () { salva('approvata'); });
  $('bScade').addEventListener('click', async function () {
    var r = await sb.from('kb_entries').update({ stato: 'scaduta' }).eq('id', $('vId').value);
    if (r.error) { $('vErr').textContent = r.error.message; return; } $('dlg').close(); caricaVoci();
  });
  $('bDel').addEventListener('click', async function () {
    if (!confirm('Eliminare definitivamente la voce? (resta in cronologia)')) return;
    var r = await sb.from('kb_entries').delete().eq('id', $('vId').value);
    if (r.error) { $('vErr').textContent = r.error.message; return; } $('dlg').close(); caricaVoci();
  });
  $('bPrev').addEventListener('click', function () {
    try {
      var row = leggiForm('bozza');
      var txt = window.LindaKB ? window.LindaKB.formatKb({ risposta: row.risposta, condizioni: row.condizioni, fonti: row.fonti, aggiornata_il: new Date().toISOString() }) : row.risposta;
      $('vPrev').textContent = txt.replace(/\*\*/g, '').replace(/\*/g, '').replace(/\[([^\]]+)\]\(([^)]+)\)/g, '$1 ($2)'); $('vPrev').hidden = false; $('vErr').textContent = '';
    } catch (e) { $('vErr').textContent = e.message; }
  });
  $('bStoria').addEventListener('click', async function () {
    var r = await sb.from('kb_history').select('id,azione,quando,snapshot').eq('entry_id', $('vId').value).order('quando', { ascending: false }).limit(20);
    var box = $('vStoria'); box.hidden = false;
    if (r.error) { box.innerHTML = '<p class="err">' + esc(r.error.message) + '</p>'; return; }
    box.innerHTML = '<h3>Versioni precedenti</h3>' + ((r.data || []).map(function (h) {
      return '<p><b>' + esc(dt(h.quando)) + '</b> — ' + esc(h.azione) + ' — «' + esc(String(h.snapshot.risposta || '').slice(0, 90)) + '…» <button type="button" data-h="' + h.id + '">Ripristina (da verificare)</button></p>';
    }).join('') || '<p class="hint">Nessuna modifica precedente.</p>');
  });
  $('vStoria').addEventListener('click', async function (e) {
    var b = e.target.closest('button[data-h]'); if (!b) return;
    var r = await sb.rpc('kb_restore', { p_history_id: Number(b.getAttribute('data-h')) });
    if (r.error) { $('vErr').textContent = r.error.message; return; } $('dlg').close(); caricaVoci();
  });

  // ---------- lacune ----------
  async function caricaLacune() {
    $('lacMsg').textContent = 'Caricamento…';
    var r = await sb.from('linda_lacune').select('*').limit(100);
    if (r.error) { $('lacMsg').innerHTML = '<span class="err">' + esc(r.error.message) + '</span>'; return; }
    $('lacMsg').textContent = (r.data || []).length + ' gruppi di domande senza risposta';
    $('lacBody').innerHTML = (r.data || []).map(function (g, i) {
      return '<tr><td>' + esc(g.esempio) + '</td><td>' + g.volte + (g.giudicate_inutili ? ' (' + g.giudicate_inutili + ' 👎)' : '') + '</td><td>' + esc(dt(g.ultima)) +
        '</td><td><button type="button" data-l="' + i + '">Crea risposta</button></td></tr>';
    }).join('');
    $('lacBody').onclick = function (e) {
      var b = e.target.closest('button[data-l]'); if (!b) return;
      pulisciEditor({ domanda: r.data[Number(b.getAttribute('data-l'))].esempio }); $('dlg').showModal();
    };
  }

  // ---------- CSV ----------
  function parseCsv(txt) {
    var rows = [], row = [], cur = '', q = false;
    txt = txt.replace(/^\uFEFF/, '');
    for (var i = 0; i < txt.length; i++) {
      var c = txt[i];
      if (q) { if (c === '"') { if (txt[i + 1] === '"') { cur += '"'; i++; } else q = false; } else cur += c; }
      else if (c === '"') q = true;
      else if (c === ';') { row.push(cur); cur = ''; }
      else if (c === '\n' || c === '\r') { if (c === '\r' && txt[i + 1] === '\n') i++; row.push(cur); rows.push(row); row = []; cur = ''; }
      else cur += c;
    }
    if (cur || row.length) { row.push(cur); rows.push(row); }
    return rows.filter(function (r) { return r.some(function (x) { return x.trim(); }); });
  }
  $('csvFile').addEventListener('change', async function () {
    var f = this.files[0]; csvRows = []; $('csvGo').hidden = true; if (!f) return;
    var rows = parseCsv(await f.text()), head = rows.shift().map(function (h) { return h.trim().toLowerCase(); });
    var idx = function (n) { return head.indexOf(n); };
    if (idx('domanda') < 0 || idx('risposta') < 0) { $('csvMsg').innerHTML = '<span class="err">Servono almeno le colonne «domanda» e «risposta».</span>'; return; }
    var esist = {}; (voci || []).forEach(function (v) { esist[norm(v.domanda)] = 1; });
    var ok = 0, dup = 0, inv = 0;
    rows.forEach(function (r) {
      var g = function (n) { return idx(n) >= 0 ? (r[idx(n)] || '').trim() : ''; };
      var dom = g('domanda'), ris = g('risposta'), cat = g('categoria') || 'azienda', url = g('fonte_url');
      if (dom.length < 5 || dom.length > 300 || ris.length < 10 || ris.length > 2500 || CATEGORIE.indexOf(cat) < 0 || (url && !/^https:\/\//i.test(url))) { inv++; return; }
      if (esist[norm(dom)]) { dup++; return; }
      esist[norm(dom)] = 1; ok++;
      csvRows.push({ domanda: dom, varianti: g('varianti').split('|').map(function (s) { return s.trim(); }).filter(Boolean), risposta: ris, categoria: cat,
        fonti: (g('fonte_titolo') || url) ? [{ titolo: g('fonte_titolo') || 'Fonte', url: url || null }] : [], scade_il: g('scade_il') || null, stato: 'da_verificare', origine: 'csv' });
    });
    $('csvMsg').textContent = ok + ' da importare · ' + dup + ' duplicate saltate · ' + inv + ' non valide (domanda/risposta troppo corte, categoria o URL errati)';
    $('csvGo').hidden = !ok;
  });
  $('csvGo').addEventListener('click', async function () {
    var r = await sb.from('kb_entries').insert(csvRows);
    if (r.error) { $('csvMsg').innerHTML = '<span class="err">' + esc(r.error.message) + '</span>'; return; }
    $('csvMsg').innerHTML = '<span class="okmsg">Importate ' + csvRows.length + ' voci in «Da verificare».</span>'; csvRows = []; $('csvGo').hidden = true; caricaVoci();
  });
  $('csvExp').addEventListener('click', async function () {
    var r = await sb.from('kb_entries').select('domanda,varianti,risposta,categoria,fonti,scade_il').eq('stato', 'approvata');
    if (r.error) { alert(r.error.message); return; }
    var q = function (s) { s = String(s == null ? '' : s); return /[;"\n\r]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };
    var out = ['domanda;varianti;risposta;categoria;fonte_titolo;fonte_url;scade_il'].concat((r.data || []).map(function (v) {
      var f = (v.fonti && v.fonti[0]) || {};
      return [v.domanda, (v.varianti || []).join('|'), v.risposta, v.categoria, f.titolo || '', f.url || '', v.scade_il || ''].map(q).join(';');
    })).join('\r\n');
    var a = document.createElement('a'); a.href = URL.createObjectURL(new Blob(['\uFEFF' + out], { type: 'text/csv' })); a.download = 'linda-kb-approvate.csv'; a.click();
  });

  // ---------- prova ----------
  $('provaGo').addEventListener('click', async function () {
    var out = $('provaOut'); out.hidden = false; out.textContent = '…';
    var r = await sb.rpc('linda_kb_search', { p_q: $('provaQ').value, p_lim: 3 });
    if (r.error) { out.textContent = 'Errore: ' + r.error.message; return; }
    var best = (r.data || [])[0];
    if (!best) { out.textContent = 'Nessuna voce approvata trova corrispondenza. Linda userebbe le regole storiche o direbbe di non sapere.'; return; }
    out.textContent = (best.score >= 0.45 ? 'RISPONDEREBBE (score ' : 'NON risponderebbe, sotto soglia (score ') + best.score.toFixed(2) + ')\n\n' + best.risposta;
  });

  mostra();
})();
