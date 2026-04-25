import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FC } from 'react';
import useBusStore from '../store/useBusStore';

const RoutesList: FC = () => {
  const { routes, loading, error, fetchRoutes } = useBusStore();

  useEffect(() => {
    fetchRoutes();
  }, [fetchRoutes]);

  if (loading) {
    return (
      <section data-testid="routes-list-loading">
        <h2 className="mb-3 text-3xl font-bold">Lista de rutas</h2>
        <p>Cargando rutas...</p>
      </section>
    );
  }

  if (error) {
    return (
      <section data-testid="routes-list-error">
        <h2 className="mb-3 text-3xl font-bold">Lista de rutas</h2>
        <p className="text-red-600">Error: {error}</p>
      </section>
    );
  }

  return (
    <section data-testid="routes-list">
      <h2 className="mb-3 text-3xl font-bold">Lista de rutas</h2>
      <p className="mb-4 text-gray-700">Aquí se muestran todas las rutas disponibles.</p>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3" data-testid="routes-grid">
        {routes.map((route) => (
          <div key={route.id} className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm" data-testid={`route-card-${route.id}`}>
            <div className="flex items-center mb-2">
              {route.color && (
                <div
                  className="w-4 h-4 rounded-full mr-2"
                  style={{ backgroundColor: route.color }}
                  data-testid={`route-color-${route.id}`}
                ></div>
              )}
              <h3 className="text-lg font-semibold" data-testid={`route-name-${route.id}`}>{route.name}</h3>
            </div>
            {route.description && <p className="text-gray-600 mb-2">{route.description}</p>}
            <Link
              to={`/route/${route.id}`}
              className="inline-block rounded bg-blue-600 px-3 py-1 text-white hover:bg-blue-700 text-sm"
              data-testid={`route-detail-link-${route.id}`}
            >
              Ver detalle
            </Link>
            <Link
              to={`/map?routeId=${route.id}`}
              className="ml-2 inline-block rounded bg-slate-700 px-3 py-1 text-sm text-white hover:bg-slate-800"
              data-testid={`route-map-link-${route.id}`}
            >
              Ver en mapa
            </Link>
          </div>
        ))}
      </div>
    </section>
  );
};

export default RoutesList;