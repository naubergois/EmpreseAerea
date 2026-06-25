# language: pt
Funcionalidade: Precificação Dinâmica
  Como sistema comercial
  Eu quero ajustar preços baseado em demanda e ocupação
  Para maximizar receita e competitividade

  Cenário: Aumentar preço em alta ocupação
    Dado que o voo GOL G3100 tem ocupação de 92%
    E a regra de alta ocupação prevê +10%
    Quando o PRE aplica precificação dinâmica
    Então o preço base de R$ 400,00 deve ser ajustado para R$ 440,00
    E deve registrar fator aplicado "high_occupancy_+10%"

  Cenário: Reduzir preço em baixa ocupação
    Dado que o voo Azul AD4521 tem ocupação de 35%
    E a regra de baixa ocupação prevê -8%
    Quando o PRE aplica precificação dinâmica
    Então o preço base de R$ 600,00 deve ser ajustado para R$ 552,00

  Cenário: Aplicar surcharge de alta demanda em feriado
    Dado que a data é Carnaval "2027-02-25"
    E a rota GRU-SSA tem surcharge de +20%
    Quando o PRE calcula a tarifa
    Então o surcharge de alta demanda deve ser aplicado
    E deve indicar "Período de alta demanda" ao cliente

  Cenário: Desconto por antecedência de compra
    Dado que a compra é feita 90 dias antes do voo
    E a regra prevê -5% para antecedência > 60 dias
    Quando o PRE aplica a regra
    Então o preço deve ter desconto de 5%

  Cenário: Surcharge por compra de última hora
    Dado que a compra é feita 2 dias antes do voo
    E a regra prevê +15% para antecedência < 7 dias
    Quando o PRE aplica a regra
    Então o preço deve ter acréscimo de 15%

  Cenário: Respeitar limite máximo de ajuste dinâmico
    Dado que múltiplos fatores somariam +30%
    E o limite máximo configurado é +15%
    Quando o PRE aplica precificação dinâmica
    Então o ajuste final deve ser limitado a +15%

  Cenário: Comparar preço com concorrente e ajustar
    Dado que nosso preço GRU-GIG é R$ 480,00
    E o concorrente pratica R$ 450,00
    E a regra permite ajuste até -5% para match
    Quando o PRE executa price matching
    Então o preço pode ser ajustado para R$ 455,00 no máximo

  Cenário: Não aplicar precificação dinâmica em tarifa promocional
    Dado que o voo tem tarifa promocional fixa de R$ 199,00
    Quando o PRE recebe a solicitação
    Então a precificação dinâmica não deve ser aplicada
    E o preço deve permanecer R$ 199,00

  Cenário: Detectar alteração de tarifa GDS durante sessão
    Dado que a cotação foi emitida com preço R$ 750,00
    E a tarifa GDS mudou para R$ 820,00 em 10 minutos
    Quando o cliente prossegue para reserva
    Então o PRE deve sinalizar "preco_alterado"
    E deve exibir novo preço R$ 820,00
    E deve solicitar confirmação do cliente

  Cenário: Garantir preço cotado dentro da validade
    Dado que a cotação QUOTE-789 foi emitida há 15 minutos
    E a validade é de 20 minutos
    Quando o cliente confirma a compra
    Então o preço cotado deve ser honrado
    E nenhum reajuste deve ser aplicado

  Cenário: Expirar cotação após 20 minutos
    Dado que a cotação QUOTE-456 foi emitida há 25 minutos
    Quando o cliente tenta prosseguir
    Então a cotação deve estar expirada
    E um novo cálculo deve ser solicitado
    E o cliente deve ser informado da expiração
