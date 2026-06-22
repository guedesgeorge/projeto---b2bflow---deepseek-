"""Envio de mensagens de texto pelo WhatsApp via Z-API."""

import logging

import requests

from src import config

logger = logging.getLogger(__name__)

# Endpoint oficial da Z-API para envio de texto simples
_URL = (
    f"https://api.z-api.io/instances/{config.ZAPI_INSTANCE_ID}"
    f"/token/{config.ZAPI_INSTANCE_TOKEN}/send-text"
)

# Timeout (em segundos) para a requisição HTTP
_TIMEOUT = 30


def enviar_mensagem(telefone: str, mensagem: str) -> bool:
    """Envia uma mensagem de texto para um número via Z-API.

    O telefone deve estar no formato DDI + DDD + número, somente dígitos.
    Ex.: 5567999999999

    Retorna True em caso de sucesso e False em caso de falha.
    """
    headers = {
        "Content-Type": "application/json",
        "Client-Token": config.ZAPI_CLIENT_TOKEN,
    }
    payload = {"phone": telefone, "message": mensagem}

    try:
        resposta = requests.post(_URL, json=payload, headers=headers, timeout=_TIMEOUT)
        resposta.raise_for_status()
    except requests.exceptions.RequestException as erro:
        # Loga o corpo da resposta quando disponível (ajuda a depurar)
        corpo = getattr(erro.response, "text", "") if getattr(erro, "response", None) else ""
        logger.error("Falha ao enviar para %s: %s %s", telefone, erro, corpo)
        return False

    logger.info("Mensagem enviada com sucesso para %s.", telefone)
    return True
