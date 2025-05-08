from odoo import models, fields


class StudentAttendance(models.Model):
    _name = 'student.attendance'
    _description = 'Student Attendance'

    student_id = fields.Many2one('student', 'Student')
    name = fields.Char(related='student_id.name')
    class_id = fields.Many2one('school.class', 'Class', related='student_id.class_id')
    date = fields.Date('Date', default=fields.Date.today())
    state = fields.Selection([('present', 'Present'), ('absent', 'Absent')], string='Attendance')