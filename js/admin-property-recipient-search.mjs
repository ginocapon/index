/* Isolated candidate, read-only. No sends, request records or client edits. */
const fields='id,nome,nome_proprio,cognome,email,telefono,cellulare,telefono_secondario,storico';
const nameFields=['nome','nome_proprio','cognome'];
const phoneFields=['telefono','cellulare','telefono_secondario'];
const digits=x=>String(x??'').replace(/\D/g,'');
const norm=x=>String(x??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('it').replace(/\s+/g,' ').trim();
function pattern(s){return '"%'+String(s).replace(/[\\%_"]/g,'\\$&')+'%"';}
export function plan(raw){
 const term=String(raw??'').trim();if(term.length<2)throw Error('Inserisci almeno 2 caratteri.');
 if(term.length>160||/[\u0000-\u001f]/.test(term))throw Error('Ricerca non valida.');
 const phone=/^[+\d\s()./-]+$/.test(term)&&digits(term).length>=4;
 if(phone){const value=digits(term);if(value.length>18)throw Error('Numero troppo lungo.');return {kind:'phone',term,value,groups:[phoneFields.map(k=>k+'.ilike."%'+value.split('').join('%')+'%"').join(',')]};}
 if(term.includes('@'))return {kind:'email',term,value:norm(term),groups:['email.ilike.'+pattern(term)]};
 const words=term.split(/\s+/).filter(Boolean);return {kind:'name',term,words,groups:words.map(w=>nameFields.map(k=>k+'.ilike.'+pattern(w)).join(','))};
}
export function matches(row,p){
 if(p.kind==='phone')return phoneFields.some(k=>digits(row[k]).includes(p.value));
 if(p.kind==='email')return norm(row.email).includes(p.value);
 const hay=norm(nameFields.map(k=>row[k]||'').join(' '));return p.words.every(w=>hay.includes(norm(w)));
}
export function createRecipientSearch({db,principal,isCurrent=()=>true}){
 let epoch=0,disposed=false;
 const alive=t=>!disposed&&t===epoch&&isCurrent()&&!!principal;
 async function auth(t){const u=await db.auth.getUser();if(!alive(t)||u.error||u.data?.user?.id!==principal)throw Error('Sessione o ricerca cambiata.');}
 return Object.freeze({
  cancel(){epoch++;},dispose(){epoch++;disposed=true;},
  async search(raw){const ticket=++epoch,p=plan(raw);await auth(ticket);let q=db.from('clienti').select(fields);for(const group of p.groups)q=q.or(group);const r=await q.order('nome',{ascending:true}).order('id',{ascending:true}).limit(51);await auth(ticket);if(r.error||!Array.isArray(r.data))throw Error('Archivio clienti non leggibile. Riprova.');if(r.data.some(x=>!x.id))throw Error('Scheda cliente senza identità verificabile.');const unique=new Map();for(const x of r.data)if(matches(x,p))unique.set(String(x.id),x);return {query:p.term,rows:[...unique.values()].slice(0,50),needsRefinement:r.data.length>50};},
  async verify(id){const ticket=++epoch;await auth(ticket);const r=await db.from('clienti').select(fields).eq('id',id).maybeSingle();await auth(ticket);if(r.error||!r.data||String(r.data.id)!==String(id))throw Error('Cliente selezionato non più verificabile. Cerca nuovamente.');return r.data;}
 });
}
