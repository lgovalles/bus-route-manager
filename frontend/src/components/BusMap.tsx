import { ChangeEvent, useEffect, useState } from 'react';
import { FC } from 'react';
import { MapContainer, Marker, Popup, Polyline, TileLayer, useMap } from 'react-leaflet';
import { useSearchParams } from 'react-router-dom';
import 'leaflet/dist/leaflet.css';
import '../lib/leaflet-icons';
import useBusStore from '../store/useBusStore';
import { fetchRouteStops, fetchRoutes, fetchStops } from '../services/api';

const DEFAULT_CENTER: [number, number] = [6.1533, -75.3737];
const DEFAULT_ZOOM = 13;

interface RouteViewportProps {
  coordinates: [number, number][];
}

const RouteViewport: FC<RouteViewportProps> = ({ coordinates }) => {
  const map = useMap();

  useEffect(() => {
    if (coordinates.length === 0) {
      map.setView(DEFAULT_CENTER, DEFAULT_ZOOM);
      return;
    }

    if (coordinates.length === 1) {
      map.setView(coordinates[0], 15);
      return;
    }

    map.fitBounds(coordinates, { padding: [32, 32] });
  }, [coordinates, map]);

  return null;
};

const BusMap: FC = () => {
  const { routes, stops, routeStops, setRoutes, setStops, setRouteStops } = useBusStore();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchParams, setSearchParams] = useSearchParams();

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      setError(null);

      try {
        const [routesData, stopsData, routeStopsData] = await Promise.all([
          fetchRoutes(),
          fetchStops(),
          fetchRouteStops(),
        ]);

        setRoutes(routesData);
        setStops(stopsData);
        setRouteStops(routeStopsData);
      } catch {
        setError('No se pudo cargar la información del mapa.');
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [setRoutes, setStops, setRouteStops]);

  const getRoutesForStop = (stopId: number) => {
    const routeIds = routeStops
      .filter(rs => rs.stop_id === stopId)
      .map(rs => rs.route_id);
    return routes.filter(route => routeIds.includes(route.id));
  };

  const selectedRouteIdParam = searchParams.get('routeId');
  const selectedRouteId = selectedRouteIdParam ? Number(selectedRouteIdParam) : null;
  const selectedRoute = selectedRouteId
    ? routes.find((route) => route.id === selectedRouteId) ?? null
    : null;

  const selectedRouteCoordinates: [number, number][] = selectedRouteId
    ? routeStops
        .filter((routeStop) => routeStop.route_id === selectedRouteId)
        .sort((firstStop, secondStop) => firstStop.stop_order - secondStop.stop_order)
        .map((routeStop) => stops.find((stop) => stop.id === routeStop.stop_id))
        .filter((stop): stop is NonNullable<typeof stop> => Boolean(stop))
        .map((stop) => [stop.latitude, stop.longitude])
    : [];

  const handleRouteChange = (event: ChangeEvent<HTMLSelectElement>) => {
    const nextRouteId = event.target.value;

    setSearchParams((currentParams) => {
      const nextParams = new URLSearchParams(currentParams);

      if (nextRouteId) {
        nextParams.set('routeId', nextRouteId);
      } else {
        nextParams.delete('routeId');
      }

      return nextParams;
    });
  };

  if (loading) {
    return (
      <div data-testid="map-loading">
        <p>Cargando mapa y paradas...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div data-testid="map-error">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-4" data-testid="bus-map">
      <div className="flex flex-col gap-3 rounded-lg border border-slate-200 bg-slate-50 p-4 md:flex-row md:items-end md:justify-between">
        <div className="space-y-1">
          <label htmlFor="route-select" className="block text-sm font-semibold text-slate-900">
            Ruta a mostrar
          </label>
          <select
            id="route-select"
            className="w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-900 md:min-w-80"
            value={selectedRouteIdParam ?? ''}
            onChange={handleRouteChange}
            data-testid="route-select"
          >
            <option value="">Selecciona una ruta</option>
            {routes.map((route) => (
              <option key={route.id} value={route.id}>
                {route.code} - {route.name}
              </option>
            ))}
          </select>
        </div>
        <div className="text-sm text-slate-600" data-testid="selected-route-summary">
          {selectedRoute ? (
            <p>
              Mostrando <strong style={{ color: selectedRoute.color ?? '#2563eb' }}>{selectedRoute.name}</strong>
              {' '}con {selectedRouteCoordinates.length} parada{selectedRouteCoordinates.length === 1 ? '' : 's'} conectadas.
            </p>
          ) : (
            <p>Selecciona una ruta para dibujar su recorrido sobre el mapa.</p>
          )}
        </div>
      </div>

      <MapContainer
        center={DEFAULT_CENTER}
        zoom={DEFAULT_ZOOM}
        style={{ height: '500px', width: '100%' }}
        data-testid="map-container"
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        <RouteViewport coordinates={selectedRouteCoordinates} />
        {selectedRouteCoordinates.length > 1 && (
          <Polyline
            positions={selectedRouteCoordinates}
            pathOptions={{
              color: selectedRoute?.color ?? '#2563eb',
              weight: 5,
              opacity: 0.9,
            }}
            data-testid="route-polyline"
          />
        )}
        {stops.map((stop) => {
          const stopRoutes = getRoutesForStop(stop.id);
          return (
            <Marker key={stop.id} position={[stop.latitude, stop.longitude]} data-testid={`map-marker-${stop.id}`}>
              <Popup data-testid={`map-popup-${stop.id}`}>
                <div>
                  <strong>{stop.name}</strong>
                  {stopRoutes.length > 0 && (
                    <div>
                      <br />
                      <strong>Rutas:</strong>
                      <ul>
                        {stopRoutes.map(route => (
                          <li key={route.id} style={{ color: route.color || 'black' }}>
                            {route.name} ({route.code})
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </Popup>
            </Marker>
          );
        })}
      </MapContainer>
    </div>
  );
};

export default BusMap;