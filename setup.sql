-- Setup da tabela no Supabase (versão com IA)
-- Cole e rode no SQL Editor do projeto (Supabase > SQL Editor > New query)

create table if not exists public.contatos (
    id           bigint generated always as identity primary key,
    nome_contato text not null,
    telefone     text not null,  -- formato DDI+DDD+numero, ex.: 5567999999999
    contexto     text,           -- usado pela IA para personalizar a mensagem
    created_at   timestamptz default now()
);

-- Garante a coluna 'contexto' caso a tabela já existisse
alter table public.contatos add column if not exists contexto text;

-- Contatos de exemplo (troque pelos números reais que você controla).
-- O 'contexto' é o que a IA usa para escrever uma abordagem sob medida.
insert into public.contatos (nome_contato, telefone, contexto) values
    ('George', '5567999999999', 'Lead que pediu orçamento de automação de WhatsApp e ainda não respondeu'),
    ('Maria',  '5567988888888', 'Cliente antiga que usava o plano básico e cancelou há 2 meses'),
    ('João',   '5511977777777', 'Indicação de um cliente atual; ainda não conhece a b2bflow');
