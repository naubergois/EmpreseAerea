"""Validators de reserva — funções puras."""
from datetime import datetime, timedelta


def validar_cpf(cpf: str) -> tuple[bool, str]:
    cpf = cpf.replace(".", "").replace("-", "")
    if len(cpf) != 11 or not cpf.isdigit():
        return False, "CPF deve ter 11 dígitos"
    # CPFs com todos os dígitos iguais (000..., 111...) são inválidos.
    if cpf == cpf[0] * 11:
        return False, "documento_invalido"
    return True, "OK"


def validar_passaporte_validade(validade: datetime, data_viagem: datetime, meses: int = 6) -> tuple[bool, str]:
    limite = data_viagem + timedelta(days=meses * 30)
    if validade < limite:
        return False, "passaporte_validade_insuficiente"
    return True, "OK"


def validar_menor_acompanhado(idade: int, tem_adulto: bool, umnr: bool = False) -> tuple[bool, str]:
    if idade < 12 and not tem_adulto and not umnr:
        return False, "Menor de 12 anos requer acompanhante"
    return True, "OK"
