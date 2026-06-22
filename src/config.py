"""Carrega e valida as variáveis de ambiente a partir do arquivo .env."""

import os

from dotenv import load_dotenv

load_dotenv()


def _obrigatoria(nome: str) -> str:
    """Retorna o valor da variável de ambiente ou levanta erro se ausente."""
    valor = os.getenv(nome)
    if not valor:
        raise RuntimeError(
            f"Variável de ambiente '{nome}' não definida. "
            f"Confira o seu arquivo .env (use o .env.example como base)."
        )
    return valor


# Supabase
SUPABASE_URL = _obrigatoria("SUPABASE_URL")
SUPABASE_KEY = _obrigatoria("SUPABASE_KEY")
SUPABASE_TABELA = os.getenv("SUPABASE_TABELA", "contatos")

# Z-API
ZAPI_INSTANCE_ID = _obrigatoria("ZAPI_INSTANCE_ID")
ZAPI_INSTANCE_TOKEN = _obrigatoria("ZAPI_INSTANCE_TOKEN")
ZAPI_CLIENT_TOKEN = _obrigatoria("ZAPI_CLIENT_TOKEN")

# Quantos contatos enviar no máximo (regra do desafio: até 3)
LIMITE_CONTATOS = int(os.getenv("LIMITE_CONTATOS", "3"))
