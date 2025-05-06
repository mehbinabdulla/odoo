from datetime import datetime, timedelta, date
from email.policy import default

from odoo import models, fields, api


class Leave(models.Model):
    _name = 'student.leave'

    name = fields.Text(compute='_compute_name', default="New Leave")
    student_id = fields.Many2one('res.partner', string='Student', domain=[('partner_type', '=', 'student')], required=True)
    class_id = fields.Many2one('school.class', string='Class')
    date_from = fields.Date('Start Date', required=True, default=fields.Date.today())
    date_to = fields.Date('End Date')
    number_of_days = fields.Float('Duration (Days)', readonly=True)
    is_half_day = fields.Boolean('Is Half Day')
    half_day = fields.Selection([('fn','Forenoon'),('an','Afternoon')], default='fn', required=True)
    reason = fields.Html()

    @api.depends('student_id','date_from','date_to')
    def _compute_name(self):
        if self.student_id and self.number_of_days:
            self.name = f"{self.student_id.name}'s Leave - ({self.number_of_days} Days)"
        else:
            self.name = "New Leave"


    @api.onchange('date_from', 'date_to', 'is_half_day')
    def _onchange_number_of_days(self):
        """To compute the age from dob"""
        if self.is_half_day:
            self.date_to = self.date_from

        if isinstance(self.date_from, date) and isinstance(self.date_to, date):
            work_days = 0
            current_date = self.date_from

            while current_date <= self.date_to:
                if current_date.weekday() not in [5,6]:
                    work_days += 1
                current_date += timedelta(days=1)

            self.number_of_days = str(work_days if not self.is_half_day else 0.5)

