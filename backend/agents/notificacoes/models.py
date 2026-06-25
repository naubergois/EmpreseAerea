"""Models de notificações."""
import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Integer, String, Text

from database import Base


class StatusNotificacao(enum.Enum):
    PENDENTE = "pendente"
    ENVIADA = "enviada"
    ENTREGUE = "entregue"
    FALHA = "falha"


class Notificacao(Base):
    __tablename__ = "notificacoes"

    id = Column(Integer, primary_key=True)
    tipo = Column(String(50))
    canal = Column(String(20), default="email")
    destinatario = Column(String(200))
    conteudo = Column(Text)
    status = Column(Enum(StatusNotificacao), default=StatusNotificacao.PENDENTE)
    criado_em = Column(DateTime, default=datetime.utcnow)
