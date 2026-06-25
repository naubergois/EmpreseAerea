"""Controller de busca de voos."""
from datetime import datetime

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from database import get_db

from .schemas import BuscaRequest, BuscaResponse
from .service import BuscaService

router = APIRouter(prefix="/api/voos", tags=["Busca de Voos"])


@router.get("/buscar", response_model=BuscaResponse)
def buscar_voos(
    origem: str = Query(...),
    destino: str = Query(...),
    data_ida: datetime = Query(...),
    data_volta: datetime | None = None,
    classe: str = "economica",
    adultos: int = 1,
    criancas: int = 0,
    bebes: int = 0,
    somente_ida: bool = True,
    flex_dias: int = 0,
    cadeirante: bool = False,
    ordenar_por: str = "relevancia",
    max_escalas: int | None = None,
    companhia: str | None = None,
    preco_max: float | None = None,
    response: Response = None,
    db: Session = Depends(get_db),
):
    req = BuscaRequest(
        origem=origem, destino=destino, data_ida=data_ida, data_volta=data_volta,
        classe=classe, adultos=adultos, criancas=criancas, bebes=bebes,
        somente_ida=somente_ida, flex_dias=flex_dias, cadeirante=cadeirante,
        ordenar_por=ordenar_por, max_escalas=max_escalas, companhia=companhia,
        preco_max=preco_max,
    )
    result = BuscaService(db).buscar(req)
    if response:
        response.headers["X-Cache"] = result.cache
    return result


@router.get("/aeroportos")
def aeroportos(q: str = "", db: Session = Depends(get_db)):
    return BuscaService(db).listar_aeroportos(q)


@router.get("/{voo_id}/assentos")
def assentos(voo_id: str, db: Session = Depends(get_db)):
    return BuscaService(db).mapa_assentos(voo_id)
