// ═══════════════════════════════════════════════════════════════
// RIGHETTO IMMOBILIARE — Audit Analysis Edge Function
// Analizza i risultati dell'audit usando Claude API (Anthropic)
// e salva la risposta in Supabase.
// Deploy: supabase functions deploy audit-analysis
// Secret necessario su Supabase:
//   ANTHROPIC_API_KEY = sk-ant-...
// ═══════════════════════════════════════════════════════════════

import { serve } from "https://deno.land/std@0.177.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

serve(async (req) => {
  // CORS preflight
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const ANTHROPIC_API_KEY = Deno.env.get("ANTHROPIC_API_KEY");
    if (!ANTHROPIC_API_KEY) {
      return new Response(
        JSON.stringify({ error: "ANTHROPIC_API_KEY non configurata. Esegui: supabase secrets set ANTHROPIC_API_KEY=sk-ant-..." }),
        { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const body = await req.json();
    const { audit_results, skill_context, snapshot_id } = body;

    if (!audit_results) {
      return new Response(
        JSON.stringify({ error: "audit_results mancante nel body" }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // Costruisci il prompt per Claude
    const systemPrompt = `Sei l'assistente SEO di Righetto Immobiliare, agenzia immobiliare a Padova.
Rispondi SEMPRE in italiano. Sii conciso e operativo.
Usa la SKILL-UNIFICATA.md come riferimento per:
- Sezione 9: Azioni tecniche (bug fix, contenuti, performance, SEO tecnico)
- Sezione 10: KPI e calendario editoriale
- Sezione 8: Standard contenuti e Entity-Based SEO

Il tuo compito:
1. Analizza i risultati dell'audit del sito
2. Identifica azioni correttive prioritarie
3. Verifica lo stato rispetto ai KPI
4. Controlla i TODO aperti
5. Proponi le prossime azioni secondo il calendario editoriale
6. Genera una sintesi breve (max 3 frasi) per lo storico

Formato risposta:
## Stato Audit
[Breve overview dei risultati]

## Azioni Prioritarie
[Lista numerata delle azioni da fare, ordinate per priorita']

## Stato KPI
[Confronto con obiettivi della sezione 10.1]

## TODO Aperti
[Dalla sezione 9.3-9.6, quali sono ancora da completare]

## Prossime Azioni (Calendario)
[Cosa fare questo mese/prossimo mese secondo sezione 10.2]

## Sintesi per Storico
[Max 3 frasi che riassumono lo stato attuale]`;

    const userMessage = `CONTESTO SKILL-UNIFICATA.md:
${skill_context || "Non fornito — analizza solo i risultati dell'audit."}

RISULTATI AUDIT:
${audit_results}

Data odierna: ${new Date().toLocaleDateString('it-IT')}`;

    // Chiama Claude API
    const claudeResp = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: "claude-sonnet-4-20250514",
        max_tokens: 2000,
        system: systemPrompt,
        messages: [
          { role: "user", content: userMessage }
        ],
      }),
    });

    if (!claudeResp.ok) {
      const errText = await claudeResp.text();
      console.error("Claude API error:", claudeResp.status, errText);
      return new Response(
        JSON.stringify({ error: "Errore Claude API: " + claudeResp.status, details: errText }),
        { status: 502, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const claudeData = await claudeResp.json();
    const analysis = claudeData.content?.[0]?.text || "Nessuna risposta da Claude";

    // Salva l'analisi in Supabase
    const supabaseUrl = Deno.env.get("SUPABASE_URL") || "";
    const supabaseKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || "";

    if (supabaseUrl && supabaseKey) {
      const sb = createClient(supabaseUrl, supabaseKey);

      // Salva nella tabella audit_analyses
      await sb.from("audit_analyses").insert({
        snapshot_id: snapshot_id || null,
        analysis: analysis,
        audit_data: audit_results,
      });
    }

    return new Response(
      JSON.stringify({ success: true, analysis }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );

  } catch (err) {
    console.error("Errore:", err);
    return new Response(
      JSON.stringify({ error: err.message || "Errore interno" }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
