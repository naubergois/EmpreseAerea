# Análise de Tempo de Resposta e Arquitetura — SkyAgent

> Documento técnico com a arquitetura da plataforma multi-agente SkyAgent e a medição
> empírica do tempo de resposta dos seus endpoints HTTP.
>
> Data da medição: **2026-06-26** · Versão da API: **1.0.0**

---

## 1. Resumo Executivo

O SkyAgent é uma plataforma de venda de passagens aéreas organizada como **10 agentes**
(módulos de domínio) expostos por uma única API **FastAPI** (backend) e consumida por um
SPA **React + Vite** (frontend). A persistência é **SQLite** via SQLAlchemy.

Resultados-chave do benchmark (loopback local, 1 worker Uvicorn, 50 repetições):

| Indicador | Valor medido |
|-----------|--------------|
| Latência típica (endpoints CRUD/cálculo, p50) | **1–4 ms** |
| Busca de voos com cache **HIT** (média) | **~4 ms** |
| Busca de voos com cache **MISS** (média) | **~15 ms** |
| Busca com `flex_dias=3` MISS (média) | **~23 ms** |
| Atendimento `/chat` (fallback FAQ, média) | **~38 ms** |
| Throughput (busca, 20 conexões simultâneas) | **~317 req/s** |
| Latência da busca sob 20 conexões (p95) | **~77 ms** (vs ~3 ms isolada) |

**Conclusões principais:**

1. Em carga leve, a aplicação é muito rápida (single-digit ms) — o trabalho é em memória/SQLite local.
2. O **cache de busca** (tabela SQLite) reduz a latência em ~4–5× e é o principal fator de performance do caminho de venda.
3. O maior risco de latência é o **agente de Atendimento**, que depende de uma **LLM externa (DeepSeek)**. Na medição a chave falhou e caiu no fallback de FAQ (~38 ms); **com a LLM ativa, espere de 1 a 5+ segundos** por resposta.
4. Sob concorrência, a latência por requisição degrada ~20× porque os endpoints são **síncronos** (`def`) e o **SQLite serializa** as escritas — gargalo de escalabilidade horizontal.

---

## 2. Arquitetura

### 2.1 Visão Geral

```
┌──────────────────────────┐        HTTP/JSON        ┌───────────────────────────────┐
│   Frontend (React+Vite)  │  ───────────────────▶   │      Backend (FastAPI)        │
│   axios · react-router   │  ◀───────────────────   │  10 routers (1 por agente)    │
│   porta 5173             │                          │  porta 8000                   │
└──────────────────────────┘                          └───────────────┬───────────────┘
                                                                       │
                                          ┌────────────────────────────┼───────────────────────┐
                                          │                            │                       │
                                   ┌──────▼──────┐            ┌────────▼────────┐      ┌────────▼────────┐
                                   │  SQLAlchemy │            │   Event Bus     │      │  LLM externa    │
                                   │  + SQLite   │            │ (pub/sub in-mem)│      │  DeepSeek API   │
                                   └─────────────┘            └─────────────────┘      └─────────────────┘
```

### 2.2 Backend

- **Framework:** FastAPI `0.115` sobre Uvicorn `0.30`.
- **ORM/DB:** SQLAlchemy `2.0` + **SQLite** (`skyagent.db`). `pool_pre_ping=True`, `check_same_thread=False`.
- **Padrão por agente:** cada agente é um pacote em `backend/agents/<agente>/` com a estrutura
  em camadas `controller.py` (rotas) → `service.py` (regra de negócio) → `repository.py`/`models.py` (dados).
- **Configuração:** `config.py` usa `pydantic-settings` com `@lru_cache` (Singleton de `Settings`, lido do `.env`).
- **Ciclo de vida:** `lifespan` executa `init_db()` (cria tabelas) e `seed_data()` (cupons + pré-carregamento de cache de voos) na inicialização.
- **CORS:** liberado para `localhost:5173/5174/3000` e `frontend_url`.

Os 10 agentes (routers):

| Agente | Prefixo | Papel |
|--------|---------|-------|
| Orquestrador (ORC) | `/api/pipeline` | Coordena o pipeline (saga, classificação de intenção, rollback) |
| Busca de Voos (BUS) | `/api/voos` | Pesquisa de voos (cache + circuit breaker) |
| Precificação (PRE) | `/api/preco` | Cálculo de tarifa, cupons, cotação |
| Reserva (RES) | `/api/reservas` | Criação/cancelamento de PNR, assentos |
| Pagamento (PAG) | `/api/pagamentos` | Cartão, PIX, boleto, split, reembolso |
| Emissão (EMI) | `/api/bilhetes` | E-ticket, PDF, void, reemissão |
| Marketing (MKT) | `/api/marketing` | Campanhas, segmentos, métricas, ofertas |
| Atendimento (ATC) | `/api/atendimento` | Chat com LLM + FAQ + análise de sentimento |
| Notificações (NOT) | `/api/notificacoes` | Envio e status de notificações |
| Fidelidade (FID) | `/api/fidelidade` | Saldo, acúmulo, resgate, nível de milhas |

### 2.3 Frontend

- **Stack:** React `18.3`, React Router `6.26`, axios `1.7`, Vite `5.4`.
- **Cliente HTTP:** `apiClient` (axios) com `timeout=15000ms`; em dev usa proxy do Vite, em produção `VITE_API_URL`.
- **Páginas:** Home, SearchResults, Booking, Payment, Confirmation, Loyalty, Support.
- **Estado:** `BookingContext` + hook `useFlightSearch`.

### 2.4 Padrões de Resiliência

- **Circuit Breaker** (`shared/circuit_breaker.py`): por serviço, estados CLOSED/OPEN/HALF_OPEN, abre em 5 falhas (`circuit_breaker_threshold`), reabre após 30s. Usado pelo agente de Busca.
- **Retry com backoff exponencial** (`shared/retry.py`): `base_delay * 2^i`, até `max_retry_attempts` (3).
- **Event Bus** (`event_bus.py`): pub/sub **in-memory** singleton para comunicação entre agentes (ex.: `search.no_results`, `payment.approved`). Sem broker externo.

### 2.5 Cache

Apesar de `config.py` declarar `redis_url`, **o cache de busca é persistido em SQLite**
(tabela `BuscaCache`, `repository.py`), com **TTL de 15 minutos**. O seed pré-carrega rotas
populares para os próximos 30 dias. Implicações de performance medidas na Seção 5.

### 2.6 Infraestrutura

`docker-compose.yml` sobe dois serviços: `backend` (Uvicorn `--reload`, porta 8000) e
`frontend` (Vite, porta 5173). Não há réplica, balanceador, Redis ou banco gerenciado —
topologia de desenvolvimento.

---

## 3. Inventário de Endpoints

| Método | Rota | Agente |
|--------|------|--------|
| GET | `/health` | (app) |
| GET | `/api/pipeline/health` | Orquestrador |
| POST | `/api/pipeline/start` | Orquestrador |
| GET | `/api/pipeline/{session_id}/status` | Orquestrador |
| POST | `/api/pipeline/{session_id}/rollback` | Orquestrador |
| POST | `/api/pipeline/classificar` | Orquestrador |
| GET | `/api/voos/buscar` | Busca |
| GET | `/api/voos/aeroportos` | Busca |
| GET | `/api/voos/{voo_id}/assentos` | Busca |
| POST | `/api/preco/calcular` | Precificação |
| POST | `/api/preco/cupom/validar` | Precificação |
| GET | `/api/preco/cotacao/{cotacao_id}` | Precificação |
| POST | `/api/reservas/` | Reserva |
| GET/DELETE/PUT | `/api/reservas/{pnr}[/assento]` | Reserva |
| POST | `/api/pagamentos/{cartao,pix,boleto,split}` | Pagamento |
| GET/POST | `/api/pagamentos/{txn_id}/{status,reembolso}` | Pagamento |
| POST/GET | `/api/bilhetes/{emitir,…}` | Emissão |
| POST/GET | `/api/marketing/{campanha,segmento,metricas,ofertas}` | Marketing |
| POST/GET | `/api/atendimento/{chat,escalar,{protocolo}}` | Atendimento |
| POST/GET/PUT | `/api/notificacoes/{enviar,…}` | Notificações |
| GET/POST | `/api/fidelidade/{cliente_id}/{saldo,nivel,extrato}` | Fidelidade |

---

## 4. Metodologia do Benchmark

- **Ambiente:** macOS, loopback `127.0.0.1`, **1 worker Uvicorn** sem `--reload`, SQLite local.
- **Ferramenta:** script Python com `httpx` — `scripts/bench.py` (incluído no repositório).
- **Amostragem:** 50 repetições sequenciais por endpoint; reportados min, média, p50, p95, max.
- **Teste de concorrência:** 100 requisições com 20 threads simultâneas no endpoint de busca (cache HIT).
- **Observações:** medições incluem ida-e-volta HTTP local (overhead de rede ~desprezível).
  O endpoint de atendimento foi medido no caminho de **fallback FAQ** (a LLM externa falhou rápido);
  com LLM ativa o tempo é dominado pela latência da DeepSeek (segundos).

Como reproduzir:

```bash
cd backend && source venv/bin/activate
uvicorn main:app --host 127.0.0.1 --port 8020 --log-level warning &
python ../scripts/bench.py http://127.0.0.1:8020 50
```

---

## 5. Resultados Medidos

### 5.1 Latência por endpoint (50 reps, isolado)

| Endpoint | Status | min (ms) | média (ms) | p50 (ms) | p95 (ms) | max (ms) |
|----------|:------:|---------:|-----------:|---------:|---------:|---------:|
| `GET /health` | 200 | 0.5 | 0.9 | 0.7 | 1.7 | 6.9 |
| `GET /api/pipeline/health` | 200 | 0.7 | 1.5 | 1.4 | 2.9 | 3.7 |
| `GET /api/voos/aeroportos` | 200 | 0.8 | 2.0 | 1.7 | 4.8 | 5.6 |
| `GET /api/voos/buscar` (cache HIT) | 200 | 1.7 | 4.4 | 3.3 | 13.1 | 23.2 |
| `GET /api/voos/buscar` (flex=3, HIT) | 200 | 1.5 | 3.3 | 2.7 | 6.5 | 11.1 |
| `GET /api/voos/{id}/assentos` | 200 | 1.1 | 2.8 | 2.0 | 9.7 | 16.2 |
| `POST /api/preco/calcular` | 200 | 2.7 | 5.4 | 4.4 | 9.8 | 22.6 |
| `POST /api/preco/cupom/validar` | 200 | 1.4 | 3.0 | 2.9 | 5.7 | 6.1 |
| `GET /api/marketing/metricas` | 200 | 1.1 | 2.8 | 2.0 | 6.6 | 15.8 |
| `GET /api/fidelidade/{id}/saldo` | 200 | 1.2 | 1.9 | 1.5 | 4.7 | 6.3 |
| `GET /api/fidelidade/{id}/nivel` | 200 | 1.2 | 1.9 | 1.6 | 3.3 | 5.4 |
| `POST /api/atendimento/chat` (fallback FAQ) | 200 | 27.7 | 38.4 | 35.8 | 47.8 | 98.5 |

### 5.2 Efeito do cache de busca

| Cenário | média (ms) | p95 (ms) | max (ms) |
|---------|-----------:|---------:|---------:|
| Busca cache **HIT** | ~4.4 | 13.1 | 23.2 |
| Busca cache **MISS** (rota nova) | ~15.5 | 20.5 | 41.6 |
| Busca cache **MISS + flex=3** | ~23.3 | — | 29.5 |

> O MISS paga geração sintética dos voos + `INSERT/commit` no SQLite. O `flex_dias`
> multiplica o trabalho (gera voos para cada dia da janela), elevando a latência.

### 5.3 Concorrência (busca, cache HIT)

| Métrica | Valor |
|---------|-------|
| Carga | 100 requisições / 20 threads |
| Throughput | **~317 req/s** |
| Latência média sob carga | ~57 ms |
| Latência p95 sob carga | ~77 ms |
| Latência isolada (referência) | ~3 ms |

> Sob 20 conexões simultâneas a latência cresce ~20× em relação ao request isolado:
> sinal claro de serialização (endpoints síncronos + SQLite single-writer).

---

## 6. Análise de Gargalos

1. **Dependência de LLM externa (Atendimento) — maior risco de latência.**
   `/api/atendimento/chat` chama a DeepSeek de forma síncrona com `llm_timeout_seconds=30`.
   Com a LLM ativa, a resposta passa de ~38 ms (FAQ) para **segundos**, e um timeout
   bloqueia o worker por até 30 s. É o ponto que mais impacta a experiência percebida.

2. **Endpoints síncronos (`def`) + SQLite single-writer.**
   As rotas usam funções síncronas e o SQLite serializa escritas. Sob concorrência, a
   latência por request degrada fortemente (Seção 5.3). Escala vertical limitada e
   horizontal inviável com SQLite local.

3. **Cache em SQLite, não em memória/Redis.**
   Mesmo o HIT executa uma `SELECT` no banco e desserializa JSON. Funciona bem em dev,
   mas não compartilha estado entre múltiplas instâncias e adiciona I/O ao caminho quente.

4. **Custo do MISS e do `flex_dias`.**
   MISS gera voos em laços aninhados `origens × destinos × dias` e faz `commit`.
   Buscas multi-aeroporto (ex.: "são paulo" → GRU+CGH) com `flex_dias` alto multiplicam o trabalho.

5. **Event Bus e Circuit Breaker em memória.**
   São singletons de processo: estado se perde a cada restart e não é compartilhado entre
   réplicas. Sem impacto em latência hoje, mas limitam a confiabilidade em escala.

6. **`--reload` em produção (docker-compose).**
   O `uvicorn --reload` adiciona overhead de watcher; adequado só para desenvolvimento.

---

## 7. Recomendações

**Curto prazo (baixo esforço, alto impacto):**

- Tornar a chamada de LLM **assíncrona** e reduzir o timeout efetivo (ex.: 5–8 s) com fallback rápido para FAQ; considerar streaming na UI.
- Promover o cache de busca para **memória de processo** (LRU) à frente do SQLite, ou migrar para **Redis** (já previsto na config).
- Rodar Uvicorn com **múltiplos workers** (`--workers N`) atrás de um proxy, removendo `--reload` em produção.

**Médio prazo:**

- Migrar de SQLite para **PostgreSQL** para suportar concorrência de escrita e múltiplas instâncias.
- Converter endpoints de I/O (atendimento, pagamento, integrações GDS) para `async def` com clientes assíncronos (`httpx.AsyncClient`).
- Externalizar **Event Bus** (ex.: Redis Streams/Kafka) e o estado do **Circuit Breaker**.

**Observabilidade:**

- Adicionar middleware de métricas (latência por rota, taxa de erro, estado dos breakers) e expor `/metrics` (Prometheus).
- Logar `X-Cache` (HIT/MISS) já disponível na busca para monitorar a taxa de acerto do cache.

---

## 8. Melhorias Implementadas (antes × depois)

As seguintes otimizações foram aplicadas e validadas com o mesmo benchmark (50 reps, 1 worker):

1. **Cache L1 em memória de processo** na frente do SQLite (`busca_voos/repository.py`):
   dict com TTL consultado antes do banco, eliminando `SELECT` + `json.loads` do caminho quente.
2. **LLM client assíncrono com pool reutilizável** (`atendimento/llm_client.py`):
   `httpx.AsyncClient` único (keep-alive/TLS reaproveitado) em vez de abrir conexão por request.
3. **Caminho de atendimento `async`** (`controller`/`service`): a chamada à LLM não bloqueia mais o worker.
4. **Timeout da LLM 30s → 8s** (`config.py`): fallback rápido para FAQ em caso de indisponibilidade.
5. **Fechamento do client no shutdown** (`main.py` lifespan): evita vazamento de conexões.

### Resultados comparativos

| Cenário | Antes (média) | Depois (média) | Antes (p95) | Depois (p95) |
|---------|--------------:|---------------:|------------:|-------------:|
| `voos/buscar` cache HIT | 4.4 ms | **1.5 ms** | 13.1 ms | **3.0 ms** |
| `voos/buscar` flex=3 | 3.3 ms | **1.9 ms** | 6.5 ms | **3.8 ms** |
| `atendimento/chat` | 38.4 ms | **9.9 ms** | 47.8 ms | **11.4 ms** |
| Busca sob 20 conexões | 57 ms / 317 req/s | **35.7 ms / 547 req/s** | 77 ms | **52 ms** |

> Ganhos: busca cache HIT **~3×** mais rápida, atendimento **~4×** mais rápido (caminho de
> fallback) e **+73% de throughput** sob concorrência. Todos os 19 testes continuam passando.

**Pendentes (recomendados, não implementados):** múltiplos workers em produção, migração para
PostgreSQL, externalização do Event Bus/Circuit Breaker e middleware de métricas (Seção 7).

---

## 9. Como Reproduzir

O script de benchmark fica em `scripts/bench.py`:

```bash
# 1. Suba uma instância limpa do backend
cd backend && source venv/bin/activate
uvicorn main:app --host 127.0.0.1 --port 8020 --log-level warning &

# 2. Rode o benchmark (50 repetições por endpoint)
python ../scripts/bench.py http://127.0.0.1:8020 50
```

> Os valores absolutos variam conforme a máquina; as **relações** entre cenários
> (HIT vs MISS, isolado vs concorrente, FAQ vs LLM) são o que importa para decisões de arquitetura.
