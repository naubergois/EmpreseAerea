# Requisitos — Agente de Notificações (NOT)

> **Responsabilidade:** Enviar notificações transacionais e informativas ao cliente por múltiplos canais.

---

## Requisitos Funcionais

| ID | Requisito | Prioridade |
|----|-----------|------------|
| NOT-RF01 | Deve enviar confirmação de reserva por e-mail | Alta |
| NOT-RF02 | Deve enviar confirmação de pagamento por e-mail | Alta |
| NOT-RF03 | Deve enviar e-ticket e boarding pass por e-mail | Alta |
| NOT-RF04 | Deve enviar lembrete de check-in (24h antes do voo) | Alta |
| NOT-RF05 | Deve notificar alterações de voo (atraso, cancelamento, gate) | Alta |
| NOT-RF06 | Deve enviar notificações por SMS | Alta |
| NOT-RF07 | Deve enviar push notifications via app | Média |
| NOT-RF08 | Deve enviar notificações via WhatsApp Business API | Média |
| NOT-RF09 | Deve personalizar templates por idioma do cliente | Alta |
| NOT-RF10 | Deve gerenciar preferências de canal por cliente | Média |
| NOT-RF11 | Deve rastrear entrega e abertura de notificações | Média |
| NOT-RF12 | Deve implementar throttling para evitar spam | Alta |
| NOT-RF13 | Deve suportar anexos (PDF do bilhete, boarding pass) | Alta |
| NOT-RF14 | Deve enviar notificação de reembolso processado | Alta |
| NOT-RF15 | Deve enviar notificação de milhas acumuladas | Média |
| NOT-RF16 | Deve enviar notificação de milhas prestes a expirar | Média |

---

## Requisitos Não-Funcionais

| ID | Requisito | Métrica |
|----|-----------|---------|
| NOT-RNF01 | Tempo de envio de notificação transacional | < 30s |
| NOT-RNF02 | Taxa de entrega | > 99% |
| NOT-RNF03 | Disponibilidade | 99.9% |
| NOT-RNF04 | Máximo de notificações por cliente por dia | Configurável (default: 5) |
