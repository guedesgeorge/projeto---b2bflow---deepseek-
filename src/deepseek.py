"""Geração de mensagens personalizadas via API do DeepSeek.

A API do DeepSeek é compatível com o formato da OpenAI, então usamos
o mesmo requests do resto do projeto, sem dependência nova.
Doc: https://api-docs.deepseek.com
"""

import logging
import os

import requests

logger = logging.getLogger(__name__)

_URL = "https://api.deepseek.com/chat/completions"
_MODELO = "deepseek-v4-flash"
_TIMEOUT = 60
_TENTATIVAS = 3  # quantas vezes tentar caso a IA devolva vazio


def _chave() -> str:
    """Lê a chave da API do DeepSeek do ambiente (.env)."""
    chave = os.getenv("DEEPSEEK_API_KEY")
    if not chave:
        raise RuntimeError(
            "Variável de ambiente 'DEEPSEEK_API_KEY' não definida. "
            "Pegue a chave em https://platform.deepseek.com e adicione no .env."
        )
    return chave


_SISTEMA = (
    "Você é um assistente de vendas da b2bflow, empresa de automação de "
    "WhatsApp para negócios. Escreva a PRIMEIRA mensagem de abordagem para um "
    "lead, em português do Brasil. Regras: tom amigável e profissional; no "
    "máximo 2 frases; comece cumprimentando a pessoa pelo nome; use no máximo "
    "1 emoji; termine com uma pergunta leve que abra conversa. NÃO invente "
    "nomes, dados ou preços que não foram informados. NUNCA use colchetes nem "
    "campos para preencher (ex.: [nome], [empresa]) — se não souber um dado, "
    "escreva a frase sem ele. Responda apenas com o texto final da mensagem, "
    "sem aspas e sem placeholders."
)


def _mensagem_reserva(nome: str) -> str:
    """Mensagem usada caso a IA insista em devolver vazio."""
    return (
        f"Olá {nome}, tudo bem? Aqui é da b2bflow — posso te contar rapidinho "
        "como a gente ajuda a automatizar o atendimento no WhatsApp?"
    )


def gerar_mensagem(nome: str, contexto: str) -> str:
    """Gera uma mensagem de abordagem personalizada para um contato.

    Tenta algumas vezes caso a IA devolva vazio; se ainda assim vier vazio,
    usa uma mensagem de reserva para nunca enviar texto em branco.
    """
    headers = {
        "Authorization": f"Bearer {_chave()}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": _MODELO,
        "messages": [
            {"role": "system", "content": _SISTEMA},
            {"role": "user", "content": f"Nome do lead: {nome}\nContexto: {contexto}"},
        ],
        "temperature": 0.8,
        "max_tokens": 300,
    }

    for tentativa in range(1, _TENTATIVAS + 1):
        resposta = requests.post(_URL, json=payload, headers=headers, timeout=_TIMEOUT)
        resposta.raise_for_status()
        dados = resposta.json()
        texto = (dados["choices"][0]["message"].get("content") or "").strip()
        if texto:
            logger.info("Mensagem gerada para %s.", nome)
            return texto
        logger.warning("IA retornou vazio para %s (tentativa %d/%d).", nome, tentativa, _TENTATIVAS)

    logger.warning("IA seguiu vazia para %s. Usando mensagem de reserva.", nome)
    return _mensagem_reserva(nome)
