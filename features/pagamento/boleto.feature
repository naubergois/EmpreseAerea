# language: pt
Funcionalidade: Pagamento via Boleto
  Como cliente
  Eu quero pagar via boleto bancário
  Para ter prazo adicional para pagamento

  Cenário: Gerar boleto com vencimento em 3 dias
    Dado que a reserva PNR "BOL001" tem valor R$ 1.200,00
    Quando o cliente escolhe pagamento por boleto
    Então um boleto deve ser gerado com vencimento em 3 dias úteis
    E o código de barras deve ser válido
    E o boleto deve ser enviado por e-mail

  Cenário: Confirmar pagamento após compensação bancária
    Dado que o boleto foi pago
    E a compensação bancária ocorreu em 2 dias úteis
    Quando o PAG recebe confirmação
    Então o pagamento deve ser aprovado
    E a emissão do bilhete deve ser acionada

  Cenário: Cancelar reserva por boleto vencido
    Dado que o boleto venceu há 1 dia
    E o pagamento não foi realizado
    Quando o PAG verifica status
    Então a reserva deve ser cancelada
    E o assento deve ser liberado

  Cenário: Não permitir boleto para voo em menos de 5 dias
    Dado que o voo é em 3 dias
    Quando o cliente tenta pagar com boleto
    Então deve rejeitar com erro "prazo_insuficiente_boleto"
    E deve sugerir PIX ou cartão

  Cenário: Gerar segunda via do boleto
    Dado que o boleto original foi gerado
    E o cliente perdeu o boleto
    Quando solicita segunda via
    Então o mesmo boleto deve ser reenviado
    E nenhum boleto duplicado deve ser criado

  Cenário: Boleto com valor atualizado após alteração de reserva
    Dado que o boleto foi gerado para R$ 800,00
    E a reserva foi alterada para R$ 950,00 antes do pagamento
    Quando o boleto antigo é invalidado
    Então um novo boleto de R$ 950,00 deve ser gerado
