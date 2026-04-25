import type { Page } from '@playwright/test';
import {
  mockedRouteStops,
  mockedRouteStopsByRoute,
  mockedRoutes,
  mockedStops,
} from '../test-data/transit-data';

const jsonHeaders = {
  'content-type': 'application/json',
};

export async function mockTransitApi(page: Page): Promise<void> {
  await page.route('**/routes', async (route) => {
    if (route.request().resourceType() === 'document') {
      await route.fallback();
      return;
    }

    await route.fulfill({
      status: 200,
      headers: jsonHeaders,
      body: JSON.stringify(mockedRoutes),
    });
  });

  await page.route('**/stops', async (route) => {
    if (route.request().resourceType() === 'document') {
      await route.fallback();
      return;
    }

    await route.fulfill({
      status: 200,
      headers: jsonHeaders,
      body: JSON.stringify(mockedStops),
    });
  });

  await page.route('**/route-stops', async (route) => {
    if (route.request().resourceType() === 'document') {
      await route.fallback();
      return;
    }

    await route.fulfill({
      status: 200,
      headers: jsonHeaders,
      body: JSON.stringify(mockedRouteStops),
    });
  });

  await page.route('**/routes/1', async (route) => {
    if (route.request().resourceType() === 'document') {
      await route.fallback();
      return;
    }

    await route.fulfill({
      status: 200,
      headers: jsonHeaders,
      body: JSON.stringify(mockedRoutes[0]),
    });
  });

  await page.route('**/routes/1/stops', async (route) => {
    if (route.request().resourceType() === 'document') {
      await route.fallback();
      return;
    }

    await route.fulfill({
      status: 200,
      headers: jsonHeaders,
      body: JSON.stringify(mockedRouteStopsByRoute),
    });
  });
}
