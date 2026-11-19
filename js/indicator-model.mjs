// Private candidate. Policy must be provided explicitly; no database side effects.
export const knownTypes=Object.freeze({activity:'gi-15',pending:'gi-9',appointments:['gi-4','gi-3','gi-8','gi-13','gi-22']});
export function activitySignal({propertyId,events=[],tasks=[],practices=[],sources}){
 if(!propertyId||!Array.isArray(sources)||sources.some(x=>!['agenda','practices'].includes(x)))throw Error('Explicit source selection required');
 const agenda=sources.includes('agenda')?events.filter(e=>e.property_id===propertyId&&e.type_id===knownTypes.activity&&e.done===false&&!e.deleted_at):[];
 const practiceIds=new Set(practices.filter(p=>p.immobile_id===propertyId&&!p.eliminata_il&&!p.chiusa_il).map(p=>p.id));
 const practice=sources.includes('practices')?tasks.filter(t=>practiceIds.has(t.pratica_id)&&t.fatta!==true&&!t.eliminata_il):[];
 return {active:agenda.length+practice.length>0,agendaIds:agenda.map(e=>e.id),taskIds:practice.map(t=>t.id)};
}
export function eventCandidates({propertyId,events=[]}){return events.filter(e=>e.property_id===propertyId&&!e.deleted_at&&e.done===false&&[knownTypes.pending,...knownTypes.appointments].includes(e.type_id));}
export function eventSignal({events=[],temporalPolicy,now=new Date()}){
 if(!['all-unfinished','not-past'].includes(temporalPolicy))throw Error('Criterio temporale non ancora confermato');
 const instant=+now;if(!Number.isFinite(instant))throw Error('Data non valida');
 const eligible=events.filter(e=>!e.deleted_at&&e.done===false&&[knownTypes.pending,...knownTypes.appointments].includes(e.type_id));
 const selected=eligible.filter(e=>{if(temporalPolicy==='all-unfinished')return true;const value=e.ends_at||e.starts_at;if(!value||!Number.isFinite(+new Date(value)))throw Error('Data appuntamento non verificabile');return +new Date(value)>instant;});
 const bright=selected.filter(e=>knownTypes.appointments.includes(e.type_id)),pending=selected.filter(e=>e.type_id===knownTypes.pending);
 if(bright.length)return {kind:'green',label:'Appuntamenti aperti'+(pending.length?' e appuntamenti da confermare':''),eventIds:[...bright,...pending].map(e=>e.id)};
 if(pending.length)return {kind:'light',label:'Appuntamenti da confermare',eventIds:pending.map(e=>e.id)};
 return {kind:null,label:'',eventIds:[]};
}
