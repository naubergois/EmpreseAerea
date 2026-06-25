"""Catálogo sintético de voos para desenvolvimento e testes."""
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

_DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "voos_sinteticos.json"
_CATALOG: dict | None = None

AEROPORTOS: dict[str, list[str]] = {
    "são paulo": ["GRU", "CGH"],
    "sao paulo": ["GRU", "CGH"],
    "rio de janeiro": ["GIG", "SDU"],
    "brasília": ["BSB"],
    "brasilia": ["BSB"],
    "salvador": ["SSA"],
    "recife": ["REC"],
    "fortaleza": ["FOR"],
    "porto alegre": ["POA"],
    "curitiba": ["CWB"],
    "miami": ["MIA"],
    "lisboa": ["LIS"],
    "paris": ["CDG"],
    "santiago": ["SCL"],
    "antananarivo": ["TNR"],
}

COMPANHIAS = {
    "LATAM": {"nome": "LATAM Airlines", "logo": "/logos/latam.png"},
    "GOL": {"nome": "GOL Linhas Aéreas", "logo": "/logos/gol.png"},
    "AZUL": {"nome": "Azul Linhas Aéreas", "logo": "/logos/azul.png"},
}

NUMEROS_FIXOS = ["3421", "3100", "4521", "8050", "3155"]


def _load_catalog() -> dict:
    global _CATALOG
    if _CATALOG is None:
        with open(_DATA_PATH, encoding="utf-8") as f:
            _CATALOG = json.load(f)
    return _CATALOG


def _rota_info(origem: str, destino: str) -> dict:
    catalog = _load_catalog()
    for rota in catalog["rotas"]:
        if rota["origem"] == origem and rota["destino"] == destino:
            return rota
    # Rota genérica para qualquer par IATA não listado
    return {"origem": origem, "destino": destino, "distancia_km": 800, "duracao_base": 120}


def _sem_voos(origem: str, destino: str) -> bool:
    catalog = _load_catalog()
    if origem == destino:
        return True
    return any(r["origem"] == origem and r["destino"] == destino for r in catalog["sem_voos"])


def _preco_base(distancia_km: int, classe: str, alta_demanda: bool) -> int:
    tarifa_km = {"economica": 0.45, "executiva": 1.2, "primeira": 3.5}.get(classe, 0.45)
    base = max(199, int(distancia_km * tarifa_km))
    if alta_demanda:
        base = int(base * 1.4)
    return base


def gerar_voos(
    origem: str,
    destino: str,
    data_ida: datetime,
    adultos: int = 1,
    classe: str = "economica",
    alta_demanda: bool = False,
) -> list[dict[str, Any]]:
    """Gera voos sintéticos para qualquer rota IATA válida."""
    if _sem_voos(origem, destino):
        return []

    rota = _rota_info(origem, destino)
    catalog = _load_catalog()
    templates = catalog["voos_template"]
    base_preco = _preco_base(rota["distancia_km"], classe, alta_demanda)
    dur_base = rota["duracao_base"]

    result = []
    for i, tpl in enumerate(templates):
        numero = f"{tpl['numero_prefixo']}{NUMEROS_FIXOS[i]}"
        escalas = tpl["escalas"]
        dur = dur_base + escalas * 90
        partida = data_ida.replace(hour=6 + i * 3, minute=15, second=0, microsecond=0)
        chegada = partida + timedelta(minutes=dur)
        preco = base_preco + i * 50
        comp = COMPANHIAS[tpl["companhia"]]
        result.append({
            "id": f"{numero}-{data_ida.strftime('%Y%m%d')}",
            "numero": numero,
            "companhia": {"codigo": tpl["companhia"], "nome": comp["nome"], "logo": comp["logo"]},
            "origem": origem,
            "destino": destino,
            "partida": partida.isoformat(),
            "chegada": chegada.isoformat(),
            "duracao_minutos": dur,
            "escalas": escalas,
            "classe": classe,
            "preco": preco,
            "preco_por_passageiro": preco,
            "preco_total": preco * adultos,
            "bagagem_inclusa": escalas == 0,
            "bagagem_mao_kg": 10,
            "bagagem_despacho_kg": 23 if escalas == 0 else 0,
            "cadeirante": True,
            "alta_demanda": alta_demanda,
            "data": data_ida.strftime("%Y-%m-%d"),
        })
    return result


def resolver_aeroportos(local: str) -> list[str]:
    """Resolve nome de cidade ou código IATA para lista de aeroportos."""
    local = local.strip()
    if len(local) == 3 and local.isupper():
        return [local]
    if len(local) == 3:
        return [local.upper()]
    return AEROPORTOS.get(local.lower(), [local.upper()[:3]])


def rotas_populares() -> list[tuple[str, str]]:
    """Rotas para pré-carregar no cache na inicialização."""
    catalog = _load_catalog()
    return [(r["origem"], r["destino"]) for r in catalog["rotas"]]
