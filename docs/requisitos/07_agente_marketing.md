# Requisitos — Agente de Marketing (MKT)

> **Responsabilidade:** Criar campanhas, segmentar clientes, personalizar ofertas, remarketing e analytics de conversão para aumentar vendas de passagens.

---

## Requisitos Funcionais

| ID | Requisito | Prioridade |
|----|-----------|------------|
| MKT-RF01 | Deve segmentar clientes por comportamento (buscas, compras, abandono) | Alta |
| MKT-RF02 | Deve segmentar clientes por nível de fidelidade e demografia | Alta |
| MKT-RF03 | Deve criar e gerenciar campanhas de e-mail marketing | Alta |
| MKT-RF04 | Deve executar remarketing de carrinho abandonado | Alta |
| MKT-RF05 | Deve gerar e validar cupons promocionais (percentual e valor fixo) | Alta |
| MKT-RF06 | Deve personalizar ofertas por rota de interesse do cliente | Alta |
| MKT-RF07 | Deve respeitar opt-out e preferências de comunicação (LGPD) | Alta |
| MKT-RF08 | Deve medir taxa de abertura, clique e conversão por campanha | Alta |
| MKT-RF09 | Deve disparar campanhas sazonais (Black Friday, Carnaval, férias) | Média |
| MKT-RF10 | Deve integrar com Agente de Fidelidade para ofertas exclusivas por nível | Alta |
| MKT-RF11 | Deve enviar alertas de queda de preço em rotas monitoradas | Média |
| MKT-RF12 | Deve criar landing pages dinâmicas por campanha | Média |
| MKT-RF13 | Deve fazer A/B testing de assuntos e conteúdo de e-mail | Média |
| MKT-RF14 | Deve limitar frequência de envio por cliente (frequency capping) | Alta |
| MKT-RF15 | Deve integrar com Agente de Notificações para envio multicanal | Alta |
| MKT-RF16 | Deve registrar ROI por campanha (custo vs. receita gerada) | Alta |
| MKT-RF17 | Deve reativar clientes inativos com ofertas personalizadas | Média |
| MKT-RF18 | Deve cruzar dados de buscas sem resultado para campanhas de demanda | Média |

---

## Requisitos Não-Funcionais

| ID | Requisito | Métrica |
|----|-----------|---------|
| MKT-RNF01 | Tempo de segmentação de base | < 30s para 1M clientes |
| MKT-RNF02 | Taxa de entrega de campanhas | > 98% |
| MKT-RNF03 | Disponibilidade | 99.9% |
| MKT-RNF04 | Conformidade | LGPD/GDPR |
| MKT-RNF05 | Latência remarketing pós-abandono | < 1h |

---

## Integração com Pipeline de Venda

| Evento | Ação do MKT |
|--------|-------------|
| `search.flights.no_results` | Campanha de rotas alternativas |
| `reservation.created` + timeout | Remarketing carrinho abandonado |
| `payment.approved` | Cross-sell (hotel, seguro viagem) |
| `ticket.issued` | Upsell upgrade de classe |
| `loyalty.level.upgraded` | Campanha exclusiva do novo nível |
