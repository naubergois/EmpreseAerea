"""Models de fidelidade."""
from sqlalchemy import Column, DateTime, Float, Integer, String

from database import Base
from shared.datetime_utils import utc_now


class ContaMilhas(Base):
    __tablename__ = "contas_milhas"

    id = Column(Integer, primary_key=True)
    cliente_id = Column(String(50), unique=True, index=True)
    saldo = Column(Integer, default=0)
    nivel = Column(String(20), default="Bronze")
    milhas_qualificadas = Column(Integer, default=0)
    atualizado_em = Column(DateTime, default=utc_now)


class TransacaoMilhas(Base):
    __tablename__ = "transacoes_milhas"

    id = Column(Integer, primary_key=True)
    cliente_id = Column(String(50), index=True)
    tipo = Column(String(20))
    quantidade = Column(Integer)
    descricao = Column(String(200))
    criado_em = Column(DateTime, default=utc_now)
