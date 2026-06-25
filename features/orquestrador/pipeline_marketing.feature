# language: pt
Funcionalidade: Coordenação do Pipeline de Marketing
  Como agente orquestrador
  Eu quero coordenar campanhas de marketing com agentes de fidelidade e notificações
  Para maximizar conversão de vendas de passagens

  Cenário: Disparar remarketing após abandono de carrinho
    Dado que o cliente "Ana" criou reserva PNR "ABN123"
    E o cliente abandonou o fluxo antes do pagamento
    E se passaram 30 minutos sem conclusão
    Quando o Orquestrador detecta o abandono
    Então o Agente de Marketing deve receber evento "cart.abandoned"
    E o Agente de Fidelidade deve verificar nível do cliente
    E o Agente de Notificações deve enviar oferta personalizada

  Cenário: Cross-sell após emissão bem-sucedida
    Dado que o bilhete 045-9876543210 foi emitido para "Carlos"
    Quando o pipeline de venda finaliza com sucesso
    Então o Orquestrador deve acionar pipeline de marketing pós-venda
    E o MKT deve oferecer seguro viagem e hotel no destino
    E o envio deve respeitar preferências de canal do cliente

  Cenário: Campanha sazonal coordenada com precificação
    Dado que a campanha "Black Friday 2026" está ativa
    E o MKT definiu desconto de 20% em rotas nacionais
    Quando o cliente busca voo GRU-GIG durante a campanha
    Então o Orquestrador deve acionar BUS e PRE em paralelo
    E o PRE deve aplicar regra promocional da campanha
    E o preço exibido deve refletir o desconto de 20%

  Cenário: Alerta de queda de preço em rota monitorada
    Dado que o cliente "Pedro" monitora rota GRU-LIS
    E o preço caiu de R$ 4.500 para R$ 3.200
    Quando o PRE detecta variação significativa
    Então o Orquestrador deve notificar o MKT
    E o MKT deve disparar alerta personalizado via NOT
    E o alerta deve conter link direto para compra

  Cenário: Respeitar opt-out em pipeline de marketing
    Dado que o cliente "Lucia" desativou comunicações promocionais
    Quando uma campanha de remarketing é disparada
    Então o Orquestrador deve filtrar "Lucia" da campanha
    E nenhuma notificação promocional deve ser enviada
    E notificações transacionais devem continuar normalmente

  Cenário: Pipeline de reativação de cliente inativo
    Dado que o cliente "Roberto" não compra há 12 meses
    E possui nível de fidelidade "Ouro"
    Quando o MKT inicia campanha de reativação
    Então o FID deve gerar cupom exclusivo de 15% de desconto
    E o NOT deve enviar oferta no canal preferencial
    E o cupom deve expirar em 7 dias

  Cenário: Coordenar upsell de upgrade após compra
    Dado que "Fernanda" comprou passagem econômica GRU-MIA
    E existem assentos em executiva disponíveis
    Quando o pipeline pós-venda é acionado
    Então o MKT deve calcular diferença de preço para upgrade
    E o NOT deve enviar oferta de upgrade com prazo de 48h
    E o PRE deve cotar valor do upgrade

  Cenário: Campanha baseada em buscas sem resultado
    Dado que 500 clientes buscaram GRU-TNR sem resultados em 7 dias
    Quando o MKT analisa demanda não atendida
    Então deve criar campanha com rotas alternativas via conexão
    E o Orquestrador deve coordenar envio segmentado
    E a métrica de conversão deve ser rastreada

  Cenário: Integração MKT-FID para oferta por nível Diamante
    Dado que o cliente "Marina" é nível Diamante
    E uma campanha VIP está ativa
    Quando o MKT segmenta a base
    Então clientes Diamante devem receber oferta com 2x milhas bônus
    E o FID deve validar elegibilidade antes do envio
    E o NOT deve personalizar template com nome e benefícios

  Cenário: Frequency capping em campanhas múltiplas
    Dado que o cliente "Tiago" já recebeu 3 e-mails promocionais esta semana
    E o limite configurado é 3 por semana
    Quando uma nova campanha tenta incluir "Tiago"
    Então o Orquestrador deve bloquear o envio promocional
    E o MKT deve registrar "frequency_cap_reached"
    E o cliente deve entrar na fila da próxima semana

  Cenário: A/B test coordenado entre MKT e NOT
    Dado que a campanha "Verão 2027" tem 2 variantes de assunto
    Quando o Orquestrador distribui os envios
    Então 50% dos clientes devem receber variante A
    E 50% dos clientes devem receber variante B
    E as métricas de abertura devem ser comparadas após 48h

  Cenário: Pipeline completo venda + marketing pós-compra
    Dado que o cliente completa compra GRU-CDG por R$ 3.800
    Quando o pipeline de venda finaliza
    Então milhas devem ser creditadas via FID
    E e-ticket deve ser enviado via NOT
    E oferta de aluguel de carro no destino deve ser enviada via MKT
    E todas as etapas devem compartilhar o mesmo trace ID
