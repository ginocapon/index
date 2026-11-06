import {chooseUnit,projectCadastral} from './catasto-projection.mjs?v=20261106-1038';
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const missing='Non presente';
function value(x){return x===null||x===undefined||x===''?missing:typeof x==='string'||typeof x==='number'?esc(x):'Formato non leggibile';}
export function reportBody(i){
 const units=Array.isArray(i.unita_catastali)?i.unita_catastali:[];
 const labels={cat_category:'Categoria',cat_municipality:'Comune catastale',cat_section:'Sezione',cat_sheet:'Foglio',cat_parcel:'Particella / mappale',cat_subordinate:'Subalterno',cat_class:'Classe'};
 const block=(label,v)=>'<div class="cr-field"><dt>'+esc(label)+'</dt><dd>'+value(v)+'</dd></div>';
 const place='<section><h2>Località da confrontare</h2><p>Titolo registrato: '+value(i.titolo)+'.<br>Comune della scheda: '+value(i.comune)+'.<br>Codici dei comuni catastali: '+(units.length?units.map(u=>value(u?.comune_catastale)).join(', '):missing)+'.</p><p>Questi campi provengono da sezioni diverse e non sono stati riconciliati. Confrontali con il documento originale: il riepilogo non conferma che indichino la stessa località.</p></section>';
 const u=units.map((unit,index)=>{try{
  const p=projectCadastral(units,chooseUnit(units,index));
  return '<section><h2>Unità '+(index+1)+'</h2><dl>'+Object.entries(labels).map(([key,label])=>block(label,p.values[key])).join('')+block('Rendita registrata (€)',unit.rendita)+block('Valore prima casa registrato (€)',unit.valore_prima)+block('Valore seconda casa registrato (€)',unit.valore_seconda)+block('Descrizione registrata',unit.descrizione)+'</dl></section>';
 }catch{return '<section><h2>Unità '+(index+1)+'</h2><p>Formato non leggibile. Nessun dato ricostruito.</p></section>';}}).join('');
 return '<header><p>Righetto Immobiliare · uso interno</p><h1>Scheda dati catastali - '+esc(i.codice||'Immobile')+'</h1><p>'+esc(i.titolo||'')+'</p></header><aside>Riepilogo dei dati salvati nel gestionale. Non è una visura e non certifica proprietà o conformità. Nessuna interrogazione esterna, nessun costo.</aside>'+place+'<section><h2>Dati generali registrati</h2><dl>'+block('Comune',i.comune)+block('Indirizzo riservato',i.indirizzo)+block('Rendita catastale totale (€)',i.rendita_catastale)+block('Valore catastale registrato (€)',i.valore_catastale)+block('Note catastali',i.note_catastali)+'</dl></section>'+(u||'<section><h2>Unità catastali</h2><p>Nessuna unità registrata.</p></section>')+'<footer>Valori mancanti lasciati tali, nessun calcolo o abbinamento automatico. I valori prima e seconda casa sono distinti come nei campi salvati. Allegati e visure restano nelle sezioni riservate: questo riepilogo non li apre né li copia.</footer>';
}
export const reportStyle='*{box-sizing:border-box}body{font:15px/1.5 Arial,sans-serif;color:#17324d;background:white;margin:0;padding:24px}h1{font-size:24px;line-height:1.25;margin:8px 0 16px}h2{font-size:18px;margin:24px 0 12px}header p,footer{font-size:13px;color:#526777}aside{padding:12px;background:#f4f2ed;border-left:3px solid #8ba66c}dl{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin:0}.cr-field{border-bottom:1px solid #dde4e8;padding-bottom:8px;min-width:0}dt{font-size:12px;font-weight:bold;color:#526777}dd{margin:4px 0 0;white-space:pre-wrap;overflow-wrap:anywhere}footer{margin-top:24px;border-top:1px solid #dde4e8;padding-top:12px}@media(max-width:500px){body{padding:16px}dl{grid-template-columns:1fr}}@media print{body{font-size:11px;padding:0}dl{gap:10px}.cr-field{padding-bottom:5px}h2{margin-top:18px}footer{margin-top:14px;padding-top:8px}h1{font-size:20px}h2{font-size:15px}section{break-inside:avoid}button{display:none}}';
export async function openCadastralReport({db,id,isCurrent,principal,overlay}){
 const valid=()=>principal&&window.RighettoGatedPrincipal===principal&&isCurrent(id);
 if(!valid())throw Error('Sessione o immobile cambiato. Riapri la scheda.');
 const auth=await db.auth.getUser();if(auth.error||auth.data?.user?.id!==principal||!valid())throw Error('Sessione non verificata.');
 const read=()=>db.from('immobili').select('id,codice,titolo,comune,indirizzo,rendita_catastale,valore_catastale,note_catastali,unita_catastali,updated_at').eq('id',id).maybeSingle();
 const r=await read();if(r.error||!r.data||String(r.data.id)!==id||!valid())throw Error('Immobile non verificato. Nessun dato cambiato.');
 const snapshot=JSON.stringify(r.data);const body=reportBody(r.data);
 const scoped=reportStyle.replace(/([^{}]+)\{/g,(all,selectors)=>selectors.startsWith('@')?all:selectors.split(',').map(sel=>sel.trim()==='body'?'#cr-report':'#cr-report '+sel.trim()).join(',')+'{');
 const o=overlay('<div id="cr-report"><style>'+scoped+'</style>'+body+'</div><p id="cr-status" role="status">Sola lettura. I dati non salvati nel modulo non compaiono qui.</p><button data-cr="print">Stampa / Salva PDF locale</button><button data-cr="close">Chiudi</button>');
 let popup=null;const closeCopy=()=>{try{popup?.close();}catch{}popup=null;};
 let authWatch;const cleanup=()=>{closeCopy();mo.disconnect();authWatch?.data?.subscription?.unsubscribe();};
 const onChange=()=>{if(!valid()||!o.isConnected){cleanup();o.remove();}};
 const mo=new MutationObserver(onChange);mo.observe(document.body,{subtree:true,childList:true,attributes:true,attributeFilter:['class','style']});
 authWatch=db.auth.onAuthStateChange?.(event=>{if(event==='SIGNED_OUT'||event==='SIGNED_IN'){cleanup();o.remove();}});
 o.querySelector('[data-cr=close]').onclick=()=>{cleanup();o.remove();};
 o.querySelector('[data-cr=print]').onclick=async()=>{
  const button=o.querySelector('[data-cr=print]');if(button.disabled)return;button.disabled=true;
  closeCopy();if(!valid()){button.disabled=false;return onChange();}
  popup=window.open('','_blank');if(!popup){o.querySelector('#cr-status').textContent='Consenti le finestre per aprire la copia locale.';button.disabled=false;return;}
  popup.document.body.textContent='Verifica dei dati salvati…';
  try{const a=await db.auth.getUser(),fresh=await read();if(a.error||a.data?.user?.id!==principal||fresh.error||!fresh.data||!valid()||!o.isConnected||JSON.stringify(fresh.data)!==snapshot)throw Error('Dati o sessione cambiati: riapri il riepilogo.');
   popup.document.open();popup.document.write('<!doctype html><html lang="it"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Scheda dati catastali</title><style>'+reportStyle+'</style><body>'+body+'</body></html>');popup.document.close();popup.focus();popup.print();
  }catch(e){closeCopy();if(o.isConnected)o.querySelector('#cr-status').textContent=e.message;}finally{button.disabled=false;}
 };
 return o;
}
