# b2bflow — Abordagem de leads personalizada com IA (Python + Supabase + Z-API + DeepSeek)

Versão estendida do desafio b2bflow. Além do disparo da mensagem fixa, este projeto usa o **DeepSeek** para gerar, a partir do contexto de cada lead no banco, uma **mensagem de abordagem única e personalizada**, enviada pelo WhatsApp via Z-API.

A ideia é mostrar uma aplicação mais próxima do produto da b2bflow: transformar uma base de leads em abordagem sob medida, em escala.

## Dois modos

| Script | O que faz |
| ------ | --------- |
| `python main.py` | Envia a mensagem fixa: `Olá, <nome> tudo bem com você?` (versão do desafio) |
| `python main_ia.py` | Para cada contato, a IA escreve uma mensagem personalizada com base no campo `contexto` e envia |

## Estrutura

```
.
├── main.py            # disparo da mensagem fixa
├── main_ia.py         # disparo personalizado com IA (DeepSeek)
├── requirements.txt
├── .env.example
├── setup.sql          # tabela com a coluna 'contexto'
└── src/
    ├── config.py      # carrega e valida o .env
    ├── database.py    # busca os contatos no Supabase (com e sem contexto)
    ├── zapi.py        # envio da mensagem pela Z-API
    └── deepseek.py    # geração da mensagem personalizada via DeepSeek
```

## 1. Setup da tabela (Supabase)

Crie um projeto gratuito em [supabase.com](https://supabase.com), abra **SQL Editor > New query**, cole o conteúdo de [`setup.sql`](./setup.sql) e rode. A tabela `contatos` tem uma coluna **`contexto`**, que descreve a situação de cada lead (ex.: "pediu orçamento e sumiu") e alimenta a personalização da IA.

## 2. Variáveis de ambiente (.env)

```bash
cp .env.example .env
```

| Variável | Onde encontrar |
| -------- | -------------- |
| `SUPABASE_URL` / `SUPABASE_KEY` | Supabase → Project Settings → API Keys |
| `ZAPI_INSTANCE_ID` / `ZAPI_INSTANCE_TOKEN` | Painel Z-API → Instâncias |
| `ZAPI_CLIENT_TOKEN` | Painel Z-API → Segurança → Token de Segurança da Conta |
| `DEEPSEEK_API_KEY` | [platform.deepseek.com](https://platform.deepseek.com) → API Keys |

> A Z-API exige conectar a instância lendo o **QR Code** com o WhatsApp antes de rodar.

## 3. Como rodar

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python main_ia.py
```

Saída esperada (a IA gera um texto diferente por contato):

```
... | INFO | 3 contato(s) encontrado(s).
... | INFO | Mensagem para George: Oi George, tudo bem? Aqui é da b2bflow...
... | INFO | Mensagem enviada com sucesso para 5567...
```

## Como funciona a personalização

`main_ia.py` lê cada contato com seu `contexto`, envia nome + contexto ao DeepSeek (modelo `deepseek-v4-flash`, via API compatível com OpenAI) com um prompt que define o papel de assistente de vendas da b2bflow, e usa o texto gerado como mensagem. O envio reaproveita o mesmo módulo `zapi.py` do fluxo principal.

## Boas práticas

- Segredos em `.env` (fora do versionamento, via `.gitignore`).
- Configuração validada em `config.py`.
- Tratamento de erros e logs em cada etapa (banco, IA e envio).
- Código modular: banco, IA, envio e orquestração separados.
- A chave do DeepSeek só é exigida no fluxo de IA, sem quebrar o `main.py`.
