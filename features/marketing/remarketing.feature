# language: pt
Funcionalidade: Remarketing e Carrinho Abandonado
  Como agente de marketing
  Eu quero recuperar vendas abandonadas
  Para aumentar a taxa de conversão

  Cenário: Disparar remarketing 30 minutos após abandono
    Dado que o cliente abandonou reserva PNR "ABN001" há 30 minutos
    E o valor da reserva é R$ 890,00
    Quando a rotina de remarketing é executada
    Então um e-mail deve ser enviado com resumo da reserva
    E deve conter link direto para retomar pagamento

  Cenário: Segunda tentativa de remarketing após 24 horas
    Dado que o cliente não retornou após o primeiro e-mail
    E se passaram 24 horas
    Quando a segunda tentativa é disparada
    Então deve enviar e-mail com cupom de 5% de desconto
    E o cupom deve expirar em 48 horas

  Cenário: Terceira tentativa com urgência após 72 horas
    Dado que o cliente não converteu após 2 tentativas
    E a reserva expira em 24 horas
    Quando a terceira tentativa é disparada
    Então deve enviar SMS com urgência "Sua reserva expira amanhã!"
    E deve oferecer 10% de desconto

  Cenário: Remarketing via WhatsApp para cliente que prefere
    Dado que o cliente tem WhatsApp como canal preferido
    E abandonou carrinho há 1 hora
    Quando o remarketing é disparado
    Então a mensagem deve ser enviada via WhatsApp Business API
    E deve conter botão "Finalizar compra"

  Cenário: Não fazer remarketing após conversão
    Dado que o cliente abandonou e depois completou a compra
    Quando a rotina de remarketing verifica
    Então nenhum e-mail de abandono deve ser enviado
    E o cliente deve receber confirmação de compra

  Cenário: Remarketing com preço atualizado
    Dado que o preço era R$ 800,00 no abandono
    E o preço atual subiu para R$ 850,00
    Quando o e-mail de remarketing é gerado
    Então deve exibir preço atual R$ 850,00
    E deve alertar "Preço pode subir"

  Cenário: Remarketing com preço reduzido
    Dado que o preço era R$ 800,00 no abandono
    E o preço atual caiu para R$ 720,00
    Quando o e-mail é gerado
    Então deve destacar "Boa notícia! O preço caiu R$ 80,00"

  Cenário: Personalizar remarketing por destino
    Dado que o cliente abandonou voo para Paris
    Quando o e-mail é montado
    Então deve incluir imagem de Paris
    E dicas de viagem para a França

  Cenário: Limitar remarketing a 3 tentativas
    Dado que o cliente já recebeu 3 e-mails de abandono
    Quando a 4ª tentativa seria disparada
    Então nenhum envio adicional deve ocorrer
    E o cliente deve entrar em cooldown de 30 dias

  Cenário: Medir taxa de recuperação de carrinho
    Dado que 1.000 carrinhos foram abandonados no mês
    E 120 foram recuperados via remarketing
    Quando o MKT calcula métricas
    Então a taxa de recuperação deve ser 12%
