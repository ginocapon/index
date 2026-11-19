import {createIndicatorStore} from './indicator-store.mjs';
import {eventSignal} from './indicator-model.mjs';
let epoch=0,expiryTimer=null,sortValues=new Map(),sortPrincipal=null;
export function indicatorSortValue(id,principal){return principal&&principal===sortPrincipal?(sortValues.get(String(id))??null):null;}
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
export function invalidateIndicators(){epoch++;sortValues.clear();sortPrincipal=null;clearTimeout(expiryTimer);expiryTimer=null;}
