"""Seed de dados iniciais e cache sintético de voos."""
from datetime import datetime, timedelta

from database import SessionLocal
from agents.busca_voos.gds_client import gerar_voos, rotas_populares
from agents.busca_voos.repository import BuscaRepository
from agents.precificacao.models import Cupom


def seed_data() -> None:
    db = SessionLocal()
    try:
        _seed_cupons(db)
        _seed_cache_voos(db)
    finally:
        db.close()


def _seed_cupons(db) -> None:
    if db.query(Cupom).count() > 0:
        return
    cupons = [
        Cupom(codigo="VERAO20", tipo="percentual", valor=20, uso_max=100,
              valido_ate=datetime.utcnow() + timedelta(days=90)),
        Cupom(codigo="PROMO50", tipo="fixo", valor=50, uso_max=50, valor_minimo=300),
    ]
    for c in cupons:
        db.add(c)
    db.commit()


def _seed_cache_voos(db) -> None:
    """Pré-carrega voos sintéticos para rotas populares (próximos 30 dias)."""
    repo = BuscaRepository(db)
    data_base = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    for origem, destino in rotas_populares():
        for dias in range(0, 30, 7):
            data = data_base + timedelta(days=dias)
            voos = gerar_voos(origem, destino, data)
            if voos:
                chave = f"['{origem}']-['{destino}']-{data.date()}-economica"
                if repo.get_cache(chave) is None:
                    repo.set_cache(chave, voos)
