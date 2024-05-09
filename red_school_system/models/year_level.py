from odoo import models, fields, api
from odoo.exceptions import ValidationError


class YearLevel(models.Model):
    _name = "year.level"
    _inherit = ["base.school"]
    _description = "Year Level"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    next_year_level_id = fields.Many2one("year.level", string="Next Year Level")
    prev_year_level_id = fields.Many2one("year.level", string="Previous Year Level")
    year_level_domain = fields.Char(compute="_compute_year_level_domain")

    def _get_onchange_school_fields(self):
        return super()._get_onchange_school_fields() + [
            "next_year_level_id",
            "prev_year_level_id",
        ]

    @api.depends("school_id")
    def _compute_year_level_domain(self):
        for rec in self:
            rec.compute_school_function(
                "year_level_domain", [("id", "not in", rec.ids)]
            )

    @api.constrains("next_year_level_id", "prev_year_level_id")
    def _check_year_levels(self):
        for record in self:
            if (
                record.next_year_level_id
                and record.prev_year_level_id
                and record.next_year_level_id == record.prev_year_level_id
            ):
                raise ValidationError(
                    "Next Year Level and Previous Year Level cannot be the same."
                )
