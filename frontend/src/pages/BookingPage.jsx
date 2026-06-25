import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useBooking } from '../context/BookingContext';
import { criarReserva } from '../api/reservaApi';
import { formatCurrency } from '../utils/formatters';

export default function BookingPage() {
  const navigate = useNavigate();
  const { selectedFlight, pricing, search, setReservation } = useBooking();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [passageiro, setPassageiro] = useState({
    nome: 'João', sobrenome: 'Silva', cpf: '529.982.247-25', data_nascimento: '1990-01-15',
  });

  if (!selectedFlight) {
    return <div className="alert alert-info">Selecione um voo primeiro.</div>;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const reserva = await criarReserva({
        voo_ida: selectedFlight.id,
        data_ida: `${search?.data_ida || '2026-08-15'}T00:00:00`,
        origem: selectedFlight.origem,
        destino: selectedFlight.destino,
        classe: selectedFlight.classe,
        valor_total: pricing?.valor_total || selectedFlight.preco,
        passageiros: [{ ...passageiro, data_nascimento: `${passageiro.data_nascimento}T00:00:00`, tipo: 'ADT' }],
      });
      setReservation(reserva);
      navigate('/pagamento');
    } catch (err) {
      setError(err.response?.data?.detail || 'Erro ao criar reserva');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" style={{ maxWidth: 600 }}>
      <h2>Reserva — {selectedFlight.numero}</h2>
      <p style={{ margin: '1rem 0', color: '#6b7280' }}>
        Total: <strong>{formatCurrency(pricing?.valor_total || selectedFlight.preco)}</strong>
      </p>
      {error && <div className="alert alert-error">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div style={{ display: 'grid', gap: '1rem', marginBottom: '1rem' }}>
          <input placeholder="Nome" value={passageiro.nome} onChange={(e) => setPassageiro({ ...passageiro, nome: e.target.value })} required />
          <input placeholder="Sobrenome" value={passageiro.sobrenome} onChange={(e) => setPassageiro({ ...passageiro, sobrenome: e.target.value })} required />
          <input placeholder="CPF" value={passageiro.cpf} onChange={(e) => setPassageiro({ ...passageiro, cpf: e.target.value })} required />
          <input type="date" value={passageiro.data_nascimento} onChange={(e) => setPassageiro({ ...passageiro, data_nascimento: e.target.value })} required />
        </div>
        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? 'Criando reserva...' : 'Continuar para pagamento'}
        </button>
      </form>
    </div>
  );
}
