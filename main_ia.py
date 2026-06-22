"""Disparo de mensagens personalizadas com IA (DeepSeek) — BÔNUS.

Lê os contatos no Supabase (com o campo 'contexto') e, para cada um,
gera com o DeepSeek uma mensagem de abordagem única e a envia via Z-API.

É um complemento ao main.py (que faz o disparo da mensagem fixa do
desafio). Este aqui mostra uma abordagem mais próxima do produto da
b2bflow: personalização de leads em escala.

Uso:
    python main_ia.py
"""

import logging
import sys

from src import config, database, deepseek, zapi

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("b2bflow-ia")


def main() -> int:
    """Executa o fluxo personalizado de ponta a ponta."""
    logger.info("Iniciando o disparo personalizado com IA (DeepSeek).")

    # 1) Buscar contatos (com contexto) no Supabase
    try:
        contatos = database.buscar_contatos_ia(config.LIMITE_CONTATOS)
    except Exception as erro:  # noqa: BLE001
        logger.error("Erro ao buscar contatos no Supabase: %s", erro)
        return 1

    if not contatos:
        logger.warning("Nenhum contato encontrado. Cadastre ao menos um na tabela.")
        return 1

    # 2) Para cada contato: gerar mensagem com IA e enviar
    enviados = 0
    for contato in contatos:
        nome = (contato.get("nome_contato") or "").strip()
        telefone = (contato.get("telefone") or "").strip()
        contexto = (contato.get("contexto") or "primeiro contato com o lead").strip()

        if not nome or not telefone:
            logger.warning("Contato ignorado por dados incompletos: %s", contato)
            continue

        # Gera a mensagem personalizada
        try:
            mensagem = deepseek.gerar_mensagem(nome, contexto)
        except Exception as erro:  # noqa: BLE001
            logger.error("Falha ao gerar mensagem para %s: %s", nome, erro)
            continue

        logger.info("Mensagem para %s: %s", nome, mensagem)

        # Envia pela Z-API (mesma função do fluxo principal)
        if zapi.enviar_mensagem(telefone, mensagem):
            enviados += 1

    # 3) Resumo
    total = len(contatos)
    logger.info("Concluido: %d de %d mensagem(ns) enviada(s) com sucesso.", enviados, total)
    return 0 if enviados > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
