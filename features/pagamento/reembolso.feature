# language: pt
Funcionalidade: Reembolso e Estorno
  Como agente de pagamento
  Eu quero processar reembolsos e estornos
  Para devolver valores ao cliente conforme política

  Cenário: Estorno total por cancelamento com reembolso integral
    Dado que o pagamento original foi R$ 800,00 no cartão Visa
    E a tarifa permite reembolso integral
    Quando o estorno é solicitado
    Então R$ 800,00 devem ser estornados no cartão
    E o estorno deve ocorrer em até 7 dias úteis

  Cenário: Reembolso parcial por cancelamento com taxa
    Dado que o pagamento foi R$ 600,00
    E a taxa de cancelamento é R$ 150,00
    Quando o reembolso é processado
    Então R$ 450,00 devem ser devolvidos ao cliente

  Cenário: Estorno automático via Saga por falha de emissão
    Dado que o pagamento de R$ 1.500,00 foi aprovado
    E a emissão do bilhete falhou
    Quando o Orquestrador aciona compensação
    Então o PAG deve estornar R$ 1.500,00 automaticamente
    E o estorno deve completar em menos de 5 segundos

  Cenário: Reembolso para pagamento original em PIX
    Dado que o pagamento foi via PIX
    E o reembolso é aprovado
    Quando o PAG processa
    Então o valor deve ser devolvido na mesma chave PIX
    E em até 1 dia útil

  Cenário: Reembolso para pagamento original em boleto
    Dado que o pagamento foi via boleto
    Quando o reembolso é aprovado
    Então deve solicitar dados bancários do cliente
    E transferir via TED em até 5 dias úteis

  Cenário: Idempotência em estorno - evitar duplo reembolso
    Dado que o estorno da transação TXN-789 já foi processado
    Quando uma segunda solicitação de estorno chega
    Então nenhum novo estorno deve ser criado
    E o resultado do estorno original deve ser retornado

  Cenário: Estorno parcial por alteração de tarifa
    Dado que o cliente pagou R$ 1.000,00
    E a alteração resultou em tarifa menor de R$ 850,00
    Quando o ajuste é processado
    Então R$ 150,00 devem ser estornados

  Cenário: Registrar reembolso para conciliação BSP
    Dado que o reembolso de R$ 2.300,00 foi processado
    Quando a conciliação diária é executada
    Então o reembolso deve aparecer no relatório BSP
    E deve estar vinculado ao bilhete original

  Cenário: Notificar cliente sobre reembolso processado
    Dado que o reembolso de R$ 450,00 foi aprovado
    Quando o estorno é confirmado pelo gateway
    Então o Agente de Notificações deve enviar confirmação
    E deve informar prazo de crédito na fatura

  Cenário: Rejeitar reembolso após prazo limite
    Dado que a tarifa permite reembolso até 24h antes do voo
    E faltam 2 horas para o voo
    Quando o cliente solicita reembolso
    Então deve rejeitar com erro "prazo_reembolso_expirado"
