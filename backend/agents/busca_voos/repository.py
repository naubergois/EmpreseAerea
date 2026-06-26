"""Repository de cache de busca.

Cache em duas camadas: L1 em memória de processo (sub-ms, sem I/O) à frente do
L2 persistido em SQLite (sobrevive a restart e é populado pelo seed).
"""
import json
import time
from datetime import timedelta

from sqlalchemy.orm import Session

from shared.datetime_utils import utc_now

from .models import BuscaCache

# L1: cache de processo compartilhado entre todas as instâncias de BuscaRepository.
# chave -> (expira_em_epoch, voos)
_MEM_CACHE: dict[str, tuple[float, list]] = {}


class BuscaRepository:
    def __init__(self, db: Session):
        self.db = db
        self.ttl_minutes = 15

    def get_cache(self, chave: str) -> list | None:
        # L1: memória
        entry = _MEM_CACHE.get(chave)
        if entry is not None:
            expira_em, voos = entry
            if time.time() < expira_em:
                return voos
            _MEM_CACHE.pop(chave, None)

        # L2: SQLite
        row = self.db.query(BuscaCache).filter(BuscaCache.chave == chave).first()
        if not row:
            return None
        if row.criado_em < utc_now() - timedelta(minutes=self.ttl_minutes):
            return None
        voos = json.loads(row.resultado_json)
        _MEM_CACHE[chave] = (time.time() + self.ttl_minutes * 60, voos)
        return voos

    def set_cache(self, chave: str, voos: list) -> None:
        _MEM_CACHE[chave] = (time.time() + self.ttl_minutes * 60, voos)
        row = self.db.query(BuscaCache).filter(BuscaCache.chave == chave).first()
        payload = json.dumps(voos)
        if row:
            row.resultado_json = payload
            row.criado_em = utc_now()
        else:
            self.db.add(BuscaCache(chave=chave, resultado_json=payload))
        self.db.commit()
