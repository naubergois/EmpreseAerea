"""Testes de integração do pipeline."""


def test_pipeline_happy_path(client):
    resp = client.post('/api/pipeline/start', json={
        'origem': 'GRU', 'destino': 'GIG', 'data_ida': '2026-08-15T00:00:00',
        'passageiros': [{
            'nome': 'João', 'sobrenome': 'Silva', 'cpf': '529.982.247-25',
            'data_nascimento': '1990-01-15T00:00:00', 'tipo': 'ADT',
        }],
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data['status'] == 'sucesso'
    assert len(data['etapas']) >= 7
    assert data['resultado']['pnr']
    assert data['resultado']['bilhete']


def test_health(client):
    resp = client.get('/health')
    assert resp.json()['status'] == 'healthy'
