"""Models de precificação."""
from sqlalchemy import Column, DateTime, Float, Integer, String, Text

from database import Base
from shared.datetime_utils import utc_now


class Cotacao(Base):
    __tablename__ = "cotacoes"

    id = Column(String(50), primary_key=True)
    voo_id = Column(String(50))
    valor_base = Column(Float)
    valor_total = Column(Float)
    breakdown_json = Column(Text)
    cupom = Column(String(50), nullable=True)
    criado_em = Column(DateTime, default=utc_now)
    expira_em = Column(DateTime)


class Cupom(Base):
    __tablename__ = "cupons"

    id = Column(Integer, primary_key=True)
    codigo = Column(String(50), unique=True, index=True)
    tipo = Column(String(20))
    valor = Column(Float)
    uso_max = Column(Integer, default=100)
    uso_atual = Column(Integer, default=0)
    valido_ate = Column(DateTime, nullable=True)
    rota_origem = Column(String(3), nullable=True)
    rota_destino = Column(String(3), nullable=True)
    nivel_minimo = Column(String(20), nullable=True)
    valor_minimo = Column(Float, default=0)
