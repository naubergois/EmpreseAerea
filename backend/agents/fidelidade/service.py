"""Service de fidelidade."""
from sqlalchemy.orm import Session

from event_bus import Events, event_bus
from shared.exceptions import BusinessError

from .miles_calculator import LIMIARES, NIVEIS, calcular_milhas
from .models import ContaMilhas, TransacaoMilhas
from .schemas import AcumularRequest, ExtratoItem, MilhasResponse, NivelResponse, ResgatarRequest


class FidelidadeService:
    def __init__(self, db: Session):
        self.db = db

    def _conta(self, cliente_id: str) -> ContaMilhas:
        conta = self.db.query(ContaMilhas).filter(ContaMilhas.cliente_id == cliente_id).first()
        if not conta:
            conta = ContaMilhas(cliente_id=cliente_id)
            self.db.add(conta)
            self.db.commit()
        return conta

    def saldo(self, cliente_id: str) -> MilhasResponse:
        c = self._conta(cliente_id)
        return MilhasResponse(
            cliente_id=cliente_id, saldo=c.saldo, nivel=c.nivel,
            milhas_qualificadas=c.milhas_qualificadas,
        )

    def acumular(self, req: AcumularRequest) -> MilhasResponse:
        milhas = calcular_milhas(req.valor, req.nivel)
        conta = self._conta(req.cliente_id)
        conta.saldo += milhas
        conta.milhas_qualificadas += milhas
        self._atualizar_nivel(conta)
        self.db.add(TransacaoMilhas(
            cliente_id=req.cliente_id, tipo="credito", quantidade=milhas,
            descricao=f"Compra PNR {req.pnr}",
        ))
        self.db.commit()
        event_bus.publish(Events.MILHAS_ACUMULADAS, {"cliente_id": req.cliente_id, "milhas": milhas})
        return self.saldo(req.cliente_id)

    def resgatar(self, req: ResgatarRequest) -> MilhasResponse:
        conta = self._conta(req.cliente_id)
        if conta.saldo < req.milhas:
            raise BusinessError("Milhas insuficientes", "milhas_insuficientes")
        conta.saldo -= req.milhas
        self.db.add(TransacaoMilhas(
            cliente_id=req.cliente_id, tipo="debito", quantidade=req.milhas,
            descricao=req.descricao,
        ))
        self.db.commit()
        return self.saldo(req.cliente_id)

    def extrato(self, cliente_id: str) -> list[ExtratoItem]:
        rows = (
            self.db.query(TransacaoMilhas)
            .filter(TransacaoMilhas.cliente_id == cliente_id)
            .order_by(TransacaoMilhas.criado_em.desc())
            .limit(50)
            .all()
        )
        return [
            ExtratoItem(tipo=r.tipo, quantidade=r.quantidade, descricao=r.descricao, criado_em=r.criado_em)
            for r in rows
        ]

    def nivel(self, cliente_id: str) -> NivelResponse:
        c = self._conta(cliente_id)
        idx = NIVEIS.index(c.nivel) if c.nivel in NIVEIS else 0
        proximo = NIVEIS[idx + 1] if idx < len(NIVEIS) - 1 else None
        if proximo:
            limiar = LIMIARES[proximo]
            progresso = min(c.milhas_qualificadas / limiar * 100, 100)
        else:
            progresso = 100.0
        beneficios = {
            "Bronze": ["Acúmulo padrão"],
            "Prata": ["Prioridade check-in", "+25% milhas"],
            "Ouro": ["Sala VIP", "+50% milhas"],
            "Diamante": ["Concierge", "+100% milhas", "Fila prioritária"],
        }
        return NivelResponse(
            nivel=c.nivel, proximo_nivel=proximo, progresso_pct=round(progresso, 1),
            beneficios=beneficios.get(c.nivel, []),
        )

    def _atualizar_nivel(self, conta: ContaMilhas) -> None:
        for nivel in reversed(NIVEIS):
            if conta.milhas_qualificadas >= LIMIARES[nivel]:
                conta.nivel = nivel
                break
