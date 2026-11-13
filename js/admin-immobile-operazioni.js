/* Menu Operazioni nella scheda immobile. Nessun invio a terzi, nessuna pubblicazione, nessuna cancellazione definitiva.
   Le azioni che scrivono dati (duplica, venduto) chiedono conferma e mostrano cosa cambia. */
(function(){
'use strict';
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function css(){if(document.getElementById('rio-css'))return;const s=document.createElement('style');s.id='rio-css';s.textContent=
'.rio-wrap{position:relative;display:inline-block}.rio-menu{position:absolute;right:0;top:38px;z-index:9000;background:#fff;border:1px solid #00508f;border-radius:8px;min-width:250px;max-width:92vw;box-shadow:0 8px 30px #0003;max-height:70vh;overflow:auto}'+
'.rio-menu button{display:block;width:100%;text-align:left;border:0;background:#fff;padding:11px 14px;font:600 14px Arial,sans-serif;color:#17324d;cursor:pointer;border-bottom:1px solid #eef2f5}.rio-menu button:hover{background:#eef4fa}'+
'#rio-ov #rio-list{display:flex;flex-direction:column;align-items:stretch;gap:0;border:1px solid #b9c7d1;border-radius:8px;max-height:65vh;overflow:auto}#rio-ov #rio-list>button{display:block;width:100%;box-sizing:border-box;margin:0;border:0;border-bottom:1px solid #e1e8ed;border-radius:0;text-align:left;background:#fff;min-height:44px;padding:10px 14px}#rio-ov #rio-list>button:hover{background:#eef4fa}#rio-ov #rio-list>.rio-unavailable{margin:0;text-align:left}'+
'.rio-unavailable{padding:10px 14px;font:12px Arial;color:#697b86;background:#f2f4f6}.rio-menu details{padding:8px 14px;font:13px Arial,sans-serif;color:#566773}.rio-menu details summary{cursor:pointer;font-weight:700}'+
'.rio-ov{position:fixed;inset:0;z-index:13000;background:#18314980;overflow:auto;padding:14px;font:15px/1.45 Arial,sans-serif;color:#17324d}.rio-box{max-width:620px;margin:6vh auto;background:#fff;border-radius:12px;padding:18px 20px;box-shadow:0 12px 50px #0004}'+
'.rio-box h3{margin:0 0 10px}.rio-box button{font:600 14px Arial,sans-serif;min-height:40px;border:1px solid #b9c7d1;border-radius:8px;background:#f3f6f8;color:#17324d;padding:8px 14px;cursor:pointer;margin:4px 6px 0 0}.rio-box button.pri{background:#00508f;color:#fff;border-color:#00508f}'+
'.rio-box pre{white-space:pre-wrap;background:#f6f8fa;border:1px solid #dde5ec;border-radius:8px;padding:10px;font:13px/1.45 Arial,sans-serif;max-height:45vh;overflow:auto}.rio-box label{display:block;margin:8px 0}.rio-box input[type=text],.rio-box input[type=number]{width:100%;padding:8px;border:1px solid #b9c7d1;border-radius:6px;font-size:15px}'+
'@media(max-width:700px){.rio-menu{position:fixed;left:10px;right:10px;top:auto;bottom:10px;max-height:62vh}}';
document.head.appendChild(s);}
function cur(){const id=(document.getElementById('editId')||{}).value;if(!id)return null;return (typeof allImmobili!=='undefined'?allImmobili:[]).find(x=>String(x.id)===String(id))||null;}
function url(i){try{return immobileAppUrl(i);}catch(e){return 'https://righettoimmobiliare.it/immobile?s='+encodeURIComponent(i.slug||i.codice||'');}}
function overlay(html){close();const o=document.createElement('div');o.className='rio-ov';o.id='rio-ov';o.innerHTML='<div class="rio-box">'+html+'</div>';o.addEventListener('click',e=>{if(e.target===o)close();});document.body.appendChild(o);return o;}
function close(){const o=document.getElementById('rio-ov');if(o)o.remove();}
function money(n){return n==null||n===''?'non indicato':Number(n).toLocaleString('it-IT')+' EUR';}
function riepilogo(i){const L=[];const add=(k,v)=>{if(v!=null&&v!==''&&v!==false)L.push(k+': '+v)};
add('Codice',i.codice);add('Titolo',i.titolo);add('Operazione',String(i.tipo_operazione||'').replace(/_/g,' '));add('Tipologia',i.tipologia||i.categoria);add('Comune',i.comune);add('Indirizzo',i.indirizzo);
add('Prezzo',i.prezzo!=null?money(i.prezzo):'');add('Superficie',i.superficie?i.superficie+' mq':'');add('Locali',i.locali);add('Bagni',i.bagni);add('Piano',i.piano);add('Classe energetica',i.classe_energetica);add('Stato',i.stato);add('Anno costruzione',i.anno_costruzione);add('Esposizione',Array.isArray(i.esposizione)?i.esposizione.join(', '):i.esposizione);
L.push('Link annuncio: '+url(i));return L.join('\n');}
async function copy(t,msg){try{await navigator.clipboard.writeText(t);if(window.toast)toast(msg||'Copiato','success');return true;}catch(e){window.prompt('Copia da qui:',t);return false;}}
const ops={
 privatephotos(i){if(!window.RighettoPrivatePhotos){toast("Lettore foto private non disponibile","error");return;}return window.RighettoPrivatePhotos.open({db:sb,property:i,isCurrent:id=>String(cur()?.id)===String(id)&&document.body.dataset.adminArea==='nuovo'&&!!document.getElementById('formTitle')?.offsetParent});},
 clienti(i){if(typeof showMatchingClienti==='function')showMatchingClienti(i.id);},
 async appuntamento(i,seed={}){
  const principal=window.RighettoGatedPrincipal,id=String(i.id);
  try{
   if(!principal||String(cur()?.id)!==id)throw Error('Scheda immobile cambiata. Riapri la scheda.');
   if(!window.RighettoAgenda?.newEvent||typeof showSection!=='function')throw Error('Agenda interna non disponibile.');
   const u=await sb.auth.getUser();if(u.error||u.data?.user?.id!==principal||principal!==window.RighettoGatedPrincipal||String(cur()?.id)!==id)throw Error('Sessione o scheda cambiata.');
   const r=await sb.from('immobili').select('id,codice,indirizzo').eq('id',id).maybeSingle();
   if(r.error||!r.data||String(r.data.id)!==id||principal!==window.RighettoGatedPrincipal||String(cur()?.id)!==id)throw Error('Immobile non verificato.');
   if(document.querySelector('#ra-form')&&!confirm('Aprire una nuova bozza in Agenda? La bozza evento aperta verrà sostituita. Nessun evento salvato automaticamente.'))return;
   await showSection('agenda');await RighettoAgenda.newEvent({property_id:id,property:r.data.codice||'Immobile collegato',address:r.data.indirizzo||'',...seed});
   const form=document.querySelector('#ra-form'),field=form?.querySelector('[name=property_search]');
   if(principal!==window.RighettoGatedPrincipal){form?.closest('.ra-modal')?.remove();throw Error('Sessione cambiata.');}
   if(!field||field.dataset.selectedId!==id||field.value!==field.dataset.selectedLabel)throw Error('Agenda non pronta o immobile non collegato. Riprova da Agenda.');
   const note=document.createElement('p');note.className='ra-note';note.textContent='Bozza dalla scheda immobile: controlla giorno, ora, agente e cliente prima di salvare. Nessun evento creato automaticamente.';form.before(note);
  }catch(error){alert(error.message+' Nessun evento salvato automaticamente.');}
 },
 async link(i){
  const result=await righettoShareForProperty(i);
  const o=overlay('<h3>Link con anteprima foto</h3><p></p><pre></pre><button data-a="copy">Copia link</button><button data-a="x">Chiudi</button>');
  o.querySelector('p').textContent=result.ok?'Link con copertina pronto. Nessun messaggio inviato.':result.reason;
  o.querySelector('pre').textContent=result.ok?result.url:'';
  const button=o.querySelector('[data-a=copy]');button.disabled=!result.ok;if(!result.ok){button.textContent='Copia non disponibile';button.style.cssText='color:#6b675f;background:#eeece8;border:1px solid #ccc;cursor:not-allowed';}
  button.onclick=async()=>{button.disabled=true;const fresh=await righettoShareForProperty(i);if(!o.isConnected)return;if(!fresh.ok){o.querySelector('p').textContent=fresh.reason;o.querySelector('pre').textContent='';button.textContent='Copia non disponibile';button.style.cssText='color:#6b675f;background:#eeece8;border:1px solid #ccc;cursor:not-allowed';return;}o.querySelector('pre').textContent=fresh.url;await copy(fresh.url,'Link con anteprima copiato');button.disabled=false;};
  o.querySelector('[data-a=x]').onclick=close;
 },
 seolink(i){copy(url(i),'Link pagina sito copiato');},
 dati(i){const t=riepilogo(i);const o=overlay('<h3>Riepilogo dati immobile</h3><pre>'+esc(t)+'</pre><button class="pri" data-a="c">Copia</button><button data-a="t">Scarica .txt</button><button data-a="x">Chiudi</button>');
  o.querySelector('[data-a=c]').onclick=()=>copy(t,'Riepilogo copiato');o.querySelector('[data-a=t]').onclick=()=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([t],{type:'text/plain;charset=utf-8'}));a.download=(i.codice||'immobile')+'.txt';a.click();};o.querySelector('[data-a=x]').onclick=close;},
 email(i){const sub='Immobile '+(i.codice||'')+' - '+(i.titolo||'');const body='Buongiorno,\n\nle segnalo questo immobile:\n\n'+riepilogo(i)+'\n\nCordiali saluti\nGino Capon - Righetto Immobiliare';
  const o=overlay('<h3>Bozza email</h3><p>Si apre il tuo programma di posta con la bozza. Il destinatario lo scegli tu. Da qui non parte nessuna email.</p><pre>'+esc('Oggetto: '+sub+'\n\n'+body)+'</pre><button class="pri" data-a="m">Apri nel programma di posta</button><button data-a="x">Chiudi</button>');
  o.querySelector('[data-a=m]').onclick=()=>{location.href='mailto:?subject='+encodeURIComponent(sub)+'&body='+encodeURIComponent(body);};o.querySelector('[data-a=x]').onclick=close;},
 async catasto(i){
  try{const module=await import('./admin-catasto-report.mjs?v=20261106-catasto');await module.openCadastralReport({db:sb,id:String(i.id),principal:window.RighettoGatedPrincipal,isCurrent:id=>String(cur()?.id)===id&&!!document.getElementById('formTitle')?.offsetParent,overlay});}
  catch(e){alert(e.message);}
 },
 duplica(i){close();if(typeof duplicateImmobile==='function')duplicateImmobile(i.id);},
 async venduto(i){
  const principal=window.RighettoGatedPrincipal,id=String(i.id),fields='id,codice,tipo_operazione,attivo,venduto,affittato,prezzo_reale,updated_at';
  const o=overlay('<h3>Stato immobile - '+esc(i.codice||'')+'</h3><p role="status">Verifica dello stato attuale in corso...</p><button data-a="x">Annulla</button>');
  o.querySelector('[data-a=x]').onclick=close;
  let row,attempted=false,locked=false;const key='righetto-property-status-v1:'+principal+':'+id;
  const alive=()=>o.isConnected&&principal&&window.RighettoGatedPrincipal===principal;
  const check=async()=>{if(!alive())throw Error('Sessione o finestra cambiata. Riapri la scheda.');const r=await sb.auth.getUser();if(r.error||r.data?.user?.id!==principal||!alive())throw Error('Sessione cambiata. Riapri la scheda.');};
  const read=async()=>{await check();const r=await sb.from('immobili').select(fields).eq('id',id).maybeSingle();await check();if(r.error||!r.data||String(r.data.id)!==id)throw Error(r.error?.message||'Immobile non leggibile.');return r.data;};
  const matches=(r,patch)=>Object.entries(patch).every(([k,v])=>r[k]===v);
  try{
   row=await read();
   const rental=['affitto_residenziale','affitto_commerciale','affitto'].includes(row.tipo_operazione);
   if(!rental&&row.tipo_operazione!=='vendita')throw Error('Tipo operazione non riconosciuto: nessuna modifica consentita.');
   const campo=rental?'affittato':'venduto',lab=rental?'affittato':'venduto';
   let pending=null;try{const raw=localStorage.getItem(key);pending=raw?JSON.parse(raw):null;localStorage.setItem(key,JSON.stringify({probe:true}));if(pending)localStorage.setItem(key,JSON.stringify(pending));else localStorage.removeItem(key);}catch(e){throw Error('Memoria di recupero non disponibile. Nessuna modifica consentita.');}
   if(pending){
    if(pending.probe||pending.id!==id||pending.principal!==principal||!pending.patch||!matches(row,pending.patch))locked=true;
    else localStorage.removeItem(key);
   }
   o.querySelector('.rio-box').innerHTML='<h3>Segna come '+lab+' - '+esc(row.codice||'')+'</h3><p>'+(rental?'Immobile in affitto: il comando modifica solo lo stato Affittato.':'Immobile in vendita: il comando modifica solo lo stato Venduto.')+'</p><p>Stato attuale: <b>'+(row[campo]?lab:'non '+lab)+'</b> | sul sito: <b>'+(row.attivo===false?'non attivo':'attivo')+'</b>.</p><p>Lo stato '+lab+' esclude l\'immobile da home e chat. Finché resta attivo, può comparire nell\'elenco pubblico con questa etichetta. Per toglierlo anche dall\'elenco seleziona Disattiva dal sito.</p><label>Prezzo reale (facoltativo)<input type="number" min="0" step="any" data-price value="'+(row.prezzo_reale!=null?esc(row.prezzo_reale):'')+'"></label><label><input type="checkbox" data-disable> Disattiva anche dal sito</label><p data-status role="status" aria-live="polite">'+(locked?'Tentativo precedente non confermato e stato diverso da quello richiesto. Non ripetere il salvataggio: occorre verificare il tentativo.':pending?'Il tentativo precedente è stato verificato nello stato attuale. Nessun nuovo invio.':'Nessuna modifica eseguita.')+'</p><button class="pri" data-a="ok">Conferma '+lab+'</button>'+(row[campo]?'<button data-a="un">Rimetti come non '+lab+'</button>':'')+'<button data-a="x">Chiudi</button>';
   o.querySelector('[data-a=x]').onclick=close;
   const status=o.querySelector('[data-status]'),buttons=[...o.querySelectorAll('[data-a=ok],[data-a=un]')];
   const disable=on=>{buttons.forEach(b=>b.disabled=on);o.querySelector('[data-price]').disabled=on;o.querySelector('[data-disable]').disabled=on;};disable(locked);
   const apply=async val=>{
    if(locked||attempted||!alive())return;
    const patch={[campo]:val},price=o.querySelector('[data-price]').value,dis=val&&o.querySelector('[data-disable]').checked;
    if(val&&price!==''){const n=Number(price);if(!Number.isFinite(n)||n<0){status.textContent='Inserisci un prezzo reale valido, maggiore o uguale a zero.';return;}patch.prezzo_reale=n;}
    if(dis)patch.attivo=false;
    if(!confirm((val?'Segnare come '+lab:'Rimettere come non '+lab)+' l\'immobile '+(row.codice||'')+'?'+(dis?'\nVerrà anche disattivato dal sito.':'\nLa visibilità sul sito non viene cambiata.')))return;
    disable(true);status.textContent='Salvataggio e verifica in corso...';
    try{
     await check();const fresh=await read();
     if(['tipo_operazione','attivo','venduto','affittato','prezzo_reale','updated_at'].some(k=>fresh[k]!==row[k]))throw Error('Stato cambiato da un altro accesso. Chiudi e riapri prima di decidere.');
     localStorage.setItem(key,JSON.stringify({id,principal,patch}));
     let q=sb.from('immobili').update(patch).eq('id',id);
     for(const k of ['tipo_operazione','attivo','venduto','affittato','prezzo_reale','updated_at'])q=row[k]==null?q.is(k,null):q.eq(k,row[k]);
     attempted=true;const r=await q.select(fields);await check();
     if(r.error)throw Error(r.error.message);
     if(r.data?.length!==1||!matches(r.data[0],patch))throw Error('Salvataggio non confermato o stato cambiato altrove.');
     const verified=await read();if(!matches(verified,patch))throw Error('Rilettura dello stato non corrispondente.');
     localStorage.removeItem(key);status.textContent='Stato '+(val?lab:'non '+lab)+' salvato e riletto.'+(dis?' Immobile disattivato dal sito.':' Visibilità sul sito invariata.');locked=true;
     Object.assign(i,verified);if(typeof allImmobili!=='undefined'){const cached=allImmobili.find(x=>String(x.id)===id);if(cached)Object.assign(cached,verified);}if(window.toast)toast('Stato immobile salvato e verificato','success');
    }catch(error){
     if(!alive())return;
     status.textContent=attempted?'Esito non confermato. Non ripetere: chiudi e riapri per la sola verifica dello stato. '+error.message:'Nessuna modifica inviata. '+error.message;
     locked=true;disable(true);
    }
   };
   o.querySelector('[data-a=ok]').onclick=()=>apply(true);const un=o.querySelector('[data-a=un]');if(un)un.onclick=()=>apply(false);
  }catch(error){if(alive()){o.querySelector('[role=status]').textContent=error.message+' Nessuna modifica eseguita.';}}
 }
};
Object.assign(ops,{
 salva(i){if(String(cur()?.id)!==String(i.id))throw Error('Apri prima la scheda corretta per salvare');document.getElementById('immobileForm')?.requestSubmit();},
 importa(){if(typeof openImportModal==='function')openImportModal();},
 async cronistoria(i){await editImmobile(i.id);window.RighettoImmobileLayout?.select('cronistoria');},
 evento(i){return window.RighettoPropertyPrivateEditor?.comment(i);},
 modifica(i){if(typeof editImmobile==='function'){Promise.resolve(editImmobile(i.id)).then(()=>window.RighettoImmobileLayout?.select('info'));}},
 proprietari(i){if(typeof openProprietariImmobile==='function')openProprietariImmobile(i.id);},
 documenti(i){if(typeof openDocsImmobile==='function')openDocsImmobile(i.codice||'',i.id);},
 foto(i){if(typeof openFotoImmobile==='function')openFotoImmobile(i.id);},
 stampa(i){if(window.RighettoImmobileStampe?.open)return RighettoImmobileStampe.open('cliente');throw Error('Modulo PDF cliente non disponibile');},
 cestino(i){if(i.cestino){if(typeof restoreImmobile==='function')restoreImmobile(i.id,i.titolo||'');}else if(typeof deleteImmobile==='function')deleteImmobile(i.id,i.titolo||'');},
 evidenza(i){if(typeof toggleEvidenza==='function')toggleEvidenza(i.id,!i.in_evidenza);},
 attivo(i){if(typeof toggleAttivo==='function')toggleAttivo(i.id,!i.attivo);}
});
const ITEMS=[['salva','Salva modifiche'],['evento','Aggiungi commento alla cronistoria'],['importa','Importa dati da Idealista'],['modifica','Modifica dati immobile'],['clienti','Trova clienti compatibili'],['appuntamento','Nuovo appuntamento'],['email','Bozza email con i dati'],['cestino','Sposta nel cestino / Ripristina'],['duplica','Duplica come bozza'],['link','Copia link con anteprima foto'],['seolink','Copia link pagina sito (SEO)'],['dati','Esporta dati immobile'],['venduto','Segna venduto / affittato'],['attivo','Attiva / disattiva sul sito'],['evidenza','Metti / togli evidenza'],['proprietari','Gestisci proprietari'],['documenti','Documenti (PDF)'],['foto','Foto pubbliche'],['privatephotos','Foto private'],['stampa','Stampa PDF'],['catasto','Scheda catastale (lettura)']];
const ROW_ITEMS=[['cronistoria','Cronistoria immobile'],['clienti','Trova clienti'],['evento','Aggiungi evento'],['appuntamento','Nuovo appuntamento'],['stampa','Crea PDF cliente'],['modifica','Modifica immobile'],['cestino','Sposta nello storico']];
const rowMenuHtml=i=>ROW_ITEMS.map(([key,label])=>'<button type="button" data-op="'+key+'"'+(key==='cestino'?' style="color:#b1202b"':'')+'>'+esc(key==='cestino'&&i?.cestino?'Recupera scheda (resta offline)':label)+'</button>').join('');
const DACOMPLETARE='<div class="rio-unavailable">Esportazione sui portali: da completare, non disponibile qui.</div>';
const menuHtml=i=>ITEMS.map(([key,label])=>'<button type="button" data-op="'+key+'">'+esc(key==='cestino'?(i?.cestino?'Recupera scheda (resta offline)':'Sposta nello storico'):key==='attivo'?(i?.attivo?'Disattiva sul sito':'Attiva sul sito'):key==='evidenza'?(i?.in_evidenza?'Togli evidenza':'Metti in evidenza'):label)+'</button>').join('')+DACOMPLETARE;
async function dispatchOp(key,i){const principal=window.RighettoGatedPrincipal;try{if(!principal||typeof sb==='undefined')throw Error('Sessione non disponibile');const u=await sb.auth.getUser();if(u.error||u.data.user?.id!==principal||window.RighettoGatedPrincipal!==principal)throw Error('Sessione cambiata');const r=await sb.from('immobili').select('*').eq('id',i.id).single();if(r.error||r.data?.id!==i.id||window.RighettoGatedPrincipal!==principal)throw Error('Immobile non verificato');i=r.data;if(['privatephotos','appuntamento','catasto','stampa'].includes(key)&&String(cur()?.id)!==String(i.id)){if(typeof editImmobile!=='function')throw Error('Scheda non disponibile');await editImmobile(i.id);if(String(cur()?.id)!==String(i.id)||window.RighettoGatedPrincipal!==principal)throw Error('Scheda immobile non confermata');}return await ops[key](i);}catch(e){if(window.toast)toast('Operazione non eseguita: '+(e.message||e),'error');else alert('Operazione non eseguita: '+(e.message||e));}}
function openMenu(i,anchor){css();document.getElementById('rio-row-menu')?.remove();if(!anchor){const o=overlay('<h3>Operazioni - '+esc(i.codice||'')+'</h3><div id="rio-list" class="rio-list">'+menuHtml(i)+'</div><button data-a="x">Chiudi</button>');o.querySelector('[data-a=x]').onclick=close;o.querySelector('#rio-list').onclick=e=>{const b=e.target.closest('[data-op]');if(!b)return;close();dispatchOp(b.dataset.op,i);};return;}
 const menu=document.createElement('div');menu.id='rio-row-menu';menu.className='rio-menu';menu.setAttribute('aria-label','Operazioni '+(i.codice||''));menu.innerHTML=rowMenuHtml(i);document.body.append(menu);const r=anchor.getBoundingClientRect();menu.style.cssText='position:fixed;right:auto;top:'+Math.min(r.bottom+3,innerHeight-310)+'px;left:'+Math.max(8,Math.min(r.right-270,innerWidth-280))+'px;max-height:min(68vh,520px);width:270px';menu.onclick=e=>{const b=e.target.closest('[data-op]');if(!b)return;menu.remove();dispatchOp(b.dataset.op,i);};const dismiss=e=>{if(e.type==='keydown'&&e.key!=='Escape')return;if(e.type==='click'&&(menu.contains(e.target)||anchor.contains(e.target)))return;menu.remove();document.removeEventListener('click',dismiss);document.removeEventListener('keydown',dismiss);};document.addEventListener('click',dismiss);document.addEventListener('keydown',dismiss);window.addEventListener('scroll',()=>menu.remove(),{once:true,capture:true});}
function addMenu(){css();const bar=document.querySelector('#formTitle');if(!bar)return;const hdr=bar.parentNode.querySelector('.modal-header-actions');if(!hdr||document.querySelector('.rio-wrap'))return;
 const w=document.createElement('span');w.className='rio-wrap';w.innerHTML='<button type="button" class="btn btn-primary btn-sm" id="rio-btn" style="background:#00508f;color:#fff">Operazioni</button><div class="rio-menu" id="rio-menu" hidden></div>';hdr.insertBefore(w,hdr.firstChild);
 const m=w.querySelector('#rio-menu');m.innerHTML=menuHtml(cur());
 w.querySelector('#rio-btn').onclick=e=>{e.stopPropagation();m.innerHTML=menuHtml(cur());m.hidden=!m.hidden;};
 m.addEventListener('click',e=>{const b=e.target.closest('[data-op]');if(!b)return;if(['salva','importa'].includes(b.dataset.op)){if(!window.RighettoGatedPrincipal)return;m.hidden=true;if(b.dataset.op==='salva')document.getElementById('immobileForm')?.requestSubmit();else if(typeof openImportModal==='function')openImportModal();return;}const i=cur();if(!i){if(window.toast)toast('Salva prima l\'immobile','error');return;}m.hidden=true;dispatchOp(b.dataset.op,i);});
 document.addEventListener('click',e=>{if(!w.contains(e.target))m.hidden=true;});}
const mo=new MutationObserver(()=>{if(document.getElementById('formTitle')&&document.getElementById('formTitle').offsetParent)addMenu();});
function boot(){mo.observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:['class','style']});addMenu();}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
window.RighettoImmobileOperazioni=ops;window.RighettoImmobileOperazioni.openMenu=openMenu;
})();
