# language: pt
Funcionalidade: FAQ e Autoatendimento
  Como cliente
  Eu quero respostas automáticas para perguntas frequentes
  Para resolver dúvidas sem esperar atendente

  Cenário: Pergunta sobre documentos para viagem internacional
    Dado que o cliente pergunta "Preciso de visto para ir aos EUA?"
    Quando o ATC processa via FAQ
    Então deve informar requisito ESTA ou visto B1/B2
    E deve linkar documentação oficial

  Cenário: Pergunta sobre política de cancelamento
    Dado que o cliente pergunta "Posso cancelar minha passagem?"
    E tem reserva em tarifa flexível
    Quando o ATC consulta política
    Então deve informar condições específicas da tarifa
    E deve informar valor de reembolso estimado

  Cenário: Pergunta sobre check-in online
    Dado que o cliente pergunta "Quando posso fazer check-in?"
    Quando o ATC responde
    Então deve informar "Check-in online abre 48h antes do voo"
    E deve fornecer link para check-in

  Cenário: Pergunta sobre transporte de animais
    Dado que o cliente pergunta "Posso levar meu cachorro no avião?"
    Quando o ATC responde
    Então deve informar política de transporte de animais
    E deve indicar necessidade de reserva prévia

  Cenário: Pergunta não reconhecida escala para humano
    Dado que o cliente pergunta algo fora da base de FAQ
    E o ATC não consegue responder com confiança > 80%
    Quando a confiança é baixa
    Então deve escalar para atendente humano
    E deve informar tempo estimado de espera

  Cenário: FAQ sobre milhas e fidelidade
    Dado que o cliente pergunta "Quantas milhas ganho nesta compra?"
    E o voo é GRU-MIA executiva
    Quando o ATC consulta FID
    Então deve calcular milhas estimadas
    E deve informar bônus por nível de fidelidade

  Cenário: FAQ sobre formas de pagamento
    Dado que o cliente pergunta "Aceitam PIX?"
    Quando o ATC responde
    Então deve listar todas as formas de pagamento aceitas
    E deve informar desconto PIX se houver

  Cenário: Sugerir solução proativa por contexto
    Dado que o cliente consultou PNR com voo amanhã
    E ainda não fez check-in
    Quando o ATC identifica contexto
    Então deve sugerir proativamente "Deseja fazer check-in agora?"

  Cenário: Registrar interação FAQ para melhoria contínua
    Dado que o cliente fez pergunta respondida pelo FAQ
    Quando a interação é concluída
    Então deve registrar pergunta, resposta e satisfação
    E deve alimentar base de conhecimento

  Cenário: Taxa de resolução sem humano acima de 80%
    Dado que 100 atendimentos foram realizados no dia
    E 85 foram resolvidos automaticamente
    Quando métricas são calculadas
    Então a taxa de resolução automática deve ser 85%
