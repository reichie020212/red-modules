from odoo import models, fields


class SchoolTeacher(models.Model):
    _name = 'school.teacher'
    _inherits = {'hr.employee': 'employee_id'}

    active = fields.Boolean(default=True)
    employee_id = fields.Many2one(
        'hr.employee',
        'Employee',
        required=True,
        ondelete='cascade',
    )
