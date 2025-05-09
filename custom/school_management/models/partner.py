# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Partner(models.Model):
    """Added partner type and student id fields"""
    _inherit = 'res.partner'

    partner_type = fields.Selection(selection=[
        ('student','Student'),
        ('teacher','Teacher'),
        ('staff','Office Staff')
    ], readonly=True, string='Partner Type')
    student_reg_id = fields.Char(string='Registration ID')
    attendance_state = fields.Selection([
        ('done','Present'),
        ('blocked','Absent'),
        ('normal','Not Marked')
    ],compute='_compute_attendance_id', string='Attendance')

    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)',
         "You entered Email is already exists. Please check the data is correct!"),
        ('unique_mobile', 'UNIQUE(mobile)',
         "You entered Mobile is already exists. Please check the data is correct!")
    ]

    def _compute_attendance_id(self):
        for rec in self:
            attendance_obj = self.env['student.attendance']
            attendance = attendance_obj.search([
                ('student_id.reg_id', '=', rec.student_reg_id),
                ('att_date', '=', fields.Date.today())
            ], limit=1).state
            if attendance == 'present':
                rec.attendance_state = 'done'
            elif attendance == 'absent':
                rec.attendance_state = 'blocked'
            else:
                rec.attendance_state = 'normal'

