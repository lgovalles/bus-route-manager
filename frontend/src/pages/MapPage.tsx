import BusMap from '../components/BusMap';
import { FC } from 'react';

const MapPage: FC = () => {
  return (
    <section data-testid="map-page">
      <h2 className="mb-3 text-3xl font-bold" data-testid="map-page-title">Mapa de rutas</h2>
      <p className="mb-4 text-gray-700" data-testid="map-page-description">Selecciona una ruta para convertir sus paradas en coordenadas y dibujar su recorrido directamente sobre el mapa.</p>
      <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm" data-testid="map-container">
        <BusMap />
      </div>
    </section>
  );
};

export default MapPage;
