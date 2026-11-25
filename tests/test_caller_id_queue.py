import tempfile
import unittest
from pathlib import Path

from features._dialer.caller_id_queue import (
    LocalCallerIdQueueStore,
    build_caller_id_queue_view,
)
from features._dialer.state import DialerState
from features.prospects import ProspectStore
from shared.vocabulary import DEFAULT_CALLER_ID_POOL


class CallerIdQueueTests(unittest.TestCase):
    def test_local_dequeue_rotates_to_back(self):
        with tempfile.TemporaryDirectory() as directory:
            store = LocalCallerIdQueueStore(Path(directory) / "crm.json")
            store.ensure_pool("local")
            first = store.dequeue("local")
            second = store.dequeue("local")
            ordered = store.list_ordered("local")
            self.assertEqual(first, DEFAULT_CALLER_ID_POOL[0])
            self.assertEqual(second, DEFAULT_CALLER_ID_POOL[1])
            self.assertEqual(ordered[0], DEFAULT_CALLER_ID_POOL[2])
            self.assertEqual(ordered[-2:], [first, second])

    def test_queue_view_statuses(self):
        ordered = list(DEFAULT_CALLER_ID_POOL)
        view = build_caller_id_queue_view(
            ordered,
            in_use=[ordered[3]],
            dialing_active=True,
        )
        self.assertEqual(view["in_use"], [ordered[3]])
        self.assertEqual(view["up_next"][:3], ordered[:3])
        statuses = {row["phone"]: row["status"] for row in view["rows"]}
        self.assertEqual(statuses[ordered[3]], "in_use")
        for phone in view["up_next"]:
            self.assertEqual(statuses[phone], "up_next")

    def test_dialer_attaches_local_store_via_accounts_pattern(self):
        with tempfile.TemporaryDirectory() as directory:
            crm = ProspectStore(Path(directory) / "crm.json")
            dialer = DialerState(crm, str(Path(directory) / ".env"))
            dialer.caller_id_queue_store = LocalCallerIdQueueStore(Path(directory) / "crm.json")
            dialer.running = True
            call = {"kind": "prospect", "caller_id": DEFAULT_CALLER_ID_POOL[0]}
            dialer.in_flight = {"a": call}
            from features._dialer.caller_id_queue import public_queue_view

            view = public_queue_view(dialer)
            self.assertTrue(view["dialing_active"])
            self.assertEqual(view["in_use"], [DEFAULT_CALLER_ID_POOL[0]])