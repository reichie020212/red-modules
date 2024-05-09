from odoo import api, fields, models, _


class Job(models.Model):

    _inherit = "hr.job"
    
    is_teaching_position = fields.Boolean(
        string='Is Teaching Position',
        help='Check this box if this job position is a teaching position.'
    )
