"""Schemas de reserva."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator


class PassageiroInput(BaseModel):
    nome: str
    sobrenome: str
    cpf: Optional[str] = None
    passaporte: Optional[str] = None
    passaporte_validade: Optional[datetime] = None
    data_nascimento: datetime
    tipo: str = "ADT"
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    adulto_vinculado_id: Optional[int] = None

    @field_validator("nome", "sobrenome")
    @classmethod
    def nome_nao_vazio(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Nome não pode ser vazio")
        return v.strip()


class ReservaRequest(BaseModel):
    voo_ida: str
    voo_volta: Optional[str] = None
    data_ida: datetime
    data_volta: Optional[datetime] = None
    origem: str
    destino: str
    classe: str = "economica"
    valor_total: float = 0
    passageiros: list[PassageiroInput]


class PassageiroResponse(PassageiroInput):
    id: Optional[int] = None
    assento: Optional[str] = None


class ReservaResponse(BaseModel):
    pnr: str
    status: str
    voo_ida: str
    origem: str
    destino: str
    valor_total: float
    expira_em: datetime
    passageiros: list[PassageiroResponse]

    class Config:
        from_attributes = True


class AssentoRequest(BaseModel):
    passageiro_id: int
    assento: str
