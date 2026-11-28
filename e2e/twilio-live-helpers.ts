import type { APIRequestContext, Page } from '@playwright/test';
import { apiJson, expectAppReady, managerAccessToken } from './helpers';

/** Twilio magic test numbers (live Voice SDK still needs live credentials + HTTPS hooks). */
export const TWILIO_MAGIC = {
  /** Valid number for availability checks; routable as To on many accounts. */
  valid: '+15005550006',
  /** Queues successfully but is treated as blocked (no real ring). */
  blockedNoRing: '+15005550004',
  /** Invalid To — expect Twilio 21217. */
  invalidTo: '+15005550001',
  /** Cannot route — expect Twilio 21214. */
  unroutable: '+15005550002',
} as const;

export function twilioLiveEnabled(): boolean {
  return process.env.E2E_TWILIO_LIVE === '1' || process.env.E2E_TWILIO_LIVE === 'true';
}

export function dialToNumber(): string {
  const custom = (process.env.E2E_TWILIO_TO || '').trim();
  if (custom) return custom;
  return TWILIO_MAGIC.blockedNoRing;
}

/** Unique E.164 for CRM seed (avoids duplicate-phone errors on repeat runs). */
export function uniqueE2ePhone(suffix = Date.now() % 10_000): string {
  const custom = (process.env.E2E_TWILIO_TO || '').trim();
  if (custom) return custom;
  return `+1202555${String(suffix).padStart(4, '0').slice(-4)}`;
}

export function liveBaseUrl(): string {
  return (process.env.E2E_BASE_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');
}

export async function fetchNgrokHttpsUrl(): Promise<string | null> {
  try {
    const res = await fetch('http://127.0.0.1:4040/api/tunnels');
    if (!res.ok) return null;
    const body = (await res.json()) as { tunnels?: { public_url?: string }[] };
    const https = (body.tunnels || []).find((t) => String(t.public_url || '').startsWith('https://'));
    return https?.public_url?.replace(/\/$/, '') || null;
  } catch {
    return null;
  }
}

export type DialerPreflight = {
  ok: boolean;
  storage?: string;
  publicBaseUrl?: string;
  ngrokUrl?: string | null;
  publicUrlMatchesNgrok?: boolean;
  hasTwilio?: boolean;
  errors: string[];
};

export async function preflightDialer(request: APIRequestContext): Promise<DialerPreflight> {
  const errors: string[] = [];
  const token = managerAccessToken();
  if (!token) {
    errors.push('Set E2E_ACCESS_TOKEN (Supabase JWT) in .env for live dial tests.');
  }
  const ngrokUrl = await fetchNgrokHttpsUrl();
  const { response: healthRes, data: health } = await apiJson<{ ok?: boolean; storage?: string }>(
    request,
    'GET',
    '/api/health',
  );
  if (!healthRes.ok()) errors.push(`/api/health returned ${healthRes.status()}.`);
  const { response: settingsRes, data: settings } = await apiJson<{
    public_base_url?: string;
    account_sid?: string;
    has_auth_token?: boolean;
    has_api_secret?: boolean;
    twiml_app_sid?: string;
    api_key?: string;
  }>(request, 'GET', '/api/settings');
  if (!settingsRes.ok()) {
    errors.push(`/api/settings returned ${settingsRes.status()} (sign-in required).`);
  }
  const publicBaseUrl = (settings?.public_base_url || '').replace(/\/$/, '');
  const hasTwilio = Boolean(
    settings?.account_sid
    && settings?.api_key
    && settings?.twiml_app_sid
    && settings?.has_auth_token
    && settings?.has_api_secret,
  );
  if (!hasTwilio) errors.push('Twilio settings incomplete (account, API key, TwiML app, secrets).');
  if (!publicBaseUrl.startsWith('https://')) {
    errors.push('PUBLIC_BASE_URL must be https (set to your ngrok URL in Settings).');
  }
  const publicUrlMatchesNgrok = Boolean(ngrokUrl && publicBaseUrl && publicBaseUrl === ngrokUrl);
  if (ngrokUrl && publicBaseUrl && !publicUrlMatchesNgrok) {
    errors.push(`PUBLIC_BASE_URL (${publicBaseUrl}) does not match ngrok (${ngrokUrl}). Twilio hooks will miss the server.`);
  }
  return {
    ok: errors.length === 0,
    storage: health?.storage,
    publicBaseUrl,
    ngrokUrl,
    publicUrlMatchesNgrok,
    hasTwilio,
    errors,
  };
}

export async function seedDialableProspect(
  request: APIRequestContext,
  phone: string,
  contactName = 'E2E Twilio Prospect',
): Promise<{ id: string; phone: string }> {
  const { response, data } = await apiJson<{
    lead?: { id?: string; phone?: string };
    error?: string;
  }>(
    request,
    'POST',
    '/api/leads',
    {
      contact_name: contactName,
      company: 'E2E Twilio Co',
      phone,
      timezone: 'Eastern',
      status: 'new',
    },
  );
  if (!response.ok()) {
    throw new Error(data?.error || `POST /api/leads failed (${response.status()})`);
  }
  const lead = data?.lead;
  if (!lead?.id) throw new Error('POST /api/leads returned no lead.id');
  return { id: lead.id, phone: lead.phone || phone };
}

export type LiveSnapshot = {
  running?: boolean;
  agent_ready?: boolean;
  stage?: string;
  next_lead?: { id?: string; phone?: string };
  in_flight?: unknown[];
  active?: { lead_id?: string };
};

export async function pollLive(
  request: APIRequestContext,
  predicate: (live: LiveSnapshot) => boolean,
  timeoutMs = 120_000,
  intervalMs = 1500,
): Promise<LiveSnapshot> {
  const deadline = Date.now() + timeoutMs;
  let last: LiveSnapshot = {};
  while (Date.now() < deadline) {
    const { response, data } = await apiJson<LiveSnapshot>(request, 'GET', '/api/live');
    if (response.ok() && data) {
      last = data;
      if (predicate(data)) return data;
    }
    await new Promise((r) => setTimeout(r, intervalMs));
  }
  return last;
}

export function refreshAccessToken(): string {
  return (process.env.E2E_REFRESH_TOKEN || '').trim();
}

export async function openDialerForLiveVoice(page: Page): Promise<void> {
  await page.context().grantPermissions(['microphone']);
  const accessToken = managerAccessToken();
  if (!accessToken) {
    throw new Error('Run scripts/mint_e2e_access_token.py (writes E2E_ACCESS_TOKEN to .env).');
  }

  await page.goto('/', { waitUntil: 'networkidle' });
  const booted = await page.evaluate(async (token) => {
    try {
      const { S } = await import('/core.js');
      S.googleAuthEnabled = true;
      S.accessToken = token;
      const { hideLoginGate, refreshAccountContext, bootApp } = await import('/features/auth.js');
      hideLoginGate();
      await refreshAccountContext();
      await bootApp();
      return { ok: true };
    } catch (error) {
      return { ok: false, message: error instanceof Error ? error.message : String(error) };
    }
  }, accessToken);
  if (!booted.ok) {
    throw new Error(`Could not boot signed-in shell: ${booted.message || 'unknown'}`);
  }
  await expectAppReady(page);
  const dialerTab = page.locator('#dialerTabButton');
  if (await dialerTab.isVisible()) await dialerTab.click();
}

export async function startDialingFromUi(page: Page): Promise<void> {
  const start = page.locator('#startButton').first();
  await start.waitFor({ state: 'visible', timeout: 15_000 });
  await start.click();
}

export async function stopDialingFromUi(page: Page): Promise<void> {
  const stop = page.locator('#stopButton').first();
  if (await stop.isVisible()) {
    await stop.click({ timeout: 5_000 }).catch(() => {});
  }
  const token = managerAccessToken();
  await page.evaluate(async (accessToken) => {
    const headers: Record<string, string> = {};
    if (accessToken) headers.Authorization = `Bearer ${accessToken}`;
    await fetch('/api/stop', { method: 'POST', headers });
  }, token).catch(() => {});
}