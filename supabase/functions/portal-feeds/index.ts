// RIGHETTO — Feed portali Immobiliare.it (XML) e Idealista (JSON di lavoro)
// Deploy: supabase functions deploy portal-feeds --no-verify-jwt
// Secrets: PORTAL_FEED_TOKEN (obbligatorio), IDEALISTA_ILC (opzionale)
// Uso (GET):
//   /functions/v1/portal-feeds?portal=immobiliare&token=TOKEN
//   /functions/v1/portal-feeds?portal=idealista&token=TOKEN
// Spec Immobiliare.it: https://feed.immobiliare.it/integration/ii/docs/import/
import { serve } from "https://deno.land/std@0.177.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.0";
import {
  buildIdealistaJson,
  buildImmobiliareXml,
  FEED_SELECT,
  type ImmobileRow,
} from "./feed.ts";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
};

function json(o: unknown, s = 200) {
  return new Response(JSON.stringify(o), {
    status: s,
    headers: { ...cors, "Content-Type": "application/json; charset=utf-8" },
  });
}

function tokenOk(req: Request, url: URL): boolean {
  const expected = (Deno.env.get("PORTAL_FEED_TOKEN") || "").trim();
  if (!expected || expected.length < 16) return false;
  const q = (url.searchParams.get("token") || "").trim();
  const h = (req.headers.get("x-portal-feed-token") || "").trim();
  return q === expected || h === expected;
}

serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "GET") return json({ error: "metodo non valido" }, 405);

  const url = new URL(req.url);
  if (!tokenOk(req, url)) return json({ error: "non autorizzato" }, 401);

  const portal = (url.searchParams.get("portal") || "").trim().toLowerCase();
  if (portal !== "immobiliare" && portal !== "idealista") {
    return json({ error: "parametro portal=immobiliare|idealista richiesto" }, 400);
  }

  const sbUrl = Deno.env.get("SUPABASE_URL") ?? "";
  const key = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "";
  if (!sbUrl || !key) return json({ error: "configurazione incompleta" }, 500);

  const sb = createClient(sbUrl, key, { auth: { persistSession: false } });
  const rows: ImmobileRow[] = [];
  for (let offset = 0; offset < 5000; offset += 500) {
    const { data, error } = await sb
      .from("immobili")
      .select(FEED_SELECT)
      .eq("attivo", true)
      .eq("venduto", false)
      .eq("affittato", false)
      .eq("cestino", false)
      .order("id")
      .range(offset, offset + 499);
    if (error) return json({ error: "lettura immobili: " + error.message }, 502);
    if (!Array.isArray(data) || !data.length) break;
    rows.push(...(data as ImmobileRow[]));
    if (data.length < 500) break;
  }

  const generatedAt = new Date();
  if (portal === "immobiliare") {
    const xml = buildImmobiliareXml(rows, generatedAt);
    return new Response(xml, {
      status: 200,
      headers: {
        ...cors,
        "Content-Type": "application/xml; charset=utf-8",
        "Cache-Control": "private, max-age=300",
        "X-Righetto-Feed-Count": String(
          rows.filter((r) => r.pubblica_immobiliare_it === true).length,
        ),
      },
    });
  }

  const body = buildIdealistaJson(rows, {
    generatedAt,
    ilc: (Deno.env.get("IDEALISTA_ILC") || "").trim(),
  });
  return new Response(JSON.stringify(body, null, 2), {
    status: 200,
    headers: {
      ...cors,
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "private, max-age=300",
      "X-Righetto-Feed-Count": String(body.properties.length),
    },
  });
});
