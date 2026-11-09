export const countKeys=['camere','bagni','posto_auto','locali'];
export const countLabels={camere:'Camere',bagni:'Bagni',posto_auto:'Posto auto',locali:'Numero locali'};
export const countChoices=[['unset','Non definito'],['0','0'],['1','1'],['2','2'],['3','3'],['gt3','più di 3']];
export function normalizeCounts(raw){if(raw===undefined)return undefined;if(!raw||typeof raw!=='object'||Array.isArray(raw)||Object.keys(raw).length!==4||countKeys.some(k=>!countChoices.some(([v])=>v===raw[k])))throw Error('Conteggi non supportati: riaprire senza modificare i valori originali');return Object.fromEntries(countKeys.map(k=>[k,raw[k]]));}
const count=v=>typeof v==='number'&&Number.isSafeInteger(v)&&v>=0?v:null;
export function propertyCount(property,key){
 if(key!=='bagni')return count(property[key]);
 if(['bagni_totali','bagni'].some(k=>property[k]!==null&&property[k]!==undefined&&count(property[k])===null))return null;
 const a=count(property.bagni_totali),b=count(property.bagni);
 if(a!==null&&b!==null&&a!==b)return null;
 return a??b;
}
export function compareCounts(raw,property){const failed=[],unknown=[],checked=[];let c;try{c=normalizeCounts(raw);}catch(e){return{failed,unknown:[e.message],checked}}if(!c)return{failed,unknown,checked};for(const key of countKeys){const criterion=c[key];if(criterion==='unset')continue;const v=propertyCount(property,key),label=countLabels[key];if(v===null)unknown.push(label+' immobile non verificato');else if(criterion==='gt3'?v<=3:v!==Number(criterion))failed.push(label+' fuori dai criteri');else checked.push(label+': '+(criterion==='gt3'?'più di 3':criterion));}return{failed,unknown,checked};}
