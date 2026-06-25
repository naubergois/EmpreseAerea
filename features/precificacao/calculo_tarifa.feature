# language: pt
Funcionalidade: Cálculo de Tarifa
  Como agente de precificação
  Eu quero calcular o valor completo da passagem
  Para apresentar preço transparente ao cliente

  Cenário: Calcular tarifa básica com taxas e impostos
    Dado que o voo LATAM LA3421 tem tarifa base de R$ 380,00
    E as taxas aeroportuárias são R$ 45,00
    E os impostos são R$ 25,00
    Quando o Agente de Precificação calcula o valor
    Então o preço final deve ser R$ 450,00
    E o breakdown deve listar: base, taxas, impostos

  Cenário: Calcular tarifa para ida e volta
    Dado que a ida GRU-GIG custa R$ 250,00
    E a volta GIG-GRU custa R$ 280,00
    E as taxas totais são R$ 90,00
    Quando o PRE calcula o pacote ida e volta
    Então o preço total deve ser R$ 620,00
    E deve exibir preço por trecho separadamente

  Cenário: Calcular tarifa para múltiplos passageiros
    Dado que são 2 adultos a R$ 400,00 cada
    E 1 criança (CHD) a 75% do adulto
    E 1 bebê (INF) a 10% do adulto
    Quando o PRE calcula o total
    Então o valor do adulto deve ser R$ 400,00 x 2 = R$ 800,00
    E o valor da criança deve ser R$ 300,00
    E o valor do bebê deve ser R$ 40,00
    E o total deve ser R$ 1.140,00 + taxas

  Cenário: Calcular tarifa internacional com taxa de embarque internacional
    Dado que o voo GRU-MIA tem tarifa base de R$ 2.800,00
    E a taxa de embarque internacional é R$ 185,00
    E o imposto de saída do país é R$ 45,00
    Quando o PRE calcula o valor
    Então o preço final deve incluir todas as taxas internacionais
    E o breakdown deve estar em conformidade com ANAC

  Cenário: Calcular tarifa multi-trecho
    Dado que o itinerário é GRU-LIS + LIS-CDG + CDG-GRU
    E cada trecho tem tarifa independente
    Quando o PRE calcula o pacote multi-destino
    Então o preço total deve ser a soma dos trechos
    E cada trecho deve ter breakdown individual

  Cenário: Rejeitar cálculo com dados de voo inválidos
    Dado que o voo informado não existe no inventário
    Quando o PRE tenta calcular a tarifa
    Então deve retornar erro "voo_nao_encontrado"
    E nenhum preço deve ser exibido

  Cenário: Calcular taxa de serviços extras
    Dado que o cliente adicionou 1 bagagem extra de 23kg por R$ 120,00
    E 1 refeição especial por R$ 45,00
    E 1 seguro viagem por R$ 89,00
    Quando o PRE calcula o total com extras
    Então os extras devem somar R$ 254,00 ao valor da passagem
    E cada extra deve aparecer no breakdown

  Cenário: Calcular tarifa em moeda estrangeira
    Dado que a tarifa GDS está em USD 450,00
    E a taxa de câmbio do dia é R$ 5,20
    Quando o PRE converte para BRL
    Então o preço em BRL deve ser R$ 2.340,00
    E deve registrar a taxa de câmbio utilizada

  Cenário: Aplicar markup comercial por canal
    Dado que a tarifa base é R$ 500,00
    E o markup do canal "app mobile" é 3%
    E o markup do canal "website" é 5%
    Quando o PRE calcula para o app mobile
    Então o preço final deve incluir markup de R$ 15,00

  Cenário: Retornar cotação com ID e validade
    Dado que o PRE calculou tarifa de R$ 890,00
    Quando a cotação é emitida
    Então deve gerar ID de cotação único
    E a cotação deve ser válida por 20 minutos
    E o timestamp de expiração deve ser retornado
