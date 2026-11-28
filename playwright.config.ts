import { defineConfig, devices } from '@playwright/test';
import { loadProjectEnv } from './e2e/load-env';

loadProjectEnv();

// Supabase E2E: set E2E_SUPABASE=1 and E2E_ACCESS_TOKEN in repo `.env` (see .env.example).
const useSupabaseApp =
  process.env.E2E_SERVER === 'existing'
  || process.env.E2E_SUPABASE === '1';
if (useSupabaseApp) {
  process.env.E2E_SERVER = 'existing';
}

const host = process.env.E2E_HOST || '127.0.0.1';
const port = process.env.E2E_PORT || (useSupabaseApp ? '8000' : '8010');
const baseURL = process.env.E2E_BASE_URL || `http://${host}:${port}`;

const bearer = (process.env.E2E_ACCESS_TOKEN || process.env.E2E_MANAGER_ACCESS_TOKEN || '').trim();
const twilioLive =
  process.env.E2E_TWILIO_LIVE === '1' || process.env.E2E_TWILIO_LIVE === 'true';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: 1,
  reporter: [['list'], ['html', { open: 'never' }]],
  timeout: 60_000,
  use: {
    baseURL,
    trace: 'on-first-retry',
    ...(bearer ? { extraHTTPHeaders: { Authorization: `Bearer ${bearer}` } } : {}),
  },
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        ...(twilioLive
          ? {
              launchOptions: {
                args: [
                  '--use-fake-device-for-media-stream',
                  '--use-fake-ui-for-media-stream',
                ],
              },
            }
          : {}),
      },
    },
  ],
  // Supabase mode: dialer.py reads repo `.env`; start it yourself on :8000 (or set E2E_SERVER=local).
  ...(!useSupabaseApp
    ? {
        webServer: {
          command: 'python scripts/e2e_server.py',
          url: `${baseURL}/api/health`,
          reuseExistingServer: !process.env.CI,
          timeout: 120_000,
          stdout: 'pipe',
          stderr: 'pipe',
        },
      }
    : {}),
});