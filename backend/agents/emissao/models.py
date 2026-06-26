"""Models de emissão."""
import enum

from sqlalchemy import Column, DateTime, Enum, Integer, String, Text

from database import Base
from shared.datetime_utils import utc_now


class StatusBilhete(enum.Enum):
    EMITIDO = "emitido"
    VOID = "void"
    REEMITIDO = "reemitido"


class Bilhete(Base):
    __tablename__ = "bilhetes"

    id = Column(Integer, primary_key=True)
    numero = Column(String(20), unique=True, index=True)
    pnr = Column(String(6), index=True)
    status = Column(Enum(StatusBilhete), default=StatusBilhete.EMITIDO)
    passageiro_nome = Column(String(200))
    itinerario_json = Column(Text)
    emitido_em = Column(DateTime, default=utc_now)
