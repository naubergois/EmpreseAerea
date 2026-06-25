# Requisitos — Agente de Precificação Dinâmica (PRE)

> **Responsabilidade:** Calcular tarifas completas com taxas, impostos, descontos e regras de precificação dinâmica, garantindo transparência e margem comercial.

---

## Requisitos Funcionais

| ID | Requisito | Prioridade |
|----|-----------|------------|
| PRE-RF01 | Deve calcular preço base da tarifa aérea por passageiro e trecho | Alta |
| PRE-RF02 | Deve adicionar taxas aeroportuárias (DU, TSA, YQ/YR) ao valor final | Alta |
| PRE-RF03 | Deve calcular impostos conforme jurisdição (ISS, PIS/COFINS) | Alta |
| PRE-RF04 | Deve retornar breakdown detalhado de todos os componentes de preço | Alta |
| PRE-RF05 | Deve aplicar precificação dinâmica baseada em demanda e ocupação | Alta |
| PRE-RF06 | Deve aplicar desconto por nível de fidelidade (Bronze a Diamante) | Alta |
| PRE-RF07 | Deve validar e aplicar cupons promocionais do Agente de Marketing | Alta |
| PRE-RF08 | Deve garantir preço cotado por 20 minutos após emissão da cotação | Alta |
| PRE-RF09 | Deve calcular preço para múltiplos passageiros (ADT/CHD/INF) | Alta |
| PRE-RF10 | Deve calcular taxa de serviços extras (bagagem, refeição, seguro) | Média |
| PRE-RF11 | Deve aplicar markup comercial configurável por rota e canal | Alta |
| PRE-RF12 | Deve comparar preço com concorrentes e ajustar dentro de limites | Média |
| PRE-RF13 | Deve rejeitar cupons expirados, esgotados ou incompatíveis com rota | Alta |
| PRE-RF14 | Deve calcular preço de resgate parcial em milhas (split payment) | Média |
| PRE-RF15 | Deve registrar histórico de cotações para auditoria | Alta |
| PRE-RF16 | Deve sinalizar alteração de preço quando tarifa GDS mudar durante sessão | Alta |

---

## Requisitos Não-Funcionais

| ID | Requisito | Métrica |
|----|-----------|---------|
| PRE-RNF01 | Tempo de cálculo de cotação | < 500ms |
| PRE-RNF02 | Precisão aritmética | Zero arredondamento incorreto |
| PRE-RNF03 | Disponibilidade | 99.95% |
| PRE-RNF04 | Consistência preço exibido vs. cobrado | 100% |

---

## Regras de Precificação Dinâmica

| Fator | Impacto no Preço | Limite |
|-------|-----------------|--------|
| Ocupação > 85% | +5% a +15% | Máx. +15% |
| Ocupação < 50% | -5% a -10% | Máx. -10% |
| Alta demanda (feriado) | +10% a +25% | Configurável |
| Antecedência < 7 dias | +5% a +20% | Configurável |
| Antecedência > 60 dias | -3% a -8% | Configurável |
