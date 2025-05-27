# -*- coding: utf-8 -*-
from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class Student(models.Model):
    """Student Registration"""
    _name = 'student'
    _description = 'Student'

    reg_id = fields.Char(string='Registration ID', readonly=True, default='New')
    stage = fields.Selection([('draft', 'Draft'),('registered', 'Registered')], string='Status', default='draft')
    first_name = fields.Char(string='Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    name = fields.Char(string='Full Name', store=True, compute='_compute_name')
    partner_id = fields.Many2one('res.partner', ondelete='cascade', readonly=True)
    email = fields.Char(string='Email', related='partner_id.email', store=True, required=True, readonly=False)
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
    dept_id = fields.Many2one('school.department', string='Department', required=True)
    class_id = fields.Many2one('school.class', string='Class', domain="[('department_id', '=?', dept_id)]", required=True)
    prev_dept_id = fields.Many2one('school.department', string='Previous Department')
    prev_class_id = fields.Many2one('school.class', string='Previous Class', domain="[('department_id', '=?', prev_dept_id)]")
    tc = fields.Binary(string='Upload TC')
    tc_filename = fields.Char()
    aadhaar_number = fields.Char(string='Aadhaar Number')
    school_id = fields.Many2one('res.company', string='School', default=lambda self: self.env.company)
    club_ids = fields.Many2many('school.club', string='Clubs')
    exam_ids = fields.Many2many('school.exam', compute='_compute_exam')

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
                val['reg_id'] = 'Draft'
        return super(Student, self).create(vals)


    @api.depends('first_name','last_name')
    def _compute_name(self):
        """To compute full name of the student"""
        for rec in self:
            if rec.first_name and rec.last_name:
                rec.name = f"{rec.first_name} {rec.last_name}"
            else:
                rec.name = 'New'

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

    @api.depends('class_id')
    def _compute_exam(self):
        """To display exams"""
        for rec in self:
            if rec.stage == 'registered':
                records = rec.env['school.exam'].search([('class_id', '=', rec.class_id.name), ('state', '=', 'assigned')])
                rec.exam_ids = records
            else:
                rec.exam_ids = None

    def action_register_student(self):
        """Actions need to occur when registering a student"""
        for val in self:
            val.stage = 'registered'

    def action_deregister_student(self):
        """To set the stage to draft"""
        for val in self:
            val.stage = 'draft'

    def create_user(self):
        """Automated actions need to occur when a student is registered"""
        group_ids = [
            self.env.ref('base.group_user').id,
            self.env.ref('event.group_event_registration_desk').id,
            self.env.ref('school_management.group_school_management_student').id,
        ]
        student_ids = self.search([])
        for val in student_ids:
            if val.reg_id in ['Draft', 'New']:
                val.reg_id = self.env['ir.sequence'].next_by_code('student_id_seq')
            if not val.partner_id:
                user_id = self.env['res.users'].create([{
                    'name': val.name,
                    'login': val.email,
                    'email': val.email,
                    'mobile': val.mobile,
                    'partner_type': 'student',
                    'student_reg_id': val.reg_id,
                    'student_id': val.id,
                    'street': val.communication_addr_street,
                    'street2': val.communication_addr_street2,
                    'zip': val.communication_addr_zip,
                    'city': val.communication_addr_city,
                    'state_id': val.communication_addr_state_id.id,
                    'country_id': val.communication_addr_country_id.id,
                    'groups_id': [(4, group_id) for group_id in group_ids]
                }])
                val.partner_id = user_id.partner_id.id
