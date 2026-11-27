import { test, expect } from '@playwright/test';
import { apiJson, hasManagerAccess, openAppShell } from './helpers';

test.describe('Usage events telemetry', () => {
  test('POST /api/usage/tab accepts tab focus in local mode', async ({ request }) => {
    const { response, text } = await apiJson(request, 'POST', '/api/usage/tab', { tab: 'dialer' });
    // Known APP BUG: web.py does not pass JSON body to post_tab_focus (expects 204).
    expect(response.status(), text || '').toBe(204);
  });

  test('POST /api/usage/tab with empty tab is a no-op', async ({ request }) => {
    const { response } = await apiJson(request, 'POST', '/api/usage/tab', { tab: '' });
    expect(response.status()).toBe(204);
  });

  test('switching tabs sends tab_focus when throttled', async ({ page }) => {
    await openAppShell(page);
    let tabPosts = 0;
    await page.route('**/api/usage/tab', (route) => {
      tabPosts += 1;
      route.continue();
    });
    await page.locator('#prospectsTabButton').click();
    await page.waitForTimeout(500);
    await page.locator('#dialerTabButton').click();
    expect(tabPosts).toBeGreaterThanOrEqual(1);
  });

  test('member usage endpoint requires manager', async ({ request }) => {
    const fakeUser = '00000000-0000-4000-8000-000000000001';
    const { response, data, text } = await apiJson(
      request,
      'GET',
      `/api/team/members/${fakeUser}/usage?minutes=60`,
    );
    if (hasManagerAccess() && process.env.E2E_SERVER === 'existing') {
      expect([200, 403, 404]).toContain(response.status());
      return;
    }
    expect(response.status(), text || '').toBe(403);
    expect(data).toHaveProperty('error');
  });
});