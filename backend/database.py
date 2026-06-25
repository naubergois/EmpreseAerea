"""Singleton de conexão com o banco de dados."""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {},
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency injection: gera sessão por request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Cria todas as tabelas."""
    import agents.busca_voos.models  # noqa: F401
    import agents.reserva.models  # noqa: F401
    import agents.pagamento.models  # noqa: F401
    import agents.emissao.models  # noqa: F401
    import agents.fidelidade.models  # noqa: F401
    import agents.notificacoes.models  # noqa: F401
    import agents.marketing.models  # noqa: F401
    import agents.atendimento.models  # noqa: F401
    import agents.orquestrador.models  # noqa: F401
    import agents.precificacao.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
