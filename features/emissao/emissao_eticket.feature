# language: pt
Funcionalidade: Emissão de E-Ticket
  Como cliente
  Eu quero receber meu bilhete eletrônico rapidamente
  Para realizar o check-in sem fricção

  Cenário: Emitir e-ticket após confirmação de pagamento
    Dado que o pagamento de R$ 450,00 foi confirmado
    E a reserva PNR "EMI001" está ativa
    Quando o Agente de Emissão processa a emissão
    Então um e-ticket com 13 dígitos deve ser gerado
    E o tempo de emissão deve ser inferior a 3 segundos
    E o evento "ticket.issued" deve ser publicado

  Cenário: Gerar número de bilhete único padrão IATA
    Dado que o pagamento foi confirmado
    Quando o EMI emite o bilhete
    Então o número deve ter 13 dígitos numéricos
    E o código da companhia deve ser os 3 primeiros dígitos
    E o número deve ser único no sistema

  Cenário: Emitir bilhete com itinerário detalhado
    Dado que a reserva é GRU-MIA com conexão em PTY
    Quando o bilhete é emitido
    Então o itinerário deve listar GRU-PTY e PTY-MIA
    E cada trecho deve ter horário, voo e classe
    E o tempo de conexão deve ser indicado

  Cenário: Emitir bilhete infantil vinculado ao adulto
    Dado que a reserva tem adulto e bebê de colo
    Quando o EMI emite os bilhetes
    Então o bilhete INF deve estar vinculado ao bilhete do adulto
    E deve indicar "INF" no campo de tipo de passageiro

  Cenário: Emitir bilhete com informações de bagagem
    Dado que a tarifa inclui 1 bagagem de 23kg
    Quando o bilhete é emitido
    Então deve indicar "1PC 23KG" na franquia de bagagem
    E bagagem de mão deve indicar "1PC 10KG"

  Cenário: Registrar bilhete no GDS
    Dado que o bilhete 045-1234567890 foi emitido
    Quando o EMI registra no GDS
    Então o status do PNR no GDS deve ser "ticketed"
    E o número do bilhete deve constar no PNR

  Cenário: Registrar bilhete no BSP
    Dado que o bilhete foi emitido para voo internacional
    Quando o EMI registra no BSP
    Então a transação deve aparecer no ciclo de faturamento BSP
    E o valor deve corresponder ao pagamento

  Cenário: Falha na emissão aciona rollback
    Dado que o GDS está indisponível
    Quando o EMI tenta emitir e falha
    Então o evento "ticket.issue.failed" deve ser publicado
    E o Orquestrador deve iniciar rollback
    E o pagamento deve ser estornado

  Cenário: Validar conformidade IATA Reso 792
    Dado que o bilhete foi emitido
    Quando o EMI valida o formato
    Então todos os campos obrigatórios IATA devem estar presentes
    E o formato deve estar em conformidade com Reso 792

  Cenário: Enviar bilhete para Agente de Notificações
    Dado que o bilhete 045-9876543210 foi emitido
    Quando a emissão é confirmada
    Então o NOT deve receber solicitação de envio
    E o e-ticket em PDF deve ser anexado ao e-mail

  Cenário: Emitir cupom de voo separado por trecho
    Dado que a reserva tem 3 trechos
    Quando o EMI emite o bilhete
    Então 3 cupons de voo devem ser gerados
    E cada cupom deve ter status independente

  Cenário: Emitir bilhete codeshare com operador real
    Dado que o voo é vendido por LATAM e operado por BA
    Quando o bilhete é emitido
    Então deve indicar operador "British Airways"
    E deve indicar vendedor "LATAM"
