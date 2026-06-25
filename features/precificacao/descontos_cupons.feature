# language: pt
Funcionalidade: Descontos e Cupons Promocionais
  Como agente de precificação
  Eu quero aplicar descontos e cupons promocionais
  Para oferecer preços competitivos e honrar campanhas de marketing

  Cenário: Aplicar desconto de fidelidade nível Prata
    Dado que o cliente tem nível "Prata"
    E o desconto Prata é de 5%
    E a tarifa base é R$ 1.000,00
    Quando o PRE aplica desconto de fidelidade
    Então o preço final deve ser R$ 950,00
    E o breakdown deve mostrar "Desconto Fidelidade Prata: -R$ 50,00"

  Cenário: Aplicar desconto de fidelidade nível Diamante
    Dado que o cliente tem nível "Diamante"
    E o desconto Diamante é de 15%
    E a tarifa base é R$ 2.000,00
    Quando o PRE aplica desconto de fidelidade
    Então o preço final deve ser R$ 1.700,00

  Cenário: Aplicar cupom percentual válido
    Dado que o cupom "VERAO20" concede 20% de desconto
    E a tarifa é R$ 800,00
    E o cupom é válido para rotas nacionais
    Quando o cliente aplica o cupom em voo GRU-SSA
    Então o desconto deve ser R$ 160,00
    E o preço final deve ser R$ 640,00

  Cenário: Aplicar cupom de valor fixo
    Dado que o cupom "DESC100" concede R$ 100,00 de desconto
    E a tarifa é R$ 500,00
    Quando o cliente aplica o cupom
    Então o preço final deve ser R$ 400,00

  Cenário: Rejeitar cupom expirado
    Dado que o cupom "NATAL2025" expirou em "2025-12-31"
    Quando o cliente tenta aplicar o cupom
    Então deve retornar erro "cupom_expirado"
    E o preço original deve ser mantido

  Cenário: Rejeitar cupom esgotado
    Dado que o cupom "FLASH50" tem limite de 100 usos
    E já foram utilizados 100 cupons
    Quando o cliente tenta aplicar o cupom
    Então deve retornar erro "cupom_esgotado"

  Cenário: Rejeitar cupom incompatível com rota
    Dado que o cupom "EUROPA10" é válido apenas para destinos europeus
    Quando o cliente aplica em voo GRU-MIA
    Então deve retornar erro "cupom_rota_invalida"

  Cenário: Não acumular cupom com desconto de fidelidade
    Dado que o cliente é nível "Ouro" com 10% de desconto
    E tenta aplicar cupom "EXTRA15" de 15%
    E a política não permite acúmulo
    Quando o PRE processa os descontos
    Então deve aplicar apenas o maior desconto (15%)
    E deve informar que descontos não são cumulativos

  Cenário: Aplicar cupom com valor mínimo de compra
    Dado que o cupom "VIP200" exige compra mínima de R$ 1.500,00
    E a tarifa atual é R$ 1.200,00
    Quando o cliente tenta aplicar o cupom
    Então deve retornar erro "valor_minimo_nao_atingido"

  Cenário: Calcular resgate parcial em milhas
    Dado que o cliente tem 50.000 milhas disponíveis
    E a tarifa é R$ 2.500,00
    E o cliente quer usar 30.000 milhas (equivalente a R$ 900,00)
    Quando o PRE calcula split payment
    Então R$ 900,00 deve ser abatido via milhas
    E R$ 1.600,00 deve ser cobrado em dinheiro

  Cenário: Validar cupom gerado pelo Agente de Marketing
    Dado que o MKT gerou cupom "MKT-CAMP-2026" para campanha Black Friday
    Quando o PRE valida o cupom
    Então deve verificar origem, validade e regras no sistema MKT
    E deve registrar uso para analytics de conversão

  Cenário: Limitar desconto máximo do cupom
    Dado que o cupom "MEGA30" concede 30% com teto de R$ 500,00
    E a tarifa é R$ 3.000,00
    Quando o PRE aplica o cupom
    Então o desconto deve ser R$ 500,00 (não R$ 900,00)
