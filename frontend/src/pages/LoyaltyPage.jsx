import { useEffect, useState } from 'react';
import { saldoMilhas, nivelFidelidade } from '../api/fidelidadeApi';

export default function LoyaltyPage() {
  const [saldo, setSaldo] = useState(null);
  const [nivel, setNivel] = useState(null);
  const clienteId = 'cliente-001';

  useEffect(() => {
    saldoMilhas(clienteId).then(setSaldo);
    nivelFidelidade(clienteId).then(setNivel);
  }, []);

  return (
    <div>
      <h2>Programa de Fidelidade</h2>
      {saldo && (
        <div className="card" style={{ marginTop: '1.5rem', maxWidth: 400 }}>
          <p>Saldo: <strong>{saldo.saldo.toLocaleString()} milhas</strong></p>
          <p>Nível: <strong>{saldo.nivel}</strong></p>
        </div>
      )}
      {nivel && (
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
