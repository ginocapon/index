/** Mapping feed Immobiliare.it + Idealista (allineato a js/portal-feeds-core.mjs). */

export const SITE_ORIGIN = "https://righettoimmobiliare.it";
export const AGENCY = {
  name: "Righetto Immobiliare",
  email: "info@righettoimmobiliare.it",
  phone: "+390498843484",
};

const ID_TYPE: Record<string, number> = {
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

export type ImmobileRow = Record<string, unknown>;

function escXml(value: unknown): string {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function cdata(value: unknown): string {
  const s = String(value ?? "").replace(/]]>/g, "]]]]><![CDATA[>");
  return `<![CDATA[${s}]]>`;
}

function isoDateTime(value: unknown): string {
  if (!value) return new Date().toISOString().slice(0, 19);
  const d = new Date(String(value));
  if (Number.isNaN(+d)) return new Date().toISOString().slice(0, 19);
  return d.toISOString().slice(0, 19);
}

function absPhotoUrl(ref: unknown): string {
  if (!ref || typeof ref !== "string") return "";
  const u = ref.trim();
  if (!u) return "";
  if (/^https?:\/\//i.test(u)) return u;
  if (u.startsWith("//")) return "https:" + u;
  return SITE_ORIGIN + "/" + u.replace(/^\/+/, "");
}

export function photoUrls(row: ImmobileRow): string[] {
  const list = Array.isArray(row.foto)
    ? row.foto
    : Array.isArray(row.foto_urls)
    ? row.foto_urls
    : [];
  return [...new Set(list.map(absPhotoUrl).filter(Boolean))].slice(0, 50);
}

export function isFeedEligible(row: ImmobileRow, portal: "immobiliare" | "idealista"): boolean {
  if (!row || row.cestino === true) return false;
  if (row.attivo !== true) return false;
  if (row.venduto === true || row.affittato === true) return false;
  if (!row.codice || !row.titolo) return false;
  if (portal === "immobiliare") return row.pubblica_immobiliare_it === true;
  return row.pubblica_idealista === true;
}

function transactionType(row: ImmobileRow): "R" | "S" {
  const t = String(row.tipo_operazione || "").toLowerCase();
  if (t.startsWith("affitto") || t === "locazione" || t === "rent") return "R";
  return "S";
}

function priceValue(row: ImmobileRow): number | null {
  const n = Number(row.prezzo_portali ?? row.prezzo);
  return Number.isFinite(n) && n > 0 ? Math.round(n) : null;
}

function surfaceValue(row: ImmobileRow): number | null {
  const n = Number(row.superficie_portali ?? row.superficie);
  return Number.isFinite(n) && n > 0 ? Math.round(n) : null;
}

function idType(row: ImmobileRow): number {
  const tip = String(row.tipologia || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/\s+/g, "_");
  for (const [key, id] of Object.entries(ID_TYPE)) {
    if (key !== "default" && tip.includes(key)) return id;
  }
  return ID_TYPE.default;
}

function energyClass(row: ImmobileRow): string {
  return String(row.classe_energetica || "")
    .trim()
    .toUpperCase()
    .replace(/\s+/g, "")
    .slice(0, 8);
}

export function buildImmobiliareXml(rows: ImmobileRow[], generatedAt = new Date()): string {
  const items = (rows || []).filter((r) => isFeedEligible(r, "immobiliare"));
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
      const desc = String(row.descrizione_ridotta || row.descrizione || row.titolo || "");
      const energy = energyClass(row);
      const pictureXml = photos
        .map((url, i) => `        <picture position="${i + 1}" url="${escXml(url)}"/>`)
        .join("\n");
      const features = [
        row.garage ? "        <box>true</box>" : "",
        row.giardino ? "        <garden>true</garden>" : "",
        row.terrazzo ? "        <terrace>true</terrace>" : "",
        row.cantina ? "        <cellar>true</cellar>" : "",
        row.ascensore ? "        <elevator>true</elevator>" : "",
        row.piscina ? "        <swimming-pool>true</swimming-pool>" : "",
        row.arredato ? "        <furniture>true</furniture>" : "",
      ]
        .filter(Boolean)
        .join("\n");

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
        <city>${cdata(row.comune || "Padova")}</city>
        <locality map="approximate">
          ${
            Number.isFinite(lat) && Number.isFinite(lng)
              ? `<latitude>${lat}</latitude>\n          <longitude>${lng}</longitude>`
              : ""
          }
          ${row.indirizzo ? `<thoroughfare display="no">${cdata(row.indirizzo)}</thoroughfare>` : ""}
        </locality>
      </location>
      <title>${cdata(row.titolo)}</title>
      <description>${cdata(desc.slice(0, 8000))}</description>
      ${mq != null ? `<size unit="m2">${mq}</size>` : ""}
      ${rooms != null ? `<rooms>${rooms}</rooms>` : ""}
      ${baths != null ? `<bathrooms>${baths}</bathrooms>` : ""}
      ${energy ? `<energy-class>${escXml(energy)}</energy-class>` : ""}
      ${
        row.ipe_kwh != null && Number.isFinite(Number(row.ipe_kwh))
          ? `<energy-value>${Number(row.ipe_kwh)}</energy-value>`
          : ""
      }
${features ? `      <features>\n${features}\n      </features>` : ""}
${pictureXml ? `      <pictures>\n${pictureXml}\n      </pictures>` : ""}
      ${row.virtual_tour ? `<virtual-tour>${cdata(row.virtual_tour)}</virtual-tour>` : ""}
      ${
        row.youtube_id
          ? `<video>${cdata("https://www.youtube.com/watch?v=" + row.youtube_id)}</video>`
          : ""
      }
      <publish>
        <portal id="immobiliare.it" status="true"/>
      </publish>
    </property>`;
    })
    .join("\n");

  return `<?xml version="1.0" encoding="UTF-8"?>
<!-- Righetto Immobiliare · feed Immobiliare.it batch · generato ${isoDateTime(generatedAt)} · ${items.length} annunci -->
<feed>
  <properties>
${body}
  </properties>
</feed>
`;
}

export function buildIdealistaJson(
  rows: ImmobileRow[],
  opts: { generatedAt?: Date; ilc?: string } = {},
) {
  const generatedAt = opts.generatedAt || new Date();
  const items = (rows || []).filter((r) => isFeedEligible(r, "idealista"));
  return {
    schema: "righetto-idealista-work-1",
    note:
      "Formato di lavoro per omologazione Idealista. Dopo il codice ILC, Idealista può richiedere aggiustamenti JSON/FTP.",
    generatedAt: generatedAt.toISOString(),
    agency: {
      name: AGENCY.name,
      email: AGENCY.email,
      phone: AGENCY.phone,
      ilc: opts.ilc || null,
    },
    properties: items.map((row) => {
      const price = priceValue(row);
      const mq = surfaceValue(row);
      const op = transactionType(row) === "R" ? "rent" : "sale";
      return {
        reference: row.codice,
        operation: op,
        propertyType: row.tipologia || row.categoria || "appartamento",
        title: row.titolo,
        description: String(row.descrizione_ridotta || row.descrizione || row.titolo || "").slice(
          0,
          4000,
        ),
        price,
        currency: "EUR",
        size: mq,
        rooms: Number(row.camere || row.locali) || null,
        bathrooms: Number(row.bagni_totali || row.bagni) || null,
        floor: row.piano || null,
        energyCertificate: energyClass(row) || null,
        energyValue: row.ipe_kwh != null ? Number(row.ipe_kwh) : null,
        address: {
          country: "IT",
          municipality: row.comune || "Padova",
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
        videoUrl: row.youtube_id ? "https://www.youtube.com/watch?v=" + row.youtube_id : null,
        updatedAt: row.updated_at || generatedAt.toISOString(),
      };
    }),
  };
}

export const FEED_SELECT =
  "id,codice,titolo,tipo_operazione,categoria,tipologia,comune,indirizzo,lat,lng,prezzo,prezzo_portali,superficie,superficie_portali,locali,camere,bagni,bagni_totali,piano,classe_energetica,ipe_kwh,garage,giardino,terrazzo,cantina,ascensore,piscina,arredato,foto,foto_urls,youtube_id,virtual_tour,descrizione,descrizione_ridotta,attivo,venduto,affittato,cestino,pubblica_immobiliare_it,pubblica_idealista,updated_at";
