"""Controller do Agente de Qualidade — expõe os dados do SonarQube."""
from fastapi import APIRouter, HTTPException

from .schemas import (
    IssueResumo,
    MetricasResponse,
    PlanoMelhoriasResponse,
    StatusResponse,
)
from .service import QualidadeService
from .sonar_client import SonarUnavailableError

router = APIRouter(prefix="/api/qualidade", tags=["Qualidade / SonarQube"])


def _service() -> QualidadeService:
    return QualidadeService()


@router.get("/status", response_model=StatusResponse)
def status():
    """Visão geral: quality gate, métricas e contagem de melhorias."""
    try:
        return _service().status()
    except SonarUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.get("/metricas", response_model=MetricasResponse)
def metricas():
    """Métricas-chave do projeto (bugs, vulnerabilidades, cobertura, etc.)."""
    try:
        return _service().metricas()
    except SonarUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.get("/issues", response_model=list[IssueResumo])
def issues():
    """Lista todas as issues abertas detectadas pelo SonarQube."""
    try:
        return _service().listar_issues()
    except SonarUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.get("/melhorias", response_model=PlanoMelhoriasResponse)
def melhorias():
    """Plano de melhorias priorizado, agrupado por regra do SonarQube."""
    try:
        return _service().plano_melhorias()
    except SonarUnavailableError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
