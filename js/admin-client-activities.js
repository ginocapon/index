/* Same practices filtered by stable client id. No copy, no automatic creation. */
(function(){'use strict';
async function mount({host,clientId,db,principal,isCurrent=()=>true}){
 const alive=()=>host.isConnected&&!host.hidden&&isCurrent()&&window.RighettoGatedPrincipal===principal;
 host.textContent='Caricamento pratiche del cliente...';
 try{if(!alive())return;const u=await db.auth.getUser(),a=await db.rpc('righetto_is_admin_request');if(!alive())return;if(u.error||u.data.user?.id!==principal||a.error||a.data!==true)throw Error('Accesso non confermato');const c=await db.from('clienti').select('id').eq('id',clientId).single();if(!alive())return;if(c.error||c.data?.id!==clientId)throw Error('Cliente non verificato');const store=window.RighettoAttivita.dbStore(db),properties=await store.properties();if(!alive())return;return await window.RighettoAttivita.init(host,{store,properties,clientId,principal,isActive:alive,openProperty:id=>{if(window.editImmobile)window.editImmobile(id);}});}catch(e){if(alive())host.textContent='Pratiche non disponibili: '+e.message;}
}
window.RighettoClientActivities={mount};})();
