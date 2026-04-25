import { expect, test } from '@playwright/test';
import { mockTransitApi } from '../fixtures/mockTransitApi';

test.describe('Smoke: core navigation', () => {
  test.beforeEach(async ({ page }) => {
    await mockTransitApi(page);
  });

  test('AT-E2E-001 should navigate through key public pages', async ({ page }) => {
    await page.goto('/');

    await expect(page.getByTestId('header')).toBeVisible();
    await expect(page.getByTestId('main-navigation')).toBeVisible();

    await page.goto('/routes');
    await expect(page).toHaveURL(/\/routes$/);
    await expect(page.getByTestId('routes-list')).toBeVisible();

    await page.goto('/map');
    await expect(page).toHaveURL(/\/map$/);
    await expect(page.getByTestId('map-page-title')).toBeVisible();

    await page.goto('/this-path-does-not-exist');
    await expect(page.getByTestId('not-found')).toBeVisible();
    await page.getByRole('link', { name: 'Volver al inicio' }).click();
    await expect(page).toHaveURL(/\/$/);
  });
});
