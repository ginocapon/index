/* Dati tabella da relazioni esistenti, mai inferiti dal nome del comune. */
(function(){'use strict';let epoch=0,pending=null;
 const timeout=15000;
 async function render(){const ticket=++epoch;pending?.abort();const controller=new AbortController();pending=controller;const timer=setTimeout(()=>controller.abort(),timeout),principal=window.RighettoGatedPrincipal;const rows=[...document.querySelectorAll('#immobiliTableWrap tr[data-property-preview]')],ids=rows.map(r=>r.dataset.propertyPreview);const current=()=>ticket===epoch&&principal===window.RighettoGatedPrincipal&&rows.every(r=>r.isConnected);if(!principal||!ids.length){clearTimeout(timer);return;}
 const values=new Map(ids.map(id=>[id,{count:0}]));
 try{const u=await sb.auth.getUser();if(!current())return;if(u.error||u.data?.user?.id!==principal)throw Error('Sessione non verificata');
 for(let start=0;start<ids.length;start+=100){const chunk=ids.slice(start,start+100);
  const ratings=await sb.from('immobile_dati_privati').select('immobile_id,punteggio_fonte,punteggio_fonte_il').in('immobile_id',chunk).abortSignal(controller.signal);if(!current())return;if(ratings.error)throw ratings.error;for(const r of ratings.data){const v=values.get(r.immobile_id);if(v){v.score=r.punteggio_fonte;v.scoreDate=r.punteggio_fonte_il;}}
  const links=await sb.from('immobile_cataloghi_collegamenti').select('immobile_id,tipo,voce_id').in('immobile_id',chunk).in('tipo',['nazione','provincia','zona_locale']).abortSignal(controller.signal);if(!current())return;if(links.error)throw links.error;
  const keys=[...new Set(links.data.map(x=>x.voce_id).filter(Boolean))];let labels=new Map();if(keys.length){const r=await sb.from('immobile_cataloghi_voci').select('id,etichetta').in('id',keys).abortSignal(controller.signal);if(!current())return;if(r.error)throw r.error;labels=new Map(r.data.map(v=>[v.id,v.etichetta]));}
  for(const link of links.data){const value=labels.get(link.voce_id);if(value)values.get(link.immobile_id)[link.tipo]=value;}
  let n=0;for(;;){const events=await sb.from('agenda_events').select('id,property_id').in('property_id',chunk).is('deleted_at',null).order('id').range(n,n+499).abortSignal(controller.signal);if(!current())return;if(events.error)throw events.error;if(!Array.isArray(events.data))throw Error('Eventi non verificati');for(const e of events.data){const v=values.get(e.property_id);if(v)v.count++;}if(events.data.length<500)break;n+=500;if(n>=20000)throw Error('Conteggio oltre il limite verificabile');}
 }
 if(!current())return;for(const row of rows){const v=values.get(row.dataset.propertyPreview);for(const cell of row.querySelectorAll('[data-pv-related]')){const key=cell.dataset.pvRelated,raw=v[key];cell.textContent=raw??'—';cell.title=key==='score'?'Punteggio osservato nella fonte, non ricalcolato'+(v.scoreDate?' il '+new Date(v.scoreDate).toLocaleString('it-IT'):''):key==='count'?'Eventi già salvati e collegati nel nuovo gestionale; non include dati vecchi ancora da recuperare':raw?'Valore collegato alla scheda':'Dato non ancora collegato alla scheda';}}
 }catch(e){if(current())for(const row of rows)for(const cell of row.querySelectorAll('[data-pv-related]')){cell.textContent='—';cell.title='Dato non verificato: '+(e.name==='AbortError'?'tempo scaduto':e.message||'errore');}}
 finally{clearTimeout(timer);if(ticket===epoch)pending=null;}}
 if(typeof sb!=='undefined')sb.auth.onAuthStateChange?.(event=>{if(event==='SIGNED_OUT'){++epoch;pending?.abort();document.querySelectorAll('[data-pv-related]').forEach(c=>{c.textContent='—';c.title='Sessione terminata';});}});
 window.RighettoPropertyTableData={render};
})();
