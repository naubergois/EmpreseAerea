"""Serviço de QA: executa a suíte BDD (behave) e estrutura os resultados.

Roda o behave como subprocesso gerando um relatório JSON, faz o parsing e
devolve, para cada cenário, o "motivo" (descrição da funcionalidade) e o
status (passou / falhou / pendente).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone

# Diretórios base ------------------------------------------------------------
_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_REPO_ROOT = os.path.dirname(_BACKEND_DIR)
_FEATURES_DIR = os.path.join(_REPO_ROOT, "features")

# Mapeia o status interno do behave para um status amigável.
_STATUS_MAP = {
    "passed": "passed",
    "failed": "failed",
    "skipped": "skipped",
    "untested": "pending",
    "undefined": "pending",
}

# Cache em memória do último relatório gerado.
_cache: dict | None = None
_lock = threading.Lock()


def _behave_executable() -> list[str]:
    """Retorna o comando para invocar o behave, preferindo o venv do backend."""
    venv_behave = os.path.join(_BACKEND_DIR, "venv", "bin", "behave")
    if os.path.exists(venv_behave):
        return [venv_behave]
    return [sys.executable, "-m", "behave"]


def _motivo_from_description(description: list[str] | None) -> str:
    """Junta as linhas de descrição da funcionalidade no 'motivo' do teste."""
    if not description:
        return ""
    return " ".join(linha.strip() for linha in description if linha and linha.strip())


def _scenario_reason(scenario: dict) -> str:
    """Determina o motivo da falha/pendência a partir dos steps do cenário."""
    for step in scenario.get("steps", []):
        result = step.get("result") or {}
        status = result.get("status")
        nome = f"{step.get('keyword', '').strip()} {step.get('name', '').strip()}".strip()
        if status == "failed":
            erro = result.get("error_message")
            if isinstance(erro, list):
                erro = " ".join(erro)
            erro = (erro or "").strip().splitlines()
            detalhe = erro[-1] if erro else "Falha na asserção"
            return f"Falhou no passo: «{nome}» — {detalhe}"
        if status in ("undefined", "untested"):
            return f"Passo não implementado: «{nome}»"
        if status == "skipped":
            return f"Passo ignorado: «{nome}»"
    return ""


# Prioridade de ordenação: falhas primeiro, depois pendentes, etc.
_STATUS_PRIORITY = {"failed": 0, "pending": 1, "skipped": 2, "passed": 3}


def _parse_report(raw: list[dict]) -> dict:
    """Transforma o JSON cru do behave numa estrutura amigável para a UI."""
    features = []
    totals = {"passed": 0, "failed": 0, "pending": 0, "skipped": 0, "total": 0}

    for feature in raw:
        loc = feature.get("location", "") or ""
        arquivo = loc.split(":")[0] if loc else ""
        # Caminho relativo a features/ para exibição amigável.
        rel = os.path.relpath(os.path.join(_FEATURES_DIR, arquivo), _FEATURES_DIR) if arquivo and not os.path.isabs(arquivo) else arquivo
        suite = rel.split(os.sep)[0] if rel and os.sep in rel else (rel or "geral")

        cenarios = []
        for el in feature.get("elements", []):
            if el.get("type") != "scenario":
                continue
            status = _STATUS_MAP.get(el.get("status"), "pending")
            passos = [
                {
                    "texto": f"{s.get('keyword', '').strip()} {s.get('name', '').strip()}".strip(),
                    "status": _STATUS_MAP.get((s.get("result") or {}).get("status"), "pending"),
                }
                for s in el.get("steps", [])
            ]
            cenarios.append(
                {
                    "nome": el.get("name", ""),
                    "status": status,
                    "motivo_falha": _scenario_reason(el) if status != "passed" else "",
                    "passos": passos,
                }
            )
            totals[status] = totals.get(status, 0) + 1
            totals["total"] += 1

        # Prioriza cenários que falharam dentro de cada funcionalidade.
        cenarios.sort(key=lambda c: _STATUS_PRIORITY.get(c["status"], 9))
        n_falhas = sum(1 for c in cenarios if c["status"] == "failed")

        features.append(
            {
                "nome": feature.get("name", ""),
                "motivo": _motivo_from_description(feature.get("description")),
                "suite": suite,
                "arquivo": rel,
                "status": _STATUS_MAP.get(feature.get("status"), "pending"),
                "falhas": n_falhas,
                "cenarios": cenarios,
            }
        )

    # Prioriza funcionalidades com falhas (mais falhas primeiro), depois nome.
    features.sort(
        key=lambda f: (
            _STATUS_PRIORITY.get(f["status"], 9),
            -f["falhas"],
            f["suite"],
            f["nome"],
        )
    )
    return {"features": features, "resumo": totals}


def run_bdd() -> dict:
    """Executa a suíte BDD via behave e devolve o relatório estruturado."""
    global _cache
    with _lock:
        inicio = time.perf_counter()
        with tempfile.NamedTemporaryFile(
            mode="r", suffix=".json", delete=False, encoding="utf-8"
        ) as tmp:
            report_path = tmp.name

        cmd = _behave_executable() + ["-f", "json", "-o", report_path, "--no-summary"]
        try:
            subprocess.run(
                cmd,
                cwd=_FEATURES_DIR,
                capture_output=True,
                text=True,
                timeout=300,
                check=False,
            )
            with open(report_path, encoding="utf-8") as fh:
                raw = json.load(fh)
        except FileNotFoundError as exc:
            raise RuntimeError(
                "behave não encontrado. Instale as dependências do backend."
            ) from exc
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("A execução dos testes BDD excedeu o tempo limite.") from exc
        finally:
            if os.path.exists(report_path):
                os.remove(report_path)

        resultado = _parse_report(raw)
        resultado["executado_em"] = datetime.now(timezone.utc).isoformat()
        resultado["duracao_segundos"] = round(time.perf_counter() - inicio, 2)
        _cache = resultado
        return resultado


def get_bdd(force: bool = False) -> dict:
    """Retorna o último relatório em cache ou executa um novo se necessário."""
    if force or _cache is None:
        return run_bdd()
    return _cache
