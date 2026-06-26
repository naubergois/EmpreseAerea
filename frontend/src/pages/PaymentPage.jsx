import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useBooking } from '../context/BookingContext';
import { pagarCartao } from '../api/pagamentoApi';
import { iniciarPipeline } from '../api/reservaApi';
import { useDocumentTitle } from '../hooks/useDocumentTitle';
import { formatCurrency, maskCard, maskExpiry, maskCVV } from '../utils/formatters';

export default function PaymentPage() {
  useDocumentTitle('Pagamento');
  const navigate = useNavigate();
  const { reservation, selectedFlight, search, setConfirmation, setPayment } = useBooking();
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState(null);
  const [metodo, setMetodo] = useState('cartao');
  const [cartao, setCartao] = useState({
    numero: '4111 1111 1111 1111', nome: 'JOAO SILVA', validade: '12/28', cvv: '123',
  });

  if (!reservation) {
    return <div className="alert alert-info">Crie uma reserva primeiro.</div>;
  }

  const updateCartao = (campo, mask) => (e) =>
    setCartao({ ...cartao, [campo]: mask ? mask(e.target.value) : e.target.value });

  const handlePay = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErro(null);
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
          numero_cartao: cartao.numero.replace(/\s/g, ''),
          nome_titular: cartao.nome,
          validade: cartao.validade,
          cvv: cartao.cvv,
        });
        setPayment(pag);
        setConfirmation({ pnr: reservation.pnr, pagamento: pag });
      }
      navigate('/confirmacao');
    } catch (err) {
      setErro(err.response?.data?.detail?.message || err.response?.data?.detail || 'Erro no pagamento');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" style={{ maxWidth: 520, margin: '0 auto' }}>
      <h2>Pagamento</h2>
      <p>PNR: <strong>{reservation.pnr}</strong></p>
      <p>Valor: <strong>{formatCurrency(reservation.valor_total)}</strong></p>

      {erro && <div className="alert alert-error" role="alert" style={{ marginTop: '1rem' }}>{erro}</div>}

      <form onSubmit={handlePay}>
        <fieldset style={{ border: 'none', margin: '1.5rem 0' }}>
          <legend style={{ fontWeight: 600, marginBottom: '0.5rem' }}>Forma de pagamento</legend>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: 400, marginBottom: '0.5rem' }}>
            <input type="radio" name="metodo" style={{ width: 'auto' }} checked={metodo === 'cartao'} onChange={() => setMetodo('cartao')} />
            Cartão de crédito
          </label>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: 400 }}>
            <input type="radio" name="metodo" style={{ width: 'auto' }} checked={metodo === 'pipeline'} onChange={() => setMetodo('pipeline')} />
            Pipeline completo (ORC)
          </label>
        </fieldset>

        {metodo === 'cartao' && (
          <div className="stack" style={{ marginBottom: '1.5rem' }}>
            <div className="field">
              <label htmlFor="card-numero">Número do cartão</label>
              <input id="card-numero" inputMode="numeric" autoComplete="cc-number" value={cartao.numero} onChange={updateCartao('numero', maskCard)} placeholder="0000 0000 0000 0000" required />
            </div>
            <div className="field">
              <label htmlFor="card-nome">Nome do titular</label>
              <input id="card-nome" autoComplete="cc-name" value={cartao.nome} onChange={updateCartao('nome')} required />
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div className="field">
                <label htmlFor="card-validade">Validade</label>
                <input id="card-validade" inputMode="numeric" autoComplete="cc-exp" value={cartao.validade} onChange={updateCartao('validade', maskExpiry)} placeholder="MM/AA" required />
              </div>
              <div className="field">
                <label htmlFor="card-cvv">CVV</label>
                <input id="card-cvv" inputMode="numeric" autoComplete="cc-csc" value={cartao.cvv} onChange={updateCartao('cvv', maskCVV)} placeholder="123" required />
              </div>
            </div>
          </div>
        )}

        <button type="submit" className="btn-primary btn-block" disabled={loading}>
          {loading ? <><span className="spinner" /> Processando...</> : 'Pagar agora'}
        </button>
      </form>
    </div>
  );
}
