"""Gerenciamento de assentos."""
from datetime import datetime
from sqlalchemy.orm import Session


class SeatManager:
    _bloqueios: dict[str, dict] = {}

    def __init__(self, db: Session):
        self.db = db

    def bloquear_assentos(self, voo: str, qtd: int, expira_em: datetime) -> None:
        self._bloqueios[voo] = {"qtd": qtd, "expira_em": expira_em}

    def liberar_assentos(self, voo: str) -> None:
        self._bloqueios.pop(voo, None)

    def atribuir(self, voo: str, assento: str) -> bool:
        """Atribui um assento a um voo. Retorna False se já estiver ocupado."""
        atribuidos = self._bloqueios.setdefault(voo, {}).setdefault("atribuidos", set())
        if assento in atribuidos:
            return False
        atribuidos.add(assento)
        return True
