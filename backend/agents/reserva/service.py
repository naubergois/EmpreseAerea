"""Service de reserva."""
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session

from config import get_settings
from event_bus import Events, event_bus
from shared.exceptions import BusinessError, NotFoundError, ValidationError

from . import validators
from .models import Passageiro, Reserva, StatusReserva
from .pnr_generator import PNRGenerator
from .repository import ReservaRepository
from .schemas import AssentoRequest, PassageiroResponse, ReservaRequest, ReservaResponse
from .seat_manager import SeatManager

VOOS_LOTADOS = {"G3100"}


class ReservaService:
    def __init__(self, db: Session):
        self.repo = ReservaRepository(db)
        self.pnr_gen = PNRGenerator(db)
        self.seat_mgr = SeatManager(db)
        self.settings = get_settings()

    def criar_reserva(self, request: ReservaRequest) -> ReservaResponse:
        self._validar_voo_disponivel(request.voo_ida)
        self._validar_passageiros(request)

        pnr = self.pnr_gen.gerar()
        expira_em = datetime.utcnow() + timedelta(minutes=self.settings.booking_hold_minutes)

        reserva = Reserva(
            pnr=pnr,
            voo_ida=request.voo_ida,
            voo_volta=request.voo_volta,
            data_ida=request.data_ida,
            data_volta=request.data_volta,
            origem=request.origem,
            destino=request.destino,
            classe=request.classe,
            valor_total=request.valor_total,
            expira_em=expira_em,
        )
        reserva = self.repo.criar(reserva)

        passageiros_resp = []
        for p in request.passageiros:
            passageiro = Passageiro(
                reserva_id=reserva.id,
                nome=p.nome,
                sobrenome=p.sobrenome,
                cpf=p.cpf,
                passaporte=p.passaporte,
                passaporte_validade=p.passaporte_validade,
                data_nascimento=p.data_nascimento,
                tipo=p.tipo,
                email=p.email,
                telefone=p.telefone,
                adulto_vinculado_id=p.adulto_vinculado_id,
            )
            passageiro = self.repo.adicionar_passageiro(passageiro)
            passageiros_resp.append(PassageiroResponse(
                id=passageiro.id, nome=p.nome, sobrenome=p.sobrenome,
                cpf=p.cpf, passaporte=p.passaporte, data_nascimento=p.data_nascimento,
                tipo=p.tipo, email=p.email, telefone=p.telefone,
            ))

        self.seat_mgr.bloquear_assentos(request.voo_ida, len(request.passageiros), expira_em)
        event_bus.publish(Events.RESERVA_CRIADA, {"pnr": pnr, "valor": request.valor_total})

        return ReservaResponse(
            pnr=pnr, status="pendente_pagamento", voo_ida=request.voo_ida,
            origem=request.origem, destino=request.destino,
            valor_total=request.valor_total, expira_em=expira_em,
            passageiros=passageiros_resp,
        )

    def buscar(self, pnr: str) -> Reserva:
        reserva = self.repo.buscar_por_pnr(pnr)
        if not reserva:
            raise NotFoundError(f"Reserva {pnr} não encontrada")
        return reserva

    def cancelar(self, pnr: str) -> bool:
        reserva = self.buscar(pnr)
        self.repo.atualizar_status(pnr, StatusReserva.CANCELADA)
        self.seat_mgr.liberar_assentos(reserva.voo_ida)
        event_bus.publish(Events.RESERVA_CANCELADA, {"pnr": pnr})
        return True

    def selecionar_assento(self, pnr: str, req: AssentoRequest) -> dict:
        reserva = self.buscar(pnr)
        for p in reserva.passageiros:
            if p.id == req.passageiro_id:
                p.assento = req.assento
                self.repo.db.commit()
                return {"message": f"Assento {req.assento} atribuído", "assento": req.assento}
        raise NotFoundError("Passageiro não encontrado")

    def _validar_voo_disponivel(self, voo_id: str) -> None:
        for lotado in VOOS_LOTADOS:
            if lotado in voo_id:
                raise BusinessError("Voo sem disponibilidade", "sem_disponibilidade")

    def _validar_passageiros(self, request: ReservaRequest) -> None:
        tem_adulto = any(p.tipo == "ADT" for p in request.passageiros)
        for p in request.passageiros:
            if p.cpf:
                valido, msg = validators.validar_cpf(p.cpf)
                if not valido:
                    raise ValidationError(msg if msg != "documento_invalido" else "documento_invalido")
            if p.passaporte and p.passaporte_validade:
                valido, msg = validators.validar_passaporte_validade(
                    p.passaporte_validade, request.data_ida,
                )
                if not valido:
                    raise ValidationError(msg)
            idade = relativedelta(datetime.utcnow(), p.data_nascimento).years
            valido, msg = validators.validar_menor_acompanhado(idade, tem_adulto)
            if not valido:
                raise ValidationError(msg)
