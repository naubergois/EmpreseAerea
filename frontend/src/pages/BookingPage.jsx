import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useBooking } from '../context/BookingContext';
import { criarReserva } from '../api/reservaApi';
import { useDocumentTitle } from '../hooks/useDocumentTitle';
import { formatCurrency, maskCPF, isValidCPF, todayISO } from '../utils/formatters';

export default function BookingPage() {
  useDocumentTitle('Dados do passageiro');
  const navigate = useNavigate();
  const { selectedFlight, pricing, search, setReservation } = useBooking();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [cpfErro, setCpfErro] = useState(null);
  const [passageiro, setPassageiro] = useState({
    nome: 'João', sobrenome: 'Silva', cpf: '529.982.247-25', data_nascimento: '1990-01-15',
  });

  if (!selectedFlight) {
    return <div className="alert alert-info">Selecione um voo primeiro.</div>;
  }

  const update = (campo) => (e) => setPassageiro({ ...passageiro, [campo]: e.target.value });
  const handleCpf = (e) => {
    const masked = maskCPF(e.target.value);
    setPassageiro({ ...passageiro, cpf: masked });
    if (cpfErro) setCpfErro(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!isValidCPF(passageiro.cpf)) {
      setCpfErro('CPF inválido. Verifique os dígitos.');
      return;
    }
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
    <div className="card" style={{ maxWidth: 600, margin: '0 auto' }}>
      <h2>Reserva — {selectedFlight.numero}</h2>
      <p className="text-muted" style={{ margin: '1rem 0' }}>
        Total: <strong>{formatCurrency(pricing?.valor_total || selectedFlight.preco)}</strong>
      </p>
      {error && <div className="alert alert-error" role="alert">{error}</div>}

      <form onSubmit={handleSubmit} noValidate>
        <div className="stack" style={{ marginBottom: '1rem' }}>
          <div className="field">
            <label htmlFor="nome">Nome</label>
            <input id="nome" autoComplete="given-name" value={passageiro.nome} onChange={update('nome')} required />
          </div>
          <div className="field">
            <label htmlFor="sobrenome">Sobrenome</label>
            <input id="sobrenome" autoComplete="family-name" value={passageiro.sobrenome} onChange={update('sobrenome')} required />
          </div>
          <div className="field">
            <label htmlFor="cpf">CPF</label>
            <input
              id="cpf"
              inputMode="numeric"
              value={passageiro.cpf}
              onChange={handleCpf}
              placeholder="000.000.000-00"
              aria-invalid={cpfErro ? 'true' : 'false'}
              aria-describedby={cpfErro ? 'cpf-erro' : undefined}
              required
            />
            {cpfErro && <span id="cpf-erro" className="field__error">{cpfErro}</span>}
          </div>
          <div className="field">
            <label htmlFor="nascimento">Data de nascimento</label>
            <input
              id="nascimento"
              type="date"
              max={todayISO()}
              value={passageiro.data_nascimento}
              onChange={update('data_nascimento')}
              required
            />
          </div>
        </div>
        <button type="submit" className="btn-primary btn-block" disabled={loading}>
          {loading ? <><span className="spinner" /> Criando reserva...</> : 'Continuar para pagamento'}
        </button>
      </form>
    </div>
  );
}
