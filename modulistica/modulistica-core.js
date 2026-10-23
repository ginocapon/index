/* Compone i dati e compila i modelli DOCX (docxtemplater, MIT). Nessun accesso a rete o DB. */
(function(root,factory){ if(typeof module==='object'&&module.exports) module.exports=factory(); else root.Modulistica=factory(); })(this,function(){
  var Z='______________';
  var ROLES={'4020':['locatori','conduttori'],'21007':['venditori','proponenti'],'31341':['venditori']};
  var PDEF={nato_a:'____________',nato_il:'__/__/____',codice_fiscale:'________________',residenza:'____________________',doc_tipo:'__________',doc_numero:'________',doc_ente:'__________',doc_rilascio:'__/__/____',doc_scadenza:'__/__/____',telefono:'__________',email:'__________'};
  var TDEF={
   '4020':{dal:'__/__/____',al:'__/__/____',canone_annuo:'__________',rata_mensile:'__________',banca:'______________',iban:'IT____________________',deposito:'__________',ape_classe:'____',ape_kwh:'____',ape_data:'__/__/____',ape_perito:'__________',ape_albo:'____',ape_scadenza:'__/__/____',importo_mensile:'______',canone_mensile:'______',spese_mensili:'______'},
   '21007':{prezzo:'(-)',caparra:'(-)',importo_2:'(-)',data_2:'(-)',saldo:'(-)',data_rogito:'(-)',data_irrevocabile:'(-)',spese_registrazione:'(-)'},
   '31341':{destinazione:'______________________________',dal:'_____/____/________',al:'_____/____/________'}};
  function v(x,d){ return (x===undefined||x===null||String(x).trim()==='')?d:String(x); }
  function persone(list){
    list=(list&&list.length)?list:[{}];
    return list.map(function(p,k){ var o={nome:v(p.nome,Z),cognome:v(p.cognome,''),first:k===0,last:k===list.length-1};
      Object.keys(PDEF).forEach(function(f){o[f]=v(p[f],PDEF[f]);}); return o; });
  }
  function unita(i){ var u=(i.unita_catastali&&i.unita_catastali.length)?i.unita_catastali:[{}]; return u; }
  function catTesto(i){
    return unita(i).map(function(u,k){
      var s=(k?'; inoltre, unità n. '+(k+1)+', ':'')+'censito al N.C.E.U di categoria '+v(u.categoria,'___')+', comune catastale '+v(u.comune_catastale,'___')+', sezione '+v(u.sezione,'___')+', foglio '+v(u.foglio,'___')+', mappale '+v(u.mappale,'___')+', subalterno '+v(u.subalterno,'___')+', classe '+v(u.classe,'___')+', rendita '+v(u.rendita,'___')+' euro';
      if(v(u.valore_prima,'')) s+=', valore catastale '+u.valore_prima+' euro'; return s; }).join('');
  }
  function catIds(i){
    return unita(i).map(function(u){return 'Fg. '+v(u.foglio,'____')+' Part. '+v(u.mappale,'____')+' Sub. '+v(u.subalterno,'______');}).join('; ');
  }
  function contesto(mod,dati){
    dati=dati||{}; var i=dati.immobile||{}, t=dati.termini||{}, r=dati.ruoli||{}, d={};
    ROLES[mod].forEach(function(k){ d[k]=persone(r[k]); });
    d.i_indirizzo=v(i.indirizzo,'____________'); d.i_comune=v(i.comune,'____________'); d.i_tipologia=v(i.tipologia,'____________'); d.i_provincia=v(i.provincia,'____');
    var cv=v(i.civico,'');
    d.civico_a=cv?'n. '+cv+', ':''; d.civico_b=cv?' n. '+cv:'';
    d.ubicazione=i.indirizzo?(i.indirizzo+(cv?' n. '+cv:'')+', '+v(i.comune,'____')+' ('+v(i.provincia,'____')+')'):'______________________________';
    d.catasto_testo=catTesto(i); d.catasto_testo4=', '+catTesto(i); d.catasto_ids=catIds(i);
    var nomi=(r.venditori||[]).map(function(p){return v(p.nome,'')+(p.cognome?' '+p.cognome:'');}).filter(Boolean);
    d.proprieta_nomi=nomi.length?nomi.join(', '):'______________________________';
    d.lbl_locatori=(r.locatori&&r.locatori.length>1)?'locatori':'locatore';
    d.lbl_conduttori=(r.conduttori&&r.conduttori.length>1)?'conduttori':'conduttore';
    Object.keys(TDEF[mod]).forEach(function(k){ d['t_'+k]=v(t[k],TDEF[mod][k]); });
    if(mod==='31341') d.t_prezzo_richiesto=t.prezzo_richiesto&&String(t.prezzo_richiesto).trim()?'€ '+t.prezzo_richiesto:'()';
    return d;
  }
  function compila(mod,dati,zipData){ /* zipData: ArrayBuffer/Uint8Array/Buffer del DOCX modello */
    var PZ=(typeof PizZip!=='undefined')?PizZip:require('pizzip'), DX=(typeof docxtemplater!=='undefined')?docxtemplater:require('docxtemplater');
    var doc=new DX(new PZ(zipData),{paragraphLoop:true,nullGetter:function(){return '';}});
    doc.render(contesto(mod,dati));
    return doc.getZip().generate({compression:'DEFLATE',type:(typeof Buffer!=='undefined'&&typeof window==='undefined')?'nodebuffer':'uint8array',mimeType:'application/vnd.openxmlformats-officedocument.wordprocessingml.document'});
  }
  return {ROLES:ROLES,PDEF:PDEF,TDEF:TDEF,contesto:contesto,compila:compila};
});
