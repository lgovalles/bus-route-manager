import { Link } from 'react-router-dom';
import { FC } from 'react';

const NotFound: FC = () => {
  return (
    <section
      className="flex flex-col items-center justify-center gap-6 py-24 text-center"
      data-testid="not-found"
    >
      <span className="text-8xl font-extrabold text-[#0C304C]/20 select-none" aria-hidden="true">
        404
      </span>
      <h1 className="text-2xl font-bold text-[#0C304C]">Página no encontrada</h1>
      <p className="max-w-md text-gray-600">
        La página que buscas no existe o fue movida. Vuelve al inicio para continuar navegando.
      </p>
      <Link
        to="/"
        className="inline-flex min-h-[44px] items-center justify-center rounded-xl bg-[#0C304C] px-6 py-2.5 text-sm font-semibold text-white shadow-sm transition-all duration-150 hover:bg-[#0a2740] focus:outline-none focus:ring-2 focus:ring-[#0C304C] focus:ring-offset-2"
      >
        Volver al inicio
      </Link>
    </section>
  );
};

export default NotFound;
