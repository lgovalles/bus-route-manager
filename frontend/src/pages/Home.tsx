import { Link } from 'react-router-dom';
import { FC, ReactElement } from 'react';

interface QuickCard {
  icon: ReactElement;
  title: string;
  description: string;
  label: string;
  to: string;
  testId: string;
}

const IconRoutes: FC = () => (
  <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8} aria-hidden="true">
    <path strokeLinecap="round" strokeLinejoin="round" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
  </svg>
);

const IconMap: FC = () => (
  <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8} aria-hidden="true">
    <path strokeLinecap="round" strokeLinejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
    <path strokeLinecap="round" strokeLinejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
  </svg>
);

const IconSelect: FC = () => (
  <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.8} aria-hidden="true">
    <path strokeLinecap="round" strokeLinejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
  </svg>
);

const cards: QuickCard[] = [
  {
    icon: <IconRoutes />,
    title: 'Ver rutas',
    description: 'Consulta el listado completo de rutas disponibles con sus paradas y recorridos.',
    label: 'Explorar rutas',
    to: '/routes',
    testId: 'home-link-routes',
  },
  {
    icon: <IconMap />,
    title: 'Ver mapa',
    description: 'Visualiza todos los recorridos y paradas de forma interactiva en el mapa.',
    label: 'Abrir mapa',
    to: '/map',
    testId: 'home-link-map',
  },
  {
    icon: <IconSelect />,
    title: 'Elegir una ruta',
    description: 'Selecciona una ruta específica para ver su detalle completo de paradas.',
    label: 'Seleccionar ruta',
    to: '/routes',
    testId: 'home-link-route-detail',
  },
];

const Home: FC = () => {
  return (
    <div className="flex flex-col gap-16">

      {/* ── Hero ── */}
      <section className="flex flex-col items-start gap-6 lg:flex-row lg:items-center lg:gap-12">
        {/* Text block */}
        <div className="flex-1">
          {/* Badge */}
          <span className="mb-4 inline-block rounded-full bg-[#0C304C]/10 px-3 py-1 text-xs font-semibold uppercase tracking-widest text-[#0C304C]">
            Plataforma de transporte
          </span>

          <h1 className="mb-4 text-3xl font-extrabold leading-tight text-[#0C304C] sm:text-4xl lg:text-5xl">
            Gestiona rutas de transporte{' '}
            <span className="text-[#78A269]">de forma simple y visual</span>
          </h1>

          <p className="mb-8 max-w-xl text-base leading-relaxed text-gray-600 sm:text-lg">
            Consulta rutas, visualiza recorridos y selecciona la información que necesitas desde
            un solo lugar.
          </p>

          {/* CTAs */}
          <div className="flex flex-wrap gap-3">
            <Link
              to="/routes"
              className="inline-flex min-h-[44px] items-center justify-center rounded-xl bg-[#0C304C] px-6 py-2.5 text-sm font-semibold text-white shadow-sm transition-all duration-150 hover:bg-[#0a2740] hover:shadow-md focus:outline-none focus:ring-2 focus:ring-[#0C304C] focus:ring-offset-2 active:scale-95"
            >
              Empezar ahora
            </Link>
            <Link
              to="/map"
              className="inline-flex min-h-[44px] items-center justify-center rounded-xl border-2 border-[#0C304C] px-6 py-2.5 text-sm font-semibold text-[#0C304C] transition-all duration-150 hover:bg-[#0C304C]/5 focus:outline-none focus:ring-2 focus:ring-[#0C304C] focus:ring-offset-2 active:scale-95"
            >
              Ver mapa
            </Link>
          </div>
        </div>

        {/* Visual accent block */}
        <div
          className="hidden w-full max-w-xs flex-shrink-0 items-center justify-center rounded-2xl bg-[#0C304C] p-10 text-center lg:flex"
          aria-hidden="true"
        >
          <div className="flex flex-col items-center gap-3 text-white">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-20 w-20 opacity-80" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2h-2M8 7H6a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2v-2" />
            </svg>
            <span className="text-lg font-bold tracking-tight">SOMOS</span>
            <span className="text-xs text-white/60">Sistema de rutas</span>
          </div>
        </div>
      </section>

      {/* ── Quick access cards ── */}
      <section>
        <h2 className="mb-6 text-xl font-bold text-[#0C304C] sm:text-2xl">Accesos rápidos</h2>
        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {cards.map((card) => (
            <div
              key={card.testId}
              className="flex flex-col rounded-2xl border border-gray-200 bg-white p-6 shadow-sm transition-all duration-150 hover:-translate-y-0.5 hover:shadow-md"
            >
              {/* Icon */}
              <div className="mb-4 flex h-14 w-14 items-center justify-center rounded-xl bg-[#0C304C]/8 text-[#0C304C]">
                {card.icon}
              </div>

              {/* Content */}
              <h3 className="mb-2 text-base font-semibold text-[#0C304C]">{card.title}</h3>
              <p className="mb-5 flex-1 text-sm leading-relaxed text-gray-500">{card.description}</p>

              {/* CTA */}
              <Link
                to={card.to}
                className="inline-flex min-h-[44px] items-center justify-center rounded-xl border border-[#78A269] px-4 py-2 text-sm font-semibold text-[#78A269] transition-all duration-150 hover:bg-[#78A269] hover:text-white focus:outline-none focus:ring-2 focus:ring-[#78A269] focus:ring-offset-2 active:scale-95"
                data-testid={card.testId}
              >
                {card.label}
              </Link>
            </div>
          ))}
        </div>
      </section>

    </div>
  );
};

export default Home;
