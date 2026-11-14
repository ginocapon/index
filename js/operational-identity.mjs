/* PRIVATE CANDIDATE. No login, DB mutation or message send. Profile != assigned agent. */
const profiles=Object.freeze({
 '5f55e259-0d0b-46d9-8d77-17ab33db0fdf':Object.freeze({label:'Gino',signature:'Gino, Righetto Immobiliare'}),
 'd082a978-3da9-4eeb-94c9-8cf885230161':Object.freeze({label:'Linda',signature:'Linda, Righetto Immobiliare'})
});
export async function readOperationalIdentity({db,principal,principalNow,isCurrent=()=>true}){
 const alive=()=>{if(!principal||principalNow()!==principal||!isCurrent())throw Error('Sessione o schermata cambiata');};
 alive();const u=await db.auth.getUser();alive();if(u.error||u.data?.user?.id!==principal)throw Error('Identità non verificata');
 const a=await db.rpc('righetto_is_admin_request');alive();if(a.error||a.data!==true)throw Error('Accesso amministratore richiesto');
 const p=profiles[principal];if(!p)throw Error('Profilo operativo non configurato: nessun ripiego su Gino');
 return Object.freeze({...p,userId:principal});
}
export function newAppointmentDraft(identity,explicit={}){if(!identity?.userId||!identity.label)throw Error('Identità richiesta');return {...explicit,agents:explicit.agents?.length?[...explicit.agents]:[identity.label]};}
export function propertyMessageDraft(identity,parts){if(!identity?.signature)throw Error('Identità richiesta');return 'Buongiorno, le segnalo questi immobili.\n\n'+parts.join('\n\n')+'\n\n'+identity.signature;}
/* requestedEmail is a profile parameter, NOT proof that a mailbox is configured or permission to send. */
