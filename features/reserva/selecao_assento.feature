# language: pt
Funcionalidade: Seleção de Assento
  Como cliente
  Eu quero selecionar meu assento no avião
  Para garantir o lugar de minha preferência

  Cenário: Selecionar assento disponível na janela
    Dado que a reserva PNR "ABC123" foi criada
    E o mapa de assentos do voo mostra o assento 15A como disponível
    Quando o passageiro seleciona o assento 15A
    Então o assento 15A deve ser atribuído ao passageiro
    E o assento deve ser marcado como "reservado" no mapa
    E nenhum custo adicional deve ser cobrado (assento standard)

  Cenário: Rejeitar seleção de assento já ocupado
    Dado que a reserva PNR "DEF456" foi criada
    E o assento 10B está ocupado por outro passageiro
    Quando o passageiro tenta selecionar o assento 10B
    Então a seleção deve ser rejeitada
    E a mensagem "Assento indisponível" deve ser retornada
    E o mapa atualizado deve ser exibido

  Cenário: Selecionar assento com custo adicional (saída de emergência)
    Dado que o passageiro seleciona o assento 21A (saída de emergência)
    E o custo adicional é R$ 80,00
    E o passageiro tem mais de 18 anos
    Quando o Agente de Reserva processa a seleção
    Então o assento 21A deve ser atribuído
    E R$ 80,00 deve ser adicionado ao valor total
    E o passageiro deve confirmar que pode operar a saída de emergência

  Cenário: Rejeitar assento de emergência para menor de 18 anos
    Dado que o passageiro tem 16 anos
    E tenta selecionar o assento 21A (saída de emergência)
    Quando o Agente de Reserva valida a seleção
    Então a seleção deve ser rejeitada
    E a mensagem "Menores de 18 anos não podem sentar na saída de emergência" deve ser retornada

  Cenário: Selecionar assento preferencial com custo adicional
    Dado que o passageiro seleciona o assento 3C (preferencial, mais espaço)
    E o custo adicional é R$ 120,00
    Quando o Agente de Reserva processa a seleção
    Então o assento 3C deve ser atribuído
    E R$ 120,00 deve ser adicionado ao valor total
    E o breakdown deve listar "Assento preferencial: R$ 120,00"

  Cenário: Atribuição automática de assento quando não selecionado
    Dado que a reserva PNR "GHI789" foi criada
    E o passageiro não selecionou assento
    Quando o check-in é realizado
    Então o sistema deve atribuir automaticamente um assento livre
    E o assento deve ser em posição standard (sem custo)
    E o passageiro deve ser notificado do assento atribuído

  Cenário: Liberar assento após timeout de reserva
    Dado que a reserva PNR "JKL012" foi criada há 21 minutos
    E o pagamento não foi realizado
    Quando o timer de timeout expira
    Então a reserva deve ser cancelada automaticamente
    E o assento reservado deve ser liberado
    E o status deve mudar para "expirado"
    E o cliente deve ser notificado via Agente de Notificações

  Cenário: Selecionar assentos adjacentes para família
    Dado que a reserva é para 2 adultos e 2 crianças
    E o passageiro solicita assentos adjacentes
    Quando o Agente de Reserva busca assentos
    Então deve retornar opções de 4 assentos na mesma fileira
    E se não houver 4 adjacentes deve oferecer 2+2 próximos
    E as crianças devem ficar ao lado de ao menos 1 adulto
