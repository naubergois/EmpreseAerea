"""
Singleton de configuração.
Carrega variáveis de ambiente UMA vez e reutiliza em toda a aplicação.
"""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação. Carregadas do .env."""

    # Banco de dados
    database_url: str = "sqlite:///./skyagent.db"

    # Redis (cache)
    redis_url: str = "redis://localhost:6379/0"

    # GDS API Keys
    amadeus_api_key: str = ""
    amadeus_api_secret: str = ""
    sabre_api_key: str = ""
    travelport_api_key: str = ""

    # Gateway de pagamento
    payment_gateway_url: str = ""
    payment_gateway_key: str = ""

    # Configurações de negócio
    session_timeout_minutes: int = 30
    booking_hold_minutes: int = 20
    pix_expiry_minutes: int = 30
    max_retry_attempts: int = 3
    circuit_breaker_threshold: int = 5

    # CORS
    frontend_url: str = "http://localhost:5173"

    # LLM (DeepSeek / OpenAI-compatible)
    llm_api_key: str = ""
    llm_base_url: str = "https://api.deepseek.com"
    llm_model: str = "deepseek-chat"
    llm_timeout_seconds: int = 30

    # JWT
    jwt_secret_key: str = "skyagent-dev-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_expiry_minutes: int = 60

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Retorna instância única de Settings (Singleton)."""
    return Settings()
