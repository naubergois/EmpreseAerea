"""Controller de marketing."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from .schemas import CampanhaRequest, MetricasResponse, OfertaResponse, SegmentoRequest
from .service import MarketingService

router = APIRouter(prefix="/api/marketing", tags=["Marketing"])


@router.post("/campanha")
def criar_campanha(request: CampanhaRequest, db: Session = Depends(get_db)):
    return MarketingService(db).criar_campanha(request)


@router.post("/segmento")
def criar_segmento(request: SegmentoRequest, db: Session = Depends(get_db)):
    return MarketingService(db).criar_segmento(request)


@router.get("/metricas", response_model=MetricasResponse)
def metricas(db: Session = Depends(get_db)):
    return MarketingService(db).metricas()


@router.get("/ofertas/{cliente_id}", response_model=OfertaResponse)
def ofertas(cliente_id: str, db: Session = Depends(get_db)):
    return MarketingService(db).ofertas(cliente_id)
