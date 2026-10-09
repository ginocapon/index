-- =====================================================================
-- LINDA KB v1 — Collega virtuale Righetto: base di conoscenza approvata
-- NON ancora eseguito in produzione. Applicare da Supabase > SQL Editor
-- SOLO dopo approvazione. Idempotente (si può rieseguire).
--
-- Principi:
--  * Linda risponde SOLO con testo approvato da un amministratore.
--  * Nessun modello AI generativo necessario (costo inferenza = 0 €).
--  * Ricerca testuale italiana (tsvector) + similarità (pg_trgm): nessun costo.
--  * Scrittura riservata agli amministratori (Supabase Auth + kb_admins),
--    NON alla password lato client di admin.html.
--  * Ogni modifica è in cronologia e ripristinabile.
--  * Domande degli utenti: minimizzate, ripulite da email/telefono, scadenza 90 gg.
-- =====================================================================

create schema if not exists extensions;
create extension if not exists pg_trgm with schema extensions;
create extension if not exists unaccent with schema extensions;
set search_path = public, extensions;

-- ---------------------------------------------------------------------
-- 0. Amministratori della KB (utenti Supabase Auth)
--    Dopo aver creato l'utente in Authentication > Users:
--    insert into kb_admins(user_id, nota) values ('<UUID utente>', 'Titolare');
-- ---------------------------------------------------------------------
create table if not exists kb_admins (
  user_id uuid primary key references auth.users(id) on delete cascade,
  nota text,
  created_at timestamptz not null default now()
);
alter table kb_admins enable row level security;

create or replace function kb_is_admin() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from kb_admins where user_id = auth.uid());
$$;
revoke all on function kb_is_admin() from public;
grant execute on function kb_is_admin() to anon, authenticated;

drop policy if exists kb_admins_self on kb_admins;
create policy kb_admins_self on kb_admins for select to authenticated
  using (user_id = auth.uid());

-- ---------------------------------------------------------------------
-- 1. Voci di conoscenza
-- ---------------------------------------------------------------------
create table if not exists kb_entries (
  id            uuid primary key default gen_random_uuid(),
  categoria     text not null default 'azienda'
                check (categoria in ('azienda','servizi','vendita','affitto','acquisto',
                                     'documenti','fiscale','mutui','territorio','procedure',
                                     'notizie','immobili','blog')),
  domanda       text not null check (char_length(domanda) between 5 and 300),
  varianti      text[] not null default '{}',
  risposta      text not null check (char_length(risposta) between 10 and 2500),
  fonti         jsonb not null default '[]'::jsonb,   -- [{"titolo":"..","url":"https://.."}]
  condizioni    text,                                 -- limiti / "da verificare in sede"
  stato         text not null default 'bozza'
                check (stato in ('bozza','da_verificare','approvata','scaduta')),
  scade_il      date,                                 -- dopo questa data non viene usata
  origine       text not null default 'manuale'
                check (origine in ('manuale','csv','faq_sito','suggerita','notizia','ipotetica')),
  gruppo        text,                                 -- raggruppa varianti della stessa domanda
  versione      int  not null default 1,
  creato_da     uuid default auth.uid(),
  approvato_da  uuid,
  approvato_il  timestamptz,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now(),
  search        tsvector
);

create index if not exists kb_entries_search_gin on kb_entries using gin (search);
create index if not exists kb_entries_trgm on kb_entries using gin (domanda gin_trgm_ops);
create index if not exists kb_entries_stato on kb_entries (stato, categoria);

create or replace function kb_entries_before_write() returns trigger
language plpgsql set search_path = public, extensions as $$
begin
  new.updated_at := now();
  new.search := to_tsvector('italian', unaccent(
      coalesce(new.domanda,'') || ' ' ||
      coalesce(array_to_string(new.varianti,' '),'') || ' ' ||
      coalesce(new.risposta,'')));
  if tg_op = 'UPDATE' then
    new.versione := old.versione + 1;
  end if;
  -- solo un admin può approvare; la modifica di una voce approvata la riporta in verifica
  if new.stato = 'approvata' then
    if not kb_is_admin() then
      raise exception 'Solo un amministratore può approvare';
    end if;
    if tg_op = 'INSERT' or old.stato is distinct from 'approvata' then
      new.approvato_da := auth.uid();
      new.approvato_il := now();
    elsif (old.risposta is distinct from new.risposta
           or old.domanda is distinct from new.domanda) then
      new.stato := 'da_verificare';          -- contenuto cambiato: richiede nuova approvazione
      new.approvato_da := null;
      new.approvato_il := null;
    end if;
  end if;
  return new;
end $$;
drop trigger if exists kb_entries_bw on kb_entries;
create trigger kb_entries_bw before insert or update on kb_entries
  for each row execute function kb_entries_before_write();

-- ---------------------------------------------------------------------
-- 2. Cronologia modifiche (audit + ripristino)
-- ---------------------------------------------------------------------
create table if not exists kb_history (
  id         bigserial primary key,
  entry_id   uuid not null,
  azione     text not null,                 -- update | delete
  utente     uuid default auth.uid(),
  quando     timestamptz not null default now(),
  snapshot   jsonb not null                 -- stato PRECEDENTE della voce
);
create index if not exists kb_history_entry on kb_history (entry_id, quando desc);

create or replace function kb_entries_audit() returns trigger
language plpgsql security definer set search_path = public as $$
begin
  if tg_op = 'UPDATE' then
    insert into kb_history(entry_id, azione, snapshot) values (old.id, 'update', to_jsonb(old) - 'search');
    return new;
  else
    insert into kb_history(entry_id, azione, snapshot) values (old.id, 'delete', to_jsonb(old) - 'search');
    return old;
  end if;
end $$;
drop trigger if exists kb_entries_aud on kb_entries;
create trigger kb_entries_aud after update or delete on kb_entries
  for each row execute function kb_entries_audit();

create or replace function kb_restore(p_history_id bigint) returns uuid
language plpgsql security definer set search_path = public as $$
declare h kb_history; s jsonb;
begin
  if not kb_is_admin() then raise exception 'Non autorizzato'; end if;
  select * into h from kb_history where id = p_history_id;
  if not found then raise exception 'Versione non trovata'; end if;
  s := h.snapshot;
  insert into kb_entries(id, categoria, domanda, varianti, risposta, fonti, condizioni, stato,
                         scade_il, origine, gruppo)
  values (h.entry_id, s->>'categoria', s->>'domanda',
          coalesce(array(select jsonb_array_elements_text(s->'varianti')), '{}'),
          s->>'risposta', coalesce(s->'fonti','[]'::jsonb), s->>'condizioni',
          'da_verificare',                      -- il ripristino richiede sempre nuova approvazione
          nullif(s->>'scade_il','')::date, coalesce(s->>'origine','manuale'), s->>'gruppo')
  on conflict (id) do update set
    categoria = excluded.categoria, domanda = excluded.domanda, varianti = excluded.varianti,
    risposta = excluded.risposta, fonti = excluded.fonti, condizioni = excluded.condizioni,
    stato = 'da_verificare', scade_il = excluded.scade_il, gruppo = excluded.gruppo;
  return h.entry_id;
end $$;
revoke all on function kb_restore(bigint) from public;
grant execute on function kb_restore(bigint) to authenticated;

-- ---------------------------------------------------------------------
-- 3. Domande reali degli utenti (privacy by design)
--    Il client rimuove email/telefono/codici fiscali PRIMA dell'invio;
--    il trigger li ripulisce di nuovo lato server.
-- ---------------------------------------------------------------------
create table if not exists linda_questions (
  id          bigserial primary key,
  created_at  timestamptz not null default now(),
  sessione    text,                                   -- id casuale, non collegato a persone
  pagina      text,
  domanda     text not null check (char_length(domanda) <= 400),
  trovata     boolean not null default false,
  kb_id       uuid references kb_entries(id) on delete set null,
  score       numeric(5,3),
  utile       boolean,                                -- feedback 👍/👎
  gestita     boolean not null default false          -- già trasformata in voce KB / ignorata
);
create index if not exists linda_questions_created on linda_questions (created_at desc);
create index if not exists linda_questions_gap on linda_questions (trovata, gestita);

create or replace function linda_redact(t text) returns text
language sql immutable as $$
  select left(
    regexp_replace(
      regexp_replace(
        regexp_replace(coalesce(t,''),
          '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', '[email]', 'g'),
        '(\+?\d[\d\s./-]{7,}\d)', '[telefono]', 'g'),
      '\m[A-Za-z]{6}\d\d[A-Za-z]\d\d[A-Za-z]\d{3}[A-Za-z]\M', '[cf]', 'g'),
    400)
$$;

create or replace function linda_questions_bi() returns trigger
language plpgsql as $$
begin
  new.domanda := linda_redact(new.domanda);
  new.utile := null;                 -- il feedback si imposta solo con linda_feedback()
  new.gestita := false;
  return new;
end $$;
drop trigger if exists linda_questions_before on linda_questions;
create trigger linda_questions_before before insert on linda_questions
  for each row execute function linda_questions_bi();

alter table linda_questions enable row level security;

-- ---------------------------------------------------------------------
-- 4. RLS: il pubblico NON legge né scrive direttamente; usa solo le RPC.
-- ---------------------------------------------------------------------
alter table kb_entries enable row level security;
alter table kb_history enable row level security;

drop policy if exists kb_entries_admin_all on kb_entries;
create policy kb_entries_admin_all on kb_entries for all to authenticated
  using (kb_is_admin()) with check (kb_is_admin());

drop policy if exists kb_history_admin_read on kb_history;
create policy kb_history_admin_read on kb_history for select to authenticated
  using (kb_is_admin());

drop policy if exists linda_questions_admin_all on linda_questions;
create policy linda_questions_admin_all on linda_questions for all to authenticated
  using (kb_is_admin()) with check (kb_is_admin());

-- ---------------------------------------------------------------------
-- 5. RPC pubbliche (anon): ricerca approvata, log domanda, feedback
-- ---------------------------------------------------------------------
create or replace function linda_kb_search(p_q text, p_lim int default 3)
returns table (id uuid, domanda text, risposta text, fonti jsonb, condizioni text,
               categoria text, aggiornata_il date, score real)
language sql stable security definer set search_path = public, extensions as $$
  with q as (
    select lower(unaccent(left(coalesce(p_q,''), 300))) as t
  ), tq as (
    -- query in OR sulle parole significative (>=3 lettere/cifre): una domanda lunga
    -- trova comunque la voce che ne contiene le parole chiave. Solo [a-z0-9]: nessuna iniezione.
    select nullif(array_to_string(array(
             select w from regexp_split_to_table(regexp_replace((select t from q), '[^a-z0-9 ]', ' ', 'g'), '\s+') w
             where char_length(w) >= 3 limit 12), ' | '), '') as s
  ), cand as (
    select e.id, e.domanda, e.risposta, e.fonti, e.condizioni, e.categoria,
           e.updated_at::date as aggiornata_il,
           ( coalesce(case when (select s from tq) is null then 0
                      else ts_rank_cd(e.search, to_tsquery('italian', (select s from tq)), 32) end, 0) * 2
             + greatest(similarity(unaccent(e.domanda), (select t from q)),
                        coalesce((select max(similarity(unaccent(v), (select t from q)))
                                  from unnest(e.varianti) v), 0))
           )::real as score
    from kb_entries e
    where e.stato = 'approvata'
      and (e.scade_il is null or e.scade_il >= current_date)
      and char_length((select t from q)) >= 3
  )
  select * from cand where score > 0.15 order by score desc limit greatest(1, least(p_lim, 5));
$$;
revoke all on function linda_kb_search(text, int) from public;
grant execute on function linda_kb_search(text, int) to anon, authenticated;

create or replace function linda_log_question(p_sessione text, p_pagina text, p_domanda text,
                                              p_trovata boolean, p_kb uuid, p_score numeric)
returns bigint language plpgsql security definer set search_path = public as $$
declare rid bigint;
begin
  if char_length(coalesce(p_domanda,'')) < 3 then return null; end if;
  insert into linda_questions(sessione, pagina, domanda, trovata, kb_id, score)
  values (left(p_sessione, 40), left(p_pagina, 120), left(p_domanda, 400),
          coalesce(p_trovata, false), p_kb, p_score)
  returning id into rid;
  return rid;
end $$;
revoke all on function linda_log_question(text, text, text, boolean, uuid, numeric) from public;
grant execute on function linda_log_question(text, text, text, boolean, uuid, numeric) to anon, authenticated;

create or replace function linda_feedback(p_id bigint, p_sessione text, p_utile boolean)
returns void language sql security definer set search_path = public as $$
  update linda_questions set utile = p_utile
  where id = p_id and sessione = left(p_sessione, 40) and created_at > now() - interval '1 day';
$$;
revoke all on function linda_feedback(bigint, text, boolean) from public;
grant execute on function linda_feedback(bigint, text, boolean) to anon, authenticated;

-- ---------------------------------------------------------------------
-- 6. Rapporto lacune (solo admin): domande senza risposta raggruppate
-- ---------------------------------------------------------------------
create or replace view linda_lacune with (security_invoker = true) as
select lower(regexp_replace(unaccent(domanda), '[^a-z0-9 ]', '', 'gi')) as chiave,
       min(domanda) as esempio,
       count(*) as volte,
       max(created_at) as ultima,
       count(*) filter (where utile is false) as giudicate_inutili
from linda_questions
where trovata = false and gestita = false
group by 1
order by volte desc, ultima desc;

-- ---------------------------------------------------------------------
-- 7. Conservazione dati: elimina domande oltre 90 giorni
--    Pianificare con pg_cron (Supabase > Database > Extensions) oppure
--    lanciare a mano:  select linda_purge_questions();
-- ---------------------------------------------------------------------
create or replace function linda_purge_questions(p_giorni int default 90) returns int
language plpgsql security definer set search_path = public as $$
declare n int;
begin
  delete from linda_questions where created_at < now() - make_interval(days => p_giorni);
  get diagnostics n = row_count;
  return n;
end $$;
revoke all on function linda_purge_questions(int) from public, anon;
grant execute on function linda_purge_questions(int) to authenticated;

-- ---------------------------------------------------------------------
-- 8. (Facoltativo, consigliato) Tabella valutazioni chatbot oggi MANCANTE:
--    js/chatbot.js scrive su recensioni_chatbot che NON esiste → voti persi.
-- ---------------------------------------------------------------------
create table if not exists recensioni_chatbot (
  id bigserial primary key,
  created_at timestamptz not null default now(),
  voto int check (voto between 1 and 5),
  pagina text check (char_length(pagina) <= 120)
);
alter table recensioni_chatbot enable row level security;
drop policy if exists recensioni_chatbot_insert on recensioni_chatbot;
create policy recensioni_chatbot_insert on recensioni_chatbot for insert to anon, authenticated
  with check (true);
drop policy if exists recensioni_chatbot_admin_read on recensioni_chatbot;
create policy recensioni_chatbot_admin_read on recensioni_chatbot for select to authenticated
  using (kb_is_admin());
