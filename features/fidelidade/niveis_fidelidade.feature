# language: pt
Funcionalidade: Níveis de Fidelidade
  Como cliente
  Eu quero progredir de nível no programa de fidelidade
  Para obter benefícios exclusivos

  Cenário: Cliente novo inicia no nível Bronze
    Dado que o cliente acabou de se cadastrar
    Quando o FID cria conta de fidelidade
    Então o nível inicial deve ser "Bronze"
    E o saldo de milhas deve ser 0

  Cenário: Upgrade de Bronze para Prata
    Dado que o cliente acumulou 12.000 milhas qualificáveis no ano
    E o threshold Prata é 10.000
    Quando o FID avalia qualificação
    Então o nível deve ser atualizado para "Prata"
    E o NOT deve notificar upgrade

  Cenário: Upgrade de Prata para Ouro
    Dado que o cliente acumulou 35.000 milhas qualificáveis
    E o threshold Ouro é 30.000
    Quando o FID avalia
    Então o nível deve ser "Ouro"
    E benefícios Ouro devem ser ativados

  Cenário: Upgrade para Diamante
    Dado que o cliente acumulou 65.000 milhas qualificáveis
    E o threshold Diamante é 60.000
    Quando o FID avalia
    Então o nível deve ser "Diamante"
    E deve incluir sala VIP e upgrade gratuito

  Cenário: Manter nível até fim do ano qualificatório
    Dado que o cliente atingiu Ouro em março/2026
    Quando o ano qualificatório termina em dezembro/2026
    Então o nível Ouro deve ser mantido até março/2027

  Cenário: Rebaixamento por inatividade
    Dado que o cliente é Ouro
    E não acumulou milhas qualificáveis por 18 meses
    Quando o FID avalia inatividade
    Então deve rebaixar para Prata
    E deve notificar o cliente

  Cenário: Benefícios por nível Prata
    Dado que o cliente é nível Prata
    Quando consulta benefícios
    Então deve ter acúmulo 1.25x e prioridade check-in

  Cenário: Benefícios por nível Diamante
    Dado que o cliente é nível Diamante
    Quando consulta benefícios
    Então deve ter acúmulo 2x, sala VIP, upgrade grátis e 15% desconto

  Cenário: Integrar nível com Agente de Marketing
    Dado que o cliente é Diamante
    Quando o MKT segmenta campanhas
    Então deve incluir em campanhas VIP exclusivas
    E cupons exclusivos devem ser oferecidos

  Cenário: Progresso para próximo nível
    Dado que o cliente Prata tem 22.000 milhas qualificáveis
    E Ouro requer 30.000
    Quando consulta progresso
    Então deve exibir "73% para Ouro - faltam 8.000 milhas"
