from datetime import timedelta, date
from odoo import models, fields, api


class StudentLeave(models.Model):
    """Mark leave of students"""
    _name = 'student.leave'
    _description = 'Student leave'

    name = fields.Text(compute='_compute_name', default="New Leave")
    student_id = fields.Many2one('student', string='Student', ondelete='cascade', required=True)
    class_id = fields.Many2one('school.class', string='Class')
    date_from = fields.Date('Start Date', required=True, default=fields.Date.today())
    date_to = fields.Date('End Date')
    number_of_days = fields.Float('Duration (Days)', compute="_compute_number_of_days")
    is_half_day = fields.Boolean('Is Half Day')
    half_day = fields.Selection([('fn','Forenoon'),('an','Afternoon')], default='fn', required=True)
    reason = fields.Html()

    @api.depends('student_id','date_from','date_to', 'is_half_day')
    def _compute_name(self):
        """To compute the title of the record"""
        for rec in self:
            rec.name = f"{rec.student_id.name if rec.student_id else "Student"}'s Leave - ({rec.number_of_days} Days)"


    @api.depends('date_from', 'date_to', 'is_half_day')
    def _compute_number_of_days(self):
        """To compute the duration of leave"""
        for rec in self:
            if rec.is_half_day:
                rec.date_to = rec.date_from

            if isinstance(rec.date_from, date) and isinstance(rec.date_to, date):
                work_days = 0
                current_date = rec.date_from

                while current_date <= rec.date_to:
                    if current_date.weekday() not in [5,6]:
                        work_days += 1
                    current_date += timedelta(days=1)

                rec.number_of_days = work_days if not rec.is_half_day else 0.5
            else:
                rec.number_of_days = 0

