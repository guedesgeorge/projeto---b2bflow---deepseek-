"""Ponto de entrada do desafio b2bflow.

Lê os contatos cadastrados no Supabase e envia, via Z-API,
a mensagem: "Olá, <nome_contato> tudo bem com você?"

Uso:
    python main.py
"""

import logging
import sys

from src import config, database, zapi

# Configuração de logs: nível INFO, com data/hora e nível em cada linha
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("b2bflow")


def montar_mensagem(nome: str) -> str:
    """Monta a mensagem exata exigida pelo desafio."""
    return f"Olá, {nome} tudo bem com você?"


def main() -> int:
    """Executa o fluxo de ponta a ponta. Retorna o código de saída do processo."""
    logger.info("Iniciando o disparo de mensagens (b2bflow).")

    # 1) Buscar contatos no Supabase
    try:
        contatos = database.buscar_contatos(config.LIMITE_CONTATOS)
    except Exception as erro:  # noqa: BLE001 - queremos logar qualquer falha de conexão
        logger.error("Erro ao buscar contatos no Supabase: %s", erro)
        return 1

    if not contatos:
        logger.warning("Nenhum contato encontrado. Cadastre ao menos um na tabela.")
        return 1

    # 2) Enviar a mensagem para cada contato
    enviados = 0
    for contato in contatos:
        nome = (contato.get("nome_contato") or "").strip()
        telefone = (contato.get("telefone") or "").strip()

        if not nome or not telefone:
            logger.warning("Contato ignorado por dados incompletos: %s", contato)
            continue

        mensagem = montar_mensagem(nome)
        logger.info("Enviando para %s (%s)...", nome, telefone)

        if zapi.enviar_mensagem(telefone, mensagem):
            enviados += 1

    # 3) Resumo final
    total = len(contatos)
    logger.info("Concluído: %d de %d mensagem(ns) enviada(s) com sucesso.", enviados, total)

    # Código de saída 0 se enviou pelo menos uma; caso contrário, 1
    return 0 if enviados > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
