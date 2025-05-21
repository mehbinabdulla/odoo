from odoo import models, fields, api
from odoo.exceptions import ValidationError


class LeaveReportFilterWizard(models.TransientModel):
    """Print reports from wizard"""
    _name = 'leave.report.wizard'
    _description = 'Leave Report Wizard'

    duration = fields.Selection([
        ('today', 'Today'),
        ('week', 'This Week'),
        ('month', 'This Month'),
        ('custom', 'Custom Date')
    ], default='today', required=True)
    start_date = fields.Date(required=True if duration == 'custom' else False)
    end_date = fields.Date(required=True if duration == 'custom' else False)
    class_ids = fields.Many2many('school.class')
    student_ids = fields.Many2many('student', domain="[('class_id', 'in', class_ids)]")

    @api.constrains('start_date', 'end_date')
    def _check_date_difference(self):
        if self.start_date > self.end_date:
            raise ValidationError('Start date must be greater than or equal to end date!')

    def action_print_report(self):
        data = {
            'duration': self.duration,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'student_ids': [student.id for student in self.student_ids],
            'class_ids': [cls.id for cls in self.class_ids],
            'student_name': [student.name for student in self.student_ids],
            'class_name': [cls.name for cls in self.class_ids],
        }
        return self.env.ref('school_management.action_report_leave_template').report_action(None, data)

