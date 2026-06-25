# language: pt
Funcionalidade: Void e Reemissão de Bilhete
  Como agente de emissão
  Eu quero anular e reemitir bilhetes
  Para tratar alterações e correções dentro das regras IATA

  Cenário: Void de bilhete dentro de 24 horas
    Dado que o bilhete 045-1234567890 foi emitido há 6 horas
    E a companhia permite void em 24h
    Quando o void é solicitado
    Então o bilhete deve ser anulado no GDS
    E o status deve mudar para "voided"
    E o pagamento deve ser estornado via PAG

  Cenário: Rejeitar void após 24 horas
    Dado que o bilhete foi emitido há 48 horas
    Quando o void é solicitado
    Então deve rejeitar com erro "prazo_void_expirado"
    E deve sugerir cancelamento com taxa

  Cenário: Reemissão por alteração de voo
    Dado que o bilhete original 045-1234567890 é para voo G3100
    E o cliente alterou para voo G3150
    Quando a reemissão é processada
    Então um novo cupom deve ser emitido no mesmo bilhete
    E a diferença tarifária deve ser calculada pelo PRE

  Cenário: Reemissão com diferença tarifária a cobrar
    Dado que a tarifa original era R$ 500,00
    E a nova tarifa é R$ 650,00
    Quando a reemissão é processada
    Então R$ 150,00 devem ser cobrados adicionalmente
    E o bilhete reemitido deve refletir novo voo

  Cenário: Reemissão com diferença tarifária a reembolsar
    Dado que a tarifa original era R$ 800,00
    E a nova tarifa é R$ 600,00
    Quando a reemissão é processada
    Então R$ 200,00 devem ser estornados via PAG

  Cenário: Void automático em rollback da Saga
    Dado que o bilhete foi emitido mas a etapa posterior falhou
    Quando o Orquestrador aciona compensação
    Então o EMI deve fazer void automático do bilhete
    E deve confirmar void ao Orquestrador

  Cenário: Reemissão de bilhete codeshare
    Dado que o bilhete codeshare envolve LATAM e BA
    Quando a reemissão é solicitada
    Então ambos os sistemas (GDS de cada cia) devem ser atualizados
    E o bilhete deve manter referência codeshare

  Cenário: Reemissão multi-trecho parcial
    Dado que o bilhete tem 3 trechos
    E apenas o trecho 2 precisa ser alterado
    Quando a reemissão parcial é processada
    Então apenas o cupom do trecho 2 deve ser reemitido
    E trechos 1 e 3 devem permanecer inalterados

  Cenário: Registrar histórico de void e reemissão
    Dado que o bilhete teve 1 void e 1 reemissão
    Quando o histórico é consultado
    Então todas as operações devem estar registradas
    E deve incluir motivo, operador e timestamp

  Cenário: Backup redundante após reemissão
    Dado que o bilhete foi reemitido
    Quando a reemissão é confirmada
    Então o backup em região secundária deve ser atualizado
    E o bilhete antigo deve ser marcado como substituído
