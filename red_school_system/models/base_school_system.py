from odoo import models, fields, api


class BaseSchoolSystem(models.AbstractModel):
    _name = "base.school.system"
    _description = "Base School System"

    def _get_school_system_domain(self):
        return [("id", "in", self.env.user._get_company_ids())]

    def _get_default_school_system(self):
        ids = self.env.user._get_company_ids()
        if len(ids) == 1:
            return ids[0]

    def _check_readonly(self):
        ids = self.user._get_company_ids()
        
        if len(ids) == 1:
            return True
        return False

    school_system_id = fields.Many2one(
        "res.company",
        string="School System",
        required=True,
        readonly=_check_readonly,
        domain=_get_school_system_domain,
        default=_get_default_school_system,
    )

    @api.model
    def _get_onchange_school_system_fields(self):
        return []

    def compute_school_system_function(self, field_domain, addt_domain=None):
        for rec in self:
            domain = [("id", "=", "0")]
            if rec.school_system_id:
                domain = [("school_system_id", "=", rec.school_system_id.id)]
            if addt_domain:
                domain.extend(addt_domain)
            setattr(rec, field_domain, domain)

    @api.onchange("school_system_id")
    def _onchange_school_system_id(self):
        for field_name in self._get_onchange_school_system_fields():
            setattr(self, field_name, False)
