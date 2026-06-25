"""Detector de fraude simplificado."""
def avaliar_fraude(valor: float, ip: str = "") -> tuple[str, float]:
    score = 0.1
    if valor > 10000:
        score = 0.8
    if "vpn" in ip.lower():
        score = 0.9
    if score >= 0.85:
        return "revisao_manual", score
    if score >= 0.95:
        return "bloqueado", score
    return "aprovado", score
