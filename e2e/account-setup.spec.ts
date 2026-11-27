import { test, expect } from '@playwright/test';
import { apiJson } from './helpers';

test.describe('Account setup API', () => {
  test('GET /api/account/setup returns onboarding shape in local mode', async ({ request }) => {
    const { response, data } = await apiJson<{
      storage: string;
      signed_in: boolean;
      org_ready: boolean;
      voice_ready: boolean;
      membership: Record<string, unknown>;
      next_steps: string[];
    }>(request, 'GET', '/api/account/setup');
    expect(response.status()).toBe(200);
    expect(data).toBeTruthy();
    expect(data!.storage).toContain('local');
    expect(data!.signed_in).toBe(true);
    expect(data!.org_ready).toBe(false);
    expect(Array.isArray(data!.next_steps)).toBe(true);
    expect(data!.next_steps).toContain('twilio_voice');
  });

  test('GET /api/auth/me includes status field', async ({ request }) => {
    const { response, data } = await apiJson<Record<string, unknown>>(request, 'GET', '/api/auth/me');
    expect(response.status()).toBe(200);
    expect(data).toHaveProperty('status');
    expect(data).toHaveProperty('can_manage_team');
  });

  test('rejects setup without session when Supabase auth required', async ({ request }) => {
    test.skip(process.env.E2E_SERVER !== 'existing', 'Only applies when testing against Supabase server');
    const { response } = await request.get('/api/account/setup');
    expect([401, 403]).toContain(response.status());
  });
});