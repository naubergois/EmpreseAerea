"""Schemas do agente de busca."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BuscaRequest(BaseModel):
    origem: str
    destino: str
    data_ida: datetime
    data_volta: Optional[datetime] = None
    classe: str = "economica"
    adultos: int = Field(default=1, ge=1)
    criancas: int = Field(default=0, ge=0)
    bebes: int = Field(default=0, ge=0)
    somente_ida: bool = True
    flex_dias: int = Field(default=0, ge=0, le=7)
    cadeirante: bool = False
    ordenar_por: str = "relevancia"
    max_escalas: Optional[int] = None
    companhia: Optional[str] = None
    preco_max: Optional[float] = None
    preco_min: Optional[float] = None


class CompanhiaInfo(BaseModel):
    codigo: str
    nome: str
    logo: str = ""


class VooResponse(BaseModel):
    id: str
    numero: str
    companhia: CompanhiaInfo
    origem: str
    destino: str
    partida: str
    chegada: str
    duracao_minutos: int
    escalas: int
    classe: str
    preco: float
    preco_por_passageiro: float
    preco_total: float
    bagagem_inclusa: bool
    bagagem_mao_kg: int = 10
    bagagem_despacho_kg: int = 0
    alta_demanda: bool = False
    special_assistance_required: bool = False


class BuscaResponse(BaseModel):
    voos: list[VooResponse]
    total: int
    sugestoes_datas: list[str] = []
    sugestoes_rotas: list[str] = []
    melhor_tarifa_data: Optional[str] = None
    menor_preco: Optional[float] = None
    cache: str = "MISS"
