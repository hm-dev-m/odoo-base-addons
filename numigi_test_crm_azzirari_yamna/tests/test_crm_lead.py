from odoo.tests.common import TransactionCase
from datetime import datetime, timedelta


class TestCrmLead(TransactionCase):

    def setUp(
        self,
        *args,
    ):
        super(TestCrmLead, self).setUp()
        self.user = self.env["res.users"].create(
            {"name": "Test user", "login": "user", "email": "user_1@example.com"}
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
                ],
            }
        )

    def test_create_opportunity(self):
        self.opportunity = self.env["crm.lead"].create(
            {
                "name": "Test opportunity",
                "email_from": "test@example.com",
                "user_id": self.user.id,
                "description": "I need informations regarding your company",
                "medium_id": self.env.ref("utm.utm_medium_website").id,
            }
        )
        self.assertEqual(
            self.opportunity.team_id.id,
            self.env.ref("numigi_test_crm_azzirari_yamna.team_sales").id,
        )

    def _check_opportinuties_ten_day_ago(self):
        today = datetime.today()
        days_ago = today - timedelta(days=11)
        draft_opportunity = self.env["crm.lead"].create(
            {
                "name": "Test opportunity",
                "stage_id": self.env.ref("crm.stage_lead1").id,
                "create_date": days_ago,
                "team_id": self.team.id,
            }
        )
        team_members = self.team.member_ids
        notification = f"""
                           Bonjour,<br/><br/>
                           Merci de donner une suite à cette opportunité : 
                           <a href="/web#id={draft_opportunity.id}&model=crm.lead&view_type=form">{draft_opportunity.name}</a>.<br/><br/>
                           Cordialement._check_opportinuties_ten_day_ago
                       """
        for member in team_members:
            draft_opportunity.message_post(
                body=notification,
                message_type="notification",
                subtype_id=self.env.ref("mail.mt_comment").id,
                partner_ids=[member.partner_id.id],
            )
        mail = (
            self.env["mail.message"]
            .sudo()
            .search(
                [
                    ("partner_ids", "in", team_members.ids),
                ]
            )
        )
        self.assertEqual(mail.body, notification)
