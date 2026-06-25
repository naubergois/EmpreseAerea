# language: pt
Funcionalidade: Ciclo Completo de Reserva
  Como cliente
  Eu quero reservar assentos com segurança
  Para concluir minha compra com tranquilidade

  Cenário: Fluxo completo de reserva até pagamento
    Dado que o cliente selecionou voo LATAM LA3421
    E informou dados de 1 passageiro válidos
    E selecionou assento 12A
    Quando o Agente de Reserva cria a reserva
    Então o PNR deve ser gerado
    E o assento 12A deve estar bloqueado por 20 minutos
    E os dados devem ser enviados ao Agente de Pagamento

  Cenário: Timeout de reserva libera assento
    Dado que a reserva PNR "TIME01" foi criada há 21 minutos
    E o pagamento não foi concluído
    Quando o timeout de 20 minutos é atingido
    Então a reserva deve ser cancelada automaticamente
    E o assento deve ser liberado
    E o NOT deve notificar o cliente

  Cenário: Reserva com serviços extras
    Dado que o cliente adicionou bagagem extra e refeição vegetariana
    Quando a reserva é criada
    Então os serviços devem constar no PNR
    E o valor adicional deve ser calculado pelo PRE

  Cenário: Reserva coordenada pelo Orquestrador
    Dado que o Orquestrador recebeu seleção de voo e cotação do PRE
    Quando aciona o Agente de Reserva
    Então o RES deve receber trace ID do pipeline
    E deve publicar evento "reservation.confirmed" ao concluir

  Cenário: Falha na reserva aciona retry
    Dado que a primeira tentativa de criar PNR falhou com erro 503
    Quando o Orquestrador executa retry
    Então a segunda tentativa deve ocorrer após 2 segundos
    E se bem-sucedida o pipeline continua

  Cenário: Reserva para grupo de 9 passageiros
    Dado que são 9 passageiros no mesmo voo
    Quando a reserva é criada
    Então todos devem estar no mesmo PNR
    E deve verificar 9 assentos disponíveis

  Cenário: Reserva com programa de fidelidade vinculado
    Dado que o cliente informou número de fidelidade
    Quando a reserva é criada
    Então o número de fidelidade deve constar no PNR
    E o FID deve ser notificado para acúmulo futuro

  Cenário: Histórico de alterações da reserva
    Dado que a reserva foi alterada 2 vezes
    Quando o histórico é consultado
    Então deve listar todas as alterações com timestamp
    E cada alteração deve ser imutável

  Cenário: Reserva bloqueada durante processamento de pagamento
    Dado que o pagamento está em andamento
    Quando outro processo tenta alterar a reserva
    Então deve bloquear alteração com "reserva_em_processamento"

  Cenário: Confirmar reserva após pagamento aprovado
    Dado que o pagamento foi aprovado para PNR "CONF01"
    Quando o RES recebe confirmação
    Então o status deve mudar para "confirmada"
    E o bloqueio temporário de assento deve ser permanente
