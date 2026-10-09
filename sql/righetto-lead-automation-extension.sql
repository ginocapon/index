-- Righetto Immobiliare — estensione CRM lead (Livello A scoring + funnel eventi)
-- Eseguire in Supabase SQL Editor (staging prima, poi produzione con OK esplicito).
-- Skill: TEST-SKILL/skill-lead-automation-righetto.md

-- 1) Colonne su richieste (compatibile con admin + rig-lead-form.js)
alter table if exists public.richieste
  add column if not exists dedup_key text,
  add column if not exists lead_score int default 0,
  add column if not exists lead_temperature text default 'cold',
  add column if not exists owner_path text,
  add column if not exists lead_stage text default 'ricevuto',
  add column if not exists ai_summary text,
  add column if not exists scored_at timestamptz,
  add column if not exists canale text default 'website';

create unique index if not exists richieste_dedup_key_uidx
  on public.richieste (dedup_key)
  where dedup_key is not null;

create index if not exists richieste_lead_score_idx
  on public.richieste (lead_score desc, created_at desc);

-- 2) Eventi funnel (punto 8 roadmap acquisizione)
create table if not exists public.lead_events (
  id uuid primary key default gen_random_uuid(),
  richiesta_id uuid not null references public.richieste(id) on delete cascade,
  evento text not null check (evento in (
    'ricevuto', 'contattato', 'appuntamento', 'incarico', 'rogito', 'provvigione_maturata'
  )),
  note text,
  created_at timestamptz default now(),
  created_by text default 'system'
);

create index if not exists lead_events_richiesta_idx on public.lead_events (richiesta_id, created_at desc);

alter table public.lead_events enable row level security;
-- Nessuna policy anon: solo service_role / admin

-- 3) pgvector KB (Livello B n8n — opzionale, stesso progetto Supabase)
create extension if not exists vector;

create table if not exists public.kb_documents (
  id uuid primary key default gen_random_uuid(),
  content text not null,
  metadata jsonb default '{}'::jsonb,
  embedding vector(768)
);

alter table public.kb_documents enable row level security;

create or replace function public.match_documents (
  query_embedding vector(768),
  match_count int default 5
) returns table (id uuid, content text, metadata jsonb, similarity float)
language sql stable as $$
  select id, content, metadata,
         1 - (kb_documents.embedding <=> query_embedding) as similarity
  from kb_documents
  order by kb_documents.embedding <=> query_embedding
  limit match_count;
$$;

-- 4) Dedup check (n8n / edge function)
create or replace function public.richiesta_exists(p_key text)
returns table(found boolean)
language sql stable as $$
  select exists(select 1 from public.richieste where dedup_key = p_key);
$$;

-- 5) Vista admin-safe (no email/telefono in dashboard pubbliche future)
create or replace view public.richieste_public_score as
  select id,
         split_part(coalesce(nome, ''), ' ', 1) as first_name,
         provenienza,
         lead_score,
         lead_temperature,
         owner_path,
         lead_stage,
         created_at
  from public.richieste
  order by lead_score desc nulls last, created_at desc;

-- grant select on richieste_public_score to anon; -- solo se dashboard esterna con RLS stretta

comment on column public.richieste.lead_stage is 'ricevuto → contattato → appuntamento → incarico → rogito → chiuso';
