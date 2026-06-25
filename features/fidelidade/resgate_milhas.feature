# language: pt
Funcionalidade: Resgate de Milhas
  Como cliente
  Eu quero resgatar milhas por passagens e benefícios
  Para aproveitar meu programa de fidelidade

  Cenário: Resgatar milhas por passagem completa
    Dado que o cliente tem 60.000 milhas
    E a passagem GRU-LIS custa 55.000 milhas
    Quando o cliente resgata
    Então 55.000 milhas devem ser debitadas
    E o saldo restante deve ser 5.000 milhas
    E o bilhete deve ser emitido sem cobrança adicional

  Cenário: Rejeitar resgate com milhas insuficientes
    Dado que o cliente tem 10.000 milhas
    E a passagem custa 40.000 milhas
    Quando tenta resgatar
    Então deve rejeitar com erro "milhas_insuficientes"
    E deve sugerir pagamento split

  Cenário: Resgatar milhas por upgrade de classe
    Dado que o cliente tem bilhete econômico GRU-MIA
    E o upgrade para executiva custa 15.000 milhas
    E o cliente tem 20.000 milhas
    Quando solicita upgrade
    Então 15.000 milhas devem ser debitadas
    E o bilhete deve ser reemitido em executiva

  Cenário: Validar milhas antes do resgate
    Dado que o cliente selecionou resgate de 30.000 milhas
    Quando o FID valida
    Então deve bloquear 30.000 milhas temporariamente
    E confirmar débito após emissão do bilhete

  Cenário: Liberar milhas bloqueadas em caso de falha
    Dado que 30.000 milhas foram bloqueadas para resgate
    E a emissão do bilhete falhou
    Quando o rollback é executado
    Então as 30.000 milhas devem ser desbloqueadas
    E o saldo deve ser restaurado

  Cenário: Resgate com taxas em dinheiro
    Dado que a passagem custa 40.000 milhas + R$ 350,00 em taxas
    Quando o cliente resgata
    Então 40.000 milhas devem ser debitadas
    E R$ 350,00 devem ser cobrados via PAG

  Cenário: Transferir milhas entre contas
    Dado que o cliente tem 50.000 milhas
    E deseja transferir 10.000 para conta do cônjuge
    Quando a transferência é solicitada
    Então 10.000 devem ser debitadas da conta origem
    E 10.000 devem ser creditadas na conta destino
    E taxa de transferência de 1.000 milhas deve ser cobrada

  Cenário: Resgate em promoção com desconto de milhas
    Dado que a promoção oferece passagem por 30.000 milhas (normal 45.000)
    Quando o cliente resgata durante promoção
    Então apenas 30.000 milhas devem ser debitadas

  Cenário: Calendário de resgate com disponibilidade limitada
    Dado que o resgate GRU-CDG tem 2 assentos disponíveis em milhas
    E 2 já foram resgatados
    Quando o 3º cliente tenta resgatar
    Então deve informar "sem_disponibilidade_resgate"
    E deve sugerir datas alternativas

  Cenário: Extrato de resgate detalhado
    Dado que o cliente resgatou 40.000 milhas
    Quando consulta extrato
    Então deve mostrar: data, destino, milhas debitadas, saldo anterior e atual
