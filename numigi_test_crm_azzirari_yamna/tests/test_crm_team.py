from odoo.tests.common import TransactionCase


class TestCrmTeam(TransactionCase):

    def setUp(
        self,
        *args,
    ):
        super(TestCrmTeam, self).setUp()
        self.user = self.env["res.users"].create(
            {"name": "Test user_1", "login": "user_1", "email": "user_1@example.com"}
        )

        self.team = self.env["crm.team"].create(
            {
                "name": "team test",
                "user_id": self.user.id,
                "member_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Test user_2",
                            "login": "user_2",
                            "email": "user_2@example.com",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "Test user_3",
                            "login": "user_3",
                            "email": "user_3@example.com",
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "name": "Test user_4",
                            "login": "user_4",
                            "email": "user_4@example.com",
                        },
                    ),
                ],
            }
        )

    def test_compute_all_team_members_emails(self):
        all_emails = self.team.emails
        self.assertEqual(
            all_emails, "user_2@example.com, user_3@example.com, user_4@example.com"
        )

    def test_create_member(self):
        self.team.member_ids |= self.user
        self.assertRecordValues(
            self.team.member_ids,
            [
                {
                    "name": "Test user_1",
                    "login": "user_1",
                    "email": "user_1@example.com",
                },
                {
                    "name": "Test user_2",
                    "login": "user_2",
                    "email": "user_2@example.com",
                },
                {
                    "name": "Test user_3",
                    "login": "user_3",
                    "email": "user_3@example.com",
                },
                {
                    "name": "Test user_4",
                    "login": "user_4",
                    "email": "user_4@example.com",
                },
            ],
        )
