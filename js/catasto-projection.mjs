/* Candidate only: map one explicitly chosen stored cadastral unit to original 1671 slots. */
const fields={categoria:'cat_category',comune_catastale:'cat_municipality',sezione:'cat_section',foglio:'cat_sheet',mappale:'cat_parcel',subalterno:'cat_subordinate',classe:'cat_class'};
export function chooseUnit(units,index){
 if(!Array.isArray(units)||!Number.isInteger(index)||index<0||index>=units.length)throw Error('Scegli una unità catastale esistente');
 const unit=units[index];if(!unit||typeof unit!=='object'||Array.isArray(unit))throw Error('Unità catastale non verificata');
 return {index,snapshot:JSON.stringify(unit)};
}
export function projectCadastral(units,choice){
 const values={},gaps=[];
 if(!choice)return {values,gaps:['Unità catastale non scelta: caselle lasciate vuote.']};
 if(!Array.isArray(units)||!Number.isInteger(choice.index)||!units[choice.index]||JSON.stringify(units[choice.index])!==choice.snapshot)throw Error('Unità catastale cambiata: rileggi e scegli di nuovo');
 const unit=units[choice.index];
 for(const [source,target]of Object.entries(fields)){
  const v=unit[source];if(v===null||v===undefined||v==='')continue;
  if(!['string','number'].includes(typeof v)||typeof v==='number'&&!Number.isFinite(v))throw Error('Campo catastale non verificato: '+source);
  values[target]=String(v).trim();
 }
 const income=unit.rendita;
 if(income!==null&&income!==undefined&&income!==''){
  // Original numeric value only: no parsing ambiguous separators, exponent or truncation.
  const raw=String(income);
  if(/^\d+(\.\d{1,2})?$/.test(raw)){const [a,b='']=raw.split('.');values.cat_income_int=a;values.cat_income_dec=b.padEnd(2,'0');}
  else gaps.push('Rendita con formato non verificato: caselle lasciate vuote.');
 }
 gaps.push('Valore catastale lasciato vuoto: valore_prima e valore_seconda non hanno una destinazione certificata nel modello.');
 return {values,gaps};
}
