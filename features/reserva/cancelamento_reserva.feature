# language: pt
Funcionalidade: Cancelamento de Reserva
  Como cliente
  Eu quero cancelar minha reserva
  Para obter reembolso conforme a política de cancelamento

  Cenário: Cancelar reserva dentro do prazo de cancelamento gratuito (24h)
    Dado que existe a reserva PNR "STU901" criada há 12 horas
    E a política permite cancelamento gratuito em até 24 horas
    Quando o cliente solicita o cancelamento
    Então a reserva deve ser cancelada
    E o reembolso total deve ser processado
    E o assento deve ser liberado
    E nenhuma taxa de cancelamento deve ser cobrada

  Cenário: Cancelar reserva após prazo com taxa de 20%
    Dado que existe a reserva PNR "VWX234" criada há 5 dias
    E a tarifa é R$ 800,00
    E a taxa de cancelamento é 20%
    Quando o cliente solicita o cancelamento
    Então a reserva deve ser cancelada
    E o reembolso deve ser R$ 640,00
    E a taxa de R$ 160,00 deve ser retida
    E o assento deve ser liberado

  Cenário: Cancelar reserva com tarifa não reembolsável
    Dado que existe a reserva PNR "NRF001" com tarifa "promo não reembolsável"
    E a tarifa foi R$ 299,00
    Quando o cliente solicita o cancelamento
    Então a reserva deve ser cancelada
    E nenhum reembolso deve ser processado
    E a mensagem "Tarifa não reembolsável" deve ser informada
    E as taxas aeroportuárias devem ser reembolsadas

  Cenário: Cancelar reserva de grupo (10+ passageiros)
    Dado que existe a reserva de grupo PNR "GRP001" com 15 passageiros
    E o líder do grupo solicita cancelamento
    Quando o cancelamento é processado
    Então todas as 15 reservas de passageiros devem ser canceladas
    E todos os 15 assentos devem ser liberados
    E o reembolso deve ser calculado sobre o valor total do grupo
    E a política de grupo deve ser aplicada

  Cenário: Cancelar 1 passageiro de reserva com múltiplos passageiros
    Dado que existe a reserva PNR "MUL001" com 3 passageiros
    E apenas "Pedro Souza" deseja cancelar
    Quando o cancelamento parcial é solicitado
    Então apenas "Pedro Souza" deve ser removido da reserva
    E o assento de "Pedro Souza" deve ser liberado
    E o valor proporcional deve ser reembolsado
    E o PNR deve permanecer ativo para os demais passageiros

  Cenário: Detectar conflito de horário com reserva existente
    Dado que o cliente "Maria" tem reserva GRU-GIG às 14:00 do dia 2026-08-15
    E o cliente tenta reservar GRU-BSB às 13:30 do dia 2026-08-15
    Quando o Agente de Reserva valida a nova reserva
    Então deve detectar conflito de horário
    E a mensagem "Conflito com reserva existente" deve ser retornada
    E deve sugerir horários alternativos

  Cenário: Cancelamento automático por timeout de pagamento
    Dado que existe a reserva PNR "TMO001" criada há 21 minutos
    E nenhum pagamento foi recebido
    Quando o job de expiração executa
    Então a reserva deve ser cancelada automaticamente
    E o status deve mudar para "expirada"
    E o assento deve ser liberado
    E o cliente deve receber notificação de expiração
