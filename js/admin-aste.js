// ═══ SEZIONE ASTE IMMOBILIARI VENETO (admin) ═══
// Dati: tabella Supabase aste_immobili, alimentata da scripts/sync_aste.py
// (workflow .github/workflows/sync-aste.yml, 2 volte al giorno).

let asteRows = [];
let asteSort = { key: 'data_asta', dir: 1 };
let asteView = 'province';
let asteGeo = null;   // {prov: {checked:bool, open:bool, comuni:{comune:bool}}} null = non inizializzato
let asteGeoOpen = false;
let asteLoaded = false;

function asteFmtEur(v) {
  if (v === null || v === undefined || v === '') return '—';
  return Number(v).toLocaleString('it-IT', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });
}
function asteFmtDt(iso) {
  if (!iso) return '—';
  const d = new Date(iso);
  if (isNaN(d)) return '—';
  return d.toLocaleDateString('it-IT') + (iso.includes('T') && !iso.endsWith('T00:00') ? ' ' + d.toLocaleTimeString('it-IT', { hour: '2-digit', minute: '2-digit' }) : '');
}
function asteEsc(s) {
  return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
function asteDispLabel(d) {
  const t = (d || '').toUpperCase();
  if (t.includes('LIBER')) return '<span style="color:#27ae60;font-weight:600">libero</span>';
  if (t.includes('OCCUP')) return '<span style="color:#e67e22;font-weight:600">occupato</span>';
  return '<span style="color:var(--caffe2)">n.d.</span>';
}

async function asteLoad(force) {
  if (asteLoaded && !force) { asteRender(); return; }
  const body = document.getElementById('asteTableBody');
  if (body) body.innerHTML = '<tr><td colspan="8" style="padding:24px;text-align:center;color:var(--caffe2)">Caricamento…</td></tr>';
  try {
    const { data, error } = await sb.from('aste_immobili').select('*')
      .eq('attivo', true).order('data_asta', { ascending: true, nullsFirst: false }).limit(1000);
    if (error) throw error;
    asteRows = data || [];
    asteLoaded = true;
  } catch (e) {
    console.error('asteLoad', e);
    asteRows = [];
    if (body) body.innerHTML = '<tr><td colspan="8" style="padding:24px;text-align:center;color:#e74c3c">Errore di lettura. Se è il primo avvio: esegui sql/aste-immobili.sql in Supabase e poi il sync (GitHub Actions → Sync aste Veneto).</td></tr>';
    return;
  }
  asteRender();
}

function asteFiltered() {
  const q = (document.getElementById('asteSearch')?.value || '').toLowerCase().trim();
  const tipo = document.getElementById('asteTipo')?.value || '';
  const pmax = parseFloat(document.getElementById('astePrezzoMax')?.value || '') || null;
  const entro = document.getElementById('asteEntro')?.value || '';
  return asteRows.filter(r => {
    if (!asteGeoPass(r)) return false;
    if (tipo && (r.tipologia || 'altro') !== tipo) return false;
    if (pmax !== null && !(r.prezzo_base <= pmax)) return false;
    if (entro && r.data_asta && r.data_asta.slice(0, 10) > entro) return false;
    if (q) {
      const hay = [r.comune, r.indirizzo, r.descrizione, r.tribunale, r.procedura, r.tipologia, r.tipologia_bene].join(' ').toLowerCase();
      if (!hay.includes(q)) return false;
    }
    return true;
  }).sort((a, b) => {
    const k = asteSort.key;
    const va = a[k] ?? '', vb = b[k] ?? '';
    if (va === vb) return 0;
    return (va < vb ? -1 : 1) * asteSort.dir;
  });
}

function asteSortBy(key) {
  if (asteSort.key === key) asteSort.dir *= -1; else asteSort = { key, dir: 1 };
  asteRender();
}

// -------------------- tendina geo (province + comuni, multi-selezione) --------------------
function asteGeoInit() {
  if (asteGeo) return;
  asteGeo = {};
  asteRows.forEach(r => {
    const p = r.provincia || 'Altro';
    if (!asteGeo[p]) asteGeo[p] = { checked: true, open: false, comuni: {} };
    if (r.comune) asteGeo[p].comuni[r.comune] = true;
  });
}

function asteGeoPass(r) {
  asteGeoInit();
  const p = asteGeo[r.provincia || 'Altro'];
  if (!p) return true;
  if (!p.checked) return false;
  if (r.comune && p.comuni[r.comune] === false) return false;
  return true;
}

function asteGeoCounts() {
  const counts = {};
  asteRows.forEach(r => {
    const p = r.provincia || 'Altro';
    counts[p] = counts[p] || { tot: 0, comuni: {} };
    counts[p].tot++;
    if (r.comune) counts[p].comuni[r.comune] = (counts[p].comuni[r.comune] || 0) + 1;
  });
  return counts;
}

function asteGeoAllSelected() {
  asteGeoInit();
  return Object.values(asteGeo).every(p => p.checked && Object.values(p.comuni).every(Boolean));
}

function asteGeoLabel() {
  asteGeoInit();
  if (asteGeoAllSelected()) return 'Tutte le province';
  const provOn = Object.keys(asteGeo).filter(p => asteGeo[p].checked);
  if (!provOn.length) return 'Nessuna provincia';
  if (provOn.length === 1) {
    const p = provOn[0];
    const comOff = Object.keys(asteGeo[p].comuni).filter(c => !asteGeo[p].comuni[c]);
    return comOff.length ? p + ' (alcuni comuni)' : p;
  }
  return provOn.length + ' province';
}

function asteGeoToggle() {
  asteGeoOpen = !asteGeoOpen;
  asteRenderGeoDD();
}

function asteGeoToggleProvOpen(p) {
  asteGeoInit();
  asteGeo[p].open = !asteGeo[p].open;
  asteRenderGeoDD();
}

function asteGeoSetProv(p, v) {
  asteGeoInit();
  asteGeo[p].checked = v;
  if (v) Object.keys(asteGeo[p].comuni).forEach(c => asteGeo[p].comuni[c] = true);
  asteRenderGeoDD();
  asteRender();
}

function asteGeoSetComune(p, c, v) {
  asteGeoInit();
  asteGeo[p].comuni[c] = v;
  if (!v) asteGeo[p].checked = true;  // la provincia resta attiva ma con comuni esclusi
  asteRenderGeoDD();
  asteRender();
}

function asteGeoSetAll(v) {
  asteGeoInit();
  Object.values(asteGeo).forEach(p => {
    p.checked = v;
    Object.keys(p.comuni).forEach(c => p.comuni[c] = v);
  });
  asteRenderGeoDD();
  asteRender();
}

function asteRenderGeoDD() {
  const wrap = document.getElementById('asteGeoDD');
  if (!wrap) return;
  asteGeoInit();
  const counts = asteGeoCounts();
  const cb = (on) => `<span style="display:inline-block;width:16px;height:16px;border:1.5px solid ${on ? 'var(--nero)' : 'var(--caffe3)'};border-radius:4px;background:${on ? 'var(--nero)' : '#fff'};color:#fff;font-size:11px;line-height:16px;text-align:center;flex:none">${on ? '✓' : ''}</span>`;
  let panel = '';
  if (asteGeoOpen) {
    const provRows = asteProvOrder(counts).map(p => {
      const g = asteGeo[p];
      const comList = Object.keys(g.comuni).sort().map(c =>
        `<label style="display:inline-flex;align-items:center;gap:5px;padding:5px 9px;margin:2px;border:1px solid var(--caffe3);border-radius:14px;font-size:.74rem;cursor:pointer;background:${g.comuni[c] ? 'var(--sfondo)' : '#fff'}">
          <input type="checkbox" ${g.comuni[c] ? 'checked' : ''} onchange="asteGeoSetComune('${asteEsc(p)}','${asteEsc(c)}',this.checked)" style="margin:0">${asteEsc(c)} <span style="color:var(--caffe2)">${counts[p].comuni[c]}</span>
        </label>`).join('');
      return `<div style="border-bottom:1px solid var(--caffe3);padding:8px 12px">
        <div style="display:flex;align-items:center;gap:8px;cursor:pointer" onclick="asteGeoSetProv('${asteEsc(p)}',${!g.checked})">${cb(g.checked)}<strong style="font-size:.84rem">${asteEsc(p)}</strong><span style="color:var(--caffe2);font-size:.76rem">${counts[p].tot} aste</span>
          <button type="button" onclick="event.stopPropagation();asteGeoToggleProvOpen('${asteEsc(p)}')" style="margin-left:auto;background:none;border:none;color:var(--nero);cursor:pointer;font-size:.8rem">${g.open ? '▴ comuni' : '▾ comuni'}</button></div>
        ${g.open ? `<div style="padding:6px 0 2px 24px;line-height:1.2">${comList || '<span style="font-size:.75rem;color:var(--caffe2)">nessun comune</span>'}</div>` : ''}
      </div>`;
    }).join('');
    panel = `<div style="position:absolute;top:calc(100% + 6px);left:0;z-index:60;background:#fff;color:var(--testo);border:1px solid var(--caffe3);border-radius:12px;box-shadow:0 12px 40px rgba(30,58,92,.18);width:min(420px,88vw);max-height:60vh;overflow-y:auto">
      <div style="display:flex;gap:10px;padding:10px 12px;border-bottom:1px solid var(--caffe3);position:sticky;top:0;background:#fff;border-radius:12px 12px 0 0">
        <button type="button" onclick="asteGeoSetAll(true)" style="background:none;border:none;color:var(--nero);font-size:.76rem;cursor:pointer;text-decoration:underline">Seleziona tutto</button>
        <button type="button" onclick="asteGeoSetAll(false)" style="background:none;border:none;color:var(--nero);font-size:.76rem;cursor:pointer;text-decoration:underline">Deseleziona tutto</button>
        <button type="button" onclick="asteGeoToggle()" style="margin-left:auto;background:var(--nero);color:#fff;border:none;border-radius:6px;padding:3px 12px;font-size:.76rem;cursor:pointer">Fatto</button>
      </div>
      ${provRows}
    </div>`;
  }
  wrap.innerHTML = `<button type="button" onclick="asteGeoToggle()" style="padding:8px 14px;border-radius:8px;border:1.5px solid var(--caffe3);background:#fff;font-size:.82rem;cursor:pointer;white-space:nowrap">🗺 ${asteEsc(asteGeoLabel())} ▾</button>` + panel;
}

function asteProvOrder(counts) {
  const prio = ['Padova', 'Vicenza', 'Treviso'];
  const rest = Object.keys(counts).filter(p => !prio.includes(p))
    .sort((a, b) => counts[b] - counts[a] || a.localeCompare(b));
  return prio.filter(p => counts[p]).concat(rest);
}

function asteChipProv(p) {
  asteGeoInit();
  if (!p) { asteGeoSetAll(true); return; }
  Object.keys(asteGeo).forEach(k => {
    asteGeo[k].checked = (k === p);
    Object.keys(asteGeo[k].comuni).forEach(c => asteGeo[k].comuni[c] = (k === p));
  });
  asteRender();
}

function asteSetView(v) {
  asteView = v;
  asteRender();
}

function asteRenderChips() {
  const wrap = document.getElementById('asteProvChips');
  if (!wrap) return;
  const counts = {};
  asteRows.forEach(r => { if (r.provincia) counts[r.provincia] = (counts[r.provincia] || 0) + 1; });
  asteGeoInit();
  const allSel = asteGeoAllSelected();
  const onlyProv = Object.keys(asteGeo).filter(p => asteGeo[p].checked && Object.values(asteGeo[p].comuni).every(Boolean));
  const cur = allSel ? '' : (onlyProv.length === 1 && Object.values(asteGeo).filter(p => p.checked).length === 1 ? onlyProv[0] : '?');
  const chip = (label, val, n) => {
    const on = cur === val;
    return `<button type="button" onclick="asteChipProv('${val}')" style="padding:6px 14px;border-radius:20px;border:1.5px solid ${on ? 'var(--nero)' : 'var(--caffe3)'};background:${on ? 'var(--nero)' : '#fff'};color:${on ? '#fff' : 'var(--testo)'};font-size:.78rem;font-weight:${on ? '700' : '500'};cursor:pointer">${asteEsc(label)} <span style="opacity:.75">(${n})</span></button>`;
  };
  const chips = [chip('Tutte', '', asteRows.length)]
    .concat(asteProvOrder(counts).map(p => chip(p, p, counts[p])));
  const btn = (v, label) => {
    const on = asteView === v;
    return `<button type="button" onclick="asteSetView('${v}')" style="padding:6px 12px;border:1.5px solid ${on ? 'var(--nero)' : 'var(--caffe3)'};background:${on ? 'var(--nero)' : '#fff'};color:${on ? '#fff' : 'var(--testo)'};font-size:.76rem;cursor:pointer;${v === 'province' ? 'border-radius:8px 0 0 8px' : 'border-radius:0 8px 8px 0;border-left:none'}">${label}</button>`;
  };
  wrap.innerHTML = chips.join('')
    + `<span style="margin-left:auto;display:inline-flex">${btn('province', '▦ Per provincia')}${btn('flat', '☰ Elenco unico')}</span>`;
}

function asteRowHtml(r) {
  const id = r.id;
  const docs = (r.documenti || []).map(d =>
    `<a href="${asteEsc(d.url)}" target="_blank" rel="noopener" style="display:inline-block;margin:2px 6px 2px 0;padding:4px 10px;background:var(--sfondo);border:1px solid var(--caffe3);border-radius:6px;font-size:.75rem">📄 ${asteEsc(d.tipo || d.nome)}</a>`).join('');
  const foto = r.foto_url ? `<img src="${asteEsc(r.foto_url)}" alt="" loading="lazy" style="max-width:220px;border-radius:8px;border:1px solid var(--caffe3)">` : '<span style="color:var(--caffe2);font-size:.78rem">Foto non disponibile</span>';
  return `<tr style="border-bottom:1px solid var(--caffe3);cursor:pointer" onclick="asteToggle('${id}')">
    <td style="padding:10px 12px">${r.foto_url ? `<img src="${asteEsc(r.foto_url)}" alt="" loading="lazy" style="width:64px;height:48px;object-fit:cover;border-radius:6px">` : '🏠'}</td>
    <td style="padding:10px 12px"><strong>${asteEsc(r.comune)}</strong> <span style="color:var(--caffe2)">(${asteEsc(r.provincia)})</span><br><span style="font-size:.76rem;color:var(--caffe2)">${asteEsc(r.indirizzo)}</span></td>
    <td style="padding:10px 12px;white-space:nowrap">${asteEsc(r.tipologia || 'altro')}</td>
    <td style="padding:10px 12px;white-space:nowrap"><strong>${asteFmtEur(r.prezzo_base)}</strong><br><span style="font-size:.74rem;color:var(--caffe2)">off. min ${asteFmtEur(r.offerta_minima)}</span></td>
    <td style="padding:10px 12px;white-space:nowrap">${asteFmtDt(r.data_asta)}<br><span style="font-size:.74rem;color:var(--caffe2)">offerte entro ${asteFmtDt(r.termine_offerte)}</span></td>
    <td style="padding:10px 12px">${asteDispLabel(r.disponibilita)}</td>
    <td style="padding:10px 12px;font-size:.78rem">${asteEsc(r.tribunale)}<br><span style="color:var(--caffe2)">proc. ${asteEsc(r.procedura)}</span></td>
    <td style="padding:10px 12px"><button class="btn btn-secondary btn-sm">▾</button></td>
  </tr>
  <tr id="asteDet-${id}" style="display:none;background:#faf9f7">
    <td colspan="8" style="padding:16px 20px">
      <div style="display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start">
        <div>${foto}</div>
        <div style="flex:1;min-width:280px">
          <p style="font-size:.85rem;line-height:1.6;margin:0 0 10px">${asteEsc(r.descrizione)}</p>
          <p style="font-size:.76rem;color:var(--caffe2);margin:0 0 10px">${asteEsc(r.tipologia_bene)} · ${asteEsc(r.modalita_vendita)}</p>
          <div style="margin-bottom:10px">${docs || '<span style="font-size:.78rem;color:var(--caffe2)">Nessun documento</span>'}</div>
          <a href="${asteEsc(r.link_dettaglio)}" target="_blank" rel="noopener" class="btn btn-primary btn-sm">Apri scheda ufficiale ↗</a>
          <div style="margin-top:12px">
            <label style="font-size:.72rem;color:var(--caffe2)">Note private</label>
            <div style="display:flex;gap:8px;margin-top:4px">
              <input type="text" id="asteNote-${id}" value="${asteEsc(r.note_admin)}" placeholder="Es. interessante, da visitare…" style="flex:1;padding:7px 10px;border:1px solid var(--caffe3);border-radius:6px;font-size:.82rem">
              <button class="btn btn-secondary btn-sm" onclick="asteSaveNote('${id}')">Salva</button>
            </div>
          </div>
        </div>
      </div>
    </td>
  </tr>`;
}

function asteRender() {
  const rows = asteFiltered();
  const soon = asteRows.filter(r => r.data_asta && (new Date(r.data_asta) - Date.now()) / 864e5 <= 7 && (new Date(r.data_asta) - Date.now()) >= 0).length;
  const el = id => document.getElementById(id);
  if (el('statAsteTot')) el('statAsteTot').textContent = asteRows.length;
  if (el('statAsteWeek')) el('statAsteWeek').textContent = soon;
  if (el('statAsteDocs')) el('statAsteDocs').textContent = asteRows.filter(r => (r.documenti || []).length > 0).length;
  if (el('statAsteFoto')) el('statAsteFoto').textContent = asteRows.filter(r => r.foto_url).length;
  const tipi = [...new Set(asteRows.map(r => r.tipologia || 'altro'))].sort();
  const selT = el('asteTipo');
  if (selT && selT.options.length <= 1) tipi.forEach(t => { const o = document.createElement('option'); o.value = t; o.textContent = t; selT.appendChild(o); });
  asteRenderChips();
  asteRenderGeoDD();

  const body = el('asteTableBody');
  if (!body) return;
  if (!rows.length) {
    body.innerHTML = '<tr><td colspan="8" style="padding:24px;text-align:center;color:var(--caffe2)">Nessuna asta trovata con questi filtri.</td></tr>';
    return;
  }
  if (asteView === 'flat') {
    body.innerHTML = rows.map(asteRowHtml).join('');
    return;
  }
  const groups = {};
  rows.forEach(r => { const k = r.provincia || 'Altro'; (groups[k] = groups[k] || []).push(r); });
  body.innerHTML = asteProvOrder(groups).map(prov => {
    const head = `<tr><td colspan="8" style="padding:10px 16px;background:linear-gradient(90deg,var(--sfondo),#fff);border-top:2px solid var(--caffe3);font-weight:700;font-size:.85rem;letter-spacing:.3px">📍 ${asteEsc(prov.toUpperCase())} <span style="color:var(--caffe2);font-weight:500">— ${groups[prov].length} aste</span></td></tr>`;
    return head + groups[prov].map(asteRowHtml).join('');
  }).join('');
}

function asteToggle(id) {
  const el = document.getElementById('asteDet-' + id);
  if (el) el.style.display = el.style.display === 'none' ? '' : 'none';
}

async function asteSaveNote(id) {
  const v = document.getElementById('asteNote-' + id)?.value || '';
  const { error } = await sb.from('aste_immobili').update({ note_admin: v, updated_at: new Date().toISOString() }).eq('id', id);
  if (error) { toast('Errore salvataggio nota', 'error'); return; }
  const r = asteRows.find(x => x.id === id);
  if (r) r.note_admin = v;
  toast('Nota salvata', 'success');
}
