# language: pt
Funcionalidade: Cache e Integração com GDS
  Como agente de busca de voos
  Eu quero cachear resultados e consultar múltiplos GDS
  Para otimizar performance e cobertura de inventário

  Cenário: Retornar resultado do cache em busca repetida
    Dado que o cliente buscou GRU-GIG em "2026-08-15" há 5 minutos
    E os resultados estão em cache válido
    Quando o mesmo cliente repete a busca com parâmetros idênticos
    Então o resultado deve vir do cache
    E o tempo de resposta deve ser inferior a 200ms
    E o header deve indicar "X-Cache: HIT"

  Cenário: Invalidar cache após 15 minutos
    Dado que uma busca GRU-MIA foi cacheada há 16 minutos
    Quando um novo cliente busca os mesmos parâmetros
    Então o cache deve ser invalidado
    E uma nova consulta aos GDS deve ser executada
    E o header deve indicar "X-Cache: MISS"

  Cenário: Consultar Amadeus, Sabre e Travelport em paralelo
    Dado que o cliente busca GRU-LHR em "2026-11-01"
    Quando o Agente de Busca inicia a consulta
    Então Amadeus, Sabre e Travelport devem ser consultados simultaneamente
    E os resultados devem ser consolidados sem duplicatas
    E o tempo total deve ser próximo ao GDS mais lento

  Cenário: Deduplicar voos codeshare entre GDS
    Dado que Amadeus retorna LATAM LA8080 operado por British Airways
    E Sabre retorna o mesmo voo com código BA7890
    Quando os resultados são consolidados
    Então apenas uma entrada deve aparecer
    E deve indicar operador real "British Airways"
    E deve indicar vendedor "LATAM"

  Cenário: Fallback quando um GDS está indisponível
    Dado que o Amadeus está indisponível
    E Sabre e Travelport respondem normalmente
    Quando o cliente busca GRU-FCO
    Então os resultados de Sabre e Travelport devem ser retornados
    E um alerta de GDS degradado deve ser registrado
    E o cliente não deve perceber indisponibilidade parcial

  Cenário: Cache não deve ser usado para verificação de disponibilidade final
    Dado que o cliente selecionou voo GOL G3100 do cache
    Quando o cliente prossegue para reserva
    Então uma verificação de disponibilidade em tempo real deve ser feita
    E o cache não deve ser usado nesta etapa

  Cenário: Registrar busca sem resultado para análise de demanda
    Dado que não existem voos GRU-TNR em "2026-09-01"
    Quando a busca retorna vazia
    Então o evento "search.no_results" deve ser publicado
    E deve conter origem, destino, data e quantidade de buscas
    E o Agente de Marketing deve poder consumir este evento

  Cenário: Cache por rota e data específica
    Dado que GRU-GIG em "2026-08-15" está em cache
    Quando o cliente busca GRU-GIG em "2026-08-16"
    Então deve ser cache miss
    E nova consulta aos GDS deve ser executada

  Cenário: Indicar voos de alta demanda no resultado
    Dado que a rota GRU-SSA no Carnaval tem ocupação acima de 90%
    Quando os resultados são retornados
    Então voos com poucas vagas devem exibir "Últimas vagas"
    E voos esgotados não devem aparecer na listagem

  Cenário: Enriquecer resultado com tempo de conexão mínima
    Dado que um voo GRU-LIS tem conexão em MAD com 45 minutos
    Quando o resultado é montado
    Então deve alertar que conexão é curta (< 60 min)
    E deve indicar terminal de chegada e partida se disponível
