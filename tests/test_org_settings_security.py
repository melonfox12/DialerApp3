import tempfile
import unittest
from pathlib import Path

from features.dialer import Dialer
from features.prospects import ProspectStore


class OrgSettingsSecurityTests(unittest.TestCase):
    def test_rep_view_strips_credentials(self):
        with tempfile.TemporaryDirectory() as directory:
            env_path = Path(directory) / ".env"
            crm = ProspectStore(Path(directory) / "crm.json")
            dialer = Dialer(crm, str(env_path))
            dialer.account_user_id = "user-rep"
            dialer.account_values = {
                "TWILIO_ACCOUNT_SID": "ACsecret",
                "TWILIO_AUTH_TOKEN": "tok",
                "TWILIO_API_KEY": "SK",
                "TWILIO_API_SECRET": "sec",
                "TWILIO_TWIML_APP_SID": "AP",
                "PUBLIC_BASE_URL": "https://example.test",
            }
            dialer.org_membership = {"role": "rep", "org_id": "org-1", "can_manage_team": False}
            view = dialer.settings_state()
            self.assertTrue(view["credentials_managed_by_org"])
            self.assertFalse(view["can_edit_credentials"])
            self.assertFalse(view["has_auth_token"])
            self.assertEqual(view["account_sid"], "")

    def test_rep_cannot_overwrite_credentials_on_save(self):
        with tempfile.TemporaryDirectory() as directory:
            env_path = Path(directory) / ".env"
            crm = ProspectStore(Path(directory) / "crm.json")
            dialer = Dialer(crm, str(env_path))
            dialer.account_user_id = "user-rep"
            dialer.account_values = {
                "TWILIO_ACCOUNT_SID": "ACkeep",
                "TWILIO_AUTH_TOKEN": "keep-tok",
                "TWILIO_API_KEY": "SKkeep",
                "TWILIO_API_SECRET": "keep-sec",
                "TWILIO_TWIML_APP_SID": "APkeep",
                "PUBLIC_BASE_URL": "https://keep.test",
            }
            dialer.org_membership = {"role": "rep", "org_id": "org-1", "can_manage_team": False}
            dialer.save_settings({
                "account_sid": "ACnew",
                "auth_token": "new-tok",
                "session_goal": "22",
            })
            merged = dialer.read_settings()
            self.assertEqual(merged["TWILIO_ACCOUNT_SID"], "ACkeep")
            self.assertEqual(merged["SESSION_GOAL"], "22")