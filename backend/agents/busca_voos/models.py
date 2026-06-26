"""Models do agente de busca."""
from sqlalchemy import Column, DateTime, Integer, String, Text

from database import Base
from shared.datetime_utils import utc_now


class BuscaCache(Base):
    __tablename__ = "busca_cache"

    id = Column(Integer, primary_key=True)
    chave = Column(String(200), unique=True, index=True)
    resultado_json = Column(Text)
    criado_em = Column(DateTime, default=utc_now)
