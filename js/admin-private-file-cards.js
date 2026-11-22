/* Measure only the existing send-button typography. No file or account operations. */
(function(){'use strict';
function measure(){
 const host=document.createElement('div');host.className='rig-file-actions';host.setAttribute('aria-hidden','true');host.inert=true;host.style.cssText='position:fixed;left:-10000px;top:0;visibility:hidden;width:max-content;max-width:none;flex-wrap:nowrap;pointer-events:none';
 for(const text of ['Scegli file per email','Scegli file per WhatsApp']){const b=document.createElement('button');b.type='button';b.textContent=text;host.append(b);}
 document.body.append(host);const [a,b]=host.children,ra=a.getBoundingClientRect(),rb=b.getBoundingClientRect();
 if(ra.width>0&&rb.width>0){const width=rb.right-ra.left;document.documentElement.style.setProperty('--rig-private-card-width',width+'px');}
 host.remove();
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',measure,{once:true});else measure();
window.addEventListener('resize',measure,{passive:true});document.fonts?.ready.then(measure);
})();
