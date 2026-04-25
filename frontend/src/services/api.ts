import axios, { AxiosError } from 'axios';
import { Route, Stop, RouteStop, StopInRoute } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10_000,
});

// ── Response interceptor: normalize errors ────────────────────────────────────
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    const status = error.response?.status;
    let message = 'Error de conexión. Verifica que el servidor esté disponible.';

    if (status === 404) {
      message = 'El recurso solicitado no fue encontrado.';
    } else if (status === 422) {
      message = 'Los datos enviados no son válidos.';
    } else if (status && status >= 500) {
      message = 'Error interno del servidor. Intenta de nuevo más tarde.';
    } else if (error.code === 'ECONNABORTED') {
      message = 'La solicitud tardó demasiado. Revisa tu conexión.';
    }

    return Promise.reject(new Error(message));
  },
);

export const fetchRoutes = async (): Promise<Route[]> => {
  const response = await api.get('/routes');
  return response.data;
};

export const fetchStops = async (): Promise<Stop[]> => {
  const response = await api.get('/stops');
  return response.data;
};

export const fetchRouteStops = async (): Promise<RouteStop[]> => {
  const response = await api.get('/route-stops');
  return response.data;
};

export const fetchRoute = async (id: number): Promise<Route> => {
  const response = await api.get(`/routes/${id}`);
  return response.data;
};

export const fetchRouteStopsByRoute = async (id: number): Promise<StopInRoute[]> => {
  const response = await api.get(`/routes/${id}/stops`);
  return response.data;
};

export default api;