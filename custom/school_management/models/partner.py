# -*- coding: utf-8 -*-
from datetime import timedelta, datetime, time
from odoo import api, fields, models


class Partner(models.Model):
    """Added partner type and student id fields"""
    _inherit = 'res.partner'

    partner_type = fields.Selection(selection=[
        ('student','Student'),
        ('teacher','Teacher'),
        ('staff','Office Staff')
    ], readonly=True, string='Partner Type')
    student_id = fields.Many2one('student', string='Registration ID')
    student_reg_id = fields.Char(related='student_id.reg_id', string='Registration ID')
    attendance_state = fields.Selection([
        ('done','Present'),
        ('blocked','Absent'),
        ('normal','Not Marked')
    ], compute='_compute_attendance_state', string='Attendance')

    _sql_constraints = [
        ('unique_email', 'UNIQUE(email)',
         "You entered Email is already exists. Please check the data is correct!"),
        ('unique_mobile', 'UNIQUE(mobile)',
         "You entered Mobile is already exists. Please check the data is correct!")
    ]

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
                print(f"{record}  {student_leave}")

    def _compute_attendance_state(self):
        """To call update_attendance action when the fields are changed"""
        self.update_attendance()