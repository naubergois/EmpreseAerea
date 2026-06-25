# language: pt
Funcionalidade: Resiliência e Circuit Breaker
  Como agente orquestrador
  Eu quero implementar padrões de resiliência
  Para manter o sistema operando mesmo com falhas em agentes individuais

  Cenário: Ativar circuit breaker quando agente está indisponível
    Dado que o Agente de Busca de Voos falhou nas últimas 5 requisições consecutivas
    Quando uma nova requisição de busca é recebida
    Então o circuit breaker do Agente de Busca deve ser ativado
    E a requisição deve retornar mensagem de indisponibilidade temporária
    E o Agente de Notificações deve alertar a equipe de operações
    E o circuit breaker deve testar reconexão após 30 segundos

  Cenário: Retry com backoff exponencial em falha temporária
    Dado que o Agente de Pagamento retornou erro 503 (timeout)
    Quando o Orquestrador tenta retry
    Então a primeira tentativa deve ocorrer após 1 segundo
    E a segunda tentativa deve ocorrer após 2 segundos
    E a terceira tentativa deve ocorrer após 4 segundos
    E após 3 falhas consecutivas o circuit breaker deve ser ativado

  Cenário: Escalação para atendente humano após falhas repetidas
    Dado que o pipeline de venda falhou 3 vezes para o cliente "João Silva"
    E as falhas foram: timeout, erro de pagamento, erro de emissão
    Quando a terceira falha é registrada
    Então o Orquestrador deve escalar para atendente humano
    E todo o contexto da sessão deve ser transferido
    E o histórico de erros deve ser anexado
    E o cliente deve ser informado que será atendido por um humano

  Cenário: Paralelizar busca em múltiplos GDS
    Dado que o cliente busca voos de "GRU" para "LHR"
    Quando o Orquestrador envia a busca
    Então as consultas para Amadeus, Sabre e Travelport devem ser paralelas
    E o resultado deve consolidar respostas de todos os GDS
    E o tempo total deve ser próximo ao do GDS mais lento

  Cenário: Paralelizar acúmulo de milhas e emissão de notificação
    Dado que o pagamento foi confirmado e o bilhete foi emitido
    Quando o Orquestrador executa as etapas pós-emissão
    Então o acúmulo de milhas e o envio de notificações devem ser paralelos
    E ambas as tarefas devem completar independentemente
    E falha no acúmulo de milhas não deve bloquear a notificação

  Cenário: Recuperar de circuit breaker após agente voltar
    Dado que o circuit breaker do Agente de Busca está ativado há 30 segundos
    Quando o Orquestrador envia uma requisição de teste (half-open)
    E o Agente de Busca responde com sucesso
    Então o circuit breaker deve ser desativado
    E as requisições devem voltar a ser roteadas normalmente
    E o contador de falhas deve ser resetado

  Cenário: Manter circuit breaker após falha no teste de reconexão
    Dado que o circuit breaker do Agente de Pagamento está ativado
    Quando o teste de reconexão é executado
    E o Agente de Pagamento continua indisponível
    Então o circuit breaker deve permanecer ativado
    E o próximo teste deve ocorrer em 60 segundos (dobro do anterior)
    E o alerta de operações deve ser atualizado

  Cenário: Degradação graciosa quando Agente de Fidelidade falha
    Dado que o pipeline de venda está em execução
    E o Agente de Fidelidade está indisponível
    Quando o pagamento é confirmado e o bilhete é emitido
    Então o acúmulo de milhas deve ser enfileirado para processamento posterior
    E o bilhete deve ser entregue normalmente ao cliente
    E o pipeline não deve falhar por indisponibilidade do Agente de Fidelidade
    E um job assíncrono deve processar as milhas quando o agente voltar

  Cenário: Health check periódico de todos os agentes
    Dado que o Orquestrador monitora 9 agentes
    Quando o health check periódico é executado a cada 15 segundos
    Então cada agente deve responder ao ping em menos de 500ms
    E o status de cada agente deve ser atualizado no dashboard
    E agentes que não respondem devem ser marcados como "degraded"
    E a equipe de operações deve ser alertada sobre agentes degradados

  Cenário: Detectar deadlock entre Agente de Reserva e Agente de Pagamento
    Dado que o Agente de Reserva aguarda confirmação do Pagamento
    E o Agente de Pagamento aguarda dados da Reserva
    E ambos estão bloqueados há mais de 10 segundos
    Quando o detector de deadlock do Orquestrador identifica o ciclo
    Então um dos agentes deve ter sua operação cancelada
    E o pipeline deve ser reiniciado do zero
    E o incidente "deadlock_detectado" deve ser registrado
