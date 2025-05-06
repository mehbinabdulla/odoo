# -*- coding: utf-8 -*-
from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class Student(models.Model):
    """Student Registration"""
    _name = 'student'
    _description = 'Student'

    name = fields.Char(string='Registration ID', readonly=True, default='New')
    stage = fields.Selection([('draft', 'Draft'),('registered', 'Registered')], string='Status', default='draft')
    first_name = fields.Char(string='Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    email = fields.Char(string='Email', related='partner_id.email', store=True, readonly=False)
    mobile = fields.Char(string='Mobile', related='partner_id.mobile', store=True, readonly=False)
    dob = fields.Date(string='Date of Birth')
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection(selection=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], default='male', string='Gender')
    reg_date = fields.Date(string='Registration Date', default=fields.Date.today)
    photo = fields.Binary(string='Photo')
    prev_dept_id = fields.Many2one('school.department', string='Previous Department')
    prev_class_id = fields.Many2one('school.class', string='Previous Class', domain="[('department_id', '=?', prev_dept_id)]")
    tc = fields.Binary(string='Upload TC')
    tc_filename = fields.Char()
    aadhaar_number = fields.Char(string='Aadhaar Number')
    school_id = fields.Many2one('res.company', string='School', default=lambda self: self.env.company)
    club_ids = fields.Many2many('school.club', string='Clubs')

    father = fields.Char(string='Father')
    mother = fields.Char(string='Mother')

    communication_addr_street = fields.Char(related='partner_id.street', store=True, readonly=False)
    communication_addr_street2 = fields.Char(related='partner_id.street2', store=True, readonly=False)
    communication_addr_zip = fields.Char(related='partner_id.zip', store=True, readonly=False, change_default=True)
    communication_addr_city = fields.Char(related='partner_id.city', store=True, readonly=False)
    communication_addr_state_id = fields.Many2one("res.country.state", ondelete='restrict',
                               domain="[('country_id', '=?', communication_addr_country_id)]", related='partner_id.state_id', store=True, readonly=False)
    communication_addr_country_id = fields.Many2one('res.country', string="Communication Addr Country", ondelete='restrict', related='communication_addr_state_id.country_id', store=True, readonly=False)

    is_same_as_com = fields.Boolean(string='Same as Communication Address')

    permanent_addr_street = fields.Char()
    permanent_addr_street2 = fields.Char()
    permanent_addr_zip = fields.Char(change_default=True)
    permanent_addr_city = fields.Char()
    permanent_addr_state_id = fields.Many2one("res.country.state",  ondelete='restrict', domain="[('country_id', '=?', permanent_addr_country_id)]")
    permanent_addr_country_id = fields.Many2one('res.country', string="Permanent Addr Country", ondelete='restrict', related='permanent_addr_state_id.country_id', readonly=False)

    _sql_constraints = [
        ('check_age', 'CHECK(age BETWEEN 5 AND 20)',
         "You entered age is not between 5 and 20. Please check the data is correct!"),
        ('length_of_aadhaar', 'CHECK(LENGTH(aadhaar_number) = 12 OR LENGTH(aadhaar_number) = 0)',
         "You entered Aadhaar Number is not in 12 digit. Please check the data is correct!"),
        ('unique_aadhaar', 'UNIQUE(aadhaar_number)',"You entered Aadhaar Number is already exists. Please check the data is correct!"),
        ('unique_partner_id', 'UNIQUE(partner_id)',"This partner is already linked with a student. Please check the data is correct!"),
    ]

    @api.model_create_multi
    def create(self, vals):
        """To create sequence number for the record"""
        for val in vals:
            if val.get('stage') == 'draft':
                val['name'] = 'Draft'
        return super(Student, self).create(vals)

    @api.onchange('prev_dept_id')
    def _onchange_prev_dept_id(self):
        """To validate class based on department"""
        for val in self:
            val.prev_class_id = None

    @api.depends('dob')
    def _compute_age(self):
        """To compute the age from dob"""
        for val in self:
            val.age = relativedelta(fields.Date.from_string(fields.Date.today()), fields.Date.from_string(val.dob)).years


    def action_register_student(self):
        """To set the sequence and stage to registered"""
        for val in self:
            val.stage = 'registered'
            if val.name in ['Draft', 'New']:
                val.name = self.env['ir.sequence'].next_by_code('student_id_seq')

    def action_deregister_student(self):
        """To set the stage to draft"""
        for val in self:
            val.stage = 'draft'

    def action_create_partner(self):
        """To create partner"""
        self.ensure_one()
        self.partner_id = self.env["res.partner"].id if self.env["res.partner"].name == f"{self.first_name} {self.last_name}" else None
        if self.partner_id:
            raise ValidationError("This employee already has a partner.")
        return {
            'name': 'Create Partner',
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'form',
            'view_id': self.env.ref('base.view_partner_simple_form').id,
            'target': 'new',
            'context': dict(self._context, **{
                'default_student_id': self.name,
                'default_name': f"{self.first_name} {self.last_name}",
                'default_mobile': self.mobile,
                'default_email': self.email,
                'default_partner_type': 'student',
                'default_street': self.communication_addr_street,
                'default_street2': self.communication_addr_street2,
                'default_zip': self.communication_addr_zip,
                'default_city': self.communication_addr_city,
                'default_state_id': self.communication_addr_state_id,
                'default_country_id': self.communication_addr_country_id,
            })
        }
