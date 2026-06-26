"""Cliente HTTP fino para a Web API do SonarQube.

Encapsula a autenticação por token e os endpoints usados pelo Agente de
Qualidade: issues, métricas, quality gate e security hotspots.
"""
from __future__ import annotations

from typing import Any

import httpx

from config import get_settings


class SonarUnavailableError(RuntimeError):
    """Lançada quando o servidor SonarQube não pode ser contatado/autenticado."""


class SonarClient:
    """Wrapper sobre a Web API do SonarQube.

    Autentica via *user token* (`squ_...`) usando Bearer token, que é o método
    recomendado e evita trafegar usuário/senha.
    """

    def __init__(
        self,
        host_url: str | None = None,
        token: str | None = None,
        project_key: str | None = None,
        timeout: float = 15.0,
    ) -> None:
        settings = get_settings()
        self.host_url = (host_url or settings.sonar_host_url).rstrip("/")
        self.token = token or settings.sonar_token
        self.project_key = project_key or settings.sonar_project_key
        self._timeout = timeout

    def _headers(self) -> dict[str, str]:
        if not self.token:
            return {}
        return {"Authorization": f"Bearer {self.token}"}

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict:
        url = f"{self.host_url}{path}"
        try:
            resp = httpx.get(
                url, params=params, headers=self._headers(), timeout=self._timeout
            )
        except httpx.HTTPError as exc:
            raise SonarUnavailableError(
                f"Não foi possível contatar o SonarQube em {self.host_url}: {exc}"
            ) from exc
        if resp.status_code == 401:
            raise SonarUnavailableError(
                "SonarQube recusou a autenticação (verifique SONAR_TOKEN)."
            )
        if resp.status_code >= 400:
            raise SonarUnavailableError(
                f"SonarQube retornou {resp.status_code} para {path}: {resp.text[:200]}"
            )
        return resp.json()

    # -- Saúde ---------------------------------------------------------------
    def system_status(self) -> dict:
        """Retorna o status do servidor (`UP`, `STARTING`, `DOWN`)."""
        return self._get("/api/system/status")

    # -- Issues --------------------------------------------------------------
    def search_issues(
        self,
        statuses: str = "OPEN,CONFIRMED,REOPENED",
        page_size: int = 500,
    ) -> list[dict]:
        """Busca todas as issues abertas do projeto, paginando automaticamente."""
        issues: list[dict] = []
        page = 1
        while True:
            data = self._get(
                "/api/issues/search",
                {
                    "components": self.project_key,
                    "statuses": statuses,
                    "ps": page_size,
                    "p": page,
                    "additionalFields": "rules",
                },
            )
            batch = data.get("issues", [])
            issues.extend(batch)
            total = data.get("paging", {}).get("total", 0)
            if page * page_size >= total or not batch:
                break
            page += 1
        return issues

    # -- Métricas ------------------------------------------------------------
    def measures(self, metric_keys: list[str] | None = None) -> dict[str, str]:
        """Retorna um dicionário {métrica: valor} para o projeto."""
        keys = metric_keys or [
            "bugs",
            "vulnerabilities",
            "code_smells",
            "security_hotspots",
            "coverage",
            "duplicated_lines_density",
            "ncloc",
            "sqale_index",
            "reliability_rating",
            "security_rating",
            "sqale_rating",
        ]
        data = self._get(
            "/api/measures/component",
            {"component": self.project_key, "metricKeys": ",".join(keys)},
        )
        measures = data.get("component", {}).get("measures", [])
        return {m["metric"]: m.get("value", "0") for m in measures}

    # -- Quality Gate --------------------------------------------------------
    def quality_gate(self) -> dict:
        """Retorna o status do quality gate do projeto."""
        data = self._get(
            "/api/qualitygates/project_status", {"projectKey": self.project_key}
        )
        return data.get("projectStatus", {})

    # -- Security Hotspots ---------------------------------------------------
    def search_hotspots(self, page_size: int = 500) -> list[dict]:
        """Busca os security hotspots do projeto."""
        hotspots: list[dict] = []
        page = 1
        while True:
            data = self._get(
                "/api/hotspots/search",
                {"projectKey": self.project_key, "ps": page_size, "p": page},
            )
            batch = data.get("hotspots", [])
            hotspots.extend(batch)
            total = data.get("paging", {}).get("total", 0)
            if page * page_size >= total or not batch:
                break
            page += 1
        return hotspots
