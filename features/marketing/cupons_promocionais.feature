# language: pt
Funcionalidade: Cupons Promocionais
  Como agente de marketing
  Eu quero criar e gerenciar cupons promocionais
  Para incentivar compras e medir efetividade de campanhas

  Cenário: Criar cupom percentual para campanha
    Dado que o MKT cria cupom "BF2026" com 25% de desconto
    E válido de "2026-11-20" a "2026-11-30"
    E limite de 10.000 usos
    Quando o cupom é ativado
    Então deve estar disponível para o PRE validar
    E deve aparecer na landing page da campanha

  Cenário: Criar cupom de valor fixo
    Dado que o cupom "DESC150" concede R$ 150,00 de desconto
    E exige compra mínima de R$ 800,00
    Quando o cliente aplica o cupom em compra de R$ 900,00
    Então o desconto de R$ 150,00 deve ser aplicado

  Cenário: Cupom exclusivo para nível Diamante
    Dado que o cupom "VIP30" é exclusivo para Diamante
    E o cliente é nível Ouro
    Quando tenta aplicar o cupom
    Então deve rejeitar com erro "cupom_nivel_insuficiente"

  Cenário: Cupom de uso único por cliente
    Dado que o cupom "UNICO10" permite 1 uso por cliente
    E o cliente já utilizou o cupom
    Quando tenta usar novamente
    Então deve rejeitar com erro "cupom_ja_utilizado"

  Cenário: Cupom com limite global esgotado
    Dado que o cupom "FLASH" tem limite de 500 usos
    E 500 já foram utilizados
    Quando novo cliente tenta aplicar
    Então deve rejeitar com erro "cupom_esgotado"

  Cenário: Cupom válido apenas para rotas específicas
    Dado que o cupom "NORDESTE" é válido para destinos SSA, REC, FOR
    Quando aplicado em voo GRU-MIA
    Então deve rejeitar com erro "cupom_rota_invalida"

  Cenário: Gerar cupom automático para carrinho abandonado
    Dado que o cliente abandonou carrinho de R$ 1.200,00
    Quando a 2ª tentativa de remarketing é disparada
    Então o MKT deve gerar cupom único "REC-ABC123" de 5%
    E o cupom deve expirar em 48 horas

  Cenário: Rastrear uso de cupom por campanha
    Dado que a campanha Black Friday gerou 500 cupons utilizados
    Quando o MKT analisa resultados
    Então deve calcular receita gerada por cupons
    E ticket médio com cupom vs. sem cupom

  Cenário: Desativar cupom antecipadamente
    Dado que o cupom "VERAO20" está ativo
    E a demanda excedeu o planejado
    Quando o gestor desativa o cupom
    Então novos usos devem ser bloqueados
    E usos em andamento devem ser honrados

  Cenário: Cupom com bônus de milhas em vez de desconto
    Dado que o cupom "MILHAS2X" concede 2x milhas na compra
    Quando o cliente compra passagem de R$ 2.000,00
    Então o FID deve creditar o dobro de milhas
    E nenhum desconto em dinheiro deve ser aplicado
