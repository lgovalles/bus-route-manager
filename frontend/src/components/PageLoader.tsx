import { FC } from 'react';

const PageLoader: FC = () => (
  <div
    className="flex min-h-[40vh] items-center justify-center"
    role="status"
    aria-label="Cargando página"
    data-testid="page-loader"
  >
    <div className="h-10 w-10 animate-spin rounded-full border-4 border-[#0C304C]/20 border-t-[#0C304C]" />
  </div>
);

export default PageLoader;
