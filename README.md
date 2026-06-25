# SkyAgent — Plataforma Multi-Agente para Empresa Aérea

> Sistema de agentes inteligentes coordenados para venda, emissão de bilhetes e marketing de passagens aéreas.

---

## Estrutura do Projeto

```
EmpreseAerea/
├── README.md
├── docs/
│   └── requisitos/
│       ├── 00_visao_geral.md          # Arquitetura e visão geral do sistema
│       ├── 01_agente_orquestrador.md  # Coordenação do pipeline
│       ├── 02_agente_busca_voos.md     # Pesquisa de voos
│       ├── 03_agente_precificacao.md   # Precificação dinâmica
│       ├── 04_agente_reserva.md        # Reservas e PNR
│       ├── 05_agente_pagamento.md      # Processamento de pagamentos
│       ├── 06_agente_emissao.md        # Emissão de e-tickets
│       ├── 07_agente_marketing.md      # Campanhas e conversão
│       ├── 08_agente_atendimento.md    # Suporte ao cliente
│       ├── 09_agente_notificacoes.md   # Envio de notificações
│       └── 10_agente_fidelidade.md     # Programa de milhas
├── features/
│   ├── orquestrador/                   # 4 arquivos
│   ├── busca_voos/                     # 5 arquivos
│   ├── precificacao/                   # 3 arquivos
│   ├── reserva/                        # 6 arquivos
│   ├── pagamento/                      # 6 arquivos
│   ├── emissao/                        # 3 arquivos
│   ├── marketing/                      # 5 arquivos
│   ├── atendimento/                    # 5 arquivos
│   ├── notificacoes/                   # 3 arquivos
│   └── fidelidade/                     # 4 arquivos
```

---

## Arquitetura de Agentes

```
┌─────────────────────────────────────────────────────────┐
│                  AGENTE ORQUESTRADOR (ORC)               │
│            Coordenação · Saga · Circuit Breaker          │
└──────────┬──────────┬──────────┬──────────┬─────────────┘
           │          │          │          │
    ┌──────▼──┐ ┌─────▼───┐ ┌───▼────┐ ┌──▼──────────┐
    │ BUS     │ │ MKT     │ │ ATC    │ │ NOT         │
    └──────┬──┘ └─────┬───┘ └───┬────┘ └─────────────┘
    ┌──────▼──────┐   │         │
    │ PRE         │   │         │
    └──────┬──────┘   │         │
    ┌──────▼──┐       │         │
    │ RES     │       │         │
    └──────┬──┘       │         │
    ┌──────▼──────┐   │         │
    │ PAG         │   │         │
    └──────┬──────┘   │         │
    ┌──────▼──────┐ ┌─▼───┐    │
    │ EMI         │ │ FID │    │
    └─────────────┘ └─────┘    │
```

## Pipelines

| Pipeline | Agentes | Descrição |
|----------|---------|-----------|
| **Venda** | BUS → PRE → RES → PAG → EMI → FID → NOT | Compra e emissão end-to-end |
| **Marketing** | MKT → FID → NOT | Campanhas, remarketing e conversão |
| **Suporte** | ATC → RES/PAG/EMI → NOT | Atendimento e pós-venda |

---

## Totais

| Categoria | Quantidade |
|-----------|------------|
| Agentes | 10 |
| Arquivos de Requisitos | 11 |
| Arquivos de Features BDD | 44 |
| Cenários BDD | 400+ |

---

## Testes

> Guia completo: [docs/guia_implementacao.md — Seção 11](docs/guia_implementacao.md#11-testes--rodar-a-cada-nova-funcionalidade)

**Regra:** rode todos os testes ao criar ou alterar funcionalidades, antes de cada commit.

```bash
# Suíte completa (recomendado)
./scripts/test-all.sh

# Backend — pytest
cd backend && source venv/bin/activate && pytest tests/ -v

# BDD — behave
cd features && behave busca_voos/ reserva/ orquestrador/ -v

# Frontend — build
cd frontend && npm run build
```

| Tipo | Comando | Quando |
|------|---------|--------|
| Unitário + integração | `pytest tests/ -v` | A cada alteração no backend |
| BDD por agente | `behave features/<agente>/` | Ao implementar requisito |
| Build frontend | `npm run build` | Ao alterar React |
| Docker Vite | `npm run test:docker` | Ao alterar Dockerfile/frontend |

