import json
import tempfile
import unittest
from pathlib import Path

from features._prospects.csv_import import build_manual_lead, parse_csv
from features.prospects import ProspectStore
from shared.vocabulary import PIPELINE_SEND_INFO_STEP
from tests.test_transcript_storage.fixtures import FakeSupabaseClient, prospect


class ManualProspectTests(unittest.TestCase):
    def test_local_add_normalizes_phone_and_keeps_columns(self):
        with tempfile.TemporaryDirectory() as directory:
            crm = ProspectStore(Path(directory) / "crm.json")
            lead = crm.add_lead({
                "contact_name": "Ada Lovelace",
                "company": "Analytical Engines",
                "phone": "(202) 555-0199",
                "timezone": "est",
                "status": "new",
                "email": "ada@example.com",
            })
            saved = ProspectStore(Path(directory) / "crm.json").snapshot()[0]
            self.assertEqual(lead["phone"], "+12025550199")
            self.assertEqual(saved["contact_name"], "Ada Lovelace")
            self.assertEqual(saved["company"], "Analytical Engines")
            self.assertEqual(saved["timezone"], "Eastern")
            self.assertEqual(saved["email"], "ada@example.com")
            self.assertEqual(saved["status"], "new")
            self.assertEqual(saved["transcript"], [])
            self.assertTrue(saved.get("id"))

    def test_field_update_normalizes_phone_and_keeps_other_data(self):
        with tempfile.TemporaryDirectory() as directory:
            crm = ProspectStore(Path(directory) / "crm.json")
            crm.leads = [prospect()]
            crm.save()
            updated = crm.update_fields("prospect-1", {
                "contact_name": "Ada Lovelace",
                "company": "Analytical Engines",
                "phone": "12025550199",
                "timezone": "pst",
                "score_reasons": "Call after 2",
            })
            self.assertEqual(updated["phone"], "+12025550199")
            self.assertEqual(updated["timezone"], "Pacific")
            self.assertEqual(updated["status"], "new")
            self.assertEqual(updated["transcript"], [])
            cleared = crm.update_fields("prospect-1", {"score_reasons": ""})
            self.assertEqual(cleared["score_reasons"], "")
            saved = ProspectStore(Path(directory) / "crm.json").snapshot()[0]
            self.assertEqual(saved["contact_name"], "Ada Lovelace")

    def test_send_info_status_places_pipeline_on_call_1_and_manual_step_sticks(self):
        with tempfile.TemporaryDirectory() as directory:
            crm = ProspectStore(Path(directory) / "crm.json")
            crm.leads = [prospect()]
            crm.save()
            updated = crm.set_status("prospect-1", "contact_engaged")
            self.assertEqual(updated["pipeline_step"], PIPELINE_SEND_INFO_STEP)
            moved = crm.set_pipeline_step("prospect-1", "email_1")
            self.assertEqual(moved["pipeline_step"], "email_1")
            crm.set_status("prospect-1", "dialed")
            back = crm.set_status("prospect-1", "contact_engaged")
            self.assertEqual(back["pipeline_step"], PIPELINE_SEND_INFO_STEP)

    def test_field_update_rejects_bad_and_duplicate_phones(self):
        with tempfile.TemporaryDirectory() as directory:
            crm = ProspectStore(Path(directory) / "crm.json")
            crm.leads = [prospect()]
            crm.save()
            crm.add_lead({"phone": "2025550188", "contact_name": "Grace"})
            with self.assertRaises(ValueError):
                crm.update_fields("prospect-1", {"phone": "not a phone"})
            with self.assertRaises(ValueError):
                crm.update_fields("prospect-1", {"phone": "2025550188"})
            saved = crm.snapshot()
            original = next(lead for lead in saved if lead["id"] == "prospect-1")
            self.assertEqual(original["phone"], "+12025550123")
            self.assertEqual(original["contact_name"], "Onyx")

    def test_csv_maps_prospect_schema_columns(self):
        sample = (
            "Business Type,Prospect,Company,State,City,Phone,Lead score,Signal,Lead tier\n"
            "HVAC,Mike,Mike Pest Control,CA,San Francisco,4155551234,142,Opened,B\n"
        )
        leads, info = parse_csv(sample)
        self.assertEqual(len(leads), 1)
        self.assertEqual(info["skipped"], 0)
        mike = leads[0]
        self.assertEqual(mike["contact_name"], "Mike")
        self.assertEqual(mike["category"], "HVAC")
        self.assertEqual(mike["company"], "Mike Pest Control")
        self.assertEqual(mike["state"], "CA")
        self.assertEqual(mike["city"], "San Francisco")
        self.assertEqual(mike["phone"], "+14155551234")
        self.assertEqual(mike["lead_score"], 142.0)
        self.assertEqual(mike["signal"], "Opened")
        self.assertEqual(mike["lead_tier"], "B")

    def test_csv_category_from_business_type_header(self):
        typed, _info = parse_csv(b"Business Type,Prospect,Company,Phone\nHVAC,Ada,Engines,2025550199\n")
        self.assertEqual(typed[0]["category"], "HVAC")
        default, _info = parse_csv(b"Prospect,Company,Phone\nAda,Engines,2025550199\n")
        self.assertEqual(default[0]["category"], "")

    def test_csv_state_and_city_columns(self):
        leads, _info = parse_csv(b"Name,Company,State,City,Phone\nAda,Engines,VA,Arlington,2025550199\n")
        lead = leads[0]
        self.assertEqual(lead["state"], "VA")
        self.assertEqual(lead["city"], "Arlington")
        self.assertEqual(lead["company"], "Engines")

    def test_editing_city_updates_lead(self):
        with tempfile.TemporaryDirectory() as directory:
            crm = ProspectStore(Path(directory) / "crm.json")
            crm.leads = [prospect()]
            crm.leads[0]["score_reasons"] = "VIP"
            crm.save()
            updated = crm.update_fields("prospect-1", {"city": "Paris", "state": "TX"})
            self.assertEqual(updated["city"], "Paris")
            self.assertEqual(updated["state"], "TX")
            self.assertEqual(updated["score_reasons"], "VIP")

    def test_duplicate_and_unusable_phone_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            crm = ProspectStore(Path(directory) / "crm.json")
            crm.leads = [prospect()]
            crm.save()
            with self.assertRaises(ValueError):
                crm.add_lead({"phone": prospect()["phone"], "contact_name": "Copy"})
            with self.assertRaises(ValueError):
                crm.add_lead({"phone": "not a phone", "contact_name": "Nope"})
            self.assertEqual(len(crm.snapshot()), 1)

    def test_callback_status_schedules_a_follow_up(self):
        lead = build_manual_lead({
            "phone": "2025550100",
            "status": "dialed",
        })
        self.assertEqual(lead["status"], "dialed")
        self.assertTrue(lead["scheduled_until"])

    def test_remove_archives_instead_of_deleting(self):
        with tempfile.TemporaryDirectory() as directory:
            crm = ProspectStore(Path(directory) / "crm.json")
            lead = crm.add_lead({"contact_name": "Ada", "phone": "2025550199"})
            crm.remove(lead["id"])
            self.assertEqual(crm.snapshot(), [])
            backend = ProspectStore(Path(directory) / "crm.json")
            stored = json.loads((Path(directory) / "crm.json").read_text(encoding="utf-8"))[0]
            self.assertTrue(stored.get("archived_at"))

    def test_supabase_add_inserts_one_prospect(self):
        client = FakeSupabaseClient(prospect(), user_id="user-a")
        crm = ProspectStore(client=client, user_id="user-a")
        lead = crm.add_lead({
            "contact_name": "Grace Hopper",
            "company": "Navy",
            "phone": "2025550188",
            "timezone": "Central",
            "email": "grace@navy.mil",
        })
        self.assertEqual(client.user_ids[lead["id"]], "user-a")
        saved = crm.snapshot()
        self.assertEqual(len(saved), 2)
        added = next(item for item in saved if item["id"] == lead["id"])
        self.assertEqual(added["phone"], "+12025550188")
        self.assertEqual(added["email"], "grace@navy.mil")

    def test_supabase_update_fields_writes_the_cache(self):
        client = FakeSupabaseClient(prospect(), user_id="user-a")
        crm = ProspectStore(client=client, user_id="user-a")
        updated = crm.update_fields("prospect-1", {"company": "Navy", "timezone": "Central"})
        self.assertEqual(updated["company"], "Navy")
        self.assertEqual(crm.snapshot()[0]["timezone"], "Central")
        self.assertEqual(client.leads["prospect-1"]["timezone"], "Central")


class FailingPatchClient(FakeSupabaseClient):
    def request(self, method, resource, params=None, payload=None, prefer=None):
        if method == "PATCH":
            raise OSError("Supabase HTTP 503")
        return super().request(method, resource, params, payload, prefer)


class SupabaseCacheTests(unittest.TestCase):
    def test_failed_write_leaves_the_cached_lead_unchanged(self):
        crm = ProspectStore(client=FailingPatchClient(prospect(), user_id="user-a"), user_id="user-a")
        self.assertEqual(crm.snapshot()[0]["status"], "new")
        with self.assertRaises(OSError):
            crm.set_status("prospect-1", "do_not_call")
        with self.assertRaises(OSError):
            crm.append_transcript("prospect-1", {"id": "s1", "speaker": "Agent", "text": "Hello"})
        with self.assertRaises(OSError):
            crm.append_call_log("prospect-1", {"id": "c1", "duration_seconds": 5})
        with self.assertRaises(OSError):
            crm.update_fields("prospect-1", {"contact_name": "Changed"})
        cached = crm.snapshot()[0]
        self.assertEqual(cached["contact_name"], "Onyx")
        self.assertEqual(cached["status"], "new")
        self.assertEqual(cached["transcript"], [])
        self.assertEqual(cached.get("call_log", []), [])

    def test_successful_write_updates_the_cache(self):
        client = FakeSupabaseClient(prospect(), user_id="user-a")
        crm = ProspectStore(client=client, user_id="user-a")
        crm.set_status("prospect-1", "do_not_call")
        crm.append_transcript("prospect-1", {"id": "s1", "speaker": "Agent", "text": "Hello"})
        cached = crm.snapshot()[0]
        self.assertEqual(cached["status"], "closed")
        self.assertEqual(cached["transcript"][0]["text"], "Hello")
        self.assertEqual(client.leads["prospect-1"]["status"], "closed")

    def test_csv_import_totals_match_between_backends(self):
        csv_body = b"Name,Phone\nBea,2025550112\nCy,2025550113\n"
        supabase = ProspectStore(client=FakeSupabaseClient(prospect()), user_id="user-a")
        with tempfile.TemporaryDirectory() as directory:
            local = ProspectStore(Path(directory) / "crm.json")
            local.leads = [prospect()]
            local.save()
            local_info = local.add_csv(csv_body)
        supabase_info = supabase.add_csv(csv_body)
        self.assertEqual(local_info["added"], 2)
        self.assertEqual(supabase_info["added"], 2)
        self.assertEqual(local_info["skipped"], supabase_info["skipped"])


class DialCapTests(unittest.TestCase):
    def test_fifth_call_log_entry_marks_no_answer_disqualified(self):
        with tempfile.TemporaryDirectory() as directory:
            crm = ProspectStore(Path(directory) / "crm.json")
            crm.leads = [prospect()]
            for index in range(4):
                crm.append_call_log("prospect-1", {"id": f"dial-{index}", "started_at": f"2026-01-0{index + 1}T12:00:00+00:00"})
            self.assertEqual(crm.snapshot()[0]["status"], "dialed")
            crm.append_call_log("prospect-1", {"id": "dial-4", "started_at": "2026-01-05T12:00:00+00:00"})
            self.assertEqual(crm.snapshot()[0]["status"], "closed")

    def test_connected_dial_does_not_trigger_no_answer_cap(self):
        with tempfile.TemporaryDirectory() as directory:
            crm = ProspectStore(Path(directory) / "crm.json")
            crm.leads = [prospect()]
            for index in range(5):
                crm.append_call_log(
                    "prospect-1",
                    {
                        "id": f"dial-{index}",
                        "started_at": f"2026-01-0{index + 1}T12:00:00+00:00",
                        "connected": index == 2,
                    },
                )
            self.assertEqual(crm.snapshot()[0]["status"], "dialed")

    def test_enforce_dial_caps_backfills_prospects_already_at_five_dials(self):
        with tempfile.TemporaryDirectory() as directory:
            crm = ProspectStore(Path(directory) / "crm.json")
            lead = prospect()
            lead["call_log"] = [
                {"id": "dial-1", "started_at": "2026-01-01T12:00:00+00:00"},
                {"id": "dial-2", "started_at": "2026-01-02T12:00:00+00:00"},
                {"id": "dial-3", "started_at": "2026-01-03T12:00:00+00:00"},
                {"id": "dial-4", "started_at": "2026-01-04T12:00:00+00:00"},
                {"id": "dial-5", "started_at": "2026-01-05T12:00:00+00:00"},
            ]
            crm.leads = [lead]
            result = crm.enforce_dial_caps()
            self.assertEqual(result["capped"], 1)
            self.assertEqual(crm.snapshot()[0]["status"], "closed")
            self.assertEqual(crm.enforce_dial_caps()["capped"], 0)

    def test_repair_resets_wrong_disqualified_without_live_contact(self):
        with tempfile.TemporaryDirectory() as directory:
            crm = ProspectStore(Path(directory) / "crm.json")
            lead = prospect()
            lead["status"] = "closed"
            lead["call_log"] = [{"id": "dial-1", "started_at": "2026-01-01T12:00:00+00:00"}]
            crm.leads = [lead]
            result = crm.enforce_dial_caps(repair_misclassified=True)
            self.assertEqual(result["to_new"], 1)
            self.assertEqual(crm.snapshot()[0]["status"], "new")

    def test_repair_keeps_disqualified_when_transcript_exists(self):
        with tempfile.TemporaryDirectory() as directory:
            crm = ProspectStore(Path(directory) / "crm.json")
            lead = prospect()
            lead["status"] = "closed"
            lead["transcript"] = [{"id": "s1", "speaker": "Agent", "text": "Hi", "timestamp": "2026-01-01T12:00:00+00:00"}]
            crm.leads = [lead]
            result = crm.enforce_dial_caps(repair_misclassified=True)
            self.assertEqual(result["to_new"], 0)
            self.assertEqual(crm.snapshot()[0]["status"], "closed")

    def test_booked_prospects_are_not_moved_to_disqualified_by_the_cap(self):
        with tempfile.TemporaryDirectory() as directory:
            crm = ProspectStore(Path(directory) / "crm.json")
            lead = prospect()
            lead["status"] = "booked"
            lead["booked_at"] = "2026-01-01T12:00:00+00:00"
            lead["call_log"] = [
                {"id": "dial-1", "started_at": "2026-01-01T12:00:00+00:00"},
                {"id": "dial-2", "started_at": "2026-01-02T12:00:00+00:00"},
            ]
            crm.leads = [lead]
            self.assertEqual(crm.enforce_dial_caps()["capped"], 0)
            self.assertEqual(crm.snapshot()[0]["status"], "booked")


if __name__ == "__main__":
    unittest.main()