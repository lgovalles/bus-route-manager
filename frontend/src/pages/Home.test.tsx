import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, it, expect } from 'vitest';
import Home from '../pages/Home';

describe('Home', () => {
  const renderHome = () =>
    render(
      <MemoryRouter>
        <Home />
      </MemoryRouter>,
    );

  it('renders the hero headline', () => {
    renderHome();
    expect(
      screen.getByText(/Gestiona rutas de transporte/i),
    ).toBeInTheDocument();
  });

  it('renders quick-access links', () => {
    renderHome();
    expect(screen.getByTestId('home-link-routes')).toBeInTheDocument();
    expect(screen.getByTestId('home-link-map')).toBeInTheDocument();
    expect(screen.getByTestId('home-link-route-detail')).toBeInTheDocument();
  });

  it('links point to the correct routes', () => {
    renderHome();
    expect(screen.getByTestId('home-link-routes').closest('a')).toHaveAttribute('href', '/routes');
    expect(screen.getByTestId('home-link-map').closest('a')).toHaveAttribute('href', '/map');
  });
});
