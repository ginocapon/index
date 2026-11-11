import {DICTIONARY_HASH} from './request-dictionaries.mjs';
const plain=x=>!!x&&typeof x==='object'&&!Array.isArray(x);
const exact=(x,keys)=>plain(x)&&Object.keys(x).length===keys.length&&keys.every(k=>Object.hasOwn(x,k));
export function normalizePropertyTypes(value,d){
 if(value===null)return null;
 if(!d||d.version!==DICTIONARY_HASH||!exact(value,['version','dictionary_version','classifications'])||value.version!==1||value.dictionary_version!==d.version||!Array.isArray(value.classifications)||value.classifications.length>50)throw Error('Tipologie aggiuntive: formato o dizionario non verificato');
 const seen=new Set(),rows=[];
 for(const item of value.classifications){if(!exact(item,['specific_id','detailed_id'])||typeof item.specific_id!=='string'||!d.specific[item.specific_id]||!(item.detailed_id===null||typeof item.detailed_id==='string'&&d.detailed[item.detailed_id]?.specific_id===item.specific_id))throw Error('Tipologia aggiuntiva non presente nella gerarchia verificata');const key=item.specific_id+':'+(item.detailed_id??'');if(seen.has(key))throw Error('Tipologie aggiuntive duplicate');seen.add(key);rows.push({...item});}
 rows.sort((a,b)=>Number(a.specific_id)-Number(b.specific_id)||Number(a.detailed_id)-Number(b.detailed_id));
 return{version:1,dictionary_version:d.version,classifications:rows};
}
export function additionalChains(property,d){if(!Object.hasOwn(property,'tipologie_ricerca'))throw Error('Tipologie aggiuntive non lette: confronto incompleto');const value=normalizePropertyTypes(property.tipologie_ricerca,d);return(value?.classifications||[]).map(x=>{const specific=d.specific[x.specific_id],generic=d.generic[specific.generic_id];return{specific_type_id:x.specific_id,detailed_type_id:x.detailed_id,generic_id:specific.generic_id,sector:generic.sector,source:'explicit-additional'};});}
export function compareTypeChains(criteria,chains){
 const failed=[],unknown=[],checked=[];if(!chains.length)return{state:'review',failed,unknown:['Nessuna classificazione immobile verificata'],checked};
 const evaluate=chain=>{const no=[],missing=[];if(!chain.sector)missing.push('Settore immobile non verificato');else if(chain.sector!==criteria.sector)no.push('Settore diverso');for(const[key,field,label]of [['generic','generic_id','Gruppo tipologia'],['specific','specific_type_id','Tipologia specifica'],['detailed','detailed_type_id','Microtipologia']]){if(!criteria.types[key].length)continue;if(!chain[field])missing.push(label+' immobile non verificata');else if(!criteria.types[key].includes(String(chain[field])))no.push(label+' fuori dai criteri');}return{chain,failed:no,unknown:missing,state:no.length?'excluded':missing.length?'review':'match'};};
 const evaluated=chains.map(evaluate),winner=evaluated.find(x=>x.state==='match');if(winner)return{state:'match',failed:[],unknown:[],checked:['Settore e tipologie nella stessa classificazione verificata'],matched_chain:winner.chain};
 const pending=evaluated.filter(x=>x.state==='review');if(pending.length)return{state:'review',failed:[],unknown:[...new Set(pending.flatMap(x=>x.unknown))],checked:[]};
 return{state:'excluded',failed:['Nessuna tipologia dell’immobile rispetta insieme settore, gruppo, tipo e dettaglio della richiesta'],unknown:[],checked:[]};
}
export function makePropertyTypes(items,d){return normalizePropertyTypes({version:1,dictionary_version:d.version,classifications:items},d);}
