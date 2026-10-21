// ═══ SEZIONE ASTE IMMOBILIARI VENETO (admin) ═══
// Dati: tabella Supabase aste_immobili, alimentata da scripts/sync_aste.py
// (workflow .github/workflows/sync-aste.yml, 2 volte al giorno).

let asteRows = [];
let asteSort = { key: 'data_asta', dir: 1 };
let asteView = 'province';
let asteGeo = null;   // {prov: {checked:bool, open:bool, comuni:{comune:bool}}} null = non inizializzato
let asteGeoOpen = false;
let asteLoaded = false;
let asteShowScartate = false;

(function asteInjectCss() {
  if (document.getElementById('asteCss')) return;
  const st = document.createElement('style');
  st.id = 'asteCss';
  st.textContent = `.aste-m{display:none}
  @media (max-width:700px){
    .aste-m{display:block;margin-top:8px}
    .aste-m-date{display:inline-block;background:#3A5578;color:#fff;font-weight:800;font-size:.98rem;padding:5px 9px;border-radius:8px;margin-bottom:6px}
    .aste-m select{display:block;width:100%;margin-top:4px}
    .aste-m-info{display:block;font-size:.74rem;color:var(--caffe2);margin-top:4px}
    .aste-c-tipo,.aste-c-data,.aste-c-stato,.aste-c-trib,.aste-c-val{display:none}
  }`;
  document.head.appendChild(st);
})();

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

function asteFmtMila(v) {
  return Math.round(Number(v) / 1000).toLocaleString('it-IT');
}
// Stima di vendita in rosso: compilata da Gianna dopo ogni import, solo provincia di Padova.
function asteStimaHtml(r) {
  if (!r.prezzo_stimato_min || !r.prezzo_stimato_max) return '';
  const fonte = r.prezzo_stimato_fonte || 'Immobiliare.it, prezzi richiesti (non compravendite)';
  const dt = r.prezzo_stimato_data ? new Date(r.prezzo_stimato_data).toLocaleDateString('it-IT') : '';
  const tip = 'Stima interna da verificare, non una perizia. Fonte: ' + fonte + (dt ? ' · agg. ' + dt : '');
  return '<br><span title="' + asteEsc(tip) + '" style="display:inline-block;margin-top:3px;font-size:.8rem;font-weight:800;color:#b00020;cursor:help">stima vendita \u20AC ' + asteFmtMila(r.prezzo_stimato_min) + '\u2013' + asteFmtMila(r.prezzo_stimato_max) + ' mila</span>';
}

function asteVotoHtml(r) {
  if (r.voto === null || r.voto === undefined || r.voto === '') return '';
  const v = Number(r.voto);
  if (!v) return '';
  const col = v >= 7 ? '#1e7d4f' : (v >= 5 ? '#b8860b' : '#c0392b');
  const bg = v >= 7 ? '#eaf6ea' : (v >= 5 ? '#fff8e1' : '#fdecea');
  const tip = 'Voto ' + v + '/10' + (r.voto_motivo ? ' \u2014 ' + r.voto_motivo : '') + ' (giudizio interno di prima lettura; il setaccio finale resta tuo)';
  return ' <span title="' + asteEsc(tip) + '" style="display:inline-block;min-width:20px;text-align:center;font-size:.8rem;font-weight:800;color:' + col + ';background:' + bg + ';border:1.2px solid ' + col + ';border-radius:6px;padding:1px 5px;cursor:help;vertical-align:1px">' + v + '</span>';
}

function asteFotoHtml(r) {
  const id = r.id;
  const n = (r.foto_sopralluogo || []).length;
  return `<div id="asteFotoBox-${id}" style="margin-top:12px;border:1.5px dashed #7a9ab8;border-radius:8px;padding:12px;background:#fbfdff;cursor:pointer"
    onclick="event.stopPropagation();document.getElementById('asteFotoIn-${id}').click()"
    ondragover="event.preventDefault();event.stopPropagation();this.style.background='#e8f0fb'"
    ondragleave="event.preventDefault();event.stopPropagation();this.style.background='#fbfdff'"
    ondrop="event.preventDefault();event.stopPropagation();this.style.background='#fbfdff';asteFotoFiles('${id}',event.dataTransfer.files)">
    <div style="font-size:.8rem;font-weight:700;color:#14315c">\uD83D\uDCF7 Foto sopralluogo di Gino${n ? ' (' + n + ')' : ''}</div>
    <div id="asteFotoTh-${id}" style="margin:6px 0;display:flex;gap:6px;flex-wrap:wrap" onclick="event.stopPropagation()"></div>
    <div id="asteFotoHint-${id}" style="font-size:.8rem;color:#3A5578;font-weight:600">Trascina qui le foto col mouse, oppure tocca questo riquadro per sceglierle: il caricamento parte da solo.</div>
    <input type="file" id="asteFotoIn-${id}" accept="image/*" multiple style="display:none" onclick="event.stopPropagation()" onchange="asteFotoFiles('${id}',this.files)">
    <div style="font-size:.72rem;color:#7a9ab8;margin-top:6px">Archivio privato (le vedi solo tu). Poi tocca "\uD83D\uDD04 Rigenera scheda PDF" qui sopra: Gianna le mette nella scheda in cima, sotto la fascia blu.</div>
  </div>`;
}

async function asteFotoRender(id) {
  const r = asteRows.find(x => x.id === id);
  const box = document.getElementById('asteFotoTh-' + id);
  if (!r || !box) return;
  const paths = r.foto_sopralluogo || [];
  if (!paths.length) { box.innerHTML = '<span style="font-size:.74rem;color:#7a9ab8">Nessuna foto ancora: scattale al sopralluogo e caricale qui.</span>'; return; }
  const { data, error } = await sb.storage.from(ASTE_SCHEDE_BUCKET).createSignedUrls(paths, 600);
  if (error || !data) { box.innerHTML = '<span style="font-size:.74rem;color:#c0392b">Errore lettura foto.</span>'; return; }
  box.innerHTML = data.map((d, i) => `<span style="position:relative;display:inline-block"><img src="${d.signedUrl}" alt="foto sopralluogo" style="height:64px;border-radius:6px;border:1px solid var(--caffe3)"><button type="button" title="Togli dalla scheda" onclick="event.stopPropagation();asteFotoDel('${id}',${i})" style="position:absolute;top:-6px;right:-6px;background:#c0392b;color:#fff;border:0;border-radius:50%;width:18px;height:18px;font-size:.7rem;line-height:1;cursor:pointer">\u00D7</button></span>`).join('');
}

async function asteFotoFiles(id, files) {
  const r = asteRows.find(x => x.id === id);
  const hint = document.getElementById('asteFotoHint-' + id);
  if (!r || !files || !files.length) return;
  const base = 'sopralluogo/' + String(r.id_pvp || r.id) + '/';
  const cur = (r.foto_sopralluogo || []).slice();
  if (hint) hint.textContent = 'Caricamento foto in corso\u2026';
  toast('Caricamento foto\u2026');
  for (let i = 0; i < files.length; i++) {
    const f = files[i];
    const ext = ((f.name.split('.').pop() || 'jpg').toLowerCase().replace(/[^a-z0-9]/g, '') || 'jpg');
    const path = base + 'foto-' + Date.now() + '-' + i + '.' + ext;
    const { error } = await sb.storage.from(ASTE_SCHEDE_BUCKET).upload(path, f, { contentType: f.type || 'image/jpeg', upsert: false });
    if (error) {
      if (hint) hint.textContent = 'Errore upload: ' + error.message;
      toast('Errore upload: ' + error.message, 'error');
      return;
    }
    cur.push(path);
  }
  const { error } = await sb.from('aste_immobili').update({ foto_sopralluogo: cur, updated_at: new Date().toISOString() }).eq('id', id);
  if (error) {
    if (hint) hint.textContent = 'Foto caricate ma elenco non salvato: ' + error.message;
    toast('Elenco foto non salvato: ' + error.message, 'error');
    return;
  }
  r.foto_sopralluogo = cur;
  const inp = document.getElementById('asteFotoIn-' + id);
  if (inp) inp.value = '';
  if (hint) hint.textContent = 'Trascina qui le foto col mouse, oppure tocca questo riquadro per sceglierle: il caricamento parte da solo.';
  await asteFotoRender(id);
  toast('Foto salvate (' + cur.length + '). Ora tocca "Rigenera scheda PDF" per averle nella scheda.');
}

async function asteFotoDel(id, idx) {
  const r = asteRows.find(x => x.id === id);
  if (!r) return;
  const cur = (r.foto_sopralluogo || []).slice();
  cur.splice(idx, 1);
  const { error } = await sb.from('aste_immobili').update({ foto_sopralluogo: cur, updated_at: new Date().toISOString() }).eq('id', id);
  if (error) { toast('Errore salvataggio: ' + error.message, 'error'); return; }
  r.foto_sopralluogo = cur;
  await asteFotoRender(id);
}

function asteDispLabel(d) {
  const t = (d || '').toUpperCase();
  if (t.includes('LIBER')) return '<span style="color:#27ae60;font-weight:600">libero</span>';
  if (t.includes('OCCUP')) return '<span style="color:#e67e22;font-weight:600">occupato</span>';
  return '<span style="color:var(--caffe2)">n.d.</span>';
}


// ═══ Scheda PDF riassuntiva (generata da Gianna su richiesta WhatsApp) ═══
const ASTE_WA_NUMBER = '16508702892';   // WhatsApp di Gianna (Instinct)
const ASTE_SCHEDE_BUCKET = 'aste-pratica';

function asteWaUrl(r) {
  const msg = 'Genera scheda asta ' + r.id_pvp + ' - ' + (r.comune || '') + ', ' + (r.indirizzo || '');
  return 'https://wa.me/' + ASTE_WA_NUMBER + '?text=' + encodeURIComponent(msg);
}

// Nome file scheda secondo la regola di Gino (20/10/2026): numero + via civico + comune
function asteNomeScheda(r) {
  const parts = [String(r.id_pvp || r.id)];
  if (r.indirizzo) parts.push(String(r.indirizzo).replace(/\//g, '-'));
  if (r.comune) parts.push(r.comune + (r.provincia ? ' (' + r.provincia + ')' : ''));
  return parts.join(' - ') + '.pdf';
}

function asteIsIOS() {
  return /iPad|iPhone|iPod/.test(navigator.userAgent) ||
    (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
}

async function asteApriScheda(id) {
  const r = asteRows.find(x => x.id === id);
  if (!r || !r.scheda_path) { toast('Nessuna scheda salvata per questa asta', 'error'); return; }
  const { data, error } = await sb.storage.from(ASTE_SCHEDE_BUCKET).createSignedUrl(r.scheda_path, 300);
  if (error || !data || !data.signedUrl) {
    toast('Scheda non raggiungibile: manca il bucket "' + ASTE_SCHEDE_BUCKET + '" o la colonna scheda_path (sql/aste-scheda-pdf.sql)?', 'error');
    return;
  }
  // iPad/iPhone: anteprima nel visualizzatore PDF nativo di Safari (nuova scheda, niente download).
  // Perche' si veda e non si scarichi, il file va caricato nel bucket con contentType 'application/pdf'.
  if (asteIsIOS()) { window.open(data.signedUrl, '_blank', 'noopener'); return; }
  asteMostraScheda(data.signedUrl, asteNomeScheda(r));
}

// Anteprima a schermo del PDF (desktop): overlay con il PDF dentro la pagina, senza scaricare.
function asteMostraScheda(url, nome) {
  const old = document.getElementById('asteSchedaOverlay');
  if (old) old.remove();
  const ov = document.createElement('div');
  ov.id = 'asteSchedaOverlay';
  ov.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:9999;display:flex;align-items:center;justify-content:center;padding:10px';
  ov.innerHTML =
    '<div style="background:#fff;width:100%;max-width:1000px;height:94%;border-radius:10px;overflow:hidden;display:flex;flex-direction:column;box-shadow:0 10px 40px rgba(0,0,0,.35)">' +
      '<div style="display:flex;align-items:center;gap:8px;padding:8px 12px;border-bottom:1px solid #e7dfcc;flex-wrap:wrap">' +
        '<strong style="flex:1 1 220px;font-size:.88rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">\uD83D\uDCC4 ' + asteEsc(nome) + '</strong>' +
        '<a href="' + url + '" target="_blank" rel="noopener" class="btn btn-secondary btn-sm">Apri in nuova scheda \u2197</a>' +
        '<a href="' + url + '" download="' + nome.replace(/"/g, '') + '" class="btn btn-secondary btn-sm">\u2B07 Scarica</a>' +
        '<button type="button" class="btn btn-primary btn-sm" onclick="document.getElementById(\'asteSchedaOverlay\').remove()">Chiudi \u2715</button>' +
      '</div>' +
      '<embed src="' + url + '" type="application/pdf" style="flex:1;width:100%;border:0;background:#525659">' +
    '</div>';
  ov.addEventListener('click', function (e) { if (e.target === ov) ov.remove(); });
  document.body.appendChild(ov);
}

async function asteLoad(force) {
  if (asteLoaded && !force) { asteRender(); return; }
  const body = document.getElementById('asteTableBody');
  if (body) body.innerHTML = '<tr><td colspan="9" style="padding:24px;text-align:center;color:var(--caffe2)">Caricamento…</td></tr>';
  try {
    const { data, error } = await sb.from('aste_immobili').select('*')
      .eq('attivo', true).order('data_asta', { ascending: true, nullsFirst: false }).limit(1000);
    if (error) throw error;
    asteRows = data || [];
    asteLoaded = true;
  } catch (e) {
    console.error('asteLoad', e);
    asteRows = [];
    if (body) body.innerHTML = '<tr><td colspan="9" style="padding:24px;text-align:center;color:#e74c3c">Errore di lettura. Se è il primo avvio: esegui sql/aste-immobili.sql in Supabase e poi il sync (GitHub Actions → Sync aste Veneto).</td></tr>';
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
    if (r.valutazione === 'scartato' && !asteShowScartate) return false;
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
    const posStyle = window.innerWidth < 700
      ? 'position:fixed;top:14vh;left:4vw;right:4vw;width:auto'
      : 'position:absolute;top:calc(100% + 6px);left:0;width:min(420px,88vw)';
    panel = `<div style="${posStyle};z-index:60;background:#fff;color:var(--testo);border:1px solid var(--caffe3);border-radius:12px;box-shadow:0 12px 40px rgba(30,58,92,.18);max-height:64vh;overflow-y:auto">
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
  const nScart = asteRows.filter(r => r.valutazione === 'scartato').length;
  const tg = `<button type="button" onclick="asteToggleScartate()" style="padding:6px 12px;border-radius:20px;border:1.5px solid ${asteShowScartate ? '#c0392b' : 'var(--caffe3)'};background:${asteShowScartate ? '#fdecea' : '#fff'};font-size:.76rem;cursor:pointer">${asteShowScartate ? '👁 Scartate visibili' : '🙈 Mostra scartate'} (${nScart})</button>`;
  wrap.innerHTML = chips.join('') + tg
    + `<span style="margin-left:auto;display:inline-flex">${btn('province', '▦ Per provincia')}${btn('flat', '☰ Elenco unico')}</span>`;
}

function asteRowHtml(r) {
  const id = r.id;
  const docs = (r.documenti || []).map(d =>
    `<a href="${asteEsc(d.url)}" target="_blank" rel="noopener" style="display:inline-block;margin:2px 6px 2px 0;padding:4px 10px;background:var(--sfondo);border:1px solid var(--caffe3);border-radius:6px;font-size:.75rem">📄 ${asteEsc(d.tipo || d.nome)}</a>`).join('');
  const foto = r.foto_url ? `<img src="${asteEsc(r.foto_url)}" alt="" loading="lazy" style="max-width:220px;border-radius:8px;border:1px solid var(--caffe3)">` : '<span style="color:var(--caffe2);font-size:.78rem">Foto non disponibile</span>';
  const val = r.valutazione || '';
  const bg = val === 'interessante' ? 'background:#FFEB00;' : (val === 'scartato' ? 'background:#ececec;opacity:.65;' : '');
  const valDate = r.valutazione_data ? new Date(r.valutazione_data).toLocaleDateString('it-IT') : '';
  const valCell = `<select onclick="event.stopPropagation()" onchange="asteSetValutazione('${id}',this.value)" style="padding:7px 8px;border-radius:8px;border:1.5px solid ${val ? '#3A5578' : 'var(--caffe3)'};font-size:.82rem;font-weight:${val ? '700' : '400'};background:#fff;min-width:118px;max-width:100%">
      <option value=""${val === '' ? ' selected' : ''}>— da valutare</option>
      <option value="interessante"${val === 'interessante' ? ' selected' : ''}>⭐ Interessante</option>
      <option value="scartato"${val === 'scartato' ? ' selected' : ''}>✖ Scartato</option>
    </select>${val && valDate ? `<br><span style="font-size:.72rem;color:#3A3000;font-weight:600">valutata il ${valDate}</span>` : ''}`;
  return `<tr style="border-bottom:1px solid var(--caffe3);cursor:pointer;${bg}" onclick="asteToggle('${id}')">
    <td style="padding:10px 12px">${r.foto_url ? `<img src="${asteEsc(r.foto_url)}" alt="" loading="lazy" style="width:64px;height:48px;object-fit:cover;border-radius:6px">` : '🏠'}</td>
    <td style="padding:10px 12px"><strong>${asteEsc(r.comune)}</strong>${asteVotoHtml(r)}${r.scheda_path ? ' <span title="Scheda PDF pronta" style="font-size:.82rem">\uD83D\uDCC4</span>' : ''} <span style="color:var(--caffe2)">(${asteEsc(r.provincia)})</span><br><span style="font-size:.76rem;color:var(--caffe2)">${asteEsc(r.indirizzo)}</span>
      <div class="aste-m" onclick="event.stopPropagation()"><span class="aste-m-date">${asteFmtDt(r.data_asta)}</span>${valCell}<span class="aste-m-info">${asteEsc(r.tipologia || 'altro')} · ${asteEsc((r.disponibilita || 'n.d.').toLowerCase().includes('liber') ? 'libero' : (r.disponibilita || '').toLowerCase().includes('occup') ? 'occupato' : 'n.d.')}</span></div></td>
    <td class="aste-c-tipo" style="padding:10px 12px;white-space:nowrap">${asteEsc(r.tipologia || 'altro')}</td>
    <td style="padding:10px 12px"><strong style="white-space:nowrap">${asteFmtEur(r.prezzo_base)}</strong><br><span style="font-size:.74rem;color:var(--caffe2);white-space:nowrap">off. min ${asteFmtEur(r.offerta_minima)}</span>${asteStimaHtml(r)}</td>
    <td class="aste-c-data" style="padding:10px 12px;white-space:nowrap"><span style="display:inline-block;background:#3A5578;color:#fff;font-size:1.02rem;font-weight:800;padding:5px 10px;border-radius:8px;letter-spacing:.2px">${asteFmtDt(r.data_asta)}</span><br><span style="font-size:.74rem;color:var(--caffe2)">offerte entro ${asteFmtDt(r.termine_offerte)}</span></td>
    <td class="aste-c-stato" style="padding:10px 12px">${asteDispLabel(r.disponibilita)}</td>
    <td class="aste-c-trib" style="padding:10px 12px;font-size:.78rem">${asteEsc(r.tribunale)}<br><span style="color:var(--caffe2)">proc. ${asteEsc(r.procedura)}</span></td>
    <td class="aste-c-val" style="padding:10px 12px">${valCell}</td>
    <td style="padding:10px 12px"><button class="btn btn-secondary btn-sm">▾</button></td>
  </tr>
  <tr id="asteDet-${id}" style="display:none;background:${val === 'interessante' ? '#FFF7A8' : '#faf9f7'}">
    <td colspan="9" style="padding:16px 20px">
      <div style="display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start;zoom:1.2">
        <div>${foto}</div>
        <div style="flex:1;min-width:280px">
          <p style="font-size:.85rem;line-height:1.6;margin:0 0 10px">${asteEsc(r.descrizione)}</p>
          <p style="font-size:.76rem;color:var(--caffe2);margin:0 0 10px">${asteEsc(r.tipologia_bene)} · ${asteEsc(r.modalita_vendita)}</p>
          <div style="margin-bottom:10px">${docs || '<span style="font-size:.78rem;color:var(--caffe2)">Nessun documento</span>'}</div>
          <div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center">
            <a href="${asteEsc(r.link_dettaglio)}" target="_blank" rel="noopener" class="btn btn-primary btn-sm">Apri scheda ufficiale ↗</a>
            <a href="${asteWaUrl(r)}" target="_blank" rel="noopener" class="btn btn-secondary btn-sm" title="Apre WhatsApp verso Gianna con la richiesta gia' scritta: ti arriva la scheda PDF riassuntiva">${r.scheda_path ? '🔄 Rigenera scheda PDF' : '💬 Genera scheda PDF'}</a>
            ${r.scheda_path ? `<button type="button" class="btn btn-primary btn-sm" style="background:#2e7d32;color:#fff" onclick="event.stopPropagation();asteApriScheda('${id}')">📄 Apri scheda PDF</button>` : ''}
          </div>
          <div style="margin-top:12px">
            <label style="font-size:.72rem;color:var(--caffe2)">Note private</label>
            <div style="display:flex;gap:8px;margin-top:4px">
              <input type="text" id="asteNote-${id}" value="${asteEsc(r.note_admin)}" placeholder="Es. interessante, da visitare…" style="flex:1;padding:7px 10px;border:1px solid var(--caffe3);border-radius:6px;font-size:.82rem">
              <button class="btn btn-secondary btn-sm" onclick="asteSaveNote('${id}')">Salva</button>
            </div>
          </div>
          ${asteFotoHtml(r)}
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
    body.innerHTML = '<tr><td colspan="9" style="padding:24px;text-align:center;color:var(--caffe2)">Nessuna asta trovata con questi filtri.</td></tr>';
    return;
  }
  if (asteView === 'flat') {
    body.innerHTML = rows.map(asteRowHtml).join('');
    return;
  }
  const groups = {};
  rows.forEach(r => { const k = r.provincia || 'Altro'; (groups[k] = groups[k] || []).push(r); });
  body.innerHTML = asteProvOrder(groups).map(prov => {
    const head = `<tr><td colspan="9" style="padding:10px 16px;background:linear-gradient(90deg,var(--sfondo),#fff);border-top:2px solid var(--caffe3);font-weight:700;font-size:.85rem;letter-spacing:.3px">📍 ${asteEsc(prov.toUpperCase())} <span style="color:var(--caffe2);font-weight:500">— ${groups[prov].length} aste</span></td></tr>`;
    return head + groups[prov].map(asteRowHtml).join('');
  }).join('');

  if (asteMapVisible) asteLeafletEnsure(() => setTimeout(asteMapRender, 50));

  // Link diretto all'anteprima: admin.html#scheda-<id riga> apre la scheda a schermo
  const m = (location.hash || '').match(/^#scheda-(.+)$/);
  if (m) {
    history.replaceState(null, '', location.pathname + location.search);
    asteApriScheda(m[1]);
  }
}

function asteToggle(id) {
  const el = document.getElementById('asteDet-' + id);
  if (el) {
    el.style.display = el.style.display === 'none' ? '' : 'none';
    if (el.style.display !== 'none') asteFotoRender(id);
  }
}

async function asteSaveNote(id) {
  const v = document.getElementById('asteNote-' + id)?.value || '';
  const { error } = await sb.from('aste_immobili').update({ note_admin: v, updated_at: new Date().toISOString() }).eq('id', id);
  if (error) { toast('Errore salvataggio nota', 'error'); return; }
  const r = asteRows.find(x => x.id === id);
  if (r) r.note_admin = v;
  toast('Nota salvata', 'success');
}


async function asteSetValutazione(id, v) {
  const r = asteRows.find(x => x.id === id);
  const when = v ? new Date().toISOString() : null;
  const { error } = await sb.from('aste_immobili').update({ valutazione: v || null, valutazione_data: when, updated_at: new Date().toISOString() }).eq('id', id);
  if (error) {
    toast('Errore: valutazione non salvata (colonne mancanti? esegui sql/aste-valutazione.sql)', 'error');
    asteRender();
    return;
  }
  if (r) { r.valutazione = v || null; r.valutazione_data = when; }
  toast(v === 'scartato' ? 'Scartata: nascosta dall\'elenco (usa "Mostra scartate" per ritrovarla)' : (v ? 'Salvato: ' + v : 'Valutazione rimossa'), 'success');
  asteRender();
}

// -------------------- mappa OSM delle aste "Interessante" (tutto il Veneto) --------------------
let asteMapObj = null;
let asteMapLayer = null;
let asteMapVisible = false;

function asteLeafletEnsure(cb) {
  if (window.L) { cb(); return; }
  if (!document.getElementById('leafletCss')) {
    const l = document.createElement('link');
    l.id = 'leafletCss'; l.rel = 'stylesheet';
    l.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
    document.head.appendChild(l);
  }
  if (document.getElementById('leafletJs')) {
    const t = setInterval(() => { if (window.L) { clearInterval(t); cb(); } }, 120);
    return;
  }
  const s = document.createElement('script');
  s.id = 'leafletJs';
  s.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
  s.onload = cb;
  document.head.appendChild(s);
}

function asteMapToggle() {
  const wrap = document.getElementById('asteMapWrap');
  if (!wrap) return;
  asteMapVisible = !asteMapVisible;
  wrap.style.display = asteMapVisible ? '' : 'none';
  const btn = document.getElementById('asteMapBtn');
  if (btn) btn.style.background = asteMapVisible ? 'var(--oro)' : '';
  if (asteMapVisible) asteLeafletEnsure(() => setTimeout(asteMapRender, 50));
}

function astePinIcon() {
  const svg = '<svg width="26" height="38" viewBox="0 0 26 38" xmlns="http://www.w3.org/2000/svg">'
    + '<defs><radialGradient id="astePinG" cx="35%" cy="30%" r="75%">'
    + '<stop offset="0%" stop-color="#ff8a80"/><stop offset="45%" stop-color="#e53935"/><stop offset="100%" stop-color="#8e0000"/>'
    + '</radialGradient></defs>'
    + '<ellipse cx="13" cy="35.5" rx="7" ry="2.4" fill="rgba(0,0,0,.28)"/>'
    + '<path d="M13 1 C6.4 1 1 6.4 1 13 c0 9 12 23 12 23 s12-14 12-23 C25 6.4 19.6 1 13 1 z" fill="url(#astePinG)" stroke="#7f0000" stroke-width="1"/>'
    + '<circle cx="13" cy="13" r="5" fill="#fff" opacity=".92"/>'
    + '</svg>';
  return L.divIcon({ className: 'aste-pin', html: svg, iconSize: [26, 38], iconAnchor: [13, 36], tooltipAnchor: [0, -30] });
}

function asteMapRender() {
  const el = document.getElementById('asteMap');
  if (!el || !window.L) return;
  if (!asteMapObj) {
    asteMapObj = L.map(el).setView([45.55, 11.75], 8);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(asteMapObj);
  }
  setTimeout(() => asteMapObj.invalidateSize(), 80);
  if (asteMapLayer) { asteMapObj.removeLayer(asteMapLayer); asteMapLayer = null; }
  const inter = asteRows.filter(r => r.valutazione === 'interessante');
  const conCoord = inter.filter(r => r.latitudine && r.longitudine);
  const senzaCoord = inter.length - conCoord.length;
  const info = document.getElementById('asteMapInfo');
  if (info) {
    info.textContent = conCoord.length
      ? conCoord.length + ' aste Interessanti sulla mappa' + (senzaCoord ? ' (' + senzaCoord + ' senza coordinate: cerco il comune…)' : '') + ' — passa sopra uno spillo per i dettagli, toccalo per aprire la riga'
      : (inter.length
          ? inter.length + ' aste Interessanti ma nessuna coordinata disponibile: cerco i comuni…'
          : 'Nessuna asta segnata come Interessante: usa la tendina "Valutazione" nelle righe sotto.');
  }
  if (!conCoord.length && !senzaCoord) { asteMapObj.setView([45.55, 11.75], 8); return; }
  const group = L.featureGroup();
  conCoord.forEach(r => {
    const mk = L.marker([r.latitudine, r.longitudine], { icon: astePinIcon() });
    mk.bindTooltip('<strong>' + asteEsc(r.comune) + '</strong> (' + asteEsc(r.provincia) + ')<br>' + asteEsc(r.indirizzo) +
      '<br>' + asteFmtEur(r.prezzo_base) + ' · asta ' + asteFmtDt(r.data_asta), { direction: 'top', offset: [0, -8] });
    mk.on('click', () => {
      const det = document.getElementById('asteDet-' + r.id);
      const row = det ? det.previousElementSibling : null;
      if (row) row.scrollIntoView({ behavior: 'smooth', block: 'center' });
      if (det && det.style.display === 'none') asteToggle(String(r.id));
    });
    group.addLayer(mk);
  });
  group.addTo(asteMapObj);
  asteMapLayer = group;
  if (conCoord.length) asteMapObj.fitBounds(group.getBounds().pad(0.15));

  // Fallback: righe Interessanti senza coordinate PVP -> geocoding gratuito OSM (Nominatim), con cache locale
  const mancanti = inter.filter(r => !(r.latitudine && r.longitudine));
  if (mancanti.length) asteMapGeocodeMissing(mancanti);
}

function asteViaPulita(via) {
  let v = (' ' + String(via || '').toLowerCase() + ' ');
  v = v.replace(/\bnn?\.\s*/g, ' ')
       .replace(/\bint(?:erno)?\.?\s*\w+\b/g, ' ')
       .replace(/\bscala\s+\w+\b/g, ' ')
       .replace(/ai civici[\s\d\-\/]*/g, ' ')
       .replace(/\s+e\s+\S+/g, ' ')
       .replace(/(\d+)[\/\-]\S+/g, '$1')
       .replace(/\s+/g, ' ')
       .trim();
  return v;
}

async function asteMapGeocodeMissing(rows) {
  let cache = {};
  try { cache = JSON.parse(localStorage.getItem('asteGeoCache') || '{}'); } catch (e) {}
  let added = false;
  for (const r of rows) {
    const q = [asteViaPulita(r.indirizzo), r.comune, r.provincia, 'Italia'].filter(Boolean).join(', ');
    let livello = 'da indirizzo';
    if (!q) continue;
    let pt = cache[q];
    if (!pt) {
      try {
        let resp = await fetch('https://nominatim.openstreetmap.org/search?format=json&limit=1&q=' + encodeURIComponent(q));
        let arr = await resp.json();
        if (!arr || !arr.length) {
          // indirizzo non trovato: spillo sul comune (richiesta di Gino)
          const qc = [r.comune, r.provincia, 'Italia'].filter(Boolean).join(', ');
          await new Promise(res => setTimeout(res, 1100));
          resp = await fetch('https://nominatim.openstreetmap.org/search?format=json&limit=1&q=' + encodeURIComponent(qc));
          arr = await resp.json();
          livello = 'sul comune';
        }
        if (arr && arr.length) { pt = [parseFloat(arr[0].lat), parseFloat(arr[0].lon)]; cache[q] = pt; }
      } catch (e) { /* rete o limite: salto */ }
      await new Promise(res => setTimeout(res, 1100));
    }
    if (!pt) continue;
    const mk = L.marker(pt, { icon: astePinIcon() });
    mk.bindTooltip('<strong>' + asteEsc(r.comune) + '</strong> (' + asteEsc(r.provincia) + ')<br>' + asteEsc(r.indirizzo) +
      '<br>' + asteFmtEur(r.prezzo_base) + ' · asta ' + asteFmtDt(r.data_asta) +
      '<br><em>posizione approssimata (' + livello + ')</em>', { direction: 'top', offset: [0, -30] });
    mk.on('click', () => {
      const det = document.getElementById('asteDet-' + r.id);
      const row = det ? det.previousElementSibling : null;
      if (row) row.scrollIntoView({ behavior: 'smooth', block: 'center' });
      if (det && det.style.display === 'none') asteToggle(String(r.id));
    });
    if (asteMapLayer) { mk.addTo(asteMapLayer); } else { mk.addTo(asteMapObj); }
    added = true;
  }
  try { localStorage.setItem('asteGeoCache', JSON.stringify(cache)); } catch (e) {}
  if (added && asteMapLayer) {
    try { asteMapObj.fitBounds(asteMapLayer.getBounds().pad(0.15)); } catch (e) {}
  }
  const info = document.getElementById('asteMapInfo');
  if (info && added) {
    const tot = asteRows.filter(r => r.valutazione === 'interessante').length;
    const nPins = asteMapLayer ? asteMapLayer.getLayers().length : 0;
    const manc = tot - nPins;
    info.textContent = nPins + ' aste Interessanti sulla mappa' +
      (manc > 0 ? ' (' + manc + ' senza posizione trovata: controlla l\'indirizzo PVP)' : '') +
      ' — passa sopra uno spillo per i dettagli, toccalo per aprire la riga';
  }
}

function asteToggleScartate() {
  asteShowScartate = !asteShowScartate;
  asteRender();
}
