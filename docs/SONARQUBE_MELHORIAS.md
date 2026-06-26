# Plano de Melhorias — SonarQube (Agente de Qualidade)

> Gerado automaticamente pelo Agente de Qualidade do SkyAgent em `2026-06-26T00:59:39.174141+00:00`.

**Quality Gate:** ❌ `ERROR`

## Métricas do projeto

| Métrica | Valor |
|---------|-------|
| 🐞 Bugs | 0 |
| 🔓 Vulnerabilidades | 0 |
| 🧹 Code Smells | 121 |
| 🔥 Security Hotspots | 6 |
| 🧪 Cobertura | 0.0% |
| 📑 Duplicação | 0.0% |
| 📏 Linhas de código | 7805 |
| ⏱️ Dívida técnica | 648 min |
| 🎯 Notas (Conf./Seg./Manut.) | A / A / A |

## Plano de melhorias priorizado (12 itens)

### 1. 🟧 P2 · CODE_SMELL · `python:S3776`
- **Ocorrências:** 3
- **Severidade:** CRITICAL
- **Título:** Refactor this function to reduce its Cognitive Complexity from 30 to the 15 allowed.
- **Ação sugerida:** Refatorar para melhorar manutenibilidade e reduzir dívida técnica. Detalhe: Refactor this function to reduce its Cognitive Complexity from 30 to the 15 allowed.
- **Arquivos:** `backend/agents/busca_voos/service.py`, `backend/agents/qa/service.py`, `backend/agents/reserva/service.py`
- **Exemplos:**
    - `backend/agents/busca_voos/service.py:19` — Refactor this function to reduce its Cognitive Complexity from 30 to the 15 allowed.
    - `backend/agents/qa/service.py:76` — Refactor this function to reduce its Cognitive Complexity from 20 to the 15 allowed.
    - `backend/agents/reserva/service.py:109` — Refactor this function to reduce its Cognitive Complexity from 18 to the 15 allowed.

### 2. 🟧 P2 · CODE_SMELL · `python:S6903`
- **Ocorrências:** 1
- **Severidade:** CRITICAL
- **Título:** Don't use `datetime.datetime.utcnow` to create this datetime object.
- **Ação sugerida:** Refatorar para melhorar manutenibilidade e reduzir dívida técnica. Detalhe: Don't use `datetime.datetime.utcnow` to create this datetime object.
- **Arquivos:** `scripts/bench.py`
- **Exemplos:**
    - `scripts/bench.py:15` — Don't use `datetime.datetime.utcnow` to create this datetime object.

### 3. 🟨 P3 · CODE_SMELL · `javascript:S6774`
- **Ocorrências:** 35
- **Severidade:** MAJOR
- **Título:** 'flight.numero' is missing in props validation
- **Ação sugerida:** Refatorar para melhorar manutenibilidade e reduzir dívida técnica. Detalhe: 'flight.numero' is missing in props validation
- **Arquivos:** `frontend/src/components/voos/FlightCard.jsx`, `frontend/src/components/voos/FlightList.jsx`, `frontend/src/context/BookingContext.jsx`, `frontend/src/pages/BddTestsPage.jsx`
- **Exemplos:**
    - `frontend/src/components/voos/FlightCard.jsx:17` — 'flight.numero' is missing in props validation
    - `frontend/src/components/voos/FlightCard.jsx:17` — 'flight.destino' is missing in props validation
    - `frontend/src/components/voos/FlightCard.jsx:17` — 'flight.preco' is missing in props validation
    - `frontend/src/components/voos/FlightCard.jsx:17` — 'flight.origem' is missing in props validation
    - `frontend/src/components/voos/FlightCard.jsx:4` — 'flight' is missing in props validation

### 4. 🟨 P3 · CODE_SMELL · `python:S8415`
- **Ocorrências:** 24
- **Severidade:** MAJOR
- **Título:** Document this HTTPException with status code 503 in the "responses" parameter.
- **Ação sugerida:** Refatorar para melhorar manutenibilidade e reduzir dívida técnica. Detalhe: Document this HTTPException with status code 503 in the "responses" parameter.
- **Arquivos:** `backend/agents/atendimento/controller.py`, `backend/agents/emissao/controller.py`, `backend/agents/fidelidade/controller.py`, `backend/agents/notificacoes/controller.py`, `backend/agents/orquestrador/controller.py`, `backend/agents/pagamento/controller.py`, `backend/agents/precificacao/controller.py`, `backend/agents/qa/controller.py`
- **Exemplos:**
    - `backend/agents/qualidade/controller.py:26` — Document this HTTPException with status code 503 in the "responses" parameter.
    - `backend/agents/qualidade/controller.py:35` — Document this HTTPException with status code 503 in the "responses" parameter.
    - `backend/agents/qualidade/controller.py:44` — Document this HTTPException with status code 503 in the "responses" parameter.
    - `backend/agents/qualidade/controller.py:53` — Document this HTTPException with status code 503 in the "responses" parameter.
    - `backend/agents/reserva/controller.py:41` — Document this HTTPException with status code 422 in the "responses" parameter.

### 5. 🟨 P3 · CODE_SMELL · `javascript:S3358`
- **Ocorrências:** 4
- **Severidade:** MAJOR
- **Título:** Extract this nested ternary operation into an independent statement.
- **Ação sugerida:** Refatorar para melhorar manutenibilidade e reduzir dívida técnica. Detalhe: Extract this nested ternary operation into an independent statement.
- **Arquivos:** `frontend/src/components/layout/Stepper.jsx`, `frontend/src/hooks/useFlightSearch.js`, `frontend/src/pages/SupportPage.jsx`
- **Exemplos:**
    - `frontend/src/components/layout/Stepper.jsx:20` — Extract this nested ternary operation into an independent statement.
    - `frontend/src/hooks/useFlightSearch.js:19` — Extract this nested ternary operation into an independent statement.
    - `frontend/src/pages/SupportPage.jsx:88` — Extract this nested ternary operation into an independent statement.
    - `frontend/src/pages/SupportPage.jsx:89` — Extract this nested ternary operation into an independent statement.

### 6. 🟨 P3 · CODE_SMELL · `javascript:S6479`
- **Ocorrências:** 3
- **Severidade:** MAJOR
- **Título:** Do not use Array index in keys
- **Ação sugerida:** Refatorar para melhorar manutenibilidade e reduzir dívida técnica. Detalhe: Do not use Array index in keys
- **Arquivos:** `frontend/src/pages/BddTestsPage.jsx`, `frontend/src/pages/SupportPage.jsx`
- **Exemplos:**
    - `frontend/src/pages/BddTestsPage.jsx:55` — Do not use Array index in keys
    - `frontend/src/pages/BddTestsPage.jsx:65` — Do not use Array index in keys
    - `frontend/src/pages/SupportPage.jsx:79` — Do not use Array index in keys

### 7. 🟨 P3 · CODE_SMELL · `javascript:S6772`
- **Ocorrências:** 2
- **Severidade:** MAJOR
- **Título:** Ambiguous spacing after previous element input
- **Ação sugerida:** Refatorar para melhorar manutenibilidade e reduzir dívida técnica. Detalhe: Ambiguous spacing after previous element input
- **Arquivos:** `frontend/src/pages/PaymentPage.jsx`
- **Exemplos:**
    - `frontend/src/pages/PaymentPage.jsx:73` — Ambiguous spacing after previous element input
    - `frontend/src/pages/PaymentPage.jsx:77` — Ambiguous spacing after previous element input

### 8. 🟨 P3 · CODE_SMELL · `javascript:S6819`
- **Ocorrências:** 1
- **Severidade:** MAJOR
- **Título:** Use <input type="button">, <input type="image">, <input type="reset">, <input type="submit">, or <button> instead of the "button" role to ensure accessibility across all devices.
- **Ação sugerida:** Refatorar para melhorar manutenibilidade e reduzir dívida técnica. Detalhe: Use <input type="button">, <input type="image">, <input type="reset">, <input type="submit">, or <button> instead of the "button" role to ensure accessibility across all devices.
- **Arquivos:** `frontend/src/components/voos/FlightCard.jsx`
- **Exemplos:**
    - `frontend/src/components/voos/FlightCard.jsx:13` — Use <input type="button">, <input type="image">, <input type="reset">, <input type="submit">, or <button> instead of the "button" role to ensure accessibility across all devices.

### 9. 🟨 P3 · CODE_SMELL · `python:S107`
- **Ocorrências:** 1
- **Severidade:** MAJOR
- **Título:** Function "buscar_voos" has 17 parameters, which is greater than the 13 authorized.
- **Ação sugerida:** Refatorar para melhorar manutenibilidade e reduzir dívida técnica. Detalhe: Function "buscar_voos" has 17 parameters, which is greater than the 13 authorized.
- **Arquivos:** `backend/agents/busca_voos/controller.py`
- **Exemplos:**
    - `backend/agents/busca_voos/controller.py:17` — Function "buscar_voos" has 17 parameters, which is greater than the 13 authorized.

### 10. 🟨 P3 · CODE_SMELL · `javascript:S6481`
- **Ocorrências:** 1
- **Severidade:** MAJOR
- **Título:** The object passed as the value prop to the Context provider changes every render. To fix this consider wrapping it in a useMemo hook.
- **Ação sugerida:** Refatorar para melhorar manutenibilidade e reduzir dívida técnica. Detalhe: The object passed as the value prop to the Context provider changes every render. To fix this consider wrapping it in a useMemo hook.
- **Arquivos:** `frontend/src/context/BookingContext.jsx`
- **Exemplos:**
    - `frontend/src/context/BookingContext.jsx:14` — The object passed as the value prop to the Context provider changes every render. To fix this consider wrapping it in a useMemo hook.

### 11. 🟨 P3 · CODE_SMELL · `javascript:S4624`
- **Ocorrências:** 1
- **Severidade:** MAJOR
- **Título:** Refactor this code to not use nested template literals.
- **Ação sugerida:** Refatorar para melhorar manutenibilidade e reduzir dívida técnica. Detalhe: Refactor this code to not use nested template literals.
- **Arquivos:** `frontend/src/utils/formatters.js`
- **Exemplos:**
    - `frontend/src/utils/formatters.js:13` — Refactor this code to not use nested template literals.

### 12. 🟦 P4 · CODE_SMELL · `python:S8410`
- **Ocorrências:** 45
- **Severidade:** MINOR
- **Título:** Use "Annotated" type hints for FastAPI dependency injection
- **Ação sugerida:** Refatorar para melhorar manutenibilidade e reduzir dívida técnica. Detalhe: Use "Annotated" type hints for FastAPI dependency injection
- **Arquivos:** `backend/agents/atendimento/controller.py`, `backend/agents/busca_voos/controller.py`, `backend/agents/emissao/controller.py`, `backend/agents/fidelidade/controller.py`, `backend/agents/marketing/controller.py`, `backend/agents/notificacoes/controller.py`, `backend/agents/orquestrador/controller.py`, `backend/agents/pagamento/controller.py`
- **Exemplos:**
    - `backend/agents/atendimento/controller.py:14` — Use "Annotated" type hints for FastAPI dependency injection
    - `backend/agents/atendimento/controller.py:19` — Use "Annotated" type hints for FastAPI dependency injection
    - `backend/agents/atendimento/controller.py:24` — Use "Annotated" type hints for FastAPI dependency injection
    - `backend/agents/busca_voos/controller.py:17` — Use "Annotated" type hints for FastAPI dependency injection
    - `backend/agents/busca_voos/controller.py:18` — Use "Annotated" type hints for FastAPI dependency injection
