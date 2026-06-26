import { Link } from 'react-router-dom';
import { useBooking } from '../context/BookingContext';
import { useDocumentTitle } from '../hooks/useDocumentTitle';

export default function ConfirmationPage() {
  useDocumentTitle('Confirmação');
  const { confirmation, reservation } = useBooking();

  const pnr = confirmation?.resultado?.pnr || confirmation?.pnr || reservation?.pnr;

  if (!pnr) {
    return (
      <div className="card text-center" style={{ maxWidth: 600, margin: '0 auto' }}>
        <h2>Nenhuma compra encontrada</h2>
        <p className="text-muted" style={{ margin: '1rem 0' }}>
          Não há confirmação para exibir. Comece uma nova busca de voos.
        </p>
        <Link to="/" className="btn-primary" style={{ display: 'inline-block' }}>Buscar voos</Link>
      </div>
    );
  }

  return (
    <div className="card text-center" style={{ maxWidth: 600, margin: '0 auto' }}>
      <div style={{ fontSize: '4rem', marginBottom: '1rem' }} role="img" aria-label="Sucesso">✅</div>
      <h2>Compra confirmada!</h2>
      <p style={{ margin: '1rem 0' }}>
        PNR: <strong>{pnr}</strong>
      </p>
      {confirmation?.resultado?.bilhete && (
        <p>Bilhete: <strong>{confirmation.resultado.bilhete}</strong></p>
      )}
      {confirmation?.trace_id && (
        <p className="text-muted" style={{ fontSize: 'var(--text-sm)' }}>Trace ID: {confirmation.trace_id}</p>
      )}
      <Link to="/" className="btn-outline" style={{ display: 'inline-block', marginTop: '1.5rem' }}>
        Nova busca
      </Link>
    </div>
  );
}
