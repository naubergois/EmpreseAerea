# language: pt
Funcionalidade: Saga e Rollback de Transações
  Como agente orquestrador
  Eu quero gerenciar transações distribuídas com rollback
  Para garantir consistência quando ocorrem falhas no pipeline

  Cenário: Executar rollback após falha no pagamento
    Dado que o cliente completou a reserva com PNR "XYZ789"
    E o assento 12A do voo GOL G31234 está reservado
    Quando o pagamento é recusado pelo Agente de Pagamento
    Então o Orquestrador deve iniciar o rollback da saga
    E o Agente de Reserva deve cancelar o PNR "XYZ789"
    E o assento 12A deve ser liberado
    E o Agente de Notificações deve enviar aviso de falha ao cliente
    E o rollback deve completar em menos de 5 segundos

  Cenário: Executar rollback após falha na emissão do bilhete
    Dado que o pagamento de R$ 1.500,00 foi confirmado
    E o Agente de Emissão tenta emitir o bilhete
    Quando a emissão falha por indisponibilidade do GDS
    Então o Orquestrador deve iniciar o rollback da saga
    E o Agente de Pagamento deve processar estorno de R$ 1.500,00
    E o Agente de Reserva deve cancelar a reserva
    E o Agente de Notificações deve informar o cliente
    E o incidente deve ser registrado para retry automático

  Cenário: Rollback parcial em transação multi-trecho
    Dado que o cliente comprou ida GRU-MIA e volta MIA-GRU
    E o bilhete de ida foi emitido com sucesso
    Quando a emissão do bilhete de volta falha
    Então o Orquestrador deve fazer void do bilhete de ida
    E o estorno completo deve ser processado
    E ambas as reservas devem ser canceladas
    E o cliente deve ser notificado sobre a falha completa

  Cenário: Rollback com compensação em caso de erro de precificação
    Dado que o cliente pagou R$ 800,00 pelo bilhete
    E após a emissão detectou-se erro no cálculo de taxa
    E o valor correto deveria ser R$ 850,00
    Quando o Orquestrador detecta a inconsistência
    Então o bilhete emitido deve ser mantido
    E a diferença de R$ 50,00 deve ser absorvida como crédito
    E um alerta de inconsistência deve ser gerado para análise
    E o Agente de Precificação deve recalibrar as regras

  Cenário: Rollback com timeout em agente que não responde
    Dado que o pagamento foi processado com sucesso
    E o Agente de Emissão não responde há 30 segundos
    Quando o timeout do Agente de Emissão é atingido
    Então o Orquestrador deve iniciar rollback por timeout
    E o Agente de Pagamento deve receber solicitação de estorno
    E o Agente de Reserva deve cancelar a reserva
    E o incidente "timeout_emissao" deve ser registrado

  Cenário: Retry de emissão antes de rollback
    Dado que a primeira tentativa de emissão falhou com erro 503
    E o Orquestrador tem política de retry configurada
    Quando o retry é executado
    Então a segunda tentativa deve ocorrer após 2 segundos
    E se a segunda tentativa for bem-sucedida o pipeline continua
    E nenhum rollback deve ser executado
    E o incidente de retry deve ser registrado

  Cenário: Rollback em cascata com 3 agentes envolvidos
    Dado que a reserva PNR "CASCADE1" foi criada
    E o pagamento de R$ 2.000,00 foi confirmado
    E a emissão do bilhete estava em progresso
    E o acúmulo de milhas estava em progresso
    Quando a emissão falha com erro crítico
    Então o acúmulo de milhas pendente deve ser cancelado
    E o estorno do pagamento deve ser processado
    E a reserva deve ser cancelada
    E todos os 3 rollbacks devem completar em menos de 5 segundos
    E a ordem do rollback deve ser: milhas, pagamento, reserva

  Cenário: Idempotência no rollback - evitar rollback duplicado
    Dado que um rollback foi iniciado para a reserva PNR "IDEM01"
    E o rollback está em andamento
    Quando uma segunda solicitação de rollback chega para o mesmo PNR
    Então a segunda solicitação deve ser ignorada
    E o status do rollback em andamento deve ser retornado
    E nenhuma operação duplicada deve ser executada
