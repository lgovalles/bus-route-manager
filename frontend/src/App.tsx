import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { FC, lazy, Suspense } from 'react';
import Layout from './components/Layout';
import PageLoader from './components/PageLoader';
import ErrorBoundary from './components/ErrorBoundary';

const Home = lazy(() => import('./pages/Home'));
const MapPage = lazy(() => import('./pages/MapPage'));
const RouteDetail = lazy(() => import('./pages/RouteDetail'));
const RoutesList = lazy(() => import('./pages/RoutesList'));
const NotFound = lazy(() => import('./pages/NotFound'));

const App: FC = () => {
  return (
    <Router>
      <Layout>
        <ErrorBoundary>
          <Suspense fallback={<PageLoader />}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/routes" element={<RoutesList />} />
              <Route path="/map" element={<MapPage />} />
              <Route path="/route/:id" element={<RouteDetail />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </Suspense>
        </ErrorBoundary>
      </Layout>
    </Router>
  );
};

export default App;