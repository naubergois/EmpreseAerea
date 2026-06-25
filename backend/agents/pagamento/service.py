"""Service de pagamento."""
import uuid
from datetime import datetime, timedelta

import qrcode
import io
import base64

from sqlalchemy.orm import Session

from config import get_settings
from event_bus import Events, event_bus
from shared.exceptions import BusinessError

from .fraud_detector import avaliar_fraude
from .models import MetodoPagamento, StatusPagamento, Transacao
from .schemas import (
    PagamentoBoletoRequest,
    PagamentoCartaoRequest,
    PagamentoPixRequest,
    PagamentoResponse,
    PagamentoSplitRequest,
    ReembolsoRequest,
)


class PagamentoService:
    def __init__(self, db: Session):
        self.db = db
        self.settings = get_settings()

    def pagar_cartao(self, req: PagamentoCartaoRequest) -> PagamentoResponse:
        if req.numero_cartao.replace(" ", "") in ("0000000000000000",):
            raise BusinessError("Cartão recusado", "cartao_recusado")
        status_fraude, _ = avaliar_fraude(req.valor)
        if status_fraude == "bloqueado":
            raise BusinessError("Suspeita de fraude", "suspeita_fraude")

        txn_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"
        txn = Transacao(
            id=txn_id, pnr=req.pnr, metodo=MetodoPagamento.CARTAO,
            status=StatusPagamento.APROVADO, valor=req.valor, parcelas=req.parcelas,
        )
        self.db.add(txn)
        self.db.commit()
        event_bus.publish(Events.PAGAMENTO_CONFIRMADO, {"id": txn_id, "pnr": req.pnr, "valor": req.valor})
        return PagamentoResponse(id=txn_id, pnr=req.pnr, status="aprovado", metodo="cartao", valor=req.valor)

    def gerar_pix(self, req: PagamentoPixRequest) -> PagamentoResponse:
        txn_id = f"PIX-{uuid.uuid4().hex[:10].upper()}"
        expira = datetime.utcnow() + timedelta(minutes=self.settings.pix_expiry_minutes)
        copia_cola = f"00020126580014br.gov.bcb.pix0136{txn_id}52040000530398654{req.valor:.2f}"
        qr = qrcode.make(copia_cola)
        buf = io.BytesIO()
        qr.save(buf, format="PNG")
        qr_b64 = base64.b64encode(buf.getvalue()).decode()

        txn = Transacao(
            id=txn_id, pnr=req.pnr, metodo=MetodoPagamento.PIX,
            status=StatusPagamento.PENDENTE, valor=req.valor,
            pix_qr=qr_b64, pix_copia_cola=copia_cola, expira_em=expira,
        )
        self.db.add(txn)
        self.db.commit()
        return PagamentoResponse(
            id=txn_id, pnr=req.pnr, status="pendente", metodo="pix",
            valor=req.valor, pix_qr=qr_b64, pix_copia_cola=copia_cola, expira_em=expira,
        )

    def webhook_pix(self, txn_id: str, valor: float) -> PagamentoResponse:
        txn = self.db.query(Transacao).filter(Transacao.id == txn_id).first()
        if not txn:
            raise BusinessError("Transação não encontrada", "transacao_nao_encontrada")
        if abs(txn.valor - valor) > 0.01:
            raise BusinessError("Valor incorreto", "valor_incorreto")
        txn.status = StatusPagamento.APROVADO
        self.db.commit()
        event_bus.publish(Events.PAGAMENTO_CONFIRMADO, {"id": txn_id, "pnr": txn.pnr, "valor": valor})
        return PagamentoResponse(id=txn_id, pnr=txn.pnr, status="aprovado", metodo="pix", valor=valor)

    def gerar_boleto(self, req: PagamentoBoletoRequest) -> PagamentoResponse:
        txn_id = f"BOL-{uuid.uuid4().hex[:10].upper()}"
        expira = datetime.utcnow() + timedelta(days=3)
        codigo = f"23793.38128 60000.000003 00000.000{txn_id[-4:]}"
        txn = Transacao(
            id=txn_id, pnr=req.pnr, metodo=MetodoPagamento.BOLETO,
            status=StatusPagamento.PENDENTE, valor=req.valor,
            boleto_codigo=codigo, expira_em=expira,
        )
        self.db.add(txn)
        self.db.commit()
        return PagamentoResponse(
            id=txn_id, pnr=req.pnr, status="pendente", metodo="boleto",
            valor=req.valor, boleto_codigo=codigo, expira_em=expira,
        )

    def status(self, txn_id: str) -> PagamentoResponse:
        txn = self.db.query(Transacao).filter(Transacao.id == txn_id).first()
        if not txn:
            raise BusinessError("Transação não encontrada", "transacao_nao_encontrada")
        return PagamentoResponse(
            id=txn.id, pnr=txn.pnr, status=txn.status.value,
            metodo=txn.metodo.value, valor=txn.valor,
        )

    def reembolsar(self, txn_id: str, req: ReembolsoRequest) -> dict:
        txn = self.db.query(Transacao).filter(Transacao.id == txn_id).first()
        if not txn:
            raise BusinessError("Transação não encontrada", "transacao_nao_encontrada")
        if txn.status == StatusPagamento.REEMBOLSADO:
            return {"id": txn_id, "status": "reembolsado", "idempotente": True}
        txn.status = StatusPagamento.REEMBOLSADO
        self.db.commit()
        valor = req.valor or txn.valor
        event_bus.publish(Events.REEMBOLSO_PROCESSADO, {"id": txn_id, "valor": valor})
        return {"id": txn_id, "status": "reembolsado", "valor": valor}

    def pagar_split(self, req: PagamentoSplitRequest) -> PagamentoResponse:
        txn_id = f"SPL-{uuid.uuid4().hex[:10].upper()}"
        txn = Transacao(
            id=txn_id, pnr=req.pnr, metodo=MetodoPagamento.SPLIT,
            status=StatusPagamento.APROVADO, valor=req.valor_total,
            milhas_usadas=req.milhas,
        )
        self.db.add(txn)
        self.db.commit()
        event_bus.publish(Events.PAGAMENTO_CONFIRMADO, {"id": txn_id, "pnr": req.pnr})
        return PagamentoResponse(id=txn_id, pnr=req.pnr, status="aprovado", metodo="split", valor=req.valor_total)
