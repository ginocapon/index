/* PRIVATE CANDIDATE. Pure routing only: never sends, opens, writes or logs a message. */
(function(root){
'use strict';
const ORIGIN='https://righettoimmobiliare.it';
function resolve(property,manifest,slugFor,catalogue){
  if(!property || !property.id) return {ok:false,reason:'Immobile non identificato.'};
  if(property.attivo!==true || property.venduto===true || property.affittato===true) return {ok:false,reason:'Immobile non pubblicato: anteprima WhatsApp non disponibile.'};
  if(!manifest || !manifest.bySlug || !manifest.byCodice) return {ok:false,reason:'Elenco anteprime non disponibile. Nessun messaggio aperto.'};
  const currentSlug=typeof slugFor==='function'?slugFor(property):'';
  const rawCode=String(property.codice||'').toUpperCase(), code=rawCode.trim();
  if(!code && (!Array.isArray(catalogue) || catalogue.filter(x=>x && typeof slugFor==='function' && slugFor(x)===currentSlug).length!==1 || !catalogue.some(x=>x.id===property.id))) return {ok:false,reason:'Immobile senza codice: identita anteprima non univoca.'};
  const entry=manifest.bySlug[currentSlug] || manifest.byCodice[code] || manifest.byCodice[rawCode];
  if(!entry || !entry.share_file || !entry.seo_slug) return {ok:false,reason:'Anteprima non ancora pubblicata per questo immobile.'};
  if(currentSlug!==entry.seo_slug || (code && String(entry.codice||'').trim().toUpperCase()!==code)) return {ok:false,reason:'Anteprima da aggiornare dopo la modifica dell’immobile.'};
  const exactFile='share-immobile-'+entry.seo_slug+'.html';
  if(entry.share_file!==exactFile) return {ok:false,reason:'File anteprima non valido.'};
  let u;try{u=new URL(entry.share_file,ORIGIN+'/');}catch(e){return {ok:false,reason:'Link anteprima non valido.'};}
  if(u.origin!==ORIGIN || u.search || u.hash || u.username || u.password || !/^\/share-immobile-[a-z0-9-]+\.html$/.test(u.pathname)) return {ok:false,reason:'Link anteprima non valido.'};
  if(u.pathname!=='/share-immobile-'+entry.seo_slug+'.html') return {ok:false,reason:'Anteprima non corrispondente all’immobile.'};
  return {ok:true,url:u.href};
}
function resolveAll(properties,manifest,slugFor,catalogue){
  const rows=properties.map(property=>({property,result:resolve(property,manifest,slugFor,catalogue)}));
  const failed=rows.filter(x=>!x.result.ok);
  return failed.length?{ok:false,failed}:{ok:true,rows};
}
const api=Object.freeze({resolve,resolveAll});
if(typeof module!=='undefined' && module.exports)module.exports=api;
else root.RighettoSharePreview=api;
})(typeof window!=='undefined'?window:globalThis);

window.righettoLoadShareManifest=(function(){let pending;return function(){
 if(!pending)pending=fetch('data/og-immobili.json',{cache:'no-store',credentials:'omit'}).then(r=>{if(!r.ok)throw Error('Elenco anteprime non disponibile.');return r.json();}).catch(e=>{pending=null;throw e;});
 return pending;
};})();
window.righettoShareForProperty=async function(property){
 const principal=window.RighettoGatedPrincipal;
 if(!principal||!property||!property.id)return {ok:false,reason:'Scheda o accesso non disponibile.'};
 try{
  const result=await sb.from('immobili').select('id,codice,tipologia,categoria,tipo_operazione,comune,attivo,venduto,affittato,cestino').eq('id',property.id).maybeSingle();
  if(window.RighettoGatedPrincipal!==principal)return {ok:false,reason:'Accesso cambiato. Riapri la scheda.'};
  if(result.error||!result.data||result.data.cestino)return {ok:false,reason:'Immobile non disponibile per la condivisione.'};
  const manifest=await righettoLoadShareManifest();
  if(window.RighettoGatedPrincipal!==principal)return {ok:false,reason:'Accesso cambiato. Riapri la scheda.'};
  return RighettoSharePreview.resolve(result.data,manifest,generatePropertySlug,typeof allImmobili!=='undefined'?allImmobili:null);
 }catch(e){return {ok:false,reason:'Anteprima non verificata. Nessun link copiato.'};}
};
