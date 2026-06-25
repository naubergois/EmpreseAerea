"""Repository de cache de busca."""
import json
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from .models import BuscaCache


class BuscaRepository:
    def __init__(self, db: Session):
        self.db = db
        self.ttl_minutes = 15

    def get_cache(self, chave: str) -> list | None:
        row = self.db.query(BuscaCache).filter(BuscaCache.chave == chave).first()
        if not row:
            return None
        if row.criado_em < datetime.utcnow() - timedelta(minutes=self.ttl_minutes):
            return None
        return json.loads(row.resultado_json)

    def set_cache(self, chave: str, voos: list) -> None:
        row = self.db.query(BuscaCache).filter(BuscaCache.chave == chave).first()
        payload = json.dumps(voos)
        if row:
            row.resultado_json = payload
            row.criado_em = datetime.utcnow()
        else:
            self.db.add(BuscaCache(chave=chave, resultado_json=payload))
        self.db.commit()
