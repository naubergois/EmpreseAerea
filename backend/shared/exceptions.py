"""Exceções customizadas do SkyAgent."""


class SkyAgentError(Exception):
    """Erro base da aplicação."""

    code: str = "erro_interno"

    def __init__(self, message: str, code: str | None = None):
        super().__init__(message)
        if code:
            self.code = code


class ValidationError(SkyAgentError):
    code = "validacao_falhou"


class NotFoundError(SkyAgentError):
    code = "nao_encontrado"


class BusinessError(SkyAgentError):
    """Erro de regra de negócio com código machine-readable."""

    def __init__(self, message: str, code: str):
        super().__init__(message, code)
