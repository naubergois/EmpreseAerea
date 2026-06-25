# language: pt
Funcionalidade: Alteração e Cancelamento via Atendimento
  Como cliente
  Eu quero alterar ou cancelar minha reserva pelo atendimento
  Para resolver minha situação com assistência

  Cenário: Solicitar alteração de data via chat
    Dado que o cliente tem PNR "ALT100" para "2026-09-01"
    E quer alterar para "2026-09-05"
    Quando o ATC processa a solicitação
    Então deve verificar disponibilidade no RES
    E deve informar taxa de alteração
    E deve solicitar confirmação do cliente

  Cenário: Processar cancelamento com reembolso via atendimento
    Dado que o cliente solicita cancelamento do PNR "CAN100"
    E a tarifa permite reembolso de 80%
    Quando o ATC processa
    Então deve acionar RES para cancelamento
    E deve acionar PAG para reembolso
    E deve informar prazo de estorno

  Cenário: Alteração com diferença tarifária a pagar
    Dado que a alteração gera diferença de R$ 300,00
    Quando o cliente confirma alteração
    Então deve gerar link de pagamento complementar
    E após pagamento deve acionar EMI para reemissão

  Cenário: Cancelamento de reserva multi-passageiro
    Dado que o PNR tem 3 passageiros
    E o cliente quer cancelar apenas 1
    Quando o ATC processa
    Então deve acionar split PNR no RES
    E deve calcular reembolso proporcional

  Cenário: Rejeitar alteração em tarifa restritiva
    Dado que a tarifa é "promocional não alterável"
    Quando o cliente solicita alteração
    Então deve informar impossibilidade
    E deve oferecer opção de cancelamento (se permitido)

  Cenário: Escalar alteração complexa para humano
    Dado que a alteração envolve 4 trechos internacionais
    E o ATC não consegue processar automaticamente
    Quando a complexidade excede limite
    Então deve escalar para atendente humano
    E deve transferir todo o contexto

  Cenário: Processar reembolso de bilhete emitido
    Dado que o bilhete 045-1234567890 foi emitido
    E o cliente solicita reembolso
    Quando o ATC processa
    Então deve acionar EMI para void (se dentro do prazo)
    E deve acionar PAG para estorno

  Cenário: Informar política de no-show
    Dado que o cliente não embarcou no voo
    Quando consulta sobre reembolso
    Então deve informar política de no-show da tarifa
    E deve indicar se há crédito disponível

  Cenário: Alteração com urgência por voo em 24h
    Dado que o voo é amanhã
    E o cliente precisa alterar
    Quando o ATC recebe solicitação
    Então deve priorizar processamento
    E deve escalar para humano se necessário

  Cenário: Registrar reclamação no sistema de qualidade
    Dado que o cliente registra reclamação formal
    Quando o ATC processa
    Então deve criar ticket no sistema de qualidade
    E deve informar prazo de resposta (5 dias úteis)
