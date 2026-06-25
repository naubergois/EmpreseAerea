# language: pt
Funcionalidade: Atendimento Multiidioma
  Como cliente internacional
  Eu quero atendimento no meu idioma
  Para comunicar minhas necessidades claramente

  Cenário: Detectar e responder em português
    Dado que o cliente escreve "Onde está meu bilhete?"
    Quando o ATC detecta idioma
    Então deve responder em português
    E deve manter português nas próximas interações

  Cenário: Detectar e responder em inglês
    Dado que o cliente escreve "Where is my boarding pass?"
    Quando o ATC detecta idioma
    Então deve responder em inglês

  Cenário: Detectar e responder em espanhol
    Dado que o cliente escreve "¿Cuál es el estado de mi reserva?"
    Quando o ATC detecta idioma
    Então deve responder em espanhol

  Cenário: Alternar idioma durante conversa
    Dado que o cliente iniciou em português
    E depois escreve "Can you help me in English?"
    Quando o ATC detecta mudança
    Então deve alternar para inglês
    E deve manter contexto da conversa

  Cenário: Templates de notificação no idioma do cliente
    Dado que o cliente tem preferência de idioma "EN"
    Quando o ATC envia confirmação
    Então o template em inglês deve ser utilizado

  Cenário: FAQ traduzido para os 3 idiomas
    Dado que o cliente pergunta sobre bagagem em francês
    Quando o ATC não suporta francês
    Então deve informar idiomas disponíveis (PT, EN, ES)
    E deve oferecer escalação humana com intérprete

  Cenário: Atendimento telefônico com menu de idiomas
    Dado que o cliente liga para central
    Quando a chamada é atendida
    Então deve oferecer opção 1-PT, 2-EN, 3-ES
    E deve rotear para fila do idioma selecionado

  Cenário: Documentos e políticas no idioma do cliente
    Dado que o cliente é estrangeiro com preferência EN
    Quando solicita política de cancelamento
    Então deve enviar documento em inglês

  Cenário: Manter qualidade de tradução em respostas automáticas
    Dado que a resposta FAQ é traduzida automaticamente
    Quando enviada ao cliente
    Então a tradução deve ter score de qualidade > 90%
    E termos técnicos aéreos devem ser corretos

  Cenário: Registrar idioma preferido no perfil do cliente
    Dado que o cliente atendeu 5 vezes em espanhol
    Quando o perfil é atualizado
    Então o idioma preferido deve ser "ES"
    E futuras interações devem iniciar em espanhol
