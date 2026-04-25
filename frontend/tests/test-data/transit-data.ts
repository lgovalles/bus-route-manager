export const mockedRoutes = [
  {
    id: 1,
    code: 'R1',
    name: 'Ruta Centro',
    description: 'Ruta principal del centro',
    color: '#1D4ED8',
  },
];

export const mockedStops = [
  {
    id: 101,
    name: 'Parque Central',
    latitude: 18.4708,
    longitude: -69.9007,
  },
  {
    id: 102,
    name: 'Av. Duarte',
    latitude: 18.475,
    longitude: -69.89,
  },
];

export const mockedRouteStops = [
  {
    id: 9001,
    route_id: 1,
    stop_id: 101,
    stop_order: 1,
  },
  {
    id: 9002,
    route_id: 1,
    stop_id: 102,
    stop_order: 2,
  },
];

export const mockedRouteStopsByRoute = [
  {
    id: 101,
    name: 'Parque Central',
    latitude: 18.4708,
    longitude: -69.9007,
    stop_order: 1,
  },
  {
    id: 102,
    name: 'Av. Duarte',
    latitude: 18.475,
    longitude: -69.89,
    stop_order: 2,
  },
];
