from odoo import models, fields, api


class School(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "base.school.system"]
    _description = "School"

    code = fields.Char(required=True)
    is_school = fields.Boolean()
    school_type = fields.Many2one("school.type", string="School Type")
    school_type_domain = fields.Char(compute="_compute_school_type_domain")

    def _get_onchange_school_system_fields(self):
        return super()._get_onchange_school_system_fields() + ["school_type"]

    @api.depends("school_system_id")
    def _compute_school_type_domain(self):
        self.compute_school_system_function("school_type_domain")
