import { Link, NavLink } from 'react-router-dom';
import { FC, ReactNode } from 'react';

interface LayoutProps {
  children: ReactNode;
}

const Layout: FC<LayoutProps> = ({ children }) => {
  return (
    <div className="flex min-h-screen flex-col bg-gray-50 text-gray-900">
      {/* Navbar */}
      <header className="bg-[#0C304C] text-white shadow-md" data-testid="header">
        <div className="mx-auto flex max-w-[1280px] flex-wrap items-center justify-between gap-4 px-4 py-3 md:flex-nowrap md:px-8">
          {/* Logo */}
          <Link
            to="/"
            className="flex items-center gap-2 text-xl font-bold tracking-tight hover:opacity-90 transition-opacity"
            data-testid="header-logo"
          >
            <span className="flex h-8 w-8 items-center justify-center rounded-full bg-[#78A269] text-white text-sm font-extrabold select-none">
              S
            </span>
            <span>SOMOS</span>
          </Link>

          {/* Nav links */}
          <nav className="flex flex-wrap items-center gap-1" data-testid="main-navigation">
            <NavLink
              to="/"
              end
              className={({ isActive }) =>
                `rounded-md px-4 py-2 text-sm font-medium transition-all duration-150 focus:outline-none focus:ring-2 focus:ring-white/60 ${
                  isActive
                    ? 'bg-white/15 text-white font-semibold underline underline-offset-4 decoration-[#F2B944]'
                    : 'text-white/80 hover:bg-white/10 hover:text-white'
                }`
              }
              data-testid="nav-home"
            >
              Inicio
            </NavLink>
            <NavLink
              to="/routes"
              className={({ isActive }) =>
                `rounded-md px-4 py-2 text-sm font-medium transition-all duration-150 focus:outline-none focus:ring-2 focus:ring-white/60 ${
                  isActive
                    ? 'bg-white/15 text-white font-semibold underline underline-offset-4 decoration-[#F2B944]'
                    : 'text-white/80 hover:bg-white/10 hover:text-white'
                }`
              }
              data-testid="nav-routes"
            >
              Rutas
            </NavLink>
            <NavLink
              to="/map"
              className={({ isActive }) =>
                `rounded-md px-4 py-2 text-sm font-medium transition-all duration-150 focus:outline-none focus:ring-2 focus:ring-white/60 ${
                  isActive
                    ? 'bg-white/15 text-white font-semibold underline underline-offset-4 decoration-[#F2B944]'
                    : 'text-white/80 hover:bg-white/10 hover:text-white'
                }`
              }
              data-testid="nav-map"
            >
              Mapa
            </NavLink>
          </nav>
        </div>
      </header>

      {/* Main content */}
      <main
        className="mx-auto w-full max-w-[1280px] flex-1 px-4 py-8 md:px-6 md:py-12 lg:px-8"
        data-testid="main-content"
      >
        {children}
      </main>

      {/* Footer */}
      <footer
        className="border-t border-gray-200 bg-white px-4 py-5 text-center text-xs text-gray-500"
        data-testid="footer"
      >
        <p>
          © {new Date().getFullYear()}{' '}
          <span className="font-semibold text-[#0C304C]">SOMOS</span> — Plataforma de gestión de
          rutas de transporte · v1.0
        </p>
      </footer>
    </div>
  );
};

export default Layout;
