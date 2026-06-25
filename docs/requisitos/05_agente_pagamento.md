# Requisitos — Agente de Pagamento (PAG)

> **Responsabilidade:** Processar pagamentos, estornos, parcelamentos, prevenção a fraude e conciliação financeira.

---

## Requisitos Funcionais

| ID | Requisito | Prioridade |
|----|-----------|------------|
| PAG-RF01 | Deve processar pagamento com cartão de crédito (Visa, Master, Amex, Elo) | Alta |
| PAG-RF02 | Deve processar pagamento com cartão de débito | Alta |
| PAG-RF03 | Deve processar pagamento via PIX com QR code dinâmico | Alta |
| PAG-RF04 | Deve processar pagamento via boleto bancário com vencimento configurável | Alta |
| PAG-RF05 | Deve suportar parcelamento de 2x a 12x sem juros (configurável) | Média |
| PAG-RF06 | Deve validar cartão (número, CVV, validade) antes de cobrança | Alta |
| PAG-RF07 | Deve integrar autenticação 3D Secure 2.0 | Alta |
| PAG-RF08 | Deve executar análise antifraude antes de aprovar transação | Alta |
| PAG-RF09 | Deve processar estorno total e parcial | Alta |
| PAG-RF10 | Deve garantir idempotência via chave única por transação | Alta |
| PAG-RF11 | Deve suportar pagamento split (cartão + milhas) | Média |
| PAG-RF12 | Deve tokenizar dados de cartão (PCI-DSS) sem armazenar PAN | Alta |
| PAG-RF13 | Deve emitir recibo eletrônico após aprovação | Alta |
| PAG-RF14 | Deve notificar ORC sobre aprovação/recusa em tempo real | Alta |
| PAG-RF15 | Deve processar reembolso automático em caso de rollback da Saga | Alta |
| PAG-RF16 | Deve conciliar transações com gateway e BSP diariamente | Alta |
| PAG-RF17 | Deve bloquear transações de países em lista de sanções | Alta |
| PAG-RF18 | Deve suportar pagamento em múltiplas moedas (BRL, USD, EUR) | Média |

---

## Requisitos Não-Funcionais

| ID | Requisito | Métrica |
|----|-----------|---------|
| PAG-RNF01 | Tempo de processamento de pagamento | < 5s |
| PAG-RNF02 | Taxa de aprovação (excluindo fraude legítima) | > 95% |
| PAG-RNF03 | Disponibilidade | 99.99% |
| PAG-RNF04 | Conformidade | PCI-DSS Level 1 |
| PAG-RNF05 | Taxa de falsos positivos antifraude | < 2% |
