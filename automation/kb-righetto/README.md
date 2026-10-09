# Knowledge base — n8n RAG (Livello B)

Inserire qui markdown/HTML estratti da pagine **pubbliche** Righetto (servizi, landing owner, FAQ blog) per embedding in `kb_documents` (pgvector 768).

**Non includere:** dati personali lead, percentuali mediazione, prezzi inventati.

Pipeline suggerita: script locale → chunk → Supabase `kb_documents.embedding` via n8n o job batch.

Skill: `TEST-SKILL/skill-lead-automation-righetto.md`
