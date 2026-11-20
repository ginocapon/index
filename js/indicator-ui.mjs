import {createIndicatorStore} from './indicator-store.mjs';
import {eventSignal} from './indicator-model.mjs';
let epoch=0,expiryTimer=null,sortValues=new Map(),sortPrincipal=null;
export function indicatorSortValue(id,principal){if(globalThis.matchMedia?.('(max-width:768px)').matches)return principal&&principal===mobilePrincipal?(mobileSortValues.get(String(id))??null):null;return principal&&principal===sortPrincipal?(sortValues.get(String(id))??null):null;}
export async function renderIndicators({db,principal,principalNow,temporalPolicy,now=new Date(),root=document.querySelector('#immobiliTableWrap')}){
 clearTimeout(expiryTimer);expiryTimer=null;
 const ticket=++epoch,rows=[...root.querySelectorAll('tr[data-property-preview]')],ids=rows.map(r=>r.dataset.propertyPreview),alive=()=>ticket===epoch&&principalNow()===principal&&rows.every(r=>r.isConnected);
 sortValues=new Map();sortPrincipal=principal;
 const cells=rows.map(r=>r.querySelector('[data-property-indicators]'));
 for(const cell of cells)if(cell){cell.textContent='…';cell.title='Verifica attività e appuntamenti in corso';}
 if(!ids.length)return;
 try{
  const store=createIndicatorStore({db,principal,principalNow,isCurrent:alive}),data=await store.load(ids,{sources:['practices']});
  if(!alive())return;
  function paint(clock){
   if(!alive())return;
   let nextExpiry=Infinity;
   for(let i=0;i<rows.length;i++){
    const cell=cells[i];if(!cell)continue;const item=data.get(ids[i]),event=eventSignal({events:item.events,temporalPolicy,now:clock});cell.replaceChildren();
    const add=(color,label)=>{const dot=document.createElement('span');dot.className='rig-property-dot rig-property-dot-'+color;dot.role='img';dot.ariaLabel=label;dot.title=label;cell.append(dot);};
    if(item.activity.active)add('orange','Attività in corso');
    if(event.kind)add(event.kind,event.label);
    sortValues.set(String(ids[i]),(item.activity.active?4:0)+(event.kind==='green'?2:event.kind==='light'?1:0));
    cell.title=[item.activity.active?'Attività in corso':'',event.label].filter(Boolean).join(' · ')||'Nessuna attività o appuntamento aperto verificato';
    for(const entry of item.events){const end=+new Date(entry.ends_at||entry.starts_at);if(end>+clock)nextExpiry=Math.min(nextExpiry,end);}
   }
   window.RighettoPropertyGroupSort?.apply();
   // Expiry only repaints the checked data. It does not poll the account.
   if(Number.isFinite(nextExpiry))expiryTimer=setTimeout(()=>paint(new Date()),Math.min(86400000,Math.max(20,nextExpiry-Date.now()+20)));
  }
  paint(now);
 }catch(error){if(alive())for(const cell of cells)if(cell){cell.textContent='?';cell.title='Indicatori non verificati: '+error.message;}}
}
export function invalidateIndicators(){mobileEpoch++;mobileCache=null;mobilePrincipal=null;mobileSortValues.clear();clearTimeout(mobileTimer);epoch++;sortValues.clear();sortPrincipal=null;clearTimeout(expiryTimer);expiryTimer=null;}

// Mobile uses the same verified sources and temporal policy as the desktop table.
let mobileEpoch=0,mobileTimer=null,mobileCache=null,mobilePrincipal=null,mobileSortValues=new Map();
export async function renderMobileIndicators({db,principal,principalNow,temporalPolicy,read=true,root=document.querySelector('#rm-imm')}){
 if(!root)return;
 const cells=[...root.querySelectorAll('[data-mobile-property-indicators]')],ids=cells.map(c=>c.dataset.mobilePropertyIndicators);
 const ticket=++mobileEpoch;clearTimeout(mobileTimer);mobileTimer=null;
 const alive=()=>ticket===mobileEpoch&&principalNow()===principal&&cells.every(c=>c.isConnected);
 const mark=(text,title)=>cells.forEach(c=>{c.textContent=text;c.title=title;});
 if(!principal||!ids.length){mobileCache=null;return;}
 const key=principal+':'+ids.slice().sort().join(',');
 mark('…','Verifica attività e appuntamenti in corso');
 try{
  let data;
  if(!read&&mobileCache?.key===key)data=mobileCache.data;
  else{const store=createIndicatorStore({db,principal,principalNow,isCurrent:alive});data=await store.load(ids,{sources:['practices']});if(!alive())return;mobileCache={key,data};}
  if(!alive())return;
  function paint(clock){
   if(!alive())return;let expiry=Infinity,changed=mobilePrincipal!==principal;if(changed){mobileSortValues=new Map();mobilePrincipal=principal;}
   for(let n=0;n<ids.length;n++){
    const item=data.get(ids[n]);if(!item)throw Error('Immobile non verificato');
    const event=eventSignal({events:item.events,temporalPolicy,now:clock}),cell=cells[n];cell.replaceChildren();
    const add=(color,label)=>{const dot=document.createElement('span');dot.className='rig-property-dot rig-property-dot-'+color;dot.role='img';dot.ariaLabel=label;dot.title=label;cell.append(dot);};
    if(item.activity.active)add('orange','Attività in corso');if(event.kind)add(event.kind,event.label);
    cell.title=[item.activity.active?'Attività in corso':'',event.label].filter(Boolean).join(' · ')||'Nessuna attività o appuntamento aperto verificato';cell.setAttribute('aria-label',cell.title);
    const value=(item.activity.active?4:0)+(event.kind==='green'?2:event.kind==='light'?1:0);if(mobileSortValues.get(String(ids[n]))!==value)changed=true;mobileSortValues.set(String(ids[n]),value);
    for(const e of item.events){const end=+new Date(e.ends_at||e.starts_at);if(end>+clock)expiry=Math.min(expiry,end);}
   }
   if(Number.isFinite(expiry))mobileTimer=setTimeout(()=>paint(new Date()),Math.min(86400000,Math.max(20,expiry-Date.now()+20)));
   if(changed)window.RighettoPropertyGroupSort?.apply();
  }
  paint(new Date());
 }catch(error){if(alive()){mobileCache=null;for(const id of ids)mobileSortValues.delete(String(id));mark('?','Indicatori non verificati: '+error.message);}}
}
