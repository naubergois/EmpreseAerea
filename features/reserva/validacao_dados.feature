# language: pt
Funcionalidade: Validação de Dados do Passageiro
  Como agente de reserva
  Eu quero validar os dados do passageiro
  Para garantir conformidade e evitar problemas no embarque

  Cenário: Rejeitar reserva com CPF inválido
    Dado que o passageiro fornece CPF "111.111.111-11"
    Quando o Agente de Reserva valida os dados
    Então a validação deve falhar
    E a mensagem "CPF inválido" deve ser retornada
    E a reserva não deve ser criada

  Cenário: Rejeitar reserva com CPF com formato incorreto
    Dado que o passageiro fornece CPF "12345"
    Quando o Agente de Reserva valida os dados
    Então a validação deve falhar
    E a mensagem "Formato de CPF inválido" deve ser retornada

  Cenário: Rejeitar reserva com nome incompleto
    Dado que o passageiro fornece nome "João"
    E o sobrenome está vazio
    Quando o Agente de Reserva valida os dados
    Então a validação deve falhar
    E a mensagem "Nome completo é obrigatório" deve ser retornada

  Cenário: Rejeitar reserva com e-mail inválido
    Dado que o passageiro fornece e-mail "joao@"
    Quando o Agente de Reserva valida os dados
    Então a validação deve falhar
    E a mensagem "E-mail inválido" deve ser retornada

  Cenário: Rejeitar reserva para menor desacompanhado sem autorização
    Dado que o passageiro tem 10 anos
    E não há adulto responsável na reserva
    E não foi fornecida autorização para menor desacompanhado
    Quando o Agente de Reserva tenta criar a reserva
    Então a reserva deve ser bloqueada
    E a mensagem "Menor de 12 anos requer acompanhante adulto ou autorização" deve ser retornada

  Cenário: Aceitar menor desacompanhado com autorização (UMNR)
    Dado que o passageiro tem 10 anos
    E não há adulto na reserva
    E a autorização de menor desacompanhado (UMNR) foi fornecida
    E os dados do responsável de embarque e desembarque foram preenchidos
    Quando o Agente de Reserva cria a reserva
    Então a reserva deve ser criada com flag "UMNR"
    E o serviço de acompanhamento deve ser adicionado
    E a taxa de UMNR deve ser incluída

  Cenário: Validar passaporte para voo internacional com validade suficiente
    Dado que o voo é GRU-MIA (internacional)
    E o passageiro fornece passaporte BR1234567 com validade 2027-03-15
    E a data da viagem é 2026-08-15
    Quando o Agente de Reserva valida os documentos
    Então a validação deve ser bem-sucedida
    E a validade do passaporte é superior a 6 meses da data da viagem

  Cenário: Rejeitar reserva com passaporte vencido
    Dado que o voo é GRU-CDG (internacional)
    E o passaporte do passageiro vence em "2026-07-01"
    E a data da viagem é "2026-08-15"
    Quando o Agente de Reserva valida os documentos
    Então a validação deve falhar
    E a mensagem "Passaporte deve ter validade mínima de 6 meses" deve ser retornada

  Cenário: Rejeitar reserva com passaporte que vence em menos de 6 meses
    Dado que o voo é GRU-LHR (internacional)
    E o passaporte vence em "2027-01-10"
    E a data da viagem é "2026-08-15"
    Quando o Agente de Reserva valida os documentos
    Então a validação deve falhar
    E a mensagem "Passaporte com validade inferior a 6 meses da data da viagem" deve ser retornada

  Cenário: Validar dados de contato obrigatórios
    Dado que o passageiro não fornece telefone nem e-mail
    Quando o Agente de Reserva valida os dados
    Então a validação deve falhar
    E a mensagem "Ao menos um contato (telefone ou e-mail) é obrigatório" deve ser retornada

  Cenário: Aceitar passageiro com necessidades especiais
    Dado que o passageiro indica necessidade de cadeira de rodas
    E o tipo de assistência é "WCHR" (cadeira até a aeronave)
    Quando o Agente de Reserva registra a necessidade
    Então o código SSR "WCHR" deve ser adicionado à reserva
    E a companhia aérea deve ser notificada
    E a confirmação de assistência deve ser retornada
