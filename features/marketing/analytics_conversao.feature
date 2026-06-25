# language: pt
Funcionalidade: Analytics de Conversão
  Como agente de marketing
  Eu quero medir conversão e performance de campanhas
  Para otimizar investimento em marketing

  Cenário: Calcular funil de conversão completo
    Dado que 100.000 clientes receberam campanha
    E 25.000 abriram, 5.000 clicaram, 500 compraram
    Quando o MKT analisa o funil
    Então abertura: 25%, CTR: 20%, conversão: 2%

  Cenário: Atribuir venda à campanha de origem
    Dado que o cliente clicou no e-mail da campanha "VERAO27"
    E comprou 2 horas depois
    Quando a venda é registrada
    Então a receita deve ser atribuída à campanha "VERAO27"
    E janela de atribuição de 7 dias deve ser respeitada

  Cenário: Comparar performance entre canais
    Dado que e-mail gerou 200 vendas e WhatsApp gerou 80
    Quando o MKT compara canais
    Então deve calcular CPA e ROAS por canal
    E identificar canal mais eficiente

  Cenário: Dashboard de campanhas em tempo real
    Dado que 3 campanhas estão ativas
    Quando o gestor acessa o dashboard
    Então deve ver envios, aberturas, cliques e vendas em tempo real
    E alertas de anomalias devem ser exibidos

  Cenário: Analisar buscas sem resultado como oportunidade
    Dado que 2.000 buscas GRU-TNR sem resultado em 30 dias
    Quando o MKT analisa demanda
    Então deve sugerir campanha com rotas alternativas
    E estimar potencial de receita

  Cenário: Medir LTV (Lifetime Value) por segmento
    Dado que clientes "alto valor" gastam R$ 12.000/ano em média
    Quando o MKT calcula LTV
    Então deve informar LTV por segmento
    E comparar com CAC (custo de aquisição)

  Cenário: Relatório de cohort de clientes adquiridos
    Dado que 500 clientes foram adquiridos em janeiro/2026
    Quando o MKT gera relatório de cohort
    Então deve mostrar retenção mês a mês
    E taxa de recompra por cohort

  Cenário: Detectar campanha com baixo ROI
    Dado que a campanha custou R$ 20.000
    E gerou apenas R$ 15.000 em vendas
    Quando o ROI é calculado
    Então deve alertar "ROI_negativo"
    E recomendar pausa da campanha

  Cenário: Integrar analytics com pipeline de venda
    Dado que o cliente veio de campanha MKT
    Quando completa compra no pipeline ORC
    Então o trace ID deve vincular campanha à venda
    E o evento "marketing.conversion" deve ser publicado

  Cenário: Exportar relatório de performance mensal
    Dado que o mês de maio/2026 encerrou
    Quando o gestor solicita relatório
    Então deve gerar PDF com todas as métricas
    E incluir comparativo com mês anterior
