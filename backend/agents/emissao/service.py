"""Service de emissão de bilhetes."""
import json
import random
import uuid
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from event_bus import Events, event_bus
from shared.exceptions import BusinessError, NotFoundError

from .models import Bilhete, StatusBilhete
from .schemas import BilheteResponse, BoardingPassResponse, EmitirRequest


class EmissaoService:
    def __init__(self, db: Session):
        self.db = db

    def emitir(self, req: EmitirRequest) -> BilheteResponse:
        from agents.reserva.models import Reserva

        reserva = self.db.query(Reserva).filter(Reserva.pnr == req.pnr.upper()).first()
        if not reserva:
            raise NotFoundError(f"Reserva {req.pnr} não encontrada")

        numero = f"045-{random.randint(1000000000, 9999999999)}"
        nome = "Passageiro"
        if reserva.passageiros:
            p = reserva.passageiros[0]
            nome = f"{p.nome} {p.sobrenome}"

        bilhete = Bilhete(
            numero=numero,
            pnr=req.pnr.upper(),
            passageiro_nome=nome,
            itinerario_json=json.dumps({
                "origem": reserva.origem,
                "destino": reserva.destino,
                "voo": reserva.voo_ida,
            }),
        )
        self.db.add(bilhete)
        self.db.commit()
        event_bus.publish(Events.BILHETE_EMITIDO, {"numero": numero, "pnr": req.pnr})
        return BilheteResponse(
            numero=numero, pnr=req.pnr, status="emitido",
            passageiro_nome=nome, emitido_em=bilhete.emitido_em,
        )

    def buscar(self, numero: str) -> BilheteResponse:
        b = self.db.query(Bilhete).filter(Bilhete.numero == numero).first()
        if not b:
            raise NotFoundError("Bilhete não encontrado")
        return BilheteResponse(
            numero=b.numero, pnr=b.pnr, status=b.status.value,
            passageiro_nome=b.passageiro_nome, emitido_em=b.emitido_em,
        )

    def boarding_pass(self, numero: str) -> BoardingPassResponse:
        b = self.db.query(Bilhete).filter(Bilhete.numero == numero).first()
        if not b:
            raise NotFoundError("Bilhete não encontrado")
        qr = f"M1{b.passageiro_nome[:20]}/{numero}/GRUGIG"
        return BoardingPassResponse(numero_bilhete=numero, qr_code=qr)

    def void(self, numero: str) -> dict:
        b = self.db.query(Bilhete).filter(Bilhete.numero == numero).first()
        if not b:
            raise NotFoundError("Bilhete não encontrado")
        if b.emitido_em < datetime.utcnow() - timedelta(hours=24):
            raise BusinessError("Prazo de void expirado", "prazo_void_expirado")
        b.status = StatusBilhete.VOID
        self.db.commit()
        return {"numero": numero, "status": "void"}

    def reemitir(self, numero: str) -> BilheteResponse:
        b = self.db.query(Bilhete).filter(Bilhete.numero == numero).first()
        if not b:
            raise NotFoundError("Bilhete não encontrado")
        novo = f"045-{random.randint(1000000000, 9999999999)}"
        novo_b = Bilhete(
            numero=novo, pnr=b.pnr, passageiro_nome=b.passageiro_nome,
            itinerario_json=b.itinerario_json, status=StatusBilhete.REEMITIDO,
        )
        self.db.add(novo_b)
        self.db.commit()
        return BilheteResponse(
            numero=novo, pnr=b.pnr, status="reemitido",
            passageiro_nome=b.passageiro_nome, emitido_em=novo_b.emitido_em,
        )
