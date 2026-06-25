# language: pt
Funcionalidade: Acúmulo de Milhas
  Como cliente
  Eu quero acumular milhas em cada compra
  Para resgatar benefícios futuros

  Cenário: Acumular milhas após emissão de bilhete
    Dado que o bilhete GRU-MIA econômica foi emitido
    E a tarifa base é R$ 2.500,00
    Quando o FID processa acúmulo
    Então deve creditar milhas proporcionais ao valor
    E o crédito deve ocorrer em menos de 1 segundo

  Cenário: Acumular milhas com multiplicador por nível Ouro
    Dado que o cliente é nível "Ouro" com multiplicador 1.5x
    E a compra geraria 2.500 milhas base
    Quando o FID calcula
    Então deve creditar 3.750 milhas

  Cenário: Acumular milhas com bônus promocional
    Dado que a promoção "2x milhas" está ativa
    E a compra geraria 1.000 milhas base
    Quando o FID processa com promoção
    Então deve creditar 2.000 milhas

  Cenário: Calcular milhas por trecho e classe
    Dado que o itinerário tem trecho econômico e executivo
    Quando o FID calcula
    Então cada trecho deve ter cálculo independente
    E executiva deve render mais milhas por km

  Cenário: Não acumular milhas em pagamento 100% milhas
    Dado que o cliente pagou integralmente com milhas
    Quando o FID avalia acúmulo
    Então nenhuma milha adicional deve ser creditada

  Cenário: Enfileirar acúmulo em degradação graciosa
    Dado que o FID está temporariamente indisponível
    E o bilhete foi emitido com sucesso
    Quando o Orquestrador detecta indisponibilidade
    Então o acúmulo deve ser enfileirado
    E processado quando o FID voltar

  Cenário: Acumular milhas de parceiro (hotel)
    Dado que o cliente reservou hotel parceiro
    E a parceria prevê 500 milhas por diária
    Quando o parceiro confirma estadia
    Então 500 milhas devem ser creditadas

  Cenário: Registrar extrato de acúmulo
    Dado que o cliente ganhou 3.500 milhas
    Quando o crédito é processado
    Então o extrato deve registrar: data, origem, quantidade, saldo
    E deve ser 100% rastreável

  Cenário: Reverter milhas em caso de cancelamento
    Dado que 3.500 milhas foram creditadas na compra
    E o bilhete foi cancelado com reembolso
    Quando o cancelamento é processado
    Então as 3.500 milhas devem ser debitadas
    E o saldo deve ser restaurado

  Cenário: Zero discrepância no saldo de milhas
    Dado que o saldo do cliente é 45.000 milhas
    Quando 3.500 são creditadas e 1.000 debitadas
    Então o saldo final deve ser exatamente 47.500
    E nenhuma discrepância deve existir
