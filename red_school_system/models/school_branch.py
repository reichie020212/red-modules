from odoo import models, fields, api


class SchoolBranch(models.Model):
    _name = "school.branch"
    _inherit = ["base.school.system"]
    _description = "School"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    school_type = fields.Many2one("school.type", string="School Type")
    school_type_domain = fields.Char(compute="_compute_school_type_domain")

    def _get_onchange_company_fields(self):
        return super()._get_onchange_company_fields() + ["school_type"]

    @api.depends("company_id")
    def _compute_school_type_domain(self):
        self.compute_company_function("school_type_domain")
