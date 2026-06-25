import { useBooking } from '../context/BookingContext';

export default function ConfirmationPage() {
  const { confirmation, reservation } = useBooking();

  return (
    <div className="card" style={{ maxWidth: 600, textAlign: 'center' }}>
      <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>✅</div>
      <h2>Compra confirmada!</h2>
      <p style={{ margin: '1rem 0' }}>
        PNR: <strong>{confirmation?.resultado?.pnr || confirmation?.pnr || reservation?.pnr}</strong>
      </p>
      {confirmation?.resultado?.bilhete && (
        <p>Bilhete: <strong>{confirmation.resultado.bilhete}</strong></p>
      )}
      {confirmation?.trace_id && (
        <p style={{ color: '#6b7280', fontSize: '0.875rem' }}>Trace ID: {confirmation.trace_id}</p>
      )}
    </div>
  );
}
