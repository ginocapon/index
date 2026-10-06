# Controllo visivo post-deploy (6 ott 2026)

URL produzione verificati (accessibility snapshot + struttura):

| URL | Esito |
|-----|--------|
| `/blog-bonus-casa-2027-detrazioni-padova` | OK — H1/H2 presenti, CTA «Consulenza immobiliare Padova» (H3), form lead |
| `/blog-affitti-padova-canoni-2026` | Da rivedere a occhio banner/stat (dopo push e14515b + commit odierno) |
| `/blog-mercato-immobiliare-padova-2026` | Tabella: th allineati via rig-blog-article.css v=5 |

Audit browser completo: `scripts/audit-blog-design.js` + `python -m http.server 8765` (cache-bust `?_=` su iframe).
