"""Service de marketing."""
from sqlalchemy.orm import Session

from event_bus import Events, event_bus

from .models import Campanha, Segmento
from .schemas import CampanhaRequest, MetricasResponse, OfertaResponse, SegmentoRequest


class MarketingService:
    def __init__(self, db: Session):
        self.db = db

    def criar_campanha(self, req: CampanhaRequest) -> dict:
        camp = Campanha(nome=req.nome, tipo=req.tipo, segmento=req.segmento)
        self.db.add(camp)
        self.db.commit()
        self.db.refresh(camp)
        event_bus.publish(Events.CAMPANHA_ENVIADA, {"id": camp.id, "nome": req.nome})
        return {"id": camp.id, "nome": camp.nome, "status": camp.status}

    def criar_segmento(self, req: SegmentoRequest) -> dict:
        import json
        seg = Segmento(nome=req.nome, criterio_json=json.dumps(req.criterio), total_clientes=100)
        self.db.add(seg)
        self.db.commit()
        return {"id": seg.id, "nome": seg.nome, "total_clientes": seg.total_clientes}

    def metricas(self) -> MetricasResponse:
        return MetricasResponse(
            impressoes=10000, cliques=1500, conversoes=150,
            taxa_conversao=1.5, roi=2.3,
        )

    def ofertas(self, cliente_id: str) -> OfertaResponse:
        return OfertaResponse(cliente_id=cliente_id, ofertas=[
            {"destino": "MIA", "desconto": 15, "valido_ate": "2026-12-31"},
            {"destino": "LIS", "desconto": 20, "valido_ate": "2026-09-30"},
        ])
