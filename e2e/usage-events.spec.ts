import { test, expect } from '@playwright/test';
import { apiJson, hasManagerAccess, openAppShell } from './helpers';

test.describe('Usage events telemetry', () => {
  test('POST /api/usage/tab accepts tab focus in local mode', async ({ request }) => {
    const { response, text } = await apiJson(request, 'POST', '/api/usage/tab', { tab: 'dialer' });
    expect(response.status(), text || '').toBe(204);
  });

  test('POST /api/usage/tab with empty tab is a no-op', async ({ request }) => {
    const { response } = await apiJson(request, 'POST', '/api/usage/tab', { tab: '' });
    expect(response.status()).toBe(204);
  });

  test('browser can POST tab_focus after navigation', async ({ page }) => {
    await openAppShell(page);
    const done = page.waitForResponse(
      (r) => r.url().includes('/api/usage/tab') && r.request().method() === 'POST' && r.status() === 204,
      { timeout: 10_000 },
    );
    await page.evaluate(async () => {
      const { setDashboardTab } = await import('/static/_core/navigation.js');
      const { S } = await import('/static/core.js');
      S.googleAuthEnabled = true;
      S.accessToken = 'e2e-local-tab-focus';
      setDashboardTab('prospects');
    });
    await done;
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