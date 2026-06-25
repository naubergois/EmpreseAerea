"""Steps do orquestrador BDD."""
from behave import given, then, when


@given('que o cliente busca voo de "{origem}" para "{destino}" em "{data}"')
def step_pipeline_busca(context, origem, destino, data):
    context.world['pipeline'] = {
        'origem': origem, 'destino': destino, 'data_ida': f'{data}T00:00:00',
        'preco_base': 450,
        'passageiros': [{
            'nome': 'João', 'sobrenome': 'Silva', 'cpf': '529.982.247-25',
            'data_nascimento': '1990-01-15T00:00:00', 'tipo': 'ADT',
        }],
    }


@given('que o cliente envia uma requisição de busca de voo')
def step_req_busca(context):
    context.world['pipeline'] = {
        'origem': 'GRU', 'destino': 'GIG', 'data_ida': '2026-08-15T00:00:00',
    }


@given('a requisição contém origem "{origem}", destino "{destino}" e data "{data}"')
def step_req_params(context, origem, destino, data):
    context.world.setdefault('pipeline', {}).update({
        'origem': origem, 'destino': destino, 'data_ida': f'{data}T00:00:00',
    })


@given('que o cliente envia a mensagem "{mensagem}"')
def step_mensagem(context, mensagem):
    context.world['mensagem'] = mensagem


@when('o Orquestrador recebe a requisição')
def step_orc_recebe(context):
    body = context.world.get('pipeline', {
        'origem': 'GRU', 'destino': 'GIG', 'data_ida': '2026-08-15T00:00:00',
    })
    resp = context.client.post('/api/pipeline/start', json=body)
    context.world['response'] = resp
    context.world['result'] = resp.json() if resp.status_code == 200 else {}


@when('o Orquestrador classifica a intenção')
def step_classificar(context):
    resp = context.client.post('/api/pipeline/classificar', params={
        'mensagem': context.world['mensagem'],
    })
    context.world['result'] = resp.json()


@when('o pipeline finaliza com sucesso')
def step_pipeline_finaliza(context):
    body = context.world.get('pipeline', {
        'origem': 'GRU', 'destino': 'GIG', 'data_ida': '2026-08-15T00:00:00',
        'passageiros': [{
            'nome': 'João', 'sobrenome': 'Silva', 'cpf': '529.982.247-25',
            'data_nascimento': '1990-01-15T00:00:00', 'tipo': 'ADT',
        }],
    })
    resp = context.client.post('/api/pipeline/start', json=body)
    context.world['response'] = resp
    context.world['result'] = resp.json() if resp.status_code == 200 else {}


@then('todas as 7 etapas devem ter status "Sucesso"')
def step_7_etapas(context):
    etapas = context.world['result'].get('etapas', [])
    assert len(etapas) >= 7
    for e in etapas[:7]:
        assert e['status'] == 'Sucesso'


@then('o trace ID deve ser único e rastreável')
def step_trace_id(context):
    trace = context.world['result'].get('trace_id', '')
    assert trace.startswith('TRC-')


@then('a intenção deve ser classificada como "{intencao}"')
def step_intencao(context, intencao):
    assert context.world['result'].get('intencao') == intencao


@then('a requisição deve ser roteada para o Agente de Busca de Voos')
def step_roteado_bus(context):
    assert context.world['result'].get('status') == 'sucesso' or context.world['response'].status_code == 200


@then('o tempo de roteamento deve ser inferior a 100ms')
def step_tempo_roteamento(context):
    assert context.world['response'].elapsed.total_seconds() < 0.1


@then('um ID de sessão deve ser criado para o cliente')
def step_session_id(context):
    assert context.world['result'].get('session_id', '').startswith('SES-')
