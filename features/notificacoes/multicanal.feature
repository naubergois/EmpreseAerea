# language: pt
Funcionalidade: Notificações Multicanal
  Como cliente
  Eu quero receber notificações no canal de minha preferência
  Para estar informado da forma mais conveniente

  Cenário: Enviar notificação por e-mail
    Dado que o canal preferido do cliente é e-mail
    Quando uma notificação transacional é disparada
    Então deve ser enviada por e-mail
    E não deve ser enviada por outros canais

  Cenário: Enviar notificação por SMS
    Dado que o cliente habilitou SMS para alertas de voo
    Quando um alerta de atraso é disparado
    Então deve ser enviado SMS para o telefone cadastrado
    E o SMS deve ter no máximo 160 caracteres

  Cenário: Enviar push notification via app
    Dado que o cliente tem o app instalado com push habilitado
    Quando uma notificação é disparada
    Então deve enviar push notification
    E deve incluir deep link para ação relevante

  Cenário: Enviar notificação via WhatsApp Business
    Dado que o cliente optou por WhatsApp
    E o número está verificado na WhatsApp Business API
    Quando a notificação é disparada
    Então deve enviar mensagem via WhatsApp
    E deve usar template aprovado pelo WhatsApp

  Cenário: Gerenciar preferências de canal por tipo
    Dado que o cliente prefere:
      | Tipo           | Canal     |
      | Transacional   | E-mail    |
      | Alerta de voo  | SMS       |
      | Promocional    | WhatsApp  |
    Quando cada tipo de notificação é enviada
    Então deve respeitar a preferência configurada

  Cenário: Fallback para e-mail quando SMS falha
    Dado que o SMS de alerta falhou na entrega
    Quando o NOT detecta falha
    Então deve enviar e-mail como fallback
    E deve registrar falha do SMS

  Cenário: Anexar PDF do bilhete no e-mail
    Dado que o e-ticket foi emitido
    Quando o NOT envia notificação
    Então o PDF do bilhete deve ser anexado
    E o tamanho do anexo deve ser inferior a 5MB

  Cenário: Respeitar horário de silêncio para promoções
    Dado que são 23:00
    E o cliente configurou silêncio das 22:00 às 08:00
    Quando uma campanha promocional tenta enviar
    Então deve ser enfileirada para 08:00
    E alertas transacionais devem ser enviados normalmente

  Cenário: Notificação de milhas acumuladas
    Dado que o cliente ganhou 3.500 milhas na compra
    Quando o FID confirma crédito
    Então o NOT deve enviar notificação com saldo atualizado
    E deve informar progresso para próximo nível

  Cenário: Taxa de entrega acima de 99%
    Dado que 10.000 notificações foram enviadas no dia
    E 9.950 foram entregues com sucesso
    Quando métricas são calculadas
    Então a taxa de entrega deve ser 99.5%
