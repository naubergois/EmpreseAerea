# language: pt
Funcionalidade: Escalação para Atendimento Humano
  Como agente de atendimento
  Eu quero escalar casos complexos para humanos
  Para garantir resolução satisfatória

  Cenário: Escalar após 3 tentativas sem resolução
    Dado que o ATC tentou resolver 3 vezes sem sucesso
    Quando a 3ª tentativa falha
    Então deve escalar para fila de atendentes humanos
    E deve informar tempo estimado de espera

  Cenário: Escalar por solicitação explícita do cliente
    Dado que o cliente diz "Quero falar com um atendente"
    Quando o ATC detecta a solicitação
    Então deve escalar imediatamente
    E deve informar posição na fila

  Cenário: Transferir contexto completo ao humano
    Dado que o atendimento será escalado
    Quando a transferência ocorre
    Então o atendente humano deve receber:
      | Dado              | Valor        |
      | PNR               | ABC123       |
      | Histórico chat    | Completo     |
      | Sentimento        | Negativo     |
      | Tentativas auto   | 3            |
      | Urgência          | Alta         |

  Cenário: Escalar por valor alto da transação
    Dado que a reserva vale R$ 25.000,00
    E o cliente solicita alteração
    Quando o valor excede limite de autoatendimento
    Então deve escalar automaticamente para humano

  Cenário: Escalar reclamação formal
    Dado que o cliente registra reclamação no Procon
    Quando o ATC identifica reclamação formal
    Então deve escalar para equipe de qualidade
    E deve marcar como prioridade máxima

  Cenário: Escalar por sentimento muito negativo
    Dado que o sentimento é classificado como "muito negativo"
    E o cliente usa linguagem agressiva
    Quando o ATC detecta
    Então deve escalar com prioridade alta
    E deve alertar supervisor

  Cenário: Retornar ao bot após resolução humana
    Dado que o atendente humano resolveu o problema
    Quando o caso é encerrado
    Então o cliente deve poder voltar ao autoatendimento
    E o histórico humano deve ser preservado

  Cenário: CSAT após atendimento humano
    Dado que o atendimento humano foi concluído
    Quando o caso é encerrado
    Então deve solicitar avaliação CSAT (1-5)
    E deve registrar para métricas de qualidade

  Cenário: Tempo máximo de 5 minutos antes de escalação
    Dado que o cliente está aguardando há 5 minutos
    E o bot não resolveu
    Quando o timeout de autoatendimento é atingido
    Então deve escalar automaticamente
    E deve pedir desculpas pela demora

  Cenário: Disponibilidade 24/7 com escalação humana em horário comercial
    Dado que o cliente solicita humano às 03:00
    Quando não há atendentes disponíveis
    Então deve informar horário de atendimento humano
    E deve criar ticket para retorno prioritário
