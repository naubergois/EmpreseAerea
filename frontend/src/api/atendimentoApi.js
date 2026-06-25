import apiClient from './apiClient';

export const enviarChat = async (body) => {
  const { data } = await apiClient.post('/api/atendimento/chat', body);
  return data;
};
