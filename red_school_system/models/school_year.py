from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SchoolYear(models.Model):
    _name = "school.year"
    _inherit = ["base.school.system"]
    _description = "School Year"

    name = fields.Char(compute="_compute_name")
    start_date = fields.Date(
        required=True, default=lambda self: fields.Date.context_today(self)
    )
    end_date = fields.Date(
        required=True, default=lambda self: fields.Date.context_today(self)
    )
    current_year_flag = fields.Boolean(readonly=True)

    @api.depends("start_date", "end_date")
    def _compute_name(self):
        for record in self:
            if record.start_date and record.end_date:
                record.name = f"{record.start_date.year}-{record.end_date.year}"

    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        for record in self:
            if (
                record.start_date
                and record.end_date
                and record.start_date > record.end_date
            ):
                raise ValidationError("Start date cannot be greater than end date.")
