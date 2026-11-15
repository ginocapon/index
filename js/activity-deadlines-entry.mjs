import {createDeadlineStore} from './activity-deadlines.mjs?v=20261115-annual-labels-v1';
import {mountDeadlinePanel} from './activity-deadlines-ui.mjs?v=20261115-annual-labels-v1';
const agents=Object.freeze({'5f55e259-0d0b-46d9-8d77-17ab33db0fdf':'Gino','d082a978-3da9-4eeb-94c9-8cf885230161':'Linda'});
let ctl=null,owner=null;
function clear(){ctl?.destroy();ctl=null;owner=null;}
function setup(){const p=window.RighettoGatedPrincipal;if(!p||!agents[p]||typeof sb==='undefined'){clear();return;}if(owner!==p){clear();owner=p;const store=createDeadlineStore({db:sb,principal:p,timeEnabled:false});ctl=mountDeadlinePanel({store,principal:p,agent:agents[p],openPractice:id=>window.RighettoOpenPractice?.(id)});}else ctl.refresh();}
window.addEventListener('righetto:section-ready',setup);
if(typeof sb!=='undefined')sb.auth.onAuthStateChange((event,session)=>{if(!session||session.user?.id!==owner)clear();});
setup();
