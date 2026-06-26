"""Testes do atendimento com LLM mockado."""
from unittest.mock import AsyncMock, patch

import pytest


@pytest.fixture
def mock_llm():
    with patch("agents.atendimento.service.llm_client") as mock:
        mock.enabled = True
        mock.chat = AsyncMock(return_value="Sua bagagem inclusa é de 23kg na tarifa Light.")
        yield mock


def test_chat_com_llm(client, mock_llm):
    resp = client.post("/api/atendimento/chat", json={
        "mensagem": "Qual a franquia de bagagem?",
        "canal": "chat",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["protocolo"].startswith("ATC-")
    assert "bagagem" in data["resposta"].lower() or "23" in data["resposta"]
    mock_llm.chat.assert_called_once()


def test_chat_fallback_faq_sem_llm(client):
    with patch("agents.atendimento.service.llm_client") as mock:
        mock.enabled = False
        mock.chat = AsyncMock(side_effect=RuntimeError("no key"))
        resp = client.post("/api/atendimento/chat", json={
            "mensagem": "Qual a política de cancelamento?",
            "canal": "chat",
        })
    assert resp.status_code == 200
    assert "ANAC" in resp.json()["resposta"] or "24h" in resp.json()["resposta"]


def test_chat_escalacao_sentimento_negativo(client, mock_llm):
    mock_llm.chat.return_value = "Lamento pelo ocorrido. [ESCALAR]"
    resp = client.post("/api/atendimento/chat", json={
        "mensagem": "Estou indignado, perdi o voo hoje!",
        "canal": "chat",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["escalado"] is True
    assert data["sentimento"] == "negativo"


def test_historico_protocolo(client, mock_llm):
    chat = client.post("/api/atendimento/chat", json={
        "mensagem": "Como faço check-in?",
        "canal": "chat",
    }).json()
    hist = client.get(f"/api/atendimento/{chat['protocolo']}")
    assert hist.status_code == 200
    assert hist.json()["protocolo"] == chat["protocolo"]
