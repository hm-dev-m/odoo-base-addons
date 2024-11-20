from odoo import fields, models, api
from datetime import timedelta


class CrmLead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def create(self, vals):
        default_team = self.env.ref("numigi_test_crm_azzirari_yamna.team_sales")
        vals["team_id"] = default_team.id
        return super(CrmLead, self).create(vals)

    def _check_opportinuties_ten_day_ago(self):
        ten_days_ago = fields.Date.to_date(fields.Date.today() - timedelta(days=10))
        opportinuties_to_notify = self.search(
            [
                ("create_date", "<=", ten_days_ago),
                ("stage_id", "=", self.env.ref("crm.stage_lead1").id),
            ]
        )
        for opportinuty in opportinuties_to_notify:
            if opportinuty.team_id and opportinuty.team_id.member_ids:
                opportinuty._send_notification_to_team_members()

    def _send_notification_to_team_members(self):
        notification = f"""
                    Bonjour,<br/><br/>
                    Merci de donner une suite à cette opportunité : 
                    <a href="/web#id={self.id}&model=crm.lead&view_type=form">{self.name}</a>.<br/><br/>
                    Cordialement.
                """
        for member in self.team_id.member_ids:
            member.partner_id.message_post(
                body=notification,
                subtype_xmlid="mail.mt_comment",
                partner_ids=[member.partner_id.id],
            )
