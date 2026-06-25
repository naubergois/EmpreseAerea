"""Análise simples de sentimento do cliente."""

NEGATIVOS = ("reclama", "péssimo", "horrível", "absurdo", "procon", "raiva", "indignado", "cancelar tudo")
POSITIVOS = ("obrigado", "ótimo", "excelente", "parabéns", "adorei", "perfeito")
URGENTES = ("hoje", "amanhã", "urgente", "embarque", "perdi o voo", "atrasou")


def analisar(mensagem: str) -> tuple[str, bool]:
    msg = mensagem.lower()
    if any(w in msg for w in NEGATIVOS):
        return "negativo", any(w in msg for w in URGENTES)
    if any(w in msg for w in POSITIVOS):
        return "positivo", False
    if any(w in msg for w in URGENTES):
        return "neutro", True
    return "neutro", False
