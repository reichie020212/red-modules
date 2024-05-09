from odoo import models, fields, api
from odoo.exceptions import UserError


class BasePerson(models.AbstractModel):
    _name = "base.person"
    _description = "Base Person"

    # personal information
    first_name = fields.Char(required=True)
    middle_name = fields.Char()
    last_name = fields.Char(required=True)
    name = fields.Char(
        compute='_compute_name',
        store=True,
        index=True,
    )
    birth_date = fields.Date()
    place_of_birth = fields.Char()
    gender = fields.Selection(
        [
            ("male", "Male"),
            ("female", "Female"),
        ],
        required=True,
    )
    marital_status = fields.Selection(
        [
            ("single", "Single"),
            ("married", "Married"),
            ('cohabitant', 'Legal Cohabitant'),
            ('widower', 'Widower'),
            ('divorced', 'Divorced'),
        ],
        default='single',
    )
    
    mobile_phone = fields.Char(
        compute="_compute_partner_details",
        store=True,
        inverse='_inverse_partner_details',
    )
    email = fields.Char(
        compute="_compute_partner_details",
        store=True,
        inverse='_inverse_partner_details',
    )
    partner_id = fields.Many2one(
        'res.partner',
        copy=False,
    )
    user_id = fields.Many2one(
        'res.users',
        copy=False,
    )

    # address fields
    street = fields.Char()
    street2 = fields.Char()
    city = fields.Char()
    zip = fields.Char()
    house_number = fields.Char()
    barangay = fields.Char()
    country_id = fields.Many2one(
        'res.country',
        'Nationality (Country)',
        tracking=True,
    )
    state_id = fields.Many2one(
        "res.country.state",
        domain="[('country_id', '=?', country_id)]",
    )

    # parents
    mother_name = fields.Char()
    mother_phone_number = fields.Char()
    father_name = fields.Char()
    father_phone_number = fields.Char()

    # other contact
    other_emergency_contact_name = fields.Char()
    other_emergency_contact_phone_number = fields.Char()
    
    # other fields
    active = fields.Boolean("Active", readonly=True, default=True)

    @api.depends("first_name", "middle_name", "last_name")
    def _compute_name(self):
        for partner in self:
            partner.name = " ".join(
                filter(None, [partner.first_name, partner.middle_name, partner.last_name])
            )
            
    @api.depends('partner_id', 'partner_id.mobile', 'partner_id.email')
    def _compute_partner_details(self):
        for person in self:
            if person.partner_id:
                person.mobile_phone = person.partner_id.mobile
                person.email = person.partner_id.email

    def _create_partner(self):
        for person in self:
            if person.partner_id:
                raise UserError(_('Some person already have a partner id'))

        partners_to_create = [{
            'email': person.email,
            'mobile': person.mobile_phone,
            'name': person.name,
            'image_1920': person.image_1920,
            'company_id': person.company_id.id if person.company_id else False
        } for person in self]

        created_partners = self.env['res.partner'].create(partners_to_create)

        for person, partner in zip(self, created_partners):
            person.partner_id = partner

    def _inverse_partner_details(self):
        person_without_partner_id = self.env[self._name]
        for rec in self:
            if not rec.partner_id:
                person_without_partner_id += rec
            else:
                rec.partner_id.sudo().write({
                    'email': emplrecoyee.work_email,
                    'mobile': rec.mobile_phone,
                })
        if person_without_partner_id:
            person_without_partner_id.sudo()._create_partner()
