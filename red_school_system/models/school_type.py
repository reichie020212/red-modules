from odoo import fields, models


class SchoolType(models.Model):
    _name = "school.type"
    _inherit = ["base.school.system"]
    _description = "School Type"

    name = fields.Char(required=True)
    description = fields.Char()

    _sql_constraints = [
        (
            "name_uniq",
            "unique(name, school_system_id)",
            "School Type name must be unique per school system!",
        ),
    ]
