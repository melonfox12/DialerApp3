import { test, expect } from '@playwright/test';
import { apiJson, openAppShell } from './helpers';

test.describe('Script analytics', () => {
  test('GET /api/scripts/performance returns segments shape', async ({ request }) => {
    const { response, data } = await apiJson<{
      days: number;
      segments: unknown[];
      totals: { dials: number };
    }>(request, 'GET', '/api/scripts/performance?days=7');
    expect(response.status()).toBe(200);
    expect(data).toBeTruthy();
    expect(data!.days).toBe(7);
    expect(Array.isArray(data!.segments)).toBe(true);
    expect(data!.totals).toHaveProperty('dials');
  });

  test('Analytics sidebar tab loads', async ({ page }) => {
    await openAppShell(page);
    await page.locator('#analyticsTabButton').click();
    await expect(page.locator('#analyticsTitle')).toBeVisible();
    await expect(page.locator('#analyticsTabPanel')).toBeVisible();
  });
});