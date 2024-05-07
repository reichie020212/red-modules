from odoo import models, fields, api


class BaseSchool(models.AbstractModel):
    _name = "base.school"
    _description = "Base School"

    _inherit = ["base.school.system"]

    def _get_school_domain(self):
        return [
            ("school_system_id", "in", self.env.user.company_ids.ids),
        ]

    school_id = fields.Many2one(
        "school.branch",
        string="School",
        domain=_get_school_domain,
        inverse="_inverse_school_id",
        required=True,
    )

    @api.model
    def _get_onchange_school_fields(self):
        return []

    @api.onchange("school_id")
    def _inverse_school_id(self):
        for record in self:
            record.school_system_id = record.school_id.school_system_id.id

    def compute_school_function(self, field_domain, addt_domain=None):
        for rec in self:
            domain = [("id", "=", "0")]
            if rec.school_id:
                domain = [("school_id", "=", rec.school_id.id)]
            if addt_domain:
                domain.extend(addt_domain)
            setattr(rec, field_domain, domain)

    @api.onchange("school_id")
    def _onchange_school_id(self):
        for field_name in self._get_onchange_school_fields():
            setattr(self, field_name, False)
