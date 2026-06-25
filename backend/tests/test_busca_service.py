"""Testes do agente de busca."""


def test_buscar_voo_ida(client):
    resp = client.get('/api/voos/buscar', params={
        'origem': 'GRU', 'destino': 'GIG', 'data_ida': '2026-08-15T00:00:00',
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data['total'] >= 1
    assert 'companhia' in data['voos'][0]


def test_buscar_sem_resultados(client):
    resp = client.get('/api/voos/buscar', params={
        'origem': 'GRU', 'destino': 'TNR', 'data_ida': '2026-08-15T00:00:00',
    })
    assert resp.status_code == 200
    assert resp.json()['total'] == 0


def test_resolver_aeroportos(client):
    resp = client.get('/api/voos/aeroportos', params={'q': 'São Paulo'})
    assert 'GRU' in resp.json()['aeroportos']
