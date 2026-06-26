"""Testes do Agente de Qualidade (SonarQube) com cliente fake."""
from agents.qualidade.service import QualidadeService
from shared.datetime_utils import utc_now


class FakeSonarClient:
    """Dublê do SonarClient — devolve respostas fixas, sem rede."""

    project_key = "skyagent"

    def search_issues(self, *args, **kwargs):
        return [
            {
                "key": "i1",
                "rule": "python:S6903",
                "type": "CODE_SMELL",
                "severity": "CRITICAL",
                "component": "skyagent:backend/agents/x/service.py",
                "line": 10,
                "message": "Don't use datetime.utcnow",
                "effort": "5min",
                "tags": ["cwe"],
            },
            {
                "key": "i2",
                "rule": "python:S6903",
                "type": "CODE_SMELL",
                "severity": "CRITICAL",
                "component": "skyagent:backend/agents/y/service.py",
                "line": 20,
                "message": "Don't use datetime.utcnow",
            },
            {
                "key": "i3",
                "rule": "secrets:S6702",
                "type": "VULNERABILITY",
                "severity": "BLOCKER",
                "component": "skyagent:backend/.env",
                "line": 1,
                "message": "Revoke this token",
            },
        ]

    def measures(self, *args, **kwargs):
        return {
            "bugs": "2",
            "vulnerabilities": "1",
            "code_smells": "10",
            "coverage": "76.5",
            "duplicated_lines_density": "0.0",
            "ncloc": "6400",
            "sqale_index": "120",
            "reliability_rating": "2.0",
            "security_rating": "5.0",
            "sqale_rating": "1.0",
        }

    def quality_gate(self, *args, **kwargs):
        return {"status": "OK"}


def _service():
    return QualidadeService(client=FakeSonarClient())


def test_listar_issues_normaliza_componente():
    issues = _service().listar_issues()
    assert len(issues) == 3
    primeira = issues[0]
    assert primeira.arquivo == "backend/agents/x/service.py"
    assert primeira.tipo == "CODE_SMELL"


def test_metricas_converte_ratings_e_numeros():
    m = _service().metricas()
    assert m.bugs == 2
    assert m.vulnerabilidades == 1
    assert m.cobertura == 76.5
    assert m.nota_confiabilidade == "B"  # 2.0 -> B
    assert m.nota_seguranca == "E"       # 5.0 -> E
    assert m.nota_manutenibilidade == "A"  # 1.0 -> A


def test_plano_melhorias_agrupa_por_regra_e_prioriza():
    plano = _service().plano_melhorias()
    # 2 regras distintas: S6903 (2 ocorrências) e S6702 (1)
    assert plano.total == 2
    # A vulnerability BLOCKER deve vir primeiro (prioridade mais alta).
    primeira = plano.melhorias[0]
    assert primeira.regra == "secrets:S6702"
    assert primeira.prioridade == 1
    assert primeira.tipo == "VULNERABILITY"
    # O grupo de smell agrega as 2 ocorrências e lista os 2 arquivos.
    smell = plano.melhorias[1]
    assert smell.ocorrencias == 2
    assert len(smell.arquivos) == 2


def test_status_resume_quality_gate_e_contagens():
    status = _service().status()
    assert status.quality_gate == "OK"
    assert status.total_issues == 3
    assert status.total_melhorias == 2


def test_utc_now_eh_naive():
    agora = utc_now()
    assert agora.tzinfo is None
