# Requisitos — Agente Orquestrador (ORC)

> **Responsabilidade:** Coordenar o pipeline end-to-end de venda, marketing e suporte, manter consistência transacional via Saga e tratar falhas com resiliência.

---

## Pipelines Coordenados

| Pipeline | Sequência de Agentes | Descrição |
|----------|---------------------|-----------|
| Venda | BUS → PRE → RES → PAG → EMI → FID → NOT | Compra e emissão de bilhetes |
| Marketing | MKT → FID → NOT | Campanhas, segmentação e conversão |
| Suporte | ATC → RES/PAG/EMI → NOT | Atendimento, alterações e reembolsos |

---

## Requisitos Funcionais

| ID | Requisito | Prioridade |
|----|-----------|------------|
| ORC-RF01 | Deve receber requisições do cliente e rotear para o agente apropriado | Alta |
| ORC-RF02 | Deve manter estado de sessão durante todo o pipeline de venda | Alta |
| ORC-RF03 | Deve implementar padrão Saga para transações distribuídas | Alta |
| ORC-RF04 | Deve executar rollback automático em falhas de qualquer etapa | Alta |
| ORC-RF05 | Deve paralelizar etapas independentes (ex.: milhas + notificação) | Alta |
| ORC-RF06 | Deve gerenciar filas de prioridade por nível de fidelidade | Média |
| ORC-RF07 | Deve registrar logs de auditoria imutáveis entre agentes | Alta |
| ORC-RF08 | Deve implementar circuit breaker para agentes indisponíveis | Alta |
| ORC-RF09 | Deve suportar retry com backoff exponencial (máx. 3 tentativas) | Alta |
| ORC-RF10 | Deve detectar e resolver deadlocks entre agentes | Média |
| ORC-RF11 | Deve escalar para atendente humano após 3 falhas consecutivas | Alta |
| ORC-RF12 | Deve expor dashboard de saúde dos agentes em tempo real | Média |
| ORC-RF13 | Deve classificar intenção do cliente (busca, compra, suporte, marketing) | Alta |
| ORC-RF14 | Deve propagar trace ID único em todas as chamadas entre agentes | Alta |
| ORC-RF15 | Deve expirar sessões inativas após 30 minutos e liberar recursos | Alta |
| ORC-RF16 | Deve coordenar pipeline de marketing disparado por eventos de venda | Média |
| ORC-RF17 | Deve garantir idempotência em rollbacks e retentativas | Alta |
| ORC-RF18 | Deve enfileirar operações não-críticas (milhas) em degradação graciosa | Média |

---

## Requisitos Não-Funcionais

| ID | Requisito | Métrica |
|----|-----------|---------|
| ORC-RNF01 | Tempo de roteamento de requisição | < 100ms |
| ORC-RNF02 | Disponibilidade | 99.99% |
| ORC-RNF03 | Sessões simultâneas suportadas | ≥ 10.000 |
| ORC-RNF04 | Tempo máximo de rollback completo | < 5s |
| ORC-RNF05 | Latência p95 do pipeline completo (happy path) | < 15s |

---

## Contratos de Integração

| Agente | Evento de Entrada | Evento de Saída |
|--------|-------------------|-----------------|
| BUS | `search.flights.requested` | `search.flights.completed` |
| PRE | `pricing.quote.requested` | `pricing.quote.ready` |
| RES | `reservation.create.requested` | `reservation.confirmed` / `reservation.cancelled` |
| PAG | `payment.charge.requested` | `payment.approved` / `payment.declined` |
| EMI | `ticket.issue.requested` | `ticket.issued` / `ticket.issue.failed` |
| FID | `loyalty.credit.requested` | `loyalty.credited` |
| NOT | `notification.send.requested` | `notification.delivered` |
| MKT | `marketing.campaign.triggered` | `marketing.campaign.sent` |
| ATC | `support.ticket.opened` | `support.ticket.resolved` |
