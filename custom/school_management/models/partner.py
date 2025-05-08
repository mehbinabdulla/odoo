# -*- coding: utf-8 -*-
from email.policy import default

from odoo import api, fields, models
from odoo.api import ValuesType, Self
from odoo.exceptions import ValidationError


class Partner(models.Model):
    """Added partner type and student id fields"""
    _inherit = 'res.partner'

    partner_type = fields.Selection(selection=[
        ('student','Student'),
        ('teacher','Teacher'),
        ('staff','Office Staff')
    ], readonly=True, string='Partner Type')
    student_reg_id = fields.Char()
    attendance_id = fields.Many2one('student.attendance', domain=[('student_id.reg_id', '=', student_reg_id), ('date', '=', fields.Date.today())])

    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)',
         "You entered Email is already exists. Please check the data is correct!"),
        ('unique_mobile', 'UNIQUE(mobile)',
         "You entered Mobile is already exists. Please check the data is correct!")
    ]

    # def _compute_attendance_id(self):
    #     for rec in self:
    #         attendance_obj = self.env['student.attendance']
    #         is_attendance = attendance_obj.search([('student_id.name', '=', rec.name), ('date', '=', fields.Date.today())]).state
    #         state = attendance_obj.state
    #         if is_attendance:
    #             if state == 'present':
    #                 rec.attendance_state = 'done'
    #             elif state == 'absent':
    #                 rec.attendance_state = 'blocked'
    #             else:
    #                 rec.attendance_state = 'normal'

