import {decideAccess} from './access-gate.mjs';
import{installAppHistory}from'./app-adapter.mjs';
// Explicit source integration only: call once after all application navigation wrappers.
// The history stores no account secrets; instance is disposed on principal change.
export async function bindAuthenticatedNavigation(sb,win=window){
 let instance=null,principal=null,epoch=0;
 async function session(session){const ticket=++epoch,next=session?.user?.id||null;if(next===principal&&((!next)||instance))return;if(instance){instance.dispose();instance=null;}principal=next;if(!next)return;const access=await decideAccess(sb);if(ticket!==epoch||access.kind!=='admin'||access.id!==next)return;
  // Initial login establishes authority; source auth already checks allowed admin.
  await Promise.resolve();if(ticket!==epoch)return;instance=installAppHistory(win,{scope:next});
 }
 if(!win.RighettoMobileNavigationReady){
  if(win.RighettoMobileNavigationFailed)throw Error('Navigazione interna non disponibile: usa il menu, non la freccia Indietro.');
  await new Promise((resolve,reject)=>{
   const clear=()=>{win.clearTimeout(timer);win.removeEventListener('righetto:navigation-ready',ready);win.removeEventListener('righetto:navigation-failed',failed);};
   const ready=()=>{clear();resolve();},failed=()=>{clear();reject(Error('Navigazione interna non disponibile: usa il menu, non la freccia Indietro.'));};
   const timer=win.setTimeout(failed,5000);
   win.addEventListener('righetto:navigation-ready',ready,{once:true});win.addEventListener('righetto:navigation-failed',failed,{once:true});
   if(win.RighettoMobileNavigationReady)ready();else if(win.RighettoMobileNavigationFailed)failed();
  });
 }
 const current=await sb.auth.getSession();await session(current.data?.session);
 const listener=sb.auth.onAuthStateChange((event,value)=>{setTimeout(()=>session(value),0);});
 return()=>{epoch++;instance?.dispose();listener.data?.subscription?.unsubscribe();};
}
