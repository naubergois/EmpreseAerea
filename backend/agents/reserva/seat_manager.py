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
        return True
