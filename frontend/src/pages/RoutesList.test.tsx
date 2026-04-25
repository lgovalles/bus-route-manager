import { render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import RoutesList from '../pages/RoutesList';
import useBusStore from '../store/useBusStore';

// Mock the store to control state in tests
vi.mock('../store/useBusStore');

const mockFetchRoutes = vi.fn();

const mockUseStore = vi.mocked(useBusStore);

describe('RoutesList', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('shows loading state', () => {
    mockUseStore.mockReturnValue({
      routes: [],
      loading: true,
      error: null,
      fetchRoutes: mockFetchRoutes,
    } as ReturnType<typeof useBusStore>);

    render(
      <MemoryRouter>
        <RoutesList />
      </MemoryRouter>,
    );

    expect(screen.getByTestId('routes-list-loading')).toBeInTheDocument();
  });

  it('shows error state', () => {
    mockUseStore.mockReturnValue({
      routes: [],
      loading: false,
      error: 'Error de conexión.',
      fetchRoutes: mockFetchRoutes,
    } as ReturnType<typeof useBusStore>);

    render(
      <MemoryRouter>
        <RoutesList />
      </MemoryRouter>,
    );

    expect(screen.getByTestId('routes-list-error')).toBeInTheDocument();
    expect(screen.getByText(/Error de conexión/i)).toBeInTheDocument();
  });

  it('renders route cards', async () => {
    const routes = [
      { id: 1, name: 'Ruta 1', code: 'R1', color: '#ff0000' },
      { id: 2, name: 'Ruta 2', code: 'R2', color: undefined },
    ];

    mockUseStore.mockReturnValue({
      routes,
      loading: false,
      error: null,
      fetchRoutes: mockFetchRoutes,
    } as ReturnType<typeof useBusStore>);

    render(
      <MemoryRouter>
        <RoutesList />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByTestId('routes-list')).toBeInTheDocument();
    });

    expect(screen.getByTestId('route-card-1')).toBeInTheDocument();
    expect(screen.getByTestId('route-card-2')).toBeInTheDocument();
    expect(screen.getByTestId('route-name-1')).toHaveTextContent('Ruta 1');
    expect(screen.getByTestId('route-detail-link-1')).toHaveAttribute('href', '/route/1');
    expect(screen.getByTestId('route-map-link-1')).toHaveAttribute('href', '/map?routeId=1');
  });

  it('calls fetchRoutes on mount', () => {
    mockUseStore.mockReturnValue({
      routes: [],
      loading: true,
      error: null,
      fetchRoutes: mockFetchRoutes,
    } as ReturnType<typeof useBusStore>);

    render(
      <MemoryRouter>
        <RoutesList />
      </MemoryRouter>,
    );

    expect(mockFetchRoutes).toHaveBeenCalledTimes(1);
  });
});
