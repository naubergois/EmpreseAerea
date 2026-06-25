# language: pt
Funcionalidade: Coordenação do Pipeline de Venda
  Como agente orquestrador
  Eu quero coordenar todos os agentes no pipeline de venda
  Para garantir que o cliente complete sua compra de forma fluida

  Cenário: Rotear requisição de busca para o Agente de Busca
    Dado que o cliente envia uma requisição de busca de voo
    E a requisição contém origem "GRU", destino "GIG" e data "2026-08-15"
    Quando o Orquestrador recebe a requisição
    Então a requisição deve ser roteada para o Agente de Busca de Voos
    E o tempo de roteamento deve ser inferior a 100ms
    E um ID de sessão deve ser criado para o cliente

  Cenário: Rotear requisição de cancelamento para o Agente de Atendimento
    Dado que o cliente envia uma requisição de cancelamento
    E a requisição contém o PNR "ABC123"
    Quando o Orquestrador recebe a requisição
    Então a requisição deve ser roteada para o Agente de Atendimento ao Cliente
    E o contexto da reserva deve ser carregado do PNR
    E o histórico do cliente deve ser anexado à requisição

  Cenário: Rotear requisição ambígua com classificação de intenção
    Dado que o cliente envia a mensagem "quero mudar meu voo de amanhã"
    Quando o Orquestrador classifica a intenção
    Então a intenção deve ser classificada como "alteração_de_reserva"
    E a requisição deve ser roteada para o Agente de Atendimento ao Cliente
    E o Agente de Reserva deve ser colocado em standby

  Cenário: Manter estado da sessão durante pipeline completo
    Dado que o cliente iniciou uma sessão de compra
    E o cliente já buscou voos de "GRU" para "MIA"
    E o cliente selecionou o voo LATAM LA8050
    Quando o cliente prossegue para pagamento
    Então o Orquestrador deve ter o voo selecionado no estado da sessão
    E o preço calculado deve estar no estado da sessão
    E o PNR da reserva deve estar no estado da sessão
    E o tempo total de sessão deve ser registrado

  Cenário: Expirar sessão após inatividade de 30 minutos
    Dado que o cliente iniciou uma sessão de compra
    E o cliente está inativo há 30 minutos
    Quando o timeout de sessão é atingido
    Então a sessão deve ser marcada como expirada
    E a reserva temporária deve ser cancelada via Agente de Reserva
    E o assento deve ser liberado
    E uma notificação de expiração deve ser enviada ao cliente

  Cenário: Executar pipeline completo com sucesso (happy path)
    Dado que o cliente busca voo de "GRU" para "GIG" em "2026-08-15"
    E o Agente de Busca retorna 5 voos disponíveis
    E o cliente seleciona o voo LATAM LA3421
    E o Agente de Precificação calcula R$ 450,00
    E o Agente de Reserva gera PNR "XYZ789"
    E o Agente de Pagamento confirma pagamento de R$ 450,00
    E o Agente de Emissão emite bilhete 045-1234567890
    Quando o pipeline finaliza com sucesso
    Então todas as 7 etapas devem ter status "Sucesso"
    E o trace ID deve ser único e rastreável
    E o tempo total do pipeline deve ser registrado

  Cenário: Priorizar cliente Diamante na fila de processamento
    Dado que existem 100 requisições na fila do Orquestrador
    E o cliente "Maria Diamante" tem nível de fidelidade "Diamante"
    Quando "Maria Diamante" envia uma requisição de busca
    Então a requisição deve ser inserida na fila de alta prioridade
    E deve ser processada antes de clientes sem nível de fidelidade
    E o tempo na fila deve ser inferior a 1 segundo

  Cenário: Registrar log de auditoria completo do pipeline
    Dado que o cliente "Carlos" completou uma compra
    Quando o pipeline finaliza com sucesso
    Então o log de auditoria deve conter todas as etapas:
      | Etapa        | Agente | Status  |
      | Busca        | BUS    | Sucesso |
      | Precificação | PRE    | Sucesso |
      | Reserva      | RES    | Sucesso |
      | Pagamento    | PAG    | Sucesso |
      | Emissão      | EMI    | Sucesso |
      | Milhas       | FID    | Sucesso |
      | Notificação  | NOT    | Sucesso |
    E o trace ID deve ser único
    E o log deve ser imutável
