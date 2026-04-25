import { expect, test } from '@playwright/test';

test.describe('Critical path: error handling', () => {
  test('AT-E2E-003 should show user-friendly error when routes API fails', async ({ page }) => {
    await page.route('**/routes', async (route) => {
      if (route.request().resourceType() === 'document') {
        await route.fallback();
        return;
      }

      await route.fulfill({
        status: 500,
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ detail: 'Internal Server Error' }),
      });
    });

    await page.goto('/routes');

    await expect(page.getByTestId('routes-list-error')).toBeVisible();
    await expect(page.getByText(/Error:/)).toBeVisible();
  });
});
