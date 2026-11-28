import unittest
from datetime import datetime, timezone, timedelta

from features import script_analytics


class ScriptAnalyticsTests(unittest.TestCase):
    def test_aggregate_groups_by_script_key(self):
        now = datetime.now(timezone.utc)
        records = [
            {
                "at": now,
                "connected": True,
                "duration": 60,
                "transcript_lines": 2,
                "answered_by": "human",
                "outcome": "call_back",
                "script_industry": "dental",
                "script_prospect_type": "gatekeeper",
                "script_variation": 1,
            },
            {
                "at": now - timedelta(hours=1),
                "connected": False,
                "duration": 0,
                "transcript_lines": 0,
                "answered_by": "no_answer",
                "outcome": None,
                "script_industry": "dental",
                "script_prospect_type": "gatekeeper",
                "script_variation": 1,
            },
        ]
        start = now - timedelta(days=7)
        end = now
        segments = script_analytics.aggregate_segments(records, start, end)
        self.assertEqual(len(segments), 1)
        self.assertEqual(segments[0]["counts"]["dials"], 2)
        self.assertEqual(segments[0]["counts"]["connected"], 1)
        self.assertEqual(segments[0]["by_outcome"].get("call_back"), 1)


if __name__ == "__main__":
    unittest.main()