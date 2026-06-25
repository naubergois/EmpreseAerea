# language: pt
Funcionalidade: Ordenação de Resultados de Busca
  Como cliente
  Eu quero ordenar os resultados da busca
  Para encontrar rapidamente o voo mais adequado

  Cenário: Ordenar resultados por menor preço
    Dado que o cliente busca voos de "CGH" para "SDU"
    E o critério de ordenação é "menor preço"
    Quando os resultados são retornados
    Então o primeiro voo deve ter o menor preço
    E os voos devem estar em ordem crescente de preço

  Cenário: Ordenar resultados por maior preço
    Dado que o cliente busca voos de "GRU" para "JFK"
    E o critério de ordenação é "maior preço"
    Quando os resultados são retornados
    Então o primeiro voo deve ter o maior preço
    E os voos devem estar em ordem decrescente de preço

  Cenário: Ordenar resultados por menor duração
    Dado que o cliente busca voos de "GRU" para "LIS"
    E o critério de ordenação é "menor duração"
    Quando os resultados são retornados
    Então o primeiro voo deve ter a menor duração total
    E os voos devem estar em ordem crescente de duração

  Cenário: Ordenar resultados por horário de partida
    Dado que o cliente busca voos de "GRU" para "BSB"
    E o critério de ordenação é "horário de partida"
    Quando os resultados são retornados
    Então o primeiro voo deve ter o horário de partida mais cedo
    E os voos devem estar em ordem cronológica

  Cenário: Ordenar resultados por relevância
    Dado que o cliente busca voos de "GRU" para "FCO"
    E o critério de ordenação é "relevância"
    Quando os resultados são retornados
    Então os voos devem ser ordenados por score de relevância
    E o score deve considerar preço com peso 40%
    E o score deve considerar duração com peso 30%
    E o score deve considerar escalas com peso 30%

  Cenário: Ordenação padrão quando nenhum critério é escolhido
    Dado que o cliente busca voos de "GRU" para "GIG"
    E nenhum critério de ordenação é selecionado
    Quando os resultados são retornados
    Então a ordenação padrão deve ser "relevância"
