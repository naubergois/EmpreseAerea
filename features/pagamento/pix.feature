# language: pt
Funcionalidade: Pagamento via PIX
  Como cliente
  Eu quero pagar minha passagem via PIX
  Para ter confirmação instantânea do pagamento

  Cenário: Gerar QR Code PIX para pagamento
    Dado que a reserva PNR "PIX001" tem valor de R$ 950,00
    E o cliente escolhe pagamento via PIX
    Quando o Agente de Pagamento gera o PIX
    Então um QR Code deve ser gerado
    E o código "copia e cola" deve ser fornecido
    E a validade do PIX deve ser 30 minutos
    E o valor deve ser exatamente R$ 950,00

  Cenário: Confirmar pagamento PIX recebido via webhook
    Dado que o PIX foi gerado para R$ 950,00
    E o cliente realizou a transferência via banco
    Quando o webhook do PSP confirma o recebimento
    Então o status do pagamento deve mudar para "confirmado"
    E o Agente de Emissão deve ser notificado imediatamente
    E o tempo entre pagamento e confirmação deve ser inferior a 10 segundos

  Cenário: Expirar PIX não pago em 30 minutos
    Dado que o PIX foi gerado há 31 minutos
    E o pagamento não foi recebido
    Quando o timer de expiração dispara
    Então o PIX deve ser cancelado
    E a reserva associada deve ser cancelada
    E o assento deve ser liberado
    E o cliente deve ser notificado da expiração

  Cenário: Rejeitar PIX com valor divergente
    Dado que o PIX foi gerado para R$ 950,00
    E o cliente transferiu R$ 900,00 (valor diferente)
    Quando o webhook recebe o pagamento
    Então o pagamento deve ser rejeitado
    E a devolução de R$ 900,00 deve ser iniciada
    E o cliente deve ser notificado do valor incorreto

  Cenário: Processar PIX duplicado (mesmo pagamento 2x)
    Dado que o PIX de R$ 950,00 já foi confirmado
    E o cliente envia um segundo PIX de R$ 950,00 por engano
    Quando o segundo pagamento é recebido
    Então o segundo PIX deve ser devolvido automaticamente
    E nenhuma ação adicional deve ser tomada na reserva
    E o log de devolução deve ser registrado
