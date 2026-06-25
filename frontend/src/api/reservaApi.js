import apiClient from './apiClient';

export const criarReserva = async (body) => {
  const { data } = await apiClient.post('/api/reserva/', body);
  return data;
};

export const buscarReserva = async (pnr) => {
  const { data } = await apiClient.get(`/api/reserva/${pnr}`);
  return data;
};

export const iniciarPipeline = async (body) => {
  const { data } = await apiClient.post('/api/pipeline/start', body);
  return data;
};
