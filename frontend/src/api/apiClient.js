import axios from 'axios';

// Em dev, usa proxy do Vite (mesma origem). Em produção, usa VITE_API_URL.
const API_BASE_URL = import.meta.env.VITE_API_URL ?? '';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (!error.response) {
      error.message = 'Não foi possível conectar à API. Verifique se o backend está rodando.';
    }
    return Promise.reject(error);
  },
);

export default apiClient;
