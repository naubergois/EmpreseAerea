"""Schemas do Agente de Qualidade."""
from __future__ import annotations

from pydantic import BaseModel


class IssueResumo(BaseModel):
    """Uma issue do SonarQube normalizada."""

    chave: str
    regra: str
    tipo: str           # BUG | VULNERABILITY | CODE_SMELL
    severidade: str     # BLOCKER | CRITICAL | MAJOR | MINOR | INFO
    arquivo: str
    linha: int | None = None
    mensagem: str
    esforco: str | None = None
    tags: list[str] = []


class Melhoria(BaseModel):
    """Item acionável do plano de melhorias (issues agrupadas por regra)."""

    regra: str
    tipo: str
    severidade: str
    prioridade: int          # 1 (mais alta) .. 5 (mais baixa)
    titulo: str
    ocorrencias: int
    arquivos: list[str]
    acao_sugerida: str
    exemplos: list[IssueResumo]


class MetricasResponse(BaseModel):
    """Métricas-chave do projeto."""

    bugs: int = 0
    vulnerabilidades: int = 0
    code_smells: int = 0
    security_hotspots: int = 0
    cobertura: float = 0.0
    duplicacao: float = 0.0
    linhas_codigo: int = 0
    divida_tecnica_min: int = 0
    nota_confiabilidade: str = "-"
    nota_seguranca: str = "-"
    nota_manutenibilidade: str = "-"


class StatusResponse(BaseModel):
    """Visão geral da qualidade do projeto."""

    projeto: str
    quality_gate: str               # OK | ERROR | NONE
    metricas: MetricasResponse
    total_issues: int
    total_melhorias: int


class PlanoMelhoriasResponse(BaseModel):
    """Plano de melhorias priorizado."""

    projeto: str
    gerado_em: str
    total: int
    melhorias: list[Melhoria]
