# language: pt
Funcionalidade: Atendimento Multicanal
  Como cliente
  Eu quero suporte rápido e eficaz em múltiplos canais
  Para resolver dúvidas e problemas de viagem

  Cenário: Consulta de status por PNR via chat
    Dado que o cliente informa PNR "ABC123" no chat
    Quando o Agente de Atendimento processa
    Então deve retornar status da reserva em menos de 5 segundos
    E deve incluir voo, data, assento e status do pagamento

  Cenário: Consulta de status por e-mail
    Dado que o cliente envia e-mail com PNR "DEF456"
    Quando o ATC processa automaticamente
    Então deve responder com status completo em menos de 5 segundos
    E deve gerar protocolo de atendimento

  Cenário: Atendimento telefônico com identificação por CPF
    Dado que o cliente liga e informa CPF
    Quando o ATC identifica o cliente
    Então deve listar reservas ativas
    E deve perguntar qual reserva deseja consultar

  Cenário: Responder FAQ sobre bagagem automaticamente
    Dado que o cliente pergunta "Quantas malas posso levar?"
    E o voo é LATAM GRU-GIG econômica
    Quando o ATC processa
    Então deve informar franquia de bagagem da tarifa
    E deve resolver sem escalação humana

  Cenário: Classificar sentimento negativo e priorizar
    Dado que o cliente escreve "Estou muito insatisfeito, perdi meu voo!"
    Quando o ATC classifica sentimento
    Então deve classificar como "negativo"
    E deve priorizar atendimento
    E deve verificar se há voo iminente

  Cenário: Atendimento em inglês
    Dado que o cliente escreve em inglês "I need to change my flight"
    Quando o ATC detecta idioma
    Então deve responder em inglês
    E deve classificar intenção como "alteração_de_reserva"

  Cenário: Atendimento em espanhol
    Dado que o cliente escreve em espanhol "Quiero cancelar mi vuelo"
    Quando o ATC detecta idioma
    Então deve responder em espanhol
    E deve iniciar fluxo de cancelamento

  Cenário: Gerar protocolo único de atendimento
    Dado que o cliente iniciou atendimento
    Quando a primeira interação é registrada
    Então um protocolo único deve ser gerado (ex: ATC-20260625-001)
    E deve ser informado ao cliente

  Cenário: Acessar histórico completo do cliente
    Dado que o cliente "João" tem 5 reservas e 2 reclamações
    Quando o atendente consulta histórico
    Então deve exibir todas as reservas, pagamentos e bilhetes
    E deve exibir interações anteriores

  Cenário: Detectar urgência por voo iminente
    Dado que o voo do cliente é em 3 horas
    Quando o cliente solicita ajuda
    Então deve classificar como "urgente"
    E deve escalar para atendente humano imediatamente
