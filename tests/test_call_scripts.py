import tempfile
import unittest
from pathlib import Path

from features.call_scripts import CallScriptsStore, panel_payload
from shared.vocabulary import DEFAULT_CALL_SCRIPT_INDUSTRY, DEFAULT_CALL_SCRIPT_PROSPECT_TYPE, DEFAULT_CALL_SCRIPT_VARIATION


class CallScriptsTests(unittest.TestCase):
    def test_local_script_round_trip_and_prefs(self):
        with tempfile.TemporaryDirectory() as directory:
            store = CallScriptsStore(crm_path=Path(directory) / "crm.json")
            store.save_prefs(None, "medical", "gatekeeper", 2)
            store.save_body(None, "medical", "gatekeeper", 2, "Hello gatekeeper v2")
            store.save_body(None, "dental", "decision_maker", 1, "Hello DM dental v1")
            prefs = store.load_prefs(None)
            self.assertEqual(prefs["industry"], "medical")
            self.assertEqual(prefs["prospect_type"], "gatekeeper")
            self.assertEqual(prefs["variation"], 2)
            self.assertEqual(store.load_body(None, "medical", "gatekeeper", 2), "Hello gatekeeper v2")
            self.assertEqual(store.load_body(None, "dental", "decision_maker", 1), "Hello DM dental v1")
            self.assertEqual(store.load_body(None, "dental", "decision_maker", 3), "")
            payload = panel_payload(store, None)
            self.assertEqual(payload["industry"], "medical")
            self.assertEqual(payload["prospect_type"], "gatekeeper")
            self.assertEqual(payload["variation"], 2)
            self.assertEqual(payload["body"], "Hello gatekeeper v2")
            self.assertEqual(len(payload["variations"]), 3)

    def test_default_selection_is_first_alphabetical(self):
        with tempfile.TemporaryDirectory() as directory:
            store = CallScriptsStore(crm_path=Path(directory) / "crm.json")
            payload = panel_payload(store, None)
            self.assertEqual(payload["industry"], DEFAULT_CALL_SCRIPT_INDUSTRY)
            self.assertEqual(payload["prospect_type"], DEFAULT_CALL_SCRIPT_PROSPECT_TYPE)
            self.assertEqual(payload["variation"], DEFAULT_CALL_SCRIPT_VARIATION)

    def test_legacy_local_key_maps_to_variation_one(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "call_scripts.json"
            path.write_text(
                '{"industry":"daycare","prospect_type":"decision_maker","scripts":{"daycare|decision_maker":"Legacy script"}}',
                encoding="utf-8",
            )
            store = CallScriptsStore(crm_path=path)
            self.assertEqual(store.load_body(None, "daycare", "decision_maker", 1), "Legacy script")
            self.assertEqual(store.load_body(None, "daycare", "decision_maker", 2), "")