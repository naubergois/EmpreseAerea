"""Models do orquestrador."""
import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Integer, String, Text

from database import Base


class PipelineStatus(enum.Enum):
    INICIADO = "iniciado"
    EM_PROGRESSO = "em_progresso"
    SUCESSO = "sucesso"
    FALHA = "falha"
    ROLLBACK = "rollback"


class SessaoPipeline(Base):
    __tablename__ = "sessoes_pipeline"

    id = Column(String(50), primary_key=True)
    trace_id = Column(String(50), unique=True, index=True)
    status = Column(Enum(PipelineStatus), default=PipelineStatus.INICIADO)
    intencao = Column(String(50), default="compra")
    estado_json = Column(Text, default="{}")
    nivel_fidelidade = Column(String(20), nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow)
    expira_em = Column(DateTime)


class EtapaAuditoria(Base):
    __tablename__ = "etapas_auditoria"

    id = Column(Integer, primary_key=True)
    sessao_id = Column(String(50), index=True)
    etapa = Column(String(50))
    agente = Column(String(10))
    status = Column(String(20))
    criado_em = Column(DateTime, default=datetime.utcnow)
