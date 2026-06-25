"""Models de atendimento."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from database import Base


class Atendimento(Base):
    __tablename__ = "atendimentos"

    id = Column(Integer, primary_key=True)
    protocolo = Column(String(30), unique=True, index=True)
    canal = Column(String(20))
    mensagem = Column(Text)
    resposta = Column(Text, nullable=True)
    sentimento = Column(String(20), default="neutro")
    status = Column(String(20), default="aberto")
    idioma = Column(String(5), default="pt")
    criado_em = Column(DateTime, default=datetime.utcnow)
