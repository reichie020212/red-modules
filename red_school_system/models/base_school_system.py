from odoo import models, fields, api


class BaseSchoolSystem(models.AbstractModel):
    _name = "base.school.system"
    _description = "Base School System"

    def _get_company_domain(self):
        return [("id", "in", self.env.user._get_company_ids())]

    def _get_default_company(self):
        ids = self.env.user._get_company_ids()
        if len(ids) == 1:
            return ids[0]

    company_id = fields.Many2one(
        "res.company",
        string="School System",
        required=True,
        domain=_get_company_domain,
        default=_get_default_company,
    )

    @api.model
    def _get_onchange_company_fields(self):
        return []

    def compute_company_function(self, field_domain, addt_domain=None):
        for rec in self:
            domain = [("id", "=", "0")]
            if rec.company_id:
                domain = [("company_id", "=", rec.company_id.id)]
            if addt_domain:
                domain.extend(addt_domain)
            setattr(rec, field_domain, domain)

    @api.onchange("company_id")
    def _onchange_company_id(self):
        for field_name in self._get_onchange_company_fields():
            setattr(self, field_name, False)
