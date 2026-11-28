import { test, expect } from '@playwright/test';
import {
  dialToNumber,
  uniqueE2ePhone,
  openDialerForLiveVoice,
  pollLive,
  preflightDialer,
  seedDialableProspect,
  startDialingFromUi,
  stopDialingFromUi,
  twilioLiveEnabled,
  TWILIO_MAGIC,
} from './twilio-live-helpers';
import { managerAccessToken } from './helpers';

test.describe.configure({ mode: 'serial', timeout: 300_000 });

test.describe('Twilio live dial (ngrok + Voice SDK)', () => {
  test.beforeEach(async ({ request }, testInfo) => {
    test.skip(
      !twilioLiveEnabled(),
      'Set E2E_TWILIO_LIVE=1 and run against your dialer on :8000 with ngrok + Twilio in Settings.',
    );
    test.skip(
      !managerAccessToken(),
      'Set E2E_ACCESS_TOKEN in repo .env (Supabase JWT for a manager/owner).',
    );
    testInfo.annotations.push({
      type: 'twilio-to',
      description: dialToNumber(),
    });
    await request.post('/api/stop', { data: {} }).catch(() => {});
  });

  test('preflight: health, Twilio settings, ngrok PUBLIC_BASE_URL', async ({ request }) => {
    const pre = await preflightDialer(request);
    if (!pre.ok) {
      // Document misconfig as test failure with actionable list (common dialer bug: stale ngrok URL).
      expect(pre.errors, pre.errors.join('\n')).toEqual([]);
    }
    expect(pre.storage).toBeTruthy();
    expect(pre.hasTwilio).toBe(true);
    expect(pre.publicBaseUrl).toMatch(/^https:\/\//);
  });

  test('rep flow: seed prospect, start dialing, reach agent leg or surfaced error', async ({
    page,
    request,
  }) => {
    const pre = await preflightDialer(request);
    test.skip(!pre.ok, `Preflight failed:\n${pre.errors.join('\n')}`);

    const prospect = await seedDialableProspect(request, uniqueE2ePhone());
    expect(prospect.phone).toMatch(/^\+/);

    await openDialerForLiveVoice(page);

    const liveBefore = await pollLive(request, () => true, 5_000, 500);
    expect(liveBefore.running).toBeFalsy();

    await startDialingFromUi(page);

    const toast = page.locator('.toast, [role="alert"]').first();
    const agentReadyDeadline = Date.now() + 90_000;
    let agentReady = false;
    let lastLive: Awaited<ReturnType<typeof pollLive>> = {};

    while (Date.now() < agentReadyDeadline) {
      const { data: live } = await (async () => {
        const res = await request.get('/api/live', {
          headers: { Authorization: `Bearer ${managerAccessToken()}` },
        });
        return { data: res.ok() ? ((await res.json()) as typeof lastLive) : {} };
      })();
      lastLive = live || {};
      if (live?.running && live?.agent_ready) {
        agentReady = true;
        break;
      }
      if (await toast.isVisible().catch(() => false)) {
        const text = (await toast.textContent()) || '';
        if (/could not start|credentials|public|caller id|microphone|audio|not supported/i.test(text)) {
          await stopDialingFromUi(page);
          throw new Error(`Start dialing failed in UI: ${text}`);
        }
      }
      await page.waitForTimeout(1500);
    }

    const lastErr = (lastLive as { activity_log?: { message?: string }[] }).activity_log
      ?.map((row) => row.message)
      .find((msg) => /error|failed|secret|credentials/i.test(msg || ''));
    expect(
      agentReady,
      lastErr || `Voice agent never became ready. See activity_log in trace.`,
    ).toBe(true);

  const prospectInQueue =
      lastLive.next_lead?.id === prospect.id
      || lastLive.next_lead?.phone === prospect.phone;

    const afterStart = await pollLive(
      request,
      (live) => Boolean(
        live.in_flight?.length
        || live.active?.lead_id
        || live.stage === 'ringing'
        || live.stage === 'connected'
        || live.stage === 'dialing',
      ),
      45_000,
    );

    if (!prospectInQueue && !afterStart.in_flight?.length) {
      // Possible bug: pool filter / recent dial window excluded seeded lead — note in assertion message.
      expect(
        afterStart.in_flight?.length || afterStart.active?.lead_id,
        `Expected outbound leg after start; next_lead=${JSON.stringify(afterStart.next_lead)}`,
      ).toBeTruthy();
    }

    await stopDialingFromUi(page);
    const stopped = await pollLive(request, (live) => !live.running, 30_000);
    expect(stopped.running).toBeFalsy();
  });

  test('invalid magic To surfaces without crashing session', async ({ request, page }) => {
    const pre = await preflightDialer(request);
    test.skip(!pre.ok, `Preflight failed:\n${pre.errors.join('\n')}`);

    await seedDialableProspect(request, TWILIO_MAGIC.invalidTo, 'E2E Invalid Twilio To');

    await openDialerForLiveVoice(page);
    await startDialingFromUi(page);

    await pollLive(request, (live) => live.running === true, 60_000);
    const withActivity = await pollLive(
      request,
      (live) => Boolean(live.in_flight?.length) || live.stage === 'idle' || !live.agent_ready,
      60_000,
    );

    await stopDialingFromUi(page);
    expect(withActivity).toBeTruthy();
  });
});