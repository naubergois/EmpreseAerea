"""Schemas de pagamento."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PagamentoCartaoRequest(BaseModel):
    pnr: str
    valor: float
    numero_cartao: str
    nome_titular: str
    validade: str
    cvv: str
    parcelas: int = 1


class PagamentoPixRequest(BaseModel):
    pnr: str
    valor: float


class PagamentoBoletoRequest(BaseModel):
    pnr: str
    valor: float


class PagamentoSplitRequest(BaseModel):
    pnr: str
    valor_total: float
    milhas: int
    cliente_id: str


class PagamentoResponse(BaseModel):
    id: str
    pnr: str
    status: str
    metodo: str
    valor: float
    pix_qr: Optional[str] = None
    pix_copia_cola: Optional[str] = None
    boleto_codigo: Optional[str] = None
    expira_em: Optional[datetime] = None


class ReembolsoRequest(BaseModel):
    valor: Optional[float] = None
    motivo: str = "cancelamento"
