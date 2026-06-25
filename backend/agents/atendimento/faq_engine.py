"""FAQ engine."""
FAQ = {
    "bagagem": "A franquia padrão é 1 bagagem de 23kg na tarifa Light.",
    "cancelamento": "Cancelamentos em até 24h têm reembolso integral conforme ANAC.",
    "check-in": "O check-in online abre 48h antes do voo.",
    "milhas": "Você acumula 1 milha a cada R$10 gastos.",
    "documentos": "Voos internacionais exigem passaporte com 6 meses de validade.",
}


def responder_faq(mensagem: str) -> str | None:
    msg = mensagem.lower()
    for chave, resposta in FAQ.items():
        if chave in msg:
            return resposta
    return None
