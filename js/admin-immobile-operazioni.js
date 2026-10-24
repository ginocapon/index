/* Menu Operazioni nella scheda immobile. Nessun invio a terzi, nessuna pubblicazione, nessuna cancellazione definitiva.
   Le azioni che scrivono dati (duplica, venduto) chiedono conferma e mostrano cosa cambia. */
(function(){
'use strict';
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function css(){if(document.getElementById('rio-css'))return;const s=document.createElement('style');s.id='rio-css';s.textContent=
'.rio-wrap{position:relative;display:inline-block}.rio-menu{position:absolute;right:0;top:38px;z-index:9000;background:#fff;border:1px solid #00508f;border-radius:8px;min-width:250px;max-width:92vw;box-shadow:0 8px 30px #0003;max-height:70vh;overflow:auto}'+
'.rio-menu button{display:block;width:100%;text-align:left;border:0;background:#fff;padding:11px 14px;font:600 14px Arial,sans-serif;color:#17324d;cursor:pointer;border-bottom:1px solid #eef2f5}.rio-menu button:hover{background:#eef4fa}'+
'.rio-menu details{padding:8px 14px;font:13px Arial,sans-serif;color:#566773}.rio-menu details summary{cursor:pointer;font-weight:700}'+
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
 clienti(i){if(typeof showMatchingClienti==='function')showMatchingClienti(i.id);},
 appuntamento(i){if(typeof showSection==='function')showSection('agenda');if(window.RighettoAgenda&&RighettoAgenda.newEvent)RighettoAgenda.newEvent({property_id:i.id,property:i.codice,address:i.indirizzo||''});},
 link(i){copy(url(i),'Link dell\'annuncio copiato');},
 dati(i){const t=riepilogo(i);const o=overlay('<h3>Riepilogo dati immobile</h3><pre>'+esc(t)+'</pre><button class="pri" data-a="c">Copia</button><button data-a="t">Scarica .txt</button><button data-a="x">Chiudi</button>');
  o.querySelector('[data-a=c]').onclick=()=>copy(t,'Riepilogo copiato');o.querySelector('[data-a=t]').onclick=()=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([t],{type:'text/plain;charset=utf-8'}));a.download=(i.codice||'immobile')+'.txt';a.click();};o.querySelector('[data-a=x]').onclick=close;},
 email(i){const sub='Immobile '+(i.codice||'')+' - '+(i.titolo||'');const body='Buongiorno,\n\nle segnalo questo immobile:\n\n'+riepilogo(i)+'\n\nCordiali saluti\nGino Capon - Righetto Immobiliare';
  const o=overlay('<h3>Bozza email</h3><p>Si apre il tuo programma di posta con la bozza. Il destinatario lo scegli tu. Da qui non parte nessuna email.</p><pre>'+esc('Oggetto: '+sub+'\n\n'+body)+'</pre><button class="pri" data-a="m">Apri nel programma di posta</button><button data-a="x">Chiudi</button>');
  o.querySelector('[data-a=m]').onclick=()=>{location.href='mailto:?subject='+encodeURIComponent(sub)+'&body='+encodeURIComponent(body);};o.querySelector('[data-a=x]').onclick=close;},
 catasto(i){const r=[];const add=(k,v)=>r.push('<div><b style="font-size:11px;text-transform:uppercase;color:#607184">'+k+'</b><br>'+(v||'<i>non compilato</i>')+'</div>');
  const un=i.unita_catastali;const unTxt=Array.isArray(un)&&un.length?'<pre>'+esc(JSON.stringify(un,null,1))+'</pre>':'';
  add('Rendita catastale',i.rendita_catastale!=null?money(i.rendita_catastale):'');add('Valore catastale',i.valore_catastale!=null?money(i.valore_catastale):'');add('Note catastali',esc(i.note_catastali||''));add('Unita catastali',unTxt);
  const cp=i.catasto_pdf;const has=cp&&((Array.isArray(cp)&&cp.length)||(typeof cp==='string'&&cp.trim()&&cp!=='[]'));add('Documento catastale',has?'presente nei documenti dell\'immobile':'');
  overlay('<h3>Scheda catastale - '+esc(i.codice||'')+'</h3><p style="color:#566773;font-size:13px">Sola lettura: mostra solo i dati gia presenti. Non scarica visure.</p>'+r.join('<hr style="border:0;border-top:1px solid #eef2f5">')+'<button data-a="x">Chiudi</button>').querySelector('[data-a=x]').onclick=close;},
 duplica(i){close();if(typeof duplicateImmobile==='function')duplicateImmobile(i.id);},
 venduto(i){const aff=i.tipo_operazione==='affitto';const campo=aff?'affittato':'venduto';const lab=aff?'affittato':'venduto';
  const o=overlay('<h3>Segna come '+lab+' - '+esc(i.codice||'')+'</h3><p>Cosa cambia sul sito:<br>- L\'elenco pubblico mostra gli immobili attivi con l\'etichetta "'+(aff?'Affittato':'Venduto')+'".<br>- La home e la chat escludono gli immobili '+lab+'.<br>- Per toglierlo anche dall\'elenco serve disattivarlo.</p>'+
  '<label>Prezzo reale (facoltativo)<input type="number" id="rio-pr" value="'+(i.prezzo_reale!=null?esc(i.prezzo_reale):'')+'"></label>'+
  '<label><input type="checkbox" id="rio-dis"> Disattiva anche dal sito (non compare piu nell\'elenco)</label>'+
  '<p style="font-size:13px;color:#566773">Stato attuale: '+(i[campo]?lab:'non '+lab)+' | sul sito: '+(i.attivo===false?'non attivo':'attivo')+'. Puoi annullare riaprendo questa finestra.</p>'+
  '<button class="pri" data-a="ok">Conferma</button>'+(i[campo]?'<button data-a="un">Rimetti come non '+lab+'</button>':'')+'<button data-a="x">Annulla</button>');
  o.querySelector('[data-a=x]').onclick=close;
  const apply=async(val)=>{const patch={};patch[campo]=val;const pr=document.getElementById('rio-pr').value;if(val&&pr!=='')patch.prezzo_reale=Number(pr);
   const dis=document.getElementById('rio-dis').checked;
   if(!confirm((val?'Segnare come '+lab:'Rimettere come non '+lab)+' l\'immobile '+(i.codice||'')+'?'+(dis&&val?'\nVerra anche disattivato dal sito.':'')))return;
   const {error}=await sb.from('immobili').update(patch).eq('id',i.id);
   if(error){if(window.toast)toast('Errore: '+error.message,'error');return;}
   if(dis&&val&&typeof _immobilePatchBool==='function')await _immobilePatchBool(i.id,{attivo:false},'Disattivato dal sito');
   if(window.toast)toast(val?'Segnato come '+lab:'Ripristinato','success');close();if(typeof loadImmobili==='function')await loadImmobili();};
  o.querySelector('[data-a=ok]').onclick=()=>apply(true);const un=o.querySelector('[data-a=un]');if(un)un.onclick=()=>apply(false);}
};
const ITEMS=[['clienti','Trova clienti compatibili'],['email','Bozza email con i dati'],['link','Copia link dell\'annuncio'],['dati','Esporta dati immobile'],['catasto','Scheda catastale (lettura)'],['duplica','Duplica come bozza'],['venduto','Segna venduto / affittato']];
const DACOMPLETARE='<details><summary>Da completare (non ancora disponibili qui)</summary><ul style="margin:6px 0 0 16px;padding:0"><li>Esportazione sui portali</li><li>Nuovo appuntamento da qui (per ora si inserisce nel vecchio gestionale)</li></ul></details>';
function openMenu(i){css();const o=overlay('<h3>Operazioni - '+esc(i.codice||'')+'</h3><div id="rio-list" class="rio-list">'+ITEMS.map(x=>'<button type="button" data-op="'+x[0]+'" style="display:block;width:100%;text-align:left;margin:4px 0">'+x[1]+'</button>').join('')+'</div>'+DACOMPLETARE+'<button data-a="x" style="margin-top:10px">Chiudi</button>');
 o.querySelector('[data-a=x]').onclick=close;o.querySelector('#rio-list').onclick=e=>{const b=e.target.closest('[data-op]');if(!b)return;close();ops[b.dataset.op](i);};}
function addMenu(){css();const bar=document.querySelector('#formTitle');if(!bar)return;const hdr=bar.parentNode.querySelector('.modal-header-actions');if(!hdr||hdr.querySelector('.rio-wrap'))return;
 const w=document.createElement('span');w.className='rio-wrap';w.innerHTML='<button type="button" class="btn btn-primary btn-sm" id="rio-btn" style="background:#00508f;color:#fff">🔧 Operazioni</button><div class="rio-menu" id="rio-menu" hidden></div>';hdr.insertBefore(w,hdr.firstChild);
 const m=w.querySelector('#rio-menu');const items=[['clienti','Trova clienti compatibili'],['email','Bozza email con i dati'],['link','Copia link dell\'annuncio'],['dati','Esporta dati immobile'],['catasto','Scheda catastale (lettura)'],['duplica','Duplica come bozza'],['venduto','Segna venduto / affittato']];
 m.innerHTML=items.map(x=>'<button type="button" data-op="'+x[0]+'">'+x[1]+'</button>').join('')+'<details><summary>Da completare (non ancora disponibili qui)</summary><ul style="margin:6px 0 0 16px;padding:0"><li>Esportazione sui portali (per ora nel vecchio gestionale)</li><li>Nuovo appuntamento da qui (per ora si inserisce nel vecchio gestionale)</li></ul></details>';
 w.querySelector('#rio-btn').onclick=e=>{e.stopPropagation();m.hidden=!m.hidden;};
 m.addEventListener('click',e=>{const b=e.target.closest('[data-op]');if(!b)return;const i=cur();if(!i){if(window.toast)toast('Salva prima l\'immobile','error');return;}m.hidden=true;ops[b.dataset.op](i);});
 document.addEventListener('click',e=>{if(!w.contains(e.target))m.hidden=true;});}
const mo=new MutationObserver(()=>{if(document.getElementById('formTitle')&&document.getElementById('formTitle').offsetParent)addMenu();});
function boot(){mo.observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:['class','style']});addMenu();}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',boot);else boot();
window.RighettoImmobileOperazioni=ops;window.RighettoImmobileOperazioni.openMenu=openMenu;
})();
