"""Schemas do orquestrador."""
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class PipelineStartRequest(BaseModel):
    origem: str
    destino: str
    data_ida: datetime
    voo_id: Optional[str] = None
    preco_base: float = 450
    passageiros: list[dict] = []
    metodo_pagamento: str = "cartao"
    cartao: Optional[dict] = None
    nivel_fidelidade: Optional[str] = None
    cliente_id: str = "cliente-001"


class EtapaStatus(BaseModel):
    etapa: str
    agente: str
    status: str


class PipelineStatusResponse(BaseModel):
    session_id: str
    trace_id: str
    status: str
    etapas: list[EtapaStatus]
    resultado: Optional[dict[str, Any]] = None
