# language: pt
Funcionalidade: Segmentação de Clientes
  Como agente de marketing
  Eu quero segmentar a base de clientes
  Para enviar ofertas relevantes e personalizadas

  Cenário: Segmentar por comportamento de busca
    Dado que o cliente buscou GRU-LIS 5 vezes sem comprar
    Quando o MKT executa segmentação comportamental
    Então o cliente deve entrar no segmento "interesse_europa"
    E deve receber ofertas para destinos europeus

  Cenário: Segmentar por nível de fidelidade
    Dado que existem clientes Bronze, Prata, Ouro e Diamante
    Quando o MKT segmenta por fidelidade
    Então cada nível deve ter segmento independente
    E ofertas VIP devem ser exclusivas para Ouro e Diamante

  Cenário: Segmentar clientes inativos
    Dado que o cliente não compra há mais de 12 meses
    Quando o MKT identifica inativos
    Então deve entrar no segmento "reativacao"
    E deve receber campanha de reativação

  Cenário: Segmentar por valor de compra (RFM)
    Dado que o cliente comprou R$ 15.000 em 12 meses
    Quando o MKT calcula RFM
    Então deve ser classificado como "alto valor"
    E deve receber tratamento premium

  Cenário: Segmentar por canal preferido
    Dado que o cliente abre e-mails mas ignora SMS
    Quando o MKT analisa preferências
    Então o canal preferido deve ser "email"
    E SMS não deve ser usado para este cliente

  Cenário: Segmentar por sazonalidade de viagem
    Dado que o cliente sempre viaja em julho
    Quando o MKT analisa histórico
    Então deve entrar no segmento "ferias_julho"
    E campanhas devem ser antecipadas em maio/junho

  Cenário: Excluir clientes com opt-out da segmentação promocional
    Dado que o cliente desativou marketing
    Quando qualquer segmentação é executada
    Então o cliente não deve aparecer em campanhas promocionais
    E deve permanecer em segmentos transacionais

  Cenário: Segmentar por destino favorito
    Dado que 80% das compras do cliente são para Miami
    Quando o MKT perfila o cliente
    Então o destino favorito deve ser "MIA"
    E ofertas para Miami devem ter prioridade

  Cenário: Criar segmento dinâmico com regras combinadas
    Dado que o segmento exige: nível Ouro + busca internacional + inativo 6 meses
    Quando o MKT avalia o cliente "Ana"
    E Ana é Ouro, buscou GRU-CDG e está inativa há 8 meses
    Então Ana deve entrar no segmento dinâmico

  Cenário: Atualizar segmentos em tempo real após compra
    Dado que o cliente estava no segmento "carrinho_abandonado"
    Quando o cliente completa uma compra
    Então deve ser removido do segmento de abandono
    E deve entrar no segmento "cliente_ativo"
