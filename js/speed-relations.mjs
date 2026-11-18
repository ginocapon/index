const OWNER='5f55e259-0d0b-46d9-8d77-17ab33db0fdf';
function unique(rows,key='id'){const s=new Set();for(const r of rows){const k=r[key];if(!k||s.has(k))throw Error('ID mancanti o ripetuti');s.add(k);}return s;}
export function reconcileRelations({properties,owners,practices,events,requests,clients,clientTotal,window,observedAt}){
 const pids=unique(properties),cids=unique(clients);unique(practices);unique(events);unique(requests);
 const link=(rows,key,targets)=>({present:rows.filter(r=>r[key]).length,valid:rows.filter(r=>r[key]&&targets.has(r[key])).length,missing:rows.filter(r=>r[key]&&!targets.has(r[key])).map(r=>r.id||[r.immobile_id,r.cliente_id].join(':'))});
 const liveEvents=events.filter(r=>!r.deleted_at),livePractices=practices.filter(r=>!r.eliminata_il);
 const typeCounts={};for(const r of liveEvents)typeCounts[r.type_id||'non documentato']=(typeCounts[r.type_id||'non documentato']||0)+1;
 const pairs=new Set();for(const r of owners){const k=r.immobile_id+':'+r.cliente_id;if(pairs.has(k))throw Error('Associazione proprietario ripetuta');pairs.add(k);}
 const po=owners.filter(r=>pids.has(r.immobile_id)&&cids.has(r.cliente_id));
 const both=liveEvents.filter(r=>r.client_id&&r.property_id&&cids.has(r.client_id)&&pids.has(r.property_id));
 return {observedAt,window,clientTotal,properties:properties.length,ownerAssociations:{total:owners.length,valid:po.length,missing:owners.length-po.length,uniqueClients:new Set(po.map(r=>r.cliente_id)).size,uniqueProperties:new Set(po.map(r=>r.immobile_id)).size},primaryOwners:link(properties,'proprietario_id',cids),requestProperties:link(requests,'immobile_id',pids),practices:{total:practices.length,notDeleted:livePractices.length,clientLinks:link(livePractices,'cliente_id',cids),propertyLinks:link(livePractices,'immobile_id',pids)},agenda:{total:events.length,notDeleted:liveEvents.length,clientLinks:link(liveEvents,'client_id',cids),propertyLinks:link(liveEvents,'property_id',pids),bothLinked:both.length,uniqueClients:new Set(both.map(r=>r.client_id)).size,types:typeCounts},mandateMetadata:{withType:properties.filter(r=>r.tipo_incarico).length,withStart:properties.filter(r=>r.incarico_inizio).length,withExpiry:properties.filter(r=>r.incarico_scadenza).length,signedMandates:null},conversion:{requestToClient:null,source:'Le richieste non hanno un cliente_id verificato. Nessun abbinamento per nome, email o telefono.'}};
}
export function createRelationsReader({sb,onClear=()=>{}}){
 let epoch=0,stopped=false,controller=null;
 const clear=()=>{epoch++;controller?.abort();onClear();};const sub=sb.auth.onAuthStateChange((_e,s)=>{if(s?.user?.id!==OWNER)clear();});
 const owner=async()=>{const r=await sb.auth.getUser();if(r.error||r.data?.user?.id!==OWNER)throw Error('Accesso non verificato');};
 return {stop(){stopped=true;clear();sub.data?.subscription?.unsubscribe();},async read(window){
 clear();const ticket=epoch;controller=new AbortController();const signal=controller.signal,current=()=>!stopped&&epoch===ticket&&!signal.aborted;
 const read=async(table,fields,filter=q=>q)=>{const rows=[];let total=null;for(let offset=0;offset<10000;offset+=200){let q=sb.from(table).select(fields,{count:'exact'});q=filter(q);q=q.order(table==='immobile_proprietari'?'immobile_id':'id');if(table==='immobile_proprietari')q=q.order('cliente_id');const r=await q.range(offset,offset+199).abortSignal(signal);if(!current()||r.error||!Array.isArray(r.data)||!Number.isInteger(r.count))throw Error('Fonte non verificata: '+table);if(total===null)total=r.count;if(total!==r.count||total>10000)throw Error('Fonte cambiata o limite superato');rows.push(...r.data);if(rows.length===total)return rows;if(!r.data.length)throw Error('Fonte incompleta');}throw Error('Limite lettura');};
 await owner();if(!current())throw Error('Sessione cambiata');
 if(!window?.start||!window?.end||!Number.isFinite(Date.parse(window.start))||Date.parse(window.end)<=Date.parse(window.start))throw Error('Periodo non verificato');
 const properties=await read('immobili','id,proprietario_id,tipo_incarico,incarico_inizio,incarico_scadenza,cestino');
 const owners=await read('immobile_proprietari','immobile_id,cliente_id,ordine');
 const practices=await read('pratiche','id,cliente_id,immobile_id,eliminata_il,chiusa_il');
 const events=await read('agenda_events','id,type_id,starts_at,property_id,client_id,deleted_at',q=>q.gte('starts_at',window.start).lt('starts_at',window.end));
 const requests=await read('richieste','id,immobile_id');
 const refIds=[...new Set([...properties.map(r=>r.proprietario_id),...owners.map(r=>r.cliente_id),...practices.map(r=>r.cliente_id),...events.map(r=>r.client_id)].filter(Boolean))];
 const clients=[];for(let i=0;i<refIds.length;i+=100){clients.push(...await read('clienti','id',q=>q.in('id',refIds.slice(i,i+100))));}
 const c=await sb.from('clienti').select('id',{count:'exact',head:true}).abortSignal(signal);if(c.error||!Number.isInteger(c.count))throw Error('Totale clienti non verificato');
 await owner();if(!current())throw Error('Sessione cambiata');return reconcileRelations({properties,owners,practices,events,requests,clients,clientTotal:c.count,window,observedAt:new Date().toISOString()});
 }};
}
