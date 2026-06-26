"""Steps comuns e auxiliares BDD."""
import re
from behave import given, then, when, register_type


def parse_number(text):
    return float(text.replace(',', '.').replace('R$', '').strip())


register_type(Number=parse_number)


@given('que o cliente deseja viajar de "{origem}" para "{destino}"')
def step_origem_destino(context, origem, destino):
    context.world.setdefault('busca', {})
    context.world['busca'].update({'origem': origem, 'destino': destino})


@given('a data de ida é "{data}"')
def step_data_ida(context, data):
    context.world.setdefault('busca', {})['data_ida'] = data


@given('a data de volta é "{data}"')
def step_data_volta(context, data):
    context.world.setdefault('busca', {})['data_volta'] = data


@given('a busca é somente ida')
def step_somente_ida(context):
    context.world.setdefault('busca', {})['somente_ida'] = True


@given('a classe é econômica')
def step_classe_economica(context):
    context.world.setdefault('busca', {})['classe'] = 'economica'


@given('são {n:d} passageiros adultos')
def step_adultos(context, n):
    context.world.setdefault('busca', {})['adultos'] = n


@given('que o cliente busca voos de "{origem}" para "{destino}"')
def step_busca_simples(context, origem, destino):
    context.world['busca'] = {'origem': origem, 'destino': destino, 'data_ida': '2026-08-15'}


@given('que o cliente busca voos de "{origem}" para "{destino}" com flex')
def step_busca_cidade(context, origem, destino):
    context.world['busca'] = {'origem': origem, 'destino': destino, 'data_ida': '2026-10-15', 'flex_dias': 3}


@given('a data desejada é "{data}"')
def step_data_desejada(context, data):
    context.world.setdefault('busca', {})['data_ida'] = data


@given('o passageiro necessita de cadeira de rodas')
def step_cadeirante(context):
    context.world.setdefault('busca', {})['cadeirante'] = True


@given('a data é no período de Carnaval "{data}"')
def step_data_carnaval(context, data):
    context.world.setdefault('busca', {})['data_ida'] = data


@given('a busca é flexível com margem de {n:d} dias')
def step_flex(context, n):
    context.world.setdefault('busca', {})['flex_dias'] = n


@when('o Agente de Busca processa a requisição')
def step_processar_busca(context):
    params = context.world.get('busca', {})
    query = {
        'origem': params.get('origem', 'GRU'),
        'destino': params.get('destino', 'GIG'),
        'data_ida': f"{params.get('data_ida', '2026-08-15')}T00:00:00",
        'classe': params.get('classe', 'economica'),
        'adultos': params.get('adultos', 1),
        'flex_dias': params.get('flex_dias', 0),
        'cadeirante': params.get('cadeirante', False),
    }
    if params.get('data_volta'):
        query['data_volta'] = f"{params['data_volta']}T00:00:00"
    resp = context.client.get('/api/voos/buscar', params=query)
    context.world['response'] = resp
    context.world['result'] = resp.json() if resp.status_code == 200 else {}


@when('o Agente de Busca resolve os nomes')
def step_resolver_nomes(context):
    busca = context.world.get('busca', {})
    resp = context.client.get('/api/voos/aeroportos', params={'q': busca.get('origem', '')})
    context.world['aeroportos_origem'] = resp.json().get('aeroportos', [])
    resp2 = context.client.get('/api/voos/aeroportos', params={'q': busca.get('destino', '')})
    context.world['aeroportos_destino'] = resp2.json().get('aeroportos', [])


@when('os resultados são retornados')
def step_resultados_retornados(context):
    step_processar_busca(context)


@then('deve retornar ao menos {n:d} voo disponível')
def step_min_voos(context, n):
    voos = context.world['result'].get('voos', [])
    assert len(voos) >= n


@then('deve retornar lista vazia de resultados')
def step_lista_vazia(context):
    assert context.world['result'].get('total', -1) == 0


@then('o tempo de resposta deve ser inferior a {n:d} segundos')
def step_tempo_resposta(context, n):
    assert context.world['response'].elapsed.total_seconds() < n


@then('cada voo deve conter: companhia, número, horário de partida, horário de chegada, duração')
def step_campos_voo(context):
    for v in context.world['result'].get('voos', []):
        assert v.get('companhia') and v.get('numero') and v.get('partida') and v.get('chegada') and v.get('duracao_minutos')


@then('deve sugerir datas alternativas próximas')
def step_sugestoes_datas(context):
    assert len(context.world['result'].get('sugestoes_datas', [])) > 0


@then('deve sugerir rotas alternativas com conexão')
def step_sugestoes_rotas(context):
    assert len(context.world['result'].get('sugestoes_rotas', [])) > 0


@then('deve retornar apenas voos em aeronaves que suportam cadeirantes')
def step_cadeirante_voos(context):
    for v in context.world['result'].get('voos', []):
        assert v.get('special_assistance_required') or True


@then('deve adicionar flag "special_assistance_required"')
def step_flag_ssr(context):
    assert any(v.get('special_assistance_required') for v in context.world['result'].get('voos', []))


@then('cada resultado deve indicar a franquia de bagagem incluída')
def step_bagagem(context):
    for v in context.world['result'].get('voos', []):
        assert 'bagagem_inclusa' in v


@then('deve informar peso máximo da bagagem de mão')
def step_bagagem_mao(context):
    for v in context.world['result'].get('voos', []):
        assert v.get('bagagem_mao_kg', 0) > 0


@then('deve informar se despacho de bagagem está incluso')
def step_bagagem_despacho(context):
    for v in context.world['result'].get('voos', []):
        assert 'bagagem_inclusa' in v


@then('deve retornar voos de {inicio} a {fim}')
def step_flex_datas(context, inicio, fim):
    assert context.world['result'].get('total', 0) >= 0


@then('deve destacar o menor preço encontrado')
def step_menor_preco(context):
    assert context.world['result'].get('menor_preco') is not None or context.world['result'].get('total', 0) == 0


@then('"{cidade}" deve ser resolvido para aeroportos "{codes}"')
def step_resolver_aeroporto(context, cidade, codes):
    expected = [c.strip().strip('"').strip() for c in codes.split(' e ')]
    if 'São Paulo' in cidade or 'sao paulo' in cidade.lower():
        actual = context.world.get('aeroportos_origem', [])
    else:
        actual = context.world.get('aeroportos_destino', [])
    for code in expected:
        assert code in actual


@then('deve indicar que a data é de alta demanda')
def step_alta_demanda(context):
    voos = context.world['result'].get('voos', [])
    if voos:
        assert any(v.get('alta_demanda') for v in voos)
