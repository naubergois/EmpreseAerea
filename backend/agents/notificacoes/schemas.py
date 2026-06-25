"""Schemas de notificações."""
from typing import Any, Optional

from pydantic import BaseModel, EmailStr


class NotificacaoRequest(BaseModel):
    tipo: str
    destinatario: str
    canal: str = "email"
    dados: dict[str, Any] = {}


class NotificacaoResponse(BaseModel):
    id: int
    tipo: str
    canal: str
    status: str


class PreferenciasRequest(BaseModel):
    cliente_id: str
    email: bool = True
    sms: bool = True
    push: bool = True
    whatsapp: bool = False
