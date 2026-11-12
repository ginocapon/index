/* Read-only adapter. Reuses the existing property-ID check and only images named by the public manifest. */
export async function verifiedPropertyShare(property,{resolve,loadManifest}){
 const link=await resolve(property);if(!link?.ok)return link;
 const url=new URL(link.url);if(url.origin!=='https://righettoimmobiliare.it'||url.search||url.hash||!/^\/share-immobile-[a-z0-9-]+\.html$/.test(url.pathname))return {ok:false,reason:'Link pubblico non valido.'};
 const manifest=await loadManifest();const entries=Object.values(manifest?.bySlug||{}).filter(x=>x?.share_file===url.pathname.slice(1)&&String(x.codice||'').trim().toUpperCase()===String(property.codice||'').trim().toUpperCase());
 if(entries.length!==1)return {ok:false,reason:'Anteprima pubblica non univoca. Aggiorna gli immobili.'};
 const entry=entries[0];let image=null;
 if(entry.image){try{const u=new URL(entry.image);if(u.origin===url.origin&&!u.search&&!u.hash&&u.pathname==='/img/og-immobili/'+entry.seo_slug+'.jpg')image=u.href;}catch{}}
 return {ok:true,url:url.href,image};
}
