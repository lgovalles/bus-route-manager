import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  message: string;
}

/**
 * Catches runtime errors in any child component tree and renders a fallback UI
 * instead of crashing the whole application.
 */
class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, message: '' };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, message: error.message };
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    // In production, send to an error-tracking service (e.g. Sentry).
    console.error('[ErrorBoundary]', error, info.componentStack);
  }

  private handleReset = (): void => {
    this.setState({ hasError: false, message: '' });
  };

  render(): ReactNode {
    if (this.state.hasError) {
      if (this.props.fallback) return this.props.fallback;

      return (
        <section
          className="flex flex-col items-center justify-center gap-4 py-20 text-center"
          role="alert"
          data-testid="error-boundary"
        >
          <span className="text-6xl" aria-hidden="true">⚠️</span>
          <h2 className="text-xl font-bold text-[#0C304C]">Algo salió mal</h2>
          <p className="max-w-sm text-sm text-gray-600">{this.state.message || 'Se produjo un error inesperado.'}</p>
          <button
            onClick={this.handleReset}
            className="mt-2 rounded-xl bg-[#0C304C] px-5 py-2.5 text-sm font-semibold text-white hover:bg-[#0a2740] focus:outline-none focus:ring-2 focus:ring-[#0C304C] focus:ring-offset-2"
          >
            Intentar de nuevo
          </button>
        </section>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
