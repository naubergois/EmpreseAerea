"""Models de pagamento."""
import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Float, Integer, String, Text

from database import Base


class StatusPagamento(enum.Enum):
    PENDENTE = "pendente"
    APROVADO = "aprovado"
    RECUSADO = "recusado"
    REEMBOLSADO = "reembolsado"
    EXPIRADO = "expirado"


class MetodoPagamento(enum.Enum):
    CARTAO = "cartao"
    PIX = "pix"
    BOLETO = "boleto"
    SPLIT = "split"


class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(String(50), primary_key=True)
    pnr = Column(String(6), index=True)
    metodo = Column(Enum(MetodoPagamento))
    status = Column(Enum(StatusPagamento), default=StatusPagamento.PENDENTE)
    valor = Column(Float, nullable=False)
    milhas_usadas = Column(Integer, default=0)
    parcelas = Column(Integer, default=1)
    pix_qr = Column(Text, nullable=True)
    pix_copia_cola = Column(Text, nullable=True)
    boleto_codigo = Column(String(100), nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    expira_em = Column(DateTime, nullable=True)
