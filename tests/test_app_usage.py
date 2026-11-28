import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

from features import app_usage, team
from shared.vocabulary import APP_SESSION_GAP_SECONDS, TEAM_ONLINE_SECONDS, TEAM_PRESENCE_WRITE_SECONDS


class AppUsageLogicTests(unittest.TestCase):
    def test_apply_tick_accumulates_capped(self):
        state = app_usage.empty_state()
        app_usage.apply_tick(state, delta_seconds=12)
        self.assertEqual(state["app_today_seconds"], 12)
        self.assertEqual(state["app_week_seconds"], 12)
        self.assertEqual(state["app_month_seconds"], 12)
        self.assertEqual(state["app_session_seconds"], 12)
        app_usage.apply_tick(state, delta_seconds=99)
        self.assertEqual(state["app_today_seconds"], 12 + 15)
        self.assertEqual(state["app_week_seconds"], 12 + 15)

    def test_apply_tick_resets_session_after_offline_gap(self):
        now = datetime.now(timezone.utc)
        stale = now - timedelta(seconds=APP_SESSION_GAP_SECONDS + 5)
        today = app_usage.utc_today()
        state = {
            "app_today_date": today.isoformat(),
            "app_today_seconds": 120,
            "app_week_key": app_usage.utc_week_key(today),
            "app_week_seconds": 200,
            "app_month_key": app_usage.utc_month_key(today),
            "app_month_seconds": 400,
            "app_session_seconds": 90,
            "app_session_started_at": stale.isoformat(),
            "last_seen_at": stale.isoformat(),
        }
        app_usage.apply_tick(state, delta_seconds=10, now=now, online_gap_seconds=APP_SESSION_GAP_SECONDS + 5)
        self.assertEqual(state["app_session_seconds"], 10)
        self.assertEqual(state["app_today_seconds"], 130)
        self.assertEqual(state["app_week_seconds"], 210)
        self.assertEqual(state["app_month_seconds"], 410)

    def test_state_from_presence_resets_stale_session(self):
        now = datetime.now(timezone.utc)
        stale = (now - timedelta(seconds=APP_SESSION_GAP_SECONDS + 30)).isoformat()
        row = {
            "app_today_date": app_usage.utc_today().isoformat(),
            "app_today_seconds": 40,
            "app_session_seconds": 40,
            "app_session_started_at": stale,
            "last_seen_at": stale,
        }
        state = app_usage.state_from_presence(row, now=now)
        self.assertEqual(state["app_session_seconds"], 0)

    def test_public_app_usage_includes_live_extra(self):
        state = app_usage.empty_state()
        state["app_today_seconds"] = 60
        state["app_week_seconds"] = 100
        state["app_month_seconds"] = 500
        state["app_session_seconds"] = 30
        payload = app_usage.public_app_usage(state, live_extra_seconds=8)
        self.assertEqual(payload["app_seconds_today"], 68)
        self.assertEqual(payload["app_seconds_week"], 108)
        self.assertEqual(payload["app_seconds_month"], 508)
        self.assertEqual(payload["app_seconds_session"], 38)

    def test_apply_tick_records_pending_browser_session_close(self):
        now = datetime.now(timezone.utc)
        state = app_usage.empty_state(now=now)
        app_usage.apply_tick(state, delta_seconds=60, now=now)
        gap_at = now + timedelta(seconds=APP_SESSION_GAP_SECONDS + 1)
        app_usage.apply_tick(state, delta_seconds=5, now=gap_at, online_gap_seconds=APP_SESSION_GAP_SECONDS + 1)
        pending = app_usage.pop_pending_browser_session_close(state)
        self.assertIsNotNone(pending)
        self.assertEqual(pending["seconds"], 15)
        self.assertEqual(state["app_session_seconds"], 5)

    def test_state_from_presence_pending_after_gap(self):
        now = datetime.now(timezone.utc)
        stale = (now - timedelta(seconds=APP_SESSION_GAP_SECONDS + 10)).isoformat()
        row = {
            "app_today_date": app_usage.utc_today().isoformat(),
            "app_today_seconds": 100,
            "app_week_key": app_usage.utc_week_key(),
            "app_week_seconds": 100,
            "app_month_key": app_usage.utc_month_key(),
            "app_month_seconds": 100,
            "app_session_seconds": 240,
            "app_session_started_at": stale,
            "last_seen_at": stale,
        }
        state = app_usage.state_from_presence(row, now=now)
        self.assertEqual(state["app_session_seconds"], 0)
        self.assertIn("_pending_browser_session_close", state)
        self.assertEqual(state["_pending_browser_session_close"]["seconds"], 240)

    def test_merged_usage_state_keeps_stored_totals(self):
        today = app_usage.utc_today()
        presence = {
            "app_today_date": today.isoformat(),
            "app_today_seconds": 3600,
            "app_week_key": app_usage.utc_week_key(today),
            "app_week_seconds": 7200,
            "app_month_key": app_usage.utc_month_key(today),
            "app_month_seconds": 14400,
            "app_session_seconds": 400,
            "last_seen_at": app_usage.utc_now().isoformat(),
        }
        dialer = MagicMock()
        dialer._team_presence_at = 0
        dialer._app_usage_state = app_usage.empty_state()
        app_usage.apply_tick(dialer._app_usage_state, delta_seconds=360)
        payload = app_usage.app_usage_for_view(presence, dialer)
        self.assertGreaterEqual(payload["app_seconds_today"], 3600)
        self.assertGreaterEqual(payload["app_seconds_week"], 7200)
        self.assertGreaterEqual(payload["app_seconds_month"], 14400)
        self.assertEqual(payload["app_seconds_session"], 15)

    def test_week_rollover_clears_stale_bucket(self):
        today = app_usage.utc_today()
        row = {
            "app_week_key": "1999-W01",
            "app_week_seconds": 999,
            "app_month_key": app_usage.utc_month_key(today),
            "app_month_seconds": 10,
            "app_today_date": today.isoformat(),
            "app_today_seconds": 5,
            "last_seen_at": app_usage.utc_now().isoformat(),
        }
        state = app_usage.state_from_presence(row)
        self.assertEqual(state["app_week_seconds"], 0)
        self.assertEqual(state["app_month_seconds"], 10)


class BrowserLiveAccountTests(unittest.TestCase):
    def test_stale_server_session_not_online(self):
        from datetime import timedelta

        from features import team
        from features.accounts import Account

        now = datetime.now(timezone.utc)
        stale = (now - timedelta(seconds=TEAM_ONLINE_SECONDS + 10)).isoformat()
        dialer = MagicMock()
        account = Account(MagicMock(), MagicMock(), dialer, MagicMock(), MagicMock())
        account.last_client_at = stale
        dialer.account_user_id = "rep-1"
        runtime = MagicMock()
        runtime.sessions = {"rep-1": account}
        self.assertIsNone(team._browser_live_account(runtime, "rep-1"))


class MaybeRecordPresenceTests(unittest.TestCase):
    def test_maybe_record_presence_ticks_app_usage(self):
        dialer = MagicMock()
        dialer.account_user_id = "u1"
        dialer.org_membership = {"org_id": "o1"}
        dialer._team_presence_at = 0
        dialer._app_usage_state = None
        runtime = MagicMock()
        runtime.client = MagicMock()
        with patch.object(team.org_storage, "get_presence", return_value=None):
            with patch.object(team.org_storage, "upsert_presence") as upsert:
                team.maybe_record_presence(runtime, dialer, {"stage": "idle", "running": False})
                self.assertIsNotNone(dialer._app_usage_state)
                upsert.assert_called_once()
                body = upsert.call_args[0][3]
                self.assertIn("app_today_seconds", body)

    def test_maybe_record_presence_throttled(self):
        dialer = MagicMock()
        dialer.account_user_id = "u1"
        dialer.org_membership = {"org_id": "o1"}
        dialer._team_presence_at = 1000.0
        runtime = MagicMock()
        runtime.client = MagicMock()
        live = {"stage": "idle"}
        with patch.object(team, "time") as mock_time:
            mock_time.monotonic.return_value = 1000.0 + TEAM_PRESENCE_WRITE_SECONDS - 1
            with patch.object(team.org_storage, "upsert_presence") as upsert:
                team.maybe_record_presence(runtime, dialer, live)
                upsert.assert_not_called()


if __name__ == "__main__":
    unittest.main()