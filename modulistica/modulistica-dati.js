/* Lettura SOLA LETTURA dei dati dal gestionale tramite il client autenticato gia' presente nell'admin (window.sb).
   Nessuna scrittura, nessun token qui. Se sb manca la pagina resta a campi manuali. */
(function(root,factory){ if(typeof module==='object'&&module.exports) module.exports=factory(); else root.ModulistDati=factory(); })(this,function(){
  var COLONNE_PERSONA={nome:'nome',codice_fiscale:'codice_fiscale',telefono:'telefono',email:'email',residenza:'indirizzo_cliente'};
  function s(x){return (x===undefined||x===null)?'':String(x);}
  function persona(row){
    var p={}; Object.keys(COLONNE_PERSONA).forEach(function(k){p[k]=s(row[COLONNE_PERSONA[k]]);});
    if(!p.nome&&row.ragione_sociale) p.nome=s(row.ragione_sociale);
    return p; // nato_a, nato_il, doc_*: nessuna colonna verificata, restano manuali
  }
  /* Riferimento interno NON accertato: serve solo a segnalare una possibile incoerenza. Non e' una verifica. */
  var CODICI_RIFERIMENTO={padova:'G224'};
  function verificaCodice(comune,codice){
    var c=s(comune).trim().toLowerCase(), k=s(codice).trim().toUpperCase();
    if(!k) return {stato:'nessun codice',msg:'Codice catastale non indicato: resta la riga da compilare.'};
    var r=CODICI_RIFERIMENTO[c];
    if(!r) return {stato:'non verificato',msg:'Codice '+k+' per '+(s(comune)||'comune non indicato')+': NON verificato. Controllare su visura o planimetria.'};
    if(r===k) return {stato:'da controllare',msg:'Codice '+k+' coincide con il riferimento interno per '+s(comune)+', ma NON e\' verificato: controllare su visura o planimetria.'};
    return {stato:'incoerente',msg:'ATTENZIONE: per '+s(comune)+' il riferimento interno indica '+r+', il dato letto e\' '+k+'. Dato NON verificato e non corretto in automatico: controllare su visura o planimetria.'};
  }
  function unitaNorm(u){var o={};Object.keys(u||{}).forEach(function(k){o[k]=s(u[k]);});
    if(/^[A-Za-z]\d{3}$/.test(o.comune_catastale||'')&&!o.codice_catastale){o.codice_catastale=o.comune_catastale.toUpperCase();o.comune_catastale='';}
    return o;}
  function immobile(row){
    var i={indirizzo:s(row.indirizzo),comune:s(row.comune),tipologia:s(row.tipologia)};
    i.unita_catastali=Array.isArray(row.unita_catastali)?row.unita_catastali.map(unitaNorm):[];
    return i;
  }
  function termini(row){var t={}; if(row.classe_energetica) t.ape_classe=s(row.classe_energetica); if(row.ipe_kwh!==undefined&&row.ipe_kwh!==null) t.ape_kwh=s(row.ipe_kwh); return t;}
  function pulisci(t){return String(t||'').replace(/[%,()]/g,' ').trim();}
  function cercaClienti(sb,term){
    term=pulisci(term); if(term.length<2) return Promise.resolve([]);
    return sb.from('clienti').select('id,nome,ragione_sociale,telefono,email').or('nome.ilike.%'+term+'%,ragione_sociale.ilike.%'+term+'%,telefono.ilike.%'+term+'%,email.ilike.%'+term+'%').order('nome').limit(15)
      .then(function(r){if(r.error)throw new Error(r.error.message);return r.data||[];});
  }
  function caricaCliente(sb,id){
    return sb.from('clienti').select('*').eq('id',id).maybeSingle().then(function(r){
      if(r.error)throw new Error(r.error.message); if(!r.data)throw new Error('cliente non trovato');
      return {persona:persona(r.data),colonne:Object.keys(r.data)};});
  }
  function caricaImmobile(sb,codice){
    codice=pulisci(codice);
    return sb.from('immobili').select('*').eq('codice',codice).limit(1).then(function(r){
      if(r.error)throw new Error(r.error.message); var row=(r.data||[])[0]; if(!row)throw new Error('immobile non trovato: '+codice);
      return sb.from('immobile_proprietari').select('cliente_id,ordine').eq('immobile_id',row.id).order('ordine').then(function(q){
        var ids=(q.error?[]:(q.data||[])).map(function(x){return x.cliente_id;});
        if(!ids.length) return {immobile:immobile(row),termini:termini(row),proprietari:[],nota:q.error?('proprietari non letti: '+q.error.message):'nessun proprietario collegato'};
        return sb.from('clienti').select('*').in('id',ids).then(function(c){
          var by={}; (c.data||[]).forEach(function(x){by[x.id]=x;});
          return {immobile:immobile(row),termini:termini(row),proprietari:ids.filter(function(id){return by[id];}).map(function(id){return persona(by[id]);})};});
      });
    });
  }
  return {verificaCodice:verificaCodice,unitaNorm:unitaNorm,persona:persona,immobile:immobile,termini:termini,cercaClienti:cercaClienti,caricaCliente:caricaCliente,caricaImmobile:caricaImmobile};
});
