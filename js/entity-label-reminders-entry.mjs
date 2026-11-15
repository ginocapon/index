import{createEntityLabelReminderStore}from'./entity-label-reminders-store.mjs?v=20261115-label-annual-v2';
import{openEntityLabelReminder}from'./entity-label-reminders-ui.mjs?v=20261115-label-annual-v2';
let owner=null,cached=null;
function store(){const p=window.RighettoGatedPrincipal;if(!p||typeof sb==='undefined')throw Error('Accesso amministratore richiesto');if(owner!==p){owner=p;cached=createEntityLabelReminderStore({db:sb,principal:p,enabled:true});}return cached;}
async function open({kind,id,labelId,associationId}){const principal=window.RighettoGatedPrincipal;if(!principal)return;try{const snapshot=await window.RighettoActivityFeatures.store().labelsFor(kind,id);if(window.RighettoGatedPrincipal!==principal)return;const link=snapshot.links.find(v=>v.id===associationId&&v.etichetta_id===labelId&&v.attiva),label=snapshot.labels.find(v=>v.id===labelId);if(!link||!label)throw Error('Abbinamento cambiato: riapri la scheda');const target=snapshot.target,entityTitle=kind==='clienti'?[target.nome,target.ragione_sociale].filter(Boolean).join(' · '):kind==='immobili'?[target.codice,target.titolo,target.indirizzo,target.comune].filter(Boolean).join(' · '):target.titolo||target.testo||'';return openEntityLabelReminder({kind,id,label,associationId,entityTitle,store:store(),principal});}catch(e){window.toast?.(e.message||'Promemoria non leggibile','error');}}
window.RighettoLabelReminders={store,open};
window.addEventListener('righetto:label-reminders-changed',()=>window.dispatchEvent(new Event('righetto:activities-changed')));
if(typeof sb!=='undefined')sb.auth.onAuthStateChange((event,session)=>{if(session?.user?.id!==owner){owner=null;cached=null;document.querySelectorAll('[data-lr-body]').forEach(h=>h.closest('.fx-overlay')?.remove());}});

window.dispatchEvent(new Event('righetto:activities-changed'));
