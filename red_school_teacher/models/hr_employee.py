from odoo import api, fields, models, _


class HrEmployeePrivate(models.Model):
    
    _inherit = "hr.employee"
    
    job_id = fields.Many2one('hr.job', 'Job Position', check_company=True)

    @api.onchange("job_id", "job_id.is_teaching_position")
    def _inverse_job_id(self):
        for employee in self:
            teacher_record = self.env['school.teacher'].search([("employee_id", "=", employee.id)], limit=1)
            if employee.job_id and employee.job_id.is_teaching_position and not teacher_record:
                self.env['school.teacher'].create({"employee_id": employee.id})
            elif not employee.job_id or not employee.job_id.is_teaching_position and teacher_record:
                teacher_record.unlink()
