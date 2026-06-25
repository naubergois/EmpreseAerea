# language: pt
Funcionalidade: Expiração de Milhas
  Como agente de fidelidade
  Eu quero gerenciar expiração de milhas
  Para manter o programa sustentável e incentivar uso

  Cenário: Expirar milhas após 24 meses de inatividade
    Dado que 5.000 milhas foram creditadas em "2024-06-01"
    E não houve movimentação desde então
    Quando completam 24 meses
    Então as 5.000 milhas devem expirar
    E o saldo deve ser reduzido

  Cenário: Notificar expiração com 90 dias de antecedência
    Dado que 10.000 milhas expiram em 90 dias
    Quando o job de alerta é executado
    Então o NOT deve enviar e-mail de alerta
    E deve sugerir opções de resgate

  Cenário: Notificar expiração com 60 dias de antecedência
    Dado que 10.000 milhas expiram em 60 dias
    Quando o job de alerta é executado
    Então deve enviar segundo alerta
    E deve incluir ofertas de resgate do MKT

  Cenário: Notificar expiração com 30 dias de antecedência
    Dado que 10.000 milhas expiram em 30 dias
    Quando o job de alerta é executado
    Então deve enviar alerta urgente via SMS e e-mail
    E deve destacar "Última chance de usar suas milhas"

  Cenário: Milhas utilizadas não expiram (FIFO)
    Dado que o cliente tem 20.000 milhas de 2024 e 10.000 de 2025
    E resgata 15.000 milhas
    Quando o débito é processado
    Então deve consumir primeiro as 20.000 de 2024 (mais antigas)
    E restam 5.000 de 2024 + 10.000 de 2025

  Cenário: Estender validade com atividade
    Dado que o cliente tem 8.000 milhas prestes a expirar
    E realiza nova compra que gera milhas
    Quando a atividade é registrada
    Então a validade das 8.000 milhas deve ser estendida por 24 meses

  Cenário: Registrar expiração no extrato
    Dado que 3.000 milhas expiraram
    Quando o extrato é consultado
    Então deve mostrar: "Expiração: -3.000 milhas em 25/06/2026"
    E saldo atualizado

  Cenário: Não expirar milhas de clientes Diamante
    Dado que o cliente é nível Diamante
    E a política Diamante isenta expiração
    Quando o job de expiração é executado
    Então as milhas do Diamante não devem expirar

  Cenário: Relatório de milhas a expirar no trimestre
    Dado que 500.000 milhas expiram no próximo trimestre
    Quando o gestor solicita relatório
    Então deve listar clientes afetados e valores
    E deve sugerir campanha de resgate do MKT

  Cenário: Reverter expiração por erro do sistema
    Dado que 2.000 milhas expiraram por erro de cálculo
    Quando o erro é identificado e corrigido
    Então as 2.000 milhas devem ser recreditadas
    E o extrato deve registrar correção
