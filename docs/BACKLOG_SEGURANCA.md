# Backlog de Segurança — SkyAgent

> Cards de desenvolvimento derivados de [`ANALISE_SEGURANCA.md`](./ANALISE_SEGURANCA.md).
> Cada card traz contexto, tarefas, critérios de aceite e estimativa para entrar direto na sprint.
> Data: 2026-06-25

## Como usar
- **ID do card** segue o achado correspondente (`SEC-XX`).
- **Prioridade:** 🔴 Crítica · 🟠 Alta · 🟡 Média · 🔵 Baixa.
- **Estimativa:** Story Points (escala Fibonacci) — referência relativa, não horas.
- **DoR/DoD** comuns ao final do documento.

## Quadro (visão Kanban)

| ID | Título | Prioridade | Épico | Pts | Status |
|----|--------|-----------|-------|-----|--------|
| SEC-01 | Autenticação e autorização base | 🔴 | AuthZ | 13 | A Fazer |
| SEC-02 | Validar assinatura do webhook PIX | 🔴 | Pagamentos | 5 | A Fazer |
| SEC-03 | Proteger endpoint de reembolso | 🔴 | Pagamentos | 3 | A Fazer |
| SEC-04 | Remover segredo JWT padrão | 🔴 | AuthZ | 2 | A Fazer |
| SEC-05 | Tokenizar dados de cartão (PCI) | 🟠 | Pagamentos | 8 | A Fazer |
| SEC-06 | Corrigir lógica do antifraude | 🟠 | Pagamentos | 3 | A Fazer |
| SEC-07 | Proteger PII / conformidade LGPD | 🟠 | Privacidade | 8 | A Fazer |
| SEC-08 | Idempotência no pagamento de cartão | 🟠 | Pagamentos | 5 | A Fazer |
| SEC-09 | Endurecer configuração de CORS | 🟡 | Plataforma | 2 | A Fazer |
| SEC-10 | Rate limiting e cotas | 🟡 | Plataforma | 5 | A Fazer |
| SEC-11 | Configuração de produção (sem reload) | 🟡 | DevOps | 3 | A Fazer |
| SEC-12 | Mitigar prompt injection no atendimento | 🟡 | IA/Atendimento | 5 | A Fazer |
| SEC-13 | TLS e security headers | 🟡 | DevOps | 3 | A Fazer |
| SEC-14 | Containers como usuário não-root | 🔵 | DevOps | 2 | A Fazer |
| SEC-15 | Migrations e seed controlado | 🔵 | Plataforma | 5 | A Fazer |
| SEC-16 | Padronizar tratamento de erros | 🔵 | Plataforma | 3 | A Fazer |
| SEC-17 | Concluir/limpar infra de auth | 🔵 | AuthZ | 2 | A Fazer |

**Total:** 77 pts · Recomenda-se entregar SEC-01→SEC-04 antes de qualquer exposição pública.

---

## 🔴 Críticas

### SEC-01 — Autenticação e autorização base
**Épico:** AuthZ · **Prioridade:** 🔴 Crítica · **Estimativa:** 13 pts

**Contexto:** Nenhum endpoint exige identidade; há IDOR generalizado por `pnr`, `txn_id`, `cliente_id`. Bloqueia o go-live.

**Tarefas**
- [ ] Definir modelo de identidade (cliente, atendente, admin) e fluxo de login.
- [ ] Implementar emissão/validação de JWT (OAuth2 password/bearer no FastAPI).
- [ ] Criar dependência `get_current_user` e aplicá-la nas rotas sensíveis.
- [ ] Implementar checagem de propriedade do recurso (ex.: `reserva.cliente_id == user.id`).
- [ ] Adicionar papéis/escopos (RBAC) para rotas administrativas/financeiras.
- [ ] Atualizar frontend (`apiClient.js`) para enviar token e tratar 401/403.

**Critérios de aceite**
- Requisições sem token válido retornam `401` em rotas protegidas.
- Usuário A não acessa recursos do usuário B (`403`).
- Rotas administrativas exigem papel adequado.
- Testes automatizados cobrindo acesso autorizado, não autenticado e cruzado.

**Dependências:** Habilita SEC-02, SEC-03, SEC-07.

---

### SEC-02 — Validar assinatura do webhook PIX
**Épico:** Pagamentos · **Prioridade:** 🔴 Crítica · **Estimativa:** 5 pts

**Contexto:** `POST /api/pagamento/webhook/pix` aprova pagamento via query params, sem assinatura/origem (`pagamento/controller.py:38`).

**Tarefas**
- [ ] Receber payload do PSP no corpo (JSON), não em query params.
- [ ] Validar assinatura HMAC sobre o corpo bruto com segredo do PSP.
- [ ] Restringir origem (allowlist de IP) quando aplicável.
- [ ] Garantir idempotência por `txn_id` (não reprocessar).
- [ ] Registrar tentativa inválida em log de auditoria.

**Critérios de aceite**
- Webhook sem assinatura válida → `401/403` e não altera status.
- Reenvio do mesmo evento não duplica confirmação.
- Teste cobrindo assinatura válida, inválida e replay.

---

### SEC-03 — Proteger endpoint de reembolso
**Épico:** Pagamentos · **Prioridade:** 🔴 Crítica · **Estimativa:** 3 pts

**Contexto:** `POST /api/pagamento/{txn_id}/reembolso` sem auth, com `valor` controlado pelo cliente (`pagamento/service.py:106`).

**Tarefas**
- [ ] Exigir autenticação + papel financeiro/admin (depende de SEC-01).
- [ ] Validar `valor <= txn.valor` e status reembolsável.
- [ ] Registrar auditoria (quem, quando, valor, motivo).
- [ ] Manter comportamento idempotente já existente.

**Critérios de aceite**
- Usuário sem papel adequado recebe `403`.
- Reembolso acima do valor original é rejeitado (`422`).
- Evento de auditoria gerado em todo reembolso.

**Dependências:** SEC-01.

---

### SEC-04 — Remover segredo JWT padrão
**Épico:** AuthZ · **Prioridade:** 🔴 Crítica · **Estimativa:** 2 pts

**Contexto:** `jwt_secret_key` tem default fixo `"skyagent-dev-secret-key"` (`config.py:45`).

**Tarefas**
- [ ] Remover valor default do segredo.
- [ ] Falhar a inicialização se ausente em produção.
- [ ] Carregar de secret manager / variável de ambiente.
- [ ] Documentar geração de segredo forte (≥256 bits) no `.env.example`.

**Critérios de aceite**
- App não sobe em produção sem `JWT_SECRET_KEY` definido.
- Nenhum segredo sensível versionado.

---

## 🟠 Altas

### SEC-05 — Tokenizar dados de cartão (PCI-DSS)
**Épico:** Pagamentos · **Prioridade:** 🟠 Alta · **Estimativa:** 8 pts

**Contexto:** Backend recebe PAN + CVV em texto puro (`pagamento/schemas.py:8`).

**Tarefas**
- [ ] Integrar tokenização client-side do gateway (ex.: iframe/Elements).
- [ ] Alterar `PagamentoCartaoRequest` para receber apenas token do gateway.
- [ ] Remover `numero_cartao`/`cvv`/`validade` do backend.
- [ ] Garantir que dados de cartão nunca apareçam em logs/exceções.
- [ ] Atualizar `PaymentPage.jsx` e `pagamentoApi.js`.

**Critérios de aceite**
- Backend nunca recebe PAN/CVV.
- Logs auditados sem dados de cartão.
- Fluxo de pagamento com cartão funcional via token.

---

### SEC-06 — Corrigir lógica do antifraude
**Épico:** Pagamentos · **Prioridade:** 🟠 Alta · **Estimativa:** 3 pts

**Contexto:** Estado `"bloqueado"` é inalcançável e `valor > 10000` nunca bloqueia (`fraud_detector.py`).

**Tarefas**
- [ ] Reordenar condições (testar `>= 0.95` antes de `>= 0.85`).
- [ ] Revisar limiares e fatores de score (valor, IP, histórico).
- [ ] Cobrir caminho de bloqueio em `pagar_cartao`.
- [ ] Adicionar testes unitários para aprovado/revisão/bloqueado.

**Critérios de aceite**
- Transação acima do limiar retorna `"bloqueado"` e é recusada.
- Testes cobrem os três desfechos.

---

### SEC-07 — Proteger PII / conformidade LGPD
**Épico:** Privacidade · **Prioridade:** 🟠 Alta · **Estimativa:** 8 pts

**Contexto:** CPF, passaporte, e-mail e telefone retornados sem auth e sem mascaramento (`reserva/controller.py:24`).

**Tarefas**
- [ ] Aplicar autorização nas respostas com PII (depende de SEC-01).
- [ ] Mascarar PII em respostas quando o solicitante não for o dono.
- [ ] Avaliar criptografia em repouso de campos sensíveis.
- [ ] Trilha de auditoria de acesso a PII.
- [ ] Revisar minimização de dados nos schemas de resposta.

**Critérios de aceite**
- PII só é exposta ao titular/perfil autorizado.
- Acessos a PII registrados em log.

**Dependências:** SEC-01.

---

### SEC-08 — Idempotência no pagamento de cartão
**Épico:** Pagamentos · **Prioridade:** 🟠 Alta · **Estimativa:** 5 pts

**Contexto:** `pagar_cartao` não deduplica; retries geram cobranças múltiplas (`pagamento/service.py:32`).

**Tarefas**
- [ ] Aceitar header `Idempotency-Key`.
- [ ] Persistir chave e resultado; retornar resposta original em replays.
- [ ] Definir janela/expiração da chave.
- [ ] Testes de requisições concorrentes/duplicadas.

**Critérios de aceite**
- Mesma `Idempotency-Key` não gera segunda transação.
- Resposta idêntica em replay.

---

## 🟡 Médias

### SEC-09 — Endurecer configuração de CORS
**Épico:** Plataforma · **Prioridade:** 🟡 Média · **Estimativa:** 2 pts

**Tarefas**
- [ ] Restringir `allow_methods`/`allow_headers` ao necessário (`main.py:47`).
- [ ] Lista de origens explícita por ambiente.
- [ ] Garantir que credenciais nunca sejam combinadas com origem refletida.

**Critérios de aceite:** Apenas origens/métodos aprovados são aceitos; testado por ambiente.

---

### SEC-10 — Rate limiting e cotas
**Épico:** Plataforma · **Prioridade:** 🟡 Média · **Estimativa:** 5 pts

**Tarefas**
- [ ] Adicionar rate limiting por IP/usuário (ex.: `slowapi`).
- [ ] Cota específica no agente de atendimento (custo LLM).
- [ ] Respostas `429` com `Retry-After`.

**Critérios de aceite:** Excesso de requisições retorna `429`; LLM protegido por cota.

---

### SEC-11 — Configuração de produção (sem reload)
**Épico:** DevOps · **Prioridade:** 🟡 Média · **Estimativa:** 3 pts

**Tarefas**
- [ ] Compose/Dockerfile de produção sem `--reload` (`docker-compose.yml:11`).
- [ ] Rodar com múltiplos workers (gunicorn/uvicorn).
- [ ] Desabilitar/proteger `/docs` e `/redoc` em produção.

**Critérios de aceite:** Imagem de produção sem modo dev; docs não públicas.

---

### SEC-12 — Mitigar prompt injection no atendimento
**Épico:** IA/Atendimento · **Prioridade:** 🟡 Média · **Estimativa:** 5 pts

**Tarefas**
- [ ] Separar rigidamente conteúdo de sistema vs. usuário (`llm_client.py:35`).
- [ ] Sanitizar/limitar tamanho da entrada do usuário.
- [ ] Validar saída e nunca usar o LLM para decisões de autorização.
- [ ] Testes com payloads de injeção conhecidos.

**Critérios de aceite:** Tentativas de override não vazam prompt de sistema nem alteram políticas.

---

### SEC-13 — TLS e security headers
**Épico:** DevOps · **Prioridade:** 🟡 Média · **Estimativa:** 3 pts

**Tarefas**
- [ ] TLS obrigatório via proxy reverso; redirecionar HTTP→HTTPS.
- [ ] Middleware com HSTS, CSP, `X-Content-Type-Options`, `X-Frame-Options`.

**Critérios de aceite:** Tráfego apenas HTTPS; headers validados por scanner.

---

## 🔵 Baixas

### SEC-14 — Containers como usuário não-root
**Épico:** DevOps · **Prioridade:** 🔵 Baixa · **Estimativa:** 2 pts

**Tarefas**
- [ ] Criar usuário não-privilegiado nos Dockerfiles (`backend`/`frontend`).
- [ ] Ajustar permissões e `USER`.

**Critérios de aceite:** Processos não rodam como root.

---

### SEC-15 — Migrations e seed controlado
**Épico:** Plataforma · **Prioridade:** 🔵 Baixa · **Estimativa:** 5 pts

**Tarefas**
- [ ] Introduzir Alembic para versionamento de schema.
- [ ] Remover `init_db()`/`seed_data()` automáticos do `lifespan` em produção (`main.py:24`).
- [ ] Pipeline de migração no deploy.

**Critérios de aceite:** Schema versionado; sem seed automático em produção.

---

### SEC-16 — Padronizar tratamento de erros
**Épico:** Plataforma · **Prioridade:** 🔵 Baixa · **Estimativa:** 3 pts

**Tarefas**
- [ ] Substituir `detail=str(e)` por mensagens genéricas ao cliente.
- [ ] Logar detalhes internamente com correlação de request.
- [ ] Handler global de exceções.

**Critérios de aceite:** Respostas de erro não expõem detalhes internos; logs preservam contexto.

---

### SEC-17 — Concluir/limpar infra de auth
**Épico:** AuthZ · **Prioridade:** 🔵 Baixa · **Estimativa:** 2 pts

**Tarefas**
- [ ] Concluir uso de `passlib`/JWT (com SEC-01) ou remover se não usado.
- [ ] Documentar decisão de arquitetura de auth.

**Critérios de aceite:** Sem dependências/configs órfãs relacionadas a auth.

---

## Definition of Ready (DoR)
- Card com contexto, tarefas e critérios de aceite claros.
- Dependências identificadas e desbloqueadas.
- Impacto de segurança compreendido pelo time.

## Definition of Done (DoD)
- Código revisado (com foco em segurança) e testes automatizados passando.
- Critérios de aceite atendidos e validados.
- Sem regressão nos fluxos existentes (pytest + BDD `features/`).
- Documentação/`.env.example` atualizados quando aplicável.
- Item de análise correspondente marcado como mitigado.

## Sugestão de sequenciamento (sprints)
1. **Sprint 1 (bloqueio de go-live):** SEC-04, SEC-01, SEC-02, SEC-03.
2. **Sprint 2 (pagamentos/privacidade):** SEC-05, SEC-06, SEC-08, SEC-07.
3. **Sprint 3 (plataforma/infra):** SEC-10, SEC-13, SEC-11, SEC-09, SEC-12.
4. **Sprint 4 (hardening):** SEC-15, SEC-16, SEC-14, SEC-17.
