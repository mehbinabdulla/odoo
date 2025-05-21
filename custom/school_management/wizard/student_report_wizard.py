
from odoo import api, models, fields


class StudentReportFilterWizard(models.TransientModel):
    """Print reports from wizard"""
    _name = 'student.report.wizard'
    _description = 'Student Report Wizard'

    department_ids = fields.Many2many('school.department')
    class_ids = fields.Many2many('school.class', domain="[('department_id', 'in', department_ids)]")

    def action_print_report(self):
        data = {
            'department_ids': [dept.id for dept in self.department_ids],
            'class_ids': [cls.id for cls in self.class_ids],
            'department_name': [dept.name for dept in self.department_ids],
            'class_name': [cls.name for cls in self.class_ids],
        }
        return self.env.ref('school_management.action_report_student_template').report_action(None, data)