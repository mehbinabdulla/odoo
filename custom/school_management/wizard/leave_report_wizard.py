import ast
from odoo import models, fields


class LeaveReportFilterWizard(models.TransientModel):
    """Print reports from wizard"""
    _name = 'leave.report.wizard'
    _description = 'Leave Report Wizard'

    duration = fields.Selection([
        ('day', 'Today'),
        ('week', 'This Week'),
        ('month', 'This Month'),
        ('custom', 'Custom Date')
    ], default='day', required=True)
    start_date = fields.Date()
    end_date = fields.Date()
    student_id = fields.Many2one('student')
    class_id = fields.Many2one('school.class')

    def action_print_report(self):
        report = self.env['school.management.report']
        report.print_student_report()

