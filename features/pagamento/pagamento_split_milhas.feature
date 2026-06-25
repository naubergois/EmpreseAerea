# language: pt
Funcionalidade: Pagamento Split com Milhas
  Como cliente
  Eu quero combinar milhas e dinheiro no pagamento
  Para aproveitar meu saldo de fidelidade

  Cenário: Pagamento 100% em milhas
    Dado que o cliente tem 80.000 milhas
    E a passagem custa 60.000 milhas
    Quando o cliente escolhe pagar integralmente com milhas
    Então 60.000 milhas devem ser debitadas
    E nenhuma cobrança em dinheiro deve ser feita
    E o FID deve confirmar o débito

  Cenário: Pagamento split 50% milhas e 50% cartão
    Dado que a passagem custa R$ 2.000,00 (40.000 milhas)
    E o cliente tem 20.000 milhas
    Quando escolhe usar todas as milhas + cartão
    Então 20.000 milhas devem ser debitadas
    E R$ 1.000,00 devem ser cobrados no cartão

  Cenário: Rejeitar split quando milhas insuficientes
    Dado que o cliente tem 5.000 milhas
    E o mínimo para resgate é 10.000 milhas
    Quando tenta pagar com milhas
    Então deve rejeitar com erro "milhas_insuficientes"

  Cenário: Reverter milhas em caso de rollback
    Dado que 30.000 milhas foram debitadas
    E o pagamento em cartão falhou
    Quando o Orquestrador executa rollback
    Então as 30.000 milhas devem ser recreditadas
    E o saldo do FID deve ser restaurado

  Cenário: Calcular conversão milhas para reais
    Dado que a taxa é 1.000 milhas = R$ 50,00
    E o cliente quer abater R$ 200,00 em milhas
    Quando o PRE calcula
    Então 4.000 milhas devem ser necessárias

  Cenário: Aplicar bônus de milhas em pagamento split
    Dado que o cliente é nível Ouro
    E a promoção oferece 50% bônus no resgate
    E a passagem custa 20.000 milhas
    Quando o cliente resgata
    Então apenas 13.333 milhas efetivas devem ser debitadas

  Cenário: Pagamento split com PIX e milhas
    Dado que o cliente usa 15.000 milhas e PIX para o restante
    E o valor restante é R$ 750,00
    Quando o PAG processa
    Então milhas devem ser debitadas primeiro
    E QR code PIX deve ser gerado para R$ 750,00

  Cenário: Validar milhas antes de confirmar split
    Dado que o cliente selecionou split payment
    Quando o PAG inicia processamento
    Então o FID deve validar saldo em tempo real
    E deve bloquear milhas durante transação
