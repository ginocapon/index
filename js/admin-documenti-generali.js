/* Admin — Documenti Generali (contratti, modelli, riferimenti) */
(function () {
  'use strict';

  var DOC_GEN_LS_KEY = 'rig_documenti_generali_v1';
  var DOC_GEN_MAX_MB = 20;
  var DOC_GEN_ACCEPT = '.pdf,.doc,.docx,.xls,.xlsx,.jpg,.jpeg,.png,.webp,.zip';
  var DOC_GEN_ALLOWED_EXT = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'jpeg', 'png', 'webp', 'zip'];
  var docGenGruppi = [];
  var docGenUseLocal = false;
  var docGenFilter = '';
  var docGenDirty = false;

  function getSb() {
    return window.sb || null;
  }

  function esc(s) {
    if (typeof escHtml === 'function') return escHtml(s);
    return String(s || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function genLocalId() {
    return 'local_' + Date.now() + '_' + Math.random().toString(36).slice(2, 8);
  }

  function storagePublicUrl(bucket, path) {
    var client = getSb();
    if (!client) return '';
    var res = client.storage.from(bucket).getPublicUrl(path);
    if (res && res.data && res.data.publicUrl) return res.data.publicUrl;
    if (res && res.publicUrl) return res.publicUrl;
    return '';
  }

  function isAllowedDocFile(file) {
    var ext = (file.name.split('.').pop() || '').toLowerCase();
    return DOC_GEN_ALLOWED_EXT.indexOf(ext) >= 0;
  }

  function shouldSkipFile(file) {
    var name = file.name || '';
    if (!name || name.charAt(0) === '.') return true;
    if (/^(thumbs\.db|desktop\.ini|\.ds_store)$/i.test(name)) return true;
    return false;
  }

  function getRelPath(file) {
    return String(file.webkitRelativePath || file._docGenRelPath || file.name || '').replace(/\\/g, '/');
  }

  function slugSegment(value) {
    if (typeof slugify === 'function') return slugify(value);
    return String(value || '').replace(/[^a-zA-Z0-9._-]/g, '-').replace(/-+/g, '-');
  }

  function buildStoragePath(g, file, batchId) {
    var rel = getRelPath(file);
    var parts = rel.split('/').filter(Boolean);
    var fileName = parts.pop() || file.name || 'file';
    var dirs = parts.map(slugSegment);
    var base = 'generali/' + String(g.id).replace(/[^a-zA-Z0-9_-]/g, '') + '/' + batchId;
    var slugFile = slugSegment(fileName);
    if (dirs.length) return base + '/' + dirs.join('/') + '/' + slugFile;
    return base + '-' + slugFile;
  }

  function readDirectoryEntries(reader) {
    return new Promise(function (resolve, reject) {
      var all = [];
      function readBatch() {
        reader.readEntries(function (entries) {
          if (!entries.length) {
            resolve(all);
            return;
          }
          all = all.concat(entries);
          readBatch();
        }, reject);
      }
      readBatch();
    });
  }

  async function traverseEntry(entry, prefix, out) {
    if (entry.isFile) {
      var file = await new Promise(function (resolve, reject) {
        entry.file(resolve, reject);
      });
      var rel = prefix ? prefix + file.name : file.name;
      if (shouldSkipFile(file)) return;
      try {
        Object.defineProperty(file, 'webkitRelativePath', { value: rel });
      } catch (e) {
        file._docGenRelPath = rel;
      }
      out.push(file);
      return;
    }
    if (entry.isDirectory) {
      var reader = entry.createReader();
      var entries = await readDirectoryEntries(reader);
      var nextPrefix = prefix ? prefix + entry.name + '/' : entry.name + '/';
      for (var i = 0; i < entries.length; i++) {
        await traverseEntry(entries[i], nextPrefix, out);
      }
    }
  }

  async function collectDroppedFiles(dataTransfer) {
    if (!dataTransfer) return [];
    var items = dataTransfer.items ? Array.prototype.slice.call(dataTransfer.items) : [];
    if (items.length && items[0] && items[0].webkitGetAsEntry) {
      var files = [];
      for (var i = 0; i < items.length; i++) {
        var entry = items[i].webkitGetAsEntry();
        if (entry) await traverseEntry(entry, '', files);
      }
      if (files.length) return files;
    }
    return Array.prototype.slice.call(dataTransfer.files || []);
  }

  function normalizeFileList(raw) {
    if (!Array.isArray(raw)) return [];
    return raw.map(function (f, i) {
      return {
        url: f.url || '',
        nome: f.nome || 'file',
        tipo: (f.tipo || '').toLowerCase() || (f.nome || '').split('.').pop().toLowerCase(),
        ordine: typeof f.ordine === 'number' ? f.ordine : i
      };
    }).sort(function (a, b) { return a.ordine - b.ordine; });
  }

  function markDocGenDirty() {
    docGenDirty = true;
    updateDocGenSaveBar();
  }

  function updateDocGenSaveBar() {
    var bar = document.getElementById('docGenSaveBar');
    var btn = document.getElementById('docGenSaveAllBtn');
    if (bar) bar.classList.toggle('is-dirty', docGenDirty);
    if (btn) {
      btn.disabled = !docGenDirty;
      btn.textContent = docGenDirty ? '💾 Salva modifiche *' : '💾 Salva modifiche';
    }
  }

  function updateDocGenSyncBanner() {
    var el = document.getElementById('docGenSyncBanner');
    if (!el) return;
    if (docGenUseLocal) {
      el.className = 'doc-gen-sync-banner is-local';
      el.innerHTML = '<strong>⚠️ Archivio solo su questo browser</strong> — i documenti caricati da un altro PC <strong>non compaiono qui</strong> perché l\'elenco è salvato in locale (localStorage), non su Supabase. ' +
        'Per sincronizzare tutti i PC: esegui <code>sql/documenti-generali.sql</code> nel SQL Editor Supabase, poi clicca <strong>Ricarica da cloud</strong> su ogni PC.';
    } else {
      el.className = 'doc-gen-sync-banner is-cloud';
      el.innerHTML = '<strong>☁️ Archivio condiviso (Supabase)</strong> — titoli, link e file sono visibili da qualsiasi PC con accesso admin. ' +
        'Se non vedi aggiornamenti recenti, clicca <strong>Ricarica da cloud</strong>. Dopo aver modificato titoli o note, premi <strong>Salva modifiche</strong>.';
    }
  }

  window.addEventListener('beforeunload', function (e) {
    if (docGenDirty) {
      e.preventDefault();
      e.returnValue = '';
    }
  });

  function sortGruppi() {
    docGenGruppi.sort(function (a, b) {
      if (a.tipo === 'riferimento' && b.tipo !== 'riferimento') return -1;
      if (a.tipo !== 'riferimento' && b.tipo === 'riferimento') return 1;
      return (a.ordine || 0) - (b.ordine || 0);
    });
  }

  function saveLocal() {
    try {
      localStorage.setItem(DOC_GEN_LS_KEY, JSON.stringify(docGenGruppi));
    } catch (e) { /* ignore */ }
  }

  function loadLocal() {
    try {
      var raw = localStorage.getItem(DOC_GEN_LS_KEY);
      if (!raw) return [];
      return JSON.parse(raw);
    } catch (e) {
      return [];
    }
  }

  var DOC_GEN_REQUIRED_RIF = [
    {
      titolo: 'Come lavoriamo con i clienti',
      link_url: '/servizio-locazioni',
      note: 'Pagina servizio locazioni — metodo Righetto'
    },
    {
      titolo: 'Costi locazione inquilino',
      link_url: '/landing-costi-locazione-inquilino',
      note: 'Guida deposito, registro, asseverazione e spese ingresso'
    }
  ];

  function normalizeLinkPath(url) {
    var u = String(url || '').trim().toLowerCase();
    if (!u) return '';
    if (u.indexOf('http') === 0) {
      try { u = new URL(u).pathname; } catch (e) { /* ignore */ }
    }
    return u.replace(/\/+$/, '') || '/';
  }

  async function ensureDefaultRiferimenti() {
    var added = false;
    var existing = docGenGruppi.filter(function (g) { return g.tipo === 'riferimento'; });
    var paths = existing.map(function (g) { return normalizeLinkPath(g.link_url); });

    for (var i = 0; i < DOC_GEN_REQUIRED_RIF.length; i++) {
      var req = DOC_GEN_REQUIRED_RIF[i];
      var path = normalizeLinkPath(req.link_url);
      if (paths.indexOf(path) >= 0) continue;
      var g = {
        id: genLocalId(),
        titolo: req.titolo,
        tipo: 'riferimento',
        ordine: existing.length,
        link_url: req.link_url,
        note: req.note || '',
        file: []
      };
      docGenGruppi.push(g);
      existing.push(g);
      paths.push(path);
      added = true;
      try { await persistGruppo(g); } catch (e) { /* ignore */ }
    }
    return added;
  }

  function seedDefaults() {
    return [
      {
        id: genLocalId(),
        titolo: 'Come lavoriamo con i clienti',
        tipo: 'riferimento',
        ordine: 0,
        link_url: '/servizio-locazioni',
        note: 'Pagina informativa — collega landing o pagina servizio',
        file: []
      },
      {
        id: genLocalId(),
        titolo: 'Costi locazione inquilino',
        tipo: 'riferimento',
        ordine: 1,
        link_url: '/landing-costi-locazione-inquilino',
        note: 'Guida deposito, registro, asseverazione e spese ingresso',
        file: []
      },
      {
        id: genLocalId(),
        titolo: 'Locazioni',
        tipo: 'documento',
        ordine: 0,
        link_url: '',
        note: 'Modelli Word, PDF, ZIP e allegati JPG',
        file: []
      }
    ];
  }

  async function persistGruppo(g) {
    if (!g || !g.id) return;
    g.updated_at = new Date().toISOString();
    g.file = normalizeFileList(g.file);
    var client = getSb();
    if (docGenUseLocal || !client) {
      saveLocal();
      return;
    }
    var row = {
      id: String(g.id).startsWith('local_') ? undefined : g.id,
      titolo: g.titolo || '',
      tipo: g.tipo || 'documento',
      ordine: g.ordine || 0,
      link_url: g.link_url || '',
      note: g.note || '',
      file: g.file,
      updated_at: g.updated_at
    };
    if (!row.id) {
      var ins = await client.from('documenti_generali').insert({
        titolo: row.titolo,
        tipo: row.tipo,
        ordine: row.ordine,
        link_url: row.link_url,
        note: row.note,
        file: row.file
      }).select().single();
      if (ins.error) throw ins.error;
      g.id = ins.data.id;
      return;
    }
    var upd = await client.from('documenti_generali').update(row).eq('id', g.id);
    if (upd.error) throw upd.error;
  }

  async function deleteGruppoDb(id) {
    var client = getSb();
    if (docGenUseLocal || !client || String(id).startsWith('local_')) return;
    await client.from('documenti_generali').delete().eq('id', id);
  }

  window.loadDocumentiGenerali = async function () {
    docGenFilter = (document.getElementById('docGenSearch') || {}).value || '';
    docGenUseLocal = false;
    docGenGruppi = [];
    var client = getSb();

    if (client) {
      try {
        var res = await client.from('documenti_generali').select('*').order('ordine', { ascending: true });
        if (res.error) {
          if (res.error.code === '42P01' || (res.error.message || '').indexOf('documenti_generali') >= 0) {
            docGenUseLocal = true;
          } else {
            toast('Documenti Generali: ' + res.error.message, 'error');
            docGenUseLocal = true;
          }
        } else {
          docGenGruppi = (res.data || []).map(function (r) {
            return {
              id: r.id,
              titolo: r.titolo,
              tipo: r.tipo || 'documento',
              ordine: r.ordine || 0,
              link_url: r.link_url || '',
              note: r.note || '',
              file: normalizeFileList(r.file)
            };
          });
        }
      } catch (e) {
        docGenUseLocal = true;
      }
    } else {
      docGenUseLocal = true;
    }

    if (docGenUseLocal) {
      docGenGruppi = loadLocal();
      if (!docGenGruppi.length) {
        docGenGruppi = seedDefaults();
        saveLocal();
      }
    } else if (!docGenGruppi.length) {
      docGenGruppi = seedDefaults();
      for (var i = 0; i < docGenGruppi.length; i++) {
        try { await persistGruppo(docGenGruppi[i]); } catch (e) { /* ignore */ }
      }
    }

    await ensureDefaultRiferimenti();

    sortGruppi();
    docGenDirty = false;
    renderDocumentiGenerali();
    updateDocGenStats();
    updateDocGenSaveBar();
    updateDocGenSyncBanner();
  };

  function updateDocGenStats() {
    var rif = docGenGruppi.filter(function (g) { return g.tipo === 'riferimento'; }).length;
    var doc = docGenGruppi.filter(function (g) { return g.tipo === 'documento'; }).length;
    var files = docGenGruppi.reduce(function (n, g) { return n + (g.file ? g.file.length : 0); }, 0);
    var el;
    el = document.getElementById('statDocGenRif'); if (el) el.textContent = rif;
    el = document.getElementById('statDocGenArg'); if (el) el.textContent = doc;
    el = document.getElementById('statDocGenFile'); if (el) el.textContent = files;
    el = document.getElementById('docGenModeBadge');
    if (el) {
      el.textContent = docGenUseLocal ? 'Salvataggio locale (esegui sql/documenti-generali.sql)' : 'Supabase';
      el.style.background = docGenUseLocal ? '#fff3e0' : '#e8f5e9';
      el.style.color = docGenUseLocal ? '#e65100' : '#2e7d32';
    }
  }

  function filteredGruppi(tipo) {
    var q = (docGenFilter || '').toLowerCase().trim();
    return docGenGruppi.filter(function (g) {
      if (g.tipo !== tipo) return false;
      if (!q) return true;
      var hay = ((g.titolo || '') + ' ' + (g.note || '') + ' ' + (g.link_url || '')).toLowerCase();
      if (hay.indexOf(q) >= 0) return true;
      return (g.file || []).some(function (f) { return (f.nome || '').toLowerCase().indexOf(q) >= 0; });
    });
  }

  function renderFileList(g) {
    var files = normalizeFileList(g.file);
    if (!files.length) {
      return '<div style="font-size:0.78rem;color:var(--caffe2);padding:8px 0">Nessun file — trascina file/cartella o usa i pulsanti sopra</div>';
    }
    return files.map(function (f, fi) {
      var displayName = String(f.nome || 'file').replace(/\\/g, '/');
      var icon = typeof getFileIcon === 'function' ? getFileIcon(displayName) : '📎';
      var isImg = /\.(jpg|jpeg|png|webp|gif)$/i.test(displayName);
      if (isImg) icon = '🖼️';
      var pathParts = displayName.split('/');
      var fileLabel = pathParts.length > 1 ? pathParts[pathParts.length - 1] : displayName;
      var folderLabel = pathParts.length > 1 ? pathParts.slice(0, -1).join('/') + '/' : '';
      return '<div class="doc-gen-file-row">' +
        '<span class="doc-gen-file-arrows">' +
        '<button type="button" onclick="docGenFileMove(\'' + g.id + '\',' + fi + ',-1)" ' + (fi === 0 ? 'disabled' : '') + ' title="Su">▲</button>' +
        '<button type="button" onclick="docGenFileMove(\'' + g.id + '\',' + fi + ',1)" ' + (fi === files.length - 1 ? 'disabled' : '') + ' title="Giù">▼</button>' +
        '</span>' +
        '<span class="doc-gen-file-icon">' + icon + '</span>' +
        '<div class="doc-gen-file-info">' +
        '<div class="doc-gen-file-name" title="' + esc(displayName) + '">' + esc(fileLabel) + '</div>' +
        '<div class="doc-gen-file-meta">' + esc((f.tipo || '').toUpperCase()) + (folderLabel ? ' · 📁 ' + esc(folderLabel) : '') + '</div>' +
        '</div>' +
        '<a href="' + esc(f.url) + '" target="_blank" rel="noopener" class="btn btn-secondary btn-sm" style="font-size:0.7rem;padding:4px 10px">Apri</a>' +
        '<button type="button" class="doc-del" onclick="docGenRemoveFile(\'' + g.id + '\',' + fi + ')" title="Elimina">✕</button>' +
        '</div>';
    }).join('');
  }

  function renderRiferimentoCard(g) {
    return '<div class="doc-gen-rif-card" data-id="' + esc(g.id) + '">' +
      '<div class="doc-gen-rif-arrows">' +
      '<button type="button" onclick="docGenGruppoMove(\'' + g.id + '\',-1)" title="Sposta a sinistra">◀</button>' +
      '<button type="button" onclick="docGenGruppoMove(\'' + g.id + '\',1)" title="Sposta a destra">▶</button>' +
      '</div>' +
      '<div class="doc-gen-rif-body">' +
      '<input type="text" class="doc-gen-title-input" value="' + esc(g.titolo) + '" placeholder="Titolo riferimento (es. Come affittiamo)" oninput="docGenUpdateField(\'' + g.id + '\',\'titolo\',this.value)">' +
      '<input type="text" class="doc-gen-link-input" value="' + esc(g.link_url) + '" placeholder="Link pagina (es. /servizio-locazioni)" oninput="docGenUpdateField(\'' + g.id + '\',\'link_url\',this.value)">' +
      (g.link_url ? '<a href="' + esc(g.link_url.indexOf('http') === 0 ? g.link_url : ('https://righettoimmobiliare.it' + (g.link_url.indexOf('/') === 0 ? '' : '/') + g.link_url)) + '" target="_blank" class="doc-gen-rif-open">Apri pagina ↗</a>' : '') +
      '</div>' +
      '<button type="button" class="doc-gen-del-gruppo" onclick="docGenDeleteGruppo(\'' + g.id + '\')" title="Elimina">🗑️</button>' +
      '</div>';
  }

  function renderDocumentoCard(g, idx) {
    return '<div class="doc-gen-card" data-id="' + esc(g.id) + '">' +
      '<div class="doc-gen-card-label">Argomento ' + (idx + 1) + '</div>' +
      '<div class="doc-gen-card-head">' +
      '<div class="doc-gen-gruppo-arrows">' +
      '<button type="button" onclick="docGenGruppoMove(\'' + g.id + '\',-1)" title="Sposta su">▲</button>' +
      '<button type="button" onclick="docGenGruppoMove(\'' + g.id + '\',1)" title="Sposta giù">▼</button>' +
      '</div>' +
      '<div style="flex:1;min-width:0">' +
      '<input type="text" class="doc-gen-title-input doc-gen-title-lg" value="' + esc(g.titolo) + '" placeholder="Titolo argomento (es. Locazioni studenti, contratti 4+4)" oninput="docGenUpdateField(\'' + g.id + '\',\'titolo\',this.value)">' +
      '<input type="text" class="doc-gen-note-input" value="' + esc(g.note || '') + '" placeholder="Nota breve (opzionale)" oninput="docGenUpdateField(\'' + g.id + '\',\'note\',this.value)">' +
      '</div>' +
      '<button type="button" class="doc-gen-del-gruppo" onclick="docGenDeleteGruppo(\'' + g.id + '\')" title="Elimina argomento">🗑️</button>' +
      '</div>' +
      '<div class="upload-zone doc-gen-drop" id="docGenDrop-' + esc(g.id) + '" ondragover="onDragOver(event)" ondragleave="docGenDragLeave(event,\'' + g.id + '\')" ondrop="docGenOnDrop(event,\'' + g.id + '\')">' +
      '<div style="font-size:1.5rem;margin-bottom:6px">📁</div>' +
      '<div style="font-size:0.82rem;font-weight:600">Trascina file o cartella intera</div>' +
      '<div style="font-size:0.72rem;color:var(--caffe2);margin-top:4px">Word, PDF, JPG, PNG, Excel, ZIP — max ' + DOC_GEN_MAX_MB + ' MB per file</div>' +
      '<div class="doc-gen-upload-actions">' +
      '<button type="button" class="btn btn-secondary btn-sm" onclick="event.stopPropagation();docGenPickFiles(\'' + g.id + '\')">+ File</button>' +
      '<button type="button" class="btn btn-secondary btn-sm" onclick="event.stopPropagation();docGenPickFolder(\'' + g.id + '\')">+ Cartella</button>' +
      '</div>' +
      '<input type="file" id="docGenInput-' + esc(g.id) + '" multiple accept="' + DOC_GEN_ACCEPT + '" style="display:none" onchange="docGenUploadFiles(\'' + g.id + '\',this.files);this.value=\'\'">' +
      '<input type="file" id="docGenFolder-' + esc(g.id) + '" multiple webkitdirectory directory style="display:none" onchange="docGenUploadFiles(\'' + g.id + '\',this.files);this.value=\'\'">' +
      '</div>' +
      '<div class="doc-gen-files">' + renderFileList(g) + '</div>' +
      '</div>';
  }

  window.renderDocumentiGenerali = function () {
    var rifWrap = document.getElementById('docGenRiferimenti');
    var docWrap = document.getElementById('docGenArchivio');
    if (!rifWrap || !docWrap) return;

    var rif = filteredGruppi('riferimento');
    var docs = filteredGruppi('documento');

    rifWrap.innerHTML = rif.length
      ? '<div class="doc-gen-rif-grid">' + rif.map(renderRiferimentoCard).join('') + '</div>'
      : '<div class="empty-state" style="padding:24px"><p>Nessun riferimento in alto — aggiungi una pagina informativa</p></div>';

    docWrap.innerHTML = docs.length
      ? docs.map(function (g, i) { return renderDocumentoCard(g, i); }).join('')
      : '<div class="empty-state" style="padding:32px"><h3>Nessun argomento</h3><p>Clicca «+ Nuovo argomento» per archiviare contratti e modelli</p></div>';
  };

  function findGruppo(id) {
    return docGenGruppi.find(function (g) { return g.id === id; });
  }

  window.docGenPickFiles = function (id) {
    var input = document.getElementById('docGenInput-' + id);
    if (input) input.click();
  };

  window.docGenPickFolder = function (id) {
    var input = document.getElementById('docGenFolder-' + id);
    if (input) input.click();
  };

  window.docGenFilterList = function () {
    docGenFilter = (document.getElementById('docGenSearch') || {}).value || '';
    renderDocumentiGenerali();
  };

  window.docGenUpdateField = function (id, field, value) {
    var g = findGruppo(id);
    if (!g) return;
    g[field] = value;
    markDocGenDirty();
  };

  window.docGenSaveAll = async function () {
    if (!docGenDirty) {
      toast('Nessuna modifica da salvare', 'info');
      return;
    }
    if (docGenUseLocal) {
      saveLocal();
      docGenDirty = false;
      updateDocGenSaveBar();
      toast('Salvato in locale su questo browser — per altri PC esegui sql/documenti-generali.sql', 'error');
      return;
    }
    var client = getSb();
    if (!client) {
      toast('Supabase non disponibile — ricarica la pagina admin', 'error');
      return;
    }
    var errors = 0;
    for (var i = 0; i < docGenGruppi.length; i++) {
      try {
        await persistGruppo(docGenGruppi[i]);
      } catch (e) {
        errors++;
      }
    }
    if (errors) {
      toast('Errore salvataggio su ' + errors + ' elementi', 'error');
      return;
    }
    docGenDirty = false;
    updateDocGenSaveBar();
    updateDocGenStats();
    toast('Tutte le modifiche salvate su Supabase', 'success');
  };

  window.docGenReloadFromCloud = async function () {
    var client = getSb();
    if (!client) {
      toast('Supabase non disponibile — ricarica la pagina admin', 'error');
      return;
    }
    if (docGenDirty && !confirm('Hai modifiche non salvate. Ricaricare da cloud e scartarle?')) return;
    docGenDirty = false;
    docGenUseLocal = false;
    docGenGruppi = [];
    try {
      var res = await client.from('documenti_generali').select('*').order('ordine', { ascending: true });
      if (res.error) {
        if (res.error.code === '42P01' || (res.error.message || '').indexOf('documenti_generali') >= 0) {
          toast('Tabella documenti_generali assente — esegui sql/documenti-generali.sql su Supabase', 'error');
          docGenUseLocal = true;
          docGenGruppi = loadLocal();
        } else {
          toast('Errore: ' + res.error.message, 'error');
          return;
        }
      } else {
        docGenGruppi = (res.data || []).map(function (r) {
          return {
            id: r.id,
            titolo: r.titolo,
            tipo: r.tipo || 'documento',
            ordine: r.ordine || 0,
            link_url: r.link_url || '',
            note: r.note || '',
            file: normalizeFileList(r.file)
          };
        });
        docGenUseLocal = false;
      }
      await ensureDefaultRiferimenti();
      sortGruppi();
      renderDocumentiGenerali();
      updateDocGenStats();
      updateDocGenSaveBar();
      updateDocGenSyncBanner();
      toast('Archivio ricaricato da cloud', 'success');
    } catch (e) {
      toast('Errore ricarica: ' + (e.message || e), 'error');
    }
  };

  window.docGenSaveGruppo = async function (id) {
    var g = findGruppo(id);
    if (!g) return;
    try {
      await persistGruppo(g);
      toast('Salvato: ' + (g.titolo || 'documento'), 'success');
      updateDocGenStats();
    } catch (e) {
      toast('Errore salvataggio: ' + (e.message || e), 'error');
    }
  };

  window.docGenAddGruppo = async function (tipo) {
    if (docGenDirty && !confirm('Hai modifiche non salvate. Aggiungere comunque un nuovo elemento?')) return;
    var sameTipo = docGenGruppi.filter(function (g) { return g.tipo === tipo; });
    var g = {
      id: genLocalId(),
      titolo: tipo === 'riferimento' ? 'Nuovo riferimento' : 'Locazioni',
      tipo: tipo,
      ordine: sameTipo.length,
      link_url: tipo === 'riferimento' ? '/servizio-locazioni' : '',
      note: '',
      file: []
    };
    docGenGruppi.push(g);
    sortGruppi();
    try {
      await persistGruppo(g);
      toast('Aggiunto — ricordati di salvare se modifichi titolo o note', 'success');
    } catch (e) {
      toast('Errore: ' + (e.message || e), 'error');
    }
    renderDocumentiGenerali();
    updateDocGenStats();
  };

  window.docGenDeleteGruppo = async function (id) {
    if (!confirm('Eliminare questo elemento e i relativi riferimenti ai file?')) return;
    var idx = docGenGruppi.findIndex(function (g) { return g.id === id; });
    if (idx < 0) return;
    docGenGruppi.splice(idx, 1);
    try {
      await deleteGruppoDb(id);
      if (docGenUseLocal) saveLocal();
      toast('Eliminato', 'success');
    } catch (e) {
      toast('Errore: ' + (e.message || e), 'error');
    }
    renderDocumentiGenerali();
    updateDocGenStats();
  };

  window.docGenGruppoMove = async function (id, delta) {
    var g = findGruppo(id);
    if (!g) return;
    var list = docGenGruppi.filter(function (x) { return x.tipo === g.tipo; });
    list.sort(function (a, b) { return (a.ordine || 0) - (b.ordine || 0); });
    var i = list.findIndex(function (x) { return x.id === id; });
    var j = i + delta;
    if (i < 0 || j < 0 || j >= list.length) return;
    var tmp = list[i];
    list[i] = list[j];
    list[j] = tmp;
    list.forEach(function (item, idx) { item.ordine = idx; });
    markDocGenDirty();
    sortGruppi();
    renderDocumentiGenerali();
  };

  window.docGenFileMove = async function (id, fileIdx, delta) {
    var g = findGruppo(id);
    if (!g) return;
    g.file = normalizeFileList(g.file);
    var j = fileIdx + delta;
    if (j < 0 || j >= g.file.length) return;
    var t = g.file[fileIdx];
    g.file[fileIdx] = g.file[j];
    g.file[j] = t;
    g.file.forEach(function (f, i) { f.ordine = i; });
    markDocGenDirty();
    renderDocumentiGenerali();
  };

  window.docGenRemoveFile = async function (id, fileIdx) {
    var g = findGruppo(id);
    if (!g || !g.file) return;
    g.file.splice(fileIdx, 1);
    g.file.forEach(function (f, i) { f.ordine = i; });
    try {
      await persistGruppo(g);
      toast('File rimosso', 'success');
    } catch (e) {
      toast('Errore: ' + (e.message || e), 'error');
    }
    renderDocumentiGenerali();
    updateDocGenStats();
  };

  window.docGenDragLeave = function (e, id) {
    var el = document.getElementById('docGenDrop-' + id);
    if (el) el.classList.remove('drag-over');
  };

  window.docGenOnDrop = async function (e, id) {
    e.preventDefault();
    e.stopPropagation();
    var el = document.getElementById('docGenDrop-' + id);
    if (el) el.classList.remove('drag-over');
    if (!e.dataTransfer) return;
    var files = await collectDroppedFiles(e.dataTransfer);
    if (files.length) docGenUploadFiles(id, files);
  };

  window.docGenUploadFiles = async function (id, files) {
    var g = findGruppo(id);
    var client = getSb();
    if (!g || !files || !files.length) return;
    if (!client) {
      toast('Upload non disponibile — ricarica la pagina admin', 'error');
      return;
    }

    g.file = normalizeFileList(g.file);
    var uploaded = 0;
    var skipped = 0;
    var batchId = Date.now();
    var list = Array.prototype.slice.call(files);

    for (var i = 0; i < list.length; i++) {
      var file = list[i];
      if (shouldSkipFile(file)) {
        skipped++;
        continue;
      }
      if (!isAllowedDocFile(file)) {
        skipped++;
        continue;
      }
      if (file.size > DOC_GEN_MAX_MB * 1024 * 1024) {
        toast('File troppo grande (max ' + DOC_GEN_MAX_MB + ' MB): ' + getRelPath(file), 'error');
        skipped++;
        continue;
      }
      var ext = (file.name.split('.').pop() || 'bin').toLowerCase();
      var path = buildStoragePath(g, file, batchId);
      var mime = file.type || 'application/octet-stream';
      if (ext === 'zip' && !mime) mime = 'application/zip';

      try {
        var up = await client.storage.from('documenti').upload(path, file, {
          cacheControl: '3600',
          upsert: false,
          contentType: mime
        });
        if (up.error) {
          toast('Errore upload: ' + up.error.message, 'error');
          continue;
        }
        var publicUrl = storagePublicUrl('documenti', path);
        if (!publicUrl) {
          toast('Upload ok ma URL non disponibile per: ' + getRelPath(file), 'error');
          continue;
        }
        g.file.push({
          url: publicUrl,
          nome: getRelPath(file),
          tipo: ext,
          ordine: g.file.length
        });
        uploaded++;
      } catch (err) {
        toast('Errore upload: ' + (err.message || err), 'error');
      }
    }

    if (!uploaded) {
      if (skipped) toast('Nessun file valido nella cartella (formati ammessi: Word, PDF, JPG, Excel, ZIP)', 'error');
      return;
    }

    try {
      await persistGruppo(g);
    } catch (e) {
      toast('Errore salvataggio elenco: ' + (e.message || e), 'error');
    }
    if (uploaded === 1) {
      toast('Caricato 1 file', 'success');
    } else {
      toast('Caricati ' + uploaded + ' file' + (skipped ? ' (' + skipped + ' ignorati)' : ''), 'success');
    }
    renderDocumentiGenerali();
    updateDocGenStats();
  };
})();
