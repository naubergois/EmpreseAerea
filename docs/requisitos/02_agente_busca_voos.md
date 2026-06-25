# Requisitos — Agente de Busca de Voos (BUS)

> **Responsabilidade:** Pesquisar voos em múltiplas fontes (GDS, NDC, inventário próprio) e retornar opções filtradas, ordenadas e enriquecidas.

---

## Requisitos Funcionais

| ID | Requisito | Prioridade |
|----|-----------|------------|
| BUS-RF01 | Deve buscar voos por origem, destino e data (ida, ida/volta, multi-destino) | Alta |
| BUS-RF02 | Deve suportar tipos de viagem: somente ida, ida e volta, multi-trecho | Alta |
| BUS-RF03 | Deve suportar classes: econômica, premium economy, executiva, primeira | Alta |
| BUS-RF04 | Deve filtrar por número de escalas (direto, máx. 1, máx. 2) | Alta |
| BUS-RF05 | Deve filtrar por companhia aérea (única ou múltipla) | Alta |
| BUS-RF06 | Deve filtrar por faixa de preço, horário de partida e duração máxima | Alta |
| BUS-RF07 | Deve ordenar por preço, duração, horário de partida ou relevância | Alta |
| BUS-RF08 | Deve consultar simultaneamente Amadeus, Sabre e Travelport | Alta |
| BUS-RF09 | Deve cachear resultados por 15 minutos com invalidação por rota | Alta |
| BUS-RF10 | Deve resolver nomes de cidade para códigos IATA de aeroportos | Alta |
| BUS-RF11 | Deve verificar disponibilidade em tempo real antes de exibir resultado | Alta |
| BUS-RF12 | Deve suportar busca flexível por ±3 dias da data desejada | Média |
| BUS-RF13 | Deve exibir franquia de bagagem e tempo total incluindo conexões | Alta |
| BUS-RF14 | Deve suportar busca para adultos, crianças (CHD), bebês (INF) | Alta |
| BUS-RF15 | Deve filtrar voos compatíveis com necessidades especiais (cadeirante) | Alta |
| BUS-RF16 | Deve sugerir datas e rotas alternativas quando não houver resultados | Média |
| BUS-RF17 | Deve registrar buscas sem resultado para análise de demanda (MKT) | Média |
| BUS-RF18 | Deve indicar voos codeshare com operador real | Média |

---

## Requisitos Não-Funcionais

| ID | Requisito | Métrica |
|----|-----------|---------|
| BUS-RNF01 | Tempo de resposta (cache miss) | < 3s |
| BUS-RNF02 | Taxa de cache hit | > 70% |
| BUS-RNF03 | Buscas simultâneas suportadas | > 5.000 |
| BUS-RNF04 | Disponibilidade | 99.9% |
