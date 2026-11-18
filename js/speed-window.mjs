export function completedRomeWindow(now=new Date()){
 if(!Number.isFinite(now.getTime()))throw Error('Data non verificata');
 const parts=d=>Object.fromEntries(new Intl.DateTimeFormat('en-GB',{timeZone:'Europe/Rome',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit',hourCycle:'h23'}).formatToParts(d).filter(p=>p.type!=='literal').map(p=>[p.type,Number(p.value)]));
 const p=parts(now),endCivil=Date.UTC(p.year,p.month-1,p.day),startCivil=endCivil-28*86400000;
 const midnight=civil=>{let t=civil;for(let n=0;n<4;n++){const z=parts(new Date(t)),shown=Date.UTC(z.year,z.month-1,z.day,z.hour,z.minute,z.second),delta=civil-shown;if(delta===0)return new Date(t).toISOString();t+=delta;}throw Error('Confine orario non verificato');};
 const civilDate=t=>new Date(t).toISOString().slice(0,10).split('-').reverse().join('/');
 return {start:midnight(startCivil),end:midnight(endCivil),days:28,timezone:'Europe/Rome',label:civilDate(startCivil)+' - '+civilDate(endCivil-86400000)+', 28 giorni completi'};
}
