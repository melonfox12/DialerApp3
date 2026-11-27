import unittest
import uuid
from datetime import datetime, timezone, timedelta
from unittest.mock import MagicMock, patch

from features import org


class OrgRulesTests(unittest.TestCase):
    def test_can_manage_team(self):
        self.assertTrue(org.can_manage_team("owner"))
        self.assertTrue(org.can_manage_team("manager"))
        self.assertFalse(org.can_manage_team("rep"))
        self.assertFalse(org.can_manage_team(""))

    def test_presence_is_online(self):
        now = datetime.now(timezone.utc)
        recent = (now - timedelta(seconds=30)).isoformat()
        stale = (now - timedelta(seconds=300)).isoformat()
        self.assertTrue(org.presence_is_online(recent, now=now))
        self.assertFalse(org.presence_is_online(stale, now=now))


class FakeOrgClient:
    def __init__(self):
        self.members = {}
        self.orgs = {}
        self.profiles = {}

    def seed_member(self, user_id, org_id, role="rep", status="active"):
        self.members[user_id] = {
            "id": str(uuid.uuid4()),
            "org_id": org_id,
            "user_id": user_id,
            "role": role,
            "status": status,
            "invited_email": "",
        }
        self.orgs[org_id] = {"id": org_id, "name": "Test org"}


class OrgAccessTests(unittest.TestCase):
    def setUp(self):
        self.client = FakeOrgClient()
        self.org_id = str(uuid.uuid4())
        self.manager_id = str(uuid.uuid4())
        self.rep_id = str(uuid.uuid4())
        self.other_id = str(uuid.uuid4())
        self.client.seed_member(self.manager_id, self.org_id, role="manager")
        self.client.seed_member(self.rep_id, self.org_id, role="rep")

    def test_rep_cannot_view_without_role(self):
        viewer = {"org_id": self.org_id, "role": "rep"}
        with self.assertRaises(PermissionError):
            org.assert_can_view_member(self.client, self.rep_id, viewer, self.manager_id)

    def test_manager_can_view_rep_in_org(self):
        from features import org_storage

        original = org_storage.get_active_membership
        try:
            org_storage.get_active_membership = lambda _client, user_id: self.client.members.get(user_id)
            viewer = {"org_id": self.org_id, "role": "manager"}
            result = org.assert_can_view_member(self.client, self.manager_id, viewer, self.rep_id)
            self.assertEqual(result, self.org_id)
        finally:
            org_storage.get_active_membership = original


class SyncLoginBootstrapTests(unittest.TestCase):
    def test_org_name_for_new_owner(self):
        self.assertEqual(org._org_name_for_new_owner("ada@example.com"), "Ada's team")
        self.assertEqual(org._org_name_for_new_owner("bad-email"), "Bad-Email's team")
        from shared.vocabulary import DEFAULT_ORG_NAME

        self.assertEqual(org._org_name_for_new_owner(""), DEFAULT_ORG_NAME)

    @patch("features.org.org_storage.add_member")
    @patch("features.org.org_storage.create_organization")
    @patch("features.org.org_storage.get_active_membership")
    @patch("features.org.org_storage.get_organization")
    def test_sync_user_on_login_bootstraps_owner_without_invite(
        self, mock_get_org, mock_get_member, mock_create_org, mock_add_member,
    ):
        user_id = str(uuid.uuid4())
        org_id = str(uuid.uuid4())
        member_row = {
            "org_id": org_id,
            "user_id": user_id,
            "role": "owner",
            "status": "active",
        }
        mock_get_member.side_effect = [None, None, member_row]
        mock_create_org.return_value = {"id": org_id, "name": "Ada's team"}
        mock_get_org.return_value = {"id": org_id, "name": "Ada's team"}
        client = MagicMock()
        with patch("features.org.org_storage.upsert_profile"), patch(
            "features.org.org_storage.find_invite_for_email", return_value=None,
        ):
            membership = org.sync_user_on_login(client, {"id": user_id, "email": "ada@example.com"})
        mock_create_org.assert_called_once()
        mock_add_member.assert_called_once()
        self.assertEqual(membership["org_id"], org_id)
        self.assertEqual(membership["role"], "owner")
        self.assertTrue(membership["can_manage_team"])

    def test_account_setup_payload_local_voice_flags(self):
        from shared.config import ENV_PATH

        class Runtime:
            client = None
            storage_name = "local JSON files"

        class Dialer:
            account_user_id = ""
            account_values = {}
            env_path = ENV_PATH
            org_membership = {
                "org_id": "",
                "org_name": "",
                "role": "",
                "status": "",
                "can_manage_team": False,
            }

        payload = org.account_setup_payload(Runtime(), Dialer())
        self.assertTrue(payload["signed_in"])
        self.assertIn("twilio_voice", payload["next_steps"])


if __name__ == "__main__":
    unittest.main()