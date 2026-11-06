/* Desktop property table: first-photo hover and existing read-only preview. */
(function(){'use strict';
 let popup=null,active=null;
 function sizeRows(){if(innerWidth<761)return;document.querySelectorAll('#immobiliTableWrap tr[data-property-preview]:not([data-doubled-row])').forEach(row=>{const height=row.getBoundingClientRect().height;if(height>0){row.dataset.doubledRow='1';row.style.height=(height*2)+'px';}});}
 sizeRows();
 const hover=()=>matchMedia('(hover:hover) and (pointer:fine)').matches;
 const current=id=>(typeof allImmobili!=='undefined'?allImmobili:[]).find(i=>String(i.id)===id);
 function hide(){popup?.remove();popup=null;active=null;}
 function allowed(raw){try{const u=new URL(raw,location.href);return ['https:','http:'].includes(u.protocol)?u.href:null;}catch{return null;}}
 function show(cell,mouse=false){hide();if((!mouse&&!hover())||!window.RighettoGatedPrincipal)return;const id=cell.closest('[data-property-preview]')?.dataset.propertyPreview,i=current(id);if(!i)return;const raw=Array.isArray(i.foto)&&i.foto.length?i.foto[0]:i.foto_principale;const url=typeof raw==='string'?allowed(raw):null;
  popup=document.createElement('div');popup.id='imm-first-photo';popup.setAttribute('role','tooltip');popup.style.cssText='position:fixed;z-index:16000;width:280px;max-width:calc(100vw - 24px);padding:8px;background:#fff;border:1px solid #b7cbd8;border-radius:8px;box-shadow:0 6px 24px #0003;pointer-events:none;color:#17324d;font:14px Arial';const text=document.createElement('div');text.textContent=(i.codice||'Immobile')+' - prima foto';popup.append(text);
  const status=document.createElement('p');status.style.margin='8px 0 0';status.textContent=url?'Caricamento foto…':'Nessuna foto disponibile.';popup.append(status);
  if(url){const img=document.createElement('img');img.alt='Prima foto '+(i.codice||'immobile');img.style.cssText='width:100%;height:180px;object-fit:contain;display:none;margin-top:8px';img.onload=()=>{if(popup?.contains(img)){img.style.display='block';status.remove();place(cell);}};img.onerror=()=>{if(popup?.contains(img)){img.remove();status.textContent='Foto non disponibile.';}};popup.append(img);img.src=url;}
  document.body.append(popup);active=cell;place(cell);
 }
 function place(cell){if(!popup)return;const r=cell.getBoundingClientRect(),b=popup.getBoundingClientRect();popup.style.left=Math.max(12,Math.min(r.right+10,innerWidth-b.width-12))+'px';popup.style.top=Math.max(12,Math.min(r.top,innerHeight-b.height-12))+'px';}
 function rowAction(e){const row=e.target.closest('#immobiliTableWrap [data-property-preview]');if(!row||e.target.closest('button,a,input,select,textarea,summary,label,[role=button],[contenteditable=true]')||getSelection()?.toString())return;if(!window.RighettoGatedPrincipal||!current(row.dataset.propertyPreview))return;hide();if(typeof previewImmobile==='function')previewImmobile(row.dataset.propertyPreview);}
 document.addEventListener('click',rowAction);
 document.addEventListener('keydown',e=>{if(e.key==='Escape')hide();if(e.key==='Enter'&&e.target.matches('#immobiliTableWrap [data-property-preview]')){e.preventDefault();rowAction(e);}});
 document.addEventListener('pointerover',e=>{const cell=e.target.closest('#immobiliTableWrap [data-first-photo]');if(cell&&cell!==active)show(cell,e.pointerType==='mouse');});
 document.addEventListener('pointerout',e=>{if(active&&e.target.closest('[data-first-photo]')===active&&!active.contains(e.relatedTarget))hide();});
 document.addEventListener('focusin',e=>{const cell=e.target.closest('#immobiliTableWrap [data-first-photo]');if(cell)show(cell);});document.addEventListener('focusout',e=>{if(e.target.closest('[data-first-photo]'))hide();});
 addEventListener('scroll',hide,true);addEventListener('resize',()=>{hide();sizeRows();});addEventListener('blur',hide);document.addEventListener('visibilitychange',()=>{if(document.hidden)hide();});
 if(typeof sb!=='undefined')sb.auth.onAuthStateChange?.(event=>{if(event==='SIGNED_OUT'||event==='SIGNED_IN')hide();});
 new MutationObserver(()=>{if(active&&!active.isConnected)hide();sizeRows();}).observe(document.documentElement,{childList:true,subtree:true,attributes:true,attributeFilter:['class','style','hidden']});
})();
