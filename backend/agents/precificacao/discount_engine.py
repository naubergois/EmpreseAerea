"""Motor de descontos e cupons."""
from datetime import datetime

from sqlalchemy.orm import Session

from shared.exceptions import BusinessError

from .models import Cupom

DESCONTOS_NIVEL = {"Bronze": 0, "Prata": 0.05, "Ouro": 0.10, "Diamante": 0.15}


def validar_cupom(db: Session, codigo: str, valor: float, origem: str | None, destino: str | None, nivel: str | None) -> tuple[float, str]:
    cupom = db.query(Cupom).filter(Cupom.codigo == codigo.upper()).first()
    if not cupom:
        raise BusinessError("Cupom não encontrado", "cupom_invalido")
    if cupom.valido_ate and cupom.valido_ate < datetime.utcnow():
        raise BusinessError("Cupom expirado", "cupom_expirado")
    if cupom.uso_atual >= cupom.uso_max:
        raise BusinessError("Cupom esgotado", "cupom_esgotado")
    if cupom.valor_minimo and valor < cupom.valor_minimo:
        raise BusinessError("Valor mínimo não atingido", "valor_minimo_nao_atingido")
    if cupom.rota_origem and origem and cupom.rota_origem != origem:
        raise BusinessError("Cupom inválido para esta rota", "cupom_rota_invalida")
    if cupom.rota_destino and destino and cupom.rota_destino != destino:
        raise BusinessError("Cupom inválido para esta rota", "cupom_rota_invalida")
    if cupom.nivel_minimo and nivel and nivel < cupom.nivel_minimo:
        raise BusinessError("Nível de fidelidade insuficiente", "cupom_nivel_insuficiente")

    if cupom.tipo == "percentual":
        return valor * (cupom.valor / 100), "OK"
    return min(cupom.valor, valor), "OK"
