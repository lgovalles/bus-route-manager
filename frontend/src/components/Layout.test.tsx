import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, it, expect } from 'vitest';
import Layout from '../components/Layout';

describe('Layout', () => {
  const renderLayout = (path = '/') =>
    render(
      <MemoryRouter initialEntries={[path]}>
        <Layout>
          <div data-testid="child-content">Contenido</div>
        </Layout>
      </MemoryRouter>,
    );

  it('renders the header with logo', () => {
    renderLayout();
    expect(screen.getByTestId('header')).toBeInTheDocument();
    expect(screen.getByTestId('header-logo')).toBeInTheDocument();
  });

  it('renders navigation links', () => {
    renderLayout();
    expect(screen.getByTestId('main-navigation')).toBeInTheDocument();
    expect(screen.getByTestId('nav-home')).toBeInTheDocument();
    expect(screen.getByTestId('nav-routes')).toBeInTheDocument();
  });

  it('renders children', () => {
    renderLayout();
    expect(screen.getByTestId('child-content')).toBeInTheDocument();
  });
});
