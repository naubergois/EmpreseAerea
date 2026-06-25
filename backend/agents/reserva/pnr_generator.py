"""Geração de PNR único."""
import random
import string

from sqlalchemy.orm import Session

from .models import Reserva

CHARS = string.ascii_uppercase + string.digits


class PNRGenerator:
    def __init__(self, db: Session):
        self.db = db

    def gerar(self) -> str:
        for _ in range(100):
            pnr = "".join(random.choices(CHARS, k=6))
            exists = self.db.query(Reserva).filter(Reserva.pnr == pnr).first()
            if not exists:
                return pnr
        raise RuntimeError("Não foi possível gerar PNR único")
