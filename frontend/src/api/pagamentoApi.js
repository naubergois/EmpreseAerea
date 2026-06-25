import apiClient from './apiClient';

export const pagarCartao = async (body) => {
  const { data } = await apiClient.post('/api/pagamento/cartao', body);
  return data;
};

export const gerarPix = async (body) => {
  const { data } = await apiClient.post('/api/pagamento/pix', body);
  return data;
};
