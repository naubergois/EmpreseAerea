# Requisitos — Agente de Atendimento ao Cliente (ATC)

> **Responsabilidade:** Responder dúvidas, resolver problemas, processar reclamações e escalar para atendimento humano quando necessário.

---

## Requisitos Funcionais

| ID | Requisito | Prioridade |
|----|-----------|------------|
| ATC-RF01 | Deve responder perguntas frequentes (FAQ) automaticamente | Alta |
| ATC-RF02 | Deve consultar status de reserva por PNR ou e-mail | Alta |
| ATC-RF03 | Deve processar solicitações de alteração de voo | Alta |
| ATC-RF04 | Deve processar solicitações de cancelamento | Alta |
| ATC-RF05 | Deve processar solicitações de reembolso | Alta |
| ATC-RF06 | Deve informar políticas de bagagem por companhia e rota | Média |
| ATC-RF07 | Deve informar requisitos de documentação para viagem internacional | Média |
| ATC-RF08 | Deve escalar para atendente humano quando não conseguir resolver | Alta |
| ATC-RF09 | Deve registrar todas as interações em log de atendimento | Alta |
| ATC-RF10 | Deve classificar o sentimento do cliente (positivo/negativo/neutro) | Média |
| ATC-RF11 | Deve suportar múltiplos idiomas (PT, EN, ES) | Alta |
| ATC-RF12 | Deve suportar atendimento via chat, e-mail e telefone | Alta |
| ATC-RF13 | Deve gerar protocolo de atendimento único | Alta |
| ATC-RF14 | Deve acessar histórico completo do cliente (reservas, pagamentos, bilhetes) | Alta |
| ATC-RF15 | Deve processar reclamações e registrar no sistema de qualidade | Alta |
| ATC-RF16 | Deve detectar urgência no atendimento (voo iminente) | Alta |
| ATC-RF17 | Deve sugerir soluções proativas baseadas no contexto | Média |

---

## Requisitos Não-Funcionais

| ID | Requisito | Métrica |
|----|-----------|---------|
| ATC-RNF01 | Tempo de primeira resposta | < 5s |
| ATC-RNF02 | Taxa de resolução sem humano | > 80% |
| ATC-RNF03 | Disponibilidade | 24/7, 99.9% |
| ATC-RNF04 | CSAT (satisfação do cliente) | > 4.0/5.0 |
| ATC-RNF05 | Tempo máximo antes de escalação | < 5min |
