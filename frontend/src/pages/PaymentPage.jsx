import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useBooking } from '../context/BookingContext';
import { pagarCartao } from '../api/pagamentoApi';
import { iniciarPipeline } from '../api/reservaApi';
import { formatCurrency } from '../utils/formatters';

export default function PaymentPage() {
  const navigate = useNavigate();
  const { reservation, selectedFlight, search, setConfirmation, setPayment } = useBooking();
  const [loading, setLoading] = useState(false);
  const [metodo, setMetodo] = useState('cartao');

  if (!reservation) {
    return <div className="alert alert-info">Crie uma reserva primeiro.</div>;
  }

  const handlePay = async () => {
    setLoading(true);
    try {
      if (metodo === 'pipeline') {
        const result = await iniciarPipeline({
          origem: selectedFlight?.origem || 'GRU',
          destino: selectedFlight?.destino || 'GIG',
          data_ida: `${search?.data_ida || '2026-08-15'}T00:00:00`,
          voo_id: selectedFlight?.id,
          preco_base: selectedFlight?.preco,
        });
        setConfirmation(result);
      } else {
        const pag = await pagarCartao({
          pnr: reservation.pnr,
          valor: reservation.valor_total,
          numero_cartao: '4111111111111111',
          nome_titular: 'JOAO SILVA',
          validade: '12/28',
          cvv: '123',
        });
        setPayment(pag);
        setConfirmation({ pnr: reservation.pnr, pagamento: pag });
      }
      navigate('/confirmacao');
    } catch (err) {
      alert(err.response?.data?.detail?.message || 'Erro no pagamento');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" style={{ maxWidth: 500 }}>
      <h2>Pagamento</h2>
      <p>PNR: <strong>{reservation.pnr}</strong></p>
      <p>Valor: <strong>{formatCurrency(reservation.valor_total)}</strong></p>
      <div style={{ margin: '1.5rem 0' }}>
        <label style={{ display: 'block', marginBottom: '0.5rem' }}>
          <input type="radio" checked={metodo === 'cartao'} onChange={() => setMetodo('cartao')} /> Cartão de crédito
        </label>
        <label style={{ display: 'block' }}>
          <input type="radio" checked={metodo === 'pipeline'} onChange={() => setMetodo('pipeline')} /> Pipeline completo (ORC)
        </label>
      </div>
      <button className="btn-primary" onClick={handlePay} disabled={loading}>
        {loading ? 'Processando...' : 'Pagar agora'}
      </button>
    </div>
  );
}
