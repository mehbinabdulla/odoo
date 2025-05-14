# -*- coding: utf-8 -*-
from datetime import timedelta, datetime, time
from odoo import fields, models


class Partner(models.Model):
    """Added partner type and student id fields"""
    _inherit = 'res.partner'

    partner_type = fields.Selection(selection=[
        ('student','Student'),
        ('teacher','Teacher'),
        ('staff','Office Staff')
    ], readonly=True, string='Partner Type')
    student_id = fields.Many2one('student')
    student_reg_id = fields.Char(related='student_id.reg_id', string='Registration ID')
    attendance_state = fields.Selection([
        ('done','Present'),
        ('blocked','Absent'),
        ('normal','Not Marked')
    ], compute='_compute_attendance_state', string='Attendance')

    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)',
         "You entered Email is already exists. Please check the data is correct!"),
    ]

    def create_user(self):
        partner_ids = self.search([('partner_type', 'in', ['teacher', 'staff'])])
        for val in partner_ids:
            existing_user = self.env['res.users'].search([('login', '=', val.email)], limit=1)
            if not existing_user:
                user_vals = {
                    'name': val.name,
                    'login': val.email,
                    'mobile': val.mobile,
                    'partner_id' : val.id
                }
                user_id = self.env['res.users'].create(user_vals)
                if val.partner_type == 'staff':
                    user_id.groups_id = [(4, self.env.ref('school_management.group_school_management_staff').id,)]
                else:
                    user_id.groups_id = [(4, self.env.ref('school_management.group_school_management_teacher').id,)]

    def update_attendance(self):
        """Action to execute when the update attendance scheduled action triggered"""
        print(self.search([]))
        record_ids = self.search([])
        for record in record_ids:
            today = fields.Date.today()
            now = fields.Datetime.now() + timedelta(hours=5, minutes=30)
            student_leave_ids = self.env['student.leave'].search([('student_id.reg_id', '=', record.student_reg_id)])
            record.attendance_state = 'done'
            for student_leave in student_leave_ids:
                date_from = student_leave.date_from
                date_to = student_leave.date_to
                is_half_day = student_leave.is_half_day
                half_day = student_leave.half_day
                noon = datetime.combine(date_from, time(hour=12, minute=0))

                record.attendance_state = 'blocked' if date_from <= today <= date_to else 'done'
                if date_from == date_to == today:
                    record.attendance_state = 'blocked' if (
                            (half_day == 'fn' and now <= noon) or
                            (half_day == 'an' and now >= noon) or
                            (date_from == date_to and not is_half_day)
                    ) else 'done'

    def _compute_attendance_state(self):
        """To call update_attendance action when the fields are changed"""
        self.update_attendance()