"""Schemas de fidelidade."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AcumularRequest(BaseModel):
    cliente_id: str
    pnr: str
    valor: float
    nivel: str = "Bronze"


class ResgatarRequest(BaseModel):
    cliente_id: str
    milhas: int
    descricao: str = "resgate_passagem"


class MilhasResponse(BaseModel):
    cliente_id: str
    saldo: int
    nivel: str
    milhas_qualificadas: int


class ExtratoItem(BaseModel):
    tipo: str
    quantidade: int
    descricao: str
    criado_em: datetime


class NivelResponse(BaseModel):
    nivel: str
    proximo_nivel: Optional[str] = None
    progresso_pct: float
    beneficios: list[str]
