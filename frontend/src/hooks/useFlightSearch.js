import { useState, useCallback } from 'react';
import { buscarVoos } from '../api/voosApi';

export function useFlightSearch() {
  const [flights, setFlights] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const search = useCallback(async (params) => {
    setLoading(true);
    setError(null);
    try {
      const data = await buscarVoos(params);
      setFlights(data.voos || []);
    } catch (err) {
      const detail = err.response?.data?.detail;
      const msg = typeof detail === 'string'
        ? detail
        : Array.isArray(detail)
          ? detail.map((d) => d.msg).join(', ')
          : err.message || 'Erro ao buscar voos';
      setError(msg);
    } finally {
      setLoading(false);
    }
  }, []);

  return { flights, loading, error, search };
}
