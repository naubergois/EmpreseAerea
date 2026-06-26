import apiClient from './apiClient';

export const listarTestesBdd = async ({ run = false } = {}) => {
  const { data } = await apiClient.get('/api/qa/bdd', {
    params: { run },
    timeout: 300000,
  });
  return data;
};

export const executarTestesBdd = async () => {
  const { data } = await apiClient.post('/api/qa/bdd/run', null, {
    timeout: 300000,
  });
  return data;
};
