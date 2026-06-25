# language: pt
Funcionalidade: Alertas de Voo
  Como cliente
  Eu quero ser notificado sobre alterações no meu voo
  Para me planejar adequadamente

  Cenário: Notificar atraso de voo
    Dado que o voo GOL G3100 atrasou 45 minutos
    E o passageiro "João" tem bilhete para este voo
    Quando o sistema recebe evento operacional
    Então o NOT deve enviar alerta via SMS e push
    E deve informar novo horário estimado de partida

  Cenário: Notificar cancelamento de voo
    Dado que o voo LATAM LA3421 foi cancelado
    Quando o evento de cancelamento é recebido
    Então deve notificar todos os passageiros afetados
    E deve informar opções de reacomodação
    E deve escalar para ATC se necessário

  Cenário: Notificar mudança de portão
    Dado que o portão mudou de 15 para 22
    Quando a atualização operacional é recebida
    Então deve enviar push notification imediata
    E deve atualizar boarding pass

  Cenário: Lembrete de check-in 24 horas antes
    Dado que o voo é amanhã às 08:00
    Quando faltam 24 horas para o voo
    Então deve enviar lembrete de check-in
    E deve incluir link direto para check-in online

  Cenário: Lembrete de check-in 2 horas antes
    Dado que o check-in ainda não foi realizado
    E faltam 2 horas para o voo
    Quando o lembrete é disparado
    Então deve enviar SMS urgente
    E deve alertar que check-in fecha 1h antes

  Cenário: Notificar alteração de horário com antecedência
    Dado que o horário do voo mudou de 14:00 para 16:30
    E a mudança foi detectada 48h antes
    Quando o NOT processa
    Então deve enviar e-mail e SMS
    E deve oferecer opção de alteração gratuita

  Cenário: Notificar início de embarque
    Dado que o embarque do voo G3100 iniciou
    E o portão é 18
    Quando o evento de embarque é recebido
    Então deve enviar push "Embarque iniciado - Portão 18"

  Cenário: Alerta de conexão apertada
    Dado que o passageiro tem conexão de 50 minutos
    E o voo de chegada atrasou 30 minutos
    Quando o NOT calcula tempo de conexão
    Então deve alertar "Conexão apertada - Procure assistência"

  Cenário: Notificar milhas prestes a expirar
    Dado que 15.000 milhas expiram em 30 dias
    Quando o FID dispara alerta
    Então o NOT deve enviar e-mail com saldo e data de expiração
    E deve sugerir opções de resgate

  Cenário: Priorizar canal por urgência do alerta
    Dado que o voo é em 2 horas e houve cancelamento
    Quando o alerta é enviado
    Então deve usar SMS + push + ligação automática
    E e-mail deve ser canal secundário
