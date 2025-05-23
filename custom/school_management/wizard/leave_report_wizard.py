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
        ('custom', 'Custom Date'),
        ('all', 'All')
    ], default='today', required=True)
    start_date = fields.Date(required=True if duration == 'custom' else False)
    end_date = fields.Date(required=True if duration == 'custom' else False)
    class_ids = fields.Many2many('school.class', readonly=False, store=True, compute='_compute_class_ids')
    student_ids = fields.Many2many('student', readonly=False, store=True, compute='_compute_student_ids')

    @api.constrains('start_date', 'end_date')
    def _check_date_difference(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError('Start date must be greater than or equal to end date!')

    @api.depends('student_ids')
    def _compute_class_ids(self):
        for record in self:
            record.class_ids = record.student_ids.class_id

    @api.depends('class_ids')
    def _compute_student_ids(self):
        for record in self:
            record.student_ids = None

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

