/* Cliente: solo spostamento della finestra con mouse, nessun campo o salvataggio. */
(function(){
'use strict';
const overlay=document.getElementById('clienteModal');
const dialog=overlay?.querySelector('.modal');
const bar=overlay?.querySelector('.client-edit-head') || overlay?.querySelector('.modal-header');
if(!dialog||!bar)return;
const desktop=matchMedia('(min-width:761px)');
let drag=null,x=0,y=0;
function end(){if(drag){const id=drag.id;drag=null;if(bar.hasPointerCapture(id))bar.releasePointerCapture(id);}bar.classList.remove('rc-client-dragging');}
function reset(){end();x=0;y=0;dialog.style.translate='';}
const style=document.createElement('style');
style.textContent='@media(min-width:761px){#clienteModal .client-edit-head{cursor:move}#clienteModal .client-edit-head button{cursor:pointer}#clienteModal .client-edit-head.rc-client-dragging{user-select:none}}';
document.head.append(style);
bar.addEventListener('pointerdown',e=>{
 if(!desktop.matches||e.pointerType!=='mouse'||e.button!==0||!overlay.classList.contains('open')||e.target.closest('button,a,input,textarea,select,label,[contenteditable]'))return;
 const r=dialog.getBoundingClientRect(),h=bar.getBoundingClientRect();
 drag={id:e.pointerId,startX:e.clientX,startY:e.clientY,x,y,left:r.left,top:r.top,width:r.width,headerHeight:h.height};
 bar.setPointerCapture(e.pointerId);bar.classList.add('rc-client-dragging');e.preventDefault();
});
bar.addEventListener('pointermove',e=>{
 if(!drag||e.pointerId!==drag.id)return;
 const pad=8,w=document.documentElement.clientWidth,h=document.documentElement.clientHeight;
 const minDx=pad-drag.left,maxDx=Math.max(minDx,w-pad-drag.width-drag.left);
 const minDy=pad-drag.top,maxDy=Math.max(minDy,h-pad-drag.headerHeight-drag.top);
 const dx=Math.min(maxDx,Math.max(minDx,e.clientX-drag.startX));
 const dy=Math.min(maxDy,Math.max(minDy,e.clientY-drag.startY));
 x=drag.x+dx;y=drag.y+dy;dialog.style.translate=x+'px '+y+'px';
});
bar.addEventListener('pointerup',end);bar.addEventListener('pointercancel',end);bar.addEventListener('lostpointercapture',end);
new MutationObserver(()=>{if(!overlay.classList.contains('open'))reset();}).observe(overlay,{attributes:true,attributeFilter:['class']});
addEventListener('resize',reset);addEventListener('blur',end);desktop.addEventListener('change',reset);
})();
