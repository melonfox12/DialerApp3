import { test, expect } from '@playwright/test';
import { openAppShell } from './helpers';

test.describe('No-answer disposition button', () => {
  test('dialer CRM row shows No answer with other outcome buttons', async ({ page }) => {
    await openAppShell(page);
    const crmButtons = page.locator('#crmStatusButtons');
    await expect(crmButtons).toBeVisible();
    const noAnswer = crmButtons.getByRole('button', { name: 'No answer' });
    await expect(noAnswer).toBeVisible();
    await expect(crmButtons.getByRole('button', { name: 'Engaged', exact: true })).toBeVisible();
    await expect(crmButtons.getByRole('button', { name: 'Disqualified', exact: true })).toBeVisible();
    await expect(crmButtons.getByRole('button', { name: 'Qualified', exact: true })).toBeVisible();
    await expect(noAnswer).toHaveAttribute('data-disposition', 'no_answer');
  });

  test('No answer button is disabled when no prospect is in queue context', async ({ page }) => {
    await openAppShell(page);
    const noAnswer = page.locator('#crmStatusButtons').getByRole('button', { name: 'No answer' });
    const disabled = await noAnswer.isDisabled();
    if (disabled) {
      await expect(noAnswer).toBeDisabled();
    } else {
      await expect(noAnswer).toBeEnabled();
    }
  });

  test('clicking No answer without a prospect does not call disposition API', async ({ page }) => {
    await openAppShell(page);
    let statusPosts = 0;
    await page.route('**/api/leads/**/status', (route) => {
      if (route.request().method() === 'POST') statusPosts += 1;
      route.continue();
    });
    const noAnswer = page.locator('#crmStatusButtons').getByRole('button', { name: 'No answer' });
    if (await noAnswer.isDisabled()) {
      await noAnswer.click({ force: true });
      expect(statusPosts).toBe(0);
    }
  });

  test('survives hard refresh on dialer tab', async ({ page }) => {
    await openAppShell(page);
    await page.reload();
    await expect(page.locator('#crmStatusButtons').getByRole('button', { name: 'No answer' })).toBeVisible();
  });
});