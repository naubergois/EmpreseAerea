"""Serviço do Agente de Qualidade.

Consome o SonarQube via :class:`SonarClient`, normaliza os achados e produz
um plano de melhorias priorizado, consumível por API e por CLI.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone

from .schemas import (
    IssueResumo,
    Melhoria,
    MetricasResponse,
    PlanoMelhoriasResponse,
    StatusResponse,
)
from .sonar_client import SonarClient

# Peso de severidade -> prioridade base (1 = mais urgente).
_SEVERIDADE_PRIORIDADE = {
    "BLOCKER": 1,
    "CRITICAL": 2,
    "MAJOR": 3,
    "MINOR": 4,
    "INFO": 5,
}

# Tipos que representam risco real recebem um "boost" de prioridade.
_TIPO_BOOST = {"BUG", "VULNERABILITY"}

# Ratings numéricos do Sonar (1=A .. 5=E) -> letra.
_RATING_LETRA = {"1.0": "A", "2.0": "B", "3.0": "C", "4.0": "D", "5.0": "E"}

# Ações sugeridas por prefixo de regra/linguagem. Fallback usa a mensagem.
_ACOES_POR_TIPO = {
    "VULNERABILITY": "Corrigir a vulnerabilidade: validar/escapar entradas e remover o vetor de ataque.",
    "BUG": "Corrigir o bug que pode causar comportamento incorreto em produção.",
    "CODE_SMELL": "Refatorar para melhorar manutenibilidade e reduzir dívida técnica.",
}


def _rating_letra(valor: str) -> str:
    return _RATING_LETRA.get(valor, "-")


class QualidadeService:
    """Orquestra a coleta e o processamento dos dados do SonarQube."""

    def __init__(self, client: SonarClient | None = None) -> None:
        self.client = client or SonarClient()

    # -- Normalização --------------------------------------------------------
    def _normalizar_issue(self, raw: dict) -> IssueResumo:
        componente = raw.get("component", "")
        # componente vem como "projeto:caminho/arquivo.py"
        arquivo = componente.split(":", 1)[1] if ":" in componente else componente
        return IssueResumo(
            chave=raw.get("key", ""),
            regra=raw.get("rule", ""),
            tipo=raw.get("type", "CODE_SMELL"),
            severidade=raw.get("severity", "INFO"),
            arquivo=arquivo,
            linha=raw.get("line"),
            mensagem=raw.get("message", ""),
            esforco=raw.get("effort") or raw.get("debt"),
            tags=raw.get("tags", []),
        )

    def listar_issues(self) -> list[IssueResumo]:
        """Retorna todas as issues abertas, normalizadas."""
        return [self._normalizar_issue(i) for i in self.client.search_issues()]

    # -- Métricas ------------------------------------------------------------
    def metricas(self) -> MetricasResponse:
        m = self.client.measures()

        def _i(chave: str) -> int:
            try:
                return int(float(m.get(chave, 0)))
            except (TypeError, ValueError):
                return 0

        def _f(chave: str) -> float:
            try:
                return round(float(m.get(chave, 0)), 1)
            except (TypeError, ValueError):
                return 0.0

        return MetricasResponse(
            bugs=_i("bugs"),
            vulnerabilidades=_i("vulnerabilities"),
            code_smells=_i("code_smells"),
            security_hotspots=_i("security_hotspots"),
            cobertura=_f("coverage"),
            duplicacao=_f("duplicated_lines_density"),
            linhas_codigo=_i("ncloc"),
            divida_tecnica_min=_i("sqale_index"),
            nota_confiabilidade=_rating_letra(m.get("reliability_rating", "")),
            nota_seguranca=_rating_letra(m.get("security_rating", "")),
            nota_manutenibilidade=_rating_letra(m.get("sqale_rating", "")),
        )

    # -- Status --------------------------------------------------------------
    def status(self) -> StatusResponse:
        gate = self.client.quality_gate()
        issues = self.listar_issues()
        melhorias = self._agrupar_melhorias(issues)
        return StatusResponse(
            projeto=self.client.project_key,
            quality_gate=gate.get("status", "NONE"),
            metricas=self.metricas(),
            total_issues=len(issues),
            total_melhorias=len(melhorias),
        )

    # -- Plano de melhorias --------------------------------------------------
    def _prioridade(self, severidade: str, tipo: str) -> int:
        base = _SEVERIDADE_PRIORIDADE.get(severidade, 5)
        if tipo in _TIPO_BOOST and base > 1:
            base -= 1  # risco real sobe um nível de prioridade
        return base

    def _acao_sugerida(self, tipo: str, mensagem: str) -> str:
        base = _ACOES_POR_TIPO.get(tipo, _ACOES_POR_TIPO["CODE_SMELL"])
        return f"{base} Detalhe: {mensagem}"

    def _agrupar_melhorias(self, issues: list[IssueResumo]) -> list[Melhoria]:
        grupos: dict[str, list[IssueResumo]] = defaultdict(list)
        for issue in issues:
            grupos[issue.regra].append(issue)

        melhorias: list[Melhoria] = []
        for regra, lista in grupos.items():
            # representante = issue de maior severidade no grupo
            rep = min(lista, key=lambda i: _SEVERIDADE_PRIORIDADE.get(i.severidade, 5))
            arquivos = sorted({i.arquivo for i in lista})
            melhorias.append(
                Melhoria(
                    regra=regra,
                    tipo=rep.tipo,
                    severidade=rep.severidade,
                    prioridade=self._prioridade(rep.severidade, rep.tipo),
                    titulo=rep.mensagem,
                    ocorrencias=len(lista),
                    arquivos=arquivos,
                    acao_sugerida=self._acao_sugerida(rep.tipo, rep.mensagem),
                    exemplos=lista[:5],
                )
            )

        # Ordena por prioridade, depois por nº de ocorrências (desc).
        melhorias.sort(key=lambda x: (x.prioridade, -x.ocorrencias))
        return melhorias

    def plano_melhorias(self) -> PlanoMelhoriasResponse:
        issues = self.listar_issues()
        melhorias = self._agrupar_melhorias(issues)
        return PlanoMelhoriasResponse(
            projeto=self.client.project_key,
            gerado_em=datetime.now(timezone.utc).isoformat(),
            total=len(melhorias),
            melhorias=melhorias,
        )
