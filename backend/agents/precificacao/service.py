"""Service de precificação."""
import json
import uuid
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from event_bus import Events, event_bus
from shared.exceptions import BusinessError

from .discount_engine import DESCONTOS_NIVEL, validar_cupom
from .models import Cotacao
from .schemas import BreakdownItem, CupomValidacaoRequest, CupomValidacaoResponse, PrecoRequest, PrecoResponse


class PrecificacaoService:
    TTL_MINUTES = 20

    def __init__(self, db: Session):
        self.db = db

    def calcular(self, req: PrecoRequest) -> PrecoResponse:
        taxas = req.preco_base * 0.12
        breakdown = [
            BreakdownItem(descricao="Tarifa base", valor=req.preco_base),
            BreakdownItem(descricao="Taxas e encargos", valor=round(taxas, 2)),
        ]

        subtotal = req.preco_base + taxas
        subtotal += req.preco_base * 0.75 * req.criancas
        subtotal += req.preco_base * 0.10 * req.bebes
        subtotal *= req.adultos if req.adultos else 1

        desconto = 0.0
        if req.nivel_fidelidade:
            pct = DESCONTOS_NIVEL.get(req.nivel_fidelidade, 0)
            desconto += subtotal * pct

        if req.cupom:
            d, _ = validar_cupom(self.db, req.cupom, subtotal, None, None, req.nivel_fidelidade)
            desconto += d

        if req.canal == "app":
            desconto += subtotal * 0.02

        valor_total = max(subtotal - desconto, 0)
        cotacao_id = f"QUOTE-{uuid.uuid4().hex[:8].upper()}"
        expira = datetime.utcnow() + timedelta(minutes=self.TTL_MINUTES)

        cotacao = Cotacao(
            id=cotacao_id,
            voo_id=req.voo_id,
            valor_base=req.preco_base,
            valor_total=valor_total,
            breakdown_json=json.dumps([b.model_dump() for b in breakdown]),
            cupom=req.cupom,
            expira_em=expira,
        )
        self.db.add(cotacao)
        self.db.commit()

        event_bus.publish(Events.PRICING_READY, {"cotacao_id": cotacao_id, "valor": valor_total})
        return PrecoResponse(
            cotacao_id=cotacao_id,
            valor_base=req.preco_base,
            valor_total=round(valor_total, 2),
            breakdown=breakdown,
            expira_em=expira,
            desconto_aplicado=round(desconto, 2),
        )

    def validar_cupom(self, req: CupomValidacaoRequest) -> CupomValidacaoResponse:
        try:
            desconto, msg = validar_cupom(
                self.db, req.codigo, req.valor_compra,
                req.origem, req.destino, req.nivel_fidelidade,
            )
            return CupomValidacaoResponse(valido=True, desconto=round(desconto, 2), mensagem=msg)
        except BusinessError as e:
            return CupomValidacaoResponse(valido=False, mensagem=str(e), codigo_erro=e.code)

    def obter_cotacao(self, cotacao_id: str) -> PrecoResponse | None:
        cot = self.db.query(Cotacao).filter(Cotacao.id == cotacao_id).first()
        if not cot:
            return None
        if cot.expira_em < datetime.utcnow():
            raise BusinessError("Cotação expirada", "cotacao_expirada")
        breakdown = [BreakdownItem(**b) for b in json.loads(cot.breakdown_json)]
        return PrecoResponse(
            cotacao_id=cot.id,
            valor_base=cot.valor_base,
            valor_total=cot.valor_total,
            breakdown=breakdown,
            expira_em=cot.expira_em,
        )
