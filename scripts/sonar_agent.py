#!/usr/bin/env python3
"""Agente de Qualidade SkyAgent — CLI.

Orquestra o ciclo de qualidade baseado no SonarQube:

  1. (opcional) dispara uma nova análise via SonarScanner em Docker;
  2. coleta issues, métricas e quality gate através do Agente de Qualidade;
  3. gera um plano de melhorias priorizado em ``docs/SONARQUBE_MELHORIAS.md``.

Uso:
    python scripts/sonar_agent.py            # coleta e gera o relatório
    python scripts/sonar_agent.py --scan     # roda o scanner antes de coletar
    python scripts/sonar_agent.py --json     # imprime o plano em JSON (stdout)

Credenciais são lidas de ``backend/.env`` (SONAR_HOST_URL, SONAR_TOKEN,
SONAR_PROJECT_KEY) — nunca passe o token por linha de comando.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = REPO_ROOT / "backend"
DOCS_DIR = REPO_ROOT / "docs"
RELATORIO = DOCS_DIR / "SONARQUBE_MELHORIAS.md"

_SEVERIDADE_EMOJI = {
    "BLOCKER": "🟥",
    "CRITICAL": "🟧",
    "MAJOR": "🟨",
    "MINOR": "🟦",
    "INFO": "⬜",
}


def _carregar_servico():
    """Importa o Agente de Qualidade com o ambiente do backend carregado."""
    os.chdir(BACKEND_DIR)  # garante que pydantic-settings ache o .env
    sys.path.insert(0, str(BACKEND_DIR))
    from agents.qualidade.service import QualidadeService  # noqa: E402

    return QualidadeService()


def _ler_env_sonar() -> dict[str, str]:
    """Lê as variáveis SONAR_* do backend/.env (sem expor o token)."""
    env: dict[str, str] = {}
    env_file = BACKEND_DIR / ".env"
    if env_file.exists():
        for linha in env_file.read_text(encoding="utf-8").splitlines():
            if linha.startswith("SONAR_") and "=" in linha:
                chave, _, valor = linha.partition("=")
                env[chave.strip()] = valor.strip()
    return env


def rodar_scanner() -> None:
    """Dispara o SonarScanner via Docker, passando o token por env-file."""
    env = _ler_env_sonar()
    token = env.get("SONAR_TOKEN", "")
    if not token:
        sys.exit("SONAR_TOKEN ausente em backend/.env — não é possível escanear.")

    # Dentro do container, o host é host.docker.internal.
    host = "http://host.docker.internal:9000"
    with tempfile.NamedTemporaryFile(
        "w", suffix=".env", delete=False, encoding="utf-8"
    ) as fh:
        fh.write(f"SONAR_HOST_URL={host}\nSONAR_TOKEN={token}\n")
        env_path = fh.name
    os.chmod(env_path, 0o600)

    print("→ Executando SonarScanner (Docker)…")
    try:
        subprocess.run(
            [
                "docker", "run", "--rm", "--env-file", env_path,
                "-v", f"{REPO_ROOT}:/usr/src",
                "sonarsource/sonar-scanner-cli",
            ],
            check=True,
        )
    finally:
        os.unlink(env_path)
    print("→ Aguardando o servidor processar o relatório…")
    time.sleep(10)


def gerar_relatorio(servico) -> str:
    """Monta o markdown do plano de melhorias e o devolve como string."""
    status = servico.status()
    plano = servico.plano_melhorias()
    m = status.metricas

    linhas: list[str] = []
    linhas.append("# Plano de Melhorias — SonarQube (Agente de Qualidade)\n")
    linhas.append(
        "> Gerado automaticamente pelo Agente de Qualidade do SkyAgent "
        f"em `{plano.gerado_em}`.\n"
    )
    gate_icon = "✅" if status.quality_gate == "OK" else "❌"
    linhas.append(f"**Quality Gate:** {gate_icon} `{status.quality_gate}`\n")

    linhas.append("## Métricas do projeto\n")
    linhas.append("| Métrica | Valor |")
    linhas.append("|---------|-------|")
    linhas.append(f"| 🐞 Bugs | {m.bugs} |")
    linhas.append(f"| 🔓 Vulnerabilidades | {m.vulnerabilidades} |")
    linhas.append(f"| 🧹 Code Smells | {m.code_smells} |")
    linhas.append(f"| 🔥 Security Hotspots | {m.security_hotspots} |")
    linhas.append(f"| 🧪 Cobertura | {m.cobertura}% |")
    linhas.append(f"| 📑 Duplicação | {m.duplicacao}% |")
    linhas.append(f"| 📏 Linhas de código | {m.linhas_codigo} |")
    linhas.append(f"| ⏱️ Dívida técnica | {m.divida_tecnica_min} min |")
    linhas.append(
        f"| 🎯 Notas (Conf./Seg./Manut.) | "
        f"{m.nota_confiabilidade} / {m.nota_seguranca} / {m.nota_manutenibilidade} |"
    )
    linhas.append("")

    linhas.append(f"## Plano de melhorias priorizado ({plano.total} itens)\n")
    if not plano.melhorias:
        linhas.append("_Nenhuma issue aberta. Parabéns! 🎉_\n")
    for i, mel in enumerate(plano.melhorias, 1):
        emoji = _SEVERIDADE_EMOJI.get(mel.severidade, "⬜")
        linhas.append(
            f"### {i}. {emoji} P{mel.prioridade} · {mel.tipo} · `{mel.regra}`"
        )
        linhas.append(f"- **Ocorrências:** {mel.ocorrencias}")
        linhas.append(f"- **Severidade:** {mel.severidade}")
        linhas.append(f"- **Título:** {mel.titulo}")
        linhas.append(f"- **Ação sugerida:** {mel.acao_sugerida}")
        arquivos = ", ".join(f"`{a}`" for a in mel.arquivos[:8])
        linhas.append(f"- **Arquivos:** {arquivos}")
        if mel.exemplos:
            linhas.append("- **Exemplos:**")
            for ex in mel.exemplos:
                loc = f":{ex.linha}" if ex.linha else ""
                linhas.append(f"    - `{ex.arquivo}{loc}` — {ex.mensagem}")
        linhas.append("")

    return "\n".join(linhas)


def main() -> None:
    parser = argparse.ArgumentParser(description="Agente de Qualidade SkyAgent")
    parser.add_argument(
        "--scan", action="store_true", help="roda o SonarScanner antes de coletar"
    )
    parser.add_argument(
        "--json", action="store_true", help="imprime o plano em JSON no stdout"
    )
    args = parser.parse_args()

    if args.scan:
        rodar_scanner()

    servico = _carregar_servico()

    from agents.qualidade.sonar_client import SonarUnavailableError

    try:
        if args.json:
            print(servico.plano_melhorias().model_dump_json(indent=2))
            return

        conteudo = gerar_relatorio(servico)
    except SonarUnavailableError as exc:
        sys.exit(f"SonarQube indisponível: {exc}")

    DOCS_DIR.mkdir(exist_ok=True)
    RELATORIO.write_text(conteudo, encoding="utf-8")
    plano = servico.plano_melhorias()
    print(f"✓ Relatório gerado: {RELATORIO.relative_to(REPO_ROOT)}")
    print(f"  {plano.total} grupos de melhoria a partir das issues do SonarQube.")


if __name__ == "__main__":
    main()
