# Guia de Implementação — SkyAgent

> **Stack:** React (Frontend) + FastAPI (Backend) + PostgreSQL (DB)  
> **Padrões:** MVC · Singleton · SRP (Single Responsibility) · Clean Code  
> **Regra de Ouro:** Código simples. Nenhuma god class. Cada classe faz UMA coisa.

---

## 1. Princípios Arquiteturais

### 1.1 Código Simples — Regras Inegociáveis

| Regra | Descrição | Limite |
|-------|-----------|--------|
| **Nenhuma God Class** | Uma classe não deve acumular responsabilidades | Máx. 200 linhas por classe |
| **SRP** | Cada classe/módulo faz UMA coisa bem feita | 1 responsabilidade por arquivo |
| **Funções curtas** | Funções devem ser legíveis de uma vez | Máx. 30 linhas por função |
| **Nomes claros** | Nomes devem expressar intenção | Sem abreviações obscuras |
| **Sem lógica aninhada** | Evitar mais de 2 níveis de indentação | Early return sempre |
| **Composição > Herança** | Preferir composição e injeção de dependência | Herança só para interfaces |

### 1.2 Anti-padrões a Evitar

```
❌ NÃO FAÇA ISSO (God Class):
class AgenteReserva:
    def buscar_voos(self): ...
    def calcular_preco(self): ...
    def processar_pagamento(self): ...
    def emitir_bilhete(self): ...
    def enviar_email(self): ...
    # 2000 linhas de código misturado

✅ FAÇA ISSO (Classes focadas):
class ReservaService:          # Só lógica de reserva
class ReservaRepository:       # Só acesso a dados de reserva
class ReservaController:       # Só rotas HTTP de reserva
class ReservaValidator:        # Só validação de dados
```

---

## 2. Arquitetura Geral

### 2.1 Visão Macro

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                      │
│  Components → Hooks → Services → API Client             │
└──────────────────────┬──────────────────────────────────┘
                       │ HTTP/REST (JSON)
┌──────────────────────▼──────────────────────────────────┐
│                   BACKEND (FastAPI)                       │
│                                                          │
│  ┌──────────┐   ┌──────────┐   ┌──────────────────┐    │
│  │Controller│──▶│ Service  │──▶│   Repository     │    │
│  │ (View)   │   │ (Control)│   │   (Model/Data)   │    │
│  └──────────┘   └──────────┘   └──────────────────┘    │
│       │              │                   │              │
│       │         ┌────▼────┐        ┌─────▼──────┐      │
│       │         │Validator│        │ PostgreSQL │      │
│       │         └─────────┘        └────────────┘      │
│       │                                                  │
│  ┌────▼──────────────────────────────────┐              │
│  │       Singleton Services              │              │
│  │  ConfigManager · EventBus · DBPool    │              │
│  └───────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Padrão MVC Aplicado

```
MVC no FastAPI:
├── Model      → models/ + repositories/    (dados + acesso)
├── View       → controllers/ (routers)     (entrada/saída HTTP)
└── Controller → services/                  (lógica de negócio)
```

| Camada | Responsabilidade | Onde fica | Pode acessar |
|--------|-----------------|-----------|--------------|
| **Controller (Router)** | Receber HTTP, validar input, retornar response | `controllers/` | Service |
| **Service** | Lógica de negócio, orquestração | `services/` | Repository, outros Services |
| **Repository** | CRUD no banco, queries | `repositories/` | Model (SQLAlchemy) |
| **Model** | Esquema do banco (tabelas) | `models/` | Nada (é passivo) |
| **Schema** | Validação de request/response (Pydantic) | `schemas/` | Nada (é passivo) |
| **Validator** | Regras de validação de negócio | `validators/` | Nada (funções puras) |

---

## 3. Estrutura de Diretórios

### 3.1 Backend (FastAPI)

```
backend/
├── main.py                          # Entrypoint FastAPI
├── config.py                        # Singleton de configuração
├── database.py                      # Singleton de conexão DB
├── event_bus.py                     # Singleton de eventos entre agentes
│
├── agents/                          # Cada agente é um módulo independente
│   ├── __init__.py
│   │
│   ├── orquestrador/
│   │   ├── __init__.py
│   │   ├── controller.py            # Rotas: POST /api/pipeline/start
│   │   ├── service.py               # Lógica de orquestração
│   │   ├── saga.py                  # Saga pattern (rollback)
│   │   └── schemas.py               # DTOs de request/response
│   │
│   ├── busca_voos/
│   │   ├── __init__.py
│   │   ├── controller.py            # Rotas: GET /api/voos/buscar
│   │   ├── service.py               # Lógica de busca
│   │   ├── repository.py            # Acesso ao cache + GDS
│   │   ├── gds_client.py            # Cliente para Amadeus/Sabre
│   │   ├── models.py                # Tabela de cache de busca
│   │   ├── schemas.py               # BuscaRequest, VooResponse
│   │   └── validators.py            # Validação de parâmetros
│   │
│   ├── precificacao/
│   │   ├── __init__.py
│   │   ├── controller.py            # Rotas: POST /api/preco/calcular
│   │   ├── service.py               # Cálculo de preço
│   │   ├── dynamic_pricing.py       # Regras de demanda/sazonalidade
│   │   ├── discount_engine.py       # Motor de descontos e cupons
│   │   ├── models.py                # Tabelas de regras de preço
│   │   ├── schemas.py               # PrecoRequest, PrecoResponse
│   │   └── validators.py            # Validação de cupons
│   │
│   ├── reserva/
│   │   ├── __init__.py
│   │   ├── controller.py            # Rotas: POST /api/reserva
│   │   ├── service.py               # Lógica de reserva
│   │   ├── repository.py            # CRUD de reservas
│   │   ├── pnr_generator.py         # Geração de PNR único
│   │   ├── seat_manager.py          # Gerenciamento de assentos
│   │   ├── models.py                # Tabelas: reserva, passageiro
│   │   ├── schemas.py               # ReservaRequest, PNRResponse
│   │   └── validators.py            # CPF, passaporte, menor
│   │
│   ├── pagamento/
│   │   ├── __init__.py
│   │   ├── controller.py            # Rotas: POST /api/pagamento
│   │   ├── service.py               # Lógica de pagamento
│   │   ├── repository.py            # CRUD de transações
│   │   ├── gateway_client.py        # Cliente para gateway de pagamento
│   │   ├── fraud_detector.py        # Motor antifraude
│   │   ├── pix_service.py           # Lógica específica PIX
│   │   ├── refund_service.py        # Lógica de reembolso
│   │   ├── models.py                # Tabelas: transacao, parcela
│   │   ├── schemas.py               # PagamentoRequest, RecibResponse
│   │   └── validators.py            # Validação de cartão
│   │
│   ├── emissao/
│   │   ├── __init__.py
│   │   ├── controller.py            # Rotas: POST /api/bilhete/emitir
│   │   ├── service.py               # Lógica de emissão
│   │   ├── repository.py            # CRUD de bilhetes
│   │   ├── ticket_generator.py      # Geração de e-ticket
│   │   ├── boarding_pass.py         # Geração de boarding pass PDF
│   │   ├── bsp_client.py            # Integração BSP
│   │   ├── models.py                # Tabela: bilhete, cupom_voo
│   │   └── schemas.py               # BilheteResponse
│   │
│   ├── marketing/
│   │   ├── __init__.py
│   │   ├── controller.py            # Rotas: POST /api/marketing/campanha
│   │   ├── service.py               # Lógica de campanhas
│   │   ├── repository.py            # CRUD de campanhas
│   │   ├── segmentation_engine.py   # Motor de segmentação
│   │   ├── campaign_builder.py      # Montagem de campanha
│   │   ├── ab_testing.py            # Motor de A/B testing
│   │   ├── analytics_service.py     # Métricas de conversão
│   │   ├── models.py                # Tabelas: campanha, segmento
│   │   └── schemas.py               # CampanhaRequest, MetricasResponse
│   │
│   ├── atendimento/
│   │   ├── __init__.py
│   │   ├── controller.py            # Rotas: POST /api/atendimento/chat
│   │   ├── service.py               # Lógica de atendimento
│   │   ├── repository.py            # CRUD de atendimentos
│   │   ├── faq_engine.py            # Motor de FAQ
│   │   ├── sentiment_analyzer.py    # Análise de sentimento
│   │   ├── escalation_service.py    # Escalação para humano
│   │   ├── models.py                # Tabela: atendimento, protocolo
│   │   └── schemas.py               # ChatRequest, ChatResponse
│   │
│   ├── notificacoes/
│   │   ├── __init__.py
│   │   ├── controller.py            # Rotas: POST /api/notificacao/enviar
│   │   ├── service.py               # Lógica de notificação
│   │   ├── repository.py            # CRUD de notificações
│   │   ├── email_sender.py          # Envio de e-mail
│   │   ├── sms_sender.py            # Envio de SMS
│   │   ├── push_sender.py           # Envio de push
│   │   ├── template_engine.py       # Templates por idioma
│   │   ├── models.py                # Tabela: notificacao
│   │   └── schemas.py               # NotificacaoRequest
│   │
│   └── fidelidade/
│       ├── __init__.py
│       ├── controller.py            # Rotas: POST /api/fidelidade/acumular
│       ├── service.py               # Lógica de milhas
│       ├── repository.py            # CRUD de milhas
│       ├── miles_calculator.py      # Cálculo de milhas por trecho
│       ├── tier_manager.py          # Gestão de níveis
│       ├── redemption_service.py    # Resgate de milhas
│       ├── models.py                # Tabelas: conta_milhas, transacao_milhas
│       └── schemas.py               # MilhasResponse, ExtratoResponse
│
├── shared/                          # Código compartilhado entre agentes
│   ├── __init__.py
│   ├── base_repository.py          # Repository base (CRUD genérico)
│   ├── base_service.py             # Service base
│   ├── exceptions.py               # Exceções customizadas
│   ├── middleware.py                # Middleware de logging, CORS
│   ├── circuit_breaker.py          # Implementação de circuit breaker
│   └── retry.py                    # Retry com backoff exponencial
│
├── tests/
│   ├── conftest.py
│   ├── agents/
│   │   ├── test_busca_service.py
│   │   ├── test_reserva_service.py
│   │   ├── test_pagamento_service.py
│   │   └── ...
│   └── integration/
│       ├── test_pipeline_completo.py
│       └── test_saga_rollback.py
│
├── alembic/                         # Migrations do banco
│   └── versions/
├── alembic.ini
├── requirements.txt
└── Dockerfile
```

### 3.2 Frontend (React)

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── index.js
│   ├── App.js
│   ├── App.css
│   │
│   ├── api/                         # Camada de comunicação com backend
│   │   ├── apiClient.js             # Singleton Axios configurado
│   │   ├── voosApi.js               # Endpoints de voos
│   │   ├── reservaApi.js            # Endpoints de reserva
│   │   ├── pagamentoApi.js          # Endpoints de pagamento
│   │   ├── marketingApi.js          # Endpoints de marketing
│   │   └── fidelidadeApi.js         # Endpoints de fidelidade
│   │
│   ├── components/                  # Componentes reutilizáveis (sem lógica de negócio)
│   │   ├── common/
│   │   │   ├── Button.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── Modal.jsx
│   │   │   ├── Loading.jsx
│   │   │   ├── Alert.jsx
│   │   │   ├── Badge.jsx
│   │   │   ├── Input.jsx
│   │   │   └── Select.jsx
│   │   ├── layout/
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   └── PageContainer.jsx
│   │   ├── voos/
│   │   │   ├── FlightCard.jsx       # Card de um voo
│   │   │   ├── FlightList.jsx       # Lista de voos
│   │   │   ├── FlightFilters.jsx    # Barra de filtros
│   │   │   ├── SeatMap.jsx          # Mapa de assentos
│   │   │   └── PriceBreakdown.jsx   # Breakdown de preço
│   │   ├── reserva/
│   │   │   ├── PassengerForm.jsx    # Formulário de passageiro
│   │   │   ├── BookingSummary.jsx   # Resumo da reserva
│   │   │   └── SeatSelector.jsx     # Seletor de assento
│   │   ├── pagamento/
│   │   │   ├── CreditCardForm.jsx   # Formulário de cartão
│   │   │   ├── PixPayment.jsx       # QR Code PIX
│   │   │   ├── BoletoPayment.jsx    # Geração de boleto
│   │   │   ├── InstallmentSelect.jsx# Seletor de parcelas
│   │   │   └── PaymentReceipt.jsx   # Comprovante
│   │   ├── marketing/
│   │   │   ├── PromoBanner.jsx      # Banner promocional
│   │   │   ├── CouponInput.jsx      # Input de cupom
│   │   │   └── DestinationCard.jsx  # Card de destino
│   │   └── fidelidade/
│   │       ├── MilesBalance.jsx     # Saldo de milhas
│   │       ├── TierBadge.jsx        # Badge de nível
│   │       └── MilesStatement.jsx   # Extrato de milhas
│   │
│   ├── pages/                       # Páginas (composição de components)
│   │   ├── HomePage.jsx
│   │   ├── SearchResultsPage.jsx
│   │   ├── BookingPage.jsx
│   │   ├── PaymentPage.jsx
│   │   ├── ConfirmationPage.jsx
│   │   ├── MyTripsPage.jsx
│   │   ├── ProfilePage.jsx
│   │   ├── LoyaltyPage.jsx
│   │   └── SupportPage.jsx
│   │
│   ├── hooks/                       # Custom hooks (lógica reutilizável)
│   │   ├── useFlightSearch.js       # Hook de busca de voos
│   │   ├── useBooking.js            # Hook de reserva
│   │   ├── usePayment.js            # Hook de pagamento
│   │   ├── useAuth.js               # Hook de autenticação
│   │   ├── useLoyalty.js            # Hook de fidelidade
│   │   └── useNotification.js       # Hook de notificações
│   │
│   ├── context/                     # React Context (estado global)
│   │   ├── AuthContext.jsx
│   │   ├── BookingContext.jsx       # Estado do pipeline de compra
│   │   └── NotificationContext.jsx
│   │
│   ├── utils/                       # Funções utilitárias puras
│   │   ├── formatters.js            # Formatação de preço, data
│   │   ├── validators.js            # Validação de CPF, email
│   │   └── constants.js             # Constantes globais
│   │
│   └── styles/
│       ├── variables.css            # Design tokens
│       ├── global.css               # Estilos globais
│       └── components/              # CSS por componente
│           ├── FlightCard.css
│           ├── SeatMap.css
│           └── ...
│
├── package.json
├── vite.config.js
└── Dockerfile
```

---

## 4. Padrão Singleton — Implementações

### 4.1 Singleton de Configuração (Backend)

```python
# backend/config.py
"""
Singleton de configuração.
Carrega variáveis de ambiente UMA vez e reutiliza em toda a aplicação.
"""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação. Carregadas do .env."""

    # Banco de dados
    database_url: str = "postgresql://user:pass@localhost:5432/skyagent"

    # Redis (cache)
    redis_url: str = "redis://localhost:6379/0"

    # API Keys dos GDS
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

    class Config:
        env_file = ".env"


@lru_cache()  # ← SINGLETON via cache: instância única
def get_settings() -> Settings:
    """Retorna instância única de Settings."""
    return Settings()
```

### 4.2 Singleton de Banco de Dados (Backend)

```python
# backend/database.py
"""
Singleton de conexão com o banco.
Pool de conexões criado UMA vez, reutilizado em toda a aplicação.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import get_settings

settings = get_settings()

# Engine SINGLETON — criado uma única vez no import
engine = create_engine(
    settings.database_url,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,  # Verifica conexão antes de usar
)

# Session factory SINGLETON
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para todos os models
Base = declarative_base()


def get_db():
    """Dependency injection: gera sessão por request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 4.3 Singleton de Event Bus (Backend)

```python
# backend/event_bus.py
"""
Singleton de Event Bus para comunicação entre agentes.
Padrão Publish/Subscribe desacoplado.
"""
from typing import Callable
from collections import defaultdict


class EventBus:
    """Bus de eventos para comunicação entre agentes."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._subscribers = defaultdict(list)
        return cls._instance

    def subscribe(self, event_type: str, handler: Callable) -> None:
        """Registra um handler para um tipo de evento."""
        self._subscribers[event_type].append(handler)

    def publish(self, event_type: str, data: dict) -> None:
        """Publica um evento para todos os handlers registrados."""
        for handler in self._subscribers[event_type]:
            handler(data)

    def clear(self) -> None:
        """Limpa todos os subscribers (útil para testes)."""
        self._subscribers.clear()


# Instância singleton global
event_bus = EventBus()

# Tipos de eventos (constantes)
class Events:
    PAGAMENTO_CONFIRMADO = "pagamento.confirmado"
    PAGAMENTO_RECUSADO = "pagamento.recusado"
    BILHETE_EMITIDO = "bilhete.emitido"
    RESERVA_CRIADA = "reserva.criada"
    RESERVA_CANCELADA = "reserva.cancelada"
    RESERVA_EXPIRADA = "reserva.expirada"
    MILHAS_ACUMULADAS = "milhas.acumuladas"
    CAMPANHA_ENVIADA = "campanha.enviada"
```

### 4.4 Singleton de API Client (Frontend React)

```javascript
// frontend/src/api/apiClient.js
/**
 * Singleton do cliente HTTP Axios.
 * Configurado UMA vez com base URL, interceptors e headers.
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Instância SINGLETON — criada uma única vez
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor de request: adiciona token de autenticação
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor de response: trata erros globalmente
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

---

## 5. Camada MVC — Exemplos de Código

### 5.1 Model (SQLAlchemy)

```python
# backend/agents/reserva/models.py
"""
Model: Representação das tabelas no banco.
Sem lógica de negócio — apenas estrutura de dados.
"""
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from database import Base


class StatusReserva(enum.Enum):
    PENDENTE = "pendente_pagamento"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    EXPIRADA = "expirada"


class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    pnr = Column(String(6), unique=True, index=True, nullable=False)
    status = Column(Enum(StatusReserva), default=StatusReserva.PENDENTE)
    voo_ida = Column(String(10), nullable=False)
    voo_volta = Column(String(10), nullable=True)
    data_ida = Column(DateTime, nullable=False)
    data_volta = Column(DateTime, nullable=True)
    origem = Column(String(3), nullable=False)
    destino = Column(String(3), nullable=False)
    classe = Column(String(20), default="economica")
    valor_total = Column(Float, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)
    expira_em = Column(DateTime, nullable=False)

    # Relacionamentos
    passageiros = relationship("Passageiro", back_populates="reserva")


class Passageiro(Base):
    __tablename__ = "passageiros"

    id = Column(Integer, primary_key=True, index=True)
    reserva_id = Column(Integer, ForeignKey("reservas.id"))
    nome = Column(String(100), nullable=False)
    sobrenome = Column(String(100), nullable=False)
    cpf = Column(String(14), nullable=True)
    passaporte = Column(String(20), nullable=True)
    data_nascimento = Column(DateTime, nullable=False)
    tipo = Column(String(10), default="ADT")  # ADT, CHD, INF
    assento = Column(String(4), nullable=True)
    email = Column(String(100), nullable=True)
    telefone = Column(String(20), nullable=True)

    reserva = relationship("Reserva", back_populates="passageiros")
```

### 5.2 Schema (Pydantic — Validação de I/O)

```python
# backend/agents/reserva/schemas.py
"""
Schemas Pydantic: validação de entrada/saída.
Separados do Model para manter responsabilidades claras.
"""
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional


class PassageiroInput(BaseModel):
    """Dados de entrada de um passageiro."""
    nome: str
    sobrenome: str
    cpf: Optional[str] = None
    passaporte: Optional[str] = None
    data_nascimento: datetime
    tipo: str = "ADT"
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None

    @field_validator("nome", "sobrenome")
    @classmethod
    def nome_nao_vazio(cls, v):
        if not v or not v.strip():
            raise ValueError("Nome não pode ser vazio")
        return v.strip()


class ReservaRequest(BaseModel):
    """Request para criar uma reserva."""
    voo_ida: str
    voo_volta: Optional[str] = None
    data_ida: datetime
    data_volta: Optional[datetime] = None
    origem: str
    destino: str
    classe: str = "economica"
    passageiros: list[PassageiroInput]


class ReservaResponse(BaseModel):
    """Response com dados da reserva criada."""
    pnr: str
    status: str
    voo_ida: str
    origem: str
    destino: str
    valor_total: float
    expira_em: datetime
    passageiros: list[PassageiroInput]

    class Config:
        from_attributes = True
```

### 5.3 Repository (Acesso a Dados)

```python
# backend/agents/reserva/repository.py
"""
Repository: CRUD puro. Sem lógica de negócio.
Faz UMA coisa: acesso ao banco de dados.
"""
from sqlalchemy.orm import Session
from .models import Reserva, Passageiro, StatusReserva
from typing import Optional


class ReservaRepository:
    """Acesso a dados de reserva. Sem lógica de negócio."""

    def __init__(self, db: Session):
        self.db = db

    def criar(self, reserva: Reserva) -> Reserva:
        """Insere reserva no banco."""
        self.db.add(reserva)
        self.db.commit()
        self.db.refresh(reserva)
        return reserva

    def buscar_por_pnr(self, pnr: str) -> Optional[Reserva]:
        """Busca reserva pelo código PNR."""
        return self.db.query(Reserva).filter(Reserva.pnr == pnr).first()

    def atualizar_status(self, pnr: str, novo_status: StatusReserva) -> bool:
        """Atualiza status da reserva."""
        reserva = self.buscar_por_pnr(pnr)
        if not reserva:
            return False
        reserva.status = novo_status
        self.db.commit()
        return True

    def buscar_expiradas(self) -> list[Reserva]:
        """Busca reservas que passaram do timeout."""
        from datetime import datetime
        return (
            self.db.query(Reserva)
            .filter(Reserva.status == StatusReserva.PENDENTE)
            .filter(Reserva.expira_em < datetime.utcnow())
            .all()
        )

    def adicionar_passageiro(self, passageiro: Passageiro) -> Passageiro:
        """Adiciona passageiro a uma reserva."""
        self.db.add(passageiro)
        self.db.commit()
        self.db.refresh(passageiro)
        return passageiro
```

### 5.4 Validator (Regras de Validação)

```python
# backend/agents/reserva/validators.py
"""
Validator: funções puras de validação.
Sem acesso ao banco. Sem side effects. Fácil de testar.
"""
from datetime import datetime, timedelta


def validar_cpf(cpf: str) -> tuple[bool, str]:
    """Valida CPF brasileiro. Retorna (válido, mensagem)."""
    cpf = cpf.replace(".", "").replace("-", "")

    if len(cpf) != 11:
        return False, "CPF deve ter 11 dígitos"

    if cpf == cpf[0] * 11:
        return False, "CPF inválido"

    # Cálculo do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    d1 = 11 - (soma % 11)
    d1 = 0 if d1 >= 10 else d1

    # Cálculo do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    d2 = 11 - (soma % 11)
    d2 = 0 if d2 >= 10 else d2

    if int(cpf[9]) != d1 or int(cpf[10]) != d2:
        return False, "CPF inválido"

    return True, "OK"


def validar_passaporte_validade(
    validade: datetime,
    data_viagem: datetime,
    meses_minimos: int = 6
) -> tuple[bool, str]:
    """Valida se passaporte tem validade mínima."""
    limite = data_viagem + timedelta(days=meses_minimos * 30)
    if validade < limite:
        return False, f"Passaporte deve ter validade mínima de {meses_minimos} meses"
    return True, "OK"


def validar_menor_acompanhado(
    idade: int,
    tem_acompanhante: bool,
    tem_autorizacao_umnr: bool
) -> tuple[bool, str]:
    """Valida regras de menor de idade."""
    if idade < 12 and not tem_acompanhante and not tem_autorizacao_umnr:
        return False, "Menor de 12 anos requer acompanhante adulto ou autorização"
    return True, "OK"


def validar_assento_emergencia(idade: int) -> tuple[bool, str]:
    """Valida se passageiro pode sentar na saída de emergência."""
    if idade < 18:
        return False, "Menores de 18 anos não podem sentar na saída de emergência"
    return True, "OK"
```

### 5.5 Service (Lógica de Negócio)

```python
# backend/agents/reserva/service.py
"""
Service: lógica de negócio da reserva.
Orquestra validators, repository e outros serviços.
NÃO acessa o banco diretamente — delega ao Repository.
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .repository import ReservaRepository
from .pnr_generator import PNRGenerator
from .seat_manager import SeatManager
from .models import Reserva, Passageiro, StatusReserva
from .schemas import ReservaRequest, ReservaResponse
from . import validators
from shared.exceptions import ValidationError, NotFoundError
from config import get_settings
from event_bus import event_bus, Events


class ReservaService:
    """
    Lógica de negócio de reserva.
    Máx. 200 linhas. Se crescer, extraia para classes menores.
    """

    def __init__(self, db: Session):
        self.repo = ReservaRepository(db)
        self.pnr_gen = PNRGenerator(db)
        self.seat_mgr = SeatManager(db)
        self.settings = get_settings()

    def criar_reserva(self, request: ReservaRequest) -> ReservaResponse:
        """Cria uma nova reserva com validação completa."""
        # 1. Validar passageiros
        self._validar_passageiros(request)

        # 2. Gerar PNR único
        pnr = self.pnr_gen.gerar()

        # 3. Calcular expiração
        expira_em = datetime.utcnow() + timedelta(
            minutes=self.settings.booking_hold_minutes
        )

        # 4. Criar reserva no banco
        reserva = Reserva(
            pnr=pnr,
            voo_ida=request.voo_ida,
            voo_volta=request.voo_volta,
            data_ida=request.data_ida,
            data_volta=request.data_volta,
            origem=request.origem,
            destino=request.destino,
            classe=request.classe,
            valor_total=0,  # Será preenchido pelo Agente de Precificação
            expira_em=expira_em,
        )
        reserva = self.repo.criar(reserva)

        # 5. Adicionar passageiros
        for p in request.passageiros:
            passageiro = Passageiro(
                reserva_id=reserva.id,
                nome=p.nome,
                sobrenome=p.sobrenome,
                cpf=p.cpf,
                passaporte=p.passaporte,
                data_nascimento=p.data_nascimento,
                tipo=p.tipo,
                email=p.email,
                telefone=p.telefone,
            )
            self.repo.adicionar_passageiro(passageiro)

        # 6. Bloquear assentos
        self.seat_mgr.bloquear_assentos(
            voo=request.voo_ida,
            qtd=len(request.passageiros),
            expira_em=expira_em,
        )

        # 7. Publicar evento
        event_bus.publish(Events.RESERVA_CRIADA, {"pnr": pnr})

        return ReservaResponse(
            pnr=pnr,
            status="pendente_pagamento",
            voo_ida=request.voo_ida,
            origem=request.origem,
            destino=request.destino,
            valor_total=0,
            expira_em=expira_em,
            passageiros=request.passageiros,
        )

    def cancelar_reserva(self, pnr: str) -> bool:
        """Cancela reserva e libera assentos."""
        reserva = self.repo.buscar_por_pnr(pnr)
        if not reserva:
            raise NotFoundError(f"Reserva {pnr} não encontrada")

        self.repo.atualizar_status(pnr, StatusReserva.CANCELADA)
        self.seat_mgr.liberar_assentos(reserva.voo_ida)
        event_bus.publish(Events.RESERVA_CANCELADA, {"pnr": pnr})
        return True

    def _validar_passageiros(self, request: ReservaRequest) -> None:
        """Valida todos os passageiros. Lança exceção se inválido."""
        for p in request.passageiros:
            # Validar CPF (voos nacionais)
            if p.cpf:
                valido, msg = validators.validar_cpf(p.cpf)
                if not valido:
                    raise ValidationError(msg)

            # Validar passaporte (voos internacionais)
            if p.passaporte:
                # Validação simplificada aqui
                pass

            # Validar menor
            from dateutil.relativedelta import relativedelta
            idade = relativedelta(datetime.utcnow(), p.data_nascimento).years
            tem_adulto = any(
                pa.tipo == "ADT" for pa in request.passageiros
            )
            valido, msg = validators.validar_menor_acompanhado(
                idade, tem_adulto, False
            )
            if not valido:
                raise ValidationError(msg)
```

### 5.6 Controller (Rotas FastAPI)

```python
# backend/agents/reserva/controller.py
"""
Controller (View no MVC): define rotas HTTP.
Sem lógica de negócio — delega tudo ao Service.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from .service import ReservaService
from .schemas import ReservaRequest, ReservaResponse
from shared.exceptions import ValidationError, NotFoundError

router = APIRouter(prefix="/api/reserva", tags=["Reserva"])


@router.post("/", response_model=ReservaResponse, status_code=201)
def criar_reserva(request: ReservaRequest, db: Session = Depends(get_db)):
    """Cria uma nova reserva de voo."""
    try:
        service = ReservaService(db)
        return service.criar_reserva(request)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/{pnr}", response_model=ReservaResponse)
def buscar_reserva(pnr: str, db: Session = Depends(get_db)):
    """Busca reserva pelo código PNR."""
    service = ReservaService(db)
    reserva = service.repo.buscar_por_pnr(pnr)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    return reserva


@router.delete("/{pnr}", status_code=204)
def cancelar_reserva(pnr: str, db: Session = Depends(get_db)):
    """Cancela uma reserva existente."""
    try:
        service = ReservaService(db)
        service.cancelar_reserva(pnr)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{pnr}/assento")
def selecionar_assento(
    pnr: str,
    passageiro_id: int,
    assento: str,
    db: Session = Depends(get_db),
):
    """Seleciona assento para um passageiro da reserva."""
    service = ReservaService(db)
    # Delegação para o serviço
    return {"message": f"Assento {assento} atribuído com sucesso"}
```

### 5.7 Entrypoint (main.py)

```python
# backend/main.py
"""
Entrypoint da aplicação FastAPI.
Registra rotas, middleware e configura CORS.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import get_settings

# Importar controllers (routers)
from agents.orquestrador.controller import router as orquestrador_router
from agents.busca_voos.controller import router as busca_router
from agents.precificacao.controller import router as precificacao_router
from agents.reserva.controller import router as reserva_router
from agents.pagamento.controller import router as pagamento_router
from agents.emissao.controller import router as emissao_router
from agents.marketing.controller import router as marketing_router
from agents.atendimento.controller import router as atendimento_router
from agents.notificacoes.controller import router as notificacoes_router
from agents.fidelidade.controller import router as fidelidade_router

settings = get_settings()

app = FastAPI(
    title="SkyAgent API",
    description="Plataforma Multi-Agente para Venda de Passagens Aéreas",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rotas de cada agente
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
    """Health check do sistema."""
    return {"status": "healthy", "version": "1.0.0"}
```

---

## 6. Frontend React — Exemplos de Código

### 6.1 API Service (camada de acesso)

```javascript
// frontend/src/api/voosApi.js
/**
 * API de Voos: funções focadas em UMA responsabilidade.
 * Não contém lógica de UI — apenas chamadas HTTP.
 */
import apiClient from './apiClient';

export const buscarVoos = async (params) => {
  const { data } = await apiClient.get('/voos/buscar', { params });
  return data;
};

export const buscarDetalhesVoo = async (vooId) => {
  const { data } = await apiClient.get(`/voos/${vooId}`);
  return data;
};

export const buscarMapaAssentos = async (vooId) => {
  const { data } = await apiClient.get(`/voos/${vooId}/assentos`);
  return data;
};
```

### 6.2 Custom Hook (lógica reutilizável)

```javascript
// frontend/src/hooks/useFlightSearch.js
/**
 * Hook de busca de voos.
 * Encapsula estado de loading, erro e dados.
 * Componentes ficam LIMPOS e focados em UI.
 */
import { useState, useCallback } from 'react';
import { buscarVoos } from '../api/voosApi';

export function useFlightSearch() {
  const [flights, setFlights] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const search = useCallback(async (params) => {
    setLoading(true);
    setError(null);
    try {
      const data = await buscarVoos(params);
      setFlights(data.voos);
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao buscar voos');
    } finally {
      setLoading(false);
    }
  }, []);

  const clearResults = useCallback(() => {
    setFlights([]);
    setError(null);
  }, []);

  return { flights, loading, error, search, clearResults };
}
```

### 6.3 Componente Focado (sem lógica de negócio)

```jsx
// frontend/src/components/voos/FlightCard.jsx
/**
 * FlightCard: exibe informações de UM voo.
 * Sem lógica de negócio. Recebe dados via props.
 * ~50 linhas. Limpo. Reutilizável.
 */
import { formatCurrency, formatTime, formatDuration } from '../../utils/formatters';
import './FlightCard.css';

export default function FlightCard({ flight, onSelect }) {
  return (
    <div className="flight-card" onClick={() => onSelect(flight)}>
      <div className="flight-card__airline">
        <img src={flight.companhia.logo} alt={flight.companhia.nome} />
        <span>{flight.companhia.nome}</span>
        <span className="flight-card__number">{flight.numero}</span>
      </div>

      <div className="flight-card__times">
        <div className="flight-card__departure">
          <strong>{formatTime(flight.partida)}</strong>
          <span>{flight.origem}</span>
        </div>

        <div className="flight-card__duration">
          <span>{formatDuration(flight.duracao)}</span>
          <div className="flight-card__line" />
          <span>{flight.escalas === 0 ? 'Direto' : `${flight.escalas} escala(s)`}</span>
        </div>

        <div className="flight-card__arrival">
          <strong>{formatTime(flight.chegada)}</strong>
          <span>{flight.destino}</span>
        </div>
      </div>

      <div className="flight-card__price">
        <span className="flight-card__price-label">a partir de</span>
        <strong>{formatCurrency(flight.preco)}</strong>
        <span className="flight-card__baggage">
          {flight.bagagem_inclusa ? '✓ Bagagem inclusa' : 'Sem bagagem'}
        </span>
      </div>
    </div>
  );
}
```

### 6.4 Página (composição de componentes)

```jsx
// frontend/src/pages/SearchResultsPage.jsx
/**
 * Página de resultados de busca.
 * Compõe componentes. A lógica está no Hook.
 */
import { useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useFlightSearch } from '../hooks/useFlightSearch';
import FlightList from '../components/voos/FlightList';
import FlightFilters from '../components/voos/FlightFilters';
import Loading from '../components/common/Loading';
import Alert from '../components/common/Alert';
import PageContainer from '../components/layout/PageContainer';

export default function SearchResultsPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { flights, loading, error, search } = useFlightSearch();

  useEffect(() => {
    const params = {
      origem: searchParams.get('origem'),
      destino: searchParams.get('destino'),
      data_ida: searchParams.get('data_ida'),
      data_volta: searchParams.get('data_volta'),
      classe: searchParams.get('classe') || 'economica',
      adultos: searchParams.get('adultos') || 1,
    };
    search(params);
  }, [searchParams, search]);

  const handleSelectFlight = (flight) => {
    navigate(`/reserva?voo=${flight.numero}&data=${flight.data}`);
  };

  return (
    <PageContainer title="Resultados da Busca">
      <FlightFilters onFilter={(filters) => search({ ...filters })} />

      {loading && <Loading message="Buscando os melhores voos..." />}
      {error && <Alert type="error" message={error} />}
      {!loading && flights.length === 0 && (
        <Alert type="info" message="Nenhum voo encontrado. Tente datas flexíveis." />
      )}

      <FlightList flights={flights} onSelect={handleSelectFlight} />
    </PageContainer>
  );
}
```

---

## 7. Endpoints da API (Catálogo)

### 7.1 Tabela Completa de Endpoints

| Agente | Método | Endpoint | Descrição |
|--------|--------|----------|-----------|
| **Orquestrador** | POST | `/api/pipeline/start` | Inicia pipeline de venda |
| | GET | `/api/pipeline/{session_id}/status` | Status do pipeline |
| | POST | `/api/pipeline/{session_id}/rollback` | Rollback manual |
| **Busca** | GET | `/api/voos/buscar` | Busca de voos com filtros |
| | GET | `/api/voos/{voo_id}` | Detalhes de um voo |
| | GET | `/api/voos/{voo_id}/assentos` | Mapa de assentos |
| | GET | `/api/voos/aeroportos` | Lista de aeroportos |
| **Precificação** | POST | `/api/preco/calcular` | Calcula preço de um voo |
| | POST | `/api/preco/cupom/validar` | Valida cupom promocional |
| | GET | `/api/preco/cotacao/{id}` | Recupera cotação salva |
| **Reserva** | POST | `/api/reserva` | Cria reserva |
| | GET | `/api/reserva/{pnr}` | Busca reserva por PNR |
| | PUT | `/api/reserva/{pnr}` | Altera reserva |
| | DELETE | `/api/reserva/{pnr}` | Cancela reserva |
| | PUT | `/api/reserva/{pnr}/assento` | Seleciona assento |
| | POST | `/api/reserva/{pnr}/servicos` | Adiciona serviço extra |
| **Pagamento** | POST | `/api/pagamento/cartao` | Paga com cartão |
| | POST | `/api/pagamento/pix` | Gera QR Code PIX |
| | POST | `/api/pagamento/boleto` | Gera boleto |
| | GET | `/api/pagamento/{id}/status` | Status do pagamento |
| | POST | `/api/pagamento/{id}/reembolso` | Solicita reembolso |
| | POST | `/api/pagamento/webhook/pix` | Webhook PIX |
| **Emissão** | POST | `/api/bilhete/emitir` | Emite e-ticket |
| | GET | `/api/bilhete/{numero}` | Busca bilhete |
| | GET | `/api/bilhete/{numero}/pdf` | Download boarding pass PDF |
| | POST | `/api/bilhete/{numero}/void` | Void do bilhete |
| | POST | `/api/bilhete/{numero}/reemitir` | Reemite bilhete |
| **Marketing** | POST | `/api/marketing/campanha` | Cria campanha |
| | GET | `/api/marketing/campanha/{id}` | Detalhes da campanha |
| | GET | `/api/marketing/metricas` | Métricas de conversão |
| | POST | `/api/marketing/segmento` | Cria segmento |
| | GET | `/api/marketing/ofertas/{cliente_id}` | Ofertas personalizadas |
| **Atendimento** | POST | `/api/atendimento/chat` | Envia mensagem no chat |
| | GET | `/api/atendimento/{protocolo}` | Histórico de atendimento |
| | POST | `/api/atendimento/escalar` | Escalar para humano |
| **Notificações** | POST | `/api/notificacao/enviar` | Envia notificação |
| | GET | `/api/notificacao/{id}/status` | Status de entrega |
| | PUT | `/api/notificacao/preferencias` | Atualiza preferências |
| **Fidelidade** | GET | `/api/fidelidade/{cliente_id}/saldo` | Saldo de milhas |
| | POST | `/api/fidelidade/acumular` | Acumula milhas |
| | POST | `/api/fidelidade/resgatar` | Resgata milhas |
| | GET | `/api/fidelidade/{cliente_id}/extrato` | Extrato de milhas |
| | GET | `/api/fidelidade/{cliente_id}/nivel` | Nível de fidelidade |

---

## 8. Padrões de Código — Checklist

### 8.1 Backend (Python/FastAPI)

```
✅ Cada agente em seu próprio módulo (pasta)
✅ Controller: máx. 5 rotas por arquivo
✅ Service: máx. 200 linhas, 1 responsabilidade
✅ Repository: CRUD puro, sem lógica de negócio
✅ Validator: funções puras, sem side effects
✅ Schema: Pydantic para validação de I/O
✅ Model: SQLAlchemy, sem lógica
✅ Singleton: Config, DB, EventBus
✅ Exceções customizadas (shared/exceptions.py)
✅ Type hints em TODAS as funções
✅ Docstrings em TODAS as classes e funções públicas
```

### 8.2 Frontend (React)

```
✅ Componentes: máx. 100 linhas JSX
✅ Hooks: encapsulam lógica, componentes ficam limpos
✅ Pages: composição de componentes, sem lógica de negócio
✅ API layer: separada dos componentes (singleton Axios)
✅ Context: estado global mínimo (auth, booking, notif)
✅ Utils: funções puras (formatação, validação)
✅ CSS: arquivo separado por componente
✅ Props bem definidas: nomes descritivos
✅ Sem fetch direto em componentes — sempre via Hook
✅ Sem lógica de negócio em componentes — sempre via Hook
```

### 8.3 Regra Anti-God-Class (Detector)

```
🚨 SINAIS DE GOD CLASS — Quebre imediatamente se detectar:

1. Arquivo com mais de 200 linhas
2. Classe com mais de 10 métodos
3. Método com mais de 30 linhas
4. Import de mais de 10 módulos
5. Classe que acessa banco E envia email E calcula preço
6. Componente React com mais de 3 useEffect
7. Componente que faz fetch E valida E formata E renderiza
```

---

## 9. Docker Compose — Ambiente Completo

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://skyagent:skyagent@db:5432/skyagent
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    environment:
      - VITE_API_URL=http://localhost:8000/api
    command: npm run dev -- --host

  db:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=skyagent
      - POSTGRES_PASSWORD=skyagent
      - POSTGRES_DB=skyagent
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

---

## 10. Comandos para Início Rápido

```bash
# 1. Criar ambiente Python
cd backend
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings alembic psycopg2-binary redis python-dateutil

# 2. Criar projeto React com Vite
cd ../frontend
npx -y create-vite@latest ./ --template react
npm install axios react-router-dom

# 3. Iniciar banco de dados
docker compose up db redis -d

# 4. Rodar migrations
cd ../backend
alembic upgrade head

# 5. Iniciar backend
uvicorn main:app --reload --port 8000

# 6. Iniciar frontend
cd ../frontend
npm run dev

# 7. Acessar
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000/docs (Swagger)
# Health: http://localhost:8000/health
```
