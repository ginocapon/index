/* Date-only annual projections. Does not write or create calendar events. */
import {validDay,plusDays,romeDay} from './activity-deadlines.mjs?v=20261115-annual-labels-v1';
export function anniversary(anchor,year,leapPolicy=null){
 if(!validDay(anchor)||!Number.isInteger(year)||year<Number(anchor.slice(0,4))||year>9998)throw Error('Annualità non valida');
 const value=String(year).padStart(4,'0')+anchor.slice(4);
 if(validDay(value))return value;
 if(anchor.slice(5)!=='02-29'||!['feb28','mar01'].includes(leapPolicy))throw Error('Per il 29 febbraio scegli 28 febbraio o 1 marzo negli anni non bisestili');
 return String(year).padStart(4,'0')+(leapPolicy==='feb28'?'-02-28':'-03-01');
}
export function annualOccurrences(series,completed=[],today=romeDay()){
 if(!series||!series.activityId||!validDay(series.anchor)||!validDay(today)||series.frequency!=='annual'||series.reminderDays!==30)throw Error('Ricorrenza non valida');
 if(series.anchor.slice(5)==='02-29'&&!['feb28','mar01'].includes(series.leapPolicy))throw Error('Scegli la regola per il 29 febbraio');
 const start=Number(series.anchor.slice(0,4)),recordedMax=Math.max(start-1,...completed.map(x=>Number.isInteger(x.year)?x.year:start-1)),end=Math.min(9998,Math.max(start,Number(today.slice(0,4))+1,recordedMax+1));
 if(end-start>150)throw Error('Intervallo ricorrenza da verificare');
 const done=new Map();for(const item of completed){if(item.activityId!==series.activityId||!Number.isInteger(item.year)||item.year<start||done.has(item.year))throw Error('Annualità incoerenti o duplicate');done.set(item.year,item);}
 const out=[];for(let year=start;year<=end;year++){
  const dueDay=anniversary(series.anchor,year,series.leapPolicy),baseReminderDay=plusDays(dueDay,-30),saved=done.get(year);if(saved?.reminderOverride&&(!validDay(saved.reminderOverride)||saved.reminderOverride<baseReminderDay))throw Error('Rinvio promemoria incoerente');const reminderDay=saved?.reminderOverride||baseReminderDay;
  out.push({id:series.activityId+':'+year,activityId:series.activityId,year,dueDay,reminderDay,done:!!saved?.completedAt,completedAt:saved?.completedAt||null,overdue:dueDay<today&&!saved?.completedAt,reminding:reminderDay<=today&&!saved?.completedAt,version:saved?.version||0});
 }return out;
}
export function nextOpenAnnual(series,completed=[],today=romeDay()){
 return annualOccurrences(series,completed,today).find(x=>!x.done)||null;
}
export function annualAgendaRows(series,completed=[],today=romeDay()){
 return annualOccurrences(series,completed,today).filter(x=>!x.done).flatMap(x=>[{...x,calendarDay:x.reminderDay,kind:'reminder'},{...x,calendarDay:x.dueDay,kind:'deadline'}]);
}
