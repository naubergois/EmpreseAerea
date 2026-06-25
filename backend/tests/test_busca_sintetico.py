"""Testes do catálogo sintético de voos."""
from datetime import datetime

from agents.busca_voos.gds_client import gerar_voos, resolver_aeroportos, rotas_populares


def test_gerar_voos_gru_gig():
    voos = gerar_voos("GRU", "GIG", datetime(2026, 8, 15))
    assert len(voos) == 5
    assert voos[0]["origem"] == "GRU"
    assert voos[0]["destino"] == "GIG"
    assert voos[0]["preco"] > 0


def test_gerar_voos_rota_generica():
    voos = gerar_voos("GRU", "CNF", datetime(2026, 8, 15))
    assert len(voos) >= 1


def test_sem_voos_tnr():
    voos = gerar_voos("GRU", "TNR", datetime(2026, 8, 15))
    assert voos == []


def test_resolver_sao_paulo():
    assert "GRU" in resolver_aeroportos("São Paulo")


def test_rotas_populares():
    rotas = rotas_populares()
    assert ("GRU", "GIG") in rotas
    assert len(rotas) >= 10
