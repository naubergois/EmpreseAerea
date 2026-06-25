# language: pt
Funcionalidade: Filtros de Busca de Voos
  Como cliente
  Eu quero aplicar filtros na busca de voos
  Para encontrar opções que atendam minhas preferências

  Cenário: Filtrar voos por voo direto
    Dado que o cliente busca voos de "GRU" para "SSA"
    E o filtro de escalas é "direto"
    Quando o Agente de Busca processa a requisição
    Então todos os voos retornados devem ter 0 escalas
    E nenhum voo com conexão deve aparecer

  Cenário: Filtrar voos por máximo de 1 escala
    Dado que o cliente busca voos de "GRU" para "LHR"
    E o filtro de escalas é "máximo 1 escala"
    Quando o Agente de Busca processa a requisição
    Então todos os voos retornados devem ter 0 ou 1 escala
    E voos com 2 ou mais escalas não devem aparecer

  Cenário: Filtrar voos por companhia aérea LATAM
    Dado que o cliente busca voos de "GRU" para "EZE"
    E o filtro de companhia é "LATAM"
    Quando o Agente de Busca processa a requisição
    Então todos os voos retornados devem ser operados pela LATAM
    E voos de outras companhias não devem aparecer

  Cenário: Filtrar voos por múltiplas companhias
    Dado que o cliente busca voos de "GRU" para "LIS"
    E o filtro de companhia inclui "LATAM" e "TAP"
    Quando o Agente de Busca processa a requisição
    Então todos os voos retornados devem ser de LATAM ou TAP
    E voos de outras companhias não devem aparecer

  Cenário: Filtrar voos por faixa de preço
    Dado que o cliente busca voos de "GRU" para "GIG"
    E o filtro de preço mínimo é R$ 200
    E o filtro de preço máximo é R$ 500
    Quando o Agente de Busca processa a requisição
    Então todos os voos retornados devem ter preço entre R$ 200 e R$ 500
    E voos fora dessa faixa não devem aparecer

  Cenário: Filtrar voos por horário de partida matutino
    Dado que o cliente busca voos de "GRU" para "BSB"
    E o filtro de horário de partida é entre 06:00 e 10:00
    Quando o Agente de Busca processa a requisição
    Então todos os voos retornados devem partir entre 06:00 e 10:00
    E voos fora desse horário não devem aparecer

  Cenário: Filtrar voos por horário de partida noturno
    Dado que o cliente busca voos de "GRU" para "REC"
    E o filtro de horário de partida é entre 20:00 e 23:59
    Quando o Agente de Busca processa a requisição
    Então todos os voos retornados devem partir entre 20:00 e 23:59

  Cenário: Filtrar voos por classe executiva
    Dado que o cliente busca voos de "GRU" para "JFK"
    E a classe desejada é "executiva"
    Quando o Agente de Busca processa a requisição
    Então todos os voos retornados devem ter disponibilidade em classe executiva
    E as tarifas exibidas devem ser de classe executiva

  Cenário: Filtrar voos por primeira classe
    Dado que o cliente busca voos de "GRU" para "CDG"
    E a classe desejada é "primeira classe"
    Quando o Agente de Busca processa a requisição
    Então apenas voos com primeira classe disponível devem aparecer
    E se nenhum voo tem primeira classe deve retornar lista vazia com sugestão de executiva

  Cenário: Aplicar múltiplos filtros simultaneamente
    Dado que o cliente busca voos de "GRU" para "MIA"
    E o filtro de companhia é "LATAM"
    E o filtro de escalas é "direto"
    E o filtro de horário de partida é entre 20:00 e 23:59
    E o filtro de classe é "executiva"
    Quando o Agente de Busca processa a requisição
    Então apenas voos que atendam todos os filtros devem aparecer
    E se nenhum voo atender todos os filtros deve sugerir relaxar critérios

  Cenário: Filtrar por duração máxima de viagem
    Dado que o cliente busca voos de "GRU" para "LIS"
    E a duração máxima aceitável é 12 horas
    Quando o Agente de Busca processa a requisição
    Então todos os voos retornados devem ter duração menor ou igual a 12 horas
    E voos com escalas longas que excedam 12h totais não devem aparecer

  Cenário: Filtrar por aeroporto específico quando cidade tem múltiplos
    Dado que o cliente busca voos saindo de "CGH" (Congonhas)
    E não quer voos saindo de "GRU" (Guarulhos)
    Quando o Agente de Busca processa a requisição
    Então todos os voos devem partir de CGH
    E nenhum voo de GRU deve aparecer
