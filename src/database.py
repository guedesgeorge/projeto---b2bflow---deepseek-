"""Acesso ao banco de dados no Supabase."""

import logging
from typing import List

from supabase import Client, create_client

from src import config

logger = logging.getLogger(__name__)


def _cliente() -> Client:
    """Cria o cliente do Supabase usando as credenciais do .env."""
    return create_client(config.SUPABASE_URL, config.SUPABASE_KEY)


def buscar_contatos(limite: int = config.LIMITE_CONTATOS) -> List[dict]:
    """Busca os contatos cadastrados no Supabase.

    Retorna uma lista de dicionários no formato:
        {"nome_contato": "...", "telefone": "..."}

    Aplica o limite definido pelo desafio (até 3 contatos).
    """
    supabase = _cliente()

    logger.info("Buscando ate %d contato(s) na tabela '%s'...", limite, config.SUPABASE_TABELA)

    resposta = (
        supabase.table(config.SUPABASE_TABELA)
        .select("nome_contato, telefone")
        .limit(limite)
        .execute()
    )

    contatos = resposta.data or []
    logger.info("%d contato(s) encontrado(s).", len(contatos))
    return contatos


def buscar_contatos_ia(limite: int = config.LIMITE_CONTATOS) -> List[dict]:
    """Igual ao buscar_contatos, mas também traz o campo 'contexto'.

    O 'contexto' é usado para personalizar a mensagem com IA (DeepSeek).
    Retorna dicionários no formato:
        {"nome_contato": "...", "telefone": "...", "contexto": "..."}
    """
    supabase = _cliente()

    logger.info("Buscando ate %d contato(s) com contexto...", limite)

    resposta = (
        supabase.table(config.SUPABASE_TABELA)
        .select("nome_contato, telefone, contexto")
        .limit(limite)
        .execute()
    )

    contatos = resposta.data or []
    logger.info("%d contato(s) encontrado(s).", len(contatos))
    return contatos
