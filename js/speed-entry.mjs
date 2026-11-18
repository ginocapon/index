import {createSpeedReader}from './speed-private-reader.mjs';
import {createSpeedUI}from './speed-ui.mjs?v=20261118-growth-v1';
const OWNER='5f55e259-0d0b-46d9-8d77-17ab33db0fdf';
let active=null,epoch=0;
function stop(){epoch++;active?.reader?.stop();active?.ui?.destroy();active?.pageHost?.remove();active?.stripHost?.remove();active=null;}
function syncMobile(){const menu=document.querySelector("#rm-menu .rm-other"),existing=document.getElementById("rig-speed-mobile-open");if(window.RighettoGatedPrincipal!==OWNER){existing?.remove();return;}if(menu&&!existing){const b=document.createElement("button");b.id="rig-speed-mobile-open";b.type="button";b.className="rm-big";b.dataset.go="analytics";b.textContent="Speed";menu.insertBefore(b,menu.querySelector("a"));}}
async function sync(){syncMobile();document.querySelectorAll('nav [data-section=analytics]').forEach(link=>link.textContent=window.RighettoGatedPrincipal===OWNER?'Speed':'Search Console');const area=document.body.dataset.adminArea;if(!['home','analytics'].includes(area)||window.RighettoGatedPrincipal!==OWNER){stop();return;}if(active){if(area==='analytics'){const title=document.getElementById('topbarTitle');if(title)title.textContent='Speed';}return;}if(area==='analytics'){const title=document.getElementById('topbarTitle');if(title)title.textContent='Speed';}const ticket=++epoch;
 const section=document.getElementById('sec-searchconsole'),home=document.getElementById('sec-home');if(!section||!home||typeof sb==='undefined')return;
 const pageHost=document.createElement('section'),stripHost=document.createElement('aside');section.replaceChildren(pageHost);home.prepend(stripHost);
 // Scope styles within shadow roots, no old admin CSS overwritten.
 const state={reader:null,ui:null,pageHost,stripHost};active=state;
 try{const response=await fetch(new URL('./speed.css?v=20261118-growth-v1',import.meta.url));if(!response.ok)throw Error('Stile non disponibile');const css=await response.text();if(active!==state||ticket!==epoch)return;const ui=createSpeedUI({pageHost,stripHost,css,openSpeed:()=>window.showSection('analytics')});state.ui=ui;ui.loading();state.reader=createSpeedReader({sb,onClear:()=>ui.clear()});const result=await state.reader.read();if(active!==state||ticket!==epoch)return;if(result.state==='empty')ui.clear('Archivio Speed vuoto. Nessun dato da mostrare.');else ui.setRows(result.rows);
 }catch(error){if(active===state){if(state.ui)state.ui.clear('Dati Speed non verificati. Nessun valore confermato.');else pageHost.textContent='Speed non disponibile. Nessun valore confermato.';}}
}
window.addEventListener('righetto:section-ready',sync);
window.addEventListener('righetto:owner-ready',sync);
if(typeof sb!=='undefined')sb.auth.onAuthStateChange((_event,session)=>{if(session?.user?.id!==OWNER){document.getElementById('rig-speed-mobile-open')?.remove();stop();}});
if(window.rigOwnerReady)window.rigOwnerReady(sync);else sync();
