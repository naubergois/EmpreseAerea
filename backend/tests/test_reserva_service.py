"""Testes de validação de reserva."""
from agents.reserva.validators import validar_cpf


def test_cpf_valido():
    ok, _ = validar_cpf('529.982.247-25')
    assert ok


def test_cpf_invalido():
    ok, msg = validar_cpf('000.000.000-00')
    assert not ok
    assert msg == 'documento_invalido'
