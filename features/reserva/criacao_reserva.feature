# language: pt
Funcionalidade: Criação de Reserva
  Como cliente
  Eu quero criar uma reserva de passagem aérea
  Para garantir meu assento enquanto finalizo o pagamento

  Cenário: Criar reserva com sucesso e gerar PNR
    Dado que o cliente selecionou voo LATAM LA3421 GRU-GIG
    E informou passageiro "João Silva" CPF "123.456.789-00"
    Quando o Agente de Reserva cria a reserva
    Então um PNR de 6 caracteres alfanuméricos deve ser gerado
    E o status da reserva deve ser "pendente_pagamento"
    E o tempo de criação deve ser inferior a 2 segundos

  Cenário: Criar reserva para múltiplos passageiros
    Dado que são 3 passageiros no mesmo voo
    Quando o Agente de Reserva cria a reserva
    Então um único PNR deve conter os 3 passageiros
    E cada passageiro deve ter registro individual no PNR

  Cenário: Rejeitar reserva com dados de passageiro inválidos
    Dado que o CPF informado é "000.000.000-00"
    Quando o Agente de Reserva valida os dados
    Então a reserva deve ser rejeitada
    E deve retornar erro "documento_invalido"

  Cenário: Rejeitar reserva quando voo sem disponibilidade
    Dado que o voo GOL G3100 está lotado
    Quando o Agente de Reserva tenta criar reserva
    Então deve retornar erro "sem_disponibilidade"
    E deve sugerir voos alternativos

  Cenário: Criar reserva com bebê de colo vinculado ao adulto
    Dado que o adulto "Maria Santos" viaja com bebê "Pedro Santos" (8 meses)
    Quando a reserva é criada
    Então o bebê deve estar vinculado ao adulto no PNR
    E não deve ocupar assento individual

  Cenário: Criar reserva internacional com passaporte
    Dado que o voo é GRU-MIA internacional
    E o passageiro informou passaporte "BR1234567" válido até "2030-05-01"
    Quando a reserva é criada
    Então o passaporte deve ser registrado no PNR
    E deve validar validade mínima de 6 meses após o voo

  Cenário: Rejeitar passaporte com validade insuficiente
    Dado que o voo internacional é em "2026-12-01"
    E o passaporte expira em "2027-02-01"
    Quando o Agente de Reserva valida documentos
    Então deve rejeitar com erro "passaporte_validade_insuficiente"

  Cenário: Detectar conflito de horário com reserva existente
    Dado que o cliente já tem reserva com voo saindo às 08:00
    E tenta reservar outro voo saindo às 07:30 no mesmo dia
    Quando o Agente de Reserva verifica conflitos
    Então deve alertar "conflito_horario"
    E deve solicitar confirmação do cliente

  Cenário: Enviar dados da reserva para pagamento
    Dado que a reserva PNR "XYZ789" foi criada com valor R$ 450,00
    Quando a reserva é confirmada para pagamento
    Então o evento "reservation.confirmed" deve ser publicado
    E o Agente de Pagamento deve receber PNR, valor e dados do cliente

  Cenário: Garantir unicidade do PNR
    Dado que o PNR "ABC123" já existe no sistema
    Quando uma nova reserva tenta usar o mesmo código
    Então um novo PNR único deve ser gerado
    E nunca deve haver duplicidade
