import { createAssignmentsModel } from './property-agent-model.mjs';
// Read-only. The caller owns the catalogue snapshot and disposes this reader on navigation/logout.
export function createAssignmentsReader({ db, principal, propertyIds, isCurrent, principalNow, timeoutMs = 20000 }) {
  const ids = [...propertyIds], snapshot = JSON.stringify(ids);
  let generation = 0, pending = null;
  function assert(ticket) { if (ticket !== generation || !principal || principalNow() !== principal || !isCurrent() || JSON.stringify(propertyIds) !== snapshot) throw Error('Catalogo o sessione cambiati'); }
  async function authenticate(ticket) { assert(ticket); const u = await db.auth.getUser(); assert(ticket); if (u.error || u.data?.user?.id !== principal) throw Error('Identità non verificata'); const a = await db.rpc('righetto_is_admin_request'); assert(ticket); if (a.error || a.data !== true) throw Error('Accesso amministratore non verificato'); }
  function stop() { generation++; pending?.abort(); pending = null; }
  async function load() {
    stop(); const ticket = generation, control = new AbortController(); pending = control;
    const timer = setTimeout(() => control.abort(), timeoutMs);
    async function read(query, label) { assert(ticket); const r = await query.abortSignal(control.signal); assert(ticket); if (control.signal.aborted || r.error || !Array.isArray(r.data)) throw Error(label + ' non verificati'); return r.data; }
    try {
      await authenticate(ticket);
      const catalogs = await read(db.from('immobile_cataloghi').select('id,fonte,tipo,contesto_voce_id,verificato_il,fonte_url').eq('fonte', 'gestionaleimmobiliare').in('tipo', ['agente']).order('id'), 'Cataloghi');
      const catalogIds = catalogs.map(c => c.id), entries = [], links = [];
      if (catalogIds.length > 1) throw Error('Cataloghi assegnazioni duplicati');
      if (catalogIds.length) {
        let completed = false;
        for (let offset = 0; offset < 20000; offset += 500) {
          const page = await read(db.from('immobile_cataloghi_voci').select('id,catalogo_id,fonte_id,etichetta').in('catalogo_id', catalogIds).order('id').range(offset, offset + 499), 'Voci');
          entries.push(...page); if (page.length < 500) { completed = true; break; }
        }
        if (!completed) throw Error('Catalogo troppo ampio, lettura interrotta');
      }
      for (let i = 0; i < ids.length; i += 100) {
        const page = await read(db.from('immobile_cataloghi_collegamenti').select('immobile_id,tipo,catalogo_id,voce_id,versione').in('immobile_id', ids.slice(i,i+100)).in('tipo', ['agente']).order('immobile_id').order('tipo'), 'Collegamenti');
        if (page.length > 200) throw Error('Numero collegamenti incompatibile');
        links.push(...page);
      }
      await authenticate(ticket);
      const model = createAssignmentsModel({ catalogs, entries, links, propertyIds: ids });
      assert(ticket); return model;
    } finally { clearTimeout(timer); if (ticket === generation) pending = null; }
  }
  return Object.freeze({ load, dispose: stop });
}
