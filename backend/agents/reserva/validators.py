"""Validators de reserva — funções puras."""
from datetime import datetime, timedelta


def validar_cpf(cpf: str) -> tuple[bool, str]:
    cpf = cpf.replace(".", "").replace("-", "")
    if len(cpf) != 11:
        return False, "CPF deve ter 11 dígitos"
    if cpf == cpf[0] * 11:
        return False, "documento_invalido"
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    d1 = 0 if (11 - soma % 11) >= 10 else 11 - soma % 11
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    d2 = 0 if (11 - soma % 11) >= 10 else 11 - soma % 11
    if int(cpf[9]) != d1 or int(cpf[10]) != d2:
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
