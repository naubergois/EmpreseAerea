# Análise de UX/UI e Backlog de Melhorias — SkyAgent (Frontend)

> Avaliação heurística do frontend da plataforma SkyAgent (SPA **React + Vite**), feita por um
> **agente avaliador de UX/UI**. O objetivo é apontar problemas de usabilidade, acessibilidade,
> consistência visual, responsividade e fluxo, com melhorias **priorizadas e acionáveis**.
>
> Data da avaliação: **2026-06-26** · Escopo: `frontend/src/**` · Método: Heurísticas de Nielsen + WCAG 2.1 AA

---

## 1. Resumo Executivo

O frontend cobre o funil completo de venda (busca → resultados → reserva → pagamento → confirmação)
mais Fidelidade, Suporte (chat com IA) e um painel de Testes BDD. O design base é limpo, com um
**design token** inicial bem definido em `global.css` (`:root` com cores, raio e sombra) e bons
microdetalhes (hover nos cards de voo, página de Testes BDD bem construída).

Porém, o produto ainda tem **lacunas relevantes de acessibilidade, consistência e fluxo** que
impactam diretamente conversão e confiança do usuário.

| Dimensão | Nota (0–5) | Síntese |
|----------|:----------:|---------|
| Hierarquia visual / estética | 3.5 | Base sólida, mas sem polimento e sem imagens/ilustração |
| Consistência / design system | 2.0 | Tokens existem mas são ignorados; muito estilo inline e hex duplicado |
| Acessibilidade (WCAG 2.1 AA) | 1.5 | Labels não associados, card clicável sem teclado, foco invisível, contraste falho |
| Responsividade (mobile) | 2.0 | Apenas 1 media query; menu e formulário quebram no celular |
| Fluxo / feedback | 2.5 | Sem indicador de etapas, `alert()` nativo, validação ausente, dados de demo fixos |

**Top 5 prioridades (maior impacto / menor esforço):**

1. **Acessibilidade de formulários e do card de voo** (labels, foco, teclado) — risco legal e de conversão.
2. **Indicador de progresso do funil** (Busca → Reserva → Pagamento → Confirmação).
3. **Substituir `alert()` por feedback inline** e padronizar mensagens de erro/sucesso.
4. **Tornar o layout realmente responsivo** (menu, grid da busca, tipografia fluida).
5. **Eliminar estilos inline** migrando para o design system existente (`global.css`).

---

## 2. Inventário de Telas Avaliadas

| Rota | Arquivo | Função | Estilo |
|------|---------|--------|--------|
| `/` | `pages/HomePage.jsx` | Busca de voos | Inline |
| `/resultados` | `pages/SearchResultsPage.jsx` + `components/voos/*` | Lista de voos | CSS file |
| `/reserva` | `pages/BookingPage.jsx` | Dados do passageiro | Inline |
| `/pagamento` | `pages/PaymentPage.jsx` | Pagamento | Inline |
| `/confirmacao` | `pages/ConfirmationPage.jsx` | Confirmação | Inline |
| `/fidelidade` | `pages/LoyaltyPage.jsx` | Milhas e nível | Inline |
| `/suporte` | `pages/SupportPage.jsx` | Chat de atendimento | Inline |
| `/testes` | `pages/BddTestsPage.jsx` | Painel BDD | CSS file (referência de qualidade) |
| layout | `components/layout/Header.jsx`, `Footer.jsx` | Navegação | CSS / inline |

---

## 3. Problemas por Categoria

### 3.1 Acessibilidade (WCAG 2.1 AA) — **Prioridade ALTA**

| # | Problema | Onde | Critério WCAG | Severidade |
|---|----------|------|----------------|:----------:|
| A1 | `<label>` não associado ao `<input>` (sem `htmlFor`/`id`); leitor de tela não anuncia o campo | `HomePage`, `BookingPage` | 1.3.1, 4.1.2 | Alta |
| A2 | Card de voo é `<div onClick>` — não focável, não acionável por teclado, sem `role`/`tabIndex` | `FlightCard.jsx` | 2.1.1, 4.1.2 | Alta |
| A3 | Sem estilo de foco visível (`:focus-visible`) em botões/inputs/links | `global.css` | 2.4.7 | Alta |
| A4 | Contraste insuficiente: texto verde `#00a86b` 0.75rem ("Bagagem inclusa") sobre branco ≈ 2.8:1 | `FlightCard.css` | 1.4.3 | Média |
| A5 | Histórico do chat sem `role="log"`/`aria-live="polite"`; novas mensagens não são anunciadas | `SupportPage.jsx` | 4.1.3 | Média |
| A6 | Ícones puramente visuais (✈, ✅, ▶) sem `aria-hidden`/texto alternativo | `Header`, `Confirmation`, `BddTests` | 1.1.1 | Baixa |
| A7 | Sem *skip link* ("pular para o conteúdo") nem `<main>` referenciável | `App.jsx` | 2.4.1 | Baixa |
| A8 | Inputs sem `inputMode`/`autoComplete` (CPF, cartão, datas) | `BookingPage`, `PaymentPage` | 1.3.5 | Baixa |

### 3.2 Consistência e Design System — **Prioridade ALTA**

- **C1 — Estilos inline em massa.** A maioria das páginas usa `style={{...}}` com hex hardcoded
  (`#6b7280`, `#0066cc`, `#e5e7eb`) em vez das variáveis já definidas em `:root`. Isso quebra a
  fonte única de verdade e dificulta tema/manutenção.
- **C2 — Tokens subutilizados.** `--color-muted`, `--radius`, `--shadow` existem mas raramente são
  usados; valores são reescritos manualmente.
- **C3 — `.btn-outline` definido e nunca usado**; falta sistema de variantes/tamanhos de botão.
- **C4 — Sem componentes reutilizáveis** de `Input`, `Field` (label+input+erro), `Button`, `PageTitle`.
  Cada página reimplementa.
- **C5 — Escala tipográfica ad-hoc** (`2.5rem`, `1.5rem`, `0.875rem`, `0.75rem` espalhados) sem
  tokens (`--text-sm`, `--text-lg`...).

### 3.3 Responsividade — **Prioridade ALTA**

- **R1 — Menu não responsivo.** `Header.__nav` é um flex fixo; em telas estreitas os 4 links
  competem com o logo. Falta *hamburger*/menu colapsável.
- **R2 — Grid da busca fixo em `1fr 1fr`** (`HomePage`) não colapsa para 1 coluna no mobile.
- **R3 — Tipografia não fluida.** `h1` fixo em `2.5rem`; usar `clamp()`.
- **R4 — Apenas uma media query** em todo o app (`FlightCard.css`). Demais telas não foram
  testadas/ajustadas para < 768px.

### 3.4 Fluxo, Feedback e Conteúdo — **Prioridade MÉDIA**

- **F1 — Sem indicador de etapas** do funil de compra (4 passos). O usuário não sabe onde está
  nem quanto falta. Forte impacto em conversão.
- **F2 — `alert()` nativo** para erro de pagamento (`PaymentPage`) é destoante e bloqueante;
  deveria usar `.alert-error` como o resto do app.
- **F3 — Ausência de validação/máscara** em CPF, cartão, validade e CVV; sem feedback de formato.
- **F4 — Dados de demonstração fixos** pré-preenchidos (origem `GRU`, CPF `529.982...`, cartão
  `4111...`). Aceitável em demo, mas precisa ser claramente separado do build de produção.
- **F5 — Busca limitada:** só ida (sem volta), passageiros fixos em 1 (campo `adultos` existe no
  estado mas não tem UI), sem *autocomplete* de aeroporto (texto IATA cru), e `origem`/`destino`
  não são convertidos para maiúsculas (o chat já faz isso para o PNR — inconsistente).
- **F6 — Data padrão fixa** `2026-08-15` pode cair no passado; usar data dinâmica e bloquear datas passadas (`min`).
- **F7 — `ConfirmationPage` não protege contra acesso direto** sem dados (outras páginas usam guard);
  pode renderizar confirmação vazia.
- **F8 — Resultados sem resumo/edição da busca** nem botão "refazer busca"/"tentar novamente" no erro.
- **F9 — Estados de carregamento são texto simples** ("Buscando...", "Digitando..."); faltam
  *skeletons*/spinner e `aria-busy`.
- **F10 — Navegação sem item ativo.** Usa `Link` em vez de `NavLink`; o usuário não vê em qual
  seção está.

### 3.5 Estética, Branding e SEO — **Prioridade BAIXA**

- **E1 — Hero sem apelo visual** (sem imagem/ilustração/gradiente); apenas título e form.
- **E2 — Sem favicon, meta description, Open Graph** ou `<title>` por página (SPA com 1 título só).
- **E3 — Footer e estados vazios genéricos**; oportunidade para microcopy mais acolhedor.
- **E4 — Logo em emoji** (✈) — frágil para identidade de marca; considerar SVG.

---

## 4. Backlog Priorizado (esforço × impacto)

Legenda de esforço: **P** pequeno (≤ meio dia) · **M** médio (1–2 dias) · **G** grande (> 2 dias).

### Sprint 1 — Acessibilidade & feedback (alto impacto, baixo esforço)

| ID | Ação | Esforço | Itens |
|----|------|:-------:|-------|
| S1.1 | Associar labels (`htmlFor`/`id`) em todos os formulários | P | A1 |
| S1.2 | Tornar `FlightCard` um `<button>`/`role="button"` com `tabIndex` e `onKeyDown` (Enter/Espaço) | P | A2 |
| S1.3 | Adicionar `:focus-visible` global (outline visível) em botões, links e inputs | P | A3 |
| S1.4 | Corrigir contraste do texto de bagagem e demais cinzas pequenos | P | A4 |
| S1.5 | Substituir `alert()` por mensagem `.alert-error` inline na `PaymentPage` | P | F2 |
| S1.6 | `aria-live="polite"` + `role="log"` no histórico do chat | P | A5 |

### Sprint 2 — Fluxo do funil & responsividade

| ID | Ação | Esforço | Itens |
|----|------|:-------:|-------|
| S2.1 | Componente `Stepper` (Busca → Reserva → Pagamento → Confirmação) | M | F1 |
| S2.2 | Menu responsivo (hamburger) e grid de busca colapsável + tipografia `clamp()` | M | R1, R2, R3 |
| S2.3 | `NavLink` com estado ativo | P | F10 |
| S2.4 | Guard de dados na `ConfirmationPage`; resumo + "refazer busca" nos resultados | P | F7, F8 |
| S2.5 | Skeletons/spinner com `aria-busy` nos estados de loading | M | F9 |

### Sprint 3 — Inputs inteligentes & design system

| ID | Ação | Esforço | Itens |
|----|------|:-------:|-------|
| S3.1 | Validação + máscara de CPF/cartão/validade/CVV; `inputMode`/`autoComplete` | M | F3, A8 |
| S3.2 | Autocomplete de aeroporto e *uppercase* de IATA; campo de passageiros; toggle ida/volta | G | F5 |
| S3.3 | Data dinâmica com `min` (sem datas passadas) | P | F6 |
| S3.4 | Componentes reutilizáveis `Field`/`Input`/`Button` e migração dos estilos inline para classes/tokens | G | C1–C5 |

### Sprint 4 — Polimento, branding & SEO

| ID | Ação | Esforço | Itens |
|----|------|:-------:|-------|
| S4.1 | Hero com imagem/ilustração e CTA reforçado | M | E1 |
| S4.2 | Favicon, meta description, Open Graph, título por página (ex.: `react-helmet`) | P | E2 |
| S4.3 | Logo SVG, microcopy de estados vazios, footer enriquecido | M | E3, E4 |
| S4.4 | Skip link + landmarks ARIA | P | A6, A7 |

---

## 5. Exemplos de Correção (amostras acionáveis)

### 5.1 Card de voo acessível por teclado (`FlightCard.jsx`)

Hoje o card captura clique num `<div>`, sem suporte a teclado:

```4:6:frontend/src/components/voos/FlightCard.jsx
export default function FlightCard({ flight, onSelect }) {
  return (
    <div className="flight-card" onClick={() => onSelect?.(flight)}>
```

Sugestão (tornar focável e acionável por Enter/Espaço):

```jsx
<div
  className="flight-card"
  role="button"
  tabIndex={0}
  onClick={() => onSelect?.(flight)}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      onSelect?.(flight);
    }
  }}
>
```

### 5.2 Label associado ao input (`HomePage.jsx`)

```27:30:frontend/src/pages/HomePage.jsx
          <div>
            <label>Origem</label>
            <input value={form.origem} onChange={(e) => setForm({ ...form, origem: e.target.value })} placeholder="GRU" />
          </div>
```

Sugestão:

```jsx
<div>
  <label htmlFor="origem">Origem</label>
  <input
    id="origem"
    autoComplete="off"
    value={form.origem}
    onChange={(e) => setForm({ ...form, origem: e.target.value.toUpperCase() })}
    placeholder="GRU"
  />
</div>
```

### 5.3 Foco visível global (`global.css`)

```css
:focus-visible {
  outline: 3px solid var(--color-primary);
  outline-offset: 2px;
  border-radius: 6px;
}
```

### 5.4 Erro de pagamento inline em vez de `alert()` (`PaymentPage.jsx`)

```43:44:frontend/src/pages/PaymentPage.jsx
    } catch (err) {
      alert(err.response?.data?.detail?.message || 'Erro no pagamento');
```

Substituir por um estado `erro` renderizado com `<div className="alert alert-error">{erro}</div>`,
mantendo consistência com o restante do app.

---

## 6. Métricas Sugeridas para Acompanhamento

| Métrica | Como medir | Meta |
|---------|------------|------|
| Acessibilidade automatizada | Lighthouse / axe-core no CI | ≥ 90 |
| Conversão do funil | Eventos por etapa (Busca→Confirmação) | Baseline + acompanhamento |
| Abandono no formulário de reserva | % que sai sem submeter | Reduzir |
| Erros de validação visíveis | Eventos de erro de formulário | Reduzir |
| Usabilidade mobile | Lighthouse mobile + teste em 360px | ≥ 90 |

---

## 7. Conclusão

A base do SkyAgent é boa (tokens, hover, página BDD), mas a **experiência de produção** exige
um esforço focado em **acessibilidade**, **consistência via design system** e **clareza do funil
de compra**. As correções da Sprint 1 são de baixo esforço e alto retorno, e devem ser priorizadas.
A médio prazo, consolidar componentes reutilizáveis e remover os estilos inline reduzirá o custo
de manutenção e elevará a qualidade percebida.
