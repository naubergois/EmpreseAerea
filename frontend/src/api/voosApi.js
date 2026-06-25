import apiClient from './apiClient';

export const buscarVoos = async (params) => {
  const { data } = await apiClient.get('/api/voos/buscar', { params });
  return data;
};

export const calcularPreco = async (body) => {
  const { data } = await apiClient.post('/api/preco/calcular', body);
  return data;
};

export const validarCupom = async (body) => {
  const { data } = await apiClient.post('/api/preco/cupom/validar', body);
  return data;
};
