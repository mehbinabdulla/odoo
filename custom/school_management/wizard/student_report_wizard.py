import ast
from odoo import models, fields


class StudentReportFilterWizard(models.TransientModel):
    """Print reports from wizard"""
    _name = 'student.report.wizard'
    _description = 'Student Report Wizard'

    department_id = fields.Many2one('school.department', readonly=False, related='class_id.department_id')
    class_id = fields.Many2one('school.class', domain="[('department_id', '=?', department_id)]")

    def action_print_report(self):
        report = self.env['school.management.report']
        return report.print_student_report(self.department_id, self.class_id)
