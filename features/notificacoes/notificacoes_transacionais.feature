# language: pt
Funcionalidade: Notificações Transacionais
  Como cliente
  Eu quero receber confirmações de cada etapa da compra
  Para acompanhar minha compra e viagem

  Cenário: Enviar confirmação de reserva por e-mail
    Dado que a reserva PNR "NOT001" foi criada
    Quando o NOT recebe evento "reservation.confirmed"
    Então um e-mail de confirmação deve ser enviado em até 30 segundos
    E deve conter PNR, voo, data e valor

  Cenário: Enviar confirmação de pagamento
    Dado que o pagamento de R$ 890,00 foi aprovado
    Quando o NOT recebe evento "payment.approved"
    Então deve enviar e-mail com recibo de pagamento
    E deve indicar forma de pagamento e parcelas

  Cenário: Enviar e-ticket com anexo PDF
    Dado que o bilhete 045-1234567890 foi emitido
    Quando o NOT recebe evento "ticket.issued"
    Então deve enviar e-mail com e-ticket em PDF anexo
    E deve incluir QR code no corpo do e-mail

  Cenário: Enviar notificação de reembolso processado
    Dado que o reembolso de R$ 450,00 foi confirmado
    Quando o NOT recebe evento "refund.processed"
    Então deve enviar e-mail informando valor e prazo de crédito

  Cenário: Enviar notificação de cancelamento
    Dado que a reserva PNR "NOT002" foi cancelada
    Quando o NOT recebe evento "reservation.cancelled"
    Então deve enviar confirmação de cancelamento
    E deve informar valor de reembolso se aplicável

  Cenário: Personalizar template por idioma do cliente
    Dado que o cliente tem preferência de idioma "EN"
    Quando a notificação transacional é enviada
    Então o template em inglês deve ser utilizado

  Cenário: Rastrear entrega do e-mail
    Dado que o e-mail de confirmação foi enviado
    Quando o provedor confirma entrega
    Então o status deve ser atualizado para "entregue"
    E o timestamp de entrega deve ser registrado

  Cenário: Rastrear abertura do e-mail
    Dado que o cliente abriu o e-mail do e-ticket
    Quando o pixel de tracking é acionado
    Então o status deve ser atualizado para "aberto"
    E a métrica deve alimentar analytics do MKT

  Cenário: Retry em caso de falha de envio
    Dado que o primeiro envio de e-mail falhou
    Quando o NOT detecta falha
    Então deve tentar reenvio após 1 minuto
    E após 3 falhas deve alertar equipe de operações

  Cenário: Throttling para evitar spam
    Dado que o cliente já recebeu 5 notificações hoje
    E o limite diário é 5
    Quando uma 6ª notificação não-transacional tenta ser enviada
    Então deve ser bloqueada
    E notificações transacionais devem continuar
