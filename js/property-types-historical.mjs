import {additionalChains} from './property-types.mjs';
/* Extra labels never bypass historical identity/result evidence. They can only move a type-only exclusion to review. */
export function historicalExtraCandidate(requestCriteria,property,d){
 const chains=additionalChains(property,d);if(!chains.length)return false;
 const groups=(requestCriteria.generic_type_groups||[]).map(x=>String(x.id)),specific=(requestCriteria.specific_types||[]).map(x=>String(x.id));
 if(!groups.length)return false;
 return chains.some(c=>groups.includes(c.generic_id)&&(!specific.length||specific.includes(c.specific_type_id)));
}
