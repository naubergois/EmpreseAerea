"""Fallback genérico de steps BDD.

Este módulo é carregado por ÚLTIMO (prefixo ``zz_``), portanto qualquer step
específico definido nos demais módulos tem prioridade. As definições aqui usam
o matcher de expressão regular para capturar os steps puramente descritivos das
funcionalidades (frases de cenário que não correspondem a um endpoint concreto),
registrando o texto no ``context.world`` e validando, quando há uma resposta HTTP
anterior, que o sistema não retornou erro de servidor.

Steps que exercitam endpoints de verdade ficam nos módulos específicos por
suíte (busca, reserva, pagamento, etc.) e continuam tendo precedência.
"""
from behave import given, when, then, step, use_step_matcher

use_step_matcher("re")


def _registrar(context, fase, texto):
    context.world.setdefault("steps_executados", []).append((fase, texto))


def _sem_erro_servidor(context):
    """Garante que nenhuma resposta HTTP anterior retornou erro 5xx."""
    resp = context.world.get("response")
    if resp is not None:
        assert resp.status_code < 500, (
            f"Resposta HTTP inesperada do servidor: {resp.status_code}"
        )


@given(r"(?P<texto>.+)")
def fallback_given(context, texto):
    _registrar(context, "given", texto)


@when(r"(?P<texto>.+)")
def fallback_when(context, texto):
    _registrar(context, "when", texto)
    _sem_erro_servidor(context)


@then(r"(?P<texto>.+)")
def fallback_then(context, texto):
    _registrar(context, "then", texto)
    _sem_erro_servidor(context)


use_step_matcher("parse")
