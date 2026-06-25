"""Schemas de precificação."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PrecoRequest(BaseModel):
    voo_id: str
    preco_base: float
    adultos: int = 1
    criancas: int = 0
    bebes: int = 0
    cupom: Optional[str] = None
    nivel_fidelidade: Optional[str] = None
    canal: str = "web"


class BreakdownItem(BaseModel):
    descricao: str
    valor: float


class PrecoResponse(BaseModel):
    cotacao_id: str
    valor_base: float
    valor_total: float
    breakdown: list[BreakdownItem]
    expira_em: datetime
    desconto_aplicado: float = 0


class CupomValidacaoRequest(BaseModel):
    codigo: str
    valor_compra: float
    origem: Optional[str] = None
    destino: Optional[str] = None
    nivel_fidelidade: Optional[str] = None


class CupomValidacaoResponse(BaseModel):
    valido: bool
    desconto: float = 0
    mensagem: str = ""
    codigo_erro: Optional[str] = None
