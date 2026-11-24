import unittest
import uuid
from datetime import datetime, timezone, timedelta

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


if __name__ == "__main__":
    unittest.main()