"""Utilitários de data/hora.

Substitui o uso de ``datetime.utcnow()`` (depreciado e sinalizado pelo
SonarQube — regra python:S6903) por uma função explícita baseada em
``datetime.now(timezone.utc)``.

Retornamos o horário UTC *sem* ``tzinfo`` (naive) para manter compatibilidade
com as colunas ``DateTime`` do SQLAlchemy/SQLite, que armazenam datas naive —
assim as comparações existentes entre valores do banco e o "agora" continuam
funcionando sem misturar datas aware e naive.
"""
from datetime import datetime, timezone


def utc_now() -> datetime:
    """Retorna o instante atual em UTC, sem informação de fuso (naive)."""
    return datetime.now(timezone.utc).replace(tzinfo=None)
