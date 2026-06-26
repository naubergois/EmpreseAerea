# Análise de Segurança — SkyAgent

> Revisão de segurança do código da plataforma multi-agente de venda de passagens (`backend/` FastAPI + `frontend/` React).
> Data: 2026-06-25 · Escopo: código-fonte versionado (não inclui pentest dinâmico).

## Resumo executivo

A aplicação **não possui nenhuma camada de autenticação ou autorização ativa**. Todos os endpoints — incluindo pagamento, reembolso, reserva e fidelidade — estão abertos a qualquer cliente. Combinado com um **webhook de pagamento PIX sem verificação de assinatura** e um **endpoint de reembolso sem dono**, isso permite fraude financeira direta. Há ainda manuseio de dados de cartão (PAN + CVV) e PII sem controles de conformidade (PCI-DSS / LGPD).

| Severidade | Qtd. | Itens |
|------------|------|-------|
| 🔴 Crítica  | 4 | SEC-01, SEC-02, SEC-03, SEC-04 |
| 🟠 Alta     | 4 | SEC-05, SEC-06, SEC-07, SEC-08 |
| 🟡 Média    | 5 | SEC-09, SEC-10, SEC-11, SEC-12, SEC-13 |
| 🔵 Baixa    | 4 | SEC-14, SEC-15, SEC-16, SEC-17 |

---

## 🔴 Críticas

### SEC-01 — Ausência total de autenticação e autorização
**Local:** `backend/main.py`, todos os `*/controller.py`

Existe configuração de JWT (`config.py`) e `passlib[bcrypt]` em `requirements.txt`, mas **nenhum endpoint exige token, sessão ou verificação de identidade**. Não há `Depends` de autenticação em nenhuma rota.

**Impacto:** Qualquer pessoa na rede pode criar/cancelar reservas, consultar PII de qualquer PNR, manipular saldo de milhas e iniciar pagamentos/reembolsos. Inclui IDOR generalizado (objetos referenciados apenas por `pnr`, `txn_id`, `cliente_id` sem checagem de propriedade).

**Exemplos de IDOR:**
- `GET /api/reserva/{pnr}` → retorna CPF, passaporte, e-mail, telefone (`reserva/controller.py:42`)
- `GET /api/fidelidade/{cliente_id}/saldo` e `/extrato` (`fidelidade/controller.py:14,32`)
- `GET /api/pagamento/{txn_id}/status` (`pagamento/controller.py:51`)

**Remediação:** Implementar autenticação (OAuth2/JWT já parcialmente preparado), middleware de autorização e checagem de propriedade do recurso (`recurso.cliente_id == usuario_atual.id`) em todas as rotas sensíveis.

---

### SEC-02 — Webhook PIX sem verificação de assinatura
**Local:** `backend/agents/pagamento/controller.py:38`, `service.py:70`

```python
@router.post("/webhook/pix", response_model=PagamentoResponse)
def webhook_pix(txn_id: str, valor: float, db: Session = Depends(get_db)):
    return PagamentoService(db).webhook_pix(txn_id, valor)
```

O webhook recebe `txn_id` e `valor` como **query params**, sem token, sem assinatura HMAC e sem validação de origem. A única checagem é se o valor bate com o registrado.

**Impacto:** Qualquer pessoa pode aprovar um pagamento PIX pendente (`POST /api/pagamento/webhook/pix?txn_id=PIX-XXXX&valor=199.00`), disparando `PAGAMENTO_CONFIRMADO` e emissão do bilhete **sem ter pago**.

**Remediação:** Validar assinatura/segredo do PSP (HMAC sobre o corpo bruto), aceitar apenas IPs/origem do provedor, usar corpo JSON assinado e idempotência.

---

### SEC-03 — Reembolso sem autenticação nem autorização
**Local:** `backend/agents/pagamento/controller.py:59`, `service.py:106`

```python
@router.post("/{txn_id}/reembolso")
def reembolso(txn_id: str, request: ReembolsoRequest, ...):
    return PagamentoService(db).reembolsar(txn_id, request)
```

Qualquer pessoa que conheça/adivinhe um `txn_id` pode acionar reembolso total ou de valor arbitrário (`req.valor`), sem checagem de propriedade ou de limite.

**Impacto:** Perda financeira direta; reembolso para destino não validado; `valor` controlado pelo atacante.

**Remediação:** Exigir autenticação + papel administrativo/financeiro, validar `valor <= txn.valor`, registrar auditoria e exigir aprovação.

---

### SEC-04 — Segredo JWT fraco e fixo no código
**Local:** `backend/config.py:45`

```python
jwt_secret_key: str = "skyagent-dev-secret-key"
```

Valor padrão previsível versionado no repositório. Se a autenticação for ativada com esse default, qualquer um pode **forjar tokens válidos**.

**Impacto:** Falsificação total de identidade/sessão quando JWT for usado.

**Remediação:** Sem default; obrigar carregamento via secret manager/variável de ambiente; gerar segredo aleatório forte (≥256 bits); falhar a inicialização se ausente em produção.

---

## 🟠 Altas

### SEC-05 — Dados de cartão (PAN + CVV) sem conformidade PCI-DSS
**Local:** `backend/agents/pagamento/schemas.py:8`, `service.py:32`

O backend recebe `numero_cartao`, `cvv`, `validade` e `nome_titular` em texto puro. Mesmo não persistindo, **transportar e processar PAN/CVV** sem tokenização do gateway viola o PCI-DSS e cria risco de vazamento (logs, exceções, tracebacks).

**Remediação:** Nunca tocar no PAN/CVV no backend; usar tokenização client-side do gateway (ex.: Stripe Elements/iframe) e enviar apenas o token. Garantir que CVV nunca seja logado/armazenado.

---

### SEC-06 — Detector de fraude ineficaz (controle morto)
**Local:** `backend/agents/pagamento/fraud_detector.py`

```python
if score >= 0.85:
    return "revisao_manual", score
if score >= 0.95:   # inalcançável: 0.95 já satisfez 0.85 acima
    return "bloqueado", score
```

A ordem das condições torna `"bloqueado"` **inacessível**. Além disso, `valor > 10000` define `score = 0.8`, que nunca atinge nenhum limiar de bloqueio. Em `service.py:36` só há bloqueio quando `status == "bloqueado"`, que nunca ocorre.

**Impacto:** Transações de alto valor/fraudulentas nunca são bloqueadas; o controle de fraude é apenas cosmético.

**Remediação:** Corrigir ordenação (testar `>= 0.95` antes de `>= 0.85`), revisar limiares, integrar antifraude real e testar o caminho de bloqueio.

---

### SEC-07 — Exposição de PII sem proteção (LGPD)
**Local:** `backend/agents/reserva/controller.py:24-28`, `fidelidade/controller.py`

CPF, passaporte, e-mail, telefone e data de nascimento são retornados na íntegra por endpoints sem autenticação. Não há mascaramento, criptografia em repouso, nem controle de acesso.

**Impacto:** Vazamento de dados pessoais sensíveis; não conformidade com a LGPD.

**Remediação:** Autenticação/autorização (ver SEC-01), mascaramento na resposta, criptografia de campos sensíveis, minimização de dados e trilha de auditoria de acesso.

---

### SEC-08 — Pagamento de cartão sem idempotência (replay / cobrança dupla)
**Local:** `backend/agents/pagamento/service.py:32`

`pagar_cartao` gera um novo `txn_id` a cada chamada e não usa chave de idempotência. Reenvio da mesma requisição (retry de rede, clique duplo, replay) gera múltiplas transações aprovadas.

**Remediação:** Exigir `Idempotency-Key` por requisição e deduplicar transações por (pnr, chave).

---

## 🟡 Médias

### SEC-09 — CORS permissivo combinado com credenciais
**Local:** `backend/main.py:47-53`

`allow_credentials=True` com `allow_methods=["*"]` e `allow_headers=["*"]`. As origens estão fixas em `localhost`, mas `frontend_url` vem de env; se mal configurada em produção (ex.: origem ampla), abre CSRF/abuso. Hoje, sem auth (SEC-01), o risco é amplificado.

**Remediação:** Restringir métodos/headers ao necessário; manter lista de origens explícita por ambiente; nunca refletir origem arbitrária com credenciais.

---

### SEC-10 — Sem rate limiting / proteção contra abuso
**Local:** Global (`main.py`)

Não há limitação de taxa. Endpoints de pagamento permitem força bruta de `txn_id`/`pnr`; o endpoint de atendimento aciona o LLM (custo $) sem limite, permitindo abuso financeiro e DoS.

**Remediação:** Rate limiting por IP/usuário (ex.: `slowapi`), cotas no agente de atendimento e backoff.

---

### SEC-11 — Servidor em modo desenvolvimento no compose
**Local:** `docker-compose.yml:11`

```yaml
command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

`--reload` é modo de desenvolvimento (watcher de arquivos, sem workers, overhead) e não deve ir para produção. Os docs `/docs` e `/redoc` também ficam expostos por padrão.

**Remediação:** Compose/Dockerfile de produção sem `--reload`, com workers (gunicorn/uvicorn workers), e desabilitar/proteger a documentação OpenAPI em produção.

---

### SEC-12 — Possível prompt injection no agente de atendimento
**Local:** `backend/agents/atendimento/llm_client.py:35-41`

A mensagem do usuário e o contexto do sistema são concatenados na mensagem enviada ao LLM. Um usuário pode tentar sobrescrever instruções do sistema ("ignore as instruções anteriores...").

**Impacto:** Manipulação de respostas, vazamento do prompt de sistema, uso indevido do canal.

**Remediação:** Separar claramente conteúdo do sistema vs. usuário, sanitizar/limitar entrada, validar saída, e nunca confiar no LLM para decisões de autorização.

---

### SEC-13 — Ausência de TLS e cabeçalhos de segurança
**Local:** Infra (`docker-compose.yml`, `main.py`)

Tráfego HTTP em claro (inclui dados de cartão e PII), sem HSTS, CSP, `X-Content-Type-Options`, `X-Frame-Options`, etc.

**Remediação:** TLS obrigatório (proxy reverso), redirecionar HTTP→HTTPS e adicionar middleware de security headers.

---

## 🔵 Baixas

### SEC-14 — Containers executando como root
**Local:** `backend/Dockerfile`, `frontend/Dockerfile`

Nenhum `USER` não-privilegiado definido. Em caso de RCE, o atacante atua como root no container.

**Remediação:** Criar e usar usuário não-root (`USER appuser`).

---

### SEC-15 — `init_db()` + `seed_data()` na inicialização da aplicação
**Local:** `backend/main.py:24-28`, `database.py`

Criação de schema e seeding rodam no `lifespan` a cada boot, sem migrations (Alembic). Risco de dados/seeds indevidos em produção e ausência de versionamento de schema.

**Remediação:** Usar migrations gerenciadas; não semear dados em produção automaticamente.

---

### SEC-16 — Vazamento de detalhes de erro nas respostas
**Local:** `reserva/controller.py:39,47`, vários controllers

`raise HTTPException(status_code=422, detail=str(e))` repassa a mensagem interna ao cliente. Pode expor detalhes de implementação.

**Remediação:** Mensagens genéricas ao cliente, detalhes apenas em logs internos.

---

### SEC-17 — Dependência de autenticação incompleta / dead code
**Local:** `backend/requirements.txt:8` (`passlib[bcrypt]`), `config.py` (JWT)

Infra de auth está parcialmente presente mas não implementada, indicando controle de segurança planejado e nunca concluído — fácil de esquecer antes do go-live.

**Remediação:** Concluir e habilitar a autenticação antes de produção; remover dependências não usadas se não for o caso.

---

## Recomendações prioritárias

1. **Bloquear go-live** até implementar autenticação/autorização (SEC-01) e proteger webhook e reembolso (SEC-02, SEC-03).
2. **Remover segredo padrão** do JWT e carregar de secret manager (SEC-04).
3. **Tokenizar pagamentos** no cliente; remover PAN/CVV do backend (SEC-05).
4. **Corrigir e validar** o caminho de bloqueio do antifraude (SEC-06).
5. **Aplicar TLS, rate limiting e security headers** antes de expor publicamente (SEC-10, SEC-13).

## Observações de escopo

- Não foram encontrados segredos commitados; o `.gitignore` cobre `.env` e `*.db` adequadamente.
- Não há SQL dinâmico montado por string (uso de SQLAlchemy ORM), portanto baixo risco de SQL injection clássico.
- Esta análise é estática; recomenda-se complementar com SAST/DAST e teste de intrusão antes de produção.
