import { Link, useParams } from 'react-router-dom';
import { FC, useEffect, useState } from 'react';
import { Route, StopInRoute } from '../types';
import { fetchRoute, fetchRouteStopsByRoute } from '../services/api';

const RouteDetail: FC = () => {
  const { id } = useParams<{ id: string }>();
  const [route, setRoute] = useState<Route | null>(null);
  const [stops, setStops] = useState<StopInRoute[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadRouteDetail = async () => {
      if (!id) return;
      const routeId = parseInt(id, 10);
      if (isNaN(routeId) || routeId <= 0) {
        setError('El ID de ruta no es válido.');
        setLoading(false);
        return;
      }
      try {
        setLoading(true);
        const [routeData, stopsData] = await Promise.all([
          fetchRoute(routeId),
          fetchRouteStopsByRoute(routeId)
        ]);
        setRoute(routeData);
        setStops(stopsData);
      } catch {
        setError('No se pudieron cargar los detalles de la ruta.');
      } finally {
        setLoading(false);
      }
    };
    loadRouteDetail();
  }, [id]);

  if (!id) {
    return (
      <section data-testid="route-detail-error">
        <h2 className="mb-3 text-3xl font-bold">Error</h2>
        <p className="text-red-600">Ruta no válida. Proporciona un ID de ruta válido.</p>
      </section>
    );
  }

  if (loading) {
    return (
      <section data-testid="route-detail-loading">
        <p>Cargando detalles de la ruta...</p>
      </section>
    );
  }

  if (error) {
    return (
      <section data-testid="route-detail-error">
        <h2 className="mb-3 text-3xl font-bold">Error</h2>
        <p className="text-red-600">{error}</p>
      </section>
    );
  }

  if (!route) {
    return (
      <section data-testid="route-detail-not-found">
        <h2 className="mb-3 text-3xl font-bold">Ruta no encontrada</h2>
        <p className="text-gray-600">La ruta con ID {id} no existe.</p>
      </section>
    );
  }

  return (
    <section data-testid="route-detail">
      <h2 className="mb-3 text-3xl font-bold" data-testid="route-detail-title">Detalle de ruta</h2>
      <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm mb-6" data-testid="route-detail-content">
        <h3 className="text-xl font-semibold mb-2">{route.name}</h3>
        <p className="text-gray-600 mb-1"><strong>Código:</strong> {route.code}</p>
        {route.color && <p className="text-gray-600 mb-1"><strong>Color:</strong> <span style={{ color: route.color }}>{route.color}</span></p>}
        {route.description && <p className="text-gray-600"><strong>Descripción:</strong> {route.description}</p>}
        <Link
          to={`/map?routeId=${route.id}`}
          className="mt-4 inline-block rounded bg-slate-700 px-3 py-2 text-sm text-white hover:bg-slate-800"
          data-testid="route-detail-map-link"
        >
          Ver recorrido en mapa
        </Link>
      </div>
      <div data-testid="route-stops">
        <h3 className="text-xl font-semibold mb-3">Paradas de la ruta</h3>
        {stops.length === 0 ? (
          <p className="text-gray-600">No hay paradas asociadas a esta ruta.</p>
        ) : (
          <ul className="space-y-2">
            {stops.map((stop) => (
              <li key={stop.id} className="rounded-lg border border-gray-200 bg-white p-3 shadow-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <span className="font-medium">{stop.stop_order}. {stop.name}</span>
                    <p className="text-sm text-gray-500">Lat: {stop.latitude}, Lon: {stop.longitude}</p>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </section>
  );
};

export default RouteDetail;
