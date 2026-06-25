import { useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useFlightSearch } from '../hooks/useFlightSearch';
import { useBooking } from '../context/BookingContext';
import { calcularPreco } from '../api/voosApi';
import FlightList from '../components/voos/FlightList';

export default function SearchResultsPage() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const { flights, loading, error, search } = useFlightSearch();
  const { setSelectedFlight, setPricing } = useBooking();

  useEffect(() => {
    search({
      origem: params.get('origem'),
      destino: params.get('destino'),
      data_ida: params.get('data_ida'),
      classe: params.get('classe') || 'economica',
      adultos: params.get('adultos') || 1,
    });
  }, [params, search]);

  const handleSelect = async (flight) => {
    setSelectedFlight(flight);
    const pricing = await calcularPreco({ voo_id: flight.id, preco_base: flight.preco });
    setPricing(pricing);
    navigate('/reserva');
  };

  return (
    <div>
      <h2 style={{ marginBottom: '1.5rem' }}>
        Voos {params.get('origem')} → {params.get('destino')}
      </h2>
      {loading && <p>Buscando os melhores voos...</p>}
      {error && <div className="alert alert-error">{error}</div>}
      {!loading && flights.length === 0 && (
        <div className="alert alert-info">Nenhum voo encontrado. Tente datas flexíveis.</div>
      )}
      <FlightList flights={flights} onSelect={handleSelect} />
    </div>
  );
}
