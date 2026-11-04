/* Private photo reader candidate. No writes, public URLs or automatic downloads. */
(function(){
'use strict';
let active=null;
const uuid=v=>/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(v||'');
function close(){if(!active)return;const a=active;active=null;a.closed=true;a.unsubscribe?.();a.observer?.disconnect();for(const u of a.urls)URL.revokeObjectURL(u);a.urls.clear();a.host.remove();}
async function open({db,property,isCurrent=()=>true}){
 close();if(!uuid(property?.id))throw Error('Apri una scheda immobile salvata.');
 const id=property.id,host=document.createElement('div');host.className='rpp-overlay';
 host.innerHTML='<section role="dialog" aria-modal="true" aria-labelledby="rpp-title"><header><h2 id="rpp-title"></h2><button type="button" data-close>Chiudi</button></header><p>Immagini riservate. Nessuna foto viene pubblicata o inviata.</p><p role="status">Verifica accesso...</p><div data-list></div></section>';
 host.querySelector('h2').textContent='Foto private - '+(property.codice||'immobile');document.body.append(host);
 const a={host,id,closed:false,urls:new Set(),principal:null};active=a;
 if(db.auth.onAuthStateChange){const sub=db.auth.onAuthStateChange((event,session)=>{if(active===a&&(!session?.user?.id||(a.principal&&session.user.id!==a.principal)))close();});a.unsubscribe=()=>sub.data?.subscription?.unsubscribe();}
 a.observer=new MutationObserver(()=>{if(active===a&&!isCurrent(id))close();});a.observer.observe(document.body,{subtree:true,childList:true,attributes:true,attributeFilter:['class','style']});
 const status=host.querySelector('[role=status]'),list=host.querySelector('[data-list]');
 const current=()=>active===a&&!a.closed&&host.isConnected&&isCurrent(id);
 host.querySelector('[data-close]').onclick=close;host.onclick=e=>{if(e.target===host)close();};
 async function authorized(){
  if(!current())throw Error('Scheda non piu aperta.');
  const u=await db.auth.getUser();if(u.error||!u.data?.user?.id)throw Error('Accedi di nuovo.');
  const who=u.data.user.id;if(a.principal&&a.principal!==who)throw Error('Sessione cambiata.');
  const admin=await db.rpc('righetto_is_admin_request');if(admin.error||admin.data!==true)throw Error('Accesso amministratore non verificato.');
  const again=await db.auth.getUser();if(again.error||again.data?.user?.id!==who||!current())throw Error('Sessione cambiata.');
  a.principal=who;return true;
 }
 function fail(error){if(current()){list.replaceChildren();for(const u of a.urls)URL.revokeObjectURL(u);a.urls.clear();status.textContent='Foto non disponibili: '+error.message;}}
 try{
  await authorized();
  const result=await db.from('immobile_media_privati').select('id,immobile_id,originale_percorso,originale_sha256,originale_mime,originale_byte,tipo_media').eq('immobile_id',id).range(0,999);
  await authorized();if(result.error||!Array.isArray(result.data))throw Error('Lettura archivio non riuscita.');
  if(result.data.length>=1000)throw Error('Elenco oltre il limite: lettura incompleta.');
  const rows=result.data.filter(r=>r.tipo_media==='foto');
  for(const r of rows){
   const path='immobili/'+id+'/media/'+r.id+'.'+({'image/jpeg':'jpg','image/png':'png','image/webp':'webp'}[r.originale_mime]||'invalid');
   if(r.immobile_id!==id||!uuid(r.id)||r.originale_percorso!==path||!Number.isSafeInteger(r.originale_byte)||r.originale_byte<=0||r.originale_byte>20*1024*1024||!/^[0-9a-f]{64}$/.test(r.originale_sha256))throw Error('Riferimento foto non verificato.');
  }
  status.textContent=rows.length?rows.length+' foto private. Apri una foto per visualizzarla.':'Nessuna foto privata presente.';
  rows.forEach((r,n)=>{
   const card=document.createElement('article'),title=document.createElement('h3'),button=document.createElement('button'),output=document.createElement('div');title.textContent='Foto privata '+(n+1);button.textContent='Apri foto';button.type='button';card.append(title,button,output);list.append(card);
   button.onclick=async()=>{
    button.disabled=true;button.textContent='Verifica in corso...';let local=null;
    try{
     await authorized();const file=await db.storage.from('documenti').download(r.originale_percorso);if(file.error||!(file.data instanceof Blob))throw Error('Download privato non riuscito.');
     const blob=file.data;if(blob.size!==r.originale_byte)throw Error('Dimensione foto diversa.');
     const hash=[...new Uint8Array(await crypto.subtle.digest('SHA-256',await blob.arrayBuffer()))].map(v=>v.toString(16).padStart(2,'0')).join('');if(hash!==r.originale_sha256)throw Error('Impronta foto diversa.');
     await authorized();local=URL.createObjectURL(new Blob([blob],{type:r.originale_mime}));a.urls.add(local);
     const image=document.createElement('img');image.alt='Foto privata '+(n+1);image.src=local;const hide=document.createElement('button');hide.type='button';hide.textContent='Chiudi foto';hide.onclick=()=>{URL.revokeObjectURL(local);a.urls.delete(local);output.replaceChildren();button.disabled=false;button.textContent='Apri foto';};output.replaceChildren(image,hide);button.textContent='Foto aperta';
    }catch(e){if(local){URL.revokeObjectURL(local);a.urls.delete(local);}fail(e);}
   };
  });
 }catch(e){fail(e);}
 return {close};
}
function style(){if(document.getElementById('rpp-style'))return;const s=document.createElement('style');s.id='rpp-style';s.textContent='.rpp-overlay{position:fixed;inset:0;background:#18314999;z-index:15000;overflow:auto;padding:16px;font:15px/1.45 Arial;color:#17324d}.rpp-overlay section{max-width:850px;background:white;margin:3vh auto;padding:20px;border-radius:10px}.rpp-overlay header{display:flex;align-items:center;justify-content:space-between;gap:12px}.rpp-overlay h2{font-size:21px;margin:0}.rpp-overlay article{border:1px solid #c5d1d9;padding:12px;margin:10px 0;border-radius:6px}.rpp-overlay h3{font-size:16px;margin:0 0 8px}.rpp-overlay button{font:600 14px Arial;background:#edf3f7;color:#17324d;border:1px solid #9ab1c3;border-radius:6px;min-height:40px;padding:8px 12px;cursor:pointer}.rpp-overlay img{display:block;max-width:100%;max-height:65vh;margin:12px auto;object-fit:contain}@media(max-width:600px){.rpp-overlay{padding:8px}.rpp-overlay section{padding:14px;margin:12px auto}.rpp-overlay h2{font-size:18px}}';document.head.append(s);}
window.RighettoPrivatePhotos={open:async args=>{style();return open(args);},close};
window.addEventListener('pagehide',close);window.addEventListener('righetto-logout',close);
})();
