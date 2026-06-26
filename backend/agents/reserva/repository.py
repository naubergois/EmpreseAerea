"""Repository de reserva."""
from sqlalchemy.orm import Session

from shared.datetime_utils import utc_now

from .models import Passageiro, Reserva, StatusReserva


class ReservaRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar(self, reserva: Reserva) -> Reserva:
        self.db.add(reserva)
        self.db.commit()
        self.db.refresh(reserva)
        return reserva

    def buscar_por_pnr(self, pnr: str) -> Reserva | None:
        return self.db.query(Reserva).filter(Reserva.pnr == pnr.upper()).first()

    def atualizar_status(self, pnr: str, status: StatusReserva) -> bool:
        reserva = self.buscar_por_pnr(pnr)
        if not reserva:
            return False
        reserva.status = status
        self.db.commit()
        return True

    def adicionar_passageiro(self, passageiro: Passageiro) -> Passageiro:
        self.db.add(passageiro)
        self.db.commit()
        self.db.refresh(passageiro)
        return passageiro

    def buscar_expiradas(self) -> list[Reserva]:
        return (
            self.db.query(Reserva)
            .filter(Reserva.status == StatusReserva.PENDENTE)
            .filter(Reserva.expira_em < utc_now())
            .all()
        )
