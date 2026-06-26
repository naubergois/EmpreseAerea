import { useEffect, useMemo, useState } from 'react';
import { listarTestesBdd, executarTestesBdd } from '../api/qaApi';
import { useDocumentTitle } from '../hooks/useDocumentTitle';
import './BddTestsPage.css';

const STATUS_META = {
  passed: { label: 'Passou', className: 'status--passed', icon: '✓' },
  failed: { label: 'Falhou', className: 'status--failed', icon: '✕' },
  pending: { label: 'Pendente', className: 'status--pending', icon: '•' },
  skipped: { label: 'Ignorado', className: 'status--skipped', icon: '–' },
};

function StatusBadge({ status }) {
  const meta = STATUS_META[status] ?? STATUS_META.pending;
  return (
    <span className={`status-badge ${meta.className}`}>
      <span className="status-badge__icon">{meta.icon}</span>
      {meta.label}
    </span>
  );
}

function FeatureCard({ feature }) {
  const [aberto, setAberto] = useState(false);
  const contagem = feature.cenarios.reduce(
    (acc, c) => {
      acc[c.status] = (acc[c.status] ?? 0) + 1;
      return acc;
    },
    {},
  );

  return (
    <div className={`feature-card feature-card--${feature.status}`}>
      <button className="feature-card__head" onClick={() => setAberto((v) => !v)}>
        <div className="feature-card__title">
          <span className="feature-card__suite">{feature.suite}</span>
          <h3>{feature.nome}</h3>
          {feature.motivo && <p className="feature-card__motivo">{feature.motivo}</p>}
        </div>
        <div className="feature-card__meta">
          <StatusBadge status={feature.status} />
          <span className="feature-card__counts">
            {contagem.passed ? <em className="c-passed">{contagem.passed}✓</em> : null}
            {contagem.failed ? <em className="c-failed">{contagem.failed}✕</em> : null}
            {contagem.pending ? <em className="c-pending">{contagem.pending}•</em> : null}
          </span>
          <span className="feature-card__chevron">{aberto ? '▾' : '▸'}</span>
        </div>
      </button>

      {aberto && (
        <div className="feature-card__body">
          {feature.cenarios.map((cenario, i) => (
            <div key={i} className="scenario">
              <div className="scenario__head">
                <StatusBadge status={cenario.status} />
                <span className="scenario__nome">{cenario.nome}</span>
              </div>
              {cenario.motivo_falha && (
                <p className="scenario__motivo">{cenario.motivo_falha}</p>
              )}
              <ul className="scenario__passos">
                {cenario.passos.map((passo, j) => (
                  <li key={j} className={`passo passo--${passo.status}`}>
                    <span className="passo__icon">
                      {STATUS_META[passo.status]?.icon ?? '•'}
                    </span>
                    {passo.texto}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default function BddTestsPage() {
  useDocumentTitle('Testes BDD');
  const [dados, setDados] = useState(null);
  const [loading, setLoading] = useState(true);
  const [executando, setExecutando] = useState(false);
  const [erro, setErro] = useState(null);
  const [filtro, setFiltro] = useState('todos');
  const [busca, setBusca] = useState('');

  const carregar = async (run = false) => {
    setErro(null);
    if (run) setExecutando(true);
    else setLoading(true);
    try {
      const data = run ? await executarTestesBdd() : await listarTestesBdd();
      setDados(data);
    } catch (e) {
      setErro(e?.response?.data?.detail ?? e.message ?? 'Erro ao carregar testes BDD.');
    } finally {
      setLoading(false);
      setExecutando(false);
    }
  };

  useEffect(() => {
    carregar(false);
  }, []);

  const featuresFiltradas = useMemo(() => {
    if (!dados) return [];
    const termo = busca.trim().toLowerCase();
    return dados.features
      .map((f) => {
        const cenarios = f.cenarios.filter((c) => {
          const okStatus = filtro === 'todos' || c.status === filtro;
          const okBusca =
            !termo ||
            f.nome.toLowerCase().includes(termo) ||
            f.motivo.toLowerCase().includes(termo) ||
            c.nome.toLowerCase().includes(termo);
          return okStatus && okBusca;
        });
        return { ...f, cenarios };
      })
      .filter((f) => f.cenarios.length > 0);
  }, [dados, filtro, busca]);

  const resumo = dados?.resumo ?? { passed: 0, failed: 0, pending: 0, skipped: 0, total: 0 };
  const pct = resumo.total ? Math.round((resumo.passed / resumo.total) * 100) : 0;

  return (
    <div className="bdd-page">
      <div className="bdd-page__header">
        <div>
          <h1>Testes BDD</h1>
          <p className="bdd-page__sub">
            Cada cenário mostra o <strong>motivo</strong> (o que o teste valida) e se{' '}
            <strong>passou</strong> ou <strong>falhou</strong>.
          </p>
        </div>
        <button
          className="bdd-page__run"
          onClick={() => carregar(true)}
          disabled={executando || loading}
        >
          {executando ? 'Executando…' : '▶ Executar testes'}
        </button>
      </div>

      {dados?.executado_em && (
        <p className="bdd-page__timestamp">
          Última execução: {new Date(dados.executado_em).toLocaleString('pt-BR')}
          {dados.duracao_segundos != null && ` · ${dados.duracao_segundos}s`}
        </p>
      )}

      {!loading && !erro && (
        <div className="bdd-summary">
          <div className="bdd-summary__bar">
            <div className="bdd-summary__fill" style={{ width: `${pct}%` }} />
          </div>
          <div className="bdd-summary__cards">
            <div className="summary-card summary-card--total">
              <span className="summary-card__num">{resumo.total}</span>
              <span>Total</span>
            </div>
            <div className="summary-card summary-card--passed">
              <span className="summary-card__num">{resumo.passed}</span>
              <span>Passou</span>
            </div>
            <div className="summary-card summary-card--failed">
              <span className="summary-card__num">{resumo.failed}</span>
              <span>Falhou</span>
            </div>
            <div className="summary-card summary-card--pending">
              <span className="summary-card__num">{resumo.pending}</span>
              <span>Pendente</span>
            </div>
          </div>
        </div>
      )}

      <div className="bdd-toolbar">
        <input
          className="bdd-toolbar__search"
          placeholder="Buscar por funcionalidade, motivo ou cenário…"
          value={busca}
          onChange={(e) => setBusca(e.target.value)}
        />
        <div className="bdd-toolbar__filters">
          {['todos', 'passed', 'failed', 'pending'].map((f) => (
            <button
              key={f}
              className={`filter-chip ${filtro === f ? 'filter-chip--active' : ''}`}
              onClick={() => setFiltro(f)}
            >
              {f === 'todos' ? 'Todos' : STATUS_META[f].label}
            </button>
          ))}
        </div>
      </div>

      {loading && <div className="bdd-state">Carregando testes BDD…</div>}
      {erro && <div className="bdd-state bdd-state--error">{erro}</div>}
      {!loading && !erro && featuresFiltradas.length === 0 && (
        <div className="bdd-state">Nenhum teste encontrado para o filtro atual.</div>
      )}

      <div className="bdd-list">
        {featuresFiltradas.map((feature, i) => (
          <FeatureCard key={`${feature.arquivo}-${i}`} feature={feature} />
        ))}
      </div>
    </div>
  );
}
