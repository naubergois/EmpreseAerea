"""Teste de integração da busca com dados sintéticos pré-carregados."""
from datetime import datetime, timedelta


def test_busca_com_cache_sintetico(client):
    data = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d")
    resp = client.get("/api/voos/buscar", params={
        "origem": "GRU", "destino": "GIG", "data_ida": data,
    })
    assert resp.status_code == 200
    body = resp.json()
    assert body["total"] >= 1
    assert body["voos"][0]["companhia"]["nome"]


def test_busca_rota_internacional(client):
    resp = client.get("/api/voos/buscar", params={
        "origem": "GRU", "destino": "MIA", "data_ida": "2026-12-20",
    })
    assert resp.status_code == 200
    assert resp.json()["total"] >= 1
    assert resp.json()["voos"][0]["duracao_minutos"] > 300


def test_busca_cors_headers(client):
    resp = client.get(
        "/api/voos/buscar",
        params={"origem": "GRU", "destino": "GIG", "data_ida": "2026-08-15"},
        headers={"Origin": "http://localhost:5174"},
    )
    assert resp.status_code == 200
