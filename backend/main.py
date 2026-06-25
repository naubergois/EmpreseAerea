"""Entrypoint FastAPI SkyAgent."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agents.atendimento.controller import router as atendimento_router
from agents.busca_voos.controller import router as busca_router
from agents.emissao.controller import router as emissao_router
from agents.fidelidade.controller import router as fidelidade_router
from agents.marketing.controller import router as marketing_router
from agents.notificacoes.controller import router as notificacoes_router
from agents.orquestrador.controller import router as orquestrador_router
from agents.pagamento.controller import router as pagamento_router
from agents.precificacao.controller import router as precificacao_router
from agents.reserva.controller import router as reserva_router
from config import get_settings
from database import init_db
from seed import seed_data

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_data()
    yield


app = FastAPI(
    title="SkyAgent API",
    description="Plataforma Multi-Agente para Venda de Passagens Aéreas",
    version="1.0.0",
    lifespan=lifespan,
)

CORS_ORIGINS = [
    settings.frontend_url,
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orquestrador_router)
app.include_router(busca_router)
app.include_router(precificacao_router)
app.include_router(reserva_router)
app.include_router(pagamento_router)
app.include_router(emissao_router)
app.include_router(marketing_router)
app.include_router(atendimento_router)
app.include_router(notificacoes_router)
app.include_router(fidelidade_router)


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}
