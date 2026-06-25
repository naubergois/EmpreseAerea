# language: pt
Funcionalidade: Campanhas de E-mail Marketing
  Como agente de marketing
  Eu quero criar e enviar campanhas de e-mail
  Para promover passagens e aumentar vendas

  Cenário: Criar campanha sazonal de verão
    Dado que a campanha "Verão 2027" está configurada
    E o desconto é de 15% em rotas para o Nordeste
    Quando a campanha é disparada para 50.000 clientes
    Então os e-mails devem ser enviados via NOT em até 2 horas
    E cada e-mail deve conter cupom "VERAO15"

  Cenário: Personalizar assunto do e-mail com nome do cliente
    Dado que o cliente se chama "Carlos"
    Quando o e-mail da campanha é montado
    Então o assunto deve conter "Carlos"
    E o corpo deve ter saudação personalizada

  Cenário: Incluir preços dinâmicos no e-mail
    Dado que a campanha promove GRU-SSA
    E o menor preço atual é R$ 389,00
    Quando o e-mail é gerado
    Então deve exibir "A partir de R$ 389,00"
    E o preço deve ser atualizado no momento do envio

  Cenário: Rastrear taxa de abertura da campanha
    Dado que 10.000 e-mails foram enviados
    E 2.500 foram abertos
    Quando o MKT analisa métricas
    Então a taxa de abertura deve ser 25%
    E deve ser registrada no dashboard

  Cenário: Rastrear taxa de clique e conversão
    Dado que 2.500 clientes abriram o e-mail
    E 500 clicaram no link de compra
    E 50 completaram a compra
    Quando o MKT analisa funil
    Então CTR deve ser 20% e conversão 2%

  Cenário: Respeitar frequency capping
    Dado que o cliente já recebeu 3 e-mails promocionais esta semana
    Quando nova campanha tenta incluir o cliente
    Então o cliente deve ser excluído do disparo

  Cenário: A/B test de assunto de e-mail
    Dado que variante A é "Sua viagem dos sonhos espera!"
    E variante B é "Carlos, voos a partir de R$ 199!"
    Quando a campanha é disparada
    Então 50% recebem variante A e 50% variante B
    E após 48h a variante vencedora deve ser identificada

  Cenário: Campanha com landing page dinâmica
    Dado que o link do e-mail aponta para landing "VERAO27"
    Quando o cliente clica
    Então deve abrir página com ofertas do Nordeste
    E o cupom VERAO15 deve ser pré-aplicado

  Cenário: Calcular ROI da campanha
    Dado que a campanha custou R$ 5.000 para enviar
    E gerou R$ 150.000 em vendas
    Quando o MKT calcula ROI
    Então o ROI deve ser 2.900%

  Cenário: Pausar campanha com alta taxa de descadastro
    Dado que a taxa de unsubscribe ultrapassou 2%
    Quando o MKT monitora a campanha
    Então a campanha deve ser pausada automaticamente
    E a equipe deve ser alertada
