import type { APIRequestContext, Page } from '@playwright/test';

/** Local E2E server skips Google gate; Supabase mode needs E2E_ACCESS_TOKEN + extraHTTPHeaders. */
export async function openAppShell(page: Page): Promise<void> {
  await page.route('**/api/auth/config', async (route) => {
    const useGoogle = process.env.E2E_SERVER === 'existing' && Boolean(managerAccessToken());
    if (useGoogle) {
      await route.continue();
      return;
    }
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ google: false, url: '', anonKey: '' }),
    });
  });
  await page.goto('/');
  await expectAppReady(page);
}

export async function expectAppReady(page: Page): Promise<void> {
  await page.locator('#loginGate').waitFor({ state: 'hidden', timeout: 45_000 });
  await page.locator('.app-shell').waitFor({ state: 'visible', timeout: 10_000 });
}

export function managerAccessToken(): string {
  return (process.env.E2E_ACCESS_TOKEN || process.env.E2E_MANAGER_ACCESS_TOKEN || '').trim();
}

export function hasManagerAccess(): boolean {
  return Boolean(managerAccessToken());
}

export function authHeaders(): Record<string, string> {
  const token = managerAccessToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function apiJson<T = unknown>(
  request: APIRequestContext,
  method: 'GET' | 'POST',
  path: string,
  body?: object,
  extraHeaders?: Record<string, string>,
) {
  const headers = { ...authHeaders(), ...extraHeaders };
  const response = await (method === 'GET'
    ? request.get(path, { headers })
  : request.post(path, { headers, data: body ?? {} }));
  const text = await response.text();
  let data: T | null = null;
  if (text) {
    try {
      data = JSON.parse(text) as T;
    } catch {
      data = null;
    }
  }
  return { response, data, text };
}