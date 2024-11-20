{
    "name": "Numigi: Test CRM",
    "version": "14.0.0.1.0",
    "author": "Yamna Azzirari",
    "licence": "AGPLv3.",
    "summary": "Personalisation du module CRM",
    "depends": [
        "crm",
        "website_crm",
    ],
    "data": [
        "data/crm_team_data.xml",
        "data/ir_cron_data.xml",
        "data/config_parameter_data.xml",
        "data/res_groups_data.xml",
        "views/crm_team_views.xml",
        "views/crm_lead_views.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}
