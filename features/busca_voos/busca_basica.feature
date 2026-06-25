# language: pt
Funcionalidade: Busca Básica de Voos
  Como cliente
  Eu quero buscar voos disponíveis
  Para encontrar a melhor opção para minha viagem

  Cenário: Buscar voo somente ida
    Dado que o cliente deseja viajar de "GRU" para "GIG"
    E a data de ida é "2026-08-15"
    E a busca é somente ida
    E a classe é econômica
    Quando o Agente de Busca processa a requisição
    Então deve retornar ao menos 1 voo disponível
    E cada voo deve conter: companhia, número, horário de partida, horário de chegada, duração
    E o tempo de resposta deve ser inferior a 3 segundos

  Cenário: Buscar voo ida e volta
    Dado que o cliente deseja viajar de "GRU" para "MIA"
    E a data de ida é "2026-12-20"
    E a data de volta é "2026-12-30"
    E a classe é econômica
    E são 2 passageiros adultos
    Quando o Agente de Busca processa a requisição
    Então deve retornar combinações de ida e volta
    E o preço exibido deve ser por passageiro
    E o preço total deve considerar 2 passageiros
    E cada resultado deve mostrar o tempo total de viagem

  Cenário: Buscar voo multi-destino
    Dado que o cliente deseja a seguinte rota:
      | Origem | Destino | Data       |
      | GRU    | LIS     | 2026-09-01 |
      | LIS    | CDG     | 2026-09-05 |
      | CDG    | GRU     | 2026-09-10 |
    Quando o Agente de Busca processa a requisição
    Então deve retornar opções para cada trecho
    E os trechos devem ser compatíveis entre si
    E o preço total deve incluir todos os trechos

  Cenário: Buscar voo com datas flexíveis
    Dado que o cliente busca voos de "GRU" para "LIS"
    E a data desejada é "2026-10-15"
    E a busca é flexível com margem de 3 dias
    Quando o Agente de Busca processa a requisição
    Então deve retornar voos de 12/10 a 18/10/2026
    E deve destacar o menor preço encontrado
    E deve indicar a data com melhor tarifa

  Cenário: Buscar voo por nome de cidade em vez de código IATA
    Dado que o cliente busca voos de "São Paulo" para "Rio de Janeiro"
    Quando o Agente de Busca resolve os nomes
    Então "São Paulo" deve ser resolvido para aeroportos "GRU" e "CGH"
    E "Rio de Janeiro" deve ser resolvido para aeroportos "GIG" e "SDU"
    E a busca deve incluir combinações de todos os aeroportos

  Cenário: Buscar voo sem resultados disponíveis
    Dado que o cliente busca voos de "GRU" para "TNR"
    E a data é "2026-08-15"
    E não existem voos disponíveis nesta data
    Quando o Agente de Busca processa a requisição
    Então deve retornar lista vazia de resultados
    E deve sugerir datas alternativas próximas
    E deve sugerir rotas alternativas com conexão
    E deve registrar a busca sem resultado para análise de demanda

  Cenário: Buscar voo para passageiro com necessidades especiais
    Dado que o cliente busca voos de "GRU" para "GIG"
    E o passageiro necessita de cadeira de rodas
    Quando o Agente de Busca processa a requisição
    Então deve retornar apenas voos em aeronaves que suportam cadeirantes
    E deve indicar se o aeroporto de destino tem acessibilidade
    E deve adicionar flag "special_assistance_required"

  Cenário: Exibir informações de bagagem nos resultados
    Dado que o cliente busca voos de "GRU" para "SCL"
    Quando os resultados são retornados
    Então cada resultado deve indicar a franquia de bagagem incluída
    E deve informar peso máximo da bagagem de mão
    E deve informar se despacho de bagagem está incluso
    E deve mostrar o custo de bagagem adicional se aplicável

  Cenário: Buscar voo para 1 adulto e 1 bebê de colo
    Dado que o cliente busca voos de "CGH" para "SDU"
    E são 1 adulto e 1 bebê de colo (INF)
    Quando o Agente de Busca processa a requisição
    Então deve retornar voos disponíveis
    E o resultado deve mostrar preço do adulto
    E o resultado deve mostrar preço do bebê separadamente (10% do adulto)
    E deve verificar disponibilidade de cinto infantil na aeronave

  Cenário: Buscar voos em data de alta demanda (Carnaval)
    Dado que o cliente busca voos de "GRU" para "SSA"
    E a data é no período de Carnaval "2027-02-25"
    Quando o Agente de Busca processa a requisição
    Então deve retornar os voos disponíveis com preços ajustados
    E deve indicar que a data é de alta demanda
    E a disponibilidade pode ser limitada
