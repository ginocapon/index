(function(){
var SB='https://qwkwkemuabfwvwuqrxlu.supabase.co';
var KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3a3drZW11YWJmd3Z3dXFyeGx1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE1OTk5NjEsImV4cCI6MjA4NzE3NTk2MX0.JxEYiWVPEOiwjZtbWAZRlMUdKXcupjw7filvrERCiqc';
var root=document.getElementById('rw-pdetail');if(!root)return;
var L=(document.documentElement.lang||'en').toLowerCase().slice(0,2);
var T={
en:{loc:'en-GB',back:'← Back to the catalogue',cat:'/international/properties/',sale:'For sale',lease:'To rent',poa:'Price on request',pm:' / month',ref:'Ref.',facts:'Key facts',feat:'Features',op:'Offer',price:'Price',type:'Type',place:'Municipality',area:'Surface',rooms:'Rooms',beds:'Bedrooms',baths:'Bathrooms',epc:'Energy class',year:'Year built',floor:'Floor',loading:'Loading the property…',gone:'This property is no longer available or the reference was not found.',err:'The property could not be loaded now. Please try again later or write to ginevra@righettoimmobiliare.it.',
 ask:'Ask about this property',contact:'Your international contact',role:'Dott.ssa Ginevra Capon',cta:'Write an email',note:'The exact address is shared only after an enquiry. Photos and details come from the Righetto catalogue; confirm price, availability and condition with the agency.',subj:'Enquiry about property ',body:'Hello, I would like more information about property ',gl:'Photos',
 f:{giardino:'Garden',garage:'Garage',terrazzo:'Terrace',cantina:'Cellar',ascensore:'Lift'},
 types:{appartamento:'Apartment',villa:'Villa',villetta:'Detached house',bifamiliare:'Two-family house',trifamiliare:'Three-family house',quadrifamiliare:'Four-family house',capannone:'Warehouse',ufficio:'Office',negozio:'Shop',terreno:'Land','':'Property'},title:function(t,c){return t+' in '+c}},
ar:{loc:'ar-u-nu-latn',back:'العودة إلى الكتالوج →',cat:'/international/ar/properties/',sale:'للبيع',lease:'للإيجار',poa:'السعر عند الطلب',pm:' / شهرياً',ref:'المرجع',facts:'أهم المعلومات',feat:'المزايا',op:'العرض',price:'السعر',type:'النوع',place:'البلدية',area:'المساحة',rooms:'الغرف',beds:'غرف النوم',baths:'الحمامات',epc:'فئة الطاقة',year:'سنة البناء',floor:'الطابق',loading:'جارٍ تحميل العقار…',gone:'هذا العقار لم يعد متاحاً أو لم يتم العثور على المرجع.',err:'تعذر تحميل العقار الآن. حاول لاحقاً أو راسل ginevra@righettoimmobiliare.it.',
 ask:'استفسر عن هذا العقار',contact:'جهة اتصالك الدولية',role:'Dott.ssa Ginevra Capon',cta:'اكتب رسالة بريد إلكتروني',note:'لا نشارك العنوان الدقيق إلا بعد الاستفسار. الصور والتفاصيل من كتالوج Righetto؛ يرجى تأكيد السعر والتوفر والحالة مع الوكالة.',subj:'استفسار عن العقار ',body:'مرحباً، أود الحصول على مزيد من المعلومات عن العقار ',gl:'الصور',
 f:{giardino:'حديقة',garage:'مرآب',terrazzo:'تراس',cantina:'قبو',ascensore:'مصعد'},
 types:{appartamento:'شقة',villa:'فيلا',villetta:'منزل مستقل',bifamiliare:'منزل لعائلتين',trifamiliare:'منزل لثلاث عائلات',quadrifamiliare:'منزل لأربع عائلات',capannone:'مستودع',ufficio:'مكتب',negozio:'محل تجاري',terreno:'أرض','':'عقار'},title:function(t,c){return t+' في '+c}},
tr:{loc:'tr-TR',back:'← Kataloğa dön',cat:'/international/tr/properties/',sale:'Satılık',lease:'Kiralık',poa:'Fiyat talep üzerine',pm:' / ay',ref:'Ref.',facts:'Temel bilgiler',feat:'Özellikler',op:'Teklif',price:'Fiyat',type:'Tür',place:'Belediye',area:'Alan',rooms:'Oda',beds:'Yatak odası',baths:'Banyo',epc:'Enerji sınıfı',year:'Yapım yılı',floor:'Kat',loading:'Gayrimenkul yükleniyor…',gone:'Bu gayrimenkul artık mevcut değil veya referans bulunamadı.',err:'Gayrimenkul şu anda yüklenemedi. Lütfen daha sonra deneyin veya ginevra@righettoimmobiliare.it adresine yazın.',
 ask:'Bu gayrimenkul hakkında sorun',contact:'Uluslararası iletişim kişiniz',role:'Dott.ssa Ginevra Capon',cta:'E-posta yazın',note:'Kesin adres yalnızca bir talepten sonra paylaşılır. Fotoğraflar ve bilgiler Righetto kataloğundan gelir; fiyat, müsaitlik ve durumu acenteyle doğrulayın.',subj:'Gayrimenkul hakkında soru ',body:'Merhaba, şu gayrimenkul hakkında daha fazla bilgi almak istiyorum: ',gl:'Fotoğraflar',
 f:{giardino:'Bahçe',garage:'Garaj',terrazzo:'Teras',cantina:'Kiler',ascensore:'Asansör'},
 types:{appartamento:'Daire',villa:'Villa',villetta:'Müstakil ev',bifamiliare:'İki aileli ev',trifamiliare:'Üç aileli ev',quadrifamiliare:'Dört aileli ev',capannone:'Depo / atölye',ufficio:'Ofis',negozio:'Dükkân',terreno:'Arsa','':'Gayrimenkul'},title:function(t,c){return c+' · '+t}},
pt:{loc:'pt-BR',back:'← Voltar ao catálogo',cat:'/international/pt-br/properties/',sale:'À venda',lease:'Para alugar',poa:'Preço sob consulta',pm:' / mês',ref:'Ref.',facts:'Dados principais',feat:'Características',op:'Oferta',price:'Preço',type:'Tipo',place:'Município',area:'Área',rooms:'Cômodos',beds:'Quartos',baths:'Banheiros',epc:'Classe energética',year:'Ano de construção',floor:'Andar',loading:'Carregando o imóvel…',gone:'Este imóvel não está mais disponível ou a referência não foi encontrada.',err:'O imóvel não pôde ser carregado agora. Tente novamente mais tarde ou escreva para ginevra@righettoimmobiliare.it.',
 ask:'Pergunte sobre este imóvel',contact:'Sua pessoa de contato internacional',role:'Dott.ssa Ginevra Capon',cta:'Escrever um e-mail',note:'O endereço exato só é compartilhado após uma consulta. Fotos e dados vêm do catálogo da Righetto; confirme preço, disponibilidade e estado com a agência.',subj:'Consulta sobre o imóvel ',body:'Olá, gostaria de mais informações sobre o imóvel ',gl:'Fotos',
 f:{giardino:'Jardim',garage:'Garagem',terrazzo:'Terraço',cantina:'Porão',ascensore:'Elevador'},
 types:{appartamento:'Apartamento',villa:'Villa',villetta:'Casa isolada',bifamiliare:'Casa bifamiliar',trifamiliare:'Casa trifamiliar',quadrifamiliare:'Casa quadrifamiliar',capannone:'Galpão',ufficio:'Escritório',negozio:'Loja',terreno:'Terreno','':'Imóvel'},title:function(t,c){return t+' em '+c}}
};
var D=T[L]||T.en;
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function img(u){if(!u)return'';u=String(u).trim();if(!u)return'';if(/^img\//.test(u))return 'https://righettoimmobiliare.it/'+u;if(!/^https?:/.test(u))u=SB+'/storage/v1/object/public/'+u.replace(/^\/+/,'');return u}
function big(u){return u.indexOf('/storage/v1/object/public/')>-1?u.replace('/object/public/','/render/image/public/')+'?width=1200&quality=80':u}
function sm(u){return u.indexOf('/storage/v1/object/public/')>-1?u.replace('/object/public/','/render/image/public/')+'?width=240&quality=70':u}
function isai(u){return /foto[-_ ]?ai/i.test(String(u||''))}
var STAGED={'LA0317':1};
function tc(s){return String(s||'').toLowerCase().replace(/(^|[\s'-])([a-zà-ú])/g,function(m,a,b){return a+b.toUpperCase()})}
var ref=(new URLSearchParams(location.search).get('ref')||'').replace(/[^A-Za-z0-9_ -]/g,'').trim().slice(0,20);
var back='<p><a class="rw-link" href="'+D.cat+'">'+D.back+'</a></p>';
root.innerHTML=back+'<p class="rw-pcount">'+D.loading+'</p>';
if(!ref){root.innerHTML=back+'<p>'+D.gone+'</p>';return}
var cols='codice,tipo_operazione,tipologia,comune,prezzo,superficie,locali,camere,bagni_totali,classe_energetica,venduto,affittato,foto,anno_costruzione,piano,giardino,garage,terrazzo,cantina,ascensore';
fetch(SB+'/rest/v1/immobili?select='+cols+'&attivo=eq.true&codice=eq.'+encodeURIComponent(ref)+'&limit=1',{headers:{apikey:KEY,Authorization:'Bearer '+KEY}}).then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(rows){
 var r=rows[0];if(!r||r.venduto||r.affittato){root.innerHTML=back+'<p>'+D.gone+'</p>';return}
 var rent=String(r.tipo_operazione||'').indexOf('affitto')===0,code=r.codice;
 var nf=new Intl.NumberFormat(D.loc,{style:'currency',currency:'EUR',maximumFractionDigits:0}),nn=new Intl.NumberFormat(D.loc);
 var price=+r.prezzo?nf.format(+r.prezzo)+(rent?D.pm:''):D.poa;
 var tl=D.title(D.types[r.tipologia||'']||D.types[''],tc(r.comune));
 var all=(Array.isArray(r.foto)?r.foto:[]).filter(function(u){return u&&(!isai(u)||STAGED[code])}).map(img);
 var facts=[[D.op,rent?D.lease:D.sale],[D.price,price],[D.type,D.types[r.tipologia||'']||D.types['']],[D.place,tc(r.comune)]];
 if(+r.superficie)facts.push([D.area,nn.format(+r.superficie)+' m²']);
 if(+r.locali)facts.push([D.rooms,+r.locali]);
 if(+r.camere)facts.push([D.beds,+r.camere]);
 if(+r.bagni_totali)facts.push([D.baths,+r.bagni_totali]);
 if(r.classe_energetica)facts.push([D.epc,r.classe_energetica]);
 if(+r.anno_costruzione)facts.push([D.year,+r.anno_costruzione]);
 if(r.piano!==null&&r.piano!==''&&r.piano!==undefined)facts.push([D.floor,r.piano]);
 var feats=Object.keys(D.f).filter(function(k){return r[k]===true}).map(function(k){return D.f[k]});
 var mail='mailto:ginevra@righettoimmobiliare.it?subject='+encodeURIComponent(D.subj+code)+'&body='+encodeURIComponent(D.body+code+'.');
 var g=all.length?'<div class="rw-pd-gal"><figure class="rw-pd-main"><img id="rw-pd-big" alt="'+esc(tl)+'" src="'+esc(big(all[0]))+'" onerror="this.onerror=null;this.src=\''+esc(all[0])+'\'"/></figure>'+(all.length>1?'<div class="rw-pd-thumbs" aria-label="'+esc(D.gl)+'">'+all.map(function(u,i){return '<button type="button" data-i="'+i+'" aria-label="'+esc(D.gl)+' '+(i+1)+'"><img alt="" loading="lazy" src="'+esc(sm(u))+'" onerror="this.onerror=null;this.src=\''+esc(u)+'\'"/></button>'}).join('')+'</div>':'')+'</div>':'';
 root.innerHTML=back+'<p class="rw-eyebrow">'+(rent?D.lease:D.sale)+' · '+D.ref+' '+esc(code)+'</p><h1 class="rw-promoted-title">'+esc(tl)+'</h1><p class="rw-pd-price">'+esc(price)+'</p>'+g+'<div class="rw-pd-cols"><section><h2>'+D.facts+'</h2><dl class="rw-pd-facts">'+facts.map(function(x){return '<div><dt>'+esc(x[0])+'</dt><dd>'+esc(x[1])+'</dd></div>'}).join('')+'</dl>'+(feats.length?'<h2>'+D.feat+'</h2><ul class="rw-pd-feat">'+feats.map(function(x){return '<li>'+esc(x)+'</li>'}).join('')+'</ul>':'')+'</section><aside class="rw-pd-ask"><img alt="Ginevra Capon" src="/international/assets/ginevra-occhiali-7f3a9c.webp" width="86" height="86"/><b>'+D.role+'</b><span>'+D.contact+'</span><a class="rw-button" href="'+mail+'">'+D.cta+'</a><small>'+D.note+'</small></aside></div>';
 var DL={en:['Description','Translated summary of the Italian listing. The Italian original prevails.'],ar:['الوصف','ملخص مترجم للإعلان الإيطالي. النص الإيطالي الأصلي هو المرجع.'],tr:['Açıklama','İtalyanca ilanın çevrilmiş özetidir. İtalyanca orijinal metin esastır.'],pt:['Descrição','Resumo traduzido do anúncio em italiano. Prevalece o original em italiano.']}[L]||null;
 if(DL){fetch('/international/assets/descriptions.json?v=1').then(function(x){return x.ok?x.json():{}}).then(function(m){var t=m[code]&&m[code][L];var sec=root.querySelector('.rw-pd-cols section');if(!t||!sec)return;var h=document.createElement('div');h.className='rw-pd-desc';h.innerHTML='<h2>'+DL[0]+'</h2><p class="rw-pd-descprice"><b>'+esc(D.price)+': '+esc(price)+'</b></p><p>'+esc(t)+'</p><small>'+DL[1]+'</small>';sec.insertBefore(h,sec.firstChild)}).catch(function(){})}
 var big_=document.getElementById('rw-pd-big');
 root.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('button[data-i]');if(!b||!big_)return;var u=all[+b.getAttribute('data-i')];big_.src=big(u);big_.onerror=function(){big_.onerror=null;big_.src=u}});
 document.title=tl+' · '+D.ref+' '+code+' | Righetto International';
}).catch(function(){root.innerHTML=back+'<p>'+D.err+'</p>'});
})();
