(function(){
var SB='https://qwkwkemuabfwvwuqrxlu.supabase.co';
var KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3a3drZW11YWJmd3Z3dXFyeGx1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE1OTk5NjEsImV4cCI6MjA4NzE3NTk2MX0.JxEYiWVPEOiwjZtbWAZRlMUdKXcupjw7filvrERCiqc';
var root=document.getElementById('rw-search');if(!root)return;
var L=(document.documentElement.lang||'en').toLowerCase();
var T={
en:{loc:'en-GB',all:'All',op:'I want to',buy:'Buy',rent:'Rent',type:'Property type',area:'Area',max:'Maximum price',any:'Any',search:'Search',reset:'Reset',homes:'Homes',com:'Commercial',land:'Land',
 count:function(n){return n+(n===1?' property found':' properties found')},none:'No property matches these filters. Change a filter or write to us: a suitable property may not be listed yet.',err:'The property list could not be loaded now. Please try again later or write to ginevra@righettoimmobiliare.it.',loading:'Loading the Righetto catalogue…',
 sale:'For sale',lease:'To rent',poa:'Price on request',pm:'/month',ref:'Ref.',rooms:function(n){return n+(n==1?' room':' rooms')},baths:function(n){return n+(n==1?' bathroom':' bathrooms')},ask:'View property details →',epc:'Energy class',subj:'Enquiry about property ',
 types:{appartamento:'Apartment',villa:'Villa',villetta:'Detached house',bifamiliare:'Two-family house',trifamiliare:'Three-family house',quadrifamiliare:'Four-family house',capannone:'Warehouse',ufficio:'Office',negozio:'Shop',terreno:'Land','':'Property'},title:function(t,c){return t+' in '+c}},
ar:{loc:'ar-u-nu-latn',all:'الكل',op:'أريد أن',buy:'أشتري',rent:'أستأجر',type:'نوع العقار',area:'المنطقة',max:'السعر الأقصى',any:'أي',search:'بحث',reset:'إعادة ضبط',homes:'منازل',com:'تجاري',land:'أرض',count:function(n){return 'عدد العقارات: '+n},none:'لا يوجد عقار مطابق لهذه الخيارات. غيّر أحد الخيارات أو راسلنا: قد يتوفر عقار مناسب لم يُنشر بعد.',err:'تعذر تحميل قائمة العقارات الآن. حاول لاحقاً أو راسل ginevra@righettoimmobiliare.it.',loading:'جارٍ تحميل كتالوج Righetto…',sale:'للبيع',lease:'للإيجار',poa:'السعر عند الطلب',pm:' / شهرياً',ref:'المرجع',rooms:function(n){return 'عدد الغرف: '+n},baths:function(n){return 'الحمامات: '+n},ask:'عرض تفاصيل العقار ←',epc:'فئة الطاقة',subj:'استفسار عن العقار ',types:{appartamento:'شقة',villa:'فيلا',villetta:'منزل مستقل',bifamiliare:'منزل لعائلتين',trifamiliare:'منزل لثلاث عائلات',quadrifamiliare:'منزل لأربع عائلات',capannone:'مستودع',ufficio:'مكتب',negozio:'محل تجاري',terreno:'أرض','':'عقار'},title:function(t,c){return t+' في '+c}},
tr:{loc:'tr-TR',all:'Tümü',op:'İstiyorum',buy:'Satın almak',rent:'Kiralamak',type:'Gayrimenkul türü',area:'Bölge',max:'En yüksek fiyat',any:'Fark etmez',search:'Ara',reset:'Sıfırla',homes:'Konut',com:'Ticari',land:'Arsa',count:function(n){return n+' gayrimenkul bulundu'},none:'Bu filtrelere uyan gayrimenkul yok. Bir filtreyi değiştirin veya bize yazın: uygun bir gayrimenkul henüz listelenmemiş olabilir.',err:'Gayrimenkul listesi şu anda yüklenemedi. Lütfen daha sonra deneyin veya ginevra@righettoimmobiliare.it adresine yazın.',loading:'Righetto kataloğu yükleniyor…',sale:'Satılık',lease:'Kiralık',poa:'Fiyat talep üzerine',pm:' / ay',ref:'Ref.',rooms:function(n){return n+' oda'},baths:function(n){return n+' banyo'},ask:'Gayrimenkul ayrıntılarını gör →',epc:'Enerji sınıfı',subj:'Gayrimenkul hakkında soru ',types:{appartamento:'Daire',villa:'Villa',villetta:'Müstakil ev',bifamiliare:'İki aileli ev',trifamiliare:'Üç aileli ev',quadrifamiliare:'Dört aileli ev',capannone:'Depo / atölye',ufficio:'Ofis',negozio:'Dükkân',terreno:'Arsa','':'Gayrimenkul'},title:function(t,c){return c+' · '+t}},
es:{loc:'es-ES',all:'Todos',op:'Quiero',buy:'Comprar',rent:'Alquilar',type:'Tipo de inmueble',area:'Zona',max:'Precio máximo',any:'Cualquiera',search:'Buscar',reset:'Borrar',homes:'Viviendas',com:'Comercial',land:'Terreno',count:function(n){return n===1?'1 inmueble encontrado':n+' inmuebles encontrados'},none:'Ningún inmueble coincide con estos filtros. Cambie un filtro o escríbanos: puede que un inmueble adecuado aún no esté publicado.',err:'No se pudo cargar la lista de inmuebles en este momento. Inténtelo más tarde o escriba a ginevra@righettoimmobiliare.it.',loading:'Cargando el catálogo de Righetto…',sale:'En venta',lease:'En alquiler',poa:'Precio a consultar',pm:' / mes',ref:'Ref.',rooms:function(n){return n+(n==1?' estancia':' estancias')},baths:function(n){return n+(n==1?' baño':' baños')},ask:'Ver detalles del inmueble →',epc:'Clase energética',subj:'Consulta sobre el inmueble ',types:{appartamento:'Apartamento',villa:'Villa',villetta:'Casa independiente',bifamiliare:'Casa bifamiliar',trifamiliare:'Casa trifamiliar',quadrifamiliare:'Casa cuadrifamiliar',capannone:'Nave',ufficio:'Oficina',negozio:'Local comercial',terreno:'Terreno','':'Inmueble'},title:function(t,c){return t+' en '+c}},
pt:{loc:'pt-BR',all:'Todos',op:'Quero',buy:'Comprar',rent:'Alugar',type:'Tipo de imóvel',area:'Área',max:'Preço máximo',any:'Qualquer',search:'Buscar',reset:'Limpar',homes:'Residencial',com:'Comercial',land:'Terreno',count:function(n){return n===1?'1 imóvel encontrado':n+' imóveis encontrados'},none:'Nenhum imóvel corresponde a estes filtros. Altere um filtro ou escreva para nós: um imóvel adequado pode ainda não estar listado.',err:'A lista de imóveis não pôde ser carregada agora. Tente novamente mais tarde ou escreva para ginevra@righettoimmobiliare.it.',loading:'Carregando o catálogo da Righetto…',sale:'À venda',lease:'Para alugar',poa:'Preço sob consulta',pm:' / mês',ref:'Ref.',rooms:function(n){return n+(n==1?' cômodo':' cômodos')},baths:function(n){return n+(n==1?' banheiro':' banheiros')},ask:'Ver detalhes do imóvel →',epc:'Classe energética',subj:'Consulta sobre o imóvel ',types:{appartamento:'Apartamento',villa:'Villa',villetta:'Casa isolada',bifamiliare:'Casa bifamiliar',trifamiliare:'Casa trifamiliar',quadrifamiliare:'Casa quadrifamiliar',capannone:'Galpão',ufficio:'Escritório',negozio:'Loja',terreno:'Terreno','':'Imóvel'},title:function(t,c){return t+' em '+c}}
};
var D=T[L.slice(0,2)]||T.en;
var HOMES=['appartamento','villa','villetta','bifamiliare','trifamiliare','quadrifamiliare'],COMM=['capannone','ufficio','negozio'];
function grp(t){return HOMES.indexOf(t)>-1?'homes':COMM.indexOf(t)>-1?'com':t==='terreno'?'land':'homes'}
function img(u){if(!u)return'';u=String(u).trim();if(!u)return'';if(/^img\//.test(u))return 'https://righettoimmobiliare.it/'+u;if(!/^https?:/.test(u))u=SB+'/storage/v1/object/public/'+u.replace(/^\/+/,'');return u}
function thumb(u){return u.indexOf('/storage/v1/object/public/')>-1?u.replace('/object/public/','/render/image/public/')+'?width=600&quality=75':u}
var STAGED={'LA0317':1};
function isai(u){return /foto[-_ ]?ai/i.test(String(u||''))}
function cover(c,fo){var f=fo[0]||'';if(f&&isai(f)&&!STAGED[c]){for(var k=1;k<fo.length;k++){if(!isai(fo[k]))return fo[k]}}return f}
function tc(s){return String(s||'').trim().toLowerCase().replace(/(^|[\s'-])([a-zà-ú])/g,function(m,a,b){return a+b.toUpperCase()})}
function el(h){var d=document.createElement('div');d.innerHTML=h;return d.firstChild}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
var data=[];
var f={op:'',type:'',area:'',max:''};
root.innerHTML='<form class="rw-psearch" onsubmit="return false"><label>'+D.op+'<select id="rwp-op"><option value="">'+D.all+'</option><option value="buy">'+D.buy+'</option><option value="rent">'+D.rent+'</option></select></label><label>'+D.type+'<select id="rwp-type"><option value="">'+D.any+'</option><option value="homes">'+D.homes+'</option><option value="com">'+D.com+'</option><option value="land">'+D.land+'</option></select></label><label>'+D.area+'<select id="rwp-area"><option value="">'+D.any+'</option></select></label><label>'+D.max+' (€)<select id="rwp-max"><option value="">'+D.any+'</option></select></label><button type="button" class="rw-button" id="rwp-reset">'+D.reset+'</button></form><p class="rw-pcount" id="rwp-count" role="status" aria-live="polite">'+D.loading+'</p><div class="rw-properties rw-pgrid" id="rwp-grid"></div>';
function pre(){try{var q=new URLSearchParams(location.search);['op','type','area'].forEach(function(k){var v=q.get(k);if(v&&document.querySelector('#rwp-'+k+' option[value="'+v+'"]')){f[k]=v;document.getElementById('rwp-'+k).value=v}})}catch(e){}}
function render(){
 var out=data.filter(function(i){
  if(f.op==='buy'&&i.op!=='vendita')return false;
  if(f.op==='rent'&&i.op.indexOf('affitto')!==0)return false;
  if(f.type&&grp(i.tipo)!==f.type)return false;
  if(f.area&&i.comune!==f.area)return false;
  if(f.max&&(!i.prezzo||i.prezzo>+f.max))return false;
  return true});
 var g=document.getElementById('rwp-grid');
 document.getElementById('rwp-count').textContent=out.length?D.count(out.length):D.none;
 g.innerHTML='';
 var nf=new Intl.NumberFormat(D.loc,{style:'currency',currency:'EUR',maximumFractionDigits:0});
 out.forEach(function(i){
  var rent=i.op.indexOf('affitto')===0;
  var price=i.prezzo?nf.format(i.prezzo)+(rent?D.pm:''):D.poa;
  var facts=[];if(i.mq)facts.push(i.mq+' m²');if(i.locali)facts.push(D.rooms(i.locali));if(i.bagni)facts.push(D.baths(i.bagni));
  var tl=D.title(D.types[i.tipo]||D.types[''],i.comune);
  var mail='/international/'+({ar:'ar/',tr:'tr/',pt:'pt-br/',es:'es/'}[L.slice(0,2)]||'')+'property/?ref='+encodeURIComponent(i.codice);
  var a=el('<a class="rw-property rw-pcard" href="'+mail+'">'+(i.foto?'<img alt="'+esc(tl)+'" loading="lazy" decoding="async" src="'+esc(thumb(i.foto))+'" onerror="this.onerror=null;this.src=\''+esc(i.foto)+'\'"/>':'<div class="rw-pnophoto"></div>')+(i.foto&&STAGED[i.codice]&&isai(i.foto)?'<span class="rw-aibadge">Foto AI</span>':'')+'<span class="rw-pbadge">'+(rent?D.lease:D.sale)+(i.ce?' · '+D.epc+' '+esc(i.ce):'')+'</span><b>'+esc(tl)+'</b><span class="rw-pprice">'+esc(price)+'</span><span>'+esc(facts.join(' · '))+'</span><span class="rw-pref">'+D.ref+' '+esc(i.codice)+'</span><small>'+D.ask+'</small></a>');
  g.appendChild(a)});document.dispatchEvent(new Event('rwfilter'))}
function fill(){
 var areas={},prices=[2e5,3e5,5e5,1e6];
 data.forEach(function(i){if(i.comune)areas[i.comune]=1});
 var sa=document.getElementById('rwp-area');Object.keys(areas).sort().forEach(function(k){var o=document.createElement('option');o.value=k;o.textContent=k;sa.appendChild(o)});
 var sm=document.getElementById('rwp-max'),nf=new Intl.NumberFormat(D.loc,{maximumFractionDigits:0});
 [1000,100000,200000,300000,500000,1000000].forEach(function(p){var o=document.createElement('option');o.value=p;o.textContent='≤ '+nf.format(p);sm.appendChild(o)});
 ['op','type','area','max'].forEach(function(k){document.getElementById('rwp-'+k).addEventListener('change',function(e){f[k]=e.target.value;render()})});
 document.getElementById('rwp-reset').addEventListener('click',function(){['op','type','area','max'].forEach(function(k){f[k]='';document.getElementById('rwp-'+k).value=''});render()});
}
var url=SB+'/rest/v1/immobili?select=codice,tipo_operazione,tipologia,comune,prezzo,superficie,locali,camere,bagni_totali,classe_energetica,venduto,affittato,foto&attivo=eq.true&order=in_evidenza.desc,created_at.desc&limit=200';
fetch(url,{headers:{apikey:KEY,Authorization:'Bearer '+KEY}}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(rows){
 data=rows.filter(function(r){return !r.venduto&&!r.affittato}).map(function(r){var fo=Array.isArray(r.foto)?r.foto:[];return{codice:r.codice||'',op:r.tipo_operazione||'vendita',tipo:r.tipologia||'',comune:tc(r.comune),prezzo:+r.prezzo||0,mq:+r.superficie||0,locali:+(r.locali||r.camere)||0,bagni:+r.bagni_totali||0,ce:r.classe_energetica||'',foto:img(cover(r.codice,fo))}});
 fill();pre();render()}).catch(function(){document.getElementById('rwp-count').textContent=D.err});
})();
