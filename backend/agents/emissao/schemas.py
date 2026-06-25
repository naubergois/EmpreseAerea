"""Schemas de emissão."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EmitirRequest(BaseModel):
    pnr: str
    pagamento_id: str


class BilheteResponse(BaseModel):
    numero: str
    pnr: str
    status: str
    passageiro_nome: str
    emitido_em: datetime


class BoardingPassResponse(BaseModel):
    numero_bilhete: str
    qr_code: str
    portao: str = "A12"
    grupo_embarque: str = "3"
