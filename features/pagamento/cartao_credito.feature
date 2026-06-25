# language: pt
Funcionalidade: Pagamento com Cartão de Crédito
  Como cliente
  Eu quero pagar minha passagem com cartão de crédito
  Para confirmar minha viagem de forma rápida e segura

  Cenário: Processar pagamento com cartão Visa à vista
    Dado que a reserva PNR "ABC123" tem valor total de R$ 1.200,00
    E o cliente fornece cartão Visa final 1111 com validade 12/2028
    E o pagamento é à vista
    Quando o Agente de Pagamento processa a transação
    Então o pagamento deve ser autorizado
    E o valor de R$ 1.200,00 deve ser capturado
    E o Agente de Emissão deve ser notificado
    E um recibo deve ser gerado
    E o tempo de processamento deve ser inferior a 5 segundos

  Cenário: Processar pagamento parcelado em 6x sem juros
    Dado que a reserva tem valor total de R$ 3.000,00
    E o cliente escolhe parcelamento em 6x sem juros
    Quando o Agente de Pagamento processa o parcelamento
    Então cada parcela deve ser de R$ 500,00
    E 6 parcelas devem ser registradas
    E o cartão deve ser autorizado para o valor total
    E as datas de cobrança de cada parcela devem ser informadas

  Cenário: Processar pagamento parcelado em 10x com juros
    Dado que a reserva tem valor total de R$ 5.000,00
    E o cliente escolhe parcelamento em 10x
    E a taxa de juros é 1.5% ao mês
    Quando o Agente de Pagamento calcula o parcelamento
    Então o valor total com juros deve ser calculado
    E cada parcela deve ser informada com o valor exato
    E o CET deve ser exibido
    E o cliente deve confirmar o valor com juros antes de processar

  Cenário: Recusar cartão com CVV inválido
    Dado que o cliente fornece cartão com CVV "99" (2 dígitos)
    Quando o Agente de Pagamento valida os dados
    Então a validação deve falhar
    E a mensagem "CVV inválido" deve ser retornada
    E nenhuma tentativa de autorização deve ser feita ao gateway

  Cenário: Recusar cartão expirado
    Dado que o cliente fornece cartão com validade "03/2025"
    E a data atual é junho de 2026
    Quando o Agente de Pagamento valida os dados
    Então a validação deve falhar
    E a mensagem "Cartão expirado" deve ser retornada

  Cenário: Recusar pagamento por saldo insuficiente
    Dado que o cliente fornece cartão Mastercard válido
    E o valor da compra é R$ 2.000,00
    E o limite disponível do cartão é R$ 1.500,00
    Quando o Agente de Pagamento tenta autorização
    Então a autorização deve ser recusada pelo emissor
    E o código "51 - Saldo insuficiente" deve ser retornado
    E o cliente deve ser informado
    E a reserva não deve ser cancelada (permitir nova tentativa)

  Cenário: Recusar cartão com número inválido (Luhn)
    Dado que o cliente fornece número de cartão "4111111111111112"
    Quando o Agente de Pagamento valida o número pelo algoritmo Luhn
    Então a validação deve falhar
    E a mensagem "Número de cartão inválido" deve ser retornada

  Cenário: Processar pagamento com cartão de débito
    Dado que a reserva PNR "DEB001" tem valor de R$ 500,00
    E o cliente fornece cartão de débito Visa Electron
    E o pagamento é à vista (débito não parcela)
    Quando o Agente de Pagamento processa
    Então o valor deve ser debitado imediatamente
    E a confirmação deve ser instantânea
    E parcelamento não deve ser oferecido

  Cenário: Processar pagamento com cartão Amex (4 dígitos CVV)
    Dado que o cliente fornece cartão American Express
    E o CVV tem 4 dígitos "1234"
    Quando o Agente de Pagamento valida os dados
    Então a validação deve aceitar CVV de 4 dígitos para Amex
    E o pagamento deve ser processado normalmente

  Cenário: Limitar tentativas de pagamento a 3 por sessão
    Dado que o cliente já tentou pagar 3 vezes e todas falharam
    Quando o cliente tenta uma 4a vez
    Então a tentativa deve ser bloqueada
    E a mensagem "Número máximo de tentativas atingido" deve ser exibida
    E o cliente deve ser orientado a contatar o suporte
