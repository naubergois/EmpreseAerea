"""Models de marketing."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text

from database import Base


class Campanha(Base):
    __tablename__ = "campanhas"

    id = Column(Integer, primary_key=True)
    nome = Column(String(200))
    tipo = Column(String(50))
    segmento = Column(String(100))
    status = Column(String(20), default="ativa")
    criado_em = Column(DateTime, default=datetime.utcnow)


class Segmento(Base):
    __tablename__ = "segmentos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    criterio_json = Column(Text)
    total_clientes = Column(Integer, default=0)
