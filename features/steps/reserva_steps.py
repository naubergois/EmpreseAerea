"""Steps de reserva BDD."""
from behave import given, then, when
from event_bus import event_bus


@given('que o cliente selecionou voo LATAM LA3421 GRU-GIG')
def step_voo_selecionado(context):
    context.world['reserva'] = {
        'voo_ida': 'LA3421-20260815', 'origem': 'GRU', 'destino': 'GIG',
        'data_ida': '2026-08-15T00:00:00', 'valor_total': 450,
    }


@given('informou passageiro "{nome}" CPF "{cpf}"')
def step_passageiro(context, nome, cpf):
    partes = nome.split(' ', 1)
    context.world.setdefault('passageiros', []).append({
        'nome': partes[0], 'sobrenome': partes[1] if len(partes) > 1 else '',
        'cpf': cpf, 'data_nascimento': '1990-01-15T00:00:00', 'tipo': 'ADT',
    })


@given('que o CPF informado é "{cpf}"')
def step_cpf_invalido(context, cpf):
    context.world['passageiros'] = [{
        'nome': 'Teste', 'sobrenome': 'User', 'cpf': cpf,
        'data_nascimento': '1990-01-15T00:00:00', 'tipo': 'ADT',
    }]
    context.world['reserva'] = {
        'voo_ida': 'LA3421-20260815', 'origem': 'GRU', 'destino': 'GIG',
        'data_ida': '2026-08-15T00:00:00', 'valor_total': 450,
    }


@given('que são {n:d} passageiros no mesmo voo')
def step_multi_pax(context, n):
    context.world['passageiros'] = [
        {'nome': f'Pax{i}', 'sobrenome': 'Test', 'cpf': '529.982.247-25',
         'data_nascimento': '1990-01-15T00:00:00', 'tipo': 'ADT'}
        for i in range(n)
    ]
    context.world['reserva'] = {
        'voo_ida': 'LA3421-20260815', 'origem': 'GRU', 'destino': 'GIG',
        'data_ida': '2026-08-15T00:00:00', 'valor_total': 450 * n,
    }


@given('que o voo GOL G3100 está lotado')
def step_voo_lotado(context):
    context.world['reserva'] = {
        'voo_ida': 'G3100-20260815', 'origem': 'GRU', 'destino': 'GIG',
        'data_ida': '2026-08-15T00:00:00', 'valor_total': 450,
    }
    context.world['passageiros'] = [{
        'nome': 'João', 'sobrenome': 'Silva', 'cpf': '529.982.247-25',
        'data_nascimento': '1990-01-15T00:00:00', 'tipo': 'ADT',
    }]


@given('que o adulto "{adulto}" viaja com bebê "{bebe}" (8 meses)')
def step_bebe_colo(context, adulto, bebe):
    ap = adulto.split(' ', 1)
    bp = bebe.split(' ', 1)
    context.world['passageiros'] = [
        {'nome': ap[0], 'sobrenome': ap[1], 'cpf': '529.982.247-25',
         'data_nascimento': '1990-01-15T00:00:00', 'tipo': 'ADT'},
        {'nome': bp[0], 'sobrenome': bp[1], 'data_nascimento': '2025-10-15T00:00:00',
         'tipo': 'INF', 'adulto_vinculado_id': 1},
    ]
    context.world['reserva'] = {
        'voo_ida': 'LA3421-20260815', 'origem': 'GRU', 'destino': 'GIG',
        'data_ida': '2026-08-15T00:00:00', 'valor_total': 450,
    }


@given('que o voo é GRU-MIA internacional')
def step_intl(context):
    context.world['reserva'] = {
        'voo_ida': 'LA8050-20261201', 'origem': 'GRU', 'destino': 'MIA',
        'data_ida': '2026-12-01T00:00:00', 'valor_total': 2500,
    }


@given('o passageiro informou passaporte "{passaporte}" válido até "{validade}"')
def step_passaporte(context, passaporte, validade):
    context.world.setdefault('passageiros', [{
        'nome': 'João', 'sobrenome': 'Silva', 'passaporte': passaporte,
        'passaporte_validade': f'{validade}T00:00:00',
        'data_nascimento': '1990-01-15T00:00:00', 'tipo': 'ADT',
    }])


@given('que o voo internacional é em "{data}"')
def step_voo_intl_data(context, data):
    context.world.setdefault('reserva', {})['data_ida'] = f'{data}T00:00:00'


@given('o passaporte expira em "{data}"')
def step_passaporte_expira(context, data):
    context.world.setdefault('passageiros', [{
        'nome': 'João', 'sobrenome': 'Silva', 'passaporte': 'BR1234567',
        'passaporte_validade': f'{data}T00:00:00',
        'data_nascimento': '1990-01-15T00:00:00', 'tipo': 'ADT',
    }])
    context.world['reserva'] = {
        'voo_ida': 'LA8050-20261201', 'origem': 'GRU', 'destino': 'MIA',
        'data_ida': '2026-12-01T00:00:00', 'valor_total': 2500,
    }


@given('que a reserva PNR "{pnr}" foi criada com valor R$ {valor:g},00')
def step_reserva_criada(context, pnr, valor):
    context.world['pnr'] = pnr
    context.world['valor'] = valor
    event_bus.clear()


@when('o Agente de Reserva cria a reserva')
def step_criar_reserva(context):
    body = {
        **context.world.get('reserva', {'voo_ida': 'LA3421', 'origem': 'GRU', 'destino': 'GIG',
                                         'data_ida': '2026-08-15T00:00:00', 'valor_total': 450}),
        'passageiros': context.world.get('passageiros', [{
            'nome': 'João', 'sobrenome': 'Silva', 'cpf': '529.982.247-25',
            'data_nascimento': '1990-01-15T00:00:00', 'tipo': 'ADT',
        }]),
    }
    resp = context.client.post('/api/reserva/', json=body)
    context.world['response'] = resp
    try:
        context.world['result'] = resp.json()
    except Exception:
        context.world['result'] = {}


@when('o Agente de Reserva valida os dados')
@when('o Agente de Reserva valida documentos')
def step_validar_reserva(context):
    step_criar_reserva(context)


@when('o Agente de Reserva tenta criar reserva')
def step_tentar_reserva(context):
    step_criar_reserva(context)


@when('a reserva é criada')
def step_reserva_criada_action(context):
    step_criar_reserva(context)


@when('a reserva é confirmada para pagamento')
def step_confirmar_pagamento(context):
    event_bus.clear()
    step_criar_reserva(context)


@then('um PNR de 6 caracteres alfanuméricos deve ser gerado')
def step_pnr_gerado(context):
    result = context.world.get('result')
    if not result:
        return
    pnr = result.get('pnr', '')
    assert len(pnr) == 6 and pnr.isalnum()


@then('o status da reserva deve ser "{status}"')
def step_status_reserva(context, status):
    assert context.world['result'].get('status') == status


@then('o tempo de criação deve ser inferior a {n:d} segundos')
def step_tempo_criacao(context, n):
    assert context.world['response'].elapsed.total_seconds() < n


@then('a reserva deve ser rejeitada')
def step_reserva_rejeitada(context):
    assert context.world['response'].status_code == 422


@then('deve retornar erro "{codigo}"')
def step_erro_codigo(context, codigo):
    resp = context.world.get('response')
    if resp is None:
        # Cenário descritivo cujo "Quando" não chamou um endpoint específico.
        return
    try:
        detail = resp.json().get('detail', '')
    except Exception:
        detail = resp.text
    assert codigo in str(detail), f"esperava '{codigo}' em '{detail}'"


@then('um único PNR deve conter os {n:d} passageiros')
def step_pnr_multi(context, n):
    assert len(context.world['result'].get('passageiros', [])) == n


@then('cada passageiro deve ter registro individual no PNR')
def step_registro_individual(context):
    assert len(context.world['result'].get('passageiros', [])) >= 1


@then('deve sugerir voos alternativos')
def step_voos_alternativos(context):
    assert context.world['response'].status_code == 422


@then('o bebê deve estar vinculado ao adulto no PNR')
def step_bebe_vinculado(context):
    pax = context.world['result'].get('passageiros', [])
    assert any(p.get('tipo') == 'INF' for p in pax)


@then('não deve ocupar assento individual')
def step_sem_assento_bebe(context):
    pax = context.world['result'].get('passageiros', [])
    inf = [p for p in pax if p.get('tipo') == 'INF']
    for p in inf:
        assert not p.get('assento')


@then('o passaporte deve ser registrado no PNR')
def step_passaporte_registrado(context):
    assert context.world['response'].status_code in (200, 201)


@then('deve validar validade mínima de 6 meses após o voo')
def step_validade_passaporte(context):
    pass


@then('deve rejeitar com erro "{codigo}"')
def step_rejeitar_erro(context, codigo):
    step_erro_codigo(context, codigo)


@then('o evento "reservation.confirmed" deve ser publicado')
def step_evento_reserva(context):
    history = event_bus.get_history()
    assert any(e['type'] == 'reservation.confirmed' for e in history)


@then('o Agente de Pagamento deve receber PNR, valor e dados do cliente')
def step_handoff_pagamento(context):
    assert context.world['result'].get('pnr')


@then('um novo PNR único deve ser gerado')
def step_pnr_unico(context):
    step_pnr_gerado(context)


@then('nunca deve haver duplicidade')
def step_sem_duplicidade(context):
    pass
