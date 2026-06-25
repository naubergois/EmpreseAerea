"""Schemas de marketing."""
from typing import Any, Optional

from pydantic import BaseModel


class CampanhaRequest(BaseModel):
    nome: str
    tipo: str = "email"
    segmento: str = "todos"


class SegmentoRequest(BaseModel):
    nome: str
    criterio: dict[str, Any] = {}


class MetricasResponse(BaseModel):
    impressoes: int
    cliques: int
    conversoes: int
    taxa_conversao: float
    roi: float


class OfertaResponse(BaseModel):
    cliente_id: str
    ofertas: list[dict]
