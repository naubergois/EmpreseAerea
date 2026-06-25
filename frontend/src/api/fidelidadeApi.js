import apiClient from './apiClient';

export const saldoMilhas = async (clienteId) => {
  const { data } = await apiClient.get(`/api/fidelidade/${clienteId}/saldo`);
  return data;
};

export const nivelFidelidade = async (clienteId) => {
  const { data } = await apiClient.get(`/api/fidelidade/${clienteId}/nivel`);
  return data;
};
