import { test, expect } from '@playwright/test';
import { authHeaders, hasManagerAccess, openAppShell } from './helpers';

test.describe('Team member live detail', () => {
  test('team tab is hidden for local non-manager shell', async ({ page }) => {
    await openAppShell(page);
    await expect(page.locator('#teamTabButton')).toBeHidden();
  });

  test('team panel is not reachable without manager chrome', async ({ page }) => {
    await openAppShell(page);
    await expect(page.locator('#teamPanel')).toBeHidden();
  });

  test('manager can open team and member detail', async ({ page, context }) => {
    test.skip(!hasManagerAccess(), 'Set E2E_ACCESS_TOKEN and E2E_SERVER=existing for Supabase manager tests');
    await context.setExtraHTTPHeaders(authHeaders());
    await openAppShell(page);
    await page.locator('#sideFolderHead-misc').click();
    const teamTab = page.locator('#teamTabButton');
    await expect(teamTab).toBeVisible({ timeout: 15_000 });
    await teamTab.click();
    await expect(page.locator('#teamTable')).toBeVisible();
    await expect.poll(async () => page.locator('#teamTableBody tr').count(), { timeout: 30_000 }).toBeGreaterThan(0);
    const firstRow = page.locator('#teamTableBody tr').first();
    await firstRow.click();
    await expect(page.locator('#teamMemberDetail')).toBeVisible();
    await expect(page.locator('#teamMemberDetailBody')).toContainText(/Updated|Live|Last seen/i);
  });
});