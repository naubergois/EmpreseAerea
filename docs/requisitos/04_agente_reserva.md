# Requisitos — Agente de Reserva (RES)

> **Responsabilidade:** Gerenciar o processo de reserva de passagens, incluindo seleção de assentos, dados de passageiros e geração de PNR.

---

## Requisitos Funcionais

| ID | Requisito | Prioridade |
|----|-----------|------------|
| RES-RF01 | Deve criar reserva (PNR) com dados do passageiro | Alta |
| RES-RF02 | Deve validar dados do passageiro (nome, documento, contato) | Alta |
| RES-RF03 | Deve permitir seleção de assento | Alta |
| RES-RF04 | Deve suportar reserva para múltiplos passageiros | Alta |
| RES-RF05 | Deve reservar assento por tempo limitado (20 minutos) | Alta |
| RES-RF06 | Deve liberar assento automaticamente após timeout | Alta |
| RES-RF07 | Deve suportar reserva de serviços extras (refeição, bagagem, seguro) | Média |
| RES-RF08 | Deve validar regras de passageiro menor de idade | Alta |
| RES-RF09 | Deve validar necessidades especiais (cadeirante, acompanhante) | Alta |
| RES-RF10 | Deve suportar alteração de reserva (data, voo, assento) | Alta |
| RES-RF11 | Deve suportar cancelamento de reserva com cálculo de taxa | Alta |
| RES-RF12 | Deve gerar código PNR único de 6 caracteres alfanuméricos | Alta |
| RES-RF13 | Deve validar documentos de viagem (passaporte, visto) para voos internacionais | Alta |
| RES-RF14 | Deve verificar conflitos de horário com reservas existentes do cliente | Média |
| RES-RF15 | Deve enviar dados da reserva para o Agente de Pagamento | Alta |
| RES-RF16 | Deve manter histórico completo de alterações da reserva | Alta |
| RES-RF17 | Deve suportar reserva de bebê de colo vinculado a adulto | Alta |
| RES-RF18 | Deve validar assento de saída de emergência (idade mínima 18 anos) | Média |

---

## Requisitos Não-Funcionais

| ID | Requisito | Métrica |
|----|-----------|---------|
| RES-RNF01 | Tempo de criação de reserva | < 2s |
| RES-RNF02 | Consistência de dados | Zero duplicidade de PNR |
| RES-RNF03 | Tempo de timeout de reserva | Configurável (default: 20min) |
| RES-RNF04 | Disponibilidade | 99.95% |
| RES-RNF05 | Retenção de dados de reserva | Mínimo 3 anos |
