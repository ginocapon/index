// Private read-only candidate. No default assignment and no writes.
const kinds = new Set(['agente']);
export function createAssignmentsModel({ catalogs, entries, links, propertyIds }) {
  if (![catalogs, entries, links, propertyIds].every(Array.isArray)) throw Error('Dati collegamenti non verificati');
  const properties = new Set(propertyIds.map(String));
  if (properties.size !== propertyIds.length || propertyIds.some(x => !x)) throw Error('Identità immobili duplicate o mancanti');
  const byCatalog = new Map(), byEntry = new Map(), root = new Map(), assigned = new Map();
  for (const c of catalogs) {
    if (!c.id || byCatalog.has(c.id)) throw Error('Catalogo duplicato o senza identità');
    byCatalog.set(c.id, c);
    if (!kinds.has(c.tipo)) continue;
    if (c.fonte !== 'gestionaleimmobiliare' || c.contesto_voce_id != null) throw Error('Fonte catalogo assegnazioni non verificata');
    if (root.has(c.tipo)) throw Error('Più cataloghi per lo stesso tipo');
    root.set(c.tipo, c);
  }
  for (const e of entries) {
    if (!e.id || byEntry.has(e.id)) throw Error('Voce duplicata o senza identità');
    const c = byCatalog.get(e.catalogo_id);
    if (!c || !kinds.has(c.tipo) || !String(e.etichetta || '').trim() || !String(e.fonte_id || '').trim() || ['0', 'all', 'q', '-'].includes(String(e.fonte_id))) throw Error('Voce non verificata');
    byEntry.set(e.id, e);
  }
  for (const l of links) {
    if (!kinds.has(l.tipo)) continue;
    const property = String(l.immobile_id || ''), c = root.get(l.tipo), e = byEntry.get(l.voce_id), key = property + ':' + l.tipo;
    if (!properties.has(property) || !c || c.id !== l.catalogo_id || !e || e.catalogo_id !== c.id || assigned.has(key)) throw Error('Collegamento estraneo, duplicato o incompatibile');
    assigned.set(key, e.id);
  }
  function choices(kind) {
    if (!kinds.has(kind)) throw Error('Tipo assegnazione non valido');
    const c = root.get(kind);
    if (!c) return [];
    return entries.filter(e => e.catalogo_id === c.id).map(e => ({ id: e.id, sourceId: e.fonte_id, label: e.etichetta })).sort((a,b) => a.label.localeCompare(b.label, 'it', { sensitivity: 'base', numeric: true }) || a.id.localeCompare(b.id));
  }
  function status(propertyId, kind) {
    if (!properties.has(String(propertyId)) || !kinds.has(kind)) throw Error('Identità non verificata');
    const id = assigned.get(String(propertyId) + ':' + kind);
    return id ? { state: 'linked', id, label: byEntry.get(id).etichetta } : { state: 'unlinked', id: null, label: null };
  }
  function filter(rows, selection = {}) {
    if (!Array.isArray(rows) || Object.keys(selection).some(k => !kinds.has(k))) throw Error('Filtro non valido');
    const active = Object.entries(selection).filter(([,v]) => v != null && v !== '');
    for (const [kind,id] of active) if (!choices(kind).some(e => e.id === id)) throw Error('Scelta filtro estranea al catalogo');
    let excludedUnlinked = 0;
    const seen = new Set(), visible = [];
    for (const row of rows) {
      const id = String(row.id || '');
      if (!properties.has(id) || seen.has(id)) throw Error('Righe immobili estranee o duplicate');
      seen.add(id);
      const values = active.map(([kind,choice]) => ({ state: status(id,kind), choice }));
      if (values.some(v => v.state.state === 'unlinked')) excludedUnlinked++;
      if (values.every(v => v.state.id === v.choice)) visible.push(row);
    }
    return { rows: visible, excludedUnlinked, total: rows.length, activeFilters: active.length, filterCoverageComplete: active.length ? excludedUnlinked === 0 : null };
  }
  return Object.freeze({ choices, status, filter });
}
