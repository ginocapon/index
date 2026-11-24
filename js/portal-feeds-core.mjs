/**
 * Generazione feed portali Immobiliare.it (XML batch) e Idealista (JSON di lavoro).
 * Usato da Edge Function e da script Node. Nessuna chiamata di rete qui.
 */

export const SITE_ORIGIN = 'https://righettoimmobiliare.it';
export const AGENCY = {
  name: 'Righetto Immobiliare',
  email: 'info@righettoimmobiliare.it',
  phone: '+390498843484',
  country: 'IT',
};

/** Tipologie → IDType Immobiliare.it (provvisori: validare con Mission Control / XSD ufficiale). */
export const IMMOBILIARE_ID_TYPE = {
  appartamento: 1,
  monolocale: 2,
  bilocale: 1,
  trilocale: 1,
  loft: 22,
  attico: 4,
  mansarda: 5,
  villa: 12,
  villetta: 11,
  casa: 10,
  rustico: 15,
  casale: 15,
  terreno: 18,
  box: 19,
  garage: 19,
  posto_auto: 20,
  ufficio: 7,
  negozio: 8,
  magazzino: 9,
  capannone: 16,
  laboratorio: 9,
  default: 1,
};

function escXml(value) {
  return String(value ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function cdata(value) {
  const s = String(value ?? '').replace(/]]>/g, ']]]]><![CDATA[>');
  return `<![CDATA[${s}]]>`;
}

function isoDateTime(value) {
  if (!value) return new Date().toISOString().slice(0, 19);
  const d = new Date(value);
  if (Number.isNaN(+d)) return new Date().toISOString().slice(0, 19);
  return d.toISOString().slice(0, 19);
}

function absPhotoUrl(ref) {
  if (!ref || typeof ref !== 'string') return '';
  const u = ref.trim();
  if (!u) return '';
  if (/^https?:\/\//i.test(u)) return u;
  if (u.startsWith('//')) return 'https:' + u;
  return SITE_ORIGIN + '/' + u.replace(/^\/+/, '');
}

export function photoUrls(row) {
  const list = Array.isArray(row.foto) ? row.foto : Array.isArray(row.foto_urls) ? row.foto_urls : [];
  return [...new Set(list.map(absPhotoUrl).filter(Boolean))].slice(0, 50);
}

export function isFeedEligible(row, portal) {
  if (!row || row.cestino === true) return false;
  if (row.attivo !== true) return false;
  if (row.venduto === true || row.affittato === true) return false;
  if (!row.codice || !row.titolo) return false;
  if (portal === 'immobiliare') return row.pubblica_immobiliare_it === true;
  if (portal === 'idealista') return row.pubblica_idealista === true;
  return false;
}

function transactionType(row) {
  const t = String(row.tipo_operazione || '').toLowerCase();
  if (t.startsWith('affitto') || t === 'locazione' || t === 'rent') return 'R';
  return 'S';
}

function priceValue(row) {
  const n = Number(row.prezzo_portali ?? row.prezzo);
  return Number.isFinite(n) && n > 0 ? Math.round(n) : null;
}

function surfaceValue(row) {
  const n = Number(row.superficie_portali ?? row.superficie);
  return Number.isFinite(n) && n > 0 ? Math.round(n) : null;
}

function idType(row) {
  const tip = String(row.tipologia || '')
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/\s+/g, '_');
  for (const [key, id] of Object.entries(IMMOBILIARE_ID_TYPE)) {
    if (key !== 'default' && tip.includes(key)) return id;
  }
  return IMMOBILIARE_ID_TYPE.default;
}

function energyClass(row) {
  const c = String(row.classe_energetica || '')
    .trim()
    .toUpperCase()
    .replace(/\s+/g, '');
  if (!c) return '';
  if (/^[A-G](\+||1|2|3|4)?$/i.test(c) || /^A[1-4]$/.test(c)) return c;
  return c.slice(0, 8);
}

/**
 * Feed batch Immobiliare.it (UTF-8 XML).
 * Spec: https://feed.immobiliare.it/integration/ii/docs/import/
 */
export function buildImmobiliareXml(rows, { generatedAt = new Date() } = {}) {
  const items = (rows || []).filter((r) => isFeedEligible(r, 'immobiliare'));
  const body = items
    .map((row) => {
      const price = priceValue(row);
      const mq = surfaceValue(row);
      const photos = photoUrls(row);
      const tx = transactionType(row);
      const rooms = Number(row.camere || row.locali) || null;
      const baths = Number(row.bagni_totali || row.bagni) || null;
      const lat = Number(row.lat);
      const lng = Number(row.lng);
      const desc = row.descrizione_ridotta || row.descrizione || row.titolo || '';
      const energy = energyClass(row);
      const pictureXml = photos
        .map((url, i) => `        <picture position="${i + 1}" url="${escXml(url)}"/>`)
        .join('\n');
      const features = [
        row.garage ? '        <box>true</box>' : '',
        row.giardino ? '        <garden>true</garden>' : '',
        row.terrazzo ? '        <terrace>true</terrace>' : '',
        row.cantina ? '        <cellar>true</cellar>' : '',
        row.ascensore ? '        <elevator>true</elevator>' : '',
        row.piscina ? '        <swimming-pool>true</swimming-pool>' : '',
        row.arredato ? '        <furniture>true</furniture>' : '',
      ]
        .filter(Boolean)
        .join('\n');

      return `    <property operation="write">
      <unique-id>${cdata(row.codice)}</unique-id>
      <date-updated>${isoDateTime(row.updated_at || generatedAt)}</date-updated>
      <agent>
        <office-name>${cdata(AGENCY.name)}</office-name>
        <email>${escXml(AGENCY.email)}</email>
      </agent>
      <building IDType="${idType(row)}"/>
      <transactions>
        <transaction type="${tx}">
          <price currency="EUR" reserved="false">${price != null ? price : 0}</price>
        </transaction>
      </transactions>
      <location>
        <country-code>IT</country-code>
        <city>${cdata(row.comune || 'Padova')}</city>
        <locality map="approximate">
          ${Number.isFinite(lat) && Number.isFinite(lng) ? `<latitude>${lat}</latitude>\n          <longitude>${lng}</longitude>` : ''}
          ${row.indirizzo ? `<thoroughfare display="no">${cdata(row.indirizzo)}</thoroughfare>` : ''}
        </locality>
      </location>
      <title>${cdata(row.titolo)}</title>
      <description>${cdata(desc.slice(0, 8000))}</description>
      ${mq != null ? `<size unit="m2">${mq}</size>` : ''}
      ${rooms != null ? `<rooms>${rooms}</rooms>` : ''}
      ${baths != null ? `<bathrooms>${baths}</bathrooms>` : ''}
      ${energy ? `<energy-class>${escXml(energy)}</energy-class>` : ''}
      ${row.ipe_kwh != null && Number.isFinite(Number(row.ipe_kwh)) ? `<energy-value>${Number(row.ipe_kwh)}</energy-value>` : ''}
${features ? `      <features>\n${features}\n      </features>` : ''}
${pictureXml ? `      <pictures>\n${pictureXml}\n      </pictures>` : ''}
      ${row.virtual_tour ? `<virtual-tour>${cdata(row.virtual_tour)}</virtual-tour>` : ''}
      ${row.youtube_id ? `<video>${cdata('https://www.youtube.com/watch?v=' + row.youtube_id)}</video>` : ''}
      <publish>
        <portal id="immobiliare.it" status="true"/>
      </publish>
    </property>`;
    })
    .join('\n');

  return `<?xml version="1.0" encoding="UTF-8"?>
<!-- Righetto Immobiliare · feed Immobiliare.it batch · generato ${isoDateTime(generatedAt)} · ${items.length} annunci -->
<feed>
  <properties>
${body}
  </properties>
</feed>
`;
}

/**
 * JSON di lavoro Idealista (formato CRM → da validare con Idealista dopo codice ILC).
 * Non è lo schema ufficiale chiuso: Idealista lo comunica alle piattaforme omologate.
 */
export function buildIdealistaJson(rows, { generatedAt = new Date(), ilc = '' } = {}) {
  const items = (rows || []).filter((r) => isFeedEligible(r, 'idealista'));
  return {
    schema: 'righetto-idealista-work-1',
    note:
      'Formato di lavoro per omologazione Idealista. Dopo il codice ILC, Idealista può richiedere aggiustamenti JSON/FTP. Non pubblicare finché il portale non conferma.',
    generatedAt: generatedAt.toISOString(),
    agency: {
      name: AGENCY.name,
      email: AGENCY.email,
      phone: AGENCY.phone,
      ilc: ilc || null,
    },
    properties: items.map((row) => {
      const price = priceValue(row);
      const mq = surfaceValue(row);
      const op = transactionType(row) === 'R' ? 'rent' : 'sale';
      return {
        reference: row.codice,
        operation: op,
        propertyType: row.tipologia || row.categoria || 'appartamento',
        title: row.titolo,
        description: String(row.descrizione_ridotta || row.descrizione || row.titolo || '').slice(
          0,
          4000
        ),
        price: price,
        currency: 'EUR',
        size: mq,
        rooms: Number(row.camere || row.locali) || null,
        bathrooms: Number(row.bagni_totali || row.bagni) || null,
        floor: row.piano || null,
        energyCertificate: energyClass(row) || null,
        energyValue: row.ipe_kwh != null ? Number(row.ipe_kwh) : null,
        address: {
          country: 'IT',
          municipality: row.comune || 'Padova',
          street: row.indirizzo || null,
          latitude: Number.isFinite(Number(row.lat)) ? Number(row.lat) : null,
          longitude: Number.isFinite(Number(row.lng)) ? Number(row.lng) : null,
          showExactLocation: false,
        },
        features: {
          garage: !!row.garage,
          garden: !!row.giardino,
          terrace: !!row.terrazzo,
          cellar: !!row.cantina,
          elevator: !!row.ascensore,
          pool: !!row.piscina,
          furnished: !!row.arredato,
        },
        images: photoUrls(row),
        virtualTour: row.virtual_tour || null,
        videoUrl: row.youtube_id ? 'https://www.youtube.com/watch?v=' + row.youtube_id : null,
        updatedAt: row.updated_at || generatedAt.toISOString(),
      };
    }),
  };
}

export function mandateAlertRows(rows, { today = new Date(), warnDays = 30 } = {}) {
  const start = new Date(Date.UTC(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate()));
  const warnUntil = new Date(start);
  warnUntil.setUTCDate(warnUntil.getUTCDate() + warnDays);
  const out = { expired: [], expiring: [] };
  for (const row of rows || []) {
    if (!row?.incarico_scadenza || row.cestino === true) continue;
    if (row.venduto === true || row.affittato === true) continue;
    const raw = String(row.incarico_scadenza).slice(0, 10);
    if (!/^\d{4}-\d{2}-\d{2}$/.test(raw)) continue;
    const d = new Date(raw + 'T12:00:00Z');
    if (Number.isNaN(+d)) continue;
    const item = {
      id: row.id,
      codice: row.codice,
      titolo: row.titolo,
      comune: row.comune,
      incarico_scadenza: raw,
      attivo: row.attivo === true,
    };
    if (d < start) out.expired.push(item);
    else if (d <= warnUntil) out.expiring.push(item);
  }
  out.expired.sort((a, b) => a.incarico_scadenza.localeCompare(b.incarico_scadenza));
  out.expiring.sort((a, b) => a.incarico_scadenza.localeCompare(b.incarico_scadenza));
  return out;
}
