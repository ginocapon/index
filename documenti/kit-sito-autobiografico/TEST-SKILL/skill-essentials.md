# SKILL-ESSENTIALS — Sito autobiografico

> Carica **SEMPRE** questo file. Regole operative core.

---

## CLAIM E DATI (compilare — unica fonte verità)

| Dato | Valore |
|------|--------|
| Nome e cognome | […] |
| Brand / palestra | […] |
| Dominio canonico | https://[dominio].it |
| Città | […] |
| Indirizzo (NAP) | [via, CAP, città] |
| Telefono | […] |
| Email | […] |
| Instagram / social | […] |
| Attivo dal | [anno] |
| Recensioni Google | [N] — [voto]/5 |
| Certificazioni | […] |

> **REGOLA D'ORO:** dati inventati vietati. Sostituire `[…]` prima di pubblicare.

---

## 1. Regole operative (sempre)

1. Leggi il file da modificare prima di modificarlo
2. **Mobile-first** — ogni modifica ok su iPhone 375px
3. **URL coerenti** — canonical, sitemap, link interni stesso formato
4. **Un dominio canonico** — apex **o** www, non entrambi indicizzati
5. **Sitemap GSC:** solo `sitemap.xml`, mai URL singole pagine
6. **Aggiorna `sitemap.xml`** ad ogni pagina nuova/rimossa
7. **Cache-busting:** CSS/JS con `?v=N`, incrementa a ogni modifica
8. **WCAG AA:** contrasto CTA ≥ 4,5:1 — no arancione acceso + bianco
9. **No CDN esterni** — font e script locali
10. **No DNS/hosting** senza conferma esplicita utente
11. **Tono:** autobiografico autentico, professionale, mai dialetto forzato

---

## 1.1 Commit e push

- **Commit:** solo se l'utente lo chiede o regola progetto esplicita
- **Push:** solo se chiede «push», «metti online», ecc.
- Mai `.env`, password, token in commit
- Messaggio commit in italiano, 1–2 frasi sul perché

---

## 1.2 Title e Meta (BLOCCANTE)

| Campo | Target | Max |
|-------|--------|-----|
| `<title>` | ≤60 caratteri | 70 |
| `meta description` | 120–155 caratteri | 160 |

- Title, H1 e meta = **varianti diverse**
- Keyword + città + nome dove naturale
- Contare caratteri prima di pubblicare

**Esempi:**
- `[Nome] — Personal trainer [Città] | [Palestra]`
- `Chi sono — [Nome], [specialità] a [Città]`

---

## 2. Checklist nuova pagina

- [ ] Title/meta §1.2
- [ ] H1 unico
- [ ] Alt text immagini
- [ ] Canonical URL ufficiale
- [ ] OG tags
- [ ] Schema JSON-LD (Person / LocalBusiness / FAQ)
- [ ] Min 3 link interni
- [ ] In `sitemap.xml`
- [ ] Prime 2 righe dichiarative (GEO)
- [ ] Min 5 FAQ su pagine servizio (se applicabile)
- [ ] Bio autore su articoli blog
- [ ] Mobile + CTA contatto visibile

---

## 3. Registrazione nuove pagine

| Tipo | Azioni |
|------|--------|
| Pagina statica | `sitemap.xml` + link da menu/footer |
| Articolo blog | `sitemap.xml` + elenco blog + link interni |
| Sezione biografica | cross-link Home ↔ Chi sono ↔ Storia |

---

## 4. Pagine obbligatorie sito autobiografico

1. **Home** — chi sei in 10 secondi + CTA
2. **Chi sono** — bio, foto, schema Person
3. **Storia / Percorso** (opzionale separata o in Chi sono)
4. **Attività / Palestra** — servizi, orari, schema LocalBusiness
5. **Contatti** — NAP, mappa, form, stesso NAP di Google Maps

---

## 5. Comunicazione agente

- Rispondi in italiano
- Diretto e pratico
- Chiedi conferma prima di operazioni irreversibili (DNS, cancellazioni massive)
- Non inventare biografia o numeri
