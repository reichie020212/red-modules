from odoo import fields, models


class SchoolStudent(models.Model):
    _name = "school.student"
    _inherit = ["base.person", "base.school"]
    _description = "School student"

