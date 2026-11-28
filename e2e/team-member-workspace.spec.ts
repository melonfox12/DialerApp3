import { test, expect } from '@playwright/test';

const MEMBER_ID = 'rep-user-1';

const roster = {
  org_id: 'org-e2e',
  org_name: 'E2E Team',
  members: [
    {
      user_id: MEMBER_ID,
      email: 'rep@example.test',
      display_name: 'Rep One',
      role: 'rep',
      status: 'active',
      online: true,
      presence: { stage: 'dialing', running: true },
      app_usage: { app_minutes_session: 5, app_minutes_today: 40, app_minutes_week: 120, app_minutes_month: 400 },
      today: { dials: 25, connected: 4, booked: 1 },
    },
  ],
};

const analytics = {
  user_id: MEMBER_ID,
  span: 'today',
  timeline: 'week',
  usage_summary: {
    live_session_minutes: 5,
    today_minutes: 40,
    week_minutes: 120,
    month_minutes: 400,
    live_online: true,
  },
  activity_bars: { dials: 25, connected: 4, conversations_30s: 3 },
  dispositions: [
    { key: 'booked', label: 'booked', count: 1 },
    { key: 'call_back', label: 'call back', count: 2 },
  ],
  activity_line: [
    { t: '2026-11-27', value: 10 },
    { t: '2026-11-28', value: 25 },
  ],
};

async function bootShellWithoutGoogleToken(page) {
  await page.route('**/api/auth/config', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ google: false, url: '', anonKey: '' }),
    });
  });
  await page.goto('/');
  await page.locator('#loginGate').waitFor({ state: 'hidden', timeout: 45_000 });
  await page.locator('.app-shell').waitFor({ state: 'visible' });
}

test.describe('Team member workspace', () => {
  test('manager workspace shows analytics tabs and member settings API section', async ({ page }) => {
    await page.route(/\/api\/team\/roster/, async (route) => {
      await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(roster) });
    });
    await page.route('**/api/auth/me', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          id: 'owner-1',
          email: 'owner@example.test',
          role: 'owner',
          org_id: 'org-e2e',
          can_manage_team: true,
        }),
      });
    });
    await page.route(`**/api/team/members/${MEMBER_ID}/live`, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          user_id: MEMBER_ID,
          online: true,
          stage: 'dialing',
          running: true,
          active_lead_name: 'Ada Shop',
        }),
      });
    });
    await page.route(`**/api/team/members/${MEMBER_ID}/analytics**`, async (route) => {
      await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify(analytics) });
    });
    await page.route(`**/api/team/members/${MEMBER_ID}/usage**`, async (route) => {
      await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ events: [], minutes: 60 }) });
    });
    await page.route(`**/api/team/members/${MEMBER_ID}/scripts/**`, async (route) => {
      await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ segments: [] }) });
    });
    await page.route(new RegExp(`/api/team/members/${MEMBER_ID}/settings$`), async (route) => {
      if (route.request().method() === 'GET') {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            user_id: MEMBER_ID,
            session_goal: 20,
            conversation_threshold: 30,
            auto_advance_delay: 2,
            account_sid: 'ACmanaged',
            has_auth_token: true,
            api_key: 'SKmanaged',
            has_api_secret: true,
            twiml_app_sid: 'APmanaged',
            public_base_url: 'https://managed.example',
            managed_by_viewer: true,
          }),
        });
        return;
      }
      await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ ok: true }) });
    });

    await bootShellWithoutGoogleToken(page);
    await page.evaluate(async () => {
      const { S, render } = await import('/static/core.js');
      S.canManageTeam = true;
      S.orgRole = 'owner';
      const { syncTeamChrome } = await import('/static/features/team.js');
      syncTeamChrome();
      render();
    });
    await page.locator('#sideFolderHead-misc').click();
    await expect(page.locator('#teamTabButton')).toBeVisible();
    await page.evaluate(async () => {
      const { setDashboardTab } = await import('/static/_core/navigation.js');
      setDashboardTab('team');
    });
    await expect.poll(async () => page.locator('#teamTableBody tr').count(), { timeout: 15_000 }).toBeGreaterThan(0);
    await page.locator('#teamTableBody tr').first().click();
    await expect(page.locator('#teamMemberDetail')).toBeVisible();
    await expect(page.locator('#pageTitle .page-title-trail')).toContainText('info');
    await expect(page.locator('#pageTitle .page-title-link')).toHaveText('Team');
    await expect(page.locator('#teamMemberSettingsPanel')).toBeHidden();
    await expect(page.locator('#teamMemberAnalyticsPanel')).toBeVisible();
    await expect(page.locator('#teamSetAccountSid')).toBeHidden();
    await expect(page.locator('#teamMemberUsageRow .team-usage-card')).toHaveCount(4);
    const usageValues = page.locator('#teamMemberUsageRow .team-usage-card-value');
    await expect(usageValues.nth(0)).toHaveText('5 min');
    await expect(usageValues.nth(1)).toHaveText('40 min');
    await expect(usageValues.nth(2)).toHaveText('120 min');
    await expect(usageValues.nth(3)).toHaveText('400 min');
    await expect(page.locator('#teamMemberChartHost svg')).toBeVisible();
    await page.locator('#teamMemberTabSettings').click();
    await expect(page.locator('#teamMemberSettingsPanel')).toBeVisible();
    await expect(page.locator('#teamMemberSettingsBody')).toContainText('Twilio Account SID');
    await page.locator('#teamMemberTabAnalytics').click();
    await expect(page.locator('#teamMemberSettingsPanel')).toBeHidden();
    await page.locator('[data-chart-view="dispositions"]').click();
    await expect(page.locator('#teamMemberChartHost svg')).toBeVisible();
    await page.locator('#teamMemberDetailClose').click();
    await expect(page.locator('#teamMemberDetail')).toBeHidden();
    await expect(page.locator('#teamRosterView')).toBeVisible();
    await expect.poll(async () => page.evaluate(() => localStorage.getItem('prospect-desk-team-member'))).toBeNull();
  });

  test('rep settings response hides credential section flag', async ({ page }) => {
    await page.route(/\/api\/settings$/, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          session_goal: 20,
          conversation_threshold: 30,
          auto_advance_delay: 2,
          credentials_managed_by_org: true,
          can_edit_credentials: false,
          sounds_enabled: true,
          sound_volume: 35,
          calling_start_hour: 9,
          calling_end_hour: 17,
          break_nudge_minutes: 45,
          opening_script: '',
          ai_llm_model: 'gpt-4o-mini',
        }),
      });
    });
    await bootShellWithoutGoogleToken(page);
    await page.locator('#settingsButton').click();
    await expect(page.locator('.settings-api-stack')).toBeHidden();
    await expect(page.locator('#settingsRepCredentialNote')).toContainText(/managed by your organization/i);
  });
});