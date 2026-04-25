import { create } from 'zustand';
import { Stop, Route, RouteStop } from '../types';
import { fetchRoutes, fetchStops, fetchRouteStops } from '../services/api';

interface BusStoreState {
  routes: Route[];
  stops: Stop[];
  routeStops: RouteStop[];
  loading: boolean;
  error: string | null;
  setRoutes: (routes: Route[]) => void;
  setStops: (stops: Stop[]) => void;
  setRouteStops: (routeStops: RouteStop[]) => void;
  addRoute: (route: Route) => void;
  addStop: (stop: Stop) => void;
  addRouteStop: (routeStop: RouteStop) => void;
  fetchRoutes: () => Promise<void>;
  fetchStops: () => Promise<void>;
  fetchRouteStops: () => Promise<void>;
}

const useBusStore = create<BusStoreState>((set) => ({
  routes: [],
  stops: [],
  routeStops: [],
  loading: false,
  error: null,
  setRoutes: (routes) => set({ routes }),
  setStops: (stops) => set({ stops }),
  setRouteStops: (routeStops) => set({ routeStops }),
  addRoute: (route) => set((state) => ({ routes: [...state.routes, route] })),
  addStop: (stop) => set((state) => ({ stops: [...state.stops, stop] })),
  addRouteStop: (routeStop) => set((state) => ({ routeStops: [...state.routeStops, routeStop] })),
  fetchRoutes: async () => {
    set({ loading: true, error: null });
    try {
      const routes = await fetchRoutes();
      set({ routes, loading: false });
    } catch {
      set({ error: 'Failed to fetch routes', loading: false });
    }
  },
  fetchStops: async () => {
    set({ loading: true, error: null });
    try {
      const stops = await fetchStops();
      set({ stops, loading: false });
    } catch {
      set({ error: 'Failed to fetch stops', loading: false });
    }
  },
  fetchRouteStops: async () => {
    set({ loading: true, error: null });
    try {
      const routeStops = await fetchRouteStops();
      set({ routeStops, loading: false });
    } catch {
      set({ error: 'Failed to fetch route stops', loading: false });
    }
  },
}));

export default useBusStore;