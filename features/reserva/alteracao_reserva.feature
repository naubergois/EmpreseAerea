# language: pt
Funcionalidade: Alteração de Reserva
  Como cliente
  Eu quero alterar minha reserva existente
  Para ajustar minha viagem conforme necessário

  Cenário: Alterar data do voo em reserva existente
    Dado que existe a reserva PNR "JKL012" para o voo GRU-GIG em 2026-08-15
    E o cliente deseja alterar para 2026-08-20
    E há disponibilidade no voo de 2026-08-20
    Quando o Agente de Reserva processa a alteração
    Então a data deve ser atualizada para 2026-08-20
    E a diferença de tarifa deve ser calculada
    E o PNR deve permanecer o mesmo
    E o histórico de alterações deve ser registrado

  Cenário: Alterar reserva com cobrança de diferença tarifária
    Dado que existe a reserva PNR "MNO345" com tarifa de R$ 400,00
    E o novo voo tem tarifa de R$ 550,00
    E a taxa de alteração é R$ 50,00
    Quando o Agente de Reserva calcula o custo da alteração
    Então a diferença tarifária deve ser R$ 150,00
    E a taxa de alteração deve ser R$ 50,00
    E o total a pagar deve ser R$ 200,00

  Cenário: Alterar reserva com crédito ao cliente (voo mais barato)
    Dado que existe a reserva PNR "ALT001" com tarifa de R$ 800,00
    E o novo voo tem tarifa de R$ 600,00
    E a taxa de alteração é R$ 50,00
    Quando o Agente de Reserva calcula o custo da alteração
    Então o crédito ao cliente deve ser R$ 150,00 (800 - 600 - 50)
    E o crédito pode ser usado como voucher para próxima compra

  Cenário: Rejeitar alteração para voo lotado
    Dado que existe a reserva PNR "PQR678" para GRU-GIG em 2026-08-15
    E o cliente deseja alterar para 2026-08-20
    E o voo de 2026-08-20 está lotado
    Quando o Agente de Reserva tenta a alteração
    Então a alteração deve ser rejeitada
    E a mensagem "Voo sem disponibilidade" deve ser retornada
    E alternativas de data devem ser sugeridas

  Cenário: Alterar assento de reserva existente
    Dado que existe a reserva PNR "ASS001" com assento 15A
    E o passageiro deseja mudar para 20C
    E o assento 20C está disponível
    Quando o Agente de Reserva processa a alteração
    Então o assento 15A deve ser liberado
    E o assento 20C deve ser atribuído ao passageiro
    E nenhuma taxa deve ser cobrada (troca de assento standard)

  Cenário: Alterar nome do passageiro (correção de grafia)
    Dado que existe a reserva PNR "NOM001"
    E o nome registrado é "Joao da Sivla"
    E o nome correto é "João da Silva"
    Quando o Agente de Reserva processa a correção
    Então o nome deve ser atualizado para "João da Silva"
    E nenhuma taxa deve ser cobrada (correção de grafia)
    E o histórico deve registrar a alteração

  Cenário: Adicionar serviço extra à reserva (refeição especial)
    Dado que existe a reserva PNR "SRV001" para voo internacional
    E o passageiro deseja refeição vegetariana
    Quando o Agente de Reserva adiciona o serviço
    Então o serviço "VGML" deve ser registrado
    E a companhia aérea deve ser notificada
    E a confirmação deve ser enviada ao passageiro

  Cenário: Adicionar seguro viagem à reserva
    Dado que existe a reserva PNR "SEG001" para GRU-CDG
    E o cliente deseja adicionar seguro viagem
    E o seguro custa R$ 120,00 para Europa por 10 dias
    Quando o Agente de Reserva adiciona o seguro
    Então o valor de R$ 120,00 deve ser adicionado ao total
    E a apólice do seguro deve ser vinculada à reserva
    E os detalhes da cobertura devem ser informados
