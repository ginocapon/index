/* Stored-file references belong to this site's storage origin. No external fallback. */
export function storageReference(db,value){
 if(typeof value!=='string'||!value)throw Error('Riferimento del file mancante.');
 let expected,url;try{expected=new URL(db.storage.from('documenti').getPublicUrl('reference-check').data.publicUrl).origin;url=new URL(value);}catch{throw Error('Riferimento del file non valido.');}
 if(url.origin!==expected)throw Error('File esterno: verifica il riferimento prima di aprirlo.');
 const match=url.pathname.match(/^\/storage\/v1\/object\/(?:public|sign|authenticated)\/(documenti|planimetrie|foto-immobili|aste-pratica)\/(.+)$/);
 if(!match)throw Error('Archivio del file non riconosciuto.');
 let path;try{path=decodeURIComponent(match[2]);}catch{throw Error('Percorso del file non valido.');}
 if(!path||path.startsWith('/')||path.split('/').includes('..'))throw Error('Percorso del file non valido.');
 return {bucket:match[1],path};
}
export async function downloadStoredFile(db,value){const ref=storageReference(db,value),result=await db.storage.from(ref.bucket).download(ref.path);if(result.error||!(result.data instanceof Blob))throw Error('File non leggibile nell’archivio '+ref.bucket+'.');return {file:result.data,...ref};}
export function initSummaryFilePreviews({db,getContext,isCurrent}){
 const urls=new Set();let epoch=0;
 function clear(){epoch++;for(const url of urls)URL.revokeObjectURL(url);urls.clear();}
 async function preview(doc,img){const c=getContext(),ticket=epoch;if(!isCurrent(c))return;try{const {file}=await downloadStoredFile(db,doc.url);if(ticket!==epoch||!isCurrent(c)||!img.isConnected)return;const type=file.type||(/\.png$/i.test(doc.nome)?'image/png':'image/jpeg');if(!type.startsWith('image/'))return;const url=URL.createObjectURL(new Blob([file],{type}));urls.add(url);img.src=url;}catch{if(img.isConnected)img.alt='Anteprima non disponibile. Apri il file.';}}
 window.addEventListener('pagehide',clear);db.auth.onAuthStateChange?.(event=>{if(event==='SIGNED_OUT')clear();});return {clear,preview};
}
