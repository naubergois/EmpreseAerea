# SkyAgent - Visão Geral e Requisitos Transversais

**Projeto:** SkyAgent — Plataforma Multi-Agente para Venda e Emissão de Passagens Aéreas  
**Versão:** 1.0  
**Data:** 2026-06-25

---

## Arquitetura

O sistema possui um **Agente Orquestrador (ORC)** que coordena três pipelines principais:

| Pipeline | Agentes | Fluxo |
|----------|---------|-------|
| **Venda** | BUS → PRE → RES → PAG → EMI | Busca, cotação, reserva, pagamento e emissão |
| **Marketing** | MKT → FID → NOT | Segmentação, campanhas, fidelidade e disparo |
| **Suporte** | ATC → NOT (+ RES/PAG/EMI) | Atendimento, resolução e notificação |

### Mapa de Agentes

```
                    ┌─────────────────────┐
                    │  ORC (Orquestrador) │
                    │  Saga · Circuit Br. │
                    └─────────┬───────────┘
          ┌───────────────────┼───────────────────┐
          │                   │                   │
    ┌─────▼─────┐      ┌─────▼─────┐      ┌─────▼─────┐
    │    BUS    │      │    MKT    │      │    ATC    │
    │   Busca   │      │ Marketing │      │ Atendim.  │
    └─────┬─────┘      └─────┬─────┘      └─────┬─────┘
    ┌─────▼─────┐      ┌─────▼─────┐            │
    │    PRE    │      │    FID    │      ┌─────▼─────┐
    │ Precific. │      │ Fidelid.  │      │    NOT    │
    └─────┬─────┘      └───────────┘      │ Notific.  │
    ┌─────▼─────┐                           └───────────┘
    │    RES    │
    │  Reserva  │
    └─────┬─────┘
    ┌─────▼─────┐
    │    PAG    │
    │ Pagamento │
    └─────┬─────┘
    ┌─────▼─────┐
    │    EMI    │
    │  Emissão  │
    └───────────┘
```

---

## Fluxos Principais

### Pipeline completo de venda (happy path)

1. Cliente solicita busca → **ORC** aciona **BUS**
2. **BUS** retorna opções → **ORC** aciona **PRE** para cotação
3. Cliente escolhe voo → **ORC** aciona **RES** (PNR + assento)
4. **ORC** aciona **PAG** → pagamento confirmado
5. **ORC** aciona **EMI** → e-ticket emitido
6. **ORC** aciona **FID** → milhas creditadas
7. **ORC** aciona **NOT** → confirmações enviadas

### Pipeline de rollback (falha de pagamento)

1. **PAG** retorna pagamento recusado
2. **ORC** executa compensação Saga → **RES** cancela PNR
3. Assento e inventário liberados
4. **NOT** notifica cliente

### Pipeline de marketing

1. **MKT** segmenta clientes e cria campanha
2. **FID** valida elegibilidade por nível de fidelidade
3. **NOT** dispara campanha multicanal
4. Conversão rastreada via **MKT** analytics

### Pipeline de suporte

1. Cliente contata **ATC** (chat, e-mail, telefone)
2. **ATC** resolve ou escala para humano
3. Se necessário, **ORC** coordena **RES/PAG/EMI**
4. **NOT** confirma resolução ao cliente

---

## Requisitos Transversais

### Segurança

| ID | Requisito |
|----|-----------|
| SEC-01 | Criptografia TLS 1.3 em trânsito |
| SEC-02 | Tokenização de dados de cartão (PCI-DSS) |
| SEC-03 | Autenticação entre agentes via mTLS |
| SEC-04 | Rate limiting em todas as APIs |
| SEC-05 | Logs de auditoria imutáveis |
| SEC-06 | Conformidade PCI-DSS, LGPD e GDPR |

### Observabilidade

| ID | Requisito |
|----|-----------|
| OBS-01 | Distributed tracing em todo o pipeline |
| OBS-02 | Métricas de latência por agente |
| OBS-03 | Alertas automatizados de degradação |
| OBS-04 | Dashboard unificado de saúde dos agentes |

### Escalabilidade

| ID | Requisito |
|----|-----------|
| ESC-01 | Auto-scaling horizontal por agente |
| ESC-02 | Suporte a picos de 10x em promoções |
| ESC-03 | Message queue para desacoplamento |

---

## Glossário

| Termo | Definição |
|-------|-----------|
| **PNR** | Passenger Name Record — código de reserva com 6 caracteres |
| **GDS** | Global Distribution System (Amadeus, Sabre, Travelport) |
| **BSP** | Billing and Settlement Plan da IATA |
| **e-ticket** | Bilhete eletrônico |
| **Saga** | Padrão de transação distribuída com compensação |
| **Circuit Breaker** | Padrão de resiliência para indisponibilidade |
| **IATA** | International Air Transport Association |
| **Codeshare** | Venda de assentos em voo operado por outra companhia |

---

## Documentação Relacionada

| Agente | Requisitos | Features BDD |
|--------|-----------|--------------|
| ORC | [01_agente_orquestrador.md](01_agente_orquestrador.md) | `features/orquestrador/` |
| BUS | [02_agente_busca_voos.md](02_agente_busca_voos.md) | `features/busca_voos/` |
| PRE | [03_agente_precificacao.md](03_agente_precificacao.md) | `features/precificacao/` |
| RES | [04_agente_reserva.md](04_agente_reserva.md) | `features/reserva/` |
| PAG | [05_agente_pagamento.md](05_agente_pagamento.md) | `features/pagamento/` |
| EMI | [06_agente_emissao.md](06_agente_emissao.md) | `features/emissao/` |
| MKT | [07_agente_marketing.md](07_agente_marketing.md) | `features/marketing/` |
| ATC | [08_agente_atendimento.md](08_agente_atendimento.md) | `features/atendimento/` |
| NOT | [09_agente_notificacoes.md](09_agente_notificacoes.md) | `features/notificacoes/` |
| FID | [10_agente_fidelidade.md](10_agente_fidelidade.md) | `features/fidelidade/` |
