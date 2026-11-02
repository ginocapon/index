// Route identifiers only. Form values never enter history, URL or storage.
export function createHistoryRouter({win=window,read,render,valid,scope='local-fixture',dirty=()=>false,confirmLeave=()=>win.confirm('Ci sono modifiche non salvate. Uscire dalla schermata senza salvarle?'),onError=error=>win.alert(error.message)}){
 const prior=win.history.state,token=prior?.righettoNav===1&&prior.scope===scope&&typeof prior.token==='string'?prior.token:win.crypto.randomUUID();
 let index=prior?.token===token&&Number.isInteger(prior.index)?prior.index:0,current=read(),busy=false,reverting=false,disposed=false;
 const state=(route,n)=>({righettoNav:1,scope,token,index:n,route});
 const url=route=>{const u=new URL(win.location.href);u.hash=route.section;return u.pathname+u.search+u.hash;};
 const accept=()=>!dirty()||confirmLeave();
 async function navigate(route,{replace=false}={}){
  if(disposed||!valid(route)||busy)return false;if(JSON.stringify(route)===JSON.stringify(current))return true;
  if(!accept())return false;busy=true;
  try{await render(route);if(disposed)return false;current=route;index+=replace?0:1;win.history[replace?'replaceState':'pushState'](state(route,index),'',url(route));return true;}
  catch(e){try{await render(current);}catch{}onError(e);return false;}finally{busy=false;}
 }
 async function pop(event){
  if(disposed)return;
  if(reverting){reverting=false;return;}
  const next=event.state;if(!next||next.righettoNav!==1||next.token!==token||next.scope!==scope||!valid(next.route))return;
  const delta=next.index-index;if(!delta)return;
  if(busy||!accept()){reverting=true;win.history.go(-delta);return;}
  busy=true;
  try{await render(next.route);if(disposed)return;current=next.route;index=next.index;}
  catch(e){try{await render(current);}catch{}reverting=true;win.history.go(-delta);onError(e);}
  finally{busy=false;}
 }
 const unload=e=>{if(dirty()){e.preventDefault();e.returnValue='';}};
 win.history.replaceState(state(current,index),'',url(current));win.addEventListener('popstate',pop);win.addEventListener('beforeunload',unload);
 return {navigate,get current(){return structuredClone(current);},get busy(){return busy;},dispose(){disposed=true;win.removeEventListener('popstate',pop);win.removeEventListener('beforeunload',unload);}};
}
