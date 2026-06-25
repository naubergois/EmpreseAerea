"""Models de reserva."""
import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class StatusReserva(enum.Enum):
    PENDENTE = "pendente_pagamento"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    EXPIRADA = "expirada"


class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True)
    pnr = Column(String(6), unique=True, index=True, nullable=False)
    status = Column(Enum(StatusReserva), default=StatusReserva.PENDENTE)
    voo_ida = Column(String(50), nullable=False)
    voo_volta = Column(String(50), nullable=True)
    data_ida = Column(DateTime, nullable=False)
    data_volta = Column(DateTime, nullable=True)
    origem = Column(String(3), nullable=False)
    destino = Column(String(3), nullable=False)
    classe = Column(String(20), default="economica")
    valor_total = Column(Float, default=0)
    criado_em = Column(DateTime, default=datetime.utcnow)
    expira_em = Column(DateTime, nullable=False)

    passageiros = relationship("Passageiro", back_populates="reserva")


class Passageiro(Base):
    __tablename__ = "passageiros"

    id = Column(Integer, primary_key=True)
    reserva_id = Column(Integer, ForeignKey("reservas.id"))
    nome = Column(String(100), nullable=False)
    sobrenome = Column(String(100), nullable=False)
    cpf = Column(String(14), nullable=True)
    passaporte = Column(String(20), nullable=True)
    passaporte_validade = Column(DateTime, nullable=True)
    data_nascimento = Column(DateTime, nullable=False)
    tipo = Column(String(10), default="ADT")
    assento = Column(String(4), nullable=True)
    email = Column(String(100), nullable=True)
    telefone = Column(String(20), nullable=True)
    adulto_vinculado_id = Column(Integer, nullable=True)

    reserva = relationship("Reserva", back_populates="passageiros")
