
from odoo import models, fields


class ExamReportFilterWizard(models.TransientModel):
    """Print reports from wizard"""
    _name = 'exam.report.wizard'
    _description = 'Exam Report Wizard'

    class_ids = fields.Many2many('school.class')
    student_ids = fields.Many2many('student')

    def action_print_report(self):
        data = {
            'student_ids': [student.id for student in self.student_ids],
            'class_ids': [cls.id for cls in self.class_ids],
            'student_name': [student.name for student in self.student_ids],
            'class_name': [cls.name for cls in self.class_ids],
        }
        return self.env.ref('school_management.action_report_exam_template').report_action(None, data)
