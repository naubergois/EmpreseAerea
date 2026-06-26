import { formatCurrency, formatTime, formatDuration } from '../../utils/formatters';
import './FlightCard.css';

export default function FlightCard({ flight, onSelect }) {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      onSelect?.(flight);
    }
  };

  return (
    <div
      className="flight-card"
      role="button"
      tabIndex={0}
      aria-label={`Selecionar voo ${flight.numero} de ${flight.origem} para ${flight.destino} por ${formatCurrency(flight.preco)}`}
      onClick={() => onSelect?.(flight)}
      onKeyDown={handleKeyDown}
    >
      <div className="flight-card__airline">
        <span className="flight-card__name">{flight.companhia?.nome}</span>
        <span className="flight-card__number">{flight.numero}</span>
      </div>
      <div className="flight-card__times">
        <div>
          <strong>{formatTime(flight.partida)}</strong>
          <span>{flight.origem}</span>
        </div>
        <div className="flight-card__duration">
          <span>{formatDuration(flight.duracao_minutos)}</span>
          <div className="flight-card__line" />
          <span>{flight.escalas === 0 ? 'Direto' : `${flight.escalas} escala(s)`}</span>
        </div>
        <div>
          <strong>{formatTime(flight.chegada)}</strong>
          <span>{flight.destino}</span>
        </div>
      </div>
      <div className="flight-card__price">
        <span>a partir de</span>
        <strong>{formatCurrency(flight.preco)}</strong>
        <span className="flight-card__baggage">
          {flight.bagagem_inclusa ? '✓ Bagagem inclusa' : 'Sem bagagem'}
        </span>
      </div>
    </div>
  );
}
