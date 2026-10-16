// ═══ SEZIONE ASTE IMMOBILIARI VENETO (admin) ═══
// Dati: tabella Supabase aste_immobili, alimentata da scripts/sync_aste.py
// (workflow .github/workflows/sync-aste.yml, 2 volte al giorno).

let asteRows = [];
let asteSort = { key: 'data_asta', dir: 1 };
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
  if (body) body.innerHTML = '<tr><td colspan="7" style="padding:24px;text-align:center;color:var(--caffe2)">Caricamento…</td></tr>';
  try {
    const { data, error } = await sb.from('aste_immobili').select('*')
      .eq('attivo', true).order('data_asta', { ascending: true, nullsFirst: false }).limit(1000);
    if (error) throw error;
    asteRows = data || [];
    asteLoaded = true;
  } catch (e) {
    console.error('asteLoad', e);
    asteRows = [];
    if (body) body.innerHTML = '<tr><td colspan="7" style="padding:24px;text-align:center;color:#e74c3c">Errore di lettura. Se è il primo avvio: esegui sql/aste-immobili.sql in Supabase e poi il sync (GitHub Actions → Sync aste Veneto).</td></tr>';
    return;
  }
  asteRender();
}

function asteFiltered() {
  const q = (document.getElementById('asteSearch')?.value || '').toLowerCase().trim();
  const prov = document.getElementById('asteProv')?.value || '';
  const pmax = parseFloat(document.getElementById('astePrezzoMax')?.value || '') || null;
  const entro = document.getElementById('asteEntro')?.value || '';
  return asteRows.filter(r => {
    if (prov && r.provincia !== prov) return false;
    if (pmax !== null && !(r.prezzo_base <= pmax)) return false;
    if (entro && r.data_asta && r.data_asta.slice(0, 10) > entro) return false;
    if (q) {
      const hay = [r.comune, r.indirizzo, r.descrizione, r.tribunale, r.procedura, r.tipologia_bene].join(' ').toLowerCase();
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

function asteRender() {
  const rows = asteFiltered();
  const soon = asteRows.filter(r => r.data_asta && (new Date(r.data_asta) - Date.now()) / 864e5 <= 7 && (new Date(r.data_asta) - Date.now()) >= 0).length;
  const provs = [...new Set(asteRows.map(r => r.provincia).filter(Boolean))].sort();
  const el = id => document.getElementById(id);
  if (el('statAsteTot')) el('statAsteTot').textContent = asteRows.length;
  if (el('statAsteWeek')) el('statAsteWeek').textContent = soon;
  if (el('statAsteDocs')) el('statAsteDocs').textContent = asteRows.filter(r => (r.documenti || []).length > 0).length;
  if (el('statAsteFoto')) el('statAsteFoto').textContent = asteRows.filter(r => r.foto_url).length;
  const sel = el('asteProv');
  if (sel && sel.options.length <= 1) provs.forEach(p => { const o = document.createElement('option'); o.value = p; o.textContent = p; sel.appendChild(o); });

  const body = el('asteTableBody');
  if (!body) return;
  if (!rows.length) {
    body.innerHTML = '<tr><td colspan="7" style="padding:24px;text-align:center;color:var(--caffe2)">Nessuna asta trovata con questi filtri.</td></tr>';
    return;
  }
  body.innerHTML = rows.map(r => {
    const id = r.id;
    const docs = (r.documenti || []).map(d =>
      `<a href="${asteEsc(d.url)}" target="_blank" rel="noopener" style="display:inline-block;margin:2px 6px 2px 0;padding:4px 10px;background:var(--sfondo);border:1px solid var(--caffe3);border-radius:6px;font-size:.75rem">📄 ${asteEsc(d.tipo || d.nome)}</a>`).join('');
    const foto = r.foto_url ? `<img src="${asteEsc(r.foto_url)}" alt="" loading="lazy" style="max-width:220px;border-radius:8px;border:1px solid var(--caffe3)">` : '<span style="color:var(--caffe2);font-size:.78rem">Foto non disponibile</span>';
    return `<tr style="border-bottom:1px solid var(--caffe3);cursor:pointer" onclick="asteToggle('${id}')">
      <td style="padding:10px 12px">${r.foto_url ? `<img src="${asteEsc(r.foto_url)}" alt="" loading="lazy" style="width:64px;height:48px;object-fit:cover;border-radius:6px">` : '🏠'}</td>
      <td style="padding:10px 12px"><strong>${asteEsc(r.comune)}</strong> <span style="color:var(--caffe2)">(${asteEsc(r.provincia)})</span><br><span style="font-size:.76rem;color:var(--caffe2)">${asteEsc(r.indirizzo)}</span></td>
      <td style="padding:10px 12px;white-space:nowrap"><strong>${asteFmtEur(r.prezzo_base)}</strong><br><span style="font-size:.74rem;color:var(--caffe2)">off. min ${asteFmtEur(r.offerta_minima)}</span></td>
      <td style="padding:10px 12px;white-space:nowrap">${asteFmtDt(r.data_asta)}<br><span style="font-size:.74rem;color:var(--caffe2)">offerte entro ${asteFmtDt(r.termine_offerte)}</span></td>
      <td style="padding:10px 12px">${asteDispLabel(r.disponibilita)}</td>
      <td style="padding:10px 12px;font-size:.78rem">${asteEsc(r.tribunale)}<br><span style="color:var(--caffe2)">proc. ${asteEsc(r.procedura)}</span></td>
      <td style="padding:10px 12px"><button class="btn btn-secondary btn-sm">▾</button></td>
    </tr>
    <tr id="asteDet-${id}" style="display:none;background:#faf9f7">
      <td colspan="7" style="padding:16px 20px">
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
