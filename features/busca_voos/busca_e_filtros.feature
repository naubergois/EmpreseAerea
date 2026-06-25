# language: pt
Funcionalidade: Busca e Filtros Integrados
  Como cliente
  Eu quero buscar e filtrar voos em uma única experiência
  Para encontrar rapidamente a melhor opção

  Cenário: Busca com filtro de preço aplicado simultaneamente
    Dado que o cliente busca voos de "GRU" para "POA"
    E aplica filtro de preço máximo R$ 400
    Quando o Agente de Busca processa
    Então busca e filtro devem ocorrer em uma única requisição
    E tempo total deve ser inferior a 3 segundos

  Cenário: Refinar resultados sem nova consulta GDS
    Dado que busca inicial retornou 50 voos cacheados
    Quando cliente aplica filtro de companhia "GOL"
    Então filtro deve ser aplicado sobre cache
    E nenhuma nova consulta GDS deve ocorrer

  Cenário: Combinar busca flexível com filtro de escalas
    Dado que busca flexível +/- 3 dias de "2026-10-15"
    E filtro de voo direto
    Quando processado
    Então voos diretos em 7 dias devem ser retornados
    E menor preço por data deve ser destacado

  Cenário: Busca internacional com filtro de duração
    Dado busca GRU-TYO com duração máxima 24h
    Quando processada
    Então voos com conexões longas excluídos
    E tempo de conexão incluído no cálculo

  Cenário: Resultados vazios sugerem relaxar filtros
    Dado busca GRU-MIA com filtros: direto + LATAM + manhã + executiva
    Quando nenhum resultado atende todos os filtros
    Então sugestão de relaxar filtros deve ser exibida
    E resultados parciais podem ser mostrados

  Cenário: Contagem de resultados por filtro
    Dado 50 voos na busca original
    Quando filtro "direto" é aplicado
    Então contagem "12 voos diretos de 50" deve ser exibida
    E filtros laterais devem mostrar contagem por opção

  Cenário: Busca com ordenação e filtro combinados
    Dado busca GRU-GIG filtrada por GOL
    E ordenação por menor preço
    Quando processada
    Então voos GOL em ordem crescente de preço
    E primeiro resultado é o GOL mais barato

  Cenário: Persistir filtros na sessão ORC
    Dado que cliente aplicou filtros na sessão
    Quando retorna à busca dentro de 30 minutos
    Então filtros devem ser restaurados
    E resultados re-aplicados

  Cenário: Busca por voz com filtros naturais
    Dado que cliente diz "voos diretos para Miami amanhã de manhã"
    Quando BUS interpreta linguagem natural
    Então origem da sessão, destino MIA, data amanhã, filtro direto e manhã

  Cenário: Exportar resultados filtrados
    Dado que cliente selecionou 3 voos para comparar
    Quando exportação é solicitada
    Então PDF ou e-mail com comparativo deve ser gerado via NOT

  Cenário: Busca com alerta de preço integrado
    Dado que nenhum voo atende faixa de preço desejada
    Quando cliente configura alerta
    Então MKT deve registrar monitoramento de preço
    E NOT deve notificar quando preço atingir meta

  Cenário: Performance com 10 filtros simultâneos
    Dado busca com 10 filtros ativos
    Quando processada sobre cache
    Então resposta deve ser inferior a 500ms
    E todos os filtros devem ser aplicados corretamente
