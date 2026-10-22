// RIGHETTO IMMOBILIARE - Ponte documenti immobili (PDF nel repo GitHub PRIVATO immobili-docs)
// Solo l'admin loggato (ADMIN_UID) puo' elencare/aprire i PDF. Il token GitHub e' solo nei segreti.
// Deploy: supabase functions deploy docs-immobili
// Secrets: ADMIN_UID, GITHUB_DOCS_TOKEN (fine-grained, sola lettura "Contents", solo repo immobili-docs)
// Opzionali: GITHUB_DOCS_REPO (default ginocapon/immobili-docs)
// Uso (POST JSON, header Authorization: Bearer <sessione admin>):
//   {"codice":"NEG2176"}                      -> elenco file
//   {"codice":"NEG2176","file":"x.pdf"}      -> PDF (application/pdf)
import { serve } from "https://deno.land/std@0.177.0/http/server.ts";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const json = (o: unknown, s = 200) =>
  new Response(JSON.stringify(o), { status: s, headers: { ...cors, "Content-Type": "application/json" } });

async function isAdmin(req: Request): Promise<boolean> {
  const adminUid = (Deno.env.get("ADMIN_UID") || "").trim();
  const token = (req.headers.get("authorization") || "").replace(/^Bearer\s+/i, "").trim();
  if (!adminUid || !token) return false;
  try {
    const r = await fetch((Deno.env.get("SUPABASE_URL") ?? "") + "/auth/v1/user", {
      headers: { Authorization: "Bearer " + token, apikey: Deno.env.get("SUPABASE_ANON_KEY") ?? "" },
    });
    if (!r.ok) return false;
    const u = await r.json();
    return !!u && u.id === adminUid;
  } catch (_) { return false; }
}

serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (req.method !== "POST") return json({ error: "metodo non valido" }, 405);
  if (!(await isAdmin(req))) return json({ error: "non autorizzato" }, 401);

  const gh = (Deno.env.get("GITHUB_DOCS_TOKEN") || "").trim();
  const repo = (Deno.env.get("GITHUB_DOCS_REPO") || "ginocapon/immobili-docs").trim();
  if (!gh) return json({ error: "token documenti non configurato" }, 500);

  let body: { codice?: string; file?: string };
  try { body = await req.json(); } catch (_) { return json({ error: "richiesta non valida" }, 400); }
  const codice = String(body.codice || "").trim();
  if (!/^[A-Za-z0-9 _-]{2,60}$/.test(codice)) return json({ error: "codice non valido" }, 400);
  const base = "https://api.github.com/repos/" + repo + "/contents/" + encodeURIComponent(codice);
  const headers = { Authorization: "Bearer " + gh, "User-Agent": "righetto-docs", "X-GitHub-Api-Version": "2022-11-28" };

  if (!body.file) {
    const r = await fetch(base, { headers: { ...headers, Accept: "application/vnd.github+json" } });
    if (r.status === 404) return json({ files: [] });
    if (!r.ok) return json({ error: "errore archivio (" + r.status + ")" }, 502);
    const items = await r.json();
    const files = (Array.isArray(items) ? items : [])
      .filter((x: any) => x.type === "file")
      .map((x: any) => ({ name: x.name, size: x.size }));
    return json({ files });
  }

  const file = String(body.file);
  if (file.includes("/") || file.includes("\\") || file.includes("..") || file.length > 200) return json({ error: "file non valido" }, 400);
  const r = await fetch(base + "/" + encodeURIComponent(file), { headers: { ...headers, Accept: "application/vnd.github.raw+json" } });
  if (!r.ok) return json({ error: "file non trovato" }, r.status === 404 ? 404 : 502);
  const type = /\.pdf$/i.test(file) ? "application/pdf" : "application/octet-stream";
  return new Response(r.body, {
    headers: { ...cors, "Content-Type": type, "Content-Disposition": 'inline; filename="' + file.replace(/"/g, "") + '"', "Cache-Control": "private, no-store" },
  });
});
