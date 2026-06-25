# language: pt
Funcionalidade: Boarding Pass
  Como cliente
  Eu quero receber meu cartão de embarque
  Para embarcar no voo com agilidade

  Cenário: Gerar boarding pass em PDF após check-in
    Dado que o bilhete 045-1234567890 foi emitido
    E o check-in foi realizado
    Quando o EMI gera o boarding pass
    Então um PDF deve ser gerado com dados do passageiro
    E deve conter código de barras PDF417
    E deve indicar portão, assento e horário de embarque

  Cenário: Gerar QR code para check-in mobile
    Dado que o check-in mobile foi realizado
    Quando o boarding pass é gerado
    Então um QR code IATA BCBP deve ser incluído
    E deve ser escaneável no portão de embarque

  Cenário: Boarding pass com assento e grupo de embarque
    Dado que o passageiro tem assento 14C
    E o grupo de embarque é 3
    Quando o boarding pass é gerado
    Então deve exibir assento "14C" e grupo "3"
    E horário de embarque deve ser 30 min antes da partida

  Cenário: Boarding pass para voo codeshare
    Dado que o voo é operado por outra companhia
    Quando o boarding pass é gerado
    Então deve exibir logo e dados do operador real
    E o número do voo do operador deve constar

  Cenário: Reenviar boarding pass por e-mail
    Dado que o boarding pass já foi gerado
    E o cliente perdeu o documento
    Quando solicita reenvio
    Então o mesmo boarding pass deve ser reenviado via NOT
    E nenhum novo check-in deve ser necessário

  Cenário: Boarding pass multi-trecho com conexão
    Dado que o passageiro tem conexão GRU-PTY-MIA
    Quando os boarding passes são gerados
    Então um boarding pass deve ser gerado por trecho
    E deve indicar terminal de conexão em PTY

  Cenário: Bloquear boarding pass sem check-in
    Dado que o check-in ainda não foi realizado
    Quando o cliente tenta obter boarding pass
    Então deve informar "checkin_necessario"
    E deve redirecionar para fluxo de check-in

  Cenário: Boarding pass com alerta de documento
    Dado que o voo é internacional
    Quando o boarding pass é gerado
    Então deve incluir lembrete "Apresente passaporte válido"

  Cenário: Atualizar boarding pass após mudança de portão
    Dado que o portão mudou de 22 para 25
    Quando o sistema recebe atualização operacional
    Então o boarding pass deve ser atualizado
    E o NOT deve notificar o passageiro

  Cenário: Boarding pass acessível para passageiro cadeirante
    Dado que o passageiro tem SSR WCHR
    Quando o boarding pass é gerado
    Então deve indicar "Assistência especial: Cadeirante"
    E prioridade de embarque deve ser destacada
