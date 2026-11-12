/* Candidato offline: nessuna chiamata o scrittura all'importazione del modulo. */
export function createPrivatePropertyAdapter({db,principal,isCurrent}){
 const same=()=>isCurrent()&&principal===globalThis.RighettoGatedPrincipal;
 async function auth(id){if(!same())throw Error('Scheda o sessione cambiata');const u=await db.auth.getUser();if(!same()||u.error||u.data?.user?.id!==principal)throw Error('Amministratore non verificato');const r=await db.from('immobili').select('id').eq('id',id).maybeSingle();if(!same()||r.error||r.data?.id!==id)throw Error('Immobile non verificato');}
 function valid(){if(!same())throw Error('Esito da verificare: scheda o sessione cambiata. Non ripetere il salvataggio con un nuovo ID.');}
 async function commentRow(id){const r=await db.from('immobile_cronistoria').select('id,immobile_id,tipo,testo,autore_id,versione').eq('id',id).maybeSingle();valid();if(r.error)throw r.error;return r.data;}
 async function saveComment({id,propertyId,text,previous=null}){
  if(!id||!propertyId||typeof text!=='string'||!text.trim()||text.length>20000)throw Error('Commento non valido');
  await auth(propertyId);const old=await commentRow(id);
  if(previous){if(old?.immobile_id===propertyId&&old.tipo==='commento'&&old.versione===previous.version&&old.testo===text&&old.testo===previous.text)return {confirmed:true,unchanged:true,row:old};if(old?.immobile_id===propertyId&&old.tipo==='commento'&&old.versione===previous.version+1&&old.testo===text)return {confirmed:true,recovered:true,row:old};if(!old||old.immobile_id!==propertyId||old.tipo!=='commento'||old.versione!==previous.version||old.testo!==previous.text)throw Error('Commento modificato altrove: ricarica prima di salvare');}
  else if(old){if(old.immobile_id===propertyId&&old.autore_id===principal&&old.tipo==='commento'&&old.testo===text)return {confirmed:true,recovered:true,row:old};throw Error('ID commento già usato: non sovrascrivo');}
  const value={id,immobile_id:propertyId,tipo:'commento',testo:text,autore_id:principal,versione:1};let write;
  try{write=previous?await db.from('immobile_cronistoria').update({testo:text,versione:previous.version+1}).eq('id',id).eq('immobile_id',propertyId).eq('versione',previous.version).eq('tipo','commento').select('id').maybeSingle():await db.from('immobile_cronistoria').insert(value).select('id').maybeSingle();}catch(e){write={error:e};}
  valid();const after=await commentRow(id);const version=previous?previous.version+1:1;
  if(after?.immobile_id===propertyId&&after.tipo==='commento'&&after.testo===text&&after.versione===version&&(!previous?after.autore_id===principal:true))return {confirmed:true,recovered:!!write?.error,row:after};
  if(write?.error)throw Error('Salvataggio non confermato. Mantieni la bozza e lo stesso ID per verificarlo: '+write.error.message);
  throw Error('Commento non confermato dal database. Mantieni la bozza, non creare un duplicato.');
 }
 return {saveComment};
}
