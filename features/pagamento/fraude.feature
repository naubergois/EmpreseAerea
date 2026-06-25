# language: pt
Funcionalidade: Prevenção a Fraude
  Como agente de pagamento
  Eu quero detectar e bloquear transações fraudulentas
  Para proteger a empresa e os clientes

  Cenário: Bloquear transação com score de fraude alto
    Dado que o motor antifraude calculou score 95/100
    E o limite de aprovação automática é 70
    Quando o PAG avalia a transação
    Então o pagamento deve ser recusado
    E o motivo deve ser "suspeita_fraude"
    E a tentativa deve ser registrada para auditoria

  Cenário: Aprovar transação com score baixo
    Dado que o score de fraude é 15/100
    E o cliente é recorrente com histórico positivo
    Quando o PAG avalia a transação
    Então o pagamento deve ser aprovado automaticamente

  Cenário: Revisão manual para score intermediário
    Dado que o score de fraude é 55/100
    Quando o PAG avalia a transação
    Então a transação deve ir para fila de revisão manual
    E o cliente deve ser informado "pagamento_em_analise"

  Cenário: Detectar múltiplas tentativas com cartões diferentes
    Dado que o mesmo IP tentou 5 cartões em 10 minutos
    Quando o PAG detecta o padrão
    Então deve bloquear novas tentativas por 1 hora
    E deve alertar equipe de fraude

  Cenário: Bloquear transação de país em lista de sanções
    Dado que o cartão é emitido em país sancionado
    Quando o PAG valida a transação
    Então deve recusar com erro "pais_bloqueado"

  Cenário: Detectar velocity check - muitas compras em pouco tempo
    Dado que o cliente comprou 4 passagens em 1 hora
    E o limite é 3 compras por hora
    Quando a 4ª compra é tentada
    Então deve bloquear e solicitar verificação adicional

  Cenário: Verificar consistência geográfica IP vs. cartão
    Dado que o IP é do Brasil
    E o cartão é emitido no Brasil
    E o destino do voo é nacional
    Quando o PAG analisa
    Então o score de fraude deve ser reduzido

  Cenário: Alertar sobre IP de VPN/proxy conhecido
    Dado que o IP está em lista de VPN/proxy
    Quando o PAG analisa a transação
    Então o score de fraude deve ser aumentado em 20 pontos

  Cenário: Whitelist de clientes VIP
    Dado que o cliente é nível Diamante com 50+ compras
    Quando o score de fraude é 60/100
    Então a transação deve ser aprovada com flag de revisão posterior

  Cenário: Registrar tentativa de fraude para machine learning
    Dado que uma transação foi bloqueada por fraude
    Quando o bloqueio é confirmado
    Então os dados devem alimentar modelo de ML
    E deve ser anonimizado conforme LGPD
