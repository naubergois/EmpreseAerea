# Requisitos — Agente de Fidelidade (FID)

> **Responsabilidade:** Gerenciar programa de milhas/pontos, níveis de fidelidade, resgate de benefícios e parcerias.

---

## Requisitos Funcionais

| ID | Requisito | Prioridade |
|----|-----------|------------|
| FID-RF01 | Deve acumular milhas/pontos por compra realizada | Alta |
| FID-RF02 | Deve calcular milhas baseado no trecho voado e classe | Alta |
| FID-RF03 | Deve gerenciar níveis de fidelidade (Bronze, Prata, Ouro, Diamante) | Alta |
| FID-RF04 | Deve permitir resgate de milhas por passagens | Alta |
| FID-RF05 | Deve permitir resgate de milhas por upgrades de classe | Média |
| FID-RF06 | Deve transferir milhas entre contas | Média |
| FID-RF07 | Deve acumular milhas de parceiros (hotéis, locadoras, cartões) | Média |
| FID-RF08 | Deve expirar milhas não utilizadas após 24 meses | Alta |
| FID-RF09 | Deve notificar cliente sobre milhas prestes a expirar (30/60/90 dias) | Média |
| FID-RF10 | Deve calcular benefícios por nível (sala VIP, prioridade embarque, upgrade) | Alta |
| FID-RF11 | Deve gerar extrato detalhado de milhas (acúmulo, resgate, expiração) | Média |
| FID-RF12 | Deve integrar com Agente de Marketing para ofertas exclusivas por nível | Alta |
| FID-RF13 | Deve aplicar bônus de milhas em promoções especiais | Média |
| FID-RF14 | Deve validar milhas suficientes antes do resgate | Alta |
| FID-RF15 | Deve calcular qualificação para upgrade de nível | Alta |
| FID-RF16 | Deve processar rebaixamento de nível por inatividade | Média |

---

## Requisitos Não-Funcionais

| ID | Requisito | Métrica |
|----|-----------|---------|
| FID-RNF01 | Tempo de acúmulo de milhas | < 1s (síncrono) |
| FID-RNF02 | Consistência do saldo | Zero discrepância |
| FID-RNF03 | Disponibilidade | 99.9% |
| FID-RNF04 | Auditabilidade de transações de milhas | 100% rastreável |

---

## Regras de Negócio — Níveis de Fidelidade

| Nível | Milhas Necessárias/Ano | Benefícios |
|-------|----------------------|------------|
| Bronze | 0 - 9.999 | Acúmulo padrão |
| Prata | 10.000 - 29.999 | Acúmulo 1.25x, prioridade check-in |
| Ouro | 30.000 - 59.999 | Acúmulo 1.5x, sala VIP, 10% desconto |
| Diamante | 60.000+ | Acúmulo 2x, sala VIP, upgrade grátis, 15% desconto |
