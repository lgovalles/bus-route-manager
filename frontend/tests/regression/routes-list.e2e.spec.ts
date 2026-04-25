import { expect, test } from '@playwright/test';
import { mockTransitApi } from '../fixtures/mockTransitApi';

test.describe('Regression: routes listing and route detail', () => {
  test.beforeEach(async ({ page }) => {
    await mockTransitApi(page);
  });

  test('AT-E2E-002 should render routes and open route detail page', async ({ page }) => {
    await page.goto('/routes');

    await expect(page.getByTestId('routes-list')).toBeVisible();
    await expect(page.getByTestId('routes-grid')).toBeVisible();
    await expect(page.getByTestId('route-card-1')).toBeVisible();
    await expect(page.getByTestId('route-name-1')).toContainText('Ruta Centro');

    const detailLink = page.getByTestId('route-detail-link-1');
    await expect(detailLink).toHaveAttribute('href', '/route/1');
    await detailLink.click();

    await expect(page).toHaveURL(/\/route\/1$/);
    await expect(page.getByTestId('route-detail')).toBeVisible();
    await expect(page.getByTestId('route-detail-title')).toContainText('Detalle de ruta');
    await expect(page.getByTestId('route-detail-map-link')).toHaveAttribute('href', '/map?routeId=1');
  });
});
