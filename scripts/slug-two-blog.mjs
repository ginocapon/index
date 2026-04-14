function generateSlug(titolo) {
  let s = String(titolo || '')
    .replace(/\u2019/g, "'").replace(/\u2018/g, "'").replace(/\u2013/g, '-').replace(/\u2014/g, '-')
    .toLowerCase()
    .replace(/[àáâãäå]/g,'a').replace(/[èéêë]/g,'e').replace(/[ìíîï]/g,'i')
    .replace(/[òóôõö]/g,'o').replace(/[ùúûü]/g,'u').replace(/[ç]/g,'c')
    .replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,80).replace(/-+$/g,'');
  if (!s.endsWith('-padova') && !s.endsWith('padova')) s += '-padova';
  return s;
}
const t1 = "Umidità negli scantinati a Padova: cause tecniche, prove scientifiche e soluzioni definitive";
const t2 = "Servizi Immobiliari 2026: Crescita, Digitale e Nuove Opportunità | Righetto Immobiliare Padova";
console.log(generateSlug(t1));
console.log(generateSlug(t2));
