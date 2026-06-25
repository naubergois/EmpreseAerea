"""Saga pattern para rollback."""
from sqlalchemy.orm import Session

from event_bus import Events, event_bus


class SagaOrchestrator:
    def __init__(self, db: Session):
        self.db = db
        self.compensacoes: list[callable] = []

    def registrar(self, compensacao: callable) -> None:
        self.compensacoes.append(compensacao)

    def rollback(self, pnr: str | None = None, motivo: str = "") -> dict:
        erros = []
        for comp in reversed(self.compensacoes):
            try:
                comp()
            except Exception as exc:
                erros.append(str(exc))
        if pnr:
            from agents.reserva.service import ReservaService
            try:
                ReservaService(self.db).cancelar(pnr)
            except Exception:
                pass
            event_bus.publish(Events.RESERVA_CANCELADA, {"pnr": pnr, "motivo": motivo})
        return {"status": "rollback", "erros": erros}
