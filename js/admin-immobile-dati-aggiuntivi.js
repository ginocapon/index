/* Campi aggiuntivi nell'archivio privato esistente. Nessun dato importato o pubblicato. */
(function(){
'use strict';
const definition={tipo_proprieta:['select','Tipo di proprietà',['non_definito','intera_proprieta','nuda_proprieta','parziale_proprieta','usufrutto','multiproprieta','diritto_di_superficie','agevolato']],finiture:['area','Finiture'],civico:['text','Numero civico reale'],interno:['text','Interno'],...Object.fromEntries(['mare','montagna','lago','terme','collina','campagna'].map(k=>['vacanza_'+k,['bool','Vacanza '+k]])),...Object.fromEntries([['en','inglese'],['fr','francese'],['de','tedesco'],['es','spagnolo'],['ru','russo'],['cn','cinese'],['ar','arabo'],['pt','portoghese']].flatMap(([k,l])=>[['titolo_'+k,['title','Titolo '+l]],['descrizione_'+k,['area','Descrizione '+l]]]))};
const columns='immobile_id,versione,aggiornato_il,'+Object.keys(definition).join(',');
let host,id=null,uid=null,epoch=0,row=null,initial={},busy=false,uncertain=false;
const node=(tag,text)=>{const x=document.createElement(tag);if(text!==undefined)x.textContent=text;return x;};
window.RighettoPropertyExtra={pending:()=>busy,dirty:()=>!!host&&!host.querySelector('[data-ipa-fields]').hidden&&dirty()};
const current=()=>document.getElementById('editId')?.value||null;
const values=()=>Object.fromEntries([...host.querySelectorAll('[data-ipa-field]')].map(e=>[e.dataset.ipaField,e.value===''?null:definition[e.dataset.ipaField][0]==='bool'?e.value==='true':e.value]));
const dirty=()=>Object.entries(values()).some(([k,v])=>v!==initial[k]);
async function verify(ticket){const u=await sb.auth.getUser();if(ticket!==epoch||current()!==id||uid!==window.RighettoGatedPrincipal||u.error||u.data?.user?.id!==uid)throw Error('Sessione o immobile cambiato. Riapri la scheda.');const a=await sb.rpc('righetto_is_admin_request');if(a.error||a.data!==true||ticket!==epoch||uid!==window.RighettoGatedPrincipal||current()!==id)throw Error('Accesso amministratore non verificato.');}
function lock(){host.querySelectorAll('input,textarea,select,button').forEach(e=>e.disabled=busy);const save=host.querySelector('[data-ipa-save]');if(save)save.disabled=busy||uncertain||!dirty();}
function controls(data){const box=host.querySelector('[data-ipa-fields]');box.replaceChildren();
 for(const [key,[type,label,choices]]of Object.entries(definition)){
  const l=node('label',label+' ');const x=node(type==='area'?'textarea':['bool','select'].includes(type)?'select':'input');x.dataset.ipaField=key;
  if(x.tagName==='SELECT'){x.append(new Option('Non indicato',''));for(const [v,t]of type==='bool'?[['true','Sì'],['false','No']]:choices.map(v=>[v,v.replaceAll('_',' ')]))x.append(new Option(t,v));}
  else{x.maxLength=type==='title'?85:type==='area'?10000:100;if(type==='area')x.rows=3;else x.type='text';}
  const saved=data?.[key];x.value=saved===null||saved===undefined?'':String(saved);
  if(saved!==null&&saved!==undefined&&x.tagName==='SELECT'&&x.value==='')throw Error('Valore non riconosciuto: '+label);
  x.addEventListener('input',lock);x.addEventListener('change',lock);l.append(x);box.append(l);
 }
 box.hidden=false;initial=values();host.querySelector('[data-ipa-save]').hidden=false;
 window.RighettoNavigation?.saved(host);lock();
}
async function load(){if(busy)return;if(!host.querySelector('[data-ipa-fields]').hidden&&dirty()&&!confirm('Scartare le sole modifiche dei campi aggiuntivi e rileggere?'))return;
 const ticket=epoch,status=host.querySelector('[data-ipa-status]');busy=true;lock();status.textContent='Lettura campi aggiuntivi...';
 try{await verify(ticket);const r=await sb.from('immobile_dati_privati').select(columns).eq('immobile_id',id).maybeSingle();await verify(ticket);if(r.error)throw Error(r.error.message);if(r.data&&(r.data.immobile_id!==id||!Number.isSafeInteger(r.data.versione)||r.data.versione<1||!r.data.aggiornato_il))throw Error('Dati non verificati');row=r.data;uncertain=false;controls(row);status.textContent=row?'Campi aggiuntivi caricati. Nessuna modifica salvata.':'Nessun campo aggiuntivo salvato. Puoi compilarli senza modificare i dati della scheda principale.';}
 catch(e){if(ticket===epoch){host.querySelector('[data-ipa-fields]').replaceChildren();host.querySelector('[data-ipa-fields]').hidden=true;host.querySelector('[data-ipa-save]').hidden=true;status.textContent='Lettura non verificata: '+e.message;}}
 finally{if(ticket===epoch){busy=false;lock();}}
}
async function save(){if(busy||uncertain||!dirty())return;const ticket=epoch,submitted=values(),patch={};for(const[k,v]of Object.entries(submitted))if(v!==initial[k])patch[k]=v;
 for(const[k,v]of Object.entries(patch)){if(v===null)continue;const[t,,choices]=definition[k];if(t==='bool'&&typeof v!=='boolean'||t==='select'&&!choices.includes(v)||!['bool','select'].includes(t)&&(typeof v!=='string'||v.length>(t==='title'?85:t==='area'?10000:100))){host.querySelector('[data-ipa-status]').textContent='Controlla il campo '+definition[k][1];return;}}
 const status=host.querySelector('[data-ipa-status]');busy=true;lock();let attempted=false;
 try{await verify(ticket);const expected={...patch,versione:(row?.versione||0)+1,aggiornato_il:new Date().toISOString()};let q=row?sb.from('immobile_dati_privati').update(expected).eq('immobile_id',id).eq('versione',row.versione).eq('aggiornato_il',row.aggiornato_il):sb.from('immobile_dati_privati').insert({immobile_id:id,...expected});attempted=true;const r=await q.select(columns);await verify(ticket);if(r.error)throw Error(r.error.message);const saved=r.data?.[0];if(r.data?.length!==1||saved.immobile_id!==id||saved.versione!==expected.versione||Date.parse(saved.aggiornato_il)!==Date.parse(expected.aggiornato_il)||Object.keys(patch).some(k=>saved[k]!==patch[k]))throw Error('Salvataggio non confermato o campi modificati altrove');row=saved;initial=submitted;window.RighettoNavigation?.saved(host);status.textContent='Salvati solo i campi aggiuntivi modificati. Nessuna modifica alla pubblicazione o agli altri dati.';}
 catch(e){if(ticket===epoch){uncertain=attempted;status.textContent=(attempted?'Esito da verificare: ':'Salvataggio non iniziato: ')+e.message+(attempted?'. Bozza conservata. Rileggi prima di riprovare.':'');}}
 finally{if(ticket===epoch){busy=false;lock();}}
}
function mount(){const p=document.getElementById('ril-panel-info');if(!p)return;const next=current(),principal=window.RighettoGatedPrincipal||null;if(host?.isConnected&&next===id&&principal===uid)return;
 epoch++;host?.remove();host=null;id=next;uid=principal;row=null;initial={};busy=false;uncertain=false;if(!id||!uid)return;
 host=node('details');host.className='ipa-panel';host.append(node('summary','Campi aggiuntivi e lingue'));host.append(node('p','Archivio riservato. Le traduzioni sono inserite manualmente e non vengono pubblicate automaticamente.'));
 const loadButton=node('button','Leggi campi aggiuntivi');loadButton.type='button';loadButton.onclick=load;const status=node('p');status.dataset.ipaStatus='';status.setAttribute('role','status');const fields=node('div');fields.dataset.ipaFields='';fields.hidden=true;const saveButton=node('button','Salva solo campi aggiuntivi');saveButton.type='button';saveButton.dataset.ipaSave='';saveButton.hidden=true;saveButton.onclick=save;host.append(loadButton,status,fields,saveButton);p.append(host);
}
const style=node('style');style.textContent='.ipa-panel{scroll-margin-top:105px;grid-column:1/-1;order:80;border:1px solid #b3c9d6;padding:12px;margin-top:12px}.ipa-panel summary{font-weight:bold;cursor:pointer}.ipa-panel [data-ipa-fields]:not([hidden]){display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}.ipa-panel label{display:grid;gap:5px;min-width:0}.ipa-panel input,.ipa-panel select,.ipa-panel textarea{width:100%;box-sizing:border-box;min-height:42px;padding:8px;border:1px solid #abc2cf;color:#17324d;font:inherit}.ipa-panel button{min-height:42px;padding:8px 12px;margin:8px 0}.ipa-panel p{font-size:13px;line-height:1.4}@media(max-width:700px){.ipa-panel [data-ipa-fields]:not([hidden]){grid-template-columns:1fr}}';document.head.append(style);
new MutationObserver(mount).observe(document.body,{childList:true,subtree:true});mount();
sb.auth.onAuthStateChange?.(event=>{if(event==='SIGNED_OUT'){epoch++;host?.remove();host=null;id=null;uid=null;row=null;initial={};}});
})();
