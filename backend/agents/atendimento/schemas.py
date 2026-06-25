"""Schemas de atendimento."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    mensagem: str
    canal: str = "chat"
    pnr: Optional[str] = None
    idioma: Optional[str] = None


class ChatResponse(BaseModel):
    protocolo: str
    resposta: str
    sentimento: str
    escalado: bool = False


class EscalarRequest(BaseModel):
    protocolo: str
    motivo: str = "solicitacao_cliente"
