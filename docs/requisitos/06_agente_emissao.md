# Requisitos — Agente de Emissão de Bilhetes (EMI)

> **Responsabilidade:** Emitir bilhetes eletrônicos (e-tickets), gerar boarding passes e integrar com sistemas das companhias aéreas.

---

## Requisitos Funcionais

| ID | Requisito | Prioridade |
|----|-----------|------------|
| EMI-RF01 | Deve emitir e-ticket após confirmação de pagamento | Alta |
| EMI-RF02 | Deve gerar número de bilhete único (13 dígitos padrão IATA) | Alta |
| EMI-RF03 | Deve gerar QR code para check-in mobile | Alta |
| EMI-RF04 | Deve gerar boarding pass em formato PDF | Alta |
| EMI-RF05 | Deve integrar com sistema BSP (Billing and Settlement Plan) | Alta |
| EMI-RF06 | Deve registrar bilhete no GDS | Alta |
| EMI-RF07 | Deve suportar emissão de bilhete infantil (INF/CHD) vinculado ao adulto | Alta |
| EMI-RF08 | Deve emitir bilhete com informações de bagagem incluída | Alta |
| EMI-RF09 | Deve suportar reemissão de bilhete (alteração de voo) | Alta |
| EMI-RF10 | Deve suportar void de bilhete (dentro de 24h) | Alta |
| EMI-RF11 | Deve gerar itinerário detalhado do passageiro para multi-trechos | Média |
| EMI-RF12 | Deve enviar bilhete para o Agente de Notificações | Alta |
| EMI-RF13 | Deve validar conformidade com regras IATA (Reso 792) | Alta |
| EMI-RF14 | Deve suportar bilhete codeshare (múltiplas companhias) | Média |
| EMI-RF15 | Deve armazenar bilhete com backup redundante em região separada | Alta |
| EMI-RF16 | Deve gerar cupom de voo separado para cada trecho em viagem multi-trecho | Alta |

---

## Requisitos Não-Funcionais

| ID | Requisito | Métrica |
|----|-----------|---------|
| EMI-RNF01 | Tempo de emissão de bilhete | < 3s |
| EMI-RNF02 | Disponibilidade | 99.99% |
| EMI-RNF03 | Retenção de dados de bilhetes | Mínimo 5 anos |
| EMI-RNF04 | Formato de bilhete | Conformidade IATA Reso 792 |
| EMI-RNF05 | Redundância de armazenamento | Multi-região |
