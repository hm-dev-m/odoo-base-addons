from odoo import fields, models, api, _


class Team(models.Model):
    _inherit = "crm.team"

    emails = fields.Char(
        "Emails des membres de l’équipe",
        compute="_compute_all_team_members_emails",
        store=True,
    )

    @api.model_create_multi
    def create(self, vals):
        res = super(Team, self).create(vals)
        for team in res:
            existing_member_ids = set(team.member_ids.ids)
            user = team.user_id.id
            if user and user not in existing_member_ids:
                new_member_ids = user
                team.member_ids |= team.env["res.users"].browse(new_member_ids)
        return res

    def write(self, values):
        res = super(Team, self).write(values)
        for team in self:
            existing_member_ids = set(team.member_ids.ids)
            user = team.user_id.id
            if user and user not in existing_member_ids:
                new_member_ids = user
                team.member_ids |= team.env["res.users"].browse(new_member_ids)

        return res

    @api.depends("member_ids.email")
    def _compute_all_team_members_emails(self):
        for team in self:
            all_emails = team.member_ids.mapped("email")
            team.emails = (
                ", ".join(email for email in all_emails if email) if all_emails else ""
            )
