import { useEffect, useCallback } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useFlightSearch } from '../hooks/useFlightSearch';
import { useBooking } from '../context/BookingContext';
import { useDocumentTitle } from '../hooks/useDocumentTitle';
import { calcularPreco } from '../api/voosApi';
import FlightList from '../components/voos/FlightList';
import './SearchResultsPage.css';

export default function SearchResultsPage() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const { flights, loading, error, search } = useFlightSearch();
  const { setSelectedFlight, setPricing } = useBooking();

  const origem = params.get('origem');
  const destino = params.get('destino');
  const dataIda = params.get('data_ida');
  const classe = params.get('classe') || 'economica';
  const adultos = params.get('adultos') || 1;

  useDocumentTitle(`Voos ${origem} → ${destino}`);

  const executarBusca = useCallback(() => {
    search({ origem, destino, data_ida: dataIda, classe, adultos });
  }, [search, origem, destino, dataIda, classe, adultos]);

  useEffect(() => {
    executarBusca();
  }, [executarBusca]);

  const handleSelect = async (flight) => {
    setSelectedFlight(flight);
    const pricing = await calcularPreco({ voo_id: flight.id, preco_base: flight.preco });
    setPricing(pricing);
    navigate('/reserva');
  };

  return (
    <div>
      <div className="results-head">
        <div>
          <h2>Voos {origem} → {destino}</h2>
          <p className="results-head__meta text-muted">
            {dataIda} · {classe === 'executiva' ? 'Executiva' : 'Econômica'} · {adultos} passageiro(s)
          </p>
        </div>
        <button type="button" className="btn-outline" onClick={() => navigate('/')}>
          Alterar busca
        </button>
      </div>

      <div aria-live="polite" aria-busy={loading}>
        {loading && (
          <div className="results-skeletons" aria-hidden="true">
            {[0, 1, 2].map((i) => <div key={i} className="skeleton results-skeleton" />)}
          </div>
        )}

        {!loading && error && (
          <div className="alert alert-error" role="alert">
            <p>{error}</p>
            <button type="button" className="btn-outline" style={{ marginTop: '0.75rem' }} onClick={executarBusca}>
              Tentar novamente
            </button>
          </div>
        )}

        {!loading && !error && flights.length === 0 && (
          <div className="alert alert-info">Nenhum voo encontrado. Tente datas flexíveis ou outra rota.</div>
        )}

        {!loading && !error && <FlightList flights={flights} onSelect={handleSelect} />}
      </div>
    </div>
  );
}
