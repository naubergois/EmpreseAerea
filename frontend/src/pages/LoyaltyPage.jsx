import { useEffect, useState } from 'react';
import { saldoMilhas, nivelFidelidade } from '../api/fidelidadeApi';
import { useDocumentTitle } from '../hooks/useDocumentTitle';

export default function LoyaltyPage() {
  useDocumentTitle('Programa de fidelidade');
  const [saldo, setSaldo] = useState(null);
  const [nivel, setNivel] = useState(null);
  const [loading, setLoading] = useState(true);
  const clienteId = 'cliente-001';

  useEffect(() => {
    Promise.all([saldoMilhas(clienteId), nivelFidelidade(clienteId)])
      .then(([s, n]) => { setSaldo(s); setNivel(n); })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      <h2>Programa de Fidelidade</h2>

      {loading && (
        <div aria-busy="true" style={{ marginTop: '1.5rem', maxWidth: 400 }}>
          <div className="skeleton" style={{ height: 96, marginBottom: '1rem' }} />
          <div className="skeleton" style={{ height: 120 }} />
        </div>
      )}

      {!loading && saldo && (
        <div className="card" style={{ marginTop: '1.5rem', maxWidth: 400 }}>
          <p>Saldo: <strong>{saldo.saldo.toLocaleString('pt-BR')} milhas</strong></p>
          <p>Nível: <strong>{saldo.nivel}</strong></p>
        </div>
      )}
      {!loading && nivel && (
        <div className="card" style={{ marginTop: '1rem', maxWidth: 400 }}>
          <p>Progresso para {nivel.proximo_nivel || 'máximo'}: {nivel.progresso_pct}%</p>
          <ul style={{ marginTop: '0.5rem', paddingLeft: '1.25rem' }}>
            {nivel.beneficios.map((b) => <li key={b}>{b}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
}
