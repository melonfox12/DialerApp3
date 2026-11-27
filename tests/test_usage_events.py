import unittest
import uuid
from unittest.mock import MagicMock, patch

from features import usage_events


class UsageEventsTests(unittest.TestCase):
    def test_record_skips_without_client(self):
        dialer = MagicMock()
        dialer.account_user_id = "u1"
        dialer.org_membership = {"org_id": "o1"}
        dialer.crm = MagicMock(client=None)
        with patch.object(usage_events.org_storage, "insert_usage_event") as insert:
            usage_events.record(dialer, "session_start", {})
            insert.assert_not_called()

    def test_record_writes_event(self):
        dialer = MagicMock()
        dialer.account_user_id = "u1"
        dialer.org_membership = {"org_id": "o1"}
        client = MagicMock()
        dialer.crm = MagicMock(client=client)
        with patch.object(usage_events.org_storage, "insert_usage_event") as insert:
            usage_events.record(dialer, "session_start", {"queue_total": 3})
            insert.assert_called_once_with(client, "o1", "u1", "session_start", {"queue_total": 3})

    def test_maybe_record_stage_dedupes(self):
        dialer = MagicMock()
        dialer._usage_last_stage = "idle"
        with patch.object(usage_events, "record") as record:
            usage_events.maybe_record_stage(dialer, "idle")
            record.assert_not_called()
            usage_events.maybe_record_stage(dialer, "connected")
            record.assert_called_once()
            self.assertEqual(dialer._usage_last_stage, "connected")

    def test_tab_focus_throttled(self):
        dialer = MagicMock()
        dialer._usage_tab_at = 1e9
        with patch.object(usage_events, "record") as record:
            usage_events.record_tab_focus(dialer, "dialer")
            record.assert_not_called()


if __name__ == "__main__":
    unittest.main()